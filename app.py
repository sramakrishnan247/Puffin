from email import message
import tensorflow as tf
import requests
import model_util
from flask import render_template, request,Flask
import pandas as pd

app = Flask(__name__)

model = None

@app.before_first_request
def before_first_request_func():
    global model
    print("This function will run once")
    model_util.dowload_model()
    model_util.load_snli_dataset()
    model = tf.keras.models.load_model('pretrained_model.h5')
    tokenizer = model_util.get_tokenizer()

@app.route('/')
def index():
    return render_template('game1.html') 

@app.route('/question', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':


    return 'Downloaded model! Now go to hello!' 

@app.route('/hello')
def hello():
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

if __name__ == '__main__':
    app.run()