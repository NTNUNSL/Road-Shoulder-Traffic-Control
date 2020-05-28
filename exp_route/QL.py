#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file    QL.py
# @author  Danny Cheng
# @date    2020-05-20
# Update Qtable

import os
import sys
import math
import random
import optparse
import pandas as pd
import numpy as np
import glob

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib

import set_data

action = [130,120,110,100,90,80,70,60]
file_name = ['a1','a2','a3','a4','a5','a6','a7','a8']
State = sorted(glob.glob('../training_data/state*'),key=os.path.basename)
Q_table = pd.read_csv('Q_table.csv')
next_state = np.loadtxt('next_state.txt',delimiter=',')
Q_now=Q_table

Epoch=100
Alpha=0.9
Gamma=0.9
#Q(S,A)<-(1-Alpha)Q(S,A)+Alpha(reward+Gamma(Q(S',A)))
flow = 430
out = 55


for i in State:
    C_state = pd.read_csv(i)
    size = len(C_state)
    for epoch in range(2):
        time = []
        for j in range (len(C_state)):
            C_flow = C_state['flow'][j]
            C_out  = C_state['out'][j]
            N_flow = C_state['flow'][j+1] if j<size-1 else 0
            C_time = []
            print('%s Epoch : %s, state : %s, flow : %s, out : %s'%(i.split('/')[2],epoch+1,j,C_flow,C_out))
            for k in range(C_flow):
                tmp = float(random.randint(0,29999)/100)
                C_time.append(tmp)
                time.append(tmp+(j*300))
            C_time.sort()
            set_data.route_generate(C_flow,C_out,C_time,action,file_name)
            set_data.simulate(C_flow)
            #####   update next state table   #####
            ns = next_state[C_flow-300]
            for k in range (len(ns)):
                if ns[k] == 0 or ns[k] == N_flow:
                    ns[k]=N_flow
                    break
        print('%s Epoch : %s Finished!'%(i.split('/')[2],epoch+1))
        time.sort()


'''set_data.route_generate(flow,out,time,action,file_name)
set_data.simulate(flow)

print(State)'''
print(State)

#for i in next_state:
#    print(i)
#print(next_state)