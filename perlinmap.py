import noise
import math
import numpy as np
from PIL import Image

lightblue = [0,191,255]
blue = [65,105,225]
green = [34,139,34]
darkgreen = [0,100,0]
sandy = [210,180,140]
beach = [238, 214, 175]
snow = [255, 250, 250]
mountain = [139, 137, 137]
black = [0, 0, 0]

def rgb_norm(world):
    world_min = np.min(world)
    world_max = np.max(world)
    norm = lambda x: (x-world_min/(world_max - world_min))*255
    return np.vectorize(norm)

def prep_world(world):
    norm = rgb_norm(world)
    world = norm(world)
    return world

def make_world(shape = (1024,1024), scale = 100, octaves = 6, persistence = 0.5, lacunarity = 2.0, seed = 1):
    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.pnoise2(i/scale, 
                                        j/scale, 
                                        octaves=octaves, 
                                        persistence=persistence, 
                                        lacunarity=lacunarity, 
                                        repeatx=1024, 
                                        repeaty=1024, 
                                        base=seed)
    return world

def add_color(world, shape = (1024, 1024)):
    threshold = 50
    color_world = np.zeros(world.shape+(3,))

    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < threshold + 100:
                color_world[i][j] = blue
            elif world[i][j] < threshold + 102:
                color_world[i][j] = beach
            elif world[i][j] < threshold + 104:
                color_world[i][j] = sandy
            elif world[i][j] < threshold + 115:
                color_world[i][j] = green
            elif world[i][j] < threshold + 130:
                color_world[i][j] = darkgreen
            elif world[i][j] < threshold + 137:
                color_world[i][j] = mountain
            else:
                color_world[i][j] = snow

    return color_world

def make_mask(shape = (1024, 1024)):
    a,b = shape[0]/2, shape[1]/2
    n = 1024
    r = 125
    y,x = np.ogrid[-a:n-a, -b:n-b]
    # creates a mask with True False values
    # at indices
    mask = x**2+y**2 <= r**2

    return mask

def make_island(color_world, shape = (1024, 1024)):
    mask = make_mask()

    for i in range(shape[0]):
        for j in range(shape[1]):
            if mask[i][j]:
                island_world[i][j] = color_world[i][j]
            else:
                island_world[i][j] = black
    return island_world

def make_circular_gradient(world, shape = (1024, 1024)):
    center_x, center_y = shape[1] // 2, shape[0] // 2
    circle_grad = np.zeros_like(world)

    for y in range(world.shape[0]):
        for x in range(world.shape[1]):
            distx = abs(x - center_x)
            disty = abs(y - center_y)
            dist = math.sqrt(distx*distx + disty*disty)
            circle_grad[y][x] = dist

    # get it between -1 and 1
    max_grad = np.max(circle_grad)
    circle_grad = circle_grad / max_grad
    circle_grad -= 0.5
    circle_grad *= 2.0
    circle_grad = -circle_grad

    return circle_grad

def add_noise(world, circle_grad, shape = (1024, 1024)):
    world_noise = np.zeros_like(world)

    for i in range(shape[0]):
        for j in range(shape[1]):
            if circle_grad[i][j]>0:
                world_noise[i][j] = (world[i][j] * circle_grad[i][j])

    return world_noise


if __name__ == '__main__':
    seed = np.random.randint(0,100)
    print(seed)
    world = make_world(seed = seed)
    color_world = add_color(world).astype(np.uint8)
    island_world = np.zeros_like(color_world)
    # Image.fromarray(prep_world(world)).show()
    # Image.fromarray(color_world,'RGB').show()
    # Image.fromarray(prep_world(make_circular_gradient(world))).show()
    # Image.fromarray(prep_world(add_noise(world, make_circular_gradient(world)))).show()

    island_world_grad = add_color(prep_world(add_noise(world, make_circular_gradient(world)))).astype(np.uint8)
    Image.fromarray(island_world_grad,'RGB').save("map.jpg")

