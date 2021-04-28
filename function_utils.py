import math

"""
TODO: implement the Jenks natural breaks optimizaiton method
"""
# input: list to be splitted, the attribute name of the data, the attribute name of the frequency
# output: [[<data of class 1 (keep other attributes)>], [<data of class 2 (keep other attributes)>]]
def Jenks_natural_breaks(input_list, data_attr_name, freq_attr_name):
    sanitized_list = []
    for elem in input_list:
        sanitized_list.append({"data": elem[data_attr_name], "freq": float(elem[freq_attr_name])})
    if len(sanitized_list) == 0:
        return [[], []]
    elif len(sanitized_list) == 1:
        return [sanitized_list[0]["data"], []]
    sanitized_list.sort(key=lambda elem: elem["freq"])
    smallest_SDCM_idx = None
    smallest_SDCM = math.inf
    for idx, elem in enumerate(sanitized_list):
        first_class_list = sanitized_list[: idx + 1]
        second_class_list = sanitized_list[idx + 1:]
        total_SDCM = SDCM([elem["freq"] for elem in first_class_list]) + SDCM([elem["freq"] for elem in second_class_list])
        if total_SDCM <= smallest_SDCM:
            smallest_SDCM = total_SDCM
            smallest_SDCM_idx = idx
    result_first_class_list = [elem["data"] for elem in sanitized_list[: smallest_SDCM_idx + 1]]
    result_second_class_list = [elem["data"] for elem in sanitized_list[smallest_SDCM_idx + 1:]]
    return [[elem for elem in input_list if elem[data_attr_name] in result_first_class_list],\
            [elem for elem in input_list if elem[data_attr_name] in result_second_class_list]]



def SDCM(input_list):
    if len(input_list) == 0:
        return 0.0
    mean = float(sum(input_list))/len(input_list)
    result = [math.pow(elem - mean, 2) for elem in input_list]
    return sum(result)
