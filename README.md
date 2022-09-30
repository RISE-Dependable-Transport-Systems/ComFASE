# ComFASE
 ComFASE is a  communication fault  and  attack  simulation  engine  that  allows  to  evaluate the behavior of interconnected automated vehicles in the presence of faults and attacks. ComFASE is built on top of [OMNeT++](https://omnetpp.org/), and integrates [SUMO](https://www.eclipse.org/sumo/), and [Veins](https://veins.car2x.org/).  
 To automate the campagin run we use [Python](https://www.python.org/), where we configure the attack injection campagin and log the injected data. To demonstrate the usefullness of ComFASE we used platooning scenario provided in [Plexe-Veins](https://plexe.car2x.org/tutorial/).

 <p align="center">
  <br><br>
  <img src="https://github.com/RISE-Dependable-Transport-Systems/ComFASE/blob/main/Documentation/pictures/ComFASE_Logo_v3.png" width="350" height="300">
</p>

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
## Step1: Using ComFASE from OMNeT++ IDE
Before integrating ComFASE into the simulator, it is recommended to have all the simulators running on your system. You can follow the instructions on the OMNeT++, Veins, and Plexe webpages to install them and get them ready to run. 

Note: ComFASE is tested in the below-mentioned versions of the simulators:

* [OMNeT++ 5.6.2](https://omnetpp.org/software/2020/01/13/omnet-5-6-released)
* [Veins 5.1](https://github.com/sommer/veins/releases/tag/veins-5.1)    ``` git clone -b veins-5.1 https://github.com/sommer/veins.git  ```
* [Plexe 3.0a2](https://github.com/michele-segata/plexe/releases/tag/plexe-3.0a3)   ``` git clone -b plexe-3.0a2 https://github.com/michele-segata/plexe.git ```
* [SUMO 1.9.2](https://sourceforge.net/projects/sumo/files/sumo/version%201.8.0/)


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
#include "<path to comfase>comfase/src/comfase/attackInjection/Injector.h"
```
Note: the path to the **Injector.h** file can be different depending on your directory.

for **Delay** and **DoS** attacks the following lines are added into the "channelAccess.cc" in source code of the Veins
```
    auto comfase = FindModule<injectorV*>::findGlobalModule();
    if (comfase->DelayAttack){
        std::cout<<"Delay Attack = is TRUE"<<std::endl;
        float correctValue = receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
        return comfase->PropagationDelayAttack(senderModule->getId(), receiverModule->getId(), correctValue);
    }
    else if (comfase->DoSAttack){
        std::cout<<"DoS Attack = is TRUE"<<std::endl;
        float correctValue = receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
        return comfase->DenialOfServiceAttack(senderModule->getId(), receiverModule->getId(), correctValue);
    }
    else{
    // this time-point is used to calculate the distance between sending and receiving host
        return receiverPos.distance(senderPos) / BaseWorldUtility::speedOfLight();
    }
```
3. Update **ned** file of the example that you want to run by adding: 
``` 
import comfase.comfase.injectorVeins.injectorV;
```
and 
```
        comfase: injectorV {
            @display("p=120,50;i=abstract/penguin");
        }
```
4. Update your example **ini** file by adding "attackInjection.ini" as following:
```
include <path to comfase>comfase/src/comfase/injectorVeins/injectorV.ini
```

5. Compile the code to make it ready to run (build all projects in OMNeT++ IDE)

Note: Step1 is suitable for working in IDE level, proceed to step2 if test automation is required (i.e., to run experiments in bulk automatically).
## Step2: Using ComFASE from cmd environment

This optinon can be used to run test campaigns automatically. A test campaign consists of many experiments where the number of the experimnets depends on the test configuration setup such as, attack start time, attack end time, and attack values vector. The test campaign can be configured by using a Python script (i.e., comfase_run.py).

Follow the below steps to compile ComFASE from the command line to be able to use the **comfase_run.py** for test configuration and automation.

1. Go to **comfase** folder, open a cmd terminal to run ```$ ./configure``` then ```$ make -j <number of cores of your PC>```
2. Go to **Veins** folder, open a cmd terminal to run ```$ ./configure``` then ```$ make -j <number of cores of your PC>```
3. Go to **Plexe-Veins** folder, open a cmd terminal to run ```$ ./configure --with-veins ~/src/veins``` then ```$ make -j <number of cores of your PC>```
4. Go to **Plexe-Veins** folder, open **run.py** and update ***run_neds*** list as ```run_neds = ['../veins/src/veins', 'src/plexe', '../comfase/src']```
5. Finally, go to **Plexe-Veins/examples/platooning_comfase** folder and configure the parameters in **comfase_run.py** script according to the test requirement and execute the script. 

# ComFASE Execution
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
##                      DoS Attack                        #
###########################################################
*.comfase.DoSAttack = false
*.comfase.myPDforDoS		= ${myPDforDoS = 60}s 
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
## Result Analysis


## License

## Papers
* [IEEE-DSN](https://ieeexplore.ieee.org/document/9833738)
