$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$finalRoot = Join-Path $root 'artifacts/psat_remaining605_20261030/final'
$apkPath = Join-Path $root 'releases/GRIT-1.3.1-5001-PSAT900-reviewed605-arm64.apk'
$buildTools = 'C:/Users/Administrator/AppData/Local/Android/Sdk/build-tools/35.0.0'
& (Join-Path $buildTools 'apksigner.bat') verify --verbose --print-certs $apkPath *> (Join-Path $finalRoot 'release-certificate.txt')
if ($LASTEXITCODE -ne 0) { throw 'APK signature verification failed.' }
& (Join-Path $buildTools 'aapt.exe') dump badging $apkPath *> (Join-Path $finalRoot 'release-badging.txt')
if ($LASTEXITCODE -ne 0) { throw 'APK package metadata inspection failed.' }
$env:PYTHONIOENCODING = 'utf-8'
& C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe (Join-Path $PSScriptRoot 'verify_remaining605_release.py')
exit $LASTEXITCODE
