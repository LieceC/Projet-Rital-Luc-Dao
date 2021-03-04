#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:10:57 2021

@author: dao
"""
import sys
sys.path.insert(1,"..")
import utils.collection as c
import utils.TextRepresenter as tr
import utils.weighters as w
import utils.modeles as m
import pagerank as pr
import time

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

base = "cisi" # cacm
col0 = c.Parser.parse("../data/"+base+"/"+base+".txt")
col1 = c.QueryParser.parse("../data/"+base+"/"+base+".qry", None)


index = c.IndexerSimple(col0)

q = pretraitement_requete(col1['16'].text)

weighter = w.Weighter1(index)

model_V = m.Vectoriel(index,weighter,False)


V, S = pr.sous_graph(model_V, q, 10, 5)