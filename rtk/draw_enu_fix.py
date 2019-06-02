#-*- coding-f:utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np

def getsite_enu(filename):
    enu=[[],[],[]]
    time = [ ]
    flag = []
    with open(filename,"r") as myfile:
        for i in myfile:
            if (i[0] == "%"):
                continue
            temp = i.split()
            enu[0].append(float(temp[2]))
            enu[1].append(float(temp[3]))
            enu[2].append(float(temp[4]))
            time.append(float(temp[1]))
            if (temp[5] == "FLOAT"):
                flag.append(0)
            else:
                flag.append(1)

    return time,enu,flag

def draw_enu(enu,ylabel):
    x = [i for i in range(len(enu[0]))]
    plt.plot(x,enu[0],color='r',label="E")
    plt.plot(x,enu[1],color='g',label="N")
    plt.plot(x,enu[2],color='b',label="U")
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend(loc="upper right")
    plt.ylim(-0.04,0.06)
    plt.yticks(np.arange(-0.04,0.06,0.02))

def draw_enu_3part(time,enu,ylabel,color,marker,size):
    x = [ i for i in range(len(enu[0]))]
    x = [ i-time[0] for i in time]
    plt.subplot(311)
    plt.plot(x,enu[0],color=color,marker=marker,lw=0,label="E",ms=size)
    #plt.plot(x,enu[0],"r.",label="E"size)
    plt.ylabel(ylabel,fontsize=13)
    plt.grid()
    plt.legend(loc="upper right")
    plt.xlim(xmin=0)
    #plt.ylim(-0.04,0.06)
    #plt.yticks(np.arange(-0.04,0.06,0.02),fontsize=13)


    plt.subplot(312)
    plt.plot(x,enu[1],color=color,marker=marker,lw=0,label="N",ms=size)
    plt.ylabel(ylabel,fontsize=13)
    plt.grid()
    plt.legend(loc="upper right")
    plt.xlim(xmin=0)
    #plt.ylim(-0.04,0.06)
    #plt.yticks(np.arange(-0.04,0.06,0.02),fontsize=13)


    plt.subplot(313)
    plt.plot(x,enu[2],color=color,marker=marker,lw=0,label="U",ms=size)
    plt.ylabel(ylabel,fontsize=13)
    plt.grid()
    plt.legend(loc="upper right")
    plt.xlim(xmin=0)
    #plt.ylim(-0.04,0.06)
    #plt.yticks(np.arange(-0.04,0.06,0.02),fontsize=13)



site ="HKSL"
plt.figure(figsize=(12,6),dpi=120)
plt.subplot()
#enu = getsite_enu("data/"+site+"-GEC-fix.enu")
time,enu,flag = getsite_enu("enufile.pos")

enu_fix = [[] ,[] ,[]]
time_fix = []
for i in range(len(flag)):
    if (flag[i]):
        enu_fix[0].append(enu[0][i])
        enu_fix[1].append(enu[1][i])
        enu_fix[2].append(enu[2][i])
        time_fix.append(time[i])
draw_enu_3part(time_fix,enu_fix,"difference [m]",'g',".",1.5)

enu_float = [[] ,[] ,[]]
time_float = []
for i in range(len(flag)):
    if (not flag[i]):
        enu_float[0].append(enu[0][i])
        enu_float[1].append(enu[1][i])
        enu_float[2].append(enu[2][i])
        time_float.append(time[i])
draw_enu_3part(time_float,enu_float,"difference [m]","#FF4040",".",1.5)

plt.xlabel("Time(epochs)",fontsize=13)
plt.savefig(site+"-enu-fix.png",dpi=120)
plt.show()