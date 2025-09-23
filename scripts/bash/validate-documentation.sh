#!/usr/bin/env bash
# Validate documentation completeness for Spec Kit projects
set -e

# Ensure UTF-8 encoding
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

PROJECT_ROOT=""
SPEC_DIR=""
BRANCH_NAME=""
VERBOSE=false
JSON_MODE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --root)
            PROJECT_ROOT="$2"
            shift 2
            ;;
        --spec-dir)
            SPEC_DIR="$2"
            shift 2
            ;;
        --branch)
            BRANCH_NAME="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --json)
            JSON_MODE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [--root <project-root>] [--spec-dir <spec-dir>] [--branch <branch-name>] [--verbose] [--json]"
            echo ""
            echo "Validate documentation completeness for Spec Kit projects"
            echo ""
            echo "Options:"
            echo "  --root <path>        Project root directory (default: auto-detect)"
            echo "  --spec-dir <path>    Specifications directory (default: <root>/specs)"
            echo "  --branch <name>      Branch name to validate (default: current branch or all branches)"
            echo "  --verbose, -v        Show detailed validation results"
            echo "  --json               Output results in JSON format"
            echo "  --help, -h           Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Auto-detect project root if not provided
if [ -z "$PROJECT_ROOT" ]; then
    if git rev-parse --show-toplevel >/dev/null 2>&1; then
        PROJECT_ROOT=$(git rev-parse --show-toplevel)
    else
        PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
    fi
fi

# Set spec directory if not provided
if [ -z "$SPEC_DIR" ]; then
    SPEC_DIR="$PROJECT_ROOT/specs"
fi

# Get current branch if not specified
if [ -z "$BRANCH_NAME" ]; then
    if git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
        BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)
    fi
fi

# Validation function
validate_documentation() {
    local branch_dir="$1"
    local branch_name=$(basename "$branch_dir")
    local issues=0
    local warnings=0
    local files_checked=0

    # Required files for regular features
    local required_files=("spec.md")
    
    # Required files for refactoring features
    local refactoring_files=("api-contracts.md" "data-models.md" "app-flows.md" "test-cases.md")
    
    # Check if this is a refactoring branch
    if [[ "$branch_name" == *"refactoring"* ]]; then
        required_files+=("${refactoring_files[@]}")
    fi
    
    # Check each required file
    for file in "${required_files[@]}"; do
        local file_path="$branch_dir/$file"
        
        if [ -f "$file_path" ]; then
            local file_size=$(wc -c < "$file_path")
            files_checked=$((files_checked + 1))
            
            # Check file content
            if [ "$file_size" -eq 0 ]; then
                issues=$((issues + 1))
            fi
            
            # Check for UTF-8 encoding
            if ! file "$file_path" | grep -q "UTF-8" 2>/dev/null; then
                if ! iconv -f utf-8 -t utf-8 "$file_path" >/dev/null 2>&1; then
                    issues=$((issues + 1))
                fi
            fi
            
            # Check for template placeholders
            if grep -q "\[项目名称\]" "$file_path" || grep -q "\[feature_description\]" "$file_path"; then
                warnings=$((warnings + 1))
            fi
        else
            issues=$((issues + 1))
        fi
    done
    
    # Check for additional recommended files
    local recommended_files=("plan.md" "tasks.md")
    for file in "${recommended_files[@]}"; do
        local file_path="$branch_dir/$file"
        if [ -f "$file_path" ]; then
            files_checked=$((files_checked + 1))
        fi
    done
    
    return $issues
}

# Verbose validation function (for detailed output)
validate_documentation_verbose() {
    local branch_dir="$1"
    local branch_name=$(basename "$branch_dir")
    local issues=0
    local warnings=0
    local files_checked=0
    local missing_files=()

    # Required files for regular features
    local required_files=("spec.md")
    
    # Required files for refactoring features
    local refactoring_files=("api-contracts.md" "data-models.md" "app-flows.md" "test-cases.md")
    
    # Check if this is a refactoring branch
    if [[ "$branch_name" == *"refactoring"* ]]; then
        required_files+=("${refactoring_files[@]}")
    fi
    
    # Check each required file
    for file in "${required_files[@]}"; do
        local file_path="$branch_dir/$file"
        
        if [ -f "$file_path" ]; then
            local file_size=$(wc -c < "$file_path")
            files_checked=$((files_checked + 1))
            
            # Check file content
            if [ "$file_size" -eq 0 ]; then
                issues=$((issues + 1))
            fi
            
            # Check for UTF-8 encoding
            if ! file "$file_path" | grep -q "UTF-8" 2>/dev/null; then
                if ! iconv -f utf-8 -t utf-8 "$file_path" >/dev/null 2>&1; then
                    issues=$((issues + 1))
                fi
            fi
            
            # Check for template placeholders
            if grep -q "\[项目名称\]" "$file_path" || grep -q "\[feature_description\]" "$file_path"; then
                warnings=$((warnings + 1))
            fi
        else
            issues=$((issues + 1))
            missing_files+=("$file")
        fi
    done
    
    # Output detailed results
    echo "=== Validation Results for $branch_name ==="
    echo "Status: $([ $issues -gt 0 ] && echo "invalid" || echo "valid")"
    echo "Issues: $issues"
    echo "Warnings: $warnings"
    echo "Files Checked: $files_checked/${#required_files[@]}"
    echo ""
    
    if [ $issues -gt 0 ]; then
        echo "Missing files:"
        for file in "${missing_files[@]}"; do
            echo "  ❌ $file"
        done
        echo ""
    fi
    
    if [ $warnings -gt 0 ]; then
        echo "Warnings:"
        echo "  ⚠ Some files contain template placeholders"
        echo ""
    fi
    
    return $issues
}

# Main validation logic
main() {
    local total_issues=0
    local total_branches=0
    local all_results=()
    
    # Validate specific branch or all branches
    if [ -n "$BRANCH_NAME" ] && [ -d "$SPEC_DIR/$BRANCH_NAME" ]; then
        if [ "$VERBOSE" = true ]; then
            validate_documentation_verbose "$SPEC_DIR/$BRANCH_NAME"
        else
            validate_documentation "$SPEC_DIR/$BRANCH_NAME"
        fi
        exit_code=$?
        total_branches=$((total_branches + 1))
        total_issues=$((total_issues + exit_code))
    elif [ -n "$BRANCH_NAME" ]; then
        if [ "$JSON_MODE" = true ]; then
            printf '{"error":"Branch not found: %s"}' "$BRANCH_NAME"
        else
            echo "Error: Branch not found: $BRANCH_NAME" >&2
        fi
        exit 1
    else
        # Validate all branches
        for branch_dir in "$SPEC_DIR"/*; do
            if [ -d "$branch_dir" ]; then
                if [ "$VERBOSE" = true ]; then
                    validate_documentation_verbose "$branch_dir"
                else
                    validate_documentation "$branch_dir"
                fi
                exit_code=$?
                total_branches=$((total_branches + 1))
                total_issues=$((total_issues + exit_code))
            fi
        done
    fi
    
    # Output final results
    if [ "$JSON_MODE" = true ]; then
        local all_results_json=""
        if [ ${#all_results[@]} -gt 0 ]; then
            all_results_json="[\"$(IFS=\",\"; echo "${all_results[*]}")\"]"
        else
            all_results_json="[]"
        fi
        printf '{"total_branches":%d,"total_issues":%d,"results":%s}' \
            "$total_branches" "$total_issues" "$all_results_json"
    else
        echo "=== Documentation Validation Summary ==="
        echo "Total Branches: $total_branches"
        echo "Total Issues: $total_issues"
        echo ""
        
        if [ $total_issues -eq 0 ]; then
            echo "✅ All documentation is complete and valid!"
        else
            echo "❌ Documentation issues found. Use --verbose for details."
        fi
    fi
    
    return $total_issues
}

# Run main function
main "$@"