from vase_generator import VaseGenerator

height = 100
radius = 40
number_points_z = 5
number_points_theta = 10
wall_thickness = 2
maximum_randomness = 15

generator = VaseGenerator(height, radius, number_points_z, number_points_theta, wall_thickness, maximum_randomness)
generator.generate_random_vase('')