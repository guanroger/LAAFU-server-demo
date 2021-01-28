import os.path

def get_altered_AP():
    f=open("alter_ap.txt","r")
    altered_ap=[]
    for x in f:
        for w in x.split('\n'):
            if w!='':
                altered_ap.append(w)

    #print (altered_ap)
    #print (V)
    f.close()
    return altered_ap
