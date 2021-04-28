import json
import os

floor_id_to_the_scale = {
    "7F": 13.913,
    "6F": 13.913,
    "5F": 13.913,
    "4F": 13.913,
    "3F": 13.913,
    "2F": 13.913,
    "1F": 13.913,
    "GF": 13.913,
    "LG1": 13.333,
    "LG3": 13.333,
    "LG4": 13.333,
    "LG5": 13.333,
    "LG7": 13.333,
    "CYT7": 13.913,
    "CYT6": 13.913,
    "CYT5": 13.913,
    "CYT4": 13.913,
    "CYT3": 13.913,
    "CYT2": 13.913,
    "CYT1": 13.913,
    "CYTG": 13.913,
    "CYTUG": 13.913,
    "LSK7": 13.913,
    "LSK6": 13.913,
    "LSK5": 13.913,
    "LSK4": 13.913,
    "LSK3": 13.913,
    "LSK2": 13.913,
    "LSK1": 13.913,
    "LSKG": 13.913,
}

#return the scale of the floor
def load_whereami_scale(floor):
    
    return floor_id_to_the_scale[floor]
