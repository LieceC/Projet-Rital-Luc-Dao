# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

from collection import Parser,IndexerSimple

################
## EXERCICE 1 ##
################


col1 = Parser.parse('./data/cacm/cacm.qry')


############################################################

indexer = IndexerSimple(col1)
print("getTfIDTS for Stem :\n",indexer.getTfIDFsForStem("test"))
print("\n\ngetTf for Stem :\n",indexer.getTfsForStem("test"))
print("\n\ngetStrDoc :\n",indexer.getStrDoc(58))
print("\n\ngetTf for Doc :\n",indexer.getTfsForDoc(58))
print("\n\ngetTfIDS for doc :\n",indexer.getTfIDFsForDoc(58))



############################################################
"""
def text_list(phrase,col):
    IS = IndexerSimple(col)
    index, index_inv = IS.indexation()
    ps = tr.PorterStemmer()
    liste = ps.getTextRepresentation(phrase)
    res = dict()
    for mot in liste.keys():
        docs = IS.getTfIDFsForStem(index,index_inv,mot)
        for doc,tf_idf in docs.items():
            try:
                res[doc]+=tf_idf
            except KeyError:
                res[doc]=tf_idf
    res = [k for k, v in sorted(res.items(), key=lambda item: item[1])]
    res.reverse()
    return res

col2 = Parser("data/cisi/cisi.qry").parse()
indexer = IndexerSimple(col2)
liste = text_list("complex theory",col2)
for doc in liste:
    print(doc)
    print(indexer.getStrDoc(doc))
        
"""  