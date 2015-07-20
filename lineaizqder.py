mport numpy as np
import math
import cv2
import os
from pyimagesearch import imutils
from pyimagesearch.facedetector import FaceDetector
from timeit import timeit
import time

cap = cv2.VideoCapture('/Users/macbookpro/VisionArtificial/video/via_lojacata.mp4')
w= cap.get(3)#width of frame
h= cap.get(4)#height of frame

num_frame = 0
inicio_tiempo = time.time()
fin_tiempo = 0

#directory = os.path.dirname(os.path.abspath(__file__))


#datos para el ROI
roiY = int(h/2)
roiX = 0
roiWid = w
roiHig = h

print roiHig

minLineLength = 100 #100
maxLineGap = 10 #10
threshold = 50 #160
threshold1 = 80

def pendiente(vx1, vx2, vy1, vy2):
    m=float(vy2-vy1)/float(vx2-vx1)
    theta1 = math.atan(m)
    return theta1*(180/np.pi)

def distancia(dx1, dx2, dy1, dy2):
    dist = pow(((dx2-dx1)**2) + ((dy2-dy1)**2),0.5)
    return dist

def nuevo_x1(ny2, ny1, m, nx2):
    n_x1=((ny2-ny1)/m) - nx2
    return n_x1

while(cap.isOpened()):
    ret, frame = cap.read()
    num_frame = num_frame + 1
#    print num_frame

#    if num_frame == 10:
#        fin_tiempo = time.time()
#        print fin_tiempo - inicio_tiempo

    #Cambiar tamano
    #frame = imutils.resize(frame, width = 500)
    
    # Filtros
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Imagen en GRIS
    gray1 = cv2.bilateralFilter(gray,11,20,20)      #filtro 1 , 11, 17, 17
    gray2 = cv2.GaussianBlur(gray,(1,1),0)          #filtro 2
    
    #ROI (Region de Interes)
    grayROI  = gray2[roiY:roiY+roiHig, roiX:roiX+roiWid]
    #grayROI1 = gray2[roiY:roiY+roiHig, roiX:roiX+roiWid]
    #grayROI = gray[roiY:roiY+roiHig, roiX:roiX+roiWid]
    
    
    #Binario
    #(T, thresh) = cv2.threshold(gray2, 155, 255, cv2.THRESH_BINARY)
    #cv2.imshow("Threshold Binary", thresh)
    
    #(T, threshInv) = cv2.threshold(gray2, 155, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow("Threshold Binary Inverse", threshInv)
    
    #cv2.imshow("Coins", cv2.bitwise_and(gray2, gray2, mask =threshInv))
    
    #borde
    edged = cv2.Canny(grayROI, 30, 175)
#edged1 = cv2.Canny(grayROI, 30, 200)
    
    #linea
    lines  = cv2.HoughLinesP(edged, 1,np.pi/180,threshold ,minLineLength,maxLineGap)[0].tolist() #test de borde
#    lines2 = cv2.HoughLinesP(edged1,1,np.pi/180,threshold ,minLineLength,maxLineGap)[0].tolist()

    frameCopy  = frame.copy()
    frameCopy1 = frame.copy()
#    frameCopy2 = frame.copy()
#    frameCopy3 = frame.copy()

    #TODO: Dibujar linea central con houghP
    for x1,y1,x2,y2 in lines:
        if (round(x2-x1)!=0):
            arctan = pendiente(x1,x2,y1,y2)
            if (round(arctan>=round(-50)) and round(arctan<=round(-30))):  #valores -50 y -30 para
                distrecta = distancia(x1,x2,y1,y2)
                #print x1, x2, y1, y2, distrecta, arctan
                cv2.line(frameCopy,(x1 + roiX,y1 + roiY),(x2 + roiX,y2 + roiY),(0,255,0),2)



    #cv2.line(frameCopy,(92 + roiX,110 + roiY),(164 + roiX,65 + roiY),(255,255,0),2)
    #cv2.line(frameCopy,(111 + roiX,89 + roiY),(129 + roiX,76 + roiY),(0,255,0),2)
    #cv2.line(frameCopy,(x1 + roiX,y1 + roiY),(x2 + roiX,y2 + roiY),(0,255,0),2)
    #cv2.line(frameCopy,(x1 + roiX,y1 + roiY),(x2 + roiX,y2 + roiY),(0,255,0),2)

#    for x1,y1,x2,y2 in lines2:
#        cv2.line(frameCopy2,(x1 + roiX,y1 + roiY),(x2 + roiX,y2 + roiY),(0,255,0),2)
#
    #linea izquierda y derecha
    lines1 = cv2.HoughLines(edged,1,np.pi/180,threshold1)

    for rho,theta in lines1[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x11 = int(x0 + 1000 * (-b))
            y11 = int(y0 + 1000 * (a))
            x22 = int(x0 - 1000 * (-b))
            y22 = int(y0 - 1000 * (a))
            
            if ((round(theta*(180/np.pi))>=round(60)  and round(theta*(180/np.pi))<=round(70)) or
                (round(theta*(180/np.pi))>=round(125) and round(theta*(180/np.pi))<=round(150))):  #<75 y >135
                
                #Linea diagonal derecha
                if y22>=roiY:
                    #cv2.line(frameCopy1,(x11 + roiX, y11 + roiY),(x22 + roiX, y22+roiY),(0,255,255),2)
                    pendienterecta = float(x22-x11)/float(y22-y11)
                    x1_nuevo = int(nuevo_x1(y22,y11,pendienterecta, x22))
                    #cv2.line(frameCopy1,(400, int(h/2)),(933, 409),(0,255,255),2)
                    cv2.line(frameCopy1,(x11 + roiX, y11 + roiY),(x22 + roiX, y22 + roiY),(0,255,255),2)
                    print x11,y11,x22, y22, pendienterecta, h/2
                
                #Linea diagonal izquierda
                if y22<=roiY:
                    #cv2.line(frameCopy1,(x11 + roiX, y11 + roiY),(x22 + roiX, y22+roiY),(0,255,255),2)
                    pendienterecta = float(x22-x11)/float(y22-y11)
                    x1_nuevo = int(nuevo_x1(y22,y11,pendienterecta, x22))
                    #cv2.line(frameCopy1,(-704, int(h/2)),(933, 409),(0,255,255),2)
                    #cv2.line(frameCopy1,(x11 + roiX, y11 + roiY),(x22 + roiX, y22 + roiY),(255,0,255),2)



#
#    # linea central
#    lines3 = cv2.HoughLines(edged,1,np.pi/180,70)
#
#    for rho,theta in lines3[0]:
#        a1 = np.cos(theta)
#        b1 = np.sin(theta)
#        x10 = a1*rho
#        y10 = b1*rho
#        x111 = int(x10 + 1000*(-b1))
#        y111 = int(y10 + 1000*(a1))
#        x222 = int(x10 - 1000*(-b1))
#        y222 = int(y10 - 1000*(a1))
#        if (round(theta*(180/np.pi))>=round(55) and round(theta*(180/np.pi))<=round(60)):
#            cv2.line(frameCopy3,(x111 + roiX, y111 + roiY),(x222 + roiX, y222 + roiY),(255,0,255),2)

#   cv2.imshow('Gris', gray)
    cv2.imshow('Canny', edged)
    cv2.imshow('Lineas HoughP', frameCopy)
    cv2.imshow('Lineas Hough', frameCopy1)
    #cv2.imshow('HSV', mask)
    #cv2.imshow('GaussianBlur', frameCopy2)
    #cv2.imshow('GaussianBlur_1', frameCopy3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()