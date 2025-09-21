#!/usr/bin/env bash
# Create a new refactoring feature with branch, directory structure, and template
set -e

JSON_MODE=false
PATH_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --path) PATH_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] [--path] <target>"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

TARGET="${ARGS[*]}"
if [ -z "$TARGET" ]; then
    echo "Usage: $0 [--json] [--path] <target>" >&2
    exit 1
fi

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
SYSTEM_NAME=$(echo "$SYSTEM_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
WORDS=$(echo "$SYSTEM_NAME" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')
BRANCH_NAME="${FEATURE_NUM}-refactoring-${WORDS}"

if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    >&2 echo "[specify-refactoring] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"

TEMPLATE="$REPO_ROOT/templates/spec-refactoring-template.md"
SPEC_FILE="$FEATURE_DIR/spec.md"
if [ -f "$TEMPLATE" ]; then cp "$TEMPLATE" "$SPEC_FILE"; else touch "$SPEC_FILE"; fi

if $JSON_MODE; then
    printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s","SYSTEM_DESCRIPTION":"%s"}\n' "$BRANCH_NAME" "$SPEC_FILE" "$FEATURE_NUM" "$SYSTEM_DESCRIPTION"
else
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "FEATURE_NUM: $FEATURE_NUM"
    echo "SYSTEM_DESCRIPTION: $SYSTEM_DESCRIPTION"
fi