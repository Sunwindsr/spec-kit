---
description: "Implementation plan template for refactoring existing systems with behavior preservation"
scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

# Refactoring Implementation Plan: [SYSTEM]

**Branch**: `[###-refactoring-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Refactoring specification from `/specs/[###-refactoring-name]/spec.md`

## Execution Flow (/plan-refactoring command scope)
```
1. Load refactoring spec from Input path
   → If not found: ERROR "No refactoring spec at {path}"
2. Perform comprehensive code analysis
   → Analyze existing implementation for behavior mapping
   → Identify all interfaces and dependencies
   → Document current architecture and patterns
3. Fill Current System Analysis section
   → Document existing behavior patterns
   → Map all public interfaces and contracts
4. Execute Automated Constitution Compliance
   → Run `specify refactoring reality-check` for mock data detection
   → Validate behavior preservation requirements automatically
   → Verify progressive refactoring prerequisites
5. Evaluate Automated Compliance results
   → If validation fails: Immediate halt with specific error guidance
   → If warnings exist: Document mitigation strategies
   → Update Progress Tracking: Automated Validation Check
6. Execute Phase 0 → research.md
   → Analyze current implementation and refactoring options
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
7. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file
   → Focus on interface preservation and behavior mapping
8. Re-evaluate Constitution Check section
   → If new violations: Refactor approach, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
9. Plan Phase 2 → Describe refactoring task generation approach
10. STOP - Ready for /tasks-refactoring command
```

**IMPORTANT**: The /plan-refactoring command STOPS at step 9. Phases 2-4 are executed by other commands:
- Phase 2: /tasks-refactoring command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
[Extract from refactoring spec: primary refactoring goals + behavior preservation requirements]

## Current System Analysis

### Existing Architecture
**Technology Stack**: [e.g., Legacy Java 8, Spring Boot 2.x, MySQL 5.7]  
**Architecture Pattern**: [e.g., Monolithic, Microservices, Layered]  
**Key Components**: [List major components and their responsibilities]  
**Integration Points**: [External systems, APIs, databases]  
**Performance Profile**: [Current performance characteristics and bottlenecks]

### Interface Inventory
**Public APIs**: [List all public API endpoints and contracts]  
**Data Models**: [List all data models and their relationships]  
**UI Components**: [List all user-facing components and interfaces]  
**External Integrations**: [List all third-party integrations and contracts]

### Behavior Mapping
**Business Logic Flows**: [Document all business processes and logic flows]  
**Data Processing Patterns**: [Document how data is processed and transformed]  
**Error Handling**: [Document current error handling patterns]  
**State Management**: [Document how system state is managed]

## Refactoring Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Verification
**Behavior Preservation (I)**: All refactoring MUST preserve 100% functional behavior - no exceptions  
**Interface Stability (II)**: Public interfaces MUST remain unchanged - signatures, parameters, contracts  
**Data Contract Integrity (III)**: Database structures and serialization formats MUST be preserved  
**Concurrency Consistency (IV)**: No new concurrency units - retry, timeout, backoff strategies unchanged  
**Structural Changes Only (V)**: Only file/module movement, splitting, type annotations, documentation permitted  

### **IMPORTANT: Frontend UI/UX Modernization Principle**
**Functional Logic vs UI/UX Distinction**:
- **✅ PRESERVE 100%**: Business logic, data flow, user workflows, functional behavior
- **🚀 ENCOURAGED TO OPTIMIZE**: UI layout, styling, interactions, UX patterns, responsiveness
- **🎯 GOAL**: Leverage new technology stack to improve user experience while maintaining functional integrity  

### Prohibited Changes Verification
**Prohibited Changes (VI)**: Backend performance optimizations, algorithm replacements, default values, log messages, sorting logic, randomness, I/O changes strictly forbidden

**Frontend-Specific Verification (VI-A/B)**:
- [ ] Frontend: **Functional behavior preserved** (business logic, data flow, user workflows)
- [ ] Frontend: **UI/UX modernization encouraged** (layout, styling, interactions based on new tech stack)
- [ ] Frontend: **Technology stack optimization** (utilize new framework capabilities for better UX)
- [ ] Frontend: **User experience enhancement** (improve interactions, responsiveness, accessibility)  

### Methodology Compliance
**Complete Migration (VII)**: Include all dependencies when extracting units - no coupling remnants  
**Immediate Updates (VIII)**: Batch-update all references after each migration unit  
**Single Responsibility (IX)**: Each commit addresses only one structural modification type  
**Incremental Revertibility (X)**: Every change must be independently verifiable and revertible  

### Automated Constitution Compliance
**Automated Enforcement**: All compliance checks are executed via `specify refactoring validate` command

**Reality Validation (Mandatory)**:
```bash
# Executed automatically before Phase 0
specify refactoring reality-check --component [COMPONENT] --fail-on-mock
```
- **Mock Data Detection**: Automatic scanning prevents mock/fake data usage
- **Business Logic Completeness**: Verifies no TODO/FIXME placeholders remain
- **Integration Authenticity**: Ensures real API calls and data sources
- **Validation Score**: Must achieve ≥80% integration authenticity

**Behavior Preservation Verification (Mandatory)**:
```bash
# Executed automatically during Phase 1-2
specify refactoring behavior-preserve --baseline [ORIGINAL] --refactored [NEW]
```
- **Interface Stability**: Automated diff analysis of public interfaces
- **Functional Equivalence**: Comparative testing of original vs refactored
- **Data Contract Integrity**: Schema validation and serialization testing
- **Concurrency Consistency**: Timing and ordering behavior verification
- **Frontend Functional Logic**: Business logic and user workflows preserved (UI/UX can be optimized)

**Progressive Refactoring Enforcement (Mandatory)**:
```bash
# Strict phase sequence enforcement
specify refactoring baseline --component [COMPONENT]           # Phase 0: Prerequisite
specify refactoring api-contract --component [COMPONENT]       # Phase 0: API Contract Extraction  
specify refactoring component-replace --component [COMPONENT]  # Phase 2: Sequential
specify refactoring parallel-validation --component [COMPONENT] # Phase 3: Validation
```
- **Phase Gates**: Each phase automatically validates completion of previous phases
- **Rollback Capability**: Every operation creates restore points
- **Atomic Operations**: Each step is independently verifiable and revertible

**Automated Compliance Status**:
- ✅ **Reality Check**: [PASS/FAIL] - Mock data detection, business logic completeness
- ✅ **Behavior Preservation**: [PASS/FAIL] - Interface stability, functional equivalence  
- ✅ **Progressive Refactoring**: [PASS/FAIL] - Phase sequence, rollback capability
- ✅ **Data Integrity**: [PASS/FAIL] - Schema preservation, serialization consistency
- ✅ **Methodology Compliance**: [PASS/FAIL] - Single responsibility, atomic changes

**Validation Failure Actions**:
- **Reality Check Fail**: Immediate halt - Fix mock data/placeholders before continuing
- **Behavior Preservation Fail**: Design review required - Revisit Phase 1 approach
- **Phase Sequence Violation**: Automatic rollback - Follow prescribed order
- **Data Integrity Fail**: Schema migration review - Ensure 100% direct replacement

*See full constitution at `/memory/constitution-refactoring.md`*

## Refactoring Project Structure

### Documentation (this refactoring)
```
specs/[###-refactoring]/
├── plan.md              # This file (/plan-refactoring command output)
├── research.md          # Phase 0 output (/plan-refactoring command)
├── data-models.md       # Phase 1A output - Data models and interfaces
├── app-flows.md         # Phase 1B output - UX interaction logic and user requirements
├── apis.md              # Phase 1C output - API contracts and endpoints
├── quickstart.md        # Phase 1 output (/plan-refactoring command)
└── tasks.md             # Phase 2 output (/tasks-refactoring command)
```

### Source Code (preserving existing structure)
```
# Existing structure maintained
# Refactoring creates new files/components alongside existing ones
# Migration strategy determines replacement timing

# Example: Component refactoring
src/
├── components/
│   ├── legacy-component.js       # Original component
│   └── refactored-component.js   # New implementation
├── services/
│   ├── legacy-service.js         # Original service
│   └── refactored-service.js     # New implementation
└── api-contracts/                # Extracted API contracts
```

**Structure Decision**: [PRESERVE existing structure, ADD new components alongside old ones]

## Phase 0: Code Analysis & Research
1. **Execute Reality Validation**:
   ```bash
   # Automated validation before any analysis
   specify refactoring reality-check --component [COMPONENT] --fail-on-mock
   ```
   - **Mock Data Detection**: Automatic scanning and prevention
   - **Business Logic Completeness**: Verify no placeholders exist
   - **Integration Authenticity**: Ensure real data sources and APIs
   - **Validation Output**: Report with specific violation locations and fixes

2. **Analyze current implementation**:
   - Map all business logic and data flows
   - Identify performance bottlenecks and technical debt
   - Document all dependencies and integration points

3. **Research refactoring approaches**:
   ```bash
   For each component to refactor:
     Task: "Analyze {component} behavior and interfaces"
   For each technical challenge:
     Task: "Research best practices for {challenge} refactoring"
   ```

4. **Consolidate findings** in `research.md` using format:
   - Current implementation analysis
   - Refactoring approach selection
   - Risk assessment and mitigation strategies
   - Migration timeline and milestones
   - **Validation Report**: Include automated reality check results

**Output**: research.md with complete behavior mapping, refactoring strategy, and validation compliance report

**Prerequisite**: Reality Validation must PASS (≥80% integration authenticity, zero mock data violations)

## Phase 1: Refactoring Design
*Prerequisites: research.md complete + Reality Validation PASS*

1. **Execute Behavior Preservation Verification**:
   ```bash
   # Automated verification during design phase
   specify refactoring behavior-preserve --baseline [ORIGINAL] --refactored [NEW]
   ```
   - **Interface Stability**: Automated diff analysis of public APIs
   - **Functional Equivalence**: Comparative testing requirements
   - **Data Contract Integrity**: Schema validation specifications
   - **Validation Output**: Compatibility report with specific preservation requirements

2. **Create core refactoring documentation trio**:
   
   **A. Extract data models** → `data-models.md`:
   - Extract all TypeScript interfaces and data models from source code
   - Document data relationships and type constraints
   - Define data integrity preservation requirements
   - **Automated extraction**: `python3 scripts/extract-api-contracts.py --source [SOURCE] --output data-models.md`

   **B. Document application flows** → `app-flows.md`:
   - Map all UX interaction logic and user workflows
   - Document business logic flows and state management
   - Define user requirement mappings from FRD
   - **Include user acceptance criteria** for each flow

   **C. Extract API contracts** → `apis.md`:
   - Extract all HTTP endpoints and API contracts from source code
   - Document request/response formats and error handling
   - Define API compatibility requirements for direct replacement
   - **Automated extraction**: `python3 scripts/extract-api-contracts.py --source [SOURCE] --output apis.md`

3. **Create refactoring test strategy** → `quickstart.md`:
   - Define comprehensive behavior preservation tests
   - Create baseline tests for current implementation
   - Define validation criteria for refactored implementation
   - **Include automated validation commands** in test strategy
   - **Include automated validation commands** in test strategy

5. **Execute Progressive Refactoring Baseline**:
   ```bash
   # Establish baseline for progressive refactoring
   specify refactoring baseline --component [COMPONENT]
   ```
   - **Component State Capture**: Current implementation state documentation
   - **Reference Point Creation**: Baseline for comparison during refactoring
   - **Rollback Point Establishment**: Restore point for safety

6. **Update agent file incrementally** (O(1) operation):
   - Run `{SCRIPT}` for your AI assistant
   - Add refactoring-specific guidance and tools
   - Preserve existing configuration
   - Add behavior preservation requirements
   - **Include automated validation command references**

**Output**: Interface contracts, data model preservation docs, test strategy, agent updates, baseline validation report

**Validation Gate**: Behavior Preservation Verification must PASS (100% interface stability, functional equivalence requirements defined)

## Phase 2: Refactoring Task Planning Approach
*This section describes what the /tasks-refactoring command will do - DO NOT execute during /plan-refactoring*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-refactoring-template.md` as base
- Generate tasks focusing on behavior preservation:
  - Each interface → API contract validation task [P0]
  - Each component → refactoring task with validation [P]
  - Each business flow → end-to-end testing task
  - Each risk → mitigation task
- Prioritize tasks based on risk and dependency order

**Ordering Strategy**:
- Behavior documentation before any changes
- API contract validation before component refactoring
- Testing throughout implementation
- Risk mitigation tasks before high-risk changes
- Mark [P] for parallel execution (independent components)

**Estimated Output**: 30-40 numbered, ordered tasks in tasks.md with heavy emphasis on testing

**IMPORTANT**: This phase is executed by the /tasks-refactoring command, NOT by /plan-refactoring

## Phase 3+: Refactoring Implementation
*These phases are beyond the scope of the /plan-refactoring command*

**Phase 3**: Refactoring task execution (/tasks-refactoring command creates tasks.md)  
**Phase 4**: Implementation with behavior validation (execute tasks.md following refactoring principles)  
**Phase 5**: Comprehensive testing and deployment (validation and rollout)

## Complexity Tracking
*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., Parallel components] | [need for zero downtime] | [big-bang approach too risky] |
| [e.g., Complex data models] | [API contract requirement] | [must extract from source code] |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [ ] Phase 0: Code analysis complete (/plan-refactoring command)
- [ ] Phase 1: Refactoring design complete (/plan-refactoring command)
- [ ] Phase 2: Refactoring task planning complete (/plan-refactoring command - describe approach only)
- [ ] Phase 3: Refactoring tasks generated (/tasks-refactoring command)
- [ ] Phase 4: Refactoring implementation complete
- [ ] Phase 5: Validation and deployment complete

**Automated Gate Status**:
- [ ] Reality Validation: PASS (≥80% integration authenticity, no mock data)
- [ ] Behavior Preservation Verification: PASS (interface stability confirmed)
- [ ] Progressive Refactoring Readiness: PASS (phase sequence validated)
- [ ] All interfaces documented and preserved
- [ ] Behavior mapping complete
- [ ] Risk mitigation documented
- [ ] Automated compliance checks integrated

---

*Based on Constitution v2.1.1 - Refactoring Methodology*