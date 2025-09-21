---
description: Create or update the refactoring constitution with predefined refactoring principles and constraints.
scripts:
  sh: scripts/bash/constitution-refactoring.sh --json "{ARGS}"
  ps: scripts/powershell/constitution-refactoring.ps1 -Json "{ARGS}"
---

The text the user typed after `/constitution-refactoring` in the triggering message **is** the additional refactoring requirements. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that additional refactoring requirements, do this:

1. Run the script `{SCRIPT}` from repo root and parse its JSON output for CONSTITUTION_FILE.
   **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
2. Load the refactoring constitution template with predefined refactoring principles.
3. Apply the user's additional requirements to customize the constitution.
4. Write the refactoring constitution to CONSTITUTION_FILE.
5. Propagate any refactoring-specific constraints to dependent templates.
6. Report completion with constitution file path and any template sync requirements.

Key differences from standard `/constitution`:
- **Predefined Principles**: Comes with refactoring-specific principles pre-filled
- **Behavior Preservation**: Core focus on maintaining 100% behavior preservation
- **Interface Stability**: Strict constraints on public interface stability
- **Incremental Migration**: Principles for safe, incremental refactoring approach
- **Risk Mitigation**: Built-in risk assessment and mitigation requirements
- **Validation Requirements**: Comprehensive testing and validation principles