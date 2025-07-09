import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Particle Fountain Simulator")
clock = pygame.time.Clock()

# Modes
MODES = ['rainbow', 'fire', 'snow']
mode_index = 0

# Background
BACKGROUND_COLOR = (10, 10, 30)

# Particle class
class Particle:
    def __init__(self, x, y, mode='rainbow'):
        self.x = x
        self.y = y
        self.size = random.randint(3, 6)
        self.speed = random.uniform(2, 8)
        self.angle = random.uniform(math.pi / 4, 3 * math.pi / 4)  # upward spread
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -abs(math.sin(self.angle) * self.speed)
        self.gravity = 0.15
        self.bounce = 0.6
        self.life = 100
        self.mode = mode
        self.color = self.get_color(mode)

    def get_color(self, mode):
        if mode == 'rainbow':
            return random.choice([
                (255, 0, 0), (255, 165, 0), (255, 255, 0),
                (0, 255, 0), (0, 127, 255), (0, 0, 255), (139, 0, 255)
            ])
        elif mode == 'fire':
            return random.choice([(255, 80, 0), (255, 140, 0), (255, 200, 50)])
        elif mode == 'snow':
            return (240, 240, 255)

    def update(self):
        self.dy += self.gravity
        self.x += self.dx
        self.y += self.dy
        self.life -= 1

        # Bounce on ground
        if self.y + self.size > HEIGHT:
            self.y = HEIGHT - self.size
            self.dy *= -self.bounce
            self.dx *= 0.7  # friction

    def draw(self, surface):
        alpha = max(0, int(255 * (self.life / 100)))
        color = (*self.color, alpha)
        surface.set_alpha(alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

# Initialize
particles = []
font = pygame.font.SysFont(None, 28)

def draw_text(surface, text, x, y, color=(200, 200, 200)):
    label = font.render(text, True, color)
    surface.blit(label, (x, y))

def main():
    global mode_index
    trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        trail_surface.fill((0, 0, 0, 20), special_flags=pygame.BLEND_RGBA_MULT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_c:
                    particles.clear()
                elif event.key == pygame.K_1:
                    mode_index = 0
                elif event.key == pygame.K_2:
                    mode_index = 1
                elif event.key == pygame.K_3:
                    mode_index = 2

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for _ in range(50):
                    particles.append(Particle(mx, my, MODES[mode_index]))

        # Update and draw particles
        for particle in particles[:]:
            particle.update()
            if particle.life <= 0:
                particles.remove(particle)
            else:
                particle.draw(trail_surface)

        screen.blit(trail_surface, (0, 0))

        # UI
        draw_text(screen, "CLICK: Shoot Particles | 1-Rainbow  2-Fire  3-Snow  |  C: Clear  |  ESC: Quit", 10, 10)
        draw_text(screen, f"Mode: {MODES[mode_index].capitalize()} | Particles: {len(particles)}", 10, 40)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
