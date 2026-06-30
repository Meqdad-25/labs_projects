@echo off
cd /d "%~dp0"
call ga_dsb_env/Scripts/activate
jupyter lab
pause


REM below is just a remark and will never be executed. it is like a comment
REM to check for which environment you are using, run the below two codes from within python (without REM):
REM import sys
REM print(sys.executable)