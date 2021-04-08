# -*- coding: utf-8 -*-
import numpy as np
class Equilibrage:
    def remove_prioritaire_2(datay,marge = 0):
    
        '''
            renvoies les indices des données à garder
        '''
        res = np.arange(0,len(datay))
        datay = np.array(datay)
        v,nb = np.unique(datay,return_counts=True)
        
        diff = np.abs(nb[0]-nb[1]) - marge
    
        if diff <= 0: return res
        if nb[0] > nb[1]:
            
            indices = np.where(datay==v[0])[0]
        else:
            indices = np.where(datay==v[1])[0]
        to_remove = np.random.choice(indices,diff,replace=False)
        
        res = np.delete(res,to_remove)
        return res

    def remove_prioritaire(datax,datay,marge = 0):
        '''
            renvoies datax et datay équilibrés
        '''
        datax = np.array(datax)
        datay = np.array(datay)
        v,nb = np.unique(datay,return_counts=True)
        
        diff = np.abs(nb[0]-nb[1]) - marge
    
        if diff <= 0: return datax,datay
        if nb[0] > nb[1]:
            
            indices = np.where(datay==v[0])[0]
        else:
            indices = np.where(datay==v[1])[0]
        to_remove = np.random.choice(indices,diff,replace=False)
        print(to_remove)
        print(datax.shape)
        datax = np.delete(datax,to_remove)
        datay = np.delete(datay,to_remove)
        return datax,datay
