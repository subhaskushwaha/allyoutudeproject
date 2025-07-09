import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beach Sunset Animation")

# Colors
SKY_DAY = (135, 206, 235)
SKY_SUNSET = (255, 140, 0)
SKY_NIGHT = (0, 0, 40)
SUN = (255, 215, 0)
MOON = (220, 220, 220)
OCEAN_DAY = (0, 105, 148)
OCEAN_NIGHT = (0, 40, 85)
SAND = (238, 214, 175)
STAR = (255, 255, 255)
PALM_TRUNK = (139, 69, 19)
PALM_LEAVES = (34, 139, 34)
BIRD = (0, 0, 0)
WAVE = (173, 216, 230)

# Game states
DAY = 0
SUNSET = 1
NIGHT = 2

class Sun:
    def __init__(self):
        self.radius = 50
        self.x = WIDTH // 2
        self.y = HEIGHT // 3
        self.target_y = HEIGHT + 100
        self.speed = 0.5
        self.is_clicked = False
        self.state = DAY
    
    def draw(self, surface):
        pygame.draw.circle(surface, SUN, (self.x, self.y), self.radius)
    
    def update(self):
        if self.is_clicked and self.y < self.target_y:
            self.y += self.speed
            if self.y > HEIGHT * 0.4:
                self.state = SUNSET
            if self.y > HEIGHT * 0.8:
                self.state = NIGHT
    
    def check_click(self, pos):
        x, y = pos
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        if distance <= self.radius:
            self.is_clicked = True
            return True
        return False

class Moon:
    def __init__(self):
        self.radius = 40
        self.x = WIDTH // 4
        self.y = -self.radius
        self.target_y = HEIGHT // 4
        self.speed = 0.3
        self.visible = False
    
    def draw(self, surface):
        if self.visible:
            pygame.draw.circle(surface, MOON, (self.x, self.y), self.radius)
            # Draw craters
            pygame.draw.circle(surface, (200, 200, 200), (self.x - 15, self.y - 10), 8)
            pygame.draw.circle(surface, (200, 200, 200), (self.x + 20, self.y + 5), 6)
            pygame.draw.circle(surface, (200, 200, 200), (self.x + 5, self.y + 20), 5)
    
    def update(self):
        if self.visible and self.y < self.target_y:
            self.y += self.speed

class Bird:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(50, 150)
        self.speed = random.uniform(1.0, 3.0)
        self.wing_up = True
        self.wing_timer = 0
    
    def draw(self, surface):
        # Draw bird body
        pygame.draw.circle(surface, BIRD, (self.x, self.y), 8)
        
        # Draw wings
        if self.wing_up:
            pygame.draw.arc(surface, BIRD, (self.x - 15, self.y - 10, 30, 20), 0, math.pi, 2)
        else:
            pygame.draw.arc(surface, BIRD, (self.x - 15, self.y, 30, 20), math.pi, 2 * math.pi, 2)
        
        # Draw tail
        pygame.draw.line(surface, BIRD, (self.x - 8, self.y), (self.x - 15, self.y - 5), 2)
    
    def update(self):
        self.x += self.speed
        if self.x > WIDTH + 20:
            self.x = -20
            self.y = random.randint(50, 150)
        
        # Animate wings
        self.wing_timer += 1
        if self.wing_timer > 10:
            self.wing_up = not self.wing_up
            self.wing_timer = 0

class Wave:
    def __init__(self, x, y, speed, amplitude, wavelength):
        self.x = x
        self.y = y
        self.speed = speed
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.offset = 0
    
    def draw(self, surface, color):
        points = []
        for x in range(0, WIDTH + 20, 20):
            wave_y = self.y + self.amplitude * math.sin((x + self.offset) / self.wavelength)
            points.append((x, wave_y))
        
        if len(points) > 1:
            pygame.draw.lines(surface, color, False, points, 3)
    
    def update(self):
        self.offset += self.speed

class PalmTree:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT - 120
    
    def draw(self, surface):
        # Draw trunk
        pygame.draw.rect(surface, PALM_TRUNK, (self.x, self.y, 15, 120))
        
        # Draw leaves
        for angle in range(-30, 31, 15):
            rad = math.radians(angle)
            end_x = self.x + 7.5 + 50 * math.cos(rad)
            end_y = self.y + 50 * math.sin(rad)
            pygame.draw.line(surface, PALM_LEAVES, (self.x + 7.5, self.y), (end_x, end_y), 5)
            
            # Draw leaf details
            for i in range(1, 4):
                leaf_x = self.x + 7.5 + (i * 15) * math.cos(rad)
                leaf_y = self.y + (i * 15) * math.sin(rad)
                pygame.draw.circle(surface, (50, 205, 50), (int(leaf_x), int(leaf_y)), 8)

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT // 2)
        self.size = random.uniform(0.5, 2)
        self.brightness = random.randint(100, 255)
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_dir = 1
    
    def draw(self, surface):
        brightness = int(self.brightness)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(surface, color, (self.x, self.y), self.size)
    
    def update(self):
        self.brightness += self.twinkle_speed * self.twinkle_dir
        if self.brightness >= 255 or self.brightness <= 100:
            self.twinkle_dir *= -1

# Create game objects
sun = Sun()
moon = Moon()
birds = [Bird() for _ in range(5)]
waves = [
    Wave(0, HEIGHT - 80, 0.5, 5, 50),
    Wave(0, HEIGHT - 60, 0.8, 8, 70),
    Wave(0, HEIGHT - 40, 1.0, 12, 90)
]
palm_trees = [PalmTree(150), PalmTree(600)]
stars = [Star() for _ in range(100)]

# Main game loop
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if sun.check_click(event.pos):
                moon.visible = True
    
    # Update game objects
    sun.update()
    moon.update()
    
    for bird in birds:
        bird.update()
    
    for wave in waves:
        wave.update()
    
    for star in stars:
        star.update()
    
    # Draw background
    if sun.state == DAY:
        screen.fill(SKY_DAY)
    elif sun.state == SUNSET:
        # Create sunset gradient
        for y in range(HEIGHT // 2):
            ratio = y / (HEIGHT / 2)
            r = int(SKY_DAY[0] * (1 - ratio) + SKY_SUNSET[0] * ratio)
            g = int(SKY_DAY[1] * (1 - ratio) + SKY_SUNSET[1] * ratio)
            b = int(SKY_DAY[2] * (1 - ratio) + SKY_SUNSET[2] * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
    else:  # NIGHT
        screen.fill(SKY_NIGHT)
        for star in stars:
            star.draw(screen)
    
    # Draw sun and moon
    sun.draw(screen)
    moon.draw(screen)
    
    # Draw ocean
    if sun.state == DAY:
        pygame.draw.rect(screen, OCEAN_DAY, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    else:
        pygame.draw.rect(screen, OCEAN_NIGHT, (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    
    # Draw waves
    for wave in waves:
        wave_color = WAVE if sun.state == DAY else (100, 100, 150)
        wave.draw(screen, wave_color)
    
    # Draw sand
    pygame.draw.rect(screen, SAND, (0, HEIGHT - 40, WIDTH, 40))
    
    # Draw palm trees
    for tree in palm_trees:
        tree.draw(screen)
    
    # Draw birds
    for bird in birds:
        bird.draw(screen)
    
    # Draw instructions
    if not sun.is_clicked:
        text = font.render("Click on the sun to watch the sunset", True, (0, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))
    
    if sun.state == NIGHT:
        text = font.render("Beautiful night at the beach!", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()