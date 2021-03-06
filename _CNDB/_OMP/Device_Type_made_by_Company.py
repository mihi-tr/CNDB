# -*- coding: utf-8 -*-
# Copyright (C) 2012-2013 Mag. Christian Tanzer All rights reserved
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
#    CNDB.OMP.Device_Type_made_by_Company
#
# Purpose
#    Model manufacturer of device-type
#
# Revision Dates
#     6-Mar-2012 (CT) Creation
#    15-May-2013 (CT) Rename `auto_cache` to `auto_rev_ref`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP
from   _GTW                   import GTW
from   _GTW._OMP._PAP         import PAP

import _CNDB._OMP.Device_Type

import _GTW._OMP._PAP.Company

_Ancestor_Essence = CNDB.OMP.Link2

class Device_Type_made_by_Company (_Ancestor_Essence) :
    """Model manufacturer of device-type."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Primary attributes

        class left (_Ancestor.left) :
            """Device type."""

            role_type          = CNDB.OMP.Device_Type
            auto_rev_ref       = True
            max_links          = 1

        # end class left

        class right (_Ancestor.right) :
            """Company manufacturing the device-type."""

            role_type          = PAP.Company
            role_name          = "manufacturer"
            ui_allow_new       = True

        # end class right

    # end class _Attributes

# end class Device_Type_made_by_Company

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.Device_Type_made_by_Company
