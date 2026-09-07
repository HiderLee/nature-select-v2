
#음... 취소 딕셔너리 쓸꺼임
#각맵에는 있고 없는지만 표시하는  그 맵에 누가있는지를 나타내는 id가존재...  0이면 아무도없음

from setting import *
import pygame
from animal import Animal, R_Animal, B_Animal
from gene import Animal_Gene
from meat import Meat
from random import randrange

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Life Simulator")
clock = pygame.time.Clock()
running = True

for _ in range(5):
    R_Animal.survivors.append(R_Animal())
for _ in range(0):
    B_Animal.survivors.append(B_Animal())
for _ in range(100):
    Meat.survivors.append(Meat(col_rect=pygame.Rect(randrange(WIDTH), randrange(HEIGHT),
                                                    PIXEL_SIZE_ANIMAL, PIXEL_SIZE_ANIMAL),poison=1))
    

cmd = 0
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))

    for a in R_Animal.survivors.copy():
        a.behaviour()
        a.display(screen)
        a.energy += 1

        if a.pos.y > HEIGHT or a.pos.y < 0 or a.pos.x>WIDTH or a.pos.x <0:
            print("좌표는 {self.pos}")

    for a in B_Animal.survivors.copy():
        a.behaviour()
        a.display(screen)
        a.energy += 1
        
    for meat in Meat.survivors.copy():
        meat.display(screen)

    

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()