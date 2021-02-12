#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 16:00:58 2021

@author: dao
"""
import numpy as np

class IRModel:
    def __init__(self,index):
        self.index=index
        
    def getScores(self,query):
        pass
    
    def getRanking(self,query):
        scores = self.getScores(query)
        res = [k for k, v in sorted(scores.items(), key=lambda item: item[1])]
        res.reverse()
        return res
        
class Vectoriel(IRModel):

    def __init__(self,index,weighter,normalized=False):
        super().__init__(index)
        self.weighter=weighter
        self.normalized=normalized
        self.doc_weight = {id_d:self.weighter.getWeightsForDoc(id_d) for id_d in self.index.getIds()}
        if self.normalized:
            self.norme_doc = {id_d:Vectoriel.__norme(w.values()) for id_d,w in self.doc_weight.items()}
        
        
    # fonction de projection
    def __projection(x,y):
        return np.array(list(x))*np.array(list(y))
    
    # fonction de norme
    def __norme(v):
        return np.linalg.norm(list(v))
    
    def __terme_doc_weight(self,id_d,t):
        try:
            return self.doc_weight[id_d][t]
        except KeyError: # le terme n'est pas dans le document
            return 0
        
    def getScores(self,query):
        score = dict()
        weight_query = self.weighter.getWeightsForQuery(query)
        if self.normalized:
            norme_query = Vectoriel.__norme(weight_query.values())
        for id_doc in self.index.getIds():
                
            weight_d = {t:self.__terme_doc_weight(id_doc,t)  for t in weight_query.keys()}
                
            score[id_doc] = Vectoriel.__norme(Vectoriel.__projection(weight_query.values(), weight_d.values()))
            if self.normalized:
                score[id_doc] /= (norme_query + self.norme_doc[id_doc])
        return score

# https://github.com/prdx/RetrievalModels/tree/master/models    
class ModeleLangue(IRModel):
    def __init__(self,index,_lambda = 0.8):
        super().__init__(index)
        self._lambda = _lambda
    
    
    def getScores(self,query):
        '''
            On realise ici le Model avec un log (ne modifie pas l'ordre)
        '''
        score = dict()
        for id_doc in self.index.getIds():
            score[id_doc] = 0 
            file_size = self.index.getDocSize(id_doc)
            for t in query.keys():
                tft = self.index.getTfsForStem(t) # tf pour le terme t
                try:
                    tftdoc = tft[id_doc] # recupère celui du fichier en cours
                except KeyError:
                    tftdoc = 0
                
                # Le modele 
                ptMc = tftdoc/file_size
                ptMd = (sum(tft.values()) - tftdoc)/(self.index.nb_mots - file_size)
                if (1-self._lambda)*ptMc + self._lambda*ptMd != 0:
                    score[id_doc] += np.log((1-self._lambda)*ptMc + self._lambda*ptMd)
        return score
    
class Okapi(IRModel):
    def __init__(self,index,k1=1.2,b = 0.75):
        super().__init__(index)
        self.k1 = k1
        self.b = b
    
    
    def getScores(self,query):
        '''
            On realise ici le Model avec un log (ne modifie pas l'ordre)
        '''
        mean_size = self.index.getMeanDocSize()
        score = dict()
        for id_doc in self.index.getIds():
            score[id_doc] = 0 
            file_size = self.index.getDocSize(id_doc)
            for t in query.keys():
                tft = self.index.getTfsForStem(t) # tf pour le terme t
                try:
                    idftdoc = self.index.getTfIDFsForStem(t)[id_doc] # idf pour le terme t sur le doc
                except KeyError:
                    idftdoc = 1
                try:
                    tftdoc = tft[id_doc] # recupère celui du fichier en cours
                except KeyError:
                    tftdoc = 0
                    
                score[id_doc] += idftdoc*(tftdoc/(tftdoc+self.k1*(1-self.b+self.b*(file_size/mean_size))))
        return score