# **ComFASE Integration**

**Steps to use ComFASE in Plexe-Veins**

1. Download Veins
```
git clone https://github.com/sommer/veins.git
```
2. Download Plexe version 3.0a2
```
git clone -b plexe-3.0a2 https://github.com/michele-segata/plexe.git
```
3. Download ComFASE
```
git clone ...
```
4. Import all the projects into the OMNeT++ IDE and follow instructions provided in [Plexe](https://plexe.car2x.org/tutorial/) to run a demo example and make sure everything is in place before integrating ComFASE.
5. Reference ComFASE in Veins and Plexe as below:

<p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/veins_ref.png" width="450" height="300">
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/plexe_ref.png" width="450" height="300">
</p>
<br/> 
<br/>  

6. To use the **injector** in the desired part of the code, you can use the below code to call it 
```
#include "/opt/sim/Dev2/comfase/src/comfase/attackInjection/Injector.h""
```
Note: this path could be different depending on your directory.

for **Delay** and **DoS** attacks the following lines are added into the "channelAccess.cc" in source code of the Veins
```
auto Injection = FindModule<Injector*>::findGlobalModule();
    if (Injection->attackActive){
        std::cout<<"AttackActive = is TRUE"<<std::endl;
        float correctValue = receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
        return Injection->AttackInjectionEngine(senderModule->getId(), receiverModule->getId(), correctValue);
    }
    else{
    // this time-point is used to calculate the distance between sending and receiving host
        return receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
    }
```
3. Update **ned** file of the example that you want to run by adding: 
``` 
import comfase.comfase.attackInjection.Injector;
```
and 
```
        comfase: Injector {
            @display("p=120,50;i=abstract/penguin");
        }
```
4. in your **ini** file call "attackInjection.ini" by adding:
```
include <path to comfase>/comfase/src/comfase/attackInjection/attackInjection.ini
```

5. Compile the code to make it ready to run (build all projects in OMNeT++ IDE)


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
