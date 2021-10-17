from opensimplex import OpenSimplex
import random
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

gen1 = OpenSimplex(seed = 2) 
gen2 = OpenSimplex(seed = 2)
def noise1(nx, ny):
    return gen1.noise2d(nx, ny) / 2.0 + 0.5
def noise2(nx, ny):
    return gen2.noise2d(nx, ny) / 2.0 + 0.5

def coordinates(width, height):
    for y in range(height):
       for x in range(width):
           nx = x/width - 0.5
           ny = y/height - 0.5
           e = (1.00 * noise1( 1 * nx,  1 * ny)
              + 0.50 * noise1( 2 * nx,  2 * ny)
              + 0.25 * noise1( 4 * nx,  4 * ny)
              + 0.13 * noise1( 8 * nx,  8 * ny)
              + 0.06 * noise1(16 * nx, 16 * ny)
              + 0.03 * noise1(32 * nx, 32 * ny))
           e = e / (1.00 + 0.50 + 0.25 + 0.13 + 0.06 + 0.03)
           e = math.pow(e, 5.00)
           m = (1.00 * noise2( 1 * nx,  1 * ny)
              + 0.75 * noise2( 2 * nx,  2 * ny)
              + 0.33 * noise2( 4 * nx,  4 * ny)
              + 0.33 * noise2( 8 * nx,  8 * ny)
              + 0.33 * noise2(16 * nx, 16 * ny)
              + 0.50 * noise2(32 * nx, 32 * ny))
           m = m / (1.00 + 0.75 + 0.33 + 0.33 + 0.33 + 0.50)
    return e, m

def plot(x, y):
    z = np.array([[x**2 + y**2 for x in range(20)] for y in range(20)])
    x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))

    # show hight map in 2d
    plt.figure()
    plt.title('z as 2d heat map')
    p = plt.imshow(z)
    plt.colorbar(p)
    plt.show()

if __name__ == '__main__':
    x, y = coordinates(100,100)
    plot(x,y)