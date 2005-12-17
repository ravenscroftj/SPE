# --------------------------------------------------------------------------- #
# NOTEBOOKCTRL Control wxPython IMPLEMENTATION
# Python Code By:
#
# Andrea Gavana, @ 11 Nov 2005
# Latest Revision: 15 Dec 2005, 23.50 CET
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
- Drag And Drop Tabs In NotebookCtrl (Plus A Visual Arrow Effect To Indicate
  Dropping Position);
- Drag And Drop Event;
- ToolTips On Individual Tabs, With Customizable ToolTip Time Popup And ToolTip
  Window Size For Individual Tabs;
- Possibility To Hide The TabCtrl There Is Only One Tab (Thus Maximizing The
  Corresponding Window);
- Possibility To Convert The Tab Image Into A Close Button While Mouse Is Hovering
  On The Tab Image;
- Popup Menus On Tabs (Popup Menus Specific To Each Tab);
- Showing Pages In "Column/Row Mode", Which Means That All Pages Will Be Shown In
  NotebookCtrl While The Tabs Are Hidden. They Can Be Shown In Columns (Default)
  Or In Rows;
- Possibility To Hide Tabs On User Request, Thus Showing Only The Current Panel;
- Multiple Tabs Selection (Hold Ctrl Key Down And Left Mouse Click), Useful When
  You Use The Show All The Panels In Columns/Rows. In This Case, Only The Selected
  Tabs Are Shown In Columns/Rows;
- Events For Mouse Events (Left Double Click, Middle Click, Right Click);
- Possibility To Reparent A NotebookCtrl Page To A Freshly Created Frame As A Simple
  Panel Or To A New NotebookCtrl Created Inside That New Frame.
- Possibility To Add A Custom Panel To Show A Logo Or HTML Information Or Whatever
  You Like When There Are No Tabs In NotebookCtrl.

Usage:

NotebookCtrl Construction Is Quite Similar To wx.Notebook:

NotebookCtrl.__init__(self, parent, id, pos=wx.DefaultPosition,
                      size=wx.DefaultSize, style=style, sizer=nbsizer)

See NotebookCtrl __init__() Method For The Definition Of Non Standard (Non
wxPython) Parameters.

NotebookCtrl Control Is Freeware And Distributed Under The wxPython License. 

Latest Revision: Andrea Gavana @ 15 Dec 2005, 23.50 CET

"""


#----------------------------------------------------------------------
# Beginning Of NOTEBOOKCTRL wxPython Code
#----------------------------------------------------------------------

import wx
import textwrap
import cStringIO, zlib

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

# Patch To Make NotebookCtrl Working Also On MacOS: Thanks To Stani ;-)
if wx.Platform == '__WXMAC__':
    DEFAULT_SIZE = wx.Size(26, 26)
else:
    DEFAULT_SIZE = wx.DefaultSize

# Themes On Mac... This May Slow Down The Paint Event If You Turn It On!
NC_MAC_LIGHT = (240, 236)
NC_MAC_DARK = (232, 228)

# NotebookoCtrl Events:
# wxEVT_NOTEBOOKCTRL_PAGE_CHANGED: Event Fired When You Switch Page;
# wxEVT_NOTEBOOKCTRL_PAGE_CHANGING: Event Fired When You Are About To Switch
# Pages, But You Can Still "Veto" The Page Changing By Avoiding To Call
# event.Skip() In Your Event Handler;
# wxEVT_NOTEBOOKCTRL_PAGE_CLOSING: Event Fired When A Page Is Closing, But
# You Can Still "Veto" The Page Changing By Avoiding To Call event.Skip()
# In Your Event Handler;
# wxEVT_NOTEBOOKCTRL_PAGE_DND: Event Fired When A Drag And Drop Action On
# Tabs Ends.
wxEVT_NOTEBOOKCTRL_PAGE_CHANGED = wx.NewEventType()
wxEVT_NOTEBOOKCTRL_PAGE_CHANGING = wx.NewEventType()
wxEVT_NOTEBOOKCTRL_PAGE_CLOSING = wx.NewEventType()
wxEVT_NOTEBOOKCTRL_PAGE_DND = wx.NewEventType()
wxEVT_NOTEBOOKCTRL_PAGE_DCLICK = wx.NewEventType()
wxEVT_NOTEBOOKCTRL_PAGE_RIGHT = wx.NewEventType()
wxEVT_NOTEBOOKCTRL_PAGE_MIDDLE = wx.NewEventType()

#-----------------------------------#
#        NotebookCtrlEvent
#-----------------------------------#

EVT_NOTEBOOKCTRL_PAGE_CHANGED = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_CHANGED, 1)
EVT_NOTEBOOKCTRL_PAGE_CHANGING = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_CHANGING, 1)
EVT_NOTEBOOKCTRL_PAGE_CLOSING = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_CLOSING, 1)
EVT_NOTEBOOKCTRL_PAGE_DND = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_DND, 1)
EVT_NOTEBOOKCTRL_PAGE_DCLICK = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_DCLICK, 1)
EVT_NOTEBOOKCTRL_PAGE_RIGHT = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_RIGHT, 1)
EVT_NOTEBOOKCTRL_PAGE_MIDDLE = wx.PyEventBinder(wxEVT_NOTEBOOKCTRL_PAGE_MIDDLE, 1)


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
        """ Sets Event Selection. """
        
        self._selection = nSel
        

    def SetOldSelection(self, nOldSel):
        """ Sets Old Event Selection. """
        
        self._oldselection = nOldSel


    def GetSelection(self):
        """ Returns Event Selection. """
        
        return self._selection
        

    def GetOldSelection(self):
        """ Returns Old Event Selection """
        
        return self._oldselection


    def SetOldPosition(self, pos):
        """ Sets Old Event Position. """
        
        self._oldposition = pos        


    def SetNewPosition(self, pos):
        """ Sets New Event Position. """
        
        self._newposition = pos
        

    def GetOldPosition(self):
        """ Returns Old Event Position. """

        return self._oldposition


    def GetNewPosition(self):
        """ Returns New Event Position. """

        return self._newposition    
    

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
        self._menu = None
    

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
                 size=DEFAULT_SIZE, style=NC_DEFAULT_STYLE,
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
        self._imageconverted = False
        self._convertimage = False
        self._disabledcolour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_GRAYTEXT)
        
        self._hover = False
        self._parent = parent
        self._firsttime = True
        self._somethingchanged = True
        self._isdragging = False
        self._tabID = -1
        self._enabledragging = False
        self._olddragpos = -1
        self._isleaving = False
        self._highlight = False
        self._usefocus = True
        self._hideonsingletab = False

        self._insidetab = -1        
        self._showtooltip = False
        self._istooltipshown = False
        self._tipwindow = None
        self._tiptimer = wx.PyTimer(self.OnShowToolTip)
        self._xvideo = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
        self._yvideo = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)

        self._selectedtabs = []        

        self._timers = []
        
        self._dragcursor = wx.StockCursor(wx.CURSOR_HAND)

        self._drawx = False
        self._drawxstyle = 1

        self._pmenu = None

        if wx.Platform == "__WXMAC__":
            self._macstyle = 1
        else:
            self._macstyle = 0
        
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
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseLeftDClick)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.Bind(wx.EVT_RIGHT_UP, self.OnMouseRightUp)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)
        self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMouseMiddleDown)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x: None)

        self.Bind(wx.EVT_TIMER, self.AnimateTab)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)


    def OnLeaveWindow(self, event):

        if self._enabledragging:
            if self._isdragging:
                self._isleaving = True
                self.Refresh()

        if self._istooltipshown:
            self._tipwindow.Destroy()
            self._istooltipshown = False
            self.Refresh()
                
        event.Skip()
        

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
         

    def DeletePage(self, nPage, oncontinue=True):
        """ Deletes The Page nPage, And The Associated Window. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In DeletePage: (" + str(nPage) + ")"

        oldselection = self.GetSelection()

        self._pages.pop(nPage)
        
        if self._timers[nPage].IsRunning():
            self._timers[nPage].Stop()
            
        self._timers[nPage].Destroy()

        if not oncontinue:
            self._somethingchanged = True
            self._firsttime = True
            self.Refresh()
            return
        
        if nPage < self._selection:
            self._selection = self._selection - 1
        elif self._selection == nPage and self._selection == self.GetPageCount():
            self._selection = self._selection - 1
        else:
            self._selection = oldselection

        self._somethingchanged = True
        self._firsttime = True
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


    def SetTabHeight(self, height=28):
        """ Sets The Tabs Height. """
        
        self.SetBestSize((-1, height))
        self._bestsize = height
        

    def SetControlBackgroundColour(self, colour=None):
        """ Sets The TabCtrl Background Colour (Behind The Tabs). """

        if colour is None:
            colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)
            
        self.SetBackgroundColour(colour)
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
        
        if show:
            try:
                wx.PopupWindow(self)
                self.TransientTipWindow = TransientTipWindow
            
            except NotImplementedError:
                
                self.TransientTipWindow = macTransientTipWindow

        else:
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
            if flags:
                return wx.NOT_FOUND, flags
            else:
                return wx.NOT_FOUND
     
        if not mirror and \
           (point.y <= size.y - height or point.y >= size.y):
            if flags:
                return wx.NOT_FOUND, flags
            else:
                return wx.NOT_FOUND
        
        if mirror and (point.y <= 0 or point.y >= height + self._padding.y*2):
            if flags:
                return wx.NOT_FOUND, flags
            else:
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


    def SetImageToCloseButton(self, convert=True):
        """ Set Whether The Tab Icon Should Be Converted To The Close Button Or Not. """
        
        self._convertimage = convert

        
    def GetImageToCloseButton(self):
        """ Get Whether The Tab Icon Should Be Converted To The Close Button Or Not. """
        
        return self._convertimage        


    def ConvertImageToCloseButton(self, page):
        """ Globally Converts The Page Image To The "Opera" Style Close Button. """

        bmpindex = self.GetPageImage(page)
        if  bmpindex < 0:
            return

        tabrect = self._tabrect[page]
        size = self.GetSize()

        maxfont = self._maxfont

        dc = wx.ClientDC(self)        

        dc.SetFont(maxfont) 
        pom, height = dc.GetTextExtent("Aq")
        
        bmp = self._imglist.GetBitmap(bmpindex)
                
        bmpposx = tabrect.x + self._padding.x
        bmpposy = size.y - (height + 2*self._padding.y + bmp.GetHeight())/2 - 1

        ypos = size.y - height - self._padding.y*2
        ysize = height + self._padding.y*2 + 3

        if page == self.GetSelection():
            bmpposx = bmpposx + 1
            bmpposy = bmpposy - 1
            ypos = ypos - 3                    
            ysize = ysize + 2
            
        colour = self.GetPageColour(page)
        bmprect = wx.Rect(bmpposx, bmpposy, bmp.GetWidth()+self._padding.x, bmp.GetHeight())
        
        dc.SetBrush(wx.Brush(colour))
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.DrawRectangleRect(bmprect)
        
        colour = self.GetPageTextColour(page)
        
        r = colour.Red()
        g = colour.Green()
        b = colour.Blue()

        hr, hg, hb = min(255,r+64), min(255,g+64), min(255,b+64)
                
        colour = wx.Colour(hr, hg, hb)
        back_colour = wx.WHITE

        yypos = ypos+(ysize-height-self._padding.y/2)/2

        xrect = wx.Rect(bmprect.x+(bmprect.width - self._padding.x - height)/2,
                        yypos, height, height)
       
        # Opera Style
        dc.SetPen(wx.Pen(colour, 1))
        dc.SetBrush(wx.Brush(colour))
        dc.DrawRoundedRectangleRect(xrect, 2)
        dc.SetPen(wx.Pen(back_colour, 2))
        dc.DrawLine(xrect[0]+2, xrect[1]+2, xrect[0]+xrect[2]-3, xrect[1]+xrect[3]-3)
        dc.DrawLine(xrect[0]+2, xrect[1]+xrect[3]-3, xrect[0]+xrect[2]-3, xrect[1]+2)
        

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
    

    def HideOnSingleTab(self, hide=True):
        """ Hides The TabCtrl When There Is Only One Tab In NotebookCtrl. """
        
        self._hideonsingletab = hide
        

    def SetPagePopupMenu(self, nPage, menu):
        """ Sets A Popup Menu Specific To A Single Tab. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPagePopupMenu: (" + str(nPage) + ")"
        
        self._pages[nPage]._menu = menu


    def GetPagePopupMenu(self, nPage):
        """ Returns The Popup Menu Associated To A Single Tab. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPagePopupMenu: (" + str(nPage) + ")"        
        
        return self._pages[nPage]._menu


    def DrawInsertionMark(self, dc, nPage):
        """
        Draw An Insertion Arrow To Let The User Understand Where A Dragged Tab Will
        Be Dropped (Between Which Tabs).
        """
        
        if nPage < 0:
            return
            
        colour = wx.BLACK

        rect = self._tabrect[nPage]
        
        x1 = rect.x - 4
        y1 = rect.y - 1
        x2 = rect.x
        y2 = y1 + 5
        x3 = rect.x + 3
        y3 = y1

        if nPage > self._tabID:
            x1 = x1 + rect.width
            x2 = x2 + rect.width
            x3 = x3 + rect.width
        
        dc.SetPen(wx.Pen(wx.BLACK, 1))
        dc.SetBrush(wx.Brush(self.GetPageTextColour(nPage)))
        dc.DrawPolygon([(x1, y1), (x2, y2), (x3, y3)])
        

    def OnMouseMotion(self, event):
        """ Handles The wx.EVT_MOTION Event For TabCtrl. """

        pt = event.GetPosition()
        
        if self._enabledragging:
            
            if event.Dragging() and not event.RightIsDown() and not event.MiddleIsDown():
                
                tolerance = 2
                
                dx = abs(pt.x - self._dragstartpos.x)
                dy = abs(pt.y - self._dragstartpos.y)
                
                if dx <= tolerance and dy <= tolerance:
                    self.SetCursor(wx.STANDARD_CURSOR)
                    return

                self.SetCursor(self._dragcursor)
                self._isdragging = True
                self._isleaving = False
                newpos = self.HitTest(pt)

                if newpos >= 0 and newpos != self._olddragpos:
                    
                    self._olddragpos = newpos
                    self.Refresh()
                    
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
            else:
                if self.GetImageToCloseButton():
                    page, flags = self.HitTest(pt, 1)
                    if page >= 0:
                        if self.IsPageEnabled(page):
                            if flags == NC_HITTEST_ONICON:
                                if not self._imageconverted:
                                    self.ConvertImageToCloseButton(page)
                                    self._imageconverted = True
                            else:
                                if self._imageconverted:
                                    self.Refresh()
                                    self._imageconverted = False
                            
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
        self._tipwindow = self.TransientTipWindow(self, self._currenttip,
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

                if event.m_controlDown:
                    if page in self._selectedtabs:
                        self._selectedtabs.remove(page)
                    else:
                        self._selectedtabs.append(page)
                    self.Refresh()
                else:
                    self._selectedtabs = []
                    if flags == NC_HITTEST_ONX or (flags == NC_HITTEST_ONICON and self.GetImageToCloseButton()):
                        eventOut = NotebookCtrlEvent(wxEVT_NOTEBOOKCTRL_PAGE_CLOSING, self.GetId())
                        eventOut.SetOldSelection(self._selection)
                        eventOut.SetSelection(page)
                        eventOut.SetEventObject(self)
                        
                        if not self.GetEventHandler().ProcessEvent(eventOut):
                            self._parent.DeletePage(page)
                            self._parent.bsizer.Layout()

                    else:
                        self.SetSelection(page)
                        self._tabID = page

        event.Skip()


    def OnMouseLeftDClick(self, event):
        """ Handles The wx.EVT_LEFT_DCLICK Event For TabCtrl. """
        
        pos = event.GetPosition()        
        page = self.HitTest(pos)
        self._selectedtabs = []

        if page == wx.NOT_FOUND:
            return

        if not self.IsPageEnabled(page):
            return

        eventOut = NotebookCtrlEvent(wxEVT_NOTEBOOKCTRL_PAGE_DCLICK, self.GetId())
        eventOut.SetOldSelection(self._selection)
        eventOut.SetSelection(page)
        eventOut.SetEventObject(self)
                
        if not self.GetEventHandler().ProcessEvent(eventOut):
            return

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

            self._isdragging = False
            self._olddragpos = -1
            eventOut = NotebookCtrlEvent(wxEVT_NOTEBOOKCTRL_PAGE_DND, self.GetId())
            eventOut.SetOldPosition(self._tabID)
            eventOut.SetNewPosition(id)
            eventOut.SetEventObject(self)
            
            if self.GetEventHandler().ProcessEvent(eventOut):
                self._tabID = -1
                self._olddragpos = -1
                self.SetCursor(wx.STANDARD_CURSOR)
                self.Refresh()
                return
            
            self._parent.Freeze()

            try:
                text = self.GetPageText(self._tabID)
                image = self.GetPageImage(self._tabID)
                font1 = self.GetPageTextFont(self._tabID)
                font2 = self.GetPageTextSecondaryFont(self._tabID)
                fontcolour = self.GetPageTextColour(self._tabID)
                pagecolour = self.GetPageColour(self._tabID)
                enabled = self.IsPageEnabled(self._tabID)
                tooltip, ontime, winsize = self.GetPageToolTip(self._tabID)
                menu = self.GetPagePopupMenu(self._tabID)
            except:
                self._parent.Thaw()
                self._tabID = -1 
                self.SetCursor(wx.STANDARD_CURSOR)
                return
            
            isanimated = 0
            if self._timers[self._tabID].IsRunning():
                isanimated = 1
                timer = self._timers[self._tabID].GetInterval()
                
            self.StopAnimation(self._tabID)
            animatedimages = self.GetAnimationImages(self._tabID)
                        
            pagerange = range(self.GetPageCount())
                
            newrange = pagerange[:]
            newrange.remove(self._tabID)
            newrange.insert(id, self._tabID)
                    
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
                if id == self.GetPageCount():
                    self.AddPage(text, True, image)
                else:
                    self.InsertPage(id, text, True, image)
            else:
                if id == self.GetPageCount():
                    self.AddPage(text, False, image)
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
            self.SetPagePopupMenu(id, menu)
            
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
            
            self._parent.Thaw()

        self._isdragging = False
        self._olddragpos = -1
        self.Refresh()
        self._tabID = -1 
        self.SetCursor(wx.STANDARD_CURSOR)
        
        event.Skip()
        
        
    def OnSize(self, event=None):
        """ Handles The wx.EVT_SIZE Event For TabCtrl. """

        self.Refresh()

        if event is not None:
            event.Skip()
             

    def OnMouseRightUp(self, event):
        """ Handles The wx.EVT_RIGHT_UP Event For TabCtrl. """
        
        pt = event.GetPosition()
        id = self.HitTest(pt)

        self._selectedtabs = []        

        if id >= 0:
            if self.IsPageEnabled(id):
                menu = self.GetPagePopupMenu(id)
                if menu:
                    self.PopupMenu(menu, pt)

        event.Skip()


    def OnMouseRightDown(self, event):
        """ Handles The wx.EVT_RIGHT_DOWN Event For TabCtrl. """

        pos = event.GetPosition()        
        page = self.HitTest(pos)

        self._selectedtabs = []
        
        if page == wx.NOT_FOUND:
            return

        if not self.IsPageEnabled(page):
            return
        
        eventOut = NotebookCtrlEvent(wxEVT_NOTEBOOKCTRL_PAGE_RIGHT, self.GetId())
        eventOut.SetOldSelection(self._selection)
        eventOut.SetSelection(page)
        eventOut.SetEventObject(self)
                
        if not self.GetEventHandler().ProcessEvent(eventOut):
            return

        event.Skip()


    def OnMouseMiddleDown(self, event):
        """ Handles The wx.EVT_MIDDLE_DOWN Event For TabCtrl. """

        pos = event.GetPosition()        
        page = self.HitTest(pos)

        self._selectedtabs = []        

        if page == wx.NOT_FOUND:
            return

        if not self.IsPageEnabled(page):
            return
        
        eventOut = NotebookCtrlEvent(wxEVT_NOTEBOOKCTRL_PAGE_MIDDLE, self.GetId())
        eventOut.SetOldSelection(self._selection)
        eventOut.SetSelection(page)
        eventOut.SetEventObject(self)
                
        if not self.GetEventHandler().ProcessEvent(eventOut):
            return

        event.Skip()


    def EnableMacStyle(self, enable=True, style=1):
        """
        Enables/Disables Mac Themes. style=1 Is The Light Style, while style=2
        Is The Dark Style.
        """
        
        if enable:
            self._macstyle = style
        else:
            self._macstyle = 0
            

    def DrawMacThemes(self, dc, tabrect):
        """ Draws The Mac Theme On Tabs, If It Is Enabled. """
        
        if self._macstyle == 1:
            col1, col2 = NC_MAC_LIGHT
        else:
            col1, col2 = NC_MAC_DARK

        colour1 = wx.Colour(col1, col1, col1)
        colour2 = wx.Colour(col2, col2, col2)

        x, y, w, h = tabrect
        index = 0
        
        for ii in xrange(0, h, 2):
            if index%2 == 0:
                colour = colour1
            else:
                colour = colour2

            dc.SetBrush(wx.Brush(colour))
            dc.SetPen(wx.Pen(colour))
            if ii > 3:
                dc.DrawRectangle(x, y+ii, w, 2)
            else:
                dc.DrawRoundedRectangle(x, y+ii, w, 3, 3)
                
            index = index + 1
                
        
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
            
            if self._macstyle:
                self.DrawMacThemes(dc, tabrect[-1])
                dc.SetPen(highlightpen)
                           
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
                    xxpos = xpos+xsize-height-self._padding.x
                    yypos = ypos+(ysize-height-self._padding.y/2)/2
                    dc.DrawRoundedRectangle(xxpos, yypos, height, height, 2)
                    dc.SetPen(wx.Pen(back_colour, 2))
                    dc.DrawLine(xxpos+2, yypos+2, xxpos+height-3, yypos+height-3)
                    dc.DrawLine(xxpos+2, yypos+height-3, xxpos+height-3, yypos+2)
                    Xrect.append(wx.Rect(xxpos, yypos, height, height))


            if ii in self._selectedtabs:
                dc.SetPen(wx.Pen(thecolour, 1, wx.DOT_DASH))
                dc.SetBrush(wx.TRANSPARENT_BRUSH)
                dc.DrawRoundedRectangle(xpos+self._padding.x/2+1, ypos+self._padding.y/2+1,
                                        xsize-self._padding.x-2,
                                        ysize-self._padding.y-2-2, 2)
                
            posx = posx + newwidth + space + self._padding.x + self._spacetabs + incrtext + xxspace
            if self._firsttime:
                self._initrect.append(tabrect[ii])

        self._tabrect = tabrect
        self._xrect = Xrect

        if self._firsttime:
            self._firsttime = False
            
        self.UpdateSpinButton()

        if self._enabledragging:
            if self._isdragging and not self._isleaving:
                self.DrawInsertionMark(dc, self._olddragpos)
                
        dc.EndDrawing()
      

# ---------------------------------------------------------------------------- #
# Class NotebookCtrl
# This Is The Main Class Implementation
# ---------------------------------------------------------------------------- #

class NotebookCtrl(wx.Panel):

    def __init__(self, parent, id, pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=NC_DEFAULT_STYLE, sizer=wx.HORIZONTAL, margin=2):
        """
        Default Class Constructor. Non-Default Parameters Are:
        
        - style: Style For The NotebookCtrl, Which May Be:
          a) NC_TOP: NotebookCtrl Placed On Top (Default);
          b) NC_BOTTOM: NotebookCtrl Placed At The Bottom;
          c) NC_FIXED_WIDTH: All Tabs Have The Same Width;
          d) wx.NO_BORDER: Shows No Border For The Control (Default, Looks Better);
          e) wx.STATIC_BORDER: Shows A Static Border On The Control.
          
        - sizer: The Sizer Orientation For The Sizer That Holds All The Panels:
          Changing This Style Is Only Useful When You Use The Tile Method.
          In This Case, If sizer=wx.HORIZONTAL, All The Panels Will Be Shown In Columns,
          While If sizer=wx.VERTICAL All The Panels Will Be Shown In Rows.

        - margin: An Integer Number Of Pixels That Add Space Above TabCtrl If style=NC_TOP,
          Or Below It If style=NC_BOTTOM
        """
        
        wx.Panel.__init__(self, parent, -1, style=wx.NO_FULL_REPAINT_ON_RESIZE |
                          wx.CLIP_CHILDREN)
        
        self.nb = TabCtrl(self, -1, pos, size, style)

        self._notebookpages = []

        if style & NC_TOP == 0 and style & NC_BOTTOM == 0:
            style = style | NC_TOP
            
        if style & wx.NO_BORDER == 0 and \
           style & wx.STATIC_BORDER == 0:
            style = style | wx.NO_BORDER
        
        self._style = style
        self._showcolumns = False
        self._showtabs = True
        self._sizerstyle = sizer
        self._custompanel = None
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.bsizer = wx.BoxSizer(sizer)

        if style & NC_TOP:
            self.sizer.Add((0, margin), 0)                
            self.sizer.Add(self.nb, 0, wx.EXPAND)
            self.sizer.Add(self.bsizer, 1, wx.EXPAND)
        else:
            self.sizer.Add(self.bsizer, 1, wx.EXPAND)
            self.sizer.Add(self.nb, 0, wx.EXPAND)
            self.sizer.Add((0, margin), 0)

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
            
            if event.Dragging() and not event.RightIsDown() and not event.MiddleIsDown():
                
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
                    try:
                        self.nb._tipwindow.Destroy()
                        self.nb._istooltipshown = False
                    except:
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

        if self.GetPageCount() == 0:
            if self.GetCustomPage() is not None:
                self.bsizer.Detach(self._custompanel)
                self._custompanel.Show(False)
                self.bsizer.Layout()
        
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

            self.bsizer.Show(page, True)
            
            if self.nb._hideonsingletab:
                
                if self._style & NC_TOP:
                    self.sizer.Show(0, False)
                    self.sizer.Show(1, False)
                else:
                    self.sizer.Show(1, False)
                    self.sizer.Show(2, False)

            else:
                self.nb.Show(True)
                if self._style & NC_TOP:
                    self.sizer.Show(0, True)
                    self.sizer.Show(1, True)
                else:
                    self.sizer.Show(1, True)
                    self.sizer.Show(2, True)

        else:
            
            self.nb.Show(True)
            if self._style & NC_TOP:
                self.sizer.Show(0, True)
                self.sizer.Show(1, True)
            else:
                self.sizer.Show(1, True)
                self.sizer.Show(2, True)

        self.bsizer.Layout()                    
        self.sizer.Layout()
            
        self.Thaw()

        self.Tile(self._showcolumns)
        self.ShowTabs(self._showtabs)
        

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

        if self.GetPageCount() == 0:
            if self.GetCustomPage() is not None:
                self.bsizer.Detach(self._custompanel)
                self._custompanel.Show(False)
                
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

            if self.nb._hideonsingletab:
                
                if self._style & NC_TOP:
                    self.sizer.Show(0, False)
                    self.sizer.Show(1, False)
                else:
                    self.sizer.Show(1, False)
                    self.sizer.Show(2, False)

            else:
                
                self.nb.Show(True)
                if self._style & NC_TOP:
                    self.sizer.Show(0, True)
                    self.sizer.Show(1, True)
                else:
                    self.sizer.Show(1, True)
                    self.sizer.Show(2, True)

        else:
            
            self.nb.Show(True)
            if self._style & NC_TOP:
                self.sizer.Show(0, True)
                self.sizer.Show(1, True)
            else:
                self.sizer.Show(1, True)
                self.sizer.Show(2, True)
                    
        self.sizer.Layout()
                        
        self.Thaw()

        self.Tile(self._showcolumns)
        self.ShowTabs(self._showtabs)

        
    def GetPage(self, nPage):
        """ Returns The Window At The Given Position nPage. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPage: (" + str(nPage) + ")"

        return self._notebookpages[nPage]
    

    def DeleteAllPages(self):
        """ Deletes All NotebookCtrl Pages. """

        self.Freeze()

        counter = self.GetPageCount() - 1
        
        for ii in xrange(self.GetPageCount()):
            self.bsizer.Detach(counter-ii)
            panels = self.GetPage(counter-ii)
            panels.Destroy()

        self.nb.DeleteAllPages()
        self._notebookpages = []
        self.nb._selection = -1

        self.nb.Show(False)

        custom = self.GetCustomPage()
            
        if custom is not None:
            self.SetCustomPage(custom)
            custom.Show(True)
            
        self.bsizer.Layout()
        
        if self._style & NC_TOP:
            self.sizer.Show(0, False)
            self.sizer.Show(1, False)
        else:
            self.sizer.Show(1, False)
            self.sizer.Show(2, False)

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
                self.sizer.Show(1, False)
            else:
                self.sizer.Show(1, False)
                self.sizer.Show(2, False)

            custom = self.GetCustomPage()
            
            if custom is not None:
                self.bsizer.Add(custom, 1, wx.EXPAND | wx.ALL, 2)
                custom.Show(True)
                
            self.bsizer.Layout()
            self.sizer.Layout()
            self.Thaw()
            return

        if self.GetPageCount() == 1:
            
            if self.nb._hideonsingletab:
                
                if self._style & NC_TOP:
                    self.sizer.Show(0, False)
                    self.sizer.Show(1, False)
                else:
                    self.sizer.Show(1, False)
                    self.sizer.Show(2, False)

            else:
                
                self.nb.Show(True)
                if self._style & NC_TOP:
                    self.sizer.Show(0, True)
                    self.sizer.Show(1, True)
                else:
                    self.sizer.Show(1, True)
                    self.sizer.Show(2, True)

        else:
            
            self.nb.Show(True)
            if self._style & NC_TOP:
                self.sizer.Show(0, True)
                self.sizer.Show(1, True)
            else:
                self.sizer.Show(1, True)
                self.sizer.Show(2, True)
                    
        self.sizer.Layout()

        self.Thaw()

        self.Tile(self._showcolumns)
        self.ShowTabs(self._showtabs)


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

        self.Tile(self._showcolumns)
        self.ShowTabs(self._showtabs)
       

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
    

    def SetImageToCloseButton(self, convert=True):
        """ Set Whether The Tab Icon Should Be Converted To The Close Button Or Not. """
        
        self.nb.SetImageToCloseButton(convert)

        
    def GetImageToCloseButton(self):
        """ Get Whether The Tab Icon Should Be Converted To The Close Button Or Not. """
        
        return self.nb._convertimage


    def HideOnSingleTab(self, hide=True):
        """ Hides The TabCtrl When There Is Only One Tab In NotebookCtrl. """
        
        self.nb.HideOnSingleTab(hide)
        
        if self.GetPageCount() == 1:
            if hide:
                if self._style & NC_TOP:
                    self.sizer.Show(0, False)
                    self.sizer.Show(1, False)
                else:
                    self.sizer.Show(1, False)
                    self.sizer.Show(2, False)
            else:
                if self._style & NC_TOP:
                    self.sizer.Show(0, True)
                    self.sizer.Show(1, True)
                else:
                    self.sizer.Show(1, True)
                    self.sizer.Show(2, True)

            self.sizer.Layout()
            

    def SetPagePopupMenu(self, nPage, menu):
        """ Sets A Popup Menu Specific To A Single Tab. """
        
        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In SetPagePopupMenu: (" + str(nPage) + ")"
        
        self.nb.SetPagePopupMenu(nPage, menu)


    def GetPagePopupMenu(self, nPage):
        """ Returns The Popup Menu Associated To A Single Tab. """

        if nPage < 0 or nPage >= self.GetPageCount():
            raise "\nERROR: Invalid Notebook Page In GetPagePopupMenu: (" + str(nPage) + ")"        
        
        return self.nb.GetPagePopupMenu(nPage)
    

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
        
        return self.nb.GetPageToolTip(nPage)


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
        
        return self.nb.GetPageText(nPage)


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


    def SetTabHeight(self, height=28):
        """ Sets The Tabs Height. """

        if height <= 0:
            raise "\nERROR: Impossible To Set An Height <= 0. "
        
        self.nb.SetTabHeight(height)


    def SetControlBackgroundColour(self, colour=None):
        """ Sets The TabCtrl Background Colour (Behind The Tabs). """

        if colour is None:
            colour = wx.SystemSettings_GetColour(wx.SYS_COLOUR_3DFACE)
            
        self.nb.SetBackgroundColour(colour)
        

    def EnableMacStyle(self, enable=True, style=1):
        """
        Enables/Disables Mac Themes. style=1 Is The Light Style, while style=2
        Is The Dark Style.
        """
        
        self.nb.EnableMacStyle(enable, style)
            

    def Tile(self, show=True, orient=None):
        """ Shows Pages In Column/Row Mode (One Panel After The Other In Columns/Rows). """
        
        if self._style & NC_TOP:
            if not self.sizer.GetItem(0).IsShown() == show and orient is None:
                return
        else:
            if not self.sizer.GetItem(2).IsShown() == show and orient is None:
                return

        self.Freeze()
        
        if orient is not None and show:
            origorient = self.bsizer.GetOrientation()
            if origorient != orient:
                for ii in xrange(self.GetPageCount()-1, -1, -1):
                    self.bsizer.Detach(ii)

                self.sizer.Detach(self.bsizer)
                self.bsizer.Destroy()
                self.bsizer = wx.BoxSizer(orient)
                
                for ii in xrange(self.GetPageCount()):
                    self.bsizer.Add(self._notebookpages[ii], 1, wx.EXPAND | wx.ALL, 2)

                if self._style & NC_TOP:
                    self.sizer.Add(self.bsizer, 1, wx.EXPAND)
                else:
                    self.sizer.Insert(0, self.bsizer, 1, wx.EXPAND)
        
                self.bsizer.Layout()
                self.sizer.Layout()
                
        selection = self.GetSelection()
        
        if show:
            if self._style & NC_TOP:
                self.sizer.Show(0, False)
                self.sizer.Show(1, False)
                if len(self.nb._selectedtabs) > 0:
                    for ii in xrange(self.GetPageCount()):
                        if ii in self.nb._selectedtabs:
                            self.bsizer.Show(ii, True)
                        else:
                            self.bsizer.Show(ii, False)
                else:
                    for ii in xrange(self.GetPageCount()):
                        if self.IsPageEnabled(ii):
                            self.bsizer.Show(ii, True)
                        else:
                            self.bsizer.Show(ii, False)
            else:
                self.sizer.Show(1, False)
                self.sizer.Show(2, False)
                if len(self.nb._selectedtabs) > 0:
                    for ii in xrange(self.GetPageCount()):
                        if ii in self.nb._selectedtabs:
                            self.bsizer.Show(ii, True)
                else:
                    for ii in xrange(self.GetPageCount()):
                        if self.IsPageEnabled(ii):
                            self.bsizer.Show(ii, True)
        else:
            if self._style & NC_TOP:
                self.sizer.Show(0, True)
                self.sizer.Show(1, True)
                for ii in xrange(self.GetPageCount()):
                    self.bsizer.Show(ii, False)
            else:
                self.sizer.Show(1, True)
                self.sizer.Show(2, True)
                for ii in xrange(self.GetPageCount()):
                    self.bsizer.Show(ii, False)

            if selection < 0:
                self.bsizer.Layout()
                self.sizer.Layout()
                return
            else:
                self.bsizer.Show(selection, True)
                self.bsizer.Layout()

        self._showcolumns = show
        
        self.bsizer.Layout()
        self.sizer.Layout()

        self.Thaw()        


    def ShowTabs(self, show=True):
        """ Shows/Hides Tabs On Request. """
        
        if self._style & NC_TOP:
            if self.sizer.GetItem(0).IsShown() == show:
                return
        else:
            if self.sizer.GetItem(2).IsShown() == show:
                return

        if self.GetPageCount() == 0:
            return
        
        self.Freeze()
        
        if not show:
                
            if self._style & NC_TOP:
                self.sizer.Show(0, False)
                self.sizer.Show(1, False)
            else:
                self.sizer.Show(1, False)
                self.sizer.Show(2, False)

        else:
            
            if self._style & NC_TOP:
                self.sizer.Show(0, True)
                self.sizer.Show(1, True)
            else:
                self.sizer.Show(1, True)
                self.sizer.Show(2, True)

        self._showtabs = show
        
        self.sizer.Layout()
        
        self.Thaw()


    def GetIndex(self, page):
        """ Returns The Page Index (Position) Based On The NotebookCtrl Page Passed. """

        if page in self._notebookpages:
            return self._notebookpages.index(page)

        return -1
    

    def ReparentPage(self, nPage, newParent):
        """ Reparents The NotebookCtrl Page nPage To A New Parent. """
        
        if nPage < 0 or (self.GetSelection() >= 0 and nPage >= self.GetPageCount()):
            raise "\nERROR: Invalid Notebook Page In ReparentPage: (" + str(nPage) + ")"
        
        page = self.GetPage(nPage)
        page.Reparent(newParent)
        

    def ReparentToFrame(self, nPage, createNotebook=False):
        """ Reparents The NotebookCtrl Page nPage To A New Frame. """
        
        if nPage < 0 or (self.GetSelection() >= 0 and nPage >= self.GetPageCount()):
            raise "\nERROR: Invalid Notebook Page In ReparentToFrame: (" + str(nPage) + ")"
        
        self.Freeze()

        infos = self.GetPageInfo(nPage)
        panel = self.GetPage(nPage)
        text = infos["text"]
        oldparent = panel.GetParent()

        frame = NCFrame(None, -1, text, nb=self, infos=infos, panel=panel, oldparent=oldparent)
        
        if createNotebook:
            nb = NotebookCtrl(frame, -1, style=self._style, sizer=self._sizerstyle)
            nb.SetImageList(infos["imagelist"])
            self.ReparentToNotebook(nPage, nb)
        else:
            self.ReparentPage(nPage, frame)
            
            self.nb.DeletePage(nPage, False)

            self.bsizer.Detach(nPage)
            self.bsizer.Layout()
            self.sizer.Layout()

            self._notebookpages.pop(nPage)
            
            self.AdvanceSelection()

        if self.GetPageCount() == 0:
            if self._style & NC_TOP:
                self.sizer.Show(0, False)
                self.sizer.Show(1, False)
            else:
                self.sizer.Show(1, False)
                self.sizer.Show(2, False)

            self.sizer.Layout()

        custom = self.GetCustomPage()
        if custom is not None:
            self.SetCustomPage(custom)
            
        self.Thaw()

        frame.Show()

        
    def ReparentToNotebook(self, nPage, notebook, newPage=None):
        """ Reparents The NotebookCtrl Page nPage To A New NotebookCtrl. """
        
        if nPage < 0 or (self.GetSelection() >= 0 and nPage >= self.GetPageCount()):
            raise "\nERROR: Invalid Notebook Page In ReparentToNotebook: (" + str(nPage) + ")"

        if newPage is not None and newPage >= notebook.GetPageCount():
            raise "\nERROR: Invalid Notebook New Page In ReparentToNotebook: (" + str(nPage) + ")"

        self.Freeze()
        
        infos = self.GetPageInfo(nPage)
        panel = self.GetPage(nPage)

        self.ReparentPage(nPage, notebook)
        
        if newPage is None:
            notebook.AddPage(panel, infos["text"], False, infos["image"])
            notebook.SetPageInfo(0, infos)
            
        self.nb.DeletePage(nPage, False)

        self.bsizer.Detach(nPage)
        self.bsizer.Layout()
        self.sizer.Layout()

        self._notebookpages.pop(nPage)
        
        self.AdvanceSelection()

        if self.GetPageCount() == 0:
            if self._style & NC_TOP:
                self.sizer.Show(0, False)
                self.sizer.Show(1, False)
            else:
                self.sizer.Show(1, False)
                self.sizer.Show(2, False)

            self.sizer.Layout()

        self.Thaw()        
        

    def GetPageInfo(self, nPage):
        """ Returns All The Style Information For A Given Page. """

        if nPage < 0 or (self.GetSelection() >= 0 and nPage >= self.GetPageCount()):
            raise "\nERROR: Invalid Notebook Page In GetPageInfo: (" + str(nPage) + ")"
        
        text = self.GetPageText(nPage)
        image = self.GetPageImage(nPage)
        font1 = self.GetPageTextFont(nPage)
        font2 = self.GetPageTextSecondaryFont(nPage)
        fontcolour = self.GetPageTextColour(nPage)
        pagecolour = self.GetPageColour(nPage)
        enabled = self.IsPageEnabled(nPage)
        tooltip, ontime, winsize = self.GetPageToolTip(nPage)
        menu = self.GetPagePopupMenu(nPage)
            
        isanimated = 0
        timer = None

        if self.nb._timers[nPage].IsRunning():
            isanimated = 1
            timer = self.nb._timers[nPage].GetInterval()
            
        self.StopAnimation(nPage)
        animatedimages = self.GetAnimationImages(nPage)

        infos = {"text": text, "image": image, "font1": font1, "font2": font2,
                 "fontcolour": fontcolour, "pagecolour": pagecolour, "enabled": enabled,
                 "tooltip": tooltip, "ontime": ontime, "winsize": winsize,
                 "menu": menu, "isanimated": isanimated, "timer": timer,
                 "animatedimages": animatedimages, "imagelist": self.nb._imglist}

        return infos


    def SetPageInfo(self, nPage, infos):
        """ Sets All The Style Information For A Given Page. """

        if nPage < 0 or (self.GetSelection() >= 0 and nPage >= self.GetPageCount()):
            raise "\nERROR: Invalid Notebook Page In SetPageInfo: (" + str(nPage) + ")"

        self.SetPageTextFont(nPage, infos["font1"])
        self.SetPageTextSecondaryFont(nPage, infos["font2"])
        self.SetPageTextColour(nPage, infos["fontcolour"])
        self.SetPageColour(nPage, infos["pagecolour"])
        self.EnablePage(nPage, infos["enabled"])
        self.SetPageToolTip(nPage, infos["tooltip"], infos["ontime"], infos["winsize"])
        self.SetPagePopupMenu(nPage, infos["menu"])
        
        if infos["isanimated"] and len(infos["animatedimages"]) > 1:
            self.SetAnimationImages(nPage, infos["animatedimages"])
            self.StartAnimation(nPage, infos["timer"])
    

    def SetCustomPage(self, panel):
        """ Sets A Custom Panel To Show When There Are No Pages Left In NotebookCtrl. """
        
        self.Freeze()
        
        if panel is None:
            if self._custompanel is not None:
                self.bsizer.Detach(self._custompanel)
                self._custompanel.Show(False)
                
            if self.GetPageCount() == 0:   
                if self._style & NC_TOP:
                    self.sizer.Show(0, False)
                    self.sizer.Show(1, False)
                else:
                    self.sizer.Show(1, False)
                    self.sizer.Show(2, False)
        else:
            if self.GetPageCount() == 0:
                if self._custompanel is not None:
                    self.bsizer.Detach(self._custompanel)
                    self._custompanel.Show(False)
                    
                self.bsizer.Add(panel, 1, wx.EXPAND | wx.ALL, 2)
                panel.Show(True)
                if self._style & NC_TOP:
                    self.sizer.Show(0, False)
                    self.sizer.Show(1, False)
                else:
                    self.sizer.Show(1, False)
                    self.sizer.Show(2, False)
            else:
                panel.Show(False)

        self._custompanel = panel
        
        self.bsizer.Layout()
        self.sizer.Layout()
        self.Thaw()
            

    def GetCustomPage(self):
        """ Gets A Custom Panel To Show When There Are No Pages Left In NotebookCtrl. """
        
        return self._custompanel
    

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

class _PopupWindow:
    
    def _Fill(self, tip, winsize):
        
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour(wx.Colour(255, 255, 230))

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
        

class TransientTipWindow(_PopupWindow, wx.PopupWindow):
    
    def __init__(self, parent, tip, winsize):
        
        wx.PopupWindow.__init__(self, parent, flags=wx.SIMPLE_BORDER)
        self._Fill(tip,winsize)
        
        
    def ProcessLeftDown(self, evt):
        
        return False


    def OnDismiss(self):
        
        return False


class macPopupWindow(wx.Frame):
    
    def __init__(self, parent, flags):
        
        wx.Frame.__init__(self, parent, id=-1, style=flags|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP)
        self._hideOnActivate = False
        #Get the parent frame: could be improved maybe?
        self._parentFrame = parent
        
        while True:
            
            parent = self._parentFrame.GetParent()

            if parent:
                self._parentFrame = parent
            else:
                break
            
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)

            
    def Show(self, show=True):
        
        wx.Frame.Show(self,show)
        
        if show:
            self._parentFrame.Raise()
            self._hideOnActivate = True
            
            
    def OnActivate(self, evt):
        """
        Let The User Hide The Tooltip By Clicking On It. 
        NotebookCtrl Will Destroy It Later.
        """
        
        if self._hideOnActivate:
            wx.Frame.Show(self,False)
        
            
class macTransientTipWindow(_PopupWindow, macPopupWindow):
    
    def __init__(self, parent, tip, winsize):
        
        macPopupWindow.__init__(self, parent, flags=wx.SIMPLE_BORDER)
        self._Fill(tip, winsize)
    

class NCFrame(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, nb=None,
                 panel=None, infos=None, oldparent=None):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self._infos = infos
        self._nb = nb
        self._panel = panel
        self._oldparent = oldparent

        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def OnClose(self, event):
        
        try:
            infos = self._infos
            self._panel.Reparent(self._oldparent)            
            self._nb.AddPage(self._panel, infos["text"], False, infos["image"])

            id = self._nb.GetPageCount() - 1
            
            self._nb.SetPageTextFont(id, infos["font1"])
            self._nb.SetPageTextSecondaryFont(id, infos["font2"])
            self._nb.SetPageTextColour(id, infos["fontcolour"])
            self._nb.SetPageColour(id, infos["pagecolour"])
            self._nb.EnablePage(id, infos["enabled"])
            self._nb.SetPageToolTip(id, infos["tooltip"], infos["ontime"], infos["winsize"])
            self._nb.SetPagePopupMenu(id, infos["menu"])
            
            if infos["isanimated"] and len(infos["animatedimages"]) > 1:
                self._nb.SetAnimationImages(id, infos["animatedimages"])
                self._nb.StartAnimation(id, infos["timer"])

        except:
            self.Destroy()
            event.Skip()
            return

        self.Destroy()        

        event.Skip()

        
