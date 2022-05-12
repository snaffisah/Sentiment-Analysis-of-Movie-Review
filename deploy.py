# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:20:36 2022

@author: snaff
"""

from tensorflow.keras.models import load_model
import os
import json
from sentiment_analysis_modules import ExploratoryDataAnalysis
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import pandas as np

MODEL_PATH = os.path.join(os.getcwd(), 'model.h5')
JSON_PATH = os.path.join(os.getcwd(), 'tokenizer_data.json')

#%%
sentiment_classifier = load_model(MODEL_PATH)
sentiment_classifier.summary()

#%% Tokenizer loading
with open(JSON_PATH, 'r') as json_file:
    token = json.load(json_file)

#%% Deploy
# Step 1) Loading of data
#new_review = ['<br \>I received the parcel a bit late, however...item was in\
#    good condition and work perfectly. Easy to use and can charge it multiple\
#        time. I would suggest this with my friends and family. It worth it.\
#            Im satisfied.<br \>']     

new_review = [input('Review about the movie\n')]
            
# Step 2) Data cleaning
eda = ExploratoryDataAnalysis()
removed_tags = eda.Remove_tags(new_review) # Remove tags
cleaned_input = eda.lower_split(removed_tags) # Convert to lower case & split

# Step 3) Feature selection
# Step 4) Data preprocessing

            
# To vectorize the new review
loaded_tokenizer = tokenizer_from_json(token)

# to vectorize the review into integers
new_review = loaded_tokenizer.texts_to_sequences(cleaned_input)
new_review = eda.sentiment_pad_sequence(new_review)

#%% model prediction
outcome = sentiment_classifier.predict(np.expand_dims(new_review, axis=-1))
#print(outcome)
#print(np.argmax(outcome))

sentiment_dict = {1:'positive', 0:'negative'}
print('This review is ' + sentiment_dict[np.argmax(outcome)])
# positive = [0,1]
# negative = [[]]
