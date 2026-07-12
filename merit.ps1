# merit-demo public/operator CLI — hides npm/vercel/git implementation details.

param()

$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
$Command = if ($args.Count -gt 0) { "$($args[0])".ToLowerInvariant() } else { 'help' }

function Write-MeritHelp {
    Write-Host @"
merit-demo CLI

Commands:
  verify      Build and verify the local consumer scaffold
  e2e         Run local/provider e2e plus Playwright screenshots when available
  deploy      Verify, link Vercel when needed, and deploy production
  closeout    Verify + e2e + git whitespace/status/head evidence
  help        Print this help

Public users should run this wrapper instead of raw npm/vercel/git commands.
"@
}

function Invoke-Step {
    param([string]$Label, [scriptblock]$Block)
    Write-Host "== $Label =="
    & $Block
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

function Invoke-Verify {
    Push-Location $Root
    try {
        Invoke-Step 'verify' { npm run verify }
        Invoke-Step 'git whitespace check' { git diff --check }
    } finally {
        Pop-Location
    }
}

function Invoke-E2E {
    Push-Location $Root
    try {
        Invoke-Step 'e2e smoke' { npm run e2e }
        Invoke-Step 'playwright route validation' { node scripts/e2e-playwright.mjs }
    } finally {
        Pop-Location
    }
}

function Get-VercelScope {
    $cfg = Join-Path $Root 'cfg/flask_deploy.json'
    if (-not (Test-Path $cfg)) { return $null }
    $json = Get-Content -LiteralPath $cfg -Raw | ConvertFrom-Json
    return $json.vercel_scope
}

function Ensure-VercelLinked {
    $scope = Get-VercelScope
    if (Test-Path (Join-Path $Root '.vercel/project.json')) { return }
    if (-not $scope) { throw 'Missing cfg/flask_deploy.json vercel_scope; run merit apply from merit-agent-skills first.' }
    Invoke-Step 'vercel link' { npx vercel link --yes --scope $scope }
}

function Invoke-Deploy {
    Invoke-Verify
    Push-Location $Root
    try {
        Ensure-VercelLinked
        $scope = Get-VercelScope
        if ($scope) {
            Invoke-Step 'vercel production deploy' { npx vercel deploy --prod --scope $scope }
        } else {
            Invoke-Step 'vercel production deploy' { npx vercel deploy --prod }
        }
    } finally {
        Pop-Location
    }
}

function Invoke-Closeout {
    Invoke-Verify
    Invoke-E2E
    Push-Location $Root
    try {
        Invoke-Step 'git whitespace check' { git diff --check }
        git status --short
        git rev-parse --short HEAD
    } finally {
        Pop-Location
    }
}

switch -Regex ($Command) {
    '^(help|\?)$' { Write-MeritHelp; exit 0 }
    '^verify$' { Invoke-Verify; exit 0 }
    '^e2e$' { Invoke-E2E; exit 0 }
    '^deploy$' { Invoke-Deploy; exit 0 }
    '^closeout$' { Invoke-Closeout; exit 0 }
    default { Write-MeritHelp; exit 1 }
}
