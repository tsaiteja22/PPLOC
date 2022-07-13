import numpy as np
from InformationFilter import run_filter
import phe
from phe import *
from phe.paillier import EncryptedNumber
import socketio
import json
import sys
import pickle
from PkGenerator import encryption_keys, s_k 


finalresultmap={}
frp = []
data = {}


"""
Below is the code for receiving the homomorphic function result (i.e.,summation)
from the sensors data and then we will use this result for decryption.
"""


def getRealDecryptedSummation(resultmap):
    
    #This function decrypts the encoded cypher text 
    
    global s_k
    sk = s_k['sk']
    print(sk)
    print (resultmap)
    
    resultvectorlist = []
    
    for i in range(len(resultmap)):

        r = sk.decrypt(resultmap[i])
        
        resultvectorlist.append(r)
    
    finalresultmap = np.matrix(resultvectorlist)
      
    print("result vector list", resultvectorlist)
    print("finalresultmap", finalresultmap)
    filter_info = run_filter(finalresultmap)
    #plot_graph(filter_info)
    return filter_info

"""
Below is the code for transmitting public_key to the sensors to the
port address ('http://'). Sensors will receive this public_key
and then encrypt the sensor data.

"""

def json_encoding():
    #print("Encode into JSON formatted Data")
    public_key = pickle.dumps(encryption_keys)
    return public_key

data = json_encoding()

sio = socketio.Client()
    
def send_sensor_readings():
    while True:
        #print(data)
        sio.emit('publicKeyData', data )

            
@sio.event
def sendData(ackData):
    if (ackData == "Send"):
        sio.emit('SensorData', data )
        print('Sending data to server')
        sys.exit()
    return
    
        
@sio.event
def connect():
     print(data)
     print('connection established')
     sio.start_background_task(send_sensor_readings)
            

@sio.event
def disconnect():
      print('disconnected from server')

#plotting = plot_graph(filter_info)


