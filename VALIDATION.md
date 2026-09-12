# 검증 기록

2026-09-13 기준. 사용자의 EULA 동의와 실행 요청을 받아 Linux Docker 서버에서 검증했습니다.

- Minecraft 1.20.1 / Forge 47.4.10 / Java 17, 서버 모드 32개(FTB Quests·FTB XMod Compat 포함).
- 모든 모드와 Forge 설치 프로그램을 공식 고정 주소에서 내려받아 SHA-256과 JAR 압축 무결성 확인.
- Docker 이미지 빌드와 일반 사용자 UID/GID 1000:1000으로 실행 성공.
- 첫 실행에서 발견한 다운로드 파일의 0600 권한 문제 수정. 신규 다운로드와 캐시 파일의 0644 권한을 검사하는 회귀 테스트 추가.
- `.env`의 EULA 동의 반영과 실제 `eula.txt` 생성 확인. `.env`와 운영 데이터는 Git에서 제외.
- Java 초기 2GB / 최대 6GB, 컨테이너 상한 8GB로 새 월드 생성과 `Done` 로그 확인.
- Windows의 기존 FarmTech Forge 클라이언트로 도메인과 25565 포트를 사용해 실제 로그인 및 월드 진입 성공.
- JEI를 클라이언트와 같은 15.56.0.205 버전으로 서버에 포함한 뒤 제작법 동기화 경고가 사라지고 제작법 화면이 표시되는 것 확인.
- FTB 지도, 한국어 UI, 셰이더가 적용된 클라이언트에서 접속 확인.
- 퀘스트 추가 전 1명 접속 중 spark로 20 TPS 확인. 최근 10초 틱 시간 중앙값 17.6ms, 95백분위 30.0ms. 컨테이너 메모리 약 2.2GiB. 새 월드의 짧은 접속 테스트이며 공장 가동이나 다인원 부하 테스트는 아님.
- Simple Backups 수동 백업 생성 성공. ZIP CRC, `level.dat` 압축 해제와 NBT 루트, 리전 및 서버 설정 파일 포함 확인. 60분 간격·최근 24개·25GB 한도 설정 반영 확인.
- 실제 `bash update.sh` 실행으로 Git pull, 이미지 빌드, 정상 종료, 업데이트 직전 백업, 컨테이너 재생성 검증.
- 업데이트 직전 백업 약 52MiB 생성. 월드·설정·화이트리스트 포함 및 재시작 후 플레이어 저장 데이터의 바이트 일치 확인.
- 같은 월드에 재접속 성공. 두 번째 부팅은 전체 약 17초, 컨테이너 재시작 횟수 0, OOM 없음.
- FTB Chunks 실제 월드 설정에서 청크 소유 500개, 강제 로딩 9개, 팀원 오프라인 시 강제 로딩 중단 확인.
- TaCZ 기본 총기팩 자동 추출 확인.
- Docker Compose 설정, Bash 문법, 설정 동기화·배포 절차 테스트 통과. EULA 미동의 시 데이터 변경 없이 종료하는 테스트도 통과.


퀘스트 추가 검증 (2026-09-13):

- FTB Quests 2001.4.22와 FTB XMod Compat 2.1.3을 CurseForge 클라이언트와 Docker 서버에 설치. 두 JAR의 버전·SHA-256 및 기존 의존 모드의 범위 일치 확인.
- 한국어 7개 챕터·50개 퀘스트를 서버에서 실제 로드. 모든 선행 조건의 연결·순환 여부·ID 고유성, 보상 범위와 아이템 비소모 설정 검사 통과.
- 퀘스트에서 참조하는 아이템 76종을 실제 서버 레지스트리의 명령 파서로 검사하여 모두 유효함을 확인. 수량 0의 `clear` 명령을 플레이어가 없는 상태에서 사용했으며 아이템을 제거하지 않음.
- 기존 한국어 팩을 유지하고 퀘스트 플레이 메뉴용 한국어 리소스팩을 추가. 192개 번역 키가 설치된 모드에 존재하고 서식 인자가 원문과 일치하는지 확인.
- 실제 정품 클라이언트 로그인 후 퀘스트 책의 7개 한국어 챕터, 안내 본문, 목표·보상 메뉴 확인.
- 안내 확인 목표 완료 및 경험치 10·빵 4개 수령 성공. 제작대 보유 목표가 자동 완료되고 경험치 25·횃불 4개를 수령함. 서버 인벤토리 조회로 제작대 1개가 소비되지 않고 남아 있으며 누적 경험치가 35임을 확인.
- 목표 아이템 클릭으로 JEI 제작법 화면 표시. FTB XMod Compat의 퀘스트·보상 JEI 연동 플러그인이 예외 없이 등록됨.
- 로그아웃 및 저장 후 `world/ftbquests/<팀 UUID>.snbt`에 대표 퀘스트 2개의 완료와 보상 4회의 수령 기록 저장 확인.
- 퀘스트 추가 후 1명 접속 중 20 TPS, 최근 10초 틱 시간 중앙값 18.0ms·95백분위 39.1ms, 컨테이너 메모리 약 2.17GiB 확인. 짧은 기능 점검 결과이며 공장 가동·다인원 부하 성능을 보장하지 않음.
- 테스트 후 서버를 정상 종료하고 플레이어 저장·발전과제·통계 파일 4개를 테스트 전과 바이트 단위로 일치하게 복원. 테스트용 퀘스트 진행은 별도 보관하여 새 진행으로 시작하도록 정리함. 월드 지형과 기존 운영 설정은 유지.
- 50개 전체 퀘스트를 생존 플레이로 완주하거나 여러 명의 팀 보상을 실사용 검증한 것은 아님. 전체 정적 검사와 대표 목표의 실제 기능 검증을 수행함.

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
python3 tools/build_quests.py --check
python3 tests/validate_quests.py
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
