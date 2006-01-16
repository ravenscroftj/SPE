import wx
import os
import _spe.info as info

LINUX_HOME          = 'Home directory'
LINUX_HOME_LENGTH   = len(LINUX_HOME)

class Browser(wx.GenericDirCtrl) :
    def __init__ (self, parent, id, init_path=''):
        wx.GenericDirCtrl.__init__(self,parent,id,
            dir     = init_path,
            size=(200,225),
            filter  = info.WILDCARD_EXTENDED,
            style   = wx.DIRCTRL_SHOW_FILTERS)
        self.dir    = init_path
        self.tree   = self.GetTreeCtrl()
        self.home   = os.path.dirname(info.INFO['userPath'])
        self.tree.Bind(wx.EVT_LEFT_DCLICK, self.onClick)
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.onClick)
        
    def update(self):
        self.SetPath(self.dir)
        
    #onClick
    def onClick (self, event) :
        tree        = self.tree
        root        = tree.GetRootItem()
        pt          = event.GetPosition();
        item, flags = tree.HitTest(pt)
        event.Skip()
        #tree.SelectItem(item)
        
        try:
            path = tree.GetItemText(item)
            parent = tree.GetItemParent ( item )        
            while parent != root :
                p = tree.GetItemText( parent )
                if not p.endswith (os.sep) : p += os.sep
                path = p + path
                parent = tree.GetItemParent(parent)
        except : # invalid item
            return
            
        if info.DARWIN:
            print 'Trying to open "%s".\nIs this a valid path (answer to s_t_a_n_i@yahoo.com)?'%path
        if info.LINUX:
            if path[:LINUX_HOME_LENGTH] == LINUX_HOME:
                path = self.home + path[LINUX_HOME_LENGTH:]
        if os.path.isfile(path): 
            self.open(path)
            
    def open(self, fname) : 
        pass
        
