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
    
def page_ranking(model, S, d, nbiter_max = 100, epsilon = 1e-3):
    s = {i : (1/len(S)) for i in S}
    
    for i in range(nbiter_max):
        
        s_new = {i : 0 for i in S}
        for j in S:
            In = model.index.getHyperlinksTo(j)
            
            if len(In) != 0:
                In = np.array(list(In.items()))
                print(S.intersection(In[:,0]))
                In = In[np.isin(In[:,0], list(S))]
                print(In)
                
                for doc, nbr in In:
                    s_new[j] += (nbr/sum(In[:,1]))*s[doc]
            else:
                print("None")
            s_new[j] *= d
            s_new[j] += (1-d)
        
        norm = np.sum(list(s_new.values()))
        s_new = {doc : (score/norm) for doc, score in s_new.items()}
        
        l1 = np.array(list(s_new.values()))
        l2 = np.array(list(s.values()))
        """
        if np.max(np.abs(l1-l2)) < epsilon :
            return s_new
        """
        s = s_new
        print(np.max(np.abs(l1-l2)))
        return s
    return s