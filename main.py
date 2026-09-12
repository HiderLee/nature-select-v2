import pygame
from ui import Simulator


simulator = Simulator()
while simulator.running:
    simulator.main_roop()
pygame.quit()