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

class Précision:
    def evalQuery(liste,query):
        return np.cumsum(np.where(liste.identifiant in query.pertinents,1,0))/\
            np.range(1,len(liste)+1)
    
class Rappel:
    def evalQuery(liste,query):
        return np.cumsum(np.where(liste.identifiant in query.pertinents,1,0))/\
            len(query.pertinents)
    
class F_mesure:
    def evalQuery(liste,query):
        pass