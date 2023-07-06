from data_collection import output_text
from data_cleaning import clean_data
from pathlib import Path
from dataset_api import get_dataset
from nlp import train_nlp

'''
GOOGLE_DRIVE_DATASET_FOLDER_ID = '1EyD75cYyLqRe0YlP7r556GkxIrDmv6Wy'
dataset = get_dataset(GOOGLE_DRIVE_DATASET_FOLDER_ID)
'''

z = Path('datasets/')

texts, targets = output_text(z)

texts = clean_data(texts)

# 'texts' array is a list of arrays (after the data cleaning), where each array represents a course
# 'targets' array is a list of arrays, where each array stores a single string and is the content of the learning outcome of a course

train_nlp(texts,targets)


