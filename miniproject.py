import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Animation")

# Colors
BACKGROUND = (10, 10, 30)
BALL_COLORS = [
    (255, 105, 97),  # Coral
    (255, 180, 128), # Peach
    (248, 243, 141), # Yellow
    (66, 214, 164),  # Mint
    (8, 202, 209),   # Turquoise
    (89, 173, 246),  # Light Blue
    (157, 148, 255), # Lavender
    (199, 128, 232)  # Purple
]

# Ball class
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(15, 40)
        self.color = random.choice(BALL_COLORS)
        self.dx = random.uniform(-4, 4)
        self.dy = random.uniform(-4, 4)
        self.gravity = 0.2
        self.elasticity = 0.8
        
    def move(self):
        # Apply gravity
        self.dy += self.gravity
        
        # Move the ball
        self.x += self.dx
        self.y += self.dy
        
        # Boundary collision
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = -self.dx * self.elasticity
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.dx = -self.dx * self.elasticity
            
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = -self.dy * self.elasticity
        elif self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.dy = -self.dy * self.elasticity
            self.dx *= 0.9  # ground friction
    
    def draw(self, surface):
        # Gradient effect
        for i in range(self.radius, 0, -1):
            alpha = i / self.radius
            color = (
                max(0, min(255, int(self.color[0] * alpha))),
                max(0, min(255, int(self.color[1] * alpha))),
                max(0, min(255, int(self.color[2] * alpha)))
            )
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), i)

        # Highlight using alpha surface
        highlight_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            highlight_surface,
            (255, 255, 255, 150),
            (self.radius, self.radius),
            int(self.radius / 4)
        )
        surface.blit(highlight_surface, (int(self.x - self.radius / 3), int(self.y - self.radius / 3)))

# Create balls
balls = [Ball(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(8)]

# Fonts
font = pygame.font.SysFont(None, 24)
title_font = pygame.font.SysFont(None, 48)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                balls.append(Ball(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            balls.append(Ball(event.pos[0], event.pos[1]))
    
    # Update
    for ball in balls:
        ball.move()
    
    # Draw background
    screen.fill(BACKGROUND)
    
    # Grid
    for x in range(0, WIDTH, 20):
        pygame.draw.line(screen, (30, 30, 50), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 20):
        pygame.draw.line(screen, (30, 30, 50), (0, y), (WIDTH, y), 1)
    
    # Draw balls
    for ball in balls:
        ball.draw(screen)
    
    # Draw title and info
    title = title_font.render("Bouncing Ball Animation", True, (220, 220, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    
    instructions = [
        "Click to add a ball",
        "Press SPACE to add a random ball",
        "Press ESC to exit",
        f"Balls: {len(balls)}"
    ]
    
    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, (180, 180, 220))
        screen.blit(text_surface, (20, 20 + i * 30))
    
    footer = font.render("PyGame Animation Mini-Project", True, (150, 150, 180))
    screen.blit(footer, (WIDTH // 2 - footer.get_width() // 2, HEIGHT - 40))
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
