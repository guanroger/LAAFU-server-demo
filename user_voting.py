def user_voting(altered_AP):
    # for i in range(len(altered_AP)):
    #     min_f=int(altered_AP[i]['frequency'])
    #     for j in range(i+1,len(altered_AP)):
    #         if (int(altered_AP[j]['frequency'])<min_f):
    #                 temp=altered_AP[i]
    #                 altered_AP[i]=altered_AP[j]
    #                 altered_AP[j]=temp
    altered_AP.sort(key=lambda elem: int(elem["frequency"]))

    #print("sorted: " ,altered_AP)

    chosen_altered_ap=[]
    # print("altered_AP = ")
    # print([{"freq": elem['frequency']} for elem in altered_AP])

    for i in range(int(len(altered_AP)/2), len(altered_AP)):
        chosen_altered_ap.append(altered_AP[i])

    return chosen_altered_ap