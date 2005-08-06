#(c)www.stani.be (read __doc__ for more information)
import sm
INFO=sm.INFO.copy()

INFO['author']    = 'Robin Dunn'
INFO['date']      = 'A long time ago, in a galaxy far, far away...'
INFO['copyright'] ='(c) 1999 by Total Control Software'
INFO['title']     = INFO['titleFull'] = 'wxPython stc control'

INFO['description']=\
"""Changes:
    - apr 2004:
        + wx namespace rewrite by SM
    - sep 2003:
        + Indent/dedent fix by SM
        + Autocompletion keyboard generic by GF (guillermo.fernandez@epfl.ch)
    - may 2003:
        + Adapted by SM (www.stani.be) for spe to include autocompletion and
          callbacks
"""

__doc__=INFO['doc']%INFO
#_______________________________________________________________________________
import re

#Original header:

#-------------------------------------------------------------------------------
# Author:       Robin Dunn
#
# Created:      A long time ago, in a galaxy far, far away...
# Copyright:    (c) 1999 by Total Control Software
# Licence:      wxWindows license
#
#-------------------------------------------------------------------------------

import wx
import wx.stc as wx_stc
import wx.gizmos as wx_gizmos

import inspect,keyword,os,sys

#-------------------------------------------------------------------------------

WORDCHARS = "_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

#-------------------------------------------------------------------------------
try:
    True
except NameError:
    True = 1==1
    False = 1==0



#----------------------------------------------------------------------

class PythonBaseSTC(wx_stc.StyledTextCtrl):
    def __init__(self, parent, id=-1,namespace={},path=None,config=None,
            ignore=None):
        wx_stc.StyledTextCtrl.__init__(self, parent, id,
                                  style = wx.FULL_REPAINT_ON_RESIZE|wx.NO_BORDER)
        #PASSING VALUES
        self.namespace=namespace
        self.config=config
        self.ignore=ignore
        if path and path not in sys.path: sys.path.append(path)
        
        #INITIALIZE
        self.calltip=0 #calltip counter
        self.SetLexer(wx_stc.STC_LEX_PYTHON)

        #KEYBOARD SHORTCUTS (what are they doing here?)
        self.CmdKeyAssign(ord('B'), wx_stc.STC_SCMOD_CTRL, wx_stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), wx_stc.STC_SCMOD_CTRL, wx_stc.STC_CMD_ZOOMOUT)
        
        #PYTHON
        self.SetLexer(wx_stc.STC_LEX_PYTHON)
        keywords=keyword.kwlist
        keywords.extend(['None','as','True','False'])
        self.SetKeyWords(0, " ".join(keywords))
        
        #GENERAL
        self.AutoCompSetIgnoreCase(False)
        
        #FOLDING
        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetProperty("fold.comment.python", "0")
        self.SetProperty("fold.quotes.python", "0")
        
        #USER SETTINGS
        if config:
            self.update()
        else:
            self.SetViewWhiteSpace(0)
            self.SetTabWidth(4)
            self.SetIndentationGuides(1)
            self.SetUseTabs(0)
            self.SetEdgeMode(wx_stc.STC_EDGE_LINE)
            self.SetEdgeColumn(79)
            #self.faces
            if wx.Platform == '__WXMSW__':
                self.faces = { 'times': 'Courier New',
                          'mono' : 'Courier New',
                          'helv' : 'Courier New',
                          'other': 'Courier New',
                          'size' : 10,
                          'size2': 10,
                         }
            ##    self.faces = { 'times': 'Times New Roman',
            ##              'mono' : 'Courier New',
            ##              'helv' : 'Arial',
            ##              'other': 'Comic Sans MS',
            ##              'size' : 10,
            ##              'size2': 8,
            ##             }
            else:
                self.faces = { 'times': 'Times',
                          'mono' : 'Courier',
                          'helv' : 'Helvetica',
                          'other': 'new century schoolbook',
                          'size' : 12,
                          'size2': 10,
                         }
            self.SetWordChars(WORDCHARS)
        self.SetStyles()

        self.SetBackSpaceUnIndents(1)
##        self.SetTabIndents(0)
##        self.SetIndent(1)
        self.SetEdgeColumn(79)
        self.SetEdgeColour(wx.Colour(200,200,200))
        
        #MARGINS
        self.SetMargins(0,0)
        #margin 1 for line numbers
        self.SetMarginType(1, wx_stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 40)
        #margin 2 for markers
        self.SetMarginType(2, wx_stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, wx_stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        if 0: # simple folder marks, like the old version
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDER, wx_stc.STC_MARK_ARROW, "navy", "navy")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDEROPEN, wx_stc.STC_MARK_ARROWDOWN, "navy", "navy")
            # Set these to an invisible mark
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDEROPENMID, wx_stc.STC_MARK_BACKGROUND, "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDERMIDTAIL, wx_stc.STC_MARK_BACKGROUND, "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDERSUB, wx_stc.STC_MARK_BACKGROUND, "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDERTAIL, wx_stc.STC_MARK_BACKGROUND, "white", "black")

        else: # more involved "outlining" folder marks
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDEREND,     wx_stc.STC_MARK_BOXPLUSCONNECTED,  "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDEROPENMID, wx_stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDERMIDTAIL, wx_stc.STC_MARK_TCORNER,  "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDERTAIL,    wx_stc.STC_MARK_LCORNER,  "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDERSUB,     wx_stc.STC_MARK_VLINE,    "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDER,        wx_stc.STC_MARK_BOXPLUS,  "white", "black")
            self.MarkerDefine(wx_stc.STC_MARKNUM_FOLDEROPEN,    wx_stc.STC_MARK_BOXMINUS, "white", "black")
        wx_stc.EVT_STC_UPDATEUI(self,    id, self.OnUpdateUI)
        wx_stc.EVT_STC_MARGINCLICK(self, id, self.OnMarginClick)

        # STYLES
        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.
        # Default style
        self.StyleSetSpec(wx_stc.STC_STYLE_DEFAULT,
                          "face:%(mono)s,size:%(size)d" % \
                          self.faces)
        self.StyleSetBackground(wx_stc.STC_STYLE_BRACELIGHT,"#AAAAFF")

        self.SetCaretForeground("BLACK")
        self.SetSelBackground(1,'DARK TURQUOISE')

        #EVENTS
        wx.EVT_KEY_DOWN(self, self.OnKeyDown)
        wx.EVT_CHAR(self, self.OnChar)

    #---events
    def OnKeyDown(self, event):
        """"""
        key = event.KeyCode()
        control = event.ControlDown()
        #shift=event.ShiftDown()
        alt=event.AltDown()
        if key == wx.WXK_RETURN and not control and not alt and not self.AutoCompActive():
            #auto-indentation
            if self.CallTipActive():
                self.CallTipCancel()
                self.calltip=0
            line = self.GetCurrentLine()
            txt = self.GetLine(line)
            pos=self.GetCurrentPos()
            linePos=self.PositionFromLine(line)
            self.CmdKeyExecute(wx_stc.STC_CMD_NEWLINE)
            indent = self.GetLineIndentation(line)
            padding = self.indentation * (indent/max(1,self.tabWidth))
            newpos = self.GetCurrentPos()
            if self.needsIndent(txt[:pos-linePos]):
                padding += self.indentation
            self.InsertText(newpos, padding)
            newpos += len(padding)
            self.SetCurrentPos(newpos)
            self.SetSelection(newpos, newpos)
        else:
            event.Skip()

    def OnChar(self,event):
        key     = event.KeyCode()
        control = event.ControlDown()
        alt     = event.AltDown()
        # GF We avoid an error while evaluating chr(key), next line.
        if key > 255:
            event.Skip()
        # GF No keyboard needs control or alt to make '(', ')' or '.'
        # GF Shift is not included as it is needed in some keyboards.
        elif chr(key) in ['(',')','.'] and not control and not alt:
            pos         = self.GetCurrentPos()
            CallTips    = self.get('CallTips').lower()
            if key == ord('(') and CallTips!='disable':
                # ( start tips
                if self.CallTipActive():
                    self.calltip    += 1
                    self.AddText('(')
                else:
                    #prepare
                    obj=self.getWordObject()
                    self.AddText('(')
                    if not obj: return
                    #docstring
                    if hasattr(obj,'__init__'):
                        init    = obj.__init__
                        tip     = getargspec(init).strip()
                        if tip == '(self, *args, **kwargs)':
                            tip = ""
                        else:
                            tip = "%s\n"%tip
                        print repr(tip)
                        doci    = init.__doc__.strip()
                        if doci:
                            doc = '%s\n'%(doci)
                    else:
                        doc = ""
                        tip = getargspec(obj)
                    doc += obj.__doc__
                    if doc:
                        if CallTips == 'first paragraph only':
                            tip += doc.split('\n')[0]
                        else:
                            tip += doc
                    if tip:
                        self.calltip=1
                        tip+='\n(Press ESC to close)'
                        self.CallTipSetBackground('#FFFFE1')
                        self.CallTipShow(pos, tip.replace('\r\n','\n'))
            elif key == ord(')'):
                # ) end tips
                self.AddText(')')
                if self.calltip:
                    self.calltip-=1
                    if not self.calltip:self.CallTipCancel()
            elif key == ord('.') and self.getint('AutoComplete'):
                # . Code completion
                self.autoComplete(object=1)
            else:
                event.Skip()
        else:
            event.Skip()

    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()
        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == wx_stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)
            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == wx_stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            #pt = self.PointFromPosition(braceOpposite)
            #self.Refresh(True, wx.Rect(pt.x, pt.y, 5,5))
            #print pt
            #self.Refresh(False)


    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())
                if self.GetFoldLevel(lineClicked) & wx_stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)


    def OnRightClick(self, event):
        if self.menu:
            self.PopupMenu(self.menu, event.GetPosition())
        else:
            event.Skip()

    def SetViewEdge(self,check):
            if check:
                self.SetEdgeMode(wx_stc.STC_EDGE_LINE)
            else:
                self.SetEdgeMode(wx_stc.STC_EDGE_NONE)

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & wx_stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break;

        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & wx_stc.STC_FOLDLEVELHEADERFLAG and \
               (level & wx_stc.STC_FOLDLEVELNUMBERMASK) == wx_stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)
                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1
        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & wx_stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1;

        return line

#---preferences-----------------------------------------------------------------
    def get(self,name):
        return self.config.get('DEFAULT',name)
        
    def getint(self,name):
        try:
            return self.config.getint('DEFAULT',name)
        except:#True,False
            if eval(self.config.get('DEFAULT',name)):
                return 1
            else:
                return 0
    
    def update(self):
        #general
        font,size=self.get('Font').split(',')
        size=eval(size)
        self.faces={'times': font, 'mono' : font, 'helv' : font, 'other': font,
                    'size' : size, 'size2': size}
        self.SetStyles()
        #guides
        self.SetEdgeColumn(self.getint('EdgeColumn'))
        self.SetViewEdge(self.getint('ViewEdge'))
        self.SetIndentationGuides(self.getint('IndentationGuides'))
        #tabs & whitespaces
        self.tabWidth = self.getint('TabWidth')
        self.SetTabWidth(self.getint('TabWidth'))
        self.SetUseTabs(self.getint('UseTabs'))
        self.SetViewWhiteSpace(self.getint('ViewWhiteSpace'))
        if self.getint('UseTabs'):
            self.indentation = '\t'
        else:
            self.indentation = " " * self.tabWidth
        self.SetWordChars(self.get('WordChars'))
        
    def SetStyles(self):
        self.StyleClearAll()

        # anti-aliasing
        if hasattr(self,'SetUseAntiAliasing'):
            self.SetUseAntiAliasing(True)

        # Global default styles for all languages
        self.StyleSetSpec(wx_stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % self.faces)
        self.StyleSetSpec(wx_stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % self.faces)
        self.StyleSetSpec(wx_stc.STC_STYLE_CONTROLCHAR, "face:%(other)s" % self.faces)
        self.StyleSetSpec(wx_stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
        self.StyleSetSpec(wx_stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")

        # Python styles
        # White space
        self.StyleSetSpec(wx_stc.STC_P_DEFAULT, "face:%(mono)s,size:%(size)d" % self.faces)
        # Comment
        self.StyleSetSpec(wx_stc.STC_P_COMMENTLINE, "fore:#007F00,back:#E8FFE8,italic,face:%(other)s,size:%(size)d" % self.faces)
        # Number
        self.StyleSetSpec(wx_stc.STC_P_NUMBER, "fore:#007F7F,size:%(size)d" % self.faces)
        # String
        self.StyleSetSpec(wx_stc.STC_P_STRING, "fore:#7F007F,face:%(times)s,size:%(size)d" % self.faces)
        # Single quoted string
        self.StyleSetSpec(wx_stc.STC_P_CHARACTER, "fore:#7F007F,face:%(times)s,size:%(size)d" % self.faces)
        # Keyword
        self.StyleSetSpec(wx_stc.STC_P_WORD, "fore:#00007F,bold,size:%(size)d" % self.faces)
        # Triple quotes
        self.StyleSetSpec(wx_stc.STC_P_TRIPLE, "fore:#7F0000,size:%(size)d" % self.faces)
        # Triple double quotes
        self.StyleSetSpec(wx_stc.STC_P_TRIPLEDOUBLE, "fore:#7F0000,size:%(size)d" % self.faces)
        # Class name definition
        self.StyleSetSpec(wx_stc.STC_P_CLASSNAME, "fore:#0000FF,bold,underline,size:%(size)d" % self.faces)
        # Function or method name definition
        self.StyleSetSpec(wx_stc.STC_P_DEFNAME, "fore:#007F7F,bold,size:%(size)d" % self.faces)
        # Operators
        self.StyleSetSpec(wx_stc.STC_P_OPERATOR, "bold,size:%(size)d" % self.faces)
        # Identifiers
        self.StyleSetSpec(wx_stc.STC_P_IDENTIFIER, "")
        # Comment-blocks
        self.StyleSetSpec(wx_stc.STC_P_COMMENTBLOCK, "fore:#990000,back:#C0C0C0,italic,size:%(size)d" % self.faces)
        # End of line where string is not closed
        self.StyleSetSpec(wx_stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % self.faces)

    #---get
    def getWord(self,whole=None):
        pos=self.GetCurrentPos()
        line = self.GetCurrentLine()
        linePos=self.PositionFromLine(line)
        txt = self.GetLine(line)
        start=self.WordStartPosition(pos,1)
        if whole:
            end=self.WordEndPosition(pos,1)
        else:
            end=pos
        return txt[start-linePos:end-linePos]

    def getWords(self,word=None,whole=None):
        if not word: word = self.getWord(whole=whole)
        if not word:
            return []
        else:
            return sm.unique([x for x in re.findall(r"\b" + word + r"\w+\b", self.GetText()) 
                if x.find(',')==-1 and x[0]!= ' '])
        
    def getWordObject(self,word=None,whole=None):
        if not word: word=self.getWord(whole=whole)
        try:
            obj = self.evaluate(word)
            return obj
        except:
            return None

    def getWordFileName(self,whole=None):
        wordList=self.getWord(whole=whole).split('.')
        wordList.append('')
        index=1
        n=len(wordList)
        while index<n:
            word='.'.join(wordList[:-index])
            try:
                fileName = self.getWordObject(word=word).__file__.replace('.pyc','.py').replace('.pyo','.py')
                if os.path.exists(fileName):
                    return fileName
            except:
                pass
            index+=1
        return '"%s.py"'%'.'.join(wordList[:-1])

    #---methods
    def assertEOL(self):
        self.ConvertEOLs(self.GetEOLMode())

    def autoComplete(self,object=0):
        word    = self.getWord()
        if object:
            self.AddText('.')
            word+='.'
        words   = self.getWords(word=word)
        if word[-1] == '.':
            try:
                obj = self.getWordObject(word[:-1])
                if obj:
                    for attr in dir(obj):
                        attr = '%s%s'%(word,attr)
                        if attr not in words: words.append(attr)
            except:
                pass
        if words:
            words.sort()
            try:
                self.AutoCompShow(len(word), " ".join(words))
            except:
                pass
            
    def evaluate(self,word):
        if word in self.namespace.keys():return self.namespace[word]
        try:
            self.namespace[word]=eval(word,self.namespace)
            return self.namespace[word]
        except:
            try:
                self.get('AutoCompleteIgnore').index(word)
                return None
            except:
                 try:
                    mod= __import__(word)
                    components = word.split('.')
                    for comp in components[1:]:
                        mod = getattr(mod, comp)
                    self.namespace[word]=mod
                    return self.namespace[word]
                 except:
                    return None
                    
    def needsIndent(self,txt):
        " tests if a line needs extra indenting, ie if, while, def, etc "
        # find the first token
        stripped = txt.split('#')[0].rstrip()
        l = stripped.lstrip().split(" ")[0]
        # remove trailing : on token
        if len(l) > 0:
            if l[-1] == ":":
                l = l[:-1]
        # control flow keywords
        if l in ["for","if", "else", "def","class","elif", "try","except","finally","while"] and stripped[-1] == ':':
            return True
        else:
            return False



class PythonViewSTC(PythonBaseSTC):
    """Mutation for dynamic class"""
    def __init__(self,parent, child = None, *args,**kwds):
        PythonBaseSTC.__init__(self,parent,*args,**kwds)
        self.dyn_sash = parent
        self.child    = child
        self._args = args
        self._kwds = kwds
        self.SetupScrollBars()
        wx_gizmos.EVT_DYNAMIC_SASH_SPLIT(self,-1,self.OnSplit)
        wx_gizmos.EVT_DYNAMIC_SASH_UNIFY(self,-1,self.OnUnify)
        wx.EVT_SET_FOCUS(self,self.OnSetFocus)
        self.SetScrollbar(wx.HORIZONTAL, 0, 0, 0)
        self.SetScrollbar(wx.VERTICAL, 0, 0, 0)
##        eventManager.Register(self.OnSplit,wx_gizmos.EVT_DYNAMIC_SASH_SPLIT,self)
##        eventManager.Register(self.OnUnify,wx_gizmos.EVT_DYNAMIC_SASH_UNIFY,self)
        
    def SetupScrollBars(self):
        # hook the scrollbars provided by the wxDynamicSashWindow
        # to this view
        v_bar = self.dyn_sash.GetVScrollBar(self)
        h_bar = self.dyn_sash.GetHScrollBar(self)
        wx.EVT_SCROLL(v_bar,self.OnSBScroll)
        wx.EVT_SCROLL(h_bar,self.OnSBScroll)
        wx.EVT_SET_FOCUS(v_bar, self.OnSBFocus)
        wx.EVT_SET_FOCUS(h_bar, self.OnSBFocus)
##        eventManager.Register(self.OnSBScroll, wx.EVT_SCROLL, v_bar)
##        eventManager.Register(self.OnSBScroll, wx.EVT_SCROLL, h_bar)
##        eventManager.Register(self.OnSBFocus,  wx.EVT_SET_FOCUS, v_bar)
##        eventManager.Register(self.OnSBFocus,  wx.EVT_SET_FOCUS, h_bar)

        # And set the wxStyledText to use these scrollbars instead
        # of its built-in ones.
        self.SetVScrollBar(v_bar)
        self.SetHScrollBar(h_bar)
        
    def OnSetFocus(self,event):
        self.child.source = self
        event.Skip()
        
    def OnSplit(self, evt):
        newview = PythonViewSTC(self.dyn_sash, child = self.child, *self._args, **self._kwds)
        newview.SetDocPointer(self.GetDocPointer())     # use the same document
        self.SetupScrollBars()

    def OnUnify(self, evt):
        self.SetupScrollBars()
        children = self.dyn_sash.GetChildren()[-1].GetChildren()
        while children[-1].__class__!=PythonViewSTC:
            children = children[-1].GetChildren()
        source = self.child.source = self.dyn_sash.view = children[-1]

    def OnSBScroll(self, evt):
        # redirect the scroll events from the dyn_sash's scrollbars to the STC
        self.GetEventHandler().ProcessEvent(evt)

    def OnSBFocus(self, evt):
        # when the scrollbar gets the focus move it back to the STC
        self.SetFocus()

class PythonSashSTC(wx_gizmos.DynamicSashWindow):
    def __init__(self,parent,*args,**kwds):
        wx_gizmos.DynamicSashWindow.__init__(self, parent,-1, style =  wx.CLIP_CHILDREN | wx.FULL_REPAINT_ON_RESIZE
                                  #| wxDS_MANAGE_SCROLLBARS
                                  #| wxDS_DRAG_CORNER
                                  )
        self.parent = parent
        self.view = PythonViewSTC(parent=self, id=-1, child = parent, *args, **kwds)
        #print dir(self)

if wx.Platform == "__WXMAC__":
    #The dynamic sash currently fails on the Mac. The problem is being looked into...
    PythonSTC = PythonBaseSTC
else:
    PythonSTC = PythonBaseSTC#PythonSashSTC
    
#-------------------------------------------------------------------------------

def getargspec(func):
    """Get argument specifications"""
    try:
        func=func.im_func
    except:
        pass
    try:
        return inspect.formatargspec(*inspect.getargspec(func))+'\n\n'
    except:
        pass
    try:
        return inspect.formatargvalues(*inspect.getargvalues(func))+'\n\n'
    except:
        return ''