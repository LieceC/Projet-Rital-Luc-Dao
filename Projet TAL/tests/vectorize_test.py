# -*- coding: utf-8 -*-

from utils.preprocessing import Preprocessing
from utils.utils import Loader 
from sklearn.feature_extraction.text import CountVectorizer

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