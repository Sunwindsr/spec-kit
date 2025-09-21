#!/usr/bin/env pwsh
[CmdletBinding()]
param([switch]$Json)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/common.ps1"

$paths = Get-FeaturePathsEnv
if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH)) { exit 1 }

New-Item -ItemType Directory -Path $paths.FEATURE_DIR -Force | Out-Null
$template = Join-Path $paths.REPO_ROOT 'templates/plan-refactoring-template.md'
if (Test-Path $template) { Copy-Item $template $paths.IMPL_PLAN -Force }

if ($Json) {
    [PSCustomObject]@{ 
        FEATURE_SPEC=$paths.FEATURE_SPEC; 
        IMPL_PLAN=$paths.IMPL_PLAN; 
        SPECS_DIR=$paths.FEATURE_DIR; 
        BRANCH=$paths.CURRENT_BRANCH;
        REFACTORING_MODE = $true
    } | ConvertTo-Json -Compress
} else {
    Write-Output "FEATURE_SPEC: $($paths.FEATURE_SPEC)"
    Write-Output "IMPL_PLAN: $($paths.IMPL_PLAN)"
    Write-Output "SPECS_DIR: $($paths.FEATURE_DIR)"
    Write-Output "BRANCH: $($paths.CURRENT_BRANCH)"
    Write-Output "REFACTORING_MODE: true"
}