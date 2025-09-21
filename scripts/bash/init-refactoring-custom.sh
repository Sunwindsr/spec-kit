#!/usr/bin/env bash
# Refactoring-specific initialization that uses your custom repository
set -e

JSON_MODE=false
ARGS=()
for arg in "$@"; do
    case "$arg" in
        --json) JSON_MODE=true ;;
        --help|-h) echo "Usage: $0 [--json] <project_path>"; exit 0 ;;
        *) ARGS+=("$arg") ;;
    esac
done

PROJECT_PATH="${ARGS[*]}"
if [ -z "$PROJECT_PATH" ]; then
    echo "Usage: $0 [--json] <project_path>" >&2
    exit 1
fi

# Resolve repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Create project directory
mkdir -p "$PROJECT_PATH"
PROJECT_PATH="$(cd "$PROJECT_PATH" && pwd)"

echo "Initializing refactoring project at: $PROJECT_PATH"

# Step 1: Initialize standard Spec Kit project using YOUR repository
echo "Step 1: Downloading Spec Kit template from your custom repository..."
cd "$PROJECT_PATH"

# Set environment variables to use your repository
export SPEC_KIT_REPO_OWNER="Sunwindsr"
export SPEC_KIT_REPO_NAME="spec-kit"

# Detect AI assistant and script type (default to claude and sh)
AI_ASSISTANT="${SPECIFY_AI:-claude}"
SCRIPT_TYPE="${SPECIFY_SCRIPT:-sh}"

# Try to use uvx specify-cli.py with custom repository
if command -v uvx &> /dev/null; then
    echo "Using uvx specify-cli.py with your custom repository..."
    if SPEC_KIT_REPO_OWNER="Sunwindsr" SPEC_KIT_REPO_NAME="spec-kit" uvx specify-cli.py init --here --ai "$AI_ASSISTANT" --script "$SCRIPT_TYPE" --ignore-agent-tools; then
        echo "✓ Spec Kit template initialized from your repository"
    else
        echo "✗ Failed to initialize from your repository" >&2
        exit 1
    fi
else
    echo "✗ No Spec Kit CLI found. Please install specify-cli or uvx" >&2
    exit 1
fi

# Check if .specify directory was created
if [ ! -d ".specify" ]; then
    echo "✗ Spec Kit initialization failed - .specify directory not found" >&2
    exit 1
fi

echo "✓ Successfully created refactoring project with your custom templates!"
echo "🎉 Your refactoring features are now included in the base template!"

if $JSON_MODE; then
    printf '{"PROJECT_PATH":"%s","STATUS":"success","SOURCE":"custom-repository","REPO":"Sunwindsr/spec-kit","REFACTORING_COMMANDS":["constitution-refactoring","specify-refactoring","plan-refactoring","tasks-refactoring","implement-refactoring","init-refactoring"]}\n' "$PROJECT_PATH"
else
    echo "PROJECT_PATH: $PROJECT_PATH"
    echo "STATUS: success"
    echo "SOURCE: custom-repository"
    echo "REPO: Sunwindsr/spec-kit"
    echo "REFACTORING_COMMANDS: constitution-refactoring, specify-refactoring, plan-refactoring, tasks-refactoring, implement-refactoring, init-refactoring"
fi

echo ""
echo "🎉 Refactoring project initialized successfully from your custom repository!"
echo "📁 Project location: $PROJECT_PATH"
echo "📋 Next steps:"
echo "   1. cd $PROJECT_PATH"
echo "   2. Your refactoring commands are already available!"
echo "   3. Use /constitution-refactoring to review principles"
echo "   4. Use /specify-refactoring to begin your refactoring project"