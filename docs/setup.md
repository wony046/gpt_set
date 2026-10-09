# 설치와 수정 방법

`gpt_set`의 `home/` 폴더가 공통 지침과 스킬의 원본입니다. 이 문서의 명령은 `gpt_set` 폴더로 이동한 상태에서 실행합니다.

## 1. Python 확인

Python 3.11 이상을 준비합니다. 설치와 빈 공유 설정은 Python 표준 라이브러리로 동작합니다.

**Windows · PowerShell**

```powershell
py -3 --version
```

**macOS·Linux · Bash**

```bash
python3 --version
```

Windows에서 Python 실행 파일을 직접 지정할 수도 있습니다. 아래 경로는 실제 Python 설치 경로로 바꾸세요.

**Windows · PowerShell**

```powershell
.\bootstrap\sync-gpt.ps1 -Status -PythonExecutable 'C:\path\to\python.exe'
```

스크립트는 Python이나 필요한 패키지를 자동으로 내려받지 않습니다.

## 2. 설치 대상과 차이 확인

**Windows · PowerShell**

```powershell
.\bootstrap\sync-gpt.ps1 -Status
```

**macOS·Linux · Bash**

```bash
bash bootstrap/sync-gpt.sh --status
```

차이 확인은 완전히 읽기 전용입니다. 대상 폴더가 없어도 만들지 않으며, 백업도 생성하지 않습니다. 출력에서 공통 지침, 스킬 파일, 공유 설정의 차이와 실제 대상 경로를 확인하세요. 스크립트 상태 메시지는 영어로 표시됩니다.

기본 경로는 다음과 같습니다.

| 항목 | 기본 위치 |
|---|---|
| 공통 지침 | `~/.codex/AGENTS.md` |
| 일반 한국어 작성 지침 | `~/.codex/korean_style.md` |
| 개인 설정 | `~/.codex/config.toml` |
| 사용자 스킬 | `~/.agents/skills/` |
| 변경 전 백업 | `~/.gpt_set/backups/` |

`~`는 현재 사용자의 홈 폴더입니다. Codex 홈은 다음 순서로 결정합니다.

1. `-CodexHome` 또는 `--codex-home`으로 명시한 경로
2. 환경 변수 `CODEX_HOME`
3. `<사용자 홈>/.codex`

사용자 홈은 `-UserHome` 또는 `--home`으로 지정할 수 있습니다. 스킬과 백업 경로는 사용자 홈을 기준으로 합니다. Codex 홈만 바꾸면 스킬 위치는 바뀌지 않습니다.

별도 Codex 프로필을 사용할 때의 예시입니다. 지정한 폴더가 실제 설치 대상이 됩니다.

**Windows · PowerShell**

```powershell
.\bootstrap\sync-gpt.ps1 -Status -CodexHome "$env:USERPROFILE\.codex-personal"
```

**macOS·Linux · Bash**

```bash
bash bootstrap/sync-gpt.sh --status --codex-home "$HOME/.codex-personal"
```

설치할 때도 같은 옵션을 사용하세요. Codex가 그 프로필을 사용하도록 실행 환경의 `CODEX_HOME`도 맞춰야 합니다. 설치 스크립트에 경로를 지정하는 것만으로 Codex의 실행 프로필이 바뀌지는 않습니다. [공식 AGENTS.md 안내](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

## 3. 설치

인자 없이 실행하면 대상 경로와 차이를 표로 보여 준 뒤 동기화 방향을 묻습니다. 메뉴에서 `Push`를 고르면 설치합니다.

**Windows · PowerShell**

```powershell
.\bootstrap\sync-gpt.ps1
```

**macOS·Linux · Bash**

```bash
bash bootstrap/sync-gpt.sh
```

| 키 | 동작 |
|---|---|
| `↑` / `↓` | 항목 이동 |
| `Enter` | 선택한 항목 실행 |
| `1` ~ `3` | 해당 번호의 항목을 바로 실행 |
| `Esc` | 변경 없이 종료 |

키 입력을 받을 수 없는 환경(파이프, CI 등)에서는 메뉴를 띄우지 않고 상태 표만 출력합니다. 이런 환경이나 스크립트에서 설치하려면 `-Push`(`--push`)를 명시합니다.

공통 지침은 원본 `AGENTS.template.md`를 설치본 `AGENTS.md`로 복사합니다. `korean_style.md`도 같은 Codex 홈에 복사합니다. 별도 프로필을 지정해도 두 파일은 함께 설치됩니다. 스킬은 원본에 있는 파일만 해당 사용자 스킬 폴더로 복사합니다.

`korean_style.md`는 파일 이름만으로 자동 로드되지 않습니다. `AGENTS.md`의 지시에 따라 한국어 설명이나 문서 본문을 작성하기 전에 읽습니다. 이번 세션에서 이미 읽었고 내용이 바뀌지 않았다면 다시 읽지 않습니다. 보고서의 구체적인 문체와 종결형 및 Word 서식은 보고서 스킬에서 확인합니다.

기존 관리 대상 파일의 내용이 바뀌면 변경 전 파일을 백업합니다. 같은 내용을 재설치하면 쓰기와 백업을 생략합니다. 원본에서 사라진 파일이나 설치본에만 있는 파일은 자동 삭제하지 않습니다.

초기 `config.shared.toml`은 주석만 있으므로 `config.toml`을 수정하거나 새로 만들지 않습니다. 공유 설정을 추가했다면 해당 항목만 병합하며, 다른 로컬 설정은 유지합니다. [공식 설정 안내](https://learn.chatgpt.com/docs/config-file/config-basic)

## 4. Codex에서 확인

설치가 끝나면 새 Codex 세션에서 다음 내용을 확인합니다.

1. “현재 적용 중인 공통 지침과 한국어 문체 규칙을 요약해줘.”라고 요청합니다.
2. 보고서 작업에서 “`$eec-lab-report`를 사용해 실험 보고서 작성 규칙을 확인해줘.”라고 요청합니다.
3. `AGENTS.md`가 같은 Codex 홈의 `korean_style.md`를 읽도록 연결되어 있고 한국어 작성 전에 실제로 읽었는지 확인합니다.
4. 일반 한국어 규칙은 `korean_style.md`에, 전전회 보고서의 구체적인 문체와 Word 서식은 스킬에 있는지 확인합니다.

Codex는 새 실행이나 세션에서 지침을 읽습니다. 스킬 변경은 자동 감지하지만 표시되지 않으면 Codex를 다시 시작하세요. [공식 공통 지침 안내](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [공식 스킬 안내](https://learn.chatgpt.com/docs/build-skills)

## 원본 수정과 변경 회수

원본을 직접 수정하는 방법이 기본입니다.

| 바꾸려는 내용 | 수정할 파일 |
|---|---|
| 공통 작업 규칙과 한국어 지침을 읽는 조건 | `home/codex/AGENTS.template.md` |
| 일반 한국어 문체와 원문 예시 | `home/codex/korean_style.md` |
| 여러 컴퓨터에서 공유할 Codex 설정 | `home/codex/config.shared.toml` |
| 전전회 보고서 절차 | `home/skills/eec-lab-report/SKILL.md` |
| 전전회 보고서 문체와 서식 세부 규칙 | `home/skills/eec-lab-report/references/report-guidelines.md` |
| 스킬 표시 이름과 호출 문구 | `home/skills/eec-lab-report/agents/openai.yaml` |

원본을 수정한 뒤 차이를 확인하고 다시 설치합니다. 설치본을 먼저 수정했다면 다음 명령으로 원본에 회수할 수 있습니다.

**Windows · PowerShell**

```powershell
.\bootstrap\sync-gpt.ps1 -Status
.\bootstrap\sync-gpt.ps1 -Pull
```

**macOS·Linux · Bash**

```bash
bash bootstrap/sync-gpt.sh --status
bash bootstrap/sync-gpt.sh --pull
```

회수는 원본에 이미 있는 파일과 공유 설정 항목만 대상으로 합니다. 원본과 설치본을 모두 수정했다면 회수 전에 어느 쪽을 유지할지 내용을 비교하세요. 회수는 충돌 내용을 자동으로 합치는 기능이 아닙니다.

새 스킬은 `home/skills/<스킬 이름>/SKILL.md`와 필요한 자료를 원본에 추가한 뒤 설치합니다. 설치본에만 있는 새 파일을 관리하려면 직접 원본에 넣어야 합니다. 설치본에서 삭제된 파일을 회수해 원본에서 자동 삭제하지 않습니다.

## 공유 설정을 추가할 때의 선택 의존성

`config.shared.toml`에 값이 있는 설정을 작성했다면 `tomlkit`이 필요합니다. `bootstrap/requirements.txt`는 `tomlkit>=0.13,<1` 범위를 지정합니다. TOML 문서 구조를 읽어 관리 항목만 병합하고, 관련 없는 로컬 내용을 보존하기 위한 의존성입니다.

아래 예시는 저장소 전용 가상환경에 패키지를 설치합니다. 기존 Python 환경을 바꾸지 않고 의존성을 분리하는 방법입니다. 가상환경 생성과 패키지 설치는 사용자가 직접 실행합니다.

**Windows · PowerShell**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\bootstrap\requirements.txt
.\bootstrap\sync-gpt.ps1 -Status -PythonExecutable .\.venv\Scripts\python.exe
.\bootstrap\sync-gpt.ps1 -Push -PythonExecutable .\.venv\Scripts\python.exe
```

**macOS·Linux · Bash**

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r bootstrap/requirements.txt
bash bootstrap/sync-gpt.sh --status
bash bootstrap/sync-gpt.sh --push
deactivate
```

이미 사용하는 Python 환경에 설치하려면 해당 환경의 Python으로 `-m pip install -r bootstrap/requirements.txt`를 실행하세요. 패키지를 설치한 Python과 동기화 도구가 사용하는 Python이 같아야 합니다.

공유 항목은 `config.shared.toml`에 명시된 키로 정합니다. 로컬 `config.toml` 전체를 복사하거나 계정 정보, 세션 기록을 추가하지 마세요. 모델이나 운영체제별 절대 경로를 공유할 필요가 없다면 원본에 넣지 않습니다.

일반 테이블은 선언한 하위 키만 관리합니다. 배열과 배열 테이블은 해당 키의 전체 값으로 교체하거나 회수합니다. 예를 들어 `[[skills.config]]`에 컴퓨터별 경로가 섞여 있다면 그 배열을 공유 대상으로 지정하지 않습니다.

## 백업과 새 컴퓨터

백업은 `<사용자 홈>/.gpt_set/backups/` 아래에 보관합니다. 필요할 때 파일 내용과 대상 경로를 확인한 뒤 해당 백업 파일을 원래 위치로 직접 복사할 수 있습니다. 자동 복원 명령은 제공하지 않습니다.

새 컴퓨터에는 이 폴더의 원본을 옮기거나, 향후 실제로 등록한 Git 원격 저장소에서 가져온 뒤 위 설치 순서를 반복합니다. 현재 폴더 구성 단계에서는 GitHub 원격 저장소의 존재를 전제로 하지 않습니다. 로그인과 컴퓨터별 설정은 새 컴퓨터에서 따로 준비합니다.

## 옵션 요약

| PowerShell | Bash | 의미 |
|---|---|---|
| 없음 | 없음 | 차이 표 출력 후 Push, Pull, Exit 중 선택 |
| `-Status` | `--status` | 차이와 대상 경로 확인, 쓰기 없음 |
| `-Push` | `--push` | 묻지 않고 원본을 설치본으로 반영 |
| `-Pull` | `--pull` | 설치본 변경을 기존 원본에 회수 |
| `-UserHome <경로>` | `--home <경로>` | 사용자 홈 기준 변경 |
| `-CodexHome <경로>` | `--codex-home <경로>` | Codex 홈 직접 지정 |
| `-PythonExecutable <경로>` | 가상환경 활성화 후 실행 | Python 선택 |
| `-Help` | `--help` | 도움말 표시 |

`Status`와 `Pull`은 각각 별도로 실행합니다.
