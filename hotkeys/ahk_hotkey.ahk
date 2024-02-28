; Recommended for performance and compatibility with future AutoHotkey releases.
#NoEnv

; This is done to set the working dir of the script to the main git directory.
SetWorkingDir ..

Menu Tray, Icon, hotkeys\icon.ico
Menu Tray, Tip, Quickscripts Hotkey

; Alt + q - Start the program
; !q::
F9::
    Run pythonw main.py
	Return
