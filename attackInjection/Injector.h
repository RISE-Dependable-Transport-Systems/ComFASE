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

#pragma once

#include "omnetpp.h"
using namespace omnetpp;

class Injector : public cSimpleModule
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


    //void PropagationDelayAttack();
    float PropagationDelayAttack(int senderID, int receiverID, float correctValue);
    float DenialOfServiceAttack(int senderID, int receiverID, float correctValue);
    float AttackInjectionEngine(int senderID, int receiverID, float correctValue);
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

