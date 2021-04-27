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
        """
            Retourne les poids des termes pour LE document IdDoc
        """
        pass
    def getWeightsForStem(self,stem):
        """
            Retourne les poids du terme stem pour TOUS les
            documents qui le contiennent.
        """
        pass
    

    def getWeightsForQuery(self,query):
        '''
            query : dictionnaire {mot : nb occurence dans la requete }  
            renvoie le poids des termes de la requete
        '''
        pass
    
class Weighter1(Weighter):
    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self,query):
        return { term : 1 for term in query.keys()}
    
class Weighter2(Weighter):
    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self,query):
        return query
    
class Weighter3(Weighter):
    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)
    
    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)
    
    def getWeightsForQuery(self,query):
        return { term : self.index.getIDFsForStem(term) for term in query.keys()}
    
class Weighter4(Weighter):
    def getWeightsForDoc(self,idDoc):
        tfs = self.index.getTfsForDoc(idDoc)
        return {t:(1 + np.log(tfs[t])) for t in tfs.keys()}
    
    def getWeightsForStem(self,stem):
        tfs = self.index.getTfsForStem(stem)
        return {t:(1 + np.log(tfs[t])) for t in tfs.keys()}
    
    def getWeightsForQuery(self,query):
        return { term : self.index.getIDFsForStem(term) for term in query.keys()}
    
class Weighter5(Weighter):
    def getWeightsForDoc(self,idDoc):
        tfs = self.index.getTfsForDoc(idDoc)
        return {t:(1 + np.log(tfs[t]))*self.index.getIDFsForStem(t) for t in tfs.keys()}
    
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
    