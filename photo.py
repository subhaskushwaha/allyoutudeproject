import pygame
import math
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lord Hanuman - Animated Visualization")

# Colors
BACKGROUND = (10, 20, 40)
HANUMAN_SKIN = (220, 180, 140)
HANUMAN_OUTLINE = (40, 30, 20)
HANUMAN_CLOTHES = (200, 40, 20)  # Deep red
HANUMAN_CROWN = (240, 200, 30)   # Gold
HALO_COLOR = (255, 220, 100, 180)  # Yellow with alpha
MOUNTAIN_COLOR = (80, 60, 40)
MOUNTAIN_HIGHLIGHT = (120, 90, 60)
MACE_COLOR = (180, 160, 140)
MACE_HIGHLIGHT = (200, 180, 160)
SUN_COLOR = (255, 220, 100)
CLOUD_COLOR = (220, 230, 240, 200)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Function to draw a cloud
def draw_cloud(surface, x, y, size, time_offset):
    pulse = math.sin(pygame.time.get_ticks() / 1000 + time_offset) * 0.1 + 1
    size = int(size * pulse)
    
    # Draw cloud with semi-transparent circles
    cloud_surf = pygame.Surface((size * 3, size * 2), pygame.SRCALPHA)
    pygame.draw.circle(cloud_surf, CLOUD_COLOR, (size, size), size)
    pygame.draw.circle(cloud_surf, CLOUD_COLOR, (size * 2, size // 2), size // 1.5)
    pygame.draw.circle(cloud_surf, CLOUD_COLOR, (size * 2, size * 1.5), size // 1.5)
    pygame.draw.circle(cloud_surf, CLOUD_COLOR, (size * 3, size), size)
    
    surface.blit(cloud_surf, (x - size * 1.5, y - size))

# Function to draw the flying mountain
def draw_mountain(surface, x, y, scale, angle):
    mountain_points = [
        (x, y - 60 * scale),
        (x - 40 * scale, y + 20 * scale),
        (x + 40 * scale, y + 20 * scale)
    ]
    
    # Rotate the mountain
    rotated_points = []
    for point in mountain_points:
        px, py = point
        # Translate point back to origin
        px -= x
        py -= y
        
        # Rotate point
        rotated_x = px * math.cos(angle) - py * math.sin(angle)
        rotated_y = px * math.sin(angle) + py * math.cos(angle)
        
        # Translate back
        rotated_points.append((rotated_x + x, rotated_y + y))
    
    pygame.draw.polygon(surface, MOUNTAIN_COLOR, rotated_points)
    pygame.draw.polygon(surface, HANUMAN_OUTLINE, rotated_points, 2)
    
    # Draw mountain details
    pygame.draw.line(surface, MOUNTAIN_HIGHLIGHT, 
                    (rotated_points[0][0], rotated_points[0][1]),
                    ((rotated_points[1][0] + rotated_points[2][0])/2, 
                     (rotated_points[1][1] + rotated_points[2][1])/2), 2)
    
    # Draw plants on mountain
    for i in range(3):
        plant_x = rotated_points[0][0] + (i-1) * 15 * scale
        plant_y = rotated_points[0][1] + 20 * scale
        pygame.draw.circle(surface, (40, 100, 40), (plant_x, plant_y), 8 * scale)
        pygame.draw.circle(surface, (30, 80, 30), (plant_x + 3 * scale, plant_y - 5 * scale), 6 * scale)

# Function to draw Hanuman's mace (gada)
def draw_mace(surface, x, y, angle):
    # Mace handle
    handle_length = 80
    handle_end_x = x + handle_length * math.cos(angle)
    handle_end_y = y + handle_length * math.sin(angle)
    
    pygame.draw.line(surface, MACE_COLOR, (x, y), (handle_end_x, handle_end_y), 8)
    pygame.draw.line(surface, MACE_HIGHLIGHT, (x, y), (handle_end_x, handle_end_y), 3)
    
    # Mace head
    mace_head_x = handle_end_x + 25 * math.cos(angle)
    mace_head_y = handle_end_y + 25 * math.sin(angle)
    
    pygame.draw.circle(surface, MACE_COLOR, (mace_head_x, mace_head_y), 20)
    pygame.draw.circle(surface, MACE_HIGHLIGHT, (mace_head_x, mace_head_y), 20, 2)
    
    # Spikes
    for i in range(8):
        spike_angle = angle + i * math.pi / 4
        spike_x = mace_head_x + 25 * math.cos(spike_angle)
        spike_y = mace_head_y + 25 * math.sin(spike_angle)
        pygame.draw.line(surface, MACE_HIGHLIGHT, 
                        (mace_head_x, mace_head_y), (spike_x, spike_y), 3)

# Function to draw Lord Hanuman
def draw_hanuman(surface, x, y, scale, frame):
    # Calculate movement for flying effect
    fly_offset = math.sin(frame / 10) * 5
    
    # Draw halo
    halo_surf = pygame.Surface((150 * scale, 150 * scale), pygame.SRCALPHA)
    pygame.draw.circle(halo_surf, HALO_COLOR, (75 * scale, 75 * scale), 70 * scale)
    
    # Draw pulsing glow
    pulse = abs(math.sin(frame / 8)) * 0.3 + 0.7
    glow_size = int(100 * scale * pulse)
    pygame.draw.circle(halo_surf, (255, 255, 200, 100), 
                      (75 * scale, 75 * scale), glow_size)
    
    surface.blit(halo_surf, (x - 75 * scale, y - 100 * scale - fly_offset))
    
    # Draw head
    pygame.draw.circle(surface, HANUMAN_SKIN, (x, y - 40 * scale - fly_offset), 30 * scale)
    pygame.draw.circle(surface, HANUMAN_OUTLINE, (x, y - 40 * scale - fly_offset), 30 * scale, 2)
    
    # Draw face details
    # Eyes
    pygame.draw.ellipse(surface, HANUMAN_OUTLINE, 
                       (x - 20 * scale, y - 50 * scale - fly_offset, 12 * scale, 8 * scale))
    pygame.draw.ellipse(surface, HANUMAN_OUTLINE, 
                       (x + 8 * scale, y - 50 * scale - fly_offset, 12 * scale, 8 * scale))
    
    # Nose
    pygame.draw.circle(surface, HANUMAN_SKIN, (x, y - 35 * scale - fly_offset), 8 * scale)
    
    # Mouth
    mouth_y = y - 25 * scale - fly_offset + math.sin(frame / 5) * 1
    pygame.draw.arc(surface, HANUMAN_OUTLINE, 
                   (x - 15 * scale, mouth_y - 5 * scale, 30 * scale, 20 * scale), 
                   0, math.pi, 2)
    
    # Crown
    crown_points = [
        (x - 30 * scale, y - 65 * scale - fly_offset),
        (x, y - 90 * scale - fly_offset),
        (x + 30 * scale, y - 65 * scale - fly_offset)
    ]
    pygame.draw.polygon(surface, HANUMAN_CROWN, crown_points)
    pygame.draw.polygon(surface, HANUMAN_OUTLINE, crown_points, 2)
    pygame.draw.circle(surface, (240, 240, 250), (x, y - 90 * scale - fly_offset), 8 * scale)
    
    # Draw torso
    pygame.draw.rect(surface, HANUMAN_CLOTHES, 
                    (x - 25 * scale, y - 40 * scale - fly_offset, 50 * scale, 60 * scale))
    pygame.draw.rect(surface, HANUMAN_OUTLINE, 
                    (x - 25 * scale, y - 40 * scale - fly_offset, 50 * scale, 60 * scale), 2)
    
    # Draw necklace
    pygame.draw.circle(surface, HANUMAN_CROWN, (x, y - 20 * scale - fly_offset), 5 * scale)
    pygame.draw.circle(surface, HANUMAN_CROWN, (x - 10 * scale, y - 15 * scale - fly_offset), 4 * scale)
    pygame.draw.circle(surface, HANUMAN_CROWN, (x + 10 * scale, y - 15 * scale - fly_offset), 4 * scale)
    
    # Draw arms
    arm_swing = math.sin(frame / 8) * 0.3
    
    # Right arm
    pygame.draw.line(surface, HANUMAN_SKIN, 
                    (x + 25 * scale, y - 20 * scale - fly_offset),
                    (x + 60 * scale, y + 20 * scale - fly_offset), 12 * scale)
    
    # Left arm (holding mountain)
    arm_angle = math.pi * 0.7 + arm_swing
    elbow_x = x - 25 * scale + 30 * scale * math.cos(arm_angle)
    elbow_y = y - 20 * scale - fly_offset + 30 * scale * math.sin(arm_angle)
    
    pygame.draw.line(surface, HANUMAN_SKIN, 
                    (x - 25 * scale, y - 20 * scale - fly_offset),
                    (elbow_x, elbow_y), 12 * scale)
    
    hand_angle = arm_angle + math.pi * 0.3
    hand_x = elbow_x + 40 * scale * math.cos(hand_angle)
    hand_y = elbow_y + 40 * scale * math.sin(hand_angle)
    
    pygame.draw.line(surface, HANUMAN_SKIN, 
                    (elbow_x, elbow_y),
                    (hand_x, hand_y), 10 * scale)
    
    # Draw hands
    pygame.draw.circle(surface, HANUMAN_SKIN, 
                      (x + 60 * scale, y + 20 * scale - fly_offset), 8 * scale)
    pygame.draw.circle(surface, HANUMAN_SKIN, (hand_x, hand_y), 8 * scale)
    
    # Draw legs
    leg_swing = math.sin(frame / 8 + math.pi) * 0.4
    
    # Right leg
    pygame.draw.line(surface, HANUMAN_CLOTHES, 
                    (x + 10 * scale, y + 20 * scale - fly_offset),
                    (x + 30 * scale, y + 70 * scale - fly_offset), 15 * scale)
    
    # Left leg
    leg_angle = math.pi * 0.8 + leg_swing
    knee_x = x - 10 * scale + 30 * scale * math.cos(leg_angle)
    knee_y = y + 20 * scale - fly_offset + 30 * scale * math.sin(leg_angle)
    
    pygame.draw.line(surface, HANUMAN_CLOTHES, 
                    (x - 10 * scale, y + 20 * scale - fly_offset),
                    (knee_x, knee_y), 15 * scale)
    
    foot_angle = leg_angle + math.pi * 0.3
    foot_x = knee_x + 40 * scale * math.cos(foot_angle)
    foot_y = knee_y + 40 * scale * math.sin(foot_angle)
    
    pygame.draw.line(surface, HANUMAN_CLOTHES, 
                    (knee_x, knee_y),
                    (foot_x, foot_y), 12 * scale)
    
    # Draw feet
    pygame.draw.circle(surface, HANUMAN_SKIN, 
                      (x + 30 * scale, y + 70 * scale - fly_offset), 8 * scale)
    pygame.draw.circle(surface, HANUMAN_SKIN, (foot_x, foot_y), 8 * scale)
    
    # Draw tail
    tail_points = [
        (x + 30 * scale, y + 20 * scale - fly_offset),
        (x + 60 * scale, y + 10 * scale - fly_offset),
        (x + 80 * scale, y - 10 * scale - fly_offset),
        (x + 90 * scale + math.sin(frame / 5) * 10 * scale, 
         y - 30 * scale - fly_offset + math.cos(frame / 5) * 5 * scale),
        (x + 70 * scale, y - 20 * scale - fly_offset)
    ]
    pygame.draw.lines(surface, HANUMAN_OUTLINE, False, tail_points, 5)
    
    # Draw the mountain in Hanuman's hand
    mountain_scale = scale * 0.6
    mountain_x = hand_x + 5 * scale
    mountain_y = hand_y + 10 * scale
    mountain_angle = math.sin(frame / 15) * 0.1
    draw_mountain(surface, mountain_x, mountain_y, mountain_scale, mountain_angle)
    
    # Draw the mace in Hanuman's other hand
    mace_angle = math.pi * 0.2 + math.sin(frame / 7) * 0.1
    draw_mace(surface, x + 60 * scale, y + 20 * scale - fly_offset, mace_angle)
    
    # Draw divine energy from feet
    for i in range(5):
        energy_x = foot_x + random.uniform(-10, 10)
        energy_y = foot_y + 20 + i * 10
        energy_size = random.uniform(5, 15)
        energy_alpha = random.randint(100, 200)
        energy_color = (255, 220, 100, energy_alpha)
        
        energy_surf = pygame.Surface((energy_size * 2, energy_size * 2), pygame.SRCALPHA)
        pygame.draw.circle(energy_surf, energy_color, (energy_size, energy_size), energy_size)
        surface.blit(energy_surf, (energy_x - energy_size, energy_y - energy_size))

# Function to draw decorative elements
def draw_decoration(surface, frame):
    # Draw sun in the background
    sun_x = 100
    sun_y = 100
    pygame.draw.circle(surface, SUN_COLOR, (sun_x, sun_y), 60)
    
    # Draw sun rays
    for i in range(12):
        angle = i * math.pi / 6 + frame / 100
        ray_length = 80 + math.sin(frame / 10 + i) * 10
        ray_x = sun_x + ray_length * math.cos(angle)
        ray_y = sun_y + ray_length * math.sin(angle)
        pygame.draw.line(surface, SUN_COLOR, (sun_x, sun_y), (ray_x, ray_y), 3)
    
    # Draw clouds
    draw_cloud(surface, 200, 150, 30, 0)
    draw_cloud(surface, 700, 100, 40, 1.5)
    draw_cloud(surface, 500, 80, 35, 3)
    draw_cloud(surface, 300, 200, 25, 4.5)
    draw_cloud(surface, 800, 180, 30, 6)
    
    # Draw decorative text
    font = pygame.font.SysFont("Arial", 36, bold=True)
    text = font.render("जय श्री राम", True, (255, 255, 200))
    surface.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))
    
    # Draw floating "Om" symbols
    for i in range(5):
        om_x = 50 + i * 180
        om_y = 500 + math.sin(frame / 20 + i) * 30
        
        om_font = pygame.font.SysFont("Arial", 28)
        om_text = om_font.render("ॐ", True, (200, 220, 255, 180))
        surface.blit(om_text, (om_x, om_y))

# Main function
def main():
    frame = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Fill the background
        screen.fill(BACKGROUND)
        
        # Draw stars
        for i in range(100):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            size = random.uniform(0.5, 2)
            brightness = random.randint(150, 255)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)
        
        # Draw decoration
        draw_decoration(screen, frame)
        
        # Draw Lord Hanuman
        hanuman_x = WIDTH // 2
        hanuman_y = HEIGHT // 2 + 50
        draw_hanuman(screen, hanuman_x, hanuman_y, 1.0, frame)
        
        # Draw floating text at the bottom
        font = pygame.font.SysFont("Arial", 24)
        text = font.render("Lord Hanuman carrying the Dronagiri mountain with the Sanjeevani herb", 
                          True, (220, 220, 180))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 50))
        
        # Update the display
        pygame.display.flip()
        
        # Control the frame rate
        clock.tick(FPS)
        frame += 1

if __name__ == "__main__":
    main()