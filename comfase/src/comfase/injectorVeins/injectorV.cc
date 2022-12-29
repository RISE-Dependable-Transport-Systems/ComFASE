

#include "../injectorVeins/injectorV.h"

#include "omnetpp.h"
using std::endl;
using namespace omnetpp;
#include <algorithm>
// Here we define the module to be able to call from main ned file (for instance from "Highway.ned" file in platooning scenario)
Define_Module(injectorV);


/*########################################################################
# Initialization of the defined parameters value                         #
##########################################################################*/
void injectorV::initialize()
{
    //

    // Parameters to set attack start and end times
    attackStartTime  = par("attackStartTime").doubleValue();
    attackEndTime    = par("attackEndTime").doubleValue();
    // Parameters to set attack surface such as sender or receiver or both
    attackOnSender   = par("attackOnSender").boolValue();
    attackOnReceiver = par("attackOnReceiver").boolValue();
    // Delay and DoS attacks
    delayAttack      = par("delayAttack").boolValue();
    injectedPDValue        = par("injectedPDValue").doubleValue();
    DoSAttack        = par("DoSAttack").boolValue();
    injectedPDforDoS       = par("injectedPDforDoS").doubleValue();
    // Jamming attacks
    destructiveInterferenceAttack= par("destructiveInterferenceAttack").boolValue();
    injectedDestructiveness     = par("injectedDestructiveness").doubleValue();
    barrageJammingAttack      = par("barrageJammingAttack").boolValue();
    injectedNoiseValue    = par("injectedNoiseValue").doubleValue();
    deceptiveJammingAttack= par("deceptiveJammingAttack").boolValue();
    injectedInterferenceValue    = par("injectedInterferenceValue").doubleValue();



    //myNodes= par("myNodes").stdstringValue();
    //const char* strController = par("controller").stringValue();
    const char* strNodes = par("targetNodes").stringValue();
    //const char str = myNodes;
    std::vector<double> vehicleList = cStringTokenizer(strNodes).asDoubleVector();
    std::cout<<"double list=========================================================================> "<<vehicleList.at(1)<<std::endl;
    //vList = vehicleList;
    vList.assign (vehicleList.begin(),vehicleList.end());
    std::cout<<"double list=========================================================================> "<<vList[1]<<std::endl;
}
/*########################################################################
# Attack Injection constructor for checking vehicle ID          #
##########################################################################*/
bool injectorV::checkVehiclesList(int vehicleID)
{
    bool result = false;
    if(std::find(vList.begin(), vList.end(), vehicleID) != vList.end() )
    {
        result = true;
    }
    return result;
}
/*########################################################################
# Attack Injection constructor for "Delay Attack" parameter          #
##########################################################################*/
float injectorV::comfase_delayAttack(int senderID, int receiverID, float correctValue)
{
    bool senderPart = injectorV::checkVehiclesList(senderID);
    bool receiverPart = injectorV::checkVehiclesList(receiverID);
    // Attack on SENDER part
    if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && !attackOnReceiver){
        std::cout<<"Delay Attack on Sender is Active"<<std::endl;
        if (senderPart){
            return injectedPDValue;
        }
        else{
            return correctValue;
        }}
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && !attackOnSender && attackOnReceiver){
        std::cout<<"Delay Attack on Receiver is Active"<<std::endl;
        if (receiverPart){
            return injectedPDValue;
        }
        else{
            return correctValue;
        }}
    // Attack on SENDER and RECEIVER parts (both sides; then we use 'or' (||) to apply this)
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && attackOnReceiver){
        std::cout<<"Delay Attack on Sender&Receiver is Active"<<std::endl;
        if (senderPart || receiverPart){
            return injectedPDValue;
        }
        else{
            return correctValue;
        }}
    else{
        return correctValue;
    }
}

/*########################################################################
# Attack Injection constructor for "DoS Attack" parameter  #
##########################################################################*/

float injectorV::comfase_DoSAttack(int senderID, int receiverID, float correctValue)
{
    bool senderPart = injectorV::checkVehiclesList(senderID);
    bool receiverPart = injectorV::checkVehiclesList(receiverID);
    // Attack on SENDER part
    if (simTime()>=attackStartTime && attackOnSender && !attackOnReceiver){
        std::cout<<"DoS Attack on Sender is Active"<<std::endl;
        if (senderPart){
            return injectedPDforDoS;
        }
        else{
            return correctValue;
        }}
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && !attackOnSender && attackOnReceiver){
        std::cout<<"DoS Attack on Receiver is Active"<<std::endl;
        if (receiverPart){
            return injectedPDforDoS;
        }
        else{
            return correctValue;
        }}
    // Attack on SENDER and RECEIVER parts (both sides; then we use 'or' (||) to apply this)
    else if (simTime()>=attackStartTime && attackOnSender && attackOnReceiver){
        if (senderPart || receiverPart){
            std::cout<<"DoS Attack on Sender&Receiver is Active"<<std::endl;
            return injectedPDforDoS;
        }
        else{
            return correctValue;
        }}
    else{
        return correctValue;
    }
}

/*########################################################################
# Attack Injection constructor for "Destructive Interference Attack" parameter          #
##########################################################################*/
float injectorV::comfase_destructiveInterferenceAttack(int senderID, int receiverID, float correctValue)
{
    bool senderPart = injectorV::checkVehiclesList(senderID);
    bool receiverPart = injectorV::checkVehiclesList(receiverID);
    // Attack on SENDER part
    if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && !attackOnReceiver){
        std::cout<<"Destructive Interference Attack on Sender is Active"<<std::endl;
        if (senderPart){
            float powwer_reduction_factor = 1 - injectedDestructiveness;
            return powwer_reduction_factor;
        }
        else{
            return 1;
        }}
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && !attackOnSender && attackOnReceiver){
        std::cout<<"Destructive Interference Attack on Receiver is Active"<<std::endl;
        if (receiverPart){
            float powwer_reduction_factor = 1 - injectedDestructiveness;
            return powwer_reduction_factor;
        }
        else{
            return 1;
        }}
    // Attack on SENDER and RECEIVER parts (both sides; then we use or (||) to apply this)
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && attackOnReceiver){
        std::cout<<"Destructive Interference Attack on Sender&Receiver is Active"<<std::endl;
        if (senderPart || receiverPart){
            float powwer_reduction_factor = 1 - injectedDestructiveness;
            return powwer_reduction_factor;
        }
        else{
            return 1;
        }}
    else{
        return 1;
    }
}
/*########################################################################
# Attack Injection constructor for "Deceptive Jamming" parameter        #
##########################################################################*/
float injectorV::comfase_deceptiveJammingAttack(int senderID, int receiverID, float correctValue)
{
    bool senderPart = injectorV::checkVehiclesList(senderID);
    bool receiverPart = injectorV::checkVehiclesList(receiverID);
    // Attack on all vehicles
    if (simTime()>=attackStartTime && simTime()<=attackEndTime){
        std::cout<<"Deceptive Jamming Attack on Sender&Receiver is Active"<<std::endl;
        return injectedInterferenceValue * 1e-5; // range: (0.0 to 1.0)*1e-5mW
        }
    else{
        return correctValue;
    }
}
/*########################################################################
# Attack Injection constructor for "Barrage Jamming" Attack              #
##########################################################################*/
float injectorV::comfase_barrageJammingAttack(int senderID, int receiverID, float correctValue)
{
    // Attack on all vehicles
    if (simTime()>=attackStartTime && simTime()<=attackEndTime){
        std::cout<<"Barrage Jamming Attack on Sender&Receiver is Active"<<std::endl;
        return injectedNoiseValue* 1e-5; // range: (0.0 to 1.0)*1e-5mW
        }

    else{
        return correctValue;
    }
}



