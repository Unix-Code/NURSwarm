class Vector:
   def __init__(self, x, y, speed):
       self.x = x
       self.y = y
       self.speed = speed
       
def convert_polar_to_cartesian(r, theta):
   return (r * cos(theta)), (r * sin(theta))

def average(nums):
  return reduce(lambda a, b: a + b, nums) / len(nums)
