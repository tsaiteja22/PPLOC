import numpy as np
import phe
from phe import *

def getkeys():
    pk, sk = phe.paillier.generate_paillier_keypair(n_length = 128)
    return pk, sk

pk, sk = getkeys()

s_k = {"sk": sk}

encryption_keys = {"pk": pk}
