@echo off
chcp 65001 >nul
cls
title Tienda para NVDA - Publicar en GitHub
echo ============================================================
echo   Tienda para NVDA - Script de publicacion en GitHub
echo ============================================================
echo.
set REPO_URL=https://github.com/hxebolax/Tienda-para-NVDA.git
set BRANCH=master
set VERSION=2026.05.11
echo  Version: %VERSION%
echo  Repositorio: %REPO_URL%
echo  Rama: %BRANCH%
echo.
echo  Que deseas hacer?
echo.
echo  [1] Subida completa (limpiar, commit, push y crear tag/release)
echo  [2] Solo commit y push (sin tag)
echo  [3] Solo crear tag y push del tag
echo  [4] Inicializar repositorio (primera vez)
echo  [5] Compilar complemento localmente (scons)
echo  [6] Salir
echo.
set /p OPCION="  Elige una opcion (1-6): "
if "%OPCION%"=="1" goto FULL
if "%OPCION%"=="2" goto PUSH_ONLY
if "%OPCION%"=="3" goto TAG_ONLY
if "%OPCION%"=="4" goto INIT
if "%OPCION%"=="5" goto BUILD
if "%OPCION%"=="6" goto END
echo  Opcion no valida.
goto END
:INIT
echo.
echo --- Inicializando repositorio ---
if exist ".git" (
echo  Ya existe un repositorio git en este directorio.
echo  Si deseas reinicializarlo, elimina la carpeta .git manualmente.
goto END
)
git init
git remote add origin %REPO_URL%
git branch -M %BRANCH%
echo.
echo  Repositorio inicializado correctamente.
echo  Ahora puedes usar la opcion [1] para subir el codigo.
goto END
:FULL
echo.
echo --- Limpiando artefactos de compilacion ---
if exist ".sconsign.dblite" del /q ".sconsign.dblite"
for %%F in (*.nvda-addon) do del /q "%%F"
for %%F in (*.pot) do del /q "%%F"
echo.
set /p MSG="  Mensaje del commit (Enter para usar 'Version %VERSION%'): "
if "%MSG%"=="" set MSG=Version %VERSION%
echo.
echo --- Agregando cambios ---
git add --all
echo --- Creando commit ---
git commit -m "%MSG%"
echo --- Subiendo a %BRANCH% ---
git push -u origin %BRANCH%
echo --- Creando tag %VERSION% ---
git tag %VERSION%
echo --- Subiendo tags ---
git push --tags
echo.
echo  Publicacion completa! El workflow de GitHub Actions generara
echo  el complemento .nvda-addon automaticamente y creara el release.
goto END
:PUSH_ONLY
echo.
set /p MSG="  Mensaje del commit (Enter para usar 'Actualizacion'): "
if "%MSG%"=="" set MSG=Actualizacion
echo.
echo --- Agregando cambios ---
git add --all
echo --- Creando commit ---
git commit -m "%MSG%"
echo --- Subiendo a %BRANCH% ---
git push -u origin %BRANCH%
echo.
echo  Push completado. No se ha creado tag ni release.
goto END
:TAG_ONLY
echo.
echo --- Creando tag %VERSION% ---
git tag %VERSION%
echo --- Subiendo tags ---
git push --tags
echo.
echo  Tag %VERSION% creado y subido.
echo  El workflow de GitHub creara el release automaticamente.
goto END
:BUILD
echo.
echo --- Compilando complemento localmente ---
scons --clean
echo.
scons
echo.
scons pot
echo.
echo  Compilacion completada.
for %%F in (*.nvda-addon) do echo  Archivo generado: %%F
goto END
:END
echo.
echo ============================================================
echo  Proceso finalizado.
echo ============================================================
pause
