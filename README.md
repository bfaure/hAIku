# hAIku
RNN Haiku generator using Keras and Tensorflow.

## Getting the data
Run `fetcher.py` to download all haiku (~350,000) from the site http://haiku.somebullshit.net/, alternatively you can use the pre-downloaded file `data.tsv` which contains all haiku from the site as of June 2018. The download/scraping takes about 20 minutes with my processor & internet speeds. The resultant `data.tsv` file is about 25 MB.

## Training the model
Run `model.py` to train.
