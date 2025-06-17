import pygame
import random
import math
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Digital Hourglass")

# Colors
BACKGROUND = (10, 10, 30)
SAND_COLOR = (255, 215, 100)
GLASS_COLOR = (200, 230, 255, 100)
HIGHLIGHT = (250, 250, 255)
TEXT_COLOR = (220, 220, 255)

# Sand particles
particles = []
for _ in range(500):
    particles.append({
        'x': random.randint(300, 500),
        'y': random.randint(100, 250),
        'size': random.randint(2, 5),
        'speed': random.uniform(0.5, 2),
        'sway': random.uniform(-0.5, 0.5)
    })

# Hourglass shape points (top triangle)
top_points = [(400, 50), (300, 250), (500, 250)]
bottom_points = [(400, 550), (300, 350), (500, 350)]

# Animation variables
flipped = False
reset_timer = 0
particles_collected = 0
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

def draw_hourglass():
    # Draw glass container
    pygame.draw.polygon(screen, GLASS_COLOR, top_points)
    pygame.draw.polygon(screen, GLASS_COLOR, bottom_points)
    
    # Draw glass highlights
    pygame.draw.line(screen, HIGHLIGHT, (400, 50), (300, 250), 2)
    pygame.draw.line(screen, HIGHLIGHT, (400, 50), (500, 250), 2)
    pygame.draw.line(screen, HIGHLIGHT, (400, 550), (300, 350), 2)
    pygame.draw.line(screen, HIGHLIGHT, (400, 550), (500, 350), 2)
    
    # Draw neck
    pygame.draw.rect(screen, GLASS_COLOR, (380, 250, 40, 100))
    pygame.draw.line(screen, HIGHLIGHT, (380, 250), (380, 350), 2)
    pygame.draw.line(screen, HIGHLIGHT, (420, 250), (420, 350), 2)

def reset_sand():
    global particles, flipped, particles_collected, reset_timer
    particles = []
    for _ in range(500):
        particles.append({
            'x': random.randint(300, 500),
            'y': random.randint(100, 250) if not flipped else random.randint(350, 500),
            'size': random.randint(2, 5),
            'speed': random.uniform(0.5, 2),
            'sway': random.uniform(-0.5, 0.5)
        })
    particles_collected = 0
    reset_timer = 0
    flipped = not flipped

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_sand()
    
    # Fill background
    screen.fill(BACKGROUND)
    
    # Draw hourglass
    draw_hourglass()
    
    # Update and draw particles
    for p in particles[:]:
        # Move particles
        if not flipped:
            p['y'] += p['speed']
            p['x'] += p['sway']
        else:
            p['y'] -= p['speed']
            p['x'] += p['sway']
        
        # Constrain particles within hourglass
        if not flipped and p['y'] > 350 and 380 <= p['x'] <= 420:
            if p['y'] > 450:
                particles_collected += 1
                particles.remove(p)
                continue
        elif flipped and p['y'] < 250 and 380 <= p['x'] <= 420:
            if p['y'] < 150:
                particles_collected += 1
                particles.remove(p)
                continue
        
        # Draw particle
        pygame.draw.circle(screen, SAND_COLOR, (int(p['x']), int(p['y'])), p['size'])
    
    # Auto-reset when all sand falls
    if particles_collected >= 500:
        reset_timer += 1
        if reset_timer > 180:  # 3 seconds delay
            reset_sand()
    
    # Display instructions
    text = font.render("Press SPACE to flip hourglass", True, TEXT_COLOR)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 20))
    
    # Display particle count
    count_text = font.render(f"Sand Particles: {len(particles)}/500", True, TEXT_COLOR)
    screen.blit(count_text, (WIDTH//2 - count_text.get_width()//2, HEIGHT - 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()