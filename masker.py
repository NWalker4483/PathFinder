# Apply edge detection method on the imag

from collections import deque
import numpy as np
import argparse
import imutils
from PIL import Image
from skimage import img_as_uint
import cv2
# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)  
cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("cont-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("real-image", cv2.WINDOW_AUTOSIZE)
#Position the windows next to eachother
cv2.moveWindow("cont-image",600,400)  
cv2.moveWindow("base-image",0,0)  
cv2.moveWindow("result-image",600,0)
cv2.moveWindow("real-image",0,400)
#Start the window thread for the two windows we are using
cv2.startWindowThread()
camera = cv2.VideoCapture("../Test_Video/testinput.mp4") #"../../Downloads/20171012_124309.mp4")
def pixelate(_image,pixelSize=32):
        backgroundColor = (0,)*3
        _image=Image.fromarray(_image)
        _image = _image.resize((int(_image.size[0]/pixelSize), int(_image.size[1]/pixelSize)), Image.NEAREST)
        _image = _image.resize((int(_image.size[0]*pixelSize), int(_image.size[1]*pixelSize)), Image.NEAREST)
        """
        pixel=_image.load()
        for i in range(0,_image.size[0],pixelSize):
            for j in range(0,_image.size[1],pixelSize):
                for r in range(pixelSize):
                    pixel[i+r,j] = backgroundColor
                    pixel[i,j+r] = backgroundColor
                    """
        return np.array(_image)
def calibrate(_frame,_width):
    _frame = imutils.resize(_frame, width=_width)
    _frame = cv2.flip(_frame,1)
    HSV= cv2.cvtColor(_frame,cv2.COLOR_BGR2HSV)
     # resize the frame, blur it, and convert it to the HSV color space
    HSV = cv2.erode(HSV, None, iterations=15)
    HSV = cv2.dilate(HSV, None, iterations=15)
    area=select_region(HSV)
    hueMax = area[:,:,0].max()
    hueMin = area[:,:,0].min()
    lowerBound = np.array([hueMin,0,0], np.uint8)
    upperBound = np.array([hueMax,255,255], np.uint8)
    mask = cv2.inRange(HSV,lowerBound,upperBound)
    return mask,area,_frame
def filter_region(image, vertices):
        #Create the mask using the vertices and apply it to the input image
        mask = np.zeros_like(image)
        if len(mask.shape)==2:
            cv2.fillPoly(mask, vertices, 255)
        else:
            cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension        
        return cv2.bitwise_and(image, mask)
def select_region(_image):
       # It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
    
        # first, define the polygon by vertices
        rows, cols = _image.shape[:2]
        bottom_left  = [cols*0.1, rows*0.95]
        top_left     = [cols*0.4, rows*0.6]
        bottom_right = [cols*0.9, rows*0.95]
        top_right    = [cols*0.6, rows*0.6] 
        # the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
        vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
        return filter_region(_image, vertices)    
def getit(_width) :
    (_, frame) = camera.read()
    #pimage= pixelate(image,pixelSize=3)
# images showing the region of interest only
    nimage,area,image=calibrate(frame,_width)
    nimage = cv2.blur(nimage,(5,5))
    #nimage = cv2.Canny(nimage,50,150,apertureSize=7
    #Output dtype = cv2.CV_64F. Then take its absolute and convert to cv2.CV_8U
    """
    sobelx64f = cv2.Sobel(nimage,cv2.CV_64F,1,0,ksize=5)
    abs_sobel64f = np.absolute(sobelx64f)
    edges = np.uint8(abs_sobel64f)
    ret,thresh=cv2.threshold(nimage,200,255,cv2.THRESH_BINARY)
    _,countours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #countours=cv2.minEnclosingTriangle(countours)
    cv2.drawContours(frame,countours,-1,(0,255,0),3)
    if len(countours) != 0:
        try:
            for cnt in countours:
                ows,cols = nimage.shape[:2]
                [vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
                lefty = int((-x*vy/vx) + y)
                righty = int(((cols-x)*vy/vx)+y)
                cv2.line(frame,(int(cols),int(righty)),(0,int(lefty)),(0,255,255),2)
        except OverflowError:
            pass
        """
    nimage = imutils.resize(nimage, width=50)
    cv2.imshow("base-image", nimage)
    cv2.imshow("result-image", area)
    cv2.imshow("cont-image", image)
    
    #cv2.imshow("result-image", mask)
	
if __name__=="__main__":
    size=600
    while True:
        key = cv2.waitKey(1) & 0xFF
        try:
            getit(size)
        except AttributeError:
            camera.release()
            camera = cv2.VideoCapture("Test_Video/20171012_124309.mp4")

        if key == ord("q"):
            camera.release()
            break
        if key == ord("w"):
            size+=10


	# if the 'q' key is pressed, stop the loop
# cleanup the camera and close any open windows

#cv2.destroyAllWindows()
