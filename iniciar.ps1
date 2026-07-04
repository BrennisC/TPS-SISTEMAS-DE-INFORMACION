Write-Host "===================================================" -ForegroundColor Green
Write-Host "    SISTEMA DE ADMISIÓN UNAS - INICIO RÁPIDO" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""

# 1. Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python detectado: $pythonVersion" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Python no está instalado o no está en el PATH." -ForegroundColor Red
    Write-Host "Por favor instala Python 3.8+ y agrégalo al PATH." -ForegroundColor Yellow
    exit
}

# 2. Verificar Node.js
try {
    $nodeVersion = node -v 2>&1
    Write-Host "[OK] Node.js detectado: $nodeVersion" -ForegroundColor Gray
} catch {
    Write-Host "[ERROR] Node.js no está instalado. Reflex lo necesita para compilar el frontend." -ForegroundColor Red
    Write-Host "Descárgalo e instálalo desde https://nodejs.org/" -ForegroundColor Yellow
    exit
}

# 3. Crear entorno virtual
if (!(Test-Path -Path ".venv")) {
    Write-Host "[INFO] Creando entorno virtual (.venv)..." -ForegroundColor Cyan
    python -m venv .venv
} else {
    Write-Host "[INFO] Entorno virtual existente detectado." -ForegroundColor Gray
}

# 4. Activar entorno virtual
Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Cyan
. .venv\Scripts\Activate.ps1

# 5. Instalar dependencias
Write-Host "[INFO] Actualizando pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

Write-Host "[INFO] Instalando dependencias desde requirements.txt..." -ForegroundColor Cyan
pip install -r requirements.txt

# 6. Iniciar app
Write-Host ""
Write-Host "===================================================" -ForegroundColor Green
Write-Host "[LISTO] Iniciando aplicación con Reflex..." -ForegroundColor Green
Write-Host "Accede en tu navegador a: http://localhost:3000" -ForegroundColor Green
Write-Host "Credenciales predeterminadas:" -ForegroundColor Yellow
Write-Host "  - Usuario: admin" -ForegroundColor Yellow
Write-Host "  - Contraseña: admin123" -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Green
Write-Host ""

reflex run
