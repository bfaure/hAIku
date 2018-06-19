import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

print("Loading data... ",end="\r")
filename="data.tsv"
raw_text=open(filename,'r').read().lower()
print("Loading data... done")

print("Getting unique chars... ",end="\r")
chars=sorted(list(set(raw_text)))
char_to_int=dict((c,i) for i,c in enumerate(chars))
print("Getting unique chars... done")

n_chars=len(raw_text)
n_vocab=len(chars)
print("Total characters: %d"%n_chars)
print("Total vocab: 	 %d"%n_vocab)



