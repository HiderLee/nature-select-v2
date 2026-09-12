from setting import *
from collections.abc import Iterable
import pygame

class BaseMeatPlant:
    survivors = []
    color = (255, 220, 0)
    energy_per_unit = ENERGY_PER_MEAT

    def __init__(self, col_rect, poison): 
        self.col_rect = col_rect
        self.poison = poison

    def eaten(self, consumer):
        self.survivors.remove(self)
        consumer.energy += self.energy_per_unit
        if self.poison > 0:
            consumer.poison_list.append(self.poison)

    def display(self, screen):
        pygame.draw.rect(screen, self.color, self.col_rect)

class Meat(BaseMeatPlant):
    survivors = []
    color = (255, 220, 0)
    energy_per_unit = ENERGY_PER_MEAT

class DeadPlant(BaseMeatPlant):
    survivors = []
    color = (100, 100, 100)
    energy_per_unit = ENERGY_PER_PLANT
