from collections import defaultdict
from email import message
import tensorflow as tf
import requests
import util
from flask import render_template, request,Flask
import pandas as pd
import random

app = Flask(__name__)

model = None

@app.before_first_request
def before_first_request_func():
    global model
    print("This function will run once")
    util.setup_model()

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/bertmatch/question', methods=['GET', 'POST'])
def bertmatch_question():
    response = defaultdict(str) 
    if request.method == 'POST':

        #retrieve previous question and answer
        data = request.get_json()
        print(data)
        prev_question = data['question']
        answer = data['answer']

        #compute similarity
        sentiment, similarity = util.is_similar(prev_question, 
                                                    answer,
                                                    util.tokenizer,
                                                    util.model)
        
        response['sentiment'] = sentiment
        response['similarity'] = str(similarity)

    #for both GET and POST definitely send a new random question 
    question = util.get_random_snli_question()
    response['question'] = question
    
    return response 

@app.route('/bertquiz/question', methods=['GET', 'POST'])
def bertquiz_question():
    response = defaultdict(str) 
    if request.method == 'POST':            

        #get previous response by the user
        data = request.get_json()
        user_answer = data['userAnswer']
        correct_answer = data['correctAnswer']

        #compute similarity with correct answer
        sentiment, similarity = util.is_similar(user_answer,
                                                correct_answer,
                                                util.tokenizer,
                                                util.model)
        response['sentiment'] = sentiment
        response['similarity'] = str(similarity)
        
    #for both GET and POST definitely send a new random para, question and answer
    context, question, answer = util.get_random_squad_question()
    response['paragraph'] = context
    response['question'] = question
    response['answer'] = answer

    return response
        

if __name__ == '__main__':
    app.run()
