import os
import sys
import math
import random
import optparse
import pandas as pd
import numpy as np

data = pd.read_csv('flow_0123.csv')
print(data)

time=0
depart_time=[]
tmp=[]
depart_time.append('time')
for i in range(np.size(data['time'])):
    if int(data['time'][i].split(':')[0])<6 :#>9 and int(data['time'][i].split(':')[0])<19:
        for a in range((data['nfbVD-N1-S-88.060-M-LOOP'][i])+(data['nfbVD-N1-S-91-I-WS-1-竹北'][i])):
            tmp.append(float(random.randint(time*100,((time+300))*100-1)/100))
        tmp.sort()
        time+=300
depart_time.append(tmp)
print(depart_time)
file =open('time_0-5.csv',"w+")
file.write(str(depart_time[0]))
for i in range(np.size(depart_time[1])):
    file.write(str(depart_time[1][i])+'\n')
file.close()