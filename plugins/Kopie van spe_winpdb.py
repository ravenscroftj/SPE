import os
import wx
import _spe.info as info
import _spe.plugins.winpdb.rpdb2 as rpdb2

class SessionManager(rpdb2.CSimpleSessionManager):
    def __init__(self,runner):
        self.runner     = runner
        self.app        = runner.app
        self.debugger   = False
        self.encrypted  = runner.app.fCrypto
        self.exception  = False
        rpdb2.CSimpleSessionManager.__init__(self,fAllowUnencrypted = not self.encrypted)
        
    def unhandled_exception_callback(self):
##        if self.debugger:
##            return
##        if self.exception:
##            self.runner.stop()
##            return
##        self.exception      = True
        
        child               = self.app.childActive
        child.setStatus('Unhandled exception at "%s"'%self.runner.commandline)
        dlg                 = wx.MessageDialog(self.app.parentFrame,
                                'An unhandled exception occurred.\nDo you want to analyze the exception with WinPdb?\n\n(Type "analyze" in WinPdb command prompt.)',
                                'SPE - %s'%self.runner.commandline,
                                wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION
                               )
        if dlg.ShowModal() == wx.ID_YES:
            dlg.Destroy()
            self.runner.debug()
        else:
            dlg.Destroy()
            self.runner.stop()
        
    def script_about_to_terminate_callback(self):
        #todo: implement checkbox in dialog box to launch winpdb at the end
        child               = self.app.childActive
        child.setStatus('Terminating "%s"'%self.runner.commandline)
        self.runner.stop()

    def script_terminated_callback(self):
        child               = self.app.childActive
        child.setStatus('Terminating "%s"'%self.runner.commandline)
        self.runner.stop()
                
class Runner:
    def __init__(self,app):
        self.app        = app
        #initialize
        self.arguments  = ''
        self.running    = None
        self.title      = 'SPE - Run file'
        if app.fCrypto:
            self.title  += ' (encrypted)'
        #winpdb path
        from _spe.plugins.winpdb import __file__ as fileName
        self.winpdb     = os.path.join(os.path.dirname(fileName),'winpdb.py')
        if info.WIN and ' ' in self.winpdb:
            self.winpdb = '"%s"'%self.winpdb
        #dialog
        from dialogs.winpdbDialog import dialog
        self.dialog     = dialog
        
    def switch(self):
        "Run/stop file"
        #todo: update toolbar
        child           = self.app.childActive
        if self.running:
            self.stop()
        else:
            if child.confirmSave():
                self.run(child)
            
    def run(self,child):
        fileName        = child.fileName
        dlg             = wx.TextEntryDialog(self.app.parentFrame, 
                            'Arguments for "%s"'%fileName,
                            self.title, 
                            self.arguments)
        if dlg.ShowModal() == wx.ID_CANCEL:
            dlg.Destroy()
            child.setStatus('Running "%s" was cancelled.'%(fileName,))
            return
        self.arguments          = dlg.GetValue()
        dlg.Destroy()
        self.commandline        = fileName
        if self.arguments:
            self.commandline    += ' ' + self.arguments
        child.statusBar.throbber.run()
        child.setStatus('Launching "%s", please wait...'%self.commandline)
        try:
            self.running    = SessionManager(self)
            self.running.launch(True, self.commandline)
            message     = ''
        except Exception,message:
            message     = ' (%s)'%message
        child.setStatus('Running "%s"%s'%(self.commandline,message))
        
    def stop(self):
        #stop running instance
        try:
            self.running.stop_debuggee()
        except:
            pass
        self.running = None
        #update status
        child               = self.app.childActive
        child.setStatus('Terminated "%s"'%self.commandline)
        child.statusBar.throbber.stop()
        
    def debug(self):
        child           = self.app.childActive
        if self.running:
            #todo: encrypted
            self.running.debugger = True
            (rid, pwd)  = self.running.prepare_attach()
            args        = [os.P_NOWAIT,
                           info.PYTHON_EXEC,
                           info.PYTHON_EXEC,
                           self.winpdb]
            if not self.running.encrypted:
                args.append('-t')
            if info.WIN:
                args.extend(['-p',pwd])
            args.extend(['-a',rid])
            os.spawnl(*args)
            child.setStatus('WinPdb Debugger is attached to "%s".'%self.commandline,1)
##        elif child.confirmSave():
##            name            = child.fileName
##            debugDialog     = self.dialog(self.app.parentFrame,name)
##            if debugDialog.ShowModal() == wx.ID_CANCEL:
##                debugDialog.Destroy()
##                child.setStatus('WinPdb Debugger was cancelled.',1)
##            else:
##                debugDialog.Destroy()
##                _info       = self.app.debugInfo
##                args        = [os.P_NOWAIT,
##                               info.PYTHON_EXEC,
##                               info.PYTHON_EXEC]
##                args.extend(_info['parameters'])
##                if os.path.exists(name):
##                    if info.WIN and ' ' in name:
##                        name    = '"%s"'%name
##                    args.append(name)
##                    script_args = _info['arguments']
##                    if script_args:
##                        args.append(script_args)
##                os.spawnl(*args)
##                child.setStatus('WinPdb Debugger is succesfully started.',1)
            
        
