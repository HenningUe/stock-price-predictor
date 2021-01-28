from keras_coach import training

# https://github.com/fchollet/deep-learning-with-python-notebooks/blob/master/3.6-classifying-newswires.ipynb

# naechste Schritte:
# https://medium.com/analytics-vidhya/what-nobody-tells-you-about-binary-classification-metrics-4998574b668
# ... accuracy is not a good meatric

# GEMACHT daten beschaffen > inkl. letztem Tag und "overlapping"
# [invalid data > add mask > 1 for valid > 0 for invalid data .. nur bei recurrent
  #  ... https://keras.io/guides/understanding_masking_and_padding/  oder https://www.tensorflow.org/guide/keras/masking_and_padding]
# Ergebnisse gegen Validate-pruefen, Model speichern, ... dann gegen Test

# wie ist das Ergebnis in scalar_regresion zu werten
# andere Layer > Rueckspeisend?
# Parallel: Langzeit > d.h. EOD fuer mehrere Tage/ Wochen
# Parallel: Vorhersage close heute zu close morgen

# GEMACHT: train. validate und test-Daten unterteilen
