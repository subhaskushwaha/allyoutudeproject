import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 700
GRID_SIZE = 25
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Colors
BACKGROUND = (18, 22, 30)
GRID_COLOR = (30, 36, 50, 80)
SNAKE_HEAD_COLOR = (0, 230, 118)
SNAKE_BODY_COLOR = (0, 200, 83)
SNAKE_SHINE = (180, 255, 180, 150)
FOOD_COLOR = (255, 82, 82)
FOOD_SHINE = (255, 220, 220, 200)
TEXT_COLOR = (220, 230, 240)
UI_BG = (30, 36, 50, 200)
ACCENT_COLOR = (41, 182, 246)

FPS = 60
INITIAL_SPEED = 10
SPEED_INCREMENT = 0.2

# Display and clock setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake")
clock = pygame.time.Clock()

# Font setup with fallback
try:
    font_large = pygame.font.Font(None, 64)
    font_medium = pygame.font.Font(None, 42)
    font_small = pygame.font.Font(None, 28)
    font_tiny = pygame.font.Font(None, 22)
except:
    font_large = pygame.font.SysFont("Arial", 64, bold=True)
    font_medium = pygame.font.SysFont("Arial", 42, bold=True)
    font_small = pygame.font.SysFont("Arial", 28)
    font_tiny = pygame.font.SysFont("Arial", 22)

class Snake:
    def __init__(self):
        self.reset()
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.score = 0
        self.speed = INITIAL_SPEED
        self.grow_to = 3
        self.last_move_time = 0
        self.is_alive = True
        self.pulse = 0
    def get_head(self):
        return self.positions[0]
    def update(self, current_time):
        if not self.is_alive: return
        if current_time - self.last_move_time > 1000 // self.speed:
            self.last_move_time = current_time
            head = self.get_head()
            x, y = self.direction
            new = ((head[0]+x)%GRID_WIDTH,(head[1]+y)%GRID_HEIGHT)
            if new in self.positions[1:]:
                self.is_alive = False
                return
            self.positions.insert(0, new)
            if len(self.positions) > self.grow_to:
                self.positions.pop()
        self.pulse = (self.pulse + 0.05) % (2*math.pi)
    def change_dir(self, d):
        if (d[0]*-1, d[1]*-1) != self.direction:
            self.direction = d
    def grow(self):
        self.grow_to += 1
        self.score += 10
        self.speed += SPEED_INCREMENT
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            if i == 0:
                color = SNAKE_HEAD_COLOR
            else:
                ratio = min(1.0, i/(self.grow_to*0.5))
                r = int(SNAKE_HEAD_COLOR[0]*(1-ratio) + SNAKE_BODY_COLOR[0]*ratio)
                g = int(SNAKE_HEAD_COLOR[1]*(1-ratio) + SNAKE_BODY_COLOR[1]*ratio)
                b = int(SNAKE_HEAD_COLOR[2]*(1-ratio) + SNAKE_BODY_COLOR[2]*ratio)
                color = (r,g,b)
            offset = math.sin(self.pulse + i*0.3) * 0.5
            rect = pygame.Rect(
                pos[0]*GRID_SIZE + offset,
                pos[1]*GRID_SIZE + offset,
                GRID_SIZE - offset*2,
                GRID_SIZE - offset*2
            )
            pygame.draw.rect(surface, color, rect, border_radius=10)
            if i == 0:
                shine_size = GRID_SIZE // 3
                shine_offset = GRID_SIZE // 4
                shine_rect = pygame.Rect(
                    rect.x + shine_offset,
                    rect.y + shine_offset,
                    shine_size, shine_size
                )
                pygame.draw.ellipse(surface, SNAKE_SHINE, shine_rect)
                eye_size = GRID_SIZE // 6
                EO = GRID_SIZE // 3
                dx, dy = self.direction
                if dx == 1:
                    eyes = [(rect.right-EO, rect.top+EO), (rect.right-EO, rect.bottom-EO)]
                elif dx == -1:
                    eyes = [(rect.left+EO, rect.top+EO), (rect.left+EO, rect.bottom-EO)]
                elif dy == 1:
                    eyes = [(rect.left+EO, rect.bottom-EO), (rect.right-EO, rect.bottom-EO)]
                else:
                    eyes = [(rect.left+EO, rect.top+EO), (rect.right-EO, rect.top+EO)]
                for e in eyes:
                    pygame.draw.circle(surface, (20,20,30), e, eye_size)

class Food:
    def __init__(self):
        self.randomize()
        self.pulse = 0
    def randomize(self):
        self.position = (
            random.randint(2, GRID_WIDTH-3),
            random.randint(2, GRID_HEIGHT-3)
        )
    def draw(self, surface):
        self.pulse = (self.pulse + 0.1) % (2*math.pi)
        ps = math.sin(self.pulse)*3
        cx = self.position[0]*GRID_SIZE + GRID_SIZE//2
        cy = self.position[1]*GRID_SIZE + GRID_SIZE//2
        r = GRID_SIZE//2 - ps/2
        pygame.draw.circle(surface, FOOD_COLOR, (cx, cy), int(r))
        shine_r = int(r*0.4)
        pygame.draw.circle(surface, FOOD_SHINE, (cx-shine_r, cy-shine_r), shine_r)

def draw_bg(surface):
    for y in range(HEIGHT):
        r = BACKGROUND[0] + int(10*(y/HEIGHT))
        g = BACKGROUND[1] + int(8*(y/HEIGHT))
        b = BACKGROUND[2] + int(15*(y/HEIGHT))
        pygame.draw.line(surface, (r,g,b), (0,y), (WIDTH,y))
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.rect(surface, GRID_COLOR, (x,y,GRID_SIZE,GRID_SIZE), 1)

def draw_ui(surface, score, speed):
    panel = pygame.Rect(WIDTH-220,20,200,100)
    pygame.draw.rect(surface, UI_BG, panel, border_radius=12)
    pygame.draw.rect(surface, ACCENT_COLOR, panel, 2, border_radius=12)
    surface.blit(font_medium.render(f"{score}", True, TEXT_COLOR), (WIDTH-210,35))
    surface.blit(font_tiny.render("SCORE", True, TEXT_COLOR), (WIDTH-210,70))
    surface.blit(font_small.render(f"{speed:.1f}", True, TEXT_COLOR), (WIDTH-210,85))
    surface.blit(font_tiny.render("SPEED", True, TEXT_COLOR), (WIDTH-140,70))
    bar = pygame.Rect(WIDTH-210,115,120,8)
    pygame.draw.rect(surface, (60,70,90), bar, border_radius=4)
    fill = pygame.Rect(WIDTH-210,115,min(120, speed/20*120),8)
    pygame.draw.rect(surface, ACCENT_COLOR, fill, border_radius=4)

def draw_overlay(surface, text, score=None):
    overlay = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    overlay.fill((10,15,25,220))
    surface.blit(overlay, (0,0))
    surface.blit(font_large.render(text, True, (255,100,100)), 
                 (WIDTH//2-200, HEIGHT//2-120))
    if score is not None:
        surf = font_medium.render("FINAL SCORE", True, TEXT_COLOR)
        surface.blit(surf, (WIDTH//2-100, HEIGHT//2-60))
        surface.blit(font_large.render(str(score), True, TEXT_COLOR),
                     (WIDTH//2-40, HEIGHT//2))
    btn = pygame.Rect(WIDTH//2-100, HEIGHT//2+100,200,50)
    pygame.draw.rect(surface, (30,40,60), btn, border_radius=10)
    pygame.draw.rect(surface, ACCENT_COLOR, btn, 3, border_radius=10)
    surface.blit(font_medium.render("RESTART", True, ACCENT_COLOR),
                 (WIDTH//2-70, HEIGHT//2+110))
    surface.blit(font_tiny.render("Press SPACE to play again", True, (150,170,190)),
                 (WIDTH//2-110, HEIGHT//2+170))

def draw_welcome(surface):
    overlay = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
    overlay.fill((10,15,25,240))
    surface.blit(overlay, (0,0))
    surface.blit(font_large.render("NEON SNAKE", True, ACCENT_COLOR), (WIDTH//2-200,80))
    surface.blit(font_medium.render("Press SPACE to Start", True, ACCENT_COLOR),
                 (WIDTH//2-160,HEIGHT//2))
    surface.blit(font_tiny.render("Use Arrow Keys to Move", True, TEXT_COLOR),
                 (WIDTH//2-150, HEIGHT//2+60))

def main():
    snake = Snake()
    food = Food()
    state = "welcome"
    while True:
        t = pygame.time.get_ticks()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if state == "playing":
                    if e.key == pygame.K_UP:    snake.change_dir((0,-1))
                    if e.key == pygame.K_DOWN:  snake.change_dir((0,1))
                    if e.key == pygame.K_LEFT:  snake.change_dir((-1,0))
                    if e.key == pygame.K_RIGHT: snake.change_dir((1,0))
                if e.key == pygame.K_SPACE:
                    snake.reset()
                    food.randomize()
                    state = "playing"
        if state == "playing":
            snake.update(t)
            if snake.get_head() == food.position:
                snake.grow()
                food.randomize()
                while food.position in snake.positions:
                    food.randomize()
            if not snake.is_alive:
                state = "game_over"
        screen.fill((0,0,0))
        draw_bg(screen)
        snake.draw(screen)
        food.draw(screen)
        draw_ui(screen, snake.score, snake.speed)
        if state == "welcome":
            draw_welcome(screen)
        elif state == "game_over":
            draw_overlay(screen, "GAME OVER", snake.score)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
