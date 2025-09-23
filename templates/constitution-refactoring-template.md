# Refactoring Constitution

## Core Refactoring Principles

### I. Behavior Preservation (NON-NEGOTIABLE)
Same inputs MUST produce identical outputs, side effects, error types/messages, and log levels/content. No behavioral changes are permitted under any circumstances. This principle supersedes all other refactoring considerations.

### II. Interface Stability (NON-NEGOTIABLE) 
Public interfaces MUST remain unchanged: class/function signatures, parameters, default values, environment variable names/semantics, and API contracts. Any interface change constitutes a breaking change and is forbidden.

### III. Data Contract Integrity
Database structures, query semantics, persistent data formats, and serialization field names/order MUST be preserved. Data integrity and compatibility must be maintained across all refactoring operations.

### IV. Concurrency & Temporal Consistency
No new concurrency units may be introduced. Retry, timeout, and backoff strategies MUST remain unchanged. Order semantics and timing behaviors MUST be preserved exactly.

### V. Structural Changes Only
Allowed changes are strictly limited to: file/module movement, class/function splitting, cohesion improvements, lightweight adapter layers, type annotations, documentation, and minimal formatting that doesn't alter behavior.

### VI. Prohibited Changes (ABSOLUTE) - Backend/Logic
Performance optimizations, algorithm replacements, default value adjustments, log message changes, sorting/deduplication logic modifications, randomness/seed changes, and I/O location/format changes are strictly forbidden.

### VI-C. Data Authenticity Principle (NON-NEGOTIABLE)
**严禁使用假数据** - All data MUST be real and authentic:
- **Zero Mock Data**: Absolutely no mockData, fakeData, dummyData, or similar fabricated data patterns
- **Real API Integration**: Must integrate with actual APIs and real data sources
- **Authentic Business Logic**: All business rules must operate on real data, not simulated or hardcoded values
- **Production-Ready Data**: Data sources must be production-grade, not development-only test data
- **Data真实性验证**: 必须验证所有数据的真实性和来源可靠性

### VI-D. Interface and Model Integrity Principle (NON-NEGOTIABLE)
**严禁自定义接口和数据模型** - All interfaces and data models MUST be extracted from source code:
- **Mandatory Code Extraction**: All interface and data model definitions must be extracted from existing source code
- **Zero Custom Definitions**: Absolutely no custom interface/type/class definitions allowed in specifications
- **Source Path Attribution**: Every interface/model MUST include exact source file path and line number
- **Automated Validation**: Specifications will be automatically validated against extracted definitions
- **Severe Penalties**: Any violation results in immediate specification rejection and restart

### VI-E. Direct Replacement Refactoring Principle (NON-NEGOTIABLE)
**直接替换重构原则** - 前端技术栈完全替换模式：
- **API Contract First**: 重构必须从后端API契约提取开始，这是专门强制性阶段
- **Complete Replacement Strategy**: 新前端直接替换旧前端，不是增量迁移，无需适配层
- **API Compatibility**: 新前端必须调用完全相同的后端API，保持请求/响应格式一致
- **Behavior Equivalence**: 新前端必须实现100%相同的功能行为和用户交互流程
- **Data Model Integrity**: 所有数据模型和字段定义必须完全保持原样，严禁自定义修改

### VI-A. Frontend-Specific Allowances
For frontend/UI refactoring, the following changes are PERMITTED and ENCOURAGED:
- **Component Modernization**: Replace legacy HTML/components with modern framework components
- **Performance Optimization**: Image optimization, lazy loading, bundle splitting, caching improvements
- **UI Enhancement**: Better styling, improved responsiveness, enhanced visual design
- **Interaction Improvements**: Better user experience, smoother animations, improved accessibility
- **Technology Stack Benefits**: Leverage modern framework capabilities for better maintainability

### VI-B. Frontend Constraints
UI layout and user workflow MUST be preserved:
- **Screen Layout**: Overall page structure and element positioning must be recognizably similar
- **User Flow**: User interaction sequences and navigation paths must remain identical
- **Functional Behavior**: Same user inputs must produce the same functional outputs
- **Business Logic**: All business rules and validation logic must be preserved exactly
- **Data Flow**: Data binding and state management behavior must remain consistent

## Refactoring Methodology

### VII. Complete Migration Principle
When extracting/migrating any unit, include all directly dependent private utility functions, constants, and data structures. Avoid cross-module coupling remnants that could create hidden dependencies.

### VIII. Immediate Caller Updates
After each migration unit is completed, immediately batch-update all references and perform minimal validation to ensure production path functionality.

### IX. Single Responsibility Changes
Each refactoring commit MUST address only one type of structural modification (e.g., "extract parser"). Avoid mixing unrelated changes in single commits.

### X. Incremental Revertibility
Every change MUST be independently verifiable and quickly revertible. Small, atomic changes reduce regression risk and enable safe rollback.

## Process Requirements

### XI. Documentation Synchronization
Complete TODO checklist updates, progress tracking, and "last updated" date modifications MUST be performed immediately after each subtask completion.

### XII. Structural Refactoring Only
Any behavior-modifying changes are strictly prohibited. Performance optimizations or other functional improvements MUST be handled as separate initiatives.

### XIII. Source Attribution
Every migrated code segment MUST include source mapping in format: `原: 路径:行 → 新: 路径`. Maintain complete consistency between original and refactored code.

### XIV. Minimal Validation Per Step
Each refactoring step MUST include: comprehensive search for remaining references (result must be 0), and sampling runs of key modes to verify error-free operation with unchanged output paths.

### XV. Task Decomposition
Large refactoring tasks MUST be broken into smaller, independently verifiable subtasks. Each subtask should be committed separately to minimize regression risk.

### XVI. Style Consistency
Original variable names, error messages, log formats, and comment tones MUST be preserved. New content should align with existing style patterns.

### XVI-A. Frontend Style Exception
For frontend projects, styling improvements are ENCOURAGED:
- **Modern CSS Practices**: Replace legacy styling with modern approaches (CSS Grid, Flexbox, CSS Variables)
- **Design System Alignment**: Adopt modern design systems and component libraries
- **Responsive Enhancement**: Improve mobile responsiveness and cross-device compatibility
- **Accessibility Improvements**: Enhance ARIA labels, keyboard navigation, and screen reader support
- **Visual Polish**: Improve spacing, typography, colors, and visual hierarchy while maintaining layout familiarity

## Quality Assurance

### XVII. Comprehensive Dependency Analysis
Understand complete functional units and calling relationships before refactoring. Use grep/rg tools to discover hidden dependencies. Systematic analysis prevents oversight.

### XVIII. Progressive Validation
Small steps with continuous validation are superior to batch operations. Each change must be verified before proceeding to the next.

### XIX. Tool-Assisted Verification
Leverage automated tools (grep, rg, static analysis) to discover dependencies and verify completeness. Manual analysis alone is insufficient.

### XX. Behavior Priority Over Aesthetics
Refactoring's primary goal is maintaining functional equivalence. Code improvements are secondary to behavior preservation.

## Governance

### Amendment Process
Refactoring constitution amendments require: documentation of proposed changes, impact analysis on existing refactoring projects, and migration plan for affected templates.

### Compliance Verification
All refactoring work MUST be verified against constitution principles before merge. Any deviation requires explicit justification and approval.

### Versioning Policy
- MAJOR: Backward incompatible changes to refactoring principles or removal of core constraints
- MINOR: New refactoring principles or expanded guidance for existing principles  
- PATCH: Clarifications, wording improvements, non-semantic refinements

### Template Synchronization
Constitution changes MUST be propagated to all refactoring templates and command files. Template consistency is mandatory for governance integrity.

**Version**: 1.1.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2025-09-23

---
*Note: This constitution establishes immutable constraints for refactoring activities. All refactoring work MUST comply with these principles.*