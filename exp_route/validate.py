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


import text
import set_data
import QL_brain

action     = {'a1':130,'a2':120,'a3':110,'a4':100,'a5':90,'a6':80,'a7':70,'a8':60}
vehicle_id = '<vehicle id="%s" type="type%s" route="route%s" depart="%s" departLane="free" departSpeed="%s" departPos="base">\n'\
                '<param key="has.driverstate.device" value="true"/>\n'\
                '</vehicle>\n'
route_title='<vType id="type1" vClass="passenger"/>\n'\
                            '<vType id="type2" vClass="custom1"/>\n'\
                            '<vType id="type3" vClass="custom2"/>\n'\
                            '<route id="route1" color="1,1,0" edges="lane_s01 lane_s02 lane_s_connect01 lane_s03 lane_s_connect02 lane_s_connect03 lane_s04"/>\n'\
                            '<route id="route2" color="0,1,0" edges="lane_s01 lane_s02 lane_s_connect01 lane_s_out01 lane_s_out02 lane_s_connect_out02"/>\n'\
                            '<route id="route3" color="1,0,0" edges="lane_s_connect_in02 lane_s_in01 lane_s_in02 lane_s_connect02 lane_s_connect03 lane_s04"/>\n'

state = pd.read_csv('../flow/state_2020-0123.csv')
Q_table = pd.read_csv('table/table_day8.csv')
com = ['origin','non_control','QL_control']

def origin():
    with open('../flow/validate/origin.sumocfg','w') as f:
        t = 'origin'
        x = text.sumo_conf(t)
        f.write(x)
    with open('../flow/validate/origin.xml','w') as freetrips:
        sumolib.writeXMLHeader(freetrips,'Danny Cheng, departLane: free','routes')
        freetrips.write(route_title)
        k=0
        for i in range(len(state['flow'])):
            #C_speed = state['speed'][i] if int(state['speed'][i])<15 else '15'
            C_speed='max'
            set_data.route_set(freetrips,state['flow'][i],state['out'][i],C_speed,time[i],0,k)
            k+=state['flow'][i]
        freetrips.write("</routes>\n")
    return 1

def non_control():
    with open('../flow/validate/non_control.sumocfg','w') as f:
        t = 'non_control'
        x = text.sumo_conf(t)
        f.write(x)
    with open('../flow/validate/non_control.xml','w') as freetrips:
        sumolib.writeXMLHeader(freetrips,'Danny Cheng, departLane: free','routes')
        freetrips.write(route_title)
        k=0
        for i in range(len(state['flow'])):
            #C_speed = state['speed'][i] if int(state['speed'][i])<15 else '15'
            C_speed='max'
            set_data.route_set(freetrips,state['flow'][i],state['out'][i],C_speed,time[i],state['shoulder'][i],k)
            k+=state['flow'][i]
        freetrips.write("</routes>\n")
    return 1

def QL_control():
    with open('../flow/validate/QL_control.sumocfg','w') as f:
        t = 'QL_control'
        x = text.sumo_conf(t)
        f.write(x)
    with open('../flow/validate/QL_control.xml','w') as freetrips:
        sumolib.writeXMLHeader(freetrips,'Danny Cheng, departLane: free','routes')
        freetrips.write(route_title)
        k=0
        action_table=[]
        for i in range(len(state['flow'])):
            #C_speed = state['speed'][i] if int(state['speed'][i])<15 else '15'
            C_speed='max'
            if i==0:
                C_action = 60
                action_table.append(C_action)
            else:
                table = Q_table.iloc[state['flow'][i]-1]
                q = np.where(table==table.max())[0]
                C_action = action['a%s'%(int(np.random.choice(q))+1)]
                Cp = action_table[i-1]
                ##### Stair case #####
                if C_action-Cp>10:
                    C_action=Cp+10
                elif C_action-Cp<(-10):
                    C_action=Cp-10
                action_table.append(C_action)

            set_data.route_set(freetrips,state['flow'][i],state['out'][i],C_speed,time[i],C_action,k)
            k+=state['flow'][i]
        freetrips.write("</routes>\n")
    return action_table

if __name__ == "__main__":
    time=[]
    for i in range(len(state['flow'])):
        C_time=[]
        for j in range(state['flow'][i]):
            tmp = float('%.2f'%(random.randint(0,29999)/100))
            C_time.append(tmp+(i*300))
        C_time.sort()
        time.append(C_time)

    #origin()
    #non_control()
    #action_table=QL_control()
    t_delay=[]
    for i in com:
        Delay = 0
        r = '../flow/validate/%s.sumocfg'%i
        for j in range(20):
            if i=='origin':
                origin()
            elif i =='non_control':
                non_control()
            elif i=='QL_control':
                action_table=QL_control()
            command='sumo -c %s --no-warnings'%(r)
            result=os.popen(command).read().split('\n')
            for k in range(np.size(result)):
                if 'DepartDelay:' in result[k]:
                    Delay+=abs(float(result[k].split(' ')[2]))
                    print(i,j,abs(float(result[k].split(' ')[2])))
        t_delay.append(Delay/20)
    for i in range(len(com)):
        print('%s: %s'%(com[i], t_delay[i]))
    


    '''k=[]
    for i in range(len(state['flow'])):
        k.append([state['shoulder'][i],action_table[i],state['out'][i]])
    df = pd.DataFrame(k,columns=['non_control','QL_control','out'])
    df.to_csv('../flow/validate/shoulder.csv',index=False)'''
