# UNIDO
__author__ = 'utpl'

import numpy as np

# Constants
RADIANS = np.pi / 180
RADIAN_90 = np.pi / 4

# Length on HoughLines
num_m = 400
magic_num_Y_offset_percent = 0.19675925925926 + 0.1

# Colors
blue = (255, 0, 0)
green = (0, 255, 0)
red = (0, 0, 255)
white = (255, 255, 255)

# Default Values:
car_default = "cascades/car.xml"
scaleFactor_default = 1.06
minNeighbors_default = 7
roiX_default = 0
roiY_default = 0
roiWidth_default = 800
roiHeight_default = 225
minLineLength_default = 100
maxLineGap_default = 10
threshold1_default = 50
threshold2_default = 150
aperture_size_default = 3
rho_default = 1
theta_default = 1.28571428571429 * RADIANS  # PI / 140
threshold_default = 80  # Old Value: 10
frameDelay_default = 0.03
car_width = 1.83
# focal_len = None
focal_len = 700
