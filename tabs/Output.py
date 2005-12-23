"""Panel to execute scripts and redirect their output for SPE"""

import os, re
import wx
import wx.stc as wx_stc
import  wx.html as  html

import _spe.info as info

FIND_ICON   = os.path.join(info.INFO['skinLocation'],'lookup.png').replace('\\','\\\\')
RE_LINK     = re.compile('(\s*)(File "(.*))\n')
RE_LOCATION = re.compile('File "([^"]*)", line (\d+)')

class Output(html.HtmlWindow):
    pid         = -1
    
    def __init__(self,*args,**keyw):
        html.HtmlWindow.__init__(self,*args,**keyw)
    
    #---execute
    def Execute(self, command, statustext = "Running script..."):
        """Executes a command of which the output will be redirected by OnIdle and OnEndProcess."""
        if self.pid is -1:
            #give feedback
            self.AddText('<table bgcolor=#CCCCCC width=100%%><tr><td><TT>&gt;&gt;&gt; %s</TT></td></tr></table>\n'%command)
            self.SetStatusText(statustext)
            self.UpdateToolbar()
            self.Raise()
            #bind events
            self.Bind(wx.EVT_IDLE,self.OnIdle)
            self.Bind(wx.EVT_END_PROCESS,self.OnEndProcess)
            #create process
            self.process        = wx.Process(self)
            self.process.Redirect()
            if info.WIN:
                self.pid        = wx.Execute(command, wx.EXEC_ASYNC | wx.EXEC_NOHIDE, self.process)
            else:
                self.pid        = wx.Execute(command, wx.EXEC_ASYNC, self.process)
            self.inputstream    = self.process.GetInputStream()        
            self.errorstream    = self.process.GetErrorStream()
            self.outputstream   = self.process.GetOutputStream()          
            
    def IsBusy(self):
        """Is the instance busy executing a command."""
        return not (self.pid is -1)
            
    #---user feedback
    def AddText(self,text,error=False):
        """Add text and in case of error, colour red and provide links."""
        text        = text.replace('\r\n','\n').replace("<string>","&lt;string&gt;")
        if error:
            text    = RE_LINK.sub(r"\g<1><img src='%s'>&nbsp;<a href='\g<2>'>\g<2></a><br>"%FIND_ICON,text)
            text    = '<font color=red>%s</font>'%text
        self.AppendToPage(text.replace('\n','<br>'))
        self.Scroll(0,self.GetVirtualSize()[1]/self.GetScrollPixelsPerUnit()[1])

    def SetStatusText(self,text):
        print text
        
    def UpdateToolbar(self):
        #print 'Updating toolbar...'
        pass

    #---event handlers
    def OnIdle(self, event):
        if (self.process is not None):
            if self.inputstream.CanRead():
                text = self.inputstream.read()
                self.AddText(text)
            if self.errorstream.CanRead():
                text = self.errorstream.read()
                self.AddText(text,error=True)

    def OnEndProcess(self, event):
        #unbind events
        self.Unbind(wx.EVT_IDLE)
        self.Unbind(wx.EVT_END_PROCESS)
        #check for any leftover output.
        self.OnIdle(event)
        #destroy process
        self.process.Destroy()
        self.process    = None
        self.pid        = -1
        #give feedback
        self.UpdateToolbar()
        self.SetStatusText("Terminated script.")
        
    def OnLinkClicked(self,linkInfo):
        match   = RE_LOCATION.match(linkInfo.GetHref())
        try:
            fileName    = match.group(1)
            lineno      = int(match.group(2))
            self.OpenFile(fileName,lineno)
            self.SetStatusText('Jumped to file "%s" (line %s).'%(fileName,lineno))
        except Exception, message:
            self.SetStatusText('SPE could not locate source file. (%s)'%message)

    def OpenFile(self,fileName,lineno):
        print fileName,lineno
        
class Panel(Output):
    def __init__(self,panel,*args,**keyw):
        Output.__init__(self,parent=panel,id=-1,*args,**keyw)
        self.app            = panel.app
        self.OpenFile       = panel.openList
        self.SetStatusText  = panel.SetActiveStatusText
        
    def Raise(self):
        self.GetParent().SetSelection(3)#todo: 3 should be determined dynamic

        
class TestFrame(wx.Frame):
    
    def __init__(self,parent=None,id=-1,*args,**keyw):
        wx.Frame.__init__(self,parent=parent,id=id,*args,**keyw)
        self.output = Output(parent=self,id=-1)
        self.Show()
        
    def test(self):
        import time
        for i in range (1):
            self.output.Execute('python -c "%s/0"'%i)
##            while self.output.IsBusy():
##                print self.output.pid
##                time.sleep(1)
        
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = TestFrame()
    app.SetTopWindow(frame)
    wx.CallAfter(frame.test)
    app.MainLoop()
