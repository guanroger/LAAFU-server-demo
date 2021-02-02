import os.path

def get_altered_AP_mac():
    f=open("alter_ap.txt","r")
    altered_ap_list=[]
    for x in f:
        for w in x.split('\n'):
            i=0
            for z in w.split(':'):
                if z != '':
                    if i==0:
                        altered_ap_list.append(z)
                    i+=1

    #print (altered_ap_list)
    #print (V)
    f.close()
    return altered_ap_list