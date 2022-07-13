import numpy as np
import matplotlib.pyplot as plt

# Initial State
x = np.matrix([[100], [200], [1], [1]])  # [x, y, dx, dy]
P = None
updatedlist = []



class InfoFilterr(object):

    def __init__(self):

        # Define the State Transition Matrix A  order is according to this [x, y, dx, dy] in all rows. This is "F" from wiki page
        self.A = np.matrix([[1, 0, 0.1, 0],
                            [0, 1, 0, 0.1],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]])

        #print("A_matrix--->", self.A, self.A.shape)

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


    def predict(self, x, P):

        # Predict state
        # x_k = Ax_(k-1) + Bu_(k-1)
        x = np.dot(self.A, x)
        #print("Predicted state X", x, x.shape)

        # Calculate error covariance
        # P= A*P*A' + Q
        if P is not None:
            self.P = np.dot(np.dot(self.A, P), self.A.T) + self.Q  # self.Q
        else:
            self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q  # self.Q
        #print("Error covariance_matrix--->", self.P, self.P.shape)

        # Predicted Information Matrix
        self.Y = np.linalg.inv(self.P)
        # print("Y_matrix--->", self.Y, self.Y.shape)

        # Predicted Information vector
        self.y = np.dot(self.Y, x)
        # print("y_vector--->", self.y, self.y.shape)


        return (self.Y,self.y,x)

    def update(self, Y,y,i):

        # Measurement Matrix
        self.R1 = np.linalg.inv(self.R)
        self.H1 = self.H.transpose()


        self.I = np.dot((np.dot(self.H1, self.R1)), self.H)
        # print("I_matrix--->", self.I, self.I.shape)

        # Update Information matrix
        self.Y = Y + (self.I * 4)
        # print("Updated Info Matrix--->", self.Y, self.Y.shape)
        
        # Update Information Vector
        self.y = y + i
        # print("Updated Info Vector--->", self.y, self.y.shape)

        # Estimated Error Covariance
        self.P = np.linalg.inv(self.Y)

        # Estimated state
        x = np.dot(self.P, self.y)

        # print("Estimated State-->", x, x.shape)
        return (x, self.P)

def run_filter(finalresultmap):
   
    global P, x, updatedlist
    predicted = []
    updated = []
    measurement = []
    errordiff = []
    for index in range(len(finalresultmap)):
        vector = InfoFilterr()
        (Y, y, prediction) = vector.predict(x, P=P)
        (X, P) = vector.update(Y, y, np.transpose(finalresultmap[index]))
        x = X
        P = P
        zz = np.array(prediction).flatten()
        yy = np.array(X).flatten()
        # mm = np.asarray()
        predicted.append(zz)
        updated.append(yy)
    predicted = np.array(predicted)
    updated = np.array(updated[0])
    print("Estimated", updated)
    updatedlist.append(updated)
    plot_graph(updatedlist)
    #return np.array(updated[0])
    return updatedlist
    

def plot_graph(updated):
    updated = np.array(updated)
    #settngCenter = np.array(settngCenter)
    plt.plot(updated[:,0], updated[:,1])  # IF // mu_current
    #plt.plot(settngCenter[:, 0], settngCenter[:, 1])  # IF // mu_current
    # plt.plot(measurement_states[:, 0], measurement_states[:, 1])

    # plt.plot(errordiff)
    # plt.xlim(-1, number_of_steps)
    # plt.ylim(-1, number_of_steps)
    plt.xlabel('x position')
    plt.ylabel('y position')
    # plt.xlabel('Time')
    # plt.ylabel('Error')
    #plt.legend(['IF', 'Ground Truth'])
    plt.legend(['IF'])
    # plt.legend(['Error'])
    plt.gca().set_aspect('equal', adjustable='box')
    #plt.show()
    plt.savefig("/home/pi/ams-50_CentralServer/Plot.png")
