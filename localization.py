import os.path
import random
import math
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import time
import fingerprint_utils

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
    RP_location, Fingerprint_A, Fingerprint_V, A, V = fingerprint_utils.load_fingerprint(json_example)
    
    #print (A)
    #print (V)


    '''
    start of the code
    '''
    #this is the setup number
    #can change later
    #generate M subsets 
    #choose the best K RP
    #choose the nearest Q RP
    #bamdwidth b for Gaussian Kernel
    M=20
    K=8
    Q=8
    b=0.02
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
    subsets=[] # only has MAC address
    subsets_RSSI=[] #only has RSSI vector 

    #generate M subset with size>3
    fulfillM=False

    while(not fulfillM):
        one_subset=[]
        one_subset_RSSI=[]
        #subset.append(one_subset)
        #add AP inside
        for j in range(len(DetectedAP)):
            coin = random.randint(1, 2)
            if coin ==1: #if it is the head
                one_subset.append(DetectedAP[j])
                one_subset_RSSI.append(float(RSS[j]['RSSI']))
            else: #if it is not the head dont do anything

                break
        
        if (len(one_subset)>=3):
            if (one_subset not in subsets):
                subsets.append(one_subset)
                subsets_RSSI.append(one_subset_RSSI)

        
        if (len(subsets)>=M):
            fulfillM=True



    #######
    #for i in range(M):
    #    one_subset=[]
    #    #subset.append(one_subset)
    #    #add AP inside
    #    for j in range(len(DetectedAP)):
    #        coin = random.randint(1, 2)
    #        if coin ==1: #if it is the head
    #            one_subset.append(DetectedAP[j])
    #        else: #if it is not the head dont do anything
    #
    #            break
    #    
    #    subsets_old.append(one_subset)
    ##print (subsets_old)
    #pop_item=[]
    #for i in range(len(subsets_old)):
    #    if len(subsets_old[i]) <3:
    #        pop_item.append(i)
    #
    ##print(pop_item)
    #subsets=[]
    #for i in range(len(subsets_old)):
    #    if i not in pop_item:
    #        subsets.append(subsets_old[i])

    #print("subsets MAC: ",subsets)
    #print("subsets MAC with RSSI: ",subsets_RSSI)



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
                    Vi.append(float(RSS[k].get("RSSI")))
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
        
    #print("estimated locations: ",locations) 



    t1=time.time()
    #APC algorithm 
    sim=np.array([[0 for j in range(len(locations))]for i in range (len(locations))], dtype= float)
    for i in range(len(sim)):
        for j in range(len(sim[i])):
            #calculate the educlidean distance between locations
            xSquare=math.pow(locations[i][0]-locations[j][0],2)
            ySquare=math.pow(locations[i][1]-locations[j][1],2)
            #sim[i][j]=math.sqrt(xSquare+ySquare)
            sim[i][j]=-(xSquare+ySquare)

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
        #print("interation: ", i)
        '''
        #create create new res
        new_res=np.array([[0 for k in range(len(res[j]))]for j in range(len(res))], dtype=float)
        for j in range(len(res)):
            for k in range(len(res[j])):
                new_res[j][k]=res[j][k]
    

        #print(new_res)

        #create create new avail
        new_avail=np.array([[0 for k in range(len(avail[j]))]for j in range(len(avail))], dtype=float)
        for j in range(len(avail)):
            for k in range(len(avail[j])):
                new_avail[j][k]=avail[j][k]
        
        
        #print(new_avail)
        '''
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

        
        #the highest criterion value of each row in sol is exemplar 
        #the rows with the same exemplar value is in the same cluster
        #sol = new_res + new_avail
        sol = res + avail
        #print(sol)
        
        #print ("last exemplars: ",last_exemplars)
        #print ("sol: ",sol)

        exemplars = np.unique(np.argmax(sol, axis=1))
        #print("label: ", np.argmax(sol, axis=1))
        #print("exemplars: ",exemplars)
        
        #exemplars_with_all=[] #all the location of the centriod id
        #exemplars=np.array([]) # the max index of each row of the sol
        #for j in range(len(sol)):
        #    max_id_in_row=np.argmax(sol[j])
        #    exemplars_with_all.append(max_id_in_row)
        #    print(max_id_in_row)
        #    if max_id_in_row not in exemplars:
        #        exemplars=np.append(exemplars,max_id_in_row)


        #print("exemplars: ",exemplars)
        #print("last exemplars: ",last_exemplars)
        #print("last_sol ", last_sol)
        #print("sol ", sol)
        


        #if the location is the same as the past location
        if  last_exemplars.size == exemplars.size and last_exemplars.all()==exemplars.all():
            #stop

            for j in range(len(np.argmax(sol, axis=1))):
                location_with_centriod_id.append(np.argmax(sol, axis=1)[j])
                
            break

        last_sol = sol
        last_exemplars = exemplars
        '''
        #update new res
        for j in range(len(new_res)):
            for k in range(len(new_res[j])):
                res[j][k]=new_res[j][k]

        #update new avaio
        for j in range(len(new_avail)):
            for k in range(len(new_avail[j])):
                avail[j][k]=new_avail[j][k]

        del new_avail
        del new_res
        '''

    #print(location_with_centriod_id)
    t2=time.time()
    time_I= t2-t1
        
    '''
    the visulization for debugging use
    '''
    '''
    fig = plt.figure(figsize=(12, 6))

    # every data point i chooses the maximum index k
    labels = np.array([location_with_centriod_id[i] for i in range(len(location_with_centriod_id))])
    exemplars = np.unique(labels)
    colors = dict(zip(exemplars, cycle('bgrcmyk')))

    x=subsets

    for i in range(len(labels)):
        X = x[i][0]
        Y = x[i][1]
        
        if i in exemplars:
            exemplar = i
            edge = 'k'
            ms = 9
        else:
            exemplar = labels[i] #####
            ms = 3
            edge = None
            plt.plot([X, x[exemplar][0]], [Y, x[exemplar][1]], c=colors[exemplar])
        plt.plot(X, Y, 'o', markersize=ms,  markeredgecolor=edge, c=colors[exemplar])
        #plt.annotate(str(i) , xy=(X, Y), xytext=(80, 280))
        

    plt.title('Number of exemplars: %s' % len(exemplars))
    '''
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

    #print(cluster)
    #print(cluster_ID)


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
    #print("Qc: ",Qc)


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

    #print("Vc: ",Vc)

    #calculate the score

    scores=[Qc[i]-Vc[i] for i in range(len(Qc))]
    #print("scores of each cluster: ",scores)
    maximum_score_id=scores.index(max(scores))
    #the location detected in the end is the maximum score location
    final_estimation=cluster[maximum_score_id]['centorid']
    final_estimation_ID=cluster_ID[maximum_score_id]['centorid']
    #print("final estimation:",final_estimation)
    #print("ID :",final_estimation_ID )


    #5.3
    #altered ap part
    dense_subsets=[]
    #print(cluster[maximum_score_id]['cluster'])
    #print(cluster_ID[maximum_score_id]['cluster'])
    for j in range(len(cluster_ID[maximum_score_id]['cluster'])):
        dummy=subsets[cluster_ID[maximum_score_id]['cluster'][j]]
        dense_subsets.append(dummy)
    #print(dense_subsets)

    unique=[]
    for i in range(len(dense_subsets)):
        for j in range(len(dense_subsets[i])):
            if dense_subsets[i][j] not in unique:
                unique.append(dense_subsets[i][j])

    #print(unique)
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
    #print(AP_freq)

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
                
        #print(class_A)
        #print(class_A_sum)
        #print(class_B)
        #print(class_B_sum)

        SDCM[i]=class_A_sum+class_B_sum
        SDCM_class_freq[i][0]=class_A_sum
        SDCM_class_freq[i][1]=class_B_sum
        classes.append(dummy)


    
    #print("SDCM each freq: ",SDCM_class_freq)


    lowest_SDCM=SDCM.argmin()
    lowest_class=SDCM[lowest_SDCM].argmin()
    alter_AP=[]
    for i in range(len(classes[lowest_SDCM][lowest_class])):
        alter_AP.append(classes[lowest_SDCM][lowest_class][i]['MAC'])



        
    return final_estimation,alter_AP

