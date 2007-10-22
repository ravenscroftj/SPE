#!BPY

#"""
#Name: 'Attach the Winpdb debugger'
#Blender: 243
#Group: 'System'
#Tooltip: 'Enables a Python debugger for Blender scripts'
#"""

__author__ = "Nir Aides"
__url__ = ("http://www.digitalpeers.com/pythondebugger")
__version__ = "1.22"
__email__ = ("witold.jaworski@tadmar.com.pl")
__bpydoc__ = """\
Winpdb, created by Nir Aides, is a platform independent GPL Python debugger,<br>
with support for:<br>
- multiple threads,<br>
- namespace modification,<br>
- embedded debugging <br>
  (and because of that it is suitable to use for Blender Python scripts),

and is up to 20 times faster than pdb.<br>

This small script, written by Witold Jaworski, enables WinPdb to debug Python 
scripts that are running inside Blender.<br>
It opens the Winpdb, and attaches it to the Blender Python environment.

IMPORTANT: <br>
When WinPdb window is opened for the first time after call to this program,
you have to press F5 (Continue), to let Blender to continue (to "unfreeze" 
its screen).

USAGE:
To break into a script:<br>
	- press "Break" button in WinPdb;
	- load the script to Blender's Text Editor;
	- run the script, pressing Alt-P

The WindPdb window will appear. You can debug your script there.
The WinPdb should be attached to the Blender only once per session. You can 
control, wheter the code has or not have to be debugged, by pressing the WinPdb 
"break" command.<br>
Remember: you will not be able to attach second time the WinPdb to the same 
session. So use it by setting the break mode when it is needed, and detach
it just before closing the Blender session.
"""
#copy this script to the .blender/scripts directory


#helper parameters - usually you do not need to change them:
WAIT_TIMEOUT  = 15  #time that this script will wait for attaching a Winpdb program instance
PASSWORD	  = 'blender' #password, that should be used in WinPdb


import rpdb2
import os
import sys
import subprocess

def debug(what):
	"""
		Opens the WinPdb window with Blender script attached to it.
		Arguments:
		what - name of the script text, as is visible at WinPdb
	"""
	#WinPdb arguments : attach to <what>, with given password:
	#I am very sorry, that I was not able to use the os.executable field
	#but the explicite Python executable name. It is because inside Blender
	#the os.executable points to Blender.exe, not the Python executable.
	#This makes this script useful for Windows, only.
	#I welcome anybody to prepare an Linux version! 
	args = ["pythonw.exe", \
			os.path.join(os.path.dirname(rpdb2.__file__),"winpdb.py"), \
			"-a", \
			"-p" + PASSWORD, \
			what]
	#Run WinPdb...
	pid = subprocess.Popen(args)
	#....and let it to connect, waiting for <timeout> seconds:
	rpdb2.start_embedded_debugger(PASSWORD, \
								  fAllowUnencrypted = True, \
								  timeout = WAIT_TIMEOUT)

debug("<string>") #every script in Blender is represented by such name 