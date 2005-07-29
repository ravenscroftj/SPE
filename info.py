import os,sys,sm.osx

PLATFORM                    = sys.platform
WIN                         = PLATFORM.startswith('win')
DARWIN                      = PLATFORM.startswith('darwin')

path=os.path.dirname(__file__)
INFO={
    'author'           : "www.stani.be",
    'title'            : "SPE",
    'date'             : "13-9-2003",
    'doc'              : "%(titleFull)s\n\n%(description)s\n\n%(links)s\n\n%(requirements)s\n\n%(copyright)s",
    'version'          : "0.7.4.x",
    'blenderVersion'   : "2.35",
    'pyVersion'        : "2.3",
    'pyVersionC'       : sys.version.split(' ')[0],
    'wxVersion'        : "2.6.1.0.",
    'location'         : path,
    'blenpyLocation'   : path.replace('_spe','blenpy'),
    'smLocation'       : path.replace('_spe','sm'),
    'smIdleLocation'   : path.replace('_spe','sm'),
    'userPath'         : sm.osx.userPath('.spe'),
}


INFO['defaults']     = os.path.join(INFO['location'],'defaults.cfg')
INFO['defaultsUser'] = os.path.join(INFO['userPath'],'defaults.cfg')

INFO['titleFull']    = "%(title)s %(version)s"%INFO

INFO['links']=\
"""Homepage : http://spe.pycs.net
Website  : http://projects.blender.org/projects/spe/
Forum    : http://projects.blender.org/forum/?group_id=30
Contact  : http://www.pycs.net/system/mailto.py?usernum=0000167"""

INFO['description']=\
"""Stani's Python Editor

Spe is a python IDE with auto-indentation, auto completion, call tips, syntax
coloring, syntax highlighting, class explorer, source index, auto todo list,
sticky notes, integrated pycrust shell, python file browser, recent file
browser, drag&drop, context help, ... Special is its blender support with a
blender 3d object browser and its ability to run interactively inside blender.
Spe is extensible with boa.

Wanted: wxpython programmers to extend spe's features, feel free to do a proposal.

For more information, see spe/doc/manual.html"""%INFO

INFO['requirements']=\
"""Python   v%(pyVersion)s      required
wxPython v%(wxVersion)s required
Blender  v%(blenderVersion)s     optional"""%INFO

INFO['copyright']=\
"""Copyright (C)%(author)s (%(date)s)

This library is released under the GPL, except from the sm.* library.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""%INFO

WILDCARD = "Python (*.py;*.pyw;*.tpy)|*.py;*.pyw;*.tpy|All files (*)|*"
WILDCARD_EXTENDED = WILDCARD+'|Python All(*.py;*.pyw;*.tpy;*.pyc;*.pyd;*.pyo)|*.py;*.pyw;*.tpy;*.pyc;*.pyd;*.pyo|Text (*.txt;*.rtf;*.htm;*.html;*.pdf)|*.txt;*.rtf;*.htm;*.html;*.pdf|Bitmap (*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.png;*.pic)|*.jpg;*.jpeg;*.bmp;*.tif;*.tiff;*.png;*.pic|Vector (*.dxf;*.dwg;*.svg;*.swf;*.vrml;*.wrl)|*.dxf;*.dwg;*.svg;*.swf;*.vrml;*.wrl'

# TH 2003/10/16:
# Check if someone is root (uid=0) on unix and therefore
# might not be able to access the Xserver.
    # Is there a better solution to check if somebody has
# access to it or not?
isnotroot=True
try:
    # again os.getuid() exists only on unix according to documentation
    isnotroot = os.getuid()
except:
    pass
if isnotroot:
    import wx
    INFO['encoding']    = wx.GetDefaultPyEncoding()
    INFO['wxVersionC']  = '.'.join([str(x)for x in wx.VERSION])

__doc__=INFO['doc']%INFO

def copy():
    return INFO.copy()



