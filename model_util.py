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

def dowload_model():
  file_id = '1--jrge8I9VvfeOUuYgJ2AxpkUbKG8jiK'
  destination = 'weights.h5'
  download_file_from_google_drive(file_id, destination)

def create_pretrained_model():
    max_length = 128
    # Encoded token ids from BERT tokenizer.
    input_ids = tf.keras.layers.Input(
        shape=(max_length,), dtype=tf.int32, name="input_ids"
    )
    # Attention masks indicates to the model which tokens should be attended to.
    attention_masks = tf.keras.layers.Input(
        shape=(max_length,), dtype=tf.int32, name="attention_masks"
    )
    # Token type ids are binary masks identifying different sequences in the model.
    token_type_ids = tf.keras.layers.Input(
        shape=(max_length,), dtype=tf.int32, name="token_type_ids"
    )

    # Loading pretrained BERT model.
    bert_model = transformers.TFBertModel.from_pretrained("bert-base-uncased")
    # Freeze the BERT model to reuse the pretrained features without modifying them.
    bert_model.trainable = False

    sequence_output, pooled_output = bert_model(
      input_ids, attention_mask=attention_masks, token_type_ids=token_type_ids
    )

    # Add trainable layers on top of frozen layers to adapt the pretrained features on the new data.
    bi_lstm = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True))(sequence_output)

    # Applying hybrid pooling approach to bi_lstm sequence output.
    avg_pool = tf.keras.layers.GlobalAveragePooling1D()(bi_lstm)
    max_pool = tf.keras.layers.GlobalMaxPooling1D()(bi_lstm)
    concat = tf.keras.layers.concatenate([avg_pool, max_pool])
    dropout = tf.keras.layers.Dropout(0.3)(concat)


    # sequence_output = tf.keras.layers.Flatten()(sequence_output)
    output = tf.keras.layers.Dense(3, activation="softmax")(dropout)
    model = tf.keras.models.Model(
        inputs=[input_ids, attention_masks, token_type_ids], outputs=output
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss="categorical_crossentropy",
        metrics=["acc"],
    )
    tokenizer = transformers.BertTokenizer.from_pretrained(
        "bert-base-uncased", do_lower_case=True
      )
    return model, tokenizer



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