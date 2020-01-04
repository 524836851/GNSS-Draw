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
            if (temp[1].find(":") == -1):
                time.append(float(temp[1]))
            else:
                h,m,s = temp[1].split(":")
                time.append(float(h)*3600.0+float(m)*60.0+float(s))
            if (temp[5] == "FLOAT"):
                flag.append(0)
            else:
                flag.append(1)

    return time,enu,flag

def draw_enu(ax,time,enu,marker,size):
    x = [ i for i in time]
    #add y=0
    ax.plot(x,[0]*len(x),color='grey',lw=1.5,ms=0)
    ax.plot(x,enu[0],color='r',marker=marker,lw=0,ms=size,label="E")
    ax.plot(x,enu[1],color='g',marker=marker,lw=0,ms=size,label="N")
    ax.plot(x,enu[2],color='b',marker=marker,lw=0,ms=size,label="U")
    ax.set_xlim(xmin=0,xmax=max(time))
    #plt.grid()
    #ax.legend(loc="upper right")

def draw_trace(x,y,color,marker,lw,ms,begin_end = False):
    plt.plot(x,y,color=color,marker=marker,lw=lw,ms=ms)
    if (begin_end):
        plt.plot(x[0],y[0],"r*",ms=10)
        plt.plot(x[-1],y[-1],"b*",ms=10)
    plt.ylabel("N(m)")
    plt.xlabel("E(m)")
    plt.grid()

def draw_enu_3part(ax,time,enu,color,marker,size,post_lable):

    x = [ i for i in time]
    
    lable_liist = [ l+post_lable for l in ["E","N","U"]]

    for i in range(3):
        ax[i].plot(x,enu[i],color=color,marker=marker,lw=0,label=lable_liist[i],ms=size)
        ax[i].set_ylim(-0.5,0.5)
        ax[i].set_xlim(xmin=0,xmax=max(time))
        #ax[i].legend(loc="upper right")
        ax[i].grid(b=True,axis='both')

        


def draw_main():

    ###get all data
    time,enu_raw,flag = getsite_enu(file_input)
    enu= []
    for j in range(3):
        enu.append([enu_raw[j][i]-ref_pos[j] for i in range(len(enu_raw[j]))])

    enu_fix = [[] ,[] ,[]]
    time_fix = []
    # get fix
    for i in range(len(flag)):
        if (flag[i]):
            enu_fix[0].append(enu[0][i])
            enu_fix[1].append(enu[1][i])
            enu_fix[2].append(enu[2][i])
            time_fix.append(time[i]-time[0])
    enu_float = [[] ,[] ,[]]
    time_float = []
    # get float
    for i in range(len(flag)):
        if (not flag[i]):
            enu_float[0].append(enu[0][i])
            enu_float[1].append(enu[1][i])
            enu_float[2].append(enu[2][i])
            time_float.append(time[i]-time[0])

    time = [ i - time[0] for i in time]
    ### draw

    # draw one part 
    fig1 = plt.figure(figsize=(8,6),dpi=80)
    ax_1 = fig1.add_subplot(1,1,1)
    draw_enu(ax_1,time,enu,".",5)
    ax_1.set_ylabel("differece [m]",fontsize=16)
    ax_1.set_xlabel("Time(s)",fontsize=16)
    ax_1.set_ylim([-0.5,0.5])
    ax_1.set_yticks(np.linspace(-0.5,0.5,5))
    ax_1.tick_params(axis="both",which="major",direction="out",length=8,width=2,labelsize=14)
    ax_1.tick_params(axis="both",which="minor",direction="out",length=4,width=1)
    ax_1.grid(b=True,axis="both")
    ax_1.minorticks_on()
    fig1.savefig(out_enu1,dpi=120)
    fig1.legend(loc="upper center",fontsize="large",ncol=3,borderaxespad=2.0,edgecolor="white")


    # draw three part
    fig2 = plt.figure(figsize=(12,6),dpi=80)
    ax = fig2.subplots(3,1,sharex=True,sharey=True)
    draw_enu_3part(ax,time_float,enu_float,"#FFB90F",".",4,"_float")
    draw_enu_3part(ax,time_fix,enu_fix,'g',".",4,"_fix")
    fig2.text(0.5,0.02,"Times[s]",ha="center",fontsize=15)
    fig2.text(0.04,0.5,"Diff[m]",va="center",rotation="vertical",fontsize=15)
    fig2.legend(loc="upper center",fontsize="medium",ncol=6)
    fig2.savefig(out_enu3,dpi=120)


    # draw trace
    plt.figure(figsize=(12,6),dpi=80)
    draw_trace(enu[0],enu[1],"grey",".",0.5,0)
    draw_trace(enu_fix[0],enu_fix[1],"g",".",0,6.5,True)
    draw_trace(enu_float[0],enu_float[1],"#FFB90F",".",0,6.5)
    plt.grid()
    plt.savefig(out_trace,dpi=120)

    ## file count
    with open(out_count,"w") as myfile:
        fix_num = len(enu_fix[0])
        float_num = len(enu_float[0])
        fix_average = [ np.mean(enu_fix[i]) for i in range(3)]
        all_average = [ np.mean(enu[i]) for i in range(3)]

        myfile.write("fix count: "+str(fix_num)+"\n")
        myfile.write("float count: "+str(float_num)+"\n")
        myfile.write("fix ratio: " +"{0:.3f}".format(float(fix_num)/(fix_num+float_num)*100.0)+"%"+"\n")
        myfile.write("fix average[E N U]: " + str(fix_average[0])+ " " + str(fix_average[1]) + " " + str(fix_average[2])+"\n")
        myfile.write("all average[E N U]: " + str(all_average[0])+ " " + str(all_average[1]) + " " + str(all_average[2])+"\n")

    plt.show()

if __name__ == "__main__":
    #file_path = "/Users/lhb/Desktop/SGG/WHUSGG/Plot/GNUT/Python-Draw/rtk/"
    #file_path = "/Users/lhb/Desktop/SGG/WHUSGG/Data/20181210-gnutdata/ppp-data/calculation example/"
    file_path = "./"
    file_input = file_path + "enufile.pos"
    #file_input = file_path + "xyzfile2.pos"
    #file_output = file_path + "enu_fix.png"
    out_trace = file_path + "trace.png"
    out_enu3 = file_path + "enu3.png"
    out_enu1 = file_path + "enu1.png"
    out_count = file_path + "count.txt"

    ref_pos = [0,0,0]
    draw_main() 
    #count_main()``