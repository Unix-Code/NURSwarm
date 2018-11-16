import utils
from utils import Vector, average_from_vectors

def avg_with_mean_vector(own_vector, mean_vector):
   return  Vector(average(mean_vector.x, own_vector.x),
                   average(mean_vector.y, own_vector.y),
                   average(mean_vector.speed, own_vector.speed))

'''
Returns desired vector based off of Alignment.

swarm_vectors : list of vectors of every bot in the swarm
'''
def alignment_desired_vector(swarm_vectors):
    return average_from_vectors(swarm_vectors)
