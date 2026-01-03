import pygame
import math 

class Obstacle:
    def __init__(self, x, ground_y, width=40, height=60):
        self.rect = pygame.Rect(x, ground_y - height, width, height)
        self.color = (255, 50, 50)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class SmallSpike:
    def __init__(self, x, ground_y, size=25):
        self.rect = pygame.Rect(x, ground_y - size, size, size)
        self.color = (255, 50, 50)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        points = [
            (self.rect.left, self.rect.bottom),
            (self.rect.centerx, self.rect.top),
            (self.rect.right, self.rect.bottom),
        ]
        pygame.draw.polygon(screen, self.color, points)

class TriangleObstacle:
    def __init__(self, x, ground_y, size=50):
        self.size = size
        # Collision box (rectangle)
        self.rect = pygame.Rect(
            x,
            ground_y - size,
            size,
            size
        )
        self.color = (255, 50, 50)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        # Triangle points
        points = [
            (self.rect.left, self.rect.bottom),        # bottom-left
            (self.rect.centerx, self.rect.top),         # top
            (self.rect.right, self.rect.bottom)         # bottom-right
        ]

        pygame.draw.polygon(screen, self.color, points)



class StairPlatform:
    def __init__(self, x, y, width=60, height=15):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (120, 200, 255)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)



class Pillar:
    def __init__(self, x, y, width=50, height=80):
        self.rect = pygame.Rect(x, y - height, width, height)
        self.color = (180, 0, 255)
        self.glow_color = (220, 120, 255)

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        # glow
        glow = pygame.Surface(
            (self.rect.width + 10, self.rect.height + 10),
            pygame.SRCALPHA
        )
        glow.fill((*self.glow_color, 80))
        screen.blit(
            glow,
            (self.rect.x - 5, self.rect.y - 5)
        )

        # pillar
        pygame.draw.rect(screen, self.color, self.rect)

class Liquid:
    def __init__(self, x, y, width, height=30):
        self.base_y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 200, 255)
        self.time = 0

    def update(self, speed):
        self.rect.x -= speed
        self.time += 0.1
        wave = math.sin(self.time) * 3
        self.rect.y = self.base_y + wave

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)