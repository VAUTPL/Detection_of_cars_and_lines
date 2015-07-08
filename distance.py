#!/bin/hbpython
__author__ = 'utpl'

from config import *


def cfg_cam():
    print "Calibrating Camera (specify focal length here or on the command line to skip)..."
    ccam_type = "x"
    while ccam_type != "F" and ccam_type != "f" and ccam_type != "A" and ccam_type != "a" and ccam_type != "Q"\
            and ccam_type != "q":
        ccam_type = raw_input("Values to Enter ([F]ocal Length | [A]uto Detect based on Object | [Q]uit): ")
    focal_len = -1
    if ccam_type == "F" or ccam_type == "f":
        focal_len = float(raw_input("Focal Length: "))
    elif ccam_type == "A" or ccam_type == "a":
        test_object_distance_from_cam = float(raw_input("Distance from Camera (test object): "))
        width_test_object = float(raw_input("Width of Test Object: "))
        # pixel_width_test_object = frame.width
        pixel_width_test_object = 20
        focal_len = func_focal_len(pixel_width_test_object, test_object_distance_from_cam, width_test_object)
    else:
        print "User requested quit, exiting..."
        exit()
    print "Camera Configured!"
    return focal_len


def get_object_data():
    # data = []
    # data.append(float(raw_input("Object Width: ")))
    # data.append(float(raw_input("Object Pixel Width: ")))
    data = [float(raw_input("Object Width: ")), float(raw_input("Object Pixel Width: "))]
    return data


def func_focal_len(pixel_width, distance, width):
    return pixel_width * distance / width


def func_calc_distance(width, focal_len, pixel_width):
    return width * focal_len / pixel_width

if __name__ == "__main__":
    focal_len = focal_len if focal_len is not None else cfg_cam()
    # print "Focal Length %f" % focal_len
    object_data = get_object_data()
    print "Distance is %f" % (func_calc_distance(object_data[0], focal_len, object_data[1]))
