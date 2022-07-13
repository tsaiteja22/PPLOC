import numpy as np
import os
from phe import *
import pickle


def encryption(measurement_states_vectors,p_k):

    """
    Takes calculated measurement vectors from the Object tracking sensors and convert that data into encrypted objects.
    Parameters:
        measurement_states_vectors - measurement vectors from measurements.
        p_k - Publickey of type 'PaillierPublicKey' received from Central Node.
    Retuns: An encryption value.
    Return Type: List of EncryptedNumber and PublicKey Objects
    """
    summationmap = {}
    #print (p_k)
    pk = p_k['pk']
    
    #print("For encryption, Public_key: ", pk)
      
    measurement_states = []
    for sindex in range(1):
        measurement_states.append(measurement_states_vectors["measurement_state_s" + str(sindex)])
        vectors = measurement_states_vectors["vectors_s" + str(sindex)]
        ixsx = {}
        for vectorindex in range(0, len(vectors)):
            vector = vectors[vectorindex]
            measurement_vector = vector[1]
            m = [[measurement_vector[0]],
                 [measurement_vector[1]],
                 [measurement_vector[2]],
                 [measurement_vector[3]]]

            final_cipher = []  # List to store cipher vectors from all the 4 sensors at every time step
            for i in range(0, len(m)):
                j = m[i]
                for l in range(0, len(j)):
                    element = j[l]
                    cipher = pk.encrypt(element)
                    """
                    encrypt(value)
                        Encode and Paillier encrypt a real number value.
                        
                        Parameters:	
                            value – an int or float to be encrypted.
                        Returns:	An encryption of value.
                        Return type: EncryptedNumber                       
                        Raises: ValueError – if value is out of range.  
                    """
                    final_cipher.append(cipher)
            ixsx[vectorindex] = final_cipher
        summationmap[sindex] = ixsx
    return (summationmap, pk)
