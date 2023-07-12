import pandas as pd
from nltk.corpus import stopwords
import nltk
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Attention, Concatenate
from keras.initializers import Constant
from keras.optimizers import Adam
from transformers import BertTokenizer, BertForPreTraining
from keras import *
from keras.layers import *
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer, one_hot
from keras.preprocessing.sequence import pad_sequences

# Function to count unique words
def count_unique_words(documents):
    counter = Counter()
    for doc in documents:
        # Tokenize the document into words
        words = nltk.word_tokenize(doc)
        # Update the counter with the words
        counter.update(words)
    return dict(counter)

df = pd.read_csv('./pytorch_summarization/news_summary.csv', encoding="latin-1")
df = df[['text', 'ctext']]
df.columns = ['summary', 'text']
df = df.dropna()
print(df.head())
print(df.shape)

train_src_txt = []
test_src_txt = []
train_sum_txt = []
test_sum_txt = []

train_df, test_df = train_test_split(df, test_size=0.1)

for index, row in train_df.iterrows():
    train_src_txt.append(row['text'])
    train_sum_txt.append(row['summary'])
    
for index, row in test_df.iterrows():
    test_src_txt.append(row['text'])
    test_sum_txt.append(row['summary'])

src_unique_word_counts = count_unique_words(train_src_txt)
num_words = len(src_unique_word_counts)
print(num_words)

src_txt_length = len(train_src_txt)
sum_txt_length = len(train_sum_txt)

# encoder input model
inputs = Input(shape=(src_txt_length,))
encoder1 = Embedding(num_words, 128)(inputs)
encoder2 = LSTM(128)(encoder1)
encoder3 = RepeatVector(sum_txt_length)(encoder2)

# decoder output model
decoder1 = LSTM(128, return_sequences=True)(encoder3)
outputs = TimeDistributed(Dense(num_words, activation='softmax'))(decoder1)

# tie it together
model = Model(inputs=inputs, outputs=outputs)
model.compile(loss='categorical_crossentropy', optimizer='adam')

model.summary()
history = model.fit(np.array(train_src_txt), np.array(train_sum_txt), epochs=20, validation_data=(np.array(test_src_txt), np.array(test_sum_txt))
