# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:39:54 2021

@author: Luc
"""
from collection import Parser,IndexerSimple

col1 = Parser.parse('./data/cacmShort-good.txt')


d1 = "the new home has been saled on top forecasts"
d2 = "the home sales rise in july"
d3 = "there is an increase in home sales in july"
d4 = "july encounter a new home sales rise"

empty_word = ['the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on']


collection = [d1, d2, d3, d4]

def ciseaux(d):
    a = str.lower(d)
    a = np.array(a.split())
    select = list(map(lambda x : x not in empty_word, a))
    a = list(map(lambda x : p.stem(x), a[select]))
    a = dict(Counter(a))
    return a

def indexation(collection):
    index = {}
    index_invers = {}
    
    for doc,value in enumerate(collection):
        c = ciseaux(value)
        index[doc] = c
        
        for name, number in c.items():
            try:
                index_invers[name][doc] = number
            except KeyError:
                index_invers[name] = {doc : number}
    
    return index, index_invers


R1 = 'top sales'
R2 = 'sales increase july'
R3 = 'new home'