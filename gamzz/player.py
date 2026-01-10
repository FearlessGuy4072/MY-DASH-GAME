import pygame
class Player:
    def __init__(self, x, ground_y):
        # -------- ROTATION --------
        self.angle = 0
        self.rotation_speed = 8   # degrees per frame

        self.size = 40

        # Collision rect (IMPORTANT: collision is still rect-based)
        self.rect = pygame.Rect(x, ground_y, self.size, self.size)

        # Physics
        self.velocity_y = 0
        self.gravity = 1
        self.jump_strength = -15
        self.ground_y = ground_y

        # State
        self.state = "run"   # run, jump, skid
        self.on_ground = False

        # -------- PLAYER ICON --------
        self.icon = pygame.image.load(
            "assets/img/icon2.png"
        ).convert_alpha()
        self.icon = pygame.transform.scale(
            self.icon, (self.size, self.size)
        )
      

    # ---------------- ACTIONS ----------------
    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

    # ---------------- UPDATE ----------------
    def update(self):
    # Gravity
     self.velocity_y += self.gravity
     self.rect.y += self.velocity_y

    # Ground collision
     if self.rect.bottom >= self.ground_y + self.size:
        if not self.on_ground:
            self.state = "skid"
            self.skid_frame_index = 0

        self.rect.bottom = self.ground_y + self.size
        self.velocity_y = 0
        self.on_ground = True

        # RESET rotation when on ground
        self.angle = 0
     else:
        self.on_ground = False
        self.state = "jump"

        # ROTATE while jumping
        self.angle = (self.angle - self.rotation_speed) % 360

    # ---------------- DRAW ----------------
    def draw(self, screen):
        # ROTATE icon
        rotated_icon = pygame.transform.rotate(self.icon, self.angle)
        icon_rect = rotated_icon.get_rect(center=self.rect.center)

        # DRAW
        screen.blit(rotated_icon, icon_rect.topleft)
    def reset(self):
        self.rect.x = 100
        self.rect.bottom = self.ground_y + 40
        self.velocity_y = 0
        self.on_ground = True
        self.angle = 0
    def set_icon(self, image):
        self.image = image
