import os.path

def get_altered_AP( mac_address ):
        
    f=open("alter_ap.txt","r")
    altered_ap=[] #dictionary
    for x in f:
        #print(x)
        #make the list
        altered_ap_mac=''
        altered_RP_location=[]
        user_location=[]
        unaltered_RP_location=[]
        i=0
        for w in x.split(' '):
            if i==0:
                #print(w)
                altered_ap_mac=w.replace(':','')

            elif i==1:
                #this is the altered RP location
                cor1=w.replace('[','')
                cor=cor1.replace(']','')
                #print(cor)
                for c in cor.split('),('):
                    one_point1=c.replace('(', '')
                    one_point=one_point1.replace(')', '')
                    #print(one_point)
                    corXY=[]
                    for p in one_point.split(','):
                        corXY.append(p)
                    altered_RP_location.append(corXY)
                #print(altered_RP_location)
            
            elif i==2:
                #this is the altered RP location
                cor1=w.replace('[','')
                cor=cor1.replace(']','')
                #print(cor)
                for c in cor.split('),('):
                    one_point1=c.replace('(', '')
                    one_point=one_point1.replace(')', '')
                    #print(one_point)
                    corXY=[]
                    for p in one_point.split(','):
                        corXY.append(p)
                    user_location.append(corXY)
                #print(user_location)

            elif i==3:
                #this is the altered RP location
                cor1=w.replace('[','')
                cor2=cor1.replace('\n','')
                cor=cor2.replace(']','')
                #print(cor)
                for c in cor.split('),('):
                    one_point1=c.replace('(', '')
                    one_point=one_point1.replace(')', '')
                    #print(one_point)
                    corXY=[]
                    for p in one_point.split(','):
                        corXY.append(p)
                    unaltered_RP_location.append(corXY)
                #print(unaltered_RP_location)

            i=i+1
        dummy=dict({"altered ap mac":altered_ap_mac, "altered RP": altered_RP_location, "User locations": user_location, "Unchanged RP": unaltered_RP_location})
        altered_ap.append(dummy)
    #print (altered_ap)
    #print (V)
    f.close()

    #return three things
    changed_RP=[]
    location=[]
    unchanged_RP=[]

    for i in range(len(altered_ap)):
        #print(altered_ap[i]['altered ap mac'])
        if altered_ap[i]['altered ap mac'] == mac_address:


            #construct dictionary
            #changed_RP=altered_ap[i]['altered RP']
            for j in range(len(altered_ap[i]['altered RP'])):
                if altered_ap[i]['altered RP'][j][0] != '':

                    dummy=dict({'x':float(altered_ap[i]['altered RP'][j][0]), 'y':float(altered_ap[i]['altered RP'][j][1])})
                else:
                    dummy=dict({'x':None, 'y':None})
                changed_RP.append(dummy)

            
            #location=altered_ap[i]['User locations']

            for j in range(len(altered_ap[i]['User locations'])):
                if altered_ap[i]['User locations'][j][0] != '':

                    dummy=dict({'x':float(altered_ap[i]['User locations'][j][0]), 'y':float(altered_ap[i]['User locations'][j][1])})
                else:
                    dummy=dict({'x':None, 'y':None})
                location.append(dummy)
            #unchanged_RP=altered_ap[i]['Unchanged RP']

            for j in range(len(altered_ap[i]['Unchanged RP'])):
                if altered_ap[i]['Unchanged RP'][j][0] != '':

                    dummy=dict({'x':float(altered_ap[i]['Unchanged RP'][j][0]), 'y':float(altered_ap[i]['Unchanged RP'][j][1])})
                else:
                    dummy=dict({'x':None, 'y':None})
                unchanged_RP.append(dummy)



    return changed_RP, location, unchanged_RP
