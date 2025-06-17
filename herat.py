import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import to_rgb

def draw_heart(size, color, x_offset=0, y_offset=0, alpha=0.3):
    t = np.linspace(0, 2*np.pi, 1000)
    x = size * 16 * np.sin(t)**3
    y = size * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t))
    plt.plot(x + x_offset, y + y_offset, color=color, linewidth=2)
    plt.fill(x + x_offset, y + y_offset, color=color, alpha=alpha)

# Create figure
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('Colorful Dancing Hearts', pad=20)

# Draw main outer heart (fixed)
draw_heart(1, 'red', 0, 0, alpha=0.1)

# Number of moving inner hearts
num_hearts = 12
base_colors = ['red', 'pink', 'magenta', 'orange', 'purple', 'hotpink']

# Store heart objects for animation
heart_lines = []
heart_fills = []

for i in range(num_hearts):
    size = 0.6 - (i * 0.03)
    line, = ax.plot([], [], color=base_colors[i%len(base_colors)], linewidth=1.5)
    fill = ax.fill([], [], color=base_colors[i%len(base_colors)], alpha=0.7)[0]
    heart_lines.append(line)
    heart_fills.append(fill)

# Animation function
def update(frame):
    for i, (line, fill) in enumerate(zip(heart_lines, heart_fills)):
        # Faster movement with frame*2
        angle = 2 * np.pi * (frame/50 + i/num_hearts)  # Changed denominator to 50 for faster speed
        
        # More dynamic radius variation
        radius = 0.4 * (1 - i/(2*num_hearts)) * (0.9 + 0.1*np.sin(frame/10))
        
        x_offset = radius * np.cos(angle)
        y_offset = radius * np.sin(angle)
        
        size = 0.6 - (i * 0.03)
        t = np.linspace(0, 2*np.pi, 100)
        x = size * 16 * np.sin(t)**3 + x_offset
        y = size * (13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)) + y_offset
        
        # Dynamic color changes
        hue = (frame/100 + i/num_hearts) % 1.0
        r, g, b = to_rgb(plt.cm.hsv(hue))
        color = (r, g, b, 0.7)
        
        line.set_data(x, y)
        line.set_color(color)
        fill.set_xy(np.column_stack([x, y]))
        fill.set_color(color)
        fill.set_alpha(0.5 + 0.3*np.sin(frame/20 + i))  # Pulsing alpha
    
    return heart_lines + heart_fills

# Create faster animation (interval=30 makes it faster than 50)
ani = FuncAnimation(fig, update, frames=200, interval=30, blit=True)

plt.tight_layout()
plt.show()