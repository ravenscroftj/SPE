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

and is up to 20 times faster than pdb.

This small script, written by Witold Jaworski, enables WinPdb to debug Python
scripts that are running inside Blender.<br>
It opens the Winpdb, and attaches it to the Blender Python environment.

IMPORTANT: <br>
When WinPdb window is opened for the first time in a Blender session, you have
to press F5 (Continue) in WinPdb, to let Blender to continue (to "unfreeze" its
 screen).

USAGE:<br>
To break into a script:<br>
    - press "Break" button in WinPdb;<br>
    - load the script to Blender's Text Editor;<br>
    - run the script, pressing Alt-P

The WindPdb window will appear. You can debug your script there.
The WinPdb should be attached to the Blender only once per session. You can
control, wheter the code has or not have to be debugged, by pressing the WinPdb
"break" command button.

Remember: Use Winpdb by setting the break mode when it is needed, as long, as you
run Blender session. Always close Blender first, unless you have detached the WinPdb
before (using "Detach" command from the File menu - it is preffered way, but not
 required). When you close Winpdb WITHOUT detaching it, Blender.exe will crash
during shutdown. (Because in such case Winpdb tries to stop Blender's Python
engine).
"""
#copy this script to the .blender/scripts directory


#helper parameters - usually you do not need to change them:
WAIT_TIMEOUT  = 15  #time that this script will wait for attaching a Winpdb program instance
PASSWORD      = 'blender' #password, that should be used in WinPdb


import os
import sys
import subprocess
#import rpdb2: delcalred below (because it requires an implicit search path)

def debug(what):
    """
        Opens the WinPdb window with Blender script attached to it.
        Arguments:
        what - name of the script text, as is visible at WinPdb
    """
    #WinPdb arguments : attach to <what>, with given password:
    if sys.platform == "win32":
        #I am very sorry, that I was not able to use the os.executable field
        #but the explicite Python executable name. It is because inside Blender
        #the os.executable points to Blender.exe, not the Python executable.
        args = ["pythonw.exe"]
    else:#in linux theres no need to prefix the interpreter: winpdb.py run itself!
        # Maybe this line should look like: args = ["python"]? I have not tested it
        args = []

    #I have no possibility to test it, but it should work for Linux, also:
    args.extend([os.path.join(os.path.dirname(rpdb2.__file__),"winpdb.py"), \
                "-a", \
                "-p" + PASSWORD, \
                what])
    #Run WinPdb...
    pid = subprocess.Popen(args)
    #....and let it to connect, waiting for <timeout> seconds:
    rpdb2.start_embedded_debugger(PASSWORD, \
                                  fAllowUnencrypted = True, \
                                  timeout = WAIT_TIMEOUT)

if not sys.modules.has_key('rpdb2'): #first call: rpdb2 is not imported, yet.
    import _spe #import this just to find the proper SPE directory
    #then we have to add the Winpdb directory to PYTHONPATH:
    #in the lines below I am trying to create the winpdb path in a
    #system - independent way :)
    winpdbdir = os.path.dirname(_spe.__file__) #take the _spe directory...
    winpdbdir = os.path.join(winpdbdir, "plugins") #... append /plugins ...
    winpdbdir = os.path.join(winpdbdir, "winpdb")  #.. and /winpdb.
    #OK, let's append it to actual PYTHONPATH...
    sys.path.append(winpdbdir)
    #...just to import the rpdb2, because it requires an implicit search path!
    import rpdb2

    debug("<string>") #every script in Blender is represented by such name

else: #Winpdb cannot be connected for second time (embedded rpdb2 is not responding):
    import Blender
    Blender.Draw.PupMenu("Cannot run Winpdb:%t|You can run Winpdb during Blender session only once. Close Blender and run it again.")
