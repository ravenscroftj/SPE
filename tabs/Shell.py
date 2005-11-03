####(c)www.stani.be-------------------------------------------------------------
import _spe.info
INFO=_spe.info.copy()

INFO['description']=\
"""Session as tab.

pyChecker support by Nicodemus"""

__doc__=INFO['doc']%INFO

####Panel class-----------------------------------------------------------------

import wx, re, os
import _spe.help

class Shell(wx.py.shell.Shell):
    def __init__(self,**keyw):
        wx.py.shell.Shell.__init__(self,**keyw)
        self.SetUseAntiAliasing(True)
        wx.EVT_LEFT_DCLICK(self,self.jumpToSource) 
        
    def jumpToSource(self,event=None):
        line=self.GetCurrentLine()
        text=None
        while not text and line>0:
            text=self.GetLine(line)
            if text.find('File')!=-1 and text.find('line')!=-1:
                text='{%s}'%text.split('in ')[0].strip().replace('File ','"file":r').replace('line','"line":')
                try:
                    text=eval(text)
                except:
                    text=None
            else: text=None
            line-=1
            
        #pyChecker support by Nicodemus
        if not text:
            # check if the line in the form filename:line: message
            current_line = self.GetLine(self.GetCurrentLine())
            m = re.match('(.*):(\d+): .*', current_line)
            if m:
                text = {}
                text['file'] = m.group(1)
                text['line'] = int(m.group(2))+1
            else:
                text = None
            
        if text:
            text['line']-=1
            self.open(r'%s'%text['file'],text['line'])
            self.setStatusText('Jumped to file "%s" (line %s)'%(text['file'],text['line']))
        else:
            self.setStatusText('Error: Impossible to locate file and line number.')
        
    def OnKeyDown(self, event):
        """Overwriting Key down event handler to allow cut,copy,paste with alt."""

        # If the auto-complete window is up let it do its thing.
        if self.AutoCompActive():
            event.Skip()
            return
        key = event.KeyCode()
        control = event.ControlDown()
        alt = event.AltDown()
        shift = event.ShiftDown()
        if key==wx.WXK_SPACE and control:
            self.jumpToSource(event)
        elif (alt and key in (ord('C'), ord('c'))):
            self.Copy()
        elif (alt and key in (ord('V'), ord('v'))):
            self.Paste()
        else:wx.py.shell.Shell.OnKeyDown(self,event)

class DropRun(wx.FileDropTarget):
    """Runs a file when dropped on shell."""
    def __init__(self,run):
        wx.FileDropTarget.__init__(self)
        self.run=run
    def OnDropFiles(self,x,y,fileNames):
        fileNames=[script for script in fileNames 
            if os.path.splitext(script)[-1].lower() in ['.py','.pyw']]
        if fileNames:
            for fileName in fileNames:
                self.run(fileName)
            return 1
        else:return 0

class Panel(Shell):
    def __init__(self,panel,*args,**kwds):
        Shell.__init__(self,parent=panel, introText=\
"""Portions Copyright 2003-2005 www.stani.be - see credits in manual for further copyright information.
Please donate if you find this program useful (see help menu). Double click to jump to error source code.""")
        self.setStatusText=panel.SetActiveStatusText
        self.open=panel.openList
        self.interp.push('namespace={}')
        self.SetDropTarget(DropRun(panel.runFile))
        self.SetHelpText(_spe.help.SHELL)
        
