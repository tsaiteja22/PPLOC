import numpy as np
import os
#from RealCentralNode import *
from phe import *
import json
import eventlet
import socketio
import pickle
from Decryption import *
from InformationFilter import plot_graph

sio = socketio.Server()
app = socketio.WSGIApp(sio)
    
@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('publicKeyData', data )
    sio.enter_room(sid,'sensor_room')

def send_sensor_readings():
    #print (data)
    sio.emit('publicKeyData', data )


@sio.event
def SensorData(sid, data):
    data = pickle.loads(data)
    print('Recieved data from node {}.{}'.format(sid, data))

    if (data != None):
        resultmap = getRealDecryptedSummation(data)
        sio.emit("sendData","Send",room="sensor_room") 
    return data

@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    sio.leave_room(sid,'sensor_room')

if __name__ == '__main__':
    print ("Server ")
    sio.start_background_task(send_sensor_readings)
    eventlet.wsgi.server(eventlet.listen(('141.44.154.242', 5003)), app)
    
    
#plot_graph(filter_info)
