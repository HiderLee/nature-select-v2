from setting import * 
from random import randrange

#seed에서 plant요소를 가지고있다가 (따로) 부화할때 딱 plant.survivors에 추가하는게 효울작이긴할듯
class Seed:
    color = SEED_COLOR
    def __init__(self):
        pass



###ANIMAL 공통으로 attack함수가 구현되있는데 이 attack에서 상대방의 데미지 모션을 줄꺼니까 damage_motion구현해라 display안에
#life라는 변수에 체력이 담겨있어야됨
class Plant:
    pass