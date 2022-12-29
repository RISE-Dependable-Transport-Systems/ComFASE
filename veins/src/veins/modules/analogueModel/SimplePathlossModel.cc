//
// Copyright (C) 2007 Technische Universitaet Berlin (TUB), Germany, Telecommunication Networks Group
// Copyright (C) 2007 Technische Universiteit Delft (TUD), Netherlands
// Copyright (C) 2007 Universitaet Paderborn (UPB), Germany
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
#include "veins/base/utils/FindModule.h"
#include "/opt/sim/Dev-3/comfase/src/comfase/injectorVeins/injectorV.h"
#include "veins/modules/analogueModel/SimplePathlossModel.h"

#include "veins/base/messages/AirFrame_m.h"

using namespace veins;

using veins::AirFrame;

void SimplePathlossModel::filterSignal(Signal* signal)
{
    //double signal_values = signal->getValues()
    //std::cout<<"Signal before attenuation= "<<signal->at(6)<<std::endl;
    auto senderPos = signal->getSenderPoa().pos.getPositionAt();
    auto receiverPos = signal->getReceiverPoa().pos.getPositionAt();

    /** Calculate the distance factor */
    double sqrDistance = useTorus ? receiverPos.sqrTorusDist(senderPos, playgroundSize) : receiverPos.sqrdist(senderPos);

    EV_TRACE << "sqrdistance is: " << sqrDistance << endl;

    if (sqrDistance <= 1.0) {
        // attenuation is negligible
        return;
    }

    // the part of the attenuation only depending on the distance
    double distFactor = pow(sqrDistance, -pathLossAlphaHalf) / (16.0 * M_PI * M_PI);
    EV_TRACE << "distance factor is: " << distFactor << endl;

    Signal attenuation(signal->getSpectrum());
    for (uint16_t i = 0; i < signal->getNumValues(); i++) {
        double wavelength = BaseWorldUtility::speedOfLight() / signal->getSpectrum().freqAt(i);
        attenuation.at(i) = (wavelength * wavelength) * distFactor;
    }
    *signal *= attenuation;
    //std::cout<<"Attenuation"<<attenuation<<std::endl;
    //double signal_values2 = signal->getValues();

//    if (simTime() >= 122){
//        signal->at(7)= 2.99107e-10;  //12.0118723363e-10;
//    }

/*
    auto comfase = FindModule<injectorV*>::findGlobalModule();
    int receiverID = 27; //frame->getArrivalModuleId();  //for now tried to keep the format of the function unchanged
    int senderID = 47; //frame->getSenderModuleId();
    if (comfase->ReceivePowerAttack){
        std::cout<<"Receive Power Attack = is Active"<<std::endl;
        float fpower = comfase->R_PowerAttack(senderID, receiverID, signal->at(7));
        signal->at(6) *= fpower;
        signal->at(7) *= fpower;
        signal->at(8) *= fpower;
    }

    if (simTime() > 7){
        std::cout<<"Signal after attenuation=?????????????????????????????????????????? "<<signal->at(7)<<" Time: "<<simTime()<<std::endl;
    }
    //std::cout<<"Signal after attenuation=?????????????????????????????????????????? "<<signal->at(7)<<std::endl;
*/
}
