#!BPY

"""
Name: 'Stani Python Editor'
Blender: 235
Group: 'Misc'
Tooltip: 'Python IDE for Blender'
"""

__author__ = "Stani Michiels"
__url__ = ("http://spe.pycs.net/","http://projects.blender.org/projects/spe/")
__version__ = "0.6"
__bpydoc__ = """\
This script opens the SPE (Stani's Python Editor).

Spe is a python IDE with auto-indentation, auto completion,
call tips, syntax coloring, syntax highlighting, class
explorer, source index, auto todo list, sticky notes,
integrated pycrust shell, python file browser, recent file
browser, drag&drop, context help, ... Special is its blender
support with a blender 3d object browser and its ability to
run interactively inside blender. Spe ships with wxGlade (gui
designer), PyChecker (source code doctor) and Kiki (regular
expression console). Spe is extensible with wxGlade.

For more info see http://spe.pycs.net
"""

#copy this script to the .blender/scripts directory
import sys
try:
  import site
  sys.path+=site.sitedirs
except:
  pass
import _spe.SPE
_spe.SPE.main() 
