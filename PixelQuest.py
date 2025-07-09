import pygame
import random

pygame.init()

WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Balls Animation")

clock = pygame.time.Clock()

# Ball class
class Ball:
    def __init__(self):
        self.radius = random.randint(15, 30)
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(self.radius, HEIGHT - self.radius)
        self.color = [random.randint(50, 255) for _ in range(3)]
        self.speed_x = random.choice([-5, -4, -3, 3, 4, 5])
        self.speed_y = random.choice([-5, -4, -3, 3, 4, 5])

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce off walls
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.speed_x = -self.speed_x
            self.change_color()

        if self.y <= self.radius or self.y >= HEIGHT - self.radius:
            self.speed_y = -self.speed_y
            self.change_color()

    def change_color(self):
        # Change to a random bright color on bounce
        self.color = [random.randint(50, 255) for _ in range(3)]

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

def main():
    balls = [Ball() for _ in range(10)]  # 10 bouncing balls
    running = True

    while running:
        clock.tick(60)
        screen.fill((30, 30, 30))  # dark background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for ball in balls:
            ball.move()
            ball.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
