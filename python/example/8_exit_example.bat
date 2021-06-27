@echo off

REM result
REM ******** 0 **********
REM Hello
REM ******** 1 **********
REM 99
REM ******** 2 **********
REM Hello

echo ******** 0 **********
call 8_exit_test.bat
echo ******** 1 **********
echo %ERRORLEVEL%
echo ******** 2 **********
8_exit_test.bat
echo ******** 3 **********
echo %ERRORLEVEL%
echo ******** 4 **********
