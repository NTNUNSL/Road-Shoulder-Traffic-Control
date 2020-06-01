#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file    QL.py
# @author  Danny Cheng
# @date    2020-05-20
# Update Qtable
# C_ -> Current state's value
# Q_ -> Q-Learning's value
# N_ -> Next state's value


###0529 Updating Q_value

import os
import sys
import math
import random
import optparse
import pandas as pd
import numpy as np
import glob
import time as Time

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
Alpha=0.7
Gamma=0.7
#Q(S,A)<-(1-Alpha)Q(S,A)+Alpha(reward+Gamma(Q(S',A)))
flow = 430
out = 55

def exp():
    P_time_s = Time.time()
    for i in State:
        C_state = pd.read_csv(i)
        size = len(C_state)
        for epoch in range(20):
            Q_now=Q_table
            time = []
            action_table=[]
            for j in range (len(C_state)):
                S_time = Time.time()
                C_flow = C_state['flow'][j] ## Current flow
                C_out  = C_state['out'][j]  ## Current out flow
                C_speed = C_state['speed'][j] if int(C_state['speed'][j])<15 else '15' ## Current speed
                N_flow = C_state['flow'][j+1] if j<size-1 else 0    ## Next state flow(real)
                N_state = next_state[C_flow-300]    ## Next state table
                C_time = []
                Q_state = Q_now.iloc[C_flow-300] ##Q_value

                ##### Choose action #####
                Qa = 'a1'
                for a in file_name:
                    if Q_state[a] > Q_state[Qa]:
                        Qa=a
                C_action=action[int(Qa.replace('a',''))-1] if Q_state[Qa]!=0 else action[random.randint(0,7)]
                print(C_action)
                if j>0:
                    Cp = action_table[j-1]
                    if C_action-Cp>10:
                        C_action=Cp+10
                    elif C_action-Cp<(-10):
                        C_action=Cp-10
                    action_table.append(C_action)
                    print(Cp)
                else:
                    action_table.append(C_action)
                print(C_action)

                for k in range(C_flow):
                    tmp = float(random.randint(0,29999)/100)
                    C_time.append(tmp)
                    time.append(tmp+(j*300))
                C_time.sort()

                ##### Generate simulation #####
                print('%s Epoch : %s, state : %s, flow : %s, out : %s'%(i.split('/')[2],epoch+1,j+1,C_flow,C_out))
                set_data.route_generate(C_flow,C_out,C_time,C_speed,action,file_name)
                result = set_data.simulate(C_flow)
                print(result)

                ##### update Q_value #####
                m=[0,'',0,0]
                if Q_state['a1']==0:
                    QN_state=0
                    for r in result:
                        Q_state[r[1]]=(1-Alpha)*Q_state[r[1]]+Alpha*(float(r[3])+Gamma*(QN_state))
                else:
                    QN_state=0
                    N_table=[]
                    for s in N_state:
                        if int(s) >0:
                            N_table.append(s)
                    Mr_state = N_table[random.randint(0,np.size(N_table)-1)]
                    print(Mr_state,N_table)
                    M_state = Q_now.iloc[int(Mr_state-300)]
                    Ma_state = 0
                    for Ma in file_name:
                        if M_state[Ma] > QN_state:
                            QN_state=M_state[Ma]
                    for r in result:
                        Q_state[r[1]]=(1-Alpha)*Q_state[r[1]]+Alpha*(float(r[3])+Gamma*(QN_state))
                Q_now.iloc[C_flow-300]=Q_state
                '''
                for r in result:
                    if float(r[3])>float(m[3]):
                        m=r
                print(m)
                C_reward = m[3]
                
                
                
                if Q_state['a1']==0:
                    QN_state = 0
                    Q_state[file_name[j]]=(1-Alpha)*Q_state[file_name[j]]+Alpha*(C_reward+Gamma*(QN_state))
                else:
                    QN_state = 0
                    for s in N_state:
                        if s >0:
                            for st in Q_now.iloc[s-300]:
                                pass
                    Q_state[file_name[j]]=(1-Alpha)*Q_state[file_name[j]]+Alpha*(C_reward+Gamma*(QN_state))
                Q_now.iloc[C_flow-300]=Q_state
                '''
                
                #set_data.route_generate(C_flow,C_out,C_time,C_speed,action,file_name)
                #set_data.simulate(C_flow)


                #####   update next state table   #####
                
                print(Time.time()-S_time)
                ns = next_state[C_flow-300]
                for k in range (len(ns)):
                    if ns[k] == 0 or ns[k] == N_flow:
                        ns[k]=N_flow
                        break
            print(action_table)
            ##Simulate all
            print('%s Epoch : %s Finished!'%(i.split('/')[2],epoch+1))
            time.sort()

    P_time_e = Time.time()



    #exp()
'''set_data.route_generate(flow,out,time,action,file_name)
set_data.simulate(flow)
print(State)'''

if __name__ == "__main__":
    '''a = Q_now.iloc[0]
    Qa='a1'
    k=0
    for i in file_name:
        a[i]+=k
        k+=1
        if a[i]>a[Qa]:
            Qa=i
        print(a[i],a[Qa])
        #a[i]+=1
    Q_now.iloc[0]=a
    print(Q_now.iloc[0])
    print(Qa.replace('a',''))'''
    exp()
    n = next_state[0]
    print(n)

#for i in next_state:
#    print(i)
#print(next_state)