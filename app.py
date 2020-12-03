from collections import defaultdict
from email import message
import tensorflow as tf
import requests
import model_util
from flask import render_template, request,Flask
import pandas as pd
import random

app = Flask(__name__)

model = None

@app.before_first_request
def before_first_request_func():
    global model
    print("This function will run once")
    model_util.setup_model()

@app.route('/')
def index():
    return render_template('game1.html') 

@app.route('/question', methods=['GET', 'POST'])
def question():
    response = defaultdict(str) 
    if request.method == 'GET':
        index = random.randint(0,9999)
        question = model_util.train_snli['sentence1'][index]
        response['question'] = question
    elif request.method == 'POST':
        data = request.get_json()
        prev_question = data['question']
        answer = data['answer']
        sentiment, similarity = model_util.is_similar(prev_question, 
                                                    answer , 
                                                    model_util.tokenizer, 
                                                    model_util.model)
        
        index = random.randint(0,9999)
        next_question = model_util.train_snli['sentence1'][index]

        response['sentiment'] = sentiment
        response['similarity'] = str(similarity)
        response['question'] = next_question
    
    return response 

if __name__ == '__main__':
    app.run()