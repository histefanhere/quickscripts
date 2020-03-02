#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
; This is done to set the working dir of the script to the main git directory.
SetWorkingDir ..

; Alt + q
!q::
    Run C:\Users\stefa\AppData\Local\Programs\Python\Python38\pythonw main.py
	Return