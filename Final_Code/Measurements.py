import numpy as np
import matplotlib.pyplot as plt

np.random

sensors = {} # Dictionary to store (measurements, (meas. matrix, meas. vector))
number_of_steps = 1

def get_sensor_measurements(measurements):
    """
    Converts sensor measurements from the object tracking sensors to measurement vector matrices
        Parameters:
            measurements - Sensor measurements from the Object tracking sensors
        Returns: measurement vectors
        Return Type: Dictonary of np.array 
    """
    
    (x_0, y_0, dx, dy) = (0,0,0,0)  # given initial position at (0,0)
    np.array([x_0, y_0, dx, dy])  # a list to store state at each step following noisy motion model

    A = np.array([[1, 0, 0.1, 0],
                  [0, 1, 0, 0.1],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])

    Q = np.array([[0.01, 0, 0.01, 0],
                  [0, 0.01, 0, 0.01],
                  [0.01, 0, 0.01, 0],
                  [0, 0.01, 0, 0.01]])
    """
    -Simulate measurements with our noisy measurement model
    -In real life, we are supposed to get these directly from our sensor
    -A list to store state at each step following noisy measurement model,
     assume we have perfect initial measurement
    """
    vectors = []
    H = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0]])  # given H matrix
    R = np.array([[0.75, 0],
                  [0, 0.6]])

    measurement_states = {}
    mmap = {"m0":measurements}

    measurement_state = [np.array([measurements[0][0],
                                   measurements[1][0]])]
    for i1 in range(1):

        measurement_state.append(np.array(mmap["m" + str(i1)]))
        R1 = np.linalg.inv(R)
        H1 = H.transpose()

        I = np.dot((np.dot(H1, R1)), H)
        
        # Measurement Vector

        i = np.dot((np.dot(H1, R1)), measurement_state[i1])
        
        vectors.append([I, i])

        measurement_states["measurement_state_s"+str(i1)] = measurement_state
        measurement_states["vectors_s"+ str(i1)] = vectors
    
    return measurement_states
