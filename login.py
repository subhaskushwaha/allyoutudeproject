import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Fireworks Simulator")

# Colors
NIGHT_BLUE = (5, 10, 30)
BUILDING_COLOR = (30, 30, 50)
BUILDING_WINDOW = (200, 200, 100)
MOUNTAIN_COLOR = (20, 25, 40)
WATER_COLOR = (10, 60, 100, 100)
WATER_HIGHLIGHT = (150, 200, 255, 50)

# Particle class for fireworks
class Particle:
    def __init__(self, x, y, color, velocity_x, velocity_y, radius, decay_rate=0.97, gravity=0.1):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.radius = radius
        self.original_radius = radius
        self.decay_rate = decay_rate
        self.gravity = gravity
        self.life = 1.0
        self.trail = []
        self.max_trail = 10
        
    def update(self):
        self.velocity_y += self.gravity
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.life *= self.decay_rate
        self.radius = self.original_radius * self.life
        
        # Add current position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
            
    def draw(self, surface):
        # Draw trail
        for i, (trail_x, trail_y) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * self.life
            trail_color = (
                min(255, self.color[0] + 50),
                min(255, self.color[1] + 50),
                min(255, self.color[2] + 50),
                alpha
            )
            s = pygame.Surface((self.original_radius*2, self.original_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, trail_color, (self.original_radius, self.original_radius), 
                              self.original_radius * (i / len(self.trail)))
            surface.blit(s, (trail_x - self.original_radius, trail_y - self.original_radius))
        
        # Draw main particle
        if self.radius > 0.1:
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.color, (self.radius, self.radius), self.radius)
            surface.blit(s, (self.x - self.radius, self.y - self.radius))

# Firework class
class Firework:
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color or (
            random.randint(200, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        self.particles = []
        self.exploded = False
        self.velocity_y = random.uniform(-12, -8)
        self.radius = 3
        self.gravity = 0.1
        
    def update(self):
        if not self.exploded:
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            
            # Random chance to explode
            if self.velocity_y >= 0 or random.random() < 0.02:
                self.explode()
        else:
            # Update particles
            for particle in self.particles[:]:
                particle.update()
                if particle.life < 0.1 or particle.radius < 0.1:
                    self.particles.remove(particle)
                    
    def explode(self):
        self.exploded = True
        explosion_type = random.choice(["circle", "ring", "willow", "double_ring", "spiral"])
        particle_count = random.randint(50, 200)
        
        if explosion_type == "circle":
            for _ in range(particle_count):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(1, 5)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                self.particles.append(Particle(
                    self.x, self.y, 
                    self.color, vx, vy, 
                    random.uniform(1, 3)
                )
                
        elif explosion_type == "ring":
            for i in range(particle_count):
                angle = (i / particle_count) * math.pi * 2
                speed = random.uniform(2, 3)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                self.particles.append(Particle(
                    self.x, self.y, 
                    self.color, vx, vy, 
                    random.uniform(1, 2)
                )
                
        elif explosion_type == "willow":
            for _ in range(particle_count):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(1, 3)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                particle = Particle(
                    self.x, self.y, 
                    self.color, vx, vy, 
                    random.uniform(1, 2),
                    decay_rate=0.98,
                    gravity=0.05
                )
                particle.max_trail = 20
                self.particles.append(particle)
                
        elif explosion_type == "double_ring":
            for i in range(particle_count//2):
                angle = (i / (particle_count//2)) * math.pi * 2
                speed1 = random.uniform(1, 2)
                speed2 = random.uniform(3, 4)
                
                # Inner ring
                vx1 = math.cos(angle) * speed1
                vy1 = math.sin(angle) * speed1
                self.particles.append(Particle(
                    self.x, self.y, 
                    self.color, vx1, vy1, 
                    random.uniform(1, 2)
                )
                
                # Outer ring
                vx2 = math.cos(angle) * speed2
                vy2 = math.sin(angle) * speed2
                self.particles.append(Particle(
                    self.x, self.y, 
                    self.color, vx2, vy2, 
                    random.uniform(1, 2)
                )
                
        elif explosion_type == "spiral":
            for i in range(particle_count):
                angle = (i / particle_count) * math.pi * 4
                radius = (i / particle_count) * 5
                vx = math.cos(angle) * radius
                vy = math.sin(angle) * radius
                self.particles.append(Particle(
                    self.x, self.y, 
                    self.color, vx, vy, 
                    random.uniform(1, 2),
                    decay_rate=0.96
                )
    
    def draw(self, surface):
        if not self.exploded:
            # Draw rising firework
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            
            # Draw trail
            for i in range(5):
                trail_y = self.y + i * 3
                alpha = 255 - i * 50
                trail_color = (*self.color, alpha)
                s = pygame.Surface((4, 4), pygame.SRCALPHA)
                pygame.draw.circle(s, trail_color, (2, 2), 2 - i * 0.3)
                surface.blit(s, (self.x - 2, trail_y - 2))
        else:
            # Draw particles
            for particle in self.particles:
                particle.draw(surface)

# Building class for cityscape
class Building:
    def __init__(self, x, width, height):
        self.x = x
        self.width = width
        self.height = height
        self.windows = []
        
        # Create windows
        for row in range(random.randint(3, 8)):
            for col in range(random.randint(2, 5)):
                if random.random() > 0.3:  # Not all windows are lit
                    self.windows.append({
                        'x': self.x + col * (self.width // 4) + random.randint(5, 15),
                        'y': HEIGHT - self.height + row * 20 + random.randint(5, 15),
                        'brightness': random.uniform(0.3, 1.0),
                        'flicker_speed': random.uniform(0.01, 0.05)
                    })
    
    def update(self):
        # Update window brightness
        for window in self.windows:
            window['brightness'] = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * window['flicker_speed'])
            
    def draw(self, surface):
        # Draw building
        pygame.draw.rect(surface, BUILDING_COLOR, (self.x, HEIGHT - self.height, self.width, self.height))
        
        # Draw windows
        for window in self.windows:
            brightness = window['brightness']
            color = (
                int(BUILDING_WINDOW[0] * brightness),
                int(BUILDING_WINDOW[1] * brightness),
                int(BUILDING_WINDOW[2] * brightness)
            )
            pygame.draw.rect(surface, color, (window['x'], window['y'], 8, 12))

# Create cityscape
buildings = []
for i in range(20):
    x = i * 50 + random.randint(-10, 10)
    width = random.randint(30, 70)
    height = random.randint(100, 400)
    buildings.append(Building(x, width, height))

# Create mountains in background
mountains = []
for i in range(10):
    x = i * 200 - 100
    height = random.randint(50, 150)
    mountains.append((x, HEIGHT - height, 200, height))

# Create water reflection
water_surface = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)

# Create initial fireworks
fireworks = []

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Create firework at mouse position
            fireworks.append(Firework(event.pos[0], event.pos[1]))
    
    # Randomly generate new fireworks
    if random.random() < 0.05 and len(fireworks) < 10:
        fireworks.append(Firework(random.randint(100, WIDTH-100), random.randint(100, HEIGHT//2)))
    
    # Fill the screen with night blue
    screen.fill(NIGHT_BLUE)
    
    # Draw stars
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT//2)
        brightness = random.uniform(0.3, 1.0)
        size = random.uniform(0.5, 2)
        pygame.draw.circle(screen, 
                          (int(255 * brightness), int(255 * brightness), int(255 * brightness)), 
                          (x, y), size)
    
    # Draw mountains
    for mountain in mountains:
        pygame.draw.rect(screen, MOUNTAIN_COLOR, mountain)
        # Add some mountain details
        pygame.draw.line(screen, (10, 15, 30), 
                         (mountain[0], mountain[1]), 
                         (mountain[0] + mountain[2], mountain[1]), 3)
    
    # Draw water surface
    water_surface.fill((0, 0, 0, 0))
    pygame.draw.rect(water_surface, WATER_COLOR, (0, 0, WIDTH, 100))
    
    # Add water highlights
    for _ in range(20):
        x = random.randint(0, WIDTH)
        width = random.randint(20, 100)
        pygame.draw.ellipse(water_surface, WATER_HIGHLIGHT, (x, random.randint(0, 20), width, 5))
    
    screen.blit(water_surface, (0, HEIGHT - 100))
    
    # Update and draw buildings
    for building in buildings:
        building.update()
        building.draw(screen)
    
    # Update and draw fireworks
    for firework in fireworks[:]:
        firework.update()
        firework.draw(screen)
        
        # Remove finished fireworks
        if firework.exploded and len(firework.particles) == 0:
            fireworks.remove(firework)
    
    # Draw water reflection of fireworks
    for firework in fireworks:
        if firework.exploded:
            for particle in firework.particles:
                # Only reflect particles near the water
                if particle.y > HEIGHT - 150:
                    # Draw reflection
                    reflection_y = HEIGHT - (particle.y - (HEIGHT - 150))
                    alpha = min(255, int(255 * (1 - (reflection_y - (HEIGHT - 150)) / 150))
                    
                    if alpha > 10:
                        # Draw particle reflection
                        s = pygame.Surface((particle.radius*2, particle.radius*2), pygame.SRCALPHA)
                        pygame.draw.circle(s, (*particle.color[:3], alpha//2), 
                                          (particle.radius, particle.radius), particle.radius)
                        screen.blit(s, (particle.x - particle.radius, reflection_y - particle.radius))
    
    # Draw title
    title_font = pygame.font.SysFont('arial', 36, bold=True)
    title = title_font.render("Interactive Fireworks Simulator", True, (255, 255, 200))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Draw instructions
    instr_font = pygame.font.SysFont('arial', 16)
    instructions = [
        "Click anywhere to launch a firework",
        "Fireworks automatically generate",
        "Press ESC to exit"
    ]
    
    for i, text in enumerate(instructions):
        rendered = instr_font.render(text, True, (200, 230, 255))
        screen.blit(rendered, (WIDTH//2 - rendered.get_width()//2, 70 + i*25))
    
    # Draw firework counter
    count_text = instr_font.render(f"Active Fireworks: {len(fireworks)}", True, (255, 255, 200))
    screen.blit(count_text, (20, HEIGHT - 30))
    
    # Draw type counter
    types = ["Circle", "Ring", "Willow", "Double Ring", "Spiral"]
    type_text = instr_font.render("Firework Types: " + ", ".join(types), True, (200, 230, 255))
    screen.blit(type_text, (WIDTH - type_text.get_width() - 20, HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()