####(c)www.stani.be-------------------------------------------------------------

import _spe.info as info
INFO=info.copy()

INFO['description']=\
"""File browser as tab."""

__doc__=INFO['doc']%INFO

####Modules---------------------------------------------------------------------
import codecs, inspect, os, sys, re, time

import wx
from wx.lib.evtmgr import eventManager

import sm, sm.spy, sm.uml, sm.wxp
from sm.wxp.stc import PythonSTC
from sm.wxp.realtime import Tree, ListCtrl

import _spe.help as help
import _spe.plugins.Pycheck as Pycheck
from sidebar.Browser import Browser

####Constants-------------------------------------------------------------------
DEFAULT                 = "<default>"
NEWFILE                 = 'unnamed'
SPE_ALLOWED_EXTENSIONS  = ['.py','.pyw','.tpy','.txt','.htm','.html']
STYLE_LIST              = wx.LC_REPORT
STYLE_NOTEBOOK          = wx.NO_BORDER
STYLE_NOTES             = wx.TE_MULTILINE|wx.TE_DONTWRAP
STYLE_SPLIT             = wx.SP_NOBORDER|wx.FULL_REPAINT_ON_RESIZE
STYLE_TREE              = wx.TR_HAS_BUTTONS
RE_TODO                 = re.compile('.*#[ ]*TODO[ ]*:(.+)', re.IGNORECASE)
RE_SEPARATOR            = re.compile('^.*(#-{3})')
RE_SEPARATOR_HIGHLIGHT  = re.compile('^.*(#{4})')
RE_ENCODING             = re.compile('# -[*]- coding[:=]\s*([-\w.]+)', re.IGNORECASE)

####Utilities-------------------------------------------------------------------
def umlAdd(classes, umlClass):
    """Add umlClass to classes dictionary"""
    if umlClass: 
        classes[umlClass.name.split('(')[0]] = umlClass

####Child Panel class-----------------------------------------------------------
class Source(PythonSTC):
    def __init__(self,parent):
        child = parent
        while child.__class__ != Panel:
            child = child.GetParent()
        PythonSTC.__init__(self,parent=parent,
            namespace= child.parentPanel.shell.interp.locals,
            path=child._fileName,config=child.parentPanel.config)
        self.SetHelpText(help.CHILD_SOURCE)
        child.source = self


class Panel(wx.SplitterWindow):
    ####Constructors------------------------------------------------------------
    def __init__(self,parent,name='',fileName='',source='',*args,**kwds):
        self._fileName      = fileName
        self._source        = source
        #initialize
        self.changed        = 0
        self.column         = 1
        self.eventChanged   = False
        self.line           = 1
        self.position       = 0
        self.sashPosition   = self.minSashPosition = [285,310][info.DARWIN]
        self.sidebarHidden  = False
        self.saved          = ''
        self.todoMax        = 1
        #delete when fixed
        self.updateBug      = False
        #construct
        wx.SplitterWindow.__init__(self, id=-1, parent=parent,style=STYLE_SPLIT)
        #Remember if this file contains DOS line endings (\r\n)
        #Otherwise assume Unix (\n)
        self.dosLines = (source.find('\r\n') >= 0)
        self.sashDelta      = 1
        
        
    def __finish__(self):
        frame = self.frame
        frame.setTitle(page=os.path.basename(self._fileName),extra=self._fileName)
        frame.SetIcon(sm.wxp.bitmap2Icon(self.app.bitmap('icon_py.png')))
        self.__source__(self._fileName,self._source)
        self.__sideBar__()
        #events
        self.source.SetDropTarget(DropOpen(self.parentPanel.openList))
        eventManager.Register(self.onSetFocus, wx.EVT_SET_FOCUS, self)
        eventManager.Register(self.onSash,wx.EVT_SPLITTER_SASH_POS_CHANGED,self)
        
    def __sideBar__(self):
        """Create notebook contents."""
        notebook = self.notebook = wx.Notebook(id=-1, parent=self, pos=wx.Point(2, 2),
              size=wx.Size(198, 481),style=STYLE_NOTEBOOK)
        self.updateSidebarTab=[self.updateExplore,self.updateBrowser,self.updateTodo,self.updateIndex,self.doNothing,self.doNothing]
        self.notebookLabel  = ['Explore','Browse','Todo','Index','Notes','Check']
        self.notebookIcons  = wx.ImageList(16,16)
        self.exploreIcon    = self.notebookIcons.Add(self.parentPanel.icons['explore.png'])
        self.browserIcon    = self.notebookIcons.Add(self.parentPanel.icons['browser.png'])
        self.todoIcon       = self.notebookIcons.Add(self.parentPanel.icons['todo.png'])
        self.indexIcon      = self.notebookIcons.Add(self.parentPanel.icons['index.png'])
        self.notesIcon      = self.notebookIcons.Add(self.parentPanel.icons['notes.png'])
        self.pycheckerIcon  = self.notebookIcons.Add(self.parentPanel.icons['pychecker.png'])
        if not info.DARWIN:
            self.notebook.SetBackgroundColour(wx.Colour(255,255,255))
        notebook.AssignImageList(self.notebookIcons)
        notebook.parentPanel=self.parentPanel

        #explore
        explore     = self.explore = Tree(parent=self.notebook,style=STYLE_TREE)#wx.TreeCtrl
        explore.SetBackgroundColour(wx.Colour(255,255,255))
        self.root   = self.explore.AddRoot('Right click to locate')
        explore.SetPyData(self.root,0)
        explore.SetImageList(self.parentPanel.iconsList)
        explore.SetItemImage(self.root,self.parentPanel.iconsListIndex['note.png'])
        explore.SetItemImage(self.root,self.parentPanel.iconsListIndex['note.png'],wx.TreeItemIcon_SelectedExpanded)
        explore.SetItemImage(self.root,self.parentPanel.iconsListIndex['note.png'],wx.TreeItemIcon_Expanded)
        explore.SetItemImage(self.root,self.parentPanel.iconsListIndex['note.png'],wx.TreeItemIcon_Selected)
        explore.SetHelpText(help.CHILD_EXPLORE)
        notebook.AddPage(page=self.explore.wx, text='Explore',imageId=self.exploreIcon)
        #browser
        browser         = self.browser = Browser(self.notebook, -1, os.path.dirname ( self._fileName ))
        browser.open    = self.onOpenFromBrowser
        notebook.AddPage (page=self.browser, text='', imageId=self.browserIcon)
        #todo
        todo            = self.todo = ListCtrl(parent=self.notebook,style=STYLE_LIST)
        todo.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, 
                heading='Line',width=40)
        todo.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, 
                heading='!',width=20)
        todo.InsertColumn(col=2, format=wx.LIST_FORMAT_LEFT, 
                heading='Task',width=500)
        todo.SetHelpText(help.CHILD_TODO)
        self.previousTodoHighlights = []
        notebook.AddPage(page=self.todo.wx, text='',imageId=self.todoIcon)
        #index
        index = self.index = ListCtrl(parent=self.notebook,style=STYLE_LIST)
        index.SetImageList(self.parentPanel.iconsList,wx.IMAGE_LIST_SMALL)
        index.InsertColumn(col=0, format=wx.LIST_FORMAT_LEFT, 
                heading='Line',width=50)
        index.InsertColumn(col=1, format=wx.LIST_FORMAT_LEFT, 
                heading='Entry',width=500)
        index.SetHelpText(help.CHILD_INDEX)
        notebook.AddPage(page=self.index.wx, text='',imageId=self.indexIcon)
        #notes
        self.notes = wx.TextCtrl(parent=self.notebook,id=-1,value=self.notesText,
            style=STYLE_NOTES)
        self.notes.SetHelpText(help.CHILD_NOTES)
        self.notebook.AddPage(page=self.notes, text='',imageId=self.notesIcon)
        #pyChecker
        self.pychecker          = Pycheck.Panel(self.notebook,page=5)
        self.notebook.AddPage(page=self.pychecker, text='',imageId=self.pycheckerIcon)        
        #events
        self.source.SetModEventMask(wx.stc.STC_MOD_DELETETEXT | wx.stc.STC_PERFORMED_USER)
        eventManager.Register(self.onSourceChange,wx.stc.EVT_STC_CHANGE,self.source)
        eventManager.Register(self.onSourceFromExplore,wx.EVT_TREE_ITEM_ACTIVATED,self.explore)
        eventManager.Register(self.onSourceFromExplore,wx.EVT_TREE_ITEM_RIGHT_CLICK,self.explore)
        eventManager.Register(self.onSourceFromTodo,wx.EVT_LIST_ITEM_SELECTED,self.todo)
        eventManager.Register(self.onSourceFromTodo,wx.EVT_LIST_ITEM_RIGHT_CLICK,self.todo)
        eventManager.Register(self.onSourceFromIndex,wx.EVT_LIST_ITEM_RIGHT_CLICK,self.index)
        eventManager.Register(self.onSourceFromIndex,wx.EVT_LIST_ITEM_SELECTED,self.index)
        eventManager.Register(self.updateSidebar,wx.EVT_NOTEBOOK_PAGE_CHANGED,self.notebook)
        #split
        self.SplitVertically(self.notebook, self.main, self.sashPosition)
        self.SetAutoLayout(True)
        #update
        self.updateExplore()

    def __source__(self,fileName,source):
        #notebook
        self.main = wx.Notebook(id=-1, parent=self, size=wx.Size(5000, 5000),style=wx.NO_BORDER)#, pos=wx.Point(2, 2),size=wx.Size(198, 481))
        self.mainIcons   = wx.ImageList(16,16)
        self.sashIcon    = self.mainIcons.Add(self.parentPanel.icons['source.png'])
        self.umlIcon     = self.mainIcons.Add(self.parentPanel.icons['uml.png'])
        self.main.AssignImageList(self.mainIcons)
        #self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        #self.mainSizer.Add(self.main, 1, wx.ALL | wx.EXPAND , 10)
        #self.SetAutoLayout(1)
        #self.SetSizer(self.mainSizer)
        
        #sash
        self.sash = PythonSTC(parent=self.main,
            namespace=self.parentPanel.shell.interp.locals,
            path=os.path.dirname(fileName),config=self.parentPanel.config)
        self.sash.SetHelpText(help.CHILD_SOURCE)
        self.source = self.sash
        #todo: implement this again with sashview
        #if wx.Platform == "__WXMAC__":
        #    self.source = self.sash
        #else:
        #    self.source = self.sash.view
        if fileName:
            self.fileName=fileName
            self.revert(source)
        else: 
            self.fileName=NEWFILE
            self.notesText=''
            self.frame.setTitle()
        self.source.EmptyUndoBuffer()
        self.source.Colourise(0, -1)
        self.source.menu=self.parentFrame.menuBar.edit
        self.main.AddPage(page=self.sash, text='Source',imageId=self.sashIcon)
        
        #uml
        self.uml    = sm.uml.wxCanvas(parent=self.main,style=wx.FULL_REPAINT_ON_RESIZE)
        self.main.AddPage(page=self.uml, text='Uml',imageId=self.umlIcon)
        
        #events
        eventManager.Register(self.onKillFocus, wx.EVT_KILL_FOCUS, self.source)
        eventManager.Register(self.source.OnRightClick, wx.EVT_RIGHT_UP, self.source)
        eventManager.Register(self.updateMain,wx.EVT_NOTEBOOK_PAGE_CHANGED,self.main)
    ####Menu--------------------------------------------------------------------
    #---file
    def save(self,fileName=None):
        """Saves the file."""
        if fileName: self.setFileName(fileName)     
        if self.fileName==NEWFILE or not(os.path.exists(os.path.dirname(self.fileName))):
            self.saveAs()
        else:
            self.source.assertEOL()
            source=self.source.GetText()
            if self.parentPanel.getValue('StripTrailingSpaces'):
                source='\n'.join([l.rstrip() for l in source.split('\n')])
            content = str(source.replace('\r\n','\n'))
            if not self.dosLines:
                #convert to Unix lines
                content     = str(source.replace('\r\n','\n'))
            #Note that the mode here must be "wb" to allow
            #line endings to be preserved.
            if self.encoding:
                file        = codecs.open(str(self.fileName),'wb',self.encoding)
            else:
                file        = open(str(self.fileName),'wb')
            file.write(content)
            file.close()
            self.notesSave(file=1)
            self.changed    = 0
            self.saved      = source
            self.parentPanel.recent.add([self.fileName])
            if self.parentPanel.getValue('CheckFileOnSave'):
                if not self.check():
                    self.parentPanel.shell.prompt()
            else:
                self.SetStatusText("File '%s' saved"%self.fileName,1)
            if fileName:
                self.frame.setTitle(os.path.basename(fileName),fileName)
            else:
                self.frame.setTitle()
        self.fileTime=os.path.getmtime(self.fileName)
        if self.parentPanel.get('UpdateSidebar')!='realtime':
            self.updateSidebar()
    
    def saveAs(self):
        defaultDir=os.path.dirname(self.fileName)
        dlg = wx.FileDialog(self, "Save As - www.stani.be", defaultDir=defaultDir, 
            wildcard=info.WILDCARD, 
            style=wx.SAVE|wx.OVERWRITE_PROMPT|wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            self.save(paths[0])
        dlg.Destroy()
        
    #---edit
    def comment(self):
        """Comment section"""
        doc = self.source
        sel = doc.GetSelection()
        start = doc.LineFromPosition(sel[0])
        end = doc.LineFromPosition(sel[1])
        if end > start and doc.GetColumn(sel[1]) == 0:
            end = end - 1
        doc.BeginUndoAction()
        for lineNumber in range(start, end + 1):
            firstChar = doc.PositionFromLine(lineNumber)
            doc.InsertText(firstChar, '##')
        doc.SetCurrentPos(doc.PositionFromLine(start))
        doc.SetAnchor(doc.GetLineEndPosition(end))
        doc.EndUndoAction()
        
    def uncomment(self):
        """Uncomment section"""
        doc = self.source
        sel = doc.GetSelection()
        start = doc.LineFromPosition(sel[0])
        end = doc.LineFromPosition(sel[1])
        if end > start and doc.GetColumn(sel[1]) == 0:
            end = end - 1
        doc.BeginUndoAction()
        for lineNumber in range(start, end + 1):
            firstChar = doc.PositionFromLine(lineNumber)
            if chr(doc.GetCharAt(firstChar)) == '#':
                if chr(doc.GetCharAt(firstChar + 1)) == '#':
                    # line starts with ##
                    doc.SetCurrentPos(firstChar + 2)
                else:
                    # line starts with #
                    doc.SetCurrentPos(firstChar + 1)
                doc.DelLineLeft()
        doc.SetSelection(sel[0],doc.PositionFromLine(end+1))
        doc.EndUndoAction()
                
    def insert_separator(self):
        from dialogs import separatorDialog
        separatorDialog.create(self).ShowModal()
        
    def go_to_line(self,scroll=1):
        """Go to line dialog & action"""
        line=self.parentPanel.messageEntry('Enter line number:')
        if line: self.scrollTo(int(line)-1)

    #---View
    def refresh(self):
        if self.parentPanel.redraw:self.parentPanel.redraw()
        if self.parentPanel.get('UpdateSidebar')!='realtime':
            self.updateSidebar()
        
    def onSash(self,event):
        if self.sidebarHidden:
            self.showSidebar()
        else:
            pos = event.GetSashPosition()
            if pos < self.minSashPosition:
                self.hideSidebar(self.minSashPosition)
            else: event.Skip()
        
    def toggle_sidebar(self,event):
        pos = self.GetSashPosition()
        if pos > 5:
            self.hideSidebar(pos)
        else:
            self.showSidebar()
        if self.frame.menuBar:
            self.frame.menuBar.check_sidebar(event)
        else:
            self.parentFrame.menuBar.check_sidebar(event)
            
    def hideSidebar(self,pos):
        self.sidebarHidden  = True
        self.sashPosition   = pos
        self.notebook.Hide()
        self.SetSashPosition(1)
        
    def showSidebar(self):
        self.sidebarHidden  = False
        self.notebook.Show()
        self.SetSashPosition(self.sashPosition)
        
    #---Tools
    def open_terminal_emulator(self):
        """Open terminal emulator"""       
        path,fileName=os.path.split(self.fileName)
        params = {'file':fileName,'path':path}
        terminal=self.parentPanel.get('Terminal')
        if terminal==DEFAULT:
            if info.WIN:
                os.system('start "Spe console - Press Ctrl+Break to stop" /D"%(path)s"'%params)
            else:
                os.system("cd \"%(path)s\"; /usr/X11R6/bin/xterm &"%params)
        else:
            os.system(terminal%params)

    def run_in_terminal_emulator(self):
        """Run in terminal emulator"""
        # todo: input stuff from preferences dialog box!
        path,fileName=os.path.split(self.fileName)
        params = {'file':fileName,'path':path}
        terminal=self.parentPanel.get('TerminalRun')
        if terminal==DEFAULT:
            if info.WIN:
                os.system('start "Spe - %(file)s - Press Ctrl+Break to stop" /D"%(path)s" start /B python "%(file)s"'%params)
            else:
                os.system("/usr/bin/Eterm -e 'cd \"%(path)s\"; python \"%(file)s\"'"%params)
        else:
            os.system(terminal%params)
            
    def run_in_terminal_emulator_exit(self):
        path,fileName=os.path.split(self.fileName)
        params = {'file':fileName,'path':path}
        terminal=self.parentPanel.get('TerminalRunExit')
        if terminal==DEFAULT:
            if info.WIN:
                os.system('start "Spe - %(file)s - Press Ctrl+Break to stop" /D"%(path)s" python "%(file)s"'%params)
            else:
                os.system("/usr/bin/Eterm -e 'cd \"%(path)s\"; python \"%(file)s\"'"%params)
        else:
            os.system(terminal%params)
        
    def check_source_with_pychecker(self): 
        """Check source with pychecker"""
        self.pychecker.check()
        
    #---Blender
    def load_in_blender(self):
        """Load in blender"""
        if self.checkBlender():
            child=self.parentPanel.childActive
            answer=child.confirmSave('Only saved contents will be loaded in Blender.')
            if answer:
                import blenpy.pyGui
                blenpy.pyGui.pythonLoad(child.fileName)
        
    def reference_in_blender(self):
        """Reference in blender"""
        if self.checkBlender():
            import blenpy.plugins.mouse
            blenpy.plugins.mouse.reference(self.parentPanel.childActive.fileName)
        
    ####Events------------------------------------------------------------------
    #---Smdi events
    def onActivate(self,event=None):
        if self.frame.menuBar:
            self.frame.menuBar.check_sidebar()
        else:
            self.parentFrame.menuBar.check_sidebar()
            self.updateStatus()
        self.source.SetFocus()

    def onClose(self, event=None):
        if self.confirmSave():
            eventManager.DeregisterWindow(self)
            self.frame.dead = 1
            if len(self.app.children)==1:
                self.parentFrame.menuBar.enable(0)
            return True
        else: return False
        return True
        
    def onSize(self, event=None):
        self.source.SetFocus()

    #---Panel events
    def onSetFocus(self,event):
        event.Skip()
        self.checkTime()
        try:
            self.source.SetFocus()
        except:
            pass
       
    #---Source events
    def onSourceChange(self,event):
        self.eventChanged = True

    def onSourcePositionChange(self,event=None):
        """Updates statusbar with current position."""
        
    def idle(self,event=None):
        if self.frame.dead: return
        if self.eventChanged:
            if self.changed     == 0:
                self.changed    = 1
                self.frame.setTitle()
            elif self.changed   < 0:
                self.changed+=1
            self.eventChanged   = False
            if self.parentPanel.get('UpdateSidebar')=='realtime':
                self.updateSidebar()
        pos = self.source.GetCurrentPos()
        if pos!= self.position:
            self.updateStatus(pos)
            #if not self.check():
            #    self.parentPanel.shell.prompt()
                
    def onKillFocus(self,event=None):
        if self.app.DEBUG:
            print 'Event:  Child: %s.onKillFocus(dead=%s)'%(self.__class__,self.frame.dead)
        try:
            if not self.frame.dead and self.parentPanel.get('UpdateSidebar')=='when clicked':
                self.source.SetSTCFocus(0)
                self.updateSidebar()
            event.Skip()
        except:
            pass
        
    #---Sidebar update methods & jump events
    def updateSidebar(self,event=None):
        if event:
            tab = event.GetSelection()
            self.notebook.SetPageText(event.GetOldSelection(),'')
            self.notebook.SetPageText(tab,self.notebookLabel[tab])
            event.Skip()
        else:
            tab = self.notebook.GetSelection()
        try:
            self.updateSidebarTab[tab]()
        except Exception, message:
            if self.updateBug:
                self.setStatus('BUG #4627: PLEASE RESTART SPE!')
            else:
                self.updateBug = True
                message= """SPE bug: updateSidebar(%s)\n
Bug #4627 has occured, which makes SPE unstable. Please save all files and
restart SPE. If you are able to reconstruct this bug, leave a detailed comment
at http://developer.berlios.de/bugs/?func=detailbug&bug_id=4627&group_id=4161
and also give these details (copy & paste from shell):\n
%s\n\n%s"""%(self.parentPanel.get('UpdateSidebar'),message,sm.spy.message(1))
                print message
                self.parentPanel.messageError(message)
        
    def updateBrowser(self): 
        self.browser.update()
        
    def updateStatus(self,pos=None):
        if hasattr(self,'source'):
            source          = self.source
            if not pos: pos = source.GetCurrentPos()
            self.position   = pos
            line            = source.LineFromPosition(pos)
            column          = source.GetColumn(pos)
            if line != self.line:
                self.line   = line
                self.SetStatusText('Line %05d'%(line+1),2)
            if column != self.column:
                self.column=column
                self.SetStatusText('Column %03d'%column,3)
        else:
            self.SetStatusText('',2)
            self.SetStatusText('',3)
       
    def updateTodo(self):
        """Update todo tab in sidebar."""
        #get text
        try:
            text=self.source.GetText().split('\n')
        except:
            return
        #initialize
        tryMode                     = 0 #try, except are false indentations
        hierarchyIndex              = 0
        todoData                    = []
        todoIndex                   = 0
        self.todoMax                = 1
        self.todoHighlights         = []
        self.todoList               = []
        hierarchy                   = [(-1,self.root)]
        self.todo.DeleteAllItems()
        #loop through code wxPython.lib.evtmgr
        for line in range(len(text)):
            l                       = text[line].strip()
            todo_hit                = RE_TODO.match(l)
            first                   = l.split(' ')[0]
            if first=='try:':
                tryMode         += 1
            elif first[:6]=='except':
                tryMode         = max(0,tryMode-1)
            elif first[:7]=='finally':
                tryMode         = max(0,tryMode-1)
            elif todo_hit:
                #todo entry
                task                    = todo_hit.group(1)
                urgency                 = task.count('!')
                self.todoList.append((line,urgency,task))
                item                    = self.todo.InsertStringItem(todoIndex, str(line+1), str(urgency), task)
                self.todo.SetItemData(item,line+1)
                #highlights
                newMax                  = max(self.todoMax,urgency)
                if newMax>self.todoMax:
                    self.todoMax        =   newMax
                    self.todoHighlights = [item]
                elif urgency==self.todoMax:
                    self.todoHighlights.append(item)
                todoIndex+=1
        #highlight most urgent todos
        for i in self.todoHighlights:
            if i not in self.previousTodoHighlights:
                item=self.todo.GetItem(i)
                item.SetBackgroundColour(wx.Colour(255,255,0))
                self.todo.SetItem(item)
        for i in self.previousTodoHighlights:
            if i not in self.todoHighlights:
                item=self.todo.GetItem(i)
                item.SetBackgroundColour(wx.Colour(255,255,255))
                self.todo.SetItem(item)
        self.previousTodoHighlights = self.todoHighlights
        self.todo.Clean()
        
    def updateIndex(self):
        """Update index tab in sidebar."""
        #get code
        try:
            text=self.source.GetText().split('\n')
        except:
            return
        #initialize
        tryMode         = 0
        hierarchyIndex  = 0
        self.indexData  = []
        #loop through code
        for line in range(len(text)):
            l           = text[line].split('#')[0].strip()
            first       = l.split(' ')[0]
            if first=='try:':
                tryMode         += 1
            elif first[:6]=='except':
                tryMode         = max(0,tryMode-1)
            elif first[:7]=='finally':
                tryMode         = max(0,tryMode-1)
            elif first in ['class','def'] and l[:8]!='__init__':
                if first=='class':
                    colour  = wx.Colour(255,0,0)
                    icon    = 'folder_tar.png'
                else:
                    colour  = wx.Colour(0,0,255)
                    icon    = 'kmail.png'
                self.indexData.append((l.replace('_',' ').lstrip(),l,line+1,colour,
                    self.parentPanel.iconsListIndex[icon],self.fileName))
        #make index tab
        self.indexData.sort()
        firstLetter = ''
        x           = 0
        self.index.DeleteAllItems()
        for element in self.indexData:
            stripped,entry,line,colour,icon,fileName=element
            if entry.split(' ')[1][0]!=firstLetter:
                firstLetter=entry.split(' ')[1][0]
                self.index.InsertStringItem(x, ' ', '%s (%s)'%(firstLetter.upper(),entry.split(' ')[0]))
                x+=1
            item=self.index.InsertImageStringItem(x, icon, str(line), entry)
            self.index.SetItemData(item,line-1)
            self.index.SetItemTextColour(item,colour)
            x+=1
        #if self.parentPanel.indexVisible...
            
    def updateExplore(self,uml=0):
        """Updates explore in sidebar."""
        #get text
        try:
            text=self.source.GetText().split('\n')
        except:
            return
        #initialize
        if uml:         
            self.umlClass   = None
            previous    = 0
        classes         = {}
        n               = len(text)
        tryMode         = 0
        hierarchyIndex  = 0
        hierarchy       = [(-1,self.root)]
        separators      = []
        self.encoding   = None
        self.explore.CollapseAndReset(self.root)
        for line in range(len(text)):
            l           = text[line].strip()
            first       = l.split(' ')[0]
            sepa_hit    = RE_SEPARATOR.match(l)
            sepb_hit    = RE_SEPARATOR_HIGHLIGHT.match(l)
            encode_hit  = RE_ENCODING.match(l)
            if first in ['class','def','import','from'] or encode_hit:
                if 1 or l.find('(')!=-1 or l.find(':') !=-1 or first in ['from','import'] or encode_hit:
                    #indentation--------------------------------------------
                    indentation         = max(0,len(text[line])-
                        len(text[line].lstrip())-tryMode*4)
                    #situate in hierachy------------------------------------
                    hierarchyIndex      = 0
                    while hierarchyIndex+1<len(hierarchy) and \
                            hierarchy[hierarchyIndex+1][0]<indentation:
                        hierarchyIndex  += 1
                    hierarchy=hierarchy[:hierarchyIndex+1]
                    if uml and hierarchyIndex<=previous: 
                        umlAdd(classes,self.umlClass)
                        self.umlClass    = None
                    #get definition-----------------------------------------
                    if encode_hit:
                        l = encode_hit.group(1)
                        self.encoding = l
                    else:
                        l = l.split('#')[0].strip()
                    i=1
                    if not(first in ['import','from'] or encode_hit):
                        search  = 1
                        rest    = ' '
                        while search and l[-1] != ':' and i+line<n:
                            #get the whole multi-line definition
                            next = text[line+i].split('#')[0].strip()
                            if next.find('class')==-1 and next.find('def')==-1 and next.find('import')==-1:
                                rest    += next
                                i       += 1
                            else:
                                search = 0
                        if rest[-1] == ':':l+= rest
                    #put in tree with color---------------------------------
                    l=l.split(':')[0].replace('class ','').replace('def ','').strip()
                    if separators: 
                        self.appendSeparators(separators,hierarchy,hierarchyIndex,uml)
                        separators      = []
                    if l:
                        item                = self.explore.AppendItem(hierarchy[hierarchyIndex][1],l)
                        self.explore.SetPyData(item,line)
                        intensity=max(50,255-indentation*20)
                        if encode_hit:
                            colour              = wx.Colour(intensity-50,0,intensity-50)
                            icon                = iconExpand = 'encoding.png'
                        elif first == 'class':
                            if uml:
                                umlAdd(classes,self.umlClass)
                                self.umlClass   = sm.uml.Class(name=l,data=line)
                                previous        = hierarchyIndex
                            colour              = wx.Colour(intensity,0,0)
                            icon                = 'class.png'
                            iconExpand          = 'class.png'
                        elif first in ['import','from']:
                            colour              = wx.Colour(0,intensity-50,0)
                            icon                = iconExpand = 'import.png'
                        else:
                            if uml and self.umlClass: self.umlClass.append(l)
                            colour          = wx.Colour(0,0,intensity)
                            icon            = iconExpand = 'def.png'
                        self.explore.SetItemTextColour(item,colour)
                        self.explore.SetItemImage(item,
                            self.parentPanel.iconsListIndex[icon],
                            which=wx.TreeItemIcon_Normal)
                        if first=='class':
                            self.explore.SetItemImage(item,
                                self.parentPanel.iconsListIndex[iconExpand],
                                which       = wx.TreeItemIcon_Expanded)
                        hierarchy.append((indentation,item))
            elif sepa_hit:
                #separator
                pos = sepa_hit.end()
                colours=l[pos:].split('#')
                if len(colours)==3:
                    s       = sm.rstrip(colours[0],'_')
                    fore    = '#'+colours[1][:6]
                    back    = '#'+colours[2][:6]
                else:
                    s=sm.rstrip(l[pos:],'-')
                    fore=wx.Colour(128,128,128)
                    back=None
                if s.strip(): separators.append((s,line,fore,back))
            elif sepb_hit:
                #highlighted separator (yellow)
                pos = sepb_hit.end()
                s   = sm.rstrip(l[pos:],'-')
                if s.strip(): separators.append((s,line,wx.Colour(0,0,0),wx.Colour(255,255,0)))
            elif first=='try:':
                tryMode         += 1
            elif first[:6]=='except':
                tryMode         = max(0,tryMode-1)
            elif first[:7]=='finally':
                tryMode         = max(0,tryMode-1)
        self.appendSeparators(separators,hierarchy,hierarchyIndex,uml)
        if uml: umlAdd(classes,self.umlClass)
        #expand root of explore
        self.explore.Expand(self.root)
        #if self.parentPanel.exploreVisible: ...
        self.explore.Clean()
        return classes
        
    def updateMain(self,event=None):
        if event:
            tab = event.GetSelection()
            event.Skip()
            if tab == 0:
                self.source.SetFocus()
            elif tab == 1:
                self.uml.DrawUml(classes=self.updateExplore(uml=1))
        else:
            tab = self.notebook.GetSelection()
        self.updateSidebarTab[tab]()
        
    def refreshMain(self):
        pos = self.GetSashPosition()
        self.sashDelta *= -1
        self.SetSashPosition(pos+self.sashDelta, redraw=1)
        
    def doNothing(self):
        pass
    
    def appendSeparators(self,separators,hierarchy,hierarchyIndex,uml):
        explore = self.explore
        for separator in separators:
            label,line,fore,back=separator
            sep=explore.AppendItem(hierarchy[hierarchyIndex][1],label)
            explore.SetItemBold(sep)
            explore.SetItemTextColour(sep,fore)
            if back:explore.SetItemBackgroundColour(sep,back)
            explore.SetItemImage(sep,self.parentPanel.iconsListIndex['separator.png'])
            explore.SetPyData(sep,line)
            if uml and self.umlClass: self.umlClass.append(label,t=sm.uml.SEPARATOR)

    def onSourceFromExplore(self,event):
        """Jump to source line by clicking class or function in explore."""
        line=self.explore.GetPyData(event.GetItem())
        self.scrollTo(line,select='line')
            
    def onOpenFromBrowser(self, fname):
        if os.path.splitext(fname)[-1] in SPE_ALLOWED_EXTENSIONS:
            self.parentPanel.openList([fname])
        else:
            os.startfile(fname)

    def onSourceFromTodo(self,event):
        """Jump to source line by clicking task in todo."""
        line=event.GetData()
        self.scrollTo(line-1,scroll=1)
        
    def onSourceFromIndex(self,event):
        """Jump to source line by clicking task in todo."""
        line=event.GetData()
        self.scrollTo(line,scroll=1)

#---methods---------------------------------------------------------------------
    def check(self):
        pythonFile=(os.path.splitext(self.fileName)[1].lower() in ['.py','.pyw'])
        if pythonFile:
            from sm.scriptutils import CheckFile
            return CheckFile(self.fileName,jump=self.parentPanel.openList,
                status=self.setStatus)
        else: return 1

    def checkTime(self):
        if (not self.frame.dead) and os.path.exists(self.fileName):
            try:
                pos=self.source.GetCurrentPos()
                fileTime=os.path.getmtime(self.fileName)
                if fileTime>self.fileTime:
                    #file is modified
                    self.fileTime=fileTime
                    baseName=os.path.basename(self.fileName)
                    message=baseName+' is modified externally.\nDo you want to reload it%s?'
                    if  (self.changed>0 and self.parentPanel.messageConfirm(message%' and loose current changes')) or\
                    (not self.changed>0 and (self.parentPanel.getValue('AutoReloadChangedFile') or self.parentPanel.messageConfirm(message%''))): 
                        self.revert()
                        self.source.GotoPos(pos)
                        return 1
            except:
                return 0
                

    def confirmSave(self, message=''):
        self.notesSave(file=1)
        if self.changed>0:
            self.Raise()
            message+='\nSave changes to "%s"?'%self.fileName
            answer=self.parentPanel.messageCancel(message)
            if answer==wx.ID_CANCEL:
                return 0
            elif self.parentPanel.messageIsOk(answer):
                self.save()
                return 1
            else:return 1
        else:return 1
        
    def refreshTitle(self):
        if self.app.DEBUG:
            print 'Method: Child: %s.refreshTitle("%s")'%(self.__class__,self.fileName)
        self.frame.setTitle()
        
    def revert(self,source=None):
        if not source:
            try:
                source          = open(self.fileName).read()
                encode_hit      = RE_ENCODING.match(source)
                if encode_hit:
                    self.encoding   = encode_hit.group(1)
                    if self.encoding != INFO['encoding']:
                        source.encode()
            except:
                source=''
        if self.parentPanel.getValue('ConvertTabsToSpaces'):
            source=source.replace('\t',' '.ljust(self.parentPanel.getValue('TabWidth')))
        self.source.SetText(source)
        self.source.assertEOL()
        try:
            self.notesText=open(self.notesFile()).read()
        except:
            self.notesText=''
        self.frame.setTitle()
        self.changed=0

    def setFileName(self,fileName):
        self.fileName   = fileName
        self.name       = self.name = os.path.basename(self.fileName)
        index           = self.frame.getIndex()
        mdi             = self.app.mdi
        if not mdi:index+= 1
        if hasattr(self.frame,'tabs'):
            self.frame.tabs.SetPageText(index,self.name)
        self.frame.setTitle()
        if not mdi:
            for child in self.app.children:
                child.frame.tabs.SetPageText(index,self.name)

    def setStatus(self,text,i=1):
        self.SetStatusText(text,i)
        
    def sidebarVisible(self):
        return self.GetSashPosition() > 5
        
    def scrollTo(self,line=0,column=0,select='pos',scroll=0):
        source  = self.source
        source.EnsureVisible(line)
        line    = source.VisibleFromDocLine(line)
        linePos = source.PositionFromLine(line)
        pos     = linePos+column
        if select=='line':
            source.SetSelection(linePos, source.GetLineEndPosition(line))
        else: #select=='pos':
            source.GotoPos(pos)
        source.ScrollToLine(line)
        source.ScrollToColumn(0)
        source.SetFocus()

    def notesFile(self):
        return os.path.splitext(self.fileName)[0]+'_notes.txt'
    
    def notesSave(self,file=0):
        if not hasattr(self,'notes'):
            return
        self.notesText=self.notes.GetValue()
        if file:
            if not self.notesText:
                try:
                    os.remove(self.notesFile())
                except:
                    pass
            else:
                f=open(self.notesFile(),'w')
                f.write(self.notesText)
                f.close()

    def selectLine(self,line):
        source=self.source
        

class DropOpen(wx.FileDropTarget):
    """Opens a file when dropped on parent frame."""
    def __init__(self,openList):
        wx.FileDropTarget.__init__(self)
        self.openList   = openList
    def OnDropFiles(self,x,y,fileNames):
        fileNames       = [script for script in fileNames 
            if os.path.splitext(script)[-1].lower() in SPE_ALLOWED_EXTENSIONS]
        if fileNames:
            self.openList(fileNames)
            return 1
        else:return 0