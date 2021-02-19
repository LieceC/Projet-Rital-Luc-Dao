#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 18:48:36 2021

@author: dao
"""

import sklearn.model_selection as ms
import utils.collection as c
import utils.TextRepresenter as tr

import utils.weighters as w
import utils.modeles as m
from utils.collection import Document, IndexerSimple
import numpy as np


def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)


col0 = c.Parser.parse("data/cisi/cisi.txt")
col1 = c.Parser.parse("data/cisi/cisi.qry")
col2 = c.Parser.parse("data/cisi/cisi.rel")

index_txt = IndexerSimple(col0)
index_rqt = IndexerSimple(col1)


# indices du  train et du test
base = list(col1.items())
train, test = ms.train_test_split(base ,test_size = 0.2)

ret = []
X = np.arange(0, 1, 0.1)
for i in X:
    model_L = m.ModeleLangue(index_txt, _lambda = i)
    sc = 0
    for n, q in train:
        q = pretraitement_requete(q.text)
        tmp = model_L.getScores(q)
        #pert = col2[n]
        tmp = np.sum(list(tmp.values()))
        
        try:
            pred = col2[n]
        except: #Il n'y a pas d'expértise pour le doc
            pred = 1
        
        print(n)
        sc += tmp
    ret += sc
    