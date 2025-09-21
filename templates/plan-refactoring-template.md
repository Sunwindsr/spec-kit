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
4. Fill Refactoring Constitution Check section
   → Verify compliance with refactoring principles
   → Validate behavior preservation requirements
5. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Refactoring approach too risky"
   → Update Progress Tracking: Initial Constitution Check
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
**Behavior Preservation (I)**: All refactoring MUST preserve 100% existing behavior - no exceptions  
**Interface Stability (II)**: Public interfaces MUST remain unchanged - signatures, parameters, contracts  
**Data Contract Integrity (III)**: Database structures and serialization formats MUST be preserved  
**Concurrency Consistency (IV)**: No new concurrency units - retry, timeout, backoff strategies unchanged  
**Structural Changes Only (V)**: Only file/module movement, splitting, adapters, annotations permitted  

### Prohibited Changes Verification
**Prohibited Changes (VI)**: Backend performance optimizations, algorithm replacements, default values, log messages, sorting logic, randomness, I/O changes strictly forbidden

**Frontend-Specific Verification (VI-A/B)**:
- [ ] Frontend: Component modernization aligns with technology stack benefits
- [ ] Frontend: UI layout and user workflow preserved (functional behavior)
- [ ] Frontend: Business logic and data flow remain consistent
- [ ] Frontend: Style improvements enhance rather than disrupt user experience  

### Methodology Compliance
**Complete Migration (VII)**: Include all dependencies when extracting units - no coupling remnants  
**Immediate Updates (VIII)**: Batch-update all references after each migration unit  
**Single Responsibility (IX)**: Each commit addresses only one structural modification type  
**Incremental Revertibility (X)**: Every change must be independently verifiable and revertible  

### Constitution Compliance
- [ ] Behavior Preservation (I): 100% functional equivalence guaranteed
- [ ] Interface Stability (II): All public interfaces preserved exactly
- [ ] Data Contract Integrity (III): No data model or serialization changes
- [ ] Concurrency Consistency (IV): Timing and ordering behaviors unchanged
- [ ] Structural Changes Only (V): Only allowed modification types used
- [ ] Prohibited Changes (VI): No forbidden backend modifications attempted
- [ ] Frontend Allowances (VI-A): Component modernization and UI enhancements utilized appropriately
- [ ] Frontend Constraints (VI-B): Layout and functional behavior preserved
- [ ] Complete Migration (VII): All dependencies properly migrated
- [ ] Immediate Updates (VIII): All references updated immediately
- [ ] Single Responsibility (IX): Each commit has single structural focus
- [ ] Incremental Revertibility (X): All changes are atomic and revertible

*See full constitution at `/memory/constitution-refactoring.md`*

## Refactoring Project Structure

### Documentation (this refactoring)
```
specs/[###-refactoring]/
├── plan.md              # This file (/plan-refactoring command output)
├── research.md          # Phase 0 output (/plan-refactoring command)
├── data-model.md        # Phase 1 output (/plan-refactoring command)
├── quickstart.md        # Phase 1 output (/plan-refactoring command)
├── contracts/           # Phase 1 output (/plan-refactoring command)
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
└── adapters/                     # Migration adapters
    ├── component-adapter.js      # Bridges old/new components
    └── service-adapter.js       # Bridges old/new services
```

**Structure Decision**: [PRESERVE existing structure, ADD new components alongside old ones]

## Phase 0: Code Analysis & Research
1. **Analyze current implementation**:
   - Map all business logic and data flows
   - Identify performance bottlenecks and technical debt
   - Document all dependencies and integration points

2. **Research refactoring approaches**:
   ```bash
   For each component to refactor:
     Task: "Analyze {component} behavior and interfaces"
   For each technical challenge:
     Task: "Research best practices for {challenge} refactoring"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Current implementation analysis
   - Refactoring approach selection
   - Risk assessment and mitigation strategies
   - Migration timeline and milestones

**Output**: research.md with complete behavior mapping and refactoring strategy

## Phase 1: Refactoring Design
*Prerequisites: research.md complete*

1. **Create interface preservation contracts** → `/contracts/`:
   - Document all existing interfaces that must remain stable
   - Create compatibility layers for old/new implementations
   - Define migration adapters and bridges

2. **Update data models** → `data-model.md`:
   - Document all existing data models and relationships
   - Define migration strategies for data model changes
   - Ensure data integrity during migration

3. **Create refactoring test strategy** → `quickstart.md`:
   - Define comprehensive behavior preservation tests
   - Create baseline tests for current implementation
   - Define validation criteria for refactored implementation

4. **Update agent file incrementally** (O(1) operation):
   - Run `{SCRIPT}` for your AI assistant
   - Add refactoring-specific guidance and tools
   - Preserve existing configuration
   - Add behavior preservation requirements

**Output**: Interface contracts, data model preservation docs, test strategy, agent updates

## Phase 2: Refactoring Task Planning Approach
*This section describes what the /tasks-refactoring command will do - DO NOT execute during /plan-refactoring*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-refactoring-template.md` as base
- Generate tasks focusing on behavior preservation:
  - Each interface → compatibility task [P]
  - Each component → refactoring task with validation [P]
  - Each business flow → end-to-end testing task
  - Each risk → mitigation task
- Prioritize tasks based on risk and dependency order

**Ordering Strategy**:
- Behavior documentation before any changes
- Interface compatibility before component refactoring
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
| [e.g., Complex adapters] | [interface compatibility requirement] | [direct replacement would break integrations] |

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [ ] Phase 0: Code analysis complete (/plan-refactoring command)
- [ ] Phase 1: Refactoring design complete (/plan-refactoring command)
- [ ] Phase 2: Refactoring task planning complete (/plan-refactoring command - describe approach only)
- [ ] Phase 3: Refactoring tasks generated (/tasks-refactoring command)
- [ ] Phase 4: Refactoring implementation complete
- [ ] Phase 5: Validation and deployment complete

**Gate Status**:
- [ ] Initial Constitution Check: PASS
- [ ] Post-Design Constitution Check: PASS
- [ ] All interfaces documented and preserved
- [ ] Behavior mapping complete
- [ ] Risk mitigation documented

---

*Based on Constitution v2.1.1 - Refactoring Methodology*