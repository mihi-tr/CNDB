# -*- coding: utf-8 -*-
# Copyright (C) 2012 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.OMP.
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
#    CNDB.OMP.Device_Type
#
# Purpose
#    Model the type of devices in CNDB
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    10-May-2012 (CT) Change `name` to `Primary`, `model_no` to
#                     `Primary_Optional`
#    10-May-2012 (RS) Change `name.length` to 40
#    13-Jun-2014 (RS) Add `ui_name` to `desc`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP

_Ancestor_Essence = CNDB.OMP.Object

class Device_Type (_Ancestor_Essence) :
    """Model the type of devices in CNDB.OMP."""

    is_partial = True

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class name (A_String) :
            """Name of device type"""

            kind               = Attr.Primary
            max_length         = 40
            ignore_case        = True
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)

        # end class name

        class model_no (A_String) :
            """Model number identifying the device type"""

            kind               = Attr.Primary_Optional
            max_length         = 40
            ignore_case        = True
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)

        # end class model_no

        class revision (A_String) :
            """Revision of hardware of device type"""

            kind               = Attr.Primary_Optional
            max_length         = 32
            ignore_case        = True
            completer          = Attr.Completer_Spec  (1, Attr.Selector.primary)

        # end class revision

        ### Non-primary attributes

        class desc (A_Text) :
            """Description of device type"""

            kind               = Attr.Optional
            ui_name            = "Description"

        # end class desc

    # end class _Attributes

# end class Device_Type

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Device_Type
