@echo off
setlocal

echo (1/2) building index.html...
python %~dp0builder.py -i %~dp0log.md -o %~dp0index.html -t %~dp0template.html
echo fin.

echo (2/2) building log_pretty.html...
python %~dp0log_indenter.py -i %~dp0log.md -o %~dp0log_pretty.md
echo fin.

echo uploading...
rem upload.bat is my original batchfile to do add, commit and push at one time.
rem see: https://github.com/stakiran/gaas_for_windows/blob/master/upload.bat
upload
echo fin.
