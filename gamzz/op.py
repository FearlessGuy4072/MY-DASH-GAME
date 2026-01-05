import pygame
import sys
import random
from obstacle import SmallSpike ,TriangleObstacle, StairPlatform
from player import Player

obstacles = []

def spawn_triple_small_spikes(x, ground_y):
    spacing = 28
    for i in range(3):
      obstacles.append(
            SmallSpike(x + i * spacing, ground_y + 40, size=25)
        )