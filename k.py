import pygame
import sys
import math 
import random 

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beach Sunset Animation")

SKY_DAY = (135, 206, 235)
SKY_SUNSET = (255, 140, 0)
SUN = (255, 215, 0)
MOON = (220, 215, 220)
OCEAN_DAY = (0, 105, 148)
OCEAN_NIGHT = (0, 40, )
SUN = (255, 215, 0)
MOON = (220, 215, 220)
OCEAN_DAY = (0, 105, 148)
OCEAN_NIGHT = (0, 40, )

DAY = 0