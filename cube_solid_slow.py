import numpy as np
import cv2
import time

screen_height = 600
screen_width = 1200
linear_spacing = 1 # spacing between points in pixels
sub_cube_spacing = 2 #1
pixel_scaling = 20 # one unit is equal to 20 pixels in my unit
r1_unit = 1 # half side length of cube
k2_unit = 20 # 12
A = 0
B = 0

r1_pixel = int(r1_unit * pixel_scaling)
k2_pixel = int(k2_unit * pixel_scaling)
sub_cube_spacing_pixel = int(sub_cube_spacing * pixel_scaling)

k1_pixel = int((screen_height*k2_pixel*3)/(8*(r1_pixel+180))) # 120 instead of 180

screen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
x_displacement = screen.shape[1]//2
y_displacement = screen.shape[0]//2

# Making filled square
points = np.arange(-r1_pixel, r1_pixel, linear_spacing)
xx, yy = np.meshgrid(points, points)
x_points = xx.flatten()
y_points = yy.flatten()

# Making filled cube's core
center_cube_x = np.repeat(x_points[np.newaxis, :], len(points), axis=0).flatten()
center_cube_y = np.repeat(y_points[np.newaxis, :], len(points), axis=0).flatten()
center_cube_z = np.repeat(points, len(x_points)) # repeat Repeats each element of an array after themselves

# Making full filled cube
cube_dict = {} # keys -> xyz position
sub_cubes = ["-1_-1_-1","0_-1_-1","1_-1_-1","-1_0_-1","0_0_-1","1_0_-1","-1_1_-1","0_1_-1","1_1_-1",
            "-1_-1_0","0_-1_0","1_-1_0","-1_0_0", "0_0_0", "1_0_0","-1_1_0","0_1_0","1_1_0",
            "-1_-1_1","0_-1_1","1_-1_1","-1_0_1","0_0_1","1_0_1","-1_1_1","0_1_1","1_1_1"
]

for cube in sub_cubes:
    x_shift, y_shift, z_shift = [int(c) for c in cube.split("_")]
    x_shift_pixel = x_shift*(sub_cube_spacing_pixel + 2*r1_pixel)
    y_shift_pixel = y_shift*(sub_cube_spacing_pixel + 2*r1_pixel)
    z_shift_pixel = z_shift*(sub_cube_spacing_pixel + 2*r1_pixel)

    cube_dict[cube] = (
        center_cube_x + x_shift_pixel,
        center_cube_y + y_shift_pixel,
        center_cube_z + z_shift_pixel,
    )

while cv2.waitKey(1) != ord('q'):
    screen[:, :] = 0
    screen[y_displacement, :, :] = 255
    screen[:, x_displacement, :] = 255

    cos_a = np.cos(A)
    sin_a = np.sin(A)
    cos_b = np.cos(B)
    sin_b = np.sin(B)

    for k, cube in cube_dict.items():
        x_shift, y_shift, z_shift = [int(c) for c in k.split("_")]
        cube_x = cube[0]
        cube_y = cube[1]
        cube_z = cube[2]

        # rotation along x axis
        x_rotate1 = cube_x
        y_rotate1 = cube_y*cos_a - cube_z*sin_a
        z_rotate1 = cube_y*sin_a + cube_z*cos_a

        # rotation along z axis
        x_rotate2 = x_rotate1*cos_b - y_rotate1*sin_b
        y_rotate2 = x_rotate1*sin_b + y_rotate1*cos_b

        cube_x_proj = ((k1_pixel*x_rotate2)/(k2_pixel+z_rotate1)).astype(np.int16) + x_displacement
        cube_y_proj = ((k1_pixel*y_rotate2)/(k2_pixel+z_rotate1)).astype(np.int16) + y_displacement

        y_proj_plot = screen_height - 1 - cube_y_proj
        screen[y_proj_plot, cube_x_proj, :] = [(x_shift+2) * 80, (y_shift+2) * 80, (z_shift+2) * 80]

    cv2.imshow("window", screen) # need to implement depth filtering. and illumination ofcourse

    A+=0.04
    B+=0.02

    # time.sleep(5e-2)
