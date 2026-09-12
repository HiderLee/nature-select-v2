from setting import * 
from random import randrange, uniform
from gene import Plant_Gene
from meat import DeadPlant
import pygame
from itertools import count
import math

#seed에서 생성되고 목표로 날라가는거다
#plant에서 목표 정해준다, 목표만정해주면된다나머지는 Seed에서
class Seed:
    survivors = []
    make_id = count(1)
    evol_tree = {}
    def __init__(self, pos=None, target=None, parent_gene=None, parent_id=0):
        self.pos = pygame.Vector2(randrange(WIDTH), randrange(HEIGHT)) if pos== None else pygame.Vector2(*pos)
        self.target =  pygame.Vector2(randrange(WIDTH), randrange(HEIGHT)) if target== None else pygame.Vector2(*target)
        self.time = 0
        self.gene = Plant_Gene() if parent_gene==None else parent_gene

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
            self.die()
    def grown(self):
        Plant.survivors.append(Plant(parent_gene=self.gene, parent_id=self.id, pos=(self.pos.x, self.pos.y)))
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
        self.gene = Plant_Gene() if parent_gene==None else Plant_Gene(parent_gene)
        self.pos = pygame.Vector2(randrange(WIDTH), randrange(HEIGHT)) if pos ==None else pygame.Vector2(*pos)
        self.current_size = 1
        self.life = 1
        self.full_size = len(self.gene.shape)
        self.growing_time = 0
        self.full_grown = False
        self.energy = 0
        self.rect_box = [pygame.Rect(*self.pos, PIXEL_SIZE_PLANT,PIXEL_SIZE_PLANT)]
        self.id = parent_id
        self.making_seed_energy = MAKE_SEED_ENERGY + self.gene.poison*PLANT_POISON_BALANCE + \
            (self.gene.hot_resist + self.gene.hot_resist)*PLANT_TEMP_BALANCE
        
        self.damage_motion_apear = False
        self.damage_motion_time = 0
        
    def growing(self):
        if self.full_size == self.current_size:
            self.full_grown = True
            return
        self.growing_time += 1
        if self.growing_time > PLANT_GROWING_TIME:
            self.growing_time = 0
            self.rect_box.append(pygame.Rect(self.pos.x + self.gene.shape[self.current_size][0]*PIXEL_SIZE_PLANT,
                                             self.pos.y + self.gene.shape[self.current_size][1]*PIXEL_SIZE_PLANT,
                                             PIXEL_SIZE_PLANT, PIXEL_SIZE_PLANT))
            self.current_size += 1
            self.life += 1

    def make_seed(self):
        if self.energy > self.making_seed_energy:
            for _ in range(self.gene.seed_num):
                angle = uniform(0, math.tau)
                seed_target = pygame.Vector2(self.pos.x + math.cos(angle) * self.gene.seed_radius*SEED_RANGE_BALANCE, 
                                            self.pos.y + math.sin(angle) * self.gene.seed_radius*SEED_RANGE_BALANCE)
                if seed_target.x < 0:
                    seed_target.x = 0
                elif seed_target.x > WIDTH:
                    seed_target.x = WIDTH
                if seed_target.y < 0:
                    seed_target.y = 0
                elif seed_target.y > HEIGHT:
                    seed_target.y = HEIGHT
                Seed.survivors.append(Seed(pos=(self.pos.x, self.pos.y), target=(seed_target.x, seed_target.y),
                                      parent_gene=self.gene, parent_id=self.id))
            self.energy -= self.making_seed_energy
    def produce_energy(self):
        self.energy += self.current_size*PLANT_ENERGY_EFFICIENT

    def die(self):
        self.survivors.remove(self)
        for rect in self.rect_box:
            DeadPlant.survivors.append(DeadPlant(col_rect=rect,poison=self.gene.poison))
    def check_dead(self):
        if self.life < 0:
            self.die()
    def damage_motion(self, screen):
        if self.damage_motion_apear:
            for rect in self.rect_box:
                pygame.draw.rect(screen, DAMAGE_MOTION_COLOR, rect, width=DAMAGE_MOTION_WIDTH)
            self.damage_motion_time += 1
            if self.damage_motion_time > DAMAGE_MOTION_TIME:
                self.damage_motion_time = 0
                self.damage_motion_apear = False
                
    def display(self,screen):
        for rect in self.rect_box:
            pygame.draw.rect(screen, PLANT_COLOR, rect)
    def behaviour(self):
        if not self.full_grown:
            self.growing()
        else:
            self.make_seed()
        self.produce_energy()
        self.check_dead()
