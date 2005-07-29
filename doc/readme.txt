Spe registers itself automatically during setup in the window explorer context menu for '.py' and '.pyw' files.  If this would fail, you can always do it manually...
   
In Windows you can associate Spe as an editor for .py files.  This adds 'Edit with Spe' as a menu item in the context pop-up of the Windows Explorer.

In the Windows Explorer choose Tools->Folder Options
On the Dialog notebook, click File Types page.
Select PY extension in file types list.
Click the Advanced button to create a new action.
Action:
Edit with Spe
Application uses to perform action:
absolute\path\to\python.exe absolute\path\to\spe.py "%1"
OK all the dialogs