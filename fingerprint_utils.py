import json
import os

floor_id_to_relative_file_path_map = {
    "7F": "/fingerprint/7F/fingerprint.txt",
    "6F": "/fingerprint/6F/fingerprint.txt",
    "5F": "/fingerprint/5F/fingerprint.txt",
    "4F": "/fingerprint/4F/fingerprint.txt",
    "3F": "/fingerprint/3F/fingerprint.txt",
    "2F": "/fingerprint/2F/fingerprint.txt",
    "1F": "/fingerprint/1F/fingerprint.txt",
    "GF": "/fingerprint/GF/fingerprint.txt",
    "LG1": "/fingerprint/LG1/fingerprint.txt",
    "LG3": "/fingerprint/LG3/fingerprint.txt",
    "LG4": "/fingerprint/LG4/fingerprint.txt",
    "LG5": "/fingerprint/LG5/fingerprint.txt",
    "LG7": "/fingerprint/LG7/fingerprint.txt",
    "CYT7": "/fingerprint/CYT7/fingerprint.txt",
    "CYT6": "/fingerprint/CYT6/fingerprint.txt",
    "CYT5": "/fingerprint/CYT5/fingerprint.txt",
    "CYT4": "/fingerprint/CYT4/fingerprint.txt",
    "CYT3": "/fingerprint/CYT3/fingerprint.txt",
    "CYT2": "/fingerprint/CYT2/fingerprint.txt",
    "CYT1": "/fingerprint/CYT1/fingerprint.txt",
    "CYTG": "/fingerprint/CYTG/fingerprint.txt",
    "CYTUG": "/fingerprint/CYTUG/fingerprint.txt",
    "LSK7": "/fingerprint/LSK7/fingerprint.txt",
    "LSK6": "/fingerprint/LSK6/fingerprint.txt",
    "LSK5": "/fingerprint/LSK5/fingerprint.txt",
    "LSK4": "/fingerprint/LSK4/fingerprint.txt",
    "LSK3": "/fingerprint/LSK3/fingerprint.txt",
    "LSK2": "/fingerprint/LSK2/fingerprint.txt",
    "LSK1": "/fingerprint/LSK1/fingerprint.txt",
    "LSKG": "/fingerprint/LSKG/fingerprint.txt",
}

# return a tuple (RP_location, Fingerprint_A, Fingerprint_V, A, V)
def load_fingerprint(json_from_request):
    json_data = json.loads(json_from_request)
    floor = json_data["floor"]
    A = json_data['A']
    A_uppercase = []
    for a in A:
        A_uppercase.append(a.upper())
    V = json_data['V']
    fingerprint_As = []
    fingerprint_Vs = []
    rp_locations = []
    f = open((os.path.abspath(os.path.dirname(os.path.abspath(__file__)))+floor_id_to_relative_file_path_map[floor]), 'r')
    for rp in f:
        parts = rp.split(' ')
        rp_location = parts[0].split(',')
        rp_locations.append([rp_location[0], rp_location[1]])
        rp_address = []
        rp_rssi = []
        for ap in parts[1:]:
            ap_parts = ap.split(',')
            rp_address.append(ap_parts[0])
            rp_rssi.append(ap_parts[1])
        fingerprint_As.append(rp_address)
        fingerprint_Vs.append(rp_rssi)
    return rp_locations, fingerprint_As, fingerprint_Vs, A_uppercase, V, floor