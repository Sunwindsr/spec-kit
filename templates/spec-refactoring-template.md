# Refactoring Specification: [SYSTEM NAME]

**Feature Branch**: `[###-refactoring-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Target System**: [DESCRIPTION OF SYSTEM TO BE REFACTORED]

## Execution Flow (main)
```
1. Analyze existing codebase from Input
   → If empty: ERROR "No target system description provided"
2. Extract current behavior and interfaces
   → Identify: existing APIs, data models, UI components, business logic
3. Document refactoring objectives and constraints
   → Preserve 100% behavior, maintain interface stability
4. For each unclear aspect:
   → Mark with [NEEDS CLARIFICATION: specific question]
5. Fill Current Behavior Analysis section
   → If no clear behavior mapping: ERROR "Cannot determine current behavior"
6. Generate Refactoring Requirements
   → Each requirement must ensure behavior preservation
   → Mark ambiguous requirements
7. Identify Interface Stability Requirements
8. Run Refactoring Review Checklist
   → If any [NEEDS CLARIFICATION]: WARN "Spec has uncertainties"
   → If behavior changes found: ERROR "Remove behavior modifications"
9. Return: SUCCESS (refactoring spec ready for planning)
```

---

## ⚡ Refactoring Guidelines
- ✅ Focus on WHAT needs refactoring and WHY
- ✅ Preserve 100% existing behavior (behavior preservation)
- ✅ Maintain interface stability (APIs, UI, data models)
- ❌ No new features or behavior changes
- 👥 Written for system architects and developers

### Section Requirements
- **Mandatory sections**: Must be completed for every refactoring
- **Optional sections**: Include only when relevant to the refactoring
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For Refactoring Generation
When creating this spec from code analysis:
1. **Document current behavior**: Thoroughly analyze existing implementation
2. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any unclear aspects
3. **Preserve interfaces**: Identify all stable interfaces that must remain unchanged
4. **Plan migration**: Include incremental migration strategy
5. **Common refactoring areas**:
   - Architecture modernization
   - Performance optimization
   - Code quality improvements
   - Technology stack updates
   - Maintenance and extensibility enhancements

---

## Current Behavior Analysis *(mandatory)*

### System Overview
[Describe the current system architecture, key components, and functionality]

### Existing User Stories & Business Value
**Primary User Stories**:
- **As a** [user type], **I want to** [action], **so that** [benefit]
- **As a** [user type], **I want to** [action], **so that** [benefit]

**Current Business Value**:
- [Value proposition 1]: [Description]
- [Value proposition 2]: [Description]

### Existing Interfaces
**RESTful API Endpoints** (CRITICAL - Must be preserved exactly):
- **GET** `/api/AppFiles/GetAppFileById?id={id}`: Retrieve file by ID
- **GET** `/api/AppFiles/GetAllSharedAppFiles?appIdentityIdAsOwner={id}`: Get all files shared by organization
- **POST** `/api/AppFiles/OnViewed`: Record file view event with file ID
- **POST** `/api/AppFiles/OnShared`: Record file share event with file ID
- **GET** `/api/AppFiles/GetComments?id={id}`: Retrieve file comments
- **POST** `/api/AppFiles/AddComment`: Add comment to file with file ID and comment ID
- **POST** `/api/AppFiles/Favorite`: Add file to favorites with file ID
- **POST** `/api/AppFiles/UnFavorite`: Remove file from favorites with file ID and optional favorite ID
- **POST** `/api/ViewTokens/ViewAViewToken`: Record token usage with token ID, new user flag, success flag
- **GET** `/api/ViewTokens/GetViewTokenById?id={id}`: Retrieve token by ID

**Repository Methods** (Internal APIs):
- [Repository method name]: [Description and signature]
- [Repository method name]: [Description and signature]

**Data Models**:
- [Model name]: [Fields and relationships]
- [Model name]: [Fields and relationships]

**UI Components**:
- [Component name]: [Functionality and interface]
- [Component name]: [Functionality and interface]

### Business Logic Flows
1. **[Flow name]**: [Description of current business logic]
2. **[Flow name]**: [Description of current business logic]

### Performance Characteristics
- [Current performance metric]: [Value and constraints]
- [Current performance metric]: [Value and constraints]

---

## Refactoring Objectives *(mandatory)*

### Business Requirements (EARS Format)
**EARS Requirements** - These describe WHAT the refactoring must achieve from a business perspective:

- **REQ-001**: When [user action or event], the system shall [maintain existing response] to preserve [business value]
- **REQ-002**: In the context of [specific scenario], when [condition occurs], the system shall [preserve existing behavior] to ensure [business outcome]
- **REQ-003**: When [integration point] is accessed, the system shall [maintain current interface] to support [business process]
- **REQ-004**: The system shall always [preserve critical business function] during and after refactoring

**Technical Refactoring Requirements**:
- **RF-001**: System MUST maintain 100% existing behavior
- **RF-002**: All public interfaces MUST remain stable and backward compatible
- **RF-003**: System MUST improve [specific aspect, e.g., "maintainability"]
- **RF-004**: System MUST preserve [specific aspect, e.g., "data integrity"]
- **RF-005**: System MUST enable [future capability, e.g., "easier testing"]

### Success Criteria
- **SC-001**: Zero behavioral changes detected through comprehensive testing
- **SC-002**: All existing integrations continue to function without modification
- **SC-003**: Performance meets or exceeds current benchmarks
- **SC-004**: Code quality metrics improve by [specific target]

### Constraints
- **C-001**: No breaking changes to public APIs
- **C-002**: No changes to existing data models
- **C-003**: Zero downtime during migration
- **C-004**: Complete rollback capability at all stages

---

## Migration Strategy *(mandatory)*

### Incremental Approach
1. **Phase 1**: [Specific refactoring phase with timeline]
2. **Phase 2**: [Specific refactoring phase with timeline]
3. **Phase 3**: [Specific refactoring phase with timeline]

### Risk Mitigation
- **Risk**: [Potential risk] → **Mitigation**: [Specific mitigation strategy]
- **Risk**: [Potential risk] → **Mitigation**: [Specific mitigation strategy]

### Rollback Strategy
- **Rollback Point 1**: [When and how to rollback]
- **Rollback Point 2**: [When and how to rollback]
- **Complete Rollback**: [Procedure for full system rollback]

---

## Interface Stability Requirements *(mandatory)*

### API Stability
- **[API name]**: MUST maintain exact signature and behavior
- **[API name]**: MUST maintain exact signature and behavior

### Data Model Stability
- **[Model name]**: MUST maintain all fields and relationships
- **[Model name]**: MUST maintain all fields and relationships

### UI Component Stability
- **[Component name]**: MUST maintain exact interface and behavior
- **[Component name]**: MUST maintain exact interface and behavior

---

## Testing Requirements *(mandatory)*

### Behavior Preservation Tests
- **BPT-001**: Verify all existing business logic remains unchanged
- **BPT-002**: Verify all API responses remain identical
- **BPT-003**: Verify all UI interactions remain identical

### Performance Regression Tests
- **PRT-001**: Ensure response times do not degrade beyond [threshold]
- **PRT-002**: Ensure resource usage does not increase beyond [threshold]

### Integration Tests
- **IT-001**: Verify all existing integrations continue to work
- **IT-002**: Verify data consistency across all operations

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Constitution Compliance
- [ ] **Behavior Preservation (I)**: 100% functional equivalence guaranteed
- [ ] **Interface Stability (II)**: All public interfaces preserved exactly
- [ ] **Data Contract Integrity (III)**: No data model or serialization changes
- [ ] **Concurrency Consistency (IV)**: Timing and ordering behaviors unchanged
- [ ] **Structural Changes Only (V)**: Only allowed modification types used
- [ ] **Prohibited Changes (VI)**: No forbidden backend modifications attempted
- [ ] **Frontend Allowances (VI-A)**: Component modernization and UI enhancements leveraged appropriately
- [ ] **Frontend Constraints (VI-B)**: UI layout and functional behavior preserved
- [ ] **Complete Migration (VII)**: All dependencies properly migrated
- [ ] **Immediate Updates (VIII)**: All references updated immediately
- [ ] **Single Responsibility (IX)**: Each commit has single structural focus
- [ ] **Incremental Revertibility (X)**: Every change must be independently verifiable and revertible

### Refactoring Compliance
- [ ] Incremental migration strategy documented
- [ ] Comprehensive testing strategy defined
- [ ] Rollback procedures established
- [ ] Source mapping maintained for all migrated code
- [ ] Minimal validation steps defined for each change

*Full refactoring constitution at `/memory/constitution-refactoring.md`*

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Success criteria are measurable and verifiable
- [ ] Risk assessment is comprehensive
- [ ] Migration path is realistic and safe

---

## Execution Status
*Updated by main() during processing*

- [ ] Target system analyzed
- [ ] Current behavior documented
- [ ] Refactoring objectives defined
- [ ] Interface stability requirements identified
- [ ] Migration strategy planned
- [ ] Testing requirements specified
- [ ] Refactoring review checklist passed

---

*Based on Spec-Driven Development v2.1 - Refactoring Methodology*