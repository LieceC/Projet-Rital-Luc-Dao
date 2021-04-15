# -*- coding: utf-8 -*-
from utils.utils import Loader
from utils.preprocessing import Preprocessing
from utils.utils import Loader 
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
from utils.oddsRatio import OddsRatioCloud
from time import time
import spacy
from nltk.corpus import stopwords
lem = spacy.load('fr_core_news_md')

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
train_x,train_y = Loader.load_pres(fname)

stop = list(stopwords.words('french')) + ['cet', 'cette']
params = {
    "lowercase":True,
    "punct":True,
    "marker":True,
    "number":True,
    "stemming": lem, #stemmer.stem,
    "ligne": None,
    "strip_accents":True,
    "stopwords": set(stop)
}
f = lambda x: Preprocessing.preprocessing(x,params)
                            
#vectorizer = CountVectorizer(preprocessor = f,lowercase=False,token_pattern = Preprocessing.token_pattern)

t = time()
#X = vectorizer.fit_transform(train_x)
print(time() - t)
print("nombres de mots différents :",len(vectorizer.get_feature_names()))
print("nombre de mots :",X.sum())

# word cloud des frequences
wordcloud_base = WordCloud(width = 800  , height = 800 , background_color ='white',\
                           max_words=100,stopwords = [],collocations = False,\
                           normalize_plurals = False, include_numbers = True)

wordcloud = wordcloud_base.generate(" ".join(train_x)) 
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 

# oddsratio cloud
datax = []
datay = []

for phrase, l in zip(train_x,train_y):
    mots = phrase.split(" ")
    for mot in mots:
        datax+=[mot]
        datay+=[l]

stopwords = set(STOPWORDS)
min_appear = 5

cloud = OddsRatioCloud(datax, datay, 
                     lower=False, 
                     stopwords=[], 
                     letters_numbers = False, 
                     numbers = False,
                     min_appear = 10,
                     lambd = 10e-3)

res, res_2 = cloud.init(1)
res, res_2 = cloud.init(-1)

# distribution d'apparitions des mots
res = dict()

for phrase in train_x:
    mots = phrase.split(" ")
    for mot in mots:
        try:
            res[mot]+=1
        except KeyError:
            res[mot]=1
        
plt.figure(figsize=(20,10))
plt.plot(list(res.values()))
plt.show()