# gpt_set

여러 컴퓨터에서 GPT의 개인 공통 지침, 작업별 스킬, 공유 설정을 유지하기 위한 저장소입니다.

`home/`의 파일을 원본으로 관리하고 `bootstrap/`의 동기화 도구로 설치본과 비교하거나 변경 사항 적용할 때 사용합니다.


## 디렉터리 구조

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

## 설치

| 원본 | 설치 위치 | 동작 |
|---|---|---|
| `home/codex/AGENTS.template.md` | `<Codex 홈>/AGENTS.md` | 공통 지침 설치 |
| `home/codex/korean_style.md` | `<Codex 홈>/korean_style.md` | 일반 한국어 작성 지침 설치 |
| `home/codex/config.shared.toml` | `<Codex 홈>/config.toml` | 원본에 적힌 공유 설정 항목만 병합 |
| `home/skills/<스킬 이름>/` | `<사용자 홈>/.agents/skills/<스킬 이름>/` | 원본에 있는 스킬 파일 설치 |

Codex 홈은 명시한 `-CodexHome` 또는 `--codex-home`, 환경 변수 `CODEX_HOME`, `<사용자 홈>/.codex` 순서로 결정합니다. 사용자 홈은 기본적으로 현재 사용자의 홈 폴더이며 `-UserHome` 또는 `--home`으로 바꿀 수 있습니다.

초기 `config.shared.toml`에는 안내 주석만 들어 있습니다.

## 빠른 시작

**Python 3.11 이상**이 필요하고 스크립트는 Python과 패키지를 자동으로 설치하지 않으므로 의존성은 직접 준비해야 합니다. 

gpt_set 폴더로 이동 후 다음을 실행

### 저장소와 컨텍스트 지점 차이 확인하기

**Windows / PowerShell** 

```powershell
py -3 --version
.\bootstrap\sync-gpt.ps1 -Status
```

**macOS,Linux / Bash**

```bash
python3 --version
bash bootstrap/sync-gpt.sh --status
```

### 복사 설치하기

**Windows / PowerShell**

```powershell
.\bootstrap\sync-gpt.ps1
```

**macOS·Linux / Bash**

```bash
bash bootstrap/sync-gpt.sh
```

인자 없이 실행하면 상태 표를 보여 준 뒤 동기화 방향을 묻습니다. `↑`/`↓`로 `Push`(원본 → 설치본), `Pull`(설치본 → 원본), `Exit` 중 하나를 고르고 `Enter`를 누릅니다. 숫자 키 `1`~`3`으로 바로 고를 수도 있고, `Esc`를 누르면 아무것도 바꾸지 않고 종료합니다. 묻지 않고 바로 설치하려면 `-Push`(`--push`)를 사용합니다.

설치 후 새 Codex 세션을 시작하여 공통 지침을 확인할 수 있게 됩니다.

## 일상적인 사용

| 목적 | PowerShell | Bash |
|---|---|---|
| 차이 확인 후 방향 선택 | `.\bootstrap\sync-gpt.ps1` | `bash bootstrap/sync-gpt.sh` |
| 원본 → 설치본 | `.\bootstrap\sync-gpt.ps1 -Push` | `bash bootstrap/sync-gpt.sh --push` |
| 차이 확인 | `.\bootstrap\sync-gpt.ps1 -Status` | `bash bootstrap/sync-gpt.sh --status` |
| 설치본 → 원본 | `.\bootstrap\sync-gpt.ps1 -Pull` | `bash bootstrap/sync-gpt.sh --pull` |
| 도움말 | `.\bootstrap\sync-gpt.ps1 -Help` | `bash bootstrap/sync-gpt.sh --help` |

- 설치본에서 수정한 내용을 유지하려면 설치하기 전에 `Pull`로 회수하거나 직접 원본에 반영하세요. 
- 회수는 원본에 이미 있는 파일과 공유 설정 항목만 대상으로 합니다. 설치본의 새 스킬이나 새 파일은 먼저 원본에 추가해야 관리 대상이 됩니다.
- 내용이 바뀌는 기존 파일은 `<사용자 홈>/.gpt_set/backups/` 아래에 백업합니다.

## 사용법

### 1. 상태 확인하고 방향 고르기

인자 없이 실행하면 저장소의 원본과 이 컴퓨터의 설치본을 비교한 표가 나옵니다.

| 상태 | 의미 |
|---|---|
| `SAME` | 원본과 설치본이 같습니다. |
| `DIFFERENT` | 원본과 설치본의 내용이 다릅니다. |
| `MISSING` | 설치본에 해당 파일이나 설정 키가 없습니다. |
| `NO SHARED SETTINGS` | `config.shared.toml`에 공유할 설정이 아직 없습니다. |

표 아래 메뉴에서 `↑`/`↓`로 고르고 `Enter`를 누릅니다.

| 메뉴 | 고르는 때 |
|---|---|
| `Push` | 저장소의 원본을 고쳤고, 그 내용을 이 컴퓨터의 Codex에 반영하려 할 때 |
| `Pull` | 설치본을 직접 고쳤고, 그 내용을 저장소에 남기려 할 때 |
| `Exit` | 상태만 확인하고 끝내려 할 때 |

### 2. 상황별 순서

**원본을 고쳐서 적용할 때**

1. `home/` 아래의 원본 파일을 수정합니다.
2. 동기화 도구를 실행하고 `Push`를 고릅니다.
3. 새 Codex 세션을 시작해서 반영되었는지 확인합니다.

**설치본에서 고친 내용을 저장소에 남길 때**

1. 동기화 도구를 실행하고 `Pull`을 고릅니다.
2. `git diff`로 저장소에 들어온 변경 내용을 확인한 뒤 커밋합니다.

**다른 컴퓨터와 맞출 때**

메뉴의 `Push`와 `Pull`은 이 컴퓨터 안에서만 파일을 복사합니다. GitHub와 주고받는 작업은 git으로 따로 합니다.

1. 변경한 컴퓨터에서 저장소에 변경을 모은 뒤(`Pull` 또는 원본 직접 수정) `git commit`과 `git push`를 실행합니다.
2. 다른 컴퓨터에서 `git pull`을 실행한 뒤 동기화 도구에서 `Push`를 고릅니다.

### 3. 주의할 점

- 파일 단위로 한쪽을 통째로 덮어씁니다. 원본과 설치본을 모두 고쳤다면 실행하기 전에 두 파일을 직접 비교하세요. 덮어쓴 파일은 `<사용자 홈>/.gpt_set/backups/`에 남습니다.
- 새 스킬이나 새 파일은 저장소의 `home/` 아래에 직접 추가해야 관리 대상이 됩니다.
- 한쪽에서 지운 파일은 다른 쪽에서 자동으로 지워지지 않습니다.


## 공유 설정을 추가할 때

- `home/codex/config.shared.toml`에 여러 컴퓨터에서 공유할 항목만 작성합니다. 
- 값이 있는 TOML 설정을 병합하거나 회수할 때는 `bootstrap/requirements.txt`의 `tomlkit` 패키지가 추가로 필요합니다.

설정은 TOML 구조로 읽어 병합합니다. 로컬 설정 전체를 원본으로 복사하지 않습니다. 선택 의존성 설치는 [설치 안내](docs/setup.md#공유-설정을-추가할-때의-선택-의존성)를 참고하세요.

## 참고 문서

- [설치와 수정 방법](docs/setup.md)
- [문제 해결](docs/troubleshooting.md)
- [공식 OpenAI 문서: AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [공식 OpenAI 문서: Codex 설정](https://learn.chatgpt.com/docs/config-file/config-basic)
- [공식 OpenAI 문서: 스킬](https://learn.chatgpt.com/docs/build-skills)

