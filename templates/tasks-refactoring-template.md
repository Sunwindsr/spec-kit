---
description: "Refactoring tasks template for behavior-preserving system modernization"
scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

# Refactoring Tasks: [SYSTEM NAME]

**Feature Branch**: `[###-refactoring-name]` | **Date**: [DATE] | **Plan**: [link-to-plan]
**Input**: Refactoring plan from `/specs/[###-refactoring-name]/plan.md`

## Execution Flow (main)
```
1. Load refactoring plan from Input path
   → If not found: ERROR "No refactoring plan at {path}"
2. Execute Automated Constitution Compliance Validation
   → Run `specify refactoring validate-compliance` to ensure plan meets standards
   → If validation fails: ERROR with specific violation details
3. Extract refactoring phases and interface preservation requirements
   → Map each component to refactoring tasks with automated validation
4. Generate tasks by refactoring phase with automated validation:
   → Phase 1: Behavior Documentation (baseline tests + reality validation)
   → Phase 2: Interface Analysis (API contract verification + behavior preservation)
   → Phase 3: Incremental Implementation (component refactoring + phase validation)
   → Phase 4: Validation & Testing (behavior preservation + comprehensive automation)
   → Phase 5: Migration & Rollback (deployment procedures + automated rollback)
5. Fill task table with specific refactoring activities
   → Each task must include automated validation commands
   → Include automated rollback procedures and risk mitigation
   → Validate task completeness via `specify refactoring validate-tasks`
6. Apply priority levels based on risk and dependency order:
   → P0: Critical (interface stability, data integrity, validation gates)
   → P1: High (core functionality, performance validation, critical migrations)
   → P2: Medium (non-critical components, automated testing)
   → P3: Low (nice-to-have improvements, monitoring)
7. Execute Automated Task Quality Validation:
   → All tasks include proper validation commands
   → Task dependencies include validation gate requirements
   → Rollback procedures are automated and testable
   → Reality validation requirements are embedded
8. Return: SUCCESS (refactoring tasks ready for implementation with automated validation)
```

## Summary
[Extract from refactoring plan: key components, interfaces, and refactoring approach]

### **IMPORTANT: Refactoring Scope Principle**
**Functional vs UI/UX Modernization**:
- **100% PRESERVE**: Business logic, data flow, user workflows, functional behavior, API contracts
- **ENCOURAGED TO IMPROVE**: UI layout, styling, interactions, UX patterns, responsiveness, accessibility
- **TECHNOLOGY STACK BENEFITS**: Leverage new framework capabilities to enhance user experience

## Refactoring Tasks Structure Template

| Field | Description | Guidelines |
|:-----|:------------|:-----------|
| **任务ID** | Unique identifier | Format: `RT-[COMPONENT]-[PHASE]-[NUMBER]` (e.g., `RT-AUTH-DOC-001`) |
| **任务描述** | Refactoring activity | Include behavior preservation requirements and interface constraints |
| **用户验收标准** | User acceptance criteria | 必须包含具体的用户场景和可衡量的成功标准 |
| **前置条件** | Required system state | Include automated validation passes and baseline tests |
| **输入数据/参数** | Specific refactoring inputs | Include existing component specs and interface contracts |
| **重构操作** | Refactoring execution steps | Preserve behavior while improving implementation with automated validation |
| **验证步骤** | Automated behavior preservation tests | Must include `specify refactoring validate` commands + User acceptance tests |
| **回滚程序** | Automated rollback procedures | Must include `specify refactoring rollback` commands |
| **优先级** | Risk and impact level | `P0`/`P1`/`P2`/`P3` based on criticality |
| **依赖关系** | Task dependencies | List prerequisite tasks and order constraints with validation gates |
| **当前状态** | Implementation status | `待实现`/`进行中`/`已完成`/`阻塞`/`已回滚`/`验证失败` |

---

## Refactoring Tasks Table

| 任务ID | 任务描述 | 用户验收标准 | 前置条件 | 输入数据/参数 | 重构操作 | 验证步骤 | 回滚程序 | 优先级 | 依赖关系 | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `RT-[COMP]-DOC-001` | `[创建现有组件的基线测试]` | `[用户可以正常使用所有功能，测试覆盖率达到90%+]` | `[系统稳定运行 + Reality Validation PASS]` | `[组件规格和接口文档]` | `[编写全面的端到端测试]` | `[specify refactoring validate-baseline]` | `[specify refactoring rollback-baseline]` | `P0` | `无` | `待实现` |
| `RT-[COMP]-INT-001` | `[验证API契约一致性]` | `[所有API调用行为完全一致，直接替换无感知]` | `[基线测试完成 + API Contract Verification PASS]` | `[提取的API契约]` | `[验证新实现与API契约100%匹配]` | `[specify refactoring validate-api-contract]` | `[specify refactoring rollback-implementation]` | `P0` | `RT-[COMP]-DOC-001` | `待实现` |
| `RT-[COMP]-REF-001` | `[重构核心组件实现]` | `[用户完成核心操作流程，功能100%保持]` | `[API契约验证完成 + Implementation Validation]` | `[新设计规格]` | `[实现新版本组件，直接调用相同API]` | `[specify refactoring validate-refactoring]` | `[specify refactoring rollback-implementation]` | `P1` | `RT-[COMP]-INT-001` | `待实现` |
| `RT-[COMP]-VAL-001` | `[性能和负载测试]` | `[系统性能不低于基线，用户体验流畅]` | `[重构完成 + All Validations PASS]` | `[性能基准]` | `[执行性能测试]` | `[specify refactoring validate-performance]` | `[specify refactoring rollback-deployment]` | `P1` | `RT-[COMP]-REF-001` | `待实现` |

---

## Refactoring Task Categories (Fill as needed)

### Phase 1: Behavior Documentation (P0)
*Establish comprehensive baseline tests with automated validation*
- [ ] `RT-[COMP]-DOC-[###]`: [Component baseline tests with reality validation]
- [ ] `RT-[COMP]-DOC-[###]`: [Integration flow documentation with automated verification]
- [ ] `RT-[COMP]-DOC-[###]`: [Performance benchmark establishment with validation commands]
**Validation Gate**: All Phase 1 tasks must pass `specify refactoring reality-check`

### Phase 2: Interface Analysis (P0/P1)
*Verify API contracts and ensure direct replacement compatibility*
- [ ] `RT-[COMP]-INT-[###]`: [API endpoint verification with exact signature matching]
- [ ] `RT-[COMP]-INT-[###]`: [Data model validation with source code extraction]
- [ ] `RT-[COMP]-INT-[###]`: [Component interface verification for direct replacement]
**Validation Gate**: All Phase 2 tasks must pass `specify refactoring validate-api-contract`

### Phase 3: Incremental Implementation (P1/P2)
*Safe, incremental component refactoring with automated validation*
- [ ] `RT-[COMP]-REF-[###]`: [Core business logic refactoring with validation]
- [ ] `RT-[COMP]-REF-[###]`: [Data access layer refactoring with rollback capability]
- [ ] `RT-[COMP]-REF-[###]`: [Service layer modernization with phase validation]
**Validation Gate**: All Phase 3 tasks must pass `specify refactoring validate-phase`

### Phase 4: Validation & Testing (P0/P1)
*Comprehensive automated behavior preservation and performance validation*
- [ ] `RT-[COMP]-VAL-[###]`: [Behavior preservation regression tests with automation]
- [ ] `RT-[COMP]-VAL-[###]`: [Integration compatibility tests with continuous validation]
- [ ] `RT-[COMP]-VAL-[###]`: [Performance and load testing with automated benchmarking]
**Validation Gate**: All Phase 4 tasks must pass `specify refactoring validate-comprehensive`

### Phase 5: Direct Replacement Deployment (P0)
*Direct frontend replacement with validation*
- [ ] `RT-[COMP]-MIG-[###]`: [Final deployment verification with API compatibility check]
- [ ] `RT-[COMP]-MIG-[###]`: [Production rollout with complete replacement validation]
- [ ] `RT-[COMP]-MIG-[###]`: [Emergency rollback to original frontend procedure]
**Validation Gate**: All Phase 5 tasks must pass `specify refactoring validate-deployment`

---

## Refactoring Task Generation Rules

### From Refactoring Plan with Automated Validation
```
For each component in the refactoring plan:
  1. Create baseline documentation task (Phase 1)
     - Must include `specify refactoring reality-check` command
     - Must achieve ≥80% integration authenticity
  2. Create API contract verification task (Phase 2)
     - Must include `specify refactoring validate-api-contract` command
     - Must validate 100% API compatibility for direct replacement
  3. Create component refactoring task (Phase 3)
     - Must include `specify refactoring validate-phase` command
     - Must implement direct API calls without adapters
  4. Create validation task (Phase 4)
     - Must include comprehensive automated testing
     - Must verify behavior preservation and API consistency
  5. Create direct replacement deployment task (Phase 5)
     - Must include deployment validation commands
     - Must have emergency rollback to original frontend

**Automated Task Validation**:
- Each task generation triggers validation via `specify refactoring validate-tasks`
- Tasks without proper validation commands are automatically rejected
- Task dependencies automatically include validation gate requirements
```

### Priority Assignment Guidelines
- **P0**: Interface stability, data integrity, baseline testing, rollback procedures
- **P1**: Core functionality refactoring, performance validation, critical migrations
- **P2**: Non-critical components, UI improvements, code quality enhancements
- **P3**: Documentation, monitoring, non-essential optimizations

### Automated Task Quality Validation
**Automated Enforcement**: All task quality checks executed via `specify refactoring validate-tasks` command

**Reality Validation Integration**:
```bash
# Embedded in each task
specify refactoring reality-check --component [COMPONENT] --task-level
```
- **Mock Data Prevention**: Tasks automatically validate no mock data usage
- **Business Logic Completeness**: Tasks verify complete implementation
- **Integration Authenticity**: Tasks ensure real API calls and data sources

**Behavior Preservation Requirements**:
```bash
# Automated behavior validation per task
specify refactoring behavior-preserve --task [TASK_ID] --baseline [ORIGINAL]
```
- **Automated Interface Diffing**: Tasks include automated interface stability validation
- **Functional Equivalence Testing**: Tasks require comparative testing automation
- **Data Contract Validation**: Tasks include automated schema integrity checks
- **Frontend Functional Logic**: Business logic preserved, UI/UX modernization encouraged

**Progressive Refactoring Compliance**:
```bash
# Phase sequence validation per task
specify refactoring validate-phase --task [TASK_ID] --phase [PHASE_NUMBER]
```
- **Phase Gate Enforcement**: Tasks automatically validate prerequisite phases complete
- **Rollback Validation**: Tasks include automated rollback capability verification
- **Atomic Operation Testing**: Tasks verify each step is independently testable

**Automated Compliance Verification**:
- ✅ **Reality Check**: Task prevents mock data and ensures business logic completeness
- ✅ **Behavior Preservation**: Task includes automated interface stability validation
- ✅ **Progressive Compliance**: Task validates phase sequence and rollback capability
- ✅ **Data Integrity**: Task includes automated schema and serialization validation
- ✅ **Methodology Compliance**: Task ensures single responsibility and atomic operations

**Validation Failure Actions**:
- **Task-Level Reality Fail**: Task cannot be marked complete - fix violations first
- **Behavior Preservation Fail**: Task requires redesign - revisit interface compatibility
- **Phase Sequence Violation**: Task blocked - complete prerequisite phases first
- **Rollback Capability Missing**: Task implementation incomplete - add restore points

*All tasks MUST comply with refactoring constitution at `/memory/constitution-refactoring.md`*

---

## Example Template (Replace with actual refactoring content)

### Component: [COMPONENT NAME - e.g., Authentication Service]

| 任务ID | 任务描述 | 前置条件 | 输入数据/参数 | 重构操作 | 验证步骤 | 回滚程序 | 优先级 | 依赖关系 | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `RT-AUTH-DOC-001` | `[创建认证服务的基线测试]` | `[认证服务稳定运行]` | `[API文档和测试用例]` | `[编写完整的认证流程测试]` | `[所有测试通过并建立基线]` | `[保留测试代码]` | `P0` | `无` | `待实现` |
| `RT-AUTH-INT-001` | `[验证认证API契约一致性]` | `[基线测试完成]` | `[现有API接口定义]` | `[验证新实现与API契约100%匹配]` | `[specify refactoring validate-api-contract]` | `[specify refactoring rollback-implementation]` | `P0` | `RT-AUTH-DOC-001` | `待实现` |

---

## Execution Status
*Updated during main() execution with automated validation*

**IMPORTANT**: All status items MUST start as [ ] (pending) and ONLY be marked [x] (completed) after actual execution.
**VIOLATION**: Pre-completing any status item violates progressive refactoring principles and constitution.

- [ ] Refactoring plan loaded
- [ ] Automated Constitution Compliance Validation executed
- [ ] Refactoring tasks generated by phase with validation commands
- [ ] Priority levels and dependencies assigned with validation gates
- [ ] Automated Task Quality Validation completed
- [ ] Behavior preservation requirements documented with automation
- [ ] All components have complete refactoring coverage with validation
- [ ] Reality validation requirements embedded in all tasks
- [ ] Automated rollback procedures integrated into all tasks
- [ ] Progressive refactoring phase validation established

---

*Based on Spec-Driven Development v2.1 - Refactoring Methodology*