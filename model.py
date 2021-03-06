import numpy,sys
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

print("\nInitializing...")
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

# prepare the dataset of input to output pairs encoded as integers
seq_length=60
dataX=[]
dataY=[]
lines=raw_text.split('\n')
total,skipped=0,0
for haiku in lines:
	if len(haiku)<seq_length: 
		skipped+=1
		continue
	haiku=haiku.strip()
	for i in range(0, len(haiku)-1-seq_length):
		total+=1
		seq_in=haiku[i:i+seq_length]
		seq_out=haiku[i+seq_length]
		dataX.append([char_to_int[char] for char in seq_in])
		dataY.append(char_to_int[seq_out])
	print("\rTotal parsed: %d, skipped: %d"%(total,skipped),end="\r")

n_patterns=len(dataX)
print("\nInput size: %d"%(n_patterns))

# creating one-hot mappings
X=numpy.reshape(dataX,(n_patterns,seq_length,1))
X=X/float(n_vocab)
y=np_utils.to_categorical(dataY)

# define LSTM model
model=Sequential()
model.add(LSTM(512, input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(512,input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(512,input_shape=(X.shape[1], X.shape[2]),return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(512))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')


# define the checkpoint
filepath="weights-improvement-{epoch:02d}-{loss:.4f}-bigger-model=1.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=False, mode='min')
callbacks_list = [checkpoint]


# fitting model
print("Fitting model...")
model.fit(X, y, nb_epoch=100, batch_size=64, callbacks=callbacks_list)

print("Done.")