#!/usr/bin/env bash
# Create comprehensive test cases from requirements with precision definition
set -e

# Ensure UTF-8 encoding
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

JSON_MODE=false
FEATURE_NAME=""
TARGET=""
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_MODE=true; shift ;;
        --feature-name) 
            FEATURE_NAME="$2"
            shift 2
            ;;
        --target)
            TARGET="$2"
            shift 2
            ;;
        --help|-h) echo "Usage: $0 [--json] [--feature-name <name>] [--target <path>] [<target>]"; exit 0 ;;
        *) ARGS+=("$1"); shift ;;
    esac
done

# If target not specified via --target, use remaining arguments
if [ -z "$TARGET" ]; then
    if [ ${#ARGS[@]} -eq 0 ]; then
        echo "Usage: $0 [--json] [--feature-name <name>] [--target <path>] [<target>]" >&2
        exit 1
    fi
    # Join all remaining arguments as the target path
    TARGET="${ARGS[*]}"
fi

echo "[specify-test-cases] Target: $TARGET" >&2

# Resolve repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"

# Find the highest existing spec number
HIGHEST=0
if [ -d "$SPECS_DIR" ]; then
    for dir in "$SPECS_DIR"/*; do
        [ -d "$dir" ] || continue
        dirname=$(basename "$dir")
        number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
        number=$((10#$number))
        if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
    done
fi

NEXT=$((HIGHEST + 1))
FEATURE_NUM=$(printf "%03d" "$NEXT")

# Create test-specific branch name
if [ -n "$FEATURE_NAME" ]; then
    # Use AI-extracted feature name
    CLEAN_FEATURE_NAME=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
    BRANCH_NAME="${FEATURE_NUM}-test-${CLEAN_FEATURE_NAME}"
    echo "[specify-test-cases] Using AI-extracted feature name: $FEATURE_NAME" >&2
else
    # Fallback to auto-generation from description
    SYSTEM_NAME=$(echo "$TARGET" | tr '[:upper:]' '[:lower]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
    WORDS=$(echo "$SYSTEM_NAME" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')
    BRANCH_NAME="${FEATURE_NUM}-test-${WORDS}"
    echo "[specify-test-cases] Using auto-generated feature name from description" >&2
fi

# Check if this is a refactoring or new feature
IS_REFACTORING=false
if [[ "$TARGET" == *"refactoring"* ]] || [[ "$TARGET" == *"Refactoring"* ]]; then
    IS_REFACTORING=true
    TEMPLATE_NAME="test-cases-refactoring-template.md"
else
    TEMPLATE_NAME="test-cases-template.md"
fi

echo "[specify-test-cases] Project type: $([ "$IS_REFACTORING" = true ] && echo 'Refactoring' || echo 'New Feature')" >&2
echo "[specify-test-cases] Using template: $TEMPLATE_NAME" >&2

# Create git branch
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    git checkout -b "$BRANCH_NAME" 2>/dev/null || {
        echo "[specify-test-cases] Warning: Branch $BRANCH_NAME may already exist, continuing..." >&2
    }
    HAS_GIT=true
else
    echo "[specify-test-cases] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME" >&2
    HAS_GIT=false
fi

FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"

# Copy appropriate template
TEMPLATE="$REPO_ROOT/templates/$TEMPLATE_NAME"
TEST_FILE="$FEATURE_DIR/test-cases.md"
if [ -f "$TEMPLATE" ]; then 
    # Ensure UTF-8 encoding when copying template
    cp "$TEMPLATE" "$TEST_FILE"
    # Verify the file is UTF-8 encoded
    if ! file "$TEST_FILE" | grep -q "UTF-8"; then
        # If not UTF-8, recreate with proper encoding
        iconv -f utf-8 -t utf-8 "$TEMPLATE" > "$TEST_FILE" 2>/dev/null || cp "$TEMPLATE" "$TEST_FILE"
    fi
else
    touch "$TEST_FILE"
fi

# Output results
if $JSON_MODE; then
    if [ "$IS_REFACTORING" = true ]; then
        REFACTORING_VAL="true"
    else
        REFACTORING_VAL="false"
    fi
    printf '{"BRANCH_NAME":"%s","TEST_FILE":"%s","FEATURE_NUM":"%s","TARGET":"%s","FEATURE_NAME":"%s","IS_REFACTORING":%s}\n' "$BRANCH_NAME" "$TEST_FILE" "$FEATURE_NUM" "$TARGET" "$FEATURE_NAME" "$REFACTORING_VAL"
else
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "TEST_FILE: $TEST_FILE"
    echo "FEATURE_NUM: $FEATURE_NUM"
    echo "TARGET: $TARGET"
    echo "FEATURE_NAME: $FEATURE_NAME"
    if [ "$IS_REFACTORING" = true ]; then
        echo "IS_REFACTORING: Yes"
    else
        echo "IS_REFACTORING: No"
    fi
fi