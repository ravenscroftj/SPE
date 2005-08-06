# text_ctrl.py: wxTextCtrl objects
# $Id: text_ctrl.py,v 1.15 2005/05/06 21:48:17 agriggio Exp $
#
# Copyright (c) 2002-2005 Alberto Griggio <agriggio@users.sourceforge.net>
# License: MIT (see license.txt)
# THIS PROGRAM COMES WITH NO WARRANTY

from wxPython.wx import *
from edit_windows import ManagedBase, WindowBase
from tree import Tree
import common, misc
from widget_properties import *

class EditTextCtrl(ManagedBase):
    """\
    Class to handle wxTextCtrl objects
    """

    events = [
        'EVT_TEXT',
        'EVT_TEXT_ENTER',
        'EVT_TEXT_URL',
        'EVT_TEXT_MAXLEN',
        ]
    
    def __init__(self, name, parent, id, sizer, pos, property_window,
                 show=True):
        import config
        ManagedBase.__init__(self, name, 'wxTextCtrl', parent, id, sizer, pos,
                             property_window, show=show)
        self.value = ""
        self.style = 0
        self.access_functions['value'] = (self.get_value, self.set_value)
        self.access_functions['style'] = (self.get_style, self.set_style)
        prop = self.properties
        # value property
        prop['value'] = TextProperty(self, 'value', None,
                                     multiline=True)
        # style property
        self.style_pos  = (wxTE_PROCESS_ENTER, wxTE_PROCESS_TAB,
                           wxTE_MULTILINE,wxTE_PASSWORD, wxTE_READONLY,
                           wxHSCROLL, wxTE_RICH, wxTE_RICH2, wxTE_AUTO_URL,
                           wxTE_NOHIDESEL, wxTE_CENTRE, wxTE_RIGHT,
                           wxTE_LINEWRAP, wxTE_WORDWRAP, wxNO_BORDER)
        style_labels = ('#section#Style', 'wxTE_PROCESS_ENTER',
                        'wxTE_PROCESS_TAB', 'wxTE_MULTILINE', 'wxTE_PASSWORD',
                        'wxTE_READONLY', 'wxHSCROLL', 'wxTE_RICH',
                        'wxTE_RICH2', 'wxTE_AUTO_URL', 'wxTE_NOHIDESEL',
                        'wxTE_CENTRE', 'wxTE_RIGHT', 'wxTE_LINEWRAP',
                        'wxTE_WORDWRAP', 'wxNO_BORDER')
        prop['style'] = CheckListProperty(self, 'style', None, style_labels)
        # 2003-09-04 added default_border
        if config.preferences.default_border:
            self.border = config.preferences.default_border_size
            self.flag = wxALL

    def create_widget(self):
        value = self.value
        if self.style & wxTE_MULTILINE:
            value = value.replace('\\n', '\n')
        self.widget = wxTextCtrl(self.parent.widget, self.id, value=value,
                                 style=self.style & wxTE_MULTILINE)

    def create_properties(self):
        ManagedBase.create_properties(self)
        panel = wxScrolledWindow(self.notebook, -1, style=wxTAB_TRAVERSAL) 
        prop = self.properties
        prop['value'].display(panel)
        prop['style'].display(panel)
        szr = wxBoxSizer(wxVERTICAL)
        szr.Add(prop['value'].panel, 0, wxEXPAND)
        szr.Add(prop['style'].panel, 0, wxEXPAND)
        panel.SetAutoLayout(True)
        panel.SetSizer(szr)
        szr.Fit(panel)
        self.notebook.AddPage(panel, 'Widget')
        import math
        panel.SetScrollbars(
            1, 5, 1, int(math.ceil(panel.GetClientSize()[1]/5.0)))

    def get_value(self):
        return self.value

    def set_value(self, value):
        value = misc.wxstr(value)
        if not misc.streq(value, self.value):
            self.value = value
            if self.style & wxTE_MULTILINE:
                value = value.replace('\\n', '\n')
            if self.widget: self.widget.SetValue(value)

    def get_style(self):
        retval = [0] * len(self.style_pos)
        try:
            for i in range(len(self.style_pos)):
                if self.style & self.style_pos[i]:
                    retval[i] = 1
        except AttributeError: pass
        return retval

    def set_style(self, value):
        old = self.style & wxTE_MULTILINE
        value = self.properties['style'].prepare_value(value)
        self.style = 0
        for v in range(len(value)):
            if value[v]:
                self.style |= self.style_pos[v]
        if self.widget:
            new = self.style & wxTE_MULTILINE
            if old != new:
                focused = misc.focused_widget is self
                self.sel_marker.Destroy()
                w = self.widget
                self.create_widget()
                if not self.properties['size'].is_active():
                    self.widget.SetSize(self.widget.GetBestSize())
                self.finish_widget_creation()
                self.sizer.layout()
                
                if focused:
                    misc.focused_widget = self
                    self.sel_marker.Show(True)

# end of class EditTextCtrl


def builder(parent, sizer, pos, number=[1]):
    """\
    factory function for EditTextCtrl objects.
    """
    name = 'text_ctrl_%d' % number[0]
    while common.app_tree.has_name(name):
        number[0] += 1
        name = 'text_ctrl_%d' % number[0]
    text = EditTextCtrl(name, parent, wxNewId(), sizer, pos,
                        common.property_panel)
    node = Tree.Node(text)
    text.node = node
    text.show_widget(True)
    common.app_tree.insert(node, sizer.node, pos-1)

def xml_builder(attrs, parent, sizer, sizeritem, pos=None):
    """\
    factory function to build EditTextCtrl objects from an xml file
    """
    from xml_parse import XmlParsingError
    try: name = attrs['name']
    except KeyError: raise XmlParsingError, "'name' attribute missing"
    if sizer is None or sizeritem is None:
        raise XmlParsingError, "sizer or sizeritem object cannot be None"
    text = EditTextCtrl(name, parent, wxNewId(), sizer, pos,
                        common.property_panel)
    sizer.set_item(text.pos, option=sizeritem.option, flag=sizeritem.flag,
                   border=sizeritem.border)
    node = Tree.Node(text)
    text.node = node
    if pos is None: common.app_tree.add(node, sizer.node)
    else: common.app_tree.insert(node, sizer.node, pos-1)
    return text


def initialize():
    """\
    initialization function for the module: returns a wxBitmapButton to be
    added to the main palette.
    """
    common.widgets['EditTextCtrl'] = builder
    common.widgets_from_xml['EditTextCtrl'] = xml_builder
        
    return common.make_object_button('EditTextCtrl', 'icons/text_ctrl.xpm')