@echo off

echo ===================================================
echo     SISTEMA DE ADMISIÓN UNAS - INICIO RÁPIDO
echo ===================================================
echo.

:: 1. Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 goto :no_python

:: 2. Verificar si Node.js está instalado (Requerido por Reflex)
node -v >nul 2>&1
if %errorlevel% neq 0 goto :no_node

:: 3. Crear entorno virtual si no existe
if exist .venv goto :venv_active
echo [INFO] Creando entorno virtual de Python (.venv)...
python -m venv .venv
if %errorlevel% neq 0 goto :err_venv

:venv_active
echo [INFO] Entorno virtual existente o creado con éxito.

:: 4. Activar entorno virtual
echo [INFO] Activando entorno virtual (.venv)...
call .venv\Scripts\activate.bat

:: 5. Actualizar pip e instalar dependencias
echo [INFO] Actualizando pip...
python -m pip install --upgrade pip

echo [INFO] Instalando dependencias de requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 goto :err_deps

:: 6. Ejecutar el proyecto
echo.
echo ===================================================
echo [LISTO] Iniciando aplicación con Reflex...
echo Para acceder, abre tu navegador en: http://localhost:3000
echo Credenciales de administrador predeterminadas:
echo   - Usuario: admin
echo   - Contraseña: admin123
echo ===================================================
echo.

reflex run
goto :end

:no_python
echo [ERROR] Python no está instalado o no está agregado al PATH de Windows.
echo Por favor, instala Python 3.8+ y asegúrate de marcar la casilla "Add Python to PATH" durante la instalación.
pause
exit /b 1

:no_node
echo [ERROR] Node.js no está instalado.
echo Reflex requiere Node.js para compilar el frontend. Por favor descárgalo de https://nodejs.org/
pause
exit /b 1

:err_venv
echo [ERROR] No se pudo crear el entorno virtual (.venv).
pause
exit /b 1

:err_deps
echo [ERROR] Hubo un error al instalar las dependencias de requirements.txt.
pause
exit /b 1

:end

pause
