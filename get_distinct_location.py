import os.path
import user_voting
import function_utils


def get_distinct_location(mode):\

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

        altered_ap_.append(dummy)

    f.close()

    altered_ap = user_voting.user_voting(altered_ap_)
    # break_result = function_utils.Jenks_natural_breaks(altered_ap_, "Altered AP MAC", "frequency")
    # altered_ap = break_result[1]

    #return four things
    location=[]
    floor_check=[]
    location_check=[]
    rssi_differnt_check=[]
    original_rssi_check=[]


    for i in range(len(altered_ap)):
        #print(altered_ap[i]['floor'])
        for j in range(len(altered_ap[i]['Location'])):
                    
            dummy=dict({"floor": altered_ap[i]['Location'][j]['floor'], "location": altered_ap[i]['Location'][j]['location'], "rssi_diff":altered_ap[i]['Location'][j]['rssi_diff'], "original_rssi": altered_ap[i]['Location'][j]['original_rssi']})
            location.append(dummy)



    location_unique=[]
    dummy=dict({"floor": location[0]['floor'], "location": location[0]['location'], "rssi_diff":location[0]['rssi_diff'], "original_rssi": location[0]['original_rssi']})
    location_unique.append(dummy)
    floor_check.append(location[0]['floor'])
    location_check.append(location[0]['location'])
    rssi_differnt_check.append(location[0]['rssi_diff'])
    original_rssi_check.append(location[0]['original_rssi'])
    for j in range(1,len(location)):
        can_append=1
        for k in range(len(floor_check)):
            if (location[j]['floor'] != floor_check[k] or
                    location[j]['location'][0] != location_check[k][0] or
                    location[j]['location'][1] != location_check[k][1] or
                    location[j]['rssi_diff'] != rssi_differnt_check[k] or
                    location[j]['original_rssi'] != original_rssi_check[k]):

                continue
            else: 
                can_append=0
                break

        if can_append==1:
            
                dummy=dict({"floor": location[j]['floor'], "location": location[j]['location'], "rssi_diff":location[j]['rssi_diff'], "original_rssi": location[j]['original_rssi']})
                location_unique.append(dummy)
                floor_check.append(location[j]['floor'])
                location_check.append(location[j]['location'])
                rssi_differnt_check.append(location[j]['rssi_diff'])
                original_rssi_check.append(location[j]['original_rssi'])

    location_new_ap = []
    location_altered_ap = []
    for loc in location_unique:
        if(loc['original_rssi'] != 0):
            location_altered_ap.append(loc)
        else:
            location_new_ap.append(loc)

    if mode == 'all_altered_AP':
        return location_altered_ap
    elif mode == 'all_new_AP':
        return location_new_ap
    else:
        return location_unique