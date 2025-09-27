# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions
- **[T]**: Test results must be recorded before completion
- **[V]**: Validation gate required before proceeding

## Path Conventions
- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 3.1: Setup
- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T004 [P][T] Contract test POST /api/users in tests/contract/test_users_post.py
  - **Test Result**: [ ] Pending [ ] Passed [ ] Failed
  - **Test Evidence**: [Link to test output/log]
  - **Validation Required**: [ ] Manual [ ] Automated
- [ ] T005 [P][T] Contract test GET /api/users/{id} in tests/contract/test_users_get.py
  - **Test Result**: [ ] Pending [ ] Passed [ ] Failed
  - **Test Evidence**: [Link to test output/log]
  - **Validation Required**: [ ] Manual [ ] Automated
- [ ] T006 [P][T] Integration test user registration in tests/integration/test_registration.py
  - **Test Result**: [ ] Pending [ ] Passed [ ] Failed
  - **Test Evidence**: [Link to test output/log]
  - **Validation Required**: [ ] Manual [ ] Automated
- [ ] T007 [P][T] Integration test auth flow in tests/integration/test_auth.py
  - **Test Result**: [ ] Pending [ ] Passed [ ] Failed
  - **Test Evidence**: [Link to test output/log]
  - **Validation Required**: [ ] Manual [ ] Automated

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [ ] T008 [P] User model in src/models/user.py
- [ ] T009 [P] UserService CRUD in src/services/user_service.py
- [ ] T010 [P] CLI --create-user in src/cli/user_commands.py
- [ ] T011 POST /api/users endpoint
- [ ] T012 GET /api/users/{id} endpoint
- [ ] T013 Input validation
- [ ] T014 Error handling and logging

## Phase 3.4: Integration
- [ ] T015 Connect UserService to DB
- [ ] T016 Auth middleware
- [ ] T017 Request/response logging
- [ ] T018 CORS and security headers

## Phase 3.5: Polish
- [ ] T019 [P][T] Unit tests for validation in tests/unit/test_validation.py
  - **Test Result**: [ ] Pending [ ] Passed [ ] Failed
  - **Test Evidence**: [Link to test output/log]
  - **Validation Required**: [ ] Manual [ ] Automated
- [ ] T020 [T] Performance tests (<200ms)
  - **Test Result**: [ ] Pending [ ] Passed [ ] Failed
  - **Test Evidence**: [Link to performance benchmark results]
  - **Validation Required**: [ ] Automated [ ] Manual
- [ ] T021 [P] Update docs/api.md
- [ ] T022 Remove duplication
- [ ] T023 [T][V] Run manual-testing.md
  - **Test Result**: [ ] Pending [ ] Passed [ ] Failed
  - **Test Evidence**: [Link to manual test results]
  - **Validation Required**: [ ] Manual
  - **Validation Gate**: Must pass before deployment

## Dependencies
- Tests (T004-T007) before implementation (T008-T014)
- T008 blocks T009, T015
- T016 blocks T018
- Implementation before polish (T019-T023)

## Parallel Example
```
# Launch T004-T007 together:
Task: "Contract test POST /api/users in tests/contract/test_users_post.py"
Task: "Contract test GET /api/users/{id} in tests/contract/test_users_get.py"
Task: "Integration test registration in tests/integration/test_registration.py"
Task: "Integration test auth in tests/integration/test_auth.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Polish
   - Dependencies block parallel execution

## Task Validation System

### Task Completion Requirements
**⚠️ CRITICAL: Tasks cannot be marked complete without fulfilling ALL requirements**

#### For [T] Tasks (Test Results Required):
- [ ] **Test Execution**: Tests must be executed and produce verifiable results
- [ ] **Result Recording**: Test results must be recorded in the designated fields
- [ ] **Evidence Provision**: Links to test outputs, logs, or screenshots must be provided
- [ ] **Validation Check**: Results must be validated by specified method (Manual/Automated)
- [ ] **Failure Handling**: If tests fail, issues must be addressed and tests re-run

#### For [V] Tasks (Validation Gates):
- [ ] **Gate Requirement**: Must pass validation before proceeding to next phase
- [ ] **Stakeholder Review**: May require human verification for critical gates
- [ ] **Rollback Capability**: Failed validation gates trigger automated rollback
- [ ] **Documentation**: Validation results must be documented with evidence

### Test Result Recording Template
```markdown
## Test Results Summary
**Task ID**: [TASK-ID]
**Execution Date**: YYYY-MM-DD HH:MM:SS
**Test Environment**: [development/staging/production]

### Test Outcomes
| Test ID | Status | Duration | Evidence Link | Notes |
|---------|--------|----------|---------------|-------|
| [TEST-ID] | ✅ Pass / ❌ Fail | 1.2s | [link] | [details] |

### Validation Evidence
- **Automated Tests**: [Link to CI/CD run or test report]
- **Manual Tests**: [Link to test documentation or screenshots]
- **Performance Metrics**: [Link to performance benchmark results]
- **Integration Results**: [Link to integration test results]

### Validation Status
- **Overall Result**: ✅ PASSED / ❌ FAILED
- **Validated By**: [Name/System]
- **Validation Date**: YYYY-MM-DD HH:MM:SS
```

### Claude Code Hook Integration
**Pre-Completion Hook**: Automatically validates task completion requirements

```bash
# Hook checks before allowing task completion
claude-code-hook validate-task-completion --task-id=TASK-ID --required-tests=true
```

**Hook Validation Logic**:
1. **Test Result Check**: Verifies all required tests have results recorded
2. **Evidence Verification**: Validates that test evidence links are accessible
3. **Quality Gates**: Runs code quality checks (linting, type checking)
4. **Dependency Check**: Ensures all dependent tasks are complete
5. **Behavioral Validation**: Compares implementation behavior with requirements

### Sequential Enforcement
**⚠️ TASK FLOW CONTROL**:

1. **Phase-Based Progression**: Cannot proceed to next phase without validation
2. **Dependency Enforcement**: Cannot start dependent tasks without prerequisites
3. **Quality Gates**: Critical validation gates must pass before continuation
4. **Automated Rollback**: Failed validation triggers automatic rollback to last stable state

### Progress Tracking
**Real-time Task Status**:
- **🟡 Pending**: Task not yet started
- **🔵 In Progress**: Task being actively worked on
- **🟠 Testing**: Task implemented, awaiting test results
- **🔴 Failed**: Tests failed, requires remediation
- **🟢 Complete**: Task passed all validation and is complete
- **⚪ Blocked**: Waiting on dependencies or validation gates

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task
- [ ] All [T] tasks have test result recording fields
- [ ] All [V] tasks have validation gate definitions
- [ ] Claude Code hook integration configured
- [ ] Sequential enforcement rules defined