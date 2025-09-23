#!/usr/bin/env bash
set -e
JSON_MODE=false
for arg in "$@"; do case "$arg" in --json) JSON_MODE=true ;; --help|-h) echo "Usage: $0 [--json]"; exit 0 ;; esac; done
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
eval $(get_feature_paths)
check_feature_branch "$CURRENT_BRANCH" || exit 1
check_plan_exists "$IMPL_PLAN" || exit 1
mkdir -p "$FEATURE_DIR"

# Validate refactoring plan includes automated validation requirements
if ! grep -q "Automated Constitution Compliance\|specify refactoring" "$IMPL_PLAN"; then
  echo "WARNING: Refactoring plan does not include automated validation requirements"
  echo "Consider updating the plan to include validation commands"
fi

# Check for reality validation requirements
if ! grep -q "reality-check\|Reality Validation" "$IMPL_PLAN"; then
  echo "WARNING: Reality validation not configured in refactoring plan"
  echo "This is required for preventing mock data and ensuring business logic completeness"
fi

# Copy tasks template
TEMPLATE="$REPO_ROOT/templates/tasks-refactoring-template.md"
[[ -f "$TEMPLATE" ]] && cp "$TEMPLATE" "$TASKS"

# Initialize validation status
echo "🔍 Initializing refactoring tasks with automated validation..."
echo "✅ Template copied with automated validation requirements"
echo "📋 Tasks file created at: $TASKS"
echo ""
echo "🚀 Next steps:"
echo "1. Edit the tasks.md file with your refactoring tasks"
echo "2. Ensure each task includes automated validation commands"
echo "3. Execute task validation: python -m specify_cli refactoring validate-tasks"
echo "4. Begin implementation following progressive refactoring phases"

if $JSON_MODE; then
  printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","TASKS_FILE":"%s","SPECS_DIR":"%s","BRANCH":"%s","REFACTORING_MODE":"true","VALIDATION_READY":"true"}\n' \
    "$FEATURE_SPEC" "$IMPL_PLAN" "$TASKS" "$FEATURE_DIR" "$CURRENT_BRANCH"
else
  echo "FEATURE_SPEC: $FEATURE_SPEC"; echo "IMPL_PLAN: $IMPL_PLAN"; echo "TASKS_FILE: $TASKS"; echo "SPECS_DIR: $FEATURE_DIR"; echo "BRANCH: $CURRENT_BRANCH"; echo "REFACTORING_MODE: true"; echo "VALIDATION_READY: true"
fi