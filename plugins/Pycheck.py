"""File ImportChecks of pychecker2 is modified."""
import os
import wx
from wx.lib.evtmgr import eventManager

COLOR           = (wx.Colour(220,220,220),wx.Colour(255,255,255))
IGNORE          = ['Warnings...']
METHOD_NAMES    = ['byte code','compiler package']
METHOD_PATHS    = ['%s" --stdlib --blacklist --varlist'%os.path.join('pychecker','checker.py'),
    '%s" --incremental'%os.path.join('pychecker2','main.py')]

#----------------------------------------------------------------------

class Panel(wx.ListCtrl):
    def __init__(self, notebook, page=5, *args, **kwds):
        wx.ListCtrl.__init__(self, notebook, -1,style=wx.LC_REPORT)
        self.notebook   = notebook
        self.page       = page
        self.panel      = notebook.GetParent()
        self.process    = None

        self.list   = [('','')]
        self.fileIndex   = 0
        self.lastFile    = 0
        self.methodIndex    = 1

        self.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, 
                heading='Line',width=40)
        self.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, 
                heading='Remark',width=600)
        self.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, 
                heading='File',width=400)

        self.InsertStringItem(0,'')
        self.SetStringItem(0,1,'Press Ctrl+Alt+C to check the current file [%s method]'%(METHOD_NAMES[self.methodIndex],))

        #events (eventManager doesn't work here ;-()
        wx.EVT_LIST_ITEM_SELECTED(self,-1,self.onSelect)
        # We can either derive from wx.Process and override OnTerminate
        # or we can let wx.Process send this window an event that is
        # caught in the normal way...
        wx.EVT_END_PROCESS(self,-1,self.OnProcessEnded)

    def __del__(self):
        if self.process is not None:
            self.process.Detach()
            self.process.CloseOutput()
            self.process = None

    def check(self):
        if not self.process:
            if self.panel.confirmSave('File must be saved to be analyzed by Pychecker.') :
                self.DeleteAllItems()
                self.focus()
                eventManager.Register(self.OnIdle, wx.EVT_IDLE, self)
                import pychecker
                self.index          = 1
                self.methodIndex    = 1
                self.started        = 1
                fileName            = self.panel.fileName
                cmd                 = 'python -u "%s "%s"'%\
                    (os.path.join(self.panel.parentPanel.pathPlugins,
                    METHOD_PATHS[self.methodIndex]),fileName)
                print cmd
                self.process = wx.Process(self)
                self.process.Redirect()
                pid = wx.Execute(cmd, wx.EXEC_ASYNC, self.process)
                self.InsertStringItem(0,'')
                self.SetStringItem(0,1,'%s checking...'%METHOD_NAMES[self.methodIndex])
                self.SetItemBackgroundColour(0,wx.Colour(255,200,200))
        else:
            self.panel.parentPanel.message('Sorry, only one pycheck at a time.')

    def OnCloseStream(self, evt):
        self.process.CloseOutput()

    def OnIdle(self, evt):
        if self.process is not None:
            stream = self.process.GetInputStream()
 
            if stream.CanRead():
                text = stream.read()
                self.add(text)


    def OnProcessEnded(self, evt):
        self.DeleteItem(0)
        del self.list[0]
        eventManager.DeregisterListener(self.OnIdle)
        self.focus()
        wx.Bell()
        stream = self.process.GetInputStream()
        if stream.CanRead():
            text = stream.read()
            self.add(text)
        self.process.Destroy()
        self.process = None
            
    def add(self,text):
        self.focus()
        if self.started: 
            #self.DeleteAllItems(0)
            self.started = 0
        text        = text.replace('\r','').split('\n')
        for data in text:
            data    = data.strip()
            if data and data not in IGNORE:
                if self.methodIndex == 0:
                    i=1
                    columns = data[2:].split(':')
                    if len(columns)==3:
                        file, line, remark  = columns
                        file                = data[:2]+file
                    else:
                        file                = ''
                        line                = ''
                        remark              = columns[0]
                else:
                    f = data.find(':',2)
                    file = data[:f]
                    l = data.find(' ',f)
                    line = data[f+1:l]
                    remark  = data[l+1:]
                self.InsertStringItem(self.index,line)
                self.SetStringItem(self.index,1,remark)
                self.SetStringItem(self.index,2,file)
                self.list.insert(self.index,(file,line))
                if file != self.lastFile:
                    self.lastFile    = file
                    self.fileIndex   += 1
                #self.SetItemBackgroundColour(self.index,COLOR[self.fileIndex%2])

                self.index+=1
            

    def onSelect(self,event):
        file,line=self.list[event.GetIndex()]
        if file and line:
            self.panel.parentPanel.openList(file,int(line)-1)

    def focus(self):
        self.notebook.SetSelection(self.page)