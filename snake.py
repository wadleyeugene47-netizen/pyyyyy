"""
SNAKE — a well-developed pygame implementation.

Features:
- Start menu, pause menu, and game-over screen
- Smooth grid-based movement with buffered input (no accidental reversals)
- Increasing difficulty: speed ramps up as your score grows
- Score + persistent high score (saved to highscore.txt next to this file)
- Particle burst effect when food is eaten
- Wrap-around toggle vs. wall-collision mode (press W on the menu to toggle)
- Clean, commented, single-file code you can easily extend

Controls:
    Arrow keys / WASD  - move
    P                  - pause / unpause
    W (on menu)        - toggle wall mode (walls kill vs. wrap around)
    Enter              - start game / restart after game over
    Esc                - quit

Run:
    pip install pygame
    python snake_game.py
"""

import pygame
import random
import sys
import os
from collections import deque

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

CELL_SIZE = 24
GRID_WIDTH = 28
GRID_HEIGHT = 22
SIDEBAR_WIDTH = 180

SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

FPS = 60
BASE_MOVE_INTERVAL = 0.14   # seconds per move at the start
MIN_MOVE_INTERVAL = 0.045   # fastest the snake will ever move
SPEEDUP_PER_FOOD = 0.004    # how much faster per food eaten

HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "highscore.txt")

# Colors
BG_COLOR = (18, 20, 24)
GRID_COLOR = (28, 31, 37)
SIDEBAR_COLOR = (24, 26, 31)
TEXT_COLOR = (235, 235, 240)
ACCENT_COLOR = (90, 200, 130)
DANGER_COLOR = (220, 90, 90)
FOOD_COLOR = (230, 160, 60)
SNAKE_HEAD_COLOR = (110, 220, 150)
SNAKE_BODY_COLOR = (70, 170, 110)
DIM_TEXT_COLOR = (150, 152, 160)

UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except OSError:
        pass  # non-fatal; game still works without persistence


class Particle:
    """A tiny fading square used for the food-eaten burst effect."""

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2.5, 2.5)
        self.vy = random.uniform(-2.5, 2.5)
        self.life = 1.0
        self.color = color
        self.size = random.randint(2, 4)

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.life -= dt * 1.8

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = max(0, min(255, int(self.life * 255)))
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        s.fill((*self.color, alpha))
        surface.blit(s, (self.x, self.y))


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("consolas", 48, bold=True)
        self.font_med = pygame.font.SysFont("consolas", 26, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 18)

        self.high_score = load_high_score()
        self.wall_mode = True  # True = walls kill, False = wrap around
        self.state = "menu"  # menu, playing, paused, game_over

        self.reset_game()

    # ----------------------------------------------------------------- #
    # Game lifecycle
    # ----------------------------------------------------------------- #

    def reset_game(self):
        start = (GRID_WIDTH // 4, GRID_HEIGHT // 2)
        self.snake = deque([start, (start[0] - 1, start[1]), (start[0] - 2, start[1])])
        self.direction = RIGHT
        self.pending_direction = RIGHT
        self.direction_queue = deque()
        self.score = 0
        self.move_interval = BASE_MOVE_INTERVAL
        self.move_timer = 0.0
        self.particles = []
        self.food = self.spawn_food()
        self.death_reason = ""

    def spawn_food(self):
        occupied = set(self.snake)
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in occupied:
                return pos

    # ----------------------------------------------------------------- #
    # Input handling
    # ----------------------------------------------------------------- #

    def handle_input(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if self.state == "menu":
            if event.key == pygame.K_RETURN:
                self.reset_game()
                self.state = "playing"
            elif event.key == pygame.K_w:
                self.wall_mode = not self.wall_mode

        elif self.state == "playing":
            key_dir = {
                pygame.K_UP: UP, pygame.K_w: UP,
                pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
                pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
                pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
            }
            if event.key in key_dir:
                new_dir = key_dir[event.key]
                # buffer the direction; ignore immediate reversals
                last_dir = self.direction_queue[-1] if self.direction_queue else self.direction
                if new_dir != OPPOSITE[last_dir] and (not self.direction_queue or new_dir != last_dir):
                    if len(self.direction_queue) < 2:
                        self.direction_queue.append(new_dir)
            elif event.key == pygame.K_p:
                self.state = "paused"

        elif self.state == "paused":
            if event.key == pygame.K_p:
                self.state = "playing"

        elif self.state == "game_over":
            if event.key == pygame.K_RETURN:
                self.reset_game()
                self.state = "playing"

    # ----------------------------------------------------------------- #
    # Update
    # ----------------------------------------------------------------- #

    def update(self, dt):
        if self.state != "playing":
            return

        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]

        self.move_timer += dt
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0.0

        if self.direction_queue:
            self.direction = self.direction_queue.popleft()

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if self.wall_mode:
            if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                self.die("You hit the wall!")
                return
        else:
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)

        if new_head in self.snake:
            self.die("You bit yourself!")
            return

        self.snake.appendleft(new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_particles(new_head)
            self.move_interval = max(MIN_MOVE_INTERVAL, self.move_interval - SPEEDUP_PER_FOOD)
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def spawn_particles(self, cell):
        px = cell[0] * CELL_SIZE + CELL_SIZE // 2
        py = cell[1] * CELL_SIZE + CELL_SIZE // 2
        for _ in range(18):
            self.particles.append(Particle(px, py, FOOD_COLOR))

    def die(self, reason):
        self.death_reason = reason
        self.state = "game_over"
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)

    # ----------------------------------------------------------------- #
    # Drawing
    # ----------------------------------------------------------------- #

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.draw_grid()

        if self.state == "menu":
            self.draw_menu()
        else:
            self.draw_snake()
            self.draw_food()
            for p in self.particles:
                p.draw(self.screen)
            self.draw_sidebar()
            if self.state == "paused":
                self.draw_overlay("PAUSED", "Press P to resume")
            elif self.state == "game_over":
                self.draw_overlay(
                    "GAME OVER",
                    f"{self.death_reason}  Press Enter to retry",
                    color=DANGER_COLOR,
                )

        pygame.display.flip()

    def draw_grid(self):
        play_w = GRID_WIDTH * CELL_SIZE
        for x in range(0, play_w + 1, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT + 1, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (play_w, y))

    def draw_snake(self):
        for i, (gx, gy) in enumerate(self.snake):
            rect = pygame.Rect(gx * CELL_SIZE + 1, gy * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=6)

    def draw_food(self):
        gx, gy = self.food
        center = (gx * CELL_SIZE + CELL_SIZE // 2, gy * CELL_SIZE + CELL_SIZE // 2)
        pulse = 2 + int(2 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
        pygame.draw.circle(self.screen, FOOD_COLOR, center, CELL_SIZE // 2 - 2 + pulse // 4)

    def draw_sidebar(self):
        rect = pygame.Rect(GRID_WIDTH * CELL_SIZE, 0, SIDEBAR_WIDTH, SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, SIDEBAR_COLOR, rect)

        pad = rect.x + 20
        self.blit_text("SNAKE", (pad, 24), self.font_med, ACCENT_COLOR)

        self.blit_text("SCORE", (pad, 90), self.font_small, DIM_TEXT_COLOR)
        self.blit_text(str(self.score), (pad, 112), self.font_big, TEXT_COLOR)

        self.blit_text("HIGH SCORE", (pad, 190), self.font_small, DIM_TEXT_COLOR)
        self.blit_text(str(self.high_score), (pad, 212), self.font_med, TEXT_COLOR)

        self.blit_text("LENGTH", (pad, 270), self.font_small, DIM_TEXT_COLOR)
        self.blit_text(str(len(self.snake)), (pad, 292), self.font_med, TEXT_COLOR)

        mode = "WALLS" if self.wall_mode else "WRAP"
        self.blit_text(f"MODE: {mode}", (pad, SCREEN_HEIGHT - 100), self.font_small, DIM_TEXT_COLOR)
        self.blit_text("P: pause", (pad, SCREEN_HEIGHT - 70), self.font_small, DIM_TEXT_COLOR)
        self.blit_text("Esc: quit", (pad, SCREEN_HEIGHT - 46), self.font_small, DIM_TEXT_COLOR)

    def draw_menu(self):
        title = self.font_big.render("SNAKE", True, ACCENT_COLOR)
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))

        lines = [
            "Arrow keys / WASD to move",
            "P to pause",
            f"W to toggle wall mode  (current: {'WALLS' if self.wall_mode else 'WRAP'})",
            "",
            "Press ENTER to start",
        ]
        y = SCREEN_HEIGHT // 2 - 20
        for line in lines:
            color = ACCENT_COLOR if "ENTER" in line else TEXT_COLOR
            text = self.font_small.render(line, True, color)
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 32

        hs = self.font_small.render(f"High Score: {self.high_score}", True, DIM_TEXT_COLOR)
        self.screen.blit(hs, hs.get_rect(center=(SCREEN_WIDTH // 2, y + 20)))

    def draw_overlay(self, title, subtitle, color=ACCENT_COLOR):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        title_surf = self.font_big.render(title, True, color)
        self.screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)))

        sub_surf = self.font_small.render(subtitle, True, TEXT_COLOR)
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)))

    def blit_text(self, text, pos, font, color):
        surf = font.render(text, True, color)
        self.screen.blit(surf, pos)

    # ----------------------------------------------------------------- #
    # Main loop
    # ----------------------------------------------------------------- #

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.handle_input(event)

            self.update(dt)
            self.draw()


if __name__ == "__main__":
    SnakeGame().run()