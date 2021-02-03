# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:43:53 2021

@author: Luc
"""
import re
import utils.TextRepresenter as tr
import math

empty_word = ['the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on']


class Document:
    def __init__(self, I, T = None, B = None, A = None, K = None, W = None, X = None):
        self.identifiant = I
        self.titre = T
        self.date_publication = B
        self.auteur = A
        self.mots_clé = K
        self.text = W
        self.liens = X
        

class Parser:
    def parse(file):
        """
        Parse la collection stockée sous la forme 
        d’un dictionnaire de Documents
        """
        text = open(file, "r").read()
        dico = dict()
        res = re.findall(r"\.I (.*)\n(.T\n(([^.].*\n)*))?(.B\n(([^.].*\n)*))?(.A\n(([^.].*\n)*))?(.K\n(([^.].*\n)*))?(.W\n(([^.].*\n)*))?(.X\n(([^.].*\n)*))?",text,re.MULTILINE)
        for i in res:
            dico[i[0]] = Document(i[0],i[2],i[5],i[8],i[11],i[14],i[17])
        return dico
        
    
class IndexerSimple:
    
    
    def __init__(self, col):
        self.col = col
        self.index, self.index_inv = self.indexation(col)
        
    
    def indexation(self,col):
        """
        Créer deux dictionnaires à partir d'une collection. 
        Le premier a comme clef les documents et comme valeurs les mots
        contenu dedans ainsi que leur nombre.
        Le second a les mots en clef et les documents et leurs nombres en
        arguments.
        """
        ps = tr.PorterStemmer()
        index = {}
        index_invers = {}
    
        for id_d,doc in col.items():
            c = ps.getTextRepresentation(doc.text)
            index[id_d] = c
            
            for name, number in c.items():
                try:    
                    index_invers[name][id_d] = number
                except KeyError:
                    index_invers[name] = {id_d : number}

        return index, index_invers
    
    def getTfsForDoc(self, id_d):
        """
        Retourne les mots contenu dans le document id_d
        """
        return self.index[str(id_d)]
    
    def getTfIDFsForDoc(self, id_d):
        """
        Rend un dictionnaire avec les mots du document id_d et leur
        score tf-idf
        """
        index_d = dict()
        for word,enum in self.index_inv.items():
            try:
                index_d[word] = self.index[str(id_d)][word]*\
                                (math.log(1+len(self.index))-\
                                 math.log(1+len(self.index_inv[word])))
            except KeyError:
                continue
        return index_d
    
    def getTfsForStem(self, terme):
        """
        Rend un dictionnaire des documents contenant le terme et combient
        de fois
        """
        return self.index_inv[terme]
    
    def getTfIDFsForStem(self, terme):
        """
        Rend un dictionnaire des documents contenant le terme et son score
        TF-IDF
        """
        index_inv_t = dict()
        for i,file in self.index.items():
            try:
                index_inv_t[i] = self.index[i][terme]*\
                                 (math.log(1+len(self.index))-\
                                  math.log(1+len(self.index_inv[terme])))
            except KeyError:
                continue
        return index_inv_t
    
    def getStrDoc(self, id_d):
        """
        Rend le text du doc id_d
        """
        return self.col[str(id_d)].text


