# lora_energy_sim

This repository includes all scripts used to simulate the different use cases evaluated in "Paper name". The folder structure is as follows:

The "simulation" folder includes the scripts necessary for the simulation of the individual scenarios and is always present. This folder also includes the sensor's dataset "collisioncalc.csv" for the city of Wuerzburg used for one of the use-cases.
The simulation can be run by executing the "run.py" in the simulation folder. 

Before running the simulation, different parameters can be set in the "configuration.yaml" file. This includes the simulation duration, network and packet specific parameters.
Here, a special parameter is "coll_calc", which is a boolean describing which use-case should be simulated:
- If coll_calc is true, the "collisioncalc.csv" file is used as input to create the sensors and gateways of the simulated network. 
- If coll_calc is false, the network is simulated by the Monte-Carlo approach as there is one gateway in the center of the coordinate system and multiple sensors are placed around it. The coordinates of all sensors are randomly but unifromly distributed within the maximum distance to the gateway. 


Executing the script produces a "log" folder with 12 subfolders named after their respective test condition. For each of these test conditions, there are 20 different simulation runs containing two CSV-files: 
- "transmission_log.csv"
- "state_log.csv" (This can be neglected.)
   
These files contain the different packet transmissions of all sensors over time. 


The "zipped_logs" folder contains two ZIP-files:
- one_gateway_logs.zip: This describes the LoRaWAN use-case.
- gateway_placement_logs.zip: This describes the second use-case.
 
Extracting these ZIP-files grants access to the transmission logs used in the evaluation of the original paper. 

A script is also provided to calculate the time on air for different payloads and spreading factors as "get_toas_for_cr_sf.py".
