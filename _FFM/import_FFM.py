# -*- coding: iso-8859-15 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package FFM.
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this module. If not, see <http://www.gnu.org/licenses/>.
# #*** </License> ***********************************************************#
#
#++
# Name
#    FFM.import_FFM
#
# Purpose
#    Import FFM object model
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Add `Node_has_Net_Device`, `Wired_Interface`, `Net_Link`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _FFM                   import FFM

import _FFM.Entity

import _FFM.Antenna
import _FFM.Antenna_Type
import _FFM.Device
import _FFM.Device_Type
import _FFM.Firmware
import _FFM.IP4_Network
import _FFM.IP_Network
import _FFM.Net_Credentials
import _FFM.Net_Device
import _FFM.Net_Device_Type
import _FFM.Net_Interface
import _FFM.Node
import _FFM.Routing_Zone
import _FFM.Wired_Interface
import _FFM.Wireless_Interface

import _FFM.Wireless_Mode
import _FFM.Zone

import _FFM.Device_Type_made_by_Company
import _FFM.Net_Interface_in_IP4_Network
import _FFM.Net_Interface_in_IP_Network
import _FFM.Net_Link
import _FFM.Node_has_Net_Device
import _FFM.Wired_Link
import _FFM.Wireless_Interface_uses_Antenna
import _FFM.Wireless_Link

### __END__ FFM.import_FFM
