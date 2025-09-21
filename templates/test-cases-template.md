---
description: "Test cases template for EARS requirements - structured test case creation"
scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

# Test Cases: [FEATURE/MODULE NAME]

**Feature Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link-to-spec]
**Input**: EARS requirements from `/specs/[###-feature-name]/spec.md`

## Execution Flow (main)
```
1. Load feature specification from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Extract EARS requirements and user stories
   → Map each EARS requirement to test scenarios
3. Generate test cases by category:
   → Happy Path (正常路径): Core functionality tests
   → Boundary Value (边界值): Edge case tests
   → Error Path (异常路径): Error handling tests
   → State-Dependent (状态依赖): State-based tests
4. Fill test case table with specific scenarios
   → Each test case must map to an EARS requirement
   → Include specific input data and expected results
5. Apply priority levels based on business impact
   → P0: Blocker (critical functionality)
   → P1: Critical (major impact)
   → P2: Major (moderate impact)
   → P3: Minor (minimal impact)
6. Validate test completeness:
   → All requirements have test coverage
   → Test cases are specific and verifiable
7. Return: SUCCESS (test cases ready for implementation)
```

## Summary
[Extract from feature spec: key requirements to be tested]

## Test Cases Structure Template

| Field | Description | Guidelines |
|:-----|:------------|:-----------|
| **用例ID** | Unique identifier | Format: `TC-[MODULE]-[NUMBER]` (e.g., `TC-LOGIN-001`) |
| **场景描述** | User story/behavior being tested | Describe specific scenario, include [NEEDS CLARIFICATION] for ambiguous requirements |
| **前置条件** | Required system state | List all prerequisites before test execution |
| **输入数据/参数** | Specific test data | Include exact values, JSON objects, or parameter sets |
| **模拟用户操作** | User actions to execute | Be specific about clicks, inputs, or API calls |
| **期望结果** | Verifiable expected outcome | Must be objectively measurable and specific |
| **优先级** | Business impact level | `P0`/`P1`/`P2`/`P3` based on user impact |
| **关联 EARS ID** | Source requirement | Link to specific EARS requirement (e.g., `REQ-LOGIN-01`) |
| **当前状态** | Implementation status | `待实现`/`通过`/`失败`/`阻塞` |

---

## Test Cases Table

| 用例ID | 场景描述 | 前置条件 | 输入数据/参数 | 模拟用户操作 | 期望结果 | 优先级 | 关联 EARS ID | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `TC-[MODULE]-001` | `[描述主要功能场景]` | `[系统初始状态]` | `[具体测试数据]` | `[用户操作步骤]` | `[可验证的预期结果]` | `[P0-P3]` | `[REQ-XX-XX]` | `待实现` |
| `TC-[MODULE]-002` | `[描述边界情况]` | `[特定前置条件]` | `[边界值测试数据]` | `[触发边界的操作]` | `[边界处理结果]` | `[P1-P2]` | `[REQ-XX-XX]` | `待实现` |
| `TC-[MODULE]-003` | `[描述错误处理]` | `[错误状态前置]` | `[错误输入数据]` | `[触发错误的操作]` | `[错误处理结果]` | `[P0-P1]` | `[REQ-XX-XX]` | `待实现` |

---

## Test Case Categories (Fill as needed)

### Happy Path Tests (正常路径) - P0/P1
*Core functionality under ideal conditions*
- [ ] `TC-[MODULE]-[###]`: [Primary success scenario]
- [ ] `TC-[MODULE]-[###]`: [Alternative success path]
- [ ] `TC-[MODULE]-[###]`: [Integration success scenario]

### Boundary Value Tests (边界值) - P1/P2  
*Edge cases, limits, and critical values*
- [ ] `TC-[MODULE]-[###]`: [Minimum/valid boundary]
- [ ] `TC-[MODULE]-[###]`: [Maximum/valid boundary]  
- [ ] `TC-[MODULE]-[###]`: [Just outside boundary]

### Error Path Tests (异常路径) - P0/P1
*Error handling and exceptional conditions*
- [ ] `TC-[MODULE]-[###]`: [Invalid input handling]
- [ ] `TC-[MODULE]-[###]`: [Missing required data]
- [ ] `TC-[MODULE]-[###]`: [System failure scenarios]

### State-Dependent Tests (状态依赖) - P1/P2
*Behavior under different system states*
- [ ] `TC-[MODULE]-[###]`: [Authentication state test]
- [ ] `TC-[MODULE]-[###]`: [Workflow state transition]
- [ ] `TC-[MODULE]-[###]`: [Configuration state test]

### Performance/Security Tests (性能/安全) - P2/P3
*Non-functional requirements*
- [ ] `TC-[MODULE]-[###]`: [Response time requirement]
- [ ] `TC-[MODULE]-[###]`: [Security validation]
- [ ] `TC-[MODULE]-[###]`: [Load/scenario test]

---

## Test Case Generation Rules

### From EARS Requirements
```
For each EARS requirement:
  1. "When A then B" → Happy path test
  2. "In context C, when A then B" → State-dependent test  
  3. "When event E happens, then B" → Event-driven test
  4. "The system shall always C" → Constraint test
```

### Priority Assignment Guidelines
- **P0**: Core user flows, authentication, data integrity
- **P1**: Major features, business logic, error handling
- **P2**: Edge cases, UI validation, performance
- **P3**: Nice-to-have, minor enhancements, corner cases

### Test Case Quality Checklist
- [ ] Each test case maps to a specific EARS requirement
- [ ] Expected results are objectively verifiable
- [ ] Input data is specific and realistic
- [ ] Prerequisites are clearly defined
- [ ] User actions are unambiguous
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Coverage includes all critical scenarios

---

## Example Template (Replace with actual feature content)

### Module: [MODULE NAME - e.g., User Authentication]

| 用例ID | 场景描述 | 前置条件 | 输入数据/参数 | 模拟用户操作 | 期望结果 | 优先级 | 关联 EARS ID | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `TC-[MODULE]-001` | `[合法用户登录成功]` | `[用户已注册，未登录]` | `[{"username": "testuser", "password": "ValidPass123!"}]` | `[输入用户名密码，点击登录]` | `[跳转到首页，显示欢迎信息]` | `P0` | `REQ-[MODULE]-01` | `待实现` |
| `TC-[MODULE]-002` | `[密码长度不足时提示错误]` | `[用户位于注册页]` | `[password: "Short1"]` | `[输入短密码，尝试提交]` | `[显示密码长度不足错误]` | `P1` | `REQ-[MODULE]-02` | `待实现` |

---

## Execution Status
*Updated during main() execution*

- [ ] Feature specification loaded
- [ ] EARS requirements extracted
- [ ] Test cases generated by category
- [ ] Priority levels assigned
- [ ] Quality checklist validated
- [ ] All requirements have test coverage

---
*Based on EARS-TC Specifications v2.1 - Test-Driven Development methodology*