# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:43:53 2021

@author: Luc
"""

import numpy as np
import re
import utils.TextRepresenter as TR
import utils.porter as p
from collections import Counter


empty_word = ['the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on']



class Document:
    def __init__(self, I, T = None, B = None, A = None, K = None, W = None, X = None):
        self.identifiant = I
        self.titre = T
        self.date_publication = B
        self.auteur = A
        self.mots_clé = K
        self.text = W
        self.liens = X
        

class Parser:
    def __init__(self, file):
        f = open(file, "r")
        text = f.read()
        self.dico = dict()
        res = re.findall(r"\.I (.*)\n(.T\n(([^.].*\n)*))?",text,re.MULTILINE)
        print(res)
        for i in res:
            self.dico[i[0]] = i[2]
        self.dico
        
class IndexerSimple:
    
    def ciseaux(self,d):
        a = str.lower(d)
        a = np.array(a.split())
        select = list(map(lambda x : x not in empty_word, a))
        a = list(map(lambda x : p.stem(x), a[select]))
        a = dict(Counter(a))
        return a

    def indexation(self,collection):
        index = {}
        index_invers = {}
        
        for doc,value in enumerate(collection):
            c = self.ciseaux(value)
            index[doc] = c
            
            for name, number in c.items():
                try:
                    index_invers[name][doc] = number
                except KeyError:
                    index_invers[name] = {doc : number}
        
        return index, index_invers
