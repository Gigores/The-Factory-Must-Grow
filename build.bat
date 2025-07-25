# just a small script i used to automatically compile the game

@echo off
chcp 65001
set /p ver="input game version: "
pyinstaller --icon=icon.ico --add-data "scripts;scripts" main.py
echo %ver%
del main.spec
rd build
mkdir "D:\TheFactoryMustGrowExecutables\%ver%"
mkdir "D:\TheFactoryMustGrowExecutables\%ver%\scripts"
copy %cd%\dist\main\main.exe "D:\TheFactoryMustGrowExecutables\%ver%\TheFactoryMustGrow.exe"
xcopy %cd%\dist\main\_internal "D:\TheFactoryMustGrowExecutables\%ver%\_internal" /e /I
xcopy %cd%\assets "D:\TheFactoryMustGrowExecutables\%ver%\assets" /e /Y /I
xcopy %cd%\sound "D:\TheFactoryMustGrowExecutables\%ver%\sound" /e /Y /I
xcopy %cd%\addons "D:\TheFactoryMustGrowExecutables\%ver%\addons" /e /Y /I
xcopy %cd%\scripts\Entities "D:\TheFactoryMustGrowExecutables\%ver%\scripts\Entities" /e /Y /I
xcopy %cd%\scripts\UI "D:\TheFactoryMustGrowExecutables\%ver%\scripts\UI" /e /Y /I
xcopy %cd%\scripts\Managers "D:\TheFactoryMustGrowExecutables\%ver%\scripts\Managers" /e /Y /I
rmdir /s /q build
rmdir /s /q dist
echo Built Successful
pause