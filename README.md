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
.\bootstrap\sync-gpt.ps1 -Status
```

**macOS·Linux / Bash**

```bash
bash bootstrap/sync-gpt.sh
bash bootstrap/sync-gpt.sh --status
```

설치 후 새 Codex 세션을 시작하여 공통 지침을 확인할 수 있게 됩니다.

## 일상적인 사용

| 목적 | PowerShell | Bash |
|---|---|---|
| 원본 → 설치본 | `.\bootstrap\sync-gpt.ps1` | `bash bootstrap/sync-gpt.sh` |
| 차이 확인 | `.\bootstrap\sync-gpt.ps1 -Status` | `bash bootstrap/sync-gpt.sh --status` |
| 설치본 → 원본 | `.\bootstrap\sync-gpt.ps1 -Pull` | `bash bootstrap/sync-gpt.sh --pull` |
| 도움말 | `.\bootstrap\sync-gpt.ps1 -Help` | `bash bootstrap/sync-gpt.sh --help` |

- 설치본에서 수정한 내용을 유지하려면 설치하기 전에 `Pull`로 회수하거나 직접 원본에 반영하세요. 
- 회수는 원본에 이미 있는 파일과 공유 설정 항목만 대상으로 합니다. 설치본의 새 스킬이나 새 파일은 먼저 원본에 추가해야 관리 대상이 됩니다.
- 내용이 바뀌는 기존 파일은 `<사용자 홈>/.gpt_set/backups/` 아래에 백업합니다.


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

