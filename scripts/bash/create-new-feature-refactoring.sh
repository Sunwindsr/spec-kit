#!/usr/bin/env bash
# Create a new refactoring feature with branch, directory structure, and template
set -e

# Ensure UTF-8 encoding
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

JSON_MODE=false
PATH_MODE=false
FEATURE_NAME=""
TARGET=""
ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_MODE=true; shift ;;
        --path) PATH_MODE=true; shift ;;
        --feature-name) 
            FEATURE_NAME="$2"
            shift 2
            ;;
        --target)
            TARGET="$2"
            shift 2
            ;;
        --help|-h) echo "Usage: $0 [--json] [--path] [--feature-name <name>] [--target <path>] [<target>]"; exit 0 ;;
        *) ARGS+=("$1"); shift ;;
    esac
done

# If target not specified via --target, use remaining arguments
if [ -z "$TARGET" ]; then
    if [ ${#ARGS[@]} -eq 0 ]; then
        echo "Usage: $0 [--json] [--path] [--feature-name <name>] [--target <path>] [<target>]" >&2
        exit 1
    fi
    # Join all remaining arguments as the target path
    TARGET="${ARGS[*]}"
fi

echo "[specify-refactoring] Target: $TARGET" >&2

if [ "$PATH_MODE" = true ]; then
    # Validate path exists
    if [ ! -d "$TARGET" ] && [ ! -f "$TARGET" ]; then
        echo "Error: Path '$TARGET' does not exist" >&2
        exit 1
    fi
    SYSTEM_DESCRIPTION="Refactoring target path: $TARGET"
else
    SYSTEM_DESCRIPTION="$TARGET"
fi

# Resolve repository root. Prefer git information when available, but fall back
# to the script location so the workflow still functions in repositories that
# were initialised with --no-git.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FALLBACK_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
if git rev-parse --show-toplevel >/dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    HAS_GIT=true
else
    REPO_ROOT="$FALLBACK_ROOT"
    HAS_GIT=false
fi

cd "$REPO_ROOT"

SPECS_DIR="$REPO_ROOT/specs"
mkdir -p "$SPECS_DIR"

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

# Create refactoring-specific branch name
if [ -n "$FEATURE_NAME" ]; then
    # Use AI-extracted feature name
    CLEAN_FEATURE_NAME=$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
    BRANCH_NAME="${FEATURE_NUM}-refactoring-${CLEAN_FEATURE_NAME}"
    echo "[specify-refactoring] Using AI-extracted feature name: $FEATURE_NAME" >&2
else
    # Fallback to auto-generation from description
    SYSTEM_NAME=$(echo "$SYSTEM_DESCRIPTION" | tr '[:upper:]' '[:lower]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
    WORDS=$(echo "$SYSTEM_NAME" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')
    BRANCH_NAME="${FEATURE_NUM}-refactoring-${WORDS}"
    echo "[specify-refactoring] Using auto-generated feature name from description" >&2
fi

if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    echo "[specify-refactoring] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME" >&2
fi

FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"

TEMPLATE="$REPO_ROOT/templates/spec-refactoring-template.md"
SPEC_FILE="$FEATURE_DIR/spec.md"
if [ -f "$TEMPLATE" ]; then 
    # Ensure UTF-8 encoding when copying template
    cp "$TEMPLATE" "$SPEC_FILE"
    # Force UTF-8 encoding verification and conversion
    if ! file "$SPEC_FILE" | grep -q "UTF-8"; then
        # If not UTF-8, recreate with proper encoding
        iconv -f utf-8 -t utf-8 "$TEMPLATE" > "$SPEC_FILE" 2>/dev/null || cp "$TEMPLATE" "$SPEC_FILE"
    fi
    # Additional UTF-8 safety check - ensure file is properly encoded
    if [ -f "$SPEC_FILE" ]; then
        # Remove any potential BOM and ensure clean UTF-8
        sed -i '1s/^\xEF\xBB\xBF//' "$SPEC_FILE" 2>/dev/null || true
        # Verify file is readable as UTF-8
        if ! iconv -f utf-8 -t utf-8 "$SPEC_FILE" >/dev/null 2>&1; then
            echo "[specify-refactoring] Warning: File may have encoding issues" >&2
        fi
    fi
else
    # Create empty file with UTF-8 encoding
    echo "" | iconv -f utf-8 -t utf-8 > "$SPEC_FILE" 2>/dev/null || touch "$SPEC_FILE"
fi

if $JSON_MODE; then
    printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s","SYSTEM_DESCRIPTION":"%s","FEATURE_NAME":"%s"}\n' "$BRANCH_NAME" "$SPEC_FILE" "$FEATURE_NUM" "$SYSTEM_DESCRIPTION" "$FEATURE_NAME"
else
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "FEATURE_NUM: $FEATURE_NUM"
    echo "SYSTEM_DESCRIPTION: $SYSTEM_DESCRIPTION"
    echo "FEATURE_NAME: $FEATURE_NAME"
fi