import numpy as np
import matplotlib.pyplot as plt
from encryption.Encryption import finalresultmap,measurement_states
from KalmanFiltering.Measurement_model import motion_states, number_of_steps
class InfoFilter(object):

    def __init__(self, z=None):
        # Define the State Transition Matrix A  order is according to the 4 dimensional state [x, y, dx, dy]
        self.A = np.matrix([[1, 0, 0.1, 0],
                            [0, 1, 0, 0.1],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        # Define Measurement Mapping Matrix
        self.H = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0]])

        # Initial Process Noise Covariance
        self.Q = np.array([[0.02, 0, 0.02, 0],
                  [0, 0.02, 0, 0.02],
                  [0.02, 0, 0.02, 0],
                  [0, 0.02, 0, 0.02]])

        # Initial Measurement Noise Covariance
        self.R = np.array([[0.75, 0],
                           [0, 0.6]])

        # Initial Covariance Matrix
        self.P = np.matrix([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])


    def predict(self, x, P = None):
        """
        Predicts the state of the object given the state estimate of the previous state or an initial estimate
        :param x: Initial state estimate/ Previous state estimate
        :param P: Initial error covariance matrix/ Updated error covariance matrix
        :return: Y : Measurement matrix
                 y:  Measurement vector
                 x:  Predicted state estimate
        """

        # Predict state
        # x_k = Ax_(k-1) + Bu_(k-1)
        x = np.dot(self.A, x)

        # Calculate error covariance
        # P= A*P*A' + Q
        if P is not None:# Error covariance matrix of the previous state
            self.P = np.dot(np.dot(self.A, P), self.A.T) + self.Q
        else:
            # Initial error covariance matrix
            self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q

        # Predicted Information Matrix
        self.Y = np.linalg.inv(self.P)

        # Predicted Information vector
        self.y = np.dot(self.Y, x)

        return (self.Y,self.y,x)

    def update(self, Y,y,i,prediction = None):
        """
        Estimates the state of the object
        :param Y: Predicted measurement matrix
        :param y: Predicted measurement vector
        :param i: Aggregated and decrypted measurement vectors
        :param prediction: None
        :return:
        X: State estimate of the object
        P : Respective error covariance of the state estimate
        """

        count =0
        while(count!=2):

            # Measurement Matrix
            self.R1 = np.linalg.inv(self.R)
            self.H1 = self.H.transpose()
            self.I = np.dot((np.dot(self.H1, self.R1)), self.H)

            # Update Information matrix
            # Since the measurement matrices I whose terms H, R are public, matrices have been aggregated directly
            self.Y = Y + (self.I * 4)

            # Update Information Vector
            self.y = y + i # Updation of the measurement vectors

            # Estimated Error Covariance
            self.P = np.linalg.inv(self.Y) # Inverse operation to calculate estimated error covariance

            # Estimated state
            x = np.dot(self.P, self.y)# Inverse operation to calculate estimated state

            # print("Estimated State-->", x, x.shape)
            count+=1
        return (x, self.P)


if __name__ == '__main__':

    # Initial State
    x = np.matrix([[0], [0], [1], [1]])  # [x, y, dx, dy]
    P = None
    predicted = []
    updated = []
    measurement = []
    errordiff = []
    for index in range(len(finalresultmap)):
        vector = InfoFilter()
        (Y, y,prediction) = vector.predict(x, P=P)
        (X,P) = vector.update(Y,y,np.transpose(np.asmatrix(finalresultmap.get(index))))
        x = X
        P = P
        zz = np.array(prediction).flatten()
        yy = np.array(X).flatten()
        #mm = np.asarray()
        predicted.append(zz)
        updated.append(yy)
    predicted = np.array(predicted)
    updated = np.array(updated)

# Calculating error between the state estimates and the ground truth using MSE ( Mean square error)
    for i in range(len(updated)):
        error = ((motion_states[i + 1][0] - updated[i][0]) ** 2) + ((motion_states[i + 1][1] - updated[i][1]) ** 2)
        error = (error ** 0.5)
        errordiff.append(error)
    errordiff = np.array(errordiff)

    """
    Plotting graphs between 
    1. Error between state estimates and ground truth
    2. Information filter and ground truth.
    """
# Error plot
    #plt.plot(errordiff)
    #plt.xlabel('Time')
    #plt.ylabel('Error')
    #plt.legend(['Error'])
    #plt.xlim(-1, number_of_steps)
    #plt.ylim(-1, number_of_steps)

# Information filter and ground truth plot
    plt.plot(updated[:, 0], updated[:, 1])  # IF // mu_current
    plt.plot(motion_states[:,0],motion_states[:,1])
    plt.xlabel('x position')
    plt.ylabel('y position')
    plt.legend(['IF', 'Ground Truth'])
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()