#!/usr/bin/env python3
"""저장소의 공통 지침, 스킬, 선언된 설정만 동기화한다."""

from __future__ import annotations

import argparse
import datetime as dt
import math
import os
from pathlib import Path
import stat
import sys
import tempfile
import tomllib
import uuid
from dataclasses import dataclass, field
from typing import Any, Iterable, TextIO


class SyncError(Exception):
    """변경 전에 사용자에게 알려야 하는 동기화 오류."""


@dataclass
class Change:
    path: Path
    boundary: Path
    content: bytes
    previous: bytes | None
    backup_relative: Path


@dataclass
class Plan:
    changes: list[Change] = field(default_factory=list)
    messages: list[str] = field(default_factory=list)
    watched: dict[Path, tuple[Path, bytes | None]] = field(default_factory=dict)
    boundaries: set[Path] = field(default_factory=set)


def absolute(path: str | Path) -> Path:
    # resolve()를 먼저 쓰면 심볼릭 링크 경유 여부를 잃으므로 절대 경로만 만든다.
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def inside(path: Path, boundary: Path) -> bool:
    try:
        return os.path.commonpath((str(path), str(boundary))) == str(boundary)
    except ValueError:
        return False


def is_link(info: os.stat_result) -> bool:
    # Windows의 junction도 심볼릭 링크와 같은 경계 이탈 위험으로 처리한다.
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def check_path(path: Path, boundary: Path, expected: str) -> None:
    """기존 조상 전체와 끝 경로의 형식을 변경 전에 확인한다."""
    if not inside(path, boundary):
        raise SyncError(f"Path escapes its managed root: {path}")
    chain = list(reversed(path.parents)) + [path]
    for current in chain:
        try:
            info = current.lstat()
        except FileNotFoundError:
            continue
        if is_link(info):
            raise SyncError(f"Linked or reparse paths are not supported: {current}")
        if current != path and not stat.S_ISDIR(info.st_mode):
            raise SyncError(f"Expected a directory: {current}")
        if current == path:
            valid = stat.S_ISDIR(info.st_mode) if expected == "dir" else stat.S_ISREG(info.st_mode)
            if not valid:
                raise SyncError(f"Expected a {expected}: {current}")


def observe(plan: Plan, path: Path, boundary: Path, required: bool = False) -> bytes | None:
    check_path(path, boundary, "file")
    try:
        content = path.read_bytes()
    except FileNotFoundError:
        if required:
            raise SyncError(f"Required source file is missing: {path}") from None
        content = None
    plan.watched[path] = (boundary, content)
    return content


def source_files(directory: Path, boundary: Path) -> Iterable[Path]:
    """관리 스킬 안의 일반 파일만 열거하고 링크는 허용하지 않는다."""
    check_path(directory, boundary, "dir")
    for child in sorted(directory.iterdir(), key=lambda p: p.name.casefold()):
        info = child.lstat()
        if is_link(info):
            raise SyncError(f"Linked or reparse paths are not supported: {child}")
        if stat.S_ISDIR(info.st_mode):
            yield from source_files(child, boundary)
        elif stat.S_ISREG(info.st_mode):
            check_path(child, boundary, "file")
            yield child
        else:
            raise SyncError(f"Unsupported source file type: {child}")


def parse_toml(content: bytes | None, path: Path) -> dict[str, Any]:
    if content is None:
        return {}
    try:
        return tomllib.loads(content.decode("utf-8-sig"))
    except (UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise SyncError(f"Invalid TOML in {path}: {exc}") from None


def leaves(data: dict[str, Any], prefix: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    for key, value in data.items():
        path = (*prefix, key)
        if isinstance(value, dict):
            yield from leaves(value, path)
        else:
            yield path, value


MISSING = object()


def lookup(data: dict[str, Any], path: tuple[str, ...]) -> Any:
    node: Any = data
    for key in path[:-1]:
        if key not in node:
            return MISSING
        node = node[key]
        if not isinstance(node, dict):
            raise SyncError(f"TOML table conflicts with a local value: {'.'.join(path)}")
    result = node.get(path[-1], MISSING)
    if isinstance(result, dict):
        raise SyncError(f"TOML value conflicts with a local table: {'.'.join(path)}")
    return result


def equal(left: Any, right: Any) -> bool:
    # TOML에서 true와 1은 서로 다른 값이며 nan도 재설치를 일으키지 않는다.
    if type(left) is not type(right):
        return False
    if isinstance(left, float) and math.isnan(left) and math.isnan(right):
        return True
    if isinstance(left, list):
        return len(left) == len(right) and all(equal(a, b) for a, b in zip(left, right))
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(equal(left[k], right[k]) for k in left)
    return left == right


def update_toml(original: bytes | None, updates: list[tuple[tuple[str, ...], Any]]) -> bytes:
    try:
        import tomlkit
    except ImportError:
        raise SyncError(
            "Shared TOML settings require tomlkit. Install bootstrap/requirements.txt with Python 3.11+."
        ) from None
    try:
        document = tomlkit.parse((original or b"").decode("utf-8-sig"))
        for path, value in updates:
            node = document
            for key in path[:-1]:
                if key not in node:
                    node[key] = tomlkit.table()
                node = node[key]
            node[path[-1]] = value
        return tomlkit.dumps(document).encode("utf-8")
    except (tomlkit.exceptions.TOMLKitError, TypeError, ValueError) as exc:
        raise SyncError(f"Cannot preserve and update TOML settings: {exc}") from None


def make_plan(repo: Path, home: Path, codex_home: Path, mode: str) -> Plan:
    repo, home, codex_home = absolute(repo), absolute(home), absolute(codex_home)
    skills_home = home / ".agents" / "skills"
    backup_home = home / ".gpt_set" / "backups"
    plan = Plan(boundaries={repo, home, codex_home, skills_home, backup_home})
    for root in plan.boundaries:
        check_path(root, root, "dir")
    if not repo.is_dir():
        raise SyncError(f"Repository directory is missing: {repo}")
    for destination in (codex_home, skills_home, backup_home):
        if inside(destination, repo) or inside(repo, destination):
            raise SyncError(f"Repository and managed destination must not overlap: {destination}")

    # 공통 지침이 참조하는 한국어 문서도 같은 Codex 홈에 설치하고 회수한다.
    mappings = [
        (repo / "home" / "codex" / "AGENTS.template.md", codex_home / "AGENTS.md", codex_home, Path("codex/AGENTS.md")),
        (repo / "home" / "codex" / "korean_style.md", codex_home / "korean_style.md", codex_home, Path("codex/korean_style.md")),
    ]
    skills_source = repo / "home" / "skills"
    check_path(skills_source, repo, "dir")
    if not skills_source.is_dir():
        raise SyncError(f"Skills source directory is missing: {skills_source}")
    for skill in sorted(skills_source.iterdir(), key=lambda p: p.name.casefold()):
        info = skill.lstat()
        if is_link(info):
            raise SyncError(f"Linked or reparse paths are not supported: {skill}")
        if not stat.S_ISDIR(info.st_mode) or not (skill / "SKILL.md").exists():
            continue
        check_path(skill / "SKILL.md", repo, "file")
        for source in source_files(skill, repo):
            relative = source.relative_to(skills_source)
            mappings.append((source, skills_home / relative, skills_home, Path("skills") / relative))

    for source, live, live_boundary, backup_relative in mappings:
        original = observe(plan, source, repo, required=True)
        installed = observe(plan, live, live_boundary)
        label = str(source.relative_to(repo)).replace("\\", "/")
        if installed == original:
            plan.messages.append(f"SAME {label}")
        elif installed is None:
            plan.messages.append(f"MISSING {label}")
        else:
            plan.messages.append(f"DIFFERENT {label}")
        if mode == "install" and installed != original:
            plan.changes.append(Change(live, live_boundary, original, installed, backup_relative))
        elif mode == "pull" and installed is not None and installed != original:
            plan.changes.append(Change(source, repo, installed, original, Path("repo-source") / source.relative_to(repo)))

    shared_path = repo / "home" / "codex" / "config.shared.toml"
    live_path = codex_home / "config.toml"
    shared_content = observe(plan, shared_path, repo, required=True)
    live_content = observe(plan, live_path, codex_home)
    shared = parse_toml(shared_content, shared_path)
    live = parse_toml(live_content, live_path)
    updates: list[tuple[tuple[str, ...], Any]] = []
    managed = list(leaves(shared))
    if not managed:
        plan.messages.append("NO SHARED SETTINGS home/codex/config.shared.toml")
    for key_path, desired in managed:
        current = lookup(live, key_path)
        label = "config:" + ".".join(key_path)
        if current is MISSING:
            plan.messages.append(f"MISSING {label}")
            if mode == "install":
                updates.append((key_path, desired))
        elif equal(desired, current):
            plan.messages.append(f"SAME {label}")
        else:
            plan.messages.append(f"DIFFERENT {label}")
            if mode == "install":
                updates.append((key_path, desired))
            elif mode == "pull":
                updates.append((key_path, current))
    if updates:
        if mode == "install":
            plan.changes.append(Change(live_path, codex_home, update_toml(live_content, updates), live_content, Path("codex/config.toml")))
        elif mode == "pull":
            plan.changes.append(Change(shared_path, repo, update_toml(shared_content, updates), shared_content, Path("repo-source/home/codex/config.shared.toml")))
    # 백업 경로의 형식 충돌도 실제 파일을 변경하기 전에 확인한다.
    for change in plan.changes:
        check_path(change.path, change.boundary, "file")
    return plan


def atomic_write(change: Change) -> None:
    check_path(change.path, change.boundary, "file")
    change.path.parent.mkdir(parents=True, exist_ok=True)
    check_path(change.path, change.boundary, "file")
    prior_mode = stat.S_IMODE(change.path.stat().st_mode) if change.path.exists() else None
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{change.path.name}.gpt-set-", dir=change.path.parent)
    temporary = Path(temporary_name)
    with os.fdopen(descriptor, "wb") as output:
        output.write(change.content)
        output.flush()
        os.fsync(output.fileno())
    if prior_mode is not None:
        temporary.chmod(prior_mode)
    # 실패 시 임시 파일을 남겨 복구할 수 있도록 하고 삭제 작업은 하지 않는다.
    os.replace(temporary, change.path)


def apply_plan(plan: Plan, home: Path, output: TextIO) -> None:
    """전체 입력을 재확인하고 덮어쓰기 전 원본을 별도 위치에 보관한다."""
    for root in plan.boundaries:
        check_path(root, root, "dir")
    for path, (boundary, previous) in plan.watched.items():
        check_path(path, boundary, "file")
        current = path.read_bytes() if path.exists() else None
        if current != previous:
            raise SyncError(f"File changed during preflight; run synchronization again: {path}")
    overwrite = [change for change in plan.changes if change.previous is not None]
    if overwrite:
        backup_home = absolute(home) / ".gpt_set" / "backups"
        identifier = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex[:8]
        backup_run = backup_home / identifier
        check_path(backup_run, backup_home, "dir")
        for change in overwrite:
            backup = backup_run / change.backup_relative
            check_path(backup, backup_home, "file")
        for change in overwrite:
            backup = backup_run / change.backup_relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            check_path(backup, backup_home, "file")
            with backup.open("xb") as saved:
                saved.write(change.previous)
        print(f"Backup: {backup_run}", file=output)
    for change in plan.changes:
        atomic_write(change)
        print(f"UPDATED {change.path}", file=output)


def run(repo: Path, home: Path, codex_home: Path, mode: str, output: TextIO = sys.stdout) -> int:
    plan = make_plan(repo, home, codex_home, mode)
    print(f"Repository: {absolute(repo)}", file=output)
    print(f"User home: {absolute(home)}", file=output)
    print(f"Codex home: {absolute(codex_home)}", file=output)
    print(f"Skills: {absolute(home) / '.agents' / 'skills'}", file=output)
    for message in plan.messages:
        print(message, file=output)
    if mode == "status":
        print("Status only; no files were changed.", file=output)
    else:
        apply_plan(plan, home, output)
        print(f"Complete: {len(plan.changes)} file(s) updated.", file=output)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Synchronize personal Codex instructions, skills, and declared settings.")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--status", action="store_true", help="Show managed differences without writing files.")
    actions.add_argument("--pull", action="store_true", help="Copy existing managed files and declared settings back to the repository.")
    parser.add_argument("--home", type=Path, default=Path.home(), help="User home for skills and backups (default: current user home).")
    parser.add_argument("--codex-home", type=Path, help="Codex home; overrides CODEX_HOME and HOME/.codex.")
    arguments = parser.parse_args(argv)
    home = absolute(arguments.home)
    codex_home = absolute(arguments.codex_home or os.environ.get("CODEX_HOME") or home / ".codex")
    repo = Path(__file__).absolute().parent.parent
    mode = "status" if arguments.status else "pull" if arguments.pull else "install"
    try:
        return run(repo, home, codex_home, mode)
    except (SyncError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
