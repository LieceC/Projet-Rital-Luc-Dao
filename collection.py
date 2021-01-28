# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:43:53 2021

@author: Luc
"""

import numpy as np
import re
import utils.TextRepresenter as TR
from collections import Counter

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
    def __init__(self, d):
        self.collection = d
        
class IndexerSimple:
    def indexation(collection):
        pass