import numpy as np
from phe import *
from phe.paillier import EncryptedNumber
import socketio
import json
import sys
from phe import EncodedNumber
from phe.util import invert, powmod, getprimeover, isqrt
import pickle

resultmap=[]
data = {}
en = {}
pk = {}
receivedFromNodes = False
receivedACKFromCentral = False


def getPublicKey():
    """
    Receives JSON seriallized fromat of PublicKey from the Central Node and
    returns PublicKey object using pickle.
    """
    global pk
    #print ("In getPublic Key")
    if (pk == {}):
        return {}
    pkObj=pickle.loads(pk)
    #print (pkObj)
    return pk

def getRealSummation(summation):
    """
    Aggregates the Encrypted data received from 4 sensor nodes and
    transfers this data to Central Node for decryption
        Parameter: summation - List of Encrypted values of 4 sensor nodes
        Returns: List of EncryptedNumber values of Encoded form.
        Return Type: List of PaillierEncryptedNumber objects
    """
    pkDict = pickle.loads(pk)
    global receivedFromNodes
    
    if (len(summation) == 4):
        # When we are working on 4 sensor nodes in evaluation part
        for i in range(1):
            resultvectorlist = []
            for j in range(4):
                smp = (summation[i][j]['_EncryptedNumber__ciphertext'] * summation[i + 1][j]['_EncryptedNumber__ciphertext'] * summation[i + 2][j]['_EncryptedNumber__ciphertext'] * summation[i + 3][j]['_EncryptedNumber__ciphertext'])
                smp = smp % pkDict['pk'].nsquare
                e_num = phe.paillier.EncryptedNumber(pkDict['pk'], smp, summation[i][j]['exponent'])
                """
                class phe.paillier.EncryptedNumber(public_key, ciphertext, exponent)
                    Represents the Paillier encryption of a float or int.Typically, an EncryptedNumber is created by PaillierPublicKey.encrypt()
                    For more info, please refer 'https://python-paillier.readthedocs.io/en/stable/phe.html'
                        Parameters:
                            public_key (PaillierPublicKey) – the PaillierPublicKey against which the number was encrypted.
                            ciphertext (int) – encrypted representation of the encoded number.
                            exponent (int) – used by EncodedNumber to keep track of fixed precision. Usually negative.
                        Returns: An EncryptedNumber value
                                          
                """
                resultvectorlist.append(e_num)
            
            resultmap = resultvectorlist
            global data,receivedACKFromCentral
            receivedFromNodes = True
            receivedACKFromCentral = False
            data = pickle.dumps(resultmap) 
            #print("In aggregation, public_key: ", pkDict)
            
    elif (len(summation)==3):
        # When we are working on 3 sensor nodes and bluring 1 sensor node in evaluation part
         for i in range(1):
            resultvectorlist = []
            for j in range(3):
                smp = (summation[i][j]['_EncryptedNumber__ciphertext'] * summation[i + 1][j]['_EncryptedNumber__ciphertext'] * summation[i + 2][j]['_EncryptedNumber__ciphertext'])
                smp = smp % pkDict['pk'].nsquare
                e_num = phe.paillier.EncryptedNumber(pkDict['pk'], smp, summation[i][j]['exponent'])
                
                resultvectorlist.append(e_num)
            
            resultmap = resultvectorlist
            print("resultmap", resultmap)
            #global data,receivedACKFromCentral
            receivedFromNodes = True
            receivedACKFromCentral = False
            data = pickle.dumps(resultmap)
    else:
        # When we are working on 1 sensor node1 and bluring 3 sensor nodes in evaluation part
         for i in range(1):
            resultvectorlist = []
            for j in range(1):
                smp = summation[i][j]['_EncryptedNumber__ciphertext']
                smp = smp % pkDict['pk'].nsquare
                e_num = phe.paillier.EncryptedNumber(pkDict['pk'], smp, summation[i][j]['exponent'])
                
                resultvectorlist.append(e_num)
            
            resultmap = resultvectorlist
            #global data,receivedACKFromCentral
            receivedFromNodes = True
            receivedACKFromCentral = False
            data = pickle.dumps(resultmap)
        

    
    return resultmap


sio = socketio.Client()

"""
Below are the events for data communication under TCP/IP protocol using python-socketio libraby
"""

@sio.on('publicKeyData')
def publicKeyData (pkFromCentralNode):
    print (pickle.loads(pkFromCentralNode))
    global pk
    pk = pkFromCentralNode

def send_sensor_readings():
     global receivedFromNodes
     global receivedACKFromCentral
     while True:
        if (data != {} and receivedFromNodes == True and receivedACKFromCentral == False):
            receivedFromNodes = False
            receivedACKFromCentral = False
            sio.emit('SensorData', data ) 
            #sys.wait()
        #sio.sleep(1)
def didReceiveACKFromCentral():
    global receivedACKFromCentral
    return receivedACKFromCentral

@sio.event
def sendData(ackData):
    if (ackData == "Send"):
        print("Received ACK From Cental")
        global receivedACKFromCentral
        receivedACKFromCentral = True
        receivedFromNodes == False
        #sio.emit('SensorData', data)
        #print('Sending data to server')

@sio.event
def connect():
     print('connection established')
     sio.start_background_task(send_sensor_readings)


@sio.event
def disconnect():
      print('disconnected from server')

sio.connect('http://141.44.154.242:5003')
