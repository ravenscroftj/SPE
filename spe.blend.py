#Press here Alt-P to launch SPE

#For more info visit http://www.stani.be/python/spe

#wxPython is required (download from www.wxpython.org)
import os,sys
site_packages   = os.path.join(sys.prefix,'Lib','site-packages')
wx_pth          = os.path.join(site_packages,'wx.pth')
if os.path.exists(wx_pth):
  sys.path.append(os.path.join(sys.prefix,'Lib','site-packages',open(wx_pth).read()))

#start SPE!
import _spe.SPE