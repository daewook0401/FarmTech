"""Build the Korean FarmTech quest book. Stable keys preserve saved progress."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'pack/defaults/config/ftbquests/quests'
CHAPTERS = []


def chapter(key, title, subtitle, icon):
    CHAPTERS.append(dict(key=key, title=title, subtitle=subtitle, icon=icon, quests=[]))


def quest(key, title, item, text, deps=(), count=1, extra=(), reward=None, xp=25):
    CHAPTERS[-1]['quests'].append(dict(key=key, title=title, item=item, text=text,
        deps=list(deps), count=count, extra=list(extra), reward=reward, xp=xp))


chapter('01_settlement', '01 · 정착과 주방', '첫 도구부터 든든한 식사까지', 'farmersdelight:cooking_pot')
quest('welcome', 'FarmTech에 오신 것을 환영합니다', None,
      ['이 책은 농업과 공장을 처음 배우는 사람을 위한 50개의 작은 목표입니다. 모든 장을 둘러보고 관심 있는 분야부터 시작하세요.',
       '아이템 목표는 인벤토리에 가진 물건을 확인하며 물건을 소비하지 않습니다. 설치하기 전에 잠시 인벤토리에 넣어 주세요. 이미 가진 물건도 인정됩니다.',
       '퀘스트의 아이템을 누르면 JEI 제작법을 볼 수 있습니다. 보상은 직접 눌러 받으며, 같은 FTB 팀은 진행을 공유하지만 보상은 각자 받을 수 있습니다.',
       '퀘스트는 제작을 제한하지 않습니다. 목표 칸의 확인 표시를 눌러 안내를 마치고 왼쪽의 장 목록을 열어 보세요.'], reward=('minecraft:bread', 4), xp=10)
quest('crafting_table', '손으로 시작하는 공장', 'minecraft:crafting_table',
      ['나무를 판자로 바꾸고 제작대를 만들어 주세요. 앞으로 만날 복잡한 기계도 여기서 시작합니다.',
       '제작대 1개를 인벤토리에 넣으면 완료됩니다. 퀘스트를 고정하면 게임 화면에서 목표를 확인할 수 있습니다.'], ['welcome'], reward=('minecraft:torch', 4))
quest('furnace', '첫 불을 지피다', 'minecraft:furnace',
      ['조약돌로 화로를 만들고 연료를 준비하세요. 철과 구리를 녹이고 음식도 익힐 수 있습니다.',
       '석탄이 부족하면 원목을 구워 목탄을 만드세요. 나중에 전기 화로를 도입해도 기본 화로는 유용합니다.'], ['crafting_table'], reward=('minecraft:coal', 2))
quest('iron_pickaxe', '철 도구로 한 걸음', 'minecraft:iron_pickaxe',
      ['철 곡괭이를 마련하고 레드스톤·금·다이아몬드 탐사를 준비하세요.',
       '기계용 자원인 오스뮴도 보관해 두세요. 설치된 모드에 맞는 제작법은 JEI를 기준으로 확인하면 됩니다.'], ['furnace'], reward=('minecraft:bread', 2))
quest('backpack', '두 손은 가볍게', 'sophisticatedbackpacks:backpack',
      ['배낭은 광물과 농산물을 들고 다니는 개인 창고입니다. 배낭을 만든 뒤 인벤토리에서 먼저 확인받으세요.',
       'Curios 액세서리 슬롯을 열어 등에 장착할 수 있습니다. 배낭 열기 키는 설정 → 조작에서 확인하세요.'], ['crafting_table'], reward=('minecraft:string', 2))
quest('knife', '요리사의 첫 도구', 'farmersdelight:flint_knife',
      ['Farmer\'s Delight의 부싯돌 칼을 만드세요. 도마 가공과 재료 수확에 쓰는 주방 도구입니다.',
       '칼·도마·냄비를 갖추면 단순히 구운 음식에서 다양한 요리로 넘어갈 수 있습니다.'], ['crafting_table'], reward=('minecraft:bowl', 2))
quest('cutting_board', '도마 위의 준비', 'farmersdelight:cutting_board',
      ['도마를 만들고 재료를 올린 뒤 알맞은 도구로 가공해 보세요.',
       'JEI의 도마 제작법에서 필요한 도구와 결과물을 확인할 수 있습니다. 이 목표는 도마 보유를 확인합니다.'], ['knife'], reward=('minecraft:carrot', 2))
quest('cooking_pot', '따뜻한 한 끼', 'farmersdelight:cooking_pot',
      ['냄비를 만든 뒤 작동하는 열원 위에 놓아 주세요. 화덕이나 모닥불 등을 활용할 수 있습니다.',
       '요리마다 필요한 재료와 그릇이 다릅니다. JEI에서 원하는 음식의 냄비 제작법을 확인하고 식량 생산을 시작하세요.'], ['cutting_board', 'furnace'], reward=('minecraft:bowl', 4), xp=40)

chapter('02_farming', '02 · 작물과 씨앗', '먹을거리에서 자라는 자원으로', 'farmingforblockheads:market')
quest('market', '농장의 작은 시장', 'farmingforblockheads:market',
      ['Farming for Blockheads의 시장을 만들면 씨앗과 묘목 등을 거래할 수 있습니다.',
       '원하는 작물을 구하기 힘들 때 시장의 판매 목록과 가격을 확인하세요. 농장을 넓히기 전에 물과 조명을 준비하면 좋습니다.'], ['welcome'], reward=('minecraft:emerald', 1))
quest('tomato', '빨갛게 익은 수확', 'farmersdelight:tomato',
      ['토마토를 얻고 씨앗을 남겨 재배를 이어 가세요. 자연에서 작물을 찾거나 시장의 판매 목록을 살펴보세요.',
       '수확한 토마토 8개를 인벤토리에 모으면 완료됩니다. 수확물은 그대로 남습니다.'], ['market'], count=8, reward=('minecraft:bone_meal', 4))
quest('cabbage', '식탁을 채우는 채소', 'farmersdelight:cabbage',
      ['양배추 8개를 수확해 주세요. 여러 작물을 함께 기르면 냄비 요리의 선택지가 늘어납니다.',
       '식량용 수확물과 다시 심을 씨앗을 구분해 보관하세요. 자동화할 때에도 씨앗을 먼저 확보하는 습관이 도움이 됩니다.'], ['market'], count=8, reward=('minecraft:bone_meal', 4))
quest('rich_soil', '좋은 흙이 좋은 농장을', 'farmersdelight:rich_soil',
      ['유기 퇴비를 적절한 환경에서 숙성해 비옥한 토양을 얻어 보세요. 퇴비 제작법은 JEI에서 확인할 수 있습니다.',
       '비옥한 토양은 Farmer\'s Delight 농장을 꾸미고 확장할 때 유용합니다. 여기서는 완성된 토양 1개를 확인합니다.'], ['tomato', 'cabbage'], reward=('minecraft:bone_meal', 4), xp=40)
quest('inferium', '작물로 자원을 만들다', 'mysticalagriculture:inferium_essence',
      ['Mystical Agriculture는 씨앗을 길러 자원을 생산하는 모드입니다. 먼저 인페리움 정수 16개를 모아 주세요.',
       '광석과 몬스터 드롭 등으로 첫 정수를 마련한 뒤 인페리움 씨앗 재배로 공급을 늘려 보세요.'], ['welcome'], count=16, reward=('minecraft:wheat_seeds', 2))
quest('infusion_altar', '씨앗 주입의 제단', 'mysticalagriculture:infusion_altar',
      ['주입 제단 1개와 주입 받침대 8개를 준비하세요. 중심의 제단과 주변 받침대에 JEI에 나온 재료를 배치합니다.',
       '정확한 배치와 레드스톤 신호가 필요합니다. 재료를 놓은 뒤 버튼이나 레버로 주입을 시작해 보세요.'], ['inferium'], extra=[('mysticalagriculture:infusion_pedestal', 8)], reward=('minecraft:redstone', 2), xp=40)
quest('iron_seeds', '철이 자라는 밭', 'mysticalagriculture:iron_seeds',
      ['주입 제단에서 철 씨앗을 만들어 주세요. 필요한 정수 등급과 재료는 JEI의 주입 제작법에서 확인하세요.',
       '씨앗을 심고 수확한 철 정수를 철 자원으로 바꾸면 채굴에만 의존하지 않는 생산 기반이 생깁니다.',
       '정수 등급을 올리는 순서는 05장에서 안내합니다. 다른 장을 오가며 진행해도 괜찮습니다.'], ['infusion_altar'], reward=('minecraft:bread', 2), xp=50)

chapter('03_power', '03 · 첫 전력과 기계', 'Mekanism으로 전기를 생산하고 활용하기', 'mekanismgenerators:heat_generator')
quest('heat_generator', '처음 켜는 발전기', 'mekanismgenerators:heat_generator',
      ['Mekanism의 열 발전기를 만들어 주세요. 연료를 사용하거나 주변의 용암을 활용해 첫 전력을 마련할 수 있습니다.',
       'FE는 여러 기술 모드가 함께 사용하는 전력 단위입니다. 발전량과 기계 소비량을 함께 확인하세요.'], ['welcome'], reward=('minecraft:coal', 2))
quest('infuser', '금속에 성질을 더하기', 'mekanism:metallurgic_infuser',
      ['야금 주입기는 철 등에 탄소나 레드스톤 성분을 주입하는 기계입니다. 첫 합금과 강철 제작의 출발점입니다.',
       '전원을 연결하고 주입 재료 칸과 가공 재료 칸을 구분해 주세요. 서로 다른 주입 성분을 바꿀 때에는 내부 상태를 확인하세요.'], ['heat_generator'], reward=('minecraft:redstone', 2))
quest('steel', '공장의 뼈대, 강철', 'mekanism:ingot_steel',
      ['강철 주괴 4개를 준비하세요. 야금 주입과 제련을 거치는 전체 과정을 JEI에서 따라가 보세요.',
       '강철은 케이블과 기계 외장재 등 여러 설비에 쓰입니다. 재료를 바로 전부 쓰기보다 조금씩 비축하세요.'], ['infuser'], count=4, reward=('minecraft:coal', 2))
quest('cable', '전기가 흐르는 길', 'mekanism:basic_universal_cable',
      ['기본 범용 케이블 8개로 발전기와 기계를 이어 주세요. 연결되어도 작동하지 않으면 기계의 면 설정을 확인하세요.',
       '전력 케이블과 유체 파이프는 역할이 다릅니다. 필요한 자원에 맞는 운송 수단을 선택하세요.'], ['steel'], count=8, reward=('minecraft:redstone', 2))
quest('energy_cube', '남는 전력을 저장하기', 'mekanism:basic_energy_cube',
      ['기본 에너지 큐브는 남는 전기를 저장해 발전량이 흔들릴 때 기계에 공급합니다.',
       '큐브의 입력·출력 면과 기계 방향을 확인하세요. 저장 장치가 있어도 장기간 소비량이 발전량보다 많으면 결국 전력이 바닥납니다.'], ['cable'], reward=('minecraft:iron_ingot', 1), xp=40)
quest('enrichment', '광물 가공의 시작', 'mekanism:enrichment_chamber',
      ['농축 챔버를 만들어 광물과 각종 재료를 가공하세요. 재료 형태에 따라 가공 비율이 달라집니다.',
       '원광·광석·가루의 제작법을 JEI에서 비교한 뒤 투입하세요. 모든 재료가 같은 비율로 늘어나지는 않습니다.'], ['cable'], reward=('minecraft:coal', 2), xp=40)
quest('smelter', '전기로 굽는 화로', 'mekanism:energized_smelter',
      ['전기 제련기를 농축 챔버와 함께 사용하면 가공된 가루를 주괴로 만들 수 있습니다.',
       '기계의 입출력 면과 자동 배출 설정을 익혀 보세요. 다음 장의 Pipez를 연결하면 상자에서 완성품까지 흐름을 만들 수 있습니다.'], ['enrichment'], reward=('minecraft:iron_ingot', 1), xp=40)
quest('wind', '바람으로 이어 가는 전력', 'mekanismgenerators:wind_generator',
      ['풍력 발전기를 설치하면 연료를 계속 보충하지 않아도 됩니다. 설치 높이에 따른 발전량을 확인하세요.',
       '확장할 때는 발전기 개수와 케이블 처리량, 에너지 저장량을 함께 늘려 주세요.'], ['energy_cube'], reward=('minecraft:bread', 2), xp=50)

chapter('04_automation', '04 · 자동 농장과 운송', 'Pipez와 Industrial Foregoing의 첫 생산 라인', 'industrialforegoing:plant_gatherer')
quest('pipe_wrench', '파이프 설정 도구', 'pipez:wrench',
      ['Pipez 렌치는 파이프 연결과 추출 방향을 설정하는 도구입니다. 먼저 렌치를 만들어 주세요.',
       '운송이 멈췄을 때는 공급원에 붙은 면이 추출 모드인지, 받는 상자에 공간이 있는지부터 확인하세요.'], ['welcome'], reward=('minecraft:iron_nugget', 4))
quest('item_pipe', '상자 사이의 작은 자동화', 'pipez:item_pipe',
      ['아이템 파이프 8개를 준비해 두 상자를 연결하세요. 공급원에 닿은 파이프 면을 렌치로 추출 모드로 바꿔 주세요.',
       '아이템 1개를 넣어 도착하는지 먼저 시험하세요. 작은 연결을 확인한 뒤 기계와 큰 창고로 확장하면 문제가 생긴 곳을 찾기 쉽습니다.'], ['pipe_wrench'], count=8, reward=('minecraft:redstone', 2))
quest('fluid_pipe', '액체도 길을 따라', 'pipez:fluid_pipe',
      ['유체 파이프 8개를 마련하세요. 물·라텍스 같은 액체를 저장 장치와 기계 사이로 옮길 수 있습니다.',
       '아이템 파이프와 마찬가지로 공급원 쪽 추출 설정이 필요합니다. 기계가 해당 면으로 유체를 받는지도 확인하세요.'], ['pipe_wrench'], count=8, reward=('minecraft:glass', 2))
quest('fluid_extractor', '나무에서 라텍스로', 'industrialforegoing:fluid_extractor',
      ['유체 추출기를 만들고 작동 면 앞에 사용할 원목을 놓아 라텍스를 얻어 보세요.',
       '사용할 원목과 추출 조건을 JEI 및 기계 화면에서 확인하세요. 원목이 소모되므로 공급 공간을 남겨 두는 것이 좋습니다.'], ['fluid_pipe'], reward=('minecraft:oak_log', 2))
quest('latex_unit', '라텍스를 재료로 가공', 'industrialforegoing:latex_processing_unit',
      ['라텍스 처리 장치에는 라텍스·물·전력이 필요합니다. 각각의 입력을 구분해 연결하세요.',
       '재료가 있어도 작동하지 않으면 전력 부족과 출력 칸을 확인하세요. 이 장치는 플라스틱 생산의 중간 단계입니다.'], ['fluid_extractor', 'cable'], reward=('minecraft:coal', 2))
quest('dry_rubber', '작은 고무를 모으다', 'industrialforegoing:tinydryrubber',
      ['라텍스 처리 장치에서 작은 건조 고무 9개를 모아 주세요.',
       '작은 건조 고무를 건조 고무로 합친 뒤 제련하면 플라스틱을 얻습니다. JEI에서 중간 제작법까지 이어서 확인하세요.'], ['latex_unit'], count=9, reward=('minecraft:bread', 2))
quest('plastic', '자동화 설비의 재료', 'industrialforegoing:plastic',
      ['플라스틱 4개를 준비하세요. Industrial Foregoing의 여러 설비에 반복해서 쓰이는 재료입니다.',
       '라텍스·물·전력·원목 공급을 안정화하면 농장 설비를 늘릴 때마다 처음부터 재료를 모을 필요가 줄어듭니다.'], ['dry_rubber'], count=4, reward=('minecraft:iron_ingot', 1), xp=40)
quest('auto_farm', '심고 거두는 자동 농장', 'industrialforegoing:plant_sower',
      ['파종기와 식물 수확기를 모두 준비하세요. 파종기는 경작지 아래에, 수확기는 작업 영역을 향하도록 배치하는 식으로 시작할 수 있습니다.',
       '기계 화면에서 실제 작업 범위를 확인하고 두 기계의 영역이 겹치게 맞추세요. 씨앗 공급·전력·수확물 출력도 필요합니다.',
       '씨앗은 파종기에 우선 돌려주고 남는 수확물은 상자로 보내세요. 이 목표는 기계 보유를 확인하며 농장 가동 상태까지 자동 검사하지는 않습니다.'], ['plastic', 'item_pipe'], extra=[('industrialforegoing:plant_gatherer', 1)], reward=('minecraft:bread', 4), xp=60)

chapter('05_resources', '05 · 정수와 강화 재료', 'Mystical Agriculture와 Powah의 성장 단계', 'mysticalagriculture:supremium_essence')
quest('prudentium', '정수의 두 번째 단계', 'mysticalagriculture:prudentium_essence',
      ['주입 수정을 이용해 인페리움 정수를 프루덴티움 정수로 합성하세요.',
       '정수 승급은 많은 하위 정수를 소비합니다. 인페리움 농장의 생산량을 먼저 늘리고 수정의 내구도도 확인하세요.'], ['inferium'], count=4, reward=('minecraft:bone_meal', 2))
quest('tertium', '중급 자원으로 확장', 'mysticalagriculture:tertium_essence',
      ['터티움 정수 4개를 만들어 주세요. 더 높은 등급의 씨앗과 설비로 나아갈 준비입니다.',
       '만들고 싶은 씨앗의 등급을 먼저 확인하면 정수를 어디에 사용할지 결정하기 쉽습니다. 철 씨앗도 함께 살펴보세요.'], ['prudentium'], count=4, reward=('minecraft:bone_meal', 2), xp=35)
quest('imperium', '생산량이 곧 힘', 'mysticalagriculture:imperium_essence',
      ['임페리움 정수 4개를 확보하세요. 이 단계에서는 수확·보관·정수 합성을 연결하는 자동화가 도움이 됩니다.',
       '농장만 넓히기보다 수확물 배출이 막히지 않는지 먼저 확인하세요. 자동 제작은 06장의 AE2로 이어집니다.'], ['tertium'], count=4, reward=('minecraft:bread', 2), xp=50)
quest('supremium', '상급 정수의 첫 결실', 'mysticalagriculture:supremium_essence',
      ['수프리미움 정수 1개를 만들어 주세요. 높은 등급의 씨앗과 장비를 선택할 수 있는 기반입니다.',
       '이 보상으로 생산 단계를 건너뛰지는 않습니다. 이후에는 필요한 자원과 목표 장비에 맞춰 농장을 성장시켜 보세요.'], ['imperium'], reward=('minecraft:gold_ingot', 1), xp=75)
quest('powah_energizing', 'Powah 에너지 주입', 'powah:energizing_orb',
      ['에너지 주입 구체와 스타터 에너지 주입 막대 1개씩을 준비하세요. 막대를 구체 근처에 두고 막대에 FE 전력을 공급합니다.',
       'Mekanism 발전기와 케이블의 전력을 활용할 수 있습니다. Powah의 Furnator 같은 별도 발전기도 선택할 수 있습니다.',
       'JEI의 에너지 주입 제작법대로 구체에 재료를 넣어 주세요. 처리에 필요한 총 에너지와 전력 공급 속도는 다릅니다.'], ['cable'], extra=[('powah:energizing_rod_starter', 1)], reward=('minecraft:redstone', 2), xp=40)
quest('energized_steel', '강화 재료를 만들다', 'powah:steel_energized',
      ['에너지 주입으로 Energized Steel 4개를 만들어 주세요. 구체에 넣을 정확한 재료는 JEI에서 확인하세요.',
       '다음 등급의 막대와 발전 설비를 선택하면 더 높은 에너지 요구량을 감당할 수 있습니다. 처음부터 가장 높은 등급을 만들 필요는 없습니다.'], ['powah_energizing'], count=4, reward=('minecraft:gold_ingot', 1), xp=50)

chapter('06_storage', '06 · AE2 통합 창고', '상자 정리에서 주문형 자동 제작까지', 'ae2:drive')
quest('certus_charger', 'AE2의 첫 결정', 'ae2:charger',
      ['충전기 1개와 서투스 석영 결정 4개를 준비하세요. 운석과 관련 자원을 탐사하고 AE2 안내서도 활용해 보세요.',
       '충전기에 전력을 공급해 서투스 석영 결정을 충전할 수 있습니다. 다른 기술 모드의 FE 전원을 연결해 시작할 수 있습니다.'], ['welcome'], extra=[('ae2:certus_quartz_crystal', 4)], reward=('minecraft:torch', 4))
quest('fluix', '플루익스 결정 만들기', 'ae2:fluix_crystal',
      ['충전된 서투스 석영 결정·레드스톤·네더 석영으로 플루익스 결정을 만드는 과정을 JEI에서 확인하세요.',
       '물속에서 재료를 반응시키는 방식으로 시작할 수 있습니다. 완성된 결정 4개를 인벤토리에 모아 주세요.'], ['certus_charger'], count=4, reward=('minecraft:redstone', 2))
quest('inscriber', '회로를 찍는 압축기', 'ae2:inscriber',
      ['AE2 인스크라이버를 만들고 필요한 프레스를 준비하세요. 프레스 종류에 따라 찍을 수 있는 회로가 달라집니다.',
       '운석의 상자에서 프레스를 찾아보세요. 한 번 얻은 프레스는 회로 한 개를 만들 때마다 사라지는 소모품이 아닙니다.'], ['fluix'], reward=('minecraft:iron_ingot', 1))
quest('engineering_processor', '프로세서 조립', 'ae2:engineering_processor',
      ['공학 프로세서 1개를 만들어 주세요. 회로 인쇄 단계와 실리콘·레드스톤을 조립하는 단계를 구분하세요.',
       '논리·연산·공학 프로세서는 서로 다른 재료를 사용합니다. 필요한 프로세서부터 준비하고 JEI로 단계를 거슬러 확인하세요.'], ['inscriber'], reward=('minecraft:redstone', 2), xp=40)
quest('energy_acceptor', '창고에 전력 공급', 'ae2:energy_acceptor',
      ['에너지 수용기를 만들고 FE 전원을 연결하세요. AE2 네트워크가 사용할 전력을 받아들입니다.',
       '작은 저장망부터 시작하고 장치가 늘어날 때 전력과 채널을 함께 관리하세요. 이 단계에서 ME 컨트롤러가 반드시 필요한 것은 아닙니다.'], ['fluix'], reward=('minecraft:coal', 2))
quest('me_drive', '상자를 저장 셀로', 'ae2:drive',
      ['ME 드라이브와 1k 아이템 저장 셀을 준비하세요. 셀을 드라이브에 넣고 전원이 공급되는 네트워크에 연결합니다.',
       '저장 셀은 바이트 용량과 아이템 종류 수에 제한이 있습니다. 한 셀에 모든 종류가 무제한으로 들어가지는 않습니다.'], ['engineering_processor', 'energy_acceptor'], extra=[('ae2:item_storage_cell_1k', 1)], reward=('minecraft:bread', 2), xp=50)
quest('terminal', '한 화면에서 찾는 물건', 'ae2:terminal',
      ['ME 터미널 1개와 플루익스 유리 케이블 4개를 준비하세요. 터미널·드라이브·전원을 하나의 네트워크로 연결합니다.',
       '터미널에 물건을 넣고 검색해 보세요. 나중에는 저장 버스나 입출력 버스로 외부 상자와 기계를 연결할 수 있습니다.'], ['me_drive'], extra=[('ae2:fluix_glass_cable', 4)], reward=('minecraft:torch', 4), xp=50)
quest('autocrafting', '필요할 때 주문하는 공장', 'ae2:pattern_provider',
      ['패턴 공급기·분자 조립기·패턴 인코딩 터미널·1k 제작 저장소·빈 패턴을 각각 1개 준비하세요.',
       '터미널에서 간단한 제작법을 패턴에 기록하고 패턴 공급기에 넣으세요. 공급기에 분자 조립기를 붙이고 제작 저장소를 같은 네트워크에 연결합니다.',
       '먼저 판자나 막대처럼 단순한 제작법을 주문해 보세요. 이후 처리 패턴으로 외부 기계까지 확장할 수 있습니다.',
       '이 목표는 시작 장비의 보유를 확인합니다. 실제 제작 성공은 주문 결과를 직접 확인해 주세요.'], ['terminal'], extra=[('ae2:molecular_assembler', 1), ('ae2:pattern_encoding_terminal', 1), ('ae2:1k_crafting_storage', 1), ('ae2:blank_pattern', 1)], reward=('minecraft:bread', 4), xp=75)

chapter('07_exploration', '07 · 탐험과 총기', '거점을 연결하고 여행을 준비하기', 'waystones:waystone')
quest('waystone', '돌아올 길을 만들다', 'waystones:waystone',
      ['전송석 1개를 준비하세요. 발견한 전송석을 활성화하거나 직접 만든 전송석을 거점에 설치해 보세요.',
       '이동 조건과 비용을 확인하고 지도를 함께 활용하세요. 퀘스트는 인벤토리의 전송석을 확인하므로, 발견한 전송석을 활성화하는 것만으로 완료되지는 않습니다.'], ['welcome'], reward=('minecraft:bread', 2), xp=35)
quest('gun_table', '총기 제작의 작업대', 'tacz:gun_smith_table',
      ['TaCZ 총기 제작대를 만들고 제작 가능한 총기와 탄약 목록을 확인하세요.',
       '기본 총기팩이 제공하는 제작법은 제작대 화면에서 확인할 수 있습니다. 첫 총은 재료 부담이 작은 것부터 선택하세요.'], ['welcome'], reward=('minecraft:iron_nugget', 4))
quest('first_gun', '첫 총기를 마련하다', 'tacz:modern_kinetic_gun',
      ['총기 제작대에서 원하는 기본 총기 1정을 만들어 주세요. 이 목표는 TaCZ의 총기 아이템 보유를 확인하며 특정 기종을 강요하지 않습니다.',
       '장전·조준·사격 키를 설정 → 조작에서 확인하세요. 총기를 만들었어도 맞는 탄약이 없으면 사용할 수 없습니다.'], ['gun_table'], reward=('minecraft:copper_ingot', 2), xp=40)
quest('ammunition', '총기에 맞는 탄약', 'tacz:ammo',
      ['보유한 총기에 맞는 탄약을 제작하세요. 총기 화면의 탄종과 제작대의 탄약 정보를 비교하면 됩니다.',
       '목표 판정은 TaCZ 탄약 총 50발을 확인합니다. 판정이 완료되어도 서로 다른 탄종을 모든 총에 사용할 수 있는 것은 아닙니다.',
       '귀환할 식량과 예비 탄약을 챙기고 거점 주변부터 익혀 보세요.'], ['first_gun'], count=50, reward=('minecraft:bread', 2), xp=40)
quest('iron_backpack', '여행 가방을 넓히다', 'sophisticatedbackpacks:iron_backpack',
      ['배낭을 철 등급으로 확장해 주세요. 현재 배낭에서 이어지는 정확한 업그레이드 순서를 JEI로 확인하세요.',
       '필요에 따라 줍기·먹이 공급·제작 등의 업그레이드를 추가할 수 있습니다. 가지고 있는 물건과 배낭 내부 공간을 확인하며 확장하세요.'], ['backpack'], reward=('minecraft:bread', 2), xp=40)


def object_id(kind, key):
    value = int.from_bytes(hashlib.sha256(('farmtech/v1/' + kind + '/' + key).encode()).digest()[:8], 'big')
    return f'{value & 0x7fffffffffffffff:016X}'


def encode(value):
    # JSON is a subset of the SNBT syntax accepted by FTB Library.
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def build():
    result = {'data.snbt': dict(version=13, title='FarmTech · 농장과 공장',
        default_reward_team=False, default_consume_items=False, default_autoclaim_rewards='disabled',
        default_quest_shape='square', default_quest_disable_jei=False, drop_loot_crates=False,
        disable_gui=False, grid_scale=0.5, pause_game=False, progression_mode='flexible',
        detection_delay=20, drop_book_on_death=False, show_lock_icons=True),
        'chapter_groups.snbt': {'chapter_groups': []}}
    index = []
    for order, ch in enumerate(CHAPTERS):
        data = dict(id=object_id('chapter', ch['key']), filename=ch['key'], order_index=order,
            title=ch['title'], subtitle=[ch['subtitle']], icon=ch['icon'],
            default_quest_shape='square', default_hide_dependency_lines=False, quests=[])
        for pos, q in enumerate(ch['quests']):
            key = q['key']
            tasks = []
            for j, (item, count) in enumerate([(q['item'], q['count'])] + q['extra']):
                task = dict(id=object_id('task', f'{key}/{j}'), type='item' if item else 'checkmark')
                if item:
                    task.update(item=item, count=count, consume_items=False, match_nbt=False)
                else:
                    task['title'] = '안내를 읽었습니다'
                tasks.append(task)
            rewards = [dict(id=object_id('xp', key), type='xp', xp=q['xp'], team_reward=False)]
            if q['reward']:
                item, count = q['reward']
                rewards.append(dict(id=object_id('reward', key), type='item', item=item,
                                    count=count, team_reward=False))
            data['quests'].append(dict(id=object_id('quest', key), title=q['title'],
                icon=q['item'] or 'ftbquests:book', x=float((pos % 4) * 3), y=float((pos // 4) * 3),
                description=q['text'], dependencies=[object_id('quest', d) for d in q['deps']],
                tasks=tasks, rewards=rewards))
            index.append(dict(key=key, id=object_id('quest', key), chapter=ch['title'],
                              title=q['title'], dependencies=q['deps']))
        result[f'chapters/{ch["key"]}.snbt'] = data
    result = {DEST / name: encode(value) for name, value in result.items()}
    result[ROOT / 'pack/quests-index.json'] = encode(index)
    return result


if __name__ == '__main__':
    check = '--check' in sys.argv
    for path, text in build().items():
        assert '\ufffd' not in text
        if path.exists():
            previous = path.read_bytes().decode('utf-8', errors='strict')
            assert '\ufffd' not in previous
        if check:
            assert path.read_bytes() == text.encode('utf-8'), f'Outdated generated file: {path}'
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode('utf-8'))
            assert path.read_bytes().decode('utf-8') == text
    print(f'{"Verified" if check else "Generated"}: {len(CHAPTERS)} chapters, '
          f'{sum(len(c["quests"]) for c in CHAPTERS)} quests')
