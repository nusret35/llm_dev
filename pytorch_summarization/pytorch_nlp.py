import json
import pandas as pd
import numpy as np
from pathlib import Path
import lightning as pl

from sklearn.model_selection import train_test_split
from termcolor import colored
import textwrap

from torch.utils.data import Dataset, DataLoader
from lightning.pytorch import Trainer
from lightning.pytorch.callbacks import ModelCheckpoint

from lightning.pytorch.loggers import TensorBoardLogger
from transformers import AdamW, T5ForConditionalGeneration, T5TokenizerFast as T5Tokenizer
from tqdm.auto import tqdm

import seaborn as sns
import matplotlib.pyplot as plt

from pytorch_dataset import NewsDataModule
from pytorch_models import SummaryModel

pl.seed_everything(1234)

df = pd.read_csv('./pytorch_summarization/news_summary.csv', encoding="latin-1")
df = df[['text', 'ctext']]
df.columns = ['summary', 'text']
df = df.dropna()
print(df.head())
print(df.shape)

train_df, test_df = train_test_split(df, test_size=0.1)

MODEL_NAME = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)

text_token_counts = [len(tokenizer.encode(row["text"])) for _, row in train_df.iterrows()]
summary_token_counts = [len(tokenizer.encode(row["summary"])) for _, row in train_df.iterrows()]

N_EPOCHS = 3
BATCH_SIZE= 16

data_module = NewsDataModule(
    train_df, 
    test_df,
    tokenizer,
    batch_size=BATCH_SIZE
)

model_1 = SummaryModel()

callbacks = ModelCheckpoint(
    dirpath="/checkpoints",
    filename="base-checkpoint",
    save_top_k=1,
    verbose=True,
    monitor="val_loss",
    mode='min'
)

logger = TensorBoardLogger("lightning_logs", name="news_summary") 

trainer= Trainer(
    logger=logger,
    callbacks=callbacks,
    max_epochs=N_EPOCHS,
)

trainer.fit(model_1,datamodule=data_module)

best_model = SummaryModel.load_from_checkpoint(
    trainer.best_model_path
)

best_model.freeze()

import pickle
filename = open('text_summarization_model.pkl', 'wb')
pickle.dump(best_model.model, filename)
model = pickle.load(open('text_summarization_model.pkl', 'rb'))

def encode_text(text):
    # Encode the text using the tokenizer
    encoding = tokenizer.encode_plus(
        text,
        max_length=512,
        padding="max_length",
        truncation=True,
        return_attention_mask=True,
        return_tensors='pt'
    )
    return encoding["input_ids"], encoding["attention_mask"]

def generate_summary(input_ids, attention_mask):
    # Generate a summary using the best model
    generated_ids = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=150,
        num_beams=2,
        repetition_penalty=2.5,
        length_penalty=1.0,
        early_stopping=True
    )
    return generated_ids

def decode_summary(generated_ids):
    # Decode the generated summary
    summary = [tokenizer.decode(gen_id, skip_special_tokens=True, clean_up_tokenization_spaces=True)
               for gen_id in generated_ids]
    return "".join(summary)

def summarize(text):
    input_ids, attention_mask = encode_text(text)
    generated_ids = generate_summary(input_ids, attention_mask)
    summary = decode_summary(generated_ids)
    return summary

text = """Delhi Capitals’ head coach Ricky Ponting during a press conference in Delhi on Friday. | Photo Credit: PTI

Ricky Ponting knows a thing or two about cricket and spotlight and how together, the two can either be a recipe for unprecedented success or unmitigated disaster, depending on how one handles them.

In India, in particular, the pressure to manage both is a lot more than anywhere else and the IPL is at the pinnacle of fan attention. “Well it is a lot different in our country than it is here. The big thing about the IPL is seeing so many younger players getting an opportunity that they are not ready for. And I don’t mean the sport per se. They are ready for the cricket side of it but there are a lot of guys not ready, yet, for the many other things that come with cricket. There wasn’t as much spotlight on me back as a young player as on some of the young Indian players today,” Ponting admitted.

And, being the coach and legend that he is, he accepts the responsibility to try and guide them. “For me, it’s letting players understand how big what they are doing actually is, in the public’s eyes. As a player you want to play cricket, you want to represent your team and franchise and country, but sometimes you can’t see the bigger picture behind it than just you playing cricket. It’s also about how everyone sees you in the real world and the IPL, for a lot of these youngsters, is not the real world. There’s a lot of other stuff happening out there,” he cautioned.


Ponting predicts this year’s IPL will see the real Prithvi Shaw
His advice? Get your act together outside the field so you can perform inside. “My job is to make them better players but, at the end of the day, I want them to be better people. I think the better you are as a person, the easier it is to be a better player and if you haven’t got your life in order off the field, it’s really difficult to be a disciplined performer on it. That’s one of the things I try to teach because I have been there, done that,” the 48-year-old World Cup-winning captain explained.

And in a World Cup year, who better than a two-time winning captain to ask about the constant hype around Indian performers in IPL? “Ideally we would want them all to have that drive and passion to be the best they can be but the one thing I always stress with young guys is, not to start looking too far ahead and thinking about the World Cup. They need to stay in the present and think about the here and now and play their role in the team. My job is to train and get these guys ready to win games for us but after that, their selections for any other event or format are not in my hands,” he shrugged."""

model_summary = summarize(text)

print(model_summary)
