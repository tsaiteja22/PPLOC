import numpy as np
np.random
states = [[-100.2, -1.65, 1, 1]]# Initialising the state
sensors = {} # Dictionary to store (measurements, (meas. matrix, meas. vector))
number_of_steps = 100

def get_sensor_measurements(state):
    """

    :param state: Each element of the list "states" is passed
    :return: motion_states, measurement states

    """
    (x_0, y_0, dx, dy) = state  # given initial position at (0,0)
    np.array([x_0, y_0, dx, dy])  # a list to store state at each step following noisy motion model
# Process model
    motion_states = [np.array([x_0, y_0, dx, dy])]
    A = np.array([[1, 0, 0.1, 0],
                  [0, 1, 0, 0.1],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])

    Q = np.array([[0.01, 0, 0.01, 0],
                  [0, 0.01, 0, 0.01],
                  [0.01, 0, 0.01, 0],
                  [0, 0.01, 0, 0.01]])
    for _ in range(number_of_steps):
        motion_noise = np.random.multivariate_normal(mean=np.array([0, 0, 0, 0]), cov=Q)  # ~N(0,Q)
        ground_truth = np.dot(A, motion_states[-1]) + motion_noise
        motion_states.append(ground_truth)

    # Simulate measurements with our noisy measurement model
    # In real life, we get these directly from our sensors

    vectors = [] # a list to store measurement matrices and measurement vectors
    H = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0]])
    R = np.array([[0.75, 0],
                  [0, 0.6]])
# Measurement model
    measurement_states = {}
    for i1 in range(4):
        measurement_state = [np.array([x_0,
                                       y_0])]
        for index in range(number_of_steps):

            new_measurement = np.dot(H, motion_states[index]) + np.random.multivariate_normal(mean=np.array([0, 0]),
                                                                                                  cov=R)  # this is z_t
            measurement_state.append(new_measurement)

            R1 = np.linalg.inv(R)
            H1 = H.transpose()

            # Measurement Matrix
            I = np.dot((np.dot(H1, R1)), H)
            # Measurement Vector
            i = np.dot((np.dot(H1, R1)), measurement_state[index])

            vectors.append([I, i])
        measurement_states["measurement_state_s"+str(i1)] = measurement_state
        measurement_states["vectors_s"+ str(i1)] = vectors
    return measurement_states,motion_states

motion_states = None
for index in range(len(states)):
    state = states[index]
    sensors[index], motion_states = get_sensor_measurements(state)
    sensors[index] = (sensors[index])
    motion_states = np.array(motion_states)

"""sensors.get(0)#whole sensor
(sensors.get(0))[0]#measurement
(sensors.get(0))[1]#vectors(I,i)
((sensors.get(0))[1])[0]#one set of [I,i]
(((sensors.get(0))[1])[0])[0]#I
(((sensors.get(0))[1])[0])[1]#i
"""