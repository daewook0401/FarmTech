# 검증 기록

2026-09-13 기준:

- 서버 모드 29개와 Forge 설치 프로그램을 고정한 공식 다운로드 주소에서 실제 내려받음.
- 다운로드 파일의 SHA-256과 JAR 압축 무결성 확인.
- 기존 정상 동작한 클라이언트와 콘텐츠 모드 버전 일치 확인.
- 같은 Forge 47.4.10 설치 프로그램으로 서버 라이브러리 생성 성공 확인.
- Docker Compose 설정 검사와 Bash 문법 검사 통과.
- Linux에서 설정 동기화 테스트 통과: 신규 설정, 기본값 업데이트, 사용자 수정 보존, 충돌 파일, 기존 설정 가져오기, 심볼릭 링크 보호.
- Linux에서 배포 절차 테스트 통과: 빌드 이후 종료, 종료된 월드의 백업 이후 재시작, 빌드 실패 시 기존 서버 유지, 백업 실패 시 이전 컨테이너 재시작. 이 테스트는 Docker 명령을 가짜 명령으로 대체하므로 실제 게임 서버를 실행하지 않음.
- EULA 미동의 시 데이터 변경 없이 종료하는 동작 확인.

로컬 Docker Desktop의 시작 오류로 전체 Docker 이미지 빌드는 실행 검증하지 못했습니다.
사용자가 직접 실행하도록 선택했으므로 원격 서버에 배포하거나 실제 Minecraft 월드 부팅·클라이언트 접속·Simple Backups 생성/복구를 실행하지 않았습니다.
위 스크립트 테스트는 실제 게임 실행 호환성 검증을 대신하지 않습니다.

Linux 테스트 명령:

```bash
bash tests/test_config_sync.sh
bash tests/test_deploy.sh
python3 tests/validate_pack.py
docker compose config --quiet
```

`validate_pack.py`는 Python 3.11 이상이 필요합니다. 서버 운영과 Docker 빌드에는 호스트 Python이 필요하지 않습니다.
다운로드까지 검증하려면 다음 명령을 실행합니다.

```bash
bash tools/download.sh pack/mods.tsv .cache/downloads
bash tools/download.sh pack/forge.tsv .cache/downloads
python3 tests/validate_pack.py .cache/downloads
```

빌드 검증: `docker compose build minecraft`.
EULA에 동의한 관리자가 `.env`를 준비한 후 `bash deploy.sh`를 실행하면 실제 서버를 시작할 수 있습니다.
