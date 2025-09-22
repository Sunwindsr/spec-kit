---
description: Create or update the refactoring specification from existing code analysis.
scripts:
  sh: scripts/bash/create-new-feature-refactoring.sh --json --path --feature-name "<extracted-feature-name>" "{ARGS}"
  ps: scripts/powershell/create-new-feature-refactoring.ps1 -Json -Path -FeatureName "<extracted-feature-name>" "{ARGS}"
---

The text the user typed after `/specify-refactoring` in the triggering message **is** the target system description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that target system description, do this:

1. **Feature Name Extraction**: Extract a meaningful feature name from the target path:
   - Extract the core system/module identifier from the path or description
   - For paths like "/home/sd_dev/projects/business-management/frontend/ClientApp/src/app/Entrances/Frontend/ViewsEntrance/BizModules/ViewAppFilesBiz", extract "ViewAppFilesBiz" as the core component
   - Remove generic prefixes like "src", "app", "frontend" and focus on the business module
   - Generate a clean, kebab-case feature name (2-5 words)
   - Examples: "view-app-files-biz", "file-viewer-component", "payment-service", "data-access-layer"

2. Run the script `{SCRIPT}` from repo root and parse its JSON output for BRANCH_NAME and SPEC_FILE. All file paths must be absolute.
   **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

3. Load `templates/spec-refactoring-template.md` to understand required sections.
4. Analyze the existing codebase to understand current behavior and interfaces.
5. Write the refactoring specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the code analysis while preserving section order and headings.
6. Report completion with branch name, spec file path, and readiness for the next phase.

Note: The script creates and checks out the new branch and initializes the spec file before writing.

Key differences from standard `/specify`:
- **Input Analysis**: Instead of user description, analyze existing codebase
- **Behavior Preservation**: All specifications must maintain 100% backward compatibility
- **Interface Stability**: Public APIs, UI components, and data models must remain unchanged
- **Migration Strategy**: Include incremental migration approach for zero-downtime refactoring
- **Validation Requirements**: Comprehensive testing to ensure behavior preservation