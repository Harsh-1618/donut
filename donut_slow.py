import numpy as np
import cv2
import time

screen_height = 600
screen_width = 1200
theta_spacing = 0.07
phi_spacing = 0.02
pixel_scaling = 20 # one unit is equal to 20 pixels in my unit
r1_unit = 1 # radius of the circle in my own pixel scale units
r2_unit = 2
k2_unit = 5
A = 0
B = 0

r1_pixel = r1_unit * pixel_scaling
r2_pixel = r2_unit * pixel_scaling
k2_pixel = k2_unit * pixel_scaling

k1_pixel = int((screen_height*k2_pixel*3)/(8*(r1_pixel+r2_pixel)))

screen = np.zeros((screen_height, screen_width), dtype=np.uint8)
x_displacement = screen.shape[1]//2
y_displacement = screen.shape[0]//2

theta_angles = np.arange(0, 2*np.pi, theta_spacing)

x_points = []
y_points = []
z_points = []
for theta in theta_angles:
    x = r1_pixel*np.cos(theta) + r2_pixel
    y = r1_pixel*np.sin(theta)
    x_points.append(x)
    y_points.append(y)
    z_points.append(0)

phi_angles = np.arange(phi_spacing, 2*np.pi, phi_spacing) # avoiding angle being 0 -> z = 0

donut_x = []
donut_y = []
donut_z = []
for phi_angle in phi_angles:
    for i in range(len(x_points)):
        x_rotate = x_points[i]*np.cos(phi_angle) + z_points[i]*np.sin(phi_angle)
        y_rotate = y_points[i]
        z_rotate = (-x_points[i]*np.sin(phi_angle)) + z_points[i]*np.cos(phi_angle)

        donut_x.append(x_rotate)
        donut_y.append(y_rotate)
        donut_z.append(z_rotate)


while cv2.waitKey(1) != ord('q'):
    screen[:, :] = 0
    screen[y_displacement, :] = 255
    screen[:, x_displacement] = 255

    donut_x_proj = []
    donut_y_proj = []

    for i in range(len(donut_x)):
        # rotation along x axis:
        x_rotate1 = donut_x[i]
        y_rotate1 = donut_y[i]*np.cos(A) - donut_z[i]*np.sin(A)
        z_rotate1 = donut_y[i]*np.sin(A) + donut_z[i]*np.cos(A)

        # rotation along z axis:
        x_rotate2 = x_rotate1*np.cos(B) - y_rotate1*np.sin(B)
        y_rotate2 = x_rotate1*np.sin(B) + y_rotate1*np.cos(B)

        donut_x_proj.append(int((k1_pixel*x_rotate2)/(k2_pixel+z_rotate1)) + x_displacement)
        donut_y_proj.append(int((k1_pixel*y_rotate2)/(k2_pixel+z_rotate1)) + y_displacement)

    y_proj_plot = screen_height - 1 - np.array(donut_y_proj)
    screen[y_proj_plot, donut_x_proj] = 255

    cv2.imshow("window", screen)

    A+=0.04
    B+=0.02