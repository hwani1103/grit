# Only the explicitly authorized phone. Never use an unqualified adb command.
$GritAdb = 'C:\Users\Administrator\AppData\Local\Android\sdk\platform-tools\adb.exe'
$GritSerial = 'R5KL20DHWAE'
function Read-GritUi {
    & $GritAdb -s $GritSerial shell uiautomator dump /data/local/tmp/grit_ui.xml | Out-Null
    [xml]$view = (& $GritAdb -s $GritSerial shell cat /data/local/tmp/grit_ui.xml) -join ''
    if (-not $view.SelectSingleNode('//node[@package="com.gritpractice.grit"]')) { throw 'GRIT is not the visible app.' }
    return $view
}
function Tap-GritNode($node) {
    if ($null -eq $node) { throw 'Target node missing' }
    if ($node.package -ne 'com.gritpractice.grit') { throw 'Not a GRIT node' }
    $coordinates = [regex]::Matches($node.bounds, '\d+') | ForEach-Object { [int]$_.Value }
    $x = [int](($coordinates[0] + $coordinates[2]) / 2)
    $y = [int](($coordinates[1] + $coordinates[3]) / 2)
    & $GritAdb -s $GritSerial shell input tap $x $y
}
function Tap-GritLabel([string]$label) {
    $view = Read-GritUi
    $node = $view.SelectNodes('//node') | Where-Object { $_.'content-desc' -eq $label -or $_.text -eq $label } | Select-Object -First 1
    Tap-GritNode $node
}
function Show-GritUi {
    $view = Read-GritUi
    $view.SelectNodes('//node') | Where-Object { $_.'content-desc' -ne '' -or $_.text -ne '' } | ForEach-Object { [pscustomobject]@{Label=($_.'content-desc' + $_.text); Bounds=$_.bounds} } | Format-Table -Wrap
}