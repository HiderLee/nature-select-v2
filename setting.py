#윈도우 크기
WIDTH, HEIGHT = 1000, 600
FPS = 30


### 유전자 관련 세팅들 ###
#유전자 변이확률 1~10 확률크기
MUTE_PER = 2
#유전자 변이할시 얼마나 크게 변할지 1~10 클수록 많이커짐
MUTE_CHANGE = 1



### 먹이  관련 ###
#MEAT 하나당 에너지양
ENERGY_PER_MEAT = 90
#dead_plant 하나당 에너지양
ENERGY_PER_PLANT = 90
#독데미지 밸런스
POISON_DAMAGE = 0.2
#독쿨타임(여러개 먹은경우 다음 독뎀까지 얼마나 걸릴지 30프레임으로 30당 1초)
POISON_TIME = 150
#독 효과 크기, 굵기
POISON_EFFECT_SIZE = 15
POISON_EFFECT_WIDTH = 5



### 동물 관련 ###
#동물 픽셀 크기
PIXEL_SIZE_ANIMAL = 10
#동물 데미지모션 크기, 굵기, 색깔, 표시시간
DAMAGE_MOTION_SIZE = 15
DAMAGE_MOTION_WIDTH = 2
DAMAGE_MOTION_COLOR = (255,255,255)
DAMAGE_MOTION_TIME = 30
#동물에너지효율(높을수록 에너지 빠르게소모)
ANIMAL_ENERGY_EFFICIENT = 0.4
#ANIMAL의 데미지, 데미지쿨타임
ANIMAL_DAMAGE = 1
ANIMAL_DAMAGE_COOLTIME = 30



### 식물관련 ###
#씨앗하고 식물 픽셀크기
PIXEL_SIZE_SEED = 4
PIXEL_SIZE_PLANT = 5
#Plant가 한픽셀성장하는데 드는시간
PLANT_GROWING_TIME = 300
#씨앗, 식물,색갈
SEED_COLOR = (100, 100, 0)
PLANT_COLOR = (0,255,0)
#씨앗날라가는속도
SEED_SPEED = 3
#씨앗을만드는데 드는 에너지
MAKE_SEED_ENERGY = 100
#식물에너지효울밸런스
PLANT_ENERGY_EFFICIENT = 1



#동물 스탯밸패 (높을수록 사기가됨)
SPEED_BALANCE = 0.5
SIGHT_BALACNCE = 3
POISON_RESIST_BALANCE = 0.5

#식물스탯밸패
SEED_RANGE_BALANCE = 10
PLANT_POISON_BALANCE = 5
PLANT_TEMP_BALANCE = 3