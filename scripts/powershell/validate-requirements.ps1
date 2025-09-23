#!/usr/bin/env pwsh
# Mandatory requirements validation checkpoint - blocks implementation until requirements pass validation
[CmdletBinding()]
param(
    [switch]$Json,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$TargetPath
)
$ErrorActionPreference = 'Stop'

if (-not $TargetPath -or $TargetPath.Count -eq 0) {
    Write-Error "Usage: ./validate-requirements.ps1 [-Json] [-target] <path-to-test-cases>"; exit 1
}
$targetPath = $TargetPath[0]

Write-Host "[validate-requirements] Starting mandatory validation checkpoint" -ForegroundColor Yellow
Write-Host "[validate-requirements] Target: $targetPath" -ForegroundColor Yellow

# Resolve repository root
$repoRoot = (Get-Item $PSScriptRoot).Parent.Parent.FullName
Set-Location $repoRoot

# Determine the test cases file path
if (Test-Path $targetPath -PathType Container) {
    $testCasesFile = Join-Path $targetPath "test-cases.md"
} elseif (Test-Path $targetPath -PathType Leaf) {
    $testCasesFile = $targetPath
} else {
    Write-Error "ERROR: No test cases file found at $targetPath"
    if ($Json) {
        ConvertTo-Json @{
            status = "ERROR"
            message = "No test cases file found"
            score = 0
            issues = @("Test cases file not found")
        } -Compress
    }
    exit 1
}

if (-not (Test-Path $testCasesFile)) {
    Write-Error "ERROR: Test cases file does not exist: $testCasesFile"
    if ($Json) {
        ConvertTo-Json @{
            status = "ERROR"
            message = "Test cases file does not exist"
            score = 0
            issues = @("Test cases file does not exist")
        } -Compress
    }
    exit 1
}

Write-Host "[validate-requirements] Validating: $testCasesFile" -ForegroundColor Yellow

# Initialize validation variables
$completenessScore = 0
$precisionScore = 0
$traceabilityScore = 0
$qualityScore = 0
$issues = @()
$suggestions = @()

# Read test cases content
$content = Get-Content -Path $testCasesFile -Raw -Encoding UTF8

# Validation functions
function Validate-Completeness {
    Write-Host "[validate-requirements] Validating completeness..." -ForegroundColor Yellow
    
    $score = 30
    $tempIssues = @()
    
    # Check if test cases table exists
    if ($content -notmatch '\|\s*用例ID') {
        $tempIssues += "Missing test cases table"
        $score -= 15
    }
    
    # Check for test cases with data
    $testCaseCount = [regex]::Matches($content, "^\|\s*`TC-").Count
    if ($testCaseCount -eq 0) {
        $tempIssues += "No test cases defined"
        $score -= 20
    } elseif ($testCaseCount -lt 3) {
        $tempIssues += "Insufficient test cases (only $testCaseCount)"
        $score -= 10
    }
    
    # Check for different test case categories
    if ($content -notmatch "Happy Path|正常路径|Boundary|边界|Error|异常") {
        $tempIssues += "Missing test case categories (happy path, boundary, error cases)"
        $score -= 10
    }
    
    # Check for precision definition section
    if ($content -notmatch "Precision Requirements Definition|精确定义|Behavior Precision") {
        $tempIssues += "Missing precision requirements definition section"
        $score -= 15
    }
    
    $script:completenessScore = $score
    $script:issues += $tempIssues | ForEach-Object { "COMPLETENESS: $_" }
}

function Validate-Precision {
    Write-Host "[validate-requirements] Validating precision..." -ForegroundColor Yellow
    
    $score = 30
    $tempIssues = @()
    
    # Check for specific, measurable criteria
    if ($content -match "快速|良好|优秀|用户友好|简单|容易") {
        $tempIssues += "Found ambiguous language (fast, good, user-friendly, etc.)"
        $score -= 10
    }
    
    # Check for specific input/output specifications
    if ($content -notmatch "输入规格|Input Specification|输出规格|Output Specification") {
        $tempIssues += "Missing input/output specifications"
        $score -= 10
    }
    
    # Check for performance metrics
    if ($content -notmatch "性能|Performance|响应时间|response time|吞吐量|throughput") {
        $tempIssues += "Missing performance metrics"
        $score -= 5
    }
    
    # Check for specific test data
    if ($content -notmatch "测试数据|test.*data|JSON|\{") {
        $tempIssues += "Missing specific test data"
        $score -= 10
    }
    
    # Check for validation criteria
    if ($content -notmatch "验证标准|validation|success.*criteria") {
        $tempIssues += "Missing validation criteria"
        $score -= 5
    }
    
    $script:precisionScore = $score
    $script:issues += $tempIssues | ForEach-Object { "PRECISION: $_" }
}

function Validate-Traceability {
    Write-Host "[validate-requirements] Validating traceability..." -ForegroundColor Yellow
    
    $score = 20
    $tempIssues = @()
    
    # Check for requirement IDs
    if ($content -notmatch "REQ-") {
        $tempIssues += "Missing requirement IDs (REQ-XXX)"
        $score -= 10
    }
    
    # Check for test case IDs
    if ($content -notmatch "TC-") {
        $tempIssues += "Missing test case IDs (TC-XXX)"
        $score -= 10
    }
    
    # Check for bidirectional linking
    if ($content -notmatch "关联需求|requirement.*id|REQ-.*TC-|TC-.*REQ-") {
        $tempIssues += "Missing bidirectional traceability between requirements and test cases"
        $score -= 8
    }
    
    $script:traceabilityScore = $score
    $script:issues += $tempIssues | ForEach-Object { "TRACEABILITY: $_" }
}

function Validate-Quality {
    Write-Host "[validate-requirements] Validating quality..." -ForegroundColor Yellow
    
    $score = 20
    $tempIssues = @()
    
    # Check for specific expected results
    if ($content -match "期望结果.*\[\]") {
        $tempIssues += "Found placeholder expected results"
        $score -= 8
    }
    
    # Check for specific execution steps
    if ($content -match "执行步骤.*\[\]") {
        $tempIssues += "Found placeholder execution steps"
        $score -= 8
    }
    
    # Check for specific preconditions
    if ($content -match "前置条件.*\[\]") {
        $tempIssues += "Found placeholder preconditions"
        $score -= 5
    }
    
    # Check for NEEDS CLARIFICATION markers
    if ($content -match "NEEDS CLARIFICATION") {
        $tempIssues += "Found unresolved NEEDS CLARIFICATION markers"
        $score -= 10
    }
    
    $script:qualityScore = $score
    $script:issues += $tempIssues | ForEach-Object { "QUALITY: $_" }
}

function Generate-ValidationReport {
    $totalScore = $completenessScore + $precisionScore + $traceabilityScore + $qualityScore
    $status = ""
    
    if ($totalScore -ge 85) {
        $status = "PASS"
    } elseif ($totalScore -ge 70) {
        $status = "WARNING"
    } else {
        $status = "FAIL"
    }
    
    Write-Host "[validate-requirements] Validation Score: $totalScore/100" -ForegroundColor Yellow
    Write-Host "[validate-requirements] Status: $status" -ForegroundColor Yellow
    
    # Generate validation certificate
    $certDir = Split-Path $testCasesFile -Parent
    $certFile = Join-Path $certDir "validation-certificate.md"
    
    $certContent = @"
# Requirements Validation Certificate

**Validation Date**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
**Test Cases File**: $(Split-Path $testCasesFile -Leaf)
**Overall Score**: $totalScore/100
**Status**: $status

## Score Breakdown

- **Completeness**: $completenessScore/30
- **Precision**: $precisionScore/30  
- **Traceability**: $traceabilityScore/20
- **Quality**: $qualityScore/20

## Validation Status: $status

"@

    if ($status -eq "PASS") {
        $certContent += @"

### ✅ Requirements Approved for Implementation

The requirements definition has passed mandatory validation and is ready for implementation.

**Next Steps**:
- Proceed to implementation phase
- Use this certificate as approval to begin coding
- All implementations must pass the defined test cases

---
*This certificate is automatically generated and is required for implementation to begin.*
"@
    } elseif ($status -eq "WARNING") {
        $certContent += @"

### ⚠️ Requirements Need Minor Improvements

The requirements definition is mostly complete but has some issues that should be addressed.

**Recommended Actions**:
$($issues -join "`n")

**Next Steps**:
- Address the identified issues
- Re-run validation if major changes are made
- Can proceed with implementation with acknowledgment of issues

---
*Minor issues exist but implementation may proceed with caution.*
"@
    } else {
        $certContent += @"

### ❌ Requirements Blocked from Implementation

The requirements definition has critical issues that must be resolved before implementation can begin.

**Blocking Issues**:
$($issues -join "`n")

**Required Actions**:
- Revise requirements to address all blocking issues
- Ensure all test cases are specific and measurable
- Add missing precision definitions
- Re-run validation after revisions

**Implementation Status**: BLOCKED until requirements pass validation

---
*Implementation is prohibited until requirements achieve PASS status.*
"@
    }
    
    $certContent | Set-Content -Path $certFile -Encoding UTF8
    Write-Host "[validate-requirements] Validation certificate generated: $certFile" -ForegroundColor Yellow
    
    # Return results based on mode
    if ($Json) {
        $result = @{
            status = $status
            score = $totalScore
            completeness = $completenessScore
            precision = $precisionScore
            traceability = $traceabilityScore
            quality = $qualityScore
            certificate_file = $certFile
            issues = $issues
            suggestions = $suggestions
            test_cases_file = $testCasesFile
        }
        ConvertTo-Json $result -Compress
    } else {
        Write-Host "=== VALIDATION RESULTS ===" -ForegroundColor Cyan
        Write-Host "Status: $status" -ForegroundColor $(if ($status -eq "PASS") { "Green" } elseif ($status -eq "WARNING") { "Yellow" } else { "Red" })
        Write-Host "Overall Score: $totalScore/100" -ForegroundColor Cyan
        Write-Host "Breakdown:" -ForegroundColor Cyan
        Write-Host "  Completeness: $completenessScore/30" -ForegroundColor Cyan
        Write-Host "  Precision: $precisionScore/30" -ForegroundColor Cyan
        Write-Host "  Traceability: $traceabilityScore/20" -ForegroundColor Cyan
        Write-Host "  Quality: $qualityScore/20" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Issues Found:" -ForegroundColor Yellow
        $issues | ForEach-Object { Write-Host "  - $_" -ForegroundColor Yellow }
        Write-Host ""
        Write-Host "Certificate: $certFile" -ForegroundColor Cyan
        
        # Exit with appropriate code
        if ($status -eq "FAIL") {
            exit 1
        }
    }
}

# Run all validation checks
Validate-Completeness
Validate-Precision
Validate-Traceability
Validate-Quality

# Generate final report
Generate-ValidationReport