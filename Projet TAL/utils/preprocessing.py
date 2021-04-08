# -*- coding: utf-8 -*-

# récupération de la ponctuation
import string
import re
from nltk.stem import PorterStemmer

import unicodedata
from sklearn.feature_extraction.text import CountVectorizer





class Preprocessing:
    
    token_pattern = r"(?u)\b\w\w+\b|\S+" # pour garder la ponctuation
    tokenizer = CountVectorizer(lowercase = False,token_pattern = token_pattern).build_tokenizer()

    # ligne : -2 = resumé, ligne = 0 : titre
    def preprocessing(x,params = dict()):
        def strip_accents(s):
            return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
        """
            params: dictionnaire de valeurs avec 
            lowercase,strip_accents,marker,number,stemming,ligne,stopwords
        """
        global tokenizer
        
        
        # si ligne != None récupère la ligne indiqué
        if params.get("ligne",None) is not None:
            x = x.split('\n')[params["ligne"]]
            
        if params.get("strip_accents",False):
            x = strip_accents(x)
            
        # si fuse => fusionne les mots avec une ponctuation au milieu
        if params.get("punct",False) == "fuse":
            punc = string.punctuation  # recupération de la ponctuation
            x = x.translate(str.maketrans('', '', punc))
            
        # si strip_accents => supprime la ponctuation
        if params.get("punct",False) == "separe":
            punc = string.punctuation  # recupération de la ponctuation
            punc += '\n\r\t'
            x = x.translate(str.maketrans(punc, ' ' * len(punc)))  
        
        if params.get("number",False):
            x = re.sub('[0-9]+', '', x) # remplacer une séquence de chiffres par rien
            
        tokens = Preprocessing.tokenizer(x)
        # --- token users
    
            
        if params.get("marker",False):
            x = " ".join(["@" if str.isupper(token) else token for token in tokens])
            tokens = tokenizer(x)
    
        # si stopwords != None suppression des mots pas dans le dictionnaire
        if params.get("stopwords",False):
            # tokens = [ token for token in tokens if token not in params["stopwords"] or token in string.punctuation]
            x = " ".join([token for token in tokens if token not in params["stopwords"]])
            
        if params.get("stemming",False):
            ps = PorterStemmer()
            x = " ".join([ps.stem(i) for i in tokens])
            tokens = tokenizer(x)
        
        # ---
        if params.get("lowercase",False):
            x = x.lower()
        
            
        return x