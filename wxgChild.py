#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.4cvs on Fri Jul 22 01:44:22 2005

import wx

class Panel(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Panel.__init__
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.split = wx.SplitterWindow(self, -1, style=wx.SP_3D|wx.SP_BORDER)
        self.main = wx.Notebook(self.split, -1, style=0)
        self.notebook = wx.Notebook(self.split, -1, style=0)
        self.explore = Tree(self.notebook, -1)
        self.browser = Browser(self.notebook, -1)
        self.todo = wx.ListCtrl(self.notebook, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.index = wx.ListCtrl(self.notebook, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.notes = wx.TextCtrl(self.notebook, -1, "")
        self.pychecker = Pycheck.Panel(self.notebook, -1)
        self.sash = PythonSTC(self.main, -1)
        self.uml = sm.uml.wxCanvas(self.main, -1)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Panel.__set_properties
        pass
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Panel.__do_layout
        splitSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.notebook.AddPage(self.explore, _("Explore"))
        self.notebook.AddPage(self.browser, _("Browser"))
        self.notebook.AddPage(self.todo, _("Todo"))
        self.notebook.AddPage(self.index, _("Index"))
        self.notebook.AddPage(self.notes, _("Notes"))
        self.notebook.AddPage(self.pychecker, _("Check"))
        self.main.AddPage(self.sash, _("Source"))
        self.main.AddPage(self.uml, _("Uml"))
        self.split.SplitVertically(self.notebook, self.main)
        splitSizer.Add(self.split, 1, wx.EXPAND, 0)
        self.SetAutoLayout(True)
        self.SetSizer(splitSizer)
        splitSizer.Fit(self)
        splitSizer.SetSizeHints(self)
        # end wxGlade

# end of class Panel

