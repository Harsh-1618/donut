import numpy as np
import cv2
import time

screen_height = 600
screen_width = 1200
linear_spacing = 3
pixel_scaling = 20 # one unit is equal to 20 pixels in my unit
r1_unit = 1 # radius of the circle in my own pixel scale units
r2_unit = 0
k2_unit = 5 #10
A = 0
B = 0

r1_pixel = r1_unit * pixel_scaling
r2_pixel = r2_unit * pixel_scaling
k2_pixel = k2_unit * pixel_scaling

k1_pixel = int((screen_height*k2_pixel*3)/(8*(r1_pixel+r2_pixel+120)))

screen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
x_displacement = screen.shape[1]//2
y_displacement = screen.shape[0]//2

# making square
points = np.arange(r2_pixel-r1_pixel, r2_pixel+r1_pixel, linear_spacing)

xx, yy = np.meshgrid(points, points)
x_points = xx.flatten()
y_points = yy.flatten()

# making cube
cube_x = []
cube_y = []
cube_z = []
for point in points:
    cube_x.extend(x_points)
    cube_y.extend(y_points)
    cube_z.extend([point]*len(x_points))

extended_y = []
for y_val in cube_y:
    extended_y.append(y_val+60)

cube_x.extend(cube_x)
cube_y.extend(extended_y)
cube_z.extend(cube_z)

while cv2.waitKey(1) != ord('q'):
    screen[:, :] = 0
    screen[y_displacement, :] = 255
    screen[:, x_displacement] = 255

    cube_x_proj = []
    cube_y_proj = []
    for i in range(len(cube_x)):
        # rotation along x axis:
        x_rotate1 = cube_x[i]
        y_rotate1 = cube_y[i]*np.cos(A) - cube_z[i]*np.sin(A)
        z_rotate1 = cube_y[i]*np.sin(A) + cube_z[i]*np.cos(A)

        # rotation along z axis:
        x_rotate2 = x_rotate1*np.cos(B) - y_rotate1*np.sin(B)
        y_rotate2 = x_rotate1*np.sin(B) + y_rotate1*np.cos(B)

        cube_x_proj.append(int((k1_pixel*x_rotate2)/(k2_pixel+z_rotate1)) + x_displacement)
        cube_y_proj.append(int((k1_pixel*y_rotate2)/(k2_pixel+z_rotate1)) + y_displacement)

    y_proj_plot = screen_height - 1 - np.array(cube_y_proj)
    screen[y_proj_plot, cube_x_proj, 0] = 0
    screen[y_proj_plot, cube_x_proj, 1] = 255
    screen[y_proj_plot, cube_x_proj, 2] = 255

    cv2.imshow("window", screen)

    A+=0.04
    B+=0.02
