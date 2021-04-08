# -*- coding: utf-8 -*-
import string
import re
from nltk.stem import PorterStemmer
import unicodedata
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


class Preprocessing:
    token_pattern = r"(?u)\b\w\w+\b|\S+"
    tokenizer = CountVectorizer(lowercase = False,token_pattern = token_pattern).build_tokenizer()

    # ligne : -2 = resumé, ligne = 0 : titre
    def preprocessing(x,params = dict()):
        """ 
        input:
            X : Une chaine de caractère
            params: dictionnaire de paramètres, peut contenir :
            lowercase,strip_accents,marker,number,stemming,ligne,stopwords

        output:
            x : La chaine de caractère traitée
        """
        def strip_accents(s): # En
            return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
        
        # si ligne != None récupère la ligne indiqué
        if params.get("ligne") is not None:
            x = x.split('\n')[params["ligne"]]
            
        if params.get("strip_accents",False):
            x = strip_accents(x)
            
        # si strip_accents => supprime la ponctuation
        if params.get("punct",False):
            punc = string.punctuation + '\n\r\t' # recupération de la ponctuation
            x = x.translate(str.maketrans(punc, ' ' * len(punc)))  
        
        if params.get("number",False):# Suppr des chiffre
            x = re.sub('[0-9]+', '', x) 
                    
        # --- token users
        tokens = Preprocessing.tokenizer(x)
        if params.get("marker",False):
            tokens = np.where(np.char.isupper(tokens), "@", tokens)
            
        # si stopwords != None suppression des mots pas dans le dictionnaire
        if params.get("stopwords",False):
            tokens = [token for token in tokens if token not in params["stopwords"]]    
        
        if params.get("stemming",False):
            ps = PorterStemmer()
            tokens = [ps.stem(i) for i in tokens]
        
        x = " ".join(tokens)
        
        if params.get("lowercase",False):
            x = x.lower()
            
        return x