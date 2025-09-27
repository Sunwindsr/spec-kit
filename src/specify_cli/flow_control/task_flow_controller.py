#!/usr/bin/env python3
"""
Task Flow Control System - Sequential Enforcement and Quality Gates

This system implements strict task flow control with sequential enforcement,
preventing AI from marking tasks complete without proper validation and ensuring
phase transitions only occur when all prerequisites are met.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue

from validation.tdd_validation import TDDValidationSystem, TaskStatus, TaskValidation, ValidationResult
from validation.reality_test_framework import RealityTestFramework, RealityTestResult

class FlowControlState(Enum):
    """States for task flow control"""
    PENDING = "pending"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class PhaseTransition(Enum):
    """Types of phase transitions"""
    SETUP_TO_TESTS = "setup_to_tests"
    TESTS_TO_IMPLEMENTATION = "tests_to_implementation"
    IMPLEMENTATION_TO_INTEGRATION = "implementation_to_integration"
    INTEGRATION_TO_POLISH = "integration_to_polish"
    POLISH_TO_DEPLOYMENT = "polish_to_deployment"

@dataclass
class FlowControlDecision:
    """Decision made by the flow control system"""
    decision_id: str
    task_id: str
    action: str  # "allow", "block", "rollback", "require_validation"
    reason: str
    conditions_met: List[str]
    conditions_failed: List[str]
    timestamp: str
    made_by: str  # "system", "human", "automated_validation"
    
@dataclass
class PhaseGate:
    """Gate that controls phase transitions"""
    gate_id: str
    from_phase: str
    to_phase: str
    conditions: List[str]
    validation_required: bool
    auto_rollback: bool
    strict_mode: bool
    created_at: str
    
@dataclass
class TaskFlowNode:
    """Node in the task flow graph"""
    task_id: str
    state: FlowControlState
    phase: str
    dependencies: List[str]
    dependents: List[str]
    validation_requirements: List[str]
    quality_gates: List[str]
    is_validation_gate: bool
    start_time: Optional[str] = None
    completion_time: Optional[str] = None
    
@dataclass
class FlowExecutionLog:
    """Log of flow control decisions and actions"""
    log_id: str
    timestamp: str
    task_id: str
    action: str
    details: Dict[str, Any]
    result: str
    reason: str

class TaskFlowController:
    """Controls task flow with sequential enforcement and quality gates"""
    
    def __init__(self, project_path: Path, validation_system: TDDValidationSystem):
        self.project_path = project_path
        self.validation_system = validation_system
        self.reality_framework = RealityTestFramework(project_path)
        
        # Flow control state
        self.task_nodes: Dict[str, TaskFlowNode] = {}
        self.phase_gates: Dict[str, PhaseGate] = {}
        self.execution_log: List[FlowExecutionLog] = []
        self.flow_decisions: List[FlowControlDecision] = []
        
        # Configuration
        self.strict_mode = True
        self.auto_rollback_enabled = True
        self.concurrent_task_limit = 4
        self.currently_running = set()
        
        # Thread-safe execution
        self.execution_lock = threading.Lock()
        self.decision_queue = queue.Queue()
        
        # Initialize phase gates
        self._initialize_phase_gates()
    
    def _initialize_phase_gates(self):
        """Initialize phase transition gates"""
        
        gates = [
            PhaseGate(
                gate_id="setup_tests_gate",
                from_phase="setup",
                to_phase="tests",
                conditions=[
                    "all_setup_tasks_complete",
                    "development_environment_ready",
                    "linting_configured"
                ],
                validation_required=True,
                auto_rollback=True,
                strict_mode=True,
                created_at=datetime.now().isoformat()
            ),
            PhaseGate(
                gate_id="tests_implementation_gate",
                from_phase="tests",
                to_phase="implementation",
                conditions=[
                    "all_tests_written",
                    "all_tests_failing_initially",
                    "test_evidence_recorded",
                    "contract_tests_valid"
                ],
                validation_required=True,
                auto_rollback=True,
                strict_mode=True,
                created_at=datetime.now().isoformat()
            ),
            PhaseGate(
                gate_id="implementation_integration_gate",
                from_phase="implementation",
                to_phase="integration",
                conditions=[
                    "all_implementation_tasks_complete",
                    "all_tests_passing",
                    "quality_gates_passed",
                    "behavioral_validation_passed"
                ],
                validation_required=True,
                auto_rollback=True,
                strict_mode=True,
                created_at=datetime.now().isoformat()
            ),
            PhaseGate(
                gate_id="integration_polish_gate",
                from_phase="integration",
                to_phase="polish",
                conditions=[
                    "all_integration_tasks_complete",
                    "performance_baseline_met",
                    "security_scan_passed",
                    "documentation_updated"
                ],
                validation_required=True,
                auto_rollback=False,
                strict_mode=False,
                created_at=datetime.now().isoformat()
            ),
            PhaseGate(
                gate_id="polish_deployment_gate",
                from_phase="polish",
                to_phase="deployment",
                conditions=[
                    "all_polish_tasks_complete",
                    "user_acceptance_tests_passed",
                    "deployment_ready",
                    "rollback_plan_in_place"
                ],
                validation_required=True,
                auto_rollback=False,
                strict_mode=True,
                created_at=datetime.now().isoformat()
            )
        ]
        
        for gate in gates:
            self.phase_gates[gate.gate_id] = gate
    
    def register_task(self, task_id: str, phase: str, dependencies: List[str] = None,
                     validation_requirements: List[str] = None, is_validation_gate: bool = False):
        """Register a task in the flow control system"""
        
        with self.execution_lock:
            self.task_nodes[task_id] = TaskFlowNode(
                task_id=task_id,
                state=FlowControlState.PENDING,
                phase=phase,
                dependencies=dependencies or [],
                dependents=[],
                validation_requirements=validation_requirements or [],
                quality_gates=[],
                is_validation_gate=is_validation_gate
            )
            
            # Update dependency relationships
            for dep_id in self.task_nodes[task_id].dependencies:
                if dep_id in self.task_nodes:
                    self.task_nodes[dep_id].dependents.append(task_id)
            
            self._log_action(
                task_id=task_id,
                action="register_task",
                details={
                    "phase": phase,
                    "dependencies": dependencies,
                    "validation_requirements": validation_requirements,
                    "is_validation_gate": is_validation_gate
                },
                result="success",
                reason="Task registered in flow control system"
            )
    
    def can_start_task(self, task_id: str) -> Tuple[bool, str, List[str]]:
        """Check if a task can be started"""
        
        if task_id not in self.task_nodes:
            return False, "Task not registered in flow control system", []
        
        node = self.task_nodes[task_id]
        
        # Check if task is already running
        if node.state == FlowControlState.IN_PROGRESS:
            return False, "Task is already in progress", []
        
        # Check if task is completed
        if node.state == FlowControlState.COMPLETED:
            return False, "Task is already completed", []
        
        # Check concurrent task limit
        if len(self.currently_running) >= self.concurrent_task_limit:
            return False, f"Concurrent task limit ({self.concurrent_task_limit}) reached", []
        
        # Check dependencies
        unmet_dependencies = []
        for dep_id in node.dependencies:
            if dep_id not in self.task_nodes:
                unmet_dependencies.append(f"Dependency {dep_id} not found")
            elif self.task_nodes[dep_id].state != FlowControlState.COMPLETED:
                unmet_dependencies.append(f"Dependency {dep_id} not completed")
        
        if unmet_dependencies:
            return False, "Dependencies not met", unmet_dependencies
        
        # Check if blocked
        if node.state == FlowControlState.BLOCKED:
            return False, "Task is blocked", ["Task state is blocked"]
        
        # Check phase gate conditions
        phase_gate_check = self._check_phase_gate_for_task(task_id)
        if not phase_gate_check["allowed"]:
            return False, "Phase gate conditions not met", phase_gate_check["issues"]
        
        return True, "Task can be started", []
    
    def start_task(self, task_id: str) -> Tuple[bool, str]:
        """Start a task if conditions are met"""
        
        can_start, reason, issues = self.can_start_task(task_id)
        if not can_start:
            decision = FlowControlDecision(
                decision_id=f"start_{task_id}_{int(time.time())}",
                task_id=task_id,
                action="block",
                reason=reason,
                conditions_met=[],
                conditions_failed=issues,
                timestamp=datetime.now().isoformat(),
                made_by="system"
            )
            self.flow_decisions.append(decision)
            return False, reason
        
        with self.execution_lock:
            node = self.task_nodes[task_id]
            node.state = FlowControlState.IN_PROGRESS
            node.start_time = datetime.now().isoformat()
            self.currently_running.add(task_id)
        
        decision = FlowControlDecision(
            decision_id=f"start_{task_id}_{int(time.time())}",
            task_id=task_id,
            action="allow",
            reason="Task started successfully",
            conditions_met=["dependencies_met", "phase_gate_clear", "concurrent_limit_ok"],
            conditions_failed=[],
            timestamp=datetime.now().isoformat(),
            made_by="system"
        )
        self.flow_decisions.append(decision)
        
        self._log_action(
            task_id=task_id,
            action="start_task",
            details={"start_time": node.start_time},
            result="success",
            reason="Task started"
        )
        
        return True, "Task started successfully"
    
    def complete_task(self, task_id: str, test_results: List[RealityTestResult] = None) -> Tuple[bool, str]:
        """Complete a task with validation"""
        
        if task_id not in self.task_nodes:
            return False, "Task not registered in flow control system"
        
        node = self.task_nodes[task_id]
        
        # Check if task is in progress
        if node.state != FlowControlState.IN_PROGRESS:
            return False, f"Task is not in progress (current state: {node.state.value})"
        
        # Validate task completion
        validation_result = self._validate_task_completion(task_id, test_results)
        
        if not validation_result["passed"]:
            # Handle validation failure
            if self.auto_rollback_enabled and self.strict_mode:
                self._rollback_task(task_id)
                decision = FlowControlDecision(
                    decision_id=f"complete_{task_id}_{int(time.time())}",
                    task_id=task_id,
                    action="rollback",
                    reason="Validation failed - auto-rollback triggered",
                    conditions_met=[],
                    conditions_failed=validation_result["issues"],
                    timestamp=datetime.now().isoformat(),
                    made_by="system"
                )
                self.flow_decisions.append(decision)
                return False, "Task validation failed - rollback triggered"
            else:
                decision = FlowControlDecision(
                    decision_id=f"complete_{task_id}_{int(time.time())}",
                    task_id=task_id,
                    action="block",
                    reason="Validation failed",
                    conditions_met=[],
                    conditions_failed=validation_result["issues"],
                    timestamp=datetime.now().isoformat(),
                    made_by="system"
                )
                self.flow_decisions.append(decision)
                return False, f"Task validation failed: {validation_result['issues'][0]}"
        
        # Mark task as completed
        with self.execution_lock:
            node.state = FlowControlState.COMPLETED
            node.completion_time = datetime.now().isoformat()
            self.currently_running.remove(task_id)
        
        decision = FlowControlDecision(
            decision_id=f"complete_{task_id}_{int(time.time())}",
            task_id=task_id,
            action="allow",
            reason="Task completed successfully",
            conditions_met=validation_result["conditions_met"],
            conditions_failed=[],
            timestamp=datetime.now().isoformat(),
            made_by="system"
        )
        self.flow_decisions.append(decision)
        
        self._log_action(
            task_id=task_id,
            action="complete_task",
            details={
                "completion_time": node.completion_time,
                "validation_result": validation_result
            },
            result="success",
            reason="Task completed with validation"
        )
        
        # Update dependent tasks
        self._update_dependent_tasks(task_id)
        
        # Check phase transitions
        self._check_phase_transitions()
        
        return True, "Task completed successfully"
    
    def _validate_task_completion(self, task_id: str, test_results: List[RealityTestResult] = None) -> Dict[str, Any]:
        """Validate that a task can be completed"""
        
        node = self.task_nodes[task_id]
        issues = []
        conditions_met = []
        
        # Check validation requirements
        for requirement in node.validation_requirements:
            if requirement == "test_results":
                if not test_results:
                    issues.append("Test results required but none provided")
                else:
                    # Validate test results
                    passed_tests = sum(1 for r in test_results if r.status == "passed")
                    total_tests = len(test_results)
                    
                    if total_tests == 0:
                        issues.append("No test results provided")
                    else:
                        pass_rate = passed_tests / total_tests
                        if pass_rate < 0.95:  # 95% pass rate required
                            issues.append(f"Test pass rate {pass_rate:.1%} below 95% threshold")
                        else:
                            conditions_met.append("test_results_sufficient")
            
            elif requirement == "quality_gates":
                # Run quality checks
                quality_result = self._run_quality_checks(task_id)
                if not quality_result["passed"]:
                    issues.extend(quality_result["issues"])
                else:
                    conditions_met.append("quality_gates_passed")
            
            elif requirement == "behavioral_validation":
                # Validate behavior matches expectations
                behavior_result = self._validate_behavior(task_id)
                if not behavior_result["passed"]:
                    issues.extend(behavior_result["issues"])
                else:
                    conditions_met.append("behavioral_validation_passed")
        
        # Check if task is a validation gate
        if node.is_validation_gate:
            gate_result = self._validate_gate_task(task_id)
            if not gate_result["passed"]:
                issues.extend(gate_result["issues"])
            else:
                conditions_met.append("validation_gate_passed")
        
        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "conditions_met": conditions_met
        }
    
    def _run_quality_checks(self, task_id: str) -> Dict[str, Any]:
        """Run quality checks for a task"""
        # Placeholder for actual quality check implementation
        return {
            "passed": True,
            "issues": []
        }
    
    def _validate_behavior(self, task_id: str) -> Dict[str, Any]:
        """Validate behavior for a task"""
        # Placeholder for actual behavior validation implementation
        return {
            "passed": True,
            "issues": []
        }
    
    def _validate_gate_task(self, task_id: str) -> Dict[str, Any]:
        """Validate a gate task"""
        node = self.task_nodes[task_id]
        
        # Check if all tasks in the phase are complete
        phase_tasks = [tid for tid, n in self.task_nodes.items() 
                       if n.phase == node.phase and tid != task_id]
        
        incomplete_tasks = [tid for tid in phase_tasks 
                          if self.task_nodes[tid].state != FlowControlState.COMPLETED]
        
        if incomplete_tasks:
            return {
                "passed": False,
                "issues": [f"Incomplete tasks in phase: {', '.join(incomplete_tasks)}"]
            }
        
        return {
            "passed": True,
            "issues": []
        }
    
    def _rollback_task(self, task_id: str):
        """Rollback a task to its previous state"""
        
        node = self.task_nodes[task_id]
        
        with self.execution_lock:
            node.state = FlowControlState.ROLLED_BACK
            if task_id in self.currently_running:
                self.currently_running.remove(task_id)
        
        self._log_action(
            task_id=task_id,
            action="rollback_task",
            details={
                "previous_state": node.state.value,
                "reason": "validation_failure"
            },
            result="success",
            reason="Task rolled back due to validation failure"
        )
    
    def _update_dependent_tasks(self, task_id: str):
        """Update the status of dependent tasks"""
        
        node = self.task_nodes[task_id]
        
        for dep_id in node.dependents:
            if dep_id in self.task_nodes:
                dep_node = self.task_nodes[dep_id]
                
                # Check if dependent task can now be started
                can_start, _, _ = self.can_start_task(dep_id)
                if can_start and dep_node.state == FlowControlState.PENDING:
                    dep_node.state = FlowControlState.READY
                    
                    self._log_action(
                        task_id=dep_id,
                        action="update_dependent_task",
                        details={
                            "trigger_task": task_id,
                            "new_state": "ready"
                        },
                        result="success",
                        reason="Dependencies met, task ready to start"
                    )
    
    def _check_phase_transitions(self):
        """Check if any phase transitions can occur"""
        
        for gate_id, gate in self.phase_gates.items():
            if self._can_transition_through_gate(gate):
                self._execute_phase_transition(gate)
    
    def _can_transition_through_gate(self, gate: PhaseGate) -> bool:
        """Check if a phase transition can occur"""
        
        # Find all tasks in the from_phase
        phase_tasks = [n for n in self.task_nodes.values() 
                       if n.phase == gate.from_phase]
        
        # Check if all tasks in the from_phase are complete
        incomplete_tasks = [n for n in phase_tasks 
                          if n.state != FlowControlState.COMPLETED]
        
        if incomplete_tasks:
            return False
        
        # Check gate-specific conditions
        for condition in gate.conditions:
            if not self._check_gate_condition(condition):
                return False
        
        return True
    
    def _check_gate_condition(self, condition: str) -> bool:
        """Check a specific gate condition"""
        # Placeholder for actual condition checking
        # This would be implemented based on specific project requirements
        return True
    
    def _execute_phase_transition(self, gate: PhaseGate):
        """Execute a phase transition"""
        
        self._log_action(
            task_id=f"phase_transition_{gate.gate_id}",
            action="phase_transition",
            details={
                "from_phase": gate.from_phase,
                "to_phase": gate.to_phase,
                "gate_id": gate.gate_id
            },
            result="success",
            reason=f"Transitioned from {gate.from_phase} to {gate.to_phase}"
        )
    
    def _check_phase_gate_for_task(self, task_id: str) -> Dict[str, Any]:
        """Check phase gate conditions for a specific task"""
        
        node = self.task_nodes[task_id]
        
        # Find the appropriate gate for this task's phase
        for gate in self.phase_gates.values():
            if gate.to_phase == node.phase:
                # Check if gate conditions are met
                if not self._can_transition_through_gate(gate):
                    return {
                        "allowed": False,
                        "issues": [f"Phase gate {gate.gate_id} conditions not met"]
                    }
        
        return {
            "allowed": True,
            "issues": []
        }
    
    def _log_action(self, task_id: str, action: str, details: Dict[str, Any], 
                   result: str, reason: str):
        """Log a flow control action"""
        
        log_entry = FlowExecutionLog(
            log_id=f"log_{int(time.time())}_{task_id}",
            timestamp=datetime.now().isoformat(),
            task_id=task_id,
            action=action,
            details=details,
            result=result,
            reason=reason
        )
        
        self.execution_log.append(log_entry)
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get the current status of a task"""
        
        if task_id not in self.task_nodes:
            return None
        
        node = self.task_nodes[task_id]
        
        return {
            "task_id": task_id,
            "state": node.state.value,
            "phase": node.phase,
            "dependencies": node.dependencies,
            "dependents": node.dependents,
            "validation_requirements": node.validation_requirements,
            "is_validation_gate": node.is_validation_gate,
            "start_time": node.start_time,
            "completion_time": node.completion_time,
            "can_start": self.can_start_task(task_id)[0]
        }
    
    def get_phase_status(self, phase: str) -> Dict[str, Any]:
        """Get the status of all tasks in a phase"""
        
        phase_tasks = [n for n in self.task_nodes.values() if n.phase == phase]
        
        total_tasks = len(phase_tasks)
        completed_tasks = sum(1 for n in phase_tasks if n.state == FlowControlState.COMPLETED)
        in_progress_tasks = sum(1 for n in phase_tasks if n.state == FlowControlState.IN_PROGRESS)
        blocked_tasks = sum(1 for n in phase_tasks if n.state == FlowControlState.BLOCKED)
        
        return {
            "phase": phase,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "in_progress_tasks": in_progress_tasks,
            "blocked_tasks": blocked_tasks,
            "completion_rate": completed_tasks / total_tasks if total_tasks > 0 else 0.0,
            "can_transition_to_next_phase": self._can_transition_from_phase(phase)
        }
    
    def _can_transition_from_phase(self, phase: str) -> bool:
        """Check if tasks can transition from this phase"""
        
        for gate in self.phase_gates.values():
            if gate.from_phase == phase:
                return self._can_transition_through_gate(gate)
        
        return True  # No gate defined, assume transition is allowed
    
    def generate_flow_report(self) -> str:
        """Generate comprehensive flow control report"""
        
        report_lines = ["# Task Flow Control Report\\n"]
        
        # Overall statistics
        total_tasks = len(self.task_nodes)
        completed_tasks = sum(1 for n in self.task_nodes.values() if n.state == FlowControlState.COMPLETED)
        in_progress_tasks = sum(1 for n in self.task_nodes.values() if n.state == FlowControlState.IN_PROGRESS)
        blocked_tasks = sum(1 for n in self.task_nodes.values() if n.state == FlowControlState.BLOCKED)
        
        report_lines.append("## Overview")
        report_lines.append(f"- Total Tasks: {total_tasks}")
        report_lines.append(f"- Completed: {completed_tasks}")
        report_lines.append(f"- In Progress: {in_progress_tasks}")
        report_lines.append(f"- Blocked: {blocked_tasks}")
        report_lines.append(f"- Completion Rate: {completed_tasks/total_tasks*100:.1f}%\\n" if total_tasks > 0 else "- Completion Rate: N/A\\n")
        
        # Phase status
        phases = set(n.phase for n in self.task_nodes.values())
        report_lines.append("## Phase Status")
        for phase in sorted(phases):
            phase_status = self.get_phase_status(phase)
            report_lines.append(f"### {phase.title()}")
            report_lines.append(f"- Completion Rate: {phase_status['completion_rate']:.1%}")
            report_lines.append(f"- Can Transition: {'Yes' if phase_status['can_transition_to_next_phase'] else 'No'}")
            report_lines.append("")
        
        # Recent decisions
        report_lines.append("## Recent Flow Control Decisions")
        recent_decisions = self.flow_decisions[-10:]  # Last 10 decisions
        for decision in recent_decisions:
            status_icon = "✅" if decision.action == "allow" else "🚫"
            report_lines.append(f"{status_icon} **{decision.task_id}**: {decision.action}")
            report_lines.append(f"   - Reason: {decision.reason}")
            report_lines.append(f"   - Made by: {decision.made_by}")
            report_lines.append("")
        
        return "\\n".join(report_lines)

def main():
    """Main function for standalone flow control execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Task Flow Control System")
    parser.add_argument("project_path", type=Path, help="Path to project directory")
    parser.add_argument("--register-task", type=str, help="Register a task")
    parser.add_argument("--phase", type=str, help="Phase for task registration")
    parser.add_argument("--dependencies", type=str, help="Comma-separated dependencies")
    parser.add_argument("--start-task", type=str, help="Start a task")
    parser.add_argument("--complete-task", type=str, help="Complete a task")
    parser.add_argument("--status", type=str, help="Get task status")
    parser.add_argument("--phase-status", type=str, help="Get phase status")
    parser.add_argument("--report", action="store_true", help="Generate flow report")
    
    args = parser.parse_args()
    
    # Initialize flow control system
    validation_system = TDDValidationSystem(args.project_path)
    flow_controller = TaskFlowController(args.project_path, validation_system)
    
    if args.register_task:
        if not args.phase:
            print("Error: --phase required for task registration")
            return 1
        
        dependencies = args.dependencies.split(",") if args.dependencies else []
        flow_controller.register_task(args.register_task, args.phase, dependencies)
        print(f"Task {args.register_task} registered in phase {args.phase}")
        return 0
    
    elif args.start_task:
        success, message = flow_controller.start_task(args.start_task)
        print(f"Start task {args.start_task}: {message}")
        return 0 if success else 1
    
    elif args.complete_task:
        success, message = flow_controller.complete_task(args.complete_task)
        print(f"Complete task {args.complete_task}: {message}")
        return 0 if success else 1
    
    elif args.status:
        status = flow_controller.get_task_status(args.status)
        if status:
            print(json.dumps(status, indent=2))
            return 0
        else:
            print(f"Task {args.status} not found")
            return 1
    
    elif args.phase_status:
        phase_status = flow_controller.get_phase_status(args.phase_status)
        print(json.dumps(phase_status, indent=2))
        return 0
    
    elif args.report:
        report = flow_controller.generate_flow_report()
        print(report)
        return 0
    
    else:
        print("No action specified. Use --help for usage information.")
        return 1

if __name__ == "__main__":
    exit(main())