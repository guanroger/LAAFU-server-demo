# LAAFU-server-demo
***Author: Roger, LIN, Guan-cherng & Gary, Cheung Wing Ho, Version: 2021.4.29***

This is the documentation of the LAAFU system, which contains: **Localization with ALtered AP** with **Random Subset Sampling & Location Clustering**, **Dense Cluster Detection & Target Localization** and **Altered AP Identification** part.

## Content
### Files and Folders

- fingerprint folder: fingerprint database files collected by Gary Cheng, which contains all the fingerprint database used for server localization and altered AP identification.
- altered_ap.txt: store the information for detected altered ap after each localization. It contains the altered aps' information about its MAC address, frequency, the estimated locations where we find this altered AP, floor, rssi_average, and rssi_difference.
- app.py: starting point of the LAAFU server for sending the data and receiving the request. Please run this if you wish to start the server.
- fingerprint_utils.py: used to fetch the fingerprint data for localization ith altered AP in localization.py.
- function_utils.py: used to do the Jenks_natural_breaks and calculate SDCM for the Altered AP identification in localization.py.
- get_altered_AP.py: used to get all the information for specific altered AP for app.py. 
- get_altered_AP_list.py: used to get only the mac address for all altered AP for app.py. 
- get_distinct_location.py: used to get all the infrormation where we find altered AP for app.py.
- (all the return velue will be sent to app.py, and sent to visualization tool for further use.)
- localization.py: which contains all the localzation woth altered AP and the altered AP identification steps where we take the user's signal vectors from app.py and fingerprint database information from fingerprint_utils.py, and send back the estimated user location to app.py, and store the altered AP information in altered_ap.txt.
- requirements.txt: if the server want to know the version of the flask server for configeration, please type in this txt file.
- user_voting.py: do the user voting for returning the altered AP information. For each request for requesting altered APs information, we do the user voting once.
- whereami_utils.py: present the data for calculating the actual distance for storing the altered AP information.
