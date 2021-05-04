# LAAFU-server-demo
***Author: Roger, LIN, Guan-cherng & Gary, Cheung Wing Ho, Version: 2021.4.29***

This is the documentation of the LAAFU system, which contains: **Localization with ALtered AP** with **Random Subset Sampling & Location Clustering**, **Dense Cluster Detection & Target Localization** and **Altered AP Identification** part.

## Content
### Files and Folders

- fingerprint folder: fingerprint database files collected by Gary Cheng. 
- loc.txt: location of all RPs
- resX: folder containing all APs' map from points to RSSIs. They will be used in visualizing
- paraX: folder containing all APs' GP parameters. They are currently used for restoring APs' location
- output_X\all_xxxxx.txt: file of one AP containing AP location, RSSI error among all RPs and corresponding std
- output_X\xxxxx.txt: file containing all RP points that deviate a lot from estimation.

