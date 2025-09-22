#!/usr/bin/env pwsh
# Create a new refactoring feature
[CmdletBinding()]
param(
    [switch]$Json,
    [switch]$Path,
    [string]$FeatureName,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Target
)
$ErrorActionPreference = 'Stop'

if (-not $Target -or $Target.Count -eq 0) {
    Write-Error "Usage: ./create-new-feature-refactoring.ps1 [-Json] [-Path] [-FeatureName <name>] <target>"; exit 1
}
$target = ($Target -join ' ').Trim()

if ($Path) {
    # Validate path exists
    if (-not (Test-Path $target)) {
        Write-Error "Error: Path '$target' does not exist"; exit 1
    }
    $systemDesc = "Refactoring target path: $target"
} else {
    $systemDesc = $target
}

$repoRoot = git rev-parse --show-toplevel
$specsDir = Join-Path $repoRoot 'specs'
New-Item -ItemType Directory -Path $specsDir -Force | Out-Null

$highest = 0
if (Test-Path $specsDir) {
    Get-ChildItem -Path $specsDir -Directory | ForEach-Object {
        if ($_.Name -match '^(\d{3})') {
            $num = [int]$matches[1]
            if ($num -gt $highest) { $highest = $num }
        }
    }
}
$next = $highest + 1
$featureNum = ('{0:000}' -f $next)

# Create refactoring-specific branch name
if ($FeatureName) {
    # Use AI-extracted feature name
    $cleanFeatureName = $FeatureName.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', ''
    $branchName = "$featureNum-refactoring-$cleanFeatureName"
    Write-Warning "[specify-refactoring] Using AI-extracted feature name: $FeatureName"
} else {
    # Fallback to auto-generation from description
    $systemName = $systemDesc.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', ''
    $words = ($systemName -split '-') | Where-Object { $_ } | Select-Object -First 3
    $branchName = "$featureNum-refactoring-$([string]::Join('-', $words))"
    Write-Warning "[specify-refactoring] Using auto-generated feature name from description"
}

git checkout -b $branchName | Out-Null

$featureDir = Join-Path $specsDir $branchName
New-Item -ItemType Directory -Path $featureDir -Force | Out-Null

$template = Join-Path $repoRoot 'templates/spec-refactoring-template.md'
$specFile = Join-Path $featureDir 'spec.md'
if (Test-Path $template) { Copy-Item $template $specFile -Force } else { New-Item -ItemType File -Path $specFile | Out-Null }

if ($Json) {
    $obj = [PSCustomObject]@{ 
        BRANCH_NAME = $branchName; 
        SPEC_FILE = $specFile; 
        FEATURE_NUM = $featureNum;
        SYSTEM_DESCRIPTION = $systemDesc;
        FEATURE_NAME = $FeatureName
    }
    $obj | ConvertTo-Json -Compress
} else {
    Write-Output "BRANCH_NAME: $branchName"
    Write-Output "SPEC_FILE: $specFile"
    Write-Output "FEATURE_NUM: $featureNum"
    Write-Output "SYSTEM_DESCRIPTION: $systemDesc"
    Write-Output "FEATURE_NAME: $FeatureName"
}