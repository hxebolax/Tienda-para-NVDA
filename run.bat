@cls
@echo off
echo Creando complemento...
scons --clean
scons
scons pot
TiendaNVDA-0.10.nvda-addon