

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
    //    //Mehdi
    myPDValue        = par("myPDValue").doubleValue();
    myPDforDoS       = par("myPDforDoS").doubleValue();
    attackActive     = par("attackActive").boolValue();
    attackOnSender   = par("attackOnSender").boolValue();
    attackOnReceiver = par("attackOnReceiver").boolValue();
    attackStartTime  = par("attackStartTime").doubleValue();
    attackEndTime    = par("attackEndTime").doubleValue();
    attackNode       = par("attackNode").intValue();
    DelayAttack      = par("DelayAttack").boolValue();
    DoSAttack        = par("DoSAttack").boolValue();
   
    const char* strNodes = par("myNodes").stringValue();
    //const char str = myNodes;
    std::vector<double> vehicleList = cStringTokenizer(strNodes).asDoubleVector();
    std::cout<<"double list=========================================================================> "<<vehicleList.at(1)<<std::endl;
    //vList = vehicleList;
    vList.assign (vehicleList.begin(),vehicleList.end());
    std::cout<<"double list=========================================================================> "<<vList[1]<<std::endl;
    t_m = attackStartTime + 1.0;
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
# Attack Injection constructor for "PropagationDelay" parameter          #
##########################################################################*/
float injectorV::PropagationDelayAttack(int senderID, int receiverID, float correctValue)
{
    bool senderPart = injectorV::checkVehiclesList(senderID);
    bool receiverPart = injectorV::checkVehiclesList(receiverID);
    // Attack on SENDER part
    if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && !attackOnReceiver){
        std::cout<<"AttackActive = condition 1"<<std::endl;
        if (senderPart){
            return myPDValue;
        }
        else{
            return correctValue;
        }}
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && !attackOnSender && attackOnReceiver){
        std::cout<<"AttackActive = condition 2"<<std::endl;
        if (receiverPart){
            return myPDValue;
        }
        else{
            return correctValue;
        }}
    // Attack on SENDER and RECEIVER parts (both sides; then we use or (||) to apply this)
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && attackOnReceiver){
        std::cout<<"AttackActive = condition 3"<<std::endl;
        if (senderPart || receiverPart){
            return myPDValue;
        }
        else{
            return correctValue;
        }}
    else{
    // this time-point is used to calculate the distance between sending and receiving host
        //return receiverPos.distance(senderPos2) / BaseWorldUtility::speedOfLight();
        return correctValue;
    }
}

/*########################################################################
# Attack Injection constructor for "Denial of Service Attack" parameter  #
##########################################################################*/

float injectorV::DenialOfServiceAttack(int senderID, int receiverID, float correctValue)
{
    // Attack on SENDER part
    if (simTime()>=attackStartTime && attackOnSender && !attackOnReceiver){
        std::cout<<"AttackActive = condition 1"<<std::endl;
        if (senderID==attackNode){
            return myPDforDoS;
        }
        else{
            return correctValue;
        }}
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && !attackOnSender && attackOnReceiver){
        std::cout<<"AttackActive = condition 2"<<std::endl;
        if (receiverID==attackNode){
            return myPDforDoS;
        }
        else{
            return correctValue;
        }}
    // Attack on SENDER and RECEIVER parts (both sides; then we use or (||) to apply this)
    else if (simTime()>=attackStartTime && attackOnSender && attackOnReceiver){
        //std::cout<<"AttackActive = condition 3"<<std::endl;
        if (senderID==attackNode || receiverID==attackNode){
            std::cout<<"AttackActive = condition 3"<<std::endl;
            return myPDforDoS;
        }
        else{
            return correctValue;
        }}
    else{
    // this time-point is used to calculate the distance between sending and receiving host
        //return receiverPos.distance(senderPos2) / BaseWorldUtility::speedOfLight();
        return correctValue;
    }
}



