from django.shortcuts import render
from . import views
import pickle
import re
import string
import pandas as pd

# Create your views here.

# preprocessed_data = 

def home (request):
    return render (request , 'homepage.html')

def wordpre(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) # remove special chars
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

def result (request):

    if request.method == 'POST':
        model = pickle.load(open('model.sav','rb'))
        txt = request.POST['text']
        txt = wordpre(txt)
        txt = pd.Series(txt)
        result = model.predict(txt)
        # print(result)

        if result[0] == 1:
            answer = 'TRUE NEWS'
        elif result[0] == 0:
            answer = 'FAKE NEWS'
        return render(request , 'homepage.html',{'answer':answer})


# if request.method == 'POST':
#         txt = request.form['txt']
#         txt = wordpre(txt)
#         txt = pd.Series(txt)
#         result = Model.predict(txt)