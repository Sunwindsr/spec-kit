---
description: Generate practical TDD-based refactoring tasks from refactoring plan focusing on implementation rather than theoretical validation.
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
4. Generate practical refactoring tasks using TDD methodology:
   - **Phase 1: Infrastructure Setup**: Target tech stack setup and configuration
   - **Phase 2: Data Migration**: Model definitions and type migration
   - **Phase 3: Core Implementation**: Business logic and component refactoring
   - **Phase 4: Testing & Optimization**: Comprehensive testing and performance
   - **Phase 5: Deployment**: Production deployment and monitoring
5. For each task, follow the TDD structure:
   - **RED Phase**: Write failing tests first
   - **GREEN Phase**: Implement minimal functionality to pass tests
   - **REFACTOR Phase**: Optimize and improve code quality
   - **EARS Criteria**: Clear acceptance criteria with Given-When-Then structure
6. Include practical implementation details:
   - Specific file paths and code examples
   - Realistic time estimates and resource allocation
   - Actual technology stack commands and configurations
   - Concrete testing strategies and frameworks
   - Performance benchmarks and optimization targets
7. Write the refactoring tasks using the updated template structure.
8. Report completion with task generation results and implementation readiness.

Key differences from standard `/tasks`:
- **TDD-First**: Every task follows RED-GREEN-REFACTOR structure
- **Practical Implementation**: Focus on actual code rather than theoretical validation
- **Real Technology Stack**: Use actual frameworks and tools instead of abstract concepts
- **Concrete Examples**: Provide specific code samples and configuration
- **Testing Focus**: Emphasize real testing frameworks and strategies
- **Performance Targets**: Include measurable performance goals