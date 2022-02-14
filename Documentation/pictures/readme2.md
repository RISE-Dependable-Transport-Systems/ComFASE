# **ComFASE Integration**


SUFI is a sumo-based fault injector tool. The tool combines [SUMO](https://www.eclipse.org/sumo/) and [Python](https://www.python.org/). SUFI uses sumo for mobility simulation, where we define the traffic scenario and vehicle features there. Also, sumo allows us to select the car-following and lane-changing models to model the car behavior during the simulation run, thereby, evaluate these models through the fault and attack injection. Python, on the other hand, allows us to write scripts for different fault models, select fault locations and define fault durations. SUMO and Python are communicating via [TraCI](https://sumo.dlr.de/docs/TraCI.html) with each other when running the experiments.

<p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/SUFI/blob/master/Documentation/pictures/SUFI.PNG">
</p>
<br/> 
<br/> 


## Simulation Setup

* Install [SUMO 1.6.0](https://sourceforge.net/projects/sumo/files/sumo/version%201.6.0/) (we used this version of SUMO so please note that for the later versions the car behavior might change)
* Install Python 3.7 or later

#### Required Python libraries:
* sumolib
* traci
* pandas
* numpy
* matplotlib

## Experiment Run 
After downolading the repository, open one of the example folders and run the Python-run file. <br/> 
For example in folder: **"SUFI/Examples/1. LC-Assertive Parameter"**    run    **"run_(stuck-at-value)_semi-permanent.py"**

## IMPORTANT NOTES!
1. Before running the experiment make sure that the ".net", ".rou", ".settings", and ".sumocfg" files are in the same directory with the Python run file. Also create two folders with names "output" and "outputG" so some of the output data will be stored in these folders.

2. In the abovementioned version (SUMO 1.6.0) the "perception errors" functionality was not active for the CACC and ACC models, therefore, in order to inject fault
into the "error state" parameter we added this functionality into the source code. But for the later versions we requested the SUMO team to add this funtionality so you might do not need to do that.

## License 
SUFI is an open source fault injector tool, the tool is free: you can redistribute it and/or modify it under the terms of the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.


## Publications about SUFI

* [IEEE-DSN](https://ieeexplore.ieee.org/document/9525530)
* [IEEE-EDCC](https://ieeexplore.ieee.org/document/9603599)
