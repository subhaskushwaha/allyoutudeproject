import turtle
import math
import random
import time

# Setup screen
screen = turtle.Screen()
screen.setup(800, 800)
screen.bgcolor("black")
screen.title("Love Design")
screen.tracer(0)  # Fast drawing

# Turtles
t = turtle.Turtle()
t.hideturtle()
t.speed(0)

circle_turtle = turtle.Turtle()
circle_turtle.hideturtle()
circle_turtle.speed(0)

text_turtle = turtle.Turtle()
text_turtle.hideturtle()
text_turtle.speed(0)
text_turtle.color("white")

# Draw heart
def draw_heart(turt, x, y, size, color):
    turt.penup()
    turt.goto(x, y)
    turt.pendown()
    turt.color(color)
    turt.begin_fill()
    for i in range(100):
        angle = 0.2 * i
        dx = size * 16 * (math.sin(angle) ** 3)
        dy = size * (13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * angle) - math.cos(4 * angle))
        turt.goto(x + dx, y + dy)
    turt.end_fill()

# Write "Love" text
def write_love_texts(positions, visible):
    text_turtle.clear()
    if visible:
        for x, y, size in positions:
            text_turtle.penup()
            text_turtle.goto(x, y - size * 5)
            text_turtle.write("Love", align="center", font=("Arial", int(size * 20), "bold"))

# Center message
def write_text():
    t.penup()
    t.goto(0, -100)
    t.color("white")

# Floating hearts
def floating_hearts():
    for _ in range(30):
        x = random.randint(-350, 350)
        y = random.randint(-300, 300)
        size = random.uniform(0.1, 0.25)
        color = random.choice(["#ff9999", "#ff6666", "#ff3333", "#ff0000"])
        draw_heart(t, x, y, size, color)

# Circle hearts and return positions for text blinking
def draw_circles_of_hearts():
    positions = []
    radii = [100, 150, 200, 250, 300]
    colors = ["#ff6666", "#ff4d4d", "#ff3333", "#ff1a1a", "#e60000"]
    for idx, radius in enumerate(radii):
        for angle in range(0, 360, 30):
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            draw_heart(circle_turtle, x, y, 0.3, colors[idx])
            positions.append((x, y, 0.3))
    return positions

# Main function
def main():
    draw_heart(t, 0, 0, 1, "#ff0000")         # Big center heart
    positions = draw_circles_of_hearts()      # Circular hearts
    floating_hearts()                         # Random small hearts
    write_text()                              # Center text
    screen.update()

    # Blinking lap-lup "Love" text
    for _ in range(10):  # 10 blinks
        write_love_texts(positions, True)
        screen.update()
        time.sleep(0.4)
        write_love_texts(positions, False)
        screen.update()
        time.sleep(0.3)

    # Final state: show text
    write_love_texts(positions, True)
    screen.update()

# Run
if __name__ == "__main__":
    main()
    turtle.done()
