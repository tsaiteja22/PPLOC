import eventlet
import socketio
import numpy as np
import json
from SensorDataAggregation import *
import pickle
from threading import Timer

sio = socketio.Server()
app = socketio.WSGIApp(sio)
sidList=[]
count = 0
sd_dict = {} 
aggr = []
publicKey = getPublicKey()
SentReqToNodes=False



def json_dec(data1):
    #print("Decode JSON formatted Data")
    JSONData = json.loads(json.loads(json.dumps(data1, default=lambda o: o.__dict__)))
    return JSONData

def send_acks():
    global SentReqToNodes
    while True:
        print ("Ok")
        sio.emit("sendData","Send",room="sensor_room")
        SentReqToNodes = True
        if (len(sidList) > 0):
            sio.send(sidList[0],"Send")
        sio.sleep(5)

@sio.event
def getACKFromCentralStatus(sid,data):
    global SentReqToNodes
    if (didReceiveACKFromCentral() and SentReqToNodes == False):
        print ('Sending acknowledgement to nodes')
        SentReqToNodes = True
        sio.emit("sendData","Send",room="sensor_room")
    #sio.emit("ackFromCentral",didReceiveACKFromCentral(),"sensor_room")

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sidList.append(sid)
    sio.enter_room(sid,'sensor_room')


@sio.event
def getPublicKeyToNodes(sid,data):
    print ("In Nodes")
    sio.emit("publicKeyData",getPublicKey(),room="sensor_room")

@sio.event
def SensorData(sid, data):
    global publicKey
    global count, aggr, sd_dict,SentReqToNodes
    pkFromRealHub = pickle.loads(getPublicKey())
    existingPK = pickle.loads(publicKey)
    if ('pk' not in existingPK.keys() or  'pk' not in pkFromRealHub.keys() or existingPK['pk'] != pkFromRealHub['pk']):
        publicKey = pkFromRealHub
        count = 0
        sio.emit("publicKeyData",publicKey,room="sensor_room")
        sio.emit("sendData","Send",room="sensor_room")
        SentReqToNodes = True
        t.cancel()
        return
   
    count=count + 1
    data = json_dec(data)
    print('Recieved data from node {}.{}'.format(sid, data))
    
    sd_dict[sid] = data['0']['0']
    
    if (count == 4):
        count = 0
        SentReqToNodes = False
        print("Received from sensor nodes")
        #sio.emit("sendData","Send",room="sensor_room")
        sd_matrix = np.array(list(sd_dict.values()))
        aggr = getRealSummation(sd_matrix)
        print(aggr)
        #t.start()
    return aggr

            
@sio.event
def disconnect(sid):
    print('disconnect ', sid)
    sidList.remove(sid)
    sio.leave_room(sid,'sensor_room')

if __name__ == '__main__':
    print ("Server ")
    t= Timer(1,getACKFromCentralStatus)
    eventlet.wsgi.server(eventlet.listen(('141.44.154.241', 5010)), app)

