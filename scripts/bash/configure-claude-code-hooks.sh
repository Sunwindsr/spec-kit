#!/bin/bash
# Claude Code Hook Configuration Script
# This script configures Claude Code to use the enhanced TDD validation system

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script information
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VALIDATION_SYSTEM="$PROJECT_ROOT/src/specify_cli/enhanced_tdd_validation_system.py"
HOOKS_DIR="$PROJECT_ROOT/.claude"

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create hooks directory if it doesn't exist
create_hooks_directory() {
    log "Creating Claude Code hooks directory..."
    
    if [[ ! -d "$HOOKS_DIR" ]]; then
        mkdir -p "$HOOKS_DIR"
        log_success "Created hooks directory: $HOOKS_DIR"
    else
        log_warning "Hooks directory already exists: $HOOKS_DIR"
    fi
}

# Verify validation system exists
verify_validation_system() {
    log "Verifying enhanced TDD validation system..."
    
    if [[ ! -f "$VALIDATION_SYSTEM" ]]; then
        log_error "Enhanced TDD validation system not found: $VALIDATION_SYSTEM"
        return 1
    fi
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 is required but not found"
        return 1
    fi
    
    # Test the validation system
    if ! python3 "$VALIDATION_SYSTEM" --help &> /dev/null; then
        log_error "Enhanced TDD validation system is not working properly"
        return 1
    fi
    
    log_success "Validation system verified successfully"
    return 0
}

# Create hooks configuration
create_hooks_configuration() {
    log "Creating Claude Code hooks configuration..."
    
    local hook_config="$HOOKS_DIR/hooks.json"
    
    # Check if configuration already exists
    if [[ -f "$hook_config" ]]; then
        log_warning "Hooks configuration already exists: $hook_config"
        log_warning "Backing up existing configuration..."
        cp "$hook_config" "$hook_config.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Create hooks configuration
    cat > "$hook_config" << 'EOF'
{
  "hooks": {
    "pre_task_completion": "python3 /home/sd_dev/projects/spec-kit/src/specify_cli/enhanced_tdd_validation_system.py --validate-task ${TASK_ID} --task-data '${TASK_DATA}'",
    "pre_commit": "python3 /home/sd_dev/projects/spec-kit/src/specify_cli/enhanced_tdd_validation_system.py --comprehensive",
    "task_status_change": "python3 /home/sd_dev/projects/spec-kit/src/specify_cli/hooks/claude_code_hooks.py task_status_change --task-id ${TASK_ID} --old-status ${OLD_STATUS} --new-status ${NEW_STATUS} --project-path ${PROJECT_PATH}",
    "phase_transition": "python3 /home/sd_dev/projects/spec-kit/src/specify_cli/hooks/claude_code_hooks.py phase_transition --from-phase ${FROM_PHASE} --to-phase ${TO_PHASE} --project-path ${PROJECT_PATH}"
  },
  "validation": {
    "test_pass_threshold": 0.95,
    "code_coverage_threshold": 0.80,
    "performance_threshold": 1.0,
    "strict_mode": true,
    "auto_rollback_enabled": true,
    "require_evidence": true
  },
  "reality_testing": {
    "enabled": true,
    "evidence_required": true,
    "behavioral_validation": true,
    "performance_metrics": true
  },
  "quality_gates": {
    "linting": {"enabled": true, "critical": true},
    "type_safety": {"enabled": true, "critical": true},
    "test_coverage": {"enabled": true, "critical": false, "threshold": 0.80},
    "security_scan": {"enabled": true, "critical": true},
    "performance_benchmark": {"enabled": true, "critical": false}
  }
}
EOF
    
    log_success "Hooks configuration created: $hook_config"
}

# Create wrapper script for Claude Code integration
create_wrapper_script() {
    log "Creating Claude Code wrapper script..."
    
    local wrapper_script="$HOOKS_DIR/claude-code-hook"
    
    cat > "$wrapper_script" << 'EOF'
#!/bin/bash
# Claude Code Hook Wrapper for Enhanced TDD Validation System

set -euo pipefail

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VALIDATION_SYSTEM="$PROJECT_ROOT/src/specify_cli/enhanced_tdd_validation_system.py"

# Parse command line arguments
TASK_ID=""
TASK_DATA=""
PROJECT_PATH=""
OLD_STATUS=""
NEW_STATUS=""
FROM_PHASE=""
TO_PHASE=""
HOOK_TYPE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --task-id)
            TASK_ID="$2"
            shift 2
            ;;
        --task-data)
            TASK_DATA="$2"
            shift 2
            ;;
        --project-path)
            PROJECT_PATH="$2"
            shift 2
            ;;
        --old-status)
            OLD_STATUS="$2"
            shift 2
            ;;
        --new-status)
            NEW_STATUS="$2"
            shift 2
            ;;
        --from-phase)
            FROM_PHASE="$2"
            shift 2
            ;;
        --to-phase)
            TO_PHASE="$2"
            shift 2
            ;;
        --hook-type)
            HOOK_TYPE="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Set default project path if not provided
if [[ -z "$PROJECT_PATH" ]]; then
    PROJECT_PATH="$PROJECT_ROOT"
fi

# Function to execute validation
execute_validation() {
    local exit_code=0
    
    case "$HOOK_TYPE" in
        "pre_task_completion")
            if [[ -n "$TASK_ID" && -n "$TASK_DATA" ]]; then
                echo "🔍 Running pre-task completion validation for: $TASK_ID"
                python3 "$VALIDATION_SYSTEM" --validate-task "$TASK_ID" --task-data "$TASK_DATA"
                exit_code=$?
            else
                echo "❌ Missing task_id or task_data for pre_task_completion hook"
                exit_code=1
            fi
            ;;
        "pre_commit")
            echo "🔍 Running pre-commit comprehensive validation"
            python3 "$VALIDATION_SYSTEM" --comprehensive --project-path "$PROJECT_PATH"
            exit_code=$?
            ;;
        "task_status_change")
            if [[ -n "$TASK_ID" && -n "$OLD_STATUS" && -n "$NEW_STATUS" ]]; then
                echo "🔍 Validating task status change: $TASK_ID ($OLD_STATUS -> $NEW_STATUS)"
                python3 "$PROJECT_ROOT/src/specify_cli/hooks/claude_code_hooks.py" \
                    task_status_change \
                    --task-id "$TASK_ID" \
                    --old-status "$OLD_STATUS" \
                    --new-status "$NEW_STATUS" \
                    --project-path "$PROJECT_PATH"
                exit_code=$?
            else
                echo "❌ Missing required parameters for task_status_change hook"
                exit_code=1
            fi
            ;;
        "phase_transition")
            if [[ -n "$FROM_PHASE" && -n "$TO_PHASE" ]]; then
                echo "🔍 Validating phase transition: $FROM_PHASE -> $TO_PHASE"
                python3 "$PROJECT_ROOT/src/specify_cli/hooks/claude_code_hooks.py" \
                    phase_transition \
                    --from-phase "$FROM_PHASE" \
                    --to-phase "$TO_PHASE" \
                    --project-path "$PROJECT_PATH"
                exit_code=$?
            else
                echo "❌ Missing required parameters for phase_transition hook"
                exit_code=1
            fi
            ;;
        *)
            echo "❌ Unknown hook type: $HOOK_TYPE"
            exit_code=1
            ;;
    esac
    
    return $exit_code
}

# Execute validation
execute_validation

# Exit with appropriate code
if [[ $exit_code -eq 0 ]]; then
    echo "✅ Hook validation passed"
    exit 0
else
    echo "❌ Hook validation failed"
    exit 1
fi
EOF
    
    # Make wrapper script executable
    chmod +x "$wrapper_script"
    
    log_success "Wrapper script created: $wrapper_script"
}

# Create example usage script
create_example_script() {
    log "Creating example usage script..."
    
    local example_script="$HOOKS_DIR/example-usage.sh"
    
    cat > "$example_script" << 'EOF'
#!/bin/bash
# Example usage of Claude Code hooks with Enhanced TDD Validation System

echo "🚀 Claude Code Hooks - Enhanced TDD Validation System"
echo "=================================================="

# Example 1: Pre-task completion validation
echo ""
echo "📋 Example 1: Pre-task completion validation"
echo "-------------------------------------------"

TASK_DATA='{
    "requires_tests": true,
    "test_results": [
        {
            "test_id": "test_user_creation",
            "status": "passed",
            "evidence_link": "test-reports/user_creation.log",
            "execution_time": 1.2
        }
    ],
    "expected_behavior": "User can be created successfully",
    "validation_requirements": ["test_results", "quality_gates"]
}'

# Run pre-task completion validation
echo "Running validation for task T001..."
python3 /home/sd_dev/projects/spec-kit/src/specify_cli/enhanced_tdd_validation_system.py \
    --validate-task T001 \
    --task-data "$TASK_DATA"

echo ""

# Example 2: Comprehensive validation
echo "🔍 Example 2: Comprehensive project validation"
echo "------------------------------------------------"

# Run comprehensive validation (this may take a while)
echo "Running comprehensive validation..."
python3 /home/sd_dev/projects/spec-kit/src/specify_cli/enhanced_tdd_validation_system.py \
    --comprehensive

echo ""

# Example 3: System status
echo "📊 Example 3: System status"
echo "--------------------------------"

# Get system status
python3 /home/sd_dev/projects/spec-kit/src/specify_cli/enhanced_tdd_validation_system.py \
    --status

echo ""
echo "✅ Examples completed!"
echo ""
echo "📖 For more information, check the documentation in:"
echo "   - /home/sd_dev/projects/spec-kit/docs/"
echo "   - /home/sd_dev/projects/spec-kit/templates/tasks-template.md"
EOF
    
    # Make example script executable
    chmod +x "$example_script"
    
    log_success "Example usage script created: $example_script"
}

# Create installation verification script
create_verification_script() {
    log "Creating installation verification script..."
    
    local verification_script="$HOOKS_DIR/verify-installation.sh"
    
    cat > "$verification_script" << 'EOF'
#!/bin/bash
# Verify Claude Code hooks installation

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HOOKS_DIR="$PROJECT_ROOT/.claude"

echo "🔍 Verifying Claude Code hooks installation..."
echo "==========================================="

# Check hooks directory
if [[ -d "$HOOKS_DIR" ]]; then
    echo -e "${GREEN}✅${NC} Hooks directory exists: $HOOKS_DIR"
else
    echo -e "${RED}❌${NC} Hooks directory missing: $HOOKS_DIR"
    exit 1
fi

# Check hooks configuration
if [[ -f "$HOOKS_DIR/hooks.json" ]]; then
    echo -e "${GREEN}✅${NC} Hooks configuration exists"
else
    echo -e "${RED}❌${NC} Hooks configuration missing"
    exit 1
fi

# Check wrapper script
if [[ -f "$HOOKS_DIR/claude-code-hook" ]]; then
    echo -e "${GREEN}✅${NC} Wrapper script exists"
else
    echo -e "${RED}❌${NC} Wrapper script missing"
    exit 1
fi

# Check validation system
if [[ -f "$PROJECT_ROOT/src/specify_cli/enhanced_tdd_validation_system.py" ]]; then
    echo -e "${GREEN}✅${NC} Validation system exists"
else
    echo -e "${RED}❌${NC} Validation system missing"
    exit 1
fi

# Test validation system
if python3 "$PROJECT_ROOT/src/specify_cli/enhanced_tdd_validation_system.py" --help &> /dev/null; then
    echo -e "${GREEN}✅${NC} Validation system working"
else
    echo -e "${RED}❌${NC} Validation system not working"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All checks passed! Claude Code hooks are properly installed.${NC}"
echo ""
echo "📋 Next steps:"
echo "   1. Restart Claude Code to load the hooks"
echo "   2. Try completing a task - it should now require validation"
echo "   3. Check the hooks documentation for usage details"
echo ""
echo "📖 Documentation:"
echo "   - Tasks template: $PROJECT_ROOT/templates/tasks-template.md"
echo "   - Example usage: $HOOKS_DIR/example-usage.sh"
EOF
    
    # Make verification script executable
    chmod +x "$verification_script"
    
    log_success "Verification script created: $verification_script"
}

# Main installation process
main() {
    log "Starting Claude Code hooks installation..."
    
    # Create hooks directory
    create_hooks_directory
    
    # Verify validation system
    if ! verify_validation_system; then
        log_error "Validation system verification failed"
        exit 1
    fi
    
    # Create hooks configuration
    create_hooks_configuration
    
    # Create wrapper script
    create_wrapper_script
    
    # Create example script
    create_example_script
    
    # Create verification script
    create_verification_script
    
    # Summary
    echo ""
    log_success "Claude Code hooks installation completed!"
    echo ""
    echo "📁 Installation Summary:"
    echo "   - Hooks directory: $HOOKS_DIR"
    echo "   - Configuration: $HOOKS_DIR/hooks.json"
    echo "   - Wrapper script: $HOOKS_DIR/claude-code-hook"
    echo "   - Example usage: $HOOKS_DIR/example-usage.sh"
    echo "   - Verification script: $HOOKS_DIR/verify-installation.sh"
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Run verification: $HOOKS_DIR/verify-installation.sh"
    echo "   2. Restart Claude Code to load hooks"
    echo "   3. Test with example: $HOOKS_DIR/example-usage.sh"
    echo ""
    echo "📖 For more information, see:"
    echo "   - Template: $PROJECT_ROOT/templates/tasks-template.md"
    echo "   - Documentation: docs/"
}

# Run main function
main "$@"