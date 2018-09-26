import numpy as np
import matplotlib.pyplot as plt
from src.Network import Network
from src.Optimizer import LeastSquares, DeltaRule
from src.Initializer import RandomNormal
from src.Centroids import Fixed
from src.Plotter import plot_centroids_1d
from src.Perceptron import Perceptron

def save_data(data_sting, path):
    with open(path, 'w+') as file:
        file.write(data_sting)
        file.close()

def square(x):
    '''
    pass y = sin(2x)
    '''
    return np.where(x >= 0, 1, -1).astype(float)

def get_radial_coordinates(arg):
    '''
    m = np.array([[np.pi/4  ],
                  [3*np.pi/4],
                  [5*np.pi/4],
                  [7*np.pi/4]]).T
    '''
    q = np.pi/16
    # Test 1

    if arg == 1:
        m = np.array([[q*1, q*7, q*9, q*15, q*17, q*23, q*25, q*31]])
        name = 'tight'

    if arg == 2:
        m = np.array([[q*4, q*12, q*20, q*28]])
        name = 'weak'

    if arg == 3:
        m = 2*np.pi * np.random.rand(1,8)
        name = 'random'

    return {'nodes': m, 'N': m.shape[1], 'name': name}

def generate_data_task31(func, noise_std):

    X = np.arange(0, 2*np.pi, 0.01).reshape(-1,1)
    Y = func(2*X)

    if noise_std > 0:
        Y += np.random.normal(0, noise_std, Y.shape)

    train_X = X[::10].copy()
    train_Y = Y[::10].copy()

    test_X = X[5::10].copy()
    test_Y = Y[5::10].copy()

    return {'X': train_X, 'Y': train_Y}, {'X': test_X, 'Y': test_Y}


def task31():
    training, testing = generate_data_task31(lambda x:np.sin(x), 0)
    #training, testing = generate_data_task31(lambda x:square(np.sin(x)), 0.1)
    rbf_nodes = get_radial_coordinates()

    RadialBasisNetwork = Network(X=training['X'],
                                Y=training['Y'],
                                sigma=1.0,
                                hidden_nodes=rbf_nodes['N'],
                                centroids=Fixed(rbf_nodes['nodes']),
                                initializer=RandomNormal())

    RadialBasisNetwork.train(epochs=1,
                             optimizer=LeastSquares(),
                             epoch_shuffle=True)

    prediction, residual_error = RadialBasisNetwork.predict(testing['X'], testing['Y'])

    print('N_hidden_nodes:',N_hidden_nodes)
    print('residual_error', residual_error)
    plt.plot(testing['X'], testing['Y'], label='True')
    plt.plot(testing['X'], prediction, label='Prediction')
    plt.ylabel('sign(sin(2x))')
    plt.xlabel('x')
    plt.scatter(rbf_nodes, np.zeros(rbf_nodes.size))
    plt.legend()
    plt.show()


def task32():
    training, testing = generate_data_task31(lambda x:np.sin(x), 0.1)

    sigma = np.arange(0.05, 1.4, 0.3)
    tests = [1, 2, 3] # weak, tighter, random

    for t in tests:
        rbf_nodes = get_radial_coordinates(t)
        centroids = Fixed(rbf_nodes['nodes'])
        for sig in sigma:


            RadialBasisNetwork = Network(X=training['X'],
                                         Y=training['Y'],
                                         sigma=sig,
                                         hidden_nodes=rbf_nodes['N'],
                                         centroids=centroids,
                                         initializer=RandomNormal(std=0.1))

            data = RadialBasisNetwork.train(epochs=20,
                                            epoch_shuffle=True,
                                            #optimizer=LeastSquares())
                                            optimizer=DeltaRule(eta=0.1))

            prediction, residual_error = RadialBasisNetwork.predict(testing['X'], testing['Y'])

            print('residual_error', residual_error)
            plt.clf()
            plt.plot(testing['X'], testing['Y'], label='True')
            plt.plot(testing['X'], prediction, label='Prediction')
            #plt.ylabel('sign(sin(2x))')
            plt.ylabel('sin(2x)')
            plt.xlabel('x')
            plt.scatter(rbf_nodes['nodes'], np.zeros(rbf_nodes['nodes'].size))
            plt.legend()
            plot_centroids_1d(centroids,sig)

            path = './figures/task3.2/sin(2x)_sig=' + str(sig) + '_set=' + rbf_nodes['name']
            plt.savefig(path + '.png')
            print(data['config'])
            save_data(data['config'] + '\n\n' + str(residual_error), path + '.txt')

def perceptron():
    training, testing = generate_data_task31(lambda x:np.sin(x), 0)
    rbf_nodes, N_hidden_nodes = get_radial_coordinates()
    eta = 0.000001
    w, c = Perceptron(eta).train(inputs = training['X'], labels = training['Y'], Ww = rbf_nodes, epochs = 1000)

#task31()
task32()
