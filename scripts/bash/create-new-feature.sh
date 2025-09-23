#!/usr/bin/env bash
# (Moved to scripts/bash/) Create a new feature with branch, directory structure, and template
set -e

JSON_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] <feature_description>"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

FEATURE_DESCRIPTION="${ARGS[*]}"
if [ -z "$FEATURE_DESCRIPTION" ]; then
    echo "Usage: $0 [--json] <feature_description>" >&2
    exit 1
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

BRANCH_NAME=$(echo "$FEATURE_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
WORDS=$(echo "$BRANCH_NAME" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')
BRANCH_NAME="${FEATURE_NUM}-${WORDS}"

if [ "$HAS_GIT" = true ]; then
    git checkout -b "$BRANCH_NAME"
else
    >&2 echo "[specify] Warning: Git repository not detected; skipped branch creation for $BRANCH_NAME"
fi

FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"

TEMPLATE="$REPO_ROOT/templates/spec-template.md"
SPEC_FILE="$FEATURE_DIR/spec.md"
if [ -f "$TEMPLATE" ]; then cp "$TEMPLATE" "$SPEC_FILE"; else touch "$SPEC_FILE"; fi

# Auto-generate all supporting documentation templates
echo "[specify] Generating supporting documentation templates..."

# Generate data-models.md
if [ -f "$REPO_ROOT/templates/data-models-template.md" ]; then
    cp "$REPO_ROOT/templates/data-models-template.md" "$FEATURE_DIR/data-models.md"
    echo "[specify] ✓ Generated data-models.md"
else
    echo "[specify] ⚠ data-models-template.md not found" >&2
fi

# Generate app-flows.md
if [ -f "$REPO_ROOT/templates/app-flows-template.md" ]; then
    cp "$REPO_ROOT/templates/app-flows-template.md" "$FEATURE_DIR/app-flows.md"
    echo "[specify] ✓ Generated app-flows.md"
else
    echo "[specify] ⚠ app-flows-template.md not found" >&2
fi

# Generate test-cases.md  
if [ -f "$REPO_ROOT/templates/test-cases-template.md" ]; then
    cp "$REPO_ROOT/templates/test-cases-template.md" "$FEATURE_DIR/test-cases.md"
    echo "[specify] ✓ Generated test-cases.md"
else
    echo "[specify] ⚠ test-cases-template.md not found" >&2
fi

# Generate api-contracts.md
if [ -f "$REPO_ROOT/templates/api-contracts-template.md" ]; then
    cp "$REPO_ROOT/templates/api-contracts-template.md" "$FEATURE_DIR/api-contracts.md"
    echo "[specify] ✓ Generated api-contracts.md"
else
    echo "[specify] ⚠ api-contracts-template.md not found" >&2
fi

echo "[specify] Documentation generation complete"

if $JSON_MODE; then
    printf '{"BRANCH_NAME":"%s","SPEC_FILE":"%s","FEATURE_NUM":"%s"}\n' "$BRANCH_NAME" "$SPEC_FILE" "$FEATURE_NUM"
else
    echo "BRANCH_NAME: $BRANCH_NAME"
    echo "SPEC_FILE: $SPEC_FILE"
    echo "FEATURE_NUM: $FEATURE_NUM"
fi
