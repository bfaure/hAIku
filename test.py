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
seq_length=9
dataX=[]
dataY=[]
lines=raw_text.split('\n')
total=0
for haiku in lines:
	haiku=haiku.strip()
	for i in range(0, len(haiku)-1-seq_length):
		total+=1
		seq_in=haiku[i:i+seq_length]
		seq_out=haiku[i+seq_length]
		dataX.append([char_to_int[char] for char in seq_in])
		dataY.append(char_to_int[seq_out])
	print("\rTotal parsed: %d"%total,end="\r")

n_patterns=len(dataX)
print("\nInput size: %d"%(n_patterns))

# creating one-hot mappings
X=numpy.reshape(dataX,(n_patterns,seq_length,1))
X=X/float(n_vocab)
y=np_utils.to_categorical(dataY)

# define LSTM model
model=Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# load the network weights
filename="weights-improvement-00-2.0333.hdf5"
model.load_weights(filename)

int_to_char=dict((i,c) for i,c in enumerate(chars))

# pick a random seed
start = numpy.random.randint(0, len(dataX)-1)
pattern = dataX[start]
print ("Seed:")
print ("\"", ''.join([int_to_char[value] for value in pattern]), "\"")
# generate characters
for i in range(1000):
	x = numpy.reshape(pattern, (1, len(pattern), 1))
	x = x / float(n_vocab)
	prediction = model.predict(x, verbose=0)
	index = numpy.argmax(prediction)
	result = int_to_char[index]
	seq_in = [int_to_char[value] for value in pattern]
	sys.stdout.write(result)
	pattern.append(index)
	pattern = pattern[1:len(pattern)]
print ("\nDone.")



