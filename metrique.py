#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:56:40 2021

@author: dao
"""
import utils.TextRepresenter as tr
import numpy as np

class EvalMesure:
    def evalQuery(liste, query, args):
        pass


class EvalIRModel:    
    def eval(mesure, model, col_q, args = None):
        def pretraitement_requete(q):
            ps = tr.PorterStemmer()
            return ps.getTextRepresentation(q)
        
        res = []
        for i,query in col_q.items():
            q = pretraitement_requete(query.text)
            ranking = model.getRanking(q)
            res += [model.evalQuery(ranking,query,args)]
            
        return np.mean(res), np.std(res)

class Précision(EvalMesure):
    def evalQuery(liste, query, args = [5]):
        return np.sum(np.isin(liste[:args[0]],query.pertinents))/args[0]
    
    def allEvalQuery(liste,query):
        return np.cumsum(np.where(np.isin(liste,query.pertinents),1,0))/\
            range(1,len(liste)+1)
    
class Rappel(EvalMesure):
    def evalQuery(liste, query, args = [5]):
        if len(query.pertinents) == 0: return 1
        return np.sum(np.isin(liste[:args[0]],query.pertinents))/\
            len(query.pertinents)
            
    def allEvalQuery(liste,query):
        if len(query.pertinents) == 0: return [1]*len(liste)
        return np.cumsum(np.where(np.isin(liste,query.pertinents),1,0))/\
            len(query.pertinents)
    
class F_mesure(EvalMesure):
    def evalQuery(liste,query,args = [4, 0.5]):
        p = Précision.evalQuery(liste,query,args[0])
        r = Rappel.evalQuery(liste,query,args[0])
        return (1+args[1]**2)*(p*r)/((args[1]**2)*p+r)
    
    def allEvalQuery(liste,query,beta=0.5):
        p = Précision.allEvalQuery(liste,query)
        r = Rappel.allEvalQuery(liste,query)
        return (1+beta**2)*(p*r)/((beta**2)*p+r)
    
    
class Précision_moyenne(EvalMesure):
    def evalQuery(liste,query, args = None):
        R = np.where(np.isin(liste,query.pertinents),1,0)
        P = Précision.allEvalQuery(liste, query)
        try: #Si query.pertinents vaut 0
            return (1/len(query.pertinents))*np.sum(R*P)
        except:
            return 1
        
class reciprocal_rank(EvalMesure):
    def evalQuery(liste, query, args = None):
        """
            querie est une liste de requêtes   
            liste est une liste de ranking de document pour chaque requêtes
        """
        return 1/(np.where(np.isin(liste.identifiant, query.pertinents))[0][0] +1)
    
class NDCG(EvalMesure):
    def evalQuery(liste, query, args = None):
        """
            querie est une requêtes avec des documents pertinents 
            liste est un ranking des documents pour la requête par un modèle
        """
        r = np.where(np.isin(liste.identifiant, query.pertinents),1,0)
        DCG =  r[0] + np.sum(r[1:] / np.log2(np.range(2,len(r)+1)))
        
        i = np.ones(len(query.pertinents))
        IDCG = i[0] + np.sum(r[1:] / np.log2(np.range(2,len(i)+1)))
        return DCG/IDCG
    
class Précision_interpolée(EvalMesure):
    def evalQuery(liste,query,args=None):
        p = np.array(Précision.allEvalQuery(liste,query))

        r = np.array(Rappel.allEvalQuery(liste,query))
        pts,ids = np.unique(p,return_index=True)
        values = []
        for i in ids:
            v = p[i]
            values+=[np.max(r[np.where(p>=v)[0]])]
        return pts,values