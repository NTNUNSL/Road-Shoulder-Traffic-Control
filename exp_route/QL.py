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
###0603 chenge Choose action(Boltzmann Distribution)
###0604 Update Q-value Q-table update, learning rate, reward calculate

import os
import sys
import math
import glob
import random
import optparse
import numpy as np
import pandas as pd
import time as Time

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib

import set_data
import QL_brain

file_name  = ['a1','a2','a3','a4','a5','a6','a7','a8']
action     = {'a1':130,'a2':120,'a3':110,'a4':100,'a5':90,'a6':80,'a7':70,'a8':60}
State      = sorted(glob.glob('../training_data/state*'),key=os.path.basename)
Q_table    = pd.read_csv('Q_table.csv',dtype=float)
next_state = np.loadtxt('next_state.txt',delimiter=',')
Q_now      = Q_table
Counter    = pd.DataFrame(np.zeros((300,8),dtype=int),columns=action.keys()) ## Counter[action][flow-300]


Epoch = 1
Alpha = 0.7
Gamma = 0.7
Epsilon = 0.2
reward=[]

#Q(S,A)<-(1-Alpha)Q(S,A)+Alpha(reward+Gamma(Q(S',A)))
flow = 430
out = 55

def exp():
    P_time_s = Time.time()
    day=1
    for i in State:
        C_state = pd.read_csv(i)
        size    = len(C_state)
        D_reward=[]
        for epoch in range(Epoch):
            C_reward=0
            #Q_now = Q_table
            time  = []
            action_table=[]
            for j in range (len(C_state)):
                S_time  = Time.time()
                C_flow  = C_state['flow'][j] ## Current flow
                C_out   = C_state['out'][j]  ## Current out flow
                C_speed = C_state['speed'][j] if int(C_state['speed'][j])<15 else '15' ## Current speed
                N_flow  = C_state['flow'][j+1] if j<size-1 else 0    ## Next state flow(real)
                N_state = next_state[C_flow-300]    ## Next state table
                C_time  = []
                Q_state = Q_now.iloc[C_flow-300] ##Q_value

                ##### Choose Action #####
                epsilon = Epsilon+((Epoch-epoch)/Epoch)*(0.5)
                print(epsilon)
                C_action = QL_brain.choose_action(Q_state,C_flow,Counter,action,epsilon)
                Qa = [ac for ac in action if action[ac]==C_action][0]
                Counter[Qa][C_flow-300]+=1
                action_table.append(C_action)
                print(C_action,Qa)

                ##### Stairs Choose action #####
                '''if j>0:
                    Cp = action_table[j-1]
                    if C_action-Cp>10:
                        C_action=Cp+10
                    elif C_action-Cp<(-10):
                        C_action=Cp-10
                    action_table.append(C_action)
                    print(Cp)
                else:
                    action_table.append(C_action)
                print(C_action)'''

                for k in range(C_flow):
                    tmp = float(random.randint(0,29999)/100)
                    C_time.append(tmp)
                    time.append(tmp+(j*300))
                C_time.sort()

                ##### Generate simulation #####
                print('%s Epoch : %s, state : %s, flow : %s, out : %s, action : %s'%(i.split('/')[2],epoch+1,j+1,C_flow,C_out,C_action))
                set_data.route_generate(C_flow,C_out,C_time,C_speed,C_action,Qa)
                result = set_data.simulate(C_flow,C_action,Qa)
                print(result)
                C_reward+=float(result[3])

                ##### update Q_value #####
                Q_now.iloc[C_flow-300]=QL_brain.Update_Q_value(Q_state,Q_now,C_flow,N_state,result,Counter,Qa,Alpha,Gamma)
                print(Q_now.iloc[C_flow-300])

                #####   update next state table   #####
                
                print(Time.time()-S_time)
                ns = next_state[C_flow-300]
                for k in range (len(ns)):
                    if ns[k] == 0 or ns[k] == N_flow:
                        ns[k] = N_flow
                        break
            D_reward.append(C_reward)
            print(action_table)
            print(C_reward)
            ##Simulate all
            print('%s Epoch : %s Finished!'%(i.split('/')[2],epoch+1))
            time.sort()

            set_data.Epo_route_generate(C_state,time,action,epoch)
        reward.append(D_reward)
        Q_now.to_csv('table/table_day%s.csv'%day,index=False)
        np.savetxt('Rewards/reward_%s.txt'%i.split('/')[2].split('.')[0].split('_')[1],D_reward,fmt='%s',delimiter=',')
        day += 1
    P_time_e = Time.time()


if __name__ == "__main__":
    exp()
    #n = next_state[0]
    #print(n)

#for i in next_state:
#    print(i)
#print(next_state)