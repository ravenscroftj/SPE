# --------------------------------------------------------------------------- #
# NOTEBOOKCTRL Control wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana, @ 11 Nov 2005
# Latest Revision: 11 Nov 2005, 21.50 CET
#
#
# TODO List/Caveats
#
# 1. Ay Idea?
#
# For All Kind Of Problems, Requests Of Enhancements And Bug Reports, Please
# Write To Me At:
#
# andrea.gavana@agip.it
# andrea_gavan@tin.it
#
# Or, Obviously, To The wxPython Mailing List!!!
#
#
# End Of Comments
# --------------------------------------------------------------------------- #


"""
Description:

NotebookCtrl Mimics The Behavior Of wx.Notebook, And Most Of Its Functionalities
Are Implemented In NotebookCtrl. However, NotebookCtrl Has A Lot Of Options That
wx.Notebook Does Not Have, And It Is Therefore Quite Customizable.
wx.Notebook Styles Not Implemented in NotebookCtrl Are:

- wx.NB_LEFT
- wx.NB_RIGHT
- wx.NB_MULTILINE (But NotebookCtrl Has A SpinButton To Navigate Through Tabs).

Supported Customizations For NotebookCtrl Include:

- Setting Individual Tab Font And Text Colour;
- Images On Tabs (Line wx.Notebook);
- Setting Individual Tab Colours;
- Disabling/Enabling Individual Tabs (Also Visually Effective);
- Drawing Of A Small Closing "X" At The Right Of Every Tab, That Enable The User
  To Close A Tab With A Mouse Click (Like eMule Tab Style);
- Enabling Highlighted Tabs On Selection;
- Drawing Focus Indicator In Each Tab (Like wx.Notebook);
- Ctrl-Tab Keyboard Navigation Between Pages;
- Tab With Animated Icons (Animation On Tabs);
- Drag And Drop Tabs In NotebookCtrl;
- ToolTips On Individual Tabs, With Customizable ToolTip Time Popup And ToolTip
  Window Size For Individual Tabs.


Usage:

NotebookCtrl Construction Is Quite Similar To wx.Notebook:

NotebookCtrl.__init__(self, parent, id, pos=wx.DefaultPosition,
                      size=wx.DefaultSize, style=NotebookCtrlStyle)

See NotebookCtrl __init__() Method For The Definition Of Non Standard (Non
wxPython) Parameters.

NotebookCtrl Control Is Freeware And Distributed Under The wxPython License. 

Latest Revision: Andrea Gavana @ 11 Nov 2005, 21.50 CET

"""


#----------------------------------------------------------------------
# Beginning Of NOTEBOOKCTRL wxPython Code
#----------------------------------------------------------------------

import wx
import textwrap
import cStringIO, zlib
from wx.lib.gestures import MouseGestures

# HitTest Results 
NC_HITTEST_NOWHERE = 0   # Not On Tab 
NC_HITTEST_ONICON  = 1   # On Icon 
NC_HITTEST_ONLABEL = 2   # On Label 
NC_HITTEST_ONITEM  = 4   # Generic, On Item
NC_HITTEST_ONX = 8       # On Small Square On Every Page

# NotebookCtrl Styles
# NotebookCtrl Placed On Top (Default)
NC_TOP = 1
# NotebookCtrl Placed At The Bottom
NC_BOTTOM = 2
# NotebookCtrl With Fixed Width Tabs
NC_FIXED_WIDTH = 4

NC_DEFAULT_STYLE = NC_TOP | wx.NO_BORDER
# Also wx.STATIC_BORDER Is Supported

# NotebookoCtrl Events:
# wxEVT_NOTEBOOKCTRL_PAGE_CHANGED: Event Fired When You Switch Page;
# wxEVT_NOTEBOOKCTRL_PAGE_CHANGING: Event Fired When You Are About To Switch
# Pages, But You Can Still "Veto" The Page Changing By Avoiding To Call
# event.Skip() In Your Event Handler;
# wxEVT_NOTEBOOKCTRL_PAGE_CLOSING: Event Fired When A Page Is Closing, But
# You Can Still "Veto" The Page Changing By Avoiding To Call event.Skip()
# In Your Event Handler.
wxEVT_NOTEBOOKCTRL_PAGE_CHANGED = wx.NewEventType()
wxEVT_NOTEBOOKCTRL_PAGE_CHANGING = wx.NewEventType()
wxEVT_NOTEBOOKCTRL_PAGE_CLOSING = wx.NewEventType()

#-----------------------------------#
#        NotebookCtrlEvent
#-----------------------------------#

EVT_NOTEBOOKCTRL_PAGE_CHANGED = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_CHANGED, 1)
EVT_NOTEBOOKCTRL_PAGE_CHANGING = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_CHANGING, 1)
EVT_NOTEBOOKCTRL_PAGE_CLOSING = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_CLOSING, 1)

# ---------------------------------------------------------------------------- #
# Class NotebookCtrlEvent
# ---------------------------------------------------------------------------- #

class NotebookCtrlEvent(wx.PyCommandEvent):
    """
    This Events Will Be Sent When A EVT_NOTEBOOKCTRL_PAGE_CHANGED,
    EVT_NOTEBOOKCTRL_PAGE_CHANGING And EVT_NOTEBOOKCTRL_PAGE_CLOSING Is Mapped In
    The Parent.
    """
    
    def __init__(self, eventType, id=1, nSel=-1, nOldSel=-1):
        """ Default Class Constructor. """
        
        wx.PyCommandEvent.__init__(self, eventType, id)
        self._eventType = eventType


    def SetSelection(self, nSel):
        """ Sets Event Position. """
        
        self._selection = nSel
        

    def SetOldSelection(self, nOldSel):
        """ Sets Old Event Position. """
        
        self._oldselection = nOldSel


    def GetSelection(self):
        """ Returns Event Position. """
        
        return self._selection
        

    def GetOldSelection(self):
        """ Returns Old Event Position """
        
        return self._oldselection


# ---------------------------------------------------------------------------- #
# Class TabbedPage
# This Is Just A Container Class That Initialize All The Default Settings For
# Every Tab.
# ---------------------------------------------------------------------------- #

class TabbedPage:

    def __init__(self, text="", image=-1):
        """ Default Class Constructor. """
        
        self._text = text
        self._image = image
        self._font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self._secondaryfont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self._pagetextcolour = wx.BLACK
        self._pagecolour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE)
        self._enable = True
        self._animationimages = []
        self._tooltip = ""
        self._tooltiptime = 500
        self._winsize = 150
    

# ---------------------------------------------------------------------------- #
# Class NotebookSpinButton
# This SpinButton Is Created/Shown Only When The Total Tabs Size Exceed The
# Client Size, Allowing The User To Navigate Between Tabs By Clicking On The
# SpinButton. It Is Very Similar To The wx.Notebook SpinButton
# ---------------------------------------------------------------------------- #

class NotebookSpinButton(wx.SpinButton):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.SP_HORIZONTAL):
        """ Default Class Constructor. """
        
        wx.SpinButton.__init__(self, parent, id, pos, size, style)        
        self._nb = parent
        self._oldvalue = 0
        self.Bind(wx.EVT_SPIN, self.OnSpin)


    def OnSpin(self, event):
        """ Handles The User's Clicks On The SpinButton. """

        if type(event) != type(1):
            pos = event.GetPosition()
        else:
            pos = event
            
        if pos < 0:
            self.SetValue(0)
            return

        if type(event) != type(1):
            self.SetValue(pos)

        if self._nb.IsLastVisible() and self._oldvalue < pos:
            self.SetValue(self._oldvalue)
            return

        self._oldvalue = pos
        
        self._nb.Refresh()
                

# ---------------------------------------------------------------------------- #
# Class TabCtrl
# This Class Handles The Drawing Of Every Tab In The NotebookCtrl, And Also
# All Settings/Methods For Every Tab.
# ---------------------------------------------------------------------------- #

class TabCtrl(wx.PyControl):

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=NC_DEFAULT_STYLE,
                 validator=wx.DefaultValidator, name="TabCtrl"):
        """
        Default Class Constructor.
        Used Internally. Do Not Call It Explicitely!
        """        

        wx.PyControl.__init__(self, parent, id, pos, size, wx.NO_BORDER | wx.WANTS_CHARS,
                              validator, name)

        # Set All The Default Parameters For TabCtrl        
        self._selection = -1
        self._imglist = 0
        self._style = style
        self._pages = []
        self._enabledpages = []

        self._padding = wx.Point(8, 5)
        self._spacetabs = 2
        self._xrect = wx.Rect()
        self._xrefreshed = False
        self._disabledcolour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_GRAYTEXT)
        
        self._hover = False
        self._parent = parent
        self._firsttime = True
        self._somethingchanged = True
        self._isdragging = False
        self._tabID = -1
        self._enabledragging = False
        self._highlight = False
        self._usefocus = True

        self._insidetab = -1        
        self._showtooltip = False
        self._istooltipshown = False
        self._tipwindow = None
        self._tiptimer = wx.PyTimer(self.OnShowToolTip)
        self._xvideo = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
        self._yvideo = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)
        
        self._timers = []
        
        self._dragcursor = wx.StockCursor(wx.CURSOR_HAND)

        self._drawx = False
        self._drawxstyle = 1

        self.SetDefaultPage()        
        
        self.SetBestSize((-1, 28))

        self._borderpen = wx.Pen(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNSHADOW)) 
        self._highlightpen = wx.Pen(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))        
        self._shadowpen = wx.Pen(wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DDKSHADOW), 2)
        self._shadowpen.SetCap(wx.CAP_BUTT)
        self._highlightpen.SetCap(wx.CAP_BUTT)
        self._selectionpen = wx.Pen(wx.Colour(255, 180, 0), 2)

        if wx.Platform == "__WXMAC__":
            self._focusindpen = wx.Pen(wx.BLACK, 1, wx.SOLID)
        else:
            self._focusindpen = wx.Pen(wx.BLACK, 1, wx.USER_DASH)
            self._focusindpen.SetDashes([1,1])
            self._focusindpen.SetCap(wx.CAP_BUTT)

        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)

        self.Bind(wx.EVT_TIMER, self.AnimateTab)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        

    def OnKeyDown(self, event):
        """
        Handles The wx.EVT_KEY_DOWN Event For TabCtrl. This Is Only Processed If
        The User Navigate Through Tabs With Ctrl-Tab Keyboard Navigation.
        """

        if event.GetKeyCode() == wx.WXK_TAB:
            if event.ControlDown():
                sel = self.GetSelection()
                if sel == self.GetPageCount() - 1:
                    sel = 0
                else:
                    sel = sel + 1

                while not self.IsPageEnabled(sel):
                    sel = sel + 1
                    if sel == self.GetPageCount() - 1:
                        sel = 0
                        
                self._parent.SetSelection(sel)

        event.Skip()
    

    def AddPage(self, text, select=False, img=-1):
        """
        Add A Page To The Notebook, With Following Parameters:
        - text: The Tab Text;
        - select: Whether The Page Should Be Selected Or Not;
        - img: Specifies The Optional Image Index For The New Page.
        """

        self._pages.append(TabbedPage(text, img))
        self._somethingchanged = True
        
        self._firsttime = True
        self._timers.append(wx.Timer(self))
        
        if select or self.GetSelection() == -1:
           self._selection = self.GetPageCount() - 1
        
        self.Refresh() 
 

    def InsertPage(self, nPage, text, select=False, img=-1):
        """
        Insert A Page Into The Notebook, With Following Parameters:
        - nPage: Specifies The Position For The New Page;
        - text: The Tab Text;
        - select: Whether The Page Should Be Selected Or Not;
        - img: Specifies The Optional Image Index For The New Page.
        """
        
        if nPage < 0 or (self.GetSelection() >= 0 and nPage >= self.GetPageCount()):
            raise "\nERROR: Invalid Notebook Page In InsertPage: (" + str(nPage) + ")"

        oldselection = self.GetSelection()
        
        self._pages.insert(nPage, TabbedPage(text, img))
        self._timers.insert(nPage, wx.Timer(self))
        
        self._somethingchanged = True
        self._firsttime = True
        
        if select or self.GetSelection() == -1:
            self._selection = nPage
            self.SetSelection(nPage)
        else:
            if nPage <= oldselection:
                self._selection = self._selection + 1
        
        self.Refresh()
            

    def DeleteAllPages(self):
        """ Deletes All NotebookCtrl Pages. """
        
        for tims in self._timers:
            if tims.IsRunning():
                tims.Stop()
                
            tims.Destroy()

        self._timers = []            
        self._pages = []
        self._selection = -1
        self._somethingchanged = True
        self._firsttime = True
        self.Refresh()
         

    def DeletePage(self, nPage):
        """ Deletes The Page nPage, And The Associated Window. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In DeletePage: (" + str(nPage) + ")"

        oldselection = self.GetSelection()

        self._pages.pop(nPage)
        
        if self._timers[nPage].IsRunning():
            self._timers[nPage].Stop()
            
        self._timers[nPage].Destroy()
    
        if nPage < self._selection:
            self._selection = self._selection - 1
        elif self._selection == nPage and self._selection == self.GetPageCount():
            self._selection = self._selection - 1
        else:
            self._selection = oldselection

        self._somethingchanged = True
        self._firsttime = True
        self.Refresh()
        self._firsttime = False
        self.Refresh()
         

    def SetSelection(self, nPage):
        """
        Sets The Current Tab Selection To The Given nPage. This Call Generates The
        EVT_NOTEBOOKCTRL_PAGE_CHANGING Event.
        """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetSelection: (" + str(nPage) + ")"
        
        oldselection = self._selection
        
        if nPage != self._selection:

            if not self.IsPageEnabled(nPage):
                return
            
            eventOut = NotebookCtrlEvent(wxEVT_NOTEBOOKCTRL_PAGE_CHANGING, self.GetId())
            eventOut.SetSelection(nPage)
            eventOut.SetOldSelection(self._selection)
            eventOut.SetEventObject(self)
        
            if not self.GetEventHandler().ProcessEvent(eventOut):

                self._firsttime = False
                # Program Allows The Page Change 
                self._selection = nPage
                eventOut.SetEventType(wxEVT_NOTEBOOKCTRL_PAGE_CHANGED) 
                eventOut.SetOldSelection(self._selection) 
                self.GetEventHandler().ProcessEvent(eventOut)
                
                if oldselection != -1:
                    self._parent.bsizer.Show(oldselection, False)

                self.EnsureVisible(self._selection)
                self._parent.bsizer.Show(self._selection, True)
                self._parent.bsizer.Layout()
                
                self.Refresh() 

                self._shown = nPage


    def EnsureVisible(self, selection):

        if self.GetPageCount() < 2:
            return

        if not self.HasSpinButton():
            return
                
        fullrect = self.GetClientSize()
        currect = self._tabrect[selection-self._firstvisible]

        spinval = self._spinbutton.GetValue()
        firstrect = self._initrect[spinval]
        xpos = currect.x
        xsize = currect.width
        torefresh = 0
        
        while xpos + xsize > fullrect[0] - self._spinbutton.GetSize()[0]:
            
            xpos = xpos - firstrect.width
            firstrect = self._initrect[spinval]
            spinval = spinval + 1
            self._spinbutton.OnSpin(spinval)
            self._spinbutton.SetValue(spinval)
            torefresh = 1

        if torefresh:
            self.Refresh()
        
                
    def GetPageCount(self):
        """ Returns The Number Of Pages In NotebookCtrl. """

        return len(self._pages)


    def GetSelection(self):
        """ Returns The Current Selection. """

        return self._selection


    def GetImageList(self):
        """ Returns The Image List Associated With The NotebookCtrl. """

        return self._imglist


    def SetImageList(self, imagelist):
        """ Associate An Image List To NotebookCtrl. """
        
        self._imglist = imagelist


    def AssignImageList(self, imagelist):
        """ Associate An Image List To NotebookCtrl. """

        self._imglist = imagelist
        

    def GetPadding(self):
        """ Returns The (Horizontal, Vertical) Padding Of The Text Inside Tabs. """

        return self._padding


    def SetPadding(self, padding):
        """ Sets The (Horizontal, Vertical) Padding Of The Text Inside Tabs. """
        
        self._padding = padding
        self._somethingchanged = True
        self._firsttime = True
        self.Refresh()
        

    def GetPageText(self, nPage):
        """ Returns The String For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageText: (" + str(nPage) + ")"
        
        return self._pages[nPage]._text 


    def SetPageText(self, nPage, text):
        """ Sets The String For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageText: (" + str(nPage) + ")"
        
        if self._pages[nPage]._text != text:
            self._pages[nPage]._text = text
            self._somethingchanged = True
            self._firsttime = True
            self.Refresh()
        
     
    def GetPageImage(self, nPage):
        """ Returns The Image Index For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageImage: (" + str(nPage) + ")"
        
        return self._pages[nPage]._image
     

    def SetPageImage(self, nPage, img):
        """ Sets The Image Index For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageImage: (" + str(nPage) + ")"
        
        if self._pages[nPage]._image != img:
            self._pages[nPage]._image = img
            self._somethingchanged = True
            self._firsttime = True
            self.Refresh()        


    def SetPageTextFont(self, nPage, font=None):
        """ Sets The Primary Font For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageTextFont: (" + str(nPage) + ")"
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)

        normalfont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        
        self._pages[nPage]._font = font

        if font == normalfont:
            self._parent.GetSizer().Layout()
            self._somethingchanged = True
            self._firsttime = True
            self.Refresh()
            return

        dc = wx.ClientDC(self)
        dc.SetFont(font)
        w1, h1 = dc.GetTextExtent("Aq")
        dc.SetFont(normalfont)
        wn, hn = dc.GetTextExtent("Aq")
        w2, h2 = (0, 0)
        
        if hasattr(self._pages[nPage], "_secondaryfont"):
            dc.SetFont(self._pages[nPage]._secondaryfont)
            w2, h2 = dc.GetTextExtent("Aq")

        h = max(h1, h2)

        if h < hn:
            self._somethingchanged = True
            self._firsttime = True
            self.Refresh()
            return

        if h + 2*self._padding.y < 24:
            newheight = 24
        else:
            newheight = h + 2*self._padding.y

        oldsize = self.GetSize()[1]

        if newheight < oldsize:
            newheight = oldsize
            
        self.SetBestSize((-1, newheight))
        self._parent.GetSizer().Layout()
        self._somethingchanged = True
        self._firsttime = True
        self.Refresh()

        
    def GetPageTextFont(self, nPage):
        """ Returns The Primary Font For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageTextFont: (" + str(nPage) + ")"
        
        return self._pages[nPage]._font


    def SetPageTextSecondaryFont(self, nPage, font=None):
        """ Sets The Secondary Font For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageTextSecondaryFont: (" + str(nPage) + ")"
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT) 

        normalfont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        
        self._pages[nPage]._secondaryfont = font

        if font == normalfont:
            self._somethingchanged = True
            self._firsttime = True
            self.Refresh()
            return

        dc = wx.ClientDC(self)
        dc.SetFont(font)
        w1, h1 = dc.GetTextExtent("Aq")
        dc.SetFont(normalfont)
        wn, hn = dc.GetTextExtent("Aq")
        w2, h2 = (0, 0)
        
        if hasattr(self._pages[nPage], "_font"):
            dc.SetFont(self._pages[nPage]._font)
            w2, h2 = dc.GetTextExtent("Aq")

        h = max(h1, h2)

        if h < hn:
            self._somethingchanged = True
            self._firsttime = True
            self.Refresh()
            return
        
        if h + 2*self._padding.y < 24:
            newheight = 24
        else:
            newheight = h + 2*self._padding.y

        oldsize = self.GetSize()[1]

        if newheight < oldsize:
            newheight = oldsize
            
        self.SetBestSize((-1, newheight))
        self._parent.GetSizer().Layout()
        
        self._somethingchanged = True
        self._firsttime = True
        self.Refresh()

        
    def GetPageTextSecondaryFont(self, nPage):
        """ Returns The Secondary Font For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageTextSecondaryFont: (" + str(nPage) + ")"
        
        return self._pages[nPage]._secondaryfont


    def SetPageTextColour(self, nPage, colour=None):
        """ Sets The Text Colour For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageTextColour: (" + str(nPage) + ")"
        
        if colour is None:
            colour = wx.BLACK

        self._pages[nPage]._pagetextcolour = colour
        self._somethingchanged = True
        self.Refresh()


    def GetPageTextColour(self, nPage):
        """ Returns The Text Colour For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageTextColour: (" + str(nPage) + ")"            

        return self._pages[nPage]._pagetextcolour


    def SetPageColour(self, nPage, colour=None):
        """ Sets The Tab Background Colour For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageColour: (" + str(nPage) + ")"
        
        if colour is None:
            colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE)

        self._pages[nPage]._pagecolour = colour
        self._somethingchanged = True
        self.Refresh()


    def GetPageColour(self, nPage):
        """ Returns The Tab Background Colour For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageColour: (" + str(nPage) + ")"            

        return self._pages[nPage]._pagecolour
    

    def EnablePage(self, nPage, enable=True):
        """ Enable/Disable The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In EnablePage: (" + str(nPage) + ")"

        self._pages[nPage]._enable = enable
        
        if not enable and self.GetSelection() == nPage:
            defpage = self.GetDefaultPage()
            if defpage < 0:
                self.AdvanceSelection()
            else:
                if defpage >= self.GetPageCount():
                    self.AdvanceSelection()
                else:
                    if defpage == nPage:
                        self.AdvanceSelection()
                    else:
                        self.SetSelection(defpage)
            
        self.Refresh()


    def IsPageEnabled(self, nPage):
        """ Returns Whether A Page Is Enabled Or Not. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In IsPageEnabled: (" + str(nPage) + ")"            

        return self._pages[nPage]._enable
    

    def SetHighlightSelection(self, highlight=True):
        """ Globally Enables/Disables Tab Highlighting On Tab Selection. """
        
        self._highlight = highlight
        self.Refresh()

        
    def GetHighlightSelection(self):
        """ Returns Globally Enable/Disable State For Tab Highlighting On Tab Selection. """

        return self._highlight


    def SetUseFocusIndicator(self, focus=True):
        """ Globally Enables/Disables Tab Focus Indicator. """
        
        self._usefocus = focus
        self.Refresh()


    def GetUseFocusIndicator(self):
        """ Returns Globally Enable/Disable State For Tab Focus Indicator. """
        
        return self._usefocus

    
    def SetPageToolTip(self, nPage, tooltip="", timer=500, winsize=150):
        """
        Sets A ToolTip For The Given Page nPage, With The Following Parameters:
        - nPage: The Given Page;
        - tooltip: The ToolTip String;
        - timer: The Timer After Which The Tip Window Is Popped Up;
        - winsize: The Maximum Width Of The Tip Window.
        """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageToolTip: (" + str(nPage) + ")"
        
        self._pages[nPage]._tooltip = tooltip
        self._pages[nPage]._tooltiptime = timer
        self._pages[nPage]._winsize = winsize


    def GetPageToolTip(self, nPage):
        """ Returns A Tuple With All Page ToolTip Parameters. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageToolTip: (" + str(nPage) + ")"        

        return self._pages[nPage]._tooltip, self._pages[nPage]._tooltiptime, \
               self._pages[nPage]._winsize


    def EnableToolTip(self, show=True):
        """ Globally Enables/Disables Tab ToolTips. """

        self._showtooltip = show
        if not show:
            if self._istooltipshown:
                self._tipwindow.Destroy()
                self._istooltipshown = False
                self.Refresh()
                
            if self._tiptimer.IsRunning():
                self._tiptimer.Stop()
    

    def AdvanceSelection(self, forward=True):
        """
        Cycles Through The Tabs. The Call To This Function Generates The
        EVT_NOTEBOOKCTRL_PAGE_CHANGING Event.
        """

        if self.GetPageCount() <= 1:
            return
        
        sel = self.GetSelection()
        count = 0
        
        if forward:          
            if sel == self.GetPageCount() - 1:
                sel = 0
            else:
                sel = sel + 1

            while not self.IsPageEnabled(sel):
                count = count + 1
                sel = sel + 1
                if sel == self.GetPageCount() - 1:
                    sel = 0
                    
                if count > self.GetPageCount() + 1:
                    return None

        else:
            if sel == 0:
                sel = self.GetPageCount() - 1
            else:
                sel = sel - 1

            while not self.IsPageEnabled(sel):
                count = count + 1
                sel = sel - 1
                if sel == 0:
                    sel = self.GetPageCount() - 1

                if count > self.GetPageCount() + 1:
                    return None
                    
        self._parent.SetSelection(sel)


    def SetDefaultPage(self, defaultpage=-1):
        """
        Sets The Default Page That Will Be Selected When An Active And Selected
        Tab Is Made Inactive.
        """
        
        if defaultpage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetDefaultPage: (" + str(defaultpage) + ")"
        
        self._defaultpage = defaultpage
        

    def GetDefaultPage(self):
        """ Returns The Default Page. """
        
        return self._defaultpage
    

    def UpdateSpinButton(self):
        """ Update The NotebookSpinButton. Used Internally. """

        count = self.GetPageCount()
        
        if count == 0:        
            return

        nbsize = []
        nbsize.append(self._initrect[-1][0] + self._initrect[-1][2])
        nbsize.append(self._initrect[-1][1] + self._initrect[-1][3])
        clsize = self.GetClientSize()
        
        if nbsize[0] > clsize[0]:
            if not hasattr(self, "_spinbutton"):
                self._spinbutton = NotebookSpinButton(self, pos=(10000,10000))
                self._spinbutton.SetValue(0)

            sbsize = self._spinbutton.GetSize()
            xpos = clsize[0] - sbsize[0]
            ypos = clsize[1] - sbsize[1]

            self._spinbutton.Move((xpos, ypos))
            self._spinbutton.Show()
            self._spinbutton.SetRange(0, count-1)
        
        else:

            if hasattr(self, "_spinbutton") and self._spinbutton.IsShown():
                self._spinbutton.Hide()
                self._spinbutton.SetValue(0)
            

    def HasSpinButton(self):
        """ Returns Wheter The NotebookSpinButton Exists And Is Shown. """

        return hasattr(self, "_spinbutton") and self._spinbutton.IsShown()


    def IsLastVisible(self):
        """ Returns Whether The Last Tab Is Visible Or Not. """

        if self.HasSpinButton():
            lastpos = self._tabrect[-1][0] + self._tabrect[-1][2]
            if lastpos < self._spinbutton.GetPosition()[0]:
                return True

        return False            
    

    def HitTest(self, point, flags=0):
        """
        Standard NotebookCtrl HitTest() Method. If Called With 2 Outputs, It
        Returns The Page Clicked (If Any) And One Of These Flags:

        NC_HITTEST_NOWHERE = 0   ==> Hit Not On Tab 
        NC_HITTEST_ONICON  = 1   ==> Hit On Icon 
        NC_HITTEST_ONLABEL = 2   ==> Hit On Label 
        NC_HITTEST_ONITEM  = 4   ==> Hit Generic, On Item
        NC_HITTEST_ONX = 8       ==> Hit On Closing "X" On Every Page
        """        

        mirror = self._style & NC_BOTTOM 
        drawx, dxstyle = self.GetDrawX()
        size = self.GetSize() 
        dc = wx.ClientDC(self)

        height = self._tabrect[0].height

        if flags:
            flags = wx.NB_HITTEST_NOWHERE

        if point.x <= 0 or point.x >= size.x:
            return wx.NOT_FOUND
     
        if not mirror and \
           (point.y <= size.y - height or point.y >= size.y):
            return wx.NOT_FOUND
        
        if mirror and (point.y <= 0 or point.y >= height + self._padding.y*2):
            return wx.NOT_FOUND 

        posx = 3
        maxwidth = max(self._maxtabwidths)
        
        if drawx:
            if dxstyle == 1:
                mins = min(self._padding.x, self._padding.y) + 1
                mins = min(mins, 6)

        if drawx:
            if dxstyle == 1:
                xxspace = self._padding.x/2
            else:
                xxspace = self._padding.x + self._maxtextheight
        else:
            xxspace = 0

        for ii in xrange(self._firstvisible, self.GetPageCount()):

            bmp = wx.NullBitmap
            
            thefont = self.GetPageTextFont(ii)
            dc.SetFont(thefont)
            width, pom = dc.GetTextExtent(self.GetPageText(ii))
           
            if self.GetPageImage(ii) >= 0:
                bmp = self.GetImageList().GetBitmap(ii)

            if self._style & NC_FIXED_WIDTH:
                width = maxwidth
                
            space = self._padding.x + self._incrtext[ii]
            
            if bmp.Ok():
                space = space + bmp.GetWidth() + self._padding.x 

            if point.x > posx and point.x < posx + width + space + self._padding.x + xxspace:
                if flags:
                    flags = NC_HITTEST_ONITEM 

                #onx attempt
                if drawx:
                    if dxstyle == 1:
                        if flags and point.x >= posx + width + self._padding.x + space - 1 and \
                             point.x <= posx + width + self._padding.x + space + mins:
                            
                            if point.y >= size.y - height - 1 \
                               and point.y <= size.y - height + mins + 1:
                                
                                flags = NC_HITTEST_ONX
                    else:
                        if flags and point.x >= posx + width + 2*self._padding.x + space - 1 and \
                             point.x <= posx + width + self._padding.x + space + xxspace - 1:
                            
                            if point.y >= size.y - height + self._padding.x \
                               and point.y <= size.y - height + 2*self._padding.x + 1:
                                
                                flags = NC_HITTEST_ONX

               #onicon attempt 
                if flags and bmp.Ok() and point.x >= posx + self._padding.x and \
                   point.x <= posx + bmp.GetWidth() + self._padding.x:

                    if not mirror and point.y >= size.y - height \
                       and point.y <= size.y - self._padding.y:
                        
                        flags = NC_HITTEST_ONICON
                        
                    elif mirror and point.y >= self._padding.y and \
                         point.y <= self._padding.y + bmp.GetHeight():
                        
                        flags = NC_HITTEST_ONICON 
              
               #onlabel attempt 
                elif flags and point.x >= posx + space and \
                     point.x <= posx + space + width:
                    
                    if not mirror and point.y >= size.y - height \
                       and point.y <= size.y - self._padding.y:
                        flags = NC_HITTEST_ONLABEL
                        
                    elif mirror and point.y >= self._padding.y and \
                         point.y <= height:
                        flags = NC_HITTEST_ONLABEL 
                        
                if flags:
                    return ii, flags
                else:
                    return ii
             
            posx = posx + width + space + self._padding.x + self._spacetabs + xxspace

        if flags:
            return wx.NOT_FOUND, flags
        else:
            return wx.NOT_FOUND


    def EnableDragAndDrop(self, enable=True):
        """ Globall Enables/Disables Tabs Drag And Drop. """
        
        self._enabledragging = enable


    def SetAnimationImages(self, nPage, imgarray):
        """
        Sets An Animation List Associated To The Given Page nPage, With The Following
        Parameters:
        - nPage: The Given Page;
        - imgarray: A List Of Image Indexes Of Images Inside The ImageList Associated
          To NotebookCtrl.
        """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetAnimationImages: (" + str(nPage) + ")"

        if not imgarray:
            raise "\nERROR: Invalid Image Array In SetAnimationImages: (" + repr(imgarray) + ")"

        if min(imgarray) < 0:
            raise "\nERROR: Invalid Image Array In SetAnimationImages: (Min(ImgArray) = " + \
                  str(min(imgarray)) + " < 0)"

        if max(imgarray) > self.GetImageList().GetImageCount() - 1:
            raise "\nERROR: Invalid Image Array In SetAnimationImages: (Max(ImgArray) = " + \
                  str(max(imgarray)) + " > " + str(self.GetImageList().GetImageCount()-1) + ")"
        
        self._pages[nPage]._animationimages = imgarray
        

    def GetAnimationImages(self, nPage):
        """ Returns The Animation Images List Associated To The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetAnimationImages: (" + str(nPage) + ")"

        return self._pages[nPage]._animationimages
    

    def AnimateTab(self, event):
        """ Called When The Refreshing Animation Timer Expires. Used Internally"""

        obj = event.GetEventObject()
        nPage = self._timers.index(obj)

        if not self.IsPageEnabled(nPage):
            return
        
        indx = self.GetPageImage(nPage)
        images = self.GetAnimationImages(nPage)
        myindx = images.index(indx)
        
        if indx == images[-1]:
            myindx = -1
        
        myindx = myindx + 1
            
        self.SetPageImage(nPage, images[myindx])


    def StartAnimation(self, nPage, timer=500):
        """ Starts The Animation On The Given Page, With Refreshing Time Rate "timer". """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In StartAnimation: (" + str(nPage) + ")"
        
        images = self.GetAnimationImages(nPage)

        if not images:
            raise "\nERROR: No Images Array Defined For Page: (" + str(nPage) + ")"

        if len(images) == 1:
            raise "\nERROR: Impossible To Animate Tab: " + str(nPage) + " With Only One Image"

        self._timers[nPage].Start(timer)


    def StopAnimation(self, nPage):
        """ Stops The Animation On The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In StopAnimation: (" + str(nPage) + ")"

        if self._timers[nPage].IsRunning():
            self._timers[nPage].Stop()


    def SetDrawX(self, drawx=True, style=1):
        """
        Globally Enables/Disables The Drawing Of A Closing "X" In The Tab. Depending
        On The "style" Parameter, You Will Have:
        - style = 1: Small "X" At The Top-Right Of The Tab;
        - style = 2: Bigger "X" In The Middle Vertical Of The Tab (Like Opera Notebook).
        """

        self._drawx = drawx
        self._drawxstyle = style
        self.Refresh()


    def GetDrawX(self):
        """
        Returns The Enable/Disable State Of Drawing Of A Small "X" At The Top-Right Of
        Every Page.
        """

        return self._drawx, self._drawxstyle
    

    def GetInsideTab(self, pt):
        """ Returns The Tab On Which The Mouse Is Hovering On. """

        count = 0
        
        for tabs in self._tabrect:
            if tabs.Inside(pt):
                return count
            
            count = count + 1

        return -1
    

    def GetInsideX(self, pt):
        """ Returns The Tab On Which The Mouse Is Hovering On The "X" Button. """
        
        count = 0
        
        for rects in self._xrect:
            if rects.Inside(pt):
                return count
            
            count = count + 1

        return -1


    def RedrawClosingX(self, pt, insidex, drawx, highlight=False):
        """ Redraw The Closing "X" Accordingly To The Mouse "Hovering" Position. """
        
        colour = self.GetPageTextColour(insidex)
        back_colour = self.GetBackgroundColour()
        
        if highlight:
            r = colour.Red()
            g = colour.Green()
            b = colour.Blue()

            hr, hg, hb = min(255,r+64), min(255,g+64), min(255,b+64)
                
            colour = wx.Colour(hr, hg, hb)
            back_colour = wx.WHITE
            
        dc = wx.ClientDC(self)
        xrect = self._xrect[insidex]
        
        if drawx == 1:
            # Emule Style
            dc.SetPen(wx.Pen(colour, 1))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangleRect(xrect)
        else:
            # Opera Style
            dc.SetPen(wx.Pen(colour, 1))
            dc.SetBrush(wx.Brush(colour))
            dc.DrawRoundedRectangleRect(xrect, 2)
            dc.SetPen(wx.Pen(back_colour, 2))
            dc.DrawLine(xrect[0]+2, xrect[1]+2, xrect[0]+xrect[2]-3, xrect[1]+xrect[3]-3)
            dc.DrawLine(xrect[0]+2, xrect[1]+xrect[3]-3, xrect[0]+xrect[2]-3, xrect[1]+2)
    

    def OnMouseMotion(self, event):
        """ Handles The wx.EVT_MOTION Event For TabCtrl. """

        pt = event.GetPosition()
        
        if self._enabledragging:
            
            if event.Dragging():
                
                tolerance = 2
                
                dx = abs(pt.x - self._dragstartpos.x)
                dy = abs(pt.y - self._dragstartpos.y)
                
                if dx <= tolerance and dy <= tolerance:
                    self.SetCursor(wx.STANDARD_CURSOR)
                    return

                self.SetCursor(self._dragcursor)
                self._isdragging = True

            else:

                self._isdragging = False
                self.SetCursor(wx.STANDARD_CURSOR)

        if not event.Dragging():
            drawx = self.GetDrawX()
            
            if drawx[0]:
                insidex = self.GetInsideX(pt)
                if insidex >= 0:
                    if self.IsPageEnabled(insidex):
                        self.RedrawClosingX(pt, insidex, drawx[1], True)
                        self._xrefreshed = False
                else:
                    if not self._xrefreshed:
                        insidetab = self.GetInsideTab(pt)
                        if insidetab >= 0:
                            if self.IsPageEnabled(insidetab):
                                self.RedrawClosingX(pt, insidetab, drawx[1])
                                self._xrefreshed = True

        if self._showtooltip:
            if not event.Dragging():
                if not event.LeftDown():
                    
                    oldinside = self._insidetab
                    self._insidetab = self.GetInsideTab(pt)

                    if self._insidetab >= 0:
                        if oldinside != self._insidetab:

                            if self._istooltipshown:
                                self._tipwindow.Destroy()
                                self._istooltipshown = False
                                self.Refresh()
                                
                            if self._tiptimer.IsRunning():
                                self._tiptimer.Stop()
                                
                            tip, ontime, winsize= self.GetPageToolTip(self._insidetab)
                            
                            if tip.strip() != "":
                                self._currenttip = tip
                                self._currentwinsize = winsize
                                self._tiptimer.Start(ontime, wx.TIMER_ONE_SHOT)
                            
                    else:
                        if self._istooltipshown:
                            self._tipwindow.Destroy()
                            self._istooltipshown = False
                            self.Refresh()

        self._mousepos = pt
        
        event.Skip()
        

    def OnShowToolTip(self):
        """ Called When The Timer For The ToolTip Expires. Used Internally. """

        self._istooltipshown = True
        self._tipwindow = TransientTipWindow(self, self._currenttip,
                                             self._currentwinsize)

        xsize, ysize = self._tipwindow.GetSize()
        xpos, ypos = self.ClientToScreen(self._mousepos)

        if xpos + xsize > self._xvideo - 10:
            if ypos + ysize > self._yvideo - 10:  # SW Tip Positioning
                posx = xpos - xsize
                posy = ypos - ysize
            else: # NE Tip Positioning
                posx = xpos - xsize
                posy = ypos
        else:
            if ypos + ysize > self._yvideo - 10:  # SE Tip Positioning
                posx = xpos + 10
                posy = ypos - ysize
            else: # NW Tip Positioning
                posx = xpos + 10
                posy = ypos
        
        self._tipwindow.SetPosition((posx, posy))
        self._tipwindow.Show()
        

    def OnMouseLeftDown(self, event):
        """ Handles The wx.EVT_LEFT_DOWN Event For TabCtrl. """
        
        pos = event.GetPosition()        
        page, flags = self.HitTest(pos, 1)
        self._dragstartpos = pos
        
        if page != wx.NOT_FOUND:

            if self.IsPageEnabled(page):
                if flags != NC_HITTEST_ONX:
                    self.SetSelection(page)
                    self._tabID = page
                else:
                    eventOut = NotebookCtrlEvent(wxEVT_NOTEBOOKCTRL_PAGE_CLOSING, self.GetId())
                    eventOut.SetOldSelection(self._selection)
                    eventOut.SetSelection(page)
                    eventOut.SetEventObject(self)
                    
                    if not self.GetEventHandler().ProcessEvent(eventOut):
                        self._parent.DeletePage(page)
                        self._parent.bsizer.Layout()
                        

        event.Skip()


    def OnMouseLeftUp(self, event):
        """ Handles The wx.EVT_LEFT_UP Event For TabCtrl. """

        if not self._enabledragging:
            event.Skip()
            return

        if not self._isdragging:
            self.SetCursor(wx.STANDARD_CURSOR)
            event.Skip()
            return

        id = self.HitTest(wx.Point(event.GetX(), event.GetY()))

        if id >= 0 and id != self._tabID: 

            self._parent.Freeze()
            
            text = self.GetPageText(self._tabID)
            image = self.GetPageImage(self._tabID)
            font1 = self.GetPageTextFont(self._tabID)
            font2 = self.GetPageTextSecondaryFont(self._tabID)
            fontcolour = self.GetPageTextColour(self._tabID)
            pagecolour = self.GetPageColour(self._tabID)
            enabled = self.IsPageEnabled(self._tabID)
            tooltip, ontime, winsize = self.GetPageToolTip(self._tabID)
            
            isanimated = 0
            if self._timers[self._tabID].IsRunning():
                isanimated = 1
                timer = self._timers[self._tabID].GetInterval()
                
            self.StopAnimation(self._tabID)
            animatedimages = self.GetAnimationImages(self._tabID)
            
            if not hasattr(self, "_pagerange"):                    
                pagerange = range(self.GetPageCount())
            else:
                pagerange = self._pagerange
                
            newrange = []
                    
            if id < self._tabID:

                for ii in xrange(id):
                    newrange.append(pagerange[ii])                

                newrange.append(pagerange[self._tabID])
                
                for ii in xrange(id, len(pagerange)):
                    if ii != self._tabID:
                        newrange.append(pagerange[ii])

            else:

                for ii in xrange(self._tabID):
                    newrange.append(pagerange[ii])
                    
                for ii in xrange(self._tabID+1, id+1):
                    newrange.append(pagerange[ii])

                newrange.append(pagerange[self._tabID])

                for ii in xrange(id+1, self.GetPageCount()):
                    newrange.append(pagerange[ii])

            newpages = []
            counter = self.GetPageCount() - 1
            
            for ii in xrange(self.GetPageCount()):  
                newpages.append(self._parent.GetPage(ii))
                self._parent.bsizer.Detach(counter-ii)

            cc = 0

            self._parent._notebookpages = []
            
            for jj in newrange:
                self._parent.bsizer.Add(newpages[jj], 1, wx.EXPAND | wx.ALL, 2)
                self._parent.bsizer.Show(cc, False)
                self._parent._notebookpages.append(newpages[jj])
                cc = cc + 1
                    
            self.DeletePage(self._tabID)
            
            if enabled:
                self.InsertPage(id, text, True, image)
            else:
                self.InsertPage(id, text, False, image)

            self.SetPageImage(id, image)
            self.SetPageText(id, text)
            self.SetPageTextFont(id, font1)
            self.SetPageTextSecondaryFont(id, font2)
            self.SetPageTextColour(id, fontcolour)
            self.SetPageColour(id, pagecolour)
            self.EnablePage(id, enabled)
            self.SetPageToolTip(id, tooltip, ontime, winsize)
            if isanimated and len(animatedimages) > 1:
                self.SetAnimationImages(id, animatedimages)
                self.StartAnimation(id, timer)
                
            if enabled:
                self._parent.bsizer.Show(id, True)
            else:
                sel = self.GetSelection()
                
                if sel == -1:
                    sel = 0
                self._parent.bsizer.Show(id, False)
                self._parent.SetSelection(sel)
                self._parent.bsizer.Show(sel, True)
                
            self._parent.bsizer.Layout()
            
            self._pagerange = newrange
            self._parent.Thaw()

        self._tabID = -1 
        self.SetCursor(wx.STANDARD_CURSOR)
        
        event.Skip()
        
        
    def OnSize(self, event=None):
        """ Handles The wx.EVT_SIZE Event For TabCtrl. """

        self.Refresh()

        if event is not None:
            event.Skip()
             

    def GetAllTextExtents(self, dc):
        """ Returns All Tabs Text Extents. Used Internally. """

        self._mintabwidths = []
        self._maxtabwidths = []
        self._mintabheights = []
        self._maxtabheights = []
        self._incrtext = []
        minheight = 0

        for ii in xrange(self.GetPageCount()):

            txts = self.GetPageText(ii)
            font1 = self.GetPageTextFont(ii)
            dc.SetFont(font1)
            w1, h1 = dc.GetTextExtent(txts)
            minheight = max(minheight, h1)
            self._mintabwidths.append(w1)
            self._mintabheights.append(h1)
            font2 = self.GetPageTextSecondaryFont(ii)
            dc.SetFont(font2)
            w2, h2 = dc.GetTextExtent(txts)
            minheight = max(minheight, h2)
            
            self._maxtabwidths.append(w2)
            self._maxtabheights.append(h2)
            self._incrtext.append(abs(self._mintabwidths[ii] - self._maxtabwidths[ii]))

        mh1 = max(self._mintabheights)
        font1 = self.GetPageTextFont(self._mintabheights.index(mh1))
        mh2 = max(self._maxtabheights)
        font2 = self.GetPageTextSecondaryFont(self._maxtabheights.index(mh2))

        mhend = max(mh1, mh2)
        
        if mhend == mh1:
            maxfont = font1
        else:
            maxfont = font2

        minheight = self.GetSize()[1]
        
        return  minheight, maxfont
                

    def OnPaint(self, event):
        """ Handles The wx.EVT_PAINT Event For TabCtrl. """
        
        dc = wx.BufferedPaintDC(self)
        size = self.GetSize()

        if self.GetPageCount() == 0:
            event.Skip()
            return
        
        back_colour = self.GetBackgroundColour()
        back_brush = wx.Brush(back_colour)
        back_pen = wx.Pen(back_colour)

        border_pen = self._borderpen
        highlightpen = self._highlightpen
        shadowpen = self._shadowpen

        mirror = self._style & NC_BOTTOM 
        fullborder = not (self._style & wx.NO_BORDER) 
        drawx, dxstyle = self.GetDrawX()
        highlight = self.GetHighlightSelection()
        usefocus = self.GetUseFocusIndicator()
        
        if highlight:
            selectionpen = self._selectionpen
            
        if drawx:
            if dxstyle == 1:
                x_pen = wx.BLACK_PEN
                mins = min(self._padding.x, self._padding.y) + 1
                mins = min(mins, 6)

        if usefocus:
            focusindpen = self._focusindpen
            
        dc.BeginDrawing() 

        #background 
        dc.SetBrush(back_brush)
        
        cancelpen = back_pen
        
        if fullborder:
            dc.SetPen(border_pen)
            dc.SetPen(highlightpen)
            dc.DrawRectangle(0, 0, size.x, size.y) 

        else:  
            dc.SetPen(back_pen)
            dc.DrawRectangle(0, 0, size.x, size.y) 
            dc.SetPen(highlightpen)
            dc.DrawLine(0, mirror and 0 or size.y-1, size.x, mirror and 0 or size.y-1) 
        
        selection = self.GetSelection()
        tabrect = []
        Xrect = []

        if self._somethingchanged:
            minheight, maxfont = self.GetAllTextExtents(dc)
            self._minheight = minheight
            self._maxfont = maxfont
        else:
            minheight = self._minheight
            maxfont = self._maxfont

        dc.SetFont(maxfont) 
        pom, height = dc.GetTextExtent("Aq")
        self._maxtextheight = height
        
        posx = 3
                    
        maxwidth = max(self._maxtabwidths)

        if self._firsttime:
            
            self._initrect = []
            self._firstvisible = 0
        else:
            if self.HasSpinButton():
                self._firstvisible = self._spinbutton.GetValue()
            else:
                self._firstvisible = 0

        lastvisible = self.GetPageCount()
        selfound = 0

        if drawx:
            if dxstyle == 1:
                xxspace = self._padding.x/2
            else:
                xxspace = self._padding.x + height
        else:
            xxspace = 0

        #and tabs 
        for ii in xrange(self._firstvisible, lastvisible):

            bmp = wx.NullBitmap
            text = self.GetPageText(ii)

            thefont = self.GetPageTextFont(ii)
            thebrush = wx.Brush(self.GetPageColour(ii))
            
            if self.IsPageEnabled(ii):
                thecolour = self.GetPageTextColour(ii)
            else:
                thecolour = self._disabledcolour
      
            dc.SetFont(thefont)
            dc.SetTextForeground(thecolour)
            dc.SetBrush(thebrush)
            
            width, pom = dc.GetTextExtent(text)

            incrtext = self._incrtext[ii]

            if self.GetPageImage(ii) >= 0:
                bmpindex = self.GetPageImage(ii)
                bmp = self._imglist.GetBitmap(bmpindex)

            bmpOk = bmp.Ok()          
            space = self._padding.x
            
            if bmpOk:
                space = space + self._padding.x + bmp.GetWidth()

            xpos = posx
            
            if self._style & NC_FIXED_WIDTH:
                xsize = maxwidth + space + self._padding.x + incrtext + xxspace
                newwidth = maxwidth
            else:
                newwidth = width
                xsize = width + space + self._padding.x + incrtext + xxspace
                
            xtextpos = posx + space + incrtext/2

            ypos = size.y - height - self._padding.y*2
            ytextpos = size.y - height - self._padding.y + abs(self._mintabheights[ii] - self._maxtabheights[ii])/2
            
            ysize = height + self._padding.y*2 + 3
            
            if ii == selection:
                selfound = 1
                xsize = xsize + self._spacetabs
                if ii > 0:
                    xpos = xpos - self._spacetabs
                    xsize = xsize + self._spacetabs
                else:
                    xtextpos = xtextpos + self._spacetabs/2.0 + 1
                
                ytextpos = ytextpos - 2
                ypos = ypos - 3                    
                ysize = ysize + 2
                
                xselpos = xpos
                yselpos = ypos
                xselsize = xsize
                yselsize = ysize
                
            if bmpOk:
                bmpxpos = posx                
            
            dc.SetPen(highlightpen)
            
            dc.DrawRoundedRectangle(xpos, ypos,
                                    xsize,
                                    ysize, 3)

            tabrect.append(wx.Rect(xpos, ypos, xsize, ysize))
                           
            if ii == selection:
                dc.SetPen(cancelpen)                    
                dc.DrawLine(xpos, ysize, xpos + xsize, ysize)
                
            dc.DrawText(text, xtextpos, ytextpos)
           
            dc.DrawLine(xpos, size.y-1, xpos + xsize, size.y-1)
            dc.SetPen(highlightpen)
            dc.DrawLine(xpos + 3, ypos, xpos + xsize - 3, ypos)
            dc.SetPen(shadowpen)
            dc.DrawLine(xpos + xsize, size.y-2, xpos+xsize, ypos+2)

            if bmpOk:
                bmpposx = posx + self._padding.x
                bmpposy = size.y - (height + 2*self._padding.y + bmp.GetHeight())/2 - 1

                if ii == selection:
                    bmpposx = bmpposx + 1
                    bmpposy = bmpposy - 1

                self._imglist.Draw(bmpindex, dc, bmpposx, bmpposy,
                                   wx.IMAGELIST_DRAW_TRANSPARENT, True)

            if ii == selection + 1 and ii != self.GetPageCount() and selfound:
                dc.SetPen(highlightpen)
                dc.DrawLine(xselpos + 3, yselpos, xselpos + xselsize - 3, yselpos)
                dc.SetPen(shadowpen)
                dc.DrawLine(xselpos + xselsize, size.y-2, xselpos+xselsize, yselpos+2)
                
            if highlight and selfound:
                dc.SetBrush(back_brush) 
                dc.SetPen(selectionpen)
                dc.DrawLine(xselpos + 1, yselpos, xselpos + xselsize - 2, yselpos)

            if ii == selection and usefocus:
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.SetPen(focusindpen)
                dc.DrawRoundedRectangle(xpos+self._padding.x/2, ypos+self._padding.y/2,
                                        xsize-self._padding.x,
                                        ysize-self._padding.y-2, 2)

            if drawx:
                if dxstyle == 1:
                    dc.SetPen(wx.Pen(thecolour, 1))
                    dc.SetBrush(wx.TRANSPARENT_BRUSH)
                    dc.DrawLine(xpos+xsize-mins-3, ypos+2, xpos+xsize-2, ypos+3+mins)
                    dc.DrawLine(xpos+xsize-mins-3, ypos+2+mins, xpos+xsize-2, ypos+1)
                    dc.DrawRectangle(xpos+xsize-mins-3, ypos+2, mins+1, mins+1)
                    Xrect.append(wx.Rect(xpos+xsize-mins-3, ypos+2, mins+1, mins+1))
                else:
                    dc.SetPen(wx.Pen(thecolour))
                    dc.SetBrush(wx.Brush(thecolour))
                    xxpos = xpos+xsize-height-self._padding.x/2
                    yypos = ypos+(ysize-height-self._padding.y/2)/2
                    dc.DrawRoundedRectangle(xxpos, yypos, height, height, 2)
                    dc.SetPen(wx.Pen(back_colour, 2))
                    dc.DrawLine(xxpos+2, yypos+2, xxpos+height-3, yypos+height-3)
                    dc.DrawLine(xxpos+2, yypos+height-3, xxpos+height-3, yypos+2)
                    Xrect.append(wx.Rect(xxpos, yypos, height, height))
                       
            posx = posx + newwidth + space + self._padding.x + self._spacetabs + incrtext + xxspace
            if self._firsttime:
                self._initrect.append(tabrect[ii])

        self._tabrect = tabrect
        self._xrect = Xrect

        if self._firsttime:
            self._firsttime = False
            
        self.UpdateSpinButton()

        dc.EndDrawing()
        
##        event.Skip()        


# ---------------------------------------------------------------------------- #
# Class NotebookCtrl
# This Is The Main Class Implementation
# ---------------------------------------------------------------------------- #

class NotebookCtrl(wx.Panel):

    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 notebookctrlstyle=NC_DEFAULT_STYLE):
        """
        Default Class Constructor. Non-Default Parameter Is:
        - notebookctrlstyle: Style For The NotebookCtrl, Which May Be:
          a) NC_TOP: NotebookCtrl Placed On Top (Default);
          b) NC_BOTTOM: NotebookCtrl Placed At The Bottom;
          c) NC_FIXED_WIDTH: All Tabs Have The Same Width;
          d) wx.NO_BORDER: Shows No Border For The Control (Default, Looks Better);
          e) wx.STATIC_BORDER: Shows A Static Border On The Control.
        """
        
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE |
                          wx.CLIP_CHILDREN)
        
        self.nb = TabCtrl(self, -1, pos, size, notebookctrlstyle)

        self._notebookpages = []

        if notebookctrlstyle & NC_TOP == 0 and notebookctrlstyle & NC_BOTTOM == 0:
            notebookctrlstyle = notebookctrlstyle | NC_TOP
            
        if notebookctrlstyle & wx.NO_BORDER == 0 and \
           notebookctrlstyle & wx.STATIC_BORDER == 0:
            notebookctrlstyle = notebookctrlstyle | wx.NO_BORDER
        
        self._style = notebookctrlstyle

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.bsizer = wx.BoxSizer(wx.HORIZONTAL)

        if notebookctrlstyle & NC_TOP:
            self.sizer.Add((0, 5), 0)                
            self.sizer.Add(self.nb, 0, wx.EXPAND)
            self.sizer.Add(self.bsizer, 1, wx.EXPAND)
        else:
            self.sizer.Add(self.bsizer, 1, wx.EXPAND)
            self.sizer.Add(self.nb, 0, wx.EXPAND)
            self.sizer.Add((0, 5), 0)

        self.SetSizer(self.sizer)
        self.sizer.Layout()  
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)


    def OnKeyDown(self, event):
        """
        Handles The wx.EVT_KEY_DOWN Event For NotebookCtrl. This Is Only Processed
        If The User Navigate Through Tabs With Ctrl-Tab Keyboard Navigation.
        """
        
        if event.GetKeyCode() == wx.WXK_TAB:
            if event.ControlDown():
                sel = self.GetSelection()
                if sel == self.GetPageCount() - 1:
                    sel = 0
                else:
                    sel = sel + 1

                while not self.IsPageEnabled(sel):
                    sel = sel + 1
                    if sel == self.GetPageCount() - 1:
                        sel = 0
                        
                self.SetSelection(sel)

        event.Skip()
        

    def OnMouseMotion(self, event):
        """ Handles The wx.EVT_MOTION Event For NotebookCtrl. """

        if self.nb._enabledragging:
            if event.Dragging():
                
                tolerance = 2
                pt = event.GetPosition()
                dx = abs(pt.x - self.nb._dragstartpos.x)
                dy = abs(pt.y - self.nb._dragstartpos.y)
                if dx <= tolerance and dy <= tolerance:
                    self.SetCursor(wx.STANDARD_CURSOR)
                    return

                self.SetCursor(self.nb._dragcursor)
                self.nb._isdragging = True

            else:

                self.nb._isdragging = False
                self.SetCursor(wx.STANDARD_CURSOR)

        if self.nb._showtooltip:
            if self.nb._istooltipshown:
                pt = event.GetPosition()
                self.nb._insidetab = self.nb.GetInsideTab(pt)
                if  self.nb._insidetab < 0:
                    self.nb._tipwindow.Destroy()
                    self.nb._istooltipshown = False
                    self.nb.Refresh()
                    
        event.Skip()
                    
    
    def AddPage(self, page, text, select=False, img=-1):
        """
        Add A Page To The Notebook, With Following Parameters:
        - page: Specifies The New Page;
        - text: The Tab Text;
        - select: Whether The Page Should Be Selected Or Not;
        - img: Specifies The Optional Image Index For The New Page.
        """
        
        self.Freeze()
        
        oldselection = self.nb.GetSelection()
        
        self.bsizer.Add(page, 1, wx.EXPAND | wx.ALL, 2)
                    
        self.nb.AddPage(text, select, img)
        self._notebookpages.append(page)

        if select:
            if oldselection >= 0:
               self.bsizer.Show(self.GetPage(oldselection), False)
               
            self.nb.SetSelection(self.GetPageCount()-1)
            self.bsizer.Layout()
        else:
            if oldselection >= 0:
                self.bsizer.Show(page, False)
            else:
                self.bsizer.Show(page, True)
                self.nb.SetSelection(self.GetPageCount()-1)
                self.bsizer.Layout()

        if self.GetPageCount() == 1:
            self.nb.Show(True)
            if self._style & NC_TOP:
                self.sizer.Show(0, True)
            else:
                self.sizer.Show(1, True)

            self.sizer.Layout()
            
        self.Thaw()
        

    def InsertPage(self, nPage, page, text, select=False, img=-1):
        """
        Insert A Page Into The Notebook, With Following Parameters:
        - page: Specifies The New Page;
        - nPage: Specifies The Position For The New Page;
        - text: The Tab Text;
        - select: Whether The Page Should Be Selected Or Not;
        - img: Specifies The Optional Image Index For The New Page.
        """
        
        if nPage < 0 or (self.GetSelection() >= 0 and nPage >= self.GetPageCount()):
            raise "\nERROR: Invalid Notebook Page In InsertPage: (" + str(nPage) + ")"

        self.Freeze()
        
        oldselection = self.nb.GetSelection()
            
        if oldselection >= 0:
            self.bsizer.Show(oldselection, False)
            self.bsizer.Layout()
        
        if oldselection >= nPage:
            oldselection = oldselection + 1
        
        self.nb.InsertPage(nPage, text, select, img)
        self.bsizer.Insert(nPage, page, 1, wx.EXPAND | wx.ALL, 2)
        self._notebookpages.insert(nPage, page)
        self.bsizer.Layout()

        for ii in xrange(self.GetPageCount()):
            self.bsizer.Show(ii, False)

        self.bsizer.Layout()
        
        if select:
            self.bsizer.Show(nPage, True)
            self.bsizer.Layout()
        else:
            if oldselection >= 0:
                self.bsizer.Show(oldselection, True)
                self.bsizer.Layout()
            else:
                self.bsizer.Show(nPage, True)

        self.bsizer.Layout()

        if self.GetPageCount() == 1:
            self.nb.Show(True)
            if self._style & NC_TOP:
                self.sizer.Show(0, True)
            else:
                self.sizer.Show(1, True)

            self.sizer.Layout()        
        
        self.Thaw()

        
    def GetPage(self, nPage):
        """ Returns The Window At The Given Position nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPage: (" + str(nPage) + ")"

        return self._notebookpages[nPage]
    

    def DeleteAllPages(self):
        """ Deletes All NotebookCtrl Pages. """

        self.Freeze()

        counter = self.GetPageCount() - 1        
        self.nb.DeleteAllPages()
        
        for ii in xrange(self.GetPageCount()):
            self.bsizer.Detach(counter-ii)
            panels = self.GetPage(counter-ii)
            panels.Destroy()

        self._notebookpages = []
        self.bsizer.Layout()
        self.nb._selection = -1

        self.nb.Show(False)
        if self._style & NC_TOP:
            self.sizer.Show(0, False)
        else:
            self.sizer.Show(1, False)

        self.sizer.Layout()            

        self.Thaw()
         

    def DeletePage(self, nPage):
        """ Deletes The Page nPage, And The Associated Window. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In DeletePage: (" + str(nPage) + ")"

        oldselection = self.GetSelection()
        
        self.Freeze()
        
        panel = self.GetPage(nPage)
        self.bsizer.Detach(nPage)
        
        panel.Destroy()
            
        self.bsizer.Layout()
        
        self._notebookpages.pop(nPage)
        self.nb.DeletePage(nPage)

        if self.GetPageCount() > 0:
            if oldselection == nPage:
                if self.GetSelection() > 0:
                    self.SetSelection(self.GetSelection()-1)
                else:
                    self.SetSelection(self.GetSelection())
                    self.bsizer.Show(self.GetSelection())
                    self.bsizer.Layout()
                
        if self.GetPageCount() == 0:
            self.nb.Show(False)
            if self._style & NC_TOP:
                self.sizer.Show(0, False)
            else:
                self.sizer.Show(1, False)

            self.sizer.Layout()      

        self.Thaw()


    def SetSelection(self, nPage):
        """
        Sets The Current Tab Selection To The Given nPage. This Call Generates The
        EVT_NOTEBOOKCTRL_PAGE_CHANGING Event.
        """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetSelection: (" + str(nPage) + ")"
        
        oldselection = self.GetSelection()
        
        if oldselection == nPage:
            return

        self.nb.SetSelection(nPage)
       

    def GetPageCount(self):
        """ Returns The Number Of Pages In NotebookCtrl. """

        return self.nb.GetPageCount()


    def GetSelection(self):
        """ Returns The Current Selection. """
        
        return self.nb.GetSelection()


    def GetImageList(self):
        """ Returns The Image List Associated With The NotebookCtrl. """
        
        return self.nb.GetImageList()


    def SetImageList(self, imagelist):
        """ Associate An Image List To NotebookCtrl. """

        self.nb.SetImageList(imagelist)


    def AssignImageList(self, imagelist):
        """ Associate An Image List To NotebookCtrl. """

        self.nb.AssignImageList(imagelist)
        

    def GetPadding(self):
        """ Returns The (Horizontal, Vertical) Padding Of The Text Inside Tabs. """

        return self.nb.GetPadding()


    def SetPadding(self, padding):
        """ Sets The (Horizontal, Vertical) Padding Of The Text Inside Tabs. """
        
        self.nb.SetPadding(padding)


    def SetUseFocusIndicator(self, focus=True):
        """ Globally Enables/Disables Tab Focus Indicator. """

        self.nb.SetUseFocusIndicator(focus)        


    def GetUseFocusIndicator(self):
        """ Returns Globally Enable/Disable State For Tab Focus Indicator. """

        return self.nb.GetUseFocusIndicator()
    

    def EnablePage(self, nPage, enable=True):
        """ Enable/Disable The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In EnablePage: (" + str(nPage) + ")"
        
        self.nb.EnablePage(nPage, enable)


    def IsPageEnabled(self, nPage):
        """ Returns Whether A Page Is Enabled Or Not. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In IsPageEnabled: (" + str(nPage) + ")"        

        return self.nb.IsPageEnabled(nPage)
    

    def SetHighlightSelection(self, highlight=True):
        """ Globally Enables/Disables Tab Highlighting On Tab Selection. """

        self.nb.SetHighlightSelection(highlight)

        
    def GetHighlightSelection(self):
        """ Returns Globally Enable/Disable State For Tab Highlighting On Tab Selection. """

        return self.nb.GetHighlightSelection()
    

    def SetAnimationImages(self, nPage, imgarray):
        """
        Sets An Animation List Associated To The Given Page nPage, With The Following
        Parameters:
        - nPage: The Given Page;
        - imgarray: A List Of Image Indexes Of Images Inside The ImageList Associated
          To NotebookCtrl.
        """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetAnimationImages: (" + str(nPage) + ")"

        if not imgarray:
            raise "\nERROR: Invalid Image Array In SetAnimationImages: (" + repr(imgarray) + ")"

        if min(imgarray) < 0:
            raise "\nERROR: Invalid Image Array In SetAnimationImages: (Min(ImgArray) = " + \
                  str(min(imgarray)) + " < 0)"

        if max(imgarray) > self.GetImageList().GetImageCount() - 1:
            raise "\nERROR: Invalid Image Array In SetAnimationImages: (Max(ImgArray) = " + \
                  str(max(imgarray)) + " > " + str(self.GetImageList().GetImageCount()-1) + ")"
        
        self.nb.SetAnimationImages(nPage, imgarray)
        

    def GetAnimationImages(self, nPage):
        """ Returns The Animation Images List Associated To The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetAnimationImages: (" + str(nPage) + ")"

        return self.nb.GetAnimationImages(nPage)
    

    def StartAnimation(self, nPage, timer=500):
        """ Starts The Animation On The Given Page nPage, With Refreshing Time Rate "timer". """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In StartAnimation: (" + str(nPage) + ")"
        
        self.nb.StartAnimation(nPage, timer)


    def StopAnimation(self, nPage):
        """ Stops The Animation On The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In StopAnimation: (" + str(nPage) + ")"

        self.nb.StopAnimation(nPage)


    def EnableDragAndDrop(self, enable=True):
        """ Globall Enables/Disables Tabs Drag And Drop. """

        self.nb.EnableDragAndDrop(enable)


    def SetDrawX(self, drawx=True, style=1):
        """
        Globally Enables/Disables The Drawing Of A Closing "X" In The Tab. Depending
        On The "style" Parameter, You Will Have:
        - style = 1: Small "X" At The Top-Right Of The Tab;
        - style = 2: Bigger "X" In The Middle Vertical Of The Tab (Like Opera Notebook).
        """

        self.nb.SetDrawX(drawx, style)


    def GetDrawX(self):
        """
        Returns The Enable/Disable State Of Drawing Of A Small "X" At The Top-Right Of
        Every Page.
        """

        return self.nb.GetDrawX()
    

    def SetPageToolTip(self, nPage, tooltip="", timer=500, winsize=150):
        """
        Sets A ToolTip For The Given Page nPage, With The Following Parameters:
        - nPage: The Given Page;
        - tooltip: The ToolTip String;
        - timer: The Timer After Which The Tip Window Is Popped Up;
        - winsize: The Maximum Width Of The Tip Window.
        """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageToolTip: (" + str(nPage) + ")"
        
        self.nb.SetPageToolTip(nPage, tooltip, timer, winsize)


    def GetPageToolTip(self, nPage):
        """ Returns A Tuple With All Page ToolTip Parameters. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageToolTip: (" + str(nPage) + ")"
        
        return self.nb.GetPageToolTip()


    def EnableToolTip(self, show=True):
        """ Globally Enables/Disables Tab ToolTips. """

        self.nb.EnableToolTip(show)        


    def AdvanceSelection(self, forward=True):
        """
        Cycles Through The Tabs. The Call To This Function Generates The
        EVT_NOTEBOOKCTRL_PAGE_CHANGING Event.
        """

        self.nb.AdvanceSelection(forward)

    
    def SetDefaultPage(self, defaultpage=-1):
        """
        Sets The Default Page That Will Be Selected When An Active And Selected
        Tab Is Made Inactive.
        """
        
        if defaultpage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetDefaultPage: (" + str(defaultpage) + ")"
        
        self.nb.SetDefaultPage(defaultpage)        


    def GetDefaultPage(self):
        """ Returns The Default Page. """
        
        return self.nb.GetDefaultPage()
        

    def GetPageText(self, nPage):
        """ Returns The String For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageText: (" + str(nPage) + ")"
        
        return self.nb.GetPageText()


    def SetPageText(self, nPage, text):
        """ Sets The String For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageText: (" + str(nPage) + ")"

        self.nb.SetPageText(nPage, text)
        
     
    def GetPageImage(self, nPage):
        """ Returns The Image Index For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageImage: (" + str(nPage) + ")"
        
        return self.nb.GetPageImage(nPage)
     

    def SetPageImage(self, nPage, img):
        """ Sets The Image Index For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageImage: (" + str(nPage) + ")"
        
        self.nb.SetPageImage(nPage, img) 
        

    def SetPageTextFont(self, nPage, font=None):
        """ Sets The Primary Font For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageTextFont: (" + str(nPage) + ")"
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)

        self.nb.SetPageTextFont(nPage, font)
        
        
    def GetPageTextFont(self, nPage):
        """ Returns The Primary Font For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageTextFont: (" + str(nPage) + ")"
        
        return self.nb.GetPageTextFont(nPage)


    def SetPageTextSecondaryFont(self, nPage, font=None):
        """ Sets The Secondary Font For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageTextSecondaryFont: (" + str(nPage) + ")"
        
        if font is None:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT) 

        self.nb.SetPageTextSecondaryFont(nPage, font)

        
    def GetPageTextSecondaryFont(self, nPage):
        """ Returns The Secondary Font For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageTextSecondaryFont: (" + str(nPage) + ")"
        
        return self.nb.GetPageTextSecondaryFont(nPage)


    def SetPageTextColour(self, nPage, colour=None):
        """ Sets The Text Colour For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageTextColour: (" + str(nPage) + ")"
        
        if colour is None:
            colour = wx.BLACK

        self.nb.SetPageTextColour(nPage, colour)


    def GetPageTextColour(self, nPage):
        """ Returns The Text Colour For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageTextColour: (" + str(nPage) + ")"            

        return self.nb.GetPageTextColour(nPage)


    def SetPageColour(self, nPage, colour=None):
        """ Sets The Tab Background Colour For The Given Page nPage. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPageColour: (" + str(nPage) + ")"
        
        if colour is None:
            colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE)

        self.nb.SetPageColour(nPage, colour)


    def GetPageColour(self, nPage):
        """ Returns The Tab Background Colour For The Given Page nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPageColour: (" + str(nPage) + ")"            

        return self.nb.GetPageColour(nPage)


    def HitTest(self, point, flags=0):
        """
        Standard NotebookCtrl HitTest() Method. If Called With 2 Outputs, It
        Returns The Page Clicked (If Any) And One Of These Flags:

        NC_HITTEST_NOWHERE = 0   ==> Hit Not On Tab 
        NC_HITTEST_ONICON  = 1   ==> Hit On Icon 
        NC_HITTEST_ONLABEL = 2   ==> Hit On Label 
        NC_HITTEST_ONITEM  = 4   ==> Hit Generic, On Item
        NC_HITTEST_ONX = 8       ==> Hit On Closing "X" On Every Page
        """
        
        return self.nb.HitTest(point, flags)

    
# ---------------------------------------------------------------------------- #
# Class TransientTipWindow
# Auxiliary Help Class. Used To Build The Tip Window.
# ---------------------------------------------------------------------------- #

class TransientTipWindow(wx.PopupWindow):
    
    def __init__(self, parent, tip, winsize):
        
        wx.PopupWindow.__init__(self, parent, flags=wx.SIMPLE_BORDER)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour(wx.Colour(255,255,230))

        # border from sides and top to text (in pixels)
        border = 5
        # how much space between text lines
        textPadding = 2
        max_len = len(tip)
        tw = winsize

        while 1:
            lines = textwrap.wrap(tip, max_len)

            for line in lines:
                w, h = self.GetTextExtent(line)
                if w > tw - border * 2:
                    max_len = max_len - 1
                    break
            else:
                break

        sts = wx.StaticText(panel, -1, "\n".join(lines))
        sx, sy = sts.GetBestSize()
        sts.SetPosition((2, 2))
            
        panel.SetSize((sx+6, sy+6))
        self.SetSize(panel.GetSize())
        

    def ProcessLeftDown(self, evt):
        return False


    def OnDismiss(self):
        return False


