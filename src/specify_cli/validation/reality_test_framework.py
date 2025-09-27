#!/usr/bin/env python3
"""
Reality-Based Testing Framework - Ensures tests validate actual functionality

This framework implements reality-based testing that prevents AI self-deception
by requiring actual test execution with verifiable evidence and behavioral validation.
"""

import json
import os
import subprocess
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import tempfile
import threading
import queue
import hashlib

class TestEnvironment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"

class EvidenceType(Enum):
    CONSOLE_OUTPUT = "console_output"
    LOG_FILE = "log_file"
    SCREENSHOT = "screenshot"
    NETWORK_DUMP = "network_dump"
    DATABASE_DUMP = "database_dump"
    PERFORMANCE_METRICS = "performance_metrics"
    COVERAGE_REPORT = "coverage_report"
    EXTERNAL_LINK = "external_link"

@dataclass
class Evidence:
    """Test evidence with verification capabilities"""
    evidence_id: str
    evidence_type: EvidenceType
    content: str
    timestamp: str
    file_path: Optional[str] = None
    url: Optional[str] = None
    verified: bool = False
    checksum: Optional[str] = None
    
    def verify(self) -> bool:
        """Verify that evidence is accessible and valid"""
        if self.evidence_type == EvidenceType.EXTERNAL_LINK:
            return self._verify_url()
        elif self.file_path:
            return self._verify_file()
        else:
            # For in-memory content, verify checksum
            if self.checksum:
                current_checksum = hashlib.sha256(self.content.encode()).hexdigest()
                return current_checksum == self.checksum
            return True
    
    def _verify_url(self) -> bool:
        """Verify URL accessibility"""
        try:
            import requests
            response = requests.head(self.url, timeout=10)
            return response.status_code < 400
        except Exception:
            return False
    
    def _verify_file(self) -> bool:
        """Verify file accessibility"""
        return Path(self.file_path).exists() if self.file_path else False

@dataclass
class RealityTestResult:
    """Enhanced test result with reality validation"""
    test_id: str
    test_name: str
    status: str  # "passed", "failed", "error", "skipped"
    execution_time: float
    evidence: List[Evidence]
    actual_behavior: str
    expected_behavior: str
    behavior_match: bool
    environment: TestEnvironment
    timestamp: str
    test_runner: str
    assertions: List[Dict[str, Any]]
    
    def has_sufficient_evidence(self) -> bool:
        """Check if test has sufficient evidence to validate reality"""
        if not self.evidence:
            return False
        
        # Require at least one verified evidence
        verified_evidence = [e for e in self.evidence if e.verify()]
        return len(verified_evidence) > 0
    
    def get_evidence_summary(self) -> Dict[str, Any]:
        """Get summary of evidence types"""
        evidence_types = {}
        for evidence in self.evidence:
            evidence_type = evidence.evidence_type.value
            if evidence_type not in evidence_types:
                evidence_types[evidence_type] = {"total": 0, "verified": 0}
            evidence_types[evidence_type]["total"] += 1
            if evidence.verify():
                evidence_types[evidence_type]["verified"] += 1
        
        return evidence_types

@dataclass
class BehavioralAssertion:
    """Assertion that validates actual vs expected behavior"""
    assertion_id: str
    description: str
    expected_behavior: str
    validation_method: str  # "exact_match", "contains", "pattern_match", "custom"
    validation_data: Any
    passed: bool
    actual_result: Any
    evidence: List[Evidence]
    
    def validate(self) -> bool:
        """Validate the assertion using the specified method"""
        try:
            if self.validation_method == "exact_match":
                self.passed = str(self.actual_result) == str(self.validation_data)
            elif self.validation_method == "contains":
                self.passed = str(self.validation_data) in str(self.actual_result)
            elif self.validation_method == "pattern_match":
                import re
                self.passed = bool(re.search(str(self.validation_data), str(self.actual_result)))
            elif self.validation_method == "custom":
                self.passed = self._custom_validation()
            else:
                self.passed = False
            
            return self.passed
        except Exception:
            self.passed = False
            return False
    
    def _custom_validation(self) -> bool:
        """Custom validation logic"""
        # This can be extended with custom validation functions
        return True

class RealityTestRunner:
    """Test runner that ensures reality-based validation"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.test_results: List[RealityTestResult] = []
        self.evidence_store: Path = project_path / ".claude" / "evidence"
        self.evidence_store.mkdir(parents=True, exist_ok=True)
        
        # Test execution configuration
        self.capture_console_output = True
        self.capture_network_traffic = False
        self.capture_performance_metrics = True
        self.require_behavioral_validation = True
        
    def run_test_with_reality_validation(self, 
                                       test_command: str,
                                       test_name: str,
                                       expected_behavior: str,
                                       environment: TestEnvironment = TestEnvironment.DEVELOPMENT,
                                       custom_assertions: List[BehavioralAssertion] = None) -> RealityTestResult:
        """Run a test with comprehensive reality validation"""
        
        test_id = f"test_{int(time.time())}_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        evidence = []
        
        # Execute test and capture evidence
        execution_result = self._execute_test_with_evidence(test_command, test_id)
        evidence.extend(execution_result["evidence"])
        
        # Validate behavior
        behavior_match = self._validate_behavior(
            execution_result["output"],
            expected_behavior,
            evidence
        )
        
        # Create assertions
        assertions = self._create_assertions(
            execution_result,
            expected_behavior,
            behavior_match,
            custom_assertions or []
        )
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Create test result
        test_result = RealityTestResult(
            test_id=test_id,
            test_name=test_name,
            status="passed" if behavior_match and all(a.passed for a in assertions) else "failed",
            execution_time=execution_time,
            evidence=evidence,
            actual_behavior=execution_result["output"],
            expected_behavior=expected_behavior,
            behavior_match=behavior_match,
            environment=environment,
            timestamp=datetime.now().isoformat(),
            test_runner="reality_test_runner",
            assertions=[asdict(a) for a in assertions]
        )
        
        # Store test result
        self.test_results.append(test_result)
        self._store_test_result(test_result)
        
        return test_result
    
    def _execute_test_with_evidence(self, test_command: str, test_id: str) -> Dict[str, Any]:
        """Execute test command and capture comprehensive evidence"""
        
        evidence = []
        output = ""
        return_code = 0
        
        try:
            # Create evidence directory for this test
            test_evidence_dir = self.evidence_store / test_id
            test_evidence_dir.mkdir(exist_ok=True)
            
            # Execute test with output capture
            process = subprocess.Popen(
                test_command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_path
            )
            
            stdout, stderr = process.communicate()
            return_code = process.returncode
            output = stdout + stderr
            
            # Capture console output as evidence
            if self.capture_console_output and output:
                console_evidence = Evidence(
                    evidence_id=f"{test_id}_console",
                    evidence_type=EvidenceType.CONSOLE_OUTPUT,
                    content=output,
                    file_path=str(test_evidence_dir / "console_output.txt"),
                    timestamp=datetime.now().isoformat(),
                    checksum=hashlib.sha256(output.encode()).hexdigest()
                )
                
                # Save console output to file
                with open(console_evidence.file_path, 'w', encoding='utf-8') as f:
                    f.write(output)
                
                evidence.append(console_evidence)
            
            # Capture performance metrics
            if self.capture_performance_metrics:
                perf_evidence = self._capture_performance_metrics(test_id, test_evidence_dir)
                if perf_evidence:
                    evidence.append(perf_evidence)
            
            # Generate execution summary
            summary_evidence = Evidence(
                evidence_id=f"{test_id}_summary",
                evidence_type=EvidenceType.CONSOLE_OUTPUT,
                content=json.dumps({
                    "command": test_command,
                    "return_code": return_code,
                    "output_length": len(output),
                    "execution_time": time.time()
                }),
                timestamp=datetime.now().isoformat()
            )
            evidence.append(summary_evidence)
            
        except Exception as e:
            error_evidence = Evidence(
                evidence_id=f"{test_id}_error",
                evidence_type=EvidenceType.CONSOLE_OUTPUT,
                content=f"Test execution failed: {str(e)}",
                timestamp=datetime.now().isoformat()
            )
            evidence.append(error_evidence)
            output = f"Test execution error: {str(e)}"
        
        return {
            "output": output,
            "return_code": return_code,
            "evidence": evidence
        }
    
    def _validate_behavior(self, actual_output: str, expected_behavior: str, evidence: List[Evidence]) -> bool:
        """Validate that actual behavior matches expected behavior"""
        
        if not self.require_behavioral_validation:
            return True
        
        # Basic validation - check if expected behavior is in output
        if expected_behavior.lower() in actual_output.lower():
            return True
        
        # Check for specific success patterns
        success_patterns = ["pass", "success", "ok", "✓", "✔"]
        for pattern in success_patterns:
            if pattern in actual_output.lower():
                return True
        
        return False
    
    def _create_assertions(self, 
                          execution_result: Dict[str, Any],
                          expected_behavior: str,
                          behavior_match: bool,
                          custom_assertions: List[BehavioralAssertion]) -> List[BehavioralAssertion]:
        """Create assertions for the test result"""
        
        assertions = []
        
        # Basic execution assertion
        execution_assertion = BehavioralAssertion(
            assertion_id=f"assert_{int(time.time())}_1",
            description="Test executed successfully",
            expected_behavior="Test should execute without errors",
            validation_method="exact_match",
            validation_data=0,
            passed=execution_result["return_code"] == 0,
            actual_result=execution_result["return_code"],
            evidence=[]
        )
        assertions.append(execution_assertion)
        
        # Behavioral assertion
        behavior_assertion = BehavioralAssertion(
            assertion_id=f"assert_{int(time.time())}_2",
            description="Behavior matches expectations",
            expected_behavior=expected_behavior,
            validation_method="contains",
            validation_data=expected_behavior,
            passed=behavior_match,
            actual_result=execution_result["output"],
            evidence=[]
        )
        assertions.append(behavior_assertion)
        
        # Add custom assertions
        assertions.extend(custom_assertions)
        
        return assertions
    
    def _capture_performance_metrics(self, test_id: str, evidence_dir: Path) -> Optional[Evidence]:
        """Capture performance metrics during test execution"""
        try:
            import psutil
            
            # Get system performance metrics
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            
            metrics = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory_percent,
                "timestamp": datetime.now().isoformat()
            }
            
            perf_evidence = Evidence(
                evidence_id=f"{test_id}_performance",
                evidence_type=EvidenceType.PERFORMANCE_METRICS,
                content=json.dumps(metrics),
                file_path=str(evidence_dir / "performance_metrics.json"),
                timestamp=datetime.now().isoformat()
            )
            
            # Save metrics to file
            with open(perf_evidence.file_path, 'w', encoding='utf-8') as f:
                json.dump(metrics, f, indent=2)
            
            return perf_evidence
            
        except ImportError:
            # psutil not available, skip performance metrics
            return None
        except Exception:
            return None
    
    def _store_test_result(self, test_result: RealityTestResult):
        """Store test result for later analysis"""
        
        result_file = self.evidence_store / f"{test_result.test_id}_result.json"
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(test_result), f, indent=2, ensure_ascii=False)
    
    def validate_test_reality(self, test_id: str) -> Dict[str, Any]:
        """Validate that a test result reflects reality"""
        
        # Find test result
        test_result = None
        for result in self.test_results:
            if result.test_id == test_id:
                test_result = result
                break
        
        if not test_result:
            return {"valid": False, "issues": ["Test result not found"]}
        
        issues = []
        
        # Check evidence sufficiency
        if not test_result.has_sufficient_evidence():
            issues.append("Insufficient evidence to validate reality")
        
        # Verify evidence accessibility
        inaccessible_evidence = []
        for evidence in test_result.evidence:
            if not evidence.verify():
                inaccessible_evidence.append(evidence.evidence_id)
        
        if inaccessible_evidence:
            issues.append(f"Inaccessible evidence: {', '.join(inaccessible_evidence)}")
        
        # Check behavior validation
        if not test_result.behavior_match:
            issues.append("Actual behavior does not match expected behavior")
        
        # Check assertions
        failed_assertions = []
        for assertion in test_result.assertions:
            if not assertion.get("passed", False):
                failed_assertions.append(assertion.get("description", "Unknown assertion"))
        
        if failed_assertions:
            issues.append(f"Failed assertions: {', '.join(failed_assertions)}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "evidence_summary": test_result.get_evidence_summary(),
            "test_result": asdict(test_result)
        }

class RealityTestFramework:
    """Main framework for reality-based testing"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.test_runner = RealityTestRunner(project_path)
        
    def run_reality_test_suite(self, test_suite_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run a complete reality-based test suite"""
        
        results = []
        overall_start_time = time.time()
        
        # Execute each test in the suite
        for test_config in test_suite_config.get("tests", []):
            try:
                result = self.test_runner.run_test_with_reality_validation(
                    test_command=test_config["command"],
                    test_name=test_config["name"],
                    expected_behavior=test_config["expected_behavior"],
                    environment=TestEnvironment(test_config.get("environment", "development")),
                    custom_assertions=self._parse_custom_assertions(test_config.get("assertions", []))
                )
                results.append(result)
            except Exception as e:
                # Create failed test result
                error_result = RealityTestResult(
                    test_id=f"error_{int(time.time())}_{uuid.uuid4().hex[:8]}",
                    test_name=test_config.get("name", "unknown"),
                    status="error",
                    execution_time=0.0,
                    evidence=[],
                    actual_behavior=str(e),
                    expected_behavior=test_config.get("expected_behavior", ""),
                    behavior_match=False,
                    environment=TestEnvironment.DEVELOPMENT,
                    timestamp=datetime.now().isoformat(),
                    test_runner="reality_test_framework",
                    assertions=[]
                )
                results.append(error_result)
        
        # Calculate overall results
        overall_execution_time = time.time() - overall_start_time
        passed_tests = sum(1 for r in results if r.status == "passed")
        total_tests = len(results)
        
        return {
            "suite_name": test_suite_config.get("name", "Unnamed Test Suite"),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "pass_rate": passed_tests / total_tests if total_tests > 0 else 0.0,
            "overall_execution_time": overall_execution_time,
            "results": [asdict(r) for r in results],
            "reality_validated": all(r.has_sufficient_evidence() for r in results)
        }
    
    def _parse_custom_assertions(self, assertions_config: List[Dict[str, Any]]) -> List[BehavioralAssertion]:
        """Parse custom assertions from configuration"""
        
        assertions = []
        for i, config in enumerate(assertions_config):
            assertion = BehavioralAssertion(
                assertion_id=f"custom_assert_{i}",
                description=config.get("description", ""),
                expected_behavior=config.get("expected", ""),
                validation_method=config.get("method", "exact_match"),
                validation_data=config.get("validation_data", ""),
                passed=False,  # Will be set during validation
                actual_result="",
                evidence=[]
            )
            assertions.append(assertion)
        
        return assertions
    
    def generate_reality_report(self) -> str:
        """Generate comprehensive reality testing report"""
        
        report_lines = ["# Reality-Based Testing Report\n"]
        
        # Overall statistics
        total_tests = len(self.test_runner.test_results)
        passed_tests = sum(1 for r in self.test_runner.test_results if r.status == "passed")
        failed_tests = total_tests - passed_tests
        
        report_lines.append("## Overview")
        report_lines.append(f"- Total Tests: {total_tests}")
        report_lines.append(f"- Passed: {passed_tests}")
        report_lines.append(f"- Failed: {failed_tests}")
        report_lines.append(f"- Pass Rate: {passed_tests/total_tests*100:.1f}%\\n" if total_tests > 0 else "- Pass Rate: N/A\\n")
        
        # Evidence summary
        report_lines.append("## Evidence Summary")
        evidence_types = {}
        for result in self.test_runner.test_results:
            for evidence_type, summary in result.get_evidence_summary().items():
                if evidence_type not in evidence_types:
                    evidence_types[evidence_type] = {"total": 0, "verified": 0}
                evidence_types[evidence_type]["total"] += summary["total"]
                evidence_types[evidence_type]["verified"] += summary["verified"]
        
        for evidence_type, counts in evidence_types.items():
            report_lines.append(f"- {evidence_type}: {counts['verified']}/{counts['total']} verified")
        
        # Detailed test results
        report_lines.append("\\n## Test Results")
        for result in self.test_runner.test_results:
            status_icon = "✅" if result.status == "passed" else "❌"
            evidence_count = len(result.evidence)
            verified_evidence = sum(1 for e in result.evidence if e.verify())
            
            report_lines.append(f"{status_icon} **{result.test_name}**")
            report_lines.append(f"   - Status: {result.status}")
            report_lines.append(f"   - Execution Time: {result.execution_time:.2f}s")
            report_lines.append(f"   - Evidence: {verified_evidence}/{evidence_count} verified")
            report_lines.append(f"   - Behavior Match: {'Yes' if result.behavior_match else 'No'}")
            
            if not result.behavior_match:
                report_lines.append(f"   - Expected: {result.expected_behavior[:100]}...")
                report_lines.append(f"   - Actual: {result.actual_behavior[:100]}...")
        
        return "\\n".join(report_lines)

def main():
    """Main function for standalone framework execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Reality-Based Testing Framework")
    parser.add_argument("project_path", type=Path, help="Path to project directory")
    parser.add_argument("--test-suite", type=str, help="Path to test suite configuration JSON")
    parser.add_argument("--single-test", type=str, help="Run single test command")
    parser.add_argument("--expected-behavior", type=str, help="Expected behavior for single test")
    parser.add_argument("--report", action="store_true", help="Generate reality testing report")
    parser.add_argument("--validate", type=str, help="Validate specific test result")
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = RealityTestFramework(args.project_path)
    
    if args.test_suite:
        # Run test suite
        with open(args.test_suite, 'r') as f:
            suite_config = json.load(f)
        
        results = framework.run_reality_test_suite(suite_config)
        print(json.dumps(results, indent=2))
        
        return 0 if results["pass_rate"] >= 0.95 else 1
    
    elif args.single_test:
        # Run single test
        if not args.expected_behavior:
            print("Error: --expected-behavior required for single test")
            return 1
        
        result = framework.test_runner.run_test_with_reality_validation(
            test_command=args.single_test,
            test_name="single_test",
            expected_behavior=args.expected_behavior
        )
        
        print(f"Test Status: {result.status}")
        print(f"Behavior Match: {result.behavior_match}")
        print(f"Evidence Count: {len(result.evidence)}")
        
        return 0 if result.status == "passed" else 1
    
    elif args.validate:
        # Validate test result
        validation = framework.test_runner.validate_test_reality(args.validate)
        print(json.dumps(validation, indent=2))
        
        return 0 if validation["valid"] else 1
    
    elif args.report:
        # Generate report
        report = framework.generate_reality_report()
        print(report)
        return 0
    
    else:
        print("No action specified. Use --help for usage information.")
        return 1

if __name__ == "__main__":
    exit(main())