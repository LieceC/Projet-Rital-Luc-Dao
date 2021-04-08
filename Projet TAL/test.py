import numpy as np
import matplotlib.pyplot as plt

import codecs
import re
import os.path

from utils import load_pres, load_movies

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = load_pres(fname)

fname = "Data/AFDpresidentutf8/corpus.tache1.test.utf8"
alltxts_test,alllabs_test = load_pres(fname)

print(len(alltxts),len(alllabs))
print(alltxts[0])
print(alllabs[0])
print(alltxts[-1])
print(alllabs[-1])

path = "Data/AFDmovies/movies1000/"
alltxts,alllabs = load_movies(path)