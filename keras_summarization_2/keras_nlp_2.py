from nltk.corpus import stopwords
import nltk
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, Model
from keras.layers import Embedding, LSTM, Dense, Attention, Concatenate, Input, RepeatVector
from keras.initializers import Constant
from keras.optimizers import Adam
from transformers import BertTokenizer, BertForPreTraining

# Function to count unique words
def count_unique_words(documents):
    counter = Counter()
    for doc in documents:
        # Tokenize the document into words
        words = nltk.word_tokenize(doc)
        # Update the counter with the words
        counter.update(words)
    return dict(counter)


def get_max_length(docs):
    unique_word_counts = count_unique_words(docs)
    num_words = len(unique_word_counts)
    # Max number of words in a sequence. We need to have the same sequence length when using TensorFlow
    max_length = len(max(docs,key=len))
    return num_words, max_length


def create_tokens(num_words, max_length, docs, train_docs, test_docs):
    #Text tokenizer
    tokenizer = Tokenizer(num_words)
    tokenizer.fit_on_texts(docs)
    word_index = tokenizer.word_index
    # Padding train sequences 
    train_sequences = tokenizer.texts_to_sequences(train_docs)
    train_padded = pad_sequences(train_sequences,maxlen=max_length,padding='post',truncating='post')
    # Padding test sequences 
    test_sequences = tokenizer.texts_to_sequences(test_docs)
    test_padded = pad_sequences(test_sequences,maxlen=max_length,padding='post',truncating='post')
    return train_padded, test_padded
    

df = pd.read_csv('./pytorch_summarization/news_summary.csv', encoding="latin-1")
df = df[['text', 'ctext']]
df.columns = ['summary', 'text']
df = df.dropna()
print(df.head())
print(df.shape)

src_txt = []
sum_txt = []

for index, row in df.iterrows():
    src_txt.append(row['text'])
    sum_txt.append(row['summary'])

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

src_num_words, src_max_length = get_max_length(src_txt)
sum_num_words, sum_max_length = get_max_length(sum_txt)

train_docs_padded, test_docs_padded = create_tokens(src_num_words, src_max_length, src_txt, train_src_txt, test_src_txt)
train_targets_padded, test_targets_padded = create_tokens(sum_num_words, sum_max_length, sum_txt, train_sum_txt, test_sum_txt)

print(f"Shape of train docs {train_docs_padded.shape}")
print(f"Shape of train targets {train_targets_padded.shape}")
print(f"Shape of test docs {test_docs_padded.shape}")
print(f"Shape of test targets {test_targets_padded.shape}")

"""
model = Sequential()
model.add(Embedding(src_num_words, 32, input_length=src_max_length))
model.add(LSTM(64))
model.add(Dense(src_num_words, activation='softmax'))

optimizer = Adam(learning_rate=3e-4)

model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
model.summary()
history = model.fit(np.array(train_docs_padded),np.array(train_targets_padded),epochs=20,validation_data=(np.array(test_docs_padded),np.array(test_targets_padded)))

#output prediction
predicted_output = model.predict(np.array(test_docs_padded))
max_prob_index = np.argmax(predicted_output[0])
print(test_docs_padded[0])
print(predicted_output)
print('Output index: ',max_prob_index)
#print('Output: ',decode(np.array([max_prob_index]),word_index=docs_word_index))
"""

# Prepare input data
input_data = [...]  # Your input data as a list of texts/documents

# Tokenization
tokenizer = Tokenizer()
tokenizer.fit_on_texts(input_data)
sequences = tokenizer.texts_to_sequences(input_data)

max_length = 100  # Maximum sequence length
vocab_size = len(tokenizer.word_index) + 1  # Vocabulary size

padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

# Define the layers
encoder_inputs = Input(shape=(max_length,))
embedding_dim = 100

embedding_layer = Embedding(vocab_size, embedding_dim)(encoder_inputs)
encoder_lstm = LSTM(256)(embedding_layer)
decoder_inputs = RepeatVector(max_length)(encoder_lstm)
decoder_lstm = LSTM(256, return_sequences=True)(decoder_inputs)
decoder_dense = Dense(vocab_size, activation='softmax')(decoder_lstm)

# Create the model
model = Model(inputs=encoder_inputs, outputs=decoder_dense)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
