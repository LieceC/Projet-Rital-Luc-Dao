#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:10:03 2021

@author: dao
"""

import numpy as np

class Weighter:
    def __init__(self,index):
        self.index=index
    def getWeightsForDoc(self,idDoc):
        pass
    def getWeightsForStem(self,stem):
        pass
    

    def getWeightsForQuery(self,query):
        '''
            query : dictionnaire mot - nb occurence de la requete  
            renvoie le poids des termes de la requete
        '''
        pass
    
class Weighter1(Weighter):
    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self,query):
        res = dict()
        for term in query.keys():
            res[term] = 1
        return res
    
class Weighter2(Weighter):
    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self,query):
        res = dict()
        for term in query.keys():
            res[term] = query[term]
        return res
    
class Weighter3(Weighter):
    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self,query):
        res = dict()
        for term in query.keys():
            res[term] = self.index.getIDFsForStem(term)
        return res
    
class Weighter4(Weighter):
    def getWeightsForDoc(self,idDoc):
        tfs = self.index.getTfsForDoc(idDoc)
        return {t:(1 + np.log(tfs[t])) for t in tfs.keys()}
    
    def getWeightsForStem(self,stem):
        tfs = self.index.getTfsForStem(stem)
        return {t:(1 + np.log(tfs[t])) for t in tfs.keys()}
    
    def getWeightsForQuery(self,query):
        res = dict()
        for term in query.keys():
            res[term] = self.index.getIDFsForStem(term)
        return res
    
class Weighter5(Weighter):
    def getWeightsForDoc(self,idDoc):
        tfs = self.index.getTfsForDoc(idDoc)
        idf = self.index.getIDFsForStem(idDoc)
        return {t:(1 + np.log(tfs[t]))*idf for t in tfs.keys()}
    
    def getWeightsForStem(self,stem):
        tfs = self.index.getTfsForStem(stem)
        idf = self.index.getIDFsForStem(stem)
        return {t:(1 + np.log(tfs[t]))*idf for t in tfs.keys()}
    
    def getWeightsForQuery(self,query):
        res = dict()
        for term in query.keys():
            idf = self.index.getIDFsForStem(term)
            tf = query[term]
            res[term] = (1+np.log(tf))*idf
        return res
    