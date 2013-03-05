# -*- coding: iso-8859-15 -*-
# Copyright (C) 2013 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package FFM.__test__.
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
#    FFM.__test__.IP_Network
#
# Purpose
#    Test IP_Network
#
# Revision Dates
#    26-Jan-2013 (CT) Creation
#     4-Mar-2013 (CT) Add tests for `allocate`
#     5-Mar-2013 (CT) Add tests for `reserve`
#    ��revision-date�����
#--

from   __future__  import absolute_import, division, print_function, unicode_literals

from   _FFM.__test__.model      import *
from   datetime                 import datetime

_test_code = """
    >>> scope = Scaffold.scope (%(p1)s, %(n1)s) # doctest:+ELLIPSIS
    Creating new scope MOMT__...

    >>> FFM = scope.FFM
    >>> PAP = scope.PAP
    >>> Adr = FFM.IP4_Network.net_address.P_Type

    >>> ff  = PAP.Association ("Funkfeuer", short_name = "0xFF", raw = True)
    >>> mg  = PAP.Person ("Glueck", "Martin", raw = True)
    >>> ak  = PAP.Person ("Kaplan", "Aaron", raw = True)
    >>> rs  = PAP.Person ("Schlatterbeck", "Ralf", raw = True)
    >>> ct  = PAP.Person ("Tanzer", "Christian", raw = True)
    >>> lt  = PAP.Person ("Tanzer", "Laurens", raw = True)
    >>> osc = PAP.Company ("Open Source Consulting", raw = True)

    >>> show_networks (FFM.IP4_Network)

    >>> ff_pool  = FFM.IP4_Network (('10.0.0.0/8', ), owner = ff, raw = True)
    >>> show_networks (FFM.IP4_Network)
    10.0.0.0/8         Funkfeuer                 False

    >>> show_network_count (FFM.IP4_Network)
    FFM.IP4_Network count: 1

    >>> osc_pool = ff_pool.allocate (16, osc)
    >>> show_networks (FFM.IP4_Network)
    10.0.0.0/8         Funkfeuer                 True
    10.0.0.0/9         Funkfeuer                 True
    10.0.0.0/10        Funkfeuer                 True
    10.0.0.0/11        Funkfeuer                 True
    10.0.0.0/12        Funkfeuer                 True
    10.0.0.0/13        Funkfeuer                 True
    10.0.0.0/14        Funkfeuer                 True
    10.0.0.0/15        Funkfeuer                 True
    10.128.0.0/9       Funkfeuer                 False
    10.64.0.0/10       Funkfeuer                 False
    10.32.0.0/11       Funkfeuer                 False
    10.16.0.0/12       Funkfeuer                 False
    10.8.0.0/13        Funkfeuer                 False
    10.4.0.0/14        Funkfeuer                 False
    10.2.0.0/15        Funkfeuer                 False
    10.0.0.0/16        Open Source Consulting    False
    10.1.0.0/16        Funkfeuer                 False

    >>> show_network_count (FFM.IP4_Network)
    FFM.IP4_Network count: 17

    >>> rs_pool = osc_pool.allocate (28, rs)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (osc_pool.net_address))
    10.0.0.0/16        Open Source Consulting    True
    10.0.0.0/17        Open Source Consulting    True
    10.0.0.0/18        Open Source Consulting    True
    10.0.0.0/19        Open Source Consulting    True
    10.0.0.0/20        Open Source Consulting    True
    10.0.0.0/21        Open Source Consulting    True
    10.0.0.0/22        Open Source Consulting    True
    10.0.0.0/23        Open Source Consulting    True
    10.0.0.0/24        Open Source Consulting    True
    10.0.0.0/25        Open Source Consulting    True
    10.0.0.0/26        Open Source Consulting    True
    10.0.0.0/27        Open Source Consulting    True
    10.0.128.0/17      Open Source Consulting    False
    10.0.64.0/18       Open Source Consulting    False
    10.0.32.0/19       Open Source Consulting    False
    10.0.16.0/20       Open Source Consulting    False
    10.0.8.0/21        Open Source Consulting    False
    10.0.4.0/22        Open Source Consulting    False
    10.0.2.0/23        Open Source Consulting    False
    10.0.1.0/24        Open Source Consulting    False
    10.0.0.128/25      Open Source Consulting    False
    10.0.0.64/26       Open Source Consulting    False
    10.0.0.32/27       Open Source Consulting    False
    10.0.0.0/28        Schlatterbeck Ralf        False
    10.0.0.16/28       Open Source Consulting    False

    >>> ct_addr = osc_pool.reserve (Adr ('10.0.0.1/32', raw = True), owner = ct)
    Traceback (most recent call last):
      ...
    Address_Already_Used: Address ("10.0.0.1", ) already in use by 'Schlatterbeck Ralf'

    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        False

    >>> show_network_count (FFM.IP4_Network)
    FFM.IP4_Network count: 41

    >>> ct_pool = rs_pool.allocate (30, ct)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.8/29        Schlatterbeck Ralf        False
    10.0.0.0/30        Tanzer Christian          False
    10.0.0.4/30        Schlatterbeck Ralf        False

    >>> ak_pool = rs_pool.allocate (28, ak)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [("10.0.0.0/28", )] of this IP4_Network doesn't contain a free subrange for mask length 28

    >>> ak_pool = rs_pool.allocate (30, ak)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.8/29        Schlatterbeck Ralf        False
    10.0.0.0/30        Tanzer Christian          False
    10.0.0.4/30        Kaplan Aaron              False

    >>> show_network_count (FFM.IP4_Network)
    FFM.IP4_Network count: 45

    >>> mg_pool = rs_pool.allocate (29, mg)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.8/29        Glueck Martin             False
    10.0.0.0/30        Tanzer Christian          False
    10.0.0.4/30        Kaplan Aaron              False

    >>> xx_pool = rs_pool.allocate (30, mg)
    Traceback (most recent call last):
      ...
    No_Free_Address_Range: Address range [("10.0.0.0/28", )] of this IP4_Network doesn't contain a free subrange for mask length 30

    >>> show_network_count (FFM.IP4_Network)
    FFM.IP4_Network count: 45

    >>> mg_addr = ct_pool.reserve (Adr ('10.0.0.1/32', raw = True), owner = mg)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.0/30        Tanzer Christian          True
    10.0.0.0/31        Tanzer Christian          True
    10.0.0.8/29        Glueck Martin             False
    10.0.0.4/30        Kaplan Aaron              False
    10.0.0.2/31        Tanzer Christian          False
    10.0.0.0           Tanzer Christian          False
    10.0.0.1           Glueck Martin             False

    >>> lt_addr = ct_pool.reserve (Adr ('10.0.0.2/32', raw = True), owner = lt)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.0/30        Tanzer Christian          True
    10.0.0.0/31        Tanzer Christian          True
    10.0.0.2/31        Tanzer Christian          True
    10.0.0.8/29        Glueck Martin             False
    10.0.0.4/30        Kaplan Aaron              False
    10.0.0.0           Tanzer Christian          False
    10.0.0.1           Glueck Martin             False
    10.0.0.2           Tanzer Laurens            False
    10.0.0.3           Tanzer Christian          False

    >>> rs_addr = ct_pool.reserve (Adr ('10.0.0.0/32', raw = True), owner = rs)
    >>> ct_addr = ct_pool.reserve (Adr ('10.0.0.3/32', raw = True), owner = ct)
    >>> show_networks (FFM.IP4_Network, Q.net_address.IN (rs_pool.net_address))
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.0.0.0/30        Tanzer Christian          True
    10.0.0.0/31        Tanzer Christian          True
    10.0.0.2/31        Tanzer Christian          True
    10.0.0.8/29        Glueck Martin             False
    10.0.0.4/30        Kaplan Aaron              False
    10.0.0.0           Schlatterbeck Ralf        False
    10.0.0.1           Glueck Martin             False
    10.0.0.2           Tanzer Laurens            False
    10.0.0.3           Tanzer Christian          False

    >>> ct_addr = ff_pool.reserve (Adr ('10.42.137.1/32', raw = True), owner = ct)
    >>> show_networks (FFM.IP4_Network)
    10.0.0.0/8         Funkfeuer                 True
    10.0.0.0/9         Funkfeuer                 True
    10.0.0.0/10        Funkfeuer                 True
    10.0.0.0/11        Funkfeuer                 True
    10.32.0.0/11       Funkfeuer                 True
    10.0.0.0/12        Funkfeuer                 True
    10.32.0.0/12       Funkfeuer                 True
    10.0.0.0/13        Funkfeuer                 True
    10.40.0.0/13       Funkfeuer                 True
    10.0.0.0/14        Funkfeuer                 True
    10.40.0.0/14       Funkfeuer                 True
    10.0.0.0/15        Funkfeuer                 True
    10.42.0.0/15       Funkfeuer                 True
    10.0.0.0/16        Open Source Consulting    True
    10.42.0.0/16       Funkfeuer                 True
    10.0.0.0/17        Open Source Consulting    True
    10.42.128.0/17     Funkfeuer                 True
    10.0.0.0/18        Open Source Consulting    True
    10.42.128.0/18     Funkfeuer                 True
    10.0.0.0/19        Open Source Consulting    True
    10.42.128.0/19     Funkfeuer                 True
    10.0.0.0/20        Open Source Consulting    True
    10.42.128.0/20     Funkfeuer                 True
    10.0.0.0/21        Open Source Consulting    True
    10.42.136.0/21     Funkfeuer                 True
    10.0.0.0/22        Open Source Consulting    True
    10.42.136.0/22     Funkfeuer                 True
    10.0.0.0/23        Open Source Consulting    True
    10.42.136.0/23     Funkfeuer                 True
    10.0.0.0/24        Open Source Consulting    True
    10.42.137.0/24     Funkfeuer                 True
    10.0.0.0/25        Open Source Consulting    True
    10.42.137.0/25     Funkfeuer                 True
    10.0.0.0/26        Open Source Consulting    True
    10.42.137.0/26     Funkfeuer                 True
    10.0.0.0/27        Open Source Consulting    True
    10.42.137.0/27     Funkfeuer                 True
    10.0.0.0/28        Schlatterbeck Ralf        True
    10.42.137.0/28     Funkfeuer                 True
    10.0.0.0/29        Schlatterbeck Ralf        True
    10.42.137.0/29     Funkfeuer                 True
    10.0.0.0/30        Tanzer Christian          True
    10.42.137.0/30     Funkfeuer                 True
    10.0.0.0/31        Tanzer Christian          True
    10.0.0.2/31        Tanzer Christian          True
    10.42.137.0/31     Funkfeuer                 True
    10.128.0.0/9       Funkfeuer                 False
    10.64.0.0/10       Funkfeuer                 False
    10.16.0.0/12       Funkfeuer                 False
    10.48.0.0/12       Funkfeuer                 False
    10.8.0.0/13        Funkfeuer                 False
    10.32.0.0/13       Funkfeuer                 False
    10.4.0.0/14        Funkfeuer                 False
    10.44.0.0/14       Funkfeuer                 False
    10.2.0.0/15        Funkfeuer                 False
    10.40.0.0/15       Funkfeuer                 False
    10.1.0.0/16        Funkfeuer                 False
    10.43.0.0/16       Funkfeuer                 False
    10.0.128.0/17      Open Source Consulting    False
    10.42.0.0/17       Funkfeuer                 False
    10.0.64.0/18       Open Source Consulting    False
    10.42.192.0/18     Funkfeuer                 False
    10.0.32.0/19       Open Source Consulting    False
    10.42.160.0/19     Funkfeuer                 False
    10.0.16.0/20       Open Source Consulting    False
    10.42.144.0/20     Funkfeuer                 False
    10.0.8.0/21        Open Source Consulting    False
    10.42.128.0/21     Funkfeuer                 False
    10.0.4.0/22        Open Source Consulting    False
    10.42.140.0/22     Funkfeuer                 False
    10.0.2.0/23        Open Source Consulting    False
    10.42.138.0/23     Funkfeuer                 False
    10.0.1.0/24        Open Source Consulting    False
    10.42.136.0/24     Funkfeuer                 False
    10.0.0.128/25      Open Source Consulting    False
    10.42.137.128/25   Funkfeuer                 False
    10.0.0.64/26       Open Source Consulting    False
    10.42.137.64/26    Funkfeuer                 False
    10.0.0.32/27       Open Source Consulting    False
    10.42.137.32/27    Funkfeuer                 False
    10.0.0.16/28       Open Source Consulting    False
    10.42.137.16/28    Funkfeuer                 False
    10.0.0.8/29        Glueck Martin             False
    10.42.137.8/29     Funkfeuer                 False
    10.0.0.4/30        Kaplan Aaron              False
    10.42.137.4/30     Funkfeuer                 False
    10.42.137.2/31     Funkfeuer                 False
    10.0.0.0           Schlatterbeck Ralf        False
    10.0.0.1           Glueck Martin             False
    10.0.0.2           Tanzer Laurens            False
    10.0.0.3           Tanzer Christian          False
    10.42.137.0        Funkfeuer                 False
    10.42.137.1        Tanzer Christian          False
    >>> show_network_count (FFM.IP4_Network)
    FFM.IP4_Network count: 93

"""

def show_networks (ETM, * qargs, ** qkw) :
    sk = TFL.Sorted_By \
        ("-has_children", "net_address.address.mask", "net_address.address.ip")
    for nw in ETM.query (* qargs, sort_key = sk, ** qkw) :
        print \
            ( "%-18s %-25s %s"
            % (nw.FO.net_address, nw.FO.owner, nw.has_children)
            )
# end def show_networks

def show_network_count (ETM) :
    print ("%s count: %s" % (ETM.type_name, ETM.count))
# end def show_network_count

__test__ = Scaffold.create_test_dict \
  ( dict
      ( main       = _test_code
      )
  )

### __END__ FFM.__test__.IP_Network
