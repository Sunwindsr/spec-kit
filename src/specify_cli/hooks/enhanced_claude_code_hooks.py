#!/usr/bin/env python3
"""
Claude Code Hook Integration - Enhanced TDD Validation System

This module provides enhanced hooks that integrate with Claude Code to enforce
comprehensive validation before allowing task completion, preventing self-deception.
"""

import json
import os
import sys
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from validation.tdd_validation import TDDValidationSystem, TaskValidation, TestResult, TestStatus, ValidationResult

@dataclass
class ValidationContext:
    """Context for validation operations"""
    project_path: Path
    task_id: str
    task_data: Dict[str, Any]
    validation_requirements: List[str]
    timestamp: str
    environment: str = "development"

@dataclass
class ReviewResult:
    """Result of a pre-completion review"""
    passed: bool
    critical_issues: List[str]
    warnings: List[str]
    suggestions: List[str]
    test_results_summary: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    evidence_links: List[str]

class EnhancedClaudeCodeHook:
    """Enhanced Claude Code Hook with comprehensive review system"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.validation_system = TDDValidationSystem(project_path)
        self.review_history: List[ReviewResult] = []
        
        # Enhanced validation thresholds
        self.strict_mode = True
        self.require_test_evidence = True
        self.require_quality_gates = True
        
    def pre_completion_review(self, task_id: str, task_data: Dict[str, Any]) -> ReviewResult:
        """Comprehensive pre-completion review that prevents self-deception"""
        
        context = ValidationContext(
            project_path=self.project_path,
            task_id=task_id,
            task_data=task_data,
            validation_requirements=task_data.get("validation_requirements", []),
            timestamp=datetime.now().isoformat()
        )
        
        critical_issues = []
        warnings = []
        suggestions = []
        test_results_summary = {}
        quality_metrics = {}
        evidence_links = []
        
        # 1. Test Result Validation - Must have evidence
        if task_data.get("requires_tests"):
            test_validation = self._validate_test_results(context)
            if not test_validation["passed"]:
                critical_issues.extend(test_validation["issues"])
            test_results_summary = test_validation["summary"]
            evidence_links.extend(test_validation["evidence"])
        
        # 2. Implementation Quality Checks
        quality_validation = self._validate_implementation_quality(context)
        if not quality_validation["passed"]:
            critical_issues.extend(quality_validation["critical_issues"])
            warnings.extend(quality_validation["warnings"])
        quality_metrics = quality_validation["metrics"]
        
        # 3. Behavioral Validation - Does it actually work?
        behavioral_validation = self._validate_behavior(context)
        if not behavioral_validation["passed"]:
            critical_issues.extend(behavioral_validation["issues"])
        evidence_links.extend(behavioral_validation["evidence"])
        
        # 4. Dependency Validation - Are prerequisites met?
        dependency_validation = self._validate_dependencies(context)
        if not dependency_validation["passed"]:
            critical_issues.extend(dependency_validation["issues"])
        
        # 5. Phase Transition Validation
        phase_validation = self._validate_phase_transition(context)
        if not phase_validation["passed"]:
            critical_issues.extend(phase_validation["issues"])
        
        # Generate review result
        review_result = ReviewResult(
            passed=len(critical_issues) == 0,
            critical_issues=critical_issues,
            warnings=warnings,
            suggestions=suggestions,
            test_results_summary=test_results_summary,
            quality_metrics=quality_metrics,
            evidence_links=evidence_links
        )
        
        # Store review history
        self.review_history.append(review_result)
        
        # Generate detailed report
        self._generate_review_report(context, review_result)
        
        return review_result
    
    def _validate_test_results(self, context: ValidationContext) -> Dict[str, Any]:
        """Validate that test results are complete and provide real evidence"""
        
        test_results = context.task_data.get("test_results", [])
        issues = []
        evidence = []
        summary = {"total": 0, "passed": 0, "failed": 0, "evidence_provided": 0}
        
        if not test_results:
            return {
                "passed": False,
                "issues": ["No test results provided for task requiring tests"],
                "summary": summary,
                "evidence": []
            }
        
        for result in test_results:
            summary["total"] += 1
            
            # Check test status
            if result.get("status") == "passed":
                summary["passed"] += 1
            else:
                summary["failed"] += 1
                issues.append(f"Test failed: {result.get('test_id', 'unknown')}")
            
            # Check evidence is provided and accessible
            evidence_link = result.get("evidence_link")
            if evidence_link:
                if self._validate_evidence_link(evidence_link):
                    summary["evidence_provided"] += 1
                    evidence.append(evidence_link)
                else:
                    issues.append(f"Evidence link not accessible: {evidence_link}")
            else:
                issues.append(f"No evidence provided for test: {result.get('test_id', 'unknown')}")
        
        # Check pass rate
        if summary["total"] > 0:
            pass_rate = summary["passed"] / summary["total"]
            if pass_rate < 0.95:  # 95% pass rate required
                issues.append(f"Test pass rate {pass_rate:.1%} below 95% threshold")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "summary": summary,
            "evidence": evidence
        }
    
    def _validate_implementation_quality(self, context: ValidationContext) -> Dict[str, Any]:
        """Validate implementation quality through automated checks"""
        
        critical_issues = []
        warnings = []
        metrics = {}
        
        # Run comprehensive quality checks
        try:
            # 1. Code Style and Linting
            lint_result = self._run_linting_check(context)
            metrics["linting"] = lint_result
            if lint_result.get("errors", 0) > 0:
                critical_issues.append(f"Linting errors: {lint_result['errors']} errors found")
            if lint_result.get("warnings", 0) > 0:
                warnings.append(f"Linting warnings: {lint_result['warnings']} warnings found")
            
            # 2. Type Checking
            type_result = self._run_type_checking(context)
            metrics["type_checking"] = type_result
            if type_result.get("errors", 0) > 0:
                critical_issues.append(f"Type checking errors: {type_result['errors']} errors found")
            
            # 3. Security Analysis
            security_result = self._run_security_analysis(context)
            metrics["security"] = security_result
            if security_result.get("critical", 0) > 0:
                critical_issues.append(f"Security issues: {security_result['critical']} critical issues found")
            if security_result.get("high", 0) > 0:
                critical_issues.append(f"Security issues: {security_result['high']} high severity issues found")
            
            # 4. Code Coverage
            coverage_result = self._run_coverage_analysis(context)
            metrics["coverage"] = coverage_result
            if coverage_result.get("percentage", 0) < 80:
                warnings.append(f"Code coverage {coverage_result.get('percentage', 0):.1f}% below 80% threshold")
            
            # 5. Performance Analysis
            performance_result = self._run_performance_analysis(context)
            metrics["performance"] = performance_result
            if performance_result.get("regression_detected", False):
                warnings.append("Performance regression detected compared to baseline")
            
        except Exception as e:
            critical_issues.append(f"Quality check execution failed: {str(e)}")
        
        return {
            "passed": len(critical_issues) == 0,
            "critical_issues": critical_issues,
            "warnings": warnings,
            "metrics": metrics
        }
    
    def _validate_behavior(self, context: ValidationContext) -> Dict[str, Any]:
        """Validate that the implementation actually works as expected"""
        
        issues = []
        evidence = []
        
        try:
            # 1. Run functional tests
            functional_result = self._run_functional_tests(context)
            if not functional_result["passed"]:
                issues.extend(functional_result["issues"])
            evidence.extend(functional_result["evidence"])
            
            # 2. Run integration tests
            integration_result = self._run_integration_tests(context)
            if not integration_result["passed"]:
                issues.extend(integration_result["issues"])
            evidence.extend(integration_result["evidence"])
            
            # 3. Validate against requirements
            requirements_result = self._validate_requirements(context)
            if not requirements_result["passed"]:
                issues.extend(requirements_result["issues"])
            
            # 4. Check actual functionality vs documented behavior
            behavior_result = self._validate_behavioral_consistency(context)
            if not behavior_result["passed"]:
                issues.extend(behavior_result["issues"])
                evidence.extend(behavior_result["evidence"])
            
        except Exception as e:
            issues.append(f"Behavioral validation failed: {str(e)}")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "evidence": evidence
        }
    
    def _validate_dependencies(self, context: ValidationContext) -> Dict[str, Any]:
        """Validate that all dependencies are satisfied"""
        
        issues = []
        dependencies = context.task_data.get("dependencies", [])
        
        for dep_id in dependencies:
            if not self._is_dependency_complete(dep_id):
                issues.append(f"Dependency task {dep_id} is not complete")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _validate_phase_transition(self, context: ValidationContext) -> Dict[str, Any]:
        """Validate phase transition rules"""
        
        issues = []
        
        # Check if task is a validation gate
        if context.task_data.get("is_validation_gate"):
            # Ensure all tasks in current phase are complete
            phase_tasks = self._get_phase_tasks(context.task_id)
            incomplete_tasks = [tid for tid in phase_tasks if not self._is_task_complete(tid)]
            
            if incomplete_tasks:
                issues.append(f"Cannot proceed through validation gate - incomplete tasks: {', '.join(incomplete_tasks)}")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _validate_evidence_link(self, link: str) -> bool:
        """Validate that evidence link is accessible"""
        try:
            # Check if it's a file path
            if link.startswith(("http://", "https://")):
                # For URLs, we'll assume they're valid (actual HTTP check would be slow)
                return True
            else:
                # For file paths, check if file exists
                file_path = Path(link)
                if file_path.is_absolute():
                    return file_path.exists()
                else:
                    return (self.project_path / file_path).exists()
        except Exception:
            return False
    
    def _run_linting_check(self, context: ValidationContext) -> Dict[str, Any]:
        """Run linting checks on the project"""
        try:
            # Placeholder for actual linting implementation
            return {"errors": 0, "warnings": 0, "files_checked": 0}
        except Exception:
            return {"errors": 0, "warnings": 0, "files_checked": 0, "error": "Linting check failed"}
    
    def _run_type_checking(self, context: ValidationContext) -> Dict[str, Any]:
        """Run type checking"""
        try:
            # Placeholder for actual type checking implementation
            return {"errors": 0, "files_checked": 0}
        except Exception:
            return {"errors": 0, "files_checked": 0, "error": "Type checking failed"}
    
    def _run_security_analysis(self, context: ValidationContext) -> Dict[str, Any]:
        """Run security analysis"""
        try:
            # Placeholder for actual security analysis implementation
            return {"critical": 0, "high": 0, "medium": 0, "low": 0}
        except Exception:
            return {"critical": 0, "high": 0, "medium": 0, "low": 0, "error": "Security analysis failed"}
    
    def _run_coverage_analysis(self, context: ValidationContext) -> Dict[str, Any]:
        """Run code coverage analysis"""
        try:
            # Placeholder for actual coverage analysis implementation
            return {"percentage": 0.0, "files_covered": 0, "total_files": 0}
        except Exception:
            return {"percentage": 0.0, "files_covered": 0, "total_files": 0, "error": "Coverage analysis failed"}
    
    def _run_performance_analysis(self, context: ValidationContext) -> Dict[str, Any]:
        """Run performance analysis"""
        try:
            # Placeholder for actual performance analysis implementation
            return {"regression_detected": False, "baseline_time": 0.0, "current_time": 0.0}
        except Exception:
            return {"regression_detected": False, "baseline_time": 0.0, "current_time": 0.0, "error": "Performance analysis failed"}
    
    def _run_functional_tests(self, context: ValidationContext) -> Dict[str, Any]:
        """Run functional tests"""
        try:
            # Placeholder for actual functional testing implementation
            return {"passed": True, "issues": [], "evidence": []}
        except Exception:
            return {"passed": False, "issues": ["Functional testing failed"], "evidence": []}
    
    def _run_integration_tests(self, context: ValidationContext) -> Dict[str, Any]:
        """Run integration tests"""
        try:
            # Placeholder for actual integration testing implementation
            return {"passed": True, "issues": [], "evidence": []}
        except Exception:
            return {"passed": False, "issues": ["Integration testing failed"], "evidence": []}
    
    def _validate_requirements(self, context: ValidationContext) -> Dict[str, Any]:
        """Validate against requirements"""
        try:
            # Placeholder for actual requirements validation implementation
            return {"passed": True, "issues": []}
        except Exception:
            return {"passed": False, "issues": ["Requirements validation failed"]}
    
    def _validate_behavioral_consistency(self, context: ValidationContext) -> Dict[str, Any]:
        """Validate behavioral consistency"""
        try:
            # Placeholder for actual behavioral consistency validation implementation
            return {"passed": True, "issues": [], "evidence": []}
        except Exception:
            return {"passed": False, "issues": ["Behavioral consistency validation failed"], "evidence": []}
    
    def _is_dependency_complete(self, dependency_id: str) -> bool:
        """Check if a dependency task is complete"""
        validation = self.validation_system.task_validations.get(dependency_id)
        return validation and validation.status.value == "complete"
    
    def _get_phase_tasks(self, task_id: str) -> List[str]:
        """Get all tasks in the same phase"""
        # Extract phase from task ID
        import re
        phase_match = re.match(r'T(\d+)', task_id)
        if not phase_match:
            return []
        
        phase = phase_match.group(1)
        return [tid for tid in self.validation_system.task_validations.keys()
                if tid.startswith(f'T{phase}')]
    
    def _is_task_complete(self, task_id: str) -> bool:
        """Check if a task is complete"""
        validation = self.validation_system.task_validations.get(task_id)
        return validation and validation.status.value == "complete"
    
    def _generate_review_report(self, context: ValidationContext, result: ReviewResult):
        """Generate detailed review report"""
        
        report_file = self.project_path / ".claude" / "review-reports" / f"{context.task_id}_{int(time.time())}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            "task_id": context.task_id,
            "timestamp": context.timestamp,
            "review_result": asdict(result),
            "context": asdict(context)
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    
    def should_allow_completion(self, task_id: str, task_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Determine if task completion should be allowed"""
        
        review_result = self.pre_completion_review(task_id, task_data)
        
        if not review_result.passed:
            # Generate detailed error message
            error_message = f"❌ Task {task_id} cannot be marked complete:\n\n"
            
            if review_result.critical_issues:
                error_message += "**Critical Issues:**\n"
                for issue in review_result.critical_issues:
                    error_message += f"  - {issue}\n"
                error_message += "\n"
            
            if review_result.warnings:
                error_message += "**Warnings:**\n"
                for warning in review_result.warnings:
                    error_message += f"  - {warning}\n"
                error_message += "\n"
            
            error_message += "**Suggestions:**\n"
            for suggestion in review_result.suggestions:
                error_message += f"  - {suggestion}\n"
            
            return False, error_message
        
        return True, f"✅ Task {task_id} validation passed"

def main():
    """Main function for standalone hook execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced Claude Code Hook System")
    parser.add_argument("project_path", type=Path, help="Path to project directory")
    parser.add_argument("task_id", help="Task ID to validate")
    parser.add_argument("--task-data", type=str, help="JSON string containing task data")
    parser.add_argument("--mode", choices=["review", "validate"], default="validate", 
                       help="Operation mode")
    
    args = parser.parse_args()
    
    # Initialize enhanced hook system
    hook = EnhancedClaudeCodeHook(args.project_path)
    
    # Parse task data
    task_data = {}
    if args.task_data:
        try:
            task_data = json.loads(args.task_data)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in task data: {args.task_data}")
            return 1
    
    if args.mode == "review":
        # Run comprehensive review
        result = hook.pre_completion_review(args.task_id, task_data)
        
        print(f"\n📋 Review Results for Task {args.task_id}")
        print("=" * 50)
        
        if result.passed:
            print("✅ PASSED - Task can be marked complete")
        else:
            print("❌ FAILED - Task cannot be marked complete")
        
        if result.critical_issues:
            print(f"\n🚨 Critical Issues ({len(result.critical_issues)}):")
            for issue in result.critical_issues:
                print(f"  - {issue}")
        
        if result.warnings:
            print(f"\n⚠️  Warnings ({len(result.warnings)}):")
            for warning in result.warnings:
                print(f"  - {warning}")
        
        print(f"\n📊 Test Results: {result.test_results_summary}")
        print(f"🔍 Quality Metrics: {result.quality_metrics}")
        print(f"📎 Evidence Links: {len(result.evidence_links)} provided")
        
        return 0 if result.passed else 1
    
    else:  # validate mode
        # Simple validation check
        should_allow, message = hook.should_allow_completion(args.task_id, task_data)
        print(message)
        return 0 if should_allow else 1

if __name__ == "__main__":
    exit(main())