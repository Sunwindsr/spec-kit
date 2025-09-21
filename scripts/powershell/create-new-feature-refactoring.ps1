#!/usr/bin/env pwsh
# Create a new refactoring feature
[CmdletBinding()]
param(
    [switch]$Json,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$SystemDescription
)
$ErrorActionPreference = 'Stop'

if (-not $SystemDescription -or $SystemDescription.Count -eq 0) {
    Write-Error "Usage: ./create-new-feature-refactoring.ps1 [-Json] <system description>"; exit 1
}
$systemDesc = ($SystemDescription -join ' ').Trim()

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
$systemName = $systemDesc.ToLower() -replace '[^a-z0-9]', '-' -replace '-{2,}', '-' -replace '^-', '' -replace '-$', ''
$words = ($systemName -split '-') | Where-Object { $_ } | Select-Object -First 3
$branchName = "$featureNum-refactoring-$([string]::Join('-', $words))"

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
        SYSTEM_DESCRIPTION = $systemDesc 
    }
    $obj | ConvertTo-Json -Compress
} else {
    Write-Output "BRANCH_NAME: $branchName"
    Write-Output "SPEC_FILE: $specFile"
    Write-Output "FEATURE_NUM: $featureNum"
    Write-Output "SYSTEM_DESCRIPTION: $systemDesc"
}