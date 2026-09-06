# merit-demo public/operator CLI — hides npm/vercel/git implementation details.

param()

$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
$Command = if ($args.Count -gt 0) { "$($args[0])".ToLowerInvariant() } else { 'help' }
$Rest = if ($args.Count -gt 1) { @($args[1..($args.Count - 1)]) } else { @() }

function Write-MeritHelp {
    Write-Host @"
merit-demo CLI

Commands:
  verify      Build and verify the local consumer scaffold
  e2e         Run local/provider e2e plus Playwright screenshots when available
  serve       Build, then serve the repo over HTTP and print /play/ URL
  deploy      Verify, link Vercel when needed, and deploy production
  closeout    Verify + e2e + git whitespace/status/head evidence
  admin       Forward MERIT admin tasks (for example: admin github access status)
  where       Show MERIT surface, repository, account, and environment context
  surface     Alias for where
  help        Print this help

Prefer this wrapper over raw npm/npx/vercel. (npm is still what the wrapper calls under the hood.)
"@
}

function Invoke-MeritSkillsForward {
    param([string[]]$ForwardArgs)
    $skills = Join-Path (Split-Path -Parent $Root) 'merit-agent-skills\merit.ps1'
    if (-not (Test-Path -LiteralPath $skills)) {
        $bench = if ($env:MYMERITAPP) { Join-Path $env:MYMERITAPP 'oss-bench.json' } else { '' }
        if ($bench -and (Test-Path $bench)) {
            $cfg = Get-Content -LiteralPath $bench -Raw | ConvertFrom-Json
            if ($cfg.skillsFolder) { $skills = Join-Path ([string]$cfg.skillsFolder) 'merit.ps1' }
        }
    }
    if (-not (Test-Path -LiteralPath $skills)) { throw "MERIT skills CLI not found. Expected sibling: $skills" }
    $runner = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
    if (-not $runner) { $runner = (Get-Command powershell -ErrorAction Stop).Source }
    & $runner -NoProfile -ExecutionPolicy Bypass -File $skills @ForwardArgs
    exit $LASTEXITCODE
}

function Invoke-Serve {
    Push-Location $Root
    try {
        Invoke-Step 'build' { npm run build }
        Write-Host ''
        Write-Host 'Serving repo root over HTTP. Open /play/ for Hosted Ready proof.'
        Write-Host 'Stop with Ctrl+C when done.'
        Write-Host ''
        # serve is a one-liner static server; --yes avoids npx prompt. Port printed by serve.
        npx --yes serve . -l 3000
    } finally {
        Pop-Location
    }
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
    param([switch]$ValidateOnly)
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
    if (-not $ValidateOnly) {
        $forward = @('release','--path',$Root)
        Invoke-MeritSkillsForward -ForwardArgs $forward
    }
}

switch -Regex ($Command) {
    '^(help|\?)$' { Write-MeritHelp; exit 0 }
    '^verify$' { Invoke-Verify; exit 0 }
    '^e2e$' { Invoke-E2E; exit 0 }
    '^(serve|play)$' { Invoke-Serve; exit 0 }
    '^deploy$' { Invoke-Deploy; exit 0 }
    '^closeout$' { Invoke-Closeout -ValidateOnly:($Rest -contains '--validate-only'); exit 0 }
    '^admin$' { $forward = @('admin') + $Rest; Invoke-MeritSkillsForward -ForwardArgs $forward }
    '^(where|surface)$' { $forward = @($Command) + $Rest; Invoke-MeritSkillsForward -ForwardArgs $forward }
    default { Write-MeritHelp; exit 1 }
}
