#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file    QL_brain.py
# @author  Danny Cheng
# @date    2020-06-04
# QL brain

import os
import sys
import math
import glob
import random
import optparse
import numpy as np
import pandas as pd
import time as Time


def choose_action(Q_state,C_flow,Counter,action,Epsilon):
    ##### Choose action #####
    Boltz_P=[]
    Boltz=0
    if random.uniform(0,1)<Epsilon:
        #random
        ##### Boltzmann Distribution #####
        for a in action:
            p = float('%.2f'%(math.exp(Q_state[a]/(1000 - Counter[a][C_flow-300]))))
            Boltz_P.append(p)
            Boltz+=p
        Boltz_P = [a/Boltz for a in Boltz_P]
        P_action = np.random.choice(list(action.keys()),size=500,p=Boltz_P)
        C_action = action[P_action[np.random.randint(0,499)]]
    else:
        #select highest Q-value
        Q_max = np.where(Q_state == Q_state.max())[0]+1
        ##### Boltzmann Distribution #####
        for a in Q_max:
            p = float('%.2f'%(math.exp(Q_state['a%s'%a]/(1000 - Counter['a%s'%a][C_flow-300]))))
            Boltz_P.append(p)
            Boltz+=p
        Boltz_P = [a/Boltz for a in Boltz_P]
        P_action = np.random.choice(Q_max,size=100,p=Boltz_P)
        C_action = action['a%s'%P_action[np.random.randint(0,99)]]
    return C_action

def Update_Q_value(Q_state,Q_now,C_flow,N_state,result,Counter,Qa,Alpha,Gamma):
    Lr = float('%.2f'%pow((1/Counter[Qa][C_flow-300]),Alpha))
    if Q_state.max()==0:
        QN_state=0
        Q_state[result[1]]=(1-Lr)*Q_state[result[1]]+Lr*(float(result[3])+Gamma*(QN_state))
    else:
        QN_state=0
        N_table=[]
        for s in N_state:
            if int(s) >0:
                N_table.append(s)
        Mr_state = np.random.choice(N_table)
        print(Mr_state,N_table)
        M_state = Q_now.iloc[int(Mr_state-300)]
        QN_state = M_state.max()
        print(M_state.max(),QN_state)
        Q_state[result[1]]=(1-Lr)*Q_state[result[1]]+Lr*(float(result[3])+Gamma*(QN_state))
    #Q_now.iloc[C_flow-300]=Q_state
    return Q_state