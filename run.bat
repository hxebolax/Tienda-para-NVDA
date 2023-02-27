@cls
@echo off
echo Creando complemento...
scons --clean
scons
scons pot
TiendaNVDA-0.9.1.nvda-addon