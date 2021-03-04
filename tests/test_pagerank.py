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
import time

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

col0 = c.Parser.parse("../data/cisi/cisi.txt")
col1 = c.QueryParser.parse("../data/cacm/cacm.qry", None)

index = c.IndexerSimple(col0)

