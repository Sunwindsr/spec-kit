#!/usr/bin/env bash
set -e
JSON_MODE=false
for arg in "$@"; do case "$arg" in --json) JSON_MODE=true ;; --help|-h) echo "Usage: $0 [--json]"; exit 0 ;; esac; done
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"
eval $(get_feature_paths)
check_feature_branch "$CURRENT_BRANCH" || exit 1
check_tasks_exist "$TASKS_FILE" || exit 1
mkdir -p "$FEATURE_DIR"
if $JSON_MODE; then
  printf '{"FEATURE_SPEC":"%s","IMPL_PLAN":"%s","TASKS_FILE":"%s","SPECS_DIR":"%s","BRANCH":"%s","REFACTORING_MODE":"true","IMPLEMENTATION_READY":"true"}\n' \
    "$FEATURE_SPEC" "$IMPL_PLAN" "$TASKS_FILE" "$FEATURE_DIR" "$CURRENT_BRANCH"
else
  echo "FEATURE_SPEC: $FEATURE_SPEC"; echo "IMPL_PLAN: $IMPL_PLAN"; echo "TASKS_FILE: $TASKS_FILE"; echo "SPECS_DIR: $FEATURE_DIR"; echo "BRANCH: $CURRENT_BRANCH"; echo "REFACTORING_MODE: true"; echo "IMPLEMENTATION_READY: true"
fi