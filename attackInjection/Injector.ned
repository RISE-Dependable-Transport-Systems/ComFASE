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

//package org.car2x.veins.base.phyLayer;
package org.car2x.veins.attackInjection;

// Basic physical layer module.
// See the class "BasePhyLayer" documentation.
//moduleinterface Injector
//simple Injector like ConnectionManager
simple Injector 
{
    parameters:
        @class(Injector);

         // Mehdi
        double attackStartTime @unit("s");
        double attackEndTime @unit("s");
        double myPDValue @unit("s");
        double myPDforDoS @unit("s");
        bool attackActive ;// = default(false);
        bool attackOnSender ;// = default(false);
  		bool attackOnReceiver ; //= default(false);
        int attackNode;
        bool DelayAttack;
        bool DoSAttack;           


}

