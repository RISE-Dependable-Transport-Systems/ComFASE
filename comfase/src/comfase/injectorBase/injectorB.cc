
//
//

#include "../injectorBase/injectorB.h"

#include "omnetpp.h"
using std::endl;
using namespace omnetpp;

// Here we define the module to be able to call from main ned file (for instance from "Highway.ned" file in platooning scenario)
Define_Module(injectorB);


/*########################################################################
# Initialization of the defined parameters value                         #
##########################################################################*/
void injectorB::initialize()
{
    //
    myPDValue        = par("myPDValue").doubleValue();
    myPDforDoS       = par("myPDforDoS").doubleValue();
    attackActive     = par("attackActive").boolValue();
    // Parameters to set attack surface such as sender or receiver or both
    attackOnSender   = par("attackOnSender").boolValue();
    attackOnReceiver = par("attackOnReceiver").boolValue();
    // Parameters to set attack start and end times
    attackStartTime  = par("attackStartTime").doubleValue();
    attackEndTime    = par("attackEndTime").doubleValue();
    attackNode       = par("attackNode").intValue();
    DelayAttack      = par("DelayAttack").boolValue();
    v_DelayAttack    = par("v_DelayAttack").boolValue();
    uc2_DelayAttack  = par("uc2_DelayAttack").boolValue();
    uc2_PDValue      = par("uc2_PDValue").doubleValue();
    DoSAttack        = par("DoSAttack").boolValue();
    myPowerValue     = par("myPowerValue").doubleValue();
    myR_PowerValue   = par("myR_PowerValue").doubleValue();
    myInterfValue    = par("myInterfValue").doubleValue();
    SignalPowerAttack= par("SignalPowerAttack").boolValue();
    ReceivePowerAttack= par("ReceivePowerAttack").boolValue();
    InterferenceAttack= par("InterferenceAttack").boolValue();

    t_m = attackStartTime + 1.0;
}
/*########################################################################
# Attack Injection constructor for "PropagationDelay" parameter          #
##########################################################################*/
float injectorB::PropagationDelayAttack(int senderID, int receiverID, float correctValue)
{
    // Attack on SENDER part
    if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && !attackOnReceiver){
        std::cout<<"AttackActive = condition 1"<<std::endl;
        if (senderID==attackNode){
            return myPDValue;
        }
        else{
            return correctValue;
        }}
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && !attackOnSender && attackOnReceiver){
        std::cout<<"AttackActive = condition 2"<<std::endl;
        if (receiverID==attackNode){
            return myPDValue;
        }
        else{
            return correctValue;
        }}
    // Attack on SENDER and RECEIVER parts (both sides; then we use or (||) to apply this)
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && attackOnReceiver){
        std::cout<<"AttackActive = condition 3"<<std::endl;
        if (senderID==attackNode || receiverID==attackNode){
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

float injectorB::DenialOfServiceAttack(int senderID, int receiverID, float correctValue)
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



/*########################################################################
# Attack Injection constructor for "PropagationDelay" parameter          #
##########################################################################*/
float injectorB::PropagationDelayAttack_uc2(int senderID, int receiverID, float correctValue)
{
    if (simTime()>=attackStartTime && simTime()<=attackEndTime){
        //std::cout<<"AttackActive = condition 1"<<std::endl;
        //if (senderID==attackNode){
        return uc2_PDValue;
        }


    else{
    // this time-point is used to calculate the distance between sending and receiving host
        //return receiverPos.distance(senderPos2) / BaseWorldUtility::speedOfLight();
        return correctValue;
    }
}

/*########################################################################
# Attack Injection constructor for "PropagationDelay" parameter          #
##########################################################################*/
float injectorB::PropagationDelayAttack_varying(int senderID, int receiverID, float correctValue)
{
    std::cout<<"correct PD is = ** "<<correctValue<<std::endl;
    // Attack on SENDER part
    if (simTime()>=attackStartTime && simTime()<=attackEndTime){
        double timee = simTime().dbl() ;
        int mm = simTime().dbl() ;
        //simtime_t b = simTime() ;
        //double timee = b.dbl();
        std::cout<<"t_m is = ** "<<t_m<<"  mm = "<<mm<<std::endl;
        double tt = (timee - attackStartTime)/2 ;
        double ttt = floor(tt) ;
        double cc = (timee - attackStartTime)/6 ;
        double ccc = floor(cc) ;

        double varying_PDValue = (1+ttt) - (ccc*3) ;
//        if ( mm % 2 != 0){
//            std::cout <<"********************************************************** "<< mm << " is odd."<<std::endl;
//            varying_PDValue = 0;
//        }
        if (timee>=t_m && timee< t_m+1){
            varying_PDValue = 0;
        }
        if (timee > t_m +1)
            t_m+=2;
        if (timee>=attackStartTime + 5)
            varying_PDValue = 0;
        std::cout<<"AttackActive = ** "<<simTime()<<"  mm = "<<mm<<std::endl;
        std::cout<<"AttackActive = *3* "<<timee<<"  ttt = "<<ttt<<"  ccc =  "<<ccc<<"  value =  "<<varying_PDValue<<std::endl;
        return varying_PDValue;
    }

//        std::cout<<"AttackActive = condition 1"<<std::endl;
//        if (senderID==attackNode){
//            return myPDValue;
//        }
//        else{
//            return correctValue;
//        }}
//    // Attack on RECEIVER part
//    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && !attackOnSender && attackOnReceiver){
//        std::cout<<"AttackActive = condition 2"<<std::endl;
//        if (receiverID==attackNode){
//            return myPDValue;
//        }
//        else{
//            return correctValue;
//        }}
//    // Attack on SENDER and RECEIVER parts (both sides; then we use or (||) to apply this)
//    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnSender && attackOnReceiver){
//        std::cout<<"AttackActive = condition 3"<<std::endl;
//        if (senderID==attackNode || receiverID==attackNode){
//            return myPDValue;
//        }
//        else{
//            return correctValue;
//        }}
    else{
    // this time-point is used to calculate the distance between sending and receiving host
        //return receiverPos.distance(senderPos2) / BaseWorldUtility::speedOfLight();
        return correctValue;
    }
}
/*########################################################################
# Attack Injection constructor for "Signal Power" parameter          #
##########################################################################*/
float injectorB::PowerAttack(int senderID, int receiverID, float correctValue)
{
    // Attack on all
    if (simTime()>=attackStartTime && simTime()<=attackEndTime && !attackOnReceiver){
        std::cout<<"AttackActive = condition 1"<<std::endl;
        return myPowerValue;
        }
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnReceiver){
        std::cout<<"AttackActive = condition 2= "<<correctValue<<std::endl;
        if (receiverID==attackNode){
            return myPowerValue;
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
# Attack Injection constructor for "Signal Power" parameter          #
##########################################################################*/
float injectorB::R_PowerAttack(int senderID, int receiverID, float correctValue)
{
    // Attack on all
    if (simTime()>=attackStartTime && simTime()<=attackEndTime && !attackOnReceiver){
        std::cout<<"AttackActive = condition 1"<<std::endl;
        return myR_PowerValue * 1e-10;
        }
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnReceiver){
        std::cout<<"AttackActive = condition 2= "<<correctValue<<std::endl;
        if (receiverID==attackNode){
            return myR_PowerValue * 1e-10;
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
# Attack Injection constructor for "Interfernce Power" parameter          #
##########################################################################*/
float injectorB::InterfAttack(int senderID, int receiverID, float correctValue)
{
    // Attack on all
    if (simTime()>=attackStartTime && simTime()<=attackEndTime && !attackOnReceiver){
        std::cout<<"AttackActive = condition 1"<<std::endl;
        return myInterfValue * 1e-5;
        }
    // Attack on RECEIVER part
    else if (simTime()>=attackStartTime && simTime()<=attackEndTime && attackOnReceiver){
        std::cout<<"AttackActive = condition 2= "<<correctValue<<std::endl;
        if (receiverID==attackNode){
            return myInterfValue * 1e-5;
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
# Attack Injection Engine  #
##########################################################################*/

float injectorB::AttackInjectionEngine(int senderID, int receiverID, float correctValue)
{
    // Delay Attack
    if (DelayAttack){
        return PropagationDelayAttack(senderID, receiverID, correctValue);
    }
    // Varying Delay
    else if (v_DelayAttack){
        return PropagationDelayAttack_varying(senderID, receiverID, correctValue);
        }
    // uc2 Delay
    else if (uc2_DelayAttack){
        return PropagationDelayAttack_uc2(senderID, receiverID, correctValue);
        }
    // DoS Attackt
    else if (DoSAttack){
        return DenialOfServiceAttack(senderID, receiverID, correctValue);
        }
    // Power Attackt
    else if (SignalPowerAttack){
        return PowerAttack(senderID, receiverID, correctValue);
        }
    else {
        return correctValue;
    }
}

