---
description: Create or update the feature specification from a natural language feature description.
scripts:
  sh: scripts/bash/create-new-feature.sh --json "{ARGS}"
  ps: scripts/powershell/create-new-feature.ps1 -Json "{ARGS}"
---

The text the user typed after `/specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. Run the script `{SCRIPT}` from repo root and parse its JSON output for BRANCH_NAME and SPEC_FILE. All file paths must be absolute.
  **IMPORTANT** You must only ever run this script once. The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for.
2. Load `templates/spec-template.md` to understand required sections.
3. **IMPORTANT**: Generate structured EARS format requirements and user stories:
   - Extract user types, actions, and business value from the feature description
   - Create user stories using "As a [user type], I want to [action], so that [benefit]" format
   - Generate EARS requirements using When-Then, In Context, Event-Response, and Always templates
   - Use REQ-001, REQ-002, etc. for business requirements and FR-001, FR-002, etc. for functional requirements

4. **Create supporting documentation**:
   ```bash
   # 数据模型文档
   cp templates/data-models-template.md specs/[BRANCH_NAME]/data-models.md
   
   # 应用流程文档  
   cp templates/app-flows-template.md specs/[BRANCH_NAME]/app-flows.md
   
   # 测试用例文档
   cp templates/test-cases-template.md specs/[BRANCH_NAME]/test-cases.md
   ```
   - **Data Models Documentation**: 为新功能创建数据模型结构文档
   - **Application Flows Documentation**: 文档化用户交互和业务流程
   - **Test Cases Documentation**: 创建精确的测试用例来验证需求实现

5. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.
6. Report completion with branch name, spec file path, and readiness for the next phase.

Note: The script creates and checks out the new branch and initializes the spec file before writing.
