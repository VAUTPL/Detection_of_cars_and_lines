#Library for saving images and video(video doesn't work)
__author__ = 'utpl'

import cv2.cv

# fourcc = cv2.VideoWriter_fourcc(*'MPEG')
fourcc = None
orig = None
dect = None


def vid_init(w, h):
    global fourcc, orig, dect
    #fourcc = cv2.cv.CV_FOURCC(*'MPEG')
    #fourcc = cv2.cv.CV_FOURCC(*'FMP4')
    fourcc = cv2.cv.CV_FOURCC(*'I420')  # YUV420P
    orig = cv2.VideoWriter('original.mp4', fourcc, 30.0, (w, h), True)
    dect = cv2.VideoWriter('detected.mp4', fourcc, 30.0, (w, h), True)


def save_vid_frame(orig_img, dect_img):
    global orig, dect
    orig.write(orig_img)
    dect.write(dect_img)


def save_frame(orig_img, dect_img, name):
    cv2.imwrite("orig/%05d.jpg" % name, orig_img)
    cv2.imwrite("dect/%05d.jpg" % name, dect_img)


def close_save():
    global orig, dect
    orig.release()
    dect.release()
