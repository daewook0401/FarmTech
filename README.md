# FarmTech

Minecraft **1.20.1 / Forge 47.4.10**용 Docker Compose 서버팩입니다.
Git에서 설정과 버전 목록을 받고, Docker 빌드 중 공식 배포처에서 지정된 모드 파일을 내려받아 SHA-256을 검사합니다.
월드·백업·서버에서 수정한 설정은 Git과 분리한 `data/`에 보관합니다.

## 처음 설치

Linux amd64, Git, Docker와 Compose, `bash`, `flock`, `tar`가 필요합니다. 호스트에 Java를 설치할 필요는 없습니다.

```bash
git clone https://github.com/daewook0401/FarmTech.git
cd FarmTech
cp .env.example .env
nano .env
```

[Minecraft EULA](https://www.minecraft.net/eula)에 동의하는 경우에만 `.env`의 `EULA=false`를 `EULA=true`로 바꿉니다.
`PUID`와 `PGID`는 서버 사용자 계정의 `id -u`, `id -g` 값과 맞춥니다. 기본값은 1000:1000입니다.

```bash
bash deploy.sh
docker compose logs -f --tail=80 minecraft
```

첫 빌드에는 Java 이미지·Forge·모드를 받는 인터넷 연결이 필요합니다.
로그에 `Done (...)! For help, type "help"`가 나타난 뒤 접속합니다. 로그 화면에서 Ctrl+C를 눌러도 서버는 계속 실행됩니다.
새 서바이벌 월드는 첫 실행에 생성됩니다.

## Git 업데이트 적용

```bash
cd FarmTech
bash update.sh
```

`update.sh`는 다음 작업을 순서대로 수행합니다.

1. `git pull --ff-only`로 최신 커밋을 받습니다.
2. 새 Docker 이미지를 빌드합니다. 다운로드나 빌드에 실패하면 실행 중인 서버를 유지합니다.
3. 실행 중인 서버를 정상 종료하고 최대 120초 기다립니다.
4. 기존 월드가 있으면 월드·설정·총기팩·권한 목록을 `deployment-backups/`에 압축합니다.
5. 새 이미지로 컨테이너를 다시 실행합니다.

직접 명령을 나누려면 `git pull --ff-only` 후 `bash deploy.sh`를 실행하면 됩니다.
Git 파일만 받아서는 이미 실행 중인 컨테이너가 바뀌지 않습니다.
업데이트 직전 백업에 실패하면 이전 컨테이너를 다시 시작합니다. 새 모드의 실행 오류까지 자동으로 되돌리지는 않습니다.
버전 변경 시에는 클라이언트의 콘텐츠 모드 버전도 함께 맞춰야 합니다.

## 접속과 운영

클라이언트는 동일한 FarmTech 모드 구성으로 `서버주소:25565`에 접속합니다.
정품 인증과 화이트리스트가 켜져 있으므로 최초 접속 전에 콘솔에서 닉네임을 추가합니다.

```bash
bash console.sh
```

콘솔 명령은 `/` 없이 입력합니다.

```text
whitelist add 닉네임
```

관리자 권한이 필요하면 소유자가 `op 닉네임`을 입력합니다.
콘솔에서 빠져나올 때는 **Ctrl+P를 누른 다음 Ctrl+Q**를 누릅니다.

```bash
docker compose logs -f --tail=80 minecraft
docker compose stop
docker compose start
docker compose down
```

`down`으로 컨테이너를 지워도 `data/`는 남습니다. 월드를 지우려는 목적이 아니라면 `data/`를 삭제하지 마세요.
외부 접속은 서버 환경에 맞는 TCP 포트 전달/방화벽 설정이 필요합니다. 배포 스크립트가 방화벽을 변경하지는 않습니다.

## 기본 설정

16GB RAM과 4코어 8스레드 환경을 고려한 시작 설정입니다. 동시 접속 인원·탐험·기계 규모에 따라 조정합니다.

| 항목 | 기본값 | 수정 위치 |
|---|---|---|
| Java 메모리 | 시작 2GB / 최대 6GB | `.env`의 `INIT_MEMORY`, `MAX_MEMORY` |
| 컨테이너 메모리 상한 | 8GB | `.env`의 `CONTAINER_MEMORY` |
| 호스트 포트 | TCP 25565 | `.env`의 `SERVER_PORT` |
| 접속 상한 | 8명 | `data/server.properties` |
| 시야 / 시뮬레이션 | 8 / 6청크 | `data/server.properties` |
| FTB 강제 로딩 | 팀당 9청크 | 아래 설명 참고 |
| FTB 오프라인 로딩 | 팀원이 모두 나가면 중단 | 아래 설명 참고 |

Java 힙 외의 메모리도 필요하므로 `CONTAINER_MEMORY`를 `MAX_MEMORY`보다 넉넉하게 둡니다.
설정을 바꾼 뒤 `bash deploy.sh`로 적용합니다.

새 월드의 FTB 기본값은 `pack/defaults/defaultconfigs/ftbchunks/ftbchunks-world.snbt`에 있습니다.
월드 생성 이후에는 `data/world/serverconfig/ftbchunks-world.snbt`를 수정합니다.
기존 월드 안의 설정은 업데이트할 때 덮어쓰지 않습니다.

## 설정 보존 방식

- `pack/defaults/`: Git으로 배포하는 기본 설정입니다.
- `data/config`, `data/defaultconfigs`, `data/server.properties`: 실제 서버가 사용하는 설정입니다.
- 사용자가 수정하지 않은 파일에는 새 기본값을 적용합니다.
- 서버에서 수정한 파일은 보존합니다. 새 기본값과 충돌하면 같은 위치에 `.farmtech-new` 파일을 만들어 비교할 수 있게 합니다.
- 모드가 설정 파일을 자동 재작성한 경우에도 사용자 수정으로 간주해 보존할 수 있습니다.
- `data/.farmtech-defaults/`는 비교 기준입니다. 평소에는 수정하지 않습니다.

`data/mods`와 `data/libraries`는 이미지 안의 파일을 가리키는 심볼릭 링크입니다.
새 이미지를 적용하면 정확히 새 모드 목록을 사용하므로 이전 버전 JAR가 남아 중복되지 않습니다.
모드를 추가·변경하려면 Git의 `pack/manifest.json`과 `pack/mods.tsv`를 함께 수정합니다.

## 저장과 백업

Minecraft 기본 자동 저장과 별도로 Simple Backups를 포함했습니다.

- 플레이 활동이 있을 때 60분 간격으로 전체 월드를 저장·백업합니다.
- 보관 한도는 최근 24개 또는 합계 25GB입니다. 한도에 따라 오래된 백업이 정리됩니다.
- 저장 위치는 `data/backups/` 아래 월드별 폴더입니다.
- 설정은 `data/config/simplebackups-common.toml`입니다.
- 수동 백업은 서버 콘솔에서 `simplebackups backup start`를 입력합니다.
- Git 업데이트 직전의 별도 백업은 `deployment-backups/`에 저장되며 자동 삭제하지 않습니다. 필요에 따라 오래된 파일을 정리합니다.

복구하려면 먼저 `docker compose stop`으로 종료합니다. 현재 `data/world`를 별도 이름으로 보관하고 선택한 백업을 임시 폴더에 풉니다.
`level.dat`가 들어 있는 폴더를 `data/world`로 복원한 뒤 시작합니다. 업데이트 직전 백업에는 `world/`뿐 아니라 설정도 들어 있으므로 필요한 범위를 확인해 복원합니다.
같은 디스크의 백업이므로 디스크 고장에 대비하려면 다른 장치에도 복사합니다.

## 이전 압축 서버팩에서 옮길 때

서버를 완전히 멈춘 뒤 이전 팩의 `server/`에서 다음 항목만 새 저장소의 `data/`로 복사합니다.

```text
world/  backups/  config/  defaultconfigs/  tacz/
server.properties  whitelist.json  ops.json  banned-players.json  banned-ips.json
```

존재하는 항목만 복사하고 소유자를 `.env`의 UID/GID와 맞춥니다.
`mods/`, `libraries/`, 이전 실행 스크립트는 이미지가 관리하므로 옮기지 않습니다.
기존 설정은 첫 실행에도 보존됩니다. `.env`의 EULA 설정은 별도로 확인합니다.

## 한국어 퀘스트

FTB Quests 2001.4.22와 FTB XMod Compat 2.1.3을 서버와 클라이언트에 포함합니다.
정착·농업·전력·자동 농장·강화 재료·AE2·탐험의 7개 장에 한국어 퀘스트 50개가 있습니다.
인벤토리의 퀘스트 책 버튼으로 열 수 있으며, 키 지정은 설정 → 조작 → FTB 퀘스트에서 확인합니다.

- 아이템 목표는 보유 여부만 확인하며 소비하지 않습니다. 기계 가동까지 자동 검사하는 목표는 아닙니다.
- 같은 FTB 팀은 진행 상황을 공유합니다. 보상은 각 플레이어가 직접 수령합니다.
- 보상은 소량의 음식·재료와 경험치이며, 핵심 기계나 고급 씨앗을 지급하지 않습니다.
- 퀘스트는 제작법을 잠그지 않습니다. 선행 퀘스트를 마치기 전에도 다른 목표의 아이템을 준비할 수 있습니다.
- 내용은 `pack/defaults/config/ftbquests/quests/`, 진행 기록은 `data/world/ftbquests/`에 저장합니다.
- `tools/build_quests.py`에서 내용을 수정한 뒤 실행해 배포 파일을 생성하고 `python3 tests/validate_quests.py`로 검사합니다.
- 기존 진행을 유지하려면 생성기의 퀘스트 키를 바꾸지 마세요. 제목과 설명만 바꾸면 같은 ID를 유지합니다.

친구의 클라이언트에도 위 두 모드를 같은 버전으로 설치하세요. 서버에 접속하면 퀘스트 내용은 동기화됩니다.
플레이 메뉴 한국어 보완은 `client-overrides/resourcepacks/FarmTech-Quests-Korean` 폴더를 클라이언트의 `resourcepacks/`에 복사하고 리소스팩 메뉴에서 활성화합니다.
싱글플레이에서도 같은 퀘스트를 쓰려면 `pack/defaults/config/ftbquests/quests` 폴더를 클라이언트의 `config/ftbquests/quests`로 복사합니다.

## 나무 벌목과 우클릭 수확

- HT’s TreeChop 0.19.0 fixed: 나무 밑동을 도끼로 계속 캐면 줄기가 단계적으로 깎입니다.
- Panda’s Falling Trees 0.13.2: TreeChop과 연동해 벌목한 나무가 옆으로 쓰러지는 애니메이션을 표시합니다. 필수 PandaLib 0.5.2도 포함합니다.
- RightClickHarvest 4.6.1+1.20.1: 다 자란 작물을 우클릭해 수확하고 다시 심습니다. 필수 JamLib 1.3.6+1.20.1-patch.1도 포함합니다.

우클릭 수확은 괭이 없이 가능하며 한 번에 한 포기만 처리합니다. 추가 허기 소모와 수확 경험치는 꺼져 있습니다.
설정은 서버의 `data/config/rightclickharvest.json5`에서 바꿀 수 있습니다.
싱글플레이에도 같은 설정을 쓰려면 `pack/defaults/config/rightclickharvest.json5`를 클라이언트 `config/`에 복사합니다.
친구 클라이언트에도 위 모드 5개를 같은 버전으로 설치하세요.
TreeChop 설정은 기본 N 키로 열 수 있으며, 웅크리면 일반 블록 파괴로 전환됩니다.
Panda’s Falling Trees와 PandaLib는 Forge 1.20.1용 베타 배포본을 고정해서 사용합니다.

## 포함 모드와 진단

Farmer's Delight, Industrial Foregoing, Mekanism, Mekanism Generators, AE2, Mystical Agriculture, Powah, Farming for Blockheads, Pipez, TaCZ, Sophisticated Backpacks, Curios, Jade, FTB Chunks, FTB Teams, Waystones와 필수 라이브러리를 포함합니다.
최적화는 FerriteCore·ModernFix, 서버 진단은 spark, 자동 백업은 Simple Backups를 사용합니다.
서버 모드 JAR는 총 37개이며 정확한 버전·출처·해시는 [`pack/manifest.json`](pack/manifest.json)에 있습니다.
JEI는 클라이언트와 서버에 같은 버전을 넣어 제작법을 동기화합니다.
Embeddium·Oculus·셰이더·한국어 리소스팩은 클라이언트에서 사용합니다.
TaCZ 기본 총기팩은 모드가 첫 실행 때 `data/tacz/`에 생성합니다.

서버 콘솔에서 `spark tps`로 TPS를 볼 수 있습니다.
`spark healthreport`, `spark profiler start`, `spark profiler stop` 등은 보고서/프로파일을 외부 뷰어에 올릴 수 있으므로 필요한 때 직접 실행합니다.

## 검증

검증 범위와 실행 방법은 [`VALIDATION.md`](VALIDATION.md)에 기록했습니다.
서버 EULA는 기본 미동의 상태이며 자동으로 동의하지 않습니다.

출처: [Forge](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.20.1.html), [Eclipse Temurin](https://hub.docker.com/_/eclipse-temurin), [spark](https://spark.lucko.me/docs/Installation), [Simple Backups](https://www.curseforge.com/minecraft/mc-mods/simple-backups).
