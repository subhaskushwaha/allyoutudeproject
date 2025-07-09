import pygame
import sys
import math
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stellar Starfield Simulator")

# Colors
DEEP_SPACE = (5, 5, 20)
NEBULA_PURPLE = (70, 20, 80)
NEBULA_BLUE = (20, 30, 70)
NEBULA_RED = (80, 10, 30)
STAR_COLORS = [
    (255, 255, 255),  # White
    (200, 200, 255),  # Blue-white
    (255, 240, 200),  # Yellow-white
    (255, 200, 150),  # Orange
    (200, 150, 255),  # Violet
]
TEXT_COLOR = (220, 220, 255)
CONSTELLATION_COLOR = (100, 150, 255, 150)

# Star class
class Star:
    def __init__(self, x=None, y=None, size=None):
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.size = size if size is not None else random.uniform(0.5, 3.0)
        self.base_size = self.size
        self.color = random.choice(STAR_COLORS)
        self.twinkle_speed = random.uniform(0.01, 0.05)
        self.twinkle_phase = random.uniform(0, 2 * math.pi)
        self.speed_x = random.uniform(-0.2, 0.2)
        self.speed_y = random.uniform(-0.2, 0.2)
        self.in_constellation = False
        self.constellation_id = None
        self.trail = []
        self.max_trail = 10
        
    def update(self):
        # Update position with parallax effect (smaller stars move slower)
        parallax_factor = 0.1 + (self.size / 3.0) * 0.9
        self.x += self.speed_x * parallax_factor
        self.y += self.speed_y * parallax_factor
        
        # Wrap around screen edges
        if self.x < -10: self.x = WIDTH + 10
        if self.x > WIDTH + 10: self.x = -10
        if self.y < -10: self.y = HEIGHT + 10
        if self.y > HEIGHT + 10: self.y = -10
        
        # Twinkle effect
        self.size = self.base_size * (0.8 + 0.4 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_phase))
        
        # Update trail for constellation stars
        if self.in_constellation:
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.max_trail:
                self.trail.pop(0)
    
    def draw(self, surface):
        # Draw star
        brightness = min(255, int(200 + 55 * math.sin(pygame.time.get_ticks() * self.twinkle_speed + self.twinkle_phase)))
        star_color = (
            min(255, self.color[0] * brightness // 255),
            min(255, self.color[1] * brightness // 255),
            min(255, self.color[2] * brightness // 255)
        )
        
        # Draw glow
        glow_size = self.size * 4
        glow_surf = pygame.Surface((glow_size*2, glow_size*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*star_color, 30), (glow_size, glow_size), glow_size)
        surface.blit(glow_surf, (int(self.x - glow_size), int(self.y - glow_size)))
        
        # Draw star core
        pygame.draw.circle(surface, star_color, (int(self.x), int(self.y)), int(self.size))
        
        # Draw trail for constellation stars
        if self.in_constellation and len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                start_pos = self.trail[i-1]
                end_pos = self.trail[i]
                alpha = int(200 * i / len(self.trail))
                pygame.draw.line(
                    surface, 
                    (*CONSTELLATION_COLOR[:3], alpha), 
                    start_pos, 
                    end_pos, 
                    1
                )

# Nebula class
class Nebula:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(100, 400)
        self.color = random.choice([NEBULA_BLUE, NEBULA_PURPLE, NEBULA_RED])
        self.speed_x = random.uniform(-0.05, 0.05)
        self.speed_y = random.uniform(-0.05, 0.05)
        self.pulse_speed = random.uniform(0.001, 0.005)
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        
        # Wrap around screen
        if self.x < -self.size: self.x = WIDTH + self.size
        if self.x > WIDTH + self.size: self.x = -self.size
        if self.y < -self.size: self.y = HEIGHT + self.size
        if self.y > HEIGHT + self.size: self.y = -self.size
        
    def draw(self, surface):
        pulse = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() * self.pulse_speed + self.pulse_phase)
        current_size = int(self.size * pulse)
        
        nebula_surf = pygame.Surface((current_size*2, current_size*2), pygame.SRCALPHA)
        
        # Draw nebula with multiple layers for depth
        for i in range(3):
            layer_size = current_size * (1 - i * 0.2)
            alpha = 80 - i * 20
            color = (
                min(255, self.color[0] + i * 20),
                min(255, self.color[1] + i * 10),
                min(255, self.color[2] + i * 15),
                alpha
            )
            pygame.draw.circle(nebula_surf, color, (current_size, current_size), int(layer_size))
        
        surface.blit(nebula_surf, (int(self.x - current_size), int(self.y - current_size)))

# Constellation class
class Constellation:
    def __init__(self, stars):
        self.stars = stars
        self.id = random.randint(1000, 9999)
        self.name = self.generate_name()
        self.color = CONSTELLATION_COLOR
        self.reveal_progress = 0
        self.reveal_speed = 0.02
        self.active = False
        
        # Assign constellation to stars
        for star in self.stars:
            star.in_constellation = True
            star.constellation_id = self.id
            star.max_trail = 20
    
    def generate_name(self):
        prefixes = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta"]
        suffixes = ["Majoris", "Minor", "Serpentis", "Draconis", "Ursae", "Orion", "Pegasi", "Lyrae"]
        return f"{random.choice(prefixes)} {random.choice(suffixes)}"
    
    def update(self):
        if self.active and self.reveal_progress < 1.0:
            self.reveal_progress += self.reveal_speed
    
    def draw(self, surface):
        if self.reveal_progress > 0:
            # Draw constellation lines
            for i in range(len(self.stars)):
                for j in range(i + 1, len(self.stars)):
                    # Only draw if both stars are revealed enough
                    dist = math.sqrt((self.stars[i].x - self.stars[j].x)**2 + 
                                    (self.stars[i].y - self.stars[j].y)**2)
                    
                    if dist < 300:  # Only connect reasonably close stars
                        alpha = int(200 * min(self.reveal_progress, 1.0))
                        pygame.draw.line(
                            surface, 
                            (*self.color[:3], alpha), 
                            (self.stars[i].x, self.stars[i].y), 
                            (self.stars[j].x, self.stars[j].y), 
                            1
                        )
            
            # Draw constellation name
            if self.reveal_progress > 0.5:
                center_x = sum(star.x for star in self.stars) / len(self.stars)
                center_y = sum(star.y for star in self.stars) / len(self.stars)
                alpha = int(255 * (self.reveal_progress - 0.5) * 2)
                
                name_surf = font.render(self.name, True, (*self.color[:3], alpha))
                surface.blit(name_surf, (center_x - name_surf.get_width() // 2, 
                                        center_y - 30))

# Create stars
stars = [Star() for _ in range(400)]

# Create some larger stars
for _ in range(20):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.uniform(2.5, 4.0)
    stars.append(Star(x, y, size))

# Create a few very large stars
for _ in range(5):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.uniform(4.5, 6.0)
    stars.append(Star(x, y, size))

# Create nebulae
nebulae = [Nebula() for _ in range(5)]

# Create constellations
constellations = []
for _ in range(8):
    # Select 4-8 stars for a constellation
    constellation_stars = random.sample(stars, random.randint(4, 8))
    constellations.append(Constellation(constellation_stars))

# Create shooting stars
shooting_stars = []
shooting_star_timer = 0

def create_shooting_star():
    start_x = random.randint(0, WIDTH)
    start_y = random.randint(0, 100)
    angle = random.uniform(math.pi/6, math.pi/3)
    length = random.randint(100, 300)
    speed = random.uniform(5, 10)
    return {
        'x': start_x,
        'y': start_y,
        'angle': angle,
        'length': length,
        'speed': speed,
        'trail': [],
        'life': 100
    }

# Main game loop
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
title_font = pygame.font.SysFont(None, 60, bold=True)
constellation_font = pygame.font.SysFont(None, 28)

# Create a surface for glow effect
glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Game state
discovered_constellations = 0
view_mode = "explore"  # "explore" or "constellation"

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_c:
                view_mode = "constellation" if view_mode == "explore" else "explore"
            elif event.key == K_r:
                # Reset constellations
                for constellation in constellations:
                    constellation.reveal_progress = 0
                    constellation.active = False
                discovered_constellations = 0
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Try to activate a constellation
                for constellation in constellations:
                    if not constellation.active:
                        center_x = sum(star.x for star in constellation.stars) / len(constellation.stars)
                        center_y = sum(star.y for star in constellation.stars) / len(constellation.stars)
                        distance = math.sqrt((event.pos[0] - center_x)**2 + (event.pos[1] - center_y)**2)
                        
                        if distance < 100:
                            constellation.active = True
                            discovered_constellations += 1
    
    # Update shooting star timer
    shooting_star_timer += 1
    if shooting_star_timer > 180 and random.random() < 0.1:
        shooting_star_timer = 0
        shooting_stars.append(create_shooting_star())
    
    # Update stars
    for star in stars:
        star.update()
    
    # Update nebulae
    for nebula in nebulae:
        nebula.update()
    
    # Update constellations
    for constellation in constellations:
        constellation.update()
    
    # Update shooting stars
    for shooting_star in shooting_stars[:]:
        # Add current position to trail
        shooting_star['trail'].append((shooting_star['x'], shooting_star['y']))
        if len(shooting_star['trail']) > 20:
            shooting_star['trail'].pop(0)
        
        # Update position
        shooting_star['x'] += math.cos(shooting_star['angle']) * shooting_star['speed']
        shooting_star['y'] += math.sin(shooting_star['angle']) * shooting_star['speed']
        shooting_star['life'] -= 1
        
        if shooting_star['life'] <= 0:
            shooting_stars.remove(shooting_star)
    
    # Draw everything
    screen.fill(DEEP_SPACE)
    
    # Draw nebulae
    for nebula in nebulae:
        nebula.draw(screen)
    
    # Draw constellation connections
    if view_mode == "constellation":
        for constellation in constellations:
            constellation.draw(screen)
    
    # Draw star trails first (for constellations)
    for star in stars:
        if star.in_constellation and view_mode == "constellation":
            if len(star.trail) > 1:
                for i in range(1, len(star.trail)):
                    start_pos = star.trail[i-1]
                    end_pos = star.trail[i]
                    alpha = int(200 * i / len(star.trail))
                    pygame.draw.line(
                        screen, 
                        (*CONSTELLATION_COLOR[:3], alpha), 
                        start_pos, 
                        end_pos, 
                        1
                    )
    
    # Draw stars
    for star in stars:
        star.draw(screen)
    
    # Draw shooting stars
    for shooting_star in shooting_stars:
        if len(shooting_star['trail']) > 1:
            for i in range(1, len(shooting_star['trail'])):
                start_pos = shooting_star['trail'][i-1]
                end_pos = shooting_star['trail'][i]
                alpha = int(255 * i / len(shooting_star['trail']))
                pygame.draw.line(
                    screen, 
                    (255, 255, 255, alpha), 
                    start_pos, 
                    end_pos, 
                    2
                )
    
    # Draw UI
    # Title
    title = title_font.render("STELLAR STARFIELD SIMULATOR", True, TEXT_COLOR)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Stats
    stats_text = font.render(f"Discovered Constellations: {discovered_constellations}/{len(constellations)}", True, TEXT_COLOR)
    screen.blit(stats_text, (20, 20))
    
    # Instructions
    instructions = [
        "C: Toggle Constellation View",
        "R: Reset Constellations",
        "Click near constellation centers to discover them",
        "ESC: Quit"
    ]
    
    # Draw semi-transparent background for text
    text_bg_height = 130
    text_bg = pygame.Surface((WIDTH, text_bg_height), pygame.SRCALPHA)
    text_bg.fill((0, 0, 0, 150))
    screen.blit(text_bg, (0, HEIGHT - text_bg_height))
    
    # Draw instructions
    for i, text in enumerate(instructions):
        text_surf = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surf, (20, HEIGHT - text_bg_height + 20 + i*25))
    
    # Draw view mode indicator
    mode_text = font.render(f"View Mode: {view_mode.capitalize()}", True, 
                          (100, 200, 255) if view_mode == "constellation" else TEXT_COLOR)
    screen.blit(mode_text, (WIDTH - mode_text.get_width() - 20, 20))
    
    # Draw constellation names in the corner
    if view_mode == "constellation":
        discovered_text = font.render("Discovered Constellations:", True, (150, 200, 255))
        screen.blit(discovered_text, (WIDTH - 350, 60))
        
        y_pos = 90
        for constellation in constellations:
            if constellation.active:
                name_text = constellation_font.render(constellation.name, True, CONSTELLATION_COLOR[:3])
                screen.blit(name_text, (WIDTH - 340, y_pos))
                y_pos += 30
    
    # Draw a compass
    pygame.draw.circle(screen, (100, 100, 150, 150), (60, 60), 40, 2)
    pygame.draw.line(screen, (200, 50, 50), (60, 60), (60, 20), 2)  # North
    pygame.draw.line(screen, (50, 200, 50), (60, 60), (100, 60), 2)  # East
    n_text = font.render("N", True, (200, 50, 50))
    screen.blit(n_text, (57, 15))
    
    pygame.display.flip()
    clock.tick(60)