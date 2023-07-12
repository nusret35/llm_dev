import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding

df = pd.read_csv('./pytorch_summarization/news_summary.csv', encoding="latin-1")
df = df[['text', 'ctext']]
df.columns = ['summary', 'text']
df = df.dropna()
print(df.head())
print(df.shape)

texts = []
summaries = []

for index, row in df.iterrows():
    texts.append(row['text'])
    summaries.append(row['summary'])

# Initialize and fit the tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts + summaries)

# Tokenize the texts and summaries
tokenized_texts = tokenizer.texts_to_sequences(texts)
tokenized_summaries = tokenizer.texts_to_sequences(summaries)

# Pad the sequences
maxlen_texts = max([len(x) for x in tokenized_texts])
maxlen_summaries = max([len(x) for x in tokenized_summaries])

padded_texts = pad_sequences(tokenized_texts, maxlen=maxlen_texts, padding='post')
padded_summaries = pad_sequences(tokenized_summaries, maxlen=maxlen_summaries, padding='post')

# Find the size of the vocabulary
vocab_size = len(tokenizer.word_index) + 1  # Adding 1 because of reserved 0 index

# Define parameters
latent_dim = 128  # Latent dimensionality of the encoding space.

# Define an input sequence and process it.
encoder_inputs = Input(shape=(None,))
enc_emb =  Embedding(vocab_size, latent_dim, mask_zero = True)(encoder_inputs)
encoder_lstm = LSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder_lstm(enc_emb)

# We discard `encoder_outputs` and only keep the states.
encoder_states = [state_h, state_c]

# Set up the decoder, using `encoder_states` as initial state.
decoder_inputs = Input(shape=(None,))
dec_emb_layer = Embedding(vocab_size, latent_dim, mask_zero = True)
dec_emb = dec_emb_layer(decoder_inputs)

# We set up our decoder to return full output sequences,
# and to return internal states as well. We don't use the 
# return states in the training model, but we will use them in inference.
decoder_lstm = LSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(dec_emb, initial_state=encoder_states)

# Softmax layer for prediction
decoder_dense = Dense(vocab_size, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Define the model that will turn
# `encoder_input_data` & `decoder_input_data` into `decoder_target_data`
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# Compile the model
model.compile(optimizer='rmsprop', loss='sparse_categorical_crossentropy')

# Define the decoder target data
decoder_target_data = np.zeros_like(padded_summaries)
decoder_target_data[:,:-1] = padded_summaries[:,1:]
decoder_target_data = decoder_target_data.reshape(decoder_target_data.shape[0], decoder_target_data.shape[1], 1)

# Train the model
model.fit([padded_texts, padded_summaries], decoder_target_data,
          batch_size=64,
          epochs=3,
          validation_split=0.2)


