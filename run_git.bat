@cls
@echo off
scons --clean
git init
git add --all
git commit -m "Versión 0.9.3"
git push -u origin master
git tag 0.9.3
git push --tags
pause