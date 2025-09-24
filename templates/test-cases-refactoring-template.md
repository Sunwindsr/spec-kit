---
description: "Test cases template for refactoring validation with behavior preservation verification"
scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

# Refactoring Test Cases: [SYSTEM/COMPONENT NAME]

**Feature Branch**: `[###-refactoring-name]` | **Date**: [DATE] | **Spec**: [link-to-spec]
**Input**: Refactoring specification from `/specs/[###-refactoring-name]/spec.md`

## Execution Flow (main)
```
1. Load refactoring specification from Input path
   → If not found: ERROR "No refactoring spec at {path}"
2. Extract behavior preservation requirements and interface stability needs
   → Map each interface and component to test scenarios
3. Generate test cases by category:
   → Behavior Preservation Tests (行为保持): Core functionality verification
   → Interface Stability Tests (接口稳定): API compatibility verification
   → Performance Regression Tests (性能回归): Performance benchmarking
   → Migration Safety Tests (迁移安全): Deployment and rollback verification
4. Fill test case table with specific validation scenarios
   → Each test case must verify behavior preservation
   → Include performance benchmarks and rollback validation
5. Apply priority levels based on criticality:
   → P0: Critical (core behavior, data integrity, interface stability)
   → P1: High (business logic, performance benchmarks)
   → P2: Medium (edge cases, non-critical paths)
   → P3: Low (nice-to-have validations)
6. Validate test completeness:
   → All interfaces have stability tests
   → All components have behavior preservation tests
   → Performance benchmarks are covered
   → Migration procedures are validated
7. Return: SUCCESS (refactoring test cases ready for implementation)
```

## Summary
[Extract from refactoring spec: key interfaces, components, and behavior preservation requirements]

---

## 🔍 Behavior Precision Definition *(critical for refactoring success)*

### Current Behavior Analysis Strategy
*Precisely document the current system's behavior before refactoring*

**1. Interface Contract Definition**
- **API Signatures**: Exact method names, parameters, return types, HTTP status codes
- **Data Formats**: Exact JSON structures, field names, data types, validation rules
- **Error Responses**: Specific error codes, messages, and formats for all failure scenarios
- **Performance Characteristics**: Current response times, throughput, resource usage patterns

**2. Business Logic Precision**
- **Algorithms**: Step-by-step processing logic with exact decision points
- **Business Rules**: All validation rules, constraints, and conditional logic
- **State Management**: How state changes and transitions occur
- **Side Effects**: Database operations, external calls, caching behavior

**3. UI/UX Behavior Precision**
- **User Interactions**: Exact sequence of user actions and system responses
- **Visual Behavior**: How UI components behave, update, and respond to user input
- **Data Flow**: How data moves between components and updates the interface
- **Error Handling**: How errors are displayed and handled in the UI

### Behavior Documentation Template

For each component being refactored, document the current behavior precisely:

| Behavior Aspect | Current Implementation | Refactoring Requirement |
|:----------------|:----------------------|:------------------------|
| **API Contract** | [Exact current API signature and behavior] | [Must maintain exact same interface] |
| **Data Processing** | [Step-by-step current processing logic] | [Must produce identical results] |
| **Error Handling** | [Current error responses and codes] | [Must match exactly] |
| **Performance** | [Current performance metrics] | [Must not degrade beyond X%] |
| **UI Behavior** | [Current user interaction patterns] | [Must feel identical to user] |

### Example: Behavior Precision Documentation

**Component**: UserFileViewer
- **API Contract**: 
  - GET /api/files/{id} → returns FileDTO with exact field structure
  - POST /api/files/{id}/view → records view event, returns 200/404
  - All requests include Authorization header with JWT token
- **Data Processing**:
  1. Validate JWT token and extract user ID
  2. Check user has permission to access file
  3. Increment file view count in database
  4. Return file metadata with exact same field structure
- **Error Handling**:
  - Invalid token: HTTP 401 with {"error": "invalid_token"}
  - File not found: HTTP 404 with {"error": "file_not_found"}
  - No permission: HTTP 403 with {"error": "access_denied"}
- **Performance**:
  - Current response time: 120ms average (P95: 350ms)
  - Current throughput: 200 requests/second
  - Memory usage: 15MB per request
- **UI Behavior**:
  - Loading spinner shows for >200ms requests
  - Files display in grid view with exact same layout
  - Sort by name/date ascending, toggleable
  - Pagination shows 20 items per page

### Behavior Verification Checklist
- [ ] All API endpoints are documented with exact signatures
- [ ] All data models are documented with exact field structures
- [ ] All business logic flows are documented step-by-step
- [ ] All error conditions and responses are documented
- [ ] Performance metrics are established as baselines
- [ ] UI behavior patterns are documented with screenshots/videos
- [ ] All external integrations are documented with exact contracts

---

## Refactoring Test Cases Structure Template

| Field | Description | Guidelines |
|:-----|:------------|:-----------|
| **用例ID** | Unique identifier | Format: `RTC-[COMPONENT]-[TYPE]-[NUMBER]` (e.g., `RTC-AUTH-BHV-001`) |
| **场景描述** | Behavior preservation scenario | Focus on verifying identical behavior between old and new implementations |
| **前置条件** | Required system state | Include both original and refactored system states |
| **输入数据/参数** | Specific test data | Use identical test data for both implementations |
| **验证操作** | Test execution steps | Execute same operations on both old and new systems |
| **期望结果** | Behavior preservation criteria | Results MUST be identical between implementations |
| **性能基准** | Performance requirements | Response times and resource usage must not degrade |
| **优先级** | Business criticality level | `P0`/`P1`/`P2`/`P3` based on impact |
| **关联重构需求** | Source requirement | Link to specific refactoring requirement |
| **当前状态** | Implementation status | `待实现`/`通过`/`失败`/`阻塞` |

---

## Refactoring Test Cases Table

| 用例ID | 场景描述 | 前置条件 | 输入数据/参数 | 验证操作 | 期望结果 | 性能基准 | 优先级 | 关联重构需求 | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `RTC-[COMP]-BHV-001` | `[验证核心业务逻辑行为一致]` | `[原系统和重构系统都可用]` | `[标准业务数据集]` | `[在两个系统上执行相同操作]` | `[结果完全一致]` | `[响应时间差异<5%]` | `P0` | `[REQ-BHV-001]` | `待实现` |
| `RTC-[COMP]-INT-001` | `[验证API接口向后兼容]` | `[现有客户端应用]` | `[标准API调用]` | `[使用原客户端调用重构后API]` | `[响应格式和内容一致]` | `[响应时间不超过原系统]` | `P0` | `[REQ-INT-001]` | `待实现` |
| `RTC-[COMP]-PER-001` | `[验证性能未回归]` | `[系统负载稳定]` | `[压力测试配置]` | `[执行性能测试套件]` | `[性能指标达到或超过基准]` | `[符合SLA要求]` | `P1` | `[REQ-PER-001]` | `待实现` |

---

## Refactoring Test Case Categories (Fill as needed)

### Behavior Preservation Tests (行为保持) - P0/P1
*Verify identical behavior between original and refactored systems*
- [ ] `RTC-[COMP]-BHV-[###]`: [Core business logic verification]
- [ ] `RTC-[COMP]-BHV-[###]`: [Data processing consistency]
- [ ] `RTC-[COMP]-BHV-[###]`: [Error handling behavior]
- [ ] `RTC-[COMP]-BHV-[###]`: [State management verification]

### Interface Stability Tests (接口稳定) - P0/P1  
*Verify all public interfaces remain backward compatible*
- [ ] `RTC-[COMP]-INT-[###]`: [API endpoint compatibility]
- [ ] `RTC-[COMP]-INT-[###]`: [Data model field preservation]
- [ ] `RTC-[COMP]-INT-[###]`: [UI component behavior]
- [ ] `RTC-[COMP]-INT-[###]`: [External integration compatibility]

### Frontend Route Preservation Tests (前端路由保持) - P0/P1
*Verify frontend routing configuration remains 100% unchanged (Constitution VI-F)*
- [ ] `RTC-[COMP]-ROU-[###]`: [Route path pattern preservation]
- [ ] `RTC-[COMP]-ROU-[###]`: [Route parameter configuration]
- [ ] `RTC-[COMP]-ROU-[###]`: [Route guards and protection]
- [ ] `RTC-[COMP]-ROU-[###]`: [Navigation logic consistency]
- [ ] `RTC-[COMP]-ROU-[###]`: [Query parameter handling]
- [ ] `RTC-[COMP]-ROU-[###]`: [Route data resolution]
- [ ] `RTC-[COMP]-ROU-[###]`: [Browser history behavior]
- [ ] `RTC-[COMP]-ROU-[###]`: [Deep linking functionality]

### Performance Regression Tests (性能回归) - P1/P2
*Ensure performance does not degrade below acceptable thresholds*
- [ ] `RTC-[COMP]-PER-[###]`: [Response time verification]
- [ ] `RTC-[COMP]-PER-[###]`: [Resource usage monitoring]
- [ ] `RTC-[COMP]-PER-[###]`: [Throughput and capacity]
- [ ] `RTC-[COMP]-PER-[###]`: [Memory and CPU utilization]

### Migration Safety Tests (迁移安全) - P0/P1
*Validate deployment and rollback procedures*
- [ ] `RTC-[COMP]-MIG-[###]`: [Canary deployment validation]
- [ ] `RTC-[COMP]-MIG-[###]`: [Rollback procedure effectiveness]
- [ ] `RTC-[COMP]-MIG-[###]`: [Data consistency during migration]
- [ ] `RTC-[COMP]-MIG-[###]`: [Zero downtime verification]

### Integration Compatibility Tests (集成兼容) - P1/P2
*Verify all existing integrations continue to work*
- [ ] `RTC-[COMP]-INT-[###]`: [Third-party API compatibility]
- [ ] `RTC-[COMP]-INT-[###]`: [Database connection stability]
- [ ] `RTC-[COMP]-INT-[###]`: [Message queue processing]
- [ ] `RTC-[COMP]-INT-[###]`: [Cache behavior consistency]

---

## Refactoring Test Case Generation Rules

### From Refactoring Requirements
```
For each behavior preservation requirement:
  1. Create behavior comparison test
  2. Create interface compatibility test
  3. Create performance benchmark test

For each interface stability requirement:
  1. Create backward compatibility test
  2. Create integration verification test
  3. Create client application test

For each migration requirement:
  1. Create deployment safety test
  2. Create rollback effectiveness test
  3. Create data consistency test
```

### Priority Assignment Guidelines
- **P0**: Core business logic behavior, interface stability, data integrity, rollback effectiveness
- **P1**: Performance benchmarks, integration compatibility, migration safety
- **P2**: Edge cases, error scenarios, non-critical paths
- **P3**: Documentation, monitoring, nice-to-have validations

### Test Case Quality Checklist
- [ ] Each test case compares old vs new implementation behavior
- [ ] Expected results are objectively measurable and identical
- [ ] Performance benchmarks are clearly defined
- [ ] Test data is realistic and comprehensive
- [ ] Both success and error scenarios are covered
- [ ] Integration points are thoroughly tested
- [ ] Migration procedures are validated

---

## Example Template (Replace with actual refactoring content)

### Component: [COMPONENT NAME - e.g., User Authentication]

| 用例ID | 场景描述 | 前置条件 | 输入数据/参数 | 验证操作 | 期望结果 | 性能基准 | 优先级 | 关联重构需求 | 当前状态 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| `RTC-AUTH-BHV-001` | `[验证用户登录行为一致]` | `[原认证系统和重构系统都可用]` | `[用户名密码组合]` | `[在两个系统上执行登录]` | `[认证结果和令牌完全一致]` | `[响应时间差异<10ms]` | `P0` | `REQ-BHV-001` | `待实现` |
| `RTC-AUTH-INT-001` | `[验证JWT令牌格式兼容]` | `[现有客户端应用]` | `[有效JWT令牌]` | `[使用原客户端验证令牌]` | `[令牌验证通过，用户信息正确]` | `[验证时间不超过原系统]` | `P0` | `REQ-INT-001` | `待实现` |

---

## Baseline Test Requirements

### Pre-Refactoring Baseline
*Establish comprehensive test coverage before any refactoring begins*
1. **Functional Baseline**: Complete test suite covering all business logic
2. **Performance Baseline**: Current performance metrics under various loads
3. **Integration Baseline**: All external integrations working correctly
4. **UI Baseline**: All user interfaces functioning as expected

### Post-Refactoring Validation
*Verify refactored system meets or exceeds baseline*
1. **Behavior Validation**: 100% test pass rate with identical results
2. **Performance Validation**: No performance degradation beyond acceptable thresholds
3. **Integration Validation**: All existing integrations continue to work
4. **User Experience Validation**: No perceptible changes to user experience

---

## Execution Status
*Updated during main() execution*

- [ ] Refactoring specification loaded
- [ ] Behavior preservation test cases generated
- [ ] Interface stability test cases generated
- [ ] Performance regression test cases generated
- [ ] Migration safety test cases generated
- [ ] Priority levels and dependencies assigned
- [ ] Quality checklist validated
- [ ] All requirements have comprehensive test coverage

---

## 需求测试覆盖矩阵 *(推荐)*

### 用户需求测试覆盖跟踪

| 用户需求ID | 需求描述 | 测试用例覆盖 | 测试类型 | 验收标准 |
|-----------|----------|-------------|----------|----------|
| **US-001** | [来自spec.md的需求描述] | BPT-001, INT-001 | Behavior Preservation | [具体验收标准] |
| **US-002** | [来自spec.md的需求描述] | PRT-001, IST-001 | Performance Regression | [具体验收标准] |

### 测试用例需求溯源

| 测试用例ID | 测试描述 | 关联用户需求 | 优先级 | 预期结果 |
|-----------|----------|-------------|--------|----------|
| **BPT-001** | [测试用例描述] | US-001 | P0 | [预期结果] |
| **BPT-002** | [测试用例描述] | US-001 | P0 | [预期结果] |
| **INT-001** | [测试用例描述] | US-002 | P1 | [预期结果] |

### 质量门禁检查点

| 检查项 | 关联需求 | 测试方法 | 通过条件 | 责任人 |
|--------|----------|----------|----------|--------|
| [质量检查项1] | US-001 | [测试方法] | [通过标准] | [角色] |
| [质量检查项2] | US-002 | [测试方法] | [通过标准] | [角色] |

---

*All test cases MUST comply with refactoring constitution at `/memory/constitution-refactoring.md`*

---

*Based on Spec-Driven Development v2.1 - Refactoring Methodology*