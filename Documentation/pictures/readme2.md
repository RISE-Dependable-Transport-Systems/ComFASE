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
git clone https://github.com/RISE-Dependable-Transport-Systems/ComFASE.git
```
4. Import all the projects into the OMNeT++ IDE and follow the instructions provided in [Plexe](https://plexe.car2x.org/tutorial/) to run a demo example and make sure everything is in place before integrating ComFASE.
5. Reference ComFASE in Veins and Plexe as below:

<p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/veins_ref.png" width="450" height="300">
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/plexe_ref.png" width="450" height="300">
</p>
<br/> 
<br/>  

6. To use **ComFASE** in the desired part of the code, you can add below code to call it 
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
7. Update **ned** file of the example that you want to run by adding: 
``` 
import comfase.comfase.attackInjection.Injector;
```
and 
```
        comfase: Injector {
            @display("p=120,50;i=abstract/penguin");
        }
```
8. in your **ini** file call "attackInjection.ini" by adding:
```
include <path to comfase>/comfase/src/comfase/attackInjection/attackInjection.ini
```

9. Compile the code to make it ready to run (build all projects in OMNeT++ IDE)
 
## Build ComFASE through the command line
After making any changes to the code in the OMNet++ IDE and successfully running an example, follow the following steps to run it automatically via a Python script:
1. Build each of the 3 projects (ComFase, Veins, Plexe) separately in their directory with this command;
```
$ make -j16   //16 is number of the cores, it might be different for your system
```
2. In the **run.py** script located in the Plexe folder, add the path to comfase folder to call Ned files:
```
run_libs = ['../veins/src/veins', 'src/plexe']
run_neds = ['../veins/src/veins', 'src/plexe', '../comfase/src']
run_imgs = ['../veins/images', 'images']
```

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
1. 

## License 
SUFI is an open source fault injector tool, the tool is free: you can redistribute it and/or modify it under the terms of the [GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.en.html) as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.


## Publications about ComFASE

* [IEEE-DSN](https://ieeexplore.ieee.org/document/9525530)
* [IEEE-EDCC](https://ieeexplore.ieee.org/document/9603599)
