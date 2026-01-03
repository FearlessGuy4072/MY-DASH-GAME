import pygame
import sys
import random

from player import Player
from obstacle import TriangleObstacle , SmallSpike, Pillar, Liquid

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/sound/bgsound.mp3")
pygame.mixer.music.set_volume(0.0)  # 0.0 → 1.0


# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Dash Game")
clock = pygame.time.Clock()
level_start_time = 0


# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

# ---------------- FONT ----------------
font = pygame.font.SysFont(None, 48)

# ---------------- GAME STATE ----------------
state = "menu"

# ---------------- BUTTON ----------------
button_rect = pygame.Rect(300, 250, 200, 60)

# ---------------- GROUND ----------------
ground_y = 450
obstacle_speed = 6
GAME_SPEED = 6

# ---------------- PLAYER ----------------
player = Player(100, ground_y)

def scale_to_width(img, width):
    w, h = img.get_size()
    scale = width / w
    return pygame.transform.scale(img, (int(w * scale), int(h * scale)))

bg_back = pygame.image.load("assets/img/bg2.png").convert()
bg_front = pygame.image.load("assets/img/pbg3.png").convert_alpha()

bg_back = scale_to_width(bg_back, WIDTH)
bg_front = scale_to_width(bg_front, WIDTH)

# -------- PARALLAX IMAGES -------- = pygame.image.load("assets/img/pbg1.png").convert()
pbg2 = pygame.image.load("assets/img/pbg2.png").convert_alpha()
pbg3 = pygame.image.load("assets/img/pbg3.png").convert_alpha()

# X positions
back_x1 = 0
back_x2 = bg_back.get_width()

front_x1 = 0
front_x2 = bg_front.get_width()

# Y positions
bg_back_y = 40
bg_front_y = ground_y + 40  # aligns with gameplay floor


back_speed = 2        # slow sky/building
front_speed = GAME_SPEED

# -------- PARALLAX POSITIONS --------



mid_x1 = 0
mid_x2 = pbg2.get_width()

near_x1 = 0
near_x2 = pbg3.get_width()



# ---------------- BACKGROUND ----------------
bg_img = pygame.image.load("assets/img/bg2.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
particles = []



def kill_player():
    global state
    pygame.mixer.music.stop()

    state = "menu"


def reset_game():
    global obstacles
    global level_start_time
    global pattern_index
    global spawn_locked
    global particles

    obstacles.clear()
    particles.clear()

    level_start_time = pygame.time.get_ticks()
    pattern_index = 0
    spawn_locked = False


# ---------------- OBSTACLES ----------------
def spawn_triple_small_spikes(x, ground_y):
    spacing = 28
    for i in range(3):
        obstacles.append(
            SmallSpike(x + i * spacing, ground_y + 40, size=25)
        )
def spawn_big_spike(x, ground_y):
    obstacles.append(
        TriangleObstacle(x, ground_y + 40)
    )


obstacles = []

pattern_index = 0
PATTERN_TIME = 10_000  # 10 seconds
fixed_patterns = [
    "big",
    "small3",
    "big",
    "big",
    "small3",
    "big",
    "small3",
    "big",
]

def spawn_pillar_liquid_section(x, ground_y):
    pillar_width = 50
    base_height = 80
    height_step = 20

    gap_width = 90       # 🔥 INCREASED GAP (was ~60)
    liquid_width = 60    # liquid smaller than gap
    liquid_offset = (gap_width - liquid_width) // 2
    liquid_raise = 35
    liquid_height = 25

    count = 2
    current_x = x

    for i in range(count):
        pillar_height = base_height + i * height_step

        # ---- PILLAR ----
        obstacles.append(
            Pillar(
                current_x,
                ground_y + 40,
                pillar_width,
                pillar_height
            )
        )

        # ---- LIQUID (centered in gap) ----
        if i < count - 1:
         obstacles.append(
            Liquid(
                current_x + pillar_width + liquid_offset,
                ground_y + 40 - liquid_raise,
                liquid_width,
                height=liquid_height
            )
        )

        current_x += pillar_width + gap_width





OBSTACLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_EVENT, 1400)

# ===================== GAME LOOP =====================
while True:
    # -------- EVENTS --------
    for event in pygame.event.get():
          
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # MENU CLICK
        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                state = "game"
                reset_game()
                pygame.mixer.music.play(-1)  # Loop indefinitely
        # JUMP
        if state == "game" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

        # SPAWN OBSTACLE
        if state == "game" and event.type == OBSTACLE_EVENT:

            elapsed_time = pygame.time.get_ticks() - level_start_time

    # FIRST 15 SECONDS → FIXED PATTERNS
            if elapsed_time < PATTERN_TIME:

                pattern = fixed_patterns[pattern_index]

                if pattern == "big":
                    spawn_big_spike(WIDTH, ground_y)

                elif pattern == "small3":
                    spawn_triple_small_spikes(WIDTH, ground_y)
                
        # move to next pattern
                pattern_index += 1

        # loop pattern list safely
                if pattern_index >= len(fixed_patterns):
                    pattern_index = 0
    # 10–20s → STAIR + LIQUID SECTION
            elif 10_000 <= elapsed_time < 15_000:
                    spawn_pillar_liquid_section(WIDTH, ground_y)       
    # AFTER 20s → (optional later)
            else:
                pass

    # -------- UPDATE --------
    if state == "game":
        # ===== STEP 2: PARALLAX BACKGROUND UPDATE =====
        # ---- MOVE BACKGROUND ----
        back_x1 -= back_speed
        back_x2 -= back_speed

        if back_x1 <= -bg_back.get_width():
            back_x1 = bg_back.get_width()
        if back_x2 <= -bg_back.get_width():
            back_x2 = bg_back.get_width()

# ---- MOVE FOREGROUND ----
        front_x1 -= front_speed
        front_x2 -= front_speed

        if front_x1 <= -bg_front.get_width():
            front_x1 = bg_front.get_width()
        if front_x2 <= -bg_front.get_width():
            front_x2 = bg_front.get_width()

        player.update()
        player_on_pillar = False

        for obs in obstacles[:]:
            obs.update(obstacle_speed)
            if obs.rect.right < 0:
                obstacles.remove(obs)
                  # LAND ON STAIR
            if isinstance(obs,  Pillar):
                 if player.rect.bottom <= obs.rect.top + 10 and \
                    player.rect.colliderect(obs.rect):
                     player.rect.bottom = obs.rect.top
                     player.velocity_y = 0
                     player.on_ground = True
                     player_on_pillar = True


            if player.rect.colliderect(obs.rect):
                state = "menu"
                # FALL INTO LIQUID = GAME OVER
        for obs in obstacles:
            if isinstance(obs, Liquid):
                if player.rect.colliderect(obs.rect) and not player_on_pillar:
                    kill_player()
                    break

    # -------- DRAW --------
    if state == "menu":
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, button_rect)
        text = font.render("START", True, WHITE)
        screen.blit(text, text.get_rect(center=button_rect.center))

    elif state == "game":
        screen.blit(bg_back, (back_x1, bg_back_y))
        screen.blit(bg_back, (back_x2, bg_back_y))

    # ---- FOREGROUND (ground) ----
        screen.blit(bg_front, (front_x1, bg_front_y))
        screen.blit(bg_front, (front_x2, bg_front_y))


        for obs in obstacles:
            obs.draw(screen)

        player.draw(screen)

        pygame.draw.line(
            screen, WHITE,
            (0, ground_y + 40),
            (WIDTH, ground_y + 40),
            2
        )

    pygame.display.flip()
    clock.tick(60)
