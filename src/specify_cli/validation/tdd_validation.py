#!/usr/bin/env python3
"""
Enhanced TDD Validation System - Strengthened test-driven development validation

This system extends the existing refactoring validation to provide comprehensive
TDD validation with test-result association, automated review, and sequential enforcement.
"""

import json
import re
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    FAILED = "failed"
    COMPLETE = "complete"
    BLOCKED = "blocked"

class TestStatus(Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"

class ValidationLevel(Enum):
    MANUAL = "manual"
    AUTOMATED = "automated"
    HYBRID = "hybrid"

@dataclass
class TestResult:
    test_id: str
    status: TestStatus
    duration: float
    evidence_link: str
    notes: str
    environment: str
    execution_date: str
    validated_by: str

@dataclass
class TaskValidation:
    task_id: str
    status: TaskStatus
    test_results: List[TestResult]
    validation_requirements: List[str]
    dependencies: List[str]
    validation_gates: List[str]
    evidence_links: List[str]
    completion_date: Optional[str] = None
    validated_by: Optional[str] = None

@dataclass
class ValidationResult:
    passed: bool
    message: str
    details: Dict[str, Any]
    severity: str  # "error", "warning", "info"
    suggestions: List[str]

class TDDValidationSystem:
    """Enhanced TDD Validation System"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.validation_log = []
        self.task_validations: Dict[str, TaskValidation] = {}
        self.test_history: List[TestResult] = []
        
        # Validation thresholds
        self.test_pass_threshold = 0.95  # 95% test pass rate required
        self.code_coverage_threshold = 0.80  # 80% code coverage required
        self.performance_threshold = 1.0  # Performance within 1x of baseline
        
    def parse_tasks_file(self, tasks_file: Path) -> Dict[str, Any]:
        """Parse tasks file and extract validation requirements"""
        if not tasks_file.exists():
            return {}
            
        with open(tasks_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract task definitions with validation requirements
        task_pattern = r'- \[ \] (T\d+)(?:\[([PVT]+\])?)?\s+(.+)'
        tasks = {}
        
        for match in re.finditer(task_pattern, content):
            task_id = match.group(1)
            flags = match.group(2) or ""
            description = match.group(3)
            
            tasks[task_id] = {
                "id": task_id,
                "description": description,
                "flags": flags,
                "requires_tests": "T" in flags,
                "is_validation_gate": "V" in flags,
                "can_parallel": "P" in flags,
                "test_results": [],
                "validation_requirements": [],
                "dependencies": []
            }
        
        return tasks
    
    def validate_task_completion(self, task_id: str, task_data: Dict[str, Any]) -> ValidationResult:
        """Validate if a task can be marked as complete"""
        validation_issues = []
        suggestions = []
        
        # Check if task has test requirements
        if task_data.get("requires_tests"):
            test_results = task_data.get("test_results", [])
            
            if not test_results:
                validation_issues.append("Task requires test results but none provided")
                suggestions.append("Execute all required tests and record results")
            else:
                # Check test pass rate
                passed_tests = sum(1 for r in test_results if r.get("status") == "passed")
                total_tests = len(test_results)
                
                if total_tests == 0:
                    validation_issues.append("No test results recorded")
                else:
                    pass_rate = passed_tests / total_tests
                    if pass_rate < self.test_pass_threshold:
                        validation_issues.append(
                            f"Test pass rate {pass_rate:.1%} below threshold {self.test_pass_threshold:.1%}"
                        )
                        suggestions.append("Fix failing tests before marking task complete")
        
        # Check if task is a validation gate
        if task_data.get("is_validation_gate"):
            # Validate that previous phase is complete
            if not self._validate_phase_completion(task_id):
                validation_issues.append("Cannot proceed - previous phase validation incomplete")
                suggestions.append("Complete all tasks in previous phase before validation gate")
        
        # Check dependencies
        dependencies = task_data.get("dependencies", [])
        for dep_id in dependencies:
            if not self._is_task_complete(dep_id):
                validation_issues.append(f"Dependency task {dep_id} not complete")
                suggestions.append(f"Complete dependency task {dep_id} first")
        
        # Run automated quality checks
        quality_issues = self._run_quality_checks(task_id)
        validation_issues.extend(quality_issues)
        
        # Determine validation result
        passed = len(validation_issues) == 0
        severity = "error" if validation_issues else "info"
        message = "Task validation passed" if passed else "Task validation failed"
        
        return ValidationResult(
            passed=passed,
            message=message,
            details={
                "task_id": task_id,
                "issues": validation_issues,
                "test_results": task_data.get("test_results", []),
                "dependencies_satisfied": all(self._is_task_complete(dep) for dep in dependencies)
            },
            severity=severity,
            suggestions=suggestions
        )
    
    def record_test_result(self, task_id: str, test_result: TestResult) -> bool:
        """Record test result for a task"""
        if task_id not in self.task_validations:
            self.task_validations[task_id] = TaskValidation(
                task_id=task_id,
                status=TaskStatus.TESTING,
                test_results=[],
                validation_requirements=[],
                dependencies=[],
                validation_gates=[],
                evidence_links=[]
            )
        
        self.task_validations[task_id].test_results.append(test_result)
        self.test_history.append(test_result)
        
        # Update task status based on test results
        if test_result.status == TestStatus.PASSED:
            passed_count = sum(1 for r in self.task_validations[task_id].test_results 
                             if r.status == TestStatus.PASSED)
            total_count = len(self.task_validations[task_id].test_results)
            
            if passed_count / total_count >= self.test_pass_threshold:
                self.task_validations[task_id].status = TaskStatus.IN_PROGRESS
        else:
            self.task_validations[task_id].status = TaskStatus.FAILED
        
        return True
    
    def _validate_phase_completion(self, task_id: str) -> bool:
        """Validate that all tasks in previous phase are complete"""
        # Extract phase from task ID (e.g., T001 -> Phase 1)
        phase_match = re.match(r'T(\d+)', task_id)
        if not phase_match:
            return True  # Non-standard task ID, assume valid
        
        current_phase = int(phase_match.group(1))
        if current_phase <= 1:
            return True  # First phase, no previous phase to validate
        
        # Check all tasks in previous phase are complete
        prev_phase = current_phase - 1
        prev_tasks = [tid for tid in self.task_validations.keys() 
                     if tid.startswith(f'T{prev_phase:03d}')]
        
        return all(self.task_validations[tid].status == TaskStatus.COMPLETE 
                  for tid in prev_tasks)
    
    def _is_task_complete(self, task_id: str) -> bool:
        """Check if a task is complete"""
        validation = self.task_validations.get(task_id)
        return validation and validation.status == TaskStatus.COMPLETE
    
    def _run_quality_checks(self, task_id: str) -> List[str]:
        """Run automated quality checks for a task"""
        issues = []
        
        # Code quality checks
        lint_result = self._run_lint_check(task_id)
        if not lint_result["passed"]:
            issues.extend(lint_result["issues"])
        
        # Type checking
        type_check_result = self._run_type_check(task_id)
        if not type_check_result["passed"]:
            issues.extend(type_check_result["issues"])
        
        # Security checks
        security_result = self._run_security_check(task_id)
        if not security_result["passed"]:
            issues.extend(security_result["issues"])
        
        return issues
    
    def _run_lint_check(self, task_id: str) -> Dict[str, Any]:
        """Run linting checks"""
        # Placeholder for actual linting implementation
        return {"passed": True, "issues": []}
    
    def _run_type_check(self, task_id: str) -> Dict[str, Any]:
        """Run type checking"""
        # Placeholder for actual type checking implementation
        return {"passed": True, "issues": []}
    
    def _run_security_check(self, task_id: str) -> Dict[str, Any]:
        """Run security checks"""
        # Placeholder for actual security checking implementation
        return {"passed": True, "issues": []}
    
    def generate_validation_report(self) -> str:
        """Generate comprehensive validation report"""
        report_lines = ["# TDD Validation Report\n"]
        
        # Overall statistics
        total_tasks = len(self.task_validations)
        completed_tasks = sum(1 for v in self.task_validations.values() 
                            if v.status == TaskStatus.COMPLETE)
        failed_tasks = sum(1 for v in self.task_validations.values() 
                          if v.status == TaskStatus.FAILED)
        
        report_lines.append(f"## Summary")
        report_lines.append(f"- Total Tasks: {total_tasks}")
        report_lines.append(f"- Completed: {completed_tasks}")
        report_lines.append(f"- Failed: {failed_tasks}")
        report_lines.append(f"- Success Rate: {completed_tasks/total_tasks*100:.1f}%\n" if total_tasks > 0 else "- Success Rate: N/A\n")
        
        # Test results summary
        total_tests = len(self.test_history)
        passed_tests = sum(1 for t in self.test_history if t.status == TestStatus.PASSED)
        failed_tests = sum(1 for t in self.test_history if t.status == TestStatus.FAILED)
        
        report_lines.append(f"## Test Results")
        report_lines.append(f"- Total Tests: {total_tests}")
        report_lines.append(f"- Passed: {passed_tests}")
        report_lines.append(f"- Failed: {failed_tests}")
        report_lines.append(f"- Pass Rate: {passed_tests/total_tests*100:.1f}%\n" if total_tests > 0 else "- Pass Rate: N/A\n")
        
        # Detailed task status
        report_lines.append("## Task Status Details")
        for task_id, validation in sorted(self.task_validations.items()):
            status_icon = {
                TaskStatus.PENDING: "🟡",
                TaskStatus.IN_PROGRESS: "🔵",
                TaskStatus.TESTING: "🟠",
                TaskStatus.FAILED: "🔴",
                TaskStatus.COMPLETE: "🟢",
                TaskStatus.BLOCKED: "⚪"
            }.get(validation.status, "❓")
            
            report_lines.append(f"{status_icon} **{task_id}**: {validation.status.value}")
            
            if validation.test_results:
                passed = sum(1 for r in validation.test_results if r.status == TestStatus.PASSED)
                total = len(validation.test_results)
                report_lines.append(f"   - Tests: {passed}/{total} passed")
            
            if validation.validation_gates:
                report_lines.append(f"   - Validation Gates: {', '.join(validation.validation_gates)}")
        
        return "\n".join(report_lines)
    
    def export_validation_data(self, output_path: Path) -> bool:
        """Export validation data for external analysis"""
        data = {
            "export_date": datetime.now().isoformat(),
            "project_path": str(self.project_path),
            "task_validations": {k: asdict(v) for k, v in self.task_validations.items()},
            "test_history": [asdict(t) for t in self.test_history],
            "validation_log": self.validation_log
        }
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.validation_log.append(f"Export failed: {str(e)}")
            return False

class ClaudeCodeHook:
    """Claude Code Hook Integration for Task Validation"""
    
    def __init__(self, validation_system: TDDValidationSystem):
        self.validation_system = validation_system
    
    def validate_task_completion(self, task_id: str, task_data: Dict[str, Any]) -> bool:
        """Hook to validate task completion before allowing it"""
        result = self.validation_system.validate_task_completion(task_id, task_data)
        
        if not result.passed:
            print(f"❌ Task {task_id} validation failed:")
            for issue in result.details.get("issues", []):
                print(f"  - {issue}")
            for suggestion in result.suggestions:
                print(f"  💡 {suggestion}")
            return False
        
        print(f"✅ Task {task_id} validation passed")
        return True
    
    def pre_commit_hook(self) -> bool:
        """Pre-commit hook to validate overall project state"""
        # Check if all completed tasks have proper validation
        incomplete_validations = [
            task_id for task_id, validation in self.validation_system.task_validations.items()
            if validation.status == TaskStatus.COMPLETE and not validation.test_results
        ]
        
        if incomplete_validations:
            print(f"❌ Found {len(incomplete_validations)} completed tasks without test validation:")
            for task_id in incomplete_validations:
                print(f"  - {task_id}")
            return False
        
        print("✅ Pre-commit validation passed")
        return True

def main():
    """Main function for standalone validation execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced TDD Validation System")
    parser.add_argument("project_path", type=Path, help="Path to project directory")
    parser.add_argument("--tasks-file", type=Path, help="Path to tasks file")
    parser.add_argument("--validate-task", type=str, help="Validate specific task")
    parser.add_argument("--export", type=Path, help="Export validation data to file")
    parser.add_argument("--report", action="store_true", help="Generate validation report")
    
    args = parser.parse_args()
    
    # Initialize validation system
    validator = TDDValidationSystem(args.project_path)
    
    # Parse tasks file if provided
    if args.tasks_file:
        tasks = validator.parse_tasks_file(args.tasks_file)
        for task_id, task_data in tasks.items():
            validator.task_validations[task_id] = TaskValidation(
                task_id=task_id,
                status=TaskStatus.PENDING,
                test_results=[],
                validation_requirements=[],
                dependencies=[],
                validation_gates=[],
                evidence_links=[]
            )
    
    # Validate specific task if requested
    if args.validate_task:
        task_data = tasks.get(args.validate_task, {})
        hook = ClaudeCodeHook(validator)
        success = hook.validate_task_completion(args.validate_task, task_data)
        return 0 if success else 1
    
    # Generate report if requested
    if args.report:
        report = validator.generate_validation_report()
        print(report)
    
    # Export data if requested
    if args.export:
        success = validator.export_validation_data(args.export)
        print(f"Export {'successful' if success else 'failed'}")
    
    return 0

if __name__ == "__main__":
    exit(main())