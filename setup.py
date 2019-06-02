import os
import pygame
from cx_Freeze import *
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

shortcut_table = [
    ("DesktopShortcut",                # Shortcut
     "DesktopFolder",                  # Directory_
     "Game Name",                   # Name
     "TARGETDIR",                      # Component_
     "[TARGETDIR]MainController.exe",  # Target
     None,                             # Arguments
     "Game Description",               # Description
     None,                             # Hotkey
     "game.ico",                      # Icon
     None,                             # IconIndex
     None,                             # ShowCmd
     'TARGETDIR'                       # WkDir
     ),
                  
    ("StartupShortcut",                # Shortcut
     "StartupFolder",                  # Directory_
     "Game Name",                   # Name
     "TARGETDIR",                      # Component_
     "[TARGETDIR]MainController.exe",  # Target
     None,                             # Arguments
     "Game Description",               # Description
     None,                             # Hotkey
     "game.ico",                      # Icon
     None,                             # IconIndex
     None,                             # ShowCmd
     'TARGETDIR'                       # WkDir
     ),
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

execs = [
    Executable(
        "MainController.py",
    )
]

include_files = [("Images", "Images"), ("Sounds", "Sounds"), ("Objects", "Objects"), ("Rooms", "Rooms")]

setup(
    name = "Game Name",
    version = "1.0",
    description = "Game Description",
    options=
    {
        "build_exe": 
        {
            "packages":["pygame"],
            "include_files":include_files,
            "include_msvcr": True
        },
        "bdist_msi": bdist_msi_options
    },    
    executables=execs
)
