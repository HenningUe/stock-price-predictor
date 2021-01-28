
# https://stackoverflow.com/questions/43533610/how-to-use-hyperopt-for-hyperparameter-optimization-of-keras-deep-learning-netwo

# https://blog.dominodatalab.com/hyperopt-bayesian-hyperparameter-optimization/

# https://towardsdatascience.com/keras-hyperparameter-tuning-in-google-colab-using-hyperas-624fa4bbf673

# https://medium.com/vooban-ai/hyperopt-tutorial-for-optimizing-neural-networks-hyperparameters-e3102814b919

import hyperopt as hypopt
from sklearn.metrics import roc_auc_score
import sys

X = []
y = []
X_val = []
y_val = []

space = {'choice': hypopt.hp.choice('num_layers', [{'layers': 'two', },
                                                   {'layers': 'three',
                                                    'units3': hypopt.hp.uniform('units3', 64, 1024),
                                                    'dropout3': hypopt.hp.uniform('dropout3', .25, .75)}
                                                   ]),

         'units1': hypopt.hp.uniform('units1', 64, 1024),
         'units2': hypopt.hp.uniform('units2', 64, 1024),

         'dropout1': hypopt.hp.uniform('dropout1', .25, .75),
         'dropout2': hypopt.hp.uniform('dropout2', .25, .75),

         'batch_size': hypopt.hp.uniform('batch_size', 28, 128),

         'nb_epochs': 100,
         'optimizer': hypopt.hp.choice('optimizer', ['adadelta', 'adam', 'rmsprop']),
         'activation': 'relu'
         }


# Objective Function
# This is a function to minimize that receives hyperparameters values as input from the search space
# and returns the loss. This means during the optimization process, we train the model with selected
# hyperparameters values and predict the target feature and then evaluate the prediction error and
# give it back to the optimizer. The optimizer will decide which values to check and iterate again.
# You will learn how to create an objective function in a practical example.
def f_nn(params):
    from keras.models import Sequential
    from keras.layers.core import Dense, Dropout, Activation
    # from keras.optimizers import Adadelta, Adam, RMSprop

    print ('Params testing: ', params)
    model = Sequential()
    model.add(Dense(output_dim=params['units1'], input_dim=X.shape[1]))
    model.add(Activation(params['activation']))
    model.add(Dropout(params['dropout1']))

    model.add(Dense(output_dim=params['units2'], init="glorot_uniform"))
    model.add(Activation(params['activation']))
    model.add(Dropout(params['dropout2']))

    if params['choice']['layers'] == 'three':
        model.add(Dense(output_dim=params['choice']['units3'], init="glorot_uniform"))
        model.add(Activation(params['activation']))
        model.add(Dropout(params['choice']['dropout3']))

    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=params['optimizer'])

    model.fit(X, y, nb_epoch=params['nb_epochs'], batch_size=params['batch_size'], verbose=0)

    pred_auc = model.predict_proba(X_val, batch_size=128, verbose=0)
    acc = roc_auc_score(y_val, pred_auc)
    print('AUC:', acc)
    sys.stdout.flush()
    acc = -acc
    return {'loss': acc, 'status': hypopt.STATUS_OK}


# Trial Object
# The Trials object is used to keep All hyperparameters, loss, and other information,
# this means you can access them after running optimization. Also, trials can help you
# to save important information and later load and then resume the optimization process.
# (you will learn more in the practical example).
trials = hypopt.Trials()

# The fmin function is the optimization function that iterates on different sets of algorithms and their
#  hyperparameters and then minimizes the objective function. the fmin takes 5 inputs which are:-
#     The objective function to minimize
#     The defined search space
#     The search algorithm to use such as Random search, TPE (Tree Parzen Estimators), and Adaptive TPE.
#     NB: hyperopt.rand.suggest and hyperopt.tpe.suggest provides logic for a sequential search of the
#         hyperparameter space.
#     The maximum number of evaluations.
#     The trials object (optional).
best = hypopt.fmin(f_nn, space, algo=hypopt.tpe.suggest, max_evals=50, trials=trials)
print('best: ', best)
