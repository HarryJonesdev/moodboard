import pickle
from sklearn import *
import dill


# Load the sentiment analysis model
with open('C:\\Users\\harry\\Desktop\\final_year_project\\moodboard\\sentiment_analysis_files\\model_lr_tf.pickle', 'rb') as f:
    model = pickle.load(f)

# Load the vectorizer
with open('C:\\Users\\harry\\Desktop\\final_year_project\\moodboard\\sentiment_analysis_files\\tf_vect.pkl', 'rb') as f:
    vectorizer = pickle.load(f)