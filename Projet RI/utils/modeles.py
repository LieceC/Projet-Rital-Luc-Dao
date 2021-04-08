#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 16:00:58 2021

@author: dao
"""
import numpy as np
import time


class IRModel:
    def __init__(self,index):
        self.index=index
        
    def getScores(self,query):
        pass
        
    def try_catch(f,x,value):
        try:
            return f[x]
        except KeyError:
            return value
        
    def getRanking(self,query):
        scores = self.getScores(query)
        
        return list(sorted(scores.items(), key=lambda item: item[1],reverse = True))

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
        
    def getScoresDoc(self,query,id_doc,weight_query):
        weight_d = {t:self.__terme_doc_weight(id_doc,t)  for t in weight_query.keys()}
        s = Vectoriel.__norme(Vectoriel.__projection(weight_query.values(), weight_d.values()))
        if self.normalized:
            s /= (Vectoriel.__norme(weight_query.values()) + self.norme_doc[id_doc])
        return s
        
    def getScores(self,query):
        weight_query = self.weighter.getWeightsForQuery(query)
        return dict(
                (id_doc,self.getScoresDoc(query,id_doc,weight_query))
                for id_doc in self.index.getIds()
                )

# https://github.com/prdx/RetrievalModels/tree/master/models    
class ModeleLangue(IRModel):
    def __init__(self,index,_lambda = 0.8):
        super().__init__(index)
        self._lambda = _lambda
    
    def getScoresDoc(self,query,id_doc,tf):
        file_size = self.index.getDocSize(id_doc)
        res = np.array(list(map(
                lambda x: [x[1],IRModel.try_catch(x[0],id_doc,0)]
                ,tf)))
        res = (1-self._lambda)*\
            res[:,1]/file_size+\
            self._lambda*\
            ((res[:,0] - res[:,1])/(self.index.nb_mots - file_size))
        return np.sum(np.where(res>0,np.log(res),0))
        
    def getScores(self,query):
        '''
            On realise ici le Model avec un log (ne modifie pas l'ordre)
        '''
        tf = np.array(list(
                map(lambda t:
                    [self.index.getTfsForStem(t),
                     np.sum(list(self.index.getTfsForStem(t).values()))],
                    query.keys())))
        return dict(
                (id_doc,self.getScoresDoc(query,id_doc,tf))
                for id_doc in self.index.getIds()
                )
    
    
class Okapi(IRModel):
    def __init__(self,index,k1=1.2,b = 0.75):
        super().__init__(index)
        self.k1 = k1
        self.b = b
    
    def getScoresDoc(self,query,id_doc,tf_idf,mean_size):
        file_size = self.index.getDocSize(id_doc)
        res = np.array(list(map(
                lambda x: [IRModel.try_catch(x[0],id_doc,0),IRModel.try_catch(x[1],id_doc,1)]
                ,tf_idf)))
        return np.sum(res[:,1]*(res[:,0]/(res[:,0]+self.k1*(1-self.b+self.b*(file_size/mean_size)))))
    
    def getScores(self,query):
        '''
            On realise ici le Model avec un log (ne modifie pas l'ordre)
        '''
        tf_idf = np.array(list(
                map(lambda t:
                    [self.index.getTfsForStem(t),self.index.getTfIDFsForStem(t)],
                    query.keys())))
        mean_size = self.index.getMeanDocSize()
        return dict(
                (id_doc,self.getScoresDoc(query,id_doc,tf_idf,mean_size))
                for id_doc in self.index.getIds()
                )

        