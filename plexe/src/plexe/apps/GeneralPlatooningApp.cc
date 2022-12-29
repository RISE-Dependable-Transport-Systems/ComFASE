//
// Copyright (C) 2012-2019 Michele Segata <segata@ccs-labs.org>
// Copyright (C) 2018-2019 Julian Heinovski <julian.heinovski@ccs-labs.org>
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

#include "plexe/apps/GeneralPlatooningApp.h"

#include "plexe/protocols/BaseProtocol.h"
#include "veins/modules/mobility/traci/TraCIColor.h"
#include "veins/modules/mobility/traci/TraCIScenarioManager.h"
#include "veins/modules/messages/BaseFrame1609_4_m.h"
#include "veins/modules/utility/Consts80211p.h"
#include "veins/modules/mac/ieee80211p/Mac1609_4.h"

using namespace veins;

namespace plexe {

Define_Module(GeneralPlatooningApp);

void GeneralPlatooningApp::initialize(int stage)
{
    BaseApp::initialize(stage);

    if (stage == 1) {
        // connect maneuver application to protocol
        protocol->registerApplication(MANEUVER_TYPE, gate("lowerLayerIn"), gate("lowerLayerOut"), gate("lowerControlIn"), gate("lowerControlOut"));
        // register to the signal indicating failed unicast transmissions
        findHost()->subscribe(Mac1609_4::sigRetriesExceeded, this);

        std::string joinManeuverName = par("joinManeuver").stdstringValue();
        if (joinManeuverName == "JoinAtBack")
            joinManeuver = new JoinAtBack(this);
        else
            throw new cRuntimeError("Invalid join maneuver implementation chosen");
    }
}

bool GeneralPlatooningApp::isJoinAllowed() const
{
    return ((role == PlatoonRole::LEADER || role == PlatoonRole::NONE) && !inManeuver);
}

void GeneralPlatooningApp::startJoinManeuver(int platoonId, int leaderId, int position)
{
    ASSERT(getPlatoonRole() == PlatoonRole::NONE);
    ASSERT(!isInManeuver());

    JoinManeuverParameters params;
    params.platoonId = platoonId;
    params.leaderId = leaderId;
    params.position = position;
    joinManeuver->startManeuver(&params);
}

void GeneralPlatooningApp::sendUnicast(cPacket* msg, int destination)
{
    Enter_Method_Silent();
    take(msg);
    BaseFrame1609_4* unicast = new BaseFrame1609_4("UnicastMessage", msg->getKind());
    unicast->setRecipientAddress(destination);
    unicast->setChannelNumber(static_cast<int>(Channel::cch));
    unicast->encapsulate(msg);
    sendDown(unicast);
}

void GeneralPlatooningApp::handleLowerMsg(cMessage* msg)
{
    BaseFrame1609_4* unicast = check_and_cast<BaseFrame1609_4*>(msg);

    cPacket* enc = unicast->getEncapsulatedPacket();
    ASSERT2(enc, "received a UnicastMessage with nothing inside");

    if (enc->getKind() == MANEUVER_TYPE) {
        ManeuverMessage* mm = check_and_cast<ManeuverMessage*>(unicast->decapsulate());
        if (UpdatePlatoonFormation* msg = dynamic_cast<UpdatePlatoonFormation*>(mm)) {
            handleUpdatePlatoonFormation(msg);
            delete msg;
        }
        else {
            onManeuverMessage(mm);
        }
        delete unicast;
    }
    else {
        BaseApp::handleLowerMsg(msg);
    }
}

void GeneralPlatooningApp::handleUpdatePlatoonFormation(const UpdatePlatoonFormation* msg)
{
    if (getPlatoonRole() != PlatoonRole::FOLLOWER) return;
    if (msg->getPlatoonId() != positionHelper->getPlatoonId()) return;
    if (msg->getVehicleId() != positionHelper->getLeaderId()) return;

    // update formation information
    std::vector<int> f;
    for (unsigned int i = 0; i < msg->getPlatoonFormationArraySize(); i++) {
        f.push_back(msg->getPlatoonFormation(i));
    }
    positionHelper->setPlatoonFormation(f);
}

void GeneralPlatooningApp::setPlatoonRole(PlatoonRole r)
{
    role = r;
}

void GeneralPlatooningApp::onPlatoonBeacon(const PlatooningBeacon* pb)
{
    joinManeuver->onPlatoonBeacon(pb);
    // maintain platoon
    BaseApp::onPlatoonBeacon(pb);
}

void GeneralPlatooningApp::onManeuverMessage(ManeuverMessage* mm)
{
    joinManeuver->onManeuverMessage(mm);
    delete mm;
}

void GeneralPlatooningApp::fillManeuverMessage(ManeuverMessage* msg, int vehicleId, std::string externalId, int platoonId, int destinationId)
{
    msg->setKind(MANEUVER_TYPE);
    msg->setVehicleId(vehicleId);
    msg->setExternalId(externalId.c_str());
    msg->setPlatoonId(platoonId);
    msg->setDestinationId(destinationId);
}

UpdatePlatoonFormation* GeneralPlatooningApp::createUpdatePlatoonFormation(int vehicleId, std::string externalId, int platoonId, int destinationId, double platoonSpeed, int platoonLane, const std::vector<int>& platoonFormation)
{
    UpdatePlatoonFormation* msg = new UpdatePlatoonFormation("UpdatePlatoonFormation");
    fillManeuverMessage(msg, vehicleId, externalId, platoonId, destinationId);
    msg->setPlatoonSpeed(platoonSpeed);
    msg->setPlatoonLane(platoonLane);
    msg->setPlatoonFormationArraySize(platoonFormation.size());
    for (unsigned int i = 0; i < platoonFormation.size(); i++) {
        msg->setPlatoonFormation(i, platoonFormation[i]);
    }
    return msg;
}

void GeneralPlatooningApp::receiveSignal(cComponent* src, simsignal_t id, cObject* value, cObject* details)
{
    if (id == Mac1609_4::sigRetriesExceeded) {
        BaseFrame1609_4* frame = check_and_cast<BaseFrame1609_4*>(value);
        ManeuverMessage* mm = check_and_cast<ManeuverMessage*>(frame->getEncapsulatedPacket());
        if (frame) {
            joinManeuver->onFailedTransmissionAttempt(mm);
        }
    }
}

GeneralPlatooningApp::~GeneralPlatooningApp()
{
    delete joinManeuver;
}

} // namespace plexe
