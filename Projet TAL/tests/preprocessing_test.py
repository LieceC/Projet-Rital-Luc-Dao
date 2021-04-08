from utils.preprocessing import Preprocessing
from wordcloud import STOPWORDS
from utils.utils import Loader 

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = Loader.load_pres(fname)


fname = "Data/AFDpresidentutf8/corpus.tache1.test.utf8"
alltxts_test,alllabs_test = Loader.load_pres(fname)

params = {
    "lowercase":False,
    "punct":False,
    "marker":False,
    "number":False,
    "stemming":False,
    "ligne": None,
    "strip_accents":False,
    "stopwords": set(STOPWORDS)
}
print("original :")
print(alltxts[0])
print("result :")
print(Preprocessing.preprocessing(alltxts[0],params))