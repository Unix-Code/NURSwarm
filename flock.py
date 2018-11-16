from utils import Vector, average_from_vectors

def steer(desired_vector, own_vector):
    """
    Returns steering vector starting from origin to desired_vectorself.

    desired_vector : Vector representing desired Vector to steer to
    own_vector : Current Vector of Bot
    """
    # Aribitrary Force for F = MA, but in this case,
    # A = F as Mass isn't at play. Essentially, the maximum
    # applied acceleration.
    max_force = 0.02

    desired = desired.set_mag(desired.MAX_SPEED)

    # Reynolds: Steering = Desired - Current
    steer = desired.sub(own_vector)
    steer.limit(max_force)

def apply_forces(acceleration, forces):
    """
    Returns acceleration after adding accelerative forces (Vectors) to itself.

    acceleration : Current Vector of acceleration
    forces : List of Vectors of new accelerative forces to apply
    """
    # performs A = Fnet / M
    # where Fnet is the sum of all accelerative forces
    # and M is 1 (thus not factored)
    return acceeration.add_many(forces)

def alignment_desired_vector(swarm_vectors):
    """
    Returns desired vector based off of Alignment.

    swarm_vectors : List of Vectors of every bot in the swarm
    """
    return average_from_vectors(swarm_vectors)

def cohesion_desired_vector(nearby_vectors):
    """
    Returns desired vector based off of Cohesion.

    nearby_vectors : List of Vectors of nearby bots reperesenting euclidean distance from origin (bot itself)
    """
    return average_from_vectors(nearby_vectors) if len(nearby_vectors) > 0 else Vector(0, 0, 0)

def separation_desired_vector(nearby_vectors):
    """
    Returns desired vector based off of Separation

    nearby_vectors : List of vectors representing euclidean distance from origin (bot itself)
    """
    # find opposing vectors from nearby robot's vectors and weight by distance
    diff_vectors = [vector.invert().normalize(
    ) / euclid_distance((0, 0), (vector.x, vector.y)) for vector in nearby_vectors]
    # find average of opposing vectors to get desired vector
    avg_diff_vector = average_from_vectors(diff_vectors)
    return avg_diff_vector

def destination_desired_vector(dest_vector):
    """
    Returns desired vector based off of desired destination

    dest_vector : Vector representing goal
    """
    # TODO: Finish
    return None

def flock(swarm_vectors, nearby_vectors, own_vector):
    """
    Returns an accelerative steering force (Vector) using the current nearby bot vectors and swarm vectors.

    swarm_vectors : List of Vectors of every bot in the swarm
    nearby_vectors : List of vectors representing euclidean distance from origin (bot itself)
    own_vector : Current Vector of Bot
    """
    sep_v = steer(separation_desired_vector(nearby_vectors))
    coh_v = steer(cohesion_desired_vector(nearby_vectors))
    ali_v = steer(alignment_desired_vector(swarm_vectors))

    # Arbitrarily Weight Steering Vectors
    sep_v = sep_v.mult(1.5)
    coh_v = coh_v.mult(1.1)
    ali_v = ali_v.mult(0.8)

    # Get Net Steering/Acceleration Vector
    accel_v = apply_forces(Vector(0, 0, 0), [sep_v, coh_v, ali_v])

    return accel_v
