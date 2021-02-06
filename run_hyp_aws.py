

from keras_coach.training import run_hyperopt
print("Start")
run_hyperopt.main(func_name_to_use="rnn_lstm_pure")
input("Press key to finish ...")
