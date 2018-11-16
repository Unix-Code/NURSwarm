from math import cos, sin, sqrt
from functools import reduce

class Vector:
   def __init__(self, x, y, speed):
       self.x = x
       self.y = y
       self.speed = speed
       self.MAX_SPEED = 5 # Arbitrary max speed for steering

   def normalize():
       return Vector(self.x / self.speed, self.y / self.speed1, 1)

   def add(other_vector):
       new_x = self.x + other_vector.x
       new_y = self.y + other_vector.y
       new_speed = sqrt(new_x ** 2 + new_y ** 2)
       return Vector(new_x, new_y, new_speed)

   def add_many(other_vectors):
       return self.add(reduce(lambda a,b : a.add(b) , other_vectors))

   def sub(other_vector):
       new_x = self.x - other_vector.x
       new_y = self.y - other_vector.y
       new_speed = euclid_distance((0, 0), (new_x, new_y))
       return Vector(new_x, new_y, new_speed)

   def mult(scalar):
       return Vector(self.x * scalar, self.y * scalar, self.speed * scalar)

   def invert():
       return Vector(self.x * -1, self.y * -1, self.speed)

   def set_mag(new_mag):
       return self.normalize().mult(new_mag)

   def limit(max):
       length_squared = self.x ** 2 + self.y ** 2;
       ratio = 1
       if length_squared > max ** 2 and length_squared > 0:
           ratio = max / sqrt(length_squared)

       new_x = self.x * ratio;
       new_y = self.y * ratio;
       new_speed = euclid_distance((0, 0), (new_x, new_y))
       return Vector(new_x, new_y, new_speed)

def average_from_vectors(vectors):
    x_coords = [vector.x for vector in vectors]
    y_coords = [vector.y for vector in vectors]
    speeds = [vector.speed for vector in vectors]
    avg_x = average(x_coords)
    avg_y = average(y_coords)
    avg_speed = average(speeds)
    avg_vector = Vector(avg_x, avg_y, avg_speed)
    return avg_vector

'''
p0 : (x, y)
p1 : (x, y)
'''
def euclid_distance(p0, p1):
    return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

# theta in Radians
def convert_polar_to_cartesian(r, theta):
   return (r * cos(theta)), (r * sin(theta))

def average(nums):
  return reduce(lambda a, b: a + b, nums) / len(nums)
