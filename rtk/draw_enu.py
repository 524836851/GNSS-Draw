#-*- coding-f:utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np

def getsite_enu(filename):
    enu=[[],[],[]]
    with open(filename,"r") as myfile:
        for i in myfile:
            if (i[0] == "%"):
                continue
            temp = i.split()
            enu[0].append(float(temp[2]))
            enu[1].append(float(temp[3]))
            enu[2].append(float(temp[4]))
    return enu

def draw_enu(enu,ylabel):
    x = [i for i in range(len(enu[0]))]
    plt.plot(x,enu[0],color='r',label="E")
    plt.plot(x,enu[1],color='g',label="N")
    plt.plot(x,enu[2],color='b',label="U")
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend(loc="upper right")
    #plt.ylim(-0.04,0.06)
    #plt.yticks(np.arange(-0.04,0.06,0.02))


site ="HKWS"
plt.figure()
plt.subplot()
#enu = getsite_enu("HKWS-GEC-float.enu")
enu = getsite_enu("enufile.pos")
draw_enu(enu,"difference [m]")

#plt.figure(1,dpi=120)
#plt.subplot(411)
#enu = getsite_enu("HKOH-G-float.enu")
#draw_enu(enu,"G(m)")
#
#plt.subplot(412)
#enu = getsite_enu("HKOH-E-float.enu")
#draw_enu(enu,"E(m)")
#
#plt.subplot(413)
#enu = getsite_enu("HKOH-C-float.enu")
#draw_enu(enu,"C(m)")
#
#plt.subplot(414)
#enu = getsite_enu("HKOH-GEC-float.enu")
#draw_enu(enu,"GEC(m)")
#
#plt.yticks(np.arange(-0.05,0.05,0.01))

plt.xlabel("Time(epochs)")

plt.savefig(site+"-enu.png")
plt.show()