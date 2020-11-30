import tensorflow as tf
import requests
from flask import Flask
import model_util

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!' 


@app.route('/hello')
def hello():
    # model_util.dowload_model()
    model, tokenizer = model_util.create_pretrained_model()
    model.load_weights('weights.h5')
    print(model.summary())
    sentence1 = 'Good Morning'
    sentence2 = 'Bad Night'
    sentiment, similarity = model_util.is_similar(sentence1, sentence2, tokenizer, model)
    
    message = 'Sentence 1:' + sentence1 + '\n' + 'Sentence 2:' + sentence2 + '\n' + \
         'Sentiment' + str(sentiment) + '\n' + 'Similarity' + str(similarity)
    return message