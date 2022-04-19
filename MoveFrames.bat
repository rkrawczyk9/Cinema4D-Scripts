@ECHO OFF
SETLOCAL
SET "sourcedir=D:\Titus BigData\Renders\test"
SET "destdir=D:\Titus BigData\Renders\test"

FOR /f "tokens=1,2,*delims=." %%a IN ('dir /b /a-d "%sourcedir%\*.*" ') DO (
 MD "%destdir%\%%a" 2>nul
 MOVE "%sourcedir%\%%a.%%b.%%c" "%destdir%\%%a\%%a.%%b.%%c" >nul
)

GOTO :EOF