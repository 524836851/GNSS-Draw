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

def draw_enu(time,enu,ylabel,color,marker,size):
    x = [i for i in range(len(enu[0]))]
    x = [ i - time[0] for i in time]
    plt.plot(x,enu[0],color='r',marker=marker,lw=0,ms=size,label="E")
    plt.plot(x,enu[1],color='g',marker=marker,lw=0,ms=size,label="N")
    plt.plot(x,enu[2],color='b',marker=marker,lw=0,ms=size,label="U")
    plt.ylabel(ylabel)
    plt.grid()
    plt.legend(loc="upper right")

def draw_trace(x,y,color,marker):
    plt.plot(x,y,color=color,marker=marker,lw=0,ms=1.5)
    plt.plot(x[0],y[0],"r*",ms=10)
    plt.plot(x[-1],y[-1],"b*",ms=10)
    plt.ylabel("N(m)")
    plt.xlabel("E(m)")
    plt.grid()

def draw_enu_3part(time,enu,ylabel,color,marker,size):
    x = [ i for i in range(len(enu[0]))]
    x = [ i-time[0] for i in time]
    plt.subplot(311)
    plt.plot(x,enu[0],color=color,marker=marker,lw=0,label="E",ms=size)
    #plt.plot(x,enu[0],"r.",label="E"size)
    plt.ylabel(ylabel,fontsize=13)
    plt.legend(loc="upper right")
    plt.xlim(xmin=0)
    plt.grid()
    #plt.ylim(-0.04,0.06)
    #plt.yticks(np.arange(-0.04,0.06,0.02),fontsize=13)


    plt.subplot(312)
    plt.plot(x,enu[1],color=color,marker=marker,lw=0,label="N",ms=size)
    plt.ylabel(ylabel,fontsize=13)
    plt.legend(loc="upper right")
    plt.xlim(xmin=0)
    plt.grid()
    #plt.ylim(-0.04,0.06)
    #plt.yticks(np.arange(-0.04,0.06,0.02),fontsize=13)


    plt.subplot(313)
    plt.plot(x,enu[2],color=color,marker=marker,lw=0,label="U",ms=size)
    plt.ylabel(ylabel,fontsize=13)
    plt.legend(loc="upper right")
    plt.xlim(xmin=0)
    plt.grid()
    #plt.ylim(-0.04,0.06)
    #plt.yticks(np.arange(-0.04,0.06,0.02),fontsize=13)



def draw_main():

    ###get all data
    time,enu,flag = getsite_enu(file_input)
    enu_fix = [[] ,[] ,[]]
    time_fix = []
    # get fix
    for i in range(len(flag)):
        if (flag[i]):
            enu_fix[0].append(enu[0][i])
            enu_fix[1].append(enu[1][i])
            enu_fix[2].append(enu[2][i])
            time_fix.append(time[i])
    enu_float = [[] ,[] ,[]]
    time_float = []
    # get float
    for i in range(len(flag)):
        if (not flag[i]):
            enu_float[0].append(enu[0][i])
            enu_float[1].append(enu[1][i])
            enu_float[2].append(enu[2][i])
            time_float.append(time[i])


    ### draw
    # draw one part
    plt.figure(figsize=(12,6),dpi=120)
    draw_enu(time,enu,"difference [m]","g",".",1.5)
    #plt.grid()
    plt.xlabel("Time(epochs)",fontsize=13)
    plt.savefig("enu-one.png",dpi=120)

    # draw three part
    plt.figure(figsize=(12,6),dpi=120)
    draw_enu_3part(time_fix,enu_fix,"difference [m]",'g',".",1.5)
    draw_enu_3part(time_float,enu_float,"difference [m]","#FF4040",".",1.5)
    plt.xlabel("Time(epochs)",fontsize=13)
    plt.savefig("enu_fix.png",dpi=120)

    # draw trace
    plt.figure(figsize=(12,6),dpi=120)
    draw_trace(enu_fix[0],enu_fix[1],"g",".")
    draw_trace(enu_float[0],enu_float[1],"r",".")
    plt.grid()
    plt.savefig("trace.png",dpi=120)

    plt.show()

    ## file count
    with open("count.txt","w") as myfile:
        fix_num = len(enu_fix[0])
        float_num = len(enu_float[0])
        fix_average = [ np.mean(enu_fix[i]) for i in range(3)]
        all_average = [ np.mean(enu[i]) for i in range(3)]

        myfile.write("fix count: "+str(fix_num)+"\n")
        myfile.write("float count: "+str(float_num)+"\n")
        myfile.write("fix ratio: " +"{0:.3f}".format(float(fix_num)/(fix_num+float_num)*100.0)+"%"+"\n")
        myfile.write("fix average[E N U]: " + str(fix_average[0])+ " " + str(fix_average[1]) + " " + str(fix_average[2])+"\n")
        myfile.write("all average[E N U]: " + str(all_average[0])+ " " + str(all_average[1]) + " " + str(all_average[2])+"\n")

if __name__ == "__main__":
    file_input = "enufile.pos"
    file_output = "enu_fix.png"
    draw_main() 
    #count_main()