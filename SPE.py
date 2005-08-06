import info
INFO=info.copy()

INFO['description']=\
"""This is the main SPE application created with SPE and wxGlade."""
__doc__=INFO['doc']%INFO
    
print """
SPE v%s (c)2003-2005 www.stani.be

If spe fails to start:
 - type "python SPE.py --debug > debug.txt 2>&1" at the command prompt
 - send debug.txt with some info to s_t_a_n_i@yahoo.com
 """%(INFO['version'],)
 
####Import Modules

#---General
import ConfigParser, sys, os, wx
import sm.wxp.smdi as smdi
import Menu,Parent,Child

#---Blender
print "Blender support",
try:
    import Blender
    redraw      = Blender.Redraw
    print 'enabled.'
except ImportError:
    Blender     = None
    redraw      = None
    print 'disabled (run SPE inside Blender to enable).'
    
#---Crypto
try:
    from Crypto.Cipher import DES
    fCrypto = True
    print "Encrypted debugging enabled.\n"
except ImportError:
    fCrypto = False
    print """\nEncrypted debugging disabled. 
  If you prefer encrypted debugging, install the "Python Cryptography Toolkit"
  from http://www.amk.ca/python/code/crypto\n"""

####Constants
MDI         = 0
DEBUG       = 0
IMAGE_PATH  = os.path.join(info.path,'skins','default')

####Command line arguments
openFiles = []
if DEBUG:
    __debug     = DEBUG
elif 'argv' in dir(sys):
    commandLine = sys.argv[1:]
    __debug     =('--debug' in commandLine)
    openFiles   = [x for x in commandLine if x[:2]!= '--']
else:
    __debug=DEBUG
    openFiles   = []

####Preferences
config=ConfigParser.ConfigParser()
config.readfp(open(INFO['defaults']))
try:
    config.read(INFO['defaultsUser'])
except:
    print 'Spe warning: could not load user options'

#---Maximize    
style   = smdi.STYLE_PARENTFRAME
try:
    maximize=eval(config.get("DEFAULT","maximize"))
except:
    maximize=True
if maximize: style |= wx.MAXIMIZE

#---Size
try:
    sizeX   = int(config.get("DEFAULT","sizex"))
    sizeY   = int(config.get("DEFAULT","sizey"))
    posX    = max(0,int(config.get("DEFAULT","posx")))
    posY    = max(0,int(config.get("DEFAULT","posy")))
except:
    sizeX   = 800
    sizeY   = 600
    posX    = 0
    posY    = 0
    
#---MDI
mdi         = config.get('DEFAULT','Mdi')
if not smdi.DI.has_key(mdi):
    mdi     = smdi.DEFAULT
    config.set('DEFAULT','Mdi',mdi)
        
####Shortcuts
class Translate:
    def __init__(self,keys):
        self.keys = keys
        
    def __call__(self,entry):
        entry           = entry.split('\t')
        if len(entry)==2:
            label, shortcut = entry
        else:
            label           = entry[0]
            shortcut        = ''
        l               = self.strip(label)
        if self.keys.has_key(l):
            shortcut    = self.keys[l]
        if shortcut:
            return '%s\t%s'%(label,shortcut)
        else:
            return label
            
    def strip(self,x):
        return x.replace('&','').replace('.','')
        
shortcuts    = config.get("DEFAULT","shortcuts")
if shortcuts == smdi.DEFAULT:
    if smdi.DARWIN:
        _shortcuts  = 'Macintosh'
    else:
        _shortcuts  = 'Windows'
else:
    _shortcuts      = shortcuts
import _spe.shortcuts as sc
execfile(os.path.join(os.path.dirname(sc.__file__),'%s.py'%_shortcuts))
import wxgMenu
wxgMenu._   = Translate(keys)

#---feedback
if __debug:
    print """Spe is running in debugging mode with this configuration:
- platform  : %s
- python    : %s
- wxPython  : %s
- interface : %s
- encoding  : %s
"""%(smdi.PLATFORM,INFO['pyVersionC'],INFO['wxVersionC'],mdi,INFO['encoding'])
    
####Application
app = smdi.App(\
        ParentPanel     = Parent.Panel,
        ChildPanel      = Child.Panel,
        MenuBar         = Menu.Bar,
        ToolBar         = Menu.Tool,
        StatusBar       = Menu.Status,
        Palette         = Menu.Palette,
        mdi             = mdi,
        debug           = __debug,
        fCrypto         = fCrypto,
        title           = 'SPE %s'%INFO['version'],
        panelFrameTitle = 'Shell',
        redraw          = redraw,
        Blender         = Blender,
        openFiles       = openFiles,
        size            = wx.Size(sizeX,sizeY),
        config          = config,
        pos             = wx.Point(posX,posY),
        shortcuts       = shortcuts,
        imagePath       = IMAGE_PATH,
        style           = style)

app.MainLoop()

print "\nThank you for using SPE, please donate to support further development."

