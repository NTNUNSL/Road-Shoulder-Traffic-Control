#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @file    set_data.py
# @author  Danny Cheng
# @date    2020-05-11
# Generate simulation file and get its result

import os
import sys
import math
import random
import optparse
import pandas as pd
import numpy as np
import text
import glob

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib


action = [130,120,110,100,90,80,70,60]
file_name = ['a1','a2','a3','a4','a5','a6','a7','a8']
vehicle_id = '<vehicle id="%s" type="type%s" route="route%s" depart="%s" departLane="free" departSpeed="%s" departPos="base">\n'\
                '<param key="has.driverstate.device" value="true"/>\n'\
                '</vehicle>\n'
route_title='<vType id="type1" vClass="passenger"/>\n'\
                            '<vType id="type2" vClass="custom1"/>\n'\
                            '<vType id="type3" vClass="custom2"/>\n'\
                            '<route id="route1" color="1,1,0" edges="lane_s01 lane_s02 lane_s_connect01 lane_s03 lane_s_connect02 lane_s_connect03 lane_s04"/>\n'\
                            '<route id="route2" color="0,1,0" edges="lane_s01 lane_s02 lane_s_connect01 lane_s_out01 lane_s_out02 lane_s_connect_out02"/>\n'\
                            '<route id="route3" color="1,0,0" edges="lane_s_connect_in02 lane_s_in01 lane_s_in02 lane_s_connect02 lane_s_connect03 lane_s04"/>\n'


#Q(S,A)<-(1-Alpha)Q(S,A)+Alpha(reward+Gamma(Q(S',A)))
Reward_total=[]
flow=427
out_flow=80

def route_set(freetrips,flow,out_flow,t_speed,time,shoulder,k):
    done_flow=[]
    num,count=0,0
    #t_speed='8.54'
    while (num<out_flow):
        if flow>np.size(done_flow):
            if(random.randint(1,20))>15:
                num+=1
                done_flow.append(num)
                v_type=3 if np.size(done_flow) < shoulder else 1
                freetrips.write(vehicle_id%(k,v_type,'2',(time[count]),t_speed))
                k+=1
                count+=1
            else:
                done_flow.append(num)
                freetrips.write(vehicle_id%(k,'1','1',(time[count]),t_speed))
                k+=1
                count+=1
        else:
            num=out_flow
    last = shoulder-np.size(done_flow)
    if last > 0 :
        #print(last)
        for a in range(last):
            freetrips.write(vehicle_id%(k,'3','1',(time[count]),t_speed))
            k+=1
            count+=1
            done_flow.append(num)
    for j in range(flow-np.size(done_flow)):
        freetrips.write(vehicle_id%(k,'1','1',(time[count]),t_speed))
        k+=1
        count+=1
    #print('done')

def route_generate(flow,out_flow,time,t_speed,action,file_name):
    with open('C_route/%s_%s.sumocfg'%(str(flow),file_name),'w') as f:
        t = '%s_%s'%(str(flow),file_name)
        x = text.sumo_conf(t)
        f.write(x)
    with open('C_route/%s_%s.xml'%(str(flow),file_name),'w') as freetrips:
        sumolib.writeXMLHeader(freetrips,'Danny Cheng, departLane: free','routes')
        freetrips.write(route_title)
        route_set(freetrips,flow,out_flow,t_speed,time,action,0)
        freetrips.write("</routes>\n")
def Epo_route_generate(state,time,action,epo):
    '''with open('C_route/epo_%s.sumocfg'%(epo),'w') as f:
        t = 'epo_%s'%epo
        x = text.sumo_conf(t)
        f.write(x)
    with open('C_route/epo_%s.xml'%(epo),'w') as freetrips:
        sumolib.writeXMLHeader(freetrips,'Danny Cheng, departLane: free','routes')
        freetrips.write(route_title)
        for i in range (np.size(time)):'''
    print(state['flow'][1],time[500],action['a1'],epo)



def simulate(flow,action,file_name):
    result_list=[]
    tmp = []
    r = 'C_route/%s_%s'%(str(flow),file_name)
    command='sumo -c %s.sumocfg --no-warnings'%(r)
    result=os.popen(command).read()
    #print(result)
    t = result.split('\n')
    for j in range(np.size(t)):
        if 'DepartDelay:' in t[j]:
            rate=action/flow
            Delay=abs(float(result.split('\n')[j].split(' ')[2])) if abs(float(result.split('\n')[j].split(' ')[2]))>1.0 else 1.01
            #print(rate)
            #print(float(math.log10(Delay)))
            tmp.append(action)
            tmp.append(file_name)
            tmp.append(Delay)
            try:
                tmp.append('%.2f'%((1-float(rate))+float((1/math.log10(Delay))*0.1)))
            except:
                tmp.append(0)
            result_list.append(tmp)
            break
    return tmp

if __name__ == "__main__":
    flow =436
    out=23
    time=[]
    for i in range(flow):
        time.append(float(random.randint(0,29999)/100))
    time.sort()
    route_generate(flow,out,time,100,'a4')
    simulate(flow)



