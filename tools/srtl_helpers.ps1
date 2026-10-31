# Only the SRTL device authorized on 2026-10-28. Verify adb devices before reuse.
$GritAdb = 'C:\Users\Administrator\AppData\Local\Android\Sdk\platform-tools\adb.exe'
$GritSerial = 'localhost:39247'
$GritEvidence = 'C:\Users\Administrator\Desktop\grit\artifacts\srtl_fold8_20261028'
function Read-GritUi {
    & $GritAdb -s $GritSerial shell uiautomator dump /data/local/tmp/grit_ui.xml | Out-Null
    [xml]$view = (& $GritAdb -s $GritSerial shell cat /data/local/tmp/grit_ui.xml) -join ''
    if (-not $view.SelectSingleNode('//node[@package="com.gritpractice.grit"]')) { throw 'GRIT is not the visible app.' }
    return $view
}
function Show-GritUi {
    $view = Read-GritUi
    $view.SelectNodes('//node') | Where-Object { $_.'content-desc' -ne '' -or $_.text -ne '' } | ForEach-Object { [pscustomobject]@{Label=($_.'content-desc' + $_.text); Bounds=$_.bounds} } | Format-Table -Wrap
}
function Tap-GritLabel([string]$label) {
    $view = Read-GritUi
    $nodes = @($view.SelectNodes('//node[@package="com.gritpractice.grit"]') | Where-Object { ($_.'content-desc' -replace [char]0x2060, '') -eq $label -or ($_.text -replace [char]0x2060, '') -eq $label })
    if ($nodes.Count -ne 1) { throw "Expected one target: $label, got $($nodes.Count)" }
    $coordinates = [regex]::Matches($nodes[0].bounds, '\d+') | ForEach-Object { [int]$_.Value }
    & $GritAdb -s $GritSerial shell input tap ([int](($coordinates[0]+$coordinates[2])/2)) ([int](($coordinates[1]+$coordinates[3])/2))
}
function Save-GritScreen([string]$name, [string]$display='4630946722019192211') {
    Start-Sleep -Milliseconds 650
    & $GritAdb -s $GritSerial shell screencap -p -d $display /data/local/tmp/grit_screen.png
    & $GritAdb -s $GritSerial pull /data/local/tmp/grit_screen.png "$GritEvidence\$name.png"
}
