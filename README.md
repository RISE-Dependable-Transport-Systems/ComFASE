# ComFASE
 ComFASE is a  communication fault  and  attack  simulation  engine  that  allows  to  evaluate the behavior of interconnected automated vehicles in the presence of faults and attacks. ComFASE is built on top of [OMNeT++](https://omnetpp.org/), and integrates [SUMO](https://www.eclipse.org/sumo/), and [Veins](https://veins.car2x.org/).  To automate the campagin run we use [Python](https://www.python.org/), where we configure the attack injection campagin and log the injected data. To demonstrate the usefullness of ComFASE we used platooning scenario provided in [Plexe-Veins](https://plexe.car2x.org/tutorial/).

<p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/ComFASE_Arc.jpg" width="450" height="300">
</p>
<br/> 
<br/> 


# ComFASE Integration

## Step1: ComFASR in OMNeT++ IDE
Before integrating ComFASE into the simulator, it is recommended to have all the simulators running on your system. You can follow the instructions on the OMNeT++, Veins, and Plexe webpages to install them and get them ready to run. 

Note: ComFASE is tested in the below-mentioned versions of the simulators:

* [OMNeT++ 5.6.2](https://omnetpp.org/software/2020/01/13/omnet-5-6-released)
* [Veins 5.1](https://github.com/sommer/veins/releases/tag/veins-5.1)
* [Plexe 3.0a2](https://github.com/michele-segata/plexe/releases/tag/plexe-3.0a3)   ``` git clone -b plexe-3.0a2 https://github.com/michele-segata/plexe.git ```
* [SUMO 1.8.0](https://sourceforge.net/projects/sumo/files/sumo/version%201.8.0/)


|       Simulator       |                                 Definition                        |
| ----------------------| ----------------------------------------------------------------- |
| *OMNeT++*             | is a modular, component-based C++ simulation library and framework|
| *Veins*               | is a framework for running vehicular network simulations          |
| *Plexe*               | is a cooperative driving framework extending SUMO and Veins permitting the realistic simulation of platooning|
| *SUMO*                | is a microscopic traffic simulator                                  |

### Integrating ComFASE into the Simulators
1. Copy the **attackInjection** folder into the "veins/src/veins" directory.
2. To use the **injector** in the desired part of the code, you can use the below code to call it 
```
#include "veins/attackInjection/Injector.h"
```
for **Delay** and **DoS** attacks the following lines are added into the "channelAccess.cc" in source code of the Veins
```
auto Injection = FindModule<Injector*>::findGlobalModule();
    if (Injection->attackActive){
        std::cout<<"AttackActive = is TRUE"<<std::endl;
        float correctValue = receiverPos.distance(senderPos2) / BaseWorldUtility::speedOfLight();
        return Injection->AttackInjectionEngine(senderModule->getId(), receiverModule->getId(), correctValue);
    }
    else{
    // this time-point is used to calculate the distance between sending and receiving host
        return receiverPos.distance(senderPos2) / BaseWorldUtility::speedOfLight();
    }
```
3. Update **ned** file of the example that you want to run by adding: 
``` 
import org.car2x.veins.attackInjection.Injector;
```
and 
```
        attacker: Injector {
            @display("p=120,50;i=abstract/penguin");
        }
```
4. in your **ini** file call "attackInjection.ini" by adding:
```
include <path to veins>/veins/src/veins/attackInjection/attackInjection.ini
```

5. Compile the code to make it ready to run (build all projects in OMNeT++ IDE)

## Step2: ComFASR in cmd environment
## Running
A Python script is written to run the ComFASE experiments, before running that you can define your attack injection setup such as target node (target vehicle), attack type (Delay or DoS), and target attack surface (sender, receiver or both):
```
Node=27  		     # NODE/VEHICLE UNDER ATTACK
Activation='true'	     # BOOLEAN FOR ATTACK ACTIVATION
Delay='true'	             # BOOLEAN FOR DELAY
Sender='true'   	     # BOOLEAN FOR TARGET SURFACE FOR SENDER
Receiver='true' 	     # BOOLEAN FOR TARGET SURFACE FOR RECEIVER
for t in numpy.arange(17.0, 21.9, 0.2):  # This loop defines the target time to inject attack
```
## Result Analyze


## License

## Papers
