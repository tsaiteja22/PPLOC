from encryption.Encryption import *
from KalmanFiltering.Measurement_model import number_of_steps
import phe
import numpy as np
resultmap={} # a dictionary to store the aggregated cipher texts

def getSummation(summationmap,pk):
    """
    Paillier homomorphic addition operation is performed

    :param summationmap: dic: Encrypted measurement vectors represented as objects
    :param pk: public key used for aggregation
    :return:resultmap: dic: Aggregated encrypted vectors represented as objects
    """
    ind_sensor_map_0 = summationmap[0]
    for i in range(number_of_steps):
        resultvectorlist = []
        for j in range(4):
            sum = (((ind_sensor_map_0.get(i)[j].ciphertext() * ind_sensor_map_0.get(i+number_of_steps)[j].ciphertext() ) * ind_sensor_map_0.get(i+(number_of_steps*2))[j].ciphertext() )) * ind_sensor_map_0.get(i+(number_of_steps*3))[j].ciphertext()
            sum = sum % pk.nsquare
            e = phe.paillier.EncryptedNumber(pk, sum, ind_sensor_map_0.get(i)[j].exponent)
            #sum = (((ind_sensor_map_0.get(i)[j] + ind_sensor_map_0.get(i+number_of_steps)[j]) + ind_sensor_map_0.get(i+(number_of_steps*2))[j])) + ind_sensor_map_0.get(i+(number_of_steps*3))[j]
            # resultvectorlist.append(sum)
            resultvectorlist.append((e))
        resultmap[i] = resultvectorlist
    return resultmap
