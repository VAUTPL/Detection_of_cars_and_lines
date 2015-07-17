#!/bin/hbpython
# UNIDO
# coding=utf-8
__author__ = 'utpl'

#Libreria de direccion de argumentos
import argparse
# Libreria de vision artificial
import cv2

# liberia para manipulacion de imagenes
from pyimagesearch import imutils
# librerias para control de frames
import time
# Importacion de valores por defecto
from config import *
# Importacion libreria de distancias
import distance as dist
# Import My Mask Library
# import mask as msk
# Import My Video Output Library
# import video as vid
# Import My library for sanitizing data
import sanitize as san
# Import my Filter Functions Library:
import filters

# Manage Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--car", help="Path to Car Haar Cascade -- default is %s" % car_default)
ap.add_argument("-v", "--video", help="Path to the (optional) video file -- default is Live Webcam Capture")
ap.add_argument("-S", "--scale-factor", help="Haar Cascade Scale Factor -- default is %f" % scaleFactor_default)
ap.add_argument("-N", "--min-neighbors", help="Haar Cascade Minimum Neighbors -- default is %d" % minNeighbors_default)
ap.add_argument("-X", "--roi-x", help="Region Of Interest top left corner X coordinate -- default is %d" % roiX_default)
ap.add_argument("-Y", "--roi-y", help="Region Of Interest top left corner Y coordinate -- default is %d" % roiY_default)
ap.add_argument("-W", "--roi-width", help="Region Of Interest Width -- default is %d" % roiWidth_default)
ap.add_argument("-H", "--roi-height", help="Region Of Interest Height -- default is %d" % roiHeight_default)
ap.add_argument("-x", "--max-line-gap", help="Max Line Gap -- default is %d" % maxLineGap_default)
ap.add_argument("-n", "--min-line-length", help="Min Line Length -- default is %d" % minLineLength_default)
ap.add_argument("-1", "--threshold-1", help="Canny 1st Threshold -- default is %d" % threshold1_default)
ap.add_argument("-2", "--threshold-2", help="Canny 2nd Threshold -- default is %d" % threshold2_default)
ap.add_argument("-a", "--aperture-size", help="Canny Aperture Size -- default is %d" % aperture_size_default)
ap.add_argument("-r", "--rho", help="Hough Rho -- default is %d" % rho_default)
ap.add_argument("-t", "--theta", help="Hough Theta in Radians -- default is %f" % theta_default)
ap.add_argument("-T", "--threshold", help="Hough Threshold -- default is %d" % threshold_default)
ap.add_argument("-D", "--delay", help="Delay for operating system to sleep between frames -- default is %f"
                                      % frameDelay_default)
args = vars(ap.parse_args())

# Set defaults for Arguments not provided
car = args['car'] if args['car'] is not None else car_default
scaleFactor = args['scale_factor'] if args['scale_factor'] is not None else scaleFactor_default
minNeighbors = args['min_neighbors'] if args['min_neighbors'] is not None else minNeighbors_default
roiX = args['roi_x'] if args['roi_x'] is not None else roiX_default
roiY = args['roi_y'] if args['roi_y'] is not None else roiY_default
roiWidth = args['roi_width'] if args['roi_width'] is not None else roiWidth_default
roiHeight = args['roi_height'] if args['roi_height'] is not None else roiHeight_default
maxLineGap = args['max_line_gap'] if args['max_line_gap'] is not None else maxLineGap_default
minLineLength = args['min_line_length'] if args['min_line_length'] is not None else minLineLength_default
threshold1 = args['threshold_1'] if args['threshold_1'] is not None else threshold1_default
threshold2 = args['threshold_2'] if args['threshold_2'] is not None else threshold2_default
aperture_size = args['aperture_size'] if args['aperture_size'] is not None else aperture_size_default
rho = args['rho'] if args['rho'] is not None else rho_default
theta = args['theta'] * RADIANS if args['theta'] is not None else theta_default
threshold = args['threshold'] if args['threshold'] is not None else threshold_default
frameDelay = float(args['delay']) if args['delay'] is not None else frameDelay_default

# Initialize Cascade
car_cascade = cv2.CascadeClassifier(car)

# Initialize Video Stream
if not args.get("video", False):
    camera = cv2.VideoCapture(1)
else:
    camera = cv2.VideoCapture(args["video"])

(grabbed, frame) = camera.read()
if args.get("video") and not grabbed:
    exit(0)

focal_len = focal_len if focal_len is not None else dist.cfg_cam()

print "------------------------------------------------BEGIN------------------------------------------------"

frame = imutils.resize(frame, width=800)

roiY_old = roiY
roiX_old = roiX
roiHeight_old = roiHeight
roiWidth_old = roiWidth

roiX = 0
roiY = frame.shape[0] / 2
roiWidth = frame.shape[1]
roiHeight = frame.shape[0]
print frame.shape

# Frame Selector
frame_num = 0

min_def = 100000000
max_def = -100000000
min = min_def
max = max_def
avg = 0.0
cnt = 0
carcnt = 0

avgline = [[[0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0]],
           [[0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0]],
           [[0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0]],
           [[0.0, 0.0], [0.0, 0.0]]]
avgline_count = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

fstat = open("a_stat.tsv", 'w')
fcstat = open("c_stat.tsv", 'w')

# Main Program Loop
while True:

    # Read Frame
    (grabbed, frame) = camera.read()
    if args.get("video") and not grabbed:
        break

    print "-------------------------BEGIN FRAME %i-------------------------" % frame_num

    # Read only every 5th Frame -- Has no effect on optimization
    '''
    if frame_num % 5 != 0:
        frame_num += 1
        continue
    frame += 1
    # '''

    # Resize Frame
    frame = imutils.resize(frame, width=800)

    # Convert Frame to Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Filter
    #                                 (src, d, sigmaColor, sigmaSpace[, dst[, borderType]])
    grayFiltered = cv2.bilateralFilter(gray, 5, 50, 50)
    # Gausian Filter
    grayFiltered = cv2.GaussianBlur(grayFiltered, (5, 5), 3)

    # Apply Histogram
    grayFiltered = cv2.equalizeHist(grayFiltered)

    # Select Area of Interest
    grayROI = grayFiltered[roiY:roiY+roiHeight, roiX:roiX+roiWidth]  # Prior ROI
    GrayROI = grayFiltered[roiY:roiY+roiHeight, roiX:roiX+roiWidth]

    # Look for Cars in Area of Interest
    #                                      (image[, scaleFactor[, minNeighbors[, flags[, minSize[, maxSize]]]]])
    carRects = car_cascade.detectMultiScale(grayROI, scaleFactor, minNeighbors, flags=cv2.cv.CV_HAAR_SCALE_IMAGE)

    # Initialize Canny
    #                 image, edges, threshold1, threshold2, aperture_size=3
    edges = cv2.Canny(grayROI, threshold1, threshold2, apertureSize=aperture_size)
    cv2.imshow("Car Detection - Edges", edges)

    # Detect Lines
    #                      (image, rho, theta, threshold[, lines[, minLineLength[, maxLineGap]]])
    lines2 = cv2.HoughLinesP(edges, rho, theta, threshold, minLineLength, maxLineGap)
    lines = cv2.HoughLines(edges, rho, theta, threshold)

    # Make a copy of the current frame
    frameClone = frame.copy()

    # Draw each car rectangle on frame copy
    cri = 1
    for (fX, fY, fW, fH) in carRects:
        d = dist.func_calc_distance(car_width, focal_len, fW)
        ratio = 1
        if 0.09 <= ratio <= 0.45:
            if avgline_count[9][0] != 0:
                avgl = avgline[9][0][0] / avgline_count[9][0]
                a = np.cos(t)
                b = np.sin(t)
                ang = np.tan(t + RADIAN_90) / RADIANS
                x0 = a*r
                y0 = b*r
                pt1 = (int(x0 + 1000*(-b) + roiX), int(y0 + 1000*a + roiY))
                pt2 = (int(x0 - 1000*(-b) + roiX), int(y0 - 1000*a + roiY))
                if filters.isBelow((fX, fY, fW, fH), pt1, pt2):
                    cv2.rectangle(frameClone, (fX + roiX, fY + roiY), (fX + fW + roiX, fY + fH + roiY), green, 2)
                    cv2.putText(frameClone, "%.1f M" % (d),(fX + fW + roiX + 5, fY + fH/2 + roiY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)
                    cv2.putText(frameClone, "fY = %d" % (fY),(fX + fW + roiX + 5, (fY + fH/2 + roiY - 5) + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)
                    cv2.rectangle(frameClone, (fX + fW/2 + roiX - 5, fY + fH/2 + roiY - 5), (fX + fW/2 + roiX + 5, fY + fH/2 + roiY + 5), (255,255,0), -2)
                    print "Distance to object %i is %f" % (cri, d)
                    #fcstat.write("%f\t%d\t%f\t%f\n" % (d, fY, fY/d, d/fY))
                    fcstat.flush()
                    carcnt += 1
            else:
                if True: # filters.isBelow((fX, fY, fW, fH), pt1, pt2):
                    cv2.rectangle(frameClone, (fX + roiX, fY + roiY), (fX + fW + roiX, fY + fH + roiY), green, 2)
                    cv2.putText(frameClone, "%.1f M" % (d),(fX + fW + roiX + 5, fY + fH/2 + roiY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)
                    cv2.putText(frameClone, "fY = %d" % (fY),(fX + fW + roiX + 5, (fY + fH/2 + roiY - 5) + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)
                    cv2.rectangle(frameClone, (fX + fW/2 + roiX - 5, fY + fH/2 + roiY - 5), (fX + fW/2 + roiX + 5, fY + fH/2 + roiY + 5), (255,255,0), -2)
                    print "Distance to object %i is %f" % (cri, d)
                    #fcstat.write("%f\t%d\t%f\t%f\n" % (d, fY, fY/d, d/fY))
                    fcstat.flush()
                    carcnt += 1
        #fstat.write("%f\t%d\t%f\t%f\n" % (d, fY, fY/d, d/fY))
        fstat.flush()
        cri += 1

    # Draw each line on frame copy
    if lines is not None:
        for i in range(9, 0, -1):
            avgline[i] = avgline[i-1]
            avgline_count[i] = avgline_count[i-1]
        avgline[0] = [[0.0, 0.0], [0.0, 0.0]]
        avgline_count[0] = [0, 0]
        for line in lines:
            # Display HoughLines
            # New Form with angles
            for r, t in line:
                a = np.cos(t)
                b = np.sin(t)
                ang = np.tan(t + RADIAN_90) / RADIANS
                x0 = a*r
                y0 = b*r
                pt1 = (int(x0 + 1000*(-b) + roiX), int(y0 + 1000*a + roiY))
                pt2 = (int(x0 - 1000*(-b) + roiX), int(y0 - 1000*a + roiY))
                delx = pt1[0] - pt2[0]
                if True:
                    if delx != 0:
                        m = (float(pt1[1] - pt2[1]) / float(delx))
                        if m < -0.5 or m > 0.5:
                            print "HLO (x1, y1) = (%i, %i) (x2, y2) = (%i, %i) m = %f angle = %f"\
                                  % (pt1[0], pt2[0], pt1[1], pt2[1], m, ang)
                            if m < 0:
                                for i in range(10):
                                    avgline[i][1][0] += r
                                    avgline[i][1][1] += t
                                    avgline_count[i][1] += 1
                            elif m > 0:
                                for i in range(10):
                                    avgline[i][0][0] += r
                                    avgline[i][0][1] += t
                                    avgline_count[i][0] += 1
                            old_ang = ang
                            ang %= 360
                            if old_ang < 0:
                                ang *= -1
                            min = ang if ang < min else min
                            max = ang if ang > max else max
                            avg += ang
                            cnt += 1
        if avgline_count[9][0] != 0:
            avgline[9][0][0] /= avgline_count[9][0]
            avgline[9][0][1] /= avgline_count[9][0]
        if avgline_count[9][1] != 0:
            avgline[9][1][0] /= avgline_count[9][1]
            avgline[9][1][1] /= avgline_count[9][1]
        tmp_lines = []
        # Draw Lines up to intersection or roi, which ever has less y
        for avgl in avgline[9]:
            # Display HoughLines
            # New Form with angles
            r = avgl[0]
            t = avgl[1]
            a = np.cos(t)
            b = np.sin(t)
            ang = np.tan(t + RADIAN_90) / RADIANS
            x0 = a*r
            y0 = b*r
            pt1 = (int(x0 + 1000*(-b) + roiX), int(y0 + 1000*a + roiY))
            pt2 = (int(x0 - 1000*(-b) + roiX), int(y0 - 1000*a + roiY))
            delx = pt1[0] - pt2[0]
            if delx != 0:
                m = (float(pt1[1] - pt2[1]) / float(delx))
                print "HLO AVG (x1, y1) = (%i, %i) (x2, y2) = (%i, %i) m = %f angle = %f"\
                      % (pt1[0], pt1[1], pt2[0], pt2[1], m, ang)
                tmp_lines.append([pt1, pt2, m, ang])
            else:
                m = 10000
        max_y = roiY
        pti = None
        # Cut Lines to Point of intersection
        if len(tmp_lines) == 2:
            # data format:
            # tmp_lines[0] = line1
            # tmp_lines[0][0] = line1_pt1
            # tmp_lines[0][0][0] = line1_pt1_x
            # tmp_lines[0][0][1] = line1_pt1_y
            # tmp_lines[0][1] = line1_pt2
            # tmp_lines[0][1][0] = line1_pt2_x
            # tmp_lines[0][1][1] = line1_pt2_y
            # tmp_lines[0][2] = line1_m
            # tmp_lines[0][3] = line1_ang
            # tmp_lines[1] = line2
            # tmp_lines[1][0] = line2_pt1
            # tmp_lines[1][0][0] = line2_pt1_x
            # tmp_lines[1][0][1] = line2_pt1_y
            # tmp_lines[1][1] = line2_pt2
            # tmp_lines[1][1][0] = line2_pt2_x
            # tmp_lines[1][1][1] = line2_pt2_y
            # tmp_lines[1][2] = line2_m
            # tmp_lines[1][3] = line2_ang
            # ----- CALCULATIONS ----- #
            # general form: y = mx + b
            # b = -1 * (mx - y)
            b1 = -1 * ((tmp_lines[0][2] * tmp_lines[0][0][0]) - tmp_lines[0][0][1])
            b2 = -1 * ((tmp_lines[1][2] * tmp_lines[1][0][0]) - tmp_lines[1][0][1])
            pti = (
                ((b2 - b1) / (tmp_lines[0][2] - tmp_lines[1][2])),
                (((tmp_lines[0][2] * b2) - (tmp_lines[1][2] * b1)) / (tmp_lines[0][2] - tmp_lines[1][2]))
            )
            if pti[1] > max_y:
                max_y = pti[1]
        crop_lines = []
        # if pti is not None and min_y == pti[1]:
        if pti is not None and max_y == pti[1]:
            print "Cropping Lines to Point of Intersection..."
            for tmpl in tmp_lines:
                if tmpl[0][1] < pti[1]:
                    pt1 = tmpl[1]
                    pt2 = pti
                elif tmpl[1][1] < pti[1]:
                    pt1 = tmpl[0]
                    pt2 = pti
                else:
                    # Should never ever ever enter this condition
                    print "GRAVE ERROR, NON-EXISTENT POINT, POS 367"
                    break
                crop_lines.append([pt1, pt2])
            # print "PTI Cropped Lines: %s" % (str(crop_lines))
        else:
            print "Cropping Lines to ROI..."
            for tmpl in tmp_lines:
                # x = ((y - y1) / m) + x1
                x1 = tmpl[0][0]
                y1 = tmpl[0][1]
                m = tmpl[2]
                y = roiY
                x = (float(y - y1) / m) + x1
                if tmpl[0][1] < tmpl[1][1]:
                    pt1 = tmpl[1]
                else:
                    pt1 = tmpl[0]
                pt2 = (x, y)
                crop_lines.append([pt1, pt2])
                
        for cropl in crop_lines:
            
            pt1 = cropl[0]
            pt2 = cropl[1]
            print cropl
            print pt1
            print pt2
            
            cv2.line(frameClone, san.double_tuple_2_int(pt1), san.double_tuple_2_int(pt2), blue, 5)
           
            print "HLO AVG CROP (x1, y1) = (%i, %i) (x2, y2) = (%i, %i) m = %f"\
                  % (pt1[0], pt1[1], pt2[0], pt2[1], ((pt2[1] - pt1[1]) / (pt2[0] - pt1[0])))
    # Second Loop
    if lines2 is not None:
        for line in lines2:
            
            # Display HoughLinesP
            for x1, y1, x2, y2 in line:
                delta_x = float(x1 - x2)
                if delta_x == 0:
                    cv2.line(frameClone, (x1 + roiX, y1 + roiY), (x2 + roiX, y2 + roiY), red, 10)
                else:
                    m = float(y1 - y2) / delta_x
                   
                    if m < -0.5 or m > 0.5:
                        
                        print "HLP (x1, y1) = (%i, %i) (x2, y2) = (%i, %i) m = %f"\
                              % (x1 + roiX, y1 + roiY, x2 + roiX, y2 + roiY, m)
                       

    # Show the frame copy
    cv2.imshow("Car Detection - Color", frameClone)

    print "--------------------------END FRAME %i--------------------------" % frame_num
    frame_num += 1

    key = cv2.waitKey(1) & 0xFF

    if key == ord("p"):
        while True:
            if cv2.waitKey(1) & 0xFF == ord("p"):
                break

    # Quit if the User has decided to quit
    if key == ord("q"):
        break

    time.sleep(frameDelay)

avg /= (cnt + 1)
print "AVG: %f, CNT: %d, MAX: %f, MIN: %f" % (avg, cnt + 1, max, min)
print "CARCNT: %d" % carcnt
fstat.close()
fcstat.close()


print "-------------------------------------------------END-------------------------------------------------"
