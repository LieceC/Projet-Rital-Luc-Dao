# -*- coding: utf-8 -*-
from utils.collection import Document, IndexerSimple, Query
import numpy as np
import utils.weighters as w
import utils.modeles as m
import utils.TextRepresenter as tr

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

if __name__ == "__main__":
    empty_word = {'the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on'}

    txt1 = "the new home has been saled on top forecasts"
    txt2 = "the home sales rise in july july"
    txt3 = "there is an increase in home sales in july"
    txt4 = "july encounter a new home sales rise"

    doc1 = Document(I = "0",W = txt1)
    doc2 = Document(I = "1",W = txt2)
    doc3 = Document(I = "2",W = txt3)
    doc4 = Document(I = "3",W = txt4)
    
    # construction de la collection
    col = dict()
    for x in [doc1,doc2,doc3,doc4]:
        col[x.identifiant] = x
        
    # indexation
    index = IndexerSimple(col,empty_word)
    
    # query
    q = Query("0","july july")
    query = pretraitement_requete(q.text)
    idf = index.getIDFsForStem("juli")
    tf = index.getTfsForStem("juli")
    
    # weighter
    normalized = False    
    
    # resultats
    print("indexation:")
    print(index.index)
    print()

    print("modele Vectoriel, Weighter1 : ")
    weighter = w.Weighter1(index)
    model_V = m.Vectoriel(index,weighter,normalized)
    print("result:",model_V.getScores(query))
    if normalized:
        print("document norme:",model_V.norme_doc)
        model_V = m.Vectoriel(index,weighter,False)
        V = model_V.getScores(query)
        norme_doc = dict()
        for x in V.keys():
            #print(model_V.doc_weight[x])
            norme_doc[x] = np.sqrt(np.sum(np.array(list(model_V.doc_weight[x].values()))**2))
        result = {x:y/(norme_doc[x] * 1) for x,y in V.items()}
        print("excepted result:",result)
        print("excepted document norme:",norme_doc)
    print()
    
    print("modele Vectoriel, Weighter2 : ")
    weighter = w.Weighter2(index)
    model_V = m.Vectoriel(index,weighter,normalized)
    print(model_V.getScores(query))
    print()
    
    print("modele Vectoriel, Weighter3 : ")
    weighter = w.Weighter3(index)
    model_V = m.Vectoriel(index,weighter,normalized)
    print("july idf :",idf)
    print(model_V.getScores(query))
    print()
    
    print("modele Vectoriel, Weighter4 (excepted - given): ")
    weighter = w.Weighter4(index)
    model_V = m.Vectoriel(index,weighter,normalized)

    res = model_V.getScores(query)
    for x in tf.keys():
        excepted = (1+np.log(tf[x]))*idf
        if normalized:
            excepted/=(model_V.norme_doc[x]*idf)
        print(excepted,"-",res[x])
    print()
    
    print("modele Vectoriel, Weighter5 (excepted - given): ")
    weighter = w.Weighter5(index)
    model_V = m.Vectoriel(index,weighter,normalized)

    res = model_V.getScores(query)
    for x in tf.keys():
        excepted = (1+np.log(tf[x]))*idf*(1+np.log(2))*idf
        if normalized:
            excepted/=(model_V.norme_doc[x]*(1+np.log(2))*idf)
        print(excepted,"-",res[x])
    print()
    
    print("modele Langue : ")
    model_L = m.ModeleLangue(index)
    excepted = dict()
    for x in index.col.keys():
        size = sum(index.getTfsForDoc(x).values())
        tot = index.nb_mots
        my_tf = tf.get(x,0)
        excepted[x] = np.log(
            (1-model_L._lambda)*(my_tf/size) + model_L._lambda*((sum(tf.values()) - my_tf)/(tot-size)))
        
    print("result:",model_L.getScores(query))
    print("excepted:",excepted)
    print()
    
    print("modele Okapi (excepted - given): ")
    k1 = 1.2
    b = 0.75
    model_O = m.Okapi(index,k1 = k1, b = b)
    res = model_O.getScores(query)
    avg = 0
    for x in res.keys():
        avg+=sum(index.getTfsForDoc(x).values())
    avg/=4
    for x in res.keys():
        if "juli" in index.getTfsForDoc(x).keys():
            size = sum(index.getTfsForDoc(x).values())
            print(idf*tf[x]
                  /(tf[x]+k1*(1-b+b*size/avg)),"-",res[x])
        else: print(0.,"-",res[x])
    print()
    