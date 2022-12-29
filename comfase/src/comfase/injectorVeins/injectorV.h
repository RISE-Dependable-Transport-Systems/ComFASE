
#pragma once
#include <string>
#include "omnetpp.h"
using namespace omnetpp;

class injectorV : public cSimpleModule
{
protected:
    virtual void initialize();

public:

    /** @brief This is the time when attack starts */
    double attackStartTime;
    /** @brief This is the time when attack ends if the attack is TRANSIENT */
    double attackEndTime;
    /** @brief This is a boolean for sender unit status */
    bool attackOnSender;
    /** @brief This is a boolean for receiver unit status */
    bool attackOnReceiver;
    /** @brief This is a boolean/double for Delay Attack model */
    bool delayAttack;
    double injectedPDValue;
    /** @brief This is a boolean/double for DoS Attack model */
    bool DoSAttack;
    double injectedPDforDoS;
    /** @brief This is a boolean/double for Destructive Interference Attack model */
    bool destructiveInterferenceAttack;
    double injectedDestructiveness;
    /** @brief This is a boolean/double for Barrage Jamming Attack model */
    bool barrageJammingAttack;
    double injectedNoiseValue;
    /** @brief This is a boolean/double for Deceptive Jamming Attack model */
    bool deceptiveJammingAttack;
    double injectedInterferenceValue;

    std::string targetNodes;
    std::vector<int> vList;

    float comfase_delayAttack(int senderID, int receiverID, float correctValue);
    float comfase_DoSAttack(int senderID, int receiverID, float correctValue);
    float comfase_destructiveInterferenceAttack(int senderID, int receiverID, float correctValue);
    float comfase_barrageJammingAttack(int senderID, int receiverID, float correctValue);
    float comfase_deceptiveJammingAttack(int senderID, int receiverID, float correctValue);

    bool checkVehiclesList(int vehicleID);
};


