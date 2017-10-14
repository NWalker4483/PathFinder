# Apply edge detection method on the imag
import imutils
from PIL import Image
import cv2
"""
Run to use usb webcam
sudo apt-get install update
sudo apt-get upgrade
sudo apt-get install python-pygame
wget http://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/resources/imgproc.zip
unzip imgproc.zip
cd library
sudo make install
cd..
"""
cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)  
#cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)
#cv2.namedWindow("cont-image", cv2.WINDOW_AUTOSIZE)
#cv2.namedWindow("real-image", cv2.WINDOW_AUTOSIZE)
#Position the windows next to eachother
#cv2.moveWindow("cont-image",600,400)  
cv2.moveWindow("base-image",0,0)  
#cv2.moveWindow("result-image",600,0)
#cv2.moveWindow("real-image",0,400)
#Start the window thread for the two windows we are using
cv2.startWindowThread()
def calibrate(_frame,_width=600):
    # define the lower and upper boundaries of the mask
    # ball in the HSV color space, then initialize the
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
    return mask
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
def getit() :
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        #nimage = Image.fromarray(nimage)
        nimage=calibrate(image)
        #nimage = imutils.resize(nimage, width=50)
        cv2.imshow("base-image", nimage)
        #cv2.imshow("result-image", area)
        #cv2.imshow("cont-image", image)
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
while True:
    try:
        getit()
    except KeyboardInterrupt:
        print("Closing...")
        camera.close()
        break
    #pimage= pixelate(image,pixelSize=3)
# images showing the region of interest only



	# if the 'q' key is pressed, stop the loop
# cleanup the camera and close any open windows

#cv2.destroyAllWindows()
