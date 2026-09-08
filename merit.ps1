# merit-demo public/operator CLI — keeps build, test, hosting, and source-control details behind MERIT commands.

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
  e2e:playwright  Run the optional browser route check and screenshots
  serve       Build, then serve the repo over HTTP and print /play/ URL
  quickstart  Verify and serve the pinned CompatSet demo
  deploy      Verify, link Vercel when needed, and deploy production
  closeout    Verify + e2e + git whitespace/status/head evidence
  admin       Forward MERIT admin tasks (for example: admin github access status)
  where       Show MERIT surface, repository, account, and environment context
  surface     Alias for where
  help        Print this help

Prefer this wrapper; it keeps implementation details behind clear MERIT commands.
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

function Resolve-MeritAuthority {
    $bench = if ($env:MYMERITAPP) { Join-Path $env:MYMERITAPP 'oss-bench.json' } else { '' }
    $vaultCandidates = @()
    if ($bench -and (Test-Path -LiteralPath $bench)) {
        try {
            $cfg = Get-Content -LiteralPath $bench -Raw | ConvertFrom-Json
            if ($cfg.vaultFolder) { $vaultCandidates += Join-Path ([string]$cfg.vaultFolder) 'scripts\merit.ps1' }
        } catch { }
    }
    if ($env:MYMERITAPP) { $vaultCandidates += Join-Path $env:MYMERITAPP 'merit-private-vault\scripts\merit.ps1' }
    $vaultCandidates += Join-Path (Split-Path -Parent $Root) 'merit-private-vault\scripts\merit.ps1'
    $vault = $vaultCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if ($vault) { return [pscustomobject]@{ plane = 'vault'; cli = $vault } }
    $skills = Join-Path (Split-Path -Parent $Root) 'merit-agent-skills\merit.ps1'
    if (-not (Test-Path -LiteralPath $skills) -and $bench -and (Test-Path $bench)) {
        try { $cfg = Get-Content -LiteralPath $bench -Raw | ConvertFrom-Json; if ($cfg.skillsFolder) { $skills = Join-Path ([string]$cfg.skillsFolder) 'merit.ps1' } } catch { }
    }
    if (-not (Test-Path -LiteralPath $skills)) { throw 'MERIT authority not found: expected vault operator CLI or merit-agent-skills CLI' }
    return [pscustomobject]@{ plane = 'oss'; cli = $skills }
}

function Invoke-Serve {
    Push-Location $Root
    try {
        Invoke-Step 'build' { node scripts/build.mjs }
        Write-Host ''
        Write-Host 'Serving repo root over HTTP. Open /play/ for Hosted Ready proof.'
        Write-Host 'Stop with Ctrl+C when done.'
        Write-Host ''
        node scripts/serve.mjs --port 3000
    } finally {
        Pop-Location
    }
}

function Invoke-Quickstart {
    Push-Location $Root
    try {
        if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw 'Node.js LTS is required for the local showcase. Install Node.js LTS, then rerun .\merit.ps1 quickstart.' }
        Invoke-Step 'verify pinned CompatSet' {
            node scripts/build.mjs
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
            node scripts/verify.mjs
        }
        Write-Host ''
        Write-Host 'MERIT Demo ready. Opening the local HTTP showcase at /play/.' -ForegroundColor Green
        Write-Host 'The hosted workbench version is read from cfg/par_pins.json; do not edit package URLs manually.'
        Write-Host ''
        node scripts/serve.mjs --port 3000
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
        Invoke-Step 'verify' {
            node scripts/build.mjs
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
            node scripts/verify.mjs
        }
        Invoke-Step 'git whitespace check' { git diff --check }
    } finally {
        Pop-Location
    }
}

function Invoke-E2E {
    Push-Location $Root
    try {
        Invoke-Step 'e2e smoke' {
            node scripts/build.mjs
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
            node scripts/e2e-smoke.mjs
        }
        Invoke-Step 'playwright route validation' { node scripts/e2e-playwright.mjs }
    } finally {
        Pop-Location
    }
}

function Invoke-E2EPlaywright {
    Push-Location $Root
    try {
        if (-not (Test-Path -LiteralPath (Join-Path $Root 'node_modules\playwright'))) {
            throw 'Optional browser tools are not present. Use the Hub 3V check for the normal proof, or ask an operator to prepare the advanced browser-check environment.'
        }
        Invoke-Step 'playwright route validation' {
            node scripts/build.mjs
            if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
            node scripts/e2e-playwright.mjs
        }
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
    $vercel = Get-Command vercel -ErrorAction SilentlyContinue
    if (-not $vercel) { throw 'Vercel deployment tool is not available. Stay on the hosted OC path, or ask an operator to prepare the advanced deployment tool.' }
    Invoke-Step 'vercel link' { & $vercel.Source link --yes --scope $scope }
}

function Invoke-Deploy {
    Invoke-Verify
    Push-Location $Root
    try {
        Ensure-VercelLinked
        $scope = Get-VercelScope
        $vercel = Get-Command vercel -ErrorAction SilentlyContinue
        if (-not $vercel) { throw 'Vercel deployment tool is not available. Stay on the hosted OC path, or ask an operator to prepare the advanced deployment tool.' }
        if ($scope) {
            Invoke-Step 'vercel production deploy' { & $vercel.Source deploy --prod --scope $scope }
        } else {
            Invoke-Step 'vercel production deploy' { & $vercel.Source deploy --prod }
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
        $authority = Resolve-MeritAuthority
        Write-Host ("Release authority: {0} ({1})" -f $authority.plane, $authority.cli) -ForegroundColor Cyan
        if ($authority.plane -eq 'vault') {
            $runner = (Get-Command pwsh -ErrorAction SilentlyContinue).Source
            if (-not $runner) { $runner = (Get-Command powershell -ErrorAction Stop).Source }
            & $runner -NoProfile -ExecutionPolicy Bypass -File $authority.cli 'mXin' '-Message' 'merit-demo release closeout'
            if ($LASTEXITCODE -ne 0) { throw "vault release closeout failed (exit $LASTEXITCODE)" }
        } else {
            Invoke-MeritSkillsForward -ForwardArgs @('release','--path',$Root)
        }
    }
}

switch -Regex ($Command) {
    '^(help|\?)$' { Write-MeritHelp; exit 0 }
    '^verify$' { Invoke-Verify; exit 0 }
    '^e2e$' { Invoke-E2E; exit 0 }
    '^e2e:playwright$' { Invoke-E2EPlaywright; exit 0 }
    '^(serve|play)$' { Invoke-Serve; exit 0 }
    '^quickstart$' { Invoke-Quickstart; exit 0 }
    '^deploy$' { Invoke-Deploy; exit 0 }
    '^closeout$' { Invoke-Closeout -ValidateOnly:($Rest -contains '--validate-only'); exit 0 }
    '^admin$' { $forward = @('admin') + $Rest; Invoke-MeritSkillsForward -ForwardArgs $forward }
    '^(where|surface)$' { $forward = @($Command) + $Rest; Invoke-MeritSkillsForward -ForwardArgs $forward }
    default { Write-MeritHelp; exit 1 }
}
