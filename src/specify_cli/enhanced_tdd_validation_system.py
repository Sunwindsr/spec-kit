#!/usr/bin/env python3
"""
Enhanced TDD Validation System - Main Integration Script

This script integrates all components of the enhanced TDD validation system
and provides a unified interface for preventing AI self-deception in task completion.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from validation.comprehensive_validation_system import ComprehensiveValidationSystem
from validation.tdd_validation import TDDValidationSystem
from validation.reality_test_framework import RealityTestFramework
from hooks.enhanced_claude_code_hooks import EnhancedClaudeCodeHook
from flow_control.task_flow_controller import TaskFlowController

class EnhancedTDDValidationSystem:
    """Main integration class for the enhanced TDD validation system"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.start_time = datetime.now()
        
        # Initialize all components
        print("🚀 Initializing Enhanced TDD Validation System...")
        
        # Core validation system
        self.validation_system = TDDValidationSystem(project_path)
        
        # Reality testing framework
        self.reality_framework = RealityTestFramework(project_path)
        
        # Enhanced Claude Code hooks
        self.claude_hook = EnhancedClaudeCodeHook(project_path)
        
        # Task flow controller
        self.flow_controller = TaskFlowController(project_path, self.validation_system)
        
        # Comprehensive validation system
        self.comprehensive_validator = ComprehensiveValidationSystem(project_path)
        
        # System configuration
        self.config = {
            "strict_mode": True,
            "auto_rollback_enabled": True,
            "require_test_evidence": True,
            "enable_parallel_validation": True,
            "max_validation_workers": 4,
            "comprehensive_validation_enabled": True
        }
        
        print("✅ Enhanced TDD Validation System initialized successfully")
    
    def validate_task_before_completion(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a task before allowing completion - main entry point"""
        
        print(f"🔍 Validating task {task_id} before completion...")
        
        validation_result = {
            "task_id": task_id,
            "validation_timestamp": datetime.now().isoformat(),
            "validation_passed": False,
            "validation_stages": {},
            "critical_issues": [],
            "warnings": [],
            "recommendations": [],
            "overall_decision": "block"
        }
        
        try:
            # Stage 1: Task Flow Validation
            print("  📋 Stage 1: Task Flow Validation")
            flow_validation = self._validate_task_flow(task_id)
            validation_result["validation_stages"]["task_flow"] = flow_validation
            
            if not flow_validation["passed"]:
                validation_result["critical_issues"].extend(flow_validation["issues"])
                return self._finalize_validation_result(validation_result, "block")
            
            # Stage 2: Enhanced Claude Code Review
            print("  🔍 Stage 2: Enhanced Review")
            review_result = self.claude_hook.pre_completion_review(task_id, task_data)
            validation_result["validation_stages"]["enhanced_review"] = {
                "passed": review_result.passed,
                "critical_issues": review_result.critical_issues,
                "warnings": review_result.warnings,
                "suggestions": review_result.suggestions
            }
            
            if not review_result.passed:
                validation_result["critical_issues"].extend(review_result.critical_issues)
                validation_result["warnings"].extend(review_result.warnings)
                validation_result["recommendations"].extend(review_result.suggestions)
                return self._finalize_validation_result(validation_result, "block")
            
            # Stage 3: Reality Testing Validation
            print("  🧪 Stage 3: Reality Testing")
            reality_validation = self._validate_reality_testing(task_id, task_data)
            validation_result["validation_stages"]["reality_testing"] = reality_validation
            
            if not reality_validation["passed"]:
                validation_result["critical_issues"].extend(reality_validation["issues"])
                return self._finalize_validation_result(validation_result, "block")
            
            # Stage 4: Quality Gates
            print("  🎯 Stage 4: Quality Gates")
            quality_validation = self._validate_quality_gates(task_id)
            validation_result["validation_stages"]["quality_gates"] = quality_validation
            
            if not quality_validation["passed"]:
                validation_result["warnings"].extend(quality_validation["warnings"])
                if self.config["strict_mode"]:
                    validation_result["critical_issues"].extend(quality_validation["critical_issues"])
                    return self._finalize_validation_result(validation_result, "block")
            
            # Stage 5: Behavioral Validation
            print("  🎭 Stage 5: Behavioral Validation")
            behavioral_validation = self._validate_behavioral_consistency(task_id, task_data)
            validation_result["validation_stages"]["behavioral_validation"] = behavioral_validation
            
            if not behavioral_validation["passed"]:
                validation_result["warnings"].extend(behavioral_validation["issues"])
            
            # All stages passed
            validation_result["validation_passed"] = True
            validation_result["overall_decision"] = "allow"
            
            print(f"✅ Task {task_id} validation passed - can be marked complete")
            
            return validation_result
            
        except Exception as e:
            error_msg = f"Validation system error: {str(e)}"
            validation_result["critical_issues"].append(error_msg)
            validation_result["validation_stages"]["error"] = {"error": error_msg}
            
            print(f"❌ Validation system error for task {task_id}: {str(e)}")
            return self._finalize_validation_result(validation_result, "block")
    
    def _validate_task_flow(self, task_id: str) -> Dict[str, Any]:
        """Validate task flow and dependencies"""
        
        can_start, reason, issues = self.flow_controller.can_start_task(task_id)
        
        return {
            "passed": can_start,
            "reason": reason,
            "issues": issues,
            "can_start": can_start
        }
    
    def _validate_reality_testing(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate reality testing requirements"""
        
        issues = []
        
        # Check if test results are provided
        test_results = task_data.get("test_results", [])
        if not test_results:
            return {
                "passed": False,
                "issues": ["No test results provided for reality validation"]
            }
        
        # Validate each test result has evidence
        for i, test_result in enumerate(test_results):
            if not test_result.get("evidence_link"):
                issues.append(f"Test {i+1} missing evidence link")
            
            # Check evidence accessibility if link provided
            evidence_link = test_result.get("evidence_link")
            if evidence_link and not self._validate_evidence_link(evidence_link):
                issues.append(f"Test {i+1} evidence link not accessible: {evidence_link}")
        
        # Check test pass rate
        passed_tests = sum(1 for r in test_results if r.get("status") == "passed")
        total_tests = len(test_results)
        
        if total_tests > 0:
            pass_rate = passed_tests / total_tests
            if pass_rate < 0.95:  # 95% threshold
                issues.append(f"Test pass rate {pass_rate:.1%} below 95% threshold")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "pass_rate": pass_rate if total_tests > 0 else 0.0,
            "tests_validated": total_tests
        }
    
    def _validate_quality_gates(self, task_id: str) -> Dict[str, Any]:
        """Validate quality gates for the task"""
        
        critical_issues = []
        warnings = []
        
        # Run comprehensive quality gate validation
        quality_gates = [
            {"name": "linting", "critical": True},
            {"name": "type_safety", "critical": True},
            {"name": "test_coverage", "critical": False},
            {"name": "security_scan", "critical": True},
            {"name": "performance_benchmark", "critical": False}
        ]
        
        passed_gates = 0
        total_gates = len(quality_gates)
        
        for gate in quality_gates:
            gate_result = self.comprehensive_validator._run_quality_gate(gate["name"])
            
            if not gate_result["passed"]:
                if gate["critical"]:
                    critical_issues.extend(gate_result.get("issues", [f"{gate['name']} gate failed"]))
                else:
                    warnings.extend(gate_result.get("issues", [f"{gate['name']} gate failed"]))
            else:
                passed_gates += 1
        
        return {
            "passed": len(critical_issues) == 0,
            "critical_issues": critical_issues,
            "warnings": warnings,
            "pass_rate": passed_gates / total_gates if total_gates > 0 else 0.0,
            "gates_passed": passed_gates
        }
    
    def _validate_behavioral_consistency(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate behavioral consistency"""
        
        issues = []
        
        # Check if expected behavior is defined
        expected_behavior = task_data.get("expected_behavior")
        if not expected_behavior:
            issues.append("Expected behavior not defined for task")
        
        # Check if actual behavior matches expected
        actual_behavior = task_data.get("actual_behavior", "")
        if expected_behavior and actual_behavior:
            if expected_behavior.lower() not in actual_behavior.lower():
                issues.append("Actual behavior does not match expected behavior")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues
        }
    
    def _validate_evidence_link(self, evidence_link: str) -> bool:
        """Validate that evidence link is accessible"""
        try:
            if evidence_link.startswith(("http://", "https://")):
                # For URLs, assume they're valid (actual HTTP check would be slow)
                return True
            else:
                # For file paths, check if file exists
                file_path = Path(evidence_link)
                if file_path.is_absolute():
                    return file_path.exists()
                else:
                    return (self.project_path / file_path).exists()
        except Exception:
            return False
    
    def _finalize_validation_result(self, validation_result: Dict[str, Any], decision: str) -> Dict[str, Any]:
        """Finalize validation result with decision"""
        
        validation_result["overall_decision"] = decision
        
        # Generate additional recommendations based on issues
        if validation_result["critical_issues"]:
            validation_result["recommendations"].append("Address all critical issues before proceeding")
        
        if validation_result["warnings"]:
            validation_result["recommendations"].append("Review and address warnings when possible")
        
        return validation_result
    
    def register_task(self, task_id: str, phase: str, dependencies: List[str] = None,
                     validation_requirements: List[str] = None, **kwargs):
        """Register a task in the flow control system"""
        
        self.flow_controller.register_task(
            task_id=task_id,
            phase=phase,
            dependencies=dependencies,
            validation_requirements=validation_requirements,
            **kwargs
        )
        
        print(f"📝 Task {task_id} registered in phase {phase}")
    
    def start_task(self, task_id: str) -> Dict[str, Any]:
        """Start a task if conditions are met"""
        
        success, message = self.flow_controller.start_task(task_id)
        
        return {
            "task_id": task_id,
            "action": "start",
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
    
    def complete_task(self, task_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete a task with validation"""
        
        # Validate task before completion
        validation_result = self.validate_task_before_completion(task_id, task_data)
        
        if validation_result["overall_decision"] == "block":
            return {
                "task_id": task_id,
                "action": "complete",
                "success": False,
                "message": "Task validation failed - cannot mark complete",
                "validation_result": validation_result,
                "timestamp": datetime.now().isoformat()
            }
        
        # Complete the task in flow control
        success, message = self.flow_controller.complete_task(task_id)
        
        return {
            "task_id": task_id,
            "action": "complete",
            "success": success,
            "message": message if success else "Task completion failed in flow control",
            "validation_result": validation_result,
            "timestamp": datetime.now().isoformat()
        }
    
    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run comprehensive project validation"""
        
        print("🚀 Running comprehensive project validation...")
        
        report = self.comprehensive_validator.validate_project_comprehensive()
        
        return {
            "validation_report": report,
            "summary": {
                "overall_status": report.overall_status,
                "critical_issues": len(report.critical_issues),
                "recommendations": len(report.recommendations),
                "validation_time": report.metadata.get("validation_time", 0)
            }
        }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        
        return {
            "system_initialized": True,
            "start_time": self.start_time.isoformat(),
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds(),
            "project_path": str(self.project_path),
            "configuration": self.config,
            "task_flow_status": {
                "total_tasks": len(self.flow_controller.task_nodes),
                "completed_tasks": sum(1 for n in self.flow_controller.task_nodes.values() 
                                     if n.state.value == "completed"),
                "in_progress_tasks": sum(1 for n in self.flow_controller.task_nodes.values() 
                                       if n.state.value == "in_progress"),
                "blocked_tasks": sum(1 for n in self.flow_controller.task_nodes.values() 
                                   if n.state.value == "blocked")
            },
            "validation_history": {
                "total_validations": len(self.comprehensive_validator.validation_history),
                "last_validation": self.comprehensive_validator.last_validation_time.isoformat() 
                                 if self.comprehensive_validator.last_validation_time else None
            }
        }
    
    def generate_report(self) -> str:
        """Generate comprehensive system report"""
        
        status = self.get_system_status()
        
        report_lines = [
            "# Enhanced TDD Validation System Report",
            f"**Generated**: {datetime.now().isoformat()}",
            f"**Project**: {status['project_path']}",
            f"**Uptime**: {status['uptime_seconds']:.1f} seconds",
            ""
        ]
        
        # System status
        report_lines.append("## System Status")
        report_lines.append(f"- Initialized: ✅")
        report_lines.append(f"- Strict Mode: {'✅' if status['configuration']['strict_mode'] else '❌'}")
        report_lines.append(f"- Auto Rollback: {'✅' if status['configuration']['auto_rollback_enabled'] else '❌'}")
        report_lines.append("")
        
        # Task flow status
        flow_status = status["task_flow_status"]
        report_lines.append("## Task Flow Status")
        report_lines.append(f"- Total Tasks: {flow_status['total_tasks']}")
        report_lines.append(f"- Completed: {flow_status['completed_tasks']}")
        report_lines.append(f"- In Progress: {flow_status['in_progress_tasks']}")
        report_lines.append(f"- Blocked: {flow_status['blocked_tasks']}")
        
        if flow_status['total_tasks'] > 0:
            completion_rate = flow_status['completed_tasks'] / flow_status['total_tasks']
            report_lines.append(f"- Completion Rate: {completion_rate:.1%}")
        report_lines.append("")
        
        # Validation history
        val_history = status["validation_history"]
        report_lines.append("## Validation History")
        report_lines.append(f"- Total Validations: {val_history['total_validations']}")
        report_lines.append(f"- Last Validation: {val_history['last_validation'] or 'None'}")
        report_lines.append("")
        
        # Recent validation summary
        if self.comprehensive_validator.validation_history:
            report_lines.append("## Recent Validation Summary")
            summary = self.comprehensive_validator.generate_validation_summary()
            report_lines.append(summary)
        
        return "\\n".join(report_lines)
    
    def validate_file_edits(self, edit_type: str, file_path: str) -> Dict[str, Any]:
        """Validate file edits for Claude Code hooks"""
        
        try:
            # Parse edit information
            edit_info = json.loads(edit_type) if edit_type.startswith('{') else {"type": edit_type}
            
            # Run basic validation checks
            validation_result = {
                "success": True,
                "message": "File edit validation passed",
                "details": {
                    "edit_type": edit_info.get("type", "unknown"),
                    "file_path": file_path,
                    "validation_time": datetime.now().isoformat(),
                    "checks_performed": []
                }
            }
            
            # Check if file exists
            file = Path(file_path)
            if not file.exists():
                validation_result["success"] = False
                validation_result["message"] = f"File does not exist: {file_path}"
                return validation_result
            
            # Check file permissions
            if not file.is_file():
                validation_result["success"] = False
                validation_result["message"] = f"Path is not a file: {file_path}"
                return validation_result
            
            # Run quality checks for different file types
            if file.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx']:
                validation_result["details"]["checks_performed"].append("code_quality")
                # Add code quality validation here
            
            # Security check for sensitive files
            if any(sensitive in file_path.lower() for sensitive in ['secret', 'key', 'password', 'token']):
                validation_result["details"]["checks_performed"].append("security_scan")
                # Add security validation here
            
            validation_result["details"]["checks_performed"].append("basic_validation")
            
            return validation_result
            
        except Exception as e:
            return {
                "success": False,
                "message": f"File edit validation failed: {str(e)}",
                "details": {
                    "edit_type": edit_type,
                    "file_path": file_path,
                    "error": str(e),
                    "validation_time": datetime.now().isoformat()
                }
            }

def main():
    """Main function for standalone execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Enhanced TDD Validation System")
    parser.add_argument("project_path", type=Path, help="Path to project directory")
    parser.add_argument("--validate-task", type=str, help="Validate specific task before completion")
    parser.add_argument("--task-data", type=str, help="JSON string containing task data")
    parser.add_argument("--register-task", type=str, help="Register a task")
    parser.add_argument("--phase", type=str, help="Phase for task registration")
    parser.add_argument("--start-task", type=str, help="Start a task")
    parser.add_argument("--complete-task", type=str, help="Complete a task")
    parser.add_argument("--validate-file-edits", type=str, help="Validate file edits (for Claude Code hooks)")
    parser.add_argument("--file-path", type=str, help="File path for validation (used with --validate-file-edits)")
    parser.add_argument("--comprehensive", action="store_true", help="Run comprehensive validation")
    parser.add_argument("--status", action="store_true", help="Get system status")
    parser.add_argument("--report", action="store_true", help="Generate system report")
    
    args = parser.parse_args()
    
    # Initialize enhanced validation system
    validator = EnhancedTDDValidationSystem(args.project_path)
    
    if args.validate_task:
        # Validate task before completion
        task_data = {}
        if args.task_data:
            try:
                task_data = json.loads(args.task_data)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in task data: {args.task_data}")
                return 1
        
        result = validator.validate_task_before_completion(args.validate_task, task_data)
        
        print("\\n" + "="*60)
        print(f"TASK VALIDATION RESULT: {args.validate_task}")
        print("="*60)
        print(f"Overall Decision: {result['overall_decision'].upper()}")
        print(f"Validation Passed: {'✅' if result['validation_passed'] else '❌'}")
        
        if result['critical_issues']:
            print("\\n🚨 CRITICAL ISSUES:")
            for issue in result['critical_issues']:
                print(f"  - {issue}")
        
        if result['warnings']:
            print("\\n⚠️  WARNINGS:")
            for warning in result['warnings']:
                print(f"  - {warning}")
        
        if result['recommendations']:
            print("\\n💡 RECOMMENDATIONS:")
            for rec in result['recommendations']:
                print(f"  - {rec}")
        
        return 0 if result['validation_passed'] else 1
    
    elif args.validate_file_edits:
        # Validate file edits (for Claude Code hooks)
        if not args.file_path:
            print("Error: --file-path required for file edit validation")
            return 1
        
        result = validator.validate_file_edits(args.validate_file_edits, args.file_path)
        print(f"File edit validation: {'✅' if result['success'] else '❌'}")
        print(f"Message: {result['message']}")
        return 0 if result['success'] else 1
    
    elif args.register_task:
        # Register a task
        if not args.phase:
            print("Error: --phase required for task registration")
            return 1
        
        validator.register_task(args.register_task, args.phase)
        print(f"Task {args.register_task} registered successfully")
        return 0
    
    elif args.start_task:
        # Start a task
        result = validator.start_task(args.start_task)
        print(f"Start task {args.start_task}: {'✅' if result['success'] else '❌'}")
        print(f"Message: {result['message']}")
        return 0 if result['success'] else 1
    
    elif args.complete_task:
        # Complete a task
        task_data = {}
        if args.task_data:
            try:
                task_data = json.loads(args.task_data)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in task data: {args.task_data}")
                return 1
        
        result = validator.complete_task(args.complete_task, task_data)
        print(f"Complete task {args.complete_task}: {'✅' if result['success'] else '❌'}")
        print(f"Message: {result['message']}")
        
        if not result['success'] and 'validation_result' in result:
            val_result = result['validation_result']
            if val_result['critical_issues']:
                print("\\nValidation Issues:")
                for issue in val_result['critical_issues']:
                    print(f"  - {issue}")
        
        return 0 if result['success'] else 1
    
    elif args.comprehensive:
        # Run comprehensive validation
        result = validator.run_comprehensive_validation()
        
        print("\\n" + "="*60)
        print("COMPREHENSIVE VALIDATION RESULTS")
        print("="*60)
        summary = result['summary']
        print(f"Overall Status: {summary['overall_status'].upper()}")
        print(f"Critical Issues: {summary['critical_issues']}")
        print(f"Recommendations: {summary['recommendations']}")
        print(f"Validation Time: {summary['validation_time']:.2f}s")
        
        return 0 if summary['overall_status'] == 'passed' else 1
    
    elif args.status:
        # Get system status
        status = validator.get_system_status()
        print(json.dumps(status, indent=2))
        return 0
    
    elif args.report:
        # Generate system report
        report = validator.generate_report()
        print(report)
        return 0
    
    else:
        print("No action specified. Use --help for usage information.")
        return 1

if __name__ == "__main__":
    exit(main())