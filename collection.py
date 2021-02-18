# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:43:53 2021

@author: Luc
"""
import re
import utils.TextRepresenter as tr
import math
import numpy as np

empty_word = ['the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on']


class Document:
    def __init__(self, I, T = None, A = None, B = None, K = None, W = None, X = None):
        self.identifiant = I
        self.titre = T
        self.date_publication = B
        self.auteur = A
        self.mots_clé = K
        self.text = W
        self.liens = X
        
class Query:
    def __init__(self, i, T, L, LS):
        self.id = i
        self.text = T
        self.pertinents = L
        self.pertinents_score = LS

class QueryParser:
    def parse(f_qry, f_rel):
        d_qry = dict()
        res = Parser.res(f_qry)
        for i in res:
            d_qry[i[0]] = Query(i[0],i[15], [], [])
        
        if f_rel:
            text = open(f_rel, "r").read()
            res = re.findall("\s*([^\s]*)\s*([^\s]*)\s*([^\s]*)\s([^\s]*)\n",\
                             text,re.MULTILINE)
            for i in res :
                d_qry[i[0]].pertinents.append(i[1])
                d_qry[i[0]].pertinents_score.append(1)
                
        return d_qry

class Parser:
    def res(file):
        """
        Parse la collection stockée sous la forme 
        d’un dictionnaire de Documents
        """
        text = open(file, "r").read()
        I = r"\.I (.*)\n"
        T = r"(\.T\s*(([^.].*\n+)*))?"
        B = r"(\.B\s*(([^.].*\n+)*))?"
        A = r"((\.A\s*(([^.].*\n+)*))*)"
        K = r"(\.K\s*(([^.].*\n+)*))?"
        W = r"(\.W\s*(([^.].*\n+)*))?"
        X = r"(\.X\s*(([^.].*\n+)*))?"
        return re.findall(I+T+A+B+K+W+X,text,re.MULTILINE)
        
    def parse(file):
        dico = dict()
        res = Parser.res(file)
        for i in res:
            dico[i[0]] = Document(i[0],i[2],i[4],i[9],i[12],i[15],i[18])
        return dico
    

    
class IndexerSimple:
    
    
    def __init__(self, col):
        self.col = col
        self.index, self.index_inv = self.indexation(col)
        
    def getIds(self):
        return self.col.keys()
    
    def getDocSize(self,doc_id):
        return sum(self.index[doc_id].values())
    
    def getMeanDocSize(self):
        ids = self.getIds()
        mean = 0
        for id_doc in ids:
            mean+=self.getDocSize(id_doc)
        return mean/len(ids)
    
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
        self.nb_mots = 0
    
        for id_d,doc in col.items():
            c = ps.getTextRepresentation(doc.text)
            index[id_d] = c
            
            for name, number in c.items():
                try:    
                    index_invers[name][id_d] = number
                except KeyError:
                    index_invers[name] = {id_d : number}
                self.nb_mots += number

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
        Rend un dictionnaire des documents contenant le terme et combien
        de fois il apparait
        """
        try:
            return self.index_inv[terme]
        except KeyError: # le mot n'apparait pas
            return dict()
    
    def getIDFsForStem(self, terme):
        """
        Renvoie l'IDF du terme
        """
        try:
            return math.log(1+len(self.index))-\
                                math.log(1+len(self.index_inv[terme]))
        except KeyError: # le mot n'apparait pas
            return math.log(1+len(self.index))-\
                                math.log(1)
        
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
    


