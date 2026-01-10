from cmath import rect
import pygame
import sys
import random
import math



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

from player import Player 
from obstacle import JumperPad, TriangleObstacle , SmallSpike, Pillar, Liquid , Flag


# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)

# ---------------- FONT ----------------
font = pygame.font.SysFont(None, 48)

# ---------------- GAME STATE ----------------
state = "menu"


# ---------------- BUTTON ----------------
button_rect = pygame.Rect(0, 0, 250, 80)
button_rect.center = (WIDTH // 2, 380)

label = font.render("Select Player", True, (180, 180, 200))

# ---------------- GROUND ----------------
ground_y = 450
obstacle_speed = 6
GAME_SPEED = 6
level_start_time = 0
GAME_START_DELAY = 0_000   # 15 seconds in milliseconds
attempts = 1
WORLD_SPEED = GAME_SPEED



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

text_img = pygame.image.load("assets/img/text.png").convert_alpha()
text_img = pygame.transform.scale(text_img, (270, 90))  # adjust size
title_img = pygame.image.load("assets/img/title.png").convert_alpha()

# Optional: scale it to fit nicely
title_img = pygame.transform.smoothscale(title_img, (420, 90))

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
text_x = WIDTH + 50
text_y = bg_front_y - 170   # above ground / building
text_active = False

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
SPEED_BOOST_DURATION = 3000  # ms
speed_boost_end_time = 0

zoom = 1.0
zoom_target = 1.08
zoom_speed = 0.12
zoom_timer = pygame.time.get_ticks()
ZOOM_DURATION = 400 # milliseconds
zoom_triggered = False

speed_boost_started = False
icon_y = 240
icon_left_btn  = pygame.Rect(WIDTH//2 - 120, icon_y - 20, 40, 40)
icon_right_btn = pygame.Rect(WIDTH//2 + 80,  icon_y - 20, 40, 40)



player_icons = [
    pygame.image.load("assets/img/icon1.png").convert_alpha(),
    pygame.image.load("assets/img/icon2.png").convert_alpha(),
    pygame.image.load("assets/img/icon3.png").convert_alpha(),
]

player_icons = [
    pygame.transform.smoothscale(img, (40, 40))
    for img in player_icons
]

start_img = pygame.image.load("assets/img/start.png").convert_alpha()

# scale if needed
start_img = pygame.transform.smoothscale(start_img, (220, 70))
start_rect = start_img.get_rect(center=(WIDTH // 2, 380))


selected_icon_index = 0
dropdown_open = False

# Buttons
start_btn = pygame.Rect(300, 360, 200, 60)
dropdown_btn = pygame.Rect(300, 260, 200, 45)

# Dropdown items
dropdown_items = []
for i in range(len(player_icons)):
    dropdown_items.append(
        pygame.Rect(300, 305 + i * 45, 200, 45)
    )


restart_btn = pygame.Rect(300, 200, 200, 50)
menu_btn    = pygame.Rect(300, 270, 200, 50)
vol_up_btn  = pygame.Rect(300, 340, 95, 50)
vol_dn_btn  = pygame.Rect(405, 340, 95, 50)

# ---------------- BACKGROUND ----------------
you_died_img = pygame.image.load("assets/img/you_died.png").convert_alpha()
retry_img    = pygame.image.load("assets/img/retry.png").convert_alpha()
menu_img     = pygame.image.load("assets/img/menu.png").convert_alpha()

# Optional scaling (adjust if needed)
you_died_img = pygame.transform.smoothscale(you_died_img, (260, 60))
retry_img    = pygame.transform.smoothscale(retry_img, (120, 50))
menu_img     = pygame.transform.smoothscale(menu_img, (120, 50))

bg_img = pygame.image.load("assets/img/bg2.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT+200))
particles = []

number_imgs = {}

for i in range(10):
    img = pygame.image.load(
        f"assets/img/numbers/{i}.png"
    ).convert_alpha()
    img = pygame.transform.smoothscale(img, (32, 40))
    number_imgs[str(i)] = img


attempt_img = pygame.image.load(
    "assets/img/attempt_bar.png"
).convert_alpha()

BAR_HEIGHT = 60   # choose what looks good



scale = 0.35
w, h = attempt_img.get_size()
attempt_img = pygame.transform.smoothscale(attempt_img, (int(w * scale), int(h * scale)))

def draw_attempts(screen, attempts, x, y):
    text = str(attempts)
    offset = 0

    for ch in text:
        img = number_imgs[ch]
        screen.blit(img, (x + offset-5, y+6))
        offset += img.get_width() + 2

def draw_menu(screen):
    screen.fill((20, 20, 30))

    # ----- GAME TITLE -----
    title_font = pygame.font.SysFont(None, 72)
    title = title_font.render("MY DASH GAME", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))

    # ----- DROPDOWN BUTTON -----
    pygame.draw.rect(screen, (60, 60, 80), dropdown_btn, border_radius=8)
    screen.blit(
        player_icons[selected_icon_index],
        (dropdown_btn.x + 10, dropdown_btn.y + 3)
    )

    arrow = font.render("▼", True, (255, 255, 255))
    screen.blit(arrow, (dropdown_btn.right - 30, dropdown_btn.y + 8))

    # ----- DROPDOWN OPTIONS -----
    if dropdown_open:
        for i, rect in enumerate(dropdown_items):
            pygame.draw.rect(screen, (80, 80, 110), rect, border_radius=6)
            screen.blit(player_icons[i], (rect.x + 10, rect.y + 3))

    # ----- START BUTTON -----
    pygame.draw.rect(screen, (0, 170, 90), start_btn, border_radius=10)
    start_text = font.render("START", True, (0, 0, 0))
    screen.blit(start_text, start_text.get_rect(center=start_btn.center))


def draw_ui(screen, font, attempts):
    # ATTEMPT label
    label_x = 20
    label_y = 6

    screen.blit(attempt_img, (label_x, label_y))

    # Draw attempt number digit-by-digit
    digits = str(attempts)
    x = label_x + attempt_img.get_width() + 8
    y = label_y + attempt_img.get_height() // 2

    for d in digits:
        digit_img = number_imgs[d]
        rect = digit_img.get_rect(midleft=(x, y))
        screen.blit(digit_img, rect)
        x += rect.width + 3

def draw_retry_panel(screen):
    panel_w, panel_h = 360, 200
    panel_rect = pygame.Rect(
        (WIDTH - panel_w) // 2,
        (HEIGHT - panel_h) // 2,
        panel_w,
        panel_h
    )

    # Panel background
    pygame.draw.rect(screen, (20, 20, 30), panel_rect, border_radius=14)
    pygame.draw.rect(screen, (255, 255, 255), panel_rect, 2, border_radius=14)

    # ---- YOU DIED IMAGE ----
    title_rect = you_died_img.get_rect(
        center=(panel_rect.centerx, panel_rect.y + 40)
    )
    screen.blit(you_died_img, title_rect)

    # ---- BUTTONS ----
    retry_btn = retry_img.get_rect(
        center=(panel_rect.x + panel_w * 0.3, panel_rect.y + 140)
    )
    menu_btn = menu_img.get_rect(
        center=(panel_rect.x + panel_w * 0.7, panel_rect.y + 140)
    )

    screen.blit(retry_img, retry_btn)
    screen.blit(menu_img, menu_btn)

    return retry_btn, menu_btn


    # Panel background
    pygame.draw.rect(screen, (30, 30, 40), panel_rect, border_radius=12)
    pygame.draw.rect(screen, (255, 255, 255), panel_rect, 2, border_radius=12)

    # Title
    title = font.render("YOU DIED", True, (255, 80, 80))
    screen.blit(title, title.get_rect(center=(panel_rect.centerx, panel_rect.y + 30)))

    # Buttons
    retry_btn = pygame.Rect(panel_rect.x + 30, panel_rect.y + 90, 110, 45)
    menu_btn  = pygame.Rect(panel_rect.x + 180, panel_rect.y + 90, 110, 45)

    pygame.draw.rect(screen, (70, 180, 90), retry_btn, border_radius=8)
    pygame.draw.rect(screen, (180, 70, 70), menu_btn, border_radius=8)

    screen.blit(font.render("Retry", True, (0, 0, 0)), retry_btn.move(25, 10))
    screen.blit(font.render("Menu", True, (0, 0, 0)), menu_btn.move(28, 10))

    return retry_btn, menu_btn



def kill_player():
    global  state, attempts 

    
    

    attempts += 1
    state = "retry"

    # stop player motion
    player.velocity_y = 0

def draw_win_screen(screen, font):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    title = font.render("CONGRATULATIONS!", True, (255, 255, 255))
    subtitle = font.render("LEVEL COMPLETED" \
    "MORE LEVELS TO COME", True, (180, 220, 255))

    screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 40)))
    screen.blit(subtitle, subtitle.get_rect(center=(WIDTH//2, HEIGHT//2 + 10)))


def restart_level():
    global obstacles, level_start_time, obstacle_speed
    global speed_boost_started, zoom, zoom_target
    global player_dead
    global spawn_locked, jumper_pattern_spawned

    obstacles.clear()
    

    player.reset()

    obstacle_speed = BASE_SPEED
    speed_boost_started = False
    zoom = 1.0
    zoom_target = 1.0

    spawn_locked = False              # ✅ RESET
    jumper_pattern_spawned = False    # ✅ RESET

    level_start_time = pygame.time.get_ticks()
    player_dead = False

def reset_game():
    global obstacles
    global level_start_time, obstacle_speed
    global speed_boost_started, zoom, zoom_target, zoom_timer
    global back_x1, back_x2, front_x1, front_x2
    global text_active, text_x
    global spawn_locked, jumper_pattern_spawned

    obstacles.clear()
    

    player.reset()
    level_start_time = pygame.time.get_ticks()

    obstacle_speed = BASE_SPEED
    speed_boost_started = False

    zoom = 1.0
    zoom_target = 1.0
    zoom_timer = 0

    back_x1 = 0
    back_x2 = bg_back.get_width()
    front_x1 = 0
    front_x2 = bg_front.get_width()

    text_active = False
    text_x = WIDTH + 100

    spawn_locked = False              # ✅ RESET
    jumper_pattern_spawned = False    # ✅ RESET

# ---------------- OBSTACLES ----------------
def spawn_triple_small_spikes(x, ground_y):
    spacing = 28

    for i in range(3):
        spike = SmallSpike(
            x + i * spacing,
            ground_y + 40,   # SAME ground reference as pillars
            size=25
        )
        obstacles.append(spike)

def spawn_big_spike(x, ground_y):
    obstacles.append(
        TriangleObstacle(x, ground_y + 40)
    )

level_completed = False
flag_spawned = False

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
    liquid_width = 90    
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

def spawn_pillar_liquid_section1(x, ground_y):
    pillar_width = 60
    base_height = 80
    height_step = 20

    gap_width = 90       
    liquid_width = 90    
    liquid_offset = (gap_width - liquid_width) // 2
    liquid_raise = 35
    liquid_height = 25

    count = 6
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
def spawn_triple_small_spikes_on_pillar(pillar, offset_x=0):
    spacing = 28
    spike_size = 25

    spike_y = pillar.rect.top - spike_size +20 # 👈 KEY LINE

    for i in range(3):
        obstacles.append(
            SmallSpike(
                pillar.rect.x + offset_x + i * spacing,
                spike_y,
                size=spike_size
            )
        )

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


def spwan_pillar_pattern1(x, ground_y): 
    spacing = 120 
    obstacles.append(Pillar(x, ground_y+40, height=60, width=80))
    x += spacing 
    obstacles.append(Liquid(x-40, ground_y+10, height=30, width=160)) 
    x += spacing 
    obstacles.append(Pillar(x, ground_y + 40, height=100, width=100)) 
    obstacles.append(Pillar(x+100, ground_y + 40, height=100, width=100)) 
    obstacles.append(Pillar(x+200, ground_y + 40, height=100, width=100)) 
    obstacles.append(Pillar(x+300, ground_y + 40, height=100, width=100)) 
    obstacles.append(Pillar(x+400, ground_y + 40, height=100, width=100)) 
    obstacles.append(Pillar(x+500, ground_y + 40, height=100, width=120)) 
    spawn_triple_small_spikes(x + 120, ground_y-100) 
    spawn_big_spike(x + 420, ground_y-100) 
    x += spacing + 600 
    obstacles.append(TriangleObstacle(x-100, ground_y + 40)) 
    obstacles.append(JumperPad(x+30, ground_y )) 
    spawn_triple_small_spikes(x-40, ground_y)
    spawn_triple_small_spikes(x+20, ground_y)
    spawn_triple_small_spikes(x+80, ground_y)
    
def spawn_pillar_spike_pattern2(x, ground_y):
    spacing =100
    obstacles.append(Pillar(x, ground_y + 40, height=90, width=100))
    x+= spacing
    for i in range(27):
        obstacles.append(
            SmallSpike(
                x + i * 40,
                ground_y + 40,
                size=30

            )
        )
    obstacles.append(Pillar(x+100 , ground_y-30 , height=10, width=80))
    x+= spacing
    obstacles.append(Pillar(x+200 , ground_y-30, height=10, width=120))
    x+= spacing
    obstacles.append(JumperPad(x+320 , ground_y-10,boost=-25))
    x+= spacing
    obstacles.append(Pillar(x+400 , ground_y -100, height=10, width=80))
    x+= spacing
    obstacles.append(Pillar(x+400 , ground_y -70, height=10, width=80))
    x+= spacing
    obstacles.append(Pillar(x+600 , ground_y +40,height=90, width=100))


    


def spawn_jumper_pillar_pattern(start_x, ground_y):
    spacing = 120
    LIQUID_HEIGHT = 30
    x = start_x

    # 1️⃣ Jumper Pad
    obstacles.append(JumperPad(x+60, ground_y+20))
    x += spacing + 80

    # 2️⃣ Large Pillar
    big_pillar = Pillar(x, ground_y+40, height=160, width=120)
    obstacles.append(big_pillar)
    x += big_pillar.rect.width + 30

    # 3️⃣ Liquid gap
    obstacles.append(
        Liquid(
            x-30,
            ground_y+10,
            width=200,
            height=LIQUID_HEIGHT
        )
    )
    x += 60 + spacing

    # 4️⃣ Small Pillar
    small_pillar = Pillar(x-20, ground_y+40, height=100, width=140)
    obstacles.append(small_pillar)
    x += small_pillar.rect.width + 30

    # 5️⃣ Jumper Pad
    obstacles.append(JumperPad(x+50, ground_y-10))
       

    # 6️⃣ Liquid gap
    obstacles.append(
        Liquid(
            x-50,
            ground_y+10,
            width=230,
            height=LIQUID_HEIGHT
        )
    )
    x +=  spacing+60

    # 7️⃣ Medium Pillar
    obstacles.append(Pillar(x-10, ground_y+40, height=140, width=100))



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
            if icon_left_btn.collidepoint(event.pos):
                selected_icon_index = (selected_icon_index - 1) % len(player_icons)

            elif icon_right_btn.collidepoint(event.pos):
                selected_icon_index = (selected_icon_index + 1) % len(player_icons)

            elif button_rect.collidepoint(event.pos):
                player.icon = player_icons[selected_icon_index]
                state = "game"
                reset_game()
                pygame.mixer.music.play(-1)

        # JUMP
        if state == "game" and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button;
                player.jump()
        if state == "retry" and event.type == pygame.MOUSEBUTTONDOWN:
            if retry_btn.collidepoint(event.pos):
                reset_game()     # restart run
                state = "game"
                pygame.mixer.music.fadeout(200)
                pygame.mixer.music.play(-1)

            elif menu_btn.collidepoint(event.pos):
                state = "menu"  
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
            elif 12_900 <= elapsed_time < 16_400:
                if  spawn_locked:
                    spawn_pillar_liquid_section(WIDTH , ground_y)
                    spawn_locked = False
                    spawn_pillar_spike_pattern(WIDTH + 350, ground_y)       
    # AFTER 20s → (optional later)
            if elapsed_time >= 16_500 and not speed_boost_started:
                obstacle_speed += 2
                speed_boost_started = True

            elif 17_000 <= elapsed_time < 20_000:
                if not jumper_pattern_spawned:
                    spawn_jumper_pillar_pattern(WIDTH, ground_y)
                    jumper_pattern_spawned = True
            elif 20_000 <= elapsed_time < 25_000:
                if not spawn_locked:
                    spwan_pillar_pattern1(WIDTH+200, ground_y)
                    spawn_locked = True
            elif 26_000 <= elapsed_time < 31_000:
                obstacle_speed = 5
    
                if spawn_locked:
                    spawn_pillar_spike_pattern2(WIDTH+200, ground_y)
                    spawn_locked = False
            elif 32_000 <= elapsed_time < 40_000:
                if not spawn_locked:
                    spawn_pillar_liquid_section1(WIDTH, ground_y)
                    spawn_locked= True
            # ---- FINAL FLAG (END OF LEVEL) ----
            if elapsed_time >= 40_000 and not flag_spawned:
                obstacles.append(Flag(WIDTH + 200, ground_y))
                flag_spawned = True

            else:
                pass
                

    # -------- UPDATE --------
    if state == "win":
        continue

    if state == "game":
        elapsed_time = pygame.time.get_ticks() - level_start_time
       

        if elapsed_time >= speed_boost_time:
            if not speed_boost_started:
                speed_boost_started = True
                speed_start_time = pygame.time.get_ticks()
                speed_boost_end_time = speed_start_time + SPEED_BOOST_DURATION

    # 🔹 Trigger zoom ONLY ONCE
            if not zoom_triggered:
                zoom_target = 1.00
                zoom_timer = pygame.time.get_ticks()
                zoom_triggered = True

    # ---- TEXT APPEAR WINDOW (25–30 sec) ----
        if 25_000 <= elapsed_time <= 30_000:
            if not text_active:
                text_active = True
                text_x = WIDTH + 100  # start from right

    # ---- Smooth speed increase ----
        if speed_boost_started:
            t = min(
            (pygame.time.get_ticks() - level_start_time) / speed_transition_duration,
            1
        )
            obstacle_speed = BASE_SPEED + (FAST_SPEED - BASE_SPEED) * t

        # ---- Auto reset speed ----
            if pygame.time.get_ticks() > speed_boost_end_time:
                obstacle_speed = BASE_SPEED
                speed_boost_started = False
  # ---- SMOOTH ZOOM ----
        zoom += (zoom_target - zoom) * zoom_speed

# Auto reset zoom after duration
        if zoom_target > 1.0:
            if pygame.time.get_ticks() - zoom_timer > ZOOM_DURATION:
                zoom_target = 1.0
                zoom_triggered = False


# Snap back cleanly (IMPORTANT)
        if zoom_target == 1.0 and abs(zoom - 1.0) < 0.002:
            zoom = 1.0


            

        # ---- MOVE BACKGROUND ----
        back_x1 -= back_speed
        back_x2 -= back_speed

        bw = bg_back.get_width()

        if back_x1 <= -bw:
            back_x1 = back_x2 + bw
        if back_x2 <= -bw:
            back_x2 = back_x1 + bw

# ---- MOVE FOREGROUND ----
        front_x1 -= front_speed
        front_x2 -= front_speed

        fw = bg_front.get_width()

        if front_x1 <= -fw:
            front_x1 = front_x2+fw
        if front_x2 <= -fw:
            front_x2 = front_x1+fw
        if text_active:
            text_x -= front_speed   # SAME speed as building

        player.update()
        player_on_pillar = False
        

        for obs in obstacles[:]:
            obs.update(obstacle_speed)

            if isinstance(obs, Flag):
                if player.rect.colliderect(obs.rect):
                    state = "win"
                    pygame.mixer.music.stop()
                    break
                continue

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

        # ✅ TOP LANDING (only when falling)
                    if (
            player.velocity_y >= 0 and
            player.rect.bottom <= obs.rect.top + 15
        ):
                        player.rect.bottom = obs.rect.top
                        player.velocity_y = 0
                        player.on_ground = True
                        player.state = "run"
                        continue

        # ❌ SIDE OR BOTTOM HIT
                    kill_player()
                    break


            

    # ================= REAL HAZARDS =================
            if isinstance(obs, (TriangleObstacle, SmallSpike, Liquid)):
                if player.rect.colliderect(obs.hitbox):
                    kill_player()
                    break

        
    # -------- DRAW --------
    world_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


    if state == "menu":
        screen.fill((16, 15, 30))

        

# ---- TITLE IMAGE ----
        title_rect = title_img.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_img, title_rect)

        

        # ---- ICON SELECTOR ----
        icon = player_icons[selected_icon_index]
        screen.blit(icon, icon.get_rect(center=(WIDTH//2, icon_y)))
        # screen.blit(label, label.get_rect(center=(WIDTH//2, icon_y + 40)))

        pygame.draw.rect(screen, (100, 100, 100), icon_left_btn, border_radius=6)
        pygame.draw.rect(screen, (100, 100, 100), icon_right_btn, border_radius=6)

        screen.blit(font.render("<", True, WHITE), icon_left_btn.move(12, 4))
        screen.blit(font.render(">", True, WHITE), icon_right_btn.move(14, 4))

        # ---- START BUTTON ----
        pygame.draw.rect(screen, (0, 180, 255), button_rect, border_radius=10)
        # ---- START IMAGE BUTTON ----
        screen.blit(start_img, start_rect)




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
        if text_active:
            world_surface.blit(text_img, (text_x, text_y))

        
       

    # ---- OBSTACLES ----
        for obs in obstacles:
            if isinstance(obs, SmallSpike):
                pygame.draw.rect(screen, (255, 0, 0), obs.rect, 1)

            obs.draw(world_surface)
            

    # ---- PLAYER ----
     
           

       
        # player.draw_skid(world_surface)
        player.draw(world_surface)

        draw_ui(world_surface, font, attempts)
        
        if state == "win":
            draw_win_screen(screen, font)


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
        
    if state == "retry":
        retry_btn, menu_btn = draw_retry_panel(screen)
 



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
    elif state == "win":
        screen.fill((10, 10, 20))

        title = font.render("CONGRATULATIONS!", True, (0, 255, 150))
        subtitle = font.render("LEVEL COMPLETED", True, (200, 200, 200))

        screen.blit(
        title,
        title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
    )
        screen.blit(
        subtitle,
        subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    )


    pygame.display.flip()
    clock.tick(60)

    
