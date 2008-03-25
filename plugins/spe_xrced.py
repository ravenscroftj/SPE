import os, sys

try:
    from wx.tools.XRCed import xrced
except ImportError:
    from plugins.XRCed import xrced

parent_path = os.path.dirname(os.path.dirname(xrced.__file__))
sys.path.append(parent_path)
xrced.main()