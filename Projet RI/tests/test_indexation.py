# -*- coding: utf-8 -*-
from utils.collection import Document, IndexerSimple
import numpy as np

if __name__ == "__main__":
    empty_word = {'the', 'a', 'an', 'on', 'behind', 'under', 'there', 'in', 'on'}

    txt1 = "the new home has been saled on top forecasts"
    txt2 = "the home sales rise in july"
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
    indexation = IndexerSimple(col,empty_word)
    
    # resultats
    print("indexation:")
    print(indexation.index)
    print()
    
    print("indexation inversé:")
    print(indexation.index_inv)
    print()
    
    print("indexation TF-IDF (triplet tf_idf_stem, tf_idf_doc, tf_term*idf_term):")
    for i,x in enumerate(np.unique(list(indexation.index_inv.keys()))):
        print("--- mot",x,"---")
        my_tf_idf = indexation.getTfIDFsForStem(x)
        my_idf = indexation.getIDFsForStem(x)
        my_tf = indexation.getTfsForStem(x)
        for j,v in my_tf_idf.items():
            document_tf_idf = indexation.getTfIDFsForDoc(j)
            print("doc",j,":")
            print(v,"-",document_tf_idf[x],"-",my_idf*my_tf[j])
    print()
    
    print("indexation TF (doublet tf_term, tf_doc):")
    for i,x in enumerate(np.unique(list(indexation.index_inv.keys()))):
        print("--- mot",x,"---")
        my_tf = indexation.getTfsForStem(x)
        for j,v in my_tf.items():
            document_tf = indexation.getTfsForDoc(j)
            print("doc",j,":")
            print(v,"-",document_tf[x])
    print()
    
    print("getStrDoc:")
    print("doc 0:",indexation.getStrDoc("0"))
