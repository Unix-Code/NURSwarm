from utils import Vector, average_from_vectors, euclid_distance

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

    desired_vector = desired_vector.set_mag(desired_vector.MAX_SPEED)

    # Reynolds: Steering = Desired - Current
    steer = desired_vector.sub(own_vector)
    steer.limit(max_force)
    return steer

def apply_forces(acceleration, forces):
    """
    Returns acceleration after adding accelerative forces (Vectors) to itself.

    acceleration : Current Vector of acceleration
    forces : List of Vectors of new accelerative forces to apply
    """
    # performs A = Fnet / M
    # where Fnet is the sum of all accelerative forces
    # and M is 1 (thus not factored)
    return acceleration.add_many(forces)

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
    diff_vectors = [vector.invert().normalize().div(euclid_distance((0, 0), (vector.x, vector.y)) ** 2) for vector in nearby_vectors]
    # find average of opposing vectors to get desired vector
    avg_diff_vector = average_from_vectors(diff_vectors)
    return avg_diff_vector

def destination_desired_vector(dest_vector):
    """
    Returns desired vector based off of desired destination

    dest_vector : Vector representing goal
    """

    return dest_vector

def flock(swarm_vectors, nearby_vectors, destination_vector,own_vector):
    """
    Returns an accelerative steering force (Vector) using the current nearby Bot vectors and Swarm vectors.

    swarm_vectors : List of Vectors of every bot in the Swarm
    nearby_vectors : List of vectors representing euclidean distance from origin (Bot itself)
    destination_vector : Relative position Vector of End Goal seen by Bot
    own_vector : Current Vector of Bot
    """
    blank_v = Vector(0, 0, 0)

    goal_v = steer(destination_desired_vector(destination_vector), blank_v) if destination_vector is not None else blank_v
    sep_v = steer(separation_desired_vector(nearby_vectors), blank_v) if len(nearby_vectors) > 0 else blank_v
    coh_v = steer(cohesion_desired_vector(nearby_vectors), blank_v) if len(nearby_vectors) > 0 else blank_v
    ali_v = steer(alignment_desired_vector(swarm_vectors), blank_v)

    # Arbitrarily Weight Steering Vectors
    goal_v = goal_v.mult(0)
    sep_v = sep_v.mult(1)
    coh_v = coh_v.mult(1)
    ali_v = ali_v.mult(1)

    # Get Net Steering/Acceleration Vector
    accel_v = apply_forces(blank_v, [goal_v, sep_v, coh_v, ali_v])

    return accel_v
