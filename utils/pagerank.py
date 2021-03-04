# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 15:43:28 2021

@author: Luc
"""
import numpy as np
import utils.collection as c
import utils.TextRepresenter as tr
import utils.weighters as w
import utils.modeles as mod
import utils.metrique as metr
from utils.metrique import EvalIRModel


def sous_graph(model, query, n, k):
    S = np.array(model.getRanking(query))[:n]
    V = set(S[:,0])
    for doc, score in S:
        Out = model.index.getHyperlinksFrom(doc)
        In  = model.index.getHyperlinksTo(doc)
        V = V.union(list(Out.keys()))
        #V = V.union(np.random.choice(list(In.keys()), k))
    return V, S
    
def page_ranking(model, S, d, nbiter_max = 100, epsilon = 1e-7):
    s = {i : (1/len(S)) for i in S}
    
    p = dict()
    for doc in S:
        nb_liens = model.index.getHyperlinksTo(doc)
        nb_liens = np.array(list(nb_liens.items()),dtype = np.intc)
        nb_liens = nb_liens[np.isin(nb_liens[:,0], list(S))]
        p[doc] = sum(nb_liens[:,1])
    
    
    
    for i in range(nbiter_max):    
        s_new = {i : 0 for i in S}
        for j in S:
            In = model.index.getHyperlinksTo(j)        
            if len(In) != 0:
                In = np.array(list(In.items()))
                In = In[np.isin(In[:,0], list(S))]
                for doc, nbr in In:
                    s_new[j] += (int(nbr)/p[doc])*s[doc]
                
            s_new[j] = s_new[j]*d + (1-d)
                    
        norm = np.sum(list(s_new.values()))
        s_new = {doc : (score/norm) for doc, score in s_new.items()}
        
        l1 = np.array(list(s_new.values()))
        l2 = np.array(list(s.values()))
        """
        if np.max(np.abs(l1-l2)) < epsilon :
            return s_new
        """
        s = s_new
    
    tr = np.array(list(s.values()), dtype = np.float32)
    sort = np.flip(np.argsort(tr))
    
    return np.array(list(s.keys()))[sort]