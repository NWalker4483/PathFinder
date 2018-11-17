# Apply edge detection method on the imag
import imutils
from PIL import Image #For pixelation
import cv2 
import time
import numpy as np
from imutils.video import VideoStream
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, Response
import datetime
#from IP import get_ip
from getch import getch

def Create_Views():
    #Create Windows to view images
    cv2.namedWindow("base-image", cv2.WINDOW_AUTOSIZE)  
    cv2.namedWindow("result-image", cv2.WINDOW_AUTOSIZE)
    #Position the windows next to eachother
    cv2.moveWindow("base-image",0,0)  
    cv2.moveWindow("result-image",600,0)
    #Start the window thread for the two windows we are using
    cv2.startWindowThread()
def Update_Views(_nimage,_area):
    cv2.imshow("base-image", _nimage)
    cv2.imshow("result-image", _area)

def pixelate(_image,pixelSize=32):
        backgroundColor = (0,)*3
        _image = cv2.flip(_image,1)
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
    
def calibrate(_frame,_width=600):
    _frame = imutils.resize(_frame, width=_width)
    _frame = cv2.flip(_frame,1)
    HSV= cv2.cvtColor(_frame,cv2.COLOR_BGR2HSV)
     # resize the frame, blur it, and convert it to the HSV color space
    HSV = cv2.erode(HSV, None, iterations=15)
    HSV = cv2.dilate(HSV, None, iterations=15)
    area=select_region(HSV)
    # define the lower and upper boundaries of the screen
    hueMax = area[:,:,0].max()
    hueMin = area[:,:,0].min()
    lowerBound = np.array([hueMin,0,0], np.uint8)
    upperBound = np.array([hueMax,255,255], np.uint8)
    mask = cv2.inRange(HSV,lowerBound,upperBound)
    mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    mask=cv2.Canny(mask,50,150)
    return imutils.resize(mask,width=300),imutils.resize(area,width=300),imutils.resize(_frame,width=300)
def filter_region(image, vertices):
        #Create the mask using the vertices and apply it to the input image
        mask = np.zeros_like(image)
        if len(mask.shape)==2:
            cv2.fillPoly(mask, vertices, 255)
        else:
            cv2.fillPoly(mask, vertices, (255,)*mask.shape[2]) # in case, the input image has a channel dimension        
        return cv2.bitwise_and(image, mask)
def select_region(_image):
       # It keeps the region surrounded by the `vertices`. Other area is set to 0 (black).
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
    while True:
        try:
            frame=camera.read()
        except AttributeError:
            pass
        nimage,area,view=calibrate(frame)
        key='w'

        frame = np.concatenate((np.stack((nimage,)*3, axis=-1), area, view), axis=1)
        if key=='q':
            cv2.imwrite("Mask_Screenshot{0}.png".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H:%M:%S')),nimage)
        #stitch Images for video feed
            cv2.imwrite("View_Screenshot{0}.png".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H:%M:%S')),view)
            cv2.imwrite("Area_Screenshot{0}.png".format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d-%H:%M:%S')),area)
   
        _, jpeg = cv2.imencode('.jpg', frame)
        frame=jpeg.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
def ConnectCam(tries=0):
    if tries<10:
        try:
            _camera = VideoStream(tries,resolution=(320, 240),framerate=32).start()
        except NameError:
            tries+=1
            _camera=ConnectCam(tries)
        return _camera
    else:
        print("We've tried to many times Camera Unavailable")

camera=ConnectCam()
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["TEMPLATES_AUTO_RELOAD"]=True
socketio = SocketIO(app, async_mode="threading")

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
   return Response(getit(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@socketio.on("requests")  
def writeout(data):
    print(data)  
if __name__ == '__main__':
    socketio.run(app,host='127.0.0.1', debug=True)
