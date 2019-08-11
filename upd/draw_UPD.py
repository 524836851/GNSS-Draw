#-*- coding-f:utf-8 -*-

import math
import matplotlib.pyplot as plt
import numpy as np

def resize(number):
    if (number < -0.5):
        number+=1
    elif (number > 0.5):
        number -=1
    
    return number

def read_wldata_oneday(filename):
    mapsat_wl = {}
    with open(filename) as wlfile:
        for i in wlfile:
            if i[0] != " ":
                continue
            temp = i.split()
            sat = temp[0]
            value = float(temp[1])
            mapsat_wl[sat] = resize(value)
    
    return mapsat_wl

def read_wldata_ndays(filelist, doylist,satsys="G",satlist = None):
    """
    read the wide-lane data from n days 
    """

    # default satlist is all sat list 
    # TODO:define the satlist in gnss_sat.py
    if not satlist:
        satlist = []
        for i in range(1, 33):
            if i != 4:
                satlist.append(f"G{i:02}")

    data = {sat:{doy:0.0 for doy in doylist} for sat in satlist if sat[0] == satsys}
                

    # read all file
    for f,doy in zip(filelist,doylist):
        wldata = read_wldata_oneday(f)

        for sat in wldata.keys():
            if sat in data:
                data[sat][doy] = wldata[sat]

    # nomallize
    for sat in satlist:
        ref_value = None
        for doy in doylist:
            if data[sat][doy] == 0.0:
                continue
            if not ref_value:
                ref_value = data[sat][doy]

            data[sat][doy] = ref_value + resize(data[sat][doy]-ref_value)


    return data 



def read_nldata(filename):
    with open(filename) as nlfile:
        hour = 0.0
        mapnl = {}
        for i in nlfile:
            temp = i.split()
            if temp[0] == "EPOCH-TIME":
                hour = float(temp[2])/3600.0
                continue
            if (i[0] != " "):
                continue
            sat = temp[0]
            sat_data = mapnl.setdefault(sat,{})
            sat_data[hour]=resize(float(temp[1]))
            
    return mapnl
            


def draw_8sat(sat_list,allsat_value):
    color = ["b","g","r","c","m","y","k","#FFA500"]
    style = ["o","v","^","<",">","s","*","d"]

    doy_list = list(allsat_value[sat_list[0]].keys())
    for i in range(len(sat_list)):
        value = allsat_value[sat_list[i]].values()
        x = allsat_value[sat_list[i]].keys()
        plt.plot(x, value, color=color[i],lw=2.5 ,marker=style[i], label=sat_list[i])
        #plt.plot(x,value,color=color[i], marker ='-.')

    plt.xlabel("Day of Year", fontsize=13)
    plt.ylabel("WL UPD(Cycle)", fontsize=13)
    plt.ylim(-0.6,0.6)
    plt.xlim(doy_list[0]-1,doy_list[-1]+5)
    #plt.xticks(x,[str(i) for i in x],fontsize=13)
    plt.yticks(np.arange(-0.6,0.6,0.2),fontsize=13)
    plt.legend(loc="upper right")


def draw_wl_ndays(wldata,doylist,save_dir="."):

    sat_list = list(wldata.keys())
    ## draw row * col pictures in one png
    count = 8 
    col = 2 
    row =  math.ceil(len(sat_list) / float(col) / float(count))
    sat_sys = sat_list[0][0]

    plt.figure(figsize=(16,8),dpi=100)
    for i in range(row * col):
        plt.subplot(row, col, i + 1)
        sats = [sat_list[i] for i in range(i*count,(i+1)*count) if i < len(sat_list)]
        draw_8sat(sats,wldata)
   
    plt.savefig(f"wl_UPD_{len(doylist)}_day_"+sat_sys,dpi=120)
    plt.show()


    
 

def compute_wl():
    mapwl_allday= {}
    for i in range(14, 20):
        filename = "upd_wl_20190" + str(i) + "_GEC"
        mapwl_1day =read_wldata_oneday(filename)
        for sat in mapwl_1day:
            sat_wldata = mapwl_allday.setdefault(sat, [])
            sat_wldata.append(mapwl_1day[sat])

    
    sat_sys = "E"
    Max_std = ["",0.0]
    Max_diff = ["",0.0]
    with open("wl_data_"+sat_sys+".txt", "w") as myfile:
        myfile.write("Sat name  Max-Min STD \n")

        sat_list = list(mapwl_allday.keys())

        for sat in sat_list:
            if sat[0] != sat_sys:
                continue
            diff = max(mapwl_allday[sat]) - min(mapwl_allday[sat])
            std = np.std(mapwl_allday[sat],ddof=1)
            if (diff > Max_diff[1]):
                Max_diff[0] = sat
                Max_diff[1] = diff
            if (std > Max_std[1]):
                Max_std[0] = sat 
                Max_std[1] = std
            myfile.write(sat + " " + "{0:.4f}".format(diff) +" "+"{0:.4f}".format(std)+"\n")

        myfile.write("Max diff:"+ Max_diff[0]+"\n")
        myfile.write("Max std:" + Max_std[0]+"\n")
        
def compute_nl():
    #get data
    mapnl = read_nldata("upd_nl_2019014_GEC")
    
    sat_list = mapnl.keys()
    sat_sys = "G"
    sat_list = [sat for sat in sat_list if sat[0] == sat_sys]
    sat_list = sorted(sat_list)

    Max_diff= ["",0.0]
    Max_std = ["",0.0]
    list_std = [ ]
    with open("nl_data_"+".txt","w") as nlfile:
        nlfile.write("Sat_name Max-Min std\n")
        for sat in sat_list:
            if (sat in ("G26")):
                continue
            value = list(mapnl[sat].values())
            diff = max(value) - min(value)
            std = np.std(value,ddof=1)
            list_std.append(std)

            if (diff > Max_diff[1]):
                Max_diff[0] = sat
                Max_diff[1] = diff
            if (std > Max_std[1]):
                Max_std[0] = sat
                Max_std[1] = std

            nlfile.write(sat+" "+"{0:.4f}".format(diff)+" "+"{0:.4f}".format(std)+"\n")
        nlfile.write("Max diff:"+Max_diff[0]+"\n")
        nlfile.write("Max std:"+Max_std[0]+"\n")
        nlfile.write("mean std:"+"{0:.4f}".format(np.std(list_std,ddof=1)))

        




def draw_1sat_nl(sat_list,allnl):
    color = ["r","g","b","c","m","y","k"]
    for i in range(len(sat_list)):
        sat_data = allnl[sat_list[i]]
        x = list(sat_data.keys())
        y = [sat_data[i] for i in x]
        plt.plot(x,y,color=color[i],lw=3,label=sat_list[i])


    

def draw_nl(nldata):

    #sat_list_G = ["G13","G15","G20","G21","G24","G29"]
    sat_list_G = ["G06"]
    sat_list_E = ["E03","E05","E09","E18","E25"]
    sat_list_C = ["C06","C07","C08","C09"]


    plt.figure(figsize=(12,6),dpi=120)
    plt.subplot(111)

    draw_1sat_nl(sat_list_G,nldata)
    plt.ylim(-1,0.4)
    plt.yticks(np.arange(-1,0.4,0.2),fontsize=13)

    plt.xlabel("Time(Hours)",fontsize=13)
    plt.ylabel("NL UPD(Cycles)",fontsize=13)

    plt.legend()
    plt.grid()
    plt.savefig("NL_DATA_C.png",dpi=120)
    plt.show()


if __name__ == "__main__":
    #draw_wl_7days()
    #compute_wl()
    #draw_nl()
    compute_nl()