import os
import sys
import math
import random
import optparse
import pandas as pd
import numpy as np
import text

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib

action = [130,120,110,100,90,80,70,60]

vehicle_id = '<vehicle id="%s" type="type%s" route="route%s" depart="%s" departLane="free" departSpeed="%s" departPos="base">\n'\
                '<param key="has.driverstate.device" value="true"/>\n'\
                '</vehicle>\n'
file_name = ['a1','a2','a3','a4','a5','a6','a7','a8']
flow=427
out_flow=80
time=[]




def route_set(freetrips,flow,out_flow,time,shoulder):
    done_flow=[]
    num,k,count=0,0,0
    t_speed='8.54'
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
        print(last)
        for a in range(last):
            freetrips.write(vehicle_id%(k,'3','1',(time[count]),t_speed))
            count+=1
            done_flow.append(num)
    for j in range(flow-np.size(done_flow)):
        freetrips.write(vehicle_id%(k,'1','1',(time[count]),t_speed))
        k+=1
        count+=1
    print('done')



for i in range(flow):
    time.append(float(random.randint(0,29999)/100))
time.sort()
for i in range(np.size(action)):
    with open(file_name[i]+'.sumocfg','w') as f:
        x=text.tt(file_name[i])
        f.write(x)
    with open(file_name[i]+'.xml','w') as freetrips:
        sumolib.writeXMLHeader(freetrips,'Danny Cheng, departLane: free','routes')
        freetrips.write('<vType id="type1" vClass="passenger"/>\n'\
                        '<vType id="type2" vClass="custom1"/>\n'\
                        '<vType id="type3" vClass="custom2"/>\n'\
                        '<route id="route1" color="1,1,0" edges="lane_s01 lane_s02 lane_s_connect01 lane_s03 lane_s_connect02 lane_s_connect03 lane_s04"/>\n'\
                        '<route id="route2" color="0,1,0" edges="lane_s01 lane_s02 lane_s_connect01 lane_s_out01 lane_s_out02 lane_s_connect_out02"/>\n'\
                        '<route id="route3" color="1,0,0" edges="lane_s_connect_in02 lane_s_in01 lane_s_in02 lane_s_connect02 lane_s_connect03 lane_s04"/>\n')
        route_set(freetrips,flow,out_flow,time,action[i])
        freetrips.write("</routes>\n")
    #print('Output %s_policy trip file done!'%options.policy)

result_list=[]
for i in range(np.size(action)):
    tmp=[]
    command='sumo -c %s.sumocfg --no-warnings'%file_name[i]
    result=os.popen(command).read()
    t = result.split('\n')
    for j in range(np.size(t)):
        if 'DepartDelay:' in t[j]:
            rate=action[i]/flow
            Delay=float(result.split('\n')[j].split(' ')[2])
            print(rate)
            print(float(math.log10(Delay)))
            tmp.append(action[i])
            tmp.append(Delay)
            tmp.append('%.2f'%((1-float(rate))+float(1/math.log10(Delay))))
            result_list.append(tmp)
            break
print(result_list)






