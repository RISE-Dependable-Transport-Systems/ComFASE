//
// Copyright (C) 2004 Telecommunication Networks Group (TKN) at Technische Universitaet Berlin, Germany.
//
// Documentation for these modules is at http://veins.car2x.org/
//
// SPDX-License-Identifier: GPL-2.0-or-later
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//

// author:      Marc Loebbers
// part of:     framework implementation developed by tkn
// description: - Base class for physical layers
//              - if you create your own physical layer, please subclass
//                from this class and use the sendToChannel() function!!


#include "omnetpp.h"
#include "veins/attackInjection/Injector.h"
using std::endl;
using namespace omnetpp;

// Here we define the module to be able to call from main ned file (for instance from "Highway.ned" file in platooning scenario)
Define_Module(Injector);


/*########################################################################
# Initialization of the defined parameters value                         #
##########################################################################*/
void Injector::initialize()
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

}
/*########################################################################
# Attack Injection constructor for "PropagationDelay" parameter          #
##########################################################################*/
float Injector::PropagationDelayAttack(int senderID, int receiverID, float correctValue)
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

float Injector::DenialOfServiceAttack(int senderID, int receiverID, float correctValue)
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
        std::cout<<"AttackActive = condition 3"<<std::endl;
        if (senderID==attackNode || receiverID==attackNode){
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
# Attack Injection Engine  #
##########################################################################*/

float Injector::AttackInjectionEngine(int senderID, int receiverID, float correctValue)
{
    // Delay Attack
    if (DelayAttack){
        return PropagationDelayAttack(senderID, receiverID, correctValue);
    }
    // Attack on RECEIVER part
    else if (DoSAttack){
        return DenialOfServiceAttack(senderID, receiverID, correctValue);
        }
    else {
        return correctValue;
    }
}
