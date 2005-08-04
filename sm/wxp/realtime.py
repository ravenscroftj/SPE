#(c)www.stani.be

import wx

class TreeItem:
    def __init__(self,text,id):
        self.id                 = id
        self.text               = text
        #
        self.backgroundColour   = (255,255,255)
        self.bold               = 0
        self.children           = []
        self.data               = None
        self.image              = {}
        self.textColour         = (0,0,0)
        self.confirmed          = 1
        self.wx                 = None
        
class Base:
    def GetPyData(self,item):
        return self.wx.GetPyData(item)
        
    def Refresh(self):
        self.wx.Refresh()
        
    def SetImageList(self,*args,**kwds):
        self.wx.SetImageList(*args,**kwds)
        
    def SetPyData(self,item,data):
        if item.data != data:
            item.data = data
            self.wx.SetPyData(item.wx,data)

    def SetHelpText(self,*args,**kwds):
        self.wx.SetHelpText(*args,**kwds)
        
"""
# TODO: Fix this bug!!! May be the reason why it crashes on mac.
  File "d:\Data\Python\_spe\Menu.py", line 424, in menu_save
    self.parentPanel.childActive.save()
  File "d:\Data\Python\_spe\Child.py", line 205, in save
    if self.encoding:
  File "d:\Data\Python\_spe\Child.py", line 435, in updateSidebar
    def updateSidebar(self,event=None):
  File "d:\Data\Python\_spe\Child.py", line 599, in updateExplore
    if rest[-1] == ':':l+= rest
  File "D:\Data\Python\sm\wxp\realtime.py", line 32, in SetPyData
    self.wx.SetPyData(item.wx,data)
  File "C:\Python23\Lib\site-packages\wx-2.5.3-msw-ansi\wx\_controls.py", line 5166, in SetItemPyData
    return _controls_.TreeCtrl_SetItemPyData(*args, **kwargs)
wx._core.PyAssertionError: C++ assertion "wxAssertFailure" failed in ..\..\src\msw\treectrl.cpp(1166): invalid tree item
"""

class Tree(Base):
    def __init__(self,*args,**kwds):
        self.items          = {}
        self.wx             = wx.TreeCtrl(*args,**kwds)
        self.Connect        = self.wx.Connect
        self.GetId          = self.wx.GetId
        self.SetBackgroundColour = self.wx.SetBackgroundColour
        
    def AddRoot(self,text):
        self.root           = TreeItem(text=text,id=text)
        self.items[text]    = self.root
        self.root.wx        = self.wx.AddRoot(text)
        self.wx.Expand(self.root.wx)
        return self.root
        
    def AppendItem(self,parent,text):
        id                  = '%s|%s'%(parent.id,text)
        children            = parent.children
        #try to find item
        item            = None
        if id in self.items.keys() or id[:-1] in self.items.keys():
            i               = 0
            while i<len(children) and not item:
                child       = children[i]
                if child.confirmed:
                    i       +=1
                else:
                    if id == child.id:
                        item            = child
                        item.confirmed  = 1
                    elif id[:-1] == child.id:
                        item            = child
                        item.id         = id
                        item.confirmed  = 1
                        self.wx.SetItemText(item.wx,text)
                        self.items[id]  = item
                        del self.items[id[:-1]]
                    else:
                        self.wx.Delete(child.wx)
                        if self.items.has_key(child.id):
                            del self.items[child.id]
                        del children[i]
        if not item:
            item            = TreeItem(text=text,id=id)
            self.items[id]  = item
            i = 0
            n = len(children)
            while i<n and children[i].confirmed:
                i+=1
            if i>0:
                item.wx         = self.wx.InsertItem(parent.wx,children[i-1].wx,text)
            else:
                item.wx         = self.wx.PrependItem(parent.wx,text)
            parent.children.insert(i,item)
        return item
        
    def Clean(self):
        self.root.confirmed = 1
        for id,item in self.items.items():
            if not item.confirmed:
                try:
                    self.wx.Delete(item.wx)
                except:
                    print 'Warning: Tree.clean: please contact s_t_a_n_i at yahoo.com'
                del self.items[id]
##        self.root.confirmed = 1
##        clear_id = []
##        clear_item = []
##        for id,item in self.items.items():
##            if not item.confirmed:
##                clear_id.append(id)
##                clear_item.append(item)
##        for i in range(len(clear_id)):
##            del (clear_id[i])
##            del (clear_item[i])

        
    def Collapse(self,item):
        if self.wx.IsExpanded(item.wx):
            self.wx.Collapse(item.wx)
            
    def CollapseAndReset(self,item):
        """Recursively"""
        item.confirmed      = 0
        for child in item.children:
            self.CollapseAndReset(child)
           
    def Expand(self,item):
        if not self.wx.IsExpanded(item.wx):
            self.wx.Expand(item.wx)
            
            
    def SetItemBackgroundColour(self,item,color):
        if item.backgroundColour != color:
            item.backgroundColour = color
            self.wx.SetItemBackgroundColour(item.wx,color)
            
    def SetItemBold(self,item):
        if not item.bold:
            item.bold = 1
            self.wx.SetItemBold(item.wx)
        
    def SetItemImage(self,item,image,which=wx.TreeItemIcon_Normal):
        if not item.image.has_key(which) or item.image[which]!= image:
            item.image[which] = image
            self.wx.SetItemImage(item.wx,image,which)
        
    def SetItemTextColour(self,item,color):
        if item.textColour != color:
            item.textColour = color
            self.wx.SetItemTextColour(item.wx,color)
            
        
class ListItem:
    def __init__(self,parent,row,*text):
        self.listCtrl           = parent.wx
        self.children           = parent.children
        self.row                = row
        self.text               = text
        #
        self.id                 = '|'.join(text)
        self.image              = None
        self.backgroundColour   = wx.Colour(255,255,255)
        self.confirmed          = 1
        self.data               = None
        self.textColour         = None
        
    def wx(self):
        return self.children.index(self)
        
class ListCtrl(Base):
    def __init__(self,*args,**kwds):
        self.items          = {}
        self.children       = []
        self.wx             = wx.ListCtrl(*args,**kwds)
        self.Connect        = self.wx.Connect
        self.GetId          = self.wx.GetId
        self.InsertColumn   = self.wx.InsertColumn
        
    def Clean(self):
        for id,item in self.items.items():
            if not item.confirmed:
                try:
                    self.wx.DeleteItem(self.children.index(item))
                except:
                    print 'Warning: List.clean: please contact s_t_a_n_i at yahoo.com'
                self.children.remove(item)
                del self.items[id]
                
    def DeleteAllItems(self):
        for child in self.children:
            child.confirmed = 0
            
    def DeleteItem(self,item):
        self.wx.DeleteItem(item.wx)
        self.children.remove(item)
        del self.items[item.id]
    
    def GetItem(self,item):
        return self.wx.GetItem(item.wx())
        
    def GetItemData(self,item):
        return self.wx.GetPyData(item)
        
    def InsertStringItem(self,row,*text):
        item            = None
        id              = '|'.join(text)
        if id in self.items.keys() or id[:-1] in self.items.keys():
            i               = 0
            while i<len(self.children) and not item:
                child       = self.children[i]
                if child.confirmed:
                    i       +=1
                else:
                    if id == child.id:
                        item            = child
                        item.confirmed  = 1
                    elif id[:-1] == child.id:
                        item            = child
                        item.id         = id
                        item.text       = text
                        item.confirmed  = 1
                        column          = 0
                        for t in item.text:
                            self.wx.SetStringItem(item.wx(),column,t)
                            column      += 1
                        self.items[id]   = item
                        del self.items[id[:-1]]
                    else:
                        self.wx.DeleteItem(child.wx())
                        self.children.remove(child)
                        del self.items[child.id]
        if not item:
            item    = ListItem(self,row,*text)
            w       = self.wx.InsertStringItem(row,text[0])
            i       = 0
            for t in text[1:]:
                i   += 1
                self.wx.SetStringItem(w,i,t)
            self.children.insert(row,item)
            self.items[id]=item
        return item
        
    def InsertImageStringItem(self,row,icon,*text):
        item = self.InsertStringItem(row,*text)
        self.SetItemImage(item,icon,icon)
        return item
        
    def SetItemImage(self,item,*image):
        if item.image != image:
            item.image = image
            self.wx.SetItemImage(item.wx(),*image)
        
    def SetHelpText(self,*args,**kwds):
        self.wx.SetHelpText(*args,**kwds)
        
    def SetItem(self,item):
        self.wx.SetItem(item)
        
    def SetItemData(self,item,data):
        if item.data != data:
            item.data = data
            self.wx.SetItemData(item.wx(),data)
        
    def SetItemTextColour(self,item,colour):
        if item.textColour != colour:
            item.textColour = colour
            i = self.wx.GetItem(item.wx())
            i.SetTextColour(colour)
            self.wx.SetItem(i)
