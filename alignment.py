from functools import reduce
import utils
from utils import Vector

def mean_swarm_vector(vectors):
    x_coords = [vector.x for vector in vectors]
    y_coords = [vector.y for vector in vectors]
    speeds = [vector.speed for vector in vectors]
    avg_x = average(x_coords)
    avg_y = average(y_coords)
    avg_speed = average(speeds)
    avg_vector = Vector(avg_x, avg_y, avg_speed)
    return avg_vector

def avg_with_mean_vector(own_vector, mean_vector):
   return  Vector(average(mean_vector.x, own_vector.x),
                   average(mean_vector.y, own_vector.y),
                   average(mean_vector.speed, own_vector.speed))

def aligned_vector(own_vector, swarm_vectors):
    return avg_with_mean_vector(own_vector, mean_swarm_vector(swarm_vectors))
