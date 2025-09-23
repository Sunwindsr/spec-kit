#!/usr/bin/env pwsh
# Create comprehensive test cases from requirements with precision definition
[CmdletBinding()]
param(
    [switch]$Json,
    [string]$FeatureName,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Target
)
$ErrorActionPreference = 'Stop'

if (-not $Target -or $Target.Count -eq 0) {
    Write-Error "Usage: ./create-new-test-cases.ps1 [-Json] [-FeatureName <name>] <target>"; exit 1
}
$target = ($Target -join ' ').Trim()

Write-Host "[specify-test-cases] Target: $target" -ForegroundColor Yellow

# Resolve repository root
$repoRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Set-Location $repoRoot

$specsDir = Join-Path $repoRoot 'specs'
New-Item -ItemType Directory -Path $specsDir -Force | Out-Null

# Find the highest existing spec number
$highest = 0
if (Test-Path $specsDir) {
    Get-ChildItem -Path $specsDir -Directory | ForEach-Object {
        $dirName = $_.Name
        if ($dirName -match '^(\d+)') {
            $number = [int]$matches[1]
            if ($number -gt $highest) { $highest = $number }
        }
    }
}

$next = $highest + 1
$featureNum = "{0:D3}" -f $next

# Create test-specific branch name
if ($FeatureName) {
    # Use AI-extracted feature name
    $cleanFeatureName = $FeatureName.ToLower() -replace '[^a-z0-9]', '-' -replace '-+', '-' -replace '^-' -replace '-$'
    $branchName = "{0}-test-{1}" -f $featureNum, $cleanFeatureName
    Write-Host "[specify-test-cases] Using AI-extracted feature name: $FeatureName" -ForegroundColor Yellow
} else {
    # Fallback to auto-generation from description
    $systemName = $target.ToLower() -replace '[^a-z0-9]', '-' -replace '-+', '-' -replace '^-' -replace '-$'
    $words = ($systemName -split '-' | Where-Object { $_ -ne '' } | Select-Object -First 3) -join '-'
    $branchName = "{0}-test-{1}" -f $featureNum, $words
    Write-Host "[specify-test-cases] Using auto-generated feature name from description" -ForegroundColor Yellow
}

# Check if this is a refactoring or new feature
$isRefactoring = $target -match "refactoring" -or $target -match "Refactoring"
if ($isRefactoring) {
    $templateName = "test-cases-refactoring-template.md"
} else {
    $templateName = "test-cases-template.md"
}

Write-Host "[specify-test-cases] Project type: $(if ($isRefactoring) { 'Refactoring' } else { 'New Feature' })" -ForegroundColor Yellow
Write-Host "[specify-test-cases] Using template: $templateName" -ForegroundColor Yellow

# Create git branch
try {
    $currentBranch = git rev-parse --abbrev-ref HEAD
    if ($currentBranch -ne "HEAD") {
        git checkout -b $branchName 2>$null
        $hasGit = $true
    } else {
        Write-Host "[specify-test-cases] Warning: In detached HEAD state; skipped branch creation for $branchName" -ForegroundColor Yellow
        $hasGit = $false
    }
} catch {
    Write-Host "[specify-test-cases] Warning: Git repository not detected; skipped branch creation for $branchName" -ForegroundColor Yellow
    $hasGit = $false
}

$featureDir = Join-Path $specsDir $branchName
New-Item -ItemType Directory -Path $featureDir -Force | Out-Null

# Copy appropriate template
$template = Join-Path $repoRoot "templates" $templateName
$testFile = Join-Path $featureDir 'test-cases.md'
if (Test-Path $template) { 
    # Copy template with UTF-8 encoding
    $content = Get-Content -Path $template -Raw -Encoding UTF8
    Set-Content -Path $testFile -Value $content -Encoding UTF8
} else { 
    New-Item -ItemType File -Path $testFile | Out-Null 
}

if ($Json) {
    $obj = [PSCustomObject]@{ 
        BRANCH_NAME = $branchName
        TEST_FILE = $testFile
        FEATURE_NUM = $featureNum
        TARGET = $target
        FEATURE_NAME = $FeatureName
        IS_REFACTORING = $isRefactoring
    }
    $obj | ConvertTo-Json -Compress
} else {
    Write-Host "BRANCH_NAME: $branchName"
    Write-Host "TEST_FILE: $testFile"
    Write-Host "FEATURE_NUM: $featureNum"
    Write-Host "TARGET: $target"
    Write-Host "FEATURE_NAME: $FeatureName"
    Write-Host "IS_REFACTORING: $(if ($isRefactoring) { 'Yes' } else { 'No' })"
}