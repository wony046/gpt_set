# gpt_set

여러 컴퓨터에서 GPT의 개인 공통 지침, 작업별 스킬, 공유 설정을 유지하기 위한 저장소입니다.

`home/`의 파일을 원본으로 관리합니다.
`bootstrap/`의 동기화 도구로 설치본과 비교하거나 변경 사항을 적용합니다.
일반 한국어 답변 규칙은 `korean_style.md`에 두고 공통 지침에서 읽도록 연결합니다.
전기전자회로 실험 보고서의 작성 절차와 Word 서식은 `eec-lab-report` 스킬에서 관리합니다.

## 폴더 구성

```text
gpt_set/
├── README.md
├── .gitattributes
├── .gitignore
├── home/
│   ├── codex/
│   │   ├── AGENTS.template.md
│   │   ├── korean_style.md
│   │   └── config.shared.toml
│   └── skills/
│       └── eec-lab-report/
│           ├── SKILL.md
│           ├── references/
│           │   └── report-guidelines.md
│           └── agents/
│               └── openai.yaml
├── bootstrap/
│   ├── sync-gpt.ps1
│   ├── sync-gpt.sh
│   ├── sync_gpt.py
│   └── requirements.txt
└── docs/
    ├── setup.md
    └── troubleshooting.md
```

`AGENTS.template.md`는 저장소의 원본 이름이며, 설치할 때 `AGENTS.md`로 복사합니다. `korean_style.md`는 같은 `.codex`에 함께 복사합니다.
- 기본적인 한국어 지침의 원문과 예시는 이 파일에서 관리합니다.

새 스킬은 `home/skills/<스킬 이름>/`에 추가합니다.

## 설치 대상

| 원본 | 설치 위치 | 동작 |
|---|---|---|
| `home/codex/AGENTS.template.md` | `<Codex 홈>/AGENTS.md` | 공통 지침 설치 |
| `home/codex/korean_style.md` | `<Codex 홈>/korean_style.md` | 일반 한국어 작성 지침 설치 |
| `home/codex/config.shared.toml` | `<Codex 홈>/config.toml` | 원본에 적힌 공유 설정 항목만 병합 |
| `home/skills/<스킬 이름>/` | `<사용자 홈>/.agents/skills/<스킬 이름>/` | 원본에 있는 스킬 파일 설치 |

Codex 홈은 명시한 `-CodexHome` 또는 `--codex-home`, 환경 변수 `CODEX_HOME`, `<사용자 홈>/.codex` 순서로 결정합니다. 사용자 홈은 기본적으로 현재 사용자의 홈 폴더이며 `-UserHome` 또는 `--home`으로 바꿀 수 있습니다.

초기 `config.shared.toml`에는 안내 주석만 들어 있습니다. 공유 설정을 직접 추가하기 전에는 기존 `config.toml`을 만들거나 수정하지 마세요. 모델, 개인 경로, 계정 정보 등은 각 컴퓨터에서 관리하세요.

## 빠른 시작

**Python 3.11 이상**이 필요합니다. 스크립트는 Python과 패키지를 자동으로 설치하지 않으므로 의존성은 직접 준비해야 합니다. 아래 명령은 `gpt_set` 폴더로 이동한 상태에서 실행합니다.

**Windows · PowerShell**

```powershell
py -3 --version
.\bootstrap\sync-gpt.ps1 -Status
```

**macOS·Linux · Bash**

```bash
python3 --version
bash bootstrap/sync-gpt.sh --status
```

차이 확인은 파일이나 폴더를 변경하지 않으므로 표시된 대상 경로와 변경 내용을 확인한 뒤 설치합니다.

**Windows · PowerShell**

```powershell
.\bootstrap\sync-gpt.ps1
.\bootstrap\sync-gpt.ps1 -Status
```

**macOS·Linux · Bash**

```bash
bash bootstrap/sync-gpt.sh
bash bootstrap/sync-gpt.sh --status
```

설치 후 새 Codex 세션을 시작하여 공통 지침을 확인하고, 보고서 작업에서 `$eec-lab-report`를 호출합니다. [자세한 설치 방법](docs/setup.md)에 별도 프로필, 선택 의존성, 검증 절차를 정리했습니다.

## 일상적인 사용

| 목적 | PowerShell | Bash |
|---|---|---|
| 원본 → 설치본 | `.\bootstrap\sync-gpt.ps1` | `bash bootstrap/sync-gpt.sh` |
| 차이 확인 | `.\bootstrap\sync-gpt.ps1 -Status` | `bash bootstrap/sync-gpt.sh --status` |
| 설치본 → 원본 | `.\bootstrap\sync-gpt.ps1 -Pull` | `bash bootstrap/sync-gpt.sh --pull` |
| 도움말 | `.\bootstrap\sync-gpt.ps1 -Help` | `bash bootstrap/sync-gpt.sh --help` |

설치본에서 수정한 내용을 유지하려면 설치하기 전에 `Pull`로 회수하거나 직접 원본에 반영하세요. 회수는 원본에 이미 있는 파일과 공유 설정 항목만 대상으로 합니다. 설치본의 새 스킬이나 새 파일은 먼저 원본에 추가해야 관리 대상이 됩니다.

내용이 바뀌는 기존 파일은 `<사용자 홈>/.gpt_set/backups/` 아래에 백업합니다. 같은 내용을 재설치하면 파일을 다시 쓰거나 불필요한 백업을 만들지 않습니다. 백업은 스킬 검색 경로 바깥에 저장합니다.

원본에서 파일을 지워도 설치본을 자동 삭제하지 않습니다. 관리 대상 밖의 스킬과 설정, 로그인 정보, 세션 기록은 동기화하지 않습니다.

## 공유 설정을 추가할 때

`home/codex/config.shared.toml`에 여러 컴퓨터에서 공유할 항목만 작성합니다. 값이 있는 TOML 설정을 병합하거나 회수할 때는 `bootstrap/requirements.txt`의 `tomlkit` 패키지가 추가로 필요합니다. 초기 빈 설정으로 공통 지침과 스킬만 설치할 때는 Python 표준 라이브러리만 사용합니다.

설정은 TOML 구조로 읽어 병합합니다. 로컬 설정 전체를 원본으로 복사하지 않습니다. 선택 의존성 설치는 [설치 안내](docs/setup.md#공유-설정을-추가할-때의-선택-의존성)를 참고하세요.

배열과 배열 테이블은 해당 키의 전체 값이 공유 단위입니다. 컴퓨터별 항목이 섞인 배열은 공유 파일에 넣지 않습니다.

## 참고 문서

- [설치와 수정 방법](docs/setup.md)
- [문제 해결](docs/troubleshooting.md)
- [공식 OpenAI 문서: AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [공식 OpenAI 문서: Codex 설정](https://learn.chatgpt.com/docs/config-file/config-basic)
- [공식 OpenAI 문서: 스킬](https://learn.chatgpt.com/docs/build-skills)

