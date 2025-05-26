import numpy as np
import cv2
import time

screen_height = 600
screen_width = 1200
linear_spacing = 0.5 # spacing between points in pixels
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

# Making hollow square
points = np.arange(-r1_pixel, r1_pixel, linear_spacing)
x_points = np.concatenate(
    (
        np.ones((len(points),)) * points[0],
        np.ones((len(points),)) * points[-1],
        points[1:-1], # removing overlapping points
        points[1:-1]
    ), axis=0
)
y_points = np.concatenate(
    (
        points,
        points,
        np.ones((len(points)-2,)) * points[0], # removing overlapping points
        np.ones((len(points)-2,)) * points[-1]
    ), axis=0
)

# Making hollow cube's core
center_cube_x = np.repeat(x_points[np.newaxis, :], len(points)-2, axis=0).flatten() # excluding front and back
center_cube_y = np.repeat(y_points[np.newaxis, :], len(points)-2, axis=0).flatten()
center_cube_z = np.repeat(points[1:-1], len(x_points)) # repeat Repeats each element of an array after themselves

xx, yy = np.meshgrid(points, points) # for rest of the 2 faces
x_points_face = xx.flatten()
y_points_face = yy.flatten()

center_cube_x = np.concatenate((x_points_face, center_cube_x, x_points_face), axis=0)
center_cube_y = np.concatenate((y_points_face, center_cube_y, y_points_face), axis=0)
center_cube_z = np.concatenate((np.ones((len(x_points_face),))*points[0], center_cube_z, np.ones((len(x_points_face),))*points[-1]), axis=0)

# Making full hollow cube
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
    screen[:, :, :] = 0
    screen[y_displacement, :, :] = 255
    screen[:, x_displacement, :] = 255

    cos_a = np.cos(A)
    sin_a = np.sin(A)
    cos_b = np.cos(B)
    sin_b = np.sin(B)

    show_points = {}
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

        xy_array = np.array(list(zip(cube_x_proj, y_proj_plot)))
        unique_xy_array = np.array(list(set(zip(cube_x_proj, y_proj_plot))))
        mask = xy_array == unique_xy_array[:, np.newaxis, :] # to compute equivalance for all unique_xy_array elements in a go
        mask = np.all(mask, axis=2)
        pos_x, pos_y = np.where(mask)
        unique_z_array = z_rotate1[pos_y]
        mask_x = pos_x == np.arange(len(unique_xy_array))[:, np.newaxis] # again, to compute equivalance in a go
        # since mask_x has zeros also, when computing min, 0 will be the output for every row, so changing this 0 with a big number so it does not interfere
        mask_x = ~mask_x
        mask_x = mask_x * 1e5
        mask_x = mask_x + unique_z_array
        unique_z_array = np.min(mask_x, axis=1) # z values corresponding to elements in unique_xy_array

        for i in range(len(unique_xy_array)):
            val = show_points.get((unique_xy_array[i][0], unique_xy_array[i][1]))
            if val is not None:
                if unique_z_array[i] < val[0]: # saving only the ones which are infront, i.e. whose z value is minimum
                    show_points[(unique_xy_array[i][0], unique_xy_array[i][1])] = (unique_z_array[i], ((x_shift+2) * 80, (y_shift+2) * 80, (z_shift+2) * 80))
            else:
                show_points[(unique_xy_array[i][0], unique_xy_array[i][1])] = (z_rotate1[i], ((x_shift+2) * 80, (y_shift+2) * 80, (z_shift+2) * 80))

    x, y = zip(*show_points.keys())
    _, rgb = zip(*show_points.values())
    r, g, b = zip(*rgb)

    screen[y, x, 0] = np.array(r)
    screen[y, x, 1] = np.array(g)
    screen[y, x, 2] = np.array(b)
    cv2.imshow("window", screen) # need to implement depth filtering (DONE!, very inefficiently though). and illumination ofcourse

    A+=0.04
    B+=0.02

    # time.sleep(5e-2)
