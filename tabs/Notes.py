####(c)www.stani.be-------------------------------------------------------------

import _spe.info
INFO=_spe.info.copy()

INFO['description']=\
"""Notes as tab."""

__doc__=INFO['doc']%INFO

####Panel class-----------------------------------------------------------------

import wx
import _spe.help

class Panel(wx.TextCtrl):
    def __init__(self,panel,*args,**kwds):
        wx.TextCtrl.__init__(self,parent=panel,id=-1,style=wx.TE_MULTILINE|wx.TE_DONTWRAP)
        self.SetHelpText(_spe.help.NOTES)
