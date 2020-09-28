#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 9/6/2020 18:56
# @Author  : Haoyu Lyu
# @File    : draw_result.py
# @Software: PyCharm
import networkx as nx
import numpy as np
import json
from pyecharts import options as opts
from pyecharts.charts import Graph
id_to_name ={0:'分水器/冷站冷冻供水管',1:'集水器/冷战冷冻回水管',2:'冷机',3:'泵',4:'空调末端',5: '  阀',
             8:'定压水箱',9:'冷却塔',10:'虚拟节点', 11:'回风口',12:'新风机组',
             13:'新风口',14:'风机盘管',15:'送风口',19:'排风口',17:"空调机组",18:'自来水',16:"板式换热器"
             }

TH = 0.6




def spec(N):
    t = np.linspace(-510, 510, N)
    rgb =  np.round(np.clip(np.stack([-t, 510-np.abs(t), t], axis=1), 0, 255)).astype(np.uint8)
    hex_c = ['#%02x%02x%02x' % (i[0],i[1],i[2]) for i in rgb]
    return hex_c


def insert_dic(dic,k,v):
    dic.update({k:dic.get(k,[])})
    dic[k].append(v)

def draw_result_html(graph,features,test,test_false, preds, preds_false):
    G = nx.DiGraph()

    # set color
    color_len = len(id_to_name)
    colors = spec(color_len)
    name_to_color = {}
    for key in id_to_name:
        if key not in name_to_color:
            name_to_color[key] = colors[len(name_to_color)]

    # Add nodes
    keys = list(graph.keys())
    g_id_to_ind = {}
    g_ind_to_id = {}
    nodes = []
    for ind in range(len(keys)):

        key = keys[ind]
        nodes.append({
            "id": str(key),
            "name": id_to_name[features[ind]],
            "symbolSize": 5,
            "itemStyle": {"normal": {"color": name_to_color[features[ind]]}}
        })
        g_id_to_ind[key] = ind
        g_ind_to_id[ind]=key



    # predict graph
    check_set = {}
    links_prob = {}
    edges = []
    corr_name ={}
    # 构建 check——set 表
    for ind in range(len(test)):
        line = test[ind]
        temp = str(line[0])+'@'+str(line[1])
        name0 = id_to_name[features[line[0]]]
        name1 = id_to_name[features[line[1]]]
        type_link = links_prob.get(name0+'->'+name1,[])
        type_link.append(preds[ind])
        links_prob[name0+'->'+name1] = type_link
        check_set[temp] = preds[ind]
        if g_ind_to_id[line[1]] in graph[g_ind_to_id[line[0]]]:
            insert_dic(corr_name, name0+'->'+name1, check_set[temp] > TH)
    # # 检测准确率
    acc_name = {}
    for key in graph:
        for v in graph[key]:
            sou = g_id_to_ind[key]
            tar = g_id_to_ind[v]
            name0 = id_to_name[features[sou]]
            name1 = id_to_name[features[tar]]
            temp_true = str(sou)+'@'+str(tar)
            temp_false = str(tar)+'@'+str(sou)
            insert_dic(acc_name,name0+'->'+name1,check_set[temp_true]>check_set[temp_false])

    prob_pick = {}
    prob_diff = {}
    one_dir = []
    not_in_graph = []
    for ind in range(len(test)):
        line = test[ind]
        temp = str(line[0])+'@'+str(line[1])
        temp1 = str(line[1])+'@'+str(line[0])
        name0 = id_to_name[features[line[0]]]
        name1 = id_to_name[features[line[1]]]
        if temp1 not in check_set:
            # edges.append({"source": str(g_ind_to_id[line[0]]),
            #               "target": str(g_ind_to_id[line[1]]),
            #               "value": "{} -> {},：{:.2}".
            #              format(name0, name1, check_set[temp])
            #               })

            one_dir.append([g_ind_to_id[line[1]],g_ind_to_id[line[0]]])
            insert_dic(prob_pick,name0 + '->' + name1, check_set[temp])
        elif temp not in check_set:

            # edges.append({"source": str(g_ind_to_id[line[1]]),
            #               "target": str(g_ind_to_id[line[0]]),
            #               "value" : "{} -> {},：{:.2}".
            #              format(name1,name0,check_set[temp1])
            #               })
            one_dir.append([g_ind_to_id[line[1]],g_ind_to_id[line[0]]])
            insert_dic(prob_pick,name1+'->'+name0, check_set[temp])

        elif check_set[temp1]>check_set[temp]:
            edges.append({"source": str(g_ind_to_id[line[1]]),
                          "target": str(g_ind_to_id[line[0]]),
                          "value" : "{} -> {},：{:.2}".
                         format(name1,name0,check_set[temp1])
                          })
            insert_dic(prob_pick,name1+'->'+name0,check_set[temp1])
            insert_dic(prob_diff,name0+'-'+name1,abs(check_set[temp]-check_set[temp1]))
        else:
            edges.append({"source": str(g_ind_to_id[line[0]]),
                          "target": str(g_ind_to_id[line[1]]),
                          "value" : "{} -> {},：{:.2}".
                         format(name0,name1,check_set[temp])
                          })
            insert_dic(prob_pick, name0 + '->' + name1, check_set[temp])
            insert_dic(prob_diff, name0 + '-' + name1, abs(check_set[temp] - check_set[temp1]))

    # original graph
    for k,v in links_prob.items():
        links_prob[k] = np.mean(v)
    for k,v in prob_pick.items():
        prob_pick[k] = np.mean(v)
    for k,v in prob_diff.items():
        prob_diff [k] = np.mean(v)
    for k,v in corr_name.items():
        corr_name [k] = np.mean(v)
    for k,v in acc_name.items():
        acc_name [k] = np.mean(v)
    json_file = './statistics.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(links_prob,f,ensure_ascii=False,indent=1)
    json_file_pick = './statistics_pick.json'
    with open(json_file_pick, 'w', encoding='utf-8') as f:
        json.dump(prob_pick,f,ensure_ascii=False,indent=1)

    json_file_diff = './statistics_diff.json'
    with open(json_file_diff, 'w', encoding='utf-8') as f:
        json.dump(prob_diff, f, ensure_ascii=False, indent=1)

    json_file_corr = './statistics_corr.json'
    with open(json_file_corr, 'w', encoding='utf-8') as f:
        json.dump(corr_name, f, ensure_ascii=False, indent=1)

    json_file_corr = './graph.json'
    with open(json_file_corr, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=1)
    json_file_corr = './one_dir.json'
    with open(json_file_corr, 'w', encoding='utf-8') as f:
        json.dump(one_dir, f, ensure_ascii=False, indent=1)
    json_file_corr = './check_set.json'
    with open(json_file_corr, 'w', encoding='utf-8') as f:
        json.dump(check_set, f, ensure_ascii=False, indent=1)
    json_file_corr = './acc_name.json'
    with open(json_file_corr, 'w', encoding='utf-8') as f:
        json.dump(acc_name, f, ensure_ascii=False, indent=1)


    np.savetxt('testlist.txt', test,fmt="%d")


    # links = [opts.GraphLink(source=nodes_id.index(e[0]), target=nodes_id.index(e[1])) for e in G.edges()]
    file_name = "temp_res/predict_epoch200_v2.html"
    (
        Graph(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add(
            series_name="",
            nodes=nodes,
            links=edges,
            repulsion=2000,
            # layout="none",
            #         is_roam=True,
            is_selected=False,
            gravity=0,
            is_draggable=True,
            is_focusnode=False,
            label_opts=opts.LabelOpts(is_show=True),
            linestyle_opts=opts.LineStyleOpts(width=0.9, opacity=0.9),
            edge_label=opts.LabelOpts(
                is_show=True, position="middle", formatter="{c}"
            ),
        )
            .set_global_opts(
            # legend_opts=opts.LegendOpts(orient="vertical", pos_left="2%", pos_top="20%"),
            title_opts=opts.TitleOpts(title="预测关系图"),
        )
            .render(file_name)
    )
    print("done")
    return G

