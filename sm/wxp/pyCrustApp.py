#(c)www.stani.be (read __doc__ for more information)                            
import sm
INFO=sm.INFO.copy()

INFO['author']      = 'www.wxpython.org'
INFO['copyright']   = '(c) www.wxpython.org'
INFO['title']       = INFO['titleFull'] = 'wxPython source code'
INFO['description'] =\
"""PyCrustApp is a python shell and namespace browser application.

Changes:
    - may 2003:
        Adapted by www.stani.be for better tab support (see #custom):
        class App got new initalization:__init__
        smWx.py will overwrite some code of wxPython crust.py
        For a demonstration: this can only be run from wxp.py 
        (because of overwritten)
"""

__doc__=INFO['doc']%INFO
#_______________________________________________________________________________

#===PyCrustApp original header=================================================
"""PyCrustApp is a python shell and namespace browser application.

Adapted by www.stani.be for better tab support (see #custom):
class App got new initalization:__init__
smWx.py will overwrite some code of wxPython crust.py

For a demonstration this can only be run from wxp.py (because of overwritten)
"""
MODULE_ERROR="Error: Module(s) %s required, but not installed (%s)!"
WXPYTHON_URL="www.wxpython.org"

# The next two lines, and the other code below that makes use of
# ``__main__`` and ``original``, serve the purpose of cleaning up the
# main namespace to look as much as possible like the regular Python
# shell environment.
import __main__
original = __main__.__dict__.keys()

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>,www.stani.be for tab enhancement"
__cvsid__ = "$Id: PyCrustApp.py,v 1.9.2.5 2003/03/20 23:14:32 RD Exp $"
__revision__ = "$Revision: 1.9.2.5 $"[11:-2]

try:
    True
except NameError:
    True = 1==1
    False = 1==0

try:
    import wx
    
    class App(wx.App):
        """PyCrust standalone application."""

        def OnInit(self,size=(800,600),frame=None):
            import wx
            wx.InitAllImageHandlers()
            if not frame:
                from wxp import SmCrustFrame as CrustFrame #custom
            self.frame = CrustFrame(title=self.title,locals=self.locals,
                                    tabs=self.tabs,welcome=self.welcome) #custom
            self.frame.SetSize(size)
            self.frame.Show()
            self.SetTopWindow(self.frame)
            return 1

        def __init__(self,parent,locals=0,title='',tabs={},welcome="",size=(800,600),frame=None):#custom
            import wx
            self.locals=locals
            self.title=title
            self.tabs=tabs
            self.welcome=welcome
            wx.App.__init__(self,parent,size)

    '''
    The main() function needs to handle being imported, such as with the
    pycrust script that wxPython installs:

        #!/usr/bin/env python

        from wx.py.PyCrust import main
        main()
    '''

    def main(extraObjects=None,title='Pycrust adapted by www.stani.be',tabs={},welcome="",frame=None):
        """The main function for the PyCrust program."""
        # Cleanup the main namespace, leaving the App class.
        import __main__
        md = __main__.__dict__
        keepers = original
        keepers.append('App')
        for key in md.keys():
            if key not in keepers:
                del md[key]
        if not extraObjects:extraObjects=md #custom
        # Create an application instance.
        app = App(0,locals=extraObjects,title=title,tabs=tabs,welcome=welcome)#custom
        # Mimic the contents of the standard Python shell's sys.path.
        import sys
        if sys.path[0]:
            sys.path[0] = ''
        # Add the application object to the sys module's namespace.
        # This allows a shell user to do:
        # >>> import sys
        # >>> sys.app.whatever
        sys.app = app
        del sys
        # Cleanup the main namespace some more.
        if md.has_key('App') and md['App'] is App:
            del md['App']
        if md.has_key('__main__') and md['__main__'] is __main__:
            del md['__main__']
        # Start the wxPython event loop.
        app.MainLoop()

except ImportError:
    def main(title='',tabs={},welcome=""):
        print MODULE_ERROR%('PyCrust',WXPYTHON_URL)

if __name__=='__main__':print "Run wxp.py instead."