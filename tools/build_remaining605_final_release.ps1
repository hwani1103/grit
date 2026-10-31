$ErrorActionPreference = 'Stop'
$finalRoot = Join-Path $PSScriptRoot '../artifacts/psat_remaining605_20261030/final'
$checks = Get-Content (Join-Path $finalRoot 'test-closure.json') -Raw | ConvertFrom-Json
if ($checks.status -ne 'PASS') { throw 'Final regression is not closed.' }
$preserved = Get-Content (Join-Path $finalRoot 'preservation-check.json') -Raw | ConvertFrom-Json
if ($preserved.status -ne 'PASS') { throw 'Final preservation is not verified.' }
if (-not (Select-String -LiteralPath (Join-Path $finalRoot 'analyze.log') -SimpleMatch 'No issues found')) { throw 'Static analysis not passed.' }
$releasePath = Join-Path $PSScriptRoot '../releases/GRIT-1.3.1-5001-PSAT900-reviewed605-arm64.apk'
if (Test-Path -LiteralPath $releasePath) { throw 'Do not overwrite an existing release.' }
$env:FLUTTER_ALREADY_LOCKED = 'true'
$env:FLUTTER_ROOT = 'C:/tools/flutter'
$env:CI = 'true'
& C:/tools/flutter/bin/cache/dart-sdk/bin/dart.exe C:/tools/flutter/bin/cache/flutter_tools.snapshot --no-version-check --suppress-analytics build apk --release --no-pub --target-platform android-arm64 --build-name=1.3.1 --build-number=5001 *> (Join-Path $finalRoot 'release-build.log')
if ($LASTEXITCODE -ne 0) { throw "Release build failed: $LASTEXITCODE" }
Copy-Item -LiteralPath (Join-Path $PSScriptRoot '../build/app/outputs/flutter-apk/app-release.apk') -Destination $releasePath
Write-Output 'Final release APK saved; awaiting signature and package verification.'
