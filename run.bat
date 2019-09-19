@ECHO OFF
CALL T:\bat\environment.bat 
"C:\Program Files\Shotgun\Python\pythonw.exe" %~dp0\wrangling_helper\model.py
pause