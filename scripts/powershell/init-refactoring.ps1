#!/usr/bin/env pwsh
# Initialize a new refactoring project by downloading standard template and adding refactoring components
param(
    [Parameter(Mandatory=$false)]
    [string]$ProjectPath,
    [switch]$Json,
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "Usage: $PSCommandPath [-Json] <project_path>"
    exit 0
}

if (-not $ProjectPath) {
    Write-Host "Usage: $PSCommandPath [-Json] <project_path>" -ForegroundColor Red
    exit 1
}

# Resolve repository root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot = (Resolve-Path "$ScriptDir/../..").Path

# Create project directory
New-Item -ItemType Directory -Force -Path $ProjectPath | Out-Null
$ProjectPath = Resolve-Path $ProjectPath

Write-Host "Initializing refactoring project at: $ProjectPath"

# Step 1: Initialize standard Spec Kit project using Python CLI
Write-Host "Step 1: Downloading standard Spec Kit template..."
Push-Location $ProjectPath

# Detect AI assistant and script type (default to claude and sh)
$AIAssistant = $env:SPECIFY_AI ?? "claude"
$ScriptType = $env:SPECIFY_SCRIPT ?? "sh"

# Try to use uvx specify-cli.py if available, otherwise fallback to local installation
if (Get-Command uvx -ErrorAction SilentlyContinue) {
    Write-Host "Using uvx specify-cli.py to initialize standard project..."
    if (uvx specify-cli.py init --here --ai $AIAssistant --script $ScriptType --ignore-agent-tools) {
        Write-Host "✓ Standard Spec Kit template initialized successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to initialize standard Spec Kit template" -ForegroundColor Red
        exit 1
    }
} elseif (Get-Command specify -ErrorAction SilentlyContinue) {
    Write-Host "Using specify CLI to initialize standard project..."
    if (specify init --here --ai $AIAssistant --script $ScriptType --ignore-agent-tools) {
        Write-Host "✓ Standard Spec Kit template initialized successfully" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed to initialize standard Spec Kit template" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✗ No Spec Kit CLI found. Please install specify-cli or uvx" -ForegroundColor Red
    exit 1
}

# Check if .specify directory was created
if (-not (Test-Path ".specify")) {
    Write-Host "✗ Standard Spec Kit initialization failed - .specify directory not found" -ForegroundColor Red
    exit 1
}

# Step 2: Add refactoring components
Write-Host "Step 2: Adding refactoring-specific components..."

# Copy refactoring command templates to .specify/templates/commands/
$commands = @("constitution-refactoring", "specify-refactoring", "plan-refactoring", "tasks-refactoring", "implement-refactoring", "init-refactoring")
foreach ($cmd in $commands) {
    $srcFile = "$RepoRoot/templates/commands/$cmd.md"
    $destFile = ".specify/templates/commands/$cmd.md"
    if (Test-Path $srcFile) {
        Copy-Item $srcFile $destFile
        Write-Host "✓ Copied $cmd.md"
    }
}

# Copy refactoring document templates to .specify/templates/
$templates = @("spec-refactoring-template", "plan-refactoring-template", "tasks-refactoring-template", "test-cases-refactoring-template", "constitution-refactoring-template")
foreach ($template in $templates) {
    $srcFile = "$RepoRoot/templates/$template.md"
    $destFile = ".specify/templates/$template.md"
    if (Test-Path $srcFile) {
        Copy-Item $srcFile $destFile
        Write-Host "✓ Copied $template.md"
    }
}

# Copy refactoring scripts to .specify/scripts/
New-Item -ItemType Directory -Force -Path ".specify/scripts/bash" | Out-Null
New-Item -ItemType Directory -Force -Path ".specify/scripts/powershell" | Out-Null

$scripts = @("create-new-feature-refactoring", "plan-refactoring", "tasks-refactoring", "implement-refactoring", "constitution-refactoring", "init-refactoring")
foreach ($script in $scripts) {
    $bashScript = "$RepoRoot/scripts/bash/$script.sh"
    $destBashScript = ".specify/scripts/bash/$script.sh"
    if (Test-Path $bashScript) {
        Copy-Item $bashScript $destBashScript
        if ($IsLinux -or $IsMacOS) {
            chmod +x $destBashScript
        }
        Write-Host "✓ Copied $script.sh"
    }
    
    $psScript = "$RepoRoot/scripts/powershell/$script.ps1"
    $destPsScript = ".specify/scripts/powershell/$script.ps1"
    if (Test-Path $psScript) {
        Copy-Item $psScript $destPsScript
        Write-Host "✓ Copied $script.ps1"
    }
}

# Copy common scripts
$commonBash = "$RepoRoot/scripts/bash/common.sh"
$destCommonBash = ".specify/scripts/bash/common.sh"
if (Test-Path $commonBash) {
    Copy-Item $commonBash $destCommonBash
    Write-Host "✓ Copied common.sh"
}

$commonPs = "$RepoRoot/scripts/powershell/common.ps1"
$destCommonPs = ".specify/scripts/powershell/common.ps1"
if (Test-Path $commonPs) {
    Copy-Item $commonPs $destCommonPs
    Write-Host "✓ Copied common.ps1"
}

# Initialize refactoring constitution in .specify/memory/
New-Item -ItemType Directory -Force -Path ".specify/memory" | Out-Null
$constitutionTemplate = "$RepoRoot/templates/constitution-refactoring-template.md"
if (Test-Path $constitutionTemplate) {
    Copy-Item $constitutionTemplate ".specify/memory/constitution-refactoring.md"
    # Update date
    $today = Get-Date -Format "yyyy-MM-dd"
    $content = Get-Content ".specify/memory/constitution-refactoring.md"
    $content = $content -replace "Last Amended: 2025-01-01", "Last Amended: $today"
    $content | Set-Content ".specify/memory/constitution-refactoring.md"
    Write-Host "✓ Initialized refactoring constitution"
}

# Create specs directory in project root
New-Item -ItemType Directory -Force -Path "specs" | Out-Null

# Create project README (append refactoring info if README exists)
if (Test-Path "README.md") {
    # Append refactoring section to existing README
    @'

## Refactoring Support

This project also includes refactoring-specific tools and templates:

### Refactoring Commands

- `/constitution-refactoring` - Manage refactoring constitution
- `/specify-refactoring` - Create refactoring specifications  
- `/plan-refactoring` - Create refactoring implementation plans
- `/tasks-refactoring` - Generate refactoring tasks
- `/implement-refactoring` - Execute refactoring with behavior preservation
- `/init-refactoring` - Initialize new refactoring projects

### Refactoring Constitution

See `.specify/memory/constitution-refactoring.md` for the complete refactoring principles and constraints, including 20 principles for behavior preservation, interface stability, and safe migration.

### Refactoring Templates

The project includes specialized templates for refactoring workflows in `.specify/templates/`.
'@ | Out-File -FilePath "README.md" -Encoding UTF8 -Append
    Write-Host "✓ Updated README with refactoring information"
} else {
    # Create full README if none exists
    @'
# Refactoring Project

This project is configured for safe, systematic refactoring using Spec Kit's refactoring methodology.

## Available Commands

### Standard Spec Kit Commands
- `/constitution` - Establish project principles
- `/specify` - Create specifications
- `/plan` - Create implementation plans
- `/tasks` - Generate actionable tasks
- `/implement` - Execute implementation

### Refactoring Commands
- `/constitution-refactoring` - Manage refactoring constitution
- `/specify-refactoring` - Create refactoring specifications  
- `/plan-refactoring` - Create refactoring implementation plans
- `/tasks-refactoring` - Generate refactoring tasks
- `/implement-refactoring` - Execute refactoring with behavior preservation
- `/init-refactoring` - Initialize new refactoring projects

## Core Principles

This project follows both standard Spec Kit principles and 20 refactoring principles ensuring:
- 100% behavior preservation
- Interface stability
- Safe incremental migration
- Comprehensive validation
- Complete rollback capability

## Getting Started

1. Run `/constitution` to establish project principles
2. Use `/constitution-refactoring` to review refactoring principles
3. Use `/specify-refactoring` to analyze your target system
4. Follow the refactoring workflow for safe system modernization

## Constitution

- Standard constitution: `memory/constitution.md`
- Refactoring constitution: `.specify/memory/constitution-refactoring.md`
'@ | Out-File -FilePath "README.md" -Encoding UTF8
    Write-Host "✓ Created project README"
}

# Create gitignore
@'
# Refactoring artifacts
specs/
*.log
.tmp/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
'@ | Out-File -FilePath "$ProjectPath/.gitignore" -Encoding UTF8

Write-Host "✓ Created .gitignore"

# Add refactoring files to git if git repository exists
if (git rev-parse --git-dir 2>$null) {
    git add .
    git commit -m "Add refactoring support to project

- Refactoring command templates
- Refactoring document templates  
- Refactoring scripts
- Refactoring constitution
- Project structure updates

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    Write-Host "✓ Committed refactoring components to git"
}

if ($Json) {
    $output = @{
        PROJECT_PATH = $ProjectPath
        STATUS = "success"
        REFACTORING_COMMANDS = @("constitution-refactoring", "specify-refactoring", "plan-refactoring", "tasks-refactoring", "implement-refactoring", "init-refactoring")
        CONSTITUTION_PATH = "$ProjectPath/.specify/memory/constitution-refactoring.md"
        STANDARD_COMMANDS = @("constitution", "specify", "plan", "tasks", "implement")
    } | ConvertTo-Json -Compress
    Write-Output $output
} else {
    Write-Host "PROJECT_PATH: $ProjectPath"
    Write-Host "STATUS: success"
    Write-Host "REFACTORING_COMMANDS: constitution-refactoring, specify-refactoring, plan-refactoring, tasks-refactoring, implement-refactoring, init-refactoring"
    Write-Host "CONSTITUTION_PATH: $ProjectPath/.specify/memory/constitution-refactoring.md"
    Write-Host "STANDARD_COMMANDS: constitution, specify, plan, tasks, implement"
}

Write-Host ""
Write-Host "🎉 Refactoring project initialized successfully!"
Write-Host "📁 Project location: $ProjectPath"
Write-Host "📋 Next steps:"
Write-Host "   1. cd $ProjectPath"
Write-Host "   2. Run /constitution to establish project principles"
Write-Host "   3. Use /constitution-refactoring to review refactoring principles"
Write-Host "   4. Use /specify-refactoring to begin your refactoring project"

Pop-Location