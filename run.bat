@cls
@echo off
echo Creando complemento...
scons --clean
scons
scons pot
TiendaNVDA-0.9.3.nvda-addon