import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sqlite3 as sql
from datetime import datetime
from dateutil import parser

x = []
y = []
x1 =[]
y1=[]

try:
    con = sql.connect("pmu_database")
    con.row_factory = sql.Row

    cur = con.cursor()
    res=cur.execute("select * from data1 LIMIT 10000").fetchall()
    print(len(res))
    start = datetime(2022,4,13,18,16,00)
    end = datetime(2022,4,13,18,20,20)
    c = 0
    for i in range(0,len(res)):
        if parser.parse((res[i]["time_stamp"]))>start and parser.parse((res[i]["time_stamp"]))<end:
            c +=1
            x.append(res[i]["arduino_sec"])
            y.append(10)
            x1.append(res[i]["server_sec"]-res[i-1]["server_sec"])
            y1.append(5)
            if c == 1000:
                break

            
    con.close()
except:     
    print("error in sql operation")
    con.close()
# ypoints = [min(y),max(y)]        
print(c)     
# plt.title("Packet Departure and Arrival Visualization - 50 packets")
# plt.xlabel('Time in Sec')
# plt.ylabel('Server                                                           Arduino')
# plt.yticks([0,15])
# plt.grid(True)
# plt.scatter(x[200:250], y[200:250], marker = 'o', c = 'g')
# plt.scatter(x1[200:250], y1[200:250], marker = 'o', c = 'r')
#plt.plot(x, z, c = 'r')
  

sns.set_style('whitegrid')
sns.kdeplot(np.array(x1),x ='Delay in sec',bw_adjust=.2)
plt.show()