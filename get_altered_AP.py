import os.path
import user_voting
import function_utils

def get_altered_AP( mac_address ):
  
    f=open("alter_ap.txt","r")
    altered_ap_=[] #dictionary
    for x in f:
        #make the list
        altered_ap_mac=''
        old_frequency =0
        old_locations=[]
        i=0
        for w in x.split(' '):
            if i==0:
                altered_ap_mac=w.replace(':','')
                if not (altered_ap_mac == mac_address):
                    continue
            elif i==1:
                old_frequency=w

            elif i==2:
                col=w.replace('[','')
                col1=col.replace(']','')
                for c in col1.split(','):
                    c1=c.replace('{','')
                    c2=c1.replace('}','')
                    old_floor=''
                    old_one_location=[]
                    old_RSSI_difference=0.0
                    old_RSSI_averge=0.0
                    j=0
                    for a in c2.split('/'):
                        if j==0: #floor
                            old_floor=a
                        elif j==1: #location
                            a1=a.replace('(','')
                            a2=a1.replace(')','')
                            for b in a2.split(';'):
                                old_one_location.append(float(b))
                        elif j==2: #RSSI difference
                            old_RSSI_difference=float(a)

                        elif j ==3:
                            old_RSSI_averge=float(a)
                        j=j+1
                    inner_dummy=dict({"floor": old_floor, "location": old_one_location, "rssi_diff": old_RSSI_difference, "original_rssi": old_RSSI_averge})
                    old_locations.append(inner_dummy)

            i=i+1
        dummy=dict({"Altered AP MAC": altered_ap_mac, "frequency": old_frequency, "Location":old_locations})

        altered_ap_.append(dummy)
    #print (altered_ap)
    f.close()

    altered_ap = user_voting.user_voting(altered_ap_)
    # break_result = function_utils.Jenks_natural_breaks(altered_ap_, "Altered AP MAC", "frequency")
    # altered_ap = break_result[1]

    #return four things
    #floors=[]
    #location=[]
    #rssi_diff=[]
    #original_rssi=[]
    location=[]

    for i in range(len(altered_ap)):
        #print(altered_ap[i]['floor'])
        if altered_ap[i]['Altered AP MAC'] == mac_address:
            for j in range(len(altered_ap[i]['Location'])):

                dummy=dict({"floor": altered_ap[i]['Location'][j]['floor'], "location": altered_ap[i]['Location'][j]['location'], "rssi_diff":altered_ap[i]['Location'][j]['rssi_diff'], "original_rssi": altered_ap[i]['Location'][j]['original_rssi']})
                location.append(dummy)


    return location
