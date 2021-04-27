# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 19:43:53 2021

@author: Luc
"""
import re
import utils.TextRepresenter as tr
import math

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
    def __init__(self, i, T):
        self.id = i
        self.text = T
        self.pertinents = []
        self.pertinents_score = dict()

class QueryParser:
    def parse(f_qry, f_rel):
        d_qry = dict()
        res = Parser.res(f_qry)
        for i in res:
            d_qry[i[0]] = Query(i[0],i[10])

        if f_rel:
            text = open(f_rel, "r").read()
            res = re.findall("\s*([^\s]*)\s*([^\s]*)\s*([^\s]*)\s([^\s]*)\n",\
                             text,re.MULTILINE)
            for i in res :
                qry = d_qry[i[0]]
                qry.pertinents.append(i[1])
                qry.pertinents_score[i[1]] = 1
        return d_qry

class Parser:
    def res(file):
        """
        Parse la collection stockée sous la forme 
        d’un dictionnaire de Documents
        """
        text = open(file, "r").read()
        I = r"^\.I (.*)\n"
        T = r"^(\.T\s*(([^.].*\n+)*))?"
        AB = r"^((\.(A|B)\s*(([^.].*\n+)*))*)"
        W = r"^(\.W\s*(([^.].*\n+)*))?"
        K = r"^(\.K\s*(([^.].*\n+)*))?"
       
        N = r"^(\.N\s*(([^.].*\n+)*))?"
        X = r"^(\.X\s*(([^.].*\n+)*))?"
        return re.findall(I+T+AB+W+K+N+X,text,re.MULTILINE)
        
    def parse(file):
        dico = dict()
        res = Parser.res(file)
        for i in res:
            
            B = re.search(r"^(\.B\s*(([^.].*\n+)*))",i[4],re.MULTILINE)
            B = "" if B == None else B.group(2)
            A = re.search(r"^((\.A\s*(([^.].*\n+)*))+)",i[4],re.MULTILINE)
            A = "" if A == None else A.group(1)[3:]
            dico[i[0]] = Document(i[0],i[2],A,B,i[13],i[10],i[19])
        return dico
    

    
class IndexerSimple:
    
    
    def __init__(self, col, stopwords = None):
        """
        ajout d'une liste de stopwords, 
        si celui-ci n'est pas donnée, celui du TextRepresenter est utilisé

        """
        self.col = col
        self.stopwords = stopwords
        self.index, self.index_inv = self.indexation(col)
        self.index_ht, self.index_inv_ht = self.indexation_hyper_text(col)

        
    def getIds(self):
        return self.col.keys()
    
    def getDocSize(self,doc_id):
        '''
        Récupère la taille du document d'id doc_id

        '''
        return sum(self.index[doc_id].values())
    
    def getMeanDocSize(self):
        '''
        Récupère la moyenne des tailles de la collection

        '''
        ids = self.getIds()
        mean = sum([self.getDocSize(id_doc) for id_doc in ids])
        return mean/len(ids)
    
    def indexation(self,col):
        """
        Créer deux dictionnaires à partir d'une collection. 
        Le premier a comme clef les documents et comme valeurs les mots
        contenu dedans ainsi que leur nombre.
        Le second a les mots en clef et les documents et leurs nombres en
        arguments.
        """
        def index_doc(self,document, ps, index, index_inv):
            '''
                Indexation d'un document
            '''
            def index_doc_mot(self,id_d, item, index_invers):
                '''
                    Indexation d'un mot du document id_d dans l'index inverse
                '''
                name = item[0] # le mot 
                number = item[1] # le nb fois ou il apparait dans le document
                try:    
                    index_invers[name][id_d] = number
                except KeyError:
                    index_invers[name] = {id_d : number}
                self.nb_mots += number
                
            id_d = document[0]
            doc = document[1]
            
            c = ps.getTextRepresentation(doc.text)
            index[id_d] = c            
            [index_doc_mot(self,id_d, item, index_invers) for item in c.items()]
                
        
        ps = tr.PorterStemmer(self.stopwords)
        index = {}
        index_invers = {}
        self.nb_mots = 0
    
        [index_doc(self,x,ps,index,index_invers) for x in col.items()]
        return index, index_invers

    def indexation_hyper_text(self,col):
        def indexation_hyper_text_doc(self,document, index_invers, index):
            '''
                Indexation des liens hyper text d'un document
            '''
            def indexation_hyper_text_lien(self, l, id_d, index_invers, index):
                '''
                    Indexation d'un lien d'un document
                '''
                l = l.split('\t')
                if l[0] == '': return
            
                try:
                    index[id_d][l[0]] += 1
                except KeyError:
                    index[id_d][l[0]] = 1
                
                try:
                    index_invers[l[0]][id_d] += 1 
                except KeyError:
                    try : 
                        index_invers[l[0]][id_d] = 1
                    except:
                        index_invers[l[0]] = dict()
                        index_invers[l[0]][id_d] = 1
            id_d = document[0]
            doc = document[1]
            index[id_d] = dict()
            if doc.liens is not None:
                links = doc.liens.split('\n')
                [indexation_hyper_text_lien(self, l, id_d, index_invers, index) for l in links]
                
        index = {}
        index_invers = {}
        [indexation_hyper_text_doc(self,document, index_invers, index) for document in col.items()]
                    
                    
        return index, index_invers
                
    def getHyperlinksTo(self,id_d):
        return self.index_inv_ht[id_d]
    
    def getHyperlinksFrom(self,id_d):
        return self.index_ht[id_d]
    
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
        def getTfIDFsForDoc_word(self, id_d, word, index_d):
            """
               Ajout d'un mot du document
            """
            try:
                index_d[word] = self.index[str(id_d)][word]*\
                                (math.log(1+len(self.index))-\
                                 math.log(1+len(self.index_inv[word])))
            except KeyError:
                return
        index_d = dict()
        [getTfIDFsForDoc_word(self, id_d, word, index_d) for word in self.index_inv.keys()]            
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
        def getTfIDFsForStem_doc(self,terme,i,index_inv_t):
            """
            TF-IDF du terme pour un document
            """
            try:
                index_inv_t[i] = self.index[i][terme]*\
                                 (math.log(1+len(self.index))-\
                                  math.log(1+len(self.index_inv[terme])))
                
            except KeyError:
                return
        index_inv_t = dict()
        [getTfIDFsForStem_doc(self,terme,i,index_inv_t) for i in self.index.keys()]
           
        return index_inv_t
    
    def getStrDoc(self, id_d):
        """
        Rend le text du doc id_d
        """
        return self.col[str(id_d)].text
    


