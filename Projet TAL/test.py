import numpy as np
import matplotlib.pyplot as plt

import codecs
import re
import os.path

from utils import Loader

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = Loader.load_pres(fname)

fname = "Data/AFDpresidentutf8/corpus.tache1.test.utf8"
alltxts_test,alllabs_test = Loader.load_pres(fname)

print(len(alltxts),len(alllabs))
print(alltxts[0])
print(alllabs[0])
print(alltxts[-1])
print(alllabs[-1])

path = "Data/AFDmovies/movies1000/"
alltxts,alllabs = Loader.load_movies(path)