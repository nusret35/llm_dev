from nltk.corpus import stopwords
import nltk
import numpy as np
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
    for doc in documents:
        for content in doc:
            # Tokenize the document into words
            words = nltk.word_tokenize(content)
            # Update the counter with the words
            counter.update(words)
    return dict(counter)

def decode(text,word_index):
    return " ".join([word_index.get(i, "?") for i in text])


def create_tokens(docs, num_words, max_length):

    #Text Tokenizer
    tokenizer = Tokenizer(num_words)
    tokenizer.fit_on_texts(docs)
    word_index = tokenizer.word_index
    print(word_index)

    # Data partitioning
    train_docs, test_docs = train_test_split(docs, test_size=0.2, random_state=42)
    
    # Padding train sequences
    train_sequences = tokenizer.texts_to_sequences(train_docs)
    train_padded = pad_sequences(train_sequences,maxlen=max_length,padding='post',truncating='post')

    # Padding test sequences
    test_sequences = tokenizer.texts_to_sequences(test_docs)
    test_padded = pad_sequences(test_sequences,maxlen=max_length,padding='post',truncating='post')

    return train_padded, test_padded

def get_max_length(docs):

    unique_word_counts = count_unique_words(docs)
    num_words = len(unique_word_counts)

    # Max number of words in a sequence. We need to have the same sequence length when using TensorFlow
    max_length = len(max(docs,key=len))

    return num_words, max_length


def train_nlp(docs,targets):
    
    num_words, max_length = get_max_length(docs)
    targets_num_words, targets_max_length = get_max_length(targets)
    
    train_docs_padded, test_docs_padded = create_tokens(docs, num_words, max_length)

    train_targets_padded, test_targets_padded = create_tokens(targets, targets_num_words, targets_max_length)

    print(f"Shape of train docs {train_docs_padded.shape}")
    print(f"Shape of train targets {train_targets_padded.shape}")
    print(f"Shape of test docs {test_docs_padded.shape}")
    print(f"Shape of test targets {test_targets_padded.shape}")

    model = Sequential()

    model.add(Embedding(num_words, 32, input_length=max_length))
    model.add(LSTM(64))
    model.add(Dense(num_words, activation='softmax'))

    optimizer = Adam(learning_rate=3e-4)

    model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    model.summary()
    history = model.fit(np.array(train_docs_padded),np.array(train_targets_padded),epochs=0,validation_data=(np.array(test_docs_padded),np.array(test_targets_padded)))
