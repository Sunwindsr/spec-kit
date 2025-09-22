---
description: Create refactoring implementation plan from existing specification and code analysis.
scripts:
  sh: scripts/bash/plan-refactoring.sh --json "{ARGS}"
  ps: scripts/powershell/plan-refactoring.ps1 -Json "{ARGS}"
---

The text the user typed after `/plan-refactoring` in the triggering message **is** the refactoring specification path. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that refactoring specification path, do this:

1. **Tech Stack Validation**: Before proceeding, check if user has provided technology stack information:
   - If no tech stack is mentioned in the conversation, **STOP** and ask user: "Please specify the target technology stack for the refactoring (e.g., 'React + TypeScript + Vite', 'Angular 17', 'Vue 3 + Composition API'). This is required for creating a proper refactoring plan."
   - If tech stack is provided, proceed with the plan generation
   - If user asks for recommendations, suggest: "For modern web application refactoring, I recommend: React + TypeScript + Vite + Zustand for state management + React Router for routing + React Query for data fetching. Would you like to use this stack or specify a different one?"

2. Run the script `{SCRIPT}` from repo root and parse its JSON output for ANALYSIS_RESULTS.
   **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
3. Load the refactoring specification from the provided path.
4. Load `templates/plan-refactoring-template.md` to understand required sections.
5. Perform comprehensive code analysis to understand current implementation:
   - Identify all public interfaces, APIs, and data models
   - Map current architecture and dependencies
   - Document existing behavior patterns and business logic
   - Analyze performance characteristics and bottlenecks
6. Generate refactoring plan with:
   - Incremental migration strategy
   - Behavior preservation verification approach
   - Risk assessment and mitigation strategies
   - Detailed implementation phases
7. Write the refactoring plan using the template structure.
8. Report completion with analysis results and readiness for task generation.

Key differences from standard `/plan`:
- **Code Analysis**: Deep analysis of existing implementation required
- **Behavior Mapping**: Comprehensive mapping of current behavior to ensure preservation
- **Incremental Strategy**: Phased approach to maintain system availability
- **Interface Preservation**: Detailed analysis of public interfaces that must remain stable
- **Migration Path**: Clear rollback strategy and validation approach
- **Risk Assessment**: Comprehensive risk analysis for refactoring operations