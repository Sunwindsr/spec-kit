---
description: Generate detailed refactoring tasks from refactoring plan with behavior preservation verification.
scripts:
  sh: scripts/bash/tasks-refactoring.sh --json "{ARGS}"
  ps: scripts/powershell/tasks-refactoring.ps1 -Json "{ARGS}"
---

The text the user typed after `/tasks-refactoring` in the triggering message **is** the refactoring plan path. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that refactoring plan path, do this:

1. Run the script `{SCRIPT}` from repo root and parse its JSON output for TASKS_CONFIG.
   **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
2. Load the refactoring plan from the provided path.
3. Load `templates/tasks-refactoring-template.md` to understand required sections.
4. Generate comprehensive refactoring tasks:
   - **Phase 1: Behavior Documentation**: Document current behavior with comprehensive tests
   - **Phase 2: Interface Analysis**: Identify and document all stable interfaces
   - **Phase 3: Incremental Implementation**: Create tasks for safe, incremental changes
   - **Phase 4: Validation & Testing**: Comprehensive verification tasks
   - **Phase 5: Migration & Rollback**: Safe deployment and rollback procedures
5. For each task, include:
   - Behavior preservation requirements
   - Interface stability constraints
   - Testing and validation steps
   - Risk mitigation measures
   - Rollback procedures
6. Write the refactoring tasks using the template structure.
7. Report completion with task generation results and implementation readiness.

Key differences from standard `/tasks`:
- **Behavior-First**: Start with comprehensive behavior documentation before any changes
- **Interface Stability**: Tasks must preserve all public interfaces
- **Incremental Safety**: Each task must be independently safe and reversible
- **Validation Focus**: Heavy emphasis on testing and verification
- **Rollback Planning**: Each task includes rollback procedures
- **Risk Mitigation**: Comprehensive risk analysis for each task