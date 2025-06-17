import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle, Ellipse, Rectangle, Polygon
from matplotlib.lines import Line2D  # This import was missing

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')
ax.set_title('Doraemon Animation', pad=20)

# Create Doraemon parts
body = Circle((5, 3), 1.5, fc='skyblue', ec='black')
head = Circle((5, 5), 1.2, fc='skyblue', ec='black')
face = Circle((5, 5), 1.0, fc='white', ec='black')
eyes = Ellipse((4.7, 5.3), 0.4, 0.3, fc='white', ec='black')
eyes2 = Ellipse((5.3, 5.3), 0.4, 0.3, fc='white', ec='black')
pupils = Circle((4.7, 5.3), 0.1, fc='black')
pupils2 = Circle((5.3, 5.3), 0.1, fc='black')
nose = Circle((5, 4.8), 0.15, fc='red')
mouth = Rectangle((4.5, 4.5), 1.0, 0.1, fc='black')
whiskers1 = Line2D([4.0, 4.5], [4.9, 4.8], lw=1, color='black')
whiskers2 = Line2D([4.0, 4.5], [4.7, 4.7], lw=1, color='black')
whiskers3 = Line2D([5.5, 6.0], [4.8, 4.9], lw=1, color='black')
whiskers4 = Line2D([5.5, 6.0], [4.7, 4.7], lw=1, color='black')
bell = Circle((5, 2.5), 0.15, fc='gold')
bell_line = Rectangle((5, 2.35), 0.01, 0.2, fc='gold')
pocket = Ellipse((5, 2.0), 1.0, 0.5, fc='white', ec='black')
arms = Rectangle((3.5, 2.8), 1.0, 0.3, fc='skyblue', angle=30)
arms2 = Rectangle((5.5, 2.8), 1.0, 0.3, fc='skyblue', angle=-30)
legs = Rectangle((4.0, 1.5), 0.8, 0.3, fc='white')
legs2 = Rectangle((5.2, 1.5), 0.8, 0.3, fc='white')

# Add all parts to the plot
parts = [body, head, face, eyes, eyes2, pupils, pupils2, nose, mouth, 
         whiskers1, whiskers2, whiskers3, whiskers4, bell, bell_line, 
         pocket, arms, arms2, legs, legs2]

for part in parts:
    if isinstance(part, (Circle, Ellipse, Rectangle, Polygon)):
        ax.add_patch(part)
    elif isinstance(part, Line2D):
        ax.add_line(part)

# Animation function
def update(frame):
    # Simple movement - swaying side to side
    x_offset = 0.2 * np.sin(frame/5)
    
    # Move all parts together
    for part in parts:
        if isinstance(part, Circle):
            part.center = (part.center[0] + x_offset, part.center[1])
        elif isinstance(part, Ellipse):
            part.center = (part.center[0] + x_offset, part.center[1])
        elif isinstance(part, Rectangle):
            part.set_xy((part.get_xy()[0] + x_offset, part.get_xy()[1]))
        elif isinstance(part, Line2D):
            xdata, ydata = part.get_data()
            part.set_data(xdata + x_offset, ydata)
    
    # Blinking animation every 30 frames
    if frame % 30 < 5:
        eyes.set_height(0.1)
        eyes2.set_height(0.1)
        pupils.set_visible(False)
        pupils2.set_visible(False)
    else:
        eyes.set_height(0.3)
        eyes2.set_height(0.3)
        pupils.set_visible(True)
        pupils2.set_visible(True)
    
    return parts

# Create animation
ani = FuncAnimation(fig, update, frames=200, interval=50, blit=False)

plt.tight_layout()
plt.show()