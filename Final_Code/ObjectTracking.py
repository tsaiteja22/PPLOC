
import cv2
import numpy as np
import os
import socketio
import json
import pickle
import time

from Encryption import encryption
from Measurements import *
import matplotlib.pyplot as plt


settngCenter = []
updatedArray = []
publicKey = {}
didSentData = False

data=[]
isConnected = False
x_init = np.matrix([[0], [0], [0], [0]])  # Initial [x, y, dx, dy]
P = None

def main():
    """
    Opens camera module and senses coordinates of the object (in our case, red-lazer)
    and send these encrypted measurement vectors for aggregation.

    Returns: An encryption value.
    Return Type: EncryptedNumber.
    """

    global data, x_init, P
    
    font_scale = 1
    font = cv2.FONT_HERSHEY_PLAIN
    
    # Create opencv video capture object
    VideoCap = cv2.VideoCapture(0)
    
    

    # Variable used to control the speed of reading the video
    ControlSpeedVar = 100       # Lowest: 1 & Highest:100

    HiSpeed = 100
    x_upd = []
    y_upd = []
    x_mod = []
    y_mod = []

    #Create KalmanFilter object KF

    #KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)

    
    while (True):

        if (publicKey == {}): # Sensors will wait until it receives PublicKey for encryption
            continue

        # Read frame
        ret, frame = VideoCap.read()
        
        cv2.circle(frame, (30, 480), 5, (0, 255, 255), -1)
        cv2.circle(frame, (360, 480), 5, (0, 255, 255), -1)
        cv2.circle(frame, (30, 130), 5, (0, 255, 255), -1)
        cv2.circle(frame, (360, 130), 5, (0, 255, 255), -1)
    
        pts1 = np.float32([[30, 480],[360, 480],[40, 130],[360, 130]])
        pts2 = np.float32([[0,0],[0,600],[600,0],[600,600]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(frame, matrix, (600,600))
      
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

        # Detect object (Red lazer)
        # lower mask (0-10)
        lower_red = np.array([0,50,50])
        upper_red = np.array([10,255,255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)

        # upper mask (170-180)
        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)

        mask = mask0+mask1
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
        

        # Draw the detected circle
        cv2.circle(result, maxLoc, 10, (0, 225, 255), 2, cv2.LINE_AA)

        #cv2.circle(frame, (int(centers[0][0]), int(centers[0][1])), 10, (0, 191, 255), 2)

        img_hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)

        ## Gen lower mask (0-5) and upper mask (175-180) of RED
        mask1 = cv2.inRange(img_hsv, (0, 50, 20), (5, 255, 255))
        mask2 = cv2.inRange(img_hsv, (175, 50, 20), (180, 255, 255))

        ## Merge the mask and crop the red regions
        mask = cv2.bitwise_or(mask1, mask2)
        cropped = cv2.bitwise_and(result, result, mask=mask)

        # Predict
        settingCenter = [[maxLoc[0]*0.160], [maxLoc[1]*0.160]]
       
        # x&z coordinates of the laser (converting pixel2cm)
        corx = maxLoc[0] * 0.160            #106/640
        cory = maxLoc[1] * 0.160

        cv2.putText(result, "X:" + str(corx) + "Y:" + str(cory), (int(10), int(20)), font, fontScale=font_scale,
                    color=(0, 255, 0), thickness=2)

        cv2.imshow('Frame', result)
        #cv2.imshow("Flipped image", flipHorizontal)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            VideoCap.release()
            cv2.destroyAllWindows()
            break
        settngCenter.append(settingCenter)
        measurement_states_vectors = get_sensor_measurements(settingCenter)
        (summationmap, pk) = encryption(measurement_states_vectors,publicKey)
    
    
        data = json_enc(summationmap)
        global isConnected
        #if (didSentData == False):
        if (isConnected):
            send_sensor_readings()

        cv2.waitKey(HiSpeed-ControlSpeedVar+1)
    plt.show()
    return summationmap

def json_enc(data1):
    """
    Coverts given data into string objects for JSON seriallization.
        Parameter: data1
        Retuns : JSON encoded string objects
    """
    JSONData = json.dumps(data1, default = lambda o: o.__dict__)
    return JSONData


sio = socketio.Client()
    
def send_sensor_readings():
     global didSentData
     while True:
        global publicKey
        if (publicKey == {}):
            sio.emit("getPublicKeyToNodes",'')  # PublicKey receives from server
        if (data != [] and publicKey != {} and didSentData == False):
            print ("Sending Data to server")
            sio.emit('SensorData', data ) #Data sent by client to server
            didSentData = True
        if (didSentData):
            sio.emit('getACKFromCentralStatus', '' )
        return
        #sio.sleep(1)          #Refreshes every 11 second1

"""
Below are communication events under TCP/IP protocol using python-socketio library
For pip installation of socketio library by using 'pip install python-socketio' command from your terminal/command prompt
"""
            
@sio.event
def sendData(ackData):
    global didSentData        
    if (ackData == "Send"):
        print ("ACK received")
        didSentData = False

        #sio.emit('SensorData', data)
        #didSentData = True

@sio.event
def publicKeyData(key):
    #print (key)
    global publicKey
    publicKey = pickle.loads(key)
        
@sio.event
def connect():
     global isConnected
     isConnected = True
     print('connection established')
     sio.start_background_task(send_sensor_readings)
                   
@sio.event
def disconnect():
      global isConnected
      isConnected = False
      didSentData == False
      print('disconnected from server')

sio.connect('http://141.44.154.241:5010')


# execute main
summationmap = main()



  
