# -*- coding: utf-8 -*-
# Copyright (C) 2012-2014 Mag. Christian Tanzer All rights reserved
# Glasauergasse 32, A--1130 Wien, Austria. tanzer@swing.co.at
# #*** <License> ************************************************************#
# This module is part of the package CNDB.GTW.
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
#    RST_addons
#
# Purpose
#    Addons for GTW.RST...
#
# Revision Dates
#     6-Dec-2012 (CT) Creation
#     7-Dec-2012 (CT) Continue creation
#    14-Dec-2012 (CT) Factor `Is_Owner_or_Manager`, set `child_permission_map`
#    14-Dec-2012 (CT) Factor `GTW.RST.TOP.MOM.Admin_Restricted`
#    14-Dec-2012 (CT) Factor `User_Entity`
#    17-Dec-2012 (CT) Add `User_Node_Dependent` and descendents
#    24-Apr-2013 (CT) Fix `Is_Owner_or_Manager.predicate`
#    25-Apr-2013 (CT) Add `eligible_objects`, `child_postconditions_map`,
#                     `_pre_commit_entity_check`
#    25-Apr-2013 (CT) Add `eligible_object_restriction`
#    28-Apr-2013 (CT) DRY `User_Node.form_parameters`
#    28-Apr-2013 (CT) Add `Login_has_Person`
#    30-Apr-2013 (CT) Add `Node_Manager_Error`, `_pre_commit_node_check`
#    30-Apr-2013 (CT) Remove `prefilled` from `User_Node.form_parameters` for
#                     `manager`
#     7-Oct-2013 (CT) Simplify `Is_Owner_or_Manager.predicate`
#                     * `belongs_to_node` works now
#                     * remove redefinitions of `query_filters_restricted`
#     7-Oct-2013 (CT) Add `User_Antenna`
#    10-Apr-2014 (CT) Add `Dashboard`
#    14-Apr-2014 (CT) Rename `belongs_to_node` to `my_node`
#    14-Apr-2014 (CT) Add `devices`, `interfaces` to `Dashboard`;
#                     add `User_Net_Interface`
#    17-Apr-2014 (CT) Add `Dashboard` divisions
#    18-Apr-2014 (CT) Add `person`, `address`, ..., to `Dashboard`
#    18-Apr-2014 (CT) Change `query_filters_restricted` to use `my_person`
#    19-Apr-2014 (CT) Add `_get_child` for `<div_name>`,
#                     `__getattr__` for `db_*`
#    26-Apr-2014 (CT) Add first draft of `_DB_E_Type_.GET` to render `MF3.Form`
#     2-May-2014 (CT) Remove `graphs` from `DB_Device.view_action_names`
#     2-May-2014 (CT) Put `name` in front of `view_field_names` of
#                     `DB_Device` and `DB_Interface`
#     2-May-2014 (CT) Add `skip` for `lifetime` to `DB_Node.form_attr_spec`
#     3-May-2014 (CT) Add and use `_setup_create_form_attr_spec`,
#                     redefine it for `DB_Device` and `DB_Interface`
#     4-May-2014 (CT) Redefine `DB_Interface.Creator` and `.Instance` to do
#                     IP allocation (very hackish for now)
#     4-May-2014 (CT) Add `DB_Interface.xtra_template_macro`
#     5-May-2014 (CT) Add `DB_Node.position`
#    17-Jun-2014 (CT) Add `DB_Person.Form_spec` to test `include_rev_refs`
#    20-Aug-2014 (CT) Adapt to changes of `GTW.RST.TOP.MOM.Admin`
#    29-Aug-2014 (CT) Adapt to changes of `GTW.RST.TOP.MOM.Admin`, again
#     1-Sep-2014 (CT) Add property `_DB_E_Type_.eligible_objects`,
#                     fix property `_DB_E_Type_.child_postconditions_map`
#     2-Sep-2014 (MB) Remove "graphs" action from node
#                     Remove "firmware" action from device
#     2-Sep-2014 (CT) Remove `_setup_create_mf3_attr_spec`
#                     (done by GTW.RST.TOP.MOM.Admin._Changer_, now)
#     3-Sep-2014 (CT) Add properties `_DB_E_Type_.query_filters_restricted`
#                     and `.user_restriction`
#     3-Sep-2014 (CT) Add `restrict_completion` for `DB_Device`, `DB_Interface`
#     3-Sep-2014 (MB) Add owner field to db_node
#     3-Sep-2014 (CT) Add `_get_dash`, `_DB_ETN_map`
#     3-Sep-2014 (CT) Move `_get_child` from `_DB_Div_Base_` to `_DB_Base_`
#     3-Sep-2014 (CT) Add `children_np` for partial `_DB_E_Type_` instances
#     3-Sep-2014 (CT) Add `DB_Wired_Interface`, `DB_Wireless_Interface`
#    ««revision-date»»···
#--

from   __future__ import absolute_import, division, print_function, unicode_literals

from   _CNDB                    import CNDB
from   _GTW                     import GTW
from   _JNJ                     import JNJ
from   _MOM                     import MOM
from   _TFL                     import TFL

import _CNDB._GTW
import _CNDB._OMP.import_CNDB

from   _GTW._MF3                import Element as MF3

import _GTW._RST._TOP.import_TOP
import _GTW._RST._TOP._MOM.import_MOM
import _GTW._RST._TOP._MOM.Admin_Restricted

from   _MOM.import_MOM          import Q

from   _TFL._Meta.Once_Property import Once_Property
from   _TFL.Decorator           import getattr_safe, Add_New_Method, Decorator
from   _TFL.I18N                import _, _T, _Tn
from   _TFL.predicate           import filtered_join
from   _TFL.Record              import Record
from   _TFL.update_combined     import update_combined

from   itertools                import chain as ichain

class Node_Manager_Error (MOM.Error._Invariant_, TypeError) :
    """You are not allowed to change owner or manager unless after the change
       you are still either owner or manager
    """

    class inv :
        name       = "Node_Manager_Error"

    def __init__ (self, obj, changed, user) :
        self.__super.__init__ (obj)
        self.obj          = obj
        self.changed      = tuple \
            ((c, getattr (obj.E_Type, c).ui_name_T) for c in changed)
        self.user         = user
        self.attributes   = ("manager", "owner")
        self.values = vs  = tuple \
            (  (v.ui_display if v is not None else v)
            for v in (getattr (obj, k) for k in self.attributes)
            )
        self.args         = (obj, changed, vs, user)
    # end def __init__

    @Once_Property
    def as_unicode (self) :
        bindings = dict (self.bindings)
        result = \
            ( _T( "You are not allowed to change %s unless afterwards "
                  "you [%s] are still either manager or owner"
                )
            % ( _T (" and ").join
                  ( "'%s' %s '%s'"
                  % (d, _T ("to"), bindings [k]) for k, d in self.changed
                  )
              , self.user
              )
            )
        return result
    # end def as_unicode

    @Once_Property
    def bindings (self) :
        return zip (self.attributes, self.values)
    # end def bindings

    @Once_Property
    def head (self) :
        return unicode (self)
    # end def head

# end class Node_Manager_Error

class Is_Owner_or_Manager (GTW.RST._Permission_) :
    """Permission if user is the owner or manager of the object"""

    def predicate (self, user, page, * args, ** kw) :
        if user :
            obj = getattr (page, "obj", None)
            if obj is not None :
                try :
                    qf = page.query_filters_restricted ()
                except AttributeError :
                    pass
                else :
                    if qf is not None :
                        return qf (obj)
    # end def predicate

# end class Is_Owner_or_Manager

class Login_has_Person (GTW.RST._Permission_) :
    """Permission if user has an associated person"""

    def predicate (self, user, page, * args, ** kw) :
        if user :
            return user.person is not None
    # end def predicate

# end class Login_has_Person

@Add_New_Method (CNDB.OMP.Net_Device, CNDB.OMP.Wired_Interface, CNDB.OMP.Wireless_Interface)
def _CNDB_User_Entity_PRC (self, resource, request, response, attribute_changes) :
    for eia in self.id_entity_attr :
        if eia.name in attribute_changes or eia.is_primary :
            ET = eia.E_Type
            eligible = resource.eligible_objects (ET.type_name)
            if eligible is not None :
                ent = getattr (self, eia.name)
                if ent not in eligible :
                    err = MOM.Error.Permission (self, eia, ent, eligible)
                    self.add_error (err)
                    raise err
# end def _CNDB_User_Entity_PRC

_pre_commit_entity_check = GTW.RST.MOM.Pre_Commit_Entity_Check \
    ("_CNDB_User_Entity_PRC")

@Add_New_Method (CNDB.OMP.Node)
def _CNDB_Node_PRC (self, resource, request, response, attribute_changes) :
    changed = tuple (k for k in ("manager", "owner") if k in attribute_changes)
    if changed :
        user = resource.user_restriction
        if not (self.manager is user or self.owner is user) :
            err = Node_Manager_Error (self, changed, user.ui_display)
            self.add_error (err)
            raise err
# end def _CNDB_Node_PRC

_pre_commit_node_check = GTW.RST.MOM.Pre_Commit_Entity_Check \
    ("_CNDB_Node_PRC")

_Ancestor = GTW.RST.TOP.MOM.Admin_Restricted.E_Type

class User_Entity (_Ancestor) :
    """Directory displaying instances of one E_Type owned or managed by """
    """the current user."""

    child_permission_map      = dict \
        ( change              = Is_Owner_or_Manager
        , delete              = Is_Owner_or_Manager
        )
    child_postconditions_map  = dict \
        ( create              = (_pre_commit_entity_check, )
        , change              = (_pre_commit_entity_check, )
        )
    et_map_name               = "admin_omu"
    restriction_desc          = _ ("owned/managed by")

    def __init__ (self, ** kw) :
        app_type = self.top.App_Type
        ET_Map   = self.top.ET_Map
        ETM      = kw.pop ("ETM", None) or self._ETM
        pns, etm = ETM.split (".")
        PNS      = app_type.PNS_Map [pns]
        Nav      = getattr (getattr (PNS, "Nav", None), "Admin", None)
        xkw      = dict (getattr (Nav, etm, {}), ETM = ETM, ** kw)
        self.__super.__init__ (** xkw)
    # end def __init__

    @property
    @getattr_safe
    def user_restriction (self) :
        user = self.top.user
        return user.person if user else None
    # end def user_restriction

    def eligible_objects (self, type_name) :
        etn = getattr (type_name, "type_name", type_name)
        adm = getattr (self.ET_Map.get (etn), self.et_map_name, None)
        if adm is not None :
            return adm.objects
    # end def eligible_objects

    def eligible_object_restriction (self, type_name) :
        etn = getattr (type_name, "type_name", type_name)
        adm = getattr (self.ET_Map.get (etn), self.et_map_name, None)
        if adm is not None :
            return adm.query_filters_restricted ()
    # end def eligible_object_restriction

    def query_filters_restricted (self) :
        person = self.user_restriction
        if person is not None :
            ### XXX remove when query expression below the `return` works
            return Q.my_person == person

            ### ATM, Q.my_group.member_links... doesn't work in QX
            ###
            ### - fix MOM.DBW.SAW.QX.Kind_Query to pass along
            ###   the `E_Type` of the query attribute `my_group`,
            ###   `my_person`, ...
            ###
            ### - additionally, maybe implement a Q-operator to restrict
            ###   the type of an `A_Id_Entity` expression to a subtype
            ###   to avoud the multiple definitions of `my_group` and
            ###   `my_person`
            ###
            ###   For instance::
            ###       Q.TYP.PAP.Group(Q.my_group)
            ###   or::
            ###       Q.my_group["PAP.Group"]
            ###
            ### Q.OR (Q.my_node.manager, Q.my_node.owner)["PAP.Person"]
            ###
            ### Q.TYP.PAP.Group (Q.OR (Q.my_node.manager, Q.my_node.owner))
            ###
            result = Q.OR \
                ( Q.my_person == person
                , Q.my_group.member_links.left == person
                )
            return result
    # end def query_filters_restricted

# end class User_Entity

class User_Node (User_Entity) :
    """Directory displaying the node instances belonging to the current user."""

    _ETM                  = "CNDB.Node"

    child_postconditions_map  = dict \
        ( User_Entity.child_postconditions_map
        , change = (_pre_commit_node_check, _pre_commit_entity_check)
        )

    @property
    @getattr_safe
    def mf3_attr_spec_d (self) :
        result = self.__super.mf3_attr_spec_d
        u = self.user_restriction
        if u is not None :
            result = update_combined \
                ( result
                , dict
                    ( manager = dict (default = u)
                    )
                )
        return result
    # end def mf3_attr_spec_d

# end class User_Node

class User_Node_Dependent (User_Entity) :
    """Temporary until query attributes with chained Q expressions work"""

    ET_depends            = "CNDB.Node" ### E_Type we depend on

    @Once_Property
    @getattr_safe
    def change_query_filters (self) :
        result = self.__super.change_query_filters [0]
        ETd    = getattr \
            (self.top.ET_Map [self.ET_depends], self.et_map_name, None)
        if ETd is not None :
            result = result | ETd.change_query_filters [0]
        return (result, )
    # end def change_query_filters

# end class User_Node_Dependent

class User_Antenna (User_Node_Dependent) :

    ET_depends            = "CNDB.Wireless_Interface_uses_Antenna"
    _ETM                  = "CNDB.Antenna"

# end class User_Antenna

class User_Net_Device (User_Node_Dependent) :

    _ETM                  = "CNDB.Net_Device"

    @property
    @getattr_safe
    def mf3_attr_spec_d (self) :
        result = self.__super.mf3_attr_spec_d
        u = self.top.user
        if u :
            u = u.person
            if u :
                result = update_combined \
                    ( result
                    , { "node.manager" : dict
                          ( default     = u
                          , prefilled   = True
                          )
                      }
                    )
        return result
    # end def mf3_attr_spec_d

# end class User_Net_Device

class User_Net_Interface (User_Node_Dependent) :

    ET_depends            = "CNDB.Net_Device"
    _ETM                  = "CNDB.Net_Interface"

# end class User_Net_Interface

class User_Person (User_Entity) :

    _ETM                  = "PAP.Person"

# end class User_Person

class _User_Person_has_Property_ (User_Entity) :

    ET_depends            = "PAP.Person"

# end class _User_Person_has_Property_

class User_Person_has_Account (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_Account"

# end class User_Person_has_Account

class User_Person_has_Address (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_Address"

# end class User_Person_has_Address

class User_Person_has_Email (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_Email"

# end class User_Person_has_Email

class User_Person_has_IM_Handle (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_IM_Handle"

# end class User_Person_has_IM_Handle

class User_Person_has_Phone (_User_Person_has_Property_) :

    _ETM                  = "PAP.Person_has_Phone"

# end class User_Person_has_Phone

class User_Wired_Interface (User_Node_Dependent) :

    ET_depends            = "CNDB.Net_Device"
    _ETM                  = "CNDB.Wired_Interface"

# end class User_Wired_Interface

class User_Wireless_Interface (User_Node_Dependent) :

    ET_depends            = "CNDB.Net_Device"
    _ETM                  = "CNDB.Wireless_Interface"

# end class User_Wireless_Interface

class User_Virtual_Wireless_Interface (User_Node_Dependent) :

    ET_depends            = "CNDB.Net_Device"
    _ETM                  = "CNDB.Virtual_Wireless_Interface"

# end class User_Virtual_Wireless_Interface

class User_Wireless_Interface_uses_Antenna (User_Node_Dependent) :

    ET_depends            = "CNDB.Wireless_Interface"
    _ETM                  = "CNDB.Wireless_Interface_uses_Antenna"

# end class User_Wireless_Interface_uses_Antenna

class User_Wireless_Interface_uses_Wireless_Channel (User_Node_Dependent) :

    ET_depends            = "CNDB.Wireless_Interface"
    _ETM                  = "CNDB.Wireless_Interface_uses_Wireless_Channel"

# end class User_Wireless_Interface_uses_Wireless_Channel

##### Dashboard ###############################################################

_Ancestor = GTW.RST.TOP.Dir

class _Meta_DB_Div_ (_Ancestor.__class__) :
    """Meta class of _DB_Div_"""

    def __init__ (cls, name, bases, dct) :
        cls.__m_super.__init__ (name, bases, dct)
        if name.startswith ("DB_") :
            cls.Div_Name   = name [3:]
            cls.div_name   = dn = cls.Div_Name.lower ()
            cls.app_div_id = cls.app_div_prefix + dn
            cls._entry_type_names = set \
                (et.type_name for et in cls._entry_types if et.type_name)
            if cls.type_name :
                cls._DB_ETN_map [cls.type_name] = cls
            setattr (cls, "fill_%s" % dn, True)
    # end def __init__

    def __call__ (cls, * args, ** kw) :
        result = cls.__m_super.__call__ (* args, ** kw)
        name   = cls.__name__
        if name.startswith ("DB_") :
            cls._db_name_map [name.lower ()] = result
            if result.type_name :
                dnm = result.parent._div_name_map
                dnm [result.div_name] = dnm [result.Div_Name] = result
        return result
    # end def __call__

# end class _Meta_DB_Div_

class _DB_Base_ (TFL.Meta.BaM (_Ancestor, metaclass = _Meta_DB_Div_)) :
    """Base class of dashboard classes"""

    app_div_class         = "pure-u-24-24"
    app_div_prefix        = "app-D:"
    app_typ_prefix        = "app-T:"
    skip_etag             = True
    type_name             = None
    _DB_ETN_map           = {}
    _db_name_map          = {}
    _entry_types          = ()
    _exclude_robots       = True

    def __init__ (self, ** kw) :
        self.__super.__init__ (** self._init_kw (** kw))
    # end def __init__

    @property
    @getattr_safe
    def entries (self) :
        result = self._entries
        if not result :
            entries = tuple  (T (parent = self) for T in self._entry_types)
            self.add_entries (* entries)
        return self._entries
    # end def entries

    def tr_instance_css_class (self, o) :
        return "%s-%d-" % (self.div_name, o.pid)
    # end def tr_instance_css_class

    def _get_child (self, child, * grandchildren) :
        self._populate_db_entries ()
        result = self.__super._get_child (child, * grandchildren)
        if result is None and child in self._div_name_map :
            result = self._div_name_map [child]
            if grandchildren :
                result = result._get_child (* grandchildren)
        return result
    # end def _get_child

    def _get_dash (self, tn) :
        et     = self.top.ET_Map [tn]
        result = getattr (et, _DB_E_Type_.et_map_name, None)
        if result is None :
            RT = self._DB_ETN_map.get (tn)
            if RT is not None :
                result = RT (parent = self)
        return result
    # end def _get_dash

    def _get_omu_admin (self, tn) :
        et     = self.top.ET_Map [tn]
        result = getattr (et, User_Entity.et_map_name, None)
        return result
    # end def _get_omu_admin

    def _init_kw (self, ** kw) :
        dkw = dict \
            ( name            = self.div_name
            , short_title     = self.Div_Name
            , title           = ": ".join ((self.parent.title, self.Div_Name))
            )
        result = dict (dkw, ** kw)
        return result
    # end def _init_kw

    def __getattr__ (self, name) :
        if name.startswith ("db_") :
            self._populate_db_entries ()
            dn_map = self._db_name_map
            if name in dn_map :
                result = dn_map [name]
                setattr (self, name, result)
                return result
        return self.__super.__getattr__ (name)
    # end def __getattr__

# end class _DB_Base_

class _DB_Div_Base_ (_DB_Base_) :

    _div_name_map         = {}

# end class _DB_Div_Base_

class _DB_Div_ (_DB_Div_Base_) :
    """Division of dashboard"""

    dir_template_name     = "html/dashboard/app.jnj"

# end class _DB_Div_

_Ancestor  = _DB_Base_
_MF3_Mixin = GTW.RST.TOP.MOM.Admin.E_Type_Mixin

class _DB_E_Type_ (_MF3_Mixin, _Ancestor) :
    """E_Type displayed by, and managed via, dashboard."""

    add_css_classes       = []
    app_div_prefix        = _Ancestor.app_typ_prefix
    et_map_name           = "dash"
    fill_edit             = True
    fill_user             = False
    fill_view             = False
    hidden                = True
    ui_allow_new          = True
    view_action_names     = ("filter", "edit", "delete")
    view_field_names      = ()    ### to be defined by subclass
    type_name             = None  ### to be defined by subclass

    child_permission_map     = property \
        (lambda s : s.admin.child_permission_map)

    child_postconditions_map = property \
        (lambda s : s.admin.child_postconditions_map)

    eligible_objects         = property \
        (lambda s : s.admin.eligible_objects)

    query_filters_restricted = property \
        (lambda s : s.admin.query_filters_restricted)

    user_restriction         = property \
        (lambda s : s.admin.user_restriction)

    class _Action_Override_ (GTW.RST.TOP._Base_) :

        fill_edit          = True
        name_postfix       = "FF"
        page_template_name = "html/dashboard/app.jnj"

    # end class _Action_Override_

    class _FF_Creator_ (_Action_Override_, _MF3_Mixin.Creator) :

        _real_name         = "Creator"

    Creator = _FF_Creator_ # end class

    class _FF_Instance_ (_Action_Override_, _MF3_Mixin.Instance) :

        _real_name         = "Instance"

    Instance = _FF_Instance_ # end class

    class _DB_E_Type_GET_ (_Ancestor.GET) :

        _real_name             = "GET"

        def __call__ (self, resource, request, response) :
            req_data = request.req_data
            if "create" in req_data :
                creator = resource._get_child ("create")
                return creator.GET () (creator, request, response)
            else :
                return self.__super.__call__ (resource, request, response)
        # end def __call__

    GET =  _DB_E_Type_GET_ # end class

    class _DB_E_Type_POST_ (_Ancestor.POST or GTW.RST.POST) :

        _real_name             = "POST"

        def __call__ (self, resource, request, response) :
            req_data = request.req_data
            if "qx_esf" in req_data :
                ### XXX ??? is this necessary ???
                json   = TFL.Record (** request.json)
                af     = resource._get_esf_filter (request, json)
                result = resource._rendered_esf   (af)
                return result
            else :
                return self.__super.__call__ (resource, request, response)
        # end def __call__

    POST =  _DB_E_Type_POST_ # end class

    _action_map           = dict \
        ( (r.name, r) for r in
            ( Record
                ( name = "change_password"
                , msg  = _ ("Change password of %s %s")
                , icon = "key"
                )
            , Record
                ( name = "create"
                , msg  = _ ("Create a new %s %s")
                , icon = "plus-circle"
                )
            , Record
                ( name = "delete"
                , msg  = _ ("Delete %s %s")
                , icon = "trash-o"
                )
            , Record
                ( name = "edit"
                , msg  = _ ("Edit %s %s")
                , icon = "pencil"
                )
            , Record
                ( name = "filter"
                , msg  = _
                    ("Restrict details below to objects belonging to %s %s")
                , icon = "eye"
                )
            , Record
                ( name = "firmware"
                , msg  = _ ("Generate firmware for %s %s")
                , icon = "magic"
                )
            , Record
                ( name = "graphs"
                , msg  = _ ("Show graphs and statistics about %s %s")
                , icon = "bar-chart-o"
                )
            , Record
                ( name = "reset_password"
                , msg  = _ ("I forgot my password; reset password of %s %s")
                , icon = "exclamation"
                )
            )
        )

    class _DB_Field_ (GTW.RST.TOP.MOM.Field.Attr) :

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
            return [self.attr_name]
        # end def add_css_classes

        @Once_Property
        @getattr_safe
        def css_class (self) :
            result = [self.__super.css_class] + self.add_css_classes
            return filtered_join (" ", result)
        # end def css_class

    Field = _DB_Field_ # end class

    class _Field_Ref_ (Field) :

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
            return [self.ref_name] ### don't want `__super.add_css_classes` here
        # end def add_css_classes

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def ui_name (self) :
            return _T (self.ref_name.capitalize ())
        # end def ui_name

    # end class _Field_Device_

    _Field_Created_ = GTW.RST.TOP.MOM.Field.Created

    class _Field_Device_ (_Field_Ref_) :

        ref_name          = "Device"

    # end class _Field_Device_

    class _Field_IP_Addresses_ (Field) :

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
            return ["ip-addresses"] ### don't want `__super.add_css_classes` here
        # end def add_css_classes

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def description (self) :
            return _T ("IP addresses assigned to interface")
        # end def description

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def ui_name (self) :
            return _T ("IP addresses")
        # end def ui_name

        def as_html (self, o, v) :
            return "<br>".join (v.split (", "))
        # end def as_thml

        def value (self, o) :
            return ", ".join \
                (   str (nw.net_address)
                for nw in ichain (o.ip4_networks, o.ip6_networks)
                )
        # end def value

    # end class _Field_IP_Addresses_

    class _Field_Node_ (_Field_Ref_) :

        ref_name          = "Node"

    # end class _Field_Node_

    class _Field_No_ (Field) :
        """Number-of field"""

        ### break inherited `property` to allow assignment in `__init__`
        attr_name         = None
        name              = None
        ui_name           = None

        def __init__ (self, name, attr_name, ET) :
            self.attr_name   = attr_name
            self.ET          = ET
            self.name        = name
            self.ui_name     = "#"
        # end def __init__

        @Once_Property
        @getattr_safe
        def attr (self) :
            return self.ET.attr_prop (self.attr_name)
        # end def attr

        @Once_Property
        @getattr_safe
        def add_css_classes (self) :
             ### don't want `__super.add_css_classes` here
            return ["number", self.name]
        # end def add_css_classes

        @property ### depends on currently selected language (I18N/L10N)
        @getattr_safe
        def description (self) :
            return _T (self._description) % \
                (self.attr.P_Type.ui_name_T, self.ET.ui_name_T)
        # end def description

        @Once_Property
        @getattr_safe
        def _description (self) :
            return _ ("Number of %s belonging to %s")
        # end def _description

        def value (self, o) :
            return len (getattr (o, self.attr_name))
        # end def value

    # end class _Field_No_

    class _Field_Type_ (_Field_Ref_) :

        icon_map = dict \
            ( W  = """<i class="fa fa-rss rotate-45-left"></i>"""
            )

        ref_name = "type"

        typ_map  = \
            { "CNDB.Virtual_Wireless_Interface" : "V"
            , "CNDB.Wired_Interface"            : "L"
            , "CNDB.Wireless_Interface"         : "W"
            }

        def value (self, o) :
            code = self.typ_map.get (o.type_name, o.ui_name_T)
            if code in self.icon_map :
                code = self.icon_map [code]
            result = """<span title="%s">%s</span""" % (o.ui_name_T, code)
            return result
        # end def value

    # end class _Field_Type_

    _field_type_map       = dict \
        ( { "my_net_device.name"    : _Field_Device_
          , "my_node.name"          : _Field_Node_
          }
        , creation_date   = _Field_Created_
        , type_name       = _Field_Type_
        )

    def __init__ (self, ** kw) :
        self.__super.__init__ (** kw)
        if self.ETM.is_partial :
            self.children_np ### materialize
    # end def __init__

    @Once_Property
    @getattr_safe
    def admin (self) :
        return self._get_omu_admin (self.type_name)
    # end def admin

    @Once_Property
    @getattr_safe
    def children_np (self) :
        E_Type = self.E_Type
        result = ()
        if E_Type.is_partial :
            def _gen (self, E_Type, dn_map) :
                for k in E_Type.children_np :
                    c = self._get_dash (k)
                    if c is not None :
                        yield c
            result = sorted \
                ( _gen (self, E_Type, self._db_name_map)
                , key = Q.E_Type.i_rank
                )
        return tuple (result)
    # end def children_np

    @Once_Property
    @getattr_safe
    def create_action (self) :
        if self.ui_allow_new :
            return self._action_map ["create"]
    # end def create_action

    @Once_Property
    @getattr_safe
    def eligible_object_restriction (self) :
        return self.admin.eligible_object_restriction
    # end def eligible_object_restriction

    @Once_Property
    @getattr_safe
    def ETM (self) :
        return self.admin.ETM
    # end def ETM

    @Once_Property
    @getattr_safe
    def E_Type (self) :
        return self.admin.E_Type
    # end def E_Type

    @property
    @getattr_safe
    def objects (self) :
        return self.admin.objects
    # end def objects

    @property
    @getattr_safe
    def pid_query_request (self):
        return self.admin.pid_query_request
    # end def pid_query_request

    @Once_Property
    @getattr_safe
    def QR (self) :
        return self.admin.QR
    # end def QR

    @Once_Property
    @getattr_safe
    def view_actions (self) :
        map = self._action_map
        return tuple (map [k] for k in self.view_action_names)
    # end def view_actions

    @Once_Property
    @getattr_safe
    def view_fields (self) :
        return self._fields (self.view_field_names)
    # end def view_fields

    @property
    @getattr_safe
    def view_title (self) :
        TN = self.Div_Name
        return _T ("%ss managed/owned by %s") % (TN, self.user.FO.person)
    # end def view_title

    @Once_Property
    @getattr_safe
    def _ETM (self) :
        return self.admin._ETM
    # end def _ETM

    def href_anchor_pid (self, obj) :
        return "#%s-%s" % (self.div_name, obj.pid) if obj else ""
    # end def href_anchor_pid

    def view_name_instance (self, o) :
        return o.FO.name
    # end def view_name_instance

    _fields = GTW.RST.TOP.MOM.Admin.E_Type._fields.__func__

    def _init_kw (self, ** kw) :
        return self.__super._init_kw (_field_map = {}, ** kw)
    # end def _init_kw

# end class _DB_E_Type_

class _DB_Person_Property_ (_DB_E_Type_) :

    view_action_names     = ("edit", "delete")
    view_field_names      = \
        ( "desc"
        , "right"
        , "creation_date"
        )

    @property
    @getattr_safe
    def mf3_attr_spec (self) :
        result = self.__super.mf3_attr_spec
        u = self.admin.user_restriction
        if u is not None :
            result = dict \
                ( result
                , left = dict (default = u, prefilled = "True")
                )
        return result
    # end def mf3_attr_spec

    @property
    @getattr_safe
    def view_title (self) :
        TN = self.Div_Name
        return _T ("%ss used by %s") % (TN, self.user.FO.person)
    # end def view_title

    def view_name_instance (self, o) :
        return o.right.FO
    # end def view_name_instance

# end class _DB_Person_Property_

class DB_Account (_DB_Person_Property_) :
    """PAP.Person_has_Account displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_Account"
    view_action_names     = \
        ("edit", "change_password", "reset_password")

    view_field_names      = \
        ( "right"
        , "creation_date"
        )

# end class DB_Account

class DB_Address (_DB_Person_Property_) :
    """PAP.Person_has_Address displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_Address"

    @property
    @getattr_safe
    def view_title (self) :
        return _T ("Addresses used by %s") % (self.user.FO.person, )
    # end def view_title

# end class DB_Address

class DB_Device (_DB_E_Type_) :
    """CNDB.Net_Device displayed by, and managed via, dashboard."""

    type_name             = "CNDB.Net_Device"

    view_action_names     = _DB_E_Type_.view_action_names
    view_field_names      = \
        ( "name"
        , "my_node.name"
        , "interfaces"
        # "type_name"
        , "creation_date"
        )

    _MF3_Attr_Spec        = dict \
        ( node            = dict (restrict_completion = True)
        )

    def __init__ (self, ** kw) :
        self.__super.__init__ (** kw)
        self._field_map.update \
            ( interfaces
            = self._Field_No_ ("interfaces", "net_interfaces", self.E_Type)
            )
    # end def __init__

    def tr_instance_css_class (self, o) :
        return "node-%d- device-%d-" % (o.my_node.pid, o.pid)
    # end def tr_instance_css_class

# end class DB_Device

class DB_Edit (_DB_Div_) :
    """Edit division of dashboard"""

    hidden                = True

# end class DB_Edit

class DB_Email (_DB_Person_Property_) :
    """PAP.Person_has_Email displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_Email"

# end class DB_Email

class DB_IM_Handle (_DB_Person_Property_) :
    """PAP.Person_has_IM_Handle displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_IM_Handle"

# end class DB_IM_Handle

_Ancestor = _DB_E_Type_

class _DB_Interface_ (_Ancestor) :

    _MF3_Attr_Spec        = dict \
        ( left            = dict (restrict_completion = True)
        )

    class _DBI_Action_Override_ (_Ancestor._Action_Override_) :

        # Freenet networks according to Wiki dokumentation (from call_convert)
        # This may be old info, ask Aaron
        # FIXME: in the future we will have permissions and don't need
        # to search by IP of network.
        freenet_networks = \
            [ '193.238.156.0/24'
            , '193.238.157.128/25'
            , '193.238.158.0/24'
            , '193.238.159.0/24'
            , '78.41.112.0/24'
            , '78.41.113.0/24'
            ]

        def _commit_scope_fv (self, scope, form_value, request, response) :
            iface = form_value.essence
            if not iface.ip4_networks :
                person = self.user.person ### XXX ??? iface.my_node.manager...
                try :
                    self._get_ip_for_interface (scope, person, iface)
                except Exception as exc :
                    logging.exception ("_get_ip_for_interface")
            self.__super._commit_scope_fv (scope, form_value, request, response)
        # end def _commit_scope_fv

        def _get_ip_for_interface (self, scope, owner, iface) :
            from rsclib.IP_Address import IP4_Address
            CNDB = scope.CNDB
            for ip in self.freenet_networks :
                ip  = IP4_Address (ip)
                net = CNDB.IP4_Network.instance (ip)
                try :
                    adr = net.allocate (32, owner)
                except CNDB.OMP.Error.No_Free_Address_Range :
                    continue
                CNDB.Net_Interface_in_IP4_Network (iface, adr, mask_len = 32)
                return adr
        # end def _get_ip_for_interface

    # end class _DBI_Action_Override_

    class _DBI_Creator (_DBI_Action_Override_, _DB_E_Type_.Creator) :

        _real_name         = "Creator"

    Creator = _DBI_Creator # end class

    class _DBI_Instance_ (_DBI_Action_Override_, _DB_E_Type_.Instance) :

        _real_name         = "Instance"

    Instance = _DBI_Instance_ # end class

# end class _DB_Interface_

_Ancestor = _DB_Interface_

class DB_Interface (_Ancestor) :
    """CNDB.Net_Interface displayed by, and managed via, dashboard."""

    app_div_class         = "pure-u-24-24"
    type_name             = "CNDB.Net_Interface"
    xtra_template_macro   = "html/dashboard/app.m.jnj, db_graph"

    view_field_names      = \
        ( "name"
        , "my_net_device.name"
        , "my_node.name"
        , "ip4_networks" ### rendered as `IP addresses` by _Field_IP_Addresses_
        , "type_name"
        , "creation_date"
        )

    _field_type_map       = dict \
        ( _DB_E_Type_._field_type_map
        , ip4_networks    = _DB_E_Type_._Field_IP_Addresses_
        )

    def tr_instance_css_class (self, o) :
        return "node-%d- device-%d- interface-%d-" % \
            (o.my_node.pid, o.my_net_device.pid, o.pid)
    # end def tr_instance_css_class

# end class DB_Interface

_Ancestor = _DB_Interface_

class DB_Wired_Interface (_Ancestor) :
    """CNDB.Wired_Interface displayed by, and managed via, dashboard."""

    type_name             = "CNDB.Wired_Interface"

# end class DB_Wired_Interface

class DB_Wireless_Interface (_Ancestor) :
    """CNDB.Wireless_Interface displayed by, and managed via, dashboard."""

    type_name             = "CNDB.Wireless_Interface"

# end class DB_Wireless_Interface

if 0 : ### Add this when there is an instance of User_Virtual_Wireless_Interface
    class DB_Virtual_Wireless_Interface (_Ancestor) :
        """CNDB.Virtual_Wireless_Interface displayed by, and managed via, dashboard."""

        type_name             = "CNDB.Virtual_Wireless_Interface"

    # end class DB_Virtual_Wireless_Interface

class DB_Node (_DB_E_Type_) :
    """CNDB.Node displayed by, and managed via, dashboard."""

    app_div_class         = "pure-u-12-24"
    type_name             = "CNDB.Node"
    xtra_template_macro   = "html/dashboard/app.m.jnj, db_node_map"

    view_field_names      = \
        ( "name"
        , "devices"
        , "creation_date"
        , "owner"
        )

    def __init__ (self, ** kw) :
        self.__super.__init__ (** kw)
        self._field_map.update \
            (devices = self._Field_No_ ("devices", "net_devices", self.E_Type))
    # end def __init__

    @property
    @getattr_safe
    def mf3_attr_spec_d (self) :
        result = {}
        u = self.admin.user_restriction
        if u is not None :
            result = dict \
                ( result
                , manager = dict (default = u)
                , owner   = dict (default = u)
                )
        result = dict \
            ( result
            # address  = dict (skip = True)
            , lifetime = dict (skip = True)
            )
        return result
    # end def mf3_attr_spec_d

    @property
    @getattr_safe
    def position (self) :
        lat, lon = (0, 0)
        n = 0
        for node in self.objects :
            if node.position.lat and node.position.lon :
                lat += node.position.lat
                lon += node.position.lon
                n += 1
        if n :
            lat /= n
            lon /= n
            result = self.E_Type.position.P_Type (lat, lon)
        else :
            result = self.E_Type.position.P_Type ()
        return result
    # end def position

# end class DB_Node

class DB_Person (_DB_E_Type_) :
    """PAP.Person displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person"

    ui_allow_new          = False
    view_action_names     = ("edit", )
    view_field_names      = \
        ( "ui_display"
        , "creation_date"
        )

    @property
    @getattr_safe
    def MF3_Form_Spec (self) :
        result = dict \
            ( include_rev_refs = ("addresses", "emails", "phones")
            )
        return result
    # end def MF3_Form_Spec

    @property
    @getattr_safe
    def view_title (self) :
        return _T ("Personal data of %s") % (self.user.FO.person, )
    # end def view_title

    def view_name_instance (self, o) :
        return o.FO
    # end def view_name_instance

# end class DB_Person

class DB_Phone (_DB_Person_Property_) :
    """PAP.Person_has_Phone displayed by, and managed via, dashboard."""

    type_name             = "PAP.Person_has_Phone"

# end class DB_Phone

class DB_User (_DB_Div_) :
    """User division of dashboard"""

    _entry_types          = \
        ( DB_Person
        , DB_Account
        , DB_Address
        , DB_Email
        , DB_IM_Handle
        , DB_Phone
        )

# end class DB_User

class DB_View (_DB_Div_) :
    """View division of dashboard"""

    _entry_types          = \
        ( DB_Node
        , DB_Device
        , DB_Interface
        )

# end class DB_View

_Ancestor = _DB_Div_Base_

class Dashboard (_Ancestor) :
    """CNDB dashboard"""

    pid                   = "Dashboard"

    _entry_types          = \
        ( DB_View
        , DB_User
        , DB_Edit
        )
    _entry_type_names     = \
        DB_View._entry_type_names | DB_User._entry_type_names

    def _init_kw (self, ** kw) :
        dkw = dict \
            ( name            = "dashboard"
            , short_title     = "Dashboard"
            , title           = "Funkfeuer Dashboard"
            , auth_required   = True
            , permission      = Login_has_Person
            )
        result = dict (dkw, ** kw)
        return result
    # end def _init_kw

    def _populate_db_entries (self) :
        ### populate `entries`, `entry_map`, `_div_name_map`
        for e in self.entries :
            e.entries
    # end def _populate_db_entries

# end class Dashboard

### __END__ RST_addons
