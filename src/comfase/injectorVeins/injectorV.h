#pragma once
#include <string>
#include "omnetpp.h"
using namespace omnetpp;

class injectorV : public cSimpleModule
{
protected:
    virtual void initialize();

    //Injector PDAttack;
public:

    //Injector target;

    /** @brief This is the time when attack starts */
    double attackStartTime;
    /** @brief This is the time when attack ends if the attack is TRANSIENT */
    double attackEndTime;
    /** @brief This is the given attack value for PROPAGATION DELAY parameter */
    double myPDValue;
    /** @brief This is the given DoS value for PROPAGATION DELAY parameter */
    double myPDforDoS;
    /** @brief This is a boolean which defines the attack injection status */
    bool attackActive;
    /** @brief This is a boolean for sender unit status */
    bool attackOnSender;
    /** @brief This is a boolean for receiver unit status */
    bool attackOnReceiver;
    /** @brief This is target node (vehicle) id */
    int attackNode;
    bool DelayAttack;
    bool DoSAttack;

    std::string myNodes;
    std::vector<int> vList;
    //std::list<int> vList;
    double t_m;

    float PropagationDelayAttack(int senderID, int receiverID, float correctValue);
    float DenialOfServiceAttack(int senderID, int receiverID, float correctValue);
    void BitFlipAttack();
    void JammingAttack();
    bool checkVehiclesList(int vehicleID);
    //void initialize(int stage) override;
//protected:
//    /** @brief Initialization of the module and some variables.*/
//    void initialize(int) override;
};
/*
//A child class of Injector
class PDAttack: protected Injector {
};
class BitAttack: protected Injector {
};
class JammingAttack: protected Injector {
};
*/

