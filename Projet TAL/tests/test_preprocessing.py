from utils.utils import Loader 
from utils.preprocessing import Preprocessing
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.snowball import FrenchStemmer
"""
Pour la lemmatization il faut intaller le paquet :
python3 -m spacy download fr_core_news_md
"""
from time import time
import spacy
#lem = spacy.load("fr_core_news_sm")
lem = spacy.load('fr_core_news_md')
def lemmatization(word):    
    return lem(str(word))

stemmer = FrenchStemmer()


fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
train_x,train_y = Loader.load_pres(fname)

fname = "Data/AFDpresidentutf8/corpus.tache1.test.utf8"
test_x, test_y = Loader.load_pres(fname)


stop = list(stopwords.words('french')) + ['cet', 'cette']
params = {
    "lowercase":True,
    "punct":True,
    "marker":True,
    "number":True,
    "stemming": lem, #stemmer.stem,
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