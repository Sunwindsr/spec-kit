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

---

## 🔍 Precision Requirements Definition *(critical for implementation success)*

### Requirement Decomposition Strategy
*Break down ambiguous requirements into precise, implementable specifications*

**1. Business Context Analysis**
- **Stakeholder Identification**: Who are the users and what are their goals?
- **Business Value**: What problem does this solve and what is the measurable impact?
- **Usage Context**: In what environment and situations will this be used?

**2. Functional Requirement Precision**
- **Exact Inputs**: Specific data formats, ranges, constraints, and validation rules
- **Processing Logic**: Step-by-step algorithms, business rules, and decision criteria
- **Exact Outputs**: Specific response formats, data structures, and content requirements
- **Error Conditions**: What errors can occur and how should they be handled?

**3. Non-Functional Requirement Precision**
- **Performance Requirements**: Response times, throughput, concurrency limits
- **Security Requirements**: Authentication, authorization, data protection needs
- **Reliability Requirements**: Availability targets, error recovery expectations
- **Usability Requirements**: User experience constraints and accessibility needs

### Precision Definition Template

For each EARS requirement, create a precise specification:

| Requirement Aspect | Precise Definition | Implementation Guidance |
|:------------------|:------------------|:------------------------|
| **Business Need** | [Specific business problem being solved] | [Why this matters to stakeholders] |
| **User Context** | [Who uses this and in what situation] | [Real-world usage scenario] |
| **Input Specification** | [Exact data format, validation rules, constraints] | [Implement with specific validation logic] |
| **Processing Logic** | [Step-by-step algorithm or business rules] | [Implement with exact logic flow] |
| **Output Specification** | [Exact response format, content, structure] | [Return specific data structure] |
| **Error Handling** | [All error conditions and recovery paths] | [Handle specific exceptions with specific responses] |
| **Performance Constraints** | [Response time, throughput, scalability limits] | [Optimize to meet specific metrics] |
| **Success Criteria** | [Objective measures of successful implementation] | [Test to verify specific outcomes] |

### Example: Precision Definition

**Original EARS Requirement**: "When a user submits valid login credentials, the system shall authenticate them and grant access"

**Precise Definition**:
- **Business Need**: Users need secure access to their personal data and account features
- **User Context**: Registered users attempting to access the application from web or mobile
- **Input Specification**: 
  - Email: string, 5-100 chars, valid email format only
  - Password: string, 8-64 chars, must contain uppercase, lowercase, number, special char
  - Remember Me: boolean, optional, defaults to false
- **Processing Logic**:
  1. Validate email format using RFC 5322 regex pattern
  2. Validate password complexity requirements
  3. Hash password using bcrypt with 12 rounds
  4. Compare with stored hash in users table
  5. If valid, generate JWT token with 24h expiration
  6. If invalid, increment failed attempt counter
- **Output Specification**:
  - Success: JWT token, user info (id, email, name), session expires in 24h
  - Failure: HTTP 401 with specific error code (invalid_credentials/account_locked)
- **Error Handling**:
  - Invalid format: HTTP 400 with field-specific validation errors
  - Account locked: HTTP 403 with "Account temporarily locked" message
  - Too many attempts: HTTP 429 with "Too many attempts" and retry-after header
- **Performance Constraints**:
  - Response time < 500ms for 95% of requests
  - Support 100 concurrent logins per second
  - Password hashing must complete in < 100ms
- **Success Criteria**:
  - Valid credentials succeed 100% of the time
  - Invalid credentials are rejected 100% of the time
  - Password hashing never takes more than 100ms

### Requirement Validation Checklist
- [ ] Each requirement is specific and unambiguous
- [ ] All input formats and validation rules are defined
- [ ] Processing logic is completely specified
- [ ] All error conditions are identified and handled
- [ ] Performance requirements are measurable
- [ ] Success criteria are objectively verifiable
- [ ] Implementation guidance is clear and actionable

---

## Test Cases Structure Template

| Field | Description | Guidelines |
|:-----|:------------|:-----------|
| **用例ID** | Unique identifier | Format: `TC-[MODULE]-[NUMBER]` (e.g., `TC-LOGIN-001`) |
| **需求场景** | Precise requirement scenario | Describe the exact business requirement being tested with specific context |
| **前置条件** | Required system state | List all prerequisites with specific system configuration and data states |
| **测试数据集** | Comprehensive test data | Include positive, negative, boundary data with exact values and formats |
| **执行步骤** | Detailed execution steps | Precise sequence of actions, API calls, or user interactions |
| **预期结果** | Measurable expected outcomes | Objectively verifiable results with specific values, formats, and behaviors |
| **验证标准** | Success criteria | Unambiguous conditions that define test pass/fail with specific metrics |
| **优先级** | Business criticality level | `P0`/`P1`/`P2`/`P3` based on business impact and risk |
| **关联需求ID** | Source requirement | Link to specific EARS requirement (e.g., `REQ-LOGIN-01`) |
| **当前状态** | Implementation status | `待实现`/`通过`/`失败`/`阻塞` |

---

## Test Cases Table

| 用例ID | 需求场景 | 前置条件 | 测试数据集 | 执行步骤 | 预期结果 | 验证标准 | 优先级 | 关联需求ID | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `TC-[MODULE]-001` | `[精确描述核心业务需求场景]` | `[详细的系统配置和数据状态]` | `[包含正例、反例、边界值的完整测试数据]` | `[精确的操作步骤序列]` | `[可量化的预期结果]` | `[明确的通过/失败判定标准]` | `[P0-P3]` | `[REQ-XX-XX]` | `待实现` |
| `TC-[MODULE]-002` | `[精确描述边界条件需求]` | `[边界状态的具体配置]` | `[边界值、临界值测试数据]` | `[边界条件触发步骤]` | `[边界处理行为]` | `[边界处理的判定标准]` | `[P1-P2]` | `[REQ-XX-XX]` | `待实现` |
| `TC-[MODULE]-003` | `[精确描述异常处理需求]` | `[异常状态的前置条件]` | `[异常数据和错误场景]` | `[异常触发步骤]` | `[异常处理结果]` | `[异常处理的验证标准]` | `[P0-P1]` | `[REQ-XX-XX]` | `待实现` |

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