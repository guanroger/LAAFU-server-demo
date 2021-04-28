import os.path
import user_voting
import function_utils

def get_altered_AP_mac():

    f=open("alter_ap.txt","r")
    altered_ap=[] #dictionary
    for x in f:
        #make the list
        altered_ap_mac=''
        old_frequency =0
        old_locations=[]
        i=0
        for w in x.split(' '):
            if i==0:
                altered_ap_mac=w.replace(':','')
                #print(altered_ap_mac)
            elif i==1:
                old_frequency=w
                #print(old_frequency)

            elif i==2:
                #print(w)
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
                #print(old_locations)

            i=i+1
        dummy=dict({"Altered AP MAC": altered_ap_mac, "frequency": old_frequency, "Location":old_locations})

        altered_ap.append(dummy)
    #print (altered_ap)
    f.close()

    """
    TODO: apply Jenks natural breaks and split it into new ap list and altered ap list
    """
    # break_result = function_utils.Jenks_natural_breaks(altered_ap, "Altered AP MAC", "frequency")
    # altered_and_new_ap_list = break_result[1]
    altered_and_new_ap_list = user_voting.user_voting(altered_ap)
    altered_ap_list = []
    new_ap_list = []
    for ap in altered_and_new_ap_list:
        is_new_ap = True
        for location in ap["Location"]:
            if not(location["original_rssi"] == 0):
                is_new_ap = False
        if is_new_ap:
            new_ap_list.append(ap["Altered AP MAC"])
        else:
            altered_ap_list.append(ap["Altered AP MAC"])
    return {"altered_AP": altered_ap_list, "new_AP": new_ap_list}