#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:56:40 2021

@author: dao
"""

import numpy as np

class EvalMesure:
    def evalQuery(liste,query):
        pass

class Précision(EvalMesure):
    def evalQuery(liste,query,k):
        return np.sum(np.isin(liste[:k],query.pertinents))/k
    
    def allEvalQuery(liste,query):
        return np.cumsum(np.where(np.isin(liste,query.pertinents),1,0))/\
            range(1,len(liste)+1)
    
class Rappel(EvalMesure):
    def evalQuery(liste,query,k):
        if len(query.pertinents) == 0: return 1
        return np.sum(np.isin(liste[:k],query.pertinents))/\
            len(query.pertinents)
            
    def allEvalQuery(liste,query):
        if len(query.pertinents) == 0: return [1]*len(liste)
        return np.cumsum(np.where(np.isin(liste,query.pertinents),1,0))/\
            len(query.pertinents)
    
class F_mesure(EvalMesure):
    def evalQuery(liste,query,k,beta=0.5):
        p = Précision.evalQuery(liste,query,k)
        r = Rappel.evalQuery(liste,query,k)
        return (1+beta**2)*(p*r)/((beta**2)*p+r)
    
    def allEvalQuery(liste,query,beta=0.5):
        p = Précision.allEvalQuery(liste,query)
        r = Rappel.allEvalQuery(liste,query)
        return (1+beta**2)*(p*r)/((beta**2)*p+r)
    
    
class Précision_moyenne:
    def evalQuery(liste,query):
        R = np.where(np.isin(liste,query.pertinents),1,0)
        P = Précision.allEvalQuery(liste, query)
        try: #Si query.pertinents vaut 0
            return (1/len(query.pertinents))*np.sum(R*P)
        except:
            return 1
        
class reciprocal_rank(EvalMesure):
    def evalQuery(liste, querie):
        """
            querie est une liste de requêtes   
            liste est une liste de ranking de document pour chaque requêtes
        """
        r = 0
        for l in liste:
            for q in querie:
                r += np.where(np.isin(l.identifiant, q.pertinents))[0][0] +1
        
        return (1/len(querie))*(1/r)
    
class NDCG(EvalMesure):
    def evalQuery(liste, querie):
        """
            querie est une requêtes avec des documents pertinents 
            liste est un ranking des documents pour la requête par un modèle
        """
        r = np.where(np.isin(liste.identifiant, querie.pertinents),1,0)
        DCG =  r[0] + np.sum(r[1:] / np.log2(np.range(2,len(r)+1)))
        
        i = np.ones(len(querie.pertinents))
        IDCG = i[0] + np.sum(r[1:] / np.log2(np.range(2,len(i)+1)))
        return DCG/IDCG