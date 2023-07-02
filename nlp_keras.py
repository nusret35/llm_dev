import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import nlp
import random
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

tokenizer = Tokenizer(num_words=10000,oov_token='<UNK>')