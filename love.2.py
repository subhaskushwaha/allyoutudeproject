import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Set up the figure
fig, ax = plt.subplots()
fig.set_facecolor("black")
ax.set_facecolor("black")
ax.axis('off')

# Set plot limits
ax.set_xlim(-30, 30)
ax.set_ylim(-30, 30)
ax.set_aspect('equal')

# Heart shape function
def heart_shape(t, scale):
    x = scale * 16 * np.sin(t)**3
    y = scale * (13 * np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t))
    return x, y

t = np.linspace(0, 2*np.pi, 300)
scales = np.linspace(0.2, 1.8, 20)

lines = []
for _ in scales:
    line, = ax.plot([], [], lw=2, color='magenta')
    lines.append(line)

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def animate(frame):
    for i, scale in enumerate(scales):
        phase = (frame + i) % len(scales)
        s = scales[phase]
        x, y = heart_shape(t, s)
        lines[i].set_data(x, y)
        lines[i].set_alpha(1 - i / len(scales))  # Fading trail
        lines[i].set_linewidth(2 + (i / 5))
    return lines

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=100, interval=50, blit=True)

plt.show()
