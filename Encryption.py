import numpy as np
np.random.seed(10)
from KalmanFiltering.Measurement_model import *
from encryption.CentralNode import *
from encryption.LocalHub import *
from encryption.CentralNode import pk,sk
summationmap = {} # A dictionary to store all the cipher vector objects in the order of sensors
measurement_states = []
for sensorindex in range(len(sensors)):
    sensor = sensors.get(sensorindex)
    for sindex in range(4):
        measurement_states.append(sensor["measurement_state_s" + str(sindex)])
        vectors = sensor["vectors_s"+str(sindex)]
        ixsx = {}
        for vectorindex in range(0,len(vectors)):
            vector = vectors[vectorindex]
            measurement_vector = vector[1]
            # Representing measurement vector in this form
            m = [[measurement_vector[0]],
                  [measurement_vector[1]],
                  [measurement_vector[2]],
                  [measurement_vector[3]]]

            final_cipher = [] # List to store cipher vectors from all the 4 sensors at every time step
            for i in range(0, len(m)):
                j = m[i]
                for l in range(0, len(j)):
                    element = j[l]
                    # Using paillier encrypt method which returns the cipher as an object
                    cipher = pk.encrypt(element)
                    # Appending the objects in this list
                    final_cipher.append(cipher)
            ixsx[vectorindex] = final_cipher
        summationmap[sensorindex] = ixsx

#print(summationmap)
resultmap= getSummation(summationmap,pk)
finalresultmap=getDecryptedSummation(sk,resultmap)
#print(finalresultmap)