import pygame
import sys
import random
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Animated Tree Generator")

# Colors
SKY_BLUE = (135, 206, 235)
GROUND_GREEN = (34, 139, 34)
TRUNK_BROWN = (101, 67, 33)
LEAF_COLORS = [
    [(60, 179, 113), (50, 160, 50), (40, 140, 40)],    # Summer greens
    [(210, 180, 140), (200, 150, 100), (190, 130, 90)],   # Autumn light browns
    [(255, 69, 0), (240, 50, 0), (220, 40, 0)],      # Autumn oranges
    [(178, 34, 34), (160, 30, 30), (140, 25, 25)],     # Autumn reds
    [(255, 215, 0), (240, 200, 0), (220, 180, 0)],     # Autumn yellows
    [(200, 220, 200), (180, 200, 180), (160, 180, 160)]  # Spring greens
]
BACKGROUND_COLORS = [
    (135, 206, 235),   # Summer sky blue
    (253, 245, 230),   # Autumn sky
    (176, 224, 230),   # Winter sky
    (173, 216, 230),   # Spring sky
]

# Tree parameters
MAX_DEPTH = 10
ANGLE_VARIATION = 0.7
LENGTH_DECREASE = 0.75
MIN_BRANCH_LENGTH = 8
LEAF_SIZE = 5
MAX_BRANCHES = 3

# Animation variables
current_season = 0
season_timer = 0
season_duration = 400  # frames per season
wind_direction = 0
wind_strength = 0
wind_change_timer = 0
leaf_fall_timer = 0
falling_leaves = []

class Tree:
    def __init__(self, x, y, trunk_length, trunk_thickness, angle=math.pi/2):
        self.x = x
        self.y = y
        self.trunk_length = trunk_length
        self.trunk_thickness = trunk_thickness
        self.angle = angle
        self.branches = []
        self.leaves = []
        self.grow_tree(self.x, self.y, self.trunk_length, self.angle, self.trunk_thickness, 0)
    
    def grow_tree(self, start_x, start_y, length, angle, thickness, depth):
        if depth > MAX_DEPTH or length < MIN_BRANCH_LENGTH:
            # Create a cluster of leaves at the branch end
            for _ in range(random.randint(8, 15)):
                offset_x = random.uniform(-15, 15)
                offset_y = random.uniform(-15, 5)
                self.leaves.append((start_x + offset_x, start_y + offset_y))
            return
        
        # Calculate end point of branch
        end_x = start_x + math.cos(angle) * length
        end_y = start_y - math.sin(angle) * length
        
        # Store branch data
        self.branches.append({
            'start': (start_x, start_y),
            'end': (end_x, end_y),
            'thickness': thickness,
            'depth': depth
        })
        
        # Recursively grow new branches
        new_thickness = max(1, thickness * 0.75)
        new_length = max(MIN_BRANCH_LENGTH, length * LENGTH_DECREASE * random.uniform(0.8, 1.0))
        
        # Main branch continuation
        self.grow_tree(end_x, end_y, new_length, angle, new_thickness, depth + 1)
        
        # Create additional branches (1-3 per node)
        branch_count = random.randint(1, MAX_BRANCHES)
        for i in range(branch_count):
            # Determine branch angle based on position
            branch_angle = angle + ANGLE_VARIATION * random.uniform(0.5, 1.5) * (1 if i % 2 == 0 else -1)
            
            # Adjust branch length based on angle
            branch_length = new_length * random.uniform(0.5, 0.8)
            
            self.grow_tree(end_x, end_y, branch_length, 
                          branch_angle, new_thickness, depth + 1)
    
    def draw(self, surface, wind_direction, wind_strength):
        # Draw branches first (from thickest to thinnest)
        sorted_branches = sorted(self.branches, key=lambda b: b['thickness'], reverse=True)
        
        for branch in sorted_branches:
            start_x, start_y = branch['start']
            end_x, end_y = branch['end']
            
            # Apply wind effect - deeper branches sway more
            wind_factor = branch['depth'] / MAX_DEPTH
            sway_x = math.sin(wind_direction) * wind_strength * wind_factor * 3
            sway_y = math.cos(wind_direction) * wind_strength * wind_factor * 1.5
            
            # Color gradient based on depth (darker near trunk, lighter near ends)
            brown_shade = 60 + int(195 * (branch['depth'] / MAX_DEPTH))
            color = (brown_shade, brown_shade // 2, brown_shade // 3)
            
            # Draw branch with thickness
            pygame.draw.line(
                surface, 
                color, 
                (start_x + sway_x, start_y + sway_y), 
                (end_x + sway_x, end_y + sway_y), 
                max(1, int(branch['thickness']))
            )
            
            # Add bark texture to thicker branches
            if branch['thickness'] > 3:
                for i in range(int(branch['thickness'] * 0.8)):
                    offset_x = random.uniform(-1, 1) * branch['thickness'] * 0.3
                    offset_y = random.uniform(-1, 1) * branch['thickness'] * 0.3
                    bark_color = (max(0, color[0]-10), max(0, color[1]-10), max(0, color[2]-10))
                    pygame.draw.circle(
                        surface, 
                        bark_color, 
                        (int((start_x+end_x)/2 + sway_x + offset_x), 
                         int((start_y+end_y)/2 + sway_y + offset_y)), 
                        max(1, int(branch['thickness'] * 0.15))
                    )  # <-- Fixed missing parenthesis here
        
        # Draw leaves
        for leaf_x, leaf_y in self.leaves:
            # Apply wind effect to leaves
            leaf_wind_x = math.sin(wind_direction) * wind_strength * random.uniform(0.5, 1.5) * 4
            leaf_wind_y = math.cos(wind_direction) * wind_strength * random.uniform(0.2, 0.7) * 2
            
            # Choose leaf color based on season
            if current_season == 1:  # Autumn - more color variation
                leaf_color = random.choice(LEAF_COLORS[random.randint(1, 4)])
            elif current_season == 3:  # Spring - light green
                leaf_color = random.choice(LEAF_COLORS[5])
            elif current_season == 2:  # Winter - no leaves
                continue
            else:  # Summer - green
                leaf_color = random.choice(LEAF_COLORS[0])
            
            # Draw leaf as a small circle with seasonal variation
            if current_season == 1:  # Autumn leaves are more varied
                size = LEAF_SIZE * random.uniform(0.8, 1.2)
                pygame.draw.ellipse(
                    surface, 
                    leaf_color, 
                    (leaf_x + leaf_wind_x - size/2, 
                     leaf_y + leaf_wind_y - size/2, 
                     size, size * 1.5)
                )
            else:
                pygame.draw.circle(
                    surface, 
                    leaf_color, 
                    (int(leaf_x + leaf_wind_x), int(leaf_y + leaf_wind_y)), 
                    LEAF_SIZE
                )

def draw_ground(surface):
    # Draw ground with texture
    pygame.draw.rect(surface, GROUND_GREEN, (0, HEIGHT - 120, WIDTH, 120))
    
    # Draw grass details
    for i in range(0, WIDTH, 4):
        grass_height = random.randint(5, 15)
        sway = math.sin(pygame.time.get_ticks() / 300 + i * 0.05) * 3
        color = random.choice([(34, 139, 34), (20, 120, 20), (50, 160, 60)])
        pygame.draw.line(
            surface, 
            color, 
            (i, HEIGHT - 120), 
            (i + sway, HEIGHT - 120 - grass_height), 
            2
        )
    
    # Draw flowers in spring
    if current_season == 3:
        for i in range(30):
            x = random.randint(0, WIDTH)
            y = HEIGHT - 130 + random.randint(0, 20)
            color = random.choice([(255, 100, 100), (255, 200, 50), (200, 50, 200), (255, 150, 150)])
            pygame.draw.circle(surface, color, (x, y), 3)
            pygame.draw.line(surface, (50, 150, 50), (x, y+3), (x, y+10), 1)

def draw_sun(surface, season):
    sun_color = (255, 255, 200) if season == 0 else (255, 220, 150)  # Brighter in summer
    sun_x = 150 if season == 0 else 850  # Position changes with seasons
    
    # Draw sun glow
    for size in range(50, 70, 5):
        alpha = 200 - (size - 50) * 10
        s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*sun_color, alpha), (size, size), size)
        surface.blit(s, (sun_x - size, 100 - size))
    
    # Draw sun core
    pygame.draw.circle(surface, sun_color, (sun_x, 100), 40)
    
    # Draw sun rays
    for i in range(0, 360, 15):
        angle = math.radians(i)
        start_x = sun_x + math.cos(angle) * 45
        start_y = 100 + math.sin(angle) * 45
        end_x = sun_x + math.cos(angle) * 65
        end_y = 100 + math.sin(angle) * 65
        pygame.draw.line(surface, sun_color, (start_x, start_y), (end_x, end_y), 4)

def draw_clouds(surface):
    for i, pos in enumerate([(100, 80), (400, 60), (700, 100), (250, 150)]):
        x, y = pos
        offset = math.sin(pygame.time.get_ticks() / 2000 + i) * 10
        for j in range(3):
            size = 30 + j * 10
            pygame.draw.circle(surface, (240, 240, 245), (x + offset + j*25, y), size)
            pygame.draw.circle(surface, (240, 240, 245), (x + offset + j*25 - 15, y + 15), size-5)

def create_falling_leaf():
    x = random.randint(200, WIDTH - 200)
    y = random.randint(50, 300)
    color = random.choice(LEAF_COLORS[random.randint(1, 4)])
    size = random.uniform(3, 6)
    speed = random.uniform(0.5, 2)
    sway = random.uniform(0.05, 0.2)
    return {'x': x, 'y': y, 'color': color, 'size': size, 'speed': speed, 'sway': sway, 'angle': 0}

# Create initial tree
tree = Tree(WIDTH // 2, HEIGHT - 120, 120, 20)

# Main game loop
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
title_font = pygame.font.SysFont(None, 48, bold=True)

# Pre-render season names
season_names = ["SUMMER", "AUTUMN", "WINTER", "SPRING"]
season_texts = [title_font.render(name, True, (50, 50, 50)) for name in season_names]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Generate a new tree
                tree = Tree(WIDTH // 2, HEIGHT - 120, 
                           random.randint(100, 140), 
                           random.randint(18, 25))
            elif event.key == K_RIGHT:
                current_season = (current_season + 1) % 4
                season_timer = 0
                tree = Tree(WIDTH // 2, HEIGHT - 120, 
                           random.randint(100, 140), 
                           random.randint(18, 25))
            elif event.key == K_LEFT:
                current_season = (current_season - 1) % 4
                season_timer = 0
                tree = Tree(WIDTH // 2, HEIGHT - 120, 
                           random.randint(100, 140), 
                           random.randint(18, 25))
            elif event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    # Update season timer
    season_timer += 1
    if season_timer >= season_duration:
        season_timer = 0
        current_season = (current_season + 1) % 4
        # Create a new tree for the new season
        tree = Tree(WIDTH // 2, HEIGHT - 120, 
                   random.randint(100, 140), 
                   random.randint(18, 25))
    
    # Update wind
    wind_change_timer += 1
    if wind_change_timer > 60:
        wind_change_timer = 0
        wind_direction = random.uniform(0, 2 * math.pi)
        wind_strength = random.randint(0, 5)
    
    # Create falling leaves in autumn
    leaf_fall_timer += 1
    if current_season == 1 and leaf_fall_timer > 5 and wind_strength > 2:
        leaf_fall_timer = 0
        falling_leaves.append(create_falling_leaf())
    
    # Update falling leaves
    for leaf in falling_leaves[:]:
        leaf['y'] += leaf['speed']
        leaf['x'] += math.sin(leaf['angle']) * 1.5
        leaf['angle'] += leaf['sway']
        
        if leaf['y'] > HEIGHT - 100:
            falling_leaves.remove(leaf)
    
    # Fill background with seasonal color
    bg_color = BACKGROUND_COLORS[current_season]
    screen.fill(bg_color)
    
    # Draw sun
    draw_sun(screen, current_season)
    
    # Draw clouds (except in winter)
    if current_season != 2:
        draw_clouds(screen)
    
    # Draw falling leaves
    for leaf in falling_leaves:
        pygame.draw.ellipse(
            screen, 
            leaf['color'], 
            (leaf['x'], leaf['y'], leaf['size'], leaf['size'] * 1.5)
        )
    
    # Draw ground
    draw_ground(screen)
    
    # Draw tree
    tree.draw(screen, wind_direction, wind_strength)
    
    # Draw UI
    season_text = font.render(f"Season: {season_names[current_season]}", True, (30, 30, 30))
    instructions = [
        "SPACE: New Tree",
        "← →: Change Season",
        "ESC: Quit"
    ]
    
    # Draw semi-transparent background for text
    text_bg = pygame.Surface((WIDTH, 140), pygame.SRCALPHA)
    text_bg.fill((255, 255, 255, 180))
    screen.blit(text_bg, (0, HEIGHT - 140))
    
    # Draw season name
    screen.blit(season_texts[current_season], (WIDTH // 2 - season_texts[current_season].get_width() // 2, HEIGHT - 130))
    
    # Draw instructions
    for i, text in enumerate(instructions):
        text_surf = font.render(text, True, (50, 50, 50))
        screen.blit(text_surf, (20, HEIGHT - 90 + i*25))
    
    # Draw wind indicator
    if wind_strength > 0:
        wind_text = font.render(f"Wind: {wind_strength}", True, (50, 50, 50))
        screen.blit(wind_text, (WIDTH - 120, 20))
        
        # Draw wind direction indicator
        arrow_x = WIDTH - 70
        arrow_y = 50
        end_x = arrow_x + math.sin(wind_direction) * 30
        end_y = arrow_y + math.cos(wind_direction) * 15
        pygame.draw.line(screen, (100, 100, 100), (arrow_x, arrow_y), (end_x, end_y), 2)
        pygame.draw.polygon(screen, (100, 100, 100), [
            (end_x, end_y),
            (end_x - math.sin(wind_direction + 0.5) * 8, end_y - math.cos(wind_direction + 0.5) * 8),
            (end_x - math.sin(wind_direction - 0.5) * 8, end_y - math.cos(wind_direction - 0.5) * 8)
        ])
    
    pygame.display.flip()
    clock.tick(60)
