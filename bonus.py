#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 18:48:36 2021

@author: dao
"""

import sklearn.model_selection as ms
import test_modeles as t
start = 0
end = 1
step = 1
test_size = 0.2

# indices du  train et du test
train, test = ms.train_test_split(list(t.col1),test_size=test_size)

train_set = {id_doc:d for id_doc,d in t.col1.items() if id_doc in train}
test_set = {id_doc:d for id_doc,d in t.col1.items() if id_doc in test}