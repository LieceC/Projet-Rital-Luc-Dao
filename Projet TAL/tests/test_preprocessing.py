from utils.utils import Loader 
from utils.preprocessing import Preprocessing
from nltk.corpus import stopwords
stop = list(stopwords.words('french'))

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
train_x,train_y = Loader.load_pres(fname)

fname = "Data/AFDpresidentutf8/corpus.tache1.test.utf8"
test_x, test_y = Loader.load_pres(fname)

params = {
    "lowercase":True,
    "punct":True,
    "marker":True,
    "number":True,
    "stemming":False,
    "ligne": None,
    "strip_accents":True,
    "stopwords": set(stop)
}

print("original :")
print(test_x[0])
print("result :")
print(Preprocessing.preprocessing(test_x[0],params))



"""
c = 'Salut, HECTOR j espere que tu vas bien moi aussi'

print("original :")
print(c)
print("result :")
print(Preprocessing.preprocessing(c,params))

"""