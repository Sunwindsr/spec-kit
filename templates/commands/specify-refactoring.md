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

7. **PHASE 0: API CONTRACT EXTRACTION** (MANDATORY - 刚性前提条件):
   ```bash
   # API Contract First: 后端API契约提取 - 这是直接替换重构的专门阶段
   python3 scripts/extract-api-contracts.py --source [SOURCE_PROJECT_PATH] --output specs/[BRANCH_NAME]/api-contracts.md
   ```
   - **API Validation**: 验证提取的API端点和数据模型完整性和准确性
   - **Direct Replacement Focus**: 新前端直接调用相同API，无需适配层或兼容层
   - **Use ONLY Extracted APIs**: 新前端实现必须严格使用提取的API契约和数据模型
   - **Validation Failure**: 如果API契约提取失败，整个重构过程立即终止
   - **CONSTITUTION VIOLATION**: 违反直接替换原则将导致重构失败

8. **PHASE 1: DATA MODELS EXTRACTION** (数据模型提取):
   ```bash
   # 数据模型专用提取 - 获取详细的TypeScript接口和数据结构
   cp templates/data-models-refactoring-template.md specs/[BRANCH_NAME]/data-models.md
   ```
   - **Data Model Documentation**: 分析源代码中的所有TypeScript接口定义、数据类型和关系
   - **Entity Relationships**: 文档化实体间的关系和约束
   - **Source Code Attribution**: 每个数据模型必须标注源代码位置 `[file_path]:[line_number]`
   - **Constitution VI-D Compliance**: 严禁自定义接口和数据模型，必须从源代码提取

9. **PHASE 2: APPLICATION FLOWS ANALYSIS** (应用流程分析):
   ```bash
   # 应用流程分析 - 基于现有代码分析用户交互和业务流程
   cp templates/app-flows-refactoring-template.md specs/[BRANCH_NAME]/app-flows.md
   ```
   - **User Journey Mapping**: 基于现有组件分析用户交互流程
   - **Business Logic Flows**: 文档化核心业务逻辑和数据处理流程
   - **Component Interactions**: 分析组件间的通信和数据流
   - **Route Configuration Analysis**: 特别关注前端路由配置分析 (Constitution VI-F)
   - **Source Code Traceability**: 所有流程步骤必须标注源代码位置

10. **PHASE 3: TEST CASES GENERATION** (测试用例生成):
   ```bash
   # 测试用例生成 - 基于重构规范创建精确的测试用例
   cp templates/test-cases-refactoring-template.md specs/[BRANCH_NAME]/test-cases.md
   ```
   - **Behavior Preservation Tests**: 创建确保100%行为保持的测试用例
   - **API Contract Validation**: 验证API契约的正确实现
   - **Interface Stability Tests**: 确保所有接口保持稳定
   - **Frontend Route Preservation Tests**: 验证前端路由100%保持 (Constitution VI-F)
   - **Precision Requirements Definition**: 精确的需求定义，为后续验证做准备

11. **Fill all generated documents with concrete content**:
    - **data-models.md**: Analyze source code to extract all TypeScript interfaces, data models, and relationships
    - **app-flows.md**: Analyze components, user interactions, business logic flows, and route configurations  
    - **test-cases.md**: Generate comprehensive test cases based on the refactoring requirements
    - **All content must be derived from actual source code analysis, not assumptions**

12. Write the refactoring specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived **ONLY** from the code extraction results while preserving section order and headings.
13. Report completion with branch name, spec file path, and readiness for the next phase.

Note: The script creates and checks out the new branch and initializes the spec file before writing.

Key differences from standard `/specify`:
- **Input Analysis**: Instead of user description, analyze existing codebase
- **Behavior Preservation**: All specifications must maintain 100% backward compatibility
- **Interface Stability**: Public APIs, UI components, and data models must remain unchanged
- **Migration Strategy**: Include incremental migration approach for zero-downtime refactoring
- **Validation Requirements**: Comprehensive testing to ensure behavior preservation