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
        self.hitbox = self.rect.inflate(-10, -10)
        self.image = pygame.image.load(
            "assets/img/spike.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, (size, size)
        )

    def update(self, speed):
        self.rect.x -= speed
        self.hitbox.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class TriangleObstacle:
    def __init__(self, x, ground_y, size=50):
        self.size = size
        
        self.rect = pygame.Rect(
            x,
            ground_y - size,
            size,
            size
        )
        self.hitbox = self.rect.inflate(-10, -10)
        self.image = pygame.image.load(
            "assets/img/spike.png"
        ).convert_alpha()
        
        self.image = pygame.transform.scale(
            self.image, (size, size)
        )

    def update(self, speed):
        self.rect.x -= speed
        self.hitbox.center = self.rect.center

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
        self.hitbox = self.rect.inflate(-12, -6)
        
        self.image = pygame.image.load(
            "assets/img/pillar.png"
        ).convert_alpha()
        
        self.image = pygame.transform.smoothscale(
            self.image,
            (width, height)
        )

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Liquid:
    def __init__(self, x, y, width, height=30):
        self.base_y = y
        self.rect = pygame.Rect(x, y, width, height)
        self.hitbox = self.rect.inflate(-10, -10)
        self.image = pygame.image.load(
            "assets/img/liquid.png"
        ).convert_alpha()

        self.image = pygame.transform.scale(
            self.image, (width, height)
        )

        self.time = 0

    def update(self, speed):
        self.rect.x -= speed
        self.hitbox.center = self.rect.center
        self.time += 0.1
        wave = math.sin(self.time) * 3
        self.rect.y = self.base_y + wave

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class JumperPad:
    def __init__(self, x, ground_y, width=50, height=20, boost=-20):
        self.rect = pygame.Rect(
            x,
            ground_y - height,
            width,
            height
        )
        self.jump_force = -18  
        self.used = False
    
        self.arrow_offset = 0
        self.arrow_dir = 1
        self.arrow_speed = 0.4     

    def update(self, speed):
        self.rect.x -= speed

        self.arrow_offset += self.arrow_dir * self.arrow_speed
        if abs(self.arrow_offset) > 6:
            self.arrow_dir *= -1

    def draw(self, screen):
        # base
        pygame.draw.rect(screen, (255, 160, 80), self.rect, border_radius=4)
        glow_rect = pygame.Rect(
            self.rect.x,
            self.rect.y,
            self.rect.width,
            4
        )
        pygame.draw.rect(screen, (255, 220, 150), glow_rect)

        cx = self.rect.centerx
        base_y = self.rect.top - 10 + self.arrow_offset

        arrow_points = [
        (cx, base_y - 12),       
        (cx - 8, base_y),         
        (cx + 8, base_y)          
                        ]

        pygame.draw.polygon(screen, (255, 255, 255), arrow_points)
class Flag:
    def __init__(self, x, ground_y):
        self.image = pygame.image.load(
            "assets/img/flag.png"
        ).convert_alpha()

        self.image = pygame.transform.smoothscale(self.image, (60, 90))

        self.rect = self.image.get_rect(
            bottomleft=(x, ground_y + 40)
        )

    def update(self, speed):
        self.rect.x -= speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)


