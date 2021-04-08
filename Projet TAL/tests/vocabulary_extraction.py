# -*- coding: utf-8 -*-
from utils.utils import Loader
from utils.preprocessing import Preprocessing
from utils.utils import Loader 
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
from utils.oddsRatio import OddsRatioCloud

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = Loader.load_pres(fname)

params = {
    "lowercase":False,
    "marker":False,
    "number":False,
    "stemming":False,
    "ligne": None,
    "punct":False,
    "strip_accents":False,
    "stopwords": None
}
f = lambda x: Preprocessing.preprocessing(x,params)
                            
vectorizer = CountVectorizer(preprocessor = f,lowercase=False,token_pattern = Preprocessing.token_pattern)
X = vectorizer.fit_transform(alltxts)

print("nombres de mots différents :",len(vectorizer.get_feature_names()))
print("nombre de mots :",X.sum())

# word cloud des frequences
wordcloud_base = WordCloud(width = 800, height = 800, 
                background_color ='white',max_words=100,stopwords = [],collocations = False,normalize_plurals = False, include_numbers = True)

wordcloud = wordcloud_base.generate(" ".join(alltxts)) 
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 
  
plt.show() 

# oddsratio cloud
datax = []
datay = []

for phrase, l in zip(alltxts,alllabs):
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

for phrase in alltxts:
    mots = phrase.split(" ")
    for mot in mots:
        try:
            res[mot]+=1
        except KeyError:
            res[mot]=1
        
plt.figure(figsize=(20,10))
plt.plot(res.values())
plt.show()