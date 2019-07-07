@echo off
setlocal

echo building...
python %~dp0builder.py -i %~dp0log.md -o %~dp0index.html -t %~dp0template.html
echo fin.

echo uploading...
rem upload.bat is my original batchfile to do add, commit and push at one time.
upload
echo fin.
