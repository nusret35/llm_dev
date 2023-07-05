from nltk.corpus import stopwords
import nltk
from collections import Counter
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.initializers import Constant
from keras.optimizers import Adam

# Basic NLP

# Function to count unique words
def count_unique_words(documents):
    counter = Counter()
    for course in documents:
        for weekly_content in course:
            # Tokenize the document into words
            words = nltk.word_tokenize(weekly_content)
            # Update the counter with the words
            counter.update(words)
    return dict(counter)

def decode(text,word_index):
    return " ".join([word_index.get(i, "?") for i in text])

def train_nlp(train_docs,train_targets,test_docs,test_targets):
    unique_word_counts = count_unique_words(train_docs)
    num_words = len(unique_word_counts)

    # Max number of words in a sequence. We need to have the same sequence length when using TensorFlow
    max_length = len(max(train_docs,key=len))

    tokenizer = Tokenizer(num_words)
    tokenizer.fit_on_texts(train_docs)
    word_index = tokenizer.word_index
    print(word_index)

    # Padding train sequences
    train_sequences = tokenizer.texts_to_sequences(train_docs)
    train_padded = pad_sequences(train_sequences,maxlen=max_length,padding='post',truncating='post')

    print(train_docs[0])
    print(train_sequences[0])
    print(train_padded[0])

    # Padding test sequences
    test_sequences = tokenizer.texts_to_sequences(test_docs)
    test_padded = pad_sequences(test_sequences,maxlen=max_length,padding='post',truncating='post')

    reverse_word_index = {v: k for k, v in word_index.items()}
    
    print(decode(train_sequences[0],reverse_word_index))

    print(f"Shape of train {train_padded.shape}")
    print(f"Shape of test {test_padded.shape}")

    model = Sequential()

    model.add(Embedding(num_words, 32, input_length=max_length))
    model.add(LSTM(64, dropout=0.1))
    model.add(Dense(1, activation="sigmoid"))

    optimizer = Adam(learning_rate=3e-4)

    model.compile(loss="binary_crossentropy", optimizer=optimizer, metrics=["accuracy"])
    model.summary()
    history = model.fit(train_padded,train_targets,epochs=20,validation_data=(test_padded,test_docs))
    