from typing import TypedDict
from gene import Animal_Gene
from random import randrange
from setting import *
import pygame
from itertools import count
from meat import Meat, DeadPlant
from plant import Plant

#동물들 위치는 맵에서 관리
#랙완화를 위해 왠만한건 함수만들지말자
#모든 스탯은 최대계수 한계가 있음!  (결국 어떤걸얻으면 다른걸 포기하게)
#기본적으로 얼마나 빠르게움직이냐에따라 에너지가 빨리소모
#animal map, plant_map,...등등 각 맵이있음

#id는 여기서 만들자 저기 gene은 스탯같으면 주소도같아서 id같아지는 일이일어난다


class Animal:
    #이거 상속한곳에서 구현해야함 make_id
    make_id = count(1)
    evol_tree = {}
    survivors = []
    color = (255, 100, 100)

    def __init__(self,parent_gene=None, parent_id=0, pos =None):
        if parent_gene == None:
            self.gene = Animal_Gene()
            self.energy = self.gene.child_energy
        else:
            self.gene = Animal_Gene(parent_gene)
            self.energy = parent_gene.child_energy
        self.id = next(self.make_id)
        self.target = pygame.Vector2(0,0)
        if pos == None:
            self.pos = pygame.Vector2(randrange(WIDTH), randrange(HEIGHT))
        else:
            self.pos =  pygame.Vector2(*pos)
        self.d_pos =  pygame.Vector2(0,0)
        self.running_random = False
        self.nothing_around = True

        self.size = len(self.gene.shape)
        self.life = self.size
        
        self.poison_list = []
        self.poison_time = 0
    
        self.speed = self.gene.speed * SPEED_BALANCE + 0.01

        self.evol_tree[self.id] = parent_id
        self.rect_box = tuple(pygame.Rect(self.pos.x+x*PIXEL_SIZE_ANIMAL, self.pos.y+y*PIXEL_SIZE_ANIMAL,
                                    PIXEL_SIZE_ANIMAL, PIXEL_SIZE_ANIMAL) for x,y in self.gene.shape)#충돌처리를위해RECT모음
        self.sight_size = self.gene.sight * SIGHT_BALACNCE
        self.sight_rect = pygame.Rect(*self.pos, self.sight_size, self.sight_size)

        self.attack_ready = True
        self.attack_cooltime = 0

    def attack(self, object):
        if self.attack_ready:
            object.life -= ANIMAL_DAMAGE
            self.attack_cooltime = ANIMAL_DAMAGE_COOLTIME
            self.attack_ready = False

    def die(self):
        ###죽음관련 매커니즘 
        self.survivors.remove(self)
        for rect in self.rect_box:
            Meat.survivors.append(Meat(col_rect=rect,poison=self.gene.poison))
    #여기사 데미지 쿨타임관리도할꺼임
    def poison_damage(self):
        if self.poison_list and self.poison_time <= 0 :
            poison = self.poison_list.pop()
            if poison > self.gene.poison_res*POISON_RESIST_BALANCE:
                self.life -= POISON_DAMAGE
                self.poison_time = POISON_TIME
        self.poison_time -= 1
        self.attack_cooltime -= 1
        if self.attack_cooltime and not self.attack_ready < 0:
            self.attack_ready = True

    #이거 각자 상속해야하고 return은 백터로
    def find_target(self):
        return pygame.Vector2(randrange(WIDTH), randrange(HEIGHT))
    #이것도 상속해야함
    def collision(self):
        pass

    def move(self):
        ###이동관련###
        self.find_target()
        if self.target.x < 0:
            self.target.x = 0
        elif self.target.x > WIDTH:
            self.target.x = WIDTH
        if self.target.y < 0:
            self.target.y = 0
        elif self.target.y > HEIGHT:
            self.target.y = HEIGHT
        self.d_pos = (self.target - self.pos)
        
        if self.d_pos.length() < self.speed:
            self.pos.x, self.pos.y = self.target.x, self.target.y
            self.running_random = False
        else:
            self.d_pos.scale_to_length(self.speed)
            self.pos = self.pos + self.d_pos
        ###에너지소모###
        self.energy -= self.speed * ANIMAL_ENERGY_EFFICIENT * self.size 
        ###충돌사각형 이동, 시야사각형이동###
        for rect, shape in zip(self.rect_box, self.gene.shape):
            rect.x = self.pos.x + shape[0]*PIXEL_SIZE_ANIMAL
            rect.y = self.pos.y + shape[1]*PIXEL_SIZE_ANIMAL
        self.sight_rect.x = self.pos.x - self.sight_size//2
        self.sight_rect.y = self.pos.y - self.sight_size//2

    def check_dead(self):
        if self.energy < 0 or self.life < 0:
            self.die()

    def breeding(self):
        ###에너지가 해당기준이상이면 자식생성###
        if self.energy > self.gene.child_caution + self.gene.child_energy * self.gene.child_num:
            for _ in range(self.gene.child_num):
                self.survivors.append(type(self)(self.gene, self.id, (self.pos.x, self.pos.y)))
            self.energy = self.gene.child_caution
    def display(self, screen):
        for rect in self.rect_box:
            pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, self.color, self.sight_rect, width=2)
        if self.poison_time > 0:
            pygame.draw.circle(screen, (0, 255,0), self.rect_box[0].center, POISON_EFFECT_SIZE, width=POISON_EFFECT_WIDTH)
    def behaviour(self):
        self.collision()
        self.move()
        self.poison_damage()
        self.breeding()
        self.check_dead()
        


class B_Animal(Animal):
    #이거 상속한곳에서 구현해야함 make_id
    make_id = count(1)
    evol_tree = {}
    survivors = []
    color = (0, 0, 255)

    def find_target(self):
        ###우선순위는 R_animal->DeadPlant->plant->random
        if target_list:=[animal.pos for animal in R_Animal.survivors 
                           if any(self.sight_rect.colliderect(rect) for rect in animal.rect_box)]:
            tar_x, tar_y= min(target_list, key=lambda target_pos: self.pos.distance_squared_to(target_pos))
            self.target.x, self.target.y = self.pos.x +self.pos.x - tar_x, self.pos.y+self.pos.y-tar_y
            self.running_random = False
        elif target_list:=[food.col_rect.center for food in DeadPlant.survivors if self.sight_rect.colliderect(food.col_rect)]:
            self.target.x, self.target.y = min(target_list, key=lambda target_pos: self.pos.distance_squared_to(target_pos))
            self.running_random = False
      ###아직 plant 구현안함 해야함
        elif not self.running_random:
            self.target.x, self.target.y = randrange(WIDTH), randrange(HEIGHT)
            self.running_random = True

    def collision(self):
        #여기서 충돌처리를 식물, 죽은식물 동시해처리
        for rect in self.rect_box:
            pass


class R_Animal(Animal):
    #이거 상속한곳에서 구현해야함 make_id
    make_id = count(1)
    evol_tree = {}
    survivors = []
    color = (255, 0, 0)

    def find_target(self):
        ###우선순위는 Meat->B_Animal->random
        if target_list:=[meat.col_rect.center for meat in Meat.survivors if self.sight_rect.colliderect(meat.col_rect)]:
            self.target.x, self.target.y = min(target_list, key=lambda target_pos: self.pos.distance_squared_to(target_pos))
            self.running_random = False
        elif target_list:=[animal.pos for animal in B_Animal.survivors 
                           if any(self.sight_rect.colliderect(rect) for rect in animal.rect_box)]:
            self.target.x, self.target.y = min(target_list, key=lambda target_pos: self.pos.distance_squared_to(target_pos))
            self.running_random = False
        elif not self.running_random:
            self.target.x, self.target.y = randrange(WIDTH), randrange(HEIGHT)
            self.running_random = True


    def collision(self):
        for rect in self.rect_box:
            #Meat와 충돌구문
            for meat in Meat.survivors:
                if rect.colliderect(meat.col_rect):
                    meat.eaten(self)
            #B_animal과 충돌구문
            for animal in B_Animal.survivors:
                if any(rect.colliderect(other_rect) for other_rect in animal.rect_box):
                    self.attack(animal)
            