#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 7/20/2020 22:13
# @Author  : Haoyu Lyu
# @File    : test.py
# @Software: PyCharm


line1=input().split()
num_point=int(line1[0])
num_query=int(line1[1])

line2=input().split()
int_list=[int(_) for _ in line2]
# 对int_list进行升序排列
for i in range(num_point):
    for j in range(num_point-i-1):
        if int_list[j]>int_list[j+1]:
            temp=int_list[j]
            int_list[j]=int_list[j+1]
            int_list[j+1]=temp
output=[]
for k in range(num_query):
    temp_line=input().split()
    left=int(temp_line[0])
    right=int(temp_line[1])

    print(len(set()))