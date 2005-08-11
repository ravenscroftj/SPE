#! /usr/bin/env python

"""
    rpdb2.py

    A remote Python debugger for Python 2.3 and Python 2.4

    Copyright (C) 2005 Nir Aides

    This program is free software; you can redistribute it and/or modify it 
    under the terms of the GNU General Public License as published by the 
    Free Software Foundation; either version 2 of the License, or any later 
    version.

    This program is distributed in the hope that it will be useful, 
    but WITHOUT ANY WARRANTY; without even the implied warranty of 
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
    See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along 
    with this program; if not, write to the Free Software Foundation, Inc., 
    59 Temple Place, Suite 330, Boston, MA 02111-1307 USA    
"""

COPYRIGHT_NOTICE = """Copyright (C) 2005 Nir Aides"""

LICENSE_NOTICE = """
This program is free software; you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the 
Free Software Foundation; either version 2 of the License, or any later 
version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

A copy of the GPL with the precise terms and conditions for 
copying, distribution and modification follow:
"""

COPY_OF_THE_GPL_LICENSE = """
TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

0. 
This License applies to any program or other work which contains a notice 
placed by the copyright holder saying it may be distributed under the terms 
of this General Public License. The "Program", below, refers to any such 
program or work, and a "work based on the Program" means either the Program 
or any derivative work under copyright law: that is to say, a work containing 
the Program or a portion of it, either verbatim or with modifications and/or 
translated into another language. (Hereinafter, translation is included 
without limitation in the term "modification".) Each licensee is addressed 
as "you".

Activities other than copying, distribution and modification are not covered 
by this License; they are outside its scope. The act of running the Program 
is not restricted, and the output from the Program is covered only if its 
contents constitute a work based on the Program (independent of having been 
made by running the Program). Whether that is true depends on what the 
Program does.

1. 
You may copy and distribute verbatim copies of the Program's source code as 
you receive it, in any medium, provided that you conspicuously and 
appropriately publish on each copy an appropriate copyright notice and 
disclaimer of warranty; keep intact all the notices that refer to this 
License and to the absence of any warranty; and give any other recipients of 
the Program a copy of this License along with the Program.

You may charge a fee for the physical act of transferring a copy, and you 
may at your option offer warranty protection in exchange for a fee.

2. 
You may modify your copy or copies of the Program or any portion of it, thus 
forming a work based on the Program, and copy and distribute such modifications 
or work under the terms of Section 1 above, provided that you also meet all 
of these conditions:

    a) You must cause the modified files to carry prominent notices stating 
    that you changed the files and the date of any change.

    b) You must cause any work that you distribute or publish, that in whole 
    or in part contains or is derived from the Program or any part thereof, 
    to be licensed as a whole at no charge to all third parties under the 
    terms of this License.

    c) If the modified program normally reads commands interactively when 
    run, you must cause it, when started running for such interactive use in 
    the most ordinary way, to print or display an announcement including an 
    appropriate copyright notice and a notice that there is no warranty (or 
    else, saying that you provide a warranty) and that users may redistribute 
    the program under these conditions, and telling the user how to view a 
    copy of this License. (Exception: if the Program itself is interactive 
    but does not normally print such an announcement, your work based on the 
    Program is not required to print an announcement.)

These requirements apply to the modified work as a whole. If identifiable 
sections of that work are not derived from the Program, and can be reasonably 
considered independent and separate works in themselves, then this License, 
and its terms, do not apply to those sections when you distribute them as 
separate works. But when you distribute the same sections as part of a whole 
which is a work based on the Program, the distribution of the whole must be 
on the terms of this License, whose permissions for other licensees extend to 
the entire whole, and thus to each and every part regardless of who wrote it.

Thus, it is not the intent of this section to claim rights or contest your 
rights to work written entirely by you; rather, the intent is to exercise the 
right to control the distribution of derivative or collective works based on 
the Program.

In addition, mere aggregation of another work not based on the Program with 
the Program (or with a work based on the Program) on a volume of a storage or 
distribution medium does not bring the other work under the scope of this 
License.

3. You may copy and distribute the Program (or a work based on it, under 
Section 2) in object code or executable form under the terms of Sections 1 
and 2 above provided that you also do one of the following:

    a) Accompany it with the complete corresponding machine-readable source 
    code, which must be distributed under the terms of Sections 1 and 2 above 
    on a medium customarily used for software interchange; or,

    b) Accompany it with a written offer, valid for at least three years, to 
    give any third party, for a charge no more than your cost of physically 
    performing source distribution, a complete machine-readable copy of the 
    corresponding source code, to be distributed under the terms of Sections 
    1 and 2 above on a medium customarily used for software interchange; or,

    c) Accompany it with the information you received as to the offer to 
    distribute corresponding source code. (This alternative is allowed only 
    for noncommercial distribution and only if you received the program in 
    object code or executable form with such an offer, in accord with 
    Subsection b above.)

The source code for a work means the preferred form of the work for making 
modifications to it. For an executable work, complete source code means all 
the source code for all modules it contains, plus any associated interface 
definition files, plus the scripts used to control compilation and 
installation of the executable. However, as a special exception, the source 
code distributed need not include anything that is normally distributed (in 
either source or binary form) with the major components (compiler, kernel, 
and so on) of the operating system on which the executable runs, unless that 
component itself accompanies the executable.

If distribution of executable or object code is made by offering access to 
copy from a designated place, then offering equivalent access to copy the 
source code from the same place counts as distribution of the source code, 
even though third parties are not compelled to copy the source along with 
the object code.

4. You may not copy, modify, sublicense, or distribute the Program except as 
expressly provided under this License. Any attempt otherwise to copy, modify, 
sublicense or distribute the Program is void, and will automatically 
terminate your rights under this License. However, parties who have received 
copies, or rights, from you under this License will not have their licenses 
terminated so long as such parties remain in full compliance.

5. You are not required to accept this License, since you have not signed it. 
However, nothing else grants you permission to modify or distribute the 
Program or its derivative works. These actions are prohibited by law if you 
do not accept this License. Therefore, by modifying or distributing the 
Program (or any work based on the Program), you indicate your acceptance of 
this License to do so, and all its terms and conditions for copying, 
distributing or modifying the Program or works based on it.

6. Each time you redistribute the Program (or any work based on the Program), 
the recipient automatically receives a license from the original licensor to 
copy, distribute or modify the Program subject to these terms and conditions. 
You may not impose any further restrictions on the recipients' exercise of 
the rights granted herein. You are not responsible for enforcing compliance 
by third parties to this License.

7. If, as a consequence of a court judgment or allegation of patent 
infringement or for any other reason (not limited to patent issues), 
conditions are imposed on you (whether by court order, agreement or otherwise) 
that contradict the conditions of this License, they do not excuse you from 
the conditions of this License. If you cannot distribute so as to satisfy 
simultaneously your obligations under this License and any other pertinent 
obligations, then as a consequence you may not distribute the Program at all. 
For example, if a patent license would not permit royalty-free redistribution 
of the Program by all those who receive copies directly or indirectly through 
you, then the only way you could satisfy both it and this License would be to 
refrain entirely from distribution of the Program.

If any portion of this section is held invalid or unenforceable under any 
particular circumstance, the balance of the section is intended to apply and 
the section as a whole is intended to apply in other circumstances.

It is not the purpose of this section to induce you to infringe any patents 
or other property right claims or to contest validity of any such claims; 
this section has the sole purpose of protecting the integrity of the free 
software distribution system, which is implemented by public license 
practices. Many people have made generous contributions to the wide range of 
software distributed through that system in reliance on consistent 
application of that system; it is up to the author/donor to decide if he or 
she is willing to distribute software through any other system and a licensee 
cannot impose that choice.

This section is intended to make thoroughly clear what is believed to be a 
consequence of the rest of this License.

8. If the distribution and/or use of the Program is restricted in certain 
countries either by patents or by copyrighted interfaces, the original 
copyright holder who places the Program under this License may add an 
explicit geographical distribution limitation excluding those countries, 
so that distribution is permitted only in or among countries not thus 
excluded. In such case, this License incorporates the limitation as if 
written in the body of this License.

9. The Free Software Foundation may publish revised and/or new versions of 
the General Public License from time to time. Such new versions will be 
similar in spirit to the present version, but may differ in detail to 
address new problems or concerns.

Each version is given a distinguishing version number. If the Program 
specifies a version number of this License which applies to it and 
"any later version", you have the option of following the terms and 
conditions either of that version or of any later version published by the 
Free Software Foundation. If the Program does not specify a version number 
of this License, you may choose any version ever published by the 
Free Software Foundation.

10. If you wish to incorporate parts of the Program into other free programs 
whose distribution conditions are different, write to the author to ask for 
permission. For software which is copyrighted by the Free Software 
Foundation, write to the Free Software Foundation; we sometimes make 
exceptions for this. Our decision will be guided by the two goals of 
preserving the free status of all derivatives of our free software and of 
promoting the sharing and reuse of software generally.

NO WARRANTY

11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO WARRANTY FOR 
THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW. EXCEPT WHEN OTHERWISE 
STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE 
PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, 
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND 
PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, 
YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING 
WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR 
REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, 
INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING 
OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO 
LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR 
THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER 
PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE 
POSSIBILITY OF SUCH DAMAGES.

END OF TERMS AND CONDITIONS
"""



import SimpleXMLRPCServer 
import SocketServer
import xmlrpclib
import threading
import linecache
import traceback
import compiler
import __main__
import cPickle
import httplib
import os.path
import socket
import getopt
import string
import thread
import random
import base64
import atexit
import time
import copy
import hmac
import sys
import cmd
import md5
import os

try:
    from Crypto.Cipher import DES
except ImportError:
    pass

try:
    from nt import _getfullpathname
except ImportError:
    pass

    

#
#--------------------------------- Export functions ------------------------------
#



TIMEOUT_FIVE_MINUTES = 5 * 60.0



def start_embedded_debugger(pwd, fAllowUnencrypted = False, fRemote = False, timeout = TIMEOUT_FIVE_MINUTES, fDebug = False):
    """
    Use 'start_embedded_debugger' to invoke the debugger engine in embedded 
    scripts. put the following line as the first line in your script:

    import rpdb2; rpdb2.start_embedded_debugger(pwd)

    This will cause the script to freeze until a debugger console attaches.

    pwd - The password that governs security of client/server communication
    fAllowUnencrypted - Allow unencrypted communications. Communication will
        be authenticated but encrypted only if possible.
    fRemote - Allow debugger consoles on remote machines to connect.
    timeout - Seconds to wait for attachment before giving up. If None, 
              never give up.
    fDebug  - debug output.

    IMPORTNAT SECURITY NOTE:
    USING A HARDCODED PASSWORD MAY BE UNSECURE SINCE ANYONE WITH READ
    PERMISSION TO THE SCRIPT WILL BE ABLE TO READ THE PASSWORD AND CONNECT TO 
    THE DEBUGGER AND DO WHATEVER THEY WISH VIA THE 'EXEX' DEBUGGER COMMAND.

    It is safer to use: start_embedded_debugger_interactive_password()    
    """

    return __start_embedded_debugger(pwd, fAllowUnencrypted, fRemote, timeout, fDebug)
    


def start_embedded_debugger_interactive_password(fAllowUnencrypted = False, fRemote = False, timeout = TIMEOUT_FIVE_MINUTES, fDebug = False, stdin = sys.stdin, stdout = sys.stdout):
    if g_server != None:
        return

    if stdout != None:
        stdout.write('Please type password:')
        
    pwd = stdin.readline()[:-1]
    
    return __start_embedded_debugger(pwd, fAllowUnencrypted, fRemote, timeout, fDebug)
    


def settrace():
    """
    Trace threads created with thread.start_new_thread()
    To trace, call this function from the thread target function.
    
    NOTE: The main thread and any threads created with the threading module are
    automatically traced, and there is no need to invoke this function for 
    them. 
    """

    return __settrace()


    
#
#----------------------------------- Interfaces ----------------------------------
#



RPDB_VERSION = "RPDB_2_0_1"



def get_version():
    return RPDB_VERSION


    
def get_interface_compatibility_version():
    return RPDB_VERSION

    

class CSessionManager:
    """
    Interface to the session manager.
    This is the interface through which the debugger controls and communicates
    with the debuggee.
    """
    
    def __init__(self, pwd, fAllowUnencrypted, fRemote, host):
        self.__smi = CSessionManagerInternal(pwd, fAllowUnencrypted, fRemote, host)

    def report_exception(self, type, value, tb):
        return self.__smi.report_exception(type, value, tb)

    def set_printer(self, printer):
        return self.__smi.set_printer(printer)

    def register_callback(self, callback, event_type_dict, fSingleUse):
        return self.__smi.register_callback(callback, event_type_dict, fSingleUse)

    def remove_callback(self, callback):
        return self.__smi.remove_callback(callback)

    def refresh(self):
        return self.__smi.refresh()

    def launch_nothrow(self, command_line):
        return self.__smi.launch_nothrow(command_line)
        
    def launch(self, command_line):
        return self.__smi.launch(command_line)
        
    def attach_nothrow(self, key):
        return self.__smi.attach_nothrow(key)

    def attach(self, key, name = None):
        return self.__smi.attach(key, name)

    def detach(self):
        return self.__smi.detach()

    def request_break(self):
        return self.__smi.request_break()
    
    def request_go(self):
        return self.__smi.request_go()
    
    def request_go_breakpoint(self, filename, scope, lineno):
        return self.__smi.request_go_breakpoint(filename, scope, lineno)

    def request_step(self):
        return self.__smi.request_step()

    def request_next(self):
        return self.__smi.request_next()

    def request_return(self):
        return self.__smi.request_return()

    def request_jump(self, lineno):
        return self.__smi.request_jump(lineno)
    
    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr):
        return self.__smi.set_breakpoint(filename, scope, lineno, fEnabled, expr)
        
    def disable_breakpoint(self, id_list, fAll):
        return self.__smi.disable_breakpoint(id_list, fAll)
    
    def enable_breakpoint(self, id_list, fAll):
        return self.__smi.enable_breakpoint(id_list, fAll)
    
    def delete_breakpoint(self, id_list, fAll):
        return self.__smi.delete_breakpoint(id_list, fAll)
    
    def get_breakpoints(self):
        return self.__smi.get_breakpoints()
        
    def save_breakpoints(self, _filename = ''):        
        return self.__smi.save_breakpoints()

    def load_breakpoints(self, _filename = ''):
        return self.__smi.load_breakpoints()

    def get_stack(self, tid_list, fAll):   
        return self.__smi.get_stack(tid_list, fAll)

    def get_source_file(self, filename, lineno, nlines): 
        return self.__smi.get_source_file(filename, lineno, nlines)
        
    def get_source_lines(self, nlines, fAll): 
        return self.__smi.get_source_lines(nlines, fAll)
        
    def set_frame_index(self, frame_index):
        return self.__smi.set_frame_index(frame_index)

    def get_frame_index(self):
        return self.__smi.get_frame_index()
        
    def set_analyze(self, fAnalyze):
        return self.__smi.set_analyze(fAnalyze)
        
    def set_host(self, host):
        return self.__smi.set_host(host)

    def get_host(self):
        return self.__smi.get_host()

    def calc_server_list(self):
        return self.__smi.calc_server_list()

    def get_server_info(self):    
        return self.__smi.get_server_info()

    def get_last_debuggee_name_safe(self):
        return self.__smi.get_last_debuggee_name_safe()

    def get_namespace(self, nl, fFilter):
        return self.__smi.get_namespace(nl, fFilter)

    def evaluate(self, expr):
        return self.__smi.evaluate(expr)

    def execute(self, suite):
        return self.__smi.execute(suite)

    def get_state(self):
        return self.__smi.get_state()

    def get_thread_list(self):
        return self.__smi.get_thread_list()
        
    def set_thread(self, tid):
        return self.__smi.set_thread(tid)

    def set_password(self, pwd):
        return self.__smi.set_password(pwd)

    def get_password(self):
        return self.__smi.get_password()

    def get_encryption(self):    
        return self.__smi.get_encryption()

    def set_remote(self, fRemote):
        return self.__smi.set_remote(fRemote)

    def get_remote(self):
        return self.__smi.get_remote()

    def stop_debuggee(self):
        return self.__smi.stop_debuggee()



class CConsole:
    """
    Interface to a debugger console.
    """
    def __init__(self, session_manager, stdin = None, stdout = None, fSplit = False):
        self.m_ci = CConsoleInternal(session_manager, stdin, stdout, fSplit)

    def start(self):
        return self.m_ci.start()

    def join(self):
        return self.m_ci.join()

    def set_filename(self, filename):
        return self.m_ci.set_filename(filename)

    

#
# ----------------------------------------- Exceptions ---------------------------------------
#




class CException(Exception):
    def __init__(self, *args):
        Exception.__init__(self, *args)


    
class InvalidScopeName(CException):
    """
    Invalid scope name.
    This exception may be thrown when a request was made to set a breakpoint
    to an unknown scope.
    """



class BadArgument(CException):
    """
    Bad Argument.
    """



class ThreadNotFound(CException):
    """
    Thread not found.
    """



class NoThreads(CException):
    """
    No Threads.
    """



class ThreadDone(CException):
    """
    Thread Done.
    """



class DebuggerNotBroken(CException):
    """
    Debugger is not broken.
    This exception is thrown when an operation that can only be performed
    while the debuggee is broken, is requested while the debuggee is running.
    """



class InvalidFrame(CException):
    """
    Invalid Frame.
    This exception is raised if an operation is requested on a stack frame
    that does not exist.
    """



class NoExceptionFound(CException):
    """
    No Exception Found.
    This exception is raised when exception information is requested, but no
    exception is found, or has been thrown.
    """

    

class CConnectionException(CException):
    def __init__(self, *args):
        CException.__init__(self, *args)



class BadVersion(CConnectionException):
    """Bad Version."""
    def __init__(self, version):
        CConnectionException.__init__(self)

        self.m_version = version

    def __str__(self):
        return repr(self.m_version)


    
class UnexpectedData(CConnectionException):
    """Unexpected data."""



class AlreadyAttached(CConnectionException):
    """Already Attached."""



class NotAttached(CConnectionException):
    """Not Attached."""



class SpawnUnsupported(CConnectionException):
    """Spawn Unsupported."""



class UnknownServer(CConnectionException):
    """Unknown Server."""



class CSecurityException(CConnectionException):
    def __init__(self, *args):
        CConnectionException.__init__(self, *args)


    
class UnsetPassword(CSecurityException):
    """Unset Password."""


    
class EncryptionNotSupported(CSecurityException):
    """Encryption Not Supported."""



class EncryptionExpected(CSecurityException):
    """Encryption Expected."""


class DecryptionFailure(CSecurityException):
    """Decryption Failure."""



class AuthenticationBadData(CSecurityException):
    """Authentication Bad Data."""



class AuthenticationFailure(CSecurityException):
    """Authentication Failure."""



class AuthenticationBadIndex(CSecurityException):
    """Authentication Bad Index."""
    def __init__(self, max_index, anchor):
        CSecurityException.__init__(self)

        self.m_max_index = max_index
        self.m_anchor = anchor

    def __str__(self):
        return repr((self.m_max_index, self.m_anchor))



#
#------------------------------------- Globals ------------------------------
#

#
# map between OS type and relvant command to initiate a new OS console.
# entries for other OSs can be added here. 
# '%s' serves as a place holder.
#
osSpawn = {
    'nt': 'start "rpdb2 - Version ' + get_version() + ' - Debugee Console" cmd /k %s %s', 
    'posix': 'xterm -e %s %s &', 
    'mac': '%s %s',
    'screen': 'screen -t debugger_console python %s'
}



IDLE_MAX_RATE = 2.0
PING_TIMEOUT = 4.0

WAIT_FOR_BREAK_TIMEOUT = 1.0

STARTUP_TIMEOUT = 3.0
STARTUP_RETRIES = 3

LOCAL_HOST = "localhost"
SERVER_PORT_RANGE_START = 51000
SERVER_PORT_RANGE_LENGTH = 20

ERROR_SOCKET_ADDRESS_IN_USE_WIN = 10048
ERROR_SOCKET_ADDRESS_IN_USE_UNIX = 98

SOURCE_EVENT_CALL = 'C'
SOURCE_EVENT_LINE = 'L'
SOURCE_EVENT_RETURN = 'R'
SOURCE_EVENT_EXCEPTION = 'E'
SOURCE_STATE_UNBROKEN = '*'
SOURCE_BP_ENABLED = 'B'
SOURCE_BP_DISABLED = 'D'

SYMBOL_MARKER = '>'
SYMBOL_ALL = '*'
SOURCE_MORE = '+'
SOURCE_LESS = '-'
SOURCE_ENTIRE_FILE = '^'
CONSOLE_PRINTER = '*** '
CONSOLE_WRAP_INDEX = 78
CONSOLE_PROMPT = '\n> '
CONSOLE_PROMPT_ANALYZE = '\nAnalayze> '
CONSOLE_INTRO = ("""RPDB - The Remote Python Debugger, version %s,
Copyright (C) 2005 Nir Aides.
Type "help", "copyright", "license" for more information.""" % (RPDB_VERSION))

PRINT_NOTICE_PROMPT = "Hit Return for more, or q (and Return) to quit:"
PRINT_NOTICE_LINES_PER_SECTION = 20

STR_NO_THREADS = "Operation failed since no traced threads were found."
STR_AUTOMATIC_LAUNCH_UNKNOWN = "RPDB doesn't know how to launch a new terminal on this platform. Please start the debuggee manually with the -d flag on a seperate console and then use the 'attach' command to attach to it."
STR_STARTUP_NOTICE = "Attaching to debuggee..."
STR_STARTUP_SPAWN_NOTICE = "Spawning debuggee..."
STR_KILL_NOTICE = "Stopping debuggee..."
STR_STARTUP_FAILURE = "Debugee failed to start in a timely manner."
STR_OUTPUT_WARNING = "Textual output will be done at the debugee."
STR_ANALYZE_GLOBALS_WARNING = "In analyze mode the globals and locals dictionaries are read only."
STR_GLOBALS_WARNING = "Any changes made to the globals dictionay at this frame will be discarded."
STR_BREAKPOINTS_LOADED = "Breakpoints were loaded."
STR_BREAKPOINTS_SAVED = "Breakpoints were saved."
STR_BREAKPOINTS_NOT_SAVED = "Breakpoints were not saved."
STR_BREAKPOINTS_FILE_NOT_FOUND = "Breakpoints file was not found." 
STR_BAD_FILENAME = "Bad File Name."
STR_SOME_BREAKPOINTS_NOT_LOADED = "Some breakpoints were not loaded, because of an error."
STR_BAD_EXPRESSION = "Bad expression '%s'."
STR_FILE_NOT_FOUND = "File '%s' not found."
STR_EXCEPTION_NOT_FOUND = "No exception was found."
STR_SCOPE_NOT_FOUND = "Scope '%s' not found."
STR_NO_SUCH_BREAKPOINT = "Breakpoint not found."
STR_THREAD_NOT_FOUND = "Thread was not found."
STR_NO_THREADS_FOUND = "No threads were found."
STR_THREAD_NOT_BROKEN = "Thread is not broken."
STR_THREAD_FOCUS_SET = "Focus was set to chosen thread."
STR_ILEGAL_ANALYZE_MODE_ARG = "Argument is not allowed in analyze mode. Type 'help analyze' for more info."
STR_ILEGAL_ANALYZE_MODE_CMD = "Command is not allowed in analyze mode. Type 'help analyze' for more info."
STR_ANALYZE_MODE_TOGGLE = "Analyze mode was set to %s."
STR_BAD_ARGUMENT = "Bad Argument."
STR_DEBUGGEE_TERMINATED = "Debuggee has terminated."
STR_DEBUGGEE_NOT_BROKEN = "Debuggee has to be broken, to complete this command."
STR_DEBUGGER_HAS_BROKEN = "Debuggee has broken (waiting further commands)."
STR_ALREADY_ATTACHED = "Already attached. Detach from debuggee and try again."
STR_NOT_ATTACHED = "Not attached to any script. Attach to a script and try again."
STR_COMMUNICATION_FAILURE = "Failed to communicate with debugged script."
STR_BAD_VERSION = "A debuggee was found that uses incompatible version (%s) of RPDB2."
STR_BAD_VERSION2 = "While attempting to find the specified debuggee at least one debuggee was found that uses incompatible version of RPDB2."
STR_UNEXPECTED_DATA = "Unexpected data received."
STR_ACCESS_DENIED = "While attempting to find the specified debuggee at least one debuggee denied connection because of mismatched passwords. Please verify your password."
STR_ACCESS_DENIED2 = "Communication is denied because of un-matching passwords."
STR_ENCRYPTION_EXPECTED = "While attempting to find the specified debuggee at least one debuggee denied connection since it accepts encrypted connections only."
STR_ENCRYPTION_EXPECTED2 = "Debuggee will only talk over an encrypted channel."
STR_DECRYPTION_FAILURE = "Bad packet was received by the debuggee."
STR_DEBUGGEE_NO_ENCRYPTION = "Debuggee does not support encrypted mode. Either install the python-crypto package on the debuggee machine or allow unencrypted connections."
STR_RANDOM_PASSWORD = "Password has been set to a random password."
STR_PASSWORD_MUST_BE_SET = "A password must be set to secure the client-server communication."
STR_BAD_DATA = "Bad data received from debuggee."
STR_BAD_FILE_DATA = "Bad data received from file."
STR_ATTACH_FAILED = "Failed to attach"
STR_ATTACH_FAILED_NAME = "Failed to attach to '%s'."
STR_ATTACH_CRYPTO_MODE = "Debug Channel is%s encrypted."
STR_ATTACH_CRYPTO_MODE_NOT = "NOT"
STR_ATTACH_SUCCEEDED = "Successfully attached to '%s'."
STR_ATTEMPTING_TO_DETACH = "Detaching from script..."
STR_DETACH_SUCCEEDED = "Detached from script."
STR_DEBUGGEE_UNKNOWN = "Failed to find script."
STR_MULTIPLE_DEBUGGEES = "WARNING: There is more than one debuggee '%s'."
STR_HOST_UNKNOWN = "Failed to find '%s'"
STR_SOURCE_NOT_FOUND = "Failed to get source from debuggee."
STR_SCRIPTS_CONNECTING = "Connecting to '%s'..."
STR_SCRIPTS_NO_SCRIPTS = "No scripts to debug on '%s'"
STR_SCRIPTS_TO_DEBUG = """Scripts to debug on '%s':

   pid    name
--------------------------"""
STR_STACK_TRACE = """Stack trace for thread %d:

   Frame  File Name                     Line  Function                 
------------------------------------------------------------------------------""" 
STR_SOURCE_LINES = """Source lines for thread %d from file '%s':
""" 
STR_ACTIVE_THREADS = """List of active threads known to the debugger:

    No    Tid  State                 
-------------------------------""" 
STR_BREAKPOINTS_LIST = """List of breakpoints:

 Id  State     Filename          Line  Scope                Condition
-----------------------------------------------------------------------------""" 

STR_ENCRYPTION_SUPPORT_ERROR = "Encryption is not supported since the python-crypto package was not found. Either install the python-crypto package or allow unencrypted connections with the '-t' command line flag."
STR_PASSWORD_NOT_SET = 'Password is not set.'
STR_PASSWORD_SET = 'Password is set to: "%s"'
STR_ENCRYPT_MODE = 'Force encryption mode: %s'
STR_REMOTE_MODE = 'Allow remote machines mode: %s'

ENCRYPTION_ENABLED = 'encrypted'
ENCRYPTION_DISABLED = 'plain-text'

ENCRYPTION_PREFIX = 'encrypted'

STATE_ENABLED = 'enabled'
STATE_DISABLED = 'disabled'

BREAKPOINTS_FILE_EXT = '.bpl'
PYTHON_FILE_EXTENSION = '.py'
MODULE_SCOPE = '?'
SCOPE_SEP = '.'

BP_FILENAME_SEP = ':'
BP_EVAL_SEP = ','

DEBUGGER_FILENAME = 'rpdb2.py'
THREADING_FILENAME = 'threading.py'

STATE_BROKEN = 'broken'
STATE_RUNNING = 'running'

STATE_ANALYZE = 'analyze'
STATE_DETACHED = 'detached'
STATE_DETACHING = 'detaching'
STATE_SPAWNING = 'spawning'
STATE_ATTACHING = 'attaching'

DEFAULT_NUMBER_OF_LINES = 15

DICT_KEY_TID = 'tid'
DICT_KEY_STACK = 'stack'
DICT_KEY_CODE_LIST = 'code_list'
DICT_KEY_CURRENT_TID = 'current tid'
DICT_KEY_BROKEN = 'broken'
DICT_KEY_BREAKPOINTS = 'breakpoints'
DICT_KEY_LINES = 'lines'
DICT_KEY_FILENAME = 'filename'
DICT_KEY_FIRST_LINENO = 'first_lineno'
DICT_KEY_FRAME_LINENO = 'frame_lineno'
DICT_KEY_EVENT = 'event'
DICT_KEY_EXPR = 'expr'
DICT_KEY_NAME = 'name'
DICT_KEY_REPR = 'repr'
DICT_KEY_TYPE = 'type'
DICT_KEY_SUBNODES = 'subnodes'
DICT_KEY_N_SUBNODES = 'n_subnodes'
DICT_KEY_ERROR = 'error'

RPDB_EXEC_INFO = 'rpdb_exception_info'

MODE_ON = 'ON'
MODE_OFF = 'OFF'

MAX_EVENT_LIST_LENGTH = 1000

EVENT_EXCLUDE = 'exclude'
EVENT_INCLUDE = 'include'

INDEX_TABLE_SIZE = 100

DISPACHER_METHOD = 'dispatcher_method'

BASIC_TYPES_LIST = ['str', 'unicode', 'int', 'long', 'float', 'bool', 'NoneType']

XML_DATA = """<?xml version='1.0'?>
<methodCall>
<methodName>dispatcher_method</methodName>
<params>
<param>
<value><string>RPDB_02_00_00</string></value>
</param>
</params>
</methodCall>"""

N_WORK_QUEUE_THREADS = 15


g_server_lock = threading.RLock()
g_server = None
g_debugger = None

g_main_module_name = None
g_main_global_dictionay = None

g_fDebug = False
g_fScreen = False

g_traceback_lock = threading.RLock()



#
# ----------------------------------- General Utils -----------------------------------
#
            


def safe_repr(x):
    try:
        y = repr(x)
        return y

    except:
        pass

    try:
        y = str(x)
        return y
        
    except:
        pass

    return 'N/A'



def safe_repr_limited(x):
    y = safe_repr(x)[0:128]

    if len(y) == 128:
        y += '...'

    return y

    
    
def print_debug():
    if g_fDebug == True:
        (t, v, b) = sys.exc_info()

        try:
            g_traceback_lock.acquire()
            traceback.print_exception(t, v, b, file = sys.stderr)
            
        finally:    
            g_traceback_lock.release()

       

def split_command_line_path_filename_args(command_line):
    command_line = command_line.strip()
    if len(command_line) == 0:
        return ('', '', '')

    if command_line[0] in ['"', "'"]:
        _command_line = command_line[1:]
        i = _command_line.find(command_line[0])
        if i == -1:
            (_path, filename) = split_path(_command_line)
            return (_path, filename, '')
        else:
            (_path, filename) = split_path(_command_line[: i])
            args = _command_line[i + 1:].strip()
            return (_path, filename, args)
    else:
        i = command_line.find(' ')
        if i == -1:
            (_path, filename) = split_path(command_line)
            return (_path, filename, '')
        else:
            args = command_line[i + 1:].strip()
            (_path, filename) = split_path(command_line[: i])
            return (_path, filename, args)



def split_path(path):
    (_path, filename) = os.path.split(path)

    if _path in [os.path.sep, os.path.altsep]:
        _path = ''
        
    if _path != '':
        _path = _path + path[len(_path): len(_path) + 1]

    return (_path, filename)

    

def my_abspath(path):
    if path[:1] == '<':
        return path

    if os.name == 'nt':
        return my_abspath1(path)

    return  os.path.abspath(path)   



def my_abspath1(path):
    if path:
        try:
            path = _getfullpathname(path)
        except WindowsError:
            pass
    else:
        path = os.getcwd()
        
    np = os.path.normpath(path)

    if (len(np) >= 2) and (np[1:2] == ':'):
        np = np[:1].upper() + np[1:]

    return np    



def IsPythonSourceFile(filename):
    return filename.endswith(PYTHON_FILE_EXTENSION)



def FindFile(filename, sources_paths = [], fModules = False):
    """ 
    Expand filname to explicit path.   
    Find file looks in the following directories in this order:
    1. full path (if exists).
    2. sources_paths.
    2. current path.
    3. PYTHONPATH
    4. PATH
    """

    if fModules:
        modulename = CalcModuleName(filename)
        _module = sys.modules.get(modulename, None)
        if _module != None:
            _filename = CalcScriptName(_module.__file__)
            abs_path = my_abspath(_filename)
            if os.path.isfile(abs_path):
                return abs_path

    _filename = CalcScriptName(filename)
        
    if os.path.dirname(_filename) != '':
        abs_path = my_abspath(_filename)
        if os.path.isfile(abs_path):
            return abs_path

    _basename = os.path.basename(_filename)
    cwd = os.getcwd()
    path = os.environ['PATH']
    paths = sources_paths + [cwd] + sys.path + path.split(os.pathsep)
    norm_filename = os.path.normpath(_filename)
    
    for p in paths:
        f = os.path.join(p, _basename)
        if not os.path.isfile(f):
            continue

        norm_f = os.path.normpath(f)
        if norm_f.endswith(norm_filename):
            abs_path = my_abspath(f)
            return abs_path

    raise IOError



def winlower(path):
    if os.name == 'nt':
        return path.lower()

    return path
    
    

def CalcModuleName(filename):
    _basename = os.path.basename(filename)
    
    if _basename[:-1].endswith(PYTHON_FILE_EXTENSION):
        module_name = _basename[:-4]
    else:    
        module_name = _basename.rstrip(PYTHON_FILE_EXTENSION)
        
    return module_name



def CalcScriptName(filename):
    if filename.endswith(PYTHON_FILE_EXTENSION):
        return filename
        
    if filename[:-1].endswith(PYTHON_FILE_EXTENSION):
        scriptname = filename[:-1]
        return scriptname

    scriptname = filename + PYTHON_FILE_EXTENSION
    return scriptname
        


def _getpid():
    try:
        return os.getpid()
    except:
        return -1



def calcURL(host, port):
    url = "http://" + str(host) + ":" + str(port)
    return url
    
    

def GetSocketError(e):
    if (type(e.args) != tuple) or (len(e.args) == 0):
        return -1

    return e.args[0]



def ControlRate(t_last_call, max_rate):
    """
    Use this function to limit the rate of an operation.
    If called more often than max_rate allows, it will sleep a little.
    """
    p = 1.0 / max_rate
    t_current = time.time()
    dt = t_current - t_last_call

    if dt < p:
        time.sleep(p - dt)

    return t_current



def generate_rid():
    return repr(random.randint(1000000, 9999999))



def generate_random_char(str):
    if str == '':
        return ''
        
    i = random.randint(0, len(str) - 1)
    return str[i]

    

def generate_random_password():
    s = 'abdefghijmnpqrt' + 'ABDEFGHJLMNQRTY'
    ds = '2346789' + s
        
    pwd = generate_random_char(s)

    for i in range(0, 7):
        pwd += generate_random_char(ds)

    return pwd    



def is_encryption_supported():
    return 'DES' in globals()



def calc_suffix(str, n):
    if len(str) <= n:
        return str

    return '...' + str[-(n - 3):]


    
def calc_prefix(str, n):
    if len(str) <= n:
        return str

    return str[: (n - 3)] + '...'


    
#
#--------------------------------------- Crypto ---------------------------------------
#



def fix_password(pwd):
    if (len(pwd) > 2) and ((pwd[0] + pwd[-1] == '""') or (pwd[0] + pwd[-1] == "''")):
        return pwd[1:-1]

    return pwd    


        
class CCrypto:
    def __init__(self, pwd, fAllowUnencrypted, rid):
        self.m_pwd = pwd
        d = md5.new()
        d.update(pwd)
        self.m_key = d.digest()
        self.m_fAllowUnencrypted = fAllowUnencrypted
        self.m_rid = rid

        self.m_failure_lock = threading.RLock()

        self.m_lock = threading.RLock()

        self.m_index_anchor_in = random.randint(0, 1000000000)
        self.m_index_anchor_ex = 0

        self.m_index = 0
        self.m_index_table = {}
        self.m_index_table_size = INDEX_TABLE_SIZE
        self.m_max_index = 0

    def set_index(self, i, anchor):
        try:    
            self.m_lock.acquire()

            self.m_index = i
            self.m_index_anchor_ex = anchor
            
        finally:
            self.m_lock.release()

    def get_max_index(self):
        return self.m_max_index

    def is_encrypted(self, str):
        return str[: len(ENCRYPTION_PREFIX)] == ENCRYPTION_PREFIX
        
    def do_crypto(self, s, fEncryption):        
        _s = self.__auth_make(s)

        if not fEncryption:
            if self.m_fAllowUnencrypted:
                return _s

            raise EncryptionExpected  
            
        if not is_encryption_supported():
            raise EncryptionNotSupported

        __s = self.__encrypt(_s)
        return __s    

    def undo_crypto(self, __s, fVerifyIndex = True):
        (_s, fEncryption) = self.__decrypt(__s)            
        s = self.__auth_verify(_s, fVerifyIndex)

        return (s, fEncryption)
    
    def __encrypt(self, s):
        s_padded = s + '0' * (DES.block_size - (len(s) % DES.block_size))
        key_padded = (self.m_key + '0' * (DES.key_size - (len(self.m_key) % DES.key_size)))[:DES.key_size]
        iv = '0' * DES.block_size
        
        d = DES.new(key_padded, DES.MODE_CBC, iv)
        r = d.encrypt(s_padded)
        __s = base64.encodestring(r)

        return ENCRYPTION_PREFIX + __s

    def __decrypt(self, s):
        if s[: len(ENCRYPTION_PREFIX)] != ENCRYPTION_PREFIX:
            if self.m_fAllowUnencrypted:
                return (s, False)
                
            raise EncryptionExpected

        if not is_encryption_supported():
            raise EncryptionNotSupported
        
        __s = s[len(ENCRYPTION_PREFIX):]
        
        try:
            _r = base64.decodestring(__s)

            key_padded = (self.m_key + '0' * (DES.key_size - (len(self.m_key) % DES.key_size)))[:DES.key_size]
            iv = '0' * DES.block_size
            
            d = DES.new(key_padded, DES.MODE_CBC, iv)
            _s = d.decrypt(_r)

            return (_s, True)
            
        except:
            self.__wait_a_little()
            raise DecryptionFailure

    def __get_next_index(self):
        try:    
            self.m_lock.acquire()

            self.m_index += 1
            return self.m_index

        finally:
            self.m_lock.release()

    def __wait_a_little(self):
        self.m_failure_lock.acquire()
        time.sleep((1.0 + random.random()) / 2)
        self.m_failure_lock.release()

    def __verify_index(self, anchor, i, id):
        try:
            try:    
                self.m_lock.acquire()

                if anchor != self.m_index_anchor_in:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                if i > self.m_max_index + INDEX_TABLE_SIZE / 2:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                _i = i % INDEX_TABLE_SIZE
                (iv, idl) = self.m_index_table.get(_i, (None, None))

                #print >> sys.__stderr__, i, _i, iv, self.m_max_index

                if (iv == None) or (i > iv):
                    iv = i
                    idl = [id]
                elif (iv == i) and (not id in idl):
                    idl.append(id)
                else:
                    raise AuthenticationBadIndex(self.m_max_index, self.m_index_anchor_in)

                self.m_index_table[_i] = (iv, idl) 

                if i > self.m_max_index:
                    self.m_max_index = i

                return self.m_index

            finally:
                self.m_lock.release()
        except:        
            self.__wait_a_little()
            raise

    def __auth_make(self, s):
        i = self.__get_next_index()
        _s = cPickle.dumps((self.m_index_anchor_ex, i, self.m_rid, s))
        
        d = hmac.new(self.m_key, _s, md5)
        _d = d.digest()
        r = (_d, _s)
        __s = cPickle.dumps(r)

        return __s

    def __auth_verify(self, s, fVerifyIndex):
        try:
            r = cPickle.loads(s)
            
            (_d, _s) = r
            
            d = hmac.new(self.m_key, _s, md5)
            __d = d.digest()

            if _d != __d:
                self.__wait_a_little()
                raise AuthenticationFailure
                
            (anchor, i, id, __s) = cPickle.loads(_s)
        except AuthenticationFailure:
            raise
        except:
            self.__wait_a_little()
            raise AuthenticationBadData
            
        if fVerifyIndex:
            self.__verify_index(anchor, i, id)

        return __s
        

        
#
# --------------------------------- Event Manager --------------------------
#



class CEvent:
    def is_match(self, arg):
        pass



class CEventExit(CEvent):
    pass
    

    
class CEventSync(CEvent):
    def __init__(self, fException):
        self.m_fException = fException
    

    
class CEventState(CEvent):
    def __init__(self, state):
        self.m_state = state

    def is_match(self, arg):
        return self.m_state == arg



class CEventNamespace(CEvent):
    pass
    


class CEventNoThreads(CEvent):
    pass


    
class CEventThreads(CEvent):
    def __init__(self, current_thread, thread_list):
        self.m_current_thread = current_thread
        self.m_thread_list = thread_list



class CEventThreadBroken(CEvent):
    def __init__(self, tid):
        self.m_tid = tid


        
class CEventStack(CEvent):
    def __init__(self, stack):
        self.m_stack = stack


    
class CEventStackFrameChange(CEvent):
    def __init__(self, frame_index):
        self.m_frame_index = frame_index


    
class CEventStackDepth(CEvent):
    def __init__(self, stack_depth, stack_depth_exception):
        self.m_stack_depth = stack_depth
        self.m_stack_depth_exception = stack_depth_exception


    
class CEventBreakpoint(CEvent):
    DISABLE = 'disable'
    ENABLE = 'enable'
    REMOVE = 'remove'
    SET = 'set'
    
    def __init__(self, bp, action = SET, id_list = [], fAll = False):
        self.m_bp = copy.copy(bp)
        if self.m_bp != None:
            self.m_bp.m_code = None
        
        self.m_action = action
        self.m_id_list = id_list
        self.m_fAll = fAll



class CEventDispatcherRecord:
    def __init__(self, callback, event_type_dict, fSingleUse):
        self.m_callback = callback
        self.m_event_type_dict = event_type_dict
        self.m_fSingleUse = fSingleUse

    def is_match(self, event):
        rtl = [t for t in self.m_event_type_dict.keys() if isinstance(event, t)]
        if len(rtl) == 0:
            return False

        rt = rtl[0]    
        rte = self.m_event_type_dict[rt].get(EVENT_EXCLUDE, [])
        if len(rte) != 0:
            for e in rte:
                if event.is_match(e):
                    return False
            return True  
        
        rte = self.m_event_type_dict[rt].get(EVENT_INCLUDE, [])
        if len(rte) != 0:
            for e in rte:
                if event.is_match(e):
                    return True
            return False  

        return True

        
        
class CEventDispatcher:
    def __init__(self, chained_event_dispatcher = None):
        self.m_chained_event_dispatcher = chained_event_dispatcher
        self.m_chain_override_types = {}

        self.m_registrants = {}

    def shutdown():
        for er in self.m_registrants.keys():
            self.__remove_dispatcher_record(er)
        
    def register_callback(self, callback, event_type_dict, fSingleUse):
        er = CEventDispatcherRecord(callback, event_type_dict, fSingleUse)

        if self.m_chained_event_dispatcher != None:
            _er = self.__register_callback_on_chain(er, event_type_dict, fSingleUse)
            self.m_registrants[er] = _er
        else:
            self.m_registrants[er] = True
        
        return er

    def remove_callback(self, callback):
        erl = [er for er in self.m_registrants.keys() if er.m_callback == callback]
        for er in erl:
            self.__remove_dispatcher_record(er)

    def fire_events(self, event_list):
        for event in event_list:
            self.fire_event(event)

    def fire_event(self, event):
        for er in self.m_registrants.keys():
            self.__fire_er(event, er)
                        
    def __fire_er(self, event, er):
        if er.is_match(event):
            try:
                er.m_callback(event)
            except:
                pass
                
            if er.m_fSingleUse:
                try:
                    del self.m_registrants[er]
                except KeyError:
                    pass
                    
    def register_chain_override(self, event_type_dict):
        for t in event_type_dict.keys():
            self.m_chain_override_types[t] = True

    def __register_callback_on_chain(self, er, event_type_dict, fSingleUse):
        _event_type_dict = copy.copy(event_type_dict)
        for t in self.m_chain_override_types:
            if t in _event_type_dict:
                del _event_type_dict[t]

        if len(_event_type_dict) == 0:
            return False

        def callback(event, er = er):
            self.__fire_er(event, er)
            
        _er = self.m_chained_event_dispatcher.register_callback(callback, _event_type_dict, fSingleUse)
        return _er
        
    def __remove_dispatcher_record(self, er):
        try:
            if self.m_chained_event_dispatcher != None:
                _er = self.m_registrants[er]
                if _er != False:
                    self.m_chained_event_dispatcher.__remove_dispatcher_record(_er)

            del self.m_registrants[er]
            
        except KeyError:
            pass
                


class CEventQueue:
    def __init__(self, event_dispatcher, max_event_list_length = MAX_EVENT_LIST_LENGTH):
        self.m_event_dispatcher = event_dispatcher

        self.m_event_lock = threading.Condition(threading.Lock())
        self.m_max_event_list_length = max_event_list_length
        self.m_event_list = []
        self.m_event_index = 0
 
    def shutdown(self):
        self.m_event_dispatcher.remove_callback(self.event_handler)
    
    def register_event_types(self, event_type_dict):
        self.m_event_dispatcher.register_callback(self.event_handler, event_type_dict, fSingleUse = False)

    def event_handler(self, event):
        try:
            self.m_event_lock.acquire()

            self.m_event_list.append(event)
            if len(self.m_event_list) > self.m_max_event_list_length:
                self.m_event_list.pop(0)
                
            self.m_event_index += 1    
            self.m_event_lock.notifyAll()

        finally:
            self.m_event_lock.release()

    def get_event_index(self):
        return self.m_event_index

    def wait_for_event(self, timeout, event_index):
        try:
            self.m_event_lock.acquire()
            if event_index >= self.m_event_index:
                self.m_event_lock.wait(timeout)

            if event_index >= self.m_event_index:
                return (self.m_event_index, [])
                
            sub_event_list = self.m_event_list[event_index - self.m_event_index:]
            return (self.m_event_index, sub_event_list)
            
        finally:
            self.m_event_lock.release()



class CStateManager:
    def __init__(self, initial_state, event_dispatcher_output = None, event_dispatcher_input = None, event_dispatcher_sync = None):
        self.m_event_dispatcher_input = event_dispatcher_input
        self.m_event_dispatcher_output = event_dispatcher_output
        self.m_event_dispatcher_sync = event_dispatcher_sync

        if self.m_event_dispatcher_sync != None:
            event_type_dict = {CEventSync: {}}
            self.m_event_dispatcher_sync.register_callback(self.event_handler, event_type_dict, fSingleUse = False)

        if self.m_event_dispatcher_input != None:
            event_type_dict = {CEventState: {}}
            self.m_event_dispatcher_input.register_callback(self.event_handler, event_type_dict, fSingleUse = False)

            if self.m_event_dispatcher_output != None:
                self.m_event_dispatcher_output.register_chain_override(event_type_dict)

        self.m_state_lock = threading.Condition(threading.Lock())

        self.m_state_queue = []
        self.m_state_index = 0        
        self.m_waiter_list = {}
        
        self.set_state(initial_state) 

    def shutdown(self):
        if self.m_event_dispatcher_sync != None:
            self.m_event_dispatcher_sync.remove_callback(self.event_handler)

        if self.m_event_dispatcher_input != None:
            self.m_event_dispatcher_input.remove_callback(self.event_handler)

    def event_handler(self, event):
        if isinstance(event, CEventSync):
            if not event.m_fException:                
                self.set_state()

            return
            
        self.set_state(event.m_state)

    def get_state(self):
        return self.m_state_queue[-1]

    def __add_state(self, state):
        self.m_state_queue.append(state)
        self.m_state_index += 1

        self.__remove_states()

    def __remove_states(self, treshold = None):
        index = self.__calc_min_index()

        if (treshold != None) and (index <= treshold):
            return
            
        _delta = 1 + self.m_state_index - index

        self.m_state_queue = self.m_state_queue[-_delta:]
        
    def __calc_min_index(self):
        if len(self.m_waiter_list) == 0:
            return self.m_state_index

        index_list = self.m_waiter_list.keys()
        min_index = min(index_list)

        return min_index
        
    def __add_waiter(self):
        index = self.m_state_index
        n = self.m_waiter_list.get(index, 0)
        self.m_waiter_list[index] = n + 1

        return index

    def __remove_waiter(self, index):
        n = self.m_waiter_list[index]
        if n == 1:
            del self.m_waiter_list[index]
            self.__remove_states(index)
        else:
            self.m_waiter_list[index] = n - 1

    def __get_states(self, index):
        _delta = 1 + self.m_state_index - index
        states = self.m_state_queue[-_delta:]
        return states
        
    def set_state(self, state = None, fLock = True):
        try:
            if fLock:
                self.m_state_lock.acquire()

            if state == None:
                state = self.get_state()
                
            self.__add_state(state)            

            self.m_state_lock.notifyAll()

        finally:    
            if fLock:
                self.m_state_lock.release()

        if self.m_event_dispatcher_output != None:
            event = CEventState(state)
            self.m_event_dispatcher_output.fire_event(event)
        
    def wait_for_state(self, state_list):
        try:
            self.m_state_lock.acquire()

            if self.get_state() in state_list:
                return self.get_state()
            
            while True:
                index = self.__add_waiter()
            
                self.m_state_lock.wait(PING_TIMEOUT)

                states = self.__get_states(index)
                self.__remove_waiter(index)

                for state in states:
                    if state in state_list:
                        return state
            
        finally:
            self.m_state_lock.release()


    def acquire(self):
        self.m_state_lock.acquire()

    def release(self):
        self.m_state_lock.release()



#
# -------------------------------------- Break Info manager ---------------------------------------
#



def CalcValidLines(code):
    l = code.co_firstlineno
    vl = [l]

    bl = [ord(c) for c in code.co_lnotab[2::2]]
    sl = [ord(c) for c in code.co_lnotab[1::2]]

    for (bi, si) in zip(bl, sl):
        l += si

        if bi == 0:
            continue

        if l != vl[-1]:
            vl.append(l)

    if len(sl) > 0:
        l += sl[-1]

        if l != vl[-1]:
            vl.append(l)
    
    return vl
    


class CScopeBreakInfo:
    def __init__(self, fqn, valid_lines):
        self.m_fqn = fqn
        self.m_first_line = valid_lines[0]
        self.m_last_line = valid_lines[-1]
        self.m_valid_lines = valid_lines

    def CalcScopeLine(self, lineno):
        rvl = copy.copy(self.m_valid_lines)
        rvl.reverse()

        for l in rvl:
            if lineno >= l:
                break

        return l
        
    def __str__(self):
        return "('" + self.m_fqn + "', " + str(self.m_valid_lines) + ')'
        


class CFileBreakInfo:
    def __init__(self, filename):
        self.m_filename = filename
        self.m_first_line = 0
        self.m_last_line = 0
        self.m_scope_break_info = []

    def __CalcSubCodesList(self, code):
        tc = type(code)
        t = [(c.co_firstlineno, c) for c in code.co_consts if type(c) == tc]
        t.sort()
        scl = [c[1] for c in t]
        return scl

    def __CalcBreakInfoFromSource(self, source):
        _source = source.replace('\r\n', '\n')
        code = compile(_source, self.m_filename, "exec")
        
        self.m_scope_break_info = []
        self.m_first_line = code.co_firstlineno
        self.m_last_line = 0
        
        fqn = []
        t = [code]
        
        while len(t) > 0:
            c = t.pop(0)

            if type(c) == tuple:
                self.m_scope_break_info.append(CScopeBreakInfo(*c))
                fqn.pop()
                continue

            fqn = fqn + [c.co_name]  
            valid_lines = CalcValidLines(c)
            self.m_last_line = max(self.m_last_line, valid_lines[-1])
            _fqn = string.join(fqn, '.')
            si = (_fqn, valid_lines)  
            subcodeslist = self.__CalcSubCodesList(c)
            t = subcodeslist + [si] + t
            
    def CalcBreakInfo(self):
        f = open(self.m_filename, "r")
        source = f.read()
        f.close()
        
        self.__CalcBreakInfoFromSource(source)

    def FindScopeByLineno(self, lineno):
        lineno = max(min(lineno, self.m_last_line), self.m_first_line)

        smaller_element = None
        exact_element = None
        
        for sbi in self.m_scope_break_info:
            if lineno > sbi.m_last_line:
                if (smaller_element == None) or (sbi.m_last_line >= smaller_element.m_last_line):
                    smaller_element = sbi
                continue

            if (lineno >= sbi.m_first_line) and (lineno <= sbi.m_last_line):
                exact_element = sbi
                break

        assert(exact_element != None)

        scope = exact_element
        l = exact_element.CalcScopeLine(lineno)
        
        if (smaller_element != None) and (l <= smaller_element.m_last_line):
            scope = smaller_element
            l = smaller_element.CalcScopeLine(lineno)

        return (scope, l)

    def FindScopeByName(self, name, offset):
        if not name.startswith(MODULE_SCOPE):
            name = MODULE_SCOPE + SCOPE_SEP + name
            
        for sbi in self.m_scope_break_info:
            if sbi.m_fqn == name:
                l = sbi.CalcScopeLine(sbi.m_first_line + offset)
                return (sbi, l)

        raise InvalidScopeName
    


class CBreakInfoManager:
    def __init__(self):
        self.m_file_info_dic = {}

    def addFile(self, filename):
        mbi = CFileBreakInfo(filename)
        mbi.CalcBreakInfo()
        self.m_file_info_dic[filename] = mbi

    def getFile(self, filename):
        if not filename in self.m_file_info_dic:
            self.addFile(filename)

        return self.m_file_info_dic[filename]



#
# -------------------------------- Break Point Manager -----------------------------
#



class CBreakPoint:
    def __init__(self, filename, scope_fqn, scope_first_line, lineno, fEnabled, expr, fTemporary = False):
        self.m_id = None
        self.m_fEnabled = fEnabled
        self.m_filename = filename
        self.m_scope_fqn = scope_fqn
        self.m_scope_name = scope_fqn.split(SCOPE_SEP)[-1]
        self.m_scope_first_line = scope_first_line
        self.m_scope_offset = lineno - scope_first_line
        self.m_lineno = lineno
        self.m_expr = expr
        self.m_code = None
        self.m_fTemporary = fTemporary

        if (expr != None) and (expr != ''):
            self.m_code = compile(expr, '', 'eval')
        
    def calc_enclosing_scope_name(self):
        if self.m_scope_offset != 0:
            return None
            
        if self.m_scope_fqn == MODULE_SCOPE:
            return None

        scope_name_list = self.m_scope_fqn.split(SCOPE_SEP)
        enclosing_scope_name = scope_name_list[-2]

        return enclosing_scope_name
            
    def enable(self):
        self.m_fEnabled = True
        
    def disable(self):
        self.m_fEnabled = False

    def isEnabled(self):
        return self.m_fEnabled
        
    def __str__(self):
        return "('" + self.m_filename + "', '" + self.m_scope_fqn + "', " + str(self.m_scope_first_line) + ', ' + str(self.m_scope_offset) + ', ' + str(self.m_lineno) + ')'
        


class CBreakPointsManagerProxy:
    def __init__(self, session_manager):
        self.m_session_manager = session_manager

        self.m_break_points_by_file = {}
        self.m_break_points_by_id = {}

        self.m_lock = threading.Lock()

        event_type_dict = {CEventBreakpoint: {}}

        self.m_session_manager.m_event_dispatcher_proxy.register_callback(self.update_bp, event_type_dict, fSingleUse = False)
        self.m_session_manager.m_event_dispatcher.register_chain_override(event_type_dict)

    def update_bp(self, event):       
        try:    
            self.m_lock.acquire()

            if event.m_fAll:
                id_list = self.m_break_points_by_id.keys()
            else:
                id_list = event.m_id_list
                
            if event.m_action == CEventBreakpoint.REMOVE:
                for id in id_list:
                    try:
                        bp = self.m_break_points_by_id.pop(id)
                        bpm = self.m_break_points_by_file[bp.m_filename]
                        del bpm[bp.m_lineno]
                        if len(bpm) == 0:
                            del self.m_break_points_by_file[bp.m_filename]
                    except KeyError:
                        pass
                return
                
            if event.m_action == CEventBreakpoint.DISABLE:
                for id in id_list:
                    try:
                        bp = self.m_break_points_by_id[id]
                        bp.disable()
                    except KeyError:
                        pass
                return

            if event.m_action == CEventBreakpoint.ENABLE:
                for id in id_list:
                    try:
                        bp = self.m_break_points_by_id[id]
                        bp.enable()
                    except KeyError:
                        pass
                return
                
            bpm = self.m_break_points_by_file.get(event.m_bp.m_filename, {})
            bpm[event.m_bp.m_lineno] = event.m_bp

            self.m_break_points_by_id[event.m_bp.m_id] = event.m_bp
            
        finally:
            self.m_lock.release()

            self.m_session_manager.m_event_dispatcher.fire_event(event)

    def sync(self):
        try:    
            self.m_lock.acquire()

            self.m_break_points_by_file = {}
            self.m_break_points_by_id = {}
            
        finally:
            self.m_lock.release()

        break_points_by_id = self.m_session_manager.getSession().getProxy().get_breakpoints()

        try:    
            self.m_lock.acquire()

            self.m_break_points_by_id.update(break_points_by_id)

            for bp in self.m_break_points_by_id.values():
                bpm = self.m_break_points_by_file.get(bp.m_filename, {})
                bpm[bp.m_lineno] = bp
            
        finally:
            self.m_lock.release()

    def clear(self):
        try:    
            self.m_lock.acquire()

            self.m_break_points_by_file = {}
            self.m_break_points_by_id = {}
            
        finally:
            self.m_lock.release()

    def get_breakpoints(self):
        return self.m_break_points_by_id

    def get_breakpoint(self, filename, lineno):
        bpm = self.m_break_points_by_file[filename]
        bp = bpm[lineno]
        return bp    


        
class CBreakPointsManager:
    def __init__(self):
        self.m_break_info_manager = CBreakInfoManager()
        self.m_active_break_points_by_file = {}
        self.m_break_points_by_function = {}
        self.m_break_points_by_file = {}
        self.m_break_points_by_id = {}
        self.m_lock = threading.Lock()

        self.m_temp_bp = None

    def get_active_break_points_by_file(self, filename):
        _filename = winlower(filename)
        
        return self.m_active_break_points_by_file.setdefault(_filename, {})
        
    def __calc_active_break_points_by_file(self, filename):
        bpmpt = self.m_active_break_points_by_file.setdefault(filename, {})        
        bpmpt.clear()

        bpm = self.m_break_points_by_file.get(filename, {})
        for bp in bpm.values():
            if bp.m_fEnabled:
                bpmpt[bp.m_lineno] = bp
                
        tbp = self.m_temp_bp
        if (tbp != None) and (tbp.m_filename == filename):
            bpmpt[tbp.m_lineno] = tbp                      
        
    def __remove_from_function_list(self, bp):
        function_name = bp.m_scope_name

        try:
            bpf = self.m_break_points_by_function[function_name]
            del bpf[bp]
            if len(bpf) == 0:
                del self.m_break_points_by_function[function_name]
        except KeyError:
            pass

        _function_name = bp.calc_enclosing_scope_name()
        if _function_name == None:
            return
            
        try:
            _bpf = self.m_break_points_by_function[_function_name]
            del _bpf[bp]
            if len(_bpf) == 0:
                del self.m_break_points_by_function[_function_name]
        except KeyError:
            pass

    def __add_to_function_list(self, bp):
        function_name = bp.m_scope_name

        bpf = self.m_break_points_by_function.setdefault(function_name, {})
        bpf[bp] = True 

        _function_name = bp.calc_enclosing_scope_name()
        if _function_name == None:
            return
            
        _bpf = self.m_break_points_by_function.setdefault(_function_name, {})
        _bpf[bp] = True 
            
    def get_breakpoint(self, filename, lineno):
        bpm = self.m_break_points_by_file[filename]
        bp = bpm[lineno]
        return bp    
        
    def del_temp_breakpoint(self, fLock = True):
        if self.m_temp_bp == None:
            return

        try:    
            if fLock:
                self.m_lock.acquire()

            if self.m_temp_bp == None:
                return

            bp = self.m_temp_bp
            self.m_temp_bp = None

            self.__remove_from_function_list(bp)
            self.__calc_active_break_points_by_file(bp.m_filename)

        finally:
            if fLock:
                self.m_lock.release()
        
    def set_temp_breakpoint(self, filename, scope, lineno):
        _filename = winlower(filename)

        mbi = self.m_break_info_manager.getFile(_filename)

        if scope != '':
            (s, l) = mbi.FindScopeByName(scope, lineno)
        else:
            (s, l) = mbi.FindScopeByLineno(lineno)

        bp = CBreakPoint(_filename, s.m_fqn, s.m_first_line, l, fEnabled = True, expr = '', fTemporary = True)

        try:    
            self.m_lock.acquire()

            self.del_temp_breakpoint(fLock = False) 
            self.m_temp_bp = bp
            self.__add_to_function_list(bp)
            self.__calc_active_break_points_by_file(bp.m_filename)

        finally:
            self.m_lock.release()

    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr):
        _filename = winlower(filename)
        
        mbi = self.m_break_info_manager.getFile(_filename)

        if scope != '':
            (s, l) = mbi.FindScopeByName(scope, lineno)
        else:
            (s, l) = mbi.FindScopeByLineno(lineno)

        bp = CBreakPoint(_filename, s.m_fqn, s.m_first_line, l, fEnabled, expr)

        try:    
            self.m_lock.acquire()

            bpm = self.m_break_points_by_file.setdefault(_filename, {})
            
            try:
                old_bp = bpm[l]
                id = old_bp.m_id
                self.__remove_from_function_list(old_bp)
            except KeyError:
                bpids = self.m_break_points_by_id.keys()
                bpids.sort()
                
                id = 0
                while id < len(bpids):
                    if bpids[id] != id:
                        break
                    id += 1

            bp.m_id = id 
            
            self.m_break_points_by_id[id] = bp    
            bpm[l] = bp    
            if fEnabled:
                self.__add_to_function_list(bp)

            self.__calc_active_break_points_by_file(bp.m_filename)

            return bp    

        finally:
            self.m_lock.release()

    def disable_breakpoint(self, id_list, fAll):
        try:    
            self.m_lock.acquire()

            if fAll:
                id_list = self.m_break_points_by_id.keys()

            for id in id_list:    
                try:
                    bp = self.m_break_points_by_id[id]
                except KeyError:
                    continue
                    
                bp.disable()
                self.__remove_from_function_list(bp)
                self.__calc_active_break_points_by_file(bp.m_filename)

        finally:
            self.m_lock.release()

    def enable_breakpoint(self, id_list, fAll):
        try:    
            self.m_lock.acquire()

            if fAll:
                id_list = self.m_break_points_by_id.keys()

            for id in id_list:  
                try:
                    bp = self.m_break_points_by_id[id]
                except KeyError:
                    continue
                    
                bp.enable()
                self.__add_to_function_list(bp)
                self.__calc_active_break_points_by_file(bp.m_filename)

        finally:
            self.m_lock.release()

    def delete_breakpoint(self, id_list, fAll):
        try:    
            self.m_lock.acquire()

            if fAll:
                id_list = self.m_break_points_by_id.keys()

            for id in id_list:    
                try:
                    bp = self.m_break_points_by_id[id]
                except KeyError:
                    continue
                    
                filename = bp.m_filename
                lineno = bp.m_lineno

                bpm = self.m_break_points_by_file[filename]
                if bp == bpm[lineno]:
                    del bpm[lineno]

                if len(bpm) == 0:
                    del self.m_break_points_by_file[filename]
                    
                self.__remove_from_function_list(bp)
                self.__calc_active_break_points_by_file(bp.m_filename)
                    
                del self.m_break_points_by_id[id]

        finally:
            self.m_lock.release()

    def get_breakpoints(self):
        return self.m_break_points_by_id



#
# ----------------------------------- Core Debugger ------------------------------------
#



class CCodeContext:
    def __init__(self, code, bp_manager):
        self.m_code = code
        self.m_filename = my_abspath(code.co_filename)
        self.m_basename = os.path.basename(self.m_filename)

        self.m_file_breakpoints = bp_manager.get_active_break_points_by_file(self.m_filename)

        self.m_fExceptionTrap = False

    def is_untraced(self):
        return self.m_basename in [THREADING_FILENAME, DEBUGGER_FILENAME]



class CDebuggerCoreThread:
    def __init__(self, core_debugger, frame, event):
        self.m_thread_id = thread.get_ident()
        self.m_fBroken = False
        self.m_fUnhandledException = False
        
        self.m_frame = frame
        self.m_event = event
        self.m_ue_lineno = None
        self.m_uef_lineno = None
        
        self.m_code_context = core_debugger.get_code_context(frame.f_code)

        self.m_locals_copy = {}

        self.m_core = core_debugger
        self.m_bp_manager = core_debugger.m_bp_manager

        self.m_frame_lock = threading.Condition(threading.Lock())
        self.m_frame_external_references = 0
        
    def profile(self, frame, event, arg):    
        if event == 'return':            
            self.m_frame = frame.f_back
            try:
                self.m_code_context = self.m_core.m_code_contexts[self.m_frame.f_code]
            except AttributeError:
                if self.m_event != 'return':
                    self.m_frame = frame
                    self.m_event = 'exception'
                    
                    self.m_uef_lineno = self.m_ue_lineno
                    
                    self.m_fUnhandledException = True                    
                    self.m_core._break(self, frame, event, arg)
                    
                    self.m_uef_lineno = None 
                    
                    if frame in self.m_locals_copy:
                        self.update_locals()

                    self.m_frame = None
                
                self.m_core.remove_thread(self.m_thread_id)
                sys.setprofile(None)
                sys.settrace(self.m_core.trace_dispatch_init)
            
            if self.m_frame_external_references == 0:
                return

            try:
                self.m_frame_lock.acquire() 

                while self.m_frame_external_references != 0:
                    self.m_frame_lock.wait(1.0)

            finally:
                self.m_frame_lock.release()
                            
    def frame_acquire(self):
        try:
            self.m_frame_lock.acquire()
            
            self.m_frame_external_references += 1
            f = self.m_frame
            if f == None:
                raise ThreadDone

            return f    

        finally:    
            self.m_frame_lock.release()

    def frame_release(self):
        try:
            self.m_frame_lock.acquire()
                
            self.m_frame_external_references -= 1
            if self.m_frame_external_references == 0:
                self.m_frame_lock.notify()

        finally:    
            self.m_frame_lock.release()
        
    def get_frame(self, base_frame, index, fException = False):
        if fException:
            tb = base_frame.f_exc_traceback
            if tb == None:
                raise NoExceptionFound
                
            while tb.tb_next != None:
                tb = tb.tb_next

            f = tb.tb_frame
        else:    
            f = base_frame
            
        while (index > 0) and (f != None):
            f = f.f_back
            index -= 1

        if (index < 0) or (f == None):
            raise InvalidFrame

        if (self.m_uef_lineno != None) and (f.f_back == None):
            lineno = self.m_uef_lineno
        else:    
            lineno = f.f_lineno
            
        if fException:
            tb = base_frame.f_exc_traceback
            while tb != None:
                if tb.tb_frame == f:
                    lineno = tb.tb_lineno
                    break
                tb = tb.tb_next

        return (f, lineno)  

    def get_locals_copy(self, frame_index, fException, fReadOnly):
        try:
            base_frame = self.frame_acquire()

            (f, lineno) = self.get_frame(base_frame, frame_index, fException)

            if f.f_globals is g_main_global_dictionay:
                gc = g_main_global_dictionay
            elif f.f_globals is vars(sys.modules['__main__']):
                gc = vars(sys.modules['__main__'])
            else:
                gc = {}
                sn1 = CalcScriptName(f.f_code.co_filename)
                
                for m in sys.modules.values():
                    if m == None:
                        continue
                        
                    fn = vars(m).get('__file__', None)
                    if fn == None:
                        continue
                        
                    sn2 = CalcScriptName(fn)
                    if sn1 == sn2:
                        gc = vars(m)
                        break
                
            try:
                lc = self.m_locals_copy[f]
            except KeyError:
                if f.f_code.co_name == '?':
                    lc = gc
                else:    
                    lc = copy.copy(f.f_locals)
                if not fReadOnly:
                    self.m_locals_copy[f] = lc
                    self.set_local_trace(f)

            return (gc, lc)

        finally:
            f = None
            base_frame = None
            
            self.frame_release()

    def update_locals(self):
        lc = self.m_locals_copy.pop(self.m_frame, None)
        if lc == None:
            return
            
        self.m_frame.f_locals.update(lc)
            
    def __eval_breakpoint(self, frame, bp):
        if not bp.m_fEnabled:
            return False

        if bp.m_expr == '':
            return True

        try:
            if frame in self.m_locals_copy:
                l = self.m_locals_copy[frame]
                v = eval(bp.m_code, frame.f_globals, l)
            else:
                v = eval(bp.m_code, frame.f_globals, frame.f_locals)
                
            return (v != False)
        except:
            return False

    def set_local_trace(self, frame):
        if not self.m_core.m_ftrace:
            frame.f_trace = self.trace_dispatch_stop
            return

        code_context = self.m_core.get_code_context(frame.f_code)

        if self.m_core.is_break(self, frame):
            frame.f_trace = self.trace_dispatch_break
        elif code_context.m_fExceptionTrap or (frame.f_back == None):    
            frame.f_trace = self.trace_dispatch_trap
        elif frame.f_code.co_name in self.m_bp_manager.m_break_points_by_function:
            frame.f_trace = self.trace_dispatch
        elif frame in self.m_locals_copy:
            frame.f_trace = self.trace_dispatch
        elif frame == self.m_core.m_return_frame:
            frame.f_trace = self.trace_dispatch
        else:    
            del frame.f_trace

    def set_tracers(self): 
        try:
            try:
                f = self.frame_acquire()
                while f != None:
                    self.set_local_trace(f)
                    f = f.f_back
                    
            except ThreadDone:
                f = None
                
        finally:      
            f = None
            self.frame_release()

    def trace_dispatch_stop(self, frame, event, arg):
        if frame in self.m_locals_copy:
            self.update_locals()

        sys.settrace(None)
        sys.setprofile(None)
        return None

    def trace_dispatch_break(self, frame, event, arg):
        if event not in ['line', 'return', 'exception']:
            return frame.f_trace

        if event == 'exception':
            self.set_exc_info(arg)
            
        self.m_event = event
        self.m_core._break(self, frame, event, arg)
        if frame in self.m_locals_copy:
            self.update_locals()
            self.set_local_trace(frame)
        
        return frame.f_trace            

    def trace_dispatch_call(self, frame, event, arg):
        if not self.m_core.m_ftrace:
            return self.trace_dispatch_stop(frame, event, arg)
            
        self.m_frame = frame

        try:
            self.m_code_context = self.m_core.m_code_contexts[frame.f_code]
        except KeyError:
            self.m_code_context = self.m_core.get_code_context(frame.f_code)

        if self.m_core.m_fBreak or (self.m_core.m_step_tid == self.m_thread_id):
            self.m_event = event
            self.m_core._break(self, frame, event, arg)
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)
            return frame.f_trace

        if not frame.f_code.co_name in self.m_bp_manager.m_break_points_by_function:
            return None

        bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)
        if bp != None and self.__eval_breakpoint(frame, bp): 
            self.m_event = event
            self.m_core._break(self, frame, event, arg)
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)
            return frame.f_trace     
    
        return self.trace_dispatch     
        
    def trace_dispatch(self, frame, event, arg):
        if (event == 'line'):
            bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)                
            if bp != None and self.__eval_breakpoint(frame, bp): 
                self.m_event = event
                self.m_core._break(self, frame, event, arg)
                
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            return frame.f_trace     
                        
        if event == 'return':
            if frame == self.m_core.m_return_frame:
                self.m_event = event
                self.m_core._break(self, frame, event, arg)
                
            if frame in self.m_locals_copy:
                self.update_locals()

            return None     
            
        if event == 'exception':
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            if frame.f_exc_traceback == None:
                (frame.f_exc_type, frame.f_exc_value, frame.f_exc_traceback) = arg

            return frame.f_trace     

        return frame.f_trace     
        
    def trace_dispatch_trap(self, frame, event, arg):
        self.m_event = event

        if (event == 'line'):
            bp = self.m_code_context.m_file_breakpoints.get(frame.f_lineno, None)                
            if bp != None and self.__eval_breakpoint(frame, bp): 
                self.m_core._break(self, frame, event, arg)
                
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            return frame.f_trace     
                        
        if event == 'return':
            if frame == self.m_core.m_return_frame:
                self.m_core._break(self, frame, event, arg)
                
            if frame in self.m_locals_copy:
                self.update_locals()

            return None     
            
        if event == 'exception':
            if self.m_code_context.m_fExceptionTrap:                
                self.set_exc_info(arg)
                
                self.m_fUnhandledException = True
                self.m_core._break(self, frame, event, arg)

                if frame in self.m_locals_copy:
                    self.update_locals()
                    
                return frame.f_trace

            self.m_ue_lineno = frame.f_lineno
            
            if frame in self.m_locals_copy:
                self.update_locals()
                self.set_local_trace(frame)

            if frame.f_exc_traceback == None:
                (frame.f_exc_type, frame.f_exc_value, frame.f_exc_traceback) = arg

            return frame.f_trace     

        return frame.f_trace     
        
    def set_exc_info(self, arg):
        (t, v, tb) = arg

        while tb != None:
            f = tb.tb_frame            
            f.f_exc_type = t
            f.f_exc_value = v 
            f.f_exc_traceback = tb

            tb = tb.tb_next

    def is_breakpoint(self):
        bp = self.m_code_context.m_file_breakpoints.get(self.m_frame.f_lineno, None)
        if bp != None and self.__eval_breakpoint(self.m_frame, bp):
            return True

        return False    



class CDebuggerCore:
    def __init__(self):
        self.m_ftrace = True

        self.m_current_ctx = None 
        self.m_f_first_to_break = True
        self.m_f_break_on_init = False

        self.m_timer_embedded_giveup = None
        
        self.m_threads_lock = threading.Condition(threading.Lock())

        self.m_threads = {}

        self.m_event_dispatcher = CEventDispatcher()
        self.m_state_manager = CStateManager(STATE_RUNNING, self.m_event_dispatcher, event_dispatcher_sync = self.m_event_dispatcher)

        self.m_fBreak = False

        self.m_lastest_event = None
        self.m_step_tid = None
        self.m_next_frame = None
        self.m_return_frame = None       

        self.m_bp_manager = CBreakPointsManager()

        self.m_code_contexts = {None: None}

    def __del__(self):
        self.m_event_dispatcher.shutdown()
        self.m_state_manager.shutdown()
        
    def set_request_go_timer(self, timeout):
        if timeout == None:
            return
            
        _timeout = max(5.0, timeout)
        self.m_timer_embedded_giveup = threading.Timer(_timeout, self.request_go)
        self.m_timer_embedded_giveup.start()
    
    def cancel_request_go_timer(self):
        t = self.m_timer_embedded_giveup
        if t != None:
            self.m_timer_embedded_giveup = None
            t.cancel()
            
    def settrace(self, f = None, f_break_on_init = True, timeout = None):
        if not self.m_ftrace:
            return 
            
        tid = thread.get_ident()
        if tid in self.m_threads:
            return

        self.set_request_go_timer(timeout)
            
        self.m_f_break_on_init = f_break_on_init
        
        threading.settrace(self.trace_dispatch_init)
        sys.settrace(self.trace_dispatch_init)

        if f != None:
            f.f_trace = self.trace_dispatch_init

    def stoptrace(self):
        threading.settrace(None)
        sys.settrace(None)
        sys.setprofile(None)
        
        self.m_ftrace = False
        self.set_all_tracers()
        self.m_threads = {}

    def get_code_context(self, code):
        try:
            return self.m_code_contexts[code]
        except KeyError:
            code_context = CCodeContext(code, self.m_bp_manager)
            return self.m_code_contexts.setdefault(code, code_context)

    def get_current_ctx(self):
        if len(self.m_threads) == 0:
            raise NoThreads

        return self.m_current_ctx 
        
    def wait_for_first_thread(self):
        if self.m_current_ctx != None:
            return

        try:
            self.m_threads_lock.acquire() 

            while self.m_current_ctx == None:
                self.m_threads_lock.wait(1.0)

        finally:
            self.m_threads_lock.release()

    def notify_first_thread(self):
        try:
            self.m_threads_lock.acquire()
            self.m_threads_lock.notify()
        finally:
            self.m_threads_lock.release()

    def set_exception_trap_frame(self, frame):
        while frame != None:
            code_context = self.get_code_context(frame.f_code)
            if code_context.is_untraced():                
                code_context.m_fExceptionTrap = True
                return

            frame = frame.f_back

    def trace_dispatch_init(self, frame, event, arg):
        if event not in ['call', 'line', 'return']:
            return None

        code_context = self.get_code_context(frame.f_code)
        if code_context.is_untraced():
            return None
        
        self.set_exception_trap_frame(frame)

        ctx = CDebuggerCoreThread(self, frame, event)
        ctx.set_tracers()
        self.m_threads[ctx.m_thread_id] = ctx

        if len(self.m_threads) == 1:
            self.m_current_ctx = ctx
            self.notify_first_thread()

            if self.m_f_break_on_init:
                self.m_f_break_on_init = False
                self.request_break()            

        sys.settrace(ctx.trace_dispatch_call)
        sys.setprofile(ctx.profile)
        
        if event == 'call':
            return ctx.trace_dispatch_call(frame, event, arg)
        elif hasattr(frame, 'f_trace') and (frame.f_trace != None):    
            return frame.f_trace(frame, event, arg)
        else:
            return None

    def set_all_tracers(self):
        for ctx in self.m_threads.values():
            ctx.set_tracers()
            
    def remove_thread(self, thread_id):
        try:
            del self.m_threads[thread_id]
            
            if self.m_current_ctx.m_thread_id == thread_id:
                self.m_current_ctx = self.m_threads.values()[0]
                
        except (KeyError, IndexError):
            pass            

    def set_break_flag(self):
        self.m_fBreak = (self.m_state_manager.get_state() == STATE_BROKEN)
        
    def is_break(self, ctx, frame, event = None):
        if self.m_fBreak:
            return True

        if ctx.m_fUnhandledException:
            return True
            
        if self.m_step_tid == ctx.m_thread_id:
            return True

        if self.m_next_frame == frame:
            return True

        if (self.m_return_frame == frame) and (event == 'return'):
            return True

        return False    
        
    def _break(self, ctx, frame, event, arg):
        if not self.is_break(ctx, frame, event) and not ctx.is_breakpoint():
            ctx.set_tracers()
            return 
            
        ctx.m_fBroken = True
        f_full_notification = False
        
        try: 
            self.m_state_manager.acquire()
            if self.m_state_manager.get_state() != STATE_BROKEN:
                self.set_break_dont_lock()
            
            if self.m_f_first_to_break or (self.m_current_ctx == ctx):                
                self.m_current_ctx = ctx
                self.m_lastest_event = event

                self.m_step_tid = None
                self.m_next_frame = None
                self.m_return_frame = None       

                self.m_bp_manager.del_temp_breakpoint()

                self.m_f_first_to_break = False
                f_full_notification = True

        finally:
            self.m_state_manager.release()

        if f_full_notification:
            self.send_events(None) 
        else:
            self.notify_thread_broken(ctx.m_thread_id)
            self.notify_namespace()

        state = self.m_state_manager.wait_for_state([STATE_RUNNING])
        
        ctx.m_fUnhandledException = False        
        ctx.m_fBroken = False 
        ctx.set_tracers()

    def notify_thread_broken(self, tid):
        _event = CEventThreadBroken(tid)
        self.m_event_dispatcher.fire_event(_event)
    
    def notify_namespace(self):
        _event = CEventNamespace()
        self.m_event_dispatcher.fire_event(_event)

    def get_state(self):
        return self.m_state_manager.get_state()

    def verify_broken(self):
        if self.m_state_manager.get_state() != STATE_BROKEN:
            raise DebuggerNotBroken
    
    def get_current_filename(self, frame_index, fException):
        ctx = self.get_current_ctx()
        
        try:
            f = None
            base_frame = ctx.frame_acquire()

            (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)
            frame_filename = my_abspath(f.f_code.co_filename)

            return frame_filename

        finally:
            f = None
            base_frame = None            
            ctx.frame_release()
        
    def get_threads(self):
        return self.m_threads

    def set_break_dont_lock(self):
        self.m_f_first_to_break = True            

        self.m_state_manager.set_state(STATE_BROKEN, fLock = False)

        self.set_break_flag()
        self.set_all_tracers()

    def request_break(self):
        if len(self.m_threads) == 0:
            self.wait_for_first_thread()
        
        try:
            self.m_state_manager.acquire()
            if self.m_state_manager.get_state() == STATE_BROKEN:
                return

            self.set_break_dont_lock()

        finally:    
            self.m_state_manager.release()

        self.send_events(None)

    def request_go(self, fLock = True):
        try:
            if fLock:
                self.m_state_manager.acquire()
                
            self.verify_broken()

            self.m_state_manager.set_state(STATE_RUNNING, fLock = False)
            self.set_break_flag()

        finally:    
            if fLock:
                self.m_state_manager.release()

    def request_go_breakpoint(self, filename, scope, lineno, frame_index, fException):
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            if filename in [None, '']:
                _filename = self.get_current_filename(frame_index, fException)
            else:
                _filename = FindFile(filename, fModules = True)
                
            self.m_bp_manager.set_temp_breakpoint(_filename, scope, lineno)
            self.set_all_tracers()
            self.request_go(fLock = False)

        finally:    
            self.m_state_manager.release()

    def request_step(self, fLock = True):
        try:
            if fLock:
                self.m_state_manager.acquire()
                
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return
                
            self.m_step_tid = ctx.m_thread_id
            self.m_next_frame = None
            self.m_return_frame = None       

            self.request_go(fLock = False)

        finally:    
            if fLock:
                self.m_state_manager.release()
        
    def request_next(self): 
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return
                
            if self.m_lastest_event in ['return', 'exception']:
                return self.request_step(fLock = False)

            self.m_next_frame = ctx.m_frame
            self.m_return_frame = None
            
            self.request_go(fLock = False)

        finally:    
            self.m_state_manager.release()
        
    def request_return(self):    
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return
                
            if self.m_lastest_event == 'return':
                return self.request_step(fLock = False)
                
            self.m_next_frame = None
            self.m_return_frame = ctx.m_frame

            self.request_go(fLock = False)

        finally:    
            self.m_state_manager.release()
        
    def request_jump(self, lineno):
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                ctx = self.get_current_ctx()
            except NoThreads:
                return
                
            frame = ctx.m_frame
            code = frame.f_code

            valid_lines = CalcValidLines(code)
            sbi = CScopeBreakInfo('', valid_lines)
            l = sbi.CalcScopeLine(lineno)

            frame.f_lineno = l

        finally:    
            frame = None
            self.m_state_manager.release()

        self.send_events(None)

    def set_thread(self, tid):
        try:
            self.m_state_manager.acquire()
            self.verify_broken()

            try:
                if (tid >= 0) and (tid < 100):
                    _tid = self.m_threads.keys()[tid]
                else:
                    _tid = tid
                    
                ctx = self.m_threads[_tid]
            except (IndexError, KeyError):
                raise ThreadNotFound

            self.m_current_ctx = ctx
            self.m_lastest_event = ctx.m_event

        finally:
            self.m_state_manager.release()

        self.send_events(None) 



class CDebuggerEngine(CDebuggerCore):
    def __init__(self):
        CDebuggerCore.__init__(self)

        event_type_dict = {
            CEventState: {}, 
            CEventStackDepth: {}, 
            CEventBreakpoint: {}, 
            CEventThreads: {},
            CEventNoThreads: {},
            CEventThreadBroken: {},
            CEventNamespace: {},
            CEventStack: {},
            CEventExit: {}
            }
        
        self.m_event_queue = CEventQueue(self.m_event_dispatcher)
        self.m_event_queue.register_event_types(event_type_dict)

        event_type_dict = {CEventSync: {}}
        self.m_event_dispatcher.register_callback(self.send_events, event_type_dict, fSingleUse = False)

        atexit.register(self.atexit)

    def __del__(self):
        self.m_event_queue.shutdown()
        
        CDebuggerCore.__del__(self)
        
    def atexit(self):
        event = CEventExit()
        self.m_event_dispatcher.fire_event(event)
        time.sleep(1.0)
        
    def sync_with_events(self, fException):
        if len(self.m_threads) == 0:
            self.wait_for_first_thread()
        
        index = self.m_event_queue.get_event_index()
        event = CEventSync(fException)
        self.m_event_dispatcher.fire_event(event)
        return index

    def wait_for_event(self, timeout, nStateChange):
        self.cancel_request_go_timer()
        
        (n, sel) = self.m_event_queue.wait_for_event(timeout, nStateChange)
        return (n, sel)

    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr, frame_index, fException):
        if expr != '':
            try:
                compile(expr, '', 'eval')
            except:
                raise SyntaxError

        fLock = False
        
        try:    
            if filename in [None, '']:
                self.m_state_manager.acquire()
                fLock = True
                self.verify_broken()
                
                _filename = self.get_current_filename(frame_index, fException)
            else:
                _filename = FindFile(filename, fModules = True)
                
            bp = self.m_bp_manager.set_breakpoint(_filename, scope, lineno, fEnabled, expr)
            self.set_all_tracers()

            event = CEventBreakpoint(bp)
            self.m_event_dispatcher.fire_event(event)

        finally:
            if fLock:
                self.m_state_manager.release()
        
    def disable_breakpoint(self, id_list, fAll):
        self.m_bp_manager.disable_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.DISABLE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)

        return 0
        
    def enable_breakpoint(self, id_list, fAll):
        self.m_bp_manager.enable_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.ENABLE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)

        return 0
        
    def delete_breakpoint(self, id_list, fAll):
        self.m_bp_manager.delete_breakpoint(id_list, fAll)
        self.set_all_tracers()

        event = CEventBreakpoint(None, CEventBreakpoint.REMOVE, id_list, fAll)
        self.m_event_dispatcher.fire_event(event)

        return 0
        
    def get_breakpoints(self):
        bpl = self.m_bp_manager.get_breakpoints()
        _items = [(id, copy.copy(bp)) for (id, bp) in bpl.items()]
        for (id, bp) in _items:
            bp.m_code = None
            
        _bpl = dict(_items)
        
        return _bpl        

    def send_events(self, event):
        if isinstance(event, CEventSync):
            fException = event.m_fException
        else:
            fException = False

        #traceback.print_stack()
        
        try:
            self.send_stack_depth()
            self.send_threads_event(fException)
            self.send_stack_event(fException)
            self.send_namespace_event()

        except NoThreads:
            self.send_no_threads_event()
            
        except:
            print_debug()
            raise
    
    def send_stack_depth(self):
        ctx = self.get_current_ctx()
        
        try:
            try:
                f = None
                f = ctx.frame_acquire()
            except ThreadDone:
                return

            try:
                g_traceback_lock.acquire()
                s = traceback.extract_stack(f)
                
            finally:    
                g_traceback_lock.release()

            stack_depth = len(s)

            if f.f_exc_traceback == None:
                stack_depth_exception = None
            else:    
                try:
                    g_traceback_lock.acquire()
                    _s = traceback.extract_tb(f.f_exc_traceback)
                    
                finally:    
                    g_traceback_lock.release()

                stack_depth_exception = stack_depth + len(_s) - 1

            event = CEventStackDepth(stack_depth, stack_depth_exception)
            self.m_event_dispatcher.fire_event(event)
            
        finally:
            f = None
            ctx.frame_release()
            
    def send_threads_event(self, fException):
        tl = self.get_thread_list()
            
        if fException:
            ctid = tl[0]
            itl = tl[1]
            _itl = [a for a in itl if a[DICT_KEY_TID] == ctid]
            _tl = (ctid, _itl)
        else:
            _tl = tl

        event = CEventThreads(*_tl)
        self.m_event_dispatcher.fire_event(event)

    def send_stack_event(self, fException):
        sl = self.get_stack([], False, fException)

        if len(sl) == 0:
            return
            
        event = CEventStack(sl[0])
        self.m_event_dispatcher.fire_event(event)
        
    def send_namespace_event(self):
        event = CEventNamespace()
        self.m_event_dispatcher.fire_event(event)

    def send_no_threads_event(self):
        _event = CEventNoThreads()
        self.m_event_dispatcher.fire_event(_event)
        
    def __get_stack(self, ctx, ctid, fException):
        tid = ctx.m_thread_id    

        try:
            try:
                f = None
                f = ctx.frame_acquire()
            except ThreadDone:
                return None

            _f = f

            try:
                g_traceback_lock.acquire()
                s = traceback.extract_stack(f)
                
            finally:    
                g_traceback_lock.release()

            if fException: 
                if f.f_exc_traceback == None:
                    raise NoExceptionFound

                _tb = f.f_exc_traceback
                while _tb.tb_next != None:
                    _tb = _tb.tb_next

                _f = _tb.tb_frame    
                    
                try:
                    g_traceback_lock.acquire()
                    _s = traceback.extract_tb(f.f_exc_traceback)
                    
                finally:    
                    g_traceback_lock.release()

                s = s[:-1] + _s

            code_list = []
            while _f != None:
                rc = repr(_f.f_code).split(',')[0].split()[-1]
                code_list.insert(0, rc)
                _f = _f.f_back
                
        finally:
            f = None
            _f = None
            ctx.frame_release()

        #print code_list

        __s = [(my_abspath(a), b, c, d) for (a, b, c, d) in s]

        if (ctx.m_uef_lineno != None) and (len(__s) > 0):
            (a, b, c, d) = __s[0]
            __s = [(a, ctx.m_uef_lineno, c, d)] + __s[1:] 
            
        r = {}
        r[DICT_KEY_STACK] = __s
        r[DICT_KEY_CODE_LIST] = code_list
        r[DICT_KEY_TID] = tid
        r[DICT_KEY_BROKEN] = ctx.m_fBroken
        r[DICT_KEY_EVENT] = ctx.m_event
        
        if tid == ctid:
            r[DICT_KEY_CURRENT_TID] = True
            
        return r
    
    def get_stack(self, tid_list, fAll, fException):
        if fException and (fAll or (len(tid_list) != 0)):
            raise BadArgument

        ctx = self.get_current_ctx()       
        ctid = ctx.m_thread_id

        if fAll:
            ctx_list = self.get_threads().values()
        elif fException or (len(tid_list) == 0):
            ctx_list = [ctx]
        else:
            ctx_list = [self.get_threads().get(t, None) for t in tid_list]

        _sl = [self.__get_stack(ctx, ctid, fException) for ctx in ctx_list if ctx != None]
        sl = [s for s in _sl if s != None] 
        
        return sl

    def get_source_file(self, filename, lineno, nlines, frame_index, fException):  
        if lineno < 1:
            lineno = 1
            nlines = -1

        #if (filename != '') and not IsPythonSourceFile(filename):
        #    raise IOError
            
        _lineno = lineno
        r = {}
        frame_filename = None
        
        try:
            ctx = self.get_current_ctx()

            try:
                f = None
                base_frame = None
                
                base_frame = ctx.frame_acquire()
                (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)
                frame_filename = my_abspath(f.f_code.co_filename)

            finally:
                f = None
                base_frame = None            
                ctx.frame_release()

            frame_event = [[ctx.m_event, 'call'][frame_index > 0], 'exception'][fException]
            
        except NoThreads:
            if filename in [None, '']:
                raise
            
        if filename in [None, '']:
            __filename = frame_filename
            r[DICT_KEY_TID] = ctx.m_thread_id
        else:
            __filename = FindFile(filename, fModules = True)

        _filename = winlower(__filename)    

        lines = []
        breakpoints = {}
        
        while nlines != 0:
            try:
                g_traceback_lock.acquire()
                line = linecache.getline(_filename, _lineno)
                
            finally:    
                g_traceback_lock.release()

            if line == '':
                break

            lines.append(line)

            try:
                bp = self.m_bp_manager.get_breakpoint(_filename, _lineno)
                breakpoints[_lineno] = [STATE_DISABLED, STATE_ENABLED][bp.isEnabled()]
            except KeyError:
                pass
                
            _lineno += 1
            nlines -= 1

        if frame_filename == _filename:
            r[DICT_KEY_FRAME_LINENO] = frame_lineno
            r[DICT_KEY_EVENT] = frame_event
            r[DICT_KEY_BROKEN] = ctx.m_fBroken
            
        r[DICT_KEY_LINES] = lines
        r[DICT_KEY_FILENAME] = _filename
        r[DICT_KEY_BREAKPOINTS] = breakpoints
        r[DICT_KEY_FIRST_LINENO] = lineno
        
        return r
            
    def __get_source(self, ctx, nlines, frame_index, fException):
        tid = ctx.m_thread_id
        _frame_index = [0, frame_index][tid == self.m_current_ctx.m_thread_id]

        try:
            try:
                f = None
                base_frame = None
                
                base_frame = ctx.frame_acquire()
                (f, frame_lineno)  = ctx.get_frame(base_frame, _frame_index, fException)
                frame_filename = my_abspath(f.f_code.co_filename)
                
            except (ThreadDone, InvalidFrame):
                return None

        finally:
            f = None
            base_frame = None            
            ctx.frame_release()
            
        frame_event = [[ctx.m_event, 'call'][frame_index > 0], 'exception'][fException]

        first_line = max(1, frame_lineno - nlines / 2)     
        _lineno = first_line

        lines = []
        breakpoints = {}
        
        while nlines != 0:
            try:
                g_traceback_lock.acquire()
                line = linecache.getline(frame_filename, _lineno)
                
            finally:    
                g_traceback_lock.release()

            if line == '':
                break

            lines.append(line)

            try:
                bp = self.m_bp_manager.get_breakpoint(frame_filename, _lineno)
                breakpoints[_lineno] = [STATE_DISABLED, STATE_ENABLED][bp.isEnabled()]
            except KeyError:
                pass
                
            _lineno += 1
            nlines -= 1

        r = {}
        
        r[DICT_KEY_FRAME_LINENO] = frame_lineno
        r[DICT_KEY_EVENT] = frame_event
        r[DICT_KEY_BROKEN] = ctx.m_fBroken
        r[DICT_KEY_TID] = tid
        r[DICT_KEY_LINES] = lines
        r[DICT_KEY_FILENAME] = frame_filename
        r[DICT_KEY_BREAKPOINTS] = breakpoints
        r[DICT_KEY_FIRST_LINENO] = first_line
        
        return r
     
    def get_source_lines(self, nlines, fAll, frame_index, fException):
        if fException and fAll:
            raise BadArgument
            
        if fAll:
            ctx_list = self.get_threads().values()
        else:
            ctx = self.get_current_ctx()
            ctx_list = [ctx]

        _sl = [self.__get_source(ctx, nlines, frame_index, fException) for ctx in ctx_list]
        sl = [s for s in _sl if s != None]    

        return sl

    def __get_locals_globals(self, frame_index, fException, fReadOnly = False):
        ctx = self.get_current_ctx()
        (_globals, _locals) = ctx.get_locals_copy(frame_index, fException, fReadOnly)

        return (_globals, _locals)

    def __is_verbose_attr(self, r, a):
        try:
            v = getattr(r, a)
        except AttributeError:
            return True
            
        if a == '__class__':
            if self.__parse_type(type(v)) != 'type':
                return False

            #return self.__parse_type(v) in BASIC_TYPES_LIST

        if (a == '__bases__'):
            if (type(v) == tuple) and (len(v) > 0):    
                return False

        if a in ['__name__', '__file__', '__doc__']:
            return False
        
        if a.startswith('__') and a.endswith('__'):
            return True
        
        if self.__is_property_attr(r, a):
            return True
            
        t = self.__parse_type(type(v))

        if ('method' in t) and not ('builtin' in t):
            return True

        return False    

    def __is_property_attr(self, r, a):
        if a.startswith('__') and a.endswith('__'):
            return False

        try:
            v = getattr(r, a)            
        except AttributeError:
            return False
            
        t = self.__parse_type(type(v))
        
        if 'descriptor' in t:
            return True
            
        if t == 'property':
            return True
            
        return False    

    def __calc_property_list(self, r):
        pl = [a for a in r.__dict__.keys() if self.__is_property_attr(r, a)]

        for b in r.__bases__:
            if (self.__parse_type(type(b)) == 'type') and (self.__parse_type(b) == 'object'):
                continue

            pl += self.__calc_property_list(b)

        return pl    
        
    def __calc_attribute_list(self, r):
        if hasattr(r, '__dict__'):
            al = r.__dict__.keys()
        else:
            al = [a for a in dir(r)]

        if hasattr(r, '__class__') and not '__class__' in al:
            al = ['__class__'] + al

        if hasattr(r, '__bases__') and not '__bases__' in al:
            al = ['__bases__'] + al

        if hasattr(r, '__class__'):
            pl = self.__calc_property_list(r.__class__)
            _pl = [p for p in pl if not p in al]
            
            al += _pl

        _al = [a for a in al if hasattr(r, a)]           
        __al = [a for a in _al if not self.__is_verbose_attr(r, a)]    

        return __al
    
    def __calc_number_of_subnodes(self, r):
        if self.__parse_type(type(r)) in BASIC_TYPES_LIST:
            return 0
            
        if type(r) in [dict, list, tuple]:
            return len(r)

        return len(self.__calc_attribute_list(r))

    def __parse_type(self, t):
        rt = repr(t)
        st = rt.split("'")[1]
        return st
        
    def __calc_subnodes(self, expr, r, fForceNames, fFilter):
        snl = []
        
        if type(r) in [list, tuple]:
            for i, v in enumerate(r):
                e = {}
                e[DICT_KEY_EXPR] = '%s[%d]' % (expr, i)
                e[DICT_KEY_NAME] = repr(i)
                e[DICT_KEY_REPR] = safe_repr_limited(v)
                e[DICT_KEY_TYPE] = self.__parse_type(type(v))
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

                snl.append(e)

            return snl

        if type(r) == dict:
            for k, v in r.items():
                rt = self.__parse_type(type(v))
                if fFilter and (rt in ['function', 'module', 'classobj']):
                    continue
                    
                e = {}
                e[DICT_KEY_EXPR] = '%s[%s]' % (expr, repr(k))
                e[DICT_KEY_NAME] = [repr(k), k][fForceNames]
                e[DICT_KEY_REPR] = safe_repr_limited(v)
                e[DICT_KEY_TYPE] = rt
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

                snl.append(e)

            return snl            

        al = self.__calc_attribute_list(r)
        for a in al:
            try:
                v = getattr(r, a)
            except AttributeError:
                continue
            
            e = {}
            e[DICT_KEY_EXPR] = '%s.%s' % (expr, a)
            e[DICT_KEY_NAME] = a
            e[DICT_KEY_REPR] = safe_repr_limited(v)
            e[DICT_KEY_TYPE] = self.__parse_type(type(v))
            e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(v)

            snl.append(e)

        return snl                

    def get_exception(self, frame_index, fException):
        ctx = self.get_current_ctx()

        try:
            f = None
            base_frame = None
            
            base_frame = ctx.frame_acquire()
            (f, frame_lineno) = ctx.get_frame(base_frame, frame_index, fException)

            e = {'type': f.f_exc_type, 'value': f.f_exc_value, 'traceback': f.f_exc_traceback}

            return e
            
        finally:
            f = None
            base_frame = None            
            ctx.frame_release()
        
    def get_namespace(self, nl, fFilter, frame_index, fException):
        try:
            (_globals, _locals) = self.__get_locals_globals(frame_index, fException, fReadOnly = True)
        except:    
            print_debug()
            raise

        rl = []
        for (expr, fExpand) in nl:
            e = {}

            try:
                __globals = _globals
                __locals = _locals
                
                if RPDB_EXEC_INFO in expr:
                    rpdb_exception_info = self.get_exception(frame_index, fException)
                    __globals = globals()
                    __locals = locals()
                    
                r = eval(expr, __globals, __locals)

                e[DICT_KEY_EXPR] = expr
                e[DICT_KEY_REPR] = safe_repr_limited(r)
                e[DICT_KEY_TYPE] = self.__parse_type(type(r))
                e[DICT_KEY_N_SUBNODES] = self.__calc_number_of_subnodes(r)

                if fExpand and (DICT_KEY_SUBNODES > 0):
                    fForceNames = (expr in ['globals()', 'locals()']) or (RPDB_EXEC_INFO in expr)
                    _fFilter = fFilter and (expr == 'globals()')
                    e[DICT_KEY_SUBNODES] = self.__calc_subnodes(expr, r, fForceNames, _fFilter)
                    
            except:
                print_debug()
                e[DICT_KEY_ERROR] = repr(sys.exc_info())
            
            rl.append(e)

        return rl 
            
    def evaluate(self, expr, frame_index, fException):
        (_globals, _locals) = self.__get_locals_globals(frame_index, fException)

        v = ''
        w = ''
        e = ''

        try:
            r = eval(expr, _globals, _locals)
            v = safe_repr(r)
        except:
            exc_info = sys.exc_info()
            e = "%s, %s" % (str(exc_info[0]), str(exc_info[1]))

        self.notify_namespace()

        return (v, w, e)
        
    def execute(self, suite, frame_index, fException):
        (_globals, _locals) = self.__get_locals_globals(frame_index, fException)

        w = ''
        e = ''

        try:    
            exec suite in _globals, _locals
        except:    
            exc_info = sys.exc_info()
            e = "%s, %s" % (str(exc_info[0]), str(exc_info[1]))

        self.notify_namespace()
        
        return (w, e)

    def get_thread_list(self):
        ctx = self.get_current_ctx()
        
        if ctx == None:
            current_thread_id = -1
        else:
            current_thread_id = ctx.m_thread_id  
            
        ctx_list = self.get_threads().values()
        tl = [{DICT_KEY_TID: c.m_thread_id, DICT_KEY_BROKEN: c.m_fBroken, DICT_KEY_EVENT: c.m_event} for c in ctx_list]

        return (current_thread_id, tl)

    def _abort(self):
        time.sleep(1.0)
        os.abort()
        
    def stop_debuggee(self):
        self.atexit()
        threading.Thread(target = self._abort).start()


    
#
# ------------------------------------- RPC Server --------------------------------------------
#



class CWorkQueue:
    def __init__(self, n_threads):
        self.m_lock = threading.Condition()
        self.m_work_items = []
        self.m_f_shutdown = False
        self.m_n_threads = 0
        
        for n in range(n_threads):
            t = threading.Thread(target = self.worker_target)
            t.setDaemon(1)
            t.start()

    def shutdown(self):
        self.m_lock.acquire()
        self.m_f_shutdown = True
        self.m_lock.notifyAll()

        while self.m_n_threads > 0:
            self.m_lock.wait()
            
        self.m_lock.release()

    def worker_target(self): 
        #
        # Turn tracing off. We don't want debugger threads traced.
        #
        sys.settrace(None)
        sys.setprofile(None)

        try:
            self.m_lock.acquire()

            self.m_n_threads += 1

            while not self.m_f_shutdown:
                self.m_lock.wait()

                if self.m_f_shutdown:
                    break
                    
                if len(self.m_work_items) == 0:
                    continue
                    
                (target, args) = self.m_work_items.pop()

                self.m_lock.release()
                
                try:
                    target(*args)
                except:
                    print_debug()

                self.m_lock.acquire()    
                    
            self.m_n_threads -= 1
            self.m_lock.notifyAll()
            
        finally:
            self.m_lock.release()

    def post_work_item(self, target, args):
        try:
            self.m_lock.acquire()
            self.m_work_items.append((target, args))
            self.m_lock.notify()
        finally:
            self.m_lock.release()
                
        
            
class CUnTracedThreadingMixIn(SocketServer.ThreadingMixIn):
    def init_work_queue(self):
        self.m_work_queue = CWorkQueue(N_WORK_QUEUE_THREADS)
    
    def shutdown_work_queue(self):
        self.m_work_queue.shutdown()

    def process_request(self, request, client_address):
        self.m_work_queue.post_work_item(target = SocketServer.ThreadingMixIn.process_request_thread, args = (self, request, client_address))



def my_xmlrpclib_loads(data):
    """data -> unmarshalled data, method name

    Convert an XML-RPC packet to unmarshalled data plus a method
    name (None if not present).

    If the XML-RPC packet represents a fault condition, this function
    raises a Fault exception.
    """
    p, u = xmlrpclib.getparser()
    p.feed(data)
    p.close()
    return u.close(), u.getmethodname()



class CXMLRPCServer(CUnTracedThreadingMixIn, SimpleXMLRPCServer.SimpleXMLRPCServer):
    def __marshaled_dispatch(self, data, dispatch_method = None):
        """Dispatches an XML-RPC method from marshalled (XML) data.

        XML-RPC methods are dispatched from the marshalled (XML) data
        using the _dispatch method and the result is returned as
        marshalled data. For backwards compatibility, a dispatch
        function can be provided as an argument (see comment in
        SimpleXMLRPCRequestHandler.do_POST) but overriding the
        existing method through subclassing is the prefered means
        of changing method dispatch behavior.
        """

        params, method = my_xmlrpclib_loads(data)

        # generate response
        try:
            if dispatch_method is not None:
                response = dispatch_method(method, params)
            else:
                response = self._dispatch(method, params)
            # wrap response in a singleton tuple
            response = (response,)
            response = xmlrpclib.dumps(response, methodresponse=1)
        except xmlrpclib.Fault, fault:
            response = xmlrpclib.dumps(fault)
        except:
            # report exception back to server
            response = xmlrpclib.dumps(
                xmlrpclib.Fault(1, "%s:%s" % (sys.exc_type, sys.exc_value))
                )
            print_debug()

        return response

    if sys.version_info[:2] <= (2, 3):
        _marshaled_dispatch = __marshaled_dispatch



class CPwdServerProxy:
    def __init__(self, crypto, uri, transport = None, target_rid = 0):
        self.m_crypto = crypto       
        self.m_proxy = xmlrpclib.ServerProxy(uri, transport)

        self.m_fEncryption = is_encryption_supported()
        self.m_target_rid = target_rid

        self.m_method = getattr(self.m_proxy, DISPACHER_METHOD)
 
    def __set_encryption(self, fEncryption):
        self.m_fEncryption = fEncryption

    def get_encryption(self):
        return self.m_fEncryption

    def __request(self, name, params):
        while True:
            try:
                _params = self.m_crypto.do_crypto((name, params, self.m_target_rid), self.get_encryption())

                rpdb_version = get_interface_compatibility_version()

                r = self.m_method(rpdb_version + _params)

                ((max_index, _r, e), fe)= self.m_crypto.undo_crypto(r, fVerifyIndex = False)

                if e != None:
                    raise e

            except AuthenticationBadIndex, e:
                self.m_crypto.set_index(e.m_max_index, e.m_anchor)
                continue

            except xmlrpclib.Fault, fault:
                if str(BadVersion) in fault.faultString:
                    s = fault.faultString.split("'")
                    version = ['', s[1]][len(s) > 0]
                    raise BadVersion(version)
                if str(EncryptionExpected) in fault.faultString:
                    raise EncryptionExpected
                elif str(EncryptionNotSupported) in fault.faultString:
                    if self.m_crypto.m_fAllowUnencrypted:
                        self.__set_encryption(False)
                        continue
                    raise EncryptionNotSupported
                elif str(DecryptionFailure) in fault.faultString:
                    raise DecryptionFailure
                elif str(AuthenticationBadData) in fault.faultString:
                    raise AuthenticationBadData
                elif str(AuthenticationFailure) in fault.faultString:
                    raise AuthenticationFailure
                else:
                    print_debug()
                    assert False 

            except xmlrpclib.ProtocolError:
                print_debug()
                raise CConnectionException
                
            return _r

    def __getattr__(self, name):
        return xmlrpclib._Method(self.__request, name)


    
class CIOServer(threading.Thread):
    def __init__(self, pwd, fAllowUnencrypted, fRemote, rid):
        threading.Thread.__init__(self)

        self.m_crypto = CCrypto(pwd, fAllowUnencrypted, rid)
        
        self.m_fRemote = fRemote
        self.m_rid = rid
        
        self.m_port = None
        self.m_stop = False
        self.m_server = None
        
        self.setDaemon(True)

    def __del__(self):
        self.stop()
    
    def stop(self):
        if self.m_stop:
            return
            
        self.m_stop = True

        try:
            proxy = CPwdServerProxy(self.m_crypto, calcURL("localhost", self.m_port))
            proxy.null()
        except (socket.error, CException):
            pass

        self.join()

        self.m_server.shutdown_work_queue()
        self.m_server = None
        
    def export_null(self):
        return 0

    def run(self):
        #
        # Turn tracing off. We don't want debugger threads traced.
        #

        sys.settrace(None)
        sys.setprofile(None)
        
        (self.m_port, self.m_server) = self.__StartXMLRPCServer()

        self.m_server.init_work_queue()
        self.m_server.register_function(self.dispatcher_method)        
        
        while not self.m_stop:
            self.m_server.handle_request()
        
    def dispatcher_method(self, params):
        r = None
        e = None

        rpdb_version = get_interface_compatibility_version()

        if params[: len(rpdb_version)] != rpdb_version:
            raise BadVersion(get_version())

        _params = params[len(rpdb_version):]
            
        try:
            ((name, _params, target_rid), fEncryption) = self.m_crypto.undo_crypto(_params)
        except AuthenticationBadIndex, _e:
            print_debug()
            e = _e 
            fEncryption = self.m_crypto.is_encrypted(_params)                           

        if e == None:
            try:
                # We are forcing the 'export_' prefix on methods that are
                # callable through XML-RPC to prevent potential security
                # problems
                func = getattr(self, 'export_' + name)
            except AttributeError:
                raise Exception('method "%s" is not supported' % ('export_' + name, ))

            try:
                if (target_rid != 0) and (target_rid != self.m_rid):
                    raise NotAttached
                    
                r = func(*_params)
            except Exception, _e:
                print_debug()
                e = _e            

        max_index = self.m_crypto.get_max_index()

        _r = self.m_crypto.do_crypto((max_index, r, e), fEncryption)

        return _r

    def __StartXMLRPCServer(self):
        host = [LOCAL_HOST, ""][self.m_fRemote]
        port = SERVER_PORT_RANGE_START

        while True:
            try:
                server = CXMLRPCServer((host, port), logRequests = 0)
                
                return (port, server)
            except socket.error, e:
                if not GetSocketError(e) in [ERROR_SOCKET_ADDRESS_IN_USE_WIN, ERROR_SOCKET_ADDRESS_IN_USE_UNIX]:
                    raise
                    
                if port >= SERVER_PORT_RANGE_START + SERVER_PORT_RANGE_LENGTH - 1:
                    raise

                port += 1
                continue



class CServerInfo:
    def __init__(self, age, port, pid, filename, rid, state):
        self.m_age = age 
        self.m_port = port
        self.m_pid = pid
        self.m_filename = filename
        self.m_module_name = CalcModuleName(filename)
        self.m_rid = rid
        self.m_state = state

    def __str__(self):
        return 'age: %d, port: %d, pid: %d, filename: %s, rid: %s' % (self.m_age, self.m_port, self.m_pid, self.m_filename, self.m_rid)


        
class CDebuggeeServer(CIOServer):
    def __init__(self, filename, debugger, pwd, fAllowUnencrypted, fRemote, rid = None):
        if rid == None:
            rid = generate_rid()
            
        CIOServer.__init__(self, pwd, fAllowUnencrypted, fRemote, rid)
        
        self.m_filename = filename
        self.m_pid = _getpid()
        self.m_time = time.time()
        self.m_debugger = debugger
        self.m_rid = rid
                
    def export_server_info(self):
        age = time.time() - self.m_time
        state = self.m_debugger.get_state()
        si = CServerInfo(age, self.m_port, self.m_pid, self.m_filename, self.m_rid, state)
        return si

    def export_sync_with_events(self, fException):
        ei = self.m_debugger.sync_with_events(fException)
        return ei

    def export_wait_for_event(self, timeout, nStateChange):
        (n, s) = self.m_debugger.wait_for_event(timeout, nStateChange)
        return (n, s)
                
    def export_set_breakpoint(self, filename, scope, lineno, fEnabled, expr, frame_index, fException):
        self.m_debugger.set_breakpoint(filename, scope, lineno, fEnabled, expr, frame_index, fException)
        return 0
        
    def export_disable_breakpoint(self, id_list, fAll):
        self.m_debugger.disable_breakpoint(id_list, fAll)
        return 0
        
    def export_enable_breakpoint(self, id_list, fAll):
        self.m_debugger.enable_breakpoint(id_list, fAll)
        return 0
        
    def export_delete_breakpoint(self, id_list, fAll):
        self.m_debugger.delete_breakpoint(id_list, fAll)
        return 0
        
    def export_get_breakpoints(self):
        bpl = self.m_debugger.get_breakpoints()
        return bpl
        
    def export_request_break(self):
        self.m_debugger.request_break()
        return 0

    def export_request_go(self):
        self.m_debugger.request_go()
        return 0

    def export_request_go_breakpoint(self, filename, scope, lineno, frame_index, fException):
        self.m_debugger.request_go_breakpoint(filename, scope, lineno, frame_index, fException)
        return 0

    def export_request_step(self):
        self.m_debugger.request_step()
        return 0

    def export_request_next(self):
        self.m_debugger.request_next()
        return 0

    def export_request_return(self):
        self.m_debugger.request_return()
        return 0

    def export_request_jump(self, lineno):
        self.m_debugger.request_jump(lineno)
        return 0

    def export_get_stack(self, tid_list, fAll, fException):
        r = self.m_debugger.get_stack(tid_list, fAll, fException)                 
        return r
    
    def export_get_source_file(self, filename, lineno, nlines, frame_index, fException): 
        r = self.m_debugger.get_source_file(filename, lineno, nlines, frame_index, fException)
        return r

    def export_get_source_lines(self, nlines, fAll, frame_index, fException): 
        r = self.m_debugger.get_source_lines(nlines, fAll, frame_index, fException)
        return r
        
    def export_get_thread_list(self):
        r = self.m_debugger.get_thread_list()
        return r
        
    def export_set_thread(self, tid):
        self.m_debugger.set_thread(tid)   
        return 0

    def export_get_namespace(self, nl, fFilter, frame_index, fException):
        r = self.m_debugger.get_namespace(nl, fFilter, frame_index, fException)
        return r
        
    def export_evaluate(self, expr, frame_index, fException):
        (v, w, e) = self.m_debugger.evaluate(expr, frame_index, fException)
        return (v, w, e)
        
    def export_execute(self, suite, frame_index, fException):
        (w, e) = self.m_debugger.execute(suite, frame_index, fException)
        return (w, e)
        
    def export_stop_debuggee(self):
        self.m_debugger.stop_debuggee()
        return 0
        
#
# ------------------------------------- RPC Client --------------------------------------------
#



class CTimeoutHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        """Connect to the host and port specified in __init__."""
        msg = "getaddrinfo returns an empty list"
        for res in socket.getaddrinfo(self.host, self.port, 0,
                                      socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.settimeout(PING_TIMEOUT)
                if self.debuglevel > 0:
                    print >> sys.__stderr__, "connect: (%s, %s)" % (self.host, self.port)
                self.sock.connect(sa)
            except socket.error, msg:
                if self.debuglevel > 0:
                    print >> sys.__stderr__, 'connect fail:', (self.host, self.port)
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error, msg



class CTimeoutHTTP(httplib.HTTP):
    _connection_class = CTimeoutHTTPConnection

    
        
class CTimeoutTransport(xmlrpclib.Transport):
    def make_connection(self, host):
        # create a HTTP connection object from a host descriptor
        host, extra_headers, x509 = self.get_host_info(host)
        return CTimeoutHTTP(host)

    
    
class CSession:
    def __init__(self, host, port, pwd, fAllowUnencrypted, rid):
        self.m_crypto = CCrypto(pwd, fAllowUnencrypted, rid)

        self.m_host = host
        self.m_port = port
        self.m_proxy = None
        self.m_server_info = None
        self.m_exc_info = None

        self.m_fShutDown = False

    def get_encryption(self):
        return self.m_proxy.get_encryption()
        
    def getServerInfo(self):
        return self.m_server_info

    def shut_down(self):
        self.m_fShutDown = True
        
    def getProxy(self):
        if self.m_fShutDown:
            raise NotAttached
            
        return self.m_proxy

    def Connect(self):
        server = CPwdServerProxy(self.m_crypto, calcURL(self.m_host, self.m_port), CTimeoutTransport())
        server_info = server.server_info()

        self.m_proxy = CPwdServerProxy(self.m_crypto, calcURL(self.m_host, self.m_port), target_rid = server_info.m_rid)
        self.m_server_info = server_info
                
    def ConnectNoThrow(self):
        try:
            self.Connect()
        except:
            #print_debug()
            self.m_exc_info = sys.exc_info() 

    def ConnectAsync(self):
        t = threading.Thread(target = self.ConnectNoThrow)
        t.setDaemon(True)
        t.start()
        return t

    def isConnected(self):
        return self.m_proxy != None

    

class CServerList:
    def __init__(self, host):
        self.m_host = host
        self.m_list = []
        self.m_errors = {}

    def calcList(self, pwd, rid, report_exception):
        sil = []
        sessions = []
        self.m_errors = {}

        port = SERVER_PORT_RANGE_START
        while port < SERVER_PORT_RANGE_START + SERVER_PORT_RANGE_LENGTH:
            s = CSession(self.m_host, port, pwd, fAllowUnencrypted = True, rid = rid)
            t = s.ConnectAsync()
            sessions.append((s, t))

            port += 1

        for (s, t) in sessions:
            t.join()

            if (s.m_exc_info != None):
                #print >> sys.__stderr__, s.m_exc_info[0]
                if issubclass(s.m_exc_info[0], CException):
                    _i = self.m_errors.get(s.m_exc_info[0], 0)
                    self.m_errors[s.m_exc_info[0]] = _i + 1
                    report_exception(*s.m_exc_info)

                continue

            si = s.getServerInfo()
            if si != None:
                sil.append((-si.m_age, si))
        
        sil.sort()
        self.m_list = [s[1] for s in sil]
        return self.m_list 

    def get_errors(self):
        return self.m_errors

    def findServers(self, key):
        fname = False

        try:
            n = int(key)
        except ValueError:   
            fname = True

        if fname:
            _s = [s for s in self.m_list if key in s.m_filename]
        else:
            _s = [s for s in self.m_list if (s.m_pid == n) or (s.m_rid == key)]

        if _s == []:
            raise UnknownServer

        return _s    



class CSessionManagerInternal:
    def __init__(self, pwd, fAllowUnencrypted, fRemote, host):
        self.m_pwd = [pwd, None][pwd in [None, '']]
        self.m_fAllowUnencrypted = fAllowUnencrypted
        self.m_fRemote = fRemote
        self.m_rid = generate_rid()
        
        self.m_host = host
        self.m_server_list_object = CServerList(host)

        self.m_session = None
        self.m_server_info = None
        
        self.m_worker_thread = None
        self.m_worker_thread_ident = None
        self.m_fStop = False

        self.m_stack_depth = None
        self.m_stack_depth_exception = None
        self.m_frame_index = 0
        self.m_frame_index_exception = 0

        self.m_remote_event_index = 0
        self.m_event_dispatcher_proxy = CEventDispatcher()
        self.m_event_dispatcher = CEventDispatcher(self.m_event_dispatcher_proxy)
        self.m_state_manager = CStateManager(STATE_DETACHED, self.m_event_dispatcher, self.m_event_dispatcher_proxy)

        self.m_breakpoints_proxy = CBreakPointsManagerProxy(self)
        
        event_type_dict = {CEventState: {EVENT_EXCLUDE: [STATE_BROKEN, STATE_ANALYZE]}}
        self.register_callback(self.reset_frame_indexes, event_type_dict, fSingleUse = False)
        event_type_dict = {CEventStackDepth: {}}
        self.register_callback(self.set_stack_depth, event_type_dict, fSingleUse = False)
        event_type_dict = {CEventNoThreads: {}}
        self.register_callback(self._reset_frame_indexes, event_type_dict, fSingleUse = False)
        
        self.m_printer = self.__nul_printer

    def __del__(self):
        self.m_event_dispatcher_proxy.shutdown()
        self.m_event_dispatcher.shutdown()
        self.m_state_manager.shutdown()
        
    def __nul_printer(self, str):
        pass
        
    def set_printer(self, printer):
        self.m_printer = printer

    def register_callback(self, callback, event_type_dict, fSingleUse):
        return self.m_event_dispatcher.register_callback(callback, event_type_dict, fSingleUse)
        
    def remove_callback(self, callback):
        return self.m_event_dispatcher.remove_callback(callback)

    def __wait_for_debuggee(self, rid):
        for i in range(0,STARTUP_RETRIES):
            try:
                self.m_server_list_object.calcList(self.m_pwd, self.m_rid, self.report_exception)
                return self.m_server_list_object.findServers(rid)[0]
            except UnknownServer:
                time.sleep(STARTUP_TIMEOUT)
                continue
                
        self.m_server_list_object.calcList(self.m_pwd, self.m_rid, self.report_exception)
        return self.m_server_list_object.findServers(rid)[0]

    def get_encryption(self):
        return self.getSession().get_encryption()
    
    def launch_nothrow(self, command_line):
        try:
            self.launch(command_line)
        except:
            pass

    def launch(self, command_line):
        self.__verify_unattached()
        
        if self.m_pwd == None:
            self.set_random_password()
            
        if command_line == '':
            raise BadArgument

        (path, filename, args) = split_command_line_path_filename_args(command_line)

        if not IsPythonSourceFile(filename):
            raise IOError
           
        ExpandedFilename = FindFile(filename, [path])
        self.set_host("localhost")

        self.m_printer(STR_STARTUP_SPAWN_NOTICE)

        rid = generate_rid()

        self.m_state_manager.set_state(STATE_SPAWNING)

        try:
            try:
                self.__spawn_server(ExpandedFilename, args, rid)            
            except SpawnUnsupported:    
                self.m_printer(STR_AUTOMATIC_LAUNCH_UNKNOWN)
                raise

            try:
                server = self.__wait_for_debuggee(rid)
            except UnknownServer:
                self.m_printer(STR_STARTUP_FAILURE)
                raise
                
            self.attach(server.m_rid, server.m_filename)
        except:
            if self.m_state_manager.get_state() != STATE_DETACHED:
                self.m_state_manager.set_state(STATE_DETACHED)

            raise    

    def __spawn_server(self, ExpandedFilename, args, rid):
        """
        Start an OS console to act as server.
        What it does is to start rpdb again in a new console in server only mode.
        """

        if g_fScreen:
            name = 'screen'
        else:
            try:
                import terminalcommand
                name = 'mac'
            except:
                if not os.name in osSpawn:
                   raise SpawnUnsupported
                   
                name = os.name
        
        e = ['', ' --plaintext'][self.m_fAllowUnencrypted]
        r = ['', ' --remote'][self.m_fRemote]

        debugger = os.path.abspath(__file__)
        if debugger[-1:] == 'c':
            debugger = debugger[:-1]

        debug_prints = ['', '--debug'][g_fDebug]    
            
        options = '"%s" %s --debugee --pwd="%s"%s%s --rid=%s "%s" %s' % (debugger, debug_prints, self.m_pwd, e, r, rid, ExpandedFilename, args)
        command = osSpawn[name] % (sys.executable, options)

        if name == 'mac':
            terminalcommand.run(command)
        else:
            os.popen(command)
    
    def attach_nothrow(self, key):
        try:
            self.attach(key)
        except:
            pass

    def attach(self, key, name = None):
        self.__verify_unattached()

        if key == '':
            raise BadArgument

        if self.m_pwd == None:
            self.m_printer(STR_PASSWORD_MUST_BE_SET)
            raise UnsetPassword
        
        if name == None:
            name = key

        _name = name
        
        self.m_printer(STR_STARTUP_NOTICE)
        self.m_state_manager.set_state(STATE_ATTACHING)

        try:
            self.m_server_list_object.calcList(self.m_pwd, self.m_rid, self.report_exception)                
            servers = self.m_server_list_object.findServers(key)
            server = servers[0] 

            _name = server.m_filename
            
            errors = self.m_server_list_object.get_errors()
            if (server.m_rid != key) and (len(errors) > 0):
                self.__report_server_errors(errors)

            self.__attach(server)
            if len(servers) > 1:
                self.m_printer(STR_MULTIPLE_DEBUGGEES % (key, ))
            self.m_printer(STR_ATTACH_CRYPTO_MODE % ([' ' + STR_ATTACH_CRYPTO_MODE_NOT, ''][self.get_encryption()], ))    
            self.m_printer(STR_ATTACH_SUCCEEDED % (server.m_filename, ))
            return

        except (socket.error, CConnectionException):
            self.report_exception(*sys.exc_info())
            self.m_printer(STR_ATTACH_FAILED_NAME % (_name, ))
            self.m_state_manager.set_state(STATE_DETACHED)
            raise
        except:
            print_debug()
            assert False
            
    def report_exception(self, type, value, tb):
        if type == socket.error:
            self.m_printer(STR_COMMUNICATION_FAILURE)
        elif type == BadVersion:
            self.m_printer((STR_BAD_VERSION % (value.m_version, )))
        elif type == UnexpectedData:
            self.m_printer(STR_UNEXPECTED_DATA)
        elif type == AlreadyAttached:
            self.m_printer(STR_ALREADY_ATTACHED)
        elif type == NotAttached:
            self.m_printer(STR_NOT_ATTACHED)
        elif type == NoThreads:
            self.m_printer(STR_NO_THREADS)
        elif type == SpawnUnsupported:
            self.m_printer(STR_AUTOMATIC_LAUNCH_UNKNOWN)
        elif type == UnknownServer:
            self.m_printer(STR_DEBUGGEE_UNKNOWN)
        elif type == UnsetPassword:
            self.m_printer(STR_PASSWORD_MUST_BE_SET)
        elif type == EncryptionNotSupported:
            self.m_printer(STR_DEBUGGEE_NO_ENCRYPTION)
        elif type == EncryptionExpected:
            self.m_printer(STR_ENCRYPTION_EXPECTED2)
        elif type == DecryptionFailure:
            self.m_printer(STR_DECRYPTION_FAILURE)
        elif type == AuthenticationBadData:
            self.m_printer(STR_ACCESS_DENIED2)
        elif type == AuthenticationFailure:
            self.m_printer(STR_ACCESS_DENIED2)
            
    def __report_server_errors(self, errors):
        for k in errors.keys():
            if k == AuthenticationBadData:
                self.m_printer(STR_ACCESS_DENIED)
            if k == AuthenticationFailure:
                self.m_printer(STR_ACCESS_DENIED)
            if k == EncryptionExpected:
                self.m_printer(STR_ENCRYPTION_EXPECTED)
            if k == BadVersion:
                self.m_printer(STR_BAD_VERSION)
        
    def __attach(self, server):
        self.__verify_unattached()

        session = CSession(self.m_host, server.m_port, self.m_pwd, self.m_fAllowUnencrypted, self.m_rid)
        session.Connect()

        if (session.getServerInfo().m_pid != server.m_pid) or (session.getServerInfo().m_filename != server.m_filename):
            raise UnexpectedData

        self.m_session = session
        
        self.m_server_info = self.get_server_info()

        self.refresh()
        self.__start_event_monitor()

        self.request_break()
        self.enable_breakpoint([], fAll = True)
        
    def __verify_unattached(self):
        if self.__is_attached():
            raise AlreadyAttached
            
    def __verify_attached(self):
        if not self.__is_attached():
            raise NotAttached

    def __is_attached(self):
        return (self.m_state_manager.get_state() != STATE_DETACHED) and (self.m_session != None)
            
    def __verify_broken(self):
        if self.m_state_manager.get_state() not in [STATE_BROKEN, STATE_ANALYZE]:
            raise DebuggerNotBroken
    
    def refresh(self):
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        self.m_remote_event_index = self.getSession().getProxy().sync_with_events(fAnalyzeMode)
        self.m_breakpoints_proxy.sync()
        
    def __start_event_monitor(self):        
        self.m_fStop = False
        self.m_worker_thread = threading.Thread(target = self.__event_monitor_proc)
        self.m_worker_thread.setDaemon(True)
        self.m_worker_thread.start()
        
    def __event_monitor_proc(self):
        self.m_worker_thread_ident = thread.get_ident()
        t = 0
        
        while not self.m_fStop:
            try:
                t = ControlRate(t, IDLE_MAX_RATE)
                if self.m_fStop:
                    return
                    
                (n, sel) = self.getSession().getProxy().wait_for_event(PING_TIMEOUT, self.m_remote_event_index)

                if True in [isinstance(e, CEventExit) for e in sel]:
                    self.getSession().shut_down()
                    self.m_fStop = True
                
                if n > self.m_remote_event_index:
                    #print >> sys.__stderr__, (n, sel)                      
                    self.m_remote_event_index = n
                    self.m_event_dispatcher_proxy.fire_events(sel)

            except CConnectionException:
                self.report_exception(*sys.exc_info())
                threading.Thread(target = self.detach).start()
                return
                
            except socket.error:
                self.report_exception(*sys.exc_info())
                #threading.Thread(target = self.detach).start()
                #return
            
    def detach(self):
        self.m_printer(STR_ATTEMPTING_TO_DETACH)

        self.m_state_manager.set_state(STATE_DETACHING)

        self.__stop_event_monitor()

        try:
            self.disable_breakpoint([], fAll = True)
            self.request_go()
        except (socket.error, CConnectionException):
            pass
        except:
            print_debug()

        self.m_state_manager.set_state(STATE_DETACHED)

        self.m_session = None

        self.m_printer(STR_DETACH_SUCCEEDED)

    def __stop_event_monitor(self):
        self.m_fStop = True
        if self.m_worker_thread != None:
            if thread.get_ident() != self.m_worker_thread_ident:  
                self.m_worker_thread.join()

            self.m_worker_thread = None
            self.m_worker_thread_ident = None
        
    def request_break(self):
        self.getSession().getProxy().request_break()
    
    def request_go(self):
        self.getSession().getProxy().request_go()
    
    def request_go_breakpoint(self, filename, scope, lineno):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        self.getSession().getProxy().request_go_breakpoint(filename, scope, lineno, frame_index, fAnalyzeMode)

    def request_step(self):
        self.getSession().getProxy().request_step()

    def request_next(self):
        self.getSession().getProxy().request_next()

    def request_return(self):
        self.getSession().getProxy().request_return()

    def request_jump(self, lineno):
        self.getSession().getProxy().request_jump(lineno)
    
    def set_breakpoint(self, filename, scope, lineno, fEnabled, expr):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        self.getSession().getProxy().set_breakpoint(filename, scope, lineno, fEnabled, expr, frame_index, fAnalyzeMode)
        
    def disable_breakpoint(self, id_list, fAll):
        self.getSession().getProxy().disable_breakpoint(id_list, fAll)
    
    def enable_breakpoint(self, id_list, fAll):
        self.getSession().getProxy().enable_breakpoint(id_list, fAll)
    
    def delete_breakpoint(self, id_list, fAll):
        self.getSession().getProxy().delete_breakpoint(id_list, fAll)
    
    def get_breakpoints(self):
        self.__verify_attached()

        bpl = self.m_breakpoints_proxy.get_breakpoints()            
        return bpl
        
    def save_breakpoints(self, _filename = ''):        
        bpl = self.get_breakpoints()
        sbpl = cPickle.dumps(bpl)

        if _filename == '':
            filename = self.getSession().getServerInfo().m_module_name + BREAKPOINTS_FILE_EXT
        else: 
            filename = _filename + BREAKPOINTS_FILE_EXT
            
        file = open(filename, 'wb')
        file.write(sbpl)
        file.close()

    def load_breakpoints(self, _filename = ''):
        self.__verify_attached()

        _e = None
        
        if _filename == '':
            filename = self.getSession().getServerInfo().m_module_name + BREAKPOINTS_FILE_EXT
        else: 
            filename = _filename + BREAKPOINTS_FILE_EXT

        file = open(filename, 'rb')
        try:
            bpl = cPickle.load(file)
            for bp in bpl.values():
                try:
                    self.set_breakpoint(bp.m_filename, bp.m_scope_fqn, bp.m_scope_offset, bp.m_fEnabled, bp.m_expr)
                except (socket.error, CConnectionException), e:
                    _e = e
        finally:
            file.close()

        if _e != None:
            raise _e

    def get_stack(self, tid_list, fAll):    
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 
        r = self.getSession().getProxy().get_stack(tid_list, fAll, fAnalyzeMode)
        return r

    def get_source_file(self, filename, lineno, nlines): 
        #if (filename != '') and not IsPythonSourceFile(filename):
        #    raise IOError
            
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        r = self.getSession().getProxy().get_source_file(filename, lineno, nlines, frame_index, fAnalyzeMode)
        return r        

    def get_source_lines(self, nlines, fAll): 
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        r = self.getSession().getProxy().get_source_lines(nlines, fAll, frame_index, fAnalyzeMode)
        return r
        
    def get_thread_list(self):
        (current_thread_id, thread_list) = self.getSession().getProxy().get_thread_list()
        return (current_thread_id, thread_list)
        
    def set_thread(self, tid):
        self.reset_frame_indexes(None)
        self.getSession().getProxy().set_thread(tid)
        
    def get_namespace(self, nl, fFilter):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        r = self.getSession().getProxy().get_namespace(nl, fFilter, frame_index, fAnalyzeMode)
        return r

    def evaluate(self, expr):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE) 

        (value, warning, error) = self.getSession().getProxy().evaluate(expr, frame_index, fAnalyzeMode)
        return (value, warning, error)
        
    def execute(self, suite):
        frame_index = self.get_frame_index()
        fAnalyzeMode = (self.m_state_manager.get_state() == STATE_ANALYZE)

        (warning, error) = self.getSession().getProxy().execute(suite, frame_index, fAnalyzeMode)
        return (warning, error)

    def set_host(self, host):
        self.__verify_unattached()
        
        socket.getaddrinfo(host, 0)        
        self.m_host = host
        self.m_server_list_object = CServerList(host)

    def get_host(self):
        return self.m_host

    def calc_server_list(self):
        if self.m_pwd == None:
            raise UnsetPassword
        
        server_list = self.m_server_list_object.calcList(self.m_pwd, self.m_rid, self.report_exception)
        errors = self.m_server_list_object.get_errors()

        return (server_list, errors)

    def get_server_info(self): 
        return self.getSession().getServerInfo()

    def get_last_debuggee_name_safe(self):
        si = self.m_server_info
        if si == None:
            return ''
        return si.m_filename    

    def _reset_frame_indexes(self, event):
        self.reset_frame_indexes(None)
    
    def reset_frame_indexes(self, event):
        try:
            self.m_state_manager.acquire()
            if event == None:
                self.__verify_broken()
            elif self.m_state_manager.get_state() in [STATE_BROKEN, STATE_ANALYZE]:
                return

            self.m_stack_depth = None
            self.m_stack_depth_exception = None
            self.m_frame_index = 0
            self.m_frame_index_exception = 0

        finally:
            self.m_state_manager.release()

    def set_stack_depth(self, event):
        try:
            self.m_state_manager.acquire()
            self.__verify_broken()

            self.m_stack_depth = event.m_stack_depth
            self.m_stack_depth_exception = event.m_stack_depth_exception
            self.m_frame_index = min(self.m_frame_index, self.m_stack_depth - 1)
            self.m_frame_index_exception = min(self.m_frame_index_exception, self.m_stack_depth_exception - 1)

        finally:
            self.m_state_manager.release()
        
    def set_frame_index(self, frame_index):
        try:
            self.m_state_manager.acquire()
            self.__verify_broken()

            if (frame_index < 0) or (self.m_stack_depth == None):
                return self.get_frame_index(fLock = False)

            if self.m_state_manager.get_state() == STATE_ANALYZE:
                self.m_frame_index_exception = min(frame_index, self.m_stack_depth_exception - 1)
                si = self.m_frame_index_exception

            else:    
                self.m_frame_index = min(frame_index, self.m_stack_depth - 1)
                si = self.m_frame_index

        finally:
            self.m_state_manager.release()

        event = CEventStackFrameChange(si)
        self.m_event_dispatcher.fire_event(event)

        event = CEventNamespace()
        self.m_event_dispatcher.fire_event(event)

        return si

    def get_frame_index(self, fLock = True):
        try:
            if fLock:
                self.m_state_manager.acquire()
                
            self.__verify_attached()

            if self.m_state_manager.get_state() == STATE_ANALYZE:
                return self.m_frame_index_exception
            else:    
                return self.m_frame_index

        finally:
            if fLock:
                self.m_state_manager.release()

    def set_analyze(self, fAnalyze):
        try:
            self.m_state_manager.acquire()

            if fAnalyze and (self.m_state_manager.get_state() != STATE_BROKEN):
                raise DebuggerNotBroken
                
            if (not fAnalyze) and (self.m_state_manager.get_state() != STATE_ANALYZE):
                return
                
            state = [STATE_BROKEN, STATE_ANALYZE][fAnalyze]
            self.m_state_manager.set_state(state, fLock = False)

        finally:
            self.m_state_manager.release()

            self.refresh()
    
    def getSession(self):
        self.__verify_attached()

        return self.m_session

    def get_state(self):
        return self.m_state_manager.get_state()

    def set_password(self, pwd):    
        try:
            self.m_state_manager.acquire()

            self.__verify_unattached()
            
            self.m_pwd = pwd
        finally:
            self.m_state_manager.release()

    def set_random_password(self):
        try:
            self.m_state_manager.acquire()

            self.__verify_unattached()
            
            self.m_pwd = generate_random_password()
            self.m_printer(STR_RANDOM_PASSWORD)        

        finally:
            self.m_state_manager.release()
            
    def get_password(self):
        return self.m_pwd

    def set_remote(self, fRemote):
        try:
            self.m_state_manager.acquire()

            self.__verify_unattached()
            
            self.m_fRemote = fRemote
        finally:
            self.m_state_manager.release()

    def get_remote(self):
        return self.m_fRemote

    def stop_debuggee(self):
        self.getSession().getProxy().stop_debuggee()


    
class CConsoleInternal(cmd.Cmd, threading.Thread):
    def __init__(self, session_manager, stdin = None, stdout = None, fSplit = False):
        cmd.Cmd.__init__(self, stdin = stdin, stdout = stdout)
        threading.Thread.__init__(self)
        
        self.fAnalyzeMode = False
        self.fPrintBroken = True

        self.m_filename = None
        
        self.use_rawinput = [1, 0][fSplit]
        self.m_fSplit = fSplit
        self.prompt = [[CONSOLE_PROMPT, CONSOLE_PROMPT_ANALYZE][self.fAnalyzeMode], ""][fSplit]
        self.intro = CONSOLE_INTRO
        self.setDaemon(True)

        event_type_dict = {CEventState: {}}
        
        self.m_session_manager = session_manager
        self.m_session_manager.set_printer(self.printer)
        self.m_session_manager.register_callback(self.event_handler, event_type_dict, fSingleUse = False)

        event_type_dict = {CEventExit: {}}
        self.m_session_manager.register_callback(self.event_atexit, event_type_dict, fSingleUse = False)
        
        self.m_last_source_line = None
        self.m_last_nlines = DEFAULT_NUMBER_OF_LINES
        
        self.m_fAddPromptBeforeMsg = False
        self.m_eInLoop = threading.Event()
        self.cmdqueue.insert(0, '')

    def set_filename(self, filename):
        self.m_filename = filename

    def event_atexit(self, event):
        self.printer(STR_DEBUGGEE_TERMINATED)        
        self.do_detach("")
        
    def precmd(self, line):
        self.m_fAddPromptBeforeMsg = True
        if not self.m_eInLoop.isSet():
            self.m_eInLoop.set()

        if not line.strip():
            return line
            
        command = line.split(' ', 1)[0].split(SOURCE_MORE, 1)[0].split(SOURCE_LESS, 1)[0]
        if command not in ['list', 'l']:
            self.m_last_source_line = None
            self.m_last_nlines = DEFAULT_NUMBER_OF_LINES

        return line    
            
    def postcmd(self, stop, line):
        self.m_fAddPromptBeforeMsg = False

        return stop

    def run(self):
        self.cmdloop()

    def __get_str_wrap(self, str, max_len):
        if len(str) <= max_len:
            return (str, '')

        s = str[: max_len]
        i = s.rfind(' ')
        if i == -1:
            return (s, str[max_len:])

        return (str[: i], str[i + 1:])    
            
    def printer(self, str):
        if not self.m_eInLoop.isSet():
            self.m_eInLoop.wait()

        fAPBM = self.m_fAddPromptBeforeMsg    
        prefix = ['', self.prompt.strip('\n')][fAPBM] + CONSOLE_PRINTER
        suffix = '\n' + [self.prompt.strip('\n'), ''][fAPBM]

        s = str
        while s != '':
            s, _s = self.__get_str_wrap(s, CONSOLE_WRAP_INDEX - len(prefix + suffix))
            self.stdout.write(prefix + s + suffix)
            s = _s 

    def print_notice(self, notice):
        nl = notice.split('\n')

        i = 0
        for l in nl:
            print >> self.stdout, l
            i += 1
            if i % PRINT_NOTICE_LINES_PER_SECTION == 0:
                print >> self.stdout, "\n" + PRINT_NOTICE_PROMPT,
                response = self.stdin.readline()
                if response != '\n':
                    break

                print >> self.stdout
        
    def event_handler(self, event): 
        state = event.m_state
        if (state == STATE_BROKEN) and self.fPrintBroken:
            self.fPrintBroken = False
            self.printer(STR_DEBUGGER_HAS_BROKEN)
            return

        if (state != STATE_ANALYZE) and self.fAnalyzeMode:
            self.fAnalyzeMode = False
            self.prompt = [CONSOLE_PROMPT, ""][self.m_fSplit]
            self.printer(STR_ANALYZE_MODE_TOGGLE % (MODE_OFF, ))
            return
        
        if (state == STATE_ANALYZE) and not self.fAnalyzeMode:
            self.fAnalyzeMode = True
            self.prompt = [CONSOLE_PROMPT_ANALYZE, ""][self.m_fSplit]
            self.printer(STR_ANALYZE_MODE_TOGGLE % (MODE_ON, ))
            return
        
    def do_launch(self, arg):
        if arg == '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        self.fPrintBroken = True

        try:
            self.m_session_manager.launch(arg)
            return
            
        except (socket.error, CConnectionException):
            pass
        except BadArgument:
            print >> self.stdout, STR_BAD_ARGUMENT
        except IOError:
            print >> self.stdout, 'File', arg, ' not found.'
        
        self.fPrintBroken = False

    def do_attach(self, arg):
        if arg == '':
            return self.__scripts(arg)
            
        self.fPrintBroken = True

        try:
            self.m_session_manager.attach(arg)
            return
            
        except (socket.error, CConnectionException):
            pass
        except BadArgument:
            print >> self.stdout, STR_BAD_ARGUMENT
        
        self.fPrintBroken = False

    def __scripts(self, arg):
        if self.m_session_manager.get_password() == None:
            print >> self.stdout, STR_PASSWORD_MUST_BE_SET
            return

        host = self.m_session_manager.get_host()
        print >> self.stdout, STR_SCRIPTS_CONNECTING % (host, )

        try:
            (server_list, errors) = self.m_session_manager.calc_server_list()
            for k in errors.keys():
                if k == AuthenticationBadData:
                    print >> self.stdout, STR_ACCESS_DENIED
                if k == AuthenticationFailure:
                    print >> self.stdout, STR_ACCESS_DENIED
                if k == EncryptionExpected:
                    print >> self.stdout, STR_ENCRYPTION_EXPECTED
                if k == BadVersion:
                    print >> self.stdout, STR_BAD_VERSION

        except UnsetPassword:
            print >> self.stdout, STR_PASSWORD_MUST_BE_SET
            return

        if server_list == []:
            print >> self.stdout, STR_SCRIPTS_NO_SCRIPTS % (host, )
            return

        try:
            spid = self.m_session_manager.get_server_info().m_pid
        except NotAttached:
            spid = None

        print >> self.stdout, STR_SCRIPTS_TO_DEBUG % (host, )    
        for s in server_list:
            m = ['', SYMBOL_MARKER][spid == s.m_pid]
            print >> self.stdout, ' %1s %-5d  %s' % (m, s.m_pid, s.m_filename)

    def do_detach(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        self.m_session_manager.save_breakpoints()
        self.m_session_manager.detach()

    def do_host(self, arg):
        if arg == '':
            host = self.m_session_manager.get_host()
            print >> self.stdout, host
            return

        try:
            self.m_session_manager.set_host(arg)
        except socket.gaierror, e:
            print >> self.stdout, STR_HOST_UNKNOWN % (arg, )
        except AlreadyAttached:
            print >> self.stdout, STR_ALREADY_ATTACHED
        
    def do_break(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        try:
            self.m_session_manager.request_break()
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_b = do_break
    
    def __parse_bp_arg(self, arg, fAllowExpr = True):
        _args = arg.split(BP_EVAL_SEP)

        if (len(_args) > 1) and (not fAllowExpr):
            raise BadArgument
            
        if len(_args) > 1:
            expr = _args[1].strip()
        else:
            expr = ''

        rf = _args[0].rfind(BP_FILENAME_SEP)
        if rf == -1:
            args = [_args[0]]
        else:
            args = [_args[0][:rf], _args[0][rf + 1:]]

        filename = ['', args[0]][len(args) > 1]

        if filename in [None, '']:
            filename = self.m_filename

        try:
            lineno = int(args[-1])
            scope = ''
        except ValueError:
            lineno = 0
            scope = args[-1].strip()

        return (filename, scope, lineno, expr)
    
    def do_go(self, arg):
        if self.fAnalyzeMode:
            print >> self.stdout, STR_ILEGAL_ANALYZE_MODE_CMD
            return

        try:
            if arg != '':
                (filename, scope, lineno, expr) = self.__parse_bp_arg(arg, fAllowExpr = False)
                self.fPrintBroken = True
                self.m_session_manager.request_go_breakpoint(filename, scope, lineno)
                return
            
            self.fPrintBroken = True
            self.m_session_manager.request_go()
            return
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except BadArgument:    
            print >> self.stdout, STR_BAD_ARGUMENT
        except IOError:
            print >> self.stdout, STR_FILE_NOT_FOUND % (filename, )
        except InvalidScopeName:
            print >> self.stdout, STR_SCOPE_NOT_FOUND % (scope, )
        except DebuggerNotBroken:
            print >> self.stdout, STR_DEBUGGEE_NOT_BROKEN

        self.fPrintBroken = False

    do_g = do_go

    def do_step(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        if self.fAnalyzeMode:
            print >> self.stdout, STR_ILEGAL_ANALYZE_MODE_CMD
            return

        try:
            self.m_session_manager.request_step()
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_s = do_step

    def do_next(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        if self.fAnalyzeMode:
            print >> self.stdout, STR_ILEGAL_ANALYZE_MODE_CMD
            return

        try:
            self.m_session_manager.request_next()
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_n = do_next
    
    def do_return(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        if self.fAnalyzeMode:
            print >> self.stdout, STR_ILEGAL_ANALYZE_MODE_CMD
            return

        try:
            self.m_session_manager.request_return()
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_r = do_return
    
    def do_jump(self, arg):
        try:
            lineno = int(arg)
        except ValueError:
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        try:
            self.m_session_manager.request_jump(lineno)
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    do_j = do_jump
    
    def do_bp(self, arg):
        if arg == '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
        
        try:
            (filename, scope, lineno, expr) = self.__parse_bp_arg(arg, fAllowExpr = True)
            self.m_session_manager.set_breakpoint(filename, scope, lineno, True, expr)
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except BadArgument:    
            print >> self.stdout, STR_BAD_ARGUMENT
        except IOError:
            print >> self.stdout, STR_FILE_NOT_FOUND % (filename, )
        except InvalidScopeName:
            print >> self.stdout, STR_SCOPE_NOT_FOUND % (scope, )
        except SyntaxError:
            print >> self.stdout, STR_BAD_EXPRESSION % (expr, )
        except DebuggerNotBroken:
            print >> self.stdout, STR_DEBUGGEE_NOT_BROKEN

    def do_be(self, arg):
        if arg == '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)
            
            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.enable_breakpoint(id_list, fAll)
        except ValueError:
            print >> self.stdout, STR_BAD_ARGUMENT
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    def do_bd(self, arg):
        if arg == '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)
            
            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.disable_breakpoint(id_list, fAll)
        except ValueError:
            print >> self.stdout, STR_BAD_ARGUMENT
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    def do_bc(self, arg):
        if arg == '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        try:
            id_list = []
            fAll = (arg == SYMBOL_ALL)
            
            if not fAll:
                sid_list = arg.split()
                id_list = [int(sid) for sid in sid_list]

            self.m_session_manager.delete_breakpoint(id_list, fAll)
        except ValueError:
            print >> self.stdout, STR_BAD_ARGUMENT
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    def do_bl(self, arg):
        try:
            bpl = self.m_session_manager.get_breakpoints()
                
            bplk = bpl.keys()
            bplk.sort()
            
            print >> self.stdout, STR_BREAKPOINTS_LIST    
            for id in bplk:
                bp = bpl[id]
                state = [STATE_DISABLED, STATE_ENABLED][bp.isEnabled()]
                print >> self.stdout, ' %2d  %-8s  %-15s  %5d  %-19s  %s' % (id, state, calc_suffix(bp.m_filename, 15), bp.m_lineno, calc_suffix(bp.m_scope_fqn, 19), calc_prefix(bp.m_expr, 20))
                
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())

    def do_save(self, arg):
        try:
            self.m_session_manager.save_breakpoints(arg)
            print >> self.stdout, STR_BREAKPOINTS_SAVED    
            return
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except IOError:
            print >> self.stdout, STR_BAD_FILENAME

        print >> self.stdout, STR_BREAKPOINTS_NOT_SAVED    
        
    def do_load(self, arg):
        try:
            self.m_session_manager.load_breakpoints(arg)
            print >> self.stdout, STR_BREAKPOINTS_LOADED    
            return
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except cPickle.PickleError:
            print >> self.stdout, STR_BAD_FILE_DATA
        except IOError:
            print >> self.stdout, STR_BREAKPOINTS_FILE_NOT_FOUND

    def do_stack(self, arg):
        if self.fAnalyzeMode and (arg != ''):
            print >> self.stdout, STR_ILEGAL_ANALYZE_MODE_ARG
            return

        try:
            tid_list = []
            fAll = (arg == SYMBOL_ALL)
            
            if not fAll:
                sid_list = arg.split()
                tid_list = [int(sid) for sid in sid_list]
                
            sl = self.m_session_manager.get_stack(tid_list, fAll)

            if len(sl) == 0:
                print >> self.stdout, STR_NO_THREADS_FOUND
                return

            frame_index = self.m_session_manager.get_frame_index()

            m = None    
            for st in sl:
                s = st.get(DICT_KEY_STACK, [])
                tid = st.get(DICT_KEY_TID, 0)
                fBroken = st.get(DICT_KEY_BROKEN, False)
                fCurrent = st.get(DICT_KEY_CURRENT_TID, False)

                if m != None:
                    print >> self.stdout
                    
                print >> self.stdout, STR_STACK_TRACE % (tid, )    
                i = 0
                while i < len(s):
                    e = s[-(1 + i)]

                    if not fBroken:
                        m = ['', SOURCE_STATE_UNBROKEN][i == 0]
                    elif fCurrent:
                        m = ['', SYMBOL_MARKER][i == frame_index]
                    else:
                        m = ['', SYMBOL_MARKER][i == 0]
                        
                    print >> self.stdout, ' %1s %5d  %-28s  %4d  %s' % (m, i, calc_suffix(e[0], 28), e[1], calc_prefix(e[2], 20))
                    i += 1
        except (socket.error, NoThreads, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except ValueError:
            print >> self.stdout, STR_BAD_ARGUMENT
        except NoExceptionFound:
            print >> self.stdout, STR_EXCEPTION_NOT_FOUND

    do_k = do_stack
    
    def do_list(self, arg):
        __args = arg.split(BP_FILENAME_SEP)
        __args2 = __args[-1]
        if len(__args) > 1:
            _filename = __args[0]
        else:
            _filename = ''
                
        _args = __args2.split(BP_EVAL_SEP)
        
        fAll = (_args[0] == SYMBOL_ALL)
        fMore = (_args[0] == SOURCE_MORE)
        fLess = (_args[0] == SOURCE_LESS)
        fEntire = (_args[0] == SOURCE_ENTIRE_FILE)
        fCurrent = (_args[0] == '')
        fLine = False
        l = 1
        
        try:
            if len(_args) > 1:
                nlines = int(_args[1])
            else:
                nlines = self.m_last_nlines

            if not (fAll or fMore or fLess or fEntire or fCurrent):     
                l = int(_args[0])
                fLine = True

        except ValueError:
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        if self.fAnalyzeMode and fAll:
            print >> self.stdout, STR_ILEGAL_ANALYZE_MODE_ARG
            return

        if fMore and self.m_last_source_line:
            l = max(1, self.m_last_source_line + self.m_last_nlines / 2 + 1)
            fLine = True
        elif fLess and self.m_last_source_line:
            l = max(1, self.m_last_source_line - (self.m_last_nlines - 1) / 2 - nlines)
            fLine = True
            
        try:
            if fEntire:
                r = [self.m_session_manager.get_source_file(_filename, -1, -1)]
            elif fLine:
                r = [self.m_session_manager.get_source_file(_filename, l, nlines)]
            elif _filename != '':
                r = [self.m_session_manager.get_source_file(_filename, l, nlines)]
            else:
                r = self.m_session_manager.get_source_lines(nlines, fAll)

            if len(r) == 0:
                print >> self.stdout, STR_NO_THREADS_FOUND
                return

            m = None    
            for d in r:
                tid = d.get(DICT_KEY_TID, 0)
                filename = d.get(DICT_KEY_FILENAME, '')
                breakpoints = d.get(DICT_KEY_BREAKPOINTS, {})
                source_lines = d.get(DICT_KEY_LINES, [])
                first_lineno = d.get(DICT_KEY_FIRST_LINENO, 0)
                
                fBroken = d.get(DICT_KEY_BROKEN, False)
                frame_event = d.get(DICT_KEY_EVENT, '')
                frame_lineno = d.get(DICT_KEY_FRAME_LINENO, 0)
                
                if m != None:
                    print >> self.stdout
                    
                print >> self.stdout, STR_SOURCE_LINES % (tid, filename)    
                for i, line in enumerate(source_lines):
                    lineno = first_lineno + i
                    if lineno != frame_lineno:
                        m = ''
                    elif not fBroken:
                        m = SOURCE_STATE_UNBROKEN + SYMBOL_MARKER
                    elif frame_event == 'call':
                        m = SOURCE_EVENT_CALL + SYMBOL_MARKER
                    elif frame_event == 'line':
                        m = SOURCE_EVENT_LINE + SYMBOL_MARKER
                    elif frame_event == 'return':
                        m = SOURCE_EVENT_RETURN + SYMBOL_MARKER
                    elif frame_event == 'exception':
                        m = SOURCE_EVENT_EXCEPTION + SYMBOL_MARKER

                    if breakpoints.get(lineno, None) == STATE_ENABLED:
                        b = SOURCE_BP_ENABLED
                    elif breakpoints.get(lineno, None) == STATE_DISABLED:
                        b = SOURCE_BP_DISABLED
                    else:
                        b = ''
                        
                    print >> self.stdout, ' %2s %1s %5d  %s' % (m, b, lineno, calc_prefix(line[:-1], 60))

            if fAll or fEntire:
                self.m_last_source_line = None        
            elif len(source_lines) != 0:
                self.m_last_source_line = [l + (nlines - 1) / 2, frame_lineno][l == -1]

            self.m_last_nlines = nlines
                
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except NoExceptionFound:
            print >> self.stdout, STR_EXCEPTION_NOT_FOUND
        except NoThreads:
            self.m_session_manager.report_exception(*sys.exc_info())
        except (InvalidFrame, IOError):
            print >> self.stdout, STR_SOURCE_NOT_FOUND

    do_l = do_list

    def do_up(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        try:
            fi = self.m_session_manager.get_frame_index()
            self.m_session_manager.set_frame_index(fi - 1)
            
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except DebuggerNotBroken:
            print >> self.stdout, STR_DEBUGGEE_NOT_BROKEN

    def do_down(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        try:
            fi = self.m_session_manager.get_frame_index()
            self.m_session_manager.set_frame_index(fi + 1)
            
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except DebuggerNotBroken:
            print >> self.stdout, STR_DEBUGGEE_NOT_BROKEN

    def do_eval(self, arg):
        if arg == '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        try:
            (value, warning, error) = self.m_session_manager.evaluate(arg)
            print >> self.stdout, warning + ['', '\n\n'][warning != ''] + error + value
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except NoExceptionFound:
            print >> self.stdout, STR_EXCEPTION_NOT_FOUND
        except DebuggerNotBroken:
            print >> self.stdout, STR_DEBUGGEE_NOT_BROKEN
        
    do_v = do_eval
    
    def do_exec(self, arg):
        if arg == '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return
            
        try:
            print >> self.stdout, STR_OUTPUT_WARNING
            (w, e) = self.m_session_manager.execute(arg)
            print >> self.stdout, w + e
        except (socket.error, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except NoExceptionFound:
            print >> self.stdout, STR_EXCEPTION_NOT_FOUND
        except DebuggerNotBroken:
            print >> self.stdout, STR_DEBUGGEE_NOT_BROKEN
        
    do_x = do_exec
    
    def do_thread(self, arg):
        if self.fAnalyzeMode and (arg != ''):
            print >> self.stdout, STR_ILEGAL_ANALYZE_MODE_ARG
            return

        try:
            if arg != '':
                tid = int(arg)
                self.m_session_manager.set_thread(tid)

                print >> self.stdout, STR_THREAD_FOCUS_SET
                return

            (current_thread_id, tl) = self.m_session_manager.get_thread_list()

            print >> self.stdout, STR_ACTIVE_THREADS    
            for i, t in enumerate(tl):
                m = ['', SYMBOL_MARKER][t[DICT_KEY_TID] == current_thread_id]
                state = [STATE_RUNNING, STATE_BROKEN][t[DICT_KEY_BROKEN]]
                print >> self.stdout, ' %1s %3d  %5d  %s' % (m, i, t[DICT_KEY_TID], state[:10])
                
        except ValueError:
            print >> self.stdout, STR_BAD_ARGUMENT
        except (socket.error, NoThreads, CConnectionException):
            self.m_session_manager.report_exception(*sys.exc_info())
        except ThreadNotFound:
            print >> self.stdout, STR_THREAD_NOT_FOUND
        except DebuggerNotBroken:
            print >> self.stdout, STR_DEBUGGEE_NOT_BROKEN

    do_t = do_thread

    def do_analyze(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        try:
            self.m_session_manager.set_analyze(not self.fAnalyzeMode)
        except NotAttached:
            print >> self.stdout, STR_NOT_ATTACHED        
        except DebuggerNotBroken:
            print >> self.stdout, STR_DEBUGGEE_NOT_BROKEN
        
    do_a = do_analyze
    
    def do_password(self, arg):
        if arg == '':
            pwd = self.m_session_manager.get_password()
            if pwd == None:
                print >> self.stdout, STR_PASSWORD_NOT_SET
            else:    
                print >> self.stdout, STR_PASSWORD_SET % (pwd, )
            return

        pwd = fix_password(arg)
        
        try:
            self.m_session_manager.set_password(pwd)
            print >> self.stdout, STR_PASSWORD_SET % (pwd, )
            return

        except AlreadyAttached:
            print >> self.stdout, STR_ALREADY_ATTACHED
            
    def do_remote(self, arg):
        if arg == '':
            fRemote = self.m_session_manager.get_remote()
            print >> self.stdout, STR_REMOTE_MODE % (str(fRemote), )
            return

        if arg == str(True):
            fRemote = True
        elif arg == str(False):
            fRemote = False
        else:
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        try:
            self.m_session_manager.set_remote(fRemote)
            print >> self.stdout, STR_REMOTE_MODE % (str(fRemote), )
            return

        except AlreadyAttached:
            print >> self.stdout, STR_ALREADY_ATTACHED

    def do_stop(self, arg):
        try:
            print >> self.stdout, STR_KILL_NOTICE
            self.m_session_manager.save_breakpoints()
            self.m_session_manager.stop_debuggee()
        except (socket.error, CConnectionException):
            pass
        
    def do_exit(self, arg):
        if arg != '':
            print >> self.stdout, STR_BAD_ARGUMENT
            return

        if self.m_session_manager.get_state() != STATE_DETACHED:    
            self.do_stop("")

        return True    

    def do_copyright(self, arg):
        self.print_notice(COPYRIGHT_NOTICE)

    def do_license(self, arg):
        self.print_notice(LICENSE_NOTICE + COPY_OF_THE_GPL_LICENSE)

    def do_help(self, arg):
        cmd.Cmd.do_help(self, arg)

        if arg == '':
            help_notice = """Security:
----------------

password    - Get or set the channel password.
remote      - Get or set "allow connections from remote machines" mode.

Session Control:
-----------------

host        - Display or change host.
attach      - Display scripts or attach to a script on host.
detach      - Detach from script.
launch      - Spawn a script and attach to it.
stop        - Shutdown the debugged script.
exit        - Exit from debugger.

Debuggee Control:
-----------------

break       - Request an immediate break.
step        - Continue to the next execution line.
next        - Continue to the next execution line in the current frame.
return      - Continue until the debugger is about to return from the frame.
jump        - Jump to a line in the current scope.
go          - Continue execution.

Breakpoints Control:
--------------------

bp          - Set a break point.
bd          - Disable a breakpoint.
be          - Enable a breakpoint.
bc          - Clear (delete) a breakpoint.
bl          - List all breakpoints.
load        - Load session breakpoints.
save        - save session breakpoints.

Misc:
-----

thread      - Display threads or switch to a particular thread.
list        - List source code.
stack       - Display stack trace.
up          - Go up one frame in stack.
down        - Go down one frame in stack.
eval        - Evaluate expression in the context of the current frame.
exec        - Execute suite in the context of the current frame.
analyze     - Toggle analyze last exception mode.

License:
----------------

copyright   - Print copyright notice.
license     - Print license."""

            self.print_notice(help_notice)
        
    def help_copyright(self, arg):
        print >> self.stdout, """copyright

Print copyright notice."""  

    def help_license(self, arg):
        print >> self.stdout, """license

Print license."""  

    def help_help(self):
        print >> self.stdout, """help <cmd>

Print help for command <cmd>.
On the other hand I guess that you already know that, don't you?"""  

    def help_analyze(self):
        print >> self.stdout, """analyze

(shorthand - a)

Toggle analyze last exception mode.

The following changes to the debugger behavior apply in analyze mode:
The debugger prompt changes to 'Analyze>'.
'go', 'step', 'next', and 'return' are not allowed.
'thread' does not allow to change the thread focus.
'stack' allows no arguments.
'list' does not accept the '*' (all threads) argument
'stack', 'list', 'eval', 'exec', 'up', and 'down' operate on the thrown 
exception."""

    help_a = help_analyze    

    def help_password(self):
        print >> self.stdout, """password <password>

Get or set the channel password.

Communication between the console and the debuggee is always authenticated and
optionally encrypted. The password (A secret known to the console and the
debuggee alone) governs both security methods. The password is never 
communicated between the two components on the communication channel.

A password is always required since unsecured communication between the 
console and the debuggee may expose your machine to attacks."""

    def help_remote(self):
        print >> self.stdout, """remote [True | False]

Get or set "allow connections from remote machines" mode.

When set to False: 
Newly launched debuggees will listen on localhost only. In this mode, debugger
consoles on remote machines will NOT BE able to see or attach to the debuggee.

When set to True: 
Newly launched debuggees will listen on INADDR_ANY. In this mode, debugger 
consoles on remote machines will BE able to see and attach to the debuggee."""

    def help_stop(self):
        print >> self.stdout, """Stop

Shutdown the debugged script."""

    def help_launch(self):
        print >> self.stdout, """Launch <script_name> [<script_args>]

Spawn script <script_name> and attach to it."""

    def help_attach(self):
        print >> self.stdout, """attach [<arg>]

Without an argument, 'attach' prints the scripts available for debugging
on the selected host. To select a host use the 'host' command. A script is
considered available for debugging only if it is using the rpdb2 module or
has been executed by the debugger.
If the debugger is already attached to a script, a special character will
mark that script in the list.

When <arg> is an integer the debugger will try to attach to a script with
that pid. 
When <arg> is a string the debugger will try to attach to a script
with that name in the list."""  

    def help_detach(self):
        print >> self.stdout, """detach

Detach from the script the debugger is currently attached to. The detached
script will continue execution."""  

    def help_break(self):
        print >> self.stdout, """break 

(shorthand - b)

Request script to break. The 'break' command returns immdeiately but the 
break is only established when an active thread submits to the debugger 
control. If a thread is doing a system call or executing C code, this 
will happen only when it returns to do python code."""  

    help_b = help_break
    
    def help_bp(self):
        print >> self.stdout, """bp [<filename>':'] (<line> | <scope>) [',' <expr>]

Set a breakpoint.

<filename> - either the filename or the module name. 
<line>     - is the line number to assign the breakpoint to.
<scope>    - is a "fully qualified" function name. That is, not only the 
             function name but also the class name (in case of a member 
             function), such as MyClass.MyMemberFunction.
<expr>     - condition to evaluate in the context of the frame. If it
             evaluates to 'True' the break point will break into the debugger.

In case the <filemame> is omitted, the current file is assumed. In this case 
the debuggee has to be broken.

Examples:

    bp test_file.py:20
    bp test_file.py:MyClass.Foo
    bp 304

Type 'help break' for more information on 'broken' and non 'broken' threads."""

    def help_be(self):
        print >> self.stdout, """be (<id_list> | '*')
        
Enable breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - Enable all breakpoints."""

    def help_bd(self):
        print >> self.stdout, """bd (<id_list> | '*')
        
Disable breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - disable all breakpoints."""

    def help_bc(self):
        print >> self.stdout, """bc (<id_list> | '*')
        
Clear (delete) breakpoints.

<id_list> - is a space delimited list of at least one breakpoint id
'*' - clear all breakpoints."""

    def help_bl(self):
        print >> self.stdout, """bl

List all breakpoints, sorted by their id."""

    def help_load(self):
        print >> self.stdout, """load [<filename>]
        
Load breakpoints.

<filename> - optional breakpoints filename. The filename should not include
             a file extension."""

    def help_save(self):
        print >> self.stdout, """save [<filename>]
        
save breakpoints.

<filename> - optional breakpoints filename. The filename should not include
             a file extension."""

    def help_go(self):
        print >> self.stdout, """go [[<filename>':'] (<line> | <scope>)]

(shorthand - g)

Resume execution of a "broken" script. 
If an argument is present, continue execution until that argument is reached.

<filename> - is the file name which basically is the script's name without
             the '.py' extension. 
<line>   - is the line number to assign the breakpoint to.
<scope>  - is a "fully qualified" function name. That is, not only the 
           function name but also the class name (in case of a member 
           function), such as MyClass.MyMemberFunction."""

    help_g = help_go
    
    def help_exit(self):
        print >> self.stdout, """exit

Exit the debugger. If the debugger is attached to a script, the debugger
will attempt to detach from the script first."""  
    
    def help_host(self):
        print >> self.stdout, """host [<arg>]

Without an argument, 'host' prints the current selected host.
With an argument <arg>, 'host' attempts to resolve <arg> to a known ip 
address or a domain name. If it is successful, that host will become the
selected host. 
The default selected host is the local host.
Subsequent 'attach' commands will be done on the selected host. 

Type 'help attach' for more information."""  

    def help_stack(self):
        print >> self.stdout, """stack [<tid> | '*']

(shorthand - k)

Without an argument, 'stack' prints the stack trace of the focused thread.
If the thread is 'broken' a special character will mark the focused frame.

<tid> - print the stack of thread <tid> 
'*'   - print the stacks of all active threads.

Type 'help break' for more information on 'broken' and un-'broken' threads.
Type 'help up' or 'help down' for more information on focused frames."""  

    help_k = help_stack
    
    def help_list(self):
        print >> self.stdout, """list [<file_name>:][<line_no> | '+' | '-' | '^' | '*'] [',' <nlines>]

(shorthand - l)

Without an argument, 'list' prints the source lines around the current line
of the focused thread in the focused frame. A special character sequence will 
mark the current line according to the event:

    'C>' - call - A function is called.
    'L>' - line - The interpreter is about to execute a new line of code.
    'R>' - return - A function is about to return.
    'E>' - exception - An exception has been thrown.
    '*>' - unbroken - The thread is running.

If a breakpoint is assigned to a line, that line will be marked with:

    'B' - if the breakpoint is enabled
    'D' - if the breakpoint is disabled

<file_name> - List source from filename    
<line_no>   - Print the source lines around that line number in the same file 
              of the current line.
'+'         - Print the next lines in the file.
'-'         - Print the previous lines in the file.
'^'         - Print the entire file.
'*'         - Print the source lines for each of the active threads.
<nlines>    - Print <nlines> of source

Type 'help break' for more information on 'broken' and un-'broken' threads.
Type 'help up' or 'help down' for more information on focused frames."""  

    help_l = help_list
    
    def help_thread(self):
        print >> self.stdout, """thread [<no> | <tid>]

(shorthand - t)

Without an argument, 'thread' prints the list of known active threads, with
their corresponding state, which can be either 'broken' or 'running'.
A special character will mark the focused thread.

With an argument <tid>, 'thread' will attempt to set the debugger focus to
the thread of that tid.
With an argument <no>, 'thread' will attempt to set the debugger focus to 
the thread of that order in the thread list.

Type 'help break' for more information on 'broken' and non 'broken' threads."""

    help_t = help_thread

    def help_jump(self):
        print >> self.stdout, """jump <lineno>

(shorthand - j)

Jump to line <lineno> in the current scope."""

    help_j = help_jump
    
    def help_next(self):
        print >> self.stdout, """next

(shorthand - n)

Continue execution until the next line in the current function
is reached or it returns."""

    help_n = help_next
    
    def help_step(self):
        print >> self.stdout, """next

(shorthand - s)

Execute the current line, stop at the first possible occasion
(either in a function that is called or in the current function)."""

    help_s = help_step    

    def help_return(self):
        print >> self.stdout, """next

(shorthand - r)

Continue execution until the current function returns."""

    help_r = help_return    

    def help_up(self):
        print >> self.stdout, """up

move the debugger focus one frame up the stack of the debugged thread 
(closer to the current, most recently executed frame). Evaluation of 
expressions or execution of statements will be done at the local and global 
name spaces of the focused frame.

Type 'help eval' for more information on evaluation of expressions.
Type 'help exec' for more information on execution of statements."""

    def help_down(self):
        print >> self.stdout, """down

move the debugger focus one frame down the stack of the debugged thread 
(closer to the current, most recently executed frame). Evaluation of 
expressions or execution of statements will be done at the local and global 
name spaces of the focused frame.

Type 'help eval' for more information on evaluation of expressions.
Type 'help exec' for more information on execution of statements."""

    def help_eval(self):
        print >> self.stdout, """eval <expr>

(shorthand - v)

Evaluate the python expression <expr> under the global and local name spaces
of the currently focused frame.

Example:
'eval locals()' - will display the dictionary of the local variables.

IMPORTANT: Any changes to the global name space will be discarded unless the
focused stack frame is the top most frame.

Type 'help up' or 'help down' for more information on focused frames."""  

    help_v = help_eval

    def help_exec(self):
        print >> self.stdout, """exec <stmt>

(shorthand - x)

Execute the python suite <stmt> under the global and local name spaces
of the currently focused frame.

Example:
'exec i += 1'

IMPORTANT: Any changes to the global name space will be discarded unless the
focused stack frame is the top most frame.

Type 'help up' or 'help down' for more information on focused frames."""  

    help_x = help_exec

    

#
# ---------------------------------------- main ------------------------------------
#



def __settrace():
    f = sys._getframe(2)
    g_debugger.settrace(f, f_break_on_init = False)

    

def __start_embedded_debugger(pwd, fAllowUnencrypted, fRemote, timeout, fDebug):
    global g_server
    global g_debugger
    global g_fDebug

    try:
        g_server_lock.acquire()
        
        if g_server != None:
            return

        g_fDebug = fDebug
        
        xmlrpclib.loads(XML_DATA)    

        if (not fAllowUnencrypted) and not is_encryption_supported():
            raise EncryptionNotSupported
        
        f = sys._getframe(2)
        filename = my_abspath(f.f_code.co_filename)
        
        g_debugger = CDebuggerEngine()

        g_server = CDebuggeeServer(filename, g_debugger, pwd, fAllowUnencrypted, fRemote)
        g_server.start()

        g_debugger.settrace(f, timeout = timeout)

    finally:
        g_server_lock.release()


    
def StartServer(args, pwd, fAllowUnencrypted, fRemote, rid): 
    global g_server
    global g_debugger
    global g_main_module_name
    global g_main_global_dictionay
    
    try:
        ExpandedFilename = FindFile(args[0])
    except IOError:
        print 'File', args[0], ' not found.'
       
    #
    # Insert script directory in front of file search path
    #
    sys.path.insert(0, os.path.dirname(ExpandedFilename))
    sys.argv = args

    d = {}
    d['__builtins__'] = __main__.__dict__['__builtins__']
    d['__name__'] = '__main__'
    d['__file__'] = ExpandedFilename
    d['__doc__'] = None

    g_main_module_name = CalcModuleName(ExpandedFilename)
    g_main_global_dictionay = d
    
    g_debugger = CDebuggerEngine()

    g_server = CDebuggeeServer(ExpandedFilename, g_debugger, pwd, fAllowUnencrypted, fRemote, rid)
    g_server.start()

    g_debugger.settrace()

    execfile(ExpandedFilename, d, d)
    
    g_debugger.stoptrace()
    #g_server.stop()
    


def StartClient(command_line, fAttach, pwd, fAllowUnencrypted, fRemote, host):
    if (not fAllowUnencrypted) and not is_encryption_supported():
        print STR_ENCRYPTION_SUPPORT_ERROR
        return 2
        
    sm = CSessionManager(pwd, fAllowUnencrypted, fRemote, host)
    c = CConsole(sm)
    c.start()

    if fAttach:
        sm.attach_nothrow(command_line)
    elif command_line != '':
        sm.launch_nothrow(command_line)
        
    c.join()



def PrintUsage(fExtended = False):
    scriptName = os.path.basename(sys.argv[0])
    print """ %(rpdb)s [options] [<script-name> [<script-args>...]]

    Where the options can be a combination of the following:
    -h, --help      print this help.
    -d, --debugee   start debugee and break into it, without starting a 
                    debugger console. 
    -a, --attach    Attach to an already started debuggee.
    -o, --host      Specify host for attachment.
    -r, --remote    Allow debuggees to accept connections from remote machines.
    -t, --plaintext Allow unencrypted connections between debugger and 
                    debuggees.
    -p, --pwd       Password.
    -s, --screen    Use the Unix screen utility when spawning the debuggee.
    --debug         Debug prints.
""" % {"rpdb": scriptName}
    
    if not fExtended:
        return
        
    print __doc__



def main(StartClient_func = StartClient):
    global g_fScreen
    global g_fDebug
    
    try:
        options, args = getopt.getopt(
                            sys.argv[1:], 
                            'hdao:rtp:s', 
                            ['help', 'debugee', 'attach', 'host=', 'remote', 'plaintext', 'pwd=', 'rid=', 'screen', 'debug']
                            )

    except getopt.GetoptError, e:
        print e
        return 2
        
    fWrap = False
    fAttach = False
    fSpawn = False
    fStart = False
    
    secret = None
    host = None
    pwd = None
    fRemote = False
    fAllowUnencrypted = False
    
    for o, a in options:
        if o in ['-h', '--help']:
            PrintUsage()
            return 0
        if o in ['--debug']:
            g_fDebug = True 
        if o in ['-d', '--debugee']:
            fWrap = True
        if o in ['-a', '--attach']:
            fAttach = True
        if o in ['-o', '--host']:
            host = a
        if o in ['-r', '--remote']:
            fRemote = True
        if o in ['-t', '--plaintext']:
            fAllowUnencrypted = True
        if o in ['-p', '--pwd']:
            pwd = a
        if o in ['--rid']:
            secret = a
        if o in ['-s', '--screen']:
            g_fScreen = True

    if fWrap and (len(args) == 0):
        print "--debuggee option requires a script name with optional <script-arg> arguments"
        return 2
        
    if fWrap and fAttach:
        print "--debuggee and --attach can not be used together."
        return 2
        
    if fAttach and (len(args) == 0):
        print "--attach option requires a script name to attach to."
        return 2
        
    if fAttach and (len(args) > 1):
        print "--attach option does not accept <script-arg> arguments."
        return 2

    if fAttach and fRemote:
        print "--attach and --remote can not be used together."
        return 2
        
    if (host != None) and not fAttach:
        print "--host can only be used together with --attach."
        return 2

    if host == None:
        host = LOCAL_HOST    

    fSpawn = (len(args) != 0) and (not fWrap) and (not fAttach)
    fStart = (len(args) == 0)
    
    assert (fWrap + fAttach + fSpawn + fStart) == 1

    if (pwd in [None, ""]) and (fWrap or fAttach):
        print STR_PASSWORD_MUST_BE_SET
        return 2

    if fWrap or fSpawn:
        #
        # Prevent rpdb from trying to debug itself, so it doesn't blow up :)
        #
        if os.path.basename(args[0]) in [DEBUGGER_FILENAME]:
            print 'Cannot debug self.'
            return 2

        try:
            FindFile(args[0])
        except IOError:
            print STR_FILE_NOT_FOUND, (args[0], )
            return 2
            
    if fWrap:
        if (not fAllowUnencrypted) and not is_encryption_supported():
            print STR_ENCRYPTION_SUPPORT_ERROR
            return 2

        StartServer(args, pwd, fAllowUnencrypted, fRemote, secret)
        
    elif fAttach:
        StartClient_func(args[0], fAttach, pwd, fAllowUnencrypted, fRemote, host)
        
    elif fStart:
        StartClient_func('', fAttach, pwd, fAllowUnencrypted, fRemote, host)
        
    else: 
        StartClient_func(string.join(args), fAttach, pwd, fAllowUnencrypted, fRemote, host)
   
    return 0



# When invoked as main program, invoke the debugger on a script
if __name__=='__main__':
    import rpdb2

    ret = rpdb2.main()
    sys.exit(ret)


    

