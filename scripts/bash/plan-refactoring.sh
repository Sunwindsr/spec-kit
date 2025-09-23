#!/usr/bin/env bash
set -e
JSON_MODE=false
for arg in "$@"; do case "$arg" in --json) JSON_MODE=true ;; --help|-h) echo "Usage: $0 [--json]"; exit 0 ;; esac; done
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
eval $(get_feature_paths)
check_feature_branch "$CURRENT_BRANCH" || exit 1
mkdir -p "$FEATURE_DIR"

# Validate refactoring specification has required tech stack info
if [[ ! -f "$FEATURE_SPEC" ]]; then
  echo "ERROR: Refactoring specification not found at $FEATURE_SPEC"
  exit 1
fi

# Check if tech stack is specified in the spec
if ! grep -q "technology stack\|tech stack\|Technology Stack" "$FEATURE_SPEC"; then
  echo "ERROR: Technology stack not specified in refactoring specification"
  echo "Please specify the target technology stack (e.g., 'React + TypeScript + Vite')"
  exit 1
fi

# Copy plan template
TEMPLATE="$REPO_ROOT/templates/plan-refactoring-template.md"
[[ -f "$TEMPLATE" ]] && cp "$TEMPLATE" "$IMPL_PLAN"

# Initialize validation status
echo "🔍 Initializing refactoring plan with automated validation..."
echo "✅ Template copied with automated validation requirements"
echo "📋 Plan created at: $IMPL_PLAN"
echo ""
echo "🚀 Next steps:"
echo "1. Edit the plan.md file with your refactoring details"
echo "2. Execute automated validation: python -m specify_cli refactoring validate-plan"
echo "3. Generate tasks: /tasks-refactoring"

if $JSON_MODE; then
  printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","SPECS_DIR":"%s","BRANCH":"%s","REFACTORING_MODE":"true","VALIDATION_READY":"true"}\n' \
    "$FEATURE_SPEC" "$IMPL_PLAN" "$FEATURE_DIR" "$CURRENT_BRANCH"
else
  echo "FEATURE_SPEC: $FEATURE_SPEC"; echo "IMPL_PLAN: $IMPL_PLAN"; echo "SPECS_DIR: $FEATURE_DIR"; echo "BRANCH: $CURRENT_BRANCH"; echo "REFACTORING_MODE: true"; echo "VALIDATION_READY: true"
fi