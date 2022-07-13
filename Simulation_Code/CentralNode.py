from phe.paillier import EncryptedNumber
import numpy as np
import phe
pk, sk = phe.paillier.generate_paillier_keypair(n_length=128)
"""Key generation using paillier library
    Args:
      n_length: key size in bits.
    Returns:
      tuple: The generated :class:`PaillierPublicKey` and
      :class:`PaillierPrivateKey`
"""
keys = [pk,sk]
finalresultmap={} # Dictionary to store decrypted measurement vectors

def getDecryptedSummation(sk,resultmap,pk=None):
    """
    Performs decryption of the aggregated cipher texts

    :param sk: class: Private key which has been generated
    :param resultmap: dic: Aggregated cipher texts represented as objects
    :param pk: class: None
    :return: d: Decrypted measurement vectors
    """
    #print(resultmap)
    for i in range(len(resultmap)):
        resultvectorlist = []
        for j in range(len(resultmap.get(i))):
            # Performs decrypt operation using paillier decrypt method
            r = sk.decrypt(resultmap.get(i)[j])
            resultvectorlist.append(r)
        finalresultmap[i] = np.matrix(resultvectorlist)
    #print(finalresultmap)
    return finalresultmap
