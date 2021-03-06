# -*- coding: utf-8 -*-
# Copyright (C) 2014 Dr. Ralf Schlatterbeck All rights reserved
# Reichergasse 131, A--3411 Weidling, Austria. rsc@runtux.com
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
#    CNDB.OMP.IP6_Pool
#
# Purpose
#    Model Attributes of an IPv6 network pool
#
# Revision Dates
#    20-Jun-2014 (RS) Creation
#    23-Jun-2014 (RS) Use correct type for `left`
#     3-Jul-2014 (RS) `IP_Pool` no longer `Link1`, rename
#                     `A_IP6_Netmask_Interval`
#    ««revision-date»»···
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _MOM.import_MOM        import *
from   _CNDB                  import CNDB
import _CNDB._OMP
from   _CNDB._OMP.Attr_Type         import A_IP6_Netmask_Interval

import _CNDB._OMP.IP_Pool

_Ancestor_Essence = CNDB.OMP.IP_Pool

class IP6_Pool (_Ancestor_Essence) :
    """Attributes of an IPv6 network pool."""

    class _Attributes (_Ancestor_Essence._Attributes) :

        _Ancestor = _Ancestor_Essence._Attributes

        ### Non-primary attributes

        class netmask_interval (A_IP6_Netmask_Interval) :
            """Limit netmasks to allocate from this %(type_name)s."""

            kind               = Attr.Optional

        # end class netmask_interval

    # end class _Attributes

# end class IP6_Pool

if __name__ != "__main__" :
    CNDB.OMP._Export ("*")
### __END__ CNDB.OMP.IP6_Pool
