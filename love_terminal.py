# Requires PyGame and Noise
import pygame
import noise

def generate_terrain(width, height):
    terrain = []
    for x in range(width):
        row = []
        for y in range(height):
            # Generate Perlin noise value
            elevation = noise.pnoise2(x/100, 
                                      y/100, 
                                      octaves=6)
            row.append(elevation)
        terrain.append(row)
    return terrain

# Visualization example
def draw_terrain(surface, terrain):
    for x, row in enumerate(terrain):
        for y, elevation in enumerate(row):
            color = (0, max(0, int(elevation * 255)), 0)
            surface.set_at((x, y), color)