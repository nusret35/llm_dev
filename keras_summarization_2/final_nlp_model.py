import numpy as np
import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding, Attention
from keras.callbacks import EarlyStopping
import nltk
from nltk.corpus import stopwords

# Download stopwords from NLTK and create a set of English stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

df = pd.read_csv('./pytorch_summarization/news_summary.csv', encoding="latin-1")
df = df[['text', 'ctext']]
df.columns = ['summary', 'text']
df = df.dropna()
print(df.head())
print(df.shape)

texts = []
summaries = []

for index, row in df.iterrows():
    text = ' '.join([word for word in row['text'].split() if word not in stop_words])
    summary = ' '.join([word for word in row['summary'].split() if word not in stop_words])
    texts.append(text)
    summaries.append(summary)

# Initialize and fit the tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts + summaries)

# Create the reverse word index
reverse_word_index = dict(map(reversed, tokenizer.word_index.items()))

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
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Define the decoder target data
decoder_target_data = np.zeros_like(padded_summaries)
decoder_target_data[:,:-1] = padded_summaries[:,1:]
decoder_target_data = decoder_target_data.reshape(decoder_target_data.shape[0], decoder_target_data.shape[1], 1)

# Define an early stopping condition to prevent overfitting
# With patience of 3 (which means the training stops if the validation loss does not reduce after 3 epochs)
early_stopping = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)

model.summary()

# Train the model
history = model.fit([padded_texts, padded_summaries], decoder_target_data,
          batch_size=64,
          epochs=3,
          validation_split=0.2,
          callbacks=[early_stopping])

# Plot the accuracy over epochs
import matplotlib.pyplot as plt

plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()

# Generating predictions from the trained model
# Define the encoder model 
encoder_model = Model(encoder_inputs, encoder_states)

# Define the decoder model
decoder_state_input_h = Input(shape=(latent_dim,))
decoder_state_input_c = Input(shape=(latent_dim,))
decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

dec_emb2= dec_emb_layer(decoder_inputs) # Get the embeddings of the decoder sequence

# To predict the next word in the sequence, set the initial states to the states from the previous time step
decoder_outputs2, state_h2, state_c2 = decoder_lstm(dec_emb2, initial_state=decoder_states_inputs)
decoder_states2 = [state_h2, state_c2]
decoder_outputs2 = decoder_dense(decoder_outputs2) # A dense softmax layer to generate prob dist. over the target vocabulary

# Final decoder model
decoder_model = Model(
    [decoder_inputs] + decoder_states_inputs,
    [decoder_outputs2] + decoder_states2)

def decode_sequence(input_seq, reverse_word_index):
    # Encode the input as state vectors.
    states_value = encoder_model.predict(input_seq)

    # Generate empty target sequence of length 1.
    target_seq = np.zeros((1,1))

    # Populate the first character of target sequence with the start character.
    target_seq[0, 0] = tokenizer.word_index['start']

    # Sampling loop for a batch of sequences
    # (to simplify, here we assume a batch of size 1).
    stop_condition = False
    decoded_sentence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value)

        # Sample a token
        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_char = reverse_word_index[sampled_token_index]
        decoded_sentence += ' '+sampled_char

        # Exit condition: either hit max length
        # or find stop character.
        if (sampled_char == 'stop' or
           len(decoded_sentence) > maxlen_summaries):
            stop_condition = True

        # Update the target sequence (of length 1).
        target_seq = np.zeros((1,1))
        target_seq[0, 0] = sampled_token_index

        # Update states
        states_value = [h, c]

    return decoded_sentence

# Preprocess the text
input_text = """
Ad sales boost Time Warner profit

Quarterly profits at US media giant TimeWarner jumped 76% to $1.13bn (£600m) for the three months to December, from $639m year-earlier.

The firm, which is now one of the biggest investors in Google, benefited from sales of high-speed internet connections and higher advert sales. TimeWarner said fourth quarter sales rose 2% to $11.1bn from $10.9bn. Its profits were buoyed by one-off gains which offset a profit dip at Warner Bros, and less users for AOL.

Time Warner said on Friday that it now owns 8 percent search-engine Google. But its own internet business, AOL, had has mixed fortunes. It lost 464,000 subscribers in the fourth quarter profits were lower than in the preceding three quarters. However, the company said AOL's underlying profit before exceptional items rose 8 percent the back of stronger internet advertising revenues. It hopes to increase subscribers by offering the online service free to TimeWarner internet customers and will try to sign up AOL's existing customers for high-speed broadband. TimeWarner also has to restate 2000 and 2003 results following a probe by the US Securities Exchange Commission (SEC), which is close to concluding.

Time Warner's fourth quarter profits were slightly better than analysts' expectations. But its film division saw profits slump 27% to $284m, helped by box-office flops Alexander and Catwoman, a sharp contrast to year-earlier, when the third and final film in the Lord of the Rings trilogy boosted results. For the full-year, TimeWarner posted a profit of $3.36bn, up 27 percent from its 2003 performance, while revenues grew 6.4% to $42.09bn. "Our financial performance was strong, meeting or exceeding all of our full-year objectives and greatly enhancing our flexibility," chairman and chief executive Richard Parsons said. For 2005, TimeWarner is projecting operating earnings growth of around 5%, and also expects higher revenue and wider profit margins.

TimeWarner is to restate its accounts as part of efforts to resolve an inquiry into AOL by US market regulators. It has already offered to pay $300m to settle charges, in a deal that is under review by the SEC. The company said it was unable to estimate the amount it needed to set aside for legal reserves, which it previously set at $500m. It intends to adjust the way it accounts for a deal with German music publisher Bertelsmann's purchase of a stake in AOL Europe, which it had reported as advertising revenue. It will now book the sale of its stake in AOL Europe as a loss on the value of that stake.
"""

tokenized_input_text = tokenizer.texts_to_sequences([input_text])
padded_input_text = pad_sequences(tokenized_input_text, maxlen=maxlen_texts, padding='post')

# Generate summary
decoded_summary = decode_sequence(padded_input_text, reverse_word_index)
original_summary = "TimeWarner said fourth quarter sales rose 2% to $11.1bn from $10.9bn.For the full-year, TimeWarner posted a profit of $3.36bn, up 27 percent from its 2003 performance, while revenues grew 6.4% to $42.09bn.Quarterly profits at US media giant TimeWarner jumped 76% to $1.13bn (£600m) for the three months to December, from $639m year-earlier.However, the company said AOL's underlying profit before exceptional items rose 8 percent on the back of stronger internet advertising revenues.Its profits were buoyed by one-off gains which offset a profit dip at Warner Bros, and less users for AOL.For 2005, TimeWarner is projecting operating earnings growth of around 5%, and also expects higher revenue and wider profit margins.It lost 464,000 subscribers in the fourth quarter profits were lower than in the preceding three quarters. Time Warner's fourth quarter profits were slightly better than analysts' expectations."

print('Original summary:', original_summary)
print('Generated summary:', decoded_summary)
