#!/usr/bin/env bash
# Mandatory requirements validation checkpoint - blocks implementation until requirements pass validation
set -e

# Ensure UTF-8 encoding
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

JSON_MODE=false
TARGET_PATH=""
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_MODE=true; shift ;;
        --target)
            TARGET_PATH="$2"
            shift 2
            ;;
        --help|-h) echo "Usage: $0 [--json] [--target <path>] [<path>]"; exit 0 ;;
        *) ARGS+=("$1"); shift ;;
    esac
done

# If target not specified via --target, use remaining arguments
if [ -z "$TARGET_PATH" ]; then
    if [ ${#ARGS[@]} -eq 0 ]; then
        echo "Usage: $0 [--json] [--target <path>] [<path>]" >&2
        exit 1
    fi
    TARGET_PATH="${ARGS[*]}"
fi

echo "[validate-requirements] Starting mandatory validation checkpoint" >&2
echo "[validate-requirements] Target: $TARGET_PATH" >&2

# Resolve repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

# Determine the test cases file path
if [ -d "$TARGET_PATH" ]; then
    TEST_CASES_FILE="$TARGET_PATH/test-cases.md"
elif [ -f "$TARGET_PATH" ]; then
    TEST_CASES_FILE="$TARGET_PATH"
else
    echo "ERROR: No test cases file found at $TARGET_PATH" >&2
    if $JSON_MODE; then
        echo '{"status":"ERROR","message":"No test cases file found","score":0,"issues":["Test cases file not found"]}'
    fi
    exit 1
fi

if [ ! -f "$TEST_CASES_FILE" ]; then
    echo "ERROR: Test cases file does not exist: $TEST_CASES_FILE" >&2
    if $JSON_MODE; then
        echo '{"status":"ERROR","message":"Test cases file does not exist","score":0,"issues":["Test cases file does not exist"]}'
    fi
    exit 1
fi

echo "[validate-requirements] Validating: $TEST_CASES_FILE" >&2

# Initialize validation variables
COMPLETENESS_SCORE=0
PRECISION_SCORE=0
TRACEABILITY_SCORE=0
QUALITY_SCORE=0
ISSUES=()
SUGGESTIONS=()

# Validation functions
validate_completeness() {
    echo "[validate-requirements] Validating completeness..." >&2
    
    local score=30
    local temp_issues=()
    
    # Check if test cases table exists
    if ! grep -q "| 用例ID" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing test cases table")
        score=$((score - 15))
    fi
    
    # Check for test cases with data
    local test_case_count=$(grep -c "^| \`TC-" "$TEST_CASES_FILE" || echo "0")
    if [ "$test_case_count" -eq 0 ]; then
        temp_issues+=("No test cases defined")
        score=$((score - 20))
    elif [ "$test_case_count" -lt 3 ]; then
        temp_issues+=("Insufficient test cases (only $test_case_count)")
        score=$((score - 10))
    fi
    
    # Check for different test case categories
    if ! grep -q "Happy Path\|正常路径\|Boundary\|边界\|Error\|异常" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing test case categories (happy path, boundary, error cases)")
        score=$((score - 10))
    fi
    
    # Check for precision definition section
    if ! grep -q "Precision Requirements Definition\|精确定义\|Behavior Precision" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing precision requirements definition section")
        score=$((score - 15))
    fi
    
    COMPLETENESS_SCORE=$score
    for issue in "${temp_issues[@]}"; do
        ISSUES+=("COMPLETENESS: $issue")
    done
}

validate_precision() {
    echo "[validate-requirements] Validating precision..." >&2
    
    local score=30
    local temp_issues=()
    
    # Check for specific, measurable criteria
    if grep -q "快速\|良好\|优秀\|用户友好\|简单\|容易" "$TEST_CASES_FILE"; then
        temp_issues+=("Found ambiguous language (fast, good, user-friendly, etc.)")
        score=$((score - 10))
    fi
    
    # Check for specific input/output specifications
    if ! grep -q "输入规格\|Input Specification\|输出规格\|Output Specification" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing input/output specifications")
        score=$((score - 10))
    fi
    
    # Check for performance metrics
    if ! grep -q "性能\|Performance\|响应时间\|response time\|吞吐量\|throughput" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing performance metrics")
        score=$((score - 5))
    fi
    
    # Check for specific test data
    if ! grep -q "测试数据\|test.*data\|JSON\|{" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing specific test data")
        score=$((score - 10))
    fi
    
    # Check for validation criteria
    if ! grep -q "验证标准\|validation\|success.*criteria" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing validation criteria")
        score=$((score - 5))
    fi
    
    PRECISION_SCORE=$score
    for issue in "${temp_issues[@]}"; do
        ISSUES+=("PRECISION: $issue")
    done
}

validate_traceability() {
    echo "[validate-requirements] Validating traceability..." >&2
    
    local score=20
    local temp_issues=()
    
    # Check for requirement IDs
    if ! grep -q "REQ-" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing requirement IDs (REQ-XXX)")
        score=$((score - 10))
    fi
    
    # Check for test case IDs
    if ! grep -q "TC-" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing test case IDs (TC-XXX)")
        score=$((score - 10))
    fi
    
    # Check for bidirectional linking
    if ! grep -q "关联需求\|requirement.*id\|REQ-.*TC-\|TC-.*REQ-" "$TEST_CASES_FILE"; then
        temp_issues+=("Missing bidirectional traceability between requirements and test cases")
        score=$((score - 8))
    fi
    
    TRACEABILITY_SCORE=$score
    for issue in "${temp_issues[@]}"; do
        ISSUES+=("TRACEABILITY: $issue")
    done
}

validate_quality() {
    echo "[validate-requirements] Validating quality..." >&2
    
    local score=20
    local temp_issues=()
    
    # Check for specific expected results
    if grep -q "期望结果.*\[\]" "$TEST_CASES_FILE"; then
        temp_issues+=("Found placeholder expected results")
        score=$((score - 8))
    fi
    
    # Check for specific execution steps
    if grep -q "执行步骤.*\[\]" "$TEST_CASES_FILE"; then
        temp_issues+=("Found placeholder execution steps")
        score=$((score - 8))
    fi
    
    # Check for specific preconditions
    if grep -q "前置条件.*\[\]" "$TEST_CASES_FILE"; then
        temp_issues+=("Found placeholder preconditions")
        score=$((score - 5))
    fi
    
    # Check for NEEDS CLARIFICATION markers
    if grep -q "NEEDS CLARIFICATION" "$TEST_CASES_FILE"; then
        temp_issues+=("Found unresolved NEEDS CLARIFICATION markers")
        score=$((score - 10))
    fi
    
    QUALITY_SCORE=$score
    for issue in "${temp_issues[@]}"; do
        ISSUES+=("QUALITY: $issue")
    done
}

generate_validation_report() {
    local total_score=$((COMPLETENESS_SCORE + PRECISION_SCORE + TRACEABILITY_SCORE + QUALITY_SCORE))
    local status=""
    
    if [ "$total_score" -ge 85 ]; then
        status="PASS"
    elif [ "$total_score" -ge 70 ]; then
        status="WARNING"
    else
        status="FAIL"
    fi
    
    echo "[validate-requirements] Validation Score: $total_score/100" >&2
    echo "[validate-requirements] Status: $status" >&2
    
    # Generate validation certificate
    local cert_dir="$(dirname "$TEST_CASES_FILE")"
    local cert_file="$cert_dir/validation-certificate.md"
    
    cat > "$cert_file" << EOF
# Requirements Validation Certificate

**Validation Date**: $(date '+%Y-%m-%d %H:%M:%S')
**Test Cases File**: $(basename "$TEST_CASES_FILE")
**Overall Score**: $total_score/100
**Status**: $status

## Score Breakdown

- **Completeness**: $COMPLETENESS_SCORE/30
- **Precision**: $PRECISION_SCORE/30  
- **Traceability**: $TRACEABILITY_SCORE/20
- **Quality**: $QUALITY_SCORE/20

## Validation Status: $status

EOF
    
    if [ "$status" = "PASS" ]; then
        cat >> "$cert_file" << EOF
### ✅ Requirements Approved for Implementation

The requirements definition has passed mandatory validation and is ready for implementation.

**Next Steps**:
- Proceed to implementation phase
- Use this certificate as approval to begin coding
- All implementations must pass the defined test cases

---
*This certificate is automatically generated and is required for implementation to begin.*
EOF
    elif [ "$status" = "WARNING" ]; then
        cat >> "$cert_file" << EOF
### ⚠️ Requirements Need Minor Improvements

The requirements definition is mostly complete but has some issues that should be addressed.

**Recommended Actions**:
$(for issue in "${ISSUES[@]}"; do echo "- $issue"; done)

**Next Steps**:
- Address the identified issues
- Re-run validation if major changes are made
- Can proceed with implementation with acknowledgment of issues

---
*Minor issues exist but implementation may proceed with caution.*
EOF
    else
        cat >> "$cert_file" << EOF
### ❌ Requirements Blocked from Implementation

The requirements definition has critical issues that must be resolved before implementation can begin.

**Blocking Issues**:
$(for issue in "${ISSUES[@]}"; do echo "- $issue"; done)

**Required Actions**:
- Revise requirements to address all blocking issues
- Ensure all test cases are specific and measurable
- Add missing precision definitions
- Re-run validation after revisions

**Implementation Status**: BLOCKED until requirements pass validation

---
*Implementation is prohibited until requirements achieve PASS status.*
EOF
    fi
    
    echo "[validate-requirements] Validation certificate generated: $cert_file" >&2
    
    # Return results based on mode
    if $JSON_MODE; then
        local issues_json=$(printf '%s\n' "${ISSUES[@]}" | jq -R . | jq -s .)
        local suggestions_json=$(printf '%s\n' "${SUGGESTIONS[@]}" | jq -R . | jq -s .)
        
        cat << EOF
{
    "status": "$status",
    "score": $total_score,
    "completeness": $COMPLETENESS_SCORE,
    "precision": $PRECISION_SCORE,
    "traceability": $TRACEABILITY_SCORE,
    "quality": $QUALITY_SCORE,
    "certificate_file": "$cert_file",
    "issues": $issues_json,
    "suggestions": $suggestions_json,
    "test_cases_file": "$TEST_CASES_FILE"
}
EOF
    else
        echo "=== VALIDATION RESULTS ==="
        echo "Status: $status"
        echo "Overall Score: $total_score/100"
        echo "Breakdown:"
        echo "  Completeness: $COMPLETENESS_SCORE/30"
        echo "  Precision: $PRECISION_SCORE/30"
        echo "  Traceability: $TRACEABILITY_SCORE/20"
        echo "  Quality: $QUALITY_SCORE/20"
        echo ""
        echo "Issues Found:"
        for issue in "${ISSUES[@]}"; do
            echo "  - $issue"
        done
        echo ""
        echo "Certificate: $cert_file"
        
        # Exit with appropriate code
        if [ "$status" = "FAIL" ]; then
            exit 1
        fi
    fi
}

# Run all validation checks
validate_completeness
validate_precision
validate_traceability
validate_quality

# Generate final report
generate_validation_report