from setting import *
from collections.abc import Iterable
import pygame

class BaseMeatPlant:
    survivors = []
    color = (255, 220, 0)

    def __init__(self, col_rect, poison): 
        self.col_rect = col_rect
        self.poison = poison

    def eaten(self, consumer):
        self.survivors.remove(self)
        consumer.energy += ENERGY_PER_MEAT
        if self.poison > 0:
            consumer.poison_list.append(self.poison)

    def display(self, screen):
        pygame.draw.rect(screen, self.color, self.col_rect)

class Meat(BaseMeatPlant):
    survivors = []
    color = (255, 220, 0)

class DeadPlant(BaseMeatPlant):
    survivors = []
    color = (100, 100, 100)
