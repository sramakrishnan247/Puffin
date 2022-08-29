# Puffin
Test your English language skills!

[![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## About
Puffin is a Web App with two games BERTMatch and BERTQuiz. It uses a pretrained neural network to compute semantic similarity and evaluate user response. BERTQuiz is a Reading Comprehension game and BERTMatch checks how well one can paraphrase a sentence.

### Requirements 🔧
* Python, Flask, Tensorflow, etc as listed in requirements.txt

### Installation 🔌

## 1. Clone this repo

  ress the **Fork** button (on the top right corner of the page) to save a copy of this project on your account.
  Download the repository as follows:
  
    git clone https://github.com/sramakrishnan247/Puffin
  
## 2. Install all required dependencies
  
  Python and its dependencies

    apt-get install -y python python-setuptools python-dev build-essential python-pip 
   
## 3. Install and Configure Web Server

Install Python Flask and Tensorflow dependencies

    pip install -r requirements.txt

## 4. Start Web Server

Start web server

    FLASK_APP=app.py flask run --host=0.0.0.0
    
## 5. Test

Open a browser and go to URL

    http://localhost:5000   
    Enjoy!
    
    
## UI

## Homepage
![Homepage](https://github.com/sramakrishnan247/Puffin/blob/main/static/img/homepage.png)

## BERT Quiz
![BERT Quiz](https://github.com/sramakrishnan247/Puffin/blob/main/static/img/bertquiz.png)

## NLP Experiments
We build and experiment with different deep learning models to predict the semantic similarity between two sentences. From our experiments, we observed that the transformer based BERT models outperformed the LSTM network and also trained faster. Moreover, the BERT models that were finetuned with a Bi-directional LSTM gave a much better performance than the BERT model that was not finetuned to the specific task of semantic similarity recognition. We have developed two games, BertMatch(Paraphrase a sentence) and BertQuiz(Reading Comprehension), both of which are fun to play and a good way to learn English language!
