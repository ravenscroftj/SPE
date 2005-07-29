import spit
import os

NAME    = "Stani's Python Editor"
LOGO    = "skins/install.jpg"
LICENSE = "spit/gpl.txt"

####SHORTCUTS
CONTRIBUTE_SHORTCUT = spit.Shortcut(
        name    = "Contribute",
        target  = 'doc/contribute.html',)

DONATE_SHORTCUT = spit.Shortcut(
        name    = "Donate",
        target  = 'doc/donate.html',)

MANUAL_SHORTCUT = spit.Shortcut(
        name    = "Donate",
        target  = 'doc/donate.html',)

SPE_SHORTCUT    = spit.Shortcut(
        name    = "Stani's Python Editor",
        target  = 'SPE.py',
        icon    = 'skins/default/favicon.ico')

####PACKAGES
#required
REQUIRED = [spit.Package(name   = 'spe',
                module          = '_spe',
                description     = """Stani's Python Editor""",
                url             = 'http://www.stani.be',
                license         = 'GPL',
                desktop         = [SPE_SHORTCUT],
                programs        = [SPE_SHORTCUT,
                                    DONATE_SHORTCUT,
                                    MANUAL_SHORTCUT,
                                    CONTRIBUTE_SHORTCUT]),
            spit.Package(name = 'sm',
                module            = 'sm',
                description     = """Stani's Python Library""",
                url             = 'http://www.stani.be',
                license         = 'GPL')
            ]
            
#optional
OPTIONAL = [spit.Package(name   = 'kiki',
                module          = 'kiki',
                description     = """Regular expression tester""",
                url             = 'http://come.to/project5',
                license         = 'GPL'),
            spit.Package(name   = 'pyChecker',
                module            = 'pychecker',
                description     = """Python source code checking tool""",
                url             = 'http://pychecker.sourceforge.net',
                license         = 'GPL'),
            spit.Package(name = 'wxGlade',
                module          = 'wxglade',
                description     = """Graphical User Interface Designer""",
                url             = 'http://wxglade.sourceforge.net',
                license         = 'MIT')
            ]

if __name__ == '__main__':
    spit.wizard(name=NAME,required=REQUIRED,optional=OPTIONAL,logo=LOGO,license=LICENSE)

