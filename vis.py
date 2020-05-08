import requests
import xml.etree.cElementTree as ET
import numpy as np
import gzip
import os


#with open('fcd/0123_open_10to19_district_fcd.xml','rb') as f:
#        tree = ET.fromstring(f.read().decode('utf-8'))

tree = ET.parse('b_0123_normal_10-18_fcd.xml')
root = tree.getroot()
V_ins={}

for i in range(1,5):
    Vs=[]
    Vs.append(['flow','speed'])
    time, speed_m,total_num=0,0,0
    for first in root:
        num,speed_s=0,0
        for second in first:
            if ('lane_s0'+str(i)) in second.attrib['lane'] and second.attrib['lane']!=('lane_s0'+str(i)+'_0'):
                if second.attrib['id'] not in V_ins.keys():
                    speed_s+=float(second.attrib['speed'])
                    num+=1
                    V_ins.update({second.attrib['id']:1})
                else:
                    pass
                #print(second.get('speed'),second.get('lane'))
        if num>0:
            speed_s = float(speed_s/num)
        else:
            speed_s = 0
        if time<60:
            speed_m+=speed_s
        else:
            tmp=[]
            speed_mo=float(((speed_m/60)*3600)/1000)
            print('%.2f, %.2f'%(speed_mo,(speed_m/60)))
            tmp.append(num)
            tmp.append('%.2f'%(speed_mo))
            Vs.append(tmp)
            time=0
            speed_m=0
        time+=1

    np.savetxt('test_0123_normal_10-18_s0%s.csv'%(i),Vs,fmt='%s',delimiter=',')