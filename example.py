from vase_generator import Vase

height = 100
radius = 40
number_points_z = 5
number_points_theta = 10
wall_thickness = 2
maximum_randomness = 15

vase = Vase(height, radius, number_points_z, number_points_theta, wall_thickness, maximum_randomness)
vase.generate_random_vase(r'')