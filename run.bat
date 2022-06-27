@cls
@echo off
echo Creando complemento...
scons --clean
scons
scons pot
TiendaNVDA-0.8.4.nvda-addon