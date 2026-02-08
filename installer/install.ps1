#Requires -Version 5.1
<#
.SYNOPSIS
    Hefesto Skill Generator - Windows Installer
.DESCRIPTION
    Installs Hefesto commands and templates for all detected AI CLIs.
    Compatible with PowerShell 5.1+ (Windows native).
    Idempotent - safe to run multiple times.
#>

[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$HEFESTO_VERSION = "2.0.0"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PayloadDir = Join-Path $ScriptDir "payload"

# ─── Helpers ─────────────────────────────────────────────────────────────────

function Write-Step  { param([string]$msg) Write-Host "[step] " -ForegroundColor Blue -NoNewline; Write-Host $msg }
function Write-Info  { param([string]$msg) Write-Host "[install] " -ForegroundColor Green -NoNewline; Write-Host $msg }
function Write-Warn  { param([string]$msg) Write-Host "[warn] " -ForegroundColor Yellow -NoNewline; Write-Host $msg }
function Write-Err   { param([string]$msg) Write-Host "[error] " -ForegroundColor Red -NoNewline; Write-Host $msg }

function Write-Action {
    param([string]$action, [string]$path, [ConsoleColor]$color)
    Write-Host "  [$action] " -ForegroundColor $color -NoNewline
    Write-Host $path
}

# ─── Find Project Root ──────────────────────────────────────────────────────

function Find-ProjectRoot {
    $dir = Get-Location
    while ($dir.Path -ne [System.IO.Path]::GetPathRoot($dir.Path)) {
        if (Test-Path (Join-Path $dir.Path ".git")) {
            return $dir.Path
        }
        $dir = Split-Path $dir.Path -Parent | Get-Item
    }
    return (Get-Location).Path
}

$ProjectRoot = Find-ProjectRoot

# ─── CLI Detection ───────────────────────────────────────────────────────────

$DetectedCLIs = @()

function Test-CLI {
    param(
        [string]$Id,
        [string]$Name,
        [string]$Command,
        [string]$DirName
    )

    # Check PATH
    if (Get-Command $Command -ErrorAction SilentlyContinue) {
        $script:DetectedCLIs += @{ Id = $Id; Name = $Name; Method = "PATH" }
        return $true
    }

    # Check directory
    $dirPath = Join-Path $ProjectRoot $DirName
    if (Test-Path $dirPath -PathType Container) {
        $script:DetectedCLIs += @{ Id = $Id; Name = $Name; Method = "directory" }
        return $true
    }

    return $false
}

function Test-Copilot {
    if (Get-Command "github-copilot" -ErrorAction SilentlyContinue) {
        $script:DetectedCLIs += @{ Id = "copilot"; Name = "GitHub Copilot"; Method = "PATH" }
        return $true
    }

    $instructionsPath = Join-Path $ProjectRoot ".github\copilot-instructions.md"
    if (Test-Path $instructionsPath) {
        $script:DetectedCLIs += @{ Id = "copilot"; Name = "GitHub Copilot"; Method = "copilot-instructions" }
        return $true
    }

    $agentsPath = Join-Path $ProjectRoot ".github\agents"
    if (Test-Path $agentsPath -PathType Container) {
        $script:DetectedCLIs += @{ Id = "copilot"; Name = "GitHub Copilot"; Method = "agents-dir" }
        return $true
    }

    return $false
}

function Detect-AllCLIs {
    Write-Step "Detecting installed AI CLIs..."

    Test-CLI -Id "claude"   -Name "Claude Code"  -Command "claude"   -DirName ".claude"   | Out-Null
    Test-CLI -Id "gemini"   -Name "Gemini CLI"   -Command "gemini"   -DirName ".gemini"   | Out-Null
    Test-CLI -Id "codex"    -Name "OpenAI Codex" -Command "codex"    -DirName ".codex"    | Out-Null
    Test-Copilot | Out-Null
    Test-CLI -Id "opencode" -Name "OpenCode"     -Command "opencode" -DirName ".opencode" | Out-Null
    Test-CLI -Id "cursor"   -Name "Cursor"       -Command "cursor"   -DirName ".cursor"   | Out-Null
    Test-CLI -Id "qwen"     -Name "Qwen Code"    -Command "qwen"     -DirName ".qwen"     | Out-Null

    if ($DetectedCLIs.Count -eq 0) {
        Write-Warn "No AI CLIs detected. Creating .claude/ as default."
        $script:DetectedCLIs += @{ Id = "claude"; Name = "Claude Code"; Method = "default" }
    }

    Write-Info "Detected $($DetectedCLIs.Count) CLI(s):"
    foreach ($cli in $DetectedCLIs) {
        Write-Host "  + $($cli.Name) (via $($cli.Method))" -ForegroundColor Green
    }
}

# ─── Directory Mapping ───────────────────────────────────────────────────────

function Get-SkillsDir {
    param([string]$CliId)
    switch ($CliId) {
        "claude"   { ".claude\skills" }
        "gemini"   { ".gemini\skills" }
        "codex"    { ".codex\skills" }
        "copilot"  { ".github\skills" }
        "opencode" { ".opencode\skills" }
        "cursor"   { ".cursor\skills" }
        "qwen"     { ".qwen\skills" }
    }
}

function Get-CommandsDir {
    param([string]$CliId)
    switch ($CliId) {
        "claude"   { ".claude\commands" }
        "gemini"   { ".gemini\commands" }
        "codex"    { ".codex\prompts" }
        "copilot"  { ".github" }
        "opencode" { ".opencode\command" }
        "cursor"   { ".cursor\commands" }
        "qwen"     { ".qwen\commands" }
    }
}

function Get-PayloadCommandsDir {
    param([string]$CliId)
    switch ($CliId) {
        "claude"   { "commands\claude" }
        "gemini"   { "commands\gemini" }
        "codex"    { "commands\codex" }
        "copilot"  { "commands\github" }
        "opencode" { "commands\opencode" }
        "cursor"   { "commands\cursor" }
        "qwen"     { "commands\qwen" }
    }
}

# ─── File Copy with Idempotency ──────────────────────────────────────────────

function Copy-FileIdempotent {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$DisplayPath
    )

    if (Test-Path $Destination) {
        $srcHash = (Get-FileHash $Source -Algorithm MD5).Hash
        $dstHash = (Get-FileHash $Destination -Algorithm MD5).Hash
        if ($srcHash -eq $dstHash) {
            Write-Action -action "skip" -path "$DisplayPath (identical)" -color Yellow
        } else {
            Copy-Item -Path $Source -Destination $Destination -Force
            Write-Action -action "update" -path $DisplayPath -color Blue
        }
    } else {
        $parentDir = Split-Path $Destination -Parent
        if (-not (Test-Path $parentDir)) {
            New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
        }
        Copy-Item -Path $Source -Destination $Destination
        Write-Action -action "install" -path $DisplayPath -color Green
    }
}

# ─── Install .hefesto/ ───────────────────────────────────────────────────────

function Install-HefestoDir {
    Write-Step "Installing .hefesto/ directory..."

    $hefestoDir = Join-Path $ProjectRoot ".hefesto"
    $templatesDir = Join-Path $hefestoDir "templates"
    New-Item -ItemType Directory -Path $templatesDir -Force | Out-Null

    # Copy templates
    $templatesSrc = Join-Path $PayloadDir "hefesto\templates"
    if (Test-Path $templatesSrc) {
        Get-ChildItem -Path $templatesSrc -Filter "*.md" | ForEach-Object {
            $dest = Join-Path $templatesDir $_.Name
            Copy-FileIdempotent -Source $_.FullName -Destination $dest -DisplayPath ".hefesto\templates\$($_.Name)"
        }
    }

    # Write version
    $versionFile = Join-Path $hefestoDir "version"
    Set-Content -Path $versionFile -Value $HEFESTO_VERSION -NoNewline
    Write-Info ".hefesto/version = $HEFESTO_VERSION"
}

# ─── Install Commands ────────────────────────────────────────────────────────

function Install-CommandsForCLI {
    param([string]$CliId)

    $targetDir = Join-Path $ProjectRoot (Get-CommandsDir -CliId $CliId)
    $sourceDir = Join-Path $PayloadDir (Get-PayloadCommandsDir -CliId $CliId)

    if (-not (Test-Path $sourceDir)) {
        Write-Warn "No payload found for $CliId, skipping commands"
        return
    }

    # Copilot has nested structure
    if ($CliId -eq "copilot") {
        Install-CopilotCommands -SourceDir $sourceDir -TargetBase $targetDir
        return
    }

    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null

    Get-ChildItem -Path $sourceDir -Filter "hefesto.*" | ForEach-Object {
        $dest = Join-Path $targetDir $_.Name
        $displayPath = "$(Get-CommandsDir -CliId $CliId)\$($_.Name)"
        Copy-FileIdempotent -Source $_.FullName -Destination $dest -DisplayPath $displayPath
    }
}

function Install-CopilotCommands {
    param([string]$SourceDir, [string]$TargetBase)

    # Install agents
    $agentsSrc = Join-Path $SourceDir "agents"
    if (Test-Path $agentsSrc) {
        $agentsDst = Join-Path $TargetBase "agents"
        New-Item -ItemType Directory -Path $agentsDst -Force | Out-Null
        Get-ChildItem -Path $agentsSrc -Filter "hefesto.*" | ForEach-Object {
            $dest = Join-Path $agentsDst $_.Name
            Copy-FileIdempotent -Source $_.FullName -Destination $dest -DisplayPath ".github\agents\$($_.Name)"
        }
    }

    # Install prompts
    $promptsSrc = Join-Path $SourceDir "prompts"
    if (Test-Path $promptsSrc) {
        $promptsDst = Join-Path $TargetBase "prompts"
        New-Item -ItemType Directory -Path $promptsDst -Force | Out-Null
        Get-ChildItem -Path $promptsSrc -Filter "hefesto.*" | ForEach-Object {
            $dest = Join-Path $promptsDst $_.Name
            Copy-FileIdempotent -Source $_.FullName -Destination $dest -DisplayPath ".github\prompts\$($_.Name)"
        }
    }
}

# ─── Install Skills Directories ──────────────────────────────────────────────

function Install-SkillsDirs {
    Write-Step "Creating skills directories..."

    foreach ($cli in $DetectedCLIs) {
        $skillsDir = Join-Path $ProjectRoot (Get-SkillsDir -CliId $cli.Id)
        if (Test-Path $skillsDir) {
            Write-Action -action "exists" -path (Get-SkillsDir -CliId $cli.Id) -color Yellow
        } else {
            New-Item -ItemType Directory -Path $skillsDir -Force | Out-Null
            Write-Action -action "create" -path (Get-SkillsDir -CliId $cli.Id) -color Green
        }
    }
}

# ─── Install All Commands ────────────────────────────────────────────────────

function Install-AllCommands {
    Write-Step "Installing hefesto commands..."

    foreach ($cli in $DetectedCLIs) {
        Install-CommandsForCLI -CliId $cli.Id
    }
}

# ─── Report ──────────────────────────────────────────────────────────────────

function Show-Report {
    Write-Host ""
    Write-Host ("=" * 48) -ForegroundColor White
    Write-Host "  Hefesto v$HEFESTO_VERSION installed successfully!" -ForegroundColor Green
    Write-Host ("=" * 48) -ForegroundColor White
    Write-Host ""
    Write-Host "  Project: $ProjectRoot"
    Write-Host "  CLIs:    $($DetectedCLIs.Count) detected"
    Write-Host ""
    Write-Host "  Installed:" -ForegroundColor White
    Write-Host "    .hefesto/          templates + version"

    foreach ($cli in $DetectedCLIs) {
        $cmdDir = Get-CommandsDir -CliId $cli.Id
        Write-Host ("    {0,-18} commands + skills/" -f "$cmdDir/")
    }

    Write-Host ""
    Write-Host "  Next steps:" -ForegroundColor White
    Write-Host "    1. Run " -NoNewline; Write-Host "/hefesto.list" -ForegroundColor Green -NoNewline; Write-Host " to verify installation"
    Write-Host "    2. Run " -NoNewline; Write-Host '/hefesto.create "description"' -ForegroundColor Green -NoNewline; Write-Host " to generate your first skill"
    Write-Host "    3. Run " -NoNewline; Write-Host "/hefesto.validate skill-name" -ForegroundColor Green -NoNewline; Write-Host " to validate a skill"
    Write-Host ""
}

# ─── Main ────────────────────────────────────────────────────────────────────

function Main {
    Write-Host ""
    Write-Host "Hefesto Skill Generator v$HEFESTO_VERSION - Installer" -ForegroundColor White
    Write-Host ""

    # Verify payload exists
    if (-not (Test-Path $PayloadDir)) {
        Write-Err "Payload directory not found: $PayloadDir"
        Write-Err "Please run this script from the installer/ directory."
        exit 1
    }

    Detect-AllCLIs
    Write-Host ""

    Install-HefestoDir
    Write-Host ""

    Install-SkillsDirs
    Write-Host ""

    Install-AllCommands
    Write-Host ""

    Show-Report
}

Main
