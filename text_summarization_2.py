from data_collection import output_text
from pathlib import Path
from dataset_api import get_dataset
from nlp import train_nlp

'''
GOOGLE_DRIVE_DATASET_FOLDER_ID = '1EyD75cYyLqRe0YlP7r556GkxIrDmv6Wy'
dataset = get_dataset(GOOGLE_DRIVE_DATASET_FOLDER_ID)
'''

z = Path('datasets/')

texts, targets = output_text(z)
print(texts)
print(targets)

train_nlp(texts[:1],targets[:1],texts[1:],targets[1:])

