cd /d %~dp0

@echo off

chcp 65001

@REM %1表示处理文件

python.exe Complete.py %1

pause