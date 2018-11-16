from utils import Vector, average_from_vectors
import alignment as ali
import cohesion as coh
import separation as sep

'''
Returns steering vector starting from origin to desired_vectorself.

desired_vector : Vector representing desired Vector to steer to
'''
def steer(desired_vector):
    # Aribitrary Force for F = MA, but in this case,
    # A = F as Mass isn't at play. Essentially, the maximum
    # applied acceleration.
    max_force = 0.02

    desired = desired.set_mag(desired.MAX_SPEED)

    # Reynolds: Steering = Desired - Current
    steer = desired.sub(velocity)
    steer.limit(max_force)

'''
Returns acceleration after adding accelerative forces (Vectors) to itself.

acceleration : Current Vector of acceleration
forces : List of Vectors of new accelerative forces to apply
'''
def apply_forces(acceleration, forces):
    return acceeration.add_many(forces)

'''
Returns desired vector based off of Alignment.

swarm_vectors : List of Vectors of every bot in the swarm
'''
def alignment_desired_vector(swarm_vectors):
    return average_from_vectors(swarm_vectors)

'''
Returns desired vector based off of Cohesion.

nearby_vectors : List of Vectors of nearby bots reperesenting euclidean distance from origin (bot itself)
'''
def cohesion_desired_vector(nearby_vectors):
    return average_from_vectors(nearby_vectors) if len(nearby_vectors) > 0 else Vector(0, 0, 0)

'''
Returns desired vector based off of Separation

nearby_vectors : List of vectors representing euclidean distance from origin (bot itself)
'''
def separation_desired_vector(nearby_vectors):
    # find opposing vectors from nearby robot's vectors and weight by distance
    diff_vectors = [vector.invert().normalize() / euclid_distance((0, 0), (vector.x, vector.y) for vector in nearby_vectors]
    # find average of opposing vectors to get desired vector
    avg_diff_vector = average_from_vectors(diff_vectors)
    return avg_diff_vector

'''
Returns an accelerative steering force (Vector) using the current nearby bot vectors and swarm vectors.

swarm_vectors : List of Vectors of every bot in the swarm
nearby_vectors : List of vectors representing euclidean distance from origin (bot itself)
'''
def flock(swarm_vectors, nearby_vectors):
    sep_v = steer(sep.separation_desired_vector(nearby_vectors))
    coh_v = steer(coh.cohesion_desired_vector(nearby_vectors))
    ali_v = steer(ali.alignment_desired_vector(swarm_vectors))

    # Arbitrarily Weight Steering Vectors
    sep_v = sep_v.mult(1.5)
    coh_v = coh_v.mult(1.1)
    ali_v = ali_v.mult(0.8)

    # Get Net Steering/Acceleration Vector
    accel_v = apply_forces(Vector(0, 0, 0), [sep_v, coh_v, ali_v])

    return accel_v
