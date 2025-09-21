#!/usr/bin/env pwsh
[CmdletBinding()]
param([switch]$Json)
$ErrorActionPreference = 'Stop'
. "$PSScriptRoot/common.ps1"

$paths = Get-FeaturePathsEnv
if (-not (Test-FeatureBranch -Branch $paths.CURRENT_BRANCH)) { exit 1 }
Test-TasksExists -Path $paths.TASKS_FILE

New-Item -ItemType Directory -Path $paths.FEATURE_DIR -Force | Out-Null

if ($Json) {
    [PSCustomObject]@{ 
        FEATURE_SPEC=$paths.FEATURE_SPEC; 
        IMPL_PLAN=$paths.IMPL_PLAN; 
        TASKS_FILE=$paths.TASKS_FILE;
        SPECS_DIR=$paths.FEATURE_DIR; 
        BRANCH=$paths.CURRENT_BRANCH;
        REFACTORING_MODE = $true;
        IMPLEMENTATION_READY = $true
    } | ConvertTo-Json -Compress
} else {
    Write-Output "FEATURE_SPEC: $($paths.FEATURE_SPEC)"
    Write-Output "IMPL_PLAN: $($paths.IMPL_PLAN)"
    Write-Output "TASKS_FILE: $($paths.TASKS_FILE)"
    Write-Output "SPECS_DIR: $($paths.FEATURE_DIR)"
    Write-Output "BRANCH: $($paths.CURRENT_BRANCH)"
    Write-Output "REFACTORING_MODE: true"
    Write-Output "IMPLEMENTATION_READY: true"
}