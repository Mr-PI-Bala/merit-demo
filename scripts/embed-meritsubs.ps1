# Consumer-hosted meritsubs embed (from merit-demo repo).
# Requires meritsubs repo at AgentDraven/meritsubs.
param(
    [string]$MeritsubsRoot = "$env:USERPROFILE\AgentDraven\meritsubs"
)

$ErrorActionPreference = "Stop"
$demoRoot = Split-Path $PSScriptRoot -Parent
$embed = Join-Path $MeritsubsRoot "scripts\embed-merit-demo.ps1"
if (-not (Test-Path $embed)) {
    Write-Error "meritsubs embed script not found: $embed"
}
& $embed -DemoRoot $demoRoot
