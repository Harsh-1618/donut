import numpy as np
import cv2
import time

screen_height = 600
screen_width = 1200
theta_spacing = 0.07
phi_spacing = 0.02
pixel_scaling = 20 # one unit is equal to 20 pixels in my unit
r1_unit = 1 # radius of the circle in my own pixel scale units
r2_unit = 2 # if r2 is 0, it'll make a sphere instead of donut!
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

# Making circle
theta_angles = np.arange(0, 2*np.pi, theta_spacing)
x_points = (r1_pixel*np.cos(theta_angles) + r2_pixel)[np.newaxis, :]
y_points = (r1_pixel*np.sin(theta_angles))[np.newaxis, :]
z_points = np.zeros((len(theta_angles),))[np.newaxis, :]

# Making donut from circle rotation along y-axis
phi_angles = np.arange(phi_spacing, 2*np.pi, phi_spacing) # avoiding angle being 0 -> z = 0
cos_phi_angles = np.cos(phi_angles)[:, np.newaxis]
sin_phi_angles = np.sin(phi_angles)[:, np.newaxis]
donut_x = ((cos_phi_angles @ x_points) + (sin_phi_angles @ z_points)).flatten()
donut_y = (np.repeat(y_points, len(phi_angles), axis=0)).flatten()
donut_z = ((-sin_phi_angles @ x_points) + (cos_phi_angles @ z_points)).flatten()

# Making the donut rotate along x and z axis
while cv2.waitKey(1) != ord('q'):
    screen[:, :] = 0
    screen[y_displacement, :] = 255
    screen[:, x_displacement] = 255

    cos_a = np.cos(A)
    sin_a = np.sin(A)
    cos_b = np.cos(B)
    sin_b = np.sin(B)

    x_rotate1 = donut_x
    y_rotate1 = donut_y*cos_a - donut_z*sin_a
    z_rotate1 = donut_y*sin_a + donut_z*cos_a

    x_rotate2 = x_rotate1*cos_b - y_rotate1*sin_b
    y_rotate2 = x_rotate1*sin_b + y_rotate1*cos_b

    donut_x_proj = ((k1_pixel*x_rotate2)/(k2_pixel+z_rotate1)).astype(np.int16) + x_displacement
    donut_y_proj = ((k1_pixel*y_rotate2)/(k2_pixel+z_rotate1)).astype(np.int16) + y_displacement

    y_proj_plot = screen_height - 1 - donut_y_proj
    screen[y_proj_plot, donut_x_proj] = 255

    cv2.imshow("window", screen)

    A+=0.04
    B+=0.02

    time.sleep(5e-2)
