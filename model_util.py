import requests
import numpy as np
import pandas as pd
import tensorflow as tf
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
import transformers
import random
import json
import random
from pprint import pprint
from os import path
import tarfile

train_snli = None
train_squad = None
model = None
tokenizer = None

#Taken from https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python
#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def download_model():
  file_id = '1xq2eOGYh1U0DLy0B40h24qmxIV0IJC7b'
#   destination = 'weights.h5'
  destination = 'pretrained_model.h5'
  if not path.exists(destination):
    download_file_from_google_drive(file_id, destination)

def setup_model():
    global model, tokenizer
    download_model() 
    model = tf.keras.models.load_model('pretrained_model.h5')
    tokenizer = get_tokenizer()
    load_snli_dataset()
    load_squad()

def get_tokenizer():
    tokenizer = transformers.BertTokenizer.from_pretrained(
        "bert-base-uncased", do_lower_case=True
      )
    return tokenizer

def load_snli_dataset():
    global train_snli
    try:
        url = 'https://raw.githubusercontent.com/MohamadMerchant/SNLI/master/data.tar.gz'
        target_path = 'snli.tar.gz'
        response = requests.get(url, stream=True)
        print('Response is:')
        print(response)
        print()
        if response.status_code == 200:
            with open(target_path, 'wb') as f:
                f.write(response.raw.read())
        tar = tarfile.open("snli.tar.gz")
        tar.extractall()
        tar.close()
        train_snli = pd.read_csv("./SNLI_Corpus/snli_1.0_train.csv", nrows=100000)
    except:
        print('snli download failed!')

def load_squad():
    try:
        global train_squad
        url = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json'
        response = requests.get(url, stream=True)
        train_squad = response.json() 
        print(len(train_squad))
    except:
        print('squad download failed!')

def is_similar(sentence1, sentence2, tokenizer, model):
    '''
    Takes a sentence1 and checks if sentence2 is symantically similar to sentence1.
    '''
    max_length = 128

    sent = [sentence1,sentence2]
    
    encoded = tokenizer([sent], return_tensors='tf',add_special_tokens=True,
            max_length=max_length,
            return_attention_mask=True,
            return_token_type_ids=True,
            padding='max_length',
            )

    input_ids = np.array(encoded["input_ids"], dtype="int32")
    attention_masks = np.array(encoded["attention_mask"], dtype="int32")
    token_type_ids = np.array(encoded["token_type_ids"], dtype="int32")

    x_train = [input_ids, attention_masks, token_type_ids]
    # y_train = tf.keras.utils.to_categorical(train_df[0].label, num_classes=3)

    y_pred = np.array(model.predict(x_train))[0]
    # print(y_pred)
    idx = np.argmax(y_pred)
    sentiment_labels = ["contradiction", "entailment", "neutral"]
    return (sentiment_labels[idx], y_pred[idx])