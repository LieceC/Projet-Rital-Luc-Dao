# -*- coding: utf-8 -*-

from utils.preprocessing import Preprocessing
from utils.utils import Loader 
from sklearn.feature_extraction.text import CountVectorizer

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = Loader.load_pres(fname)

params = {
    "lowercase":True,
    "punct":True,
    "marker":False,
    "number":True,
    "stemming": Preprocessing.stem,
    "ligne": None,
    "strip_accents":True,
    "stopwords": None # set(stop)
}

# 12899
f = lambda x: Preprocessing.preprocessing(x,params)
                            
vectorizer = CountVectorizer(preprocessor = f,lowercase=False,token_pattern = Preprocessing.token_pattern,min_df = 50e-6)

X = vectorizer.fit_transform(alltxts)
print(vectorizer.get_feature_names())