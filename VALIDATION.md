# 검증 기록

2026-09-13 기준. 사용자의 EULA 동의와 실행 요청을 받아 Linux Docker 서버에서 검증했습니다.

- Minecraft 1.20.1 / Forge 47.4.10 / Java 17, 서버 모드 30개.
- 모든 모드와 Forge 설치 프로그램을 공식 고정 주소에서 내려받아 SHA-256과 JAR 압축 무결성 확인.
- Docker 이미지 빌드와 일반 사용자 UID/GID 1000:1000으로 실행 성공.
- 첫 실행에서 발견한 다운로드 파일의 0600 권한 문제 수정. 신규 다운로드와 캐시 파일의 0644 권한을 검사하는 회귀 테스트 추가.
- `.env`의 EULA 동의 반영과 실제 `eula.txt` 생성 확인. `.env`와 운영 데이터는 Git에서 제외.
- Java 초기 2GB / 최대 6GB, 컨테이너 상한 8GB로 새 월드 생성과 `Done` 로그 확인.
- Windows의 기존 FarmTech Forge 클라이언트로 도메인과 25565 포트를 사용해 실제 로그인 및 월드 진입 성공.
- JEI를 클라이언트와 같은 15.56.0.205 버전으로 서버에 포함한 뒤 제작법 동기화 경고가 사라지고 제작법 화면이 표시되는 것 확인.
- FTB 지도, 한국어 UI, 셰이더가 적용된 클라이언트에서 접속 확인.
- 1명 접속 중 spark로 20 TPS 확인. 최근 10초 틱 시간 중앙값 17.6ms, 95백분위 30.0ms. 컨테이너 메모리 약 2.2GiB. 새 월드의 짧은 접속 테스트이며 공장 가동이나 다인원 부하 테스트는 아님.
- Simple Backups 수동 백업 생성 성공. ZIP CRC, `level.dat` 압축 해제와 NBT 루트, 리전 및 서버 설정 파일 포함 확인. 60분 간격·최근 24개·25GB 한도 설정 반영 확인.
- 실제 `bash update.sh` 실행으로 Git pull, 이미지 빌드, 정상 종료, 업데이트 직전 백업, 컨테이너 재생성 검증.
- 업데이트 직전 백업 약 52MiB 생성. 월드·설정·화이트리스트 포함 및 재시작 후 플레이어 저장 데이터의 바이트 일치 확인.
- 같은 월드에 재접속 성공. 두 번째 부팅은 전체 약 17초, 컨테이너 재시작 횟수 0, OOM 없음.
- FTB Chunks 실제 월드 설정에서 청크 소유 500개, 강제 로딩 9개, 팀원 오프라인 시 강제 로딩 중단 확인.
- TaCZ 기본 총기팩 자동 추출 확인.
- Docker Compose 설정, Bash 문법, 설정 동기화·배포 절차 테스트 통과. EULA 미동의 시 데이터 변경 없이 종료하는 테스트도 통과.

남은 검증 범위와 알려진 로그:

- 백업을 별도 서버에 복원해 부팅하는 재해 복구 테스트와 60분 타이머 대기는 수행하지 않았습니다.
- Industrial Foregoing 3.5.22에 `forge:plastic`을 참조하는 `simulated_hydroponic_bed` 제작법 발전과제 1개의 로드 오류가 남습니다. 해당 발전과제는 로드되지 않으며, 이번 부팅·접속·JEI 화면 검증은 통과했습니다.
- Docker에서 LAN 자동 검색 방송의 `Network is unreachable` 경고가 발생하지만, 주소를 직접 입력한 접속은 통과했습니다.

Linux 테스트 명령:

```bash
bash tests/test_download.sh
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

최초 배포는 EULA에 동의한 관리자가 `.env`를 준비한 후 `bash deploy.sh`, 이후 업데이트는 `bash update.sh`로 실행합니다.
