from opensimplex import OpenSimplex
import random
import math
gen1 = OpenSimplex(seed=random.seed(None,2))
gen2 = OpenSimplex(seed=random.seed(None,2))
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

def biome(e, m):
    if e < 0.1: return OCEAN
    if e < 0.12: return BEACH
  
    if e > 0.8: 
        if (m < 0.1): return SCORCHED
        if (m < 0.2): return BARE
        if (m < 0.5): return TUNDRA
        return SNOW
  

    if e > 0.6:
        if m < 0.33: return TEMPERATE_DESERT
        if m < 0.66: return SHRUBLAND
        return TAIGA

    if e > 0.3: 
        if m < 0.16: return TEMPERATE_DESERT
        if m < 0.50: return GRASSLAND
        if m < 0.83: return TEMPERATE_DECIDUOUS_FOREST
        return TEMPERATE_RAIN_FOREST

    if m < 0.16: return SUBTROPICAL_DESERT
    if m < 0.33: return GRASSLAND
    if m < 0.66: return TROPICAL_SEASONAL_FOREST
    return TROPICAL_RAIN_FOREST 

if __name__ == "__main__":
    