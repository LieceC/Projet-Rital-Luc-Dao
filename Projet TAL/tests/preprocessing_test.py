from utils.utils import Loader 
from utils.preprocessing import Preprocessing
from wordcloud import STOPWORDS

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = Loader.load_pres(fname)

fname = "Data/AFDpresidentutf8/corpus.tache1.test.utf8"
alltxts_test,alllabs_test = Loader.load_pres(fname)

params = {
    "lowercase":False,
    "punct":True,
    "marker":True,
    "number":False,
    "stemming":True,
    "ligne": None,
    "strip_accents":False,
    "stopwords": set(STOPWORDS)
}

print("original :")
print(alltxts[0])
print("result :")
print(Preprocessing.preprocessing(alltxts[0],params))

c = 'Salut, HECTOR j espere que tu vas bien moi aussi'

print("original :")
print(c)
print("result :")
print(Preprocessing.preprocessing(c,params))