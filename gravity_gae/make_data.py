#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 6/28/2020 19:33
# @Author  : Haoyu Lyu
# @File    : make_data.py
# @Software: PyCharm

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 5/14/2020 14:33
# @Author  : Haoyu Lyu
# @File    : generate_graph.py
# @Software: PyCharm
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm

import numpy as np
import csv
import re
import ast
import random
import copy

from scipy.sparse import csr_matrix
from scipy import sparse
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
id_pos = 0
num_conn_pos = 2
conned_nodes_pos = 3
can_be_extend_pos = 4
extend_type_pos = 5
who_conn_this = 6




def add_new_valve(g, c_p0, c_p1):
    try:
        new_id = max([r[0] for r in g]) + 1
        g.append([new_id, 5, 2, [c_p0, c_p1], [], []])
        g[c_p0][conned_nodes_pos][g[c_p0][conned_nodes_pos].index(c_p1)] = new_id
        del g[c_p0][extend_type_pos][g[c_p0][can_be_extend_pos].index(c_p1)]
        g[c_p0][can_be_extend_pos].remove(c_p1)
        g[c_p1][conned_nodes_pos][g[c_p1][conned_nodes_pos].index(c_p0)] = new_id
        del g[c_p1][extend_type_pos][g[c_p1][can_be_extend_pos].index(c_p0)]
        g[c_p1][can_be_extend_pos].remove(c_p0)
    except Exception as inst:
        print(g)
        print(c_p0, " ", c_p1)
        print(inst)
    return g


# 添加新的节点
def add_new_node(g, li):
    try:
        id_start = max([r[0] for r in g]) + 1
        new_ids = [id_start+i for i in range(len(li))]
        ind_to_id = {i:g[i][0] for i in range(len(g))}
        id_to_ind = {g[i][0]:i for i in range(len(g))}
        # print('new_ids:{}'.format(new_ids))
        # 删除之前链接的边
        # 加入新的链接
        rows = [copy.deepcopy(g[id_to_ind[i]]) for i in li]
        # 新旧节点对应关系
        id_dic = {li[i]:new_ids[i] for i in range(len(li))}
        # 它指向谁
        for r in rows:
            # print('r in rows:{}'.format(r))
            r[0] = id_dic[r[0]]
            r[conned_nodes_pos] = [id_dic.get(i,i) for i in r[conned_nodes_pos]]
            r[who_conn_this] = [id_dic.get(i,i) for i in r[who_conn_this]]
            # print('r in rows:{}'.format(r))
        # print('rows : {}'.format(rows))
        for r in rows: g.append(r)
        id_to_ind = {g[i][0]:i for i in range(len(g))}
        # 谁指向它
        for r in rows:
            for tar in r[who_conn_this] :
                if tar not in new_ids:
                    # print('tar: {}'.format(g[id_to_ind[tar]]))
                    g[id_to_ind[tar]][num_conn_pos] += 1
                    g[id_to_ind[tar]][conned_nodes_pos].append(r[0])
                    # print('new list: {}'.format(g[id_to_ind[tar]]))
        # 谁被它指
        for r in rows:
            for tar in r[conned_nodes_pos]:
                if tar not in new_ids:
                    # print('tar: {}'.format(g[id_to_ind[tar]]))
                    g[id_to_ind[tar]][num_conn_pos] += 1
                    g[id_to_ind[tar]][who_conn_this].append(r[0])
                    # print('new list: {}'.format(g[id_to_ind[tar]]))
    # 异常处理
    except Exception as inst:
        print('error',g)
        print(inst)
    return g

# 添加对应的信息
def extend_g(g, pointer, ref_li,temp_out,flag):
    '''
    :param g: 输入的图
    :param pointer: 加到了list的那一位
    :param ref_li: refer list， 根据那个添加节点
    :param temp_out: 输出的图组
    :param flag: 确定是添加的节点还是阀 1 add node; 2 add valve
    :return:
    '''
    if not ref_li[pointer]:
        return
    info = ref_li[pointer]
    if flag == 1:
        temp = add_new_node(g,info)
    else:
        temp = add_new_valve(g, info[0], info[1])

    iteration_controll(copy.deepcopy(temp), pointer + 1, ref_li,temp_out,flag)

# 控制递归的方法
# 假设输入的 可以添加节点的选择有： [[A],[B]]
# 那可以生成四张不同的图，每一位可以选择添加或者不添加，对应的方法是extend_g和not_extend
def iteration_controll(g, pointer, ref_li, temp_out,flag):
    '''
    :param g: 输入的图
    :param pointer: 加到了list的那一位
    :param ref_li: refer list， 根据那个添加节点
    :param temp_out: 输出的图组
    :param flag: 确定是添加的节点还是阀 1 add node; 2 add valve
    :return:
    '''
    if pointer > len(ref_li) - 1:
        temp_out.append(copy.deepcopy(g))
        return

    extend_g(copy.deepcopy(g), pointer, ref_li, temp_out,flag)
    not_extend(copy.deepcopy(g), pointer, ref_li, temp_out,flag)
    return



def not_extend(g, pointer, ref_li, temp_out,flag):
    iteration_controll(g, pointer + 1, ref_li, temp_out,flag)

# 读取输入的数据
def load_csv_data(path= ""):
    with open(path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        rows = []
        for row in reader:
            line = []
            if not len(row):
                continue
            for ind,r in enumerate(row):
                temp = r.strip('[').strip(']')
                if len(temp.split()):
                    r = r.strip('[').strip(']')
                    if len(r.split(","))>1:
                        line.append([int(num) for num in r.split(',')])
                    elif ind in [3,6]:
                        # print(r)
                        line.append([int(num) for num in r.split(',')])
                    else:
                        line.append(int(r))
                else:
                    line.append([])
            rows.append(line)
    data = rows # convert list to array
    print('load data from ' + path)
    temp = data[:-1]
    te_ex_li = data[-1]
    ex_li = []
    for i in te_ex_li:
        # print(i)
        if isinstance(i,int):
            if i <0:
                ex_li.append([])
            else:
                ex_li.append([i])
        else:
            ex_li.append(i)
    return temp,ex_li

import os
def get_file_name():
    g = os.walk(r"../data/csv_input_data")
    input_file_list = []
    for path, dir_list, file_list in g:
        for file_name in file_list:
            # print(os.path.join(path, file_name))
            input_file_list.append(str(os.path.join(path, file_name)))

    # for name in input_file_list:
    #     print(name)
    return input_file_list

def get_data():
    temp_out = []
    input_file_list = get_file_name()
    # for file_name in input_file_list:
    #     temp, ex_li = load_csv_data(file_name)
    #     for i in range(2):
    #         iteration_controll(temp, 0, ex_li, temp_out,1)
    # temp, ex_li = load_csv_data('../data/csv_input_data/2-15-1.csv ')
    # for i in range(5):
    #     iteration_controll(temp, 0, ex_li, temp_out,1)
    temp, ex_li = load_csv_data('../data/csv_input_data/2-16-1.csv')
    for i in range(20):
        iteration_controll(temp, 0, ex_li, temp_out,1)
    print('There are {} graph in the list'.format(len(temp_out)))

    final_out = []

    # feature
    feature_arr = []
    for g in temp_out:
        for line in g:
            feature_arr.append(line[1])
    allx = np.eye(20)[feature_arr]
    features = csr_matrix(allx)
    return input_1(temp_out),features,feature_arr

#所有图绘制成一个大图
def input_1(final_out):
    graph = {}
    features = {}
    ptr = 0
    for g in final_out:
        for line in g:
            graph[line[0]+ptr] = [i+ptr for i in line[conned_nodes_pos]]
            features[line[0]+ptr] = line[1]
        ptr = max(graph.keys())+1
    return graph

if __name__ == '__main__':
    get_data()
