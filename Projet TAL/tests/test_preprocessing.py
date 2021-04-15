from utils.utils import Loader 
from utils.preprocessing import Preprocessing
from nltk.corpus import stopwords
from time import time
"""
Pour la lemmatization il faut intaller le paquet :
python3 -m spacy download fr_core_news_md
"""
fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
train_x,train_y = Loader.load_pres(fname)

fname = "Data/AFDpresidentutf8/corpus.tache1.test.utf8"
test_x, test_y = Loader.load_pres(fname)


stop = list(stopwords.words('french')) + ['cet', 'cette', 'là']
params = {
    "lowercase":True,
    "punct":True,
    "marker":True,
    "number":True,
    "stemming": Preprocessing.stem, #lem,
    "ligne": None,
    "strip_accents":True,
    "stopwords": set(stop)
}
i = 10000
t = time()
for i in range(100, 101):
    print("original : {}\nresult : {}\n".format(test_x[i],Preprocessing.preprocessing(test_x[i],params)))
print(time()-t)
c = 'Salut, HECTOR j espere que tu vas bien moi aussi'
#print("original :\n{}\n\nresult :\n{}".format(c, Preprocessing.preprocessing(c,params)))