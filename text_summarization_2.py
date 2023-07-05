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
# 'texts' array is a list of dictionaries, where each dictionary represents a course
# 'targets' array is a list of strings, where each string is the content of the learning outcome of a course

texts = clean_data(texts)
print(texts[0])

train_nlp(texts[:2],targets[:2],texts[2:],targets[2:])

