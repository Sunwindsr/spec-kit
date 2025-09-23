---
description: Create or update the refactoring specification from existing code analysis.
scripts:
  sh: scripts/bash/create-new-feature-refactoring.sh --json --path --feature-name "<extracted-feature-name>" --target "{ARGS}"
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

2. **Automatic Refactoring Constitution Setup**: Create the refactoring constitution file if it doesn't exist:
   - Copy `templates/constitution-refactoring-template.md` to `/memory/constitution-refactoring.md`
   - Update the constitution date to today's date
   - This ensures all refactoring activities follow the predefined 20 core principles

3. Run the script `{SCRIPT}` from repo root and parse its JSON output for BRANCH_NAME and SPEC_FILE. All file paths must be absolute.
   **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.

4. Load `templates/spec-refactoring-template.md` to understand required sections.
5. Analyze the existing codebase to understand current behavior and interfaces.
6. **IMPORTANT**: Extract and document user stories and business value from the existing code:
   - Identify user types who interact with the system
   - Document the key user journeys and business value
   - Create EARS format requirements for business-critical behaviors
   - Use REQ-001, REQ-002, etc. for business requirements (not just RF-001 for refactoring)
   - **CRITICAL**: Extract and document all RESTful API endpoints with exact HTTP methods and URL patterns
   - **MANDATORY**: Extract and document exact data models from source code:
     - Find all interface/class definitions (AppFileDTO, CommentDTO, FavoriteDTO, etc.)
     - Document exact field names, types, and relationships from actual TypeScript files
     - Include all properties, validation rules, and default values from source
     - Verify data models match actual API responses and component usage
     - **严禁基于假设创建数据模型** - 必须从源代码精确提取

7. **PHASE 0: CONTRACT-FIRST EXTRACTION** (MANDATORY - 刚性前提条件):
   ```bash
   # Contract-First: 接口、数据模型先行 - 这是重构的专门阶段和刚性前提
   python3 scripts/extract-code-definitions.py --source [SOURCE_PROJECT_PATH] --output phase0-contracts.md
   ```
   - **Contract Validation**: 验证提取的contracts完整性和准确性
   - **Contract Immutability**: 提取的contracts成为不可变更的基准，后续所有阶段必须严格遵循
   - **Use ONLY Phase 0 Contracts**: 后续所有组件实现只能使用Phase 0提取的contracts，严禁自行定义
   - **Validation Failure**: 如果contract提取失败，整个重构过程立即终止
   - **CONSTITUTION VIOLATION**: 违反Contract-First原则将导致立即回滚到Phase 0重新开始

8. Write the refactoring specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived **ONLY** from the code extraction results while preserving section order and headings.
9. Report completion with branch name, spec file path, and readiness for the next phase.

Note: The script creates and checks out the new branch and initializes the spec file before writing.

Key differences from standard `/specify`:
- **Input Analysis**: Instead of user description, analyze existing codebase
- **Behavior Preservation**: All specifications must maintain 100% backward compatibility
- **Interface Stability**: Public APIs, UI components, and data models must remain unchanged
- **Migration Strategy**: Include incremental migration approach for zero-downtime refactoring
- **Validation Requirements**: Comprehensive testing to ensure behavior preservation