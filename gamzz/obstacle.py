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
        self.image = pygame.image.load(
            "assets/img/spike.png"
        ).convert_alpha()

        # Scale image to match size
        self.image = pygame.transform.scale(
            self.image, (size, size)
        )

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
        self.image = pygame.image.load(
            "assets/img/spike.png"
        ).convert_alpha()

        # Scale image to match size
        self.image = pygame.transform.scale(
            self.image, (size, size)
        )

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        
        screen.blit(self.image, self.rect)



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

class JumperPad:
    def __init__(self, x, ground_y, width=50, height=20, boost=-20):
        self.rect = pygame.Rect(
            x,
            ground_y - height,
            width,
            height
        )
        self.jump_force = -18   # 🔥 stronger than normal jump
        self.used = False       # prevents double trigger

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        # base
        pygame.draw.rect(screen, (255, 160, 80), self.rect, border_radius=4)

        # top glow
        glow_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            4
        )
        pygame.draw.rect(screen, (255, 220, 150), glow_rect)

        # arrow / symbol
        cx = self.rect.centerx
        cy = self.rect.centery
        pygame.draw.polygon(
            screen,
            (255, 90, 90),
            [
                (cx - 6, cy + 3),
                (cx + 6, cy + 3),
                (cx, cy - 6)
            ]
        )
