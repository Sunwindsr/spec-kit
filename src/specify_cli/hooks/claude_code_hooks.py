#!/usr/bin/env python3
"""
Claude Code Hook System - Integrates TDD validation with Claude Code

This module provides hooks that integrate with Claude Code to enforce
TDD validation rules and prevent invalid task completion.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import subprocess
import tempfile

from .tdd_validation import TDDValidationSystem, ClaudeCodeHook, TaskStatus

class HookRegistry:
    """Registry for Claude Code hooks"""
    
    def __init__(self):
        self.hooks = {}
        self.validation_systems = {}
    
    def register_hook(self, hook_name: str, hook_function):
        """Register a hook function"""
        self.hooks[hook_name] = hook_function
    
    def register_validation_system(self, project_path: Path, validation_system: TDDValidationSystem):
        """Register a validation system for a project"""
        self.validation_systems[str(project_path)] = validation_system
    
    def execute_hook(self, hook_name: str, *args, **kwargs) -> Any:
        """Execute a registered hook"""
        if hook_name not in self.hooks:
            return True  # Default to allowing if hook not found
        
        return self.hooks[hook_name](*args, **kwargs)
    
    def get_validation_system(self, project_path: Path) -> Optional[TDDValidationSystem]:
        """Get validation system for a project"""
        return self.validation_systems.get(str(project_path))

# Global hook registry
hook_registry = HookRegistry()

def setup_tdd_hooks(project_path: Path):
    """Setup TDD validation hooks for Claude Code"""
    validation_system = TDDValidationSystem(project_path)
    hook_system = ClaudeCodeHook(validation_system)
    
    # Register validation system
    hook_registry.register_validation_system(project_path, validation_system)
    
    # Register hooks
    hook_registry.register_hook("pre_task_completion", hook_system.validate_task_completion)
    hook_registry.register_hook("pre_commit", hook_system.pre_commit_hook)
    hook_registry.register_hook("task_status_change", validate_task_status_change)
    hook_registry.register_hook("phase_transition", validate_phase_transition)

def validate_task_status_change(task_id: str, old_status: str, new_status: str, project_path: Path) -> bool:
    """Validate task status changes"""
    validation_system = hook_registry.get_validation_system(project_path)
    if not validation_system:
        return True
    
    # Prevent transitioning to COMPLETE without validation
    if new_status.lower() == "complete":
        task_data = {"id": task_id, "requires_tests": True}  # Load actual task data
        result = validation_system.validate_task_completion(task_id, task_data)
        
        if not result.passed:
            print(f"❌ Cannot mark task {task_id} complete:")
            for issue in result.details.get("issues", []):
                print(f"  - {issue}")
            return False
    
    return True

def validate_phase_transition(from_phase: str, to_phase: str, project_path: Path) -> bool:
    """Validate phase transitions"""
    validation_system = hook_registry.get_validation_system(project_path)
    if not validation_system:
        return True
    
    # Check if all tasks in current phase are complete
    current_tasks = [tid for tid in validation_system.task_validations.keys() 
                    if tid.startswith(from_phase)]
    
    incomplete_tasks = [
        tid for tid in current_tasks
        if validation_system.task_validations[tid].status != TaskStatus.COMPLETE
    ]
    
    if incomplete_tasks:
        print(f"❌ Cannot transition to phase {to_phase}: incomplete tasks")
        for task_id in incomplete_tasks:
            print(f"  - {task_id}")
        return False
    
    return True

def execute_claude_code_hook(hook_name: str, *args, **kwargs) -> bool:
    """Execute Claude Code hook"""
    return hook_registry.execute_hook(hook_name, *args, **kwargs)

def main():
    """Main function for standalone hook execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Code Hook System")
    parser.add_argument("hook_name", help="Name of the hook to execute")
    parser.add_argument("--project-path", type=Path, help="Path to project directory")
    parser.add_argument("--task-id", type=str, help="Task ID for task-specific hooks")
    parser.add_argument("--old-status", type=str, help="Old task status")
    parser.add_argument("--new-status", type=str, help="New task status")
    parser.add_argument("--from-phase", type=str, help="Source phase for transition")
    parser.add_argument("--to-phase", type=str, help="Target phase for transition")
    
    args = parser.parse_args()
    
    # Setup hooks if project path provided
    if args.project_path:
        setup_tdd_hooks(args.project_path)
    
    # Execute requested hook
    hook_args = []
    hook_kwargs = {}
    
    if args.task_id:
        hook_kwargs["task_id"] = args.task_id
    if args.old_status:
        hook_kwargs["old_status"] = args.old_status
    if args.new_status:
        hook_kwargs["new_status"] = args.new_status
    if args.from_phase:
        hook_kwargs["from_phase"] = args.from_phase
    if args.to_phase:
        hook_kwargs["to_phase"] = args.to_phase
    if args.project_path:
        hook_kwargs["project_path"] = args.project_path
    
    success = execute_claude_code_hook(args.hook_name, *hook_args, **hook_kwargs)
    
    if success:
        print(f"✅ Hook {args.hook_name} executed successfully")
        return 0
    else:
        print(f"❌ Hook {args.hook_name} execution failed")
        return 1

if __name__ == "__main__":
    exit(main())