"""realtime.py | GPL - license | (c)2005 www.stani.be

This module provides two classes which enable to update only selectively parts
of a wx.TreeCtrl or a wx.ListCtrl. This makes fast/realtime updating without 
collapse and resetting the whole tree or list."""

import wx

WARNING = 'Warning: %s: please contact spe.stani.be at gmail.com'

class Base:
    """Base class to pass methods to its corresponding wx method."""
    def GetPyData(self,item):
        """Retrieves the data of an item. Usually used by events.
        Important notice: item is wx, not TreeItem!"""
        return self.wx.GetPyData(item)
        
    def Refresh(self):
        """Refresh the wx control."""
        self.wx.Refresh()
        
    def SetImageList(self,*args,**kwds):
        """Sets the image list of the wx control."""
        self.wx.SetImageList(*args,**kwds)
        
    def SetPyData(self,item,data):
        """Sets the py data of a TreeItem."""
        if item.data != data:
            item.data = data
            item._update.append((self.wx.SetPyData,data))

    def SetHelpText(self,*args,**kwds):
        """Sets the help text of the wx control."""
        self.wx.SetHelpText(*args,**kwds)
        
    def Update(self):
        """This might be overwritten. """
        self.wx.Update()
        
class TreeItem:
    """All the wx actions are handled by the Tree class."""
    def __init__(self,text,id):
        """self.wx holds the """
        self.id                 = id
        self.text               = text
        #
        self.backgroundColour   = (255,255,255)
        self.bold               = 0
        self.children           = []
        self.previousChildren   = []
        self.data               = None
        self.image              = {}
        self.textColour         = (0,0,0)
        self.deleted            = False
        self.wx                 = None
        self._update            = []
        
    def Delete(self):
        """When an item is removed its children are also removed automatically."""
        for child in self.children:
            if child.children:
                child.Delete();
            child.deleted = True
        self.deleted    = True
        
class Tree(Base):
    def __init__(self,*args,**kwds):
        self.items          = {}
        self.wx             = wx.TreeCtrl(*args,**kwds)
        self.Connect        = self.wx.Connect
        self.GetId          = self.wx.GetId
        self.SetBackgroundColour = self.wx.SetBackgroundColour
        
    def AddRoot(self,text):
        self.root           = TreeItem(text=text,id=text)
        self.root._update.append((self.wx.Expand,))
        self.SetPyData(self.root,1)
        self.items[text]    = self.root
        self.root.wx        = self.wx.AddRoot(text)
        return self.root
        
    def AppendItem(self,parent,text):
        """There are two possibilities that an item is appended to its parent
        - if already present, pick it up and update the text
        - if not, create one item"""
        id                  = '%s|%s'%(parent.id,text)
        if self.items.has_key(id):
            item            = self.items[id]
            item.children   = []
        else:
            item            = self.items[id] = TreeItem(text=text,id=id)
        parent.children.append(item)
        return item
        
    def Delete(self,item):
        """Delete item and all its children from the tree."""
        if not item.deleted:
            item.Delete()
            try:
                self.wx.Delete(item.wx)
            except:
                print WARNING%'realtime.Tree.Delete'
        if self.items.has_key(item.id):
            del self.items[item.id]
        
    def Update(self):
        """Update only differences between current and previous state.
        This method MUST be called in the end otherwise there will be no visual
        change."""
        self._Update(self.root)
        self.UpdateItem(self.root)
        
    def _Update(self,parent):
        """Update recursively all children (TreeItem) of parent."""
        children                = parent.children
        previousChildren        = parent.previousChildren
        toDelete                = []
        for index, child in enumerate(children[:]):
            if child in previousChildren:
                #child exists already
                index           = previousChildren.index(child)
                for abandoned in previousChildren[:index]:
                    self.Delete(abandoned)
                previousChildren= previousChildren[index+1:]
            elif previousChildren and previousChildren[0] not in children:
                #child can be copied in existing, abandoned item
                empty_slot      = previousChildren[0]
                child           = children[index]\
                                = self.CopyItemTo(child,empty_slot)
                previousChildren= previousChildren[1:]
                self.UpdateItem(child)
            else:
                #child must be created
                if index>0:
                    child.wx        = self.wx.InsertItem(parent.wx,children[index-1].wx,child.text)
                else:
                    child.wx        = self.wx.PrependItem(parent.wx,child.text)
                child.wx.realtime   = child
                self.UpdateItem(child)
            #recursive on its children
            self._Update(child)
        for abandoned in previousChildren:
            self.Delete(item)
        parent.previousChildren = children
        
    def Collapse(self,item):
        """Collapse a TreeItem."""
        if self.wx.IsExpanded(item.wx):
            self.wx.Collapse(item.wx)
            
    def CollapseAndReset(self,item):
        """Remove children of a TreeItem, mostly used for self.root."""
        item.children = []
           
    def Expand(self,item):
        """Expands a TreeItem."""
        if not self.wx.IsExpanded(item.wx):
            self.wx.Expand(item.wx)
            
    def SetItemBackgroundColour(self,item,color):
        """Sets the background colour of a TreeItem"""
        if item.backgroundColour != color:
            item.backgroundColour = color
            item._update.append((self.wx.SetItemBackgroundColour,color))
            
    def SetItemBold(self,item,bold=True):
        """Sets the background colour of a TreeItem"""
        if item.bold != bold:
            item.bold = bold
            item._update.append((self.wx.SetItemBold,bold))
        
    def SetItemImage(self,item,image,which=wx.TreeItemIcon_Normal):
        """Sets the image for a certain state (which) of a TreeItem"""
        if (not item.image.has_key(which)) or item.image[which] != image:
            item.image[which] = image
            item._update.append((self.wx.SetItemImage,image,which))
        
    def SetItemTextColour(self,item,color):
        """Sets the text colour of a TreeItem"""
        if item.textColour != color:
            item.textColour = color
            item._update.append((self.wx.SetItemTextColour,color))
            
    def CopyItemTo(self,frm,to):
        """Copy/steal wx control from an abandoned TreeItem to avoid creating a new wx control."""
        frm.wx  = to.wx
        frm._update.append((self.wx.SetItemText,frm.text))
        return frm
        
    def UpdateItem(self,item):
        """Execute pending update actions of TreeItem"""
        for action in item._update:
            arguments = [item.wx]
            arguments.extend(action[1:])
            action[0](*arguments)

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
                    print 'Warning: List.clean: please contact spe.stani.be at gmail.com'
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
