from setting import * 
from random import randrange
import pygame
from itertools import count

#seed에서 생성되고 목표로 날라가는거다
#plant에서 목표 정해준다, 목표만정해주면된다나머지는 Seed에서
class Seed:
    survivors = []
    make_id = count(1)
    evol_tree = {}
    def __init__(self, pos, target, parent_gene=None, parent_id=0):
        self.pos = pygame.Vector2(*pos)
        self.target = pygame.Vector2(*target)
        self.time = 0
        self.gene = parent_gene
        self.id = next(self.make_id)
        self.evol_tree[self.id] = parent_id
        self.throwing = True

    def display(self, screen):
        pygame.draw.rect(screen, SEED_COLOR, (*self.pos, PIXEL_SIZE_SEED, PIXEL_SIZE_SEED))

    def spreading(self):
        self.d_pos = (self.target - self.pos)
        if self.d_pos.length() < SEED_SPEED:
            self.pos.x, self.pos.y = self.target.x, self.target.y
            self.throwing = False
        else:
            self.d_pos.scale_to_length(SEED_SPEED)
            self.pos = self.pos + self.d_pos

        if self.pos.x < 0 or self.pos.x > WIDTH or self.pos.y < 0 or self.pos.y > HEIGHT:
            self.die()
    def die(self):
        self.survivors.remove(self)
    def growing(self):
        self.time += 1
        if self.time > self.gene.seed_time:
            self.grown()
    def grown(self):
        pass
    
    def behaviour(self):
        if self.throwing:
            self.spreading()
        else:
            self.growing()


###ANIMAL 공통으로 attack함수가 구현되있는데 이 attack에서 상대방의 데미지 모션을 줄꺼니까 damage_motion구현해라 display안에
#life라는 변수에 체력이 담겨있어야됨
class Plant:
    survivors = []
    color = PLANT_COLOR

    def __init__(self,parent_gene=None, parent_id=0, pos =None):
        pass