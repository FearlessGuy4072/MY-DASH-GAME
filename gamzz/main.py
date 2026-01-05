from cmath import rect
import pygame
import sys
import random

from player import Player
from obstacle import JumperPad, TriangleObstacle , SmallSpike, Pillar, Liquid ,JumperPad

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/sound/bgsound1.mp3")
pygame.mixer.music.set_volume(0.3)  # 0.0 → 1.0


# ---------------- WINDOW ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
temp_surface = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption("My Dash Game")
clock = pygame.time.Clock()
level_start_time = 0
GAME_START_DELAY = 0_000   # 15 seconds in milliseconds
attempts = 0




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

# -------- SPEED & ZOOM TRANSITION --------
BASE_SPEED = 6
FAST_SPEED = 7
obstacle_speed = BASE_SPEED

speed_boost_time = 16_000  # ms (16 sec)
speed_transition_duration = 1000  # 1 sec

zoom = 1.0
zoom_target = 1.0
zoom_speed = 0.15
zoom_timer = 0
ZOOM_DURATION = 400 # milliseconds

speed_boost_started = False

restart_btn = pygame.Rect(300, 200, 200, 50)
menu_btn    = pygame.Rect(300, 270, 200, 50)
vol_up_btn  = pygame.Rect(300, 340, 95, 50)
vol_dn_btn  = pygame.Rect(405, 340, 95, 50)



# ---------------- BACKGROUND ----------------
bg_img = pygame.image.load("assets/img/bg2.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT+200))
particles = []


def draw_ui(screen, font, attempts):
    text = font.render(f"Attempts: {attempts}", True, (255, 255, 255))
    screen.blit(text, (20, 10))

def kill_player():
    global state , attempts
    pygame.mixer.music.stop()
    attempts += 1

    state = "menu"


def reset_game():
    global obstacles
    global obstacle_speed
    global zoom
    global zoom_target
    global speed_boost_started
    global level_start_time
    global pattern_index
    global spawn_locked
    global jumper_pattern_spawned
    jumper_pattern_spawned = False

    obstacle_speed = BASE_SPEED
    zoom = 1.0
    zoom_target = 1.0
    speed_boost_started = False
    level_start_time = pygame.time.get_ticks()

    obstacles.clear()
    particles.clear()

    pattern_index = 0
    spawn_locked = False

    player.reset()



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
    pillar_width = 60
    base_height = 80
    height_step = 20

    gap_width = 90       
    liquid_width = 60    
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
def spawn_pillar_spike_pattern(x, ground_y):
    spacing = 100
    obstacles.append(TriangleObstacle(x-140, ground_y + 40))
    obstacles.append(TriangleObstacle(x-100, ground_y + 40))
    
    obstacles.append(
        TriangleObstacle(x-60, ground_y + 40)
    )
    obstacles.append(
        Pillar(x, ground_y + 40, height=60, width=80)
    )

def spawn_jumper_pillar_pattern(start_x, ground_y):
    spacing = 120
    LIQUID_HEIGHT = 30
    x = start_x

    # 1️⃣ Jumper Pad
    obstacles.append(JumperPad(x, ground_y+20))
    x += spacing + 80

    # 2️⃣ Large Pillar
    big_pillar = Pillar(x, ground_y+40, height=160, width=120)
    obstacles.append(big_pillar)
    x += big_pillar.rect.width + 30

    # 3️⃣ Liquid gap
    obstacles.append(
        Liquid(
            x-10,
            ground_y+10,
            width=120,
            height=LIQUID_HEIGHT
        )
    )
    x += 60 + spacing

    # 4️⃣ Small Pillar
    small_pillar = Pillar(x-20, ground_y+40, height=100, width=120)
    obstacles.append(small_pillar)
    x += small_pillar.rect.width + 30

    # 5️⃣ Jumper Pad
    obstacles.append(JumperPad(x+50, ground_y-10))
       

    # 6️⃣ Liquid gap
    obstacles.append(
        Liquid(
            x-20,
            ground_y+10,
            width=200,
            height=LIQUID_HEIGHT
        )
    )
    x +=  spacing+60

    # 7️⃣ Medium Pillar
    obstacles.append(Pillar(x, ground_y+40, height=140, width=80))



OBSTACLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(OBSTACLE_EVENT, 1400)

# ===================== GAME LOOP =====================
while True:
    # -------- EVENTS --------
    for event in pygame.event.get():
          
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if state == "game":
                    state = "settings"
                elif state == "settings":
                    state = "game"

        # MENU CLICK
        if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                state = "game"
                reset_game()
                pygame.mixer.music.play(-1)  # Loop indefinitely
        # JUMP
        if state == "game" and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button;
                player.jump()

        # SPAWN OBSTACLE
        if state == "game" and event.type == OBSTACLE_EVENT:

            elapsed_time = pygame.time.get_ticks() - level_start_time

    # FIRST 15 SECONDS → FIXED PATTERNS
            if elapsed_time < GAME_START_DELAY:
                pass
            elif elapsed_time < 10_000:
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
            elif 10_000 <= elapsed_time < 12_000:
                if not spawn_locked:
                    spawn_pillar_liquid_section(WIDTH, ground_y)
                    spawn_locked = True
            elif 12_000 <= elapsed_time < 16_000:
                if spawn_locked:
                    spawn_pillar_liquid_section(WIDTH , ground_y)
                    spawn_locked = False
                    spawn_pillar_spike_pattern(WIDTH + 400, ground_y)       
    # AFTER 20s → (optional later)
            if elapsed_time >= 16_000 and not speed_boost_started:
                obstacle_speed += 2
                zoom_target = 1.15      # zoom in
                zoom_timer = pygame.time.get_ticks()
                speed_boost_started = True

            elif 17_000 <= elapsed_time < 20_000:
                if not jumper_pattern_spawned:
                    spawn_jumper_pillar_pattern(WIDTH, ground_y)
                    jumper_pattern_spawned = True

            else:
                pass
                

    # -------- UPDATE --------
    if state == "game":
        elapsed_time = pygame.time.get_ticks() - level_start_time

    # ---- SPEED + ZOOM TRANSITION ----
        if elapsed_time >= speed_boost_time:
            if not speed_boost_started:
                speed_boost_started = True
                speed_start_time = pygame.time.get_ticks()

                zoom_target = 1.08
                zoom_timer = pygame.time.get_ticks()


    # Smooth speed increase
            t = min(
                (pygame.time.get_ticks() - speed_start_time) / speed_transition_duration,
                    1
                    )
            obstacle_speed = BASE_SPEED + (FAST_SPEED - BASE_SPEED) * t

    # Smooth zoom
        # Smooth zoom interpolation
        zoom += (zoom_target - zoom) * zoom_speed

# Auto reset zoom after duration
        if zoom_target > 1.0:
            if pygame.time.get_ticks() - zoom_timer > ZOOM_DURATION:
                zoom_target = 1.0

            

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
                continue
    # ================= JUMPER PAD =================
            if isinstance(obs, JumperPad):
                if player.rect.colliderect(obs.rect):
                    if player.velocity_y >= 0 and player.rect.bottom <= obs.rect.centery:
                        player.velocity_y = obs.jump_force
                        player.on_ground = False
                continue  # ✅ continue ONLY for jumper
    # ================= PILLAR (LANDING) =================
            
            if isinstance(obs, Pillar):
                if player.rect.colliderect(obs.rect):

        # ✅ LANDING FROM TOP (safe)
                    if (
            player.velocity_y >= 0 and
            player.rect.bottom <= obs.rect.top + 12
        ):
                        player.rect.bottom = obs.rect.top
                        player.velocity_y = 0
                        player.on_ground = True
                        continue

        # ❌ HIT FROM SIDE or BOTTOM → DIE
                    kill_player()
                    break

    # ================= REAL HAZARDS =================
            if isinstance(obs, (TriangleObstacle, SmallSpike, Liquid)):
                if player.rect.colliderect(obs.rect):
                    kill_player()
                    break

        
    # -------- DRAW --------
    world_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


    if state == "menu":
        screen.fill(BLACK)
        pygame.draw.rect(screen, BLUE, button_rect)
        text = font.render("START", True, WHITE)
        screen.blit(text, text.get_rect(center=button_rect.center))


    elif state == "game":

    # -------------------------
    # CLEAR WORLD EACH FRAME
    # -------------------------
        world_surface.fill((36, 41, 92))  # sky color

    # ---- BACKGROUND ----
        world_surface.blit(bg_back, (back_x1, bg_back_y))
        world_surface.blit(bg_back, (back_x2, bg_back_y))

        world_surface.blit(bg_front, (front_x1, bg_front_y))
        world_surface.blit(bg_front, (front_x2, bg_front_y))

    # ---- OBSTACLES ----
        for obs in obstacles:
            obs.draw(world_surface)

    # ---- PLAYER ----
        player.draw(world_surface)

    # -------------------------
    # APPLY ZOOM (WORLD ONLY)
    # -------------------------
        scaled_world = pygame.transform.smoothscale(
        world_surface,
        (int(WIDTH * zoom), int(HEIGHT * zoom))
    )

        world_rect = scaled_world.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(scaled_world, world_rect)

    # -------------------------
    # UI (NO ZOOM)
    # -------------------------
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, 40))
        draw_ui(screen, font, attempts)


    elif state == "settings":
        screen.fill((20, 20, 20))

        def draw_btn(rect, text):
            pygame.draw.rect(screen, (80, 80, 80), rect)
            t = font.render(text, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=rect.center))

        draw_btn(restart_btn, "Restart")
        draw_btn(menu_btn, "Main Menu")
        draw_btn(vol_up_btn, "Vol +")
        draw_btn(vol_dn_btn, "Vol -")

    pygame.display.flip()
    clock.tick(60)
