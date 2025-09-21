---
description: Execute refactoring tasks with behavior preservation validation and rollback capabilities.
scripts:
  sh: scripts/bash/implement-refactoring.sh --json "{ARGS}"
  ps: scripts/powershell/implement-refactoring.ps1 -Json "{ARGS}"
---

The text the user typed after `/implement-refactoring` in the triggering message **is** the refactoring tasks file path. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that refactoring tasks file path, do this:

1. Run the script `{SCRIPT}` from repo root and parse its JSON output for IMPLEMENTATION_CONFIG.
   **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
2. Load the refactoring tasks from the provided path.
3. Execute refactoring implementation with strict behavior preservation:
   - **Phase 1: Baseline Establishment**: Create comprehensive test baseline
   - **Phase 2: Incremental Implementation**: Execute tasks with verification
   - **Phase 3: Continuous Validation**: Run behavior preservation tests
   - **Phase 4: Integration Testing**: Verify system-wide behavior
   - **Phase 5: Deployment Preparation**: Prepare for safe deployment
4. For each task execution:
   - Run pre-implementation behavior tests
   - Implement changes with interface preservation
   - Run post-implementation behavior validation
   - Verify 100% behavior preservation
   - Prepare rollback procedures
5. Monitor and report on:
   - Behavior preservation metrics
   - Interface stability verification
   - Performance impact analysis
   - Risk mitigation effectiveness
6. Report completion with implementation results and deployment readiness.

Key differences from standard implementation:
- **Behavior Baseline**: Comprehensive testing before any changes
- **Continuous Validation**: Behavior testing throughout implementation
- **Interface Monitoring**: Real-time monitoring of interface stability
- **Rollback Readiness**: Immediate rollback capability for all changes
- **Performance Tracking**: Monitor performance impact of refactoring
- **Compliance Verification**: Ensure all refactoring principles are followed