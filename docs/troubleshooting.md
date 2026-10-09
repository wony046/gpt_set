# 문제 해결

모든 명령은 `gpt_set` 폴더에서 실행합니다. 먼저 차이 확인으로 실제 대상 경로와 변경 내용을 확인하세요.

**Windows · PowerShell**

```powershell
.\bootstrap\sync-gpt.ps1 -Status
```

**macOS·Linux · Bash**

```bash
bash bootstrap/sync-gpt.sh --status
```

## Python을 찾을 수 없거나 버전이 낮음

Python 3.11 이상이 필요합니다. 터미널에서 버전을 확인하고 Python을 설치한 뒤 터미널을 다시 여세요. Windows에서는 `-PythonExecutable`로 실행 파일을 직접 지정할 수 있습니다.

**Windows · PowerShell**

```powershell
py -3 --version
.\bootstrap\sync-gpt.ps1 -Status -PythonExecutable 'C:\path\to\python.exe'
```

**macOS·Linux · Bash**

```bash
python3 --version
```

## tomlkit을 찾을 수 없음

초기 빈 공유 설정으로 지침과 스킬만 설치할 때는 `tomlkit`이 필요하지 않습니다. 값이 있는 공유 TOML을 병합하거나 회수할 때 패키지가 필요합니다.

[설치 안내의 가상환경 예시](setup.md#공유-설정을-추가할-때의-선택-의존성)대로 설치하세요. 패키지가 설치되어 있는데 오류가 나면 동기화 도구가 다른 Python을 실행하고 있는지 확인합니다. Windows에서는 가상환경 Python을 `-PythonExecutable`로 지정하고, Bash에서는 가상환경을 활성화한 뒤 실행합니다.

## PowerShell 실행 정책으로 실행이 막힘

스크립트 내용을 확인한 후, 현재 PowerShell 프로세스에만 실행 정책을 적용할 수 있습니다. 조직 정책이 실행을 제한하면 관리 정책을 따르세요.

**Windows · PowerShell**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\bootstrap\sync-gpt.ps1 -Status
```

이 설정은 현재 PowerShell 창을 닫으면 종료됩니다.

## Bash 스크립트 실행 권한 오류

실행 파일 권한 없이도 Bash에 파일을 전달하여 실행할 수 있습니다.

**macOS·Linux · Bash**

```bash
bash bootstrap/sync-gpt.sh --status
```

`$'\r'` 등의 오류가 나오면 `sync-gpt.sh`의 줄바꿈을 LF로 저장하세요. `.gitattributes`는 Bash 파일의 LF 줄바꿈을 지정합니다. PowerShell 파일은 Windows PowerShell 5.1에서 한국어 주석을 읽을 수 있도록 UTF-8 BOM과 CRLF로 저장합니다.

## 설치 후 공통 지침이 적용되지 않음

새 Codex 세션을 시작하고 동기화 도구가 표시한 Codex 홈이 실행 중인 Codex의 홈과 같은지 확인하세요. `CODEX_HOME`을 설정했다면 기본 `~/.codex`와 다른 경로를 사용할 수 있습니다.

Codex 홈에 `AGENTS.override.md`가 있으면 `AGENTS.md`보다 먼저 읽습니다. 프로젝트나 하위 폴더의 지침도 함께 적용될 수 있습니다. 관련 파일의 내용을 확인하고 필요한 쪽에 규칙을 정리하세요. [공식 AGENTS.md 안내](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

## 분리한 한국어 지침이 적용되지 않음

차이 확인 출력에서 `home/codex/korean_style.md`가 설치본과 같은지 확인하세요. `AGENTS.md`와 `korean_style.md`는 동기화 도구가 표시한 같은 Codex 홈에 있어야 합니다. 별도 프로필을 사용한다면 그 프로필의 두 파일을 확인합니다.

Markdown 링크만으로 파일 내용이 자동 포함되지는 않습니다. `AGENTS.md`에는 한국어 설명이나 문서 본문을 작성하기 전에 해당 파일을 읽으라는 지시가 있어야 합니다. 새 세션에서 한국어 작성 지침의 출처를 확인하여 실제로 파일을 읽었는지 점검하세요.

보고서 스킬만 별도로 설치한 환경에서도 보고서 고유의 문체와 예시 및 Word 서식은 스킬 안의 가이드로 적용할 수 있습니다. 일반 한국어 지침까지 동일하게 적용하려면 공통 지침과 `korean_style.md`도 해당 환경에서 사용할 수 있도록 제공해야 합니다.

## eec-lab-report가 표시되지 않음

차이 확인 출력에서 대상 사용자 홈을 확인하고 `<사용자 홈>/.agents/skills/eec-lab-report/SKILL.md`가 설치되어 있는지 확인하세요. Codex를 다시 시작한 뒤 `$eec-lab-report`로 호출합니다.

동일한 `name`의 스킬이 여러 위치에 있으면 별도로 표시될 수 있습니다. 스킬이 설정에서 비활성화되어 있는지도 확인하세요. [공식 스킬 안내](https://learn.chatgpt.com/docs/build-skills)

## config.toml이 바뀌지 않음

초기 `home/codex/config.shared.toml`은 주석만 있으므로 정상입니다. 공유 파일에 실제 설정 항목을 추가한 경우에만 해당 키를 반영합니다. 그 밖의 모델, 경로, 개인 설정은 유지합니다.

설정을 추가했는데 Codex의 동작이 바뀌지 않으면 새 세션을 시작하고 프로젝트 설정이나 실행 옵션이 우선 적용되는지 확인하세요. [공식 설정 안내](https://learn.chatgpt.com/docs/config-file/config-basic)

## TOML 오류가 표시됨

공유 설정과 설치본 `config.toml`의 문법을 확인합니다. 따옴표, 중복 키, 테이블 선언을 살펴보세요. 설정 문법이나 값의 의미는 [공식 설정 안내](https://learn.chatgpt.com/docs/config-file/config-basic)를 참고합니다.

## Pull로 새 파일이나 삭제가 반영되지 않음

회수는 원본에 이미 존재하는 파일과 공유 항목만 대상으로 합니다. 설치본에만 있는 새 스킬이나 파일은 직접 `home/skills/`에 넣어 관리 대상으로 추가합니다. 설치본에서 삭제된 파일이나 원본에서 삭제한 파일을 자동으로 반대쪽에서도 삭제하지 않습니다.

## 설치본의 수정 내용이 덮어써짐

기본 설치는 원본 내용을 설치본에 반영합니다. 설치본을 먼저 수정했다면 설치 전 차이를 확인하고 `Pull`로 원본에 회수하세요. 원본과 설치본 모두에 변경이 있으면 유지할 내용을 직접 비교합니다.

이전 내용은 `<사용자 홈>/.gpt_set/backups/`에서 확인할 수 있습니다. 대상 경로와 내용을 확인한 뒤 필요한 파일을 원래 위치로 복사하여 복원합니다.

## 재설치했는데 백업이 늘어나지 않음

동일한 내용의 파일은 다시 쓰지 않으므로 정상입니다. 백업은 기존 관리 대상 파일의 내용이 실제로 달라질 때 생성합니다.
