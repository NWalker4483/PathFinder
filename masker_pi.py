# Apply edge detection method on the image
print("Importing Junks & Stuff")
from imutils.video import VideoStream
from imutils import resize
from PIL import Image
import cv2
def CreateViews():
    cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)  
    cv2.moveWindow("base-image",0,0) 
    cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("result-image",600,0)

    cv2.startWindowThread()
def calibrate(_frame,_width=400):
    # define the lower and upper boundaries of the mask
    # ball in the HSV color space, then initialize the
    _frame = resize(_frame, width=_width)
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
def show_mask() :
    try:
        frame=camera.read()
    except AttributeError:
        pass
    nimage=calibrate(frame)
    #nimage = imutils.resize(nimage, width=50)
    cv2.imshow("base-image", frame)
    cv2.imshow("result-image", nimage)
def ConnectCam(tries=0):
    if tries<10:
        try:
            _camera = VideoStream(tries,resolution=(320, 240),framerate=32).start()
        except NameError:
            tries+=1
            _camera=ConnectCam(tries)
        return _camera
    else:
        print("We've tried to many times")

camera=ConnectCam()
print("Lets get it started in here")
while True:
    try:
        show_mask()
    except KeyboardInterrupt:
        print("Closing...")
        cv2.destroyAllWindows()
        camera.stream.stop()
        break
    #pimage= pixelate(image,pixelSize=3)
# images showing the region of interest only



	# if the 'q' key is pressed, stop the loop
# cleanup the camera and close any open windows


