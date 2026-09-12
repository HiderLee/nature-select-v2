"""
여기에 기본세팅, 루프에들어갈명령어,  저장매커니즘, 정보뜨는시스템, 등등등....실행에필요한모든걸 정리할것이다
"""
import pygame
from animal import B_Animal, R_Animal
from plant import Seed, Plant
from meat import Meat, DeadPlant
from setting import *
from random import randrange
from gene import Plant_Gene

class Simulator:
    def __init__(self):
        self.pause = False
        self.running = True


        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Life Simulator")
        for _ in range(5):
            R_Animal.survivors.append(R_Animal())
        for _ in range(20):
            B_Animal.survivors.append(B_Animal())
        for _ in range(50):
            Plant.survivors.append(Plant(parent_gene=Plant_Gene()))


    def main_roop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.pause_event(event=event)

        if not self.pause:
            self.creature_roop()

        pygame.display.flip()
        self.clock.tick(FPS)

    def creature_roop(self):
        self.screen.fill((0, 0, 0))
        for r_animal in R_Animal.survivors.copy():
            r_animal.behaviour()
            r_animal.display(self.screen)
        for b_animal in B_Animal.survivors.copy():
            b_animal.behaviour()
            b_animal.display(self.screen)
        for seed in Seed.survivors.copy():
            seed.behaviour()
            seed.display(self.screen)
        for plant in Plant.survivors.copy():
            plant.behaviour()
            plant.display(self.screen)
        for meat in Meat.survivors.copy():
            meat.display(self.screen)

    def pause_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.pause = not self.pause

    def save_file(self):
        pass

