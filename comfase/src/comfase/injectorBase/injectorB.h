//
// ComFASE (Communication-Based Fault and Attack Simulation Engine)
// ComFASE is a tool for Simulation-Based Fault and Attack Injection at System-level.
// The purpose of simulation-based attack injection at system-level is to evaluate system's cybersecurity properties
// by injecting faults and attacks, e.g., using simulator control commands during target system simulations.

// authors:      Mehdi Maleki, Mateen Malik
// description: - Base class for ComFASE
//              - if you implement your own attack model to ComFASE, please use ComFASE "injectorBase" to extend comFASE.
//

#pragma once

#include "omnetpp.h"
using namespace omnetpp;

class injectorB : public cSimpleModule
{
protected:
    virtual void initialize();

    //Injector PDAttack;
public:

    //Injector target;

    /** @brief This parameter is used to set the attack start time */
    double attackStartTime;
    /** @brief This parameter is used to set the attack end time */
    double attackEndTime;
    /** @brief This parameter is used to set the attack value for PROPAGATION DELAY parameter */
    double myPDValue;
    /** @brief This parameter is used to set the attack value for Signal Power of frequency elements in the spectrum  */
    double myPowerValue;
    /** @brief This is the given attack value for Receive Signal Power elements */
    double myR_PowerValue;
    /** @brief This is the given attack value for Interference power elements */
    double myInterfValue;
    /** @brief This is the given DoS (Denial of Service) value for PROPAGATION DELAY parameter */
    double myPDforDoS;
    /** @brief This is a boolean which defines the attack injection status */
    bool attackActive;
    /** @brief This is a boolean which represents the attack on sender status */
    bool attackOnSender;
    /** @brief This is a boolean for receiver unit status */
    bool attackOnReceiver;
    /** @brief This is target node (vehicle) id */
    int attackNode;
    /** @brief This is a boolean which represents the Delay Attack status (Active=1, Not Active=0) */
    bool DelayAttack;
    /** @brief This is a boolean which represents the Varying Delay Attack status (Active=1, Not Active=0) */
    bool v_DelayAttack;
    /** @brief This is a boolean which represents the Delay Attack status (Active=1, Not Active=0) for teleoperation scenario */
    bool uc2_DelayAttack;
    /** @brief This parameter is used to set the attack value for PROPAGATION DELAY parameter in a teleoperation scenario*/
    double uc2_PDValue;
    /** @brief This is a boolean which represents the DoS Attack status (Active=1, Not Active=0) */
    bool DoSAttack;
    /** @brief This is a boolean which represents the Signal Power Attack status (Active=1, Not Active=0) */
    bool SignalPowerAttack;
    /** @brief This is a boolean which represents the status (Active=1, Not Active=0) of Signal Power Attack at the receiver */
    bool ReceivePowerAttack;
    /** @brief This is a boolean which represents the status (Active=1, Not Active=0) of Signal Interference Attack */
    bool InterferenceAttack;

    double t_m;

    //void PropagationDelayAttack();
    float PropagationDelayAttack(int senderID, int receiverID, float correctValue);
    float PropagationDelayAttack_varying(int senderID, int receiverID, float correctValue);
    float PropagationDelayAttack_uc2(int senderID, int receiverID, float correctValue);
    float DenialOfServiceAttack(int senderID, int receiverID, float correctValue);
    float PowerAttack(int senderID, int receiverID, float correctValue);
    float R_PowerAttack(int senderID, int receiverID, float correctValue);
    float InterfAttack(int senderID, int receiverID, float correctValue);
    float AttackInjectionEngine(int senderID, int receiverID, float correctValue);  // the idea was to have one Injection Engine but it didn't work!
    void BitFlipAttack();
    void JammingAttack();
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

