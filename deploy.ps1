# Local deployment helper for Student Attention Monitoring System
# Run from PowerShell: .\deploy.ps1

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $repoRoot

$pythonCmd = Get-Command py -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
}

if (-not $pythonCmd) {
    Write-Error "Python is not installed or not available on PATH. Install Python 3.8+ and retry."
    exit 1
}

$pythonExe = $pythonCmd.Source
Write-Host "Using Python: $pythonExe"

if (-not (Test-Path "$repoRoot\venv")) {
    Write-Host "Creating virtual environment..."
    & $pythonExe -m venv "$repoRoot\venv"
}

$venvPython = "$repoRoot\venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Error "Virtual environment Python not found at $venvPython"
    exit 1
}

Write-Host "Installing dependencies..."
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r "$repoRoot\requirements.txt"

Write-Host "Starting Student Attention Monitoring System..."
& $venvPython "$repoRoot\main.py"
