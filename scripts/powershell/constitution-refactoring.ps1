#!/usr/bin/env pwsh
# Create refactoring constitution with predefined principles
[CmdletBinding()]
param(
    [switch]$Json,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$AdditionalRequirements
)
$ErrorActionPreference = 'Stop'

$additionalReq = ($AdditionalRequirements -join ' ').Trim()

$repoRoot = git rev-parse --show-toplevel
$memoryDir = Join-Path $repoRoot 'memory'
New-Item -ItemType Directory -Path $memoryDir -Force | Out-Null

$constitutionFile = Join-Path $memoryDir 'constitution-refactoring.md'
$template = Join-Path $repoRoot 'templates/constitution-refactoring-template.md'

if (Test-Path $template) {
    Copy-Item $template $constitutionFile -Force
    
    if ($additionalReq) {
        Add-Content -Path $constitutionFile -Value ""
        Add-Content -Path $constitutionFile -Value "## Additional Requirements"
        Add-Content -Path $constitutionFile -Value ""
        Add-Content -Path $constitutionFile -Value $additionalReq
    }
    
    # Update version and date
    $today = Get-Date -Format "yyyy-MM-dd"
    (Get-Content $constitutionFile) -replace 'Last Amended: 2025-01-01', "Last Amended: $today" | Set-Content $constitutionFile
} else {
    Write-Error "Error: Constitution template not found at $template"
    exit 1
}

if ($Json) {
    [PSCustomObject]@{ 
        CONSTITUTION_FILE = $constitutionFile; 
        TEMPLATE = $template;
        ADDITIONAL_REQUIREMENTS = $additionalReq;
        REFACTORING_MODE = $true
    } | ConvertTo-Json -Compress
} else {
    Write-Output "CONSTITUTION_FILE: $constitutionFile"
    Write-Output "TEMPLATE: $template"
    Write-Output "ADDITIONAL_REQUIREMENTS: $additionalReq"
    Write-Output "REFACTORING_MODE: true"
}