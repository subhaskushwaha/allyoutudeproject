import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colorful Bouncing Balls with Particle Trails")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(15, 30)
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(3, 7)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.gravity = 0.1
        self.elasticity = 0.8
        self.trail = []
        self.max_trail_length = 20
        
    def move(self):
        # Apply gravity
        self.dy += self.gravity
        
        # Update position
        self.x += self.dx
        self.y += self.dy
        
        # Wall collision
        if self.x - self.radius < 0:
            self.x = self.radius
            self.dx = -self.dx * self.elasticity
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.dx = -self.dx * self.elasticity
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.dy = -self.dy * self.elasticity
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.dy = -self.dy * self.elasticity
            
        # Add current position to trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)
    
    def draw(self, surface):
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)))
            radius = int(self.radius * (i / len(self.trail)))
            color = (
                min(255, self.color[0] + i * 2),
                min(255, self.color[1] + i * 2),
                min(255, self.color[2] + i * 2)
            )
            pygame.draw.circle(surface, color, (int(pos[0]), int(pos[1])), max(1, radius))
        
        # Draw main ball
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), self.radius - 5, 2)

# Particle effect for collisions
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        self.lifetime = random.randint(20, 40)
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
        
    def draw(self, surface):
        alpha = min(255, self.lifetime * 6)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

# Create balls
balls = [Ball(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(8)]
particles = []

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(Ball(event.pos[0], event.pos[1]))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                balls = [Ball(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) for _ in range(8)]
                particles = []
    
    # Move balls
    for ball in balls:
        ball.move()
    
    # Create particles
    if random.random() < 0.3:
        for ball in balls:
            particles.append(Particle(
                ball.x + random.randint(-10, 10),
                ball.y + random.randint(-10, 10),
                ball.color
            ))
    
    # Move and filter particles
    particles = [p for p in particles if p.lifetime > 0]
    for p in particles:
        p.move()
    
    # Drawing
    screen.fill((0, 0, 0))
    
    # Draw particles
    for p in particles:
        p.draw(screen)
    
    # Draw balls
    for ball in balls:
        ball.draw(screen)
    
    # Draw instructions
    font = pygame.font.SysFont(None, 24)
    text = font.render("Click to add balls | SPACE: Reset | ESC: Quit", True, (200, 200, 200))
    screen.blit(text, (10, HEIGHT - 30))
    
    pygame.display.flip()
    clock.tick(60)