#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:56:40 2021

@author: dao
"""

import utils.TextRepresenter as tr
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


class EvalMesure:
    def evalQuery(liste, query, args):
        pass


class EvalIRModel:    
    def eval_query(mesure,model,query,ps,args = None):
        q = ps.getTextRepresentation(query.text)
        ranking = np.array(model.getRanking(q))
        m = mesure.evalQuery(ranking,query,args)
        return m
        
    def eval(mesure, model, col_q, args = None):
        ps = tr.PorterStemmer()
        res = list(map(lambda query: EvalIRModel.eval_query(mesure,model,query,ps,args),col_q.values()))
        return np.mean(res), np.std(res)
    
    def precision_interpolée_graph(model,col_q):
        def pretraitement_requete(q):
            ps = tr.PorterStemmer()
            return ps.getTextRepresentation(q)

        for i,query in col_q.items():
            q = pretraitement_requete(query.text)
            ranking = model.getRanking(q)
            x,y = Précision_interpolée.evalQuery(ranking,query)

            plt.figure()
            plt.title("Precision Interpolée pour la requête "+query.id)
            plt.plot(x,y)
            
    def significativité(p_value, mesure, model, model_test, col_q, args1, args2):
        m, std = EvalIRModel.eval(mesure, model, col_q, args1)
        m_test, std_test = EvalIRModel.eval(mesure, model_test, col_q, args2)

        alpha = norm.ppf(p_value)
        alpha = alpha*(std / np.sqrt(len(col_q)))
        
        if m_test >  std + alpha or m_test <  std - alpha:
            return False
        return True
        

class Précision(EvalMesure):
    def evalQuery(liste, query, args = [5]):
        '''
            Compute the Précision at rank k
            args[0] : k
        '''
        return np.sum(np.isin(liste[:args[0]],query.pertinents))/args[0]
    
    def allEvalQuery(liste,query, args = None):
        '''
            Compute for all k the Query
        '''
        return np.cumsum(np.where(np.isin(liste,query.pertinents),1,0))/\
            range(1,len(liste)+1)
    
class Rappel(EvalMesure):
    def evalQuery(liste, query, args = [5]):
        '''
            Compute the Rappel at rank k
            args[0] : k
        '''
        if len(query.pertinents) == 0: return 1
        return np.sum(np.isin(liste[:args[0]],query.pertinents))/\
            len(query.pertinents)
            
    def allEvalQuery(liste,query,args = None):
        '''
            Compute for all k the Rappel
        '''
        if len(query.pertinents) == 0: return [1]*len(liste)
        return np.cumsum(np.where(np.isin(liste,query.pertinents),1,0))/\
            len(query.pertinents)
    
class F_mesure(EvalMesure):
    def evalQuery(liste,query,args = [4, 0.5]):
        '''
            Compute the F_mesure at rank k
            args[0] : k
            args[1] : beta
        '''
        p = Précision.evalQuery(liste,query,[args[0]])
        r = Rappel.evalQuery(liste,query,[args[0]])
        if ((args[1]**2)*p+r) == 0: return 0
        return (1+args[1]**2)*(p*r)/((args[1]**2)*p+r)
    
    def allEvalQuery(liste,query,args = [0.5]):
        '''
            Compute for all k the F_mesure
            args[0] : beta
        '''
        p = Précision.allEvalQuery(liste,query)
        r = Rappel.allEvalQuery(liste,query)
        return (1+args[0]**2)*(p*r)/((args[0]**2)*p+r)
    
    
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
            query est une requête 
            liste est une liste de ranking de document pour chaque requêtes
        """
        ens = np.where(np.isin(liste, query.pertinents))[0]
        if len(ens) == 0: return 0
        return 1/(ens[0] +1)
    
class NDCG(EvalMesure):
    def __tryvalue(x,l):
        try:
            return l[x]
        except KeyError:
            return 0
        
    def evalQuery(liste, query, args = None):
        """
            query est une requêtes avec des documents pertinents 
            liste est un ranking des documents pour la requête par un modèle
        """
        if len(query.pertinents) == 0: return 1
       
        r = np.array(list(
                map(lambda x: NDCG.__tryvalue(x,query.pertinents_score),liste)
                ))
        #r = np.where(np.isin(liste, query.pertinents),1,0)
        DCG =  r[0] + np.sum(r[1:] / np.log2(np.arange(2,len(r)+1)))
        
        i = np.ones(len(query.pertinents))
        
        IDCG = i[0] + np.sum(i[1:] / np.log2(np.arange(2,len(i)+1)))
        return DCG/IDCG
    
class Précision_interpolée(EvalMesure):
    def evalQuery(liste,query,args = None):
        p = np.array(Précision.allEvalQuery(liste,query))

        r = np.array(Rappel.allEvalQuery(liste,query))
        pts,ids = np.unique(p,return_index=True)
        values = []
        for i in ids:
            v = p[i]
            values+=[np.max(r[np.where(p>=v)[0]])]
        return pts,values