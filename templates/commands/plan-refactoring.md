---
description: Create refactoring implementation plan from existing specification and code analysis.
scripts:
  sh: scripts/bash/plan-refactoring.sh --json "{ARGS}"
  ps: scripts/powershell/plan-refactoring.ps1 -Json "{ARGS}"
---

The text the user typed after `/plan-refactoring` in the triggering message **is** the refactoring specification path. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that refactoring specification path, do this:

1. Run the script `{SCRIPT}` from repo root and parse its JSON output for ANALYSIS_RESULTS.
   **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
2. Load the refactoring specification from the provided path.
3. Load `templates/plan-refactoring-template.md` to understand required sections.
4. Perform comprehensive code analysis to understand current implementation:
   - Identify all public interfaces, APIs, and data models
   - Map current architecture and dependencies
   - Document existing behavior patterns and business logic
   - Analyze performance characteristics and bottlenecks
5. Generate refactoring plan with:
   - Incremental migration strategy
   - Behavior preservation verification approach
   - Risk assessment and mitigation strategies
   - Detailed implementation phases
6. Write the refactoring plan using the template structure.
7. Report completion with analysis results and readiness for task generation.

Key differences from standard `/plan`:
- **Code Analysis**: Deep analysis of existing implementation required
- **Behavior Mapping**: Comprehensive mapping of current behavior to ensure preservation
- **Incremental Strategy**: Phased approach to maintain system availability
- **Interface Preservation**: Detailed analysis of public interfaces that must remain stable
- **Migration Path**: Clear rollback strategy and validation approach
- **Risk Assessment**: Comprehensive risk analysis for refactoring operations