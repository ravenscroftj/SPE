
import re
import wx, wx.lib.ogl as ogl

INITIALIZED = False

BOTTOM      = 9999
DEFAULT     = '-'
SEPARATOR   = '+'

RE_PARENT   = re.compile("[^(]+[(]([^)]+)[)]")

####Utilities
def htmlColour(c):
    return ('#%2s%2s%2s'%tuple([hex(x)[2:] for x in (c.Red(),c.Green(),c.Blue())])).replace(' ','0').upper()
    
####Generic
class Class:
    def __init__(self,name='class',container=[],children=[],data=None):
        #passing values...
        self.name           = name
        self.container      = container[:]
        self.children       = children
        self.data           = data
        #initialize
        match               = RE_PARENT.match(self.name)
        if match:
            self.parents    = [x.strip() for x in match.group(1).split(',')]
            self.hierarchy  = BOTTOM
            self.verified   = False
        else:
            self.parents    = []
            self.hierarchy  = 0
            self.verified   = True
        
    def __measure(self):
        self.width      = max([len(x) for x in [self.name]+self.container])
        self.height     = len(self.container)+1
        self.wxWidth    = self.width*8
        self.wxHeight   = self.height*20
        
    def __str__(self):
        self.__measure()
        entry           = '| %%-%ss |'%self.width
        line            = '+'+'-'*(self.width+2)+'+'
        return '\n'.join([line]+[entry%x for x in self.container]+[line])

    def append(self,x,t=DEFAULT):
        self.container.append('%s%s'%(t,x))
            
    def extend(self,l,t=DEFAULT):
        for x in l: self.append(x,t=t)
        
    def getHierarchy(self,classes):
        if not self.verified:
            parents = [classes[parent].getHierarchy(classes) 
                    for parent in self.parents if classes.has_key(parent)]
            if parents:
                self.hierarchy  = max(parents)+1
            else:
                self.hierarchy  = 1
            self.verified   = True
        return self.hierarchy
            
    #---wx
    def wx(self,canvas):
        self.__measure()
        return wxClass(self.wxWidth, self.wxHeight,canvas,self.name,self.container)
        
####WxPython
def wxAssertColour(c):
    name    = htmlColour(c)
    wx.TheColourDatabase.AddColour(name,c)
    return name

class wxClass(ogl.DividedShape):
    def __init__(self, width, height, canvas, name, container, 
            lineColour=wx.Colour(80,80,80), textColour=wx.Colour(0,0,0),
            pen=wx.BLACK_PEN,brush=wx.LIGHT_GREY_BRUSH):
        #initialize
        ogl.DividedShape.__init__(self, width, height)
        self.lineColour         = wxAssertColour(lineColour)
        self.textColour         = wxAssertColour(textColour)
        self.width              = width
        self.height             = height
        self.SetPen(pen)
        self.SetBrush(brush)
        #generate contents
        total                   = float(len(container))+1
        current                 = 0
        text                    = ''
        self.AddText(name,prop=1/total, textColour=wx.RED,format=ogl.FORMAT_CENTRE_HORIZ)
        for entry in container:
            if entry[0] == SEPARATOR:
                self.AddText(text,prop=current/total)
                self.AddText(entry[1:],prop=1/total, textColour=wx.Colour(0,0,200),format=ogl.FORMAT_CENTRE_HORIZ)
                text            = ''
                current    = 0
            else:
                text            = '%s%s\n'%(text,entry[1:])
                current     +=1
        self.AddText(text,prop=current/total)
        self.SetRegionSizes()
        self.ReformatRegions(canvas)
        
    def AddText(self,text,lineColour=None,textColour=None,prop=0.1,format=ogl.FORMAT_NONE):
        if text:
            region          = ogl.ShapeRegion()
            if lineColour:  region.SetPenColour(wxAssertColour(lineColour))
            else:           region.SetPenColour(self.lineColour)
            if textColour:  region.SetColour(wxAssertColour(textColour))
            else:           region.SetColour(self.textColour)
            region.SetText(text)
            region.SetProportions(0.0, prop)
            region.SetFormatMode(format)
            self.AddRegion(region)
            
    def Goto(self,x,y):
        self.SetX(x+self.width/2)
        self.SetY(y+self.height/2)

    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.DividedShape.OnSizingEndDragLeft(self, pt, x, y, keys, attch)
        self.SetRegionSizes()
        self.ReformatRegions()
        self.GetCanvas().Refresh()

    def ReformatRegions(self, canvas=None):
        rnum = 0

        if canvas is None:
            canvas = self.GetCanvas()

        dc = wx.ClientDC(canvas)  # used for measuring

        for region in self.GetRegions():
            text = region.GetText()
            self.FormatText(dc, text, rnum)
            rnum += 1


class wxCanvas(ogl.ShapeCanvas):
    def __init__(self, parent,**keyw):
        global INITIALIZED
        if not INITIALIZED: 
            ogl.OGLInitialize()
            INITIALIZED = True
        maxWidth  = 10000
        maxHeight = 10000

        ogl.ShapeCanvas.__init__(self, parent,size=(maxWidth,maxHeight),**keyw)
        self.SetScrollbars(20, 20, maxWidth/20, maxHeight/20)

        self.parent = parent
        self.frame = self#frame
        self.SetBackgroundColour(wx.WHITE)
        self.diagram = ogl.Diagram()
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = []
        self.save_gdi = []
        
    def DrawUml(self,classes={},between=20):
        """Draws the uml diagram"""
        #verify all hierachies
        rows        = [[] for x in range(len(classes)+2)]
        for name, u in classes.items():
            if not u.verified:
                u.getHierarchy(classes)
            rows[u.hierarchy].append(u)
        #draw uml
        shapes              = {}
        dc              = wx.ClientDC(self)
        self.PrepareDC(dc)
        
        self.diagram.DeleteAllShapes()
        total_height        = total_width   = y = between

        for row in rows:
            if row:
                x           = between
                height      = 0
                for u in row:
                    shape   = u.wx(self)
                    shapes[u.name.split('(')[0]]  = shape
                    ds      = self.__addShape(shape, x, y, '')
                    x       += between+shape.width
                    height  = max(height,shape.height)
                    for parent in u.parents:
                        if shapes.has_key(parent):
                            line = ogl.LineShape()
                            line.SetCanvas(self)
                            line.SetPen(wx.BLACK_PEN)
                            line.SetBrush(wx.BLACK_BRUSH)
                            line.AddArrow(ogl.ARROW_ARROW)
                            line.MakeLineControlPoints(2)
                            shapes[parent].AddLine(line, shape)
                            self.diagram.AddShape(line)
                            line.Show(True)
                width       = int(x+between)
                height      = int(height+3*between)
                total_width = max(width,total_width)
                y           += height
                total_height+= height
        total_height        -= 3*between
        self.SetVirtualSize((total_width, total_height))
        self.SetScrollRate(20,20)
        #self.SetCursor(wx.StockCursor(wx.CURSOR_MAGNIFIER))

    def __addShape(self, shape, x, y, text):
        # Composites have to be moved for all children to get in place
        if isinstance(shape, ogl.CompositeShape):
            dc = wx.ClientDC(self)
            self.PrepareDC(dc)
            shape.Move(dc, x, y)
        else:
            shape.SetDraggable(True, True)
        shape.SetCanvas(self)
        shape.Goto(x,y)
        if text:
            for line in text.split('\n'):
                shape.AddText(line)
        shape.SetShadowMode(ogl.SHADOW_RIGHT)
        self.diagram.AddShape(shape)
        shape.Show(True)

        evthandler = wxEvtHandler(self.frame)
        evthandler.SetShape(shape)
        evthandler.SetPreviousHandler(shape.GetEventHandler())
        shape.SetEventHandler(evthandler)

        self.shapes.append(shape)
        return shape

    def OnBeginDragLeft(self, x, y, keys):
        pass
        #self log.write("OnBeginDragLeft: %s, %s, %s\n" % (x, y, keys))

    def OnEndDragLeft(self, x, y, keys):
        pass
        #self log.write("OnEndDragLeft: %s, %s, %s\n" % (x, y, keys))

class wxEvtHandler(ogl.ShapeEvtHandler):
    def __init__(self, frame):
        ogl.ShapeEvtHandler.__init__(self)
        self.statbarFrame = frame

    def OnLeftClick(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        dc = wx.ClientDC(canvas)
        canvas.PrepareDC(dc)

        if shape.Selected():
            shape.Select(False, dc)
            canvas.Redraw(dc)
        else:
            redraw = False
            shapeList = canvas.GetDiagram().GetShapeList()
            toUnselect = []
            for s in shapeList:
                if s.Selected():
                    # If we unselect it now then some of the objects in
                    # shapeList will become invalid (the control points are
                    # shapes too!) and bad things will happen...
                    toUnselect.append(s)
            shape.Select(True, dc)
            if toUnselect:
                for s in toUnselect:
                    s.Select(False, dc)
                canvas.Redraw(dc)

    def OnEndDragLeft(self, x, y, keys=0, attachment=0):
        shape = self.GetShape()
        ogl.ShapeEvtHandler.OnEndDragLeft(self, x, y, keys, attachment)
        if not shape.Selected():
            self.OnLeftClick(x, y, keys, attachment)

    def OnSizingEndDragLeft(self, pt, x, y, keys, attch):
        ogl.ShapeEvtHandler.OnSizingEndDragLeft(self, pt, x, y, keys, attch)

    def OnMovePost(self, dc, x, y, oldX, oldY, display):
        ogl.ShapeEvtHandler.OnMovePost(self, dc, x, y, oldX, oldY, display)

    def OnRightClick(self, dc, *dontcare):

        pass
        
if __name__=='__main__':
    import sm.wxp
    u = Class()
    u.append('mmmm')
    u.append('test')
    u.append('test')
    u.append('test')
    u.append('haha',SEPARATOR)
    u.append('test')
    u.append('test')
    u.append('test')
    
    sm.wxp.panelApp(wxCanvas,classes=[u,u])
