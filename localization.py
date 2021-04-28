import os.path
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import fingerprint_utils
import whereami_utils
import logging

logger = logging.getLogger('app.sub')

'''
functions and class
'''

class ReferencePoint:
      def __init__(self, location, fingerprint_A, fingerprint_V, distance=0, weight=0):
        self. distance= distance
        self. location= [location[i] for i in range(len(location))]
        self. fingerprint_A= [fingerprint_A[i] for i in range(len(fingerprint_A))]
        self. fingerprint_V= [fingerprint_V[i] for i in range(len(fingerprint_V))]
        self. weight = weight

def cosine(Fingerprint_Address, Fingerprint_F, Vi_MAC_address, Vi):
    Common=list(set(Fingerprint_Address) and set(Vi_MAC_address))
    if (Common[0]==0):
        Common.remove(0)
    #print(Common)
    
    Fingerprint_V_Common=[]
    for k in range(len(Fingerprint_Address)):
        if Fingerprint_Address[k] in Common:
            #print(Fingerprint_Address[k])
            Fingerprint_V_Common.append(float(Fingerprint_F[k]))

    #print(Fingerprint_V_Common)

    Vi_V_Common=[]
    for k in range(len(Vi_MAC_address)):
        if Vi_MAC_address[k] in Common:
            #print(Vi_MAC_address[k])
            Vi_V_Common.append(Vi[k])

    #print(Vi_V_Common)

    AdotB=0
    ASquareSum=0
    BSquareSum=0

    for k in range(len(Fingerprint_V_Common)):
        AdotB += Fingerprint_V_Common[k]*Vi_V_Common[k]
    #print (AdotB)

    for k in range (len(Fingerprint_F)):
        ASquareSum+=math.pow(float(Fingerprint_F[k]),2)
    #print (ASquareSum)    
    
    for k in range(len(Vi)):
        BSquareSum+=math.pow(Vi[k],2)
    #print(BSquareSum)

    #print (AdotB/(math.sqrt(ASquareSum)*math.sqrt(BSquareSum)))
    return (AdotB/(math.sqrt(ASquareSum)*math.sqrt(BSquareSum)))


def distance(x1, y1, x2, y2):
    return math.sqrt(math.pow(x1-x2,2) + math.pow(y1-y2,2))
     

'''
get the data from the file
'''
def localization(json_example):
    logger.debug("test1")
    logger.debug("test2")
    '''
    #RP location
    f= open("p_all.txt", "r")
    RP_location=[]
    for x in f:
        dummy=[]
        i=0
        for w in x.split(","):
            dummy.append(w)
            i=i+1
            if i==2:
                RP_location.append(dummy)
                break
    #print(RP_location)
    f.close()
    
    # fingerprint
    f= open("p_all.txt", "r")
    Fingerprint_A=[]
    Fingerprint_V=[]
    for x in f:
        i=0
        dummy_A=[]
        dummy_V=[]
        for a in x.split(" "):
            if i!=0:
                s=a.split(":")
                dummy_A.append(s[0])
                dummy_V.append(s[1].split(",")[0])
            i=i+1

        Fingerprint_A.append(dummy_A)
        Fingerprint_V.append(dummy_V)
    #print(Fingerprint_A[0])
    #print(Fingerprint_V[0])
    f.close()
    
    # A(MAC address) & V(RSSI vector) from fast detection
    f=open("mac_rssi.txt","r")
    A=[]
    V=[]
    for x in f:
        for w in x.split():
            a=w.split(":")
            A.append(a[0])
            V.append(a[1])
    #print (A)
    #print (V)
    f.close()   
    '''
    
    RP_location, Fingerprint_A, Fingerprint_V, A, V , floor = fingerprint_utils.load_fingerprint(json_example)
    #print(Fingerprint_A)
    #print(floor)
    '''
    TODO: filter new AP (element in A not in Fingerprint_A, also remove from V) and store it in a array
    '''
    to_be_deleted_idxs = []
    new_ap_list = []
    fingerprint_ap_list = set([ap for ap_list in Fingerprint_A for ap in ap_list])
    for idx, mac in enumerate(A):
        if mac not in fingerprint_ap_list:
            to_be_deleted_idxs.append(idx)
            new_ap_list.append({'mac': mac, 'rssi': V[idx]})
    for idx in sorted(to_be_deleted_idxs, reverse=True):
        A.pop(idx)
        V.pop(idx)
    
    '''
    start of the code
    '''
    #this is the setup number
    #can change later
    #generate M subsets 
    #choose the best K RP
    #choose the nearest Q RP
    #bamdwidth b for Gaussian Kernel
    M=30
    K=8
    Q=8
    b=0.02
    RP_radius=10
    #the max of K is the total number of fingerprint


    APindex=[]
    for i in range(len(A)):
        dummy=dict({"MAC_address":A[i], "index": i})
        APindex.append(dummy)    
    #print (APindex)

    RSS=[] #has mac address and the rssi, detected ap address and its RSSI
    DetectedAP=[] #only has mac address
    for i in range(len(V)):
        if V[i]!=0:
            dummy=dict({"MAC_address":A[i], "RSSI": V[i]})
            RSS.append(dummy)
            DetectedAP.append(A[i])

    #print(RSS)
    #print(DetectedAP)


    #generagte M subset
    #with subsets vector 
    #subsets_old =[[dictionary of detected AP1,dictionary of detected AP2, dictionary of detected AP3, ...], []]
    subsets_number=[]
    subsets_number_bin=[]
    subsets=[] # only has MAC address
    subsets_RSSI=[] #only has RSSI vector 
    '''
    #generate M subset with size>3
    fulfillM=False

    while(not fulfillM):
        one_subset=[]
        one_subset_RSSI=[]

        #add AP inside
        for j in range(len(DetectedAP)):
            coin = random.randint(1, 2)
            if coin ==1: #if it is the head
                one_subset.append(DetectedAP[j])
                one_subset_RSSI.append(int(RSS[j]['RSSI']))
            else: #if it is not the head dont do anything

                break

        #delete different constraint

        if (len(one_subset)>=3):
            if (one_subset not in subsets):
                subsets.append(one_subset)
                subsets_RSSI.append(one_subset_RSSI)
        
        if (len(subsets)>=M):
            fulfillM=True

    '''
    """
    TODO: add a counter to break the while loop
    """
    fulfillM=False
    total_prop_number_of_subsets = int(math.pow(2, len(DetectedAP))-1)
    iter_ctr = 0
    #print(total_prop_number_of_subsets)

    while(not fulfillM and not(iter_ctr > M*10)):
        number_of_subset=random.randint(0, total_prop_number_of_subsets)
        #print(number_of_subset)
        binary=bin(number_of_subset)[2:].zfill(len(DetectedAP))
        #print(binary)


        
        #check whether the lenth>=3
        #print(binary.count("1"))
        if (binary.count("1")>=3):
            if (number_of_subset not in subsets_number):
                subsets_number.append(number_of_subset)    
                subsets_number_bin.append(binary)

        if (len(subsets_number)>=M):
            fulfillM= True
        iter_ctr += 1

    if len(subsets_number)==0:
        subsets_number.append(total_prop_number_of_subsets)
        subsets_number_bin.append(bin(total_prop_number_of_subsets)[2:])
    print(subsets_number)
    print(subsets_number_bin)
    #generate subset according to subset number


    for i in range(len(subsets_number_bin)):
        one_subset=[]
        one_subset_RSSI=[]
        for j in range(len(subsets_number_bin[i])):
            #print(subsets_number_bin[i][j])
            if (subsets_number_bin[i][j]=='1'):
                one_subset.append(DetectedAP[j])
                one_subset_RSSI.append(int(RSS[j]['RSSI']))
        subsets.append(one_subset)
        subsets_RSSI.append(one_subset_RSSI)



    print("subsets MAC: ",subsets)
    print("subsets MAC with RSSI: ",subsets_RSSI)




    locations = [[0 for j in range(2)] for i in range(len(subsets))] 
    locations_id= [i for i in range(len(subsets))]

    for i in range (len(subsets)):
        #get one of the subsets
        one_subset=subsets[i] # list of MAC address in one subset
        Vi=[]
        Vi_MAC_address=[]
        for j in range(len(one_subset)):
            for k in range(len(RSS)):
                if one_subset[j] == RSS[k].get("MAC_address"):
                    Vi.append(int(RSS[k].get("RSSI")))
                    Vi_MAC_address.append( RSS[k].get("MAC_address"))
                else:
                    Vi.append(0)
                    Vi_MAC_address.append(0)
        #print(Vi)
        #print(Vi_MAC_address)
        #print(Fingerprint_A)

        RPs=[]
        for j in range(len(Fingerprint_A)):
            #print(Fingerprint_A[j])
            #print(Fingerprint_V[j])
            #print(Vi)
            #print(Vi_MAC_address)
            RP=ReferencePoint(RP_location[j], Fingerprint_A[j], Fingerprint_V[j], 1 - cosine(Fingerprint_A[j],Fingerprint_V[j], Vi_MAC_address, Vi), cosine(Fingerprint_A[j], Fingerprint_V[j], Vi_MAC_address, Vi))
            #print(RP.location)
            #print(RP.distance)
            #print(RP.weight)
            RPs.append(RP)

        #for k in range(len(RPs)):
        #    print(RPs[k].distance)

        totalWeight=0
        for k in range(K):
            lowestDistance=RPs[k].distance
            for j in range(k+1,len(RPs)):
                if (RPs[j].distance <lowestDistance):
                    temp=RPs[k]
                    RPs[k]=RPs[j]
                    RPs[j]=temp
                    lowestDistance=RPs[k].distance
            totalWeight+=RPs[k].weight

        #print("/n")

        #for k in range(len(RPs)):
        #    print(RPs[k].distance)

        #print("end")

        for k in range(K):
            weight=0
            if totalWeight==0:
                weight=1/K
            else:
                weight = RPs[k].weight/totalWeight

            #print(float(RPs[k].location[0])*weight)
            locations[i][0] += float(RPs[k].location[0]) * weight
            locations[i][1] += float(RPs[k].location[1]) * weight
        
    print("estimated locations: ",locations) 




    #APC algorithm 
    sim=np.array([[0 for j in range(len(locations))]for i in range (len(locations))], dtype= float)
    for i in range(len(sim)):
        for j in range(len(sim[i])):
            #calculate the educlidean distance between locations
            xSquare=math.pow(locations[i][0]-locations[j][0],2)
            ySquare=math.pow(locations[i][1]-locations[j][1],2)
            #sim[i][j]=math.sqrt(xSquare+ySquare)
            sim[i][j]=-(xSquare+ySquare)
            #sim[i][j]=-math.exp(math.sqrt(xSquare+ySquare))

    #print("sim: ",sim)

    #availablity matrix initially set to 0 M*M
    avail=np.array([[0 for j in range(len(locations))]for i in range (len(locations))], dtype=float)

    #responsibility matrix M*M
    res =np.array([[0 for j in range(len(locations))]for i in range (len(locations))], dtype= float)

    #print(avail)
    #initialize
    last_exemplars=np.array([])
    last_sol=np.array([])

    #return the location array with centriod id
    location_with_centriod_id=[]
    damping=0

    for i in range (200):
        print("interation: ", i)

        #res update
        for j in range(len(locations)):
            for k in range(len(locations)):
                v = sim[j, :] + avail[j, :]
                v[k]= -math.inf
                #v[j]= -math.inf
                #if j==0 and k==0:
                #    print("for debug use: ",v)
                #new_res[j, k] = damping * res[j, k] + (1-damping) * (sim[j, k] - np.max(v))
                res[j, k] = damping * res[j, k] + (1-damping) * (sim[j, k] - np.max(v))

        #print("res: ",new_res)

        
        #avil update
        for j in range(len(locations)):
            for k in range(len(locations)):
                a = np.array(res[:, k]) # Select column k
                #print (res[:, k])
                # All indices but the diagonal
                if j != k:
                    a[j] = -math.inf
                    a[k] = -math.inf
                    a[a < 0] = 0
                    #print (a)
                    #print(res[k, k] + a.sum())
                    #new_avail[j, k] = damping * avail[j,k] + (1-damping) * min(0, res[k, k] + np.sum(a))
                    avail[j, k] = damping * avail[j,k] + (1-damping) * min(0, res[k, k] + np.sum(a))
                # The diagonal
                else:
                    a[k] = -math.inf
                    a[a < 0] = 0
                    #print (a)

                    #new_avail[k, k] = damping * avail[k,k] + (1-damping) * np.sum(a)
                    avail[k, k] = damping * avail[k,k] + (1-damping) * np.sum(a)
        
        #print("avail: ",new_avail)

        
    
        sol = res+avail
        #print(sol)
        
        print ("last exemplars: ",last_exemplars)
        #print ("sol: ",sol)

        exemplars = np.unique(np.argmax(sol, axis=1))
        print("label: ", np.argmax(sol, axis=1))
        print("exemplars: ",exemplars)

        


        #if the location is the same as the past location
        if  last_exemplars.size == exemplars.size and last_exemplars.all()==exemplars.all():
            #stop

            for j in range(len(np.argmax(sol, axis=1))):
                location_with_centriod_id.append(np.argmax(sol, axis=1)[j])
                
            break

        last_sol = sol
        last_exemplars = exemplars

        

    print(location_with_centriod_id)

    
    #High average signal similarity
    cluster_centorid=[]
    centorid_ID=[]
    for i in range(len(exemplars)):
        cluster_centorid.append(locations[exemplars[i]])
        centorid_ID.append(locations_id[exemplars[i]])

    #print(cluster_centorid)

    clustering=[]
    clustering_ID=[]
    for i in range(len(exemplars)):
        one_cluster=[]
        one_cluster_ID=[]
        for j in range(len(location_with_centriod_id)):
            if location_with_centriod_id[j]==exemplars[i]:
                one_cluster.append(locations[j])
                one_cluster_ID.append(locations_id[j])
        clustering.append(one_cluster)
        clustering_ID.append(one_cluster_ID)


    #create list if dicetionary
    cluster=[]
    cluster_ID=[]
    for i in range(len(cluster_centorid)):
        dummy1=dict({"centorid": cluster_centorid[i], "cluster": clustering[i]})
        dummy2=dict({"centorid": centorid_ID[i], "cluster": clustering_ID[i]})
        cluster.append(dummy1)
        cluster_ID.append(dummy2)

    print(cluster)
    print(cluster_ID)


    #find Q nearest location of RPs

    Qc=[]
    for i in range(len(cluster)):

        subset_in_one_cluster_MAC=[]
        subset_in_one_cluster_RSSI=[]
        #find the RSSI vector that generate each location
        for j in range(len(cluster[i]['cluster'])):
            #find the index of each location in cluster in the estimated location
            ind=locations.index(cluster[i]['cluster'][j])
            #print(ind)
            subset_in_one_cluster_MAC.append(subsets[ind])
            subset_in_one_cluster_RSSI.append(subsets_RSSI[ind])

        #print(subset_in_one_cluster_MAC)
        #print(subset_in_one_cluster_RSSI)

        consine_matrix=[[0 for i in range(Q)] for j in range(len(subset_in_one_cluster_MAC))]

        #make the vector of each subsets 
        #we have the MAC address of subsets

        X2=cluster[i]['centorid'][0]
        Y2=cluster[i]['centorid'][1]
        #print (X2)
        #print (Y2)
        

        RPs=[]
        for j in range(len(Fingerprint_A)):
            #print(Fingerprint_A[j])
            #print(Fingerprint_V[j])
            #print(Vi)
            #print(Vi_MAC_address)
            RP=ReferencePoint(RP_location[j], Fingerprint_A[j], Fingerprint_V[j], distance(float(RP_location[j][0]), float(RP_location[j][1]), X2, Y2), 0)
            #print(RP.location)
            #print(RP.distance)
            #print(RP.weight)

            #calculate the consine matrix 
            RPs.append(RP)

        
        #find the nearest Q RPs

        for k in range(Q):
            lowestDistance=RPs[k].distance
            for j in range(k+1,len(RPs)):
                if (RPs[j].distance <lowestDistance):
                    temp=RPs[k]
                    RPs[k]=RPs[j]
                    RPs[j]=temp
                    lowestDistance=RPs[k].distance


        #calculate the cosine
        for i in range(len(consine_matrix)):
        
            for j in range (len(consine_matrix[i])):
                #print("RPs",RPs[j].fingerprint_A)
                #print("Subset:",subsets[i])
                #if i==0 and j==0:
                #    print(list(set(RPs[j].fingerprint_A) and set(subsets[i])) )
                consine_matrix[i][j]=cosine(RPs[j].fingerprint_A, RPs[j].fingerprint_V, subset_in_one_cluster_MAC[i], subset_in_one_cluster_RSSI[i])

        #print(consine_matrix)

        #calculate the Qc 
        totalCosine=0
        for j in range(len(consine_matrix)):
            for k in range(len(consine_matrix[j])):
                totalCosine=totalCosine+consine_matrix[j][k]

        Qc_for_one_cluster=totalCosine*(1/(len(consine_matrix)*len(consine_matrix[0])))
        Qc.append(Qc_for_one_cluster)
        #print(totalCosine)
        #print(Q*len(cluster[i]['cluster']))
    print("Qc: ",Qc)


    #Large cluster size
    Vc=[]
    #find the minimum number of cluster size

    Cmin=len(cluster[0]['cluster'])
    for i in range(len(cluster)):
        if (len(cluster[i]['cluster'])<Cmin):
            Cmin=len(cluster[i]['cluster'])

    for i in range(len(cluster)):
        C=len(cluster[i]['cluster'])
        Vc.append( math.exp(-(1 / ( 2 * math.pow(b,2) ) ) * ( math.pow(C - Cmin, 2) )))
        #print(type(Vc[i]))

    print("Vc: ",Vc)

    #calculate the score

    scores=[Qc[i]-Vc[i] for i in range(len(Qc))]
    print("scores of each cluster: ",scores)
    maximum_score_id=scores.index(max(scores))
    #the location detected in the end is the maximum score location
    final_estimation=cluster[maximum_score_id]['centorid']
    final_estimation_ID=cluster_ID[maximum_score_id]['centorid']
    print("final estimation:",final_estimation)
    print("ID :",final_estimation_ID )

    #5.3
    #altered ap part
    dense_subsets=[]
    #print(cluster[maximum_score_id]['cluster'])
    print(cluster_ID[maximum_score_id]['cluster'])
    for j in range(len(cluster_ID[maximum_score_id]['cluster'])):
        dummy=subsets[cluster_ID[maximum_score_id]['cluster'][j]]
        dense_subsets.append(dummy)
    print("dense subsets: ",dense_subsets)

    unique=[]
    for i in range(len(dense_subsets)):
        for j in range(len(dense_subsets[i])):
            if dense_subsets[i][j] not in unique:
                unique.append(dense_subsets[i][j])

    print("unique ",unique)
    frequency=[0 for i in range (len(unique))]
    for i in range(len(dense_subsets)):
        for j in range(len(dense_subsets[i])):
            frequency[unique.index(dense_subsets[i][j])]+=1

    #print(frequency)

    #make the dict
    AP_freq=[]
    for i in range(len(unique)):
        dummy=dict({"MAC": unique[i], "frequency": frequency[i]})
        AP_freq.append(dummy)
    print("AP frequency in dense cluster: ",AP_freq)

    #ordered by freq
    for i in range(len(AP_freq)):
        min_f=AP_freq[i]['frequency']
        for j in range(i+1,len(AP_freq)):
            if (AP_freq[j]['frequency']<min_f):
                    temp=AP_freq[i]
                    AP_freq[i]=AP_freq[j]
                    AP_freq[j]=temp
                    lowestDistance=AP_freq[i]['frequency']

    #print(AP_freq)

    SDCM=np.array([0 for i in range(len(AP_freq)+1)],dtype=float)
    SDCM_class_freq=np.array([[0 for j in range(2)]for i in range(len(AP_freq)+1)],dtype=float)
    classes=[]
    #range(len(AP_freq)+1)
    for i in range(len(AP_freq)+1):
        dummy=[]
        class_A=[ AP_freq[j] for j in range(0,i)]
        dummy.append(class_A)
        f_mean_in_A=0
        if len(class_A)!= 0:
            f_sum_in_A=0
            for j in range(len(class_A)):
                f_sum_in_A+=class_A[j]['frequency']
            f_mean_in_A=f_sum_in_A/len(class_A)


        class_A_sum=0
        for j in range(len(class_A)):
            class_A_sum=math.pow((class_A[j]['frequency']-f_mean_in_A),2)

        class_B=[AP_freq[j] for j in range(i,len(AP_freq))]
        dummy.append(class_B)
        f_mean_in_B=0
        if len(class_B)!= 0:
            f_sum_in_B=0
            for j in range(len(class_B)):
                f_sum_in_B+=class_B[j]['frequency']
            f_mean_in_B=f_sum_in_B/len(class_B)


        class_B_sum=0
        for j in range(len(class_B)):
            class_B_sum=math.pow((class_B[j]['frequency']-f_mean_in_B),2)
                

        SDCM[i]=class_A_sum+class_B_sum
        SDCM_class_freq[i][0]=class_A_sum
        SDCM_class_freq[i][1]=class_B_sum
        classes.append(dummy)


    print("SDCM: ",SDCM)
    #print("SDCM each freq: ",SDCM_class_freq

    lowest_SDCM=SDCM.argmin()
    lowest_class=SDCM[lowest_SDCM].argmin()
    print("lowest",len(classes))
    alter_AP=[]
    for i in range(len(classes[int(lowest_SDCM)][int(lowest_class)])):
        alter_AP.append(classes[int(lowest_SDCM)][int(lowest_class)][i]['MAC'])

    # altered ap size is 0--> means that many of the fingerprint has changed

    print("altered AP: ", alter_AP)

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
    print (altered_ap)
    f.close()

    #append new data
    #all altered ap for check
    All_altered_ap=[]
    for i in range(len(altered_ap)):
        All_altered_ap.append(altered_ap[i]['Altered AP MAC'])
    print("old altered AP", All_altered_ap)

    # do the natual break for the ap
    # firtly append the old one
    all_altered_ap_frequency_map=[] # dictionary
    '''
    for i in range(len(All_altered_ap)):
        index_of_mac = next((index for (index, d) in enumerate(altered_ap) if d["Altered AP MAC"] ==  All_altered_ap[i]), None)
        dummy=dict({"Altered AP MAC": All_altered_ap[i],"Frequency": altered_ap[index_of_mac]['frequency'], "RSSI average": 0.0, "RSSI difference": 0.0})
        all_altered_ap_frequency_map.append(dummy)
    altered_AP_new=[]
    '''
    # add the new altered ap
    for i in range(len(alter_AP)):
        if alter_AP[i] not in All_altered_ap:
            dummy=dict({"Altered AP MAC": alter_AP[i],"Frequency": 1, "RSSI average":0.0, "RSSI difference": 0.0})
            all_altered_ap_frequency_map.append(dummy)


        else:
            index_of_mac = next((index for (index, d) in enumerate(altered_ap) if d["Altered AP MAC"] == alter_AP[i]), None)
            fre=int(altered_ap[index_of_mac]["frequency"])
            fre+=1
            dummy=dict({"Altered AP MAC": alter_AP[i],"Frequency": fre, "RSSI average":0.0, "RSSI difference": 0.0})
            all_altered_ap_frequency_map.append(dummy)


    print("all altered",all_altered_ap_frequency_map)


    #choose the highest among two
    '''
    for i in range(len(all_altered_ap_frequency_map)):
        min_f=int(all_altered_ap_frequency_map[i]['Frequency'])
        for j in range(i+1,len(all_altered_ap_frequency_map)):
            if (int(all_altered_ap_frequency_map[j]['Frequency'])<min_f):
                    temp=all_altered_ap_frequency_map[i]
                    all_altered_ap_frequency_map[i]=all_altered_ap_frequency_map[j]
                    all_altered_ap_frequency_map[j]=temp

    print("sorted: " ,all_altered_ap_frequency_map)

    chosen_altered_ap=[]

    for i in range(int(len(all_altered_ap_frequency_map)/2), len(all_altered_ap_frequency_map)):
        chosen_altered_ap.append(all_altered_ap_frequency_map[i])

    '''
    chosen_altered_ap=[]
    for i in range(len(all_altered_ap_frequency_map)):
        chosen_altered_ap.append(all_altered_ap_frequency_map[i])
    #after finding the chosen Altered AP, we need to find the RP that is 5m with the location

    scale=whereami_utils.load_whereami_scale(floor)

    #choose the nearest RP in radius of 5 meter---> 5* scale for calculation
    distances = RP_radius*scale

    RP_in_radius=[]

    # need to use the Fingerprint_A, and Fingerprint_V
    for i in range(len(RP_location)):
        dis=distance(float(RP_location[i][0]), float(RP_location[i][1]),final_estimation[0], final_estimation[1])
        if dis <= distances:
            #print(dis)
            dummy=dict({"RP location": RP_location[i], "RP fingerprint MAC": Fingerprint_A[i], "RP fingerprint V": Fingerprint_V[i]})
            RP_in_radius.append(dummy)

    #checking print all RP location in raduis
    print("RP")
    for i in range(len(RP_in_radius)):
        print("RP in the radius",RP_in_radius[i]['RP fingerprint MAC'])

    """
    TODO: adjust the average function so that it suits the range of rssi value, [-101, 20](?), use[-105.0, -20] to play safe
    """
    for i in range (len(RP_in_radius)):
        for j in range(len(chosen_altered_ap)):
            if chosen_altered_ap[j]['Altered AP MAC'] in RP_in_radius[i]['RP fingerprint MAC']:
                #print("chosen ap in radius",chosen_altered_ap[j]['Altered AP MAC'])
                #print("RP in radius", RP_in_radius[i]['RP fingerprint MAC'])
                index_of_mac_address=RP_in_radius[i]['RP fingerprint MAC'].index(chosen_altered_ap[j]['Altered AP MAC'])
                #print(RP_in_radius[i]['RP fingerprint V'][index_of_mac_address])
                chosen_altered_ap[j]['RSSI average']+=(float(RP_in_radius[i]['RP fingerprint V'][index_of_mac_address]) + 105.0)
            else:
                #print("AP not in fingerprint",chosen_altered_ap[j]['Altered AP MAC'] )
                chosen_altered_ap[j]['RSSI average']+=0

    #averageing
    for i in range(len(chosen_altered_ap)):
        if(len(RP_in_radius)!=0):
            chosen_altered_ap[i]['RSSI average']=(chosen_altered_ap[i]['RSSI average']/len(RP_in_radius)) - 105.0
        #print(chosen_altered_ap[i]['RSSI average'])

    #calculate the difference between the estimated and the RSSI average

    print("final altered AP: ", chosen_altered_ap)

    for i in range(len(chosen_altered_ap)):
        if (chosen_altered_ap[i]['Altered AP MAC'] in A):
            A_index=A.index(chosen_altered_ap[i]['Altered AP MAC'])
            chosen_altered_ap[i]['RSSI difference'] = abs(chosen_altered_ap[i]['RSSI average']-V[A_index])
        print ("RSSI difference: ",chosen_altered_ap[i]['RSSI difference'])

    print("finally chosen AP: ",chosen_altered_ap)


    """
    TODO: insert new ap to chosen_altered_ap: [{'Altered AP MAC': mac, 'RSSI difference': should be mearsured value from the request of the AP - min possible value of rssi (which is 105), 'RSSI average': should be 0 for new AP}]
    not the best approach but a workaround
    """
    for new_ap in new_ap_list:
        chosen_altered_ap.append({'Altered AP MAC': new_ap['mac'], "RSSI difference": new_ap['rssi'] + 105, 'RSSI average': 0})

    #store the data for writing into file
    for i in range(len(chosen_altered_ap)):
        if chosen_altered_ap[i]['Altered AP MAC'] not in All_altered_ap:
            print( "new ap not in old")
            
            inner_list=[]
            inner_dummy=dict({"floor":floor, "location": final_estimation, "rssi_diff": chosen_altered_ap[i]['RSSI difference'], "original_rssi": chosen_altered_ap[i]['RSSI average']})
            inner_list.append(inner_dummy)
            dummy=dict({"Altered AP MAC": chosen_altered_ap[i]['Altered AP MAC'],"frequency": 1 , "Location": inner_list})
            altered_ap.append(dummy)
        else:
            print( "already in")
            index_of_altered_AP=All_altered_ap.index(chosen_altered_ap[i]['Altered AP MAC'])
            original_frequency=int(altered_ap[index_of_altered_AP]['frequency'])
            original_frequency+=1
            altered_ap[index_of_altered_AP]['frequency']=original_frequency
            original_Location=altered_ap[index_of_altered_AP]['Location'] #is a list of smaller dict
            #print(original_Location)
            # if it the previour is
            #append to the old location
            inner_dummy=dict({"floor":floor, "location": final_estimation, "rssi_diff": chosen_altered_ap[i]['RSSI difference'], "original_rssi": chosen_altered_ap[i]['RSSI average']})
            original_Location.append(inner_dummy)
            #print("original location ",original_Location)


        
    #write
    f= open("alter_ap.txt", "w")
    for i in range(len(altered_ap)):

        f.write(altered_ap[i]['Altered AP MAC'])
        f.write(': ')
        f.write(str(altered_ap[i]['frequency']))
        f.write(' [')

        for j in range(len(altered_ap[i]['Location'])):
            #print(altered_ap[i]['Location'])
            f.write('{')
            f.write(altered_ap[i]['Location'][j]['floor'])
            f.write('/(')
            f.write(str(altered_ap[i]['Location'][j]['location'][0]))
            f.write(';')
            f.write(str(altered_ap[i]['Location'][j]['location'][1]))
            f.write(')/')
            f.write(str(altered_ap[i]['Location'][j]['rssi_diff']))
            f.write('/')
            f.write(str(altered_ap[i]['Location'][j]['original_rssi']))
            f.write('}')
            if j != len(altered_ap[i]['Location'])-1:
                f.write(',')

        f.write(']')
        f.write('\n')

    return final_estimation

