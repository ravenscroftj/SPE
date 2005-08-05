####(c)www.stani.be                                                                
import _spe.info as info
INFO=info.copy()

INFO['description']=\
"""Subclassed smdi Parent frame."""

__doc__=INFO['doc']%INFO

####Importing modules-----------------------------------------------------------

#---general modules
import ConfigParser,os,string,sys,time,types,webbrowser, pprint
import _spe,sm.scriptutils,sm.wxp

#---wxPython
import wx
import wx.stc
from wx.lib.evtmgr import eventManager

BLENDER_MESSAGE = 'Spe must be launched within Blender for this feature.'
PYTHON_EXEC     = (r'%s'%sys.executable).replace('Program Files','progra~1')

import Child

####Constants-------------------------------------------------------------------
DEFAULT         = "<default>"
FOLDERS         = 'folders.txt'
HELP_SORRY      = "Sorry, '%s' was not found on your system, getting it from internet instead."
HELP_WWW        = 'http://www.python.org/doc/current/%s/%s.html'
MAIL            = 'mailto:s_t_a_n_i@yahoo.com?subject=About spe...'
NOTES           = 'notes.txt'
PATH            = os.path.dirname(__file__)
PLATFORM        = sys.platform
PREFIX          = sys.prefix
RECENT          = 'recent.txt'
REMEMBER        = 'remember.txt'
SIZE            = (600,400)
SKIN            = 'default'
TABS            = ['Shell','Locals','Session','Find','Browser','Recent','Todo','Index','Notes','Donate']
TITLE           = 'SPE %s'
UNNAMED         = 'unnamed'

####Subclassed Parent class-----------------------------------------------------
class Panel(wx.Notebook):
    ####Constructors
    def __init__(self, parent, openFiles=[], splash=None, redirect=1, path=PATH,
                 size = SIZE,**settings):
        wx.Notebook.__init__(self,parent=parent,id=wx.ID_ANY,style=wx.NB_BOTTOM,size=size)
        self.__paths__(path)
        self.__settings__(openFiles,redirect,**settings)
        self.__findReplaceEvents__()
        
    def __paths__(self,path,skin='default'):
        self.path           = path
        self.pathDoc        = os.path.join(self.path,       'doc')
        self.pathSkins      = os.path.join(self.path,       'skins')
        self.pathImages     = os.path.join(self.pathSkins,  skin)
        self.pathPlugins    = os.path.join(self.path,       'plugins')
        self.pathTabs       = os.path.join(self.path,       'tabs')
        sys.path.append(self.pathPlugins)
        try:
            os.mkdir(INFO['userPath'])
        except:
            if not os.path.exists(INFO['userPath']):
                print 'Warning: could not find or create user path (%s).'%INFO['userPath']
            
    def __settings__(self,openFiles,redirect,redraw=None,Blender=None,**kwds):
        self.idleTime       = time.time()
        #arguments
        self._openFiles = openFiles
        self._redirect  = redirect
        self.redraw         = redraw
        self.Blender        = Blender
        #panel
        self.defaultEncoding= None
        self.findDialog     = None
        self.folders        = []
        self.kiki           = None
        self.remember       = 0
        self.restartMessage = ''
        if PLATFORM == 'win32':
            self.LIST_STYLE = wx.LC_SMALL_ICON# todo: verify this better |wx.LC_LIST 
        else:
            self.LIST_STYLE = wx.LC_LIST
            
    def __findReplaceEvents__(self):
        self.findStr=''
        self.replaceStr=''
        self.findFlags=1
        self.stcFindFlags=0
        #This can't be done with the eventManager unfortunately ;-(
        wx.EVT_COMMAND_FIND(self,-1,self.onFind)
        wx.EVT_COMMAND_FIND_NEXT(self, -1,self.onFind)
        wx.EVT_COMMAND_FIND_REPLACE(self, -1,self.onReplace)
        wx.EVT_COMMAND_FIND_REPLACE_ALL(self, -1,self.onReplaceAll)
        wx.EVT_COMMAND_FIND_CLOSE(self, -1,self.onFindClose)
    
    #---finish
    def __finish__(self):
        self.__icons__()
        self.__sash__()
        self.__frame__()
        #self.app.childActive.source.SetFocus()
        
    def __icons__(self):
        self.iconsList=wx.ImageList(16,16)
        self.icons={}
        self.iconsListIndex={}
        iconFiles=sm.osx.listdir(self.pathImages,extensions=['.png'])
        iconFiles.sort()
        for icon in iconFiles:
            self.icons[icon]=self.app.bitmap(icon)
            if self.icons[icon].GetHeight() == 16:
                self.iconsListIndex[icon]=self.iconsList.Add(self.icons[icon])
                
    def __sash__(self):
        if self.app.DEBUG: print 'Creating tabs...'
        self.config = self.app.config 
        self.AssignImageList(self.iconsList)
        tabs = [os.path.splitext(x)[0] for x in sm.osx.listdir(self.pathTabs,extensions=['.py']) if x[:1]!='_'] 
        tabs.sort()
        tabs = TABS[:-1] + [x for x in tabs if x not in TABS] + [TABS[-1]]
        if not self.app.Blender:
            tabs.remove('Blender')
        for tab in tabs:
            if self.app.DEBUG: print '\t',tab
            __import__('_spe.tabs.'+tab)
            page = self.__dict__[tab.lower()] = eval('_spe.tabs.%s.Panel'%tab)(self)
            if info.DARWIN and tab!='Shell':    text    = ''
            else:                               text    = tab
            self.AddPage(page=page,text=text,imageId=self.iconsListIndex[tab.lower()+'.png'])
        self.tabs = tabs
        if self.get('version')!=INFO['version']:
            self.SetSelection(self.GetPageCount()-1)
            self.set('version',INFO['version'])
        eventManager.Register(self.onTab,wx.EVT_NOTEBOOK_PAGE_CHANGED,self)

    def __frame__(self):
        #parent frame
        frame   = self.frame
        frame.SetDropTarget(Child.DropOpen(self.openList))
        icon    = wx.Icon(os.path.join(self.pathImages,'favicon.ico'),wx.BITMAP_TYPE_ICO)
        frame.SetIcon(icon)
        if hasattr(frame,'panelFrame'):
            frame.panelFrame.SetIcon(icon)
        #constructors
        self.preferencesSave()
        self.__remember__(openFiles=self._openFiles)
        self.__menus__()

                
    def __menus__(self):
        #parentInit.importMenus
        menuBar = self.frame.menuBar
        if self.app.mdi:
            #d#self.frame.menuBar.parentPanel = self
            menuBar.check_sidebar()
            menuBar.check_view()
        if not self.app.children:
            menuBar.enable(0)
        
    def __remember__(self,openFiles=[]):
        global RECENT,FOLDERS,NOTES,REMEMBER

        self.recent.files=[]
        try:
            files=eval(self.userOpen(RECENT))
            self.recent.add([file for file in files if file and os.path.exists(file)])
        except:
            pass
        
        try:
            folders=eval(self.userOpen(FOLDERS))
            self.browser.depth.SetValue(folders[0])
            self.browser.add([file for file in folders[1:] if file])
        except:
            pass
            
        try:
            notes=self.userOpen(NOTES)
            self.notes.SetValue(notes)
        except:
            pass
            
        fileList=[]
        try:
            files=eval(self.userOpen(REMEMBER))
            fileList=[file for file in files if file]
        except:
            pass
        fileList.extend([os.path.abspath(f) for f in openFiles])
        if fileList:
            self.rememberSet(1)
            self.openList(fileList,
                message     = 0,
                select      = None, 
                maximize    = self.getValue("MaxChildren"))
        else:
            self.rememberSet(0)
            self.new(maximize = self.getValue("MaxChildren"))
    
    ####Menu
    #---File
    def new(self,name=UNNAMED,source='',maximize=None):
        """Create a new empty script window.?"""
        app = self.app
        child = app.ChildFrame(self.frame,
            page        = os.path.basename(name),
            extra       = name,
            fileName    = name,
            source      = source,
            size        = app.size,
            maximize    = maximize)
        self.frame.menuBar.enable(1)
        return child.panel
        
    def open(self, event=None):
        """Open file(s) dialog."""
        try:
            defaultDir=os.path.dirname(self.app.childActive.fileName)
        except:
            defaultDir=''
        dlg = wx.FileDialog(self, "Choose a file - www.stani.be", 
            defaultDir=defaultDir, defaultFile="", 
            wildcard=info.WILDCARD, 
            style=wx.OPEN|wx.MULTIPLE)
        if dlg.ShowModal() == wx.ID_OK:
            fileList = dlg.GetPaths()
            if fileList:
                child           = self.app.childActive
                if child and child.fileName==Child.NEWFILE and not child.changed:
                    child.frame.onFrameClose()
            self.openList(fileList)
        dlg.Destroy()
        
    #---Edit
    def browse_source(self, event=None):
        """Locate source file of word and open it."""
        fileName=self.app.childActive.source.getWordFileName(whole=1)
        if fileName and fileName[0]!='"': 
            self.openList(fileName)
        else:
            if not fileName: fileName=''
            self.SetActiveStatusText('Sorry, can not locate file %s'%fileName)

    def find_replace(self, event=None):
        """Find and Replace dialog and action."""
        #dialog already open, if yes give focus
        if self.findDialog:
            self.findDialog.SetFocus()
            return
        #find string
        findStr = self.app.childActive.source.GetSelectedText()
        if not findStr:
                findStr = self.findStr
        self.numberMessages=0
        #find data
        data    = wx.FindReplaceData(self.findFlags)
        data.SetFindString(findStr)
        data.SetReplaceString(self.replaceStr)
        #dialog
        self.findDialog = wx.FindReplaceDialog(self, data, "Find & Replace", 
                wx.FR_REPLACEDIALOG|wx.FR_NOUPDOWN)
        self.findDialog.Show(1)    
        self.findDialog.data = data  # save a reference to it...
           
    def preferences(self):
        """Show preferences dialog box."""
        from dialogs import preferencesDialog
        prefs=preferencesDialog.Create(self,-1,'')
        prefs.ShowModal()
        
    #---View
    def whitespace(self,event):
        """Toggle visibility white space."""
        for child in self.app.children:
            child.source.SetViewWhiteSpace(event.IsChecked())
        self.set('ViewWhiteSpace',event.IsChecked())

    def indentation_guides(self,event):
        """Toggle visibility indentation guides."""
        for child in self.app.children:
            child.source.SetIndentationGuides(event.IsChecked())
        self.set('IndentationGuides',event.IsChecked())
        
    def right_edge_indicator(self,event):
        """Toggle visibility right edge indicator."""
        for child in self.app.children:
            child.source.SetViewEdge(event.IsChecked())
        self.set('ViewEdge',event.IsChecked())
        
    def end_of_line_marker(self,event):
        """Toggle visibility end of line marker."""
        for child in self.app.children:
            child.source.SetViewEOL(event.IsChecked())
        self.set('ViewEol',event.IsChecked())
        
    def toggle_shell(self):
        """Show/hide shell"""
        frame               = self.frame
        if hasattr(frame,'sash'):
            height          = frame.sash.GetSize()[1]
            if height<10:
                hidden      = 1
            else:
                hidden      = 0
        elif hasattr(frame,'panelFrame'):
            hidden          = not frame.panelFrame.IsShown()
        else: return
        self.showShell(hidden,save=True)
        return hidden
        
    def showShell(self,show,save=False):
        if save: self.set('ShowShell',show)
        frame = self.frame
        if hasattr(frame,'sash'):
            if show:
                frame.sash.SetDefaultSize(wx.Size(1000,200))
            else:
                frame.sash.SetDefaultSize(wx.Size(1000,1))
            wx.LayoutAlgorithm().LayoutMDIFrame(frame)
        elif hasattr(frame,'panelFrame'):
            frame.panelFrame.Show(show)
            frame.panelFrame.Activate()

    #---Tools
    def browse_folder(self):
        """Browse folder"""
        fileName=self.app.childActive.fileName
        if fileName[0]=='/': fileName = 'file://'+fileName
        webbrowser.open(os.path.dirname(fileName))
        
    def run(self):
        """Run file"""
        child           = self.app.childActive
        if not self.getValue('SaveBeforeRun') or child.confirmSave():
            fileName    = child.fileName
            self.runFile(fileName,repr(self.getText()),separate=0)
        
    def run_with_profile(self):
        """Run file with profile"""
        child           = self.app.childActive
        if not self.getValue('SaveBeforeRun') or child.confirmSave():
            fileName    = child.fileName
            self.runFile(fileName,repr(self.getText()),separate=0,profiling=1)

    def run_in_separate_namespace(self):
        """Run in separate namespace"""
        child           = self.app.childActive
        if not self.getValue('SaveBeforeRun') or child.confirmSave():
            fileName    = child.fileName
            self.runFile(fileName,repr(self.getText()),separate=1)
        
    def run_verbose(self):
        """Run verbose"""
        child           = self.app.childActive
        if not self.getValue('SaveBeforeRun') or child.confirmSave():
            self.busyShow()
            for command in self.getText().split('\n'):
                self.shell.run(command,prompt=0)
            if self.redraw:self.redraw()
            self.shell.prompt()
            self.activateShell()
            self.busyHide()
        
    def import_(self):
        """Import"""
        child           = self.app.childActive
        if not self.getValue('SaveBeforeRun') or child.confirmSave():
            self.busyShow()
            name=child.fileName
            self.shell.write("Importing '%s' ..."%name)
            self.shell.waiting = 1
            self.shell.interp.push('import sm.scriptutils')
            self.shell.interp.push('sm.scriptutils.importMod(r"%s",mainDict=locals())'\
                    %name)
            self.shell.waiting = 0
            self.shell.prompt()
            if self.redraw:self.redraw()
            self.activateShell()
            self.busyHide()

    def debug(self):
        child   = self.app.childActive
        if child.confirmSave():
            from plugins.winpdb import __file__ as fileName
            path    = os.path.dirname(fileName)
            args    = [os.P_NOWAIT,
                       PYTHON_EXEC,
                       PYTHON_EXEC,
                       os.path.join(path,'_winpdb.py'),
                       '-t']
            name    = child.fileName
            if name != UNNAMED: args.append(name)
            os.spawnl(*args)
            self.SetStatusText('winpdb debugger is succesfully started.',1)

    def browse_object_with_pyfilling(self):
        """Browse object with pyfilling"""
        from wx.py.filling import FillingFrame
        name=self.messageEntry('Enter object:')
        try:
            object=self.shell.interp.locals[name]
        except:
            self.SetActiveStatusText('%s is not defined'%name,1)
            return
        filling=FillingFrame(parent=self, id=-1, title='PyFilling', 
                 pos=wx.DefaultPosition, size=wx.Size(600,300), 
                 style=wx.DEFAULT_FRAME_STYLE, rootObject=object, 
                 rootLabel=str(object), rootIsNamespace=0, static=0)
        filling.Show(1)
        
    def test_regular_expression_with_kiki(self):
        """Test regular expression with Kiki..."""
        if wx.Platform == "__WXMAC__":
            os.system('open -a /Applications/SPE-OSX/KikiOSX.app')
        else:
            try:
                self.kiki.Raise()
            except:
                from plugins.kiki import kiki
                INFO['kikiPath']=os.path.dirname(kiki.__file__)
                self.kiki=kiki.speCreate(self,info=INFO)
        self.SetStatusText('Kiki is succesfully started.',1)

    def design_a_gui_with_wxglade(self):
        if wx.Platform == "__WXMAC__":
            os.system('open -a /Applications/SPE-OSX/wxGladeOSX.app')
        else:
            from plugins.wxGlade import __file__ as fileName
            path    = os.path.dirname(fileName)
            os.spawnl(os.P_NOWAIT,PYTHON_EXEC,PYTHON_EXEC,os.path.join(path,'wxglade.py'))
            self.SetStatusText('wxGlade is succesfully started.',1)

    def design_a_gui_with_xrc(self):
        if wx.Platform == "__WXMAC__":
            os.system('open -a /Applications/SPE-OSX/XRCed.app')
        else:
            from wx.tools.XRCed.xrced import __file__ as fileName
            os.spawnl(os.P_NOWAIT,PYTHON_EXEC,PYTHON_EXEC,fileName)
            self.SetStatusText('XRC editor is succesfully started.',1)

    #---Links
    def contact_author(self):
        WebBrowser=self.get('WebBrowser')
        if WebBrowser==DEFAULT:
            webbrowser.open(MAIL)
        else:
            os.system("%s '%s'"%(WebBrowser,MAIL))

    #---Help
    def keyboard_shortcuts(self):
        from dialogs import helpShortcutsDialog
        helpShortcutsDialog.create(self,path=self.path).Show(1)

    def python_help(self,what):
        pythonDocs  = self.get('PythonDocs')
        wwwHelp     = HELP_WWW%(what,what)
        if pythonDocs==DEFAULT:
            if sys.platform=='win32':
                helpActivePython=os.path.join(PREFIX,"Doc","ActivePython.chm")
                helpEntoughtPython=os.path.join(PREFIX,"Enthought","Doc","enthought_python.chm")
                if os.path.exists(helpActivePython):
                    self.messageHtml(helpActivePython)
                elif os.path.exists(helpEntoughtPython):
                    self.messageHtml(helpEntoughtPython)
                else:
                    library=os.path.join(PREFIX,"Doc",what,"index.html")
                    if os.path.exists(library):
                        self.messageHtml(library)
                    else:
                        self.messageHtml(wwwHelp)
                        self.SetStatusText(HELP_SORRY%library,1)
            else:
                linux1=''.join([PREFIX, "/share/doc/python", str(sys.version_info[0]), 
                                ".", str(sys.version_info[1]), "/html/%s/index.html"%what])
                linux2=''.join([PREFIX, "/share/doc/python-docs-", 
                                str(sys.version_info[0]), ".", str(sys.version_info[1]), ".", 
                                str(sys.version_info[2]), "/html/%s/index.html"%what])
                if os.path.exists(linux1):self.messageHtml(linux1)
                elif os.path.exists(linux2):self.messageHtml(linux2)
                else: 
                    self.messageHtml(wwwHelp)
                    self.SetStatusText(HELP_SORRY%linux1,1)
        else:
            # TODO: pythondocs laten loopen over alle mogelijkheden, dit iets eleganter.
            helpActivePython=os.path.join(pythonDocs,"Doc","ActivePython.chm")
            if sys.platform=='win32' and os.path.exists(helpActivePython):
                library = helpActivePython
            else:
                library = os.path.join(pythonDocs,what,"index.html")
            if os.path.exists(library):
                self.messageHtml(library)
            else:
                self.messageHtml(wwwHelp)
                self.SetStatusText(HELP_SORRY%library,1)

    def python_documentation_server(self):
        from pydoc import __file__ as fileName
        os.spawnl(os.P_NOWAIT,sys.executable,sys.executable,fileName,'-g')
        self.messageHtml('http://localhost:7464/')

    def wxglade_manual(self):
        from plugins.wxGlade import __file__
        path=os.path.dirname(__file__)
        self.messageHtml(os.path.join(path,'docs','html','index.html'))
        
    def wxglade_tutorial(self):
        from plugins.wxGlade import __file__
        path=os.path.dirname(__file__)
        self.messageHtml(os.path.join(path,'docs','tutorial.html'))
        
    def wxwindows_documentation(self):
        WxPythonDocs=self.get('WxPythonDocs')
        if WxPythonDocs==DEFAULT:
            WxPythonDocs    = os.path.join(os.path.dirname(wx.__file__),'docs')
        WxPythonDocs2       = os.path.join(os.path.dirname(os.path.dirname(WxPythonDocs)),'docs')
        WxPythonDocs3        = 'C:\\Program Files\\wxPython2.5 Docs and Demos\\docs'
        path = None
        for dir in [WxPythonDocs,WxPythonDocs2,WxPythonDocs3]:
            for docs in ['wx.chm','wxPythonDocs.html','wxPythonManual.html']:
                if not path:
                    p = os.path.join(dir,docs)
                    if os.path.exists(p):
                        path = p
        if path:
            self.messageHtml(path)
        else:
            self.SetActiveStatusText('wxPython documentation could not be found. Check the path in the preferences dialog.')
            
    def about(self):
        from dialogs import helpDialog
        helpDialog.create(self,self.path,'about.htm', replacements=INFO)

    #---Backstage
    def openList(self,fileList,lineno=None,col=1,message=1,select='line',maximize=None):
        """Open a list of files."""
        if type(fileList)!=types.ListType:
            fileList=[fileList]
        for fileName in fileList:
            if type(fileName)==types.TupleType:
                fileName, lineno, col = fileName
            child=self.getChildByFileName(fileName)
            if child:
                #opened already
                child.Raise()
                if lineno:child.scrollTo(lineno,col,select=select)
                else:self.SetStatusText("'%s' is already open"%fileName,1)
            else:
                #not opened yet
                try:
                    source=open(fileName).read()
                except:
                    source='' # todo: make this an option
                child=self.new(name=fileName,source=source,maximize=maximize)
                self.recent.add([fileName])
                if lineno:child.scrollTo(lineno,col,select=select)
            lineno=None
            col=1
        if len(self.app.children)>0:self.frame.menuBar.enable(1)
        return child
        
    def runFile(self,fileName,source=None,separate=0,profiling=0):
        """
        separate: run in seperate namespace to avoid conflicts with the spe namespace
        """
        self.shell.write("Running '%s' ..."%fileName)
        #self.busyShow()
        self.shell.waiting = 1
        self.shell.interp.push('import sm.scriptutils')
        if separate:
            nameSpace='namespace["%s"]'%fileName
            self.shell.interp.push('%s={"__fileName__":"%s"}'%(nameSpace,fileName))
        else:
            nameSpace='locals()'
        try:
            runCommand='sm.scriptutils.run(fileName=r"%s",source=%s,mainDict=%s,profiling=%s)'\
                %(fileName,source,nameSpace,profiling)
            self.shell.interp.push(runCommand)
        except Exception,message:
            print '\n(Spe internal warning: %s!)'%message
        self.shell.prompt()
        if self.redraw:self.redraw()
        #raise
        self.activateShell()
        #self.busyHide()
        
    def activateShell(self):
        if self.app.mdi:
            self.showShell(True,save=True)
        else:
            self.frame.Raise()
        self.SetSelection(0)

    ####Events
    #---smdi events
    def onActivate(self,event):
        """Check and update, if files are changed when parent frame is activated."""
        if self.app.DEBUG: 
            print 'Event:  Parent: %s.onActivate'%self.__class__
        try:
            reloaded=[]
            for child in self.app.children:
                if child.checkTime():
                    reloaded.append(os.path.basename(child.fileName))
            if reloaded: self.SetStatusText('Reloaded %s'%','.join(reloaded),1)
            if event: event.Skip()
        except Exception,m:
            if self.app.DEBUG: 
                print 'Warning: Parent: %s.onActivate failed\n%s\n%s\n'%(self.__class__,Exception,m)

    def onClose(self,event=None):
        """Called when the parent frame is closed."""
        if self.app.DEBUG: 
            print 'Event:  Parent: %s.onClose'%self.__class__
        for child in self.app.children:
            if not child.confirmSave():
                child.Raise()
                child.SetStatusText('Please save this file before quitting SPE.')
                return False
        eventManager.DeregisterWindow(self)
        self.frame.dead = 1
        if (not self.app.DEBUG) and self.getValue('RedirectShell'):
            self.shell.redirectStdin(0)
            self.shell.redirectStdout(0)
            self.shell.redirectStderr(0)
        fileList=[]
        if self.remember and self.app.children:
            active=self.app.childActive
            self.app.children.remove(active)
            self.app.children.append(active)
            for child in self.app.children :
                if child.fileName!=Child.NEWFILE:
                    pos     = child.source.GetCurrentPos()
                    lineno  = child.source.LineFromPosition(pos)
                    col     = child.source.GetColumn(pos)
                    fileList.append((child.fileName,lineno,col))
            if self.app.mdi and active:
                self.set('MaxChildren',active.frame.IsMaximized())
        #save the window size
        mainWindow=self.app.GetTopWindow()
        selfSize=mainWindow.GetRect()
        if not mainWindow.IsMaximized():
            self.set("sizex",selfSize.GetSize().x)
            self.set("sizey",selfSize.GetSize().y)
            self.set("posx",selfSize.GetPosition().x)
            self.set("posy",selfSize.GetPosition().y)
            self.set("maximize","False")
        else:
            self.set("maximize","True")
        try:
            self.userSave(NOTES,self.notes.GetValue())
            self.userSave(REMEMBER,str(fileList)) 
            self.userSave(RECENT,str(self.recent.files[:self.getValue('RecentFileAmount')]))
            self.userSave(FOLDERS,str([self.browser.depth.GetValue()]+self.browser.getFolders()[1:]))
        except Exception, message:
            self.messageEmail("""\
Spe Warning: can't save user settings (%s).  
Please report these details and operating system to s_t_a_n_i@yahoo.com."""%message)
        return 1
        
    def onClosePanelFrame(self,event=None):
        self.showShell(show=False,save=True)
        self.frame.menuBar.check_view()
        
    def onIdle(self,event=None):
        """Called when the parent frame is idle."""
        #child
        child=self.app.childActive
        if child:
            child.idle()
        #redraw
        if self.redraw:
            newTime=time.time()
            if newTime-self.idleTime>self.getValue('Redraw'):
                self.idleTime=newTime
                self.redraw()
                
    def onMove(self,event=None):
        """Called when the parent frame is moved."""
        if self.app.DEBUG: 
            print 'Event:  Parent: %s.onMove'%self.__class__
        if self.redraw:self.redraw()
        
    def onSize(self,event=None):
        """Called when the parent frame is resized."""
        if self.app.DEBUG: 
            print 'Event:  Parent: %s.onSize'%self.__class__
        if self.redraw:self.redraw()
        
    #---extra
    def excepthook(self, type, value, traceback) :
        webbrowser.open('''mailto:s_t_a_n_i@yahoo.com?subject=SPE %s error report&body="%s %s\n%s"'''%(type,type,value,traceback))
        
    def onFind(self,event,message=1):
        source=self.app.childActive.source
        try:
            self.findStr=event.GetFindString()
            self.findFlags=event.GetFlags()
            flags=0
            if wx.FR_WHOLEWORD & self.findFlags:
                flags|=wx.stc.STC_FIND_WHOLEWORD
            if wx.FR_MATCHCASE & self.findFlags:
                flags|=wx.stc.STC_FIND_MATCHCASE
            self.stcFindFlags=flags
        except:
            pass
        current=source.GetCurrentPos()
        position=source.FindText(current,len(source.GetText()),self.findStr,
                self.stcFindFlags)
        if position==-1:#wrap around
            self.wrapped=1
            position=source.FindText(0,current+len(self.findStr),self.findStr,self.stcFindFlags)
            self.SetActiveStatusText("Wrapped around to find '%s'"%self.findStr,1)
        if position==-1 and message and self.numberMessages<1:
            self.numberMessages=1
            self.message("'%s' not found!"%self.findStr)
            self.numberMessages=0
        source.GotoPos(position)
        source.SetSelection(position,position+len(self.findStr))
        return position
        
    def onFindClose(self,event):
        event.GetDialog().Destroy()
        self.numberMessages=0

    def onReplace(self,event,message=1):
        ## Next line avoid infinite loop
        findStr=event.GetFindString()
        self.replaceStr=event.GetReplaceString()
        if findStr==self.replaceStr:
            return -1
        source=self.app.childActive.source
        selection=source.GetSelectedText()
        if not(event.GetFlags() & wx.FR_WHOLEWORD):
            findStr=findStr.lower()
            selection=selection.lower()
            if findStr==self.replaceStr.lower():
                return -1
        if selection==findStr:
            position=source.GetSelectionStart()
            source.ReplaceSelection(self.replaceStr)
            source.SetSelection(position,position+len(self.replaceStr))
        position=self.onFind(event,message=message)
        return position

    def onReplaceAll(self,event):
        source=self.app.childActive.source
        count=0
        self.wrapped=0
        position=start=source.GetCurrentPos()
        while position>-1 and ((not self.wrapped) or position<start):
            position=self.onReplace(event,message=0)
            if position != -1: count+=1
        if count:
            self.SetActiveStatusText("'%s' is %s times replaced with '%s'"%\
                (event.GetFindString(),count,event.GetReplaceString()),1)
        elif not count and self.numberMessages<1:
            self.numberMessages=1
            self.message("'%s' not found!"%event.GetFindString())
            self.numberMessages=0
        
    ####Tabs
    def onTab(self,event):
        tab     = event.GetSelection()
        tabName = self.tabs[tab]
        method  = 'update'+tabName
        if hasattr(self,method):
            getattr(self,method)()
        if info.DARWIN:
            self.SetPageText(event.GetOldSelection(),'')
            self.SetPageText(tab,tabName)
        event.Skip()
        
        
    ####Sidebar
    def onTodoJump(self,event):
        file,line=self.todoList[event.GetData()]
        self.openList(file,line-1)

    def todoMax(self,child):
        try:
            child.updateTodo()
            return child.todoMax
        except:
            return 1
        
    def updateTodo(self):
        self.todo.DeleteAllItems()
        todoIndex=0
        self.todo.list=[]
        todoMax=[self.todoMax(child) for child in self.app.children]+[1]
        todoMax=max(todoMax)
        for child in self.app.children:
            todoIndexStart=todoIndex
            for task in child.todoList:
                line,urgency,entry=task
                item=self.todo.InsertStringItem(todoIndex, os.path.basename(child.fileName))
                self.todo.SetStringItem(todoIndex, 1, str(line+1))
                self.todo.SetStringItem(todoIndex, 2, str(urgency))
                self.todo.SetStringItem(todoIndex, 3, entry)
                self.todo.list.append((child.fileName,line+1))
                self.todo.SetItemData(item,todoIndex)
                todoIndex+=1
            if child.todoMax==todoMax:
                for i in child.todoHighlights:
                    item=self.todo.GetItem(todoIndexStart+i.wx())
                    item.SetBackgroundColour(wx.Colour(255,255,0))
                    self.todo.SetItem(item)

    #---index
    def onIndexJump(self,event):
        stripped,entry,line,colour,icon,file=self.indexList[event.GetData()]
        self.openList(file,line-1)
        
    def updateIndex(self):
        self.index.DeleteAllItems()
        indexList= self.index.list = []
        for child in self.app.children:
            child.updateIndex()
            indexList.extend(child.indexData)
        indexList.sort()
        firstLetter=''
        x=0
        index=0
        for element in indexList:
            stripped,entry,line,colour,icon,fileName=element
            if stripped[0]!=firstLetter:
                firstLetter=stripped[0]
                self.index.InsertStringItem(x, firstLetter)
                x+=1
            item=self.index.InsertImageStringItem(x, '%s@%s'%(entry.split('(')[0],os.path.basename(fileName)),icon)
            self.index.SetItemData(item,index)
            item=self.index.GetItem(item)
            item.SetTextColour(colour)
            self.index.SetItem(item)
            x+=1
            index+=1
        if self.index.GetItemCount():
            try:
                self.index.SetColumnWidth(-1,100)
            except:
                pass
    ####Methods
    def busyShow(self):
        wx.BeginBusyCursor()

    def busyHide(self):
        wx.EndBusyCursor()

    def checkBlender(self):
        """Check if source is running in Blender, otherwise give error message."""
        if self.Blender:return 1
        else:
            self.messageError(BLENDER_MESSAGE)
            return 0
            
    def redirect(self,value):
        self.shell.redirectStdin(value)
        self.shell.redirectStdout(value)
        self.shell.redirectStderr(value)

    def rememberSet(self,value):
        self.remember   = value
        self.frame.menuBar.check_remember(self.remember)

    def SetActiveStatusText(self,x,pos=1):
        try:
            self.app.childActive.SetStatusText(x,pos)
        except:
            self.SetStatusText(x,pos)

    def userOpen(self,fileName):
        f=open(os.path.join(INFO['userPath'],fileName),'r')
        content=f.read()
        f.close()
        return content

    def userSave(self,fileName,content):
        f=open(os.path.join(INFO['userPath'],fileName),'w')
        f.write(content)
        f.close()

    #---get
    def getChildByFileName(self,fileName):
        if fileName=='<source>':
            return self.app.childActive
        fileName = os.path.normcase(fileName)
        for child in self.app.children:
            if os.path.normcase(child.fileName)==fileName:
                return child
        return None
        
    def getFileNames(self):
        return [child.fileName for child in self.app.children]
    
    def getText(self):
        """Get raw text of current script window."""
        return str(self.app.childActive.source.GetText())
    
    #---messages
    def message(self,message,style=wx.OK | wx.ICON_INFORMATION):
        """Show a message with Ok button. (style offers other options)"""
        dlg = wx.MessageDialog(self, message, self.app.title, style)
        answer = dlg.ShowModal()
        dlg.Destroy()
        return answer
    
    def messageConfirm(self,message):
        """Show a confirm message (yes,no)"""
        answer=self.message(message,style=wx.YES_NO|wx.ICON_QUESTION)
        return self.messageIsOk(answer)

    def messageIsOk(self,answer):
        return answer==wx.ID_OK or answer==wx.ID_YES
        
    def messageCancel(self,message):
        """Show a yes,no or cancel message"""
        if self.app.DEBUG:
            print 'Dialog: Parent: %s.messageCancel'%self.__class__
        return self.message(message,style=wx.YES_NO|wx.ICON_QUESTION | wx.CANCEL)

    def messageError(self,message):
        """Display error message."""
        self.message(message,style=wx.OK | wx.ICON_ERROR)
        
    def messageEmail(self,message):
        webbrowser.open('mailto:s_t_a_n_i@yahoo.com?subject=SPE error (automatic report)&body=%s'%message)
        
    def messageEntry(self,message,default=''):
        """Show entry dialog box for user input."""
        dlg = wx.TextEntryDialog(self, message,self.app.title, default)
        if dlg.ShowModal() == wx.ID_OK:value=dlg.GetValue()
        else:value=None
        dlg.Destroy()
        return value

    def messageScrolled(self,message):
        """Show multiline scrollable message box."""
        from dialogs import speDialog
        if sys.platform!='win32':message='<font size=-2>%s</font>'%message
        speDialog.create(self, message, self.path)

    def messageHtml(self,fileName,doc=None):
        """Launch html with webbrowser."""
        if doc:
            fileName=os.path.join(doc,'doc',fileName)
        if fileName[0]=='/': fileName = 'file://'+fileName
        WebBrowser=self.get('WebBrowser')
        if WebBrowser==DEFAULT:
            webbrowser.open(fileName, 1)
        else:
            os.system("%s '%s'"%(WebBrowser,fileName))
            
    #---preferences     
    def preferencesSave(self):
        self.preferencesUpdate()
        try:
            defaults=open(INFO['defaultsUser'],'w')
            self.config.write(defaults)
            defaults.close()
        except Exception, message:
            print 'Spe warning: could not save user options in',INFO['defaultsUser']
            print message
            
    def preferencesUpdate(self):
        self.redirect((not self.app.DEBUG) and self.getValue('RedirectShell'))
        self.showShell(self.getValue('ShowShell'))
        self.frame.menuBar.check_view()
        for child in self.app.children:
            child.source.update()
        #restart?!
        restart = ''
        if self.app.mdiName     != self.get('Mdi'):
            restart += '- switch between multiple and single document interface\n  (%s>%s)\n'%(self.app.mdiName,self.get('Mdi'))
        if self.app.shortcuts   != self.get('Shortcuts'):
            restart += '- to use other keyboad shortcuts\n  (%s>%s)\n'%(self.app.shortcuts, self.get('Shortcuts'))
        #encoding
        encoding                = self.get('Encoding').split(',')[0].split(' ')[0]
        if encoding!=self.defaultEncoding:
            self.defaultEncoding = encoding
            if encoding=='<default>':
                wx.SetDefaultPyEncoding(INFO['encoding'])
            else:
                wx.SetDefaultPyEncoding(encoding)
        #restart
        if restart!=self.restartMessage:
            self.restartMessage = restart
            if restart:
                self.message('Please restart SPE to apply following changes:\n%s'%restart)

    def set(self,name,value,save=1):
        self.config.set('DEFAULT',name,str(value))
        if save: self.preferencesSave()       

    def get(self,name):
        return self.config.get('DEFAULT',name)
    
    def getValue(self,name):
        return eval(self.config.get('DEFAULT',name))
          
