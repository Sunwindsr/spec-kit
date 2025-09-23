#!/usr/bin/env bash
# Initialize a new refactoring project by downloading standard template and adding refactoring components
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

# Step 1: Initialize standard Spec Kit project using Python CLI
echo "Step 1: Downloading standard Spec Kit template..."
cd "$PROJECT_PATH"

# Detect AI assistant and script type (default to claude and sh)
AI_ASSISTANT="${SPECIFY_AI:-claude}"
SCRIPT_TYPE="${SPECIFY_SCRIPT:-sh}"

# Try to use uvx specify-cli.py if available, otherwise fallback to local installation
if command -v uvx &> /dev/null; then
    echo "Using uvx specify-cli.py to initialize standard project..."
    if uvx specify-cli.py init --here --ai "$AI_ASSISTANT" --script "$SCRIPT_TYPE" --ignore-agent-tools; then
        echo "✓ Standard Spec Kit template initialized successfully"
    else
        echo "✗ Failed to initialize standard Spec Kit template" >&2
        exit 1
    fi
elif command -v specify &> /dev/null; then
    echo "Using specify CLI to initialize standard project..."
    if specify init --here --ai "$AI_ASSISTANT" --script "$SCRIPT_TYPE" --ignore-agent-tools; then
        echo "✓ Standard Spec Kit template initialized successfully"
    else
        echo "✗ Failed to initialize standard Spec Kit template" >&2
        exit 1
    fi
else
    echo "✗ No Spec Kit CLI found. Please install specify-cli or uvx" >&2
    exit 1
fi

# Check if .specify directory was created
if [ ! -d ".specify" ]; then
    echo "✗ Standard Spec Kit initialization failed - .specify directory not found" >&2
    exit 1
fi

# Step 2: Add refactoring components
echo "Step 2: Adding refactoring-specific components..."

# Copy refactoring command templates to .claude/commands/
for cmd in constitution-refactoring specify-refactoring plan-refactoring tasks-refactoring implement-refactoring init-refactoring; do
    if [ -f "$REPO_ROOT/templates/commands/$cmd.md" ]; then
        cp "$REPO_ROOT/templates/commands/$cmd.md" ".claude/commands/"
        echo "✓ Copied $cmd.md"
    fi
done

# Copy refactoring document templates to .specify/templates/
for template in spec-refactoring-template plan-refactoring-template tasks-refactoring-template test-cases-refactoring-template constitution-refactoring-template; do
    if [ -f "$REPO_ROOT/templates/$template.md" ]; then
        cp "$REPO_ROOT/templates/$template.md" ".specify/templates/"
        echo "✓ Copied $template.md"
    fi
done

# Copy refactoring scripts to .specify/scripts/
mkdir -p ".specify/scripts/bash"
mkdir -p ".specify/scripts/powershell"

for script in create-new-feature-refactoring plan-refactoring tasks-refactoring implement-refactoring constitution-refactoring init-refactoring; do
    if [ -f "$REPO_ROOT/scripts/bash/$script.sh" ]; then
        cp "$REPO_ROOT/scripts/bash/$script.sh" ".specify/scripts/bash/"
        chmod +x ".specify/scripts/bash/$script.sh"
        echo "✓ Copied $script.sh"
    fi
done

for script in create-new-feature-refactoring plan-refactoring tasks-refactoring implement-refactoring constitution-refactoring init-refactoring; do
    if [ -f "$REPO_ROOT/scripts/powershell/$script.ps1" ]; then
        cp "$REPO_ROOT/scripts/powershell/$script.ps1" ".specify/scripts/powershell/"
        echo "✓ Copied $script.ps1"
    fi
done

# Copy common scripts
if [ -f "$REPO_ROOT/scripts/bash/common.sh" ]; then
    cp "$REPO_ROOT/scripts/bash/common.sh" ".specify/scripts/bash/"
    echo "✓ Copied common.sh"
fi

if [ -f "$REPO_ROOT/scripts/powershell/common.ps1" ]; then
    cp "$REPO_ROOT/scripts/powershell/common.ps1" ".specify/scripts/powershell/"
    echo "✓ Copied common.ps1"
fi

# Initialize refactoring constitution in .specify/memory/
mkdir -p ".specify/memory"
if [ -f "$REPO_ROOT/templates/constitution-refactoring-template.md" ]; then
    cp "$REPO_ROOT/templates/constitution-refactoring-template.md" ".specify/memory/constitution-refactoring.md"
    # Update date
    sed -i "s/Last Amended: 2025-01-01/Last Amended: $(date +%Y-%m-%d)/" ".specify/memory/constitution-refactoring.md"
    echo "✓ Initialized refactoring constitution"
fi

# Create specs directory in project root
mkdir -p "specs"

# Create project README (append refactoring info if README exists)
if [ -f "README.md" ]; then
    # Append refactoring section to existing README
    cat >> "README.md" << 'EOF'

## Refactoring Support

This project also includes refactoring-specific tools and templates:

### Refactoring Commands

- `/constitution-refactoring` - Manage refactoring constitution
- `/specify-refactoring` - Create refactoring specifications  
- `/plan-refactoring` - Create refactoring implementation plans
- `/tasks-refactoring` - Generate refactoring tasks
- `/implement-refactoring` - Execute refactoring with behavior preservation
- `/init-refactoring` - Initialize new refactoring projects

### Refactoring Constitution

See `.specify/memory/constitution-refactoring.md` for the complete refactoring principles and constraints, including 20 principles for behavior preservation, interface stability, and safe migration.

### Refactoring Templates

The project includes specialized templates for refactoring workflows in `.specify/templates/`.
EOF
    echo "✓ Updated README with refactoring information"
else
    # Create full README if none exists
    cat > "README.md" << 'EOF'
# Refactoring Project

This project is configured for safe, systematic refactoring using Spec Kit's refactoring methodology.

## Available Commands

### Standard Spec Kit Commands
- `/constitution` - Establish project principles
- `/specify` - Create specifications
- `/plan` - Create implementation plans
- `/tasks` - Generate actionable tasks
- `/implement` - Execute implementation

### Refactoring Commands
- `/constitution-refactoring` - Manage refactoring constitution
- `/specify-refactoring` - Create refactoring specifications  
- `/plan-refactoring` - Create refactoring implementation plans
- `/tasks-refactoring` - Generate refactoring tasks
- `/implement-refactoring` - Execute refactoring with behavior preservation
- `/init-refactoring` - Initialize new refactoring projects

## Core Principles

This project follows both standard Spec Kit principles and 20 refactoring principles ensuring:
- 100% behavior preservation
- Interface stability
- Safe incremental migration
- Comprehensive validation
- Complete rollback capability

## Getting Started

1. Run `/constitution` to establish project principles
2. Use `/constitution-refactoring` to review refactoring principles
3. Use `/specify-refactoring` to analyze your target system
4. Follow the refactoring workflow for safe system modernization

## Constitution

- Standard constitution: `memory/constitution.md`
- Refactoring constitution: `.specify/memory/constitution-refactoring.md`
EOF
    echo "✓ Created project README"
fi

# Create gitignore
cat > "$PROJECT_PATH/.gitignore" << 'EOF'
# Refactoring artifacts
specs/
*.log
.tmp/

# IDE and editor files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
EOF

echo "✓ Created .gitignore"

# Add refactoring files to git if git repository exists
if git rev-parse --git-dir > /dev/null 2>&1; then
    git add .
    git commit -m "Add refactoring support to project

- Refactoring command templates
- Refactoring document templates  
- Refactoring scripts
- Refactoring constitution
- Project structure updates

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
    echo "✓ Committed refactoring components to git"
fi

if $JSON_MODE; then
    printf '{"PROJECT_PATH":"%s","STATUS":"success","REFACTORING_COMMANDS":["constitution-refactoring","specify-refactoring","plan-refactoring","tasks-refactoring","implement-refactoring","init-refactoring"],"CONSTITUTION_PATH":"%s/.specify/memory/constitution-refactoring.md","STANDARD_COMMANDS":["constitution","specify","plan","tasks","implement"]}\n' "$PROJECT_PATH" "$PROJECT_PATH"
else
    echo "PROJECT_PATH: $PROJECT_PATH"
    echo "STATUS: success"
    echo "REFACTORING_COMMANDS: constitution-refactoring, specify-refactoring, plan-refactoring, tasks-refactoring, implement-refactoring, init-refactoring"
    echo "CONSTITUTION_PATH: $PROJECT_PATH/.specify/memory/constitution-refactoring.md"
    echo "STANDARD_COMMANDS: constitution, specify, plan, tasks, implement"
fi

echo ""
echo "🎉 Refactoring project initialized successfully!"
echo "📁 Project location: $PROJECT_PATH"
echo "📋 Next steps:"
echo "   1. cd $PROJECT_PATH"
echo "   2. Run /constitution to establish project principles"
echo "   3. Use /constitution-refactoring to review refactoring principles"
echo "   4. Use /specify-refactoring to begin your refactoring project"