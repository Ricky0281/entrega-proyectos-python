import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Moto Ramp Race Mejorado")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (10, 10, 15)
BLUE = (0, 180, 255)
RED = (255, 60, 80)
GREEN = (80, 255, 140)
YELLOW = (255, 220, 70)
PURPLE = (180, 90, 255)
GRAY = (110, 110, 120)
DARK = (12, 14, 28)
ROAD = (38, 38, 46)

font_big = pygame.font.SysFont("arialblack", 58)
font_med = pygame.font.SysFont("arialblack", 34)
font_small = pygame.font.SysFont("arial", 24)

TRACK_LENGTH = 5200
GROUND_Y = 520
FINISH_X = 120
TURN_X = TRACK_LENGTH

difficulty_data = {
    "Fácil": 0.70,
    "Normal": 0.86,
    "Difícil": 0.98
}

state = "menu"
menu_index = 0
difficulty_index = 1
name_text = ""
winner_text = ""
selected_mode = None

modes = [
    "Humano vs PC",
    "PC vs PC",
    "Humano vs PC vs PC"
]

difficulties = ["Fácil", "Normal", "Difícil"]

ramps = []
obstacles = []

for x in range(750, TRACK_LENGTH - 700, 760):
    ramps.append(pygame.Rect(x, GROUND_Y - 35, 160, 35))

for x in range(1250, TRACK_LENGTH - 650, 900):
    obstacles.append(pygame.Rect(x, GROUND_Y - 45, 55, 45))


class Moto:
    def __init__(self, name, color, lane_offset, human=False):
        self.name = name
        self.color = color
        self.x = FINISH_X
        self.y = GROUND_Y - lane_offset
        self.lane_offset = lane_offset
        self.vel_x = 0
        self.vel_y = 0
        self.width = 72
        self.height = 34
        self.human = human
        self.returning = False
        self.finished = False
        self.distance_done = 0
        self.max_speed = random.uniform(8.0, 9.3)
        self.accel = random.uniform(0.15, 0.22)

    def rect(self):
        return pygame.Rect(self.x - 36, self.y - 30, self.width, self.height)

    def on_ground(self):
        return self.y >= GROUND_Y - self.lane_offset - 2

    def update(self, keys, difficulty):
        if self.finished:
            return

        direction = -1 if self.returning else 1

        if self.human:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.vel_x += self.accel
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.vel_x -= self.accel
            else:
                self.vel_x *= 0.985

            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground():
                self.vel_y = -14

        else:
            self.vel_x += self.accel * direction

            must_jump = False

            for ob in obstacles:
                dist = ob.x - self.x if not self.returning else self.x - ob.x
                if 90 < dist < 270:
                    must_jump = True

            for ramp in ramps:
                dist = ramp.x - self.x if not self.returning else self.x - ramp.x
                if 50 < dist < 210:
                    must_jump = True

            if must_jump and self.on_ground():
                if random.random() < difficulty_data[difficulty]:
                    self.vel_y = -13.5

        self.vel_x = max(-self.max_speed, min(self.max_speed, self.vel_x))
        self.x += self.vel_x

        self.vel_y += 0.65
        self.y += self.vel_y

        ground = GROUND_Y - self.lane_offset

        if self.y >= ground:
            self.y = ground
            self.vel_y = 0

        for ramp in ramps:
            ramp_rect = pygame.Rect(ramp.x, ramp.y - self.lane_offset, ramp.w, ramp.h)
            if self.rect().colliderect(ramp_rect):
                if self.vel_y >= 0:
                    self.y = ramp_rect.top
                    self.vel_y = -10.8

        for ob in obstacles:
            ob_rect = pygame.Rect(ob.x, ob.y - self.lane_offset, ob.w, ob.h)
            if self.rect().colliderect(ob_rect):
                if self.y < ob_rect.top + 10:
                    self.y = ob_rect.top
                    self.vel_y = -9
                else:
                    self.vel_x *= -0.45

        if self.x >= TURN_X:
            self.returning = True
            self.x = TURN_X

        if self.returning and self.x <= FINISH_X:
            self.finished = True
            self.distance_done = TRACK_LENGTH * 2

        if not self.returning:
            self.distance_done = self.x - FINISH_X
        else:
            self.distance_done = TRACK_LENGTH + (TRACK_LENGTH - self.x)

    def draw(self, camera_x):
        sx = self.x - camera_x
        sy = self.y

        pygame.draw.circle(screen, BLACK, (int(sx - 25), int(sy + 8)), 16)
        pygame.draw.circle(screen, BLACK, (int(sx + 28), int(sy + 8)), 16)

        pygame.draw.circle(screen, self.color, (int(sx - 25), int(sy + 8)), 9)
        pygame.draw.circle(screen, self.color, (int(sx + 28), int(sy + 8)), 9)

        pygame.draw.polygon(screen, self.color, [
            (sx - 38, sy),
            (sx - 5, sy - 28),
            (sx + 38, sy - 10),
            (sx + 20, sy + 5),
            (sx - 25, sy + 6)
        ])

        pygame.draw.circle(screen, WHITE, (int(sx - 5), int(sy - 36)), 10)
        pygame.draw.line(screen, WHITE, (sx - 5, sy - 26), (sx + 18, sy - 7), 4)

        if self.human:
            pygame.draw.circle(screen, YELLOW, (int(sx), int(sy - 78)), 8)

        label = font_small.render(self.name, True, WHITE)
        screen.blit(label, (sx - label.get_width() // 2, sy - 70))


def draw_text_center(text, font, color, y):
    img = font.render(text, True, color)
    screen.blit(img, (WIDTH // 2 - img.get_width() // 2, y))


def draw_background(camera_x, speed):
    screen.fill((7, 9, 22))

    for i in range(80):
        x = (i * 210 - camera_x * 0.18) % WIDTH
        y = 45 + (i * 41) % 270
        pygame.draw.circle(screen, (70, 90, 130), (int(x), int(y)), 2)

    pygame.draw.rect(screen, (18, 24, 42), (0, 355, WIDTH, HEIGHT - 355))
    pygame.draw.rect(screen, ROAD, (0, GROUND_Y - 155, WIDTH, 300))

    for lane in range(3):
        y = GROUND_Y - lane * 55 + 45
        for i in range(-5, 30):
            x = i * 180 - (camera_x % 180)
            pygame.draw.rect(screen, YELLOW, (x, y, 90, 7), border_radius=3)

    for i in range(20):
        x = i * 160 - (camera_x * (1 + speed * 0.015)) % 160
        pygame.draw.line(screen, (85, 85, 95), (x, GROUND_Y + 120), (x - 80, HEIGHT), 2)


def draw_track_items(camera_x):
    for lane_offset in [0, 55, 110]:
        for ramp in ramps:
            r = pygame.Rect(ramp.x - camera_x, ramp.y - lane_offset, ramp.w, ramp.h)
            pygame.draw.polygon(screen, BLUE, [
                (r.left, r.bottom),
                (r.right, r.bottom),
                (r.right, r.top)
            ])

        for ob in obstacles:
            r = pygame.Rect(ob.x - camera_x, ob.y - lane_offset, ob.w, ob.h)
            pygame.draw.rect(screen, RED, r, border_radius=8)
            pygame.draw.rect(screen, WHITE, r, 2, border_radius=8)

    pygame.draw.rect(screen, GREEN, (FINISH_X - camera_x, GROUND_Y - 230, 10, 270))
    pygame.draw.rect(screen, PURPLE, (TURN_X - camera_x, GROUND_Y - 230, 10, 270))

    meta = font_small.render("META", True, GREEN)
    retorno = font_small.render("RETORNO", True, PURPLE)

    screen.blit(meta, (FINISH_X - camera_x - 25, GROUND_Y - 260))
    screen.blit(retorno, (TURN_X - camera_x - 45, GROUND_Y - 260))


def draw_hud(motos, difficulty):
    pygame.draw.rect(screen, (0, 0, 0), (20, 20, 430, 145), border_radius=16)

    txt = font_small.render(f"Dificultad: {difficulty}", True, WHITE)
    screen.blit(txt, (40, 35))

    for i, moto in enumerate(motos):
        progress = min(1, moto.distance_done / (TRACK_LENGTH * 2))
        pygame.draw.rect(screen, GRAY, (40, 75 + i * 30, 260, 13), border_radius=8)
        pygame.draw.rect(screen, moto.color, (40, 75 + i * 30, int(260 * progress), 13), border_radius=8)

        name = font_small.render(moto.name, True, WHITE)
        screen.blit(name, (315, 66 + i * 30))


def draw_minimap(motos):
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 390, 25, 350, 95), border_radius=16)
    pygame.draw.line(screen, WHITE, (WIDTH - 350, 78), (WIDTH - 80, 78), 3)

    meta = font_small.render("META", True, GREEN)
    vuelta = font_small.render("RETORNO", True, PURPLE)

    screen.blit(meta, (WIDTH - 365, 45))
    screen.blit(vuelta, (WIDTH - 140, 45))

    for moto in motos:
        progress = min(1, moto.distance_done / (TRACK_LENGTH * 2))
        px = WIDTH - 350 + int(progress * 270)
        pygame.draw.circle(screen, moto.color, (px, 78), 8)
        if moto.human:
            pygame.draw.circle(screen, YELLOW, (px, 78), 13, 2)


def create_race():
    player_name = name_text.strip() if name_text.strip() else "Jugador"
    new_motos = []

    if selected_mode == "Humano vs PC":
        new_motos.append(Moto(player_name, BLUE, 0, True))
        new_motos.append(Moto("CPU-Rayo", RED, 55, False))

    elif selected_mode == "PC vs PC":
        new_motos.append(Moto("CPU-Rayo", RED, 0, False))
        new_motos.append(Moto("CPU-Nitro", GREEN, 55, False))

    elif selected_mode == "Humano vs PC vs PC":
        new_motos.append(Moto(player_name, BLUE, 0, True))
        new_motos.append(Moto("CPU-Rayo", RED, 55, False))
        new_motos.append(Moto("CPU-Nitro", GREEN, 110, False))

    return new_motos


motos = []

running = True
while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if state == "menu":
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    selected_mode = modes[menu_index]
                    state = "name" if "Humano" in selected_mode else "difficulty"

            elif state == "name":
                if event.key == pygame.K_RETURN:
                    state = "difficulty"
                elif event.key == pygame.K_BACKSPACE:
                    name_text = name_text[:-1]
                else:
                    if len(name_text) < 14 and event.unicode.isprintable():
                        name_text += event.unicode

            elif state == "difficulty":
                if event.key == pygame.K_UP:
                    difficulty_index = (difficulty_index - 1) % len(difficulties)
                elif event.key == pygame.K_DOWN:
                    difficulty_index = (difficulty_index + 1) % len(difficulties)
                elif event.key == pygame.K_RETURN:
                    motos = create_race()
                    state = "race"

            elif state == "winner":
                if event.key == pygame.K_RETURN:
                    state = "menu"
                    winner_text = ""
                    motos = []

    if state == "menu":
        screen.fill(DARK)

        draw_text_center("MOTO RAMP RACE", font_big, BLUE, 95)
        draw_text_center("Carrera de motos con rampas, obstáculos y retorno", font_small, WHITE, 170)

        for i, mode in enumerate(modes):
            color = YELLOW if i == menu_index else WHITE
            prefix = "▶ " if i == menu_index else "   "
            draw_text_center(prefix + mode, font_med, color, 270 + i * 70)

        draw_text_center("↑ ↓ elegir | ENTER continuar | ESC salir", font_small, GRAY, 610)

    elif state == "name":
        screen.fill(DARK)

        draw_text_center("Nombre de tu moto/jugador", font_big, BLUE, 140)

        pygame.draw.rect(screen, (30, 35, 55), (390, 310, 500, 70), border_radius=16)
        pygame.draw.rect(screen, BLUE, (390, 310, 500, 70), 3, border_radius=16)

        shown = name_text if name_text else "Escribe aquí..."
        draw_text_center(shown, font_med, WHITE, 325)

        draw_text_center("ENTER continuar | BACKSPACE borrar", font_small, GRAY, 470)

    elif state == "difficulty":
        screen.fill(DARK)

        draw_text_center("Selecciona dificultad", font_big, BLUE, 120)

        for i, diff in enumerate(difficulties):
            color = YELLOW if i == difficulty_index else WHITE
            prefix = "▶ " if i == difficulty_index else "   "
            draw_text_center(prefix + diff, font_med, color, 270 + i * 70)

        draw_text_center("La dificultad mejora los saltos de la IA", font_small, GRAY, 560)

    elif state == "race":
        for moto in motos:
            moto.update(keys, difficulties[difficulty_index])

        human_motos = [m for m in motos if m.human]

        if human_motos:
            focus = human_motos[0]
        else:
            focus = max(motos, key=lambda m: m.distance_done)

        camera_x = focus.x - WIDTH // 2
        camera_x = max(0, min(camera_x, TRACK_LENGTH - WIDTH + 300))

        speed_fx = abs(focus.vel_x)

        winners = [m for m in motos if m.finished]
        if winners:
            winner_text = winners[0].name
            state = "winner"

        draw_background(camera_x, speed_fx)
        draw_track_items(camera_x)

        for moto in motos:
            moto.draw(camera_x)

        draw_hud(motos, difficulties[difficulty_index])
        draw_minimap(motos)

        controls = font_small.render(
            "La cámara sigue al humano | D/→ acelerar | A/← frenar | SPACE/W/↑ saltar | ESC salir",
            True,
            WHITE
        )
        screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT - 45))

    elif state == "winner":
        screen.fill(DARK)

        draw_text_center("🏆 GANADOR 🏆", font_big, YELLOW, 170)
        draw_text_center(winner_text, font_big, WHITE, 280)
        draw_text_center("ENTER para volver al menú", font_med, BLUE, 420)
        draw_text_center("ESC para salir", font_small, GRAY, 500)

    pygame.display.flip()

pygame.quit()
sys.exit()