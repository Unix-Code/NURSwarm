from utils import Vector, average_from_vectors

'''
Returns desired vector based off of separation

other_vectors : unit vectors representing euclidean distance from origin (bot itself)
'''
def separation_desired_vector(other_vectors):
    diff_vectors = [vector.normalize() / euclid_distance((0, 0), (vector.x, vector.y) for vector in other_vectors]
    avg_diff_vector = average_from_vectors(diff_vectors)
    return avg_diff_vector
