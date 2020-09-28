#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 7/20/2020 22:13
# @Author  : Haoyu Lyu
# @File    : test.py
# @Software: PyCharm


import networkx as nx
import numpy as np
from scipy import sparse
import numpy as np
import scipy.sparse as sp
def sparse_to_tuple(sparse_mx):
    if not sp.isspmatrix_coo(sparse_mx):
        sparse_mx = sparse_mx.tocoo()
    coords = np.vstack((sparse_mx.row, sparse_mx.col)).transpose()
    values = sparse_mx.data
    shape = sparse_mx.shape
    return coords, values, shape

g = {1:[2,9],2:[3],3:[1],5:[9],9:[2]}
# GG= nx.from_dict_of_lists(g)
# print("directed graph:\n", GG.edges())
# adj = nx.adjacency_matrix(GG)
# print("method: adjacency_matrix\n", adj)
a = ["1","2","-7"]
y = sorted(a)
print(ys)