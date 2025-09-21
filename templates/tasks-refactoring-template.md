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
2. Extract refactoring phases and interface preservation requirements
   → Map each component to refactoring tasks
3. Generate tasks by refactoring phase:
   → Phase 1: Behavior Documentation (baseline tests)
   → Phase 2: Interface Analysis (compatibility layers)
   → Phase 3: Incremental Implementation (component refactoring)
   → Phase 4: Validation & Testing (behavior preservation)
   → Phase 5: Migration & Rollback (deployment procedures)
4. Fill task table with specific refactoring activities
   → Each task must include behavior preservation validation
   → Include rollback procedures and risk mitigation
5. Apply priority levels based on risk and dependency order:
   → P0: Critical (interface stability, data integrity)
   → P1: High (core functionality, performance)
   → P2: Medium (non-critical components)
   → P3: Low (nice-to-have improvements)
6. Validate task completeness:
   → All interfaces have compatibility tasks
   → All components have refactoring tasks
   → Comprehensive testing coverage
7. Return: SUCCESS (refactoring tasks ready for implementation)
```

## Summary
[Extract from refactoring plan: key components, interfaces, and refactoring approach]

## Refactoring Tasks Structure Template

| Field | Description | Guidelines |
|:-----|:------------|:-----------|
| **任务ID** | Unique identifier | Format: `RT-[COMPONENT]-[PHASE]-[NUMBER]` (e.g., `RT-AUTH-DOC-001`) |
| **任务描述** | Refactoring activity | Include behavior preservation requirements and interface constraints |
| **前置条件** | Required system state | Include baseline tests and compatibility checks |
| **输入数据/参数** | Specific refactoring inputs | Include existing component specs and interface contracts |
| **重构操作** | Refactoring execution steps | Preserve behavior while improving implementation |
| **验证步骤** | Behavior preservation tests | Must verify 100% behavior preservation |
| **回滚程序** | Rollback procedures | Immediate rollback capability for all changes |
| **优先级** | Risk and impact level | `P0`/`P1`/`P2`/`P3` based on criticality |
| **依赖关系** | Task dependencies | List prerequisite tasks and order constraints |
| **当前状态** | Implementation status | `待实现`/`进行中`/`已完成`/`阻塞`/`已回滚` |

---

## Refactoring Tasks Table

| 任务ID | 任务描述 | 前置条件 | 输入数据/参数 | 重构操作 | 验证步骤 | 回滚程序 | 优先级 | 依赖关系 | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `RT-[COMP]-DOC-001` | `[创建现有组件的基线测试]` | `[系统稳定运行]` | `[组件规格和接口文档]` | `[编写全面的端到端测试]` | `[验证测试通过并建立基线]` | `[保留测试代码]` | `P0` | `无` | `待实现` |
| `RT-[COMP]-INT-001` | `[创建接口兼容层]` | `[基线测试完成]` | `[现有接口定义]` | `[创建新旧实现之间的适配器]` | `[验证兼容层正常工作]` | `[移除兼容层，恢复原接口]` | `P0` | `RT-[COMP]-DOC-001` | `待实现` |
| `RT-[COMP]-REF-001` | `[重构核心组件实现]` | `[兼容层完成]` | `[新设计规格]` | `[实现新版本组件]` | `[通过基线测试验证行为]` | `[切换回原始实现]` | `P1` | `RT-[COMP]-INT-001` | `待实现` |
| `RT-[COMP]-VAL-001` | `[性能和负载测试]` | `[重构完成]` | `[性能基准]` | `[执行性能测试]` | `[验证性能达到或超过基准]` | `[回滚到原始实现]` | `P1` | `RT-[COMP]-REF-001` | `待实现` |

---

## Refactoring Task Categories (Fill as needed)

### Phase 1: Behavior Documentation (P0)
*Establish comprehensive baseline tests before any changes*
- [ ] `RT-[COMP]-DOC-[###]`: [Component baseline tests]
- [ ] `RT-[COMP]-DOC-[###]`: [Integration flow documentation]
- [ ] `RT-[COMP]-DOC-[###]`: [Performance benchmark establishment]

### Phase 2: Interface Analysis (P0/P1)
*Create compatibility layers and interface preservation strategies*
- [ ] `RT-[COMP]-INT-[###]`: [Public API compatibility layer]
- [ ] `RT-[COMP]-INT-[###]`: [Data model adapter]
- [ ] `RT-[COMP]-INT-[###]`: [UI component compatibility wrapper]

### Phase 3: Incremental Implementation (P1/P2)
*Safe, incremental component refactoring with validation*
- [ ] `RT-[COMP]-REF-[###]`: [Core business logic refactoring]
- [ ] `RT-[COMP]-REF-[###]`: [Data access layer refactoring]
- [ ] `RT-[COMP]-REF-[###]`: [Service layer modernization]

### Phase 4: Validation & Testing (P0/P1)
*Comprehensive behavior preservation and performance validation*
- [ ] `RT-[COMP]-VAL-[###]`: [Behavior preservation regression tests]
- [ ] `RT-[COMP]-VAL-[###]`: [Integration compatibility tests]
- [ ] `RT-[COMP]-VAL-[###]`: [Performance and load testing]

### Phase 5: Migration & Rollback (P0)
*Safe deployment and rollback procedures*
- [ ] `RT-[COMP]-MIG-[###]`: [Canary deployment procedure]
- [ ] `RT-[COMP]-MIG-[###]`: [Production rollout plan]
- [ ] `RT-[COMP]-MIG-[###]`: [Emergency rollback procedure]

---

## Refactoring Task Generation Rules

### From Refactoring Plan
```
For each component in the refactoring plan:
  1. Create baseline documentation task (Phase 1)
  2. Create interface compatibility task (Phase 2)
  3. Create component refactoring task (Phase 3)
  4. Create validation task (Phase 4)
  5. Create migration task (Phase 5)
```

### Priority Assignment Guidelines
- **P0**: Interface stability, data integrity, baseline testing, rollback procedures
- **P1**: Core functionality refactoring, performance validation, critical migrations
- **P2**: Non-critical components, UI improvements, code quality enhancements
- **P3**: Documentation, monitoring, non-essential optimizations

### Task Quality Checklist
- [ ] Each task includes behavior preservation requirements (Constitution Principle I)
- [ ] All tasks have comprehensive validation steps (Constitution Principle XVIII)
- [ ] Rollback procedures are clearly defined (Constitution Principle X)
- [ ] Dependencies are properly mapped (Constitution Principle XVII)
- [ ] Risk mitigation is addressed (Constitution Principle XIX)
- [ ] Performance considerations are included (Constitution Principle VI - no changes)
- [ ] Interface compatibility is ensured (Constitution Principle II)
- [ ] Single responsibility per task (Constitution Principle IX)
- [ ] Source mapping is maintained (Constitution Principle XIII)
- [ ] Minimal validation steps defined (Constitution Principle XIV)

*All tasks MUST comply with refactoring constitution at `/memory/constitution-refactoring.md`*

---

## Example Template (Replace with actual refactoring content)

### Component: [COMPONENT NAME - e.g., Authentication Service]

| 任务ID | 任务描述 | 前置条件 | 输入数据/参数 | 重构操作 | 验证步骤 | 回滚程序 | 优先级 | 依赖关系 | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `RT-AUTH-DOC-001` | `[创建认证服务的基线测试]` | `[认证服务稳定运行]` | `[API文档和测试用例]` | `[编写完整的认证流程测试]` | `[所有测试通过并建立基线]` | `[保留测试代码]` | `P0` | `无` | `待实现` |
| `RT-AUTH-INT-001` | `[创建认证API兼容层]` | `[基线测试完成]` | `[现有API接口定义]` | `[实现新旧的认证API适配器]` | `[验证所有现有调用正常]` | `[移除适配器，恢复原API]` | `P0` | `RT-AUTH-DOC-001` | `待实现` |

---

## Execution Status
*Updated during main() execution*

- [ ] Refactoring plan loaded
- [ ] Refactoring tasks generated by phase
- [ ] Priority levels and dependencies assigned
- [ ] Quality checklist validated
- [ ] Behavior preservation requirements documented
- [ ] All components have complete refactoring coverage

---

*Based on Spec-Driven Development v2.1 - Refactoring Methodology*