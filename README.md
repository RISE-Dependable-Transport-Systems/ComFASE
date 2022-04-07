# ComFASE
 ComFASE is a  communication fault  and  attack  simulation  engine  that  allows  to  evaluate the behavior of interconnected automated vehicles in the presence of faults and attacks. ComFASE is built on top of [OMNeT++](https://omnetpp.org/), and integrates [SUMO](https://www.eclipse.org/sumo/), and [Veins](https://veins.car2x.org/).  To automate the campagin run we use [Python](https://www.python.org/), where we configure the attack injection campagin and log the injected data. To demonstrate the usefullness of ComFASE we used platooning scenario provided in [Plexe-Veins](https://plexe.car2x.org/tutorial/).

<p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/ComFASE_Arc.jpg" width="450" height="300">
</p>
<br/> 
<br/> 

|       Simulator       |                                 Definition                        |
| ----------------------| ----------------------------------------------------------------- |
| *OMNeT++*             | is a modular, component-based C++ simulation library and framework|
| *Veins*               | is a framework for running vehicular network simulations          |
| *Plexe*               | is a cooperative driving framework extending SUMO and Veins permitting the realistic simulation of platooning|
| *SUMO*                | is a microscopic traffic simulator                                  |

# ComFASE Integration

## Option1: ComFASE in OMNeT++ IDE
Before integrating ComFASE into the simulator, it is recommended to have all the simulators running on your system. You can follow the instructions on the OMNeT++, Veins, and Plexe webpages to install them and get them ready to run. 

Note: ComFASE is tested in the below-mentioned versions of the simulators:

* [OMNeT++ 5.6.2](https://omnetpp.org/software/2020/01/13/omnet-5-6-released)
* [Veins 5.1](https://github.com/sommer/veins/releases/tag/veins-5.1)    ``` git clone -b veins-5.1 https://github.com/sommer/veins.git  ```
* [Plexe 3.0a2](https://github.com/michele-segata/plexe/releases/tag/plexe-3.0a3)   ``` git clone -b plexe-3.0a2 https://github.com/michele-segata/plexe.git ```
* [SUMO 1.8.0](https://sourceforge.net/projects/sumo/files/sumo/version%201.8.0/)


### Integrating ComFASE into the Simulators
1. Clone the [ComFASE](https://github.com/RISE-Dependable-Transport-Systems/ComFASE) project and import it into the OMNeT++ IDE.
2. Reference ComFASE in Veins and Plexe as below:
<p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/veins_ref.png" width="450" height="300">
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/plexe_ref.png" width="450" height="300">
</p>
<br/> 
<br/> 

3. To use the **ComFASE** in the desired part of the code, add below lines to call comfase header file: 
```
#include "veins/base/utils/FindModule.h"
#include "/opt/sim/Dev2/comfase/src/comfase/attackInjection/Injector.h"
```
Note: the path to the **Injector.h** file can be different depending on your directory.

for **Delay** and **DoS** attacks the following lines are added into the "channelAccess.cc" in source code of the Veins
```
    auto Injection = FindModule<Injector*>::findGlobalModule();
    if (Injection->DelayAttack){
        std::cout<<"Delay Attack = is TRUE"<<std::endl;
        float correctValue = receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
        return Injection->PropagationDelayAttack(senderModule->getId(), receiverModule->getId(), correctValue);
    }
    else if (Injection->DoSAttack){
        std::cout<<"DoS Attack = is TRUE"<<std::endl;
        float correctValue = receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
        return Injection->DenialOfServiceAttack(senderModule->getId(), receiverModule->getId(), correctValue);
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
4. Update your example **ini** file by adding "attackInjection.ini" as following:
```
include <path to veins>/veins/src/veins/attackInjection/attackInjection.ini
```

5. Compile the code to make it ready to run (build all projects in OMNeT++ IDE)

## Option2: ComFASE in cmd environment
# ComFASE Running
## Option1: in OMNeT++ IDE
Configure the attack injection scenario through updating the **attackInjection.ini** file as denoted below, and run the desired example.
```
##########################################################
#                       Attack Start                     #
##########################################################
*.comfase.attackStartTime 	= ${attackStartTime = 12}s
###                      Attack End                       #
###########################################################
*.comfase.attackEndTime 	= ${attackEndTime = 15}s # This is not for DoS attack
#
##          Target Vehicle and Attack Surface             #
###########################################################
*.comfase.attackNode 		= 27
*.comfase.attackActive 	= false
*.comfase.attackOnSender 	= true
*.comfase.attackOnReceiver = false
#
#
##                     Delay Attack                       #
###########################################################
*.comfase.DelayAttack = true
*.comfase.myPDValue 		= ${myPDValue = 0.5}s
#
#
##                 Varying Delay Attack                   #
###########################################################
*.comfase.v_DelayAttack = false
#
#
##                   uc2 Delay Attack                     #
###########################################################
*.comfase.uc2_DelayAttack = false
*.comfase.uc2_PDValue 	   = 305s
#
#
##            Denial of Service Attack                    #
###########################################################
*.comfase.DoSAttack = false
*.comfase.myPDforDoS		= ${myPDforDoS = 60}s 
#
#
##            Signal Jamming Attack                       #
###########################################################
*.comfase.SignalPowerAttack = false
*.comfase.ReceivePowerAttack = false
*.comfase.myPowerValue = 0.1 mW
*.comfase.myR_PowerValue = 9 mW
#
#
##            Interference Jamming Attack                 #
###########################################################
*.comfase.InterferenceAttack = false
*.comfase.myInterfValue = 0.97 mW
```

## Option2: in cmd
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
