from email import message
import tensorflow as tf
import requests
from flask import Flask
import model_util

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!' 

@app.route('/load')
def load_model():
    model_util.dowload_model()
    return 'Downloaded model! Now go to hello!' 

@app.route('/hello')
def hello():
    model = tf.keras.models.load_model('pretrained_model.h5')
    tokenizer = model_util.get_tokenizer()
    # stringlist = []
    # model.summary(print_fn=lambda x: stringlist.append(x))
    # message = "\n".join(stringlist)
    # print(model.summary())
    sentence1 = 'Good Morning'
    sentence2 = 'Bad Night'
    sentiment, similarity = model_util.is_similar(sentence1, sentence2, tokenizer, model)
    
    message = 'Sentence 1:' + sentence1 + '\n' + 'Sentence 2:' + sentence2 + '\n' + \
         'Sentiment' + str(sentiment) + '\n' + 'Similarity' + str(similarity)

    return message