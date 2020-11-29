# Sentence-Similarity
EE 526 Deep Learning Final Project

## About
We build and experiment with different deep learning models to predict the semantic similarity between two sentences. From our experiments, we have observed that the transformer based BERT models outperformed the LSTM network and also trained faster. Moreover, the BERT models that were finetuned with a Bi-directional LSTM gave a much better performance than the BERT model that was not finetuned to the specific task of semantic similarity recognition. We have developed two games, SemanticSimilarityGame and ReadingComprehensionGame, both of which are fun to play and a good way to learn English language

### Core Notebook
BERTPlay_Core.ipynb - This notebook contains our experiments on different BERT and NLP models for the Semantic similarity task.

### Game 1
SemanticSimilarityGame.ipynb<br>
This notebook contains an interactive game where a user needs to enter a sentence that is semantically similar to the provided sentence. A pretrained BERT-based model is used to evaluate the user's performance. 


### Game 2
ReadingComprehensionGame.ipynb <br>
This notebook contains an interactive game where a user needs to answer questions based on the given reading comprehension. A pretrained BERT-based model is used to evaluate the user's performance. 
