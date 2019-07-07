@echo off
setlocal

python %~dp0builder.py -i %~dp0log.md -o %~dp0index.html -t %~dp0template.html

timeout 3