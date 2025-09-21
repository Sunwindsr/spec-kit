#!/usr/bin/env bash
# Create refactoring constitution with predefined principles
set -e

JSON_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] [additional_requirements]"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

ADDITIONAL_REQUIREMENTS="${ARGS[*]}"

# Resolve repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MEMORY_DIR="$REPO_ROOT/memory"
mkdir -p "$MEMORY_DIR"

CONSTITUTION_FILE="$MEMORY_DIR/constitution-refactoring.md"
TEMPLATE="$REPO_ROOT/templates/constitution-refactoring-template.md"

# Copy template to constitution file
if [ -f "$TEMPLATE" ]; then
    cp "$TEMPLATE" "$CONSTITUTION_FILE"
    
    # If additional requirements provided, append them
    if [ -n "$ADDITIONAL_REQUIREMENTS" ]; then
        echo "" >> "$CONSTITUTION_FILE"
        echo "## Additional Requirements" >> "$CONSTITUTION_FILE"
        echo "" >> "$CONSTITUTION_FILE"
        echo "$ADDITIONAL_REQUIREMENTS" >> "$CONSTITUTION_FILE"
    fi
    
    # Update version and date
    sed -i "s/Last Amended: 2025-01-01/Last Amended: $(date +%Y-%m-%d)/" "$CONSTITUTION_FILE"
else
    echo "Error: Constitution template not found at $TEMPLATE" >&2
    exit 1
fi

if $JSON_MODE; then
    printf '{"CONSTITUTION_FILE":"%s","TEMPLATE":"%s","ADDITIONAL_REQUIREMENTS":"%s","REFactoring_MODE":"true"}\n' \
        "$CONSTITUTION_FILE" "$TEMPLATE" "$ADDITIONAL_REQUIREMENTS"
else
    echo "CONSTITUTION_FILE: $CONSTITUTION_FILE"
    echo "TEMPLATE: $TEMPLATE"
    echo "ADDITIONAL_REQUIREMENTS: $ADDITIONAL_REQUIREMENTS"
    echo "REFACTORING_MODE: true"
fi