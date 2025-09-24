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
**User Pain Points & Context**:
> **重要**: 必须从实际用户调研和使用数据中提取真实的用户痛点
- [具体的用户问题描述和发生场景]
- [用户当前的解决方案及其局限性]
- [业务影响和用户满意度数据]

**Primary User Stories** (EARS Format with Real Context):
- **US-001**: **As a** [specific user role with real context], **I want to** [specific action], **so that** [tangible benefit]
  - **Real Scenario**: [具体的使用场景和环境]
  - **Current Pain**: [当前解决方案的痛点]
  - **Success Metrics**: [如何衡量成功]

- **US-002**: **As a** [specific user role with real context], **I want to** [specific action], **so that** [tangible benefit]
  - **Real Scenario**: [具体的使用场景和环境]
  - **Current Pain**: [当前解决方案的痛点]
  - **Success Metrics**: [如何衡量成功]

**Current Business Value** (with Metrics):
- [Value proposition 1]: [Description with measurable impact]
- [Value proposition 2]: [Description with measurable impact]

### User Acceptance Test Scenarios
> **必须包含具体的用户验收测试用例，确保重构后用户体验一致性**

**Critical User Journey Tests**:
1. **[User Journey Name]**:
   - **Given** [具体的前置条件]
   - **When** [用户执行的具体操作序列]
   - **Then** [期望的结果和用户体验]
   - **Success Criteria** [可衡量的成功标准]

2. **[User Journey Name]**:
   - **Given** [具体的前置条件]
   - **When** [用户执行的具体操作序列]
   - **Then** [期望的结果和用户体验]
   - **Success Criteria** [可衡量的成功标准]

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

**Data Models** (EXTRACTED FROM SOURCE CODE - MANDATORY):
> **警告：以下数据模型必须从实际源代码精确提取，不得基于假设创建**

**[DataModelName]** (Source: [path/to/file.ts:line]):
```typescript
// Exact interface/class definition from source code
export interface [DataModelName] {
  [fieldName]: [fieldType]; // From source with comments
  [fieldName]: [fieldType]; // Include all properties, validation, defaults
}
```

**Field Validation Rules**:
- [Field name]: [Validation rule from source]
- [Field name]: [Validation rule from source]

**Data Relationships**:
- [Relationship description based on actual usage]

**Repository Methods** (Internal APIs):
- [Repository method name]: [Description and signature]
- [Repository method name]: [Description and signature]


**Component Architecture & Functionality**:
> **必须详细描述每个组件的功能职责、关键逻辑和交互关系**

**[ComponentName]** (Source: [path/to/component.ts:line])
- **Function Description**: [详细的组件功能描述和业务职责]
- **Key Business Logic**: [关键业务逻辑和算法说明]
- **Complexity Level**: [High/Medium/Low] | **Lines**: [approximate]
- **Dependencies**: [依赖的服务、组件和外部系统]

**Layout & UX Structure** (ASCII Diagram):

### 完整组件架构
```
[MainContainerComponent] (主导航容器 + 路由分发)
├── 路由守卫: [Guard Names]
├── [Service Dependencies] 集成
└── RouterOutlet (动态组件加载)
    ├── [PrimaryComponent] (主要功能组件)
    ├── [SecondaryComponent] (次要功能组件)
    └── [OptionalComponent] (可选组件)
```

### [PrimaryComponent] 详细布局
```
[PrimaryComponent] ([组件功能描述])
┌─────────────────────────────────────────────────────────────┐
│ Header Section ([头部功能描述])                           │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ [Logo] [标题] [副标题] [操作按钮1] [操作按钮2]         │ │
├─────────────────────────────────────────────────────────────┤ │
│ Configuration/Control Area ([配置/控制区域描述])            │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ [配置项1] [配置项2] [统计信息] [预览区域]              │ │
├─────────────────────────────────────────────────────────────┤ │
│ Main Content Area ([主内容区域描述])                       │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ Content Item 1                                     │ │ │
│ │ │ ├─────────────┬─────────────────────────────────┤ │ │
│ │ │ │ 预览/缩略图  │ 详细信息                         │ │ │
│ │ │ │             │ ├─ 标题 + 副标题                 │ │ │
│ │ │ │             │ ├─ 关键数据1 + 关键数据2           │ │ │
│ │ │ │             │ ├─ 统计信息1 + 统计信息2           │ │ │
│ │ │ │             │ ├─ 状态指示器                     │ │ │
│ │ │ │             │ └─ 操作菜单 [操作1][操作2][...]   │ │ │
│ │ │ └─────────────┴─────────────────────────────────┤ │ │
│ │ │                                                     │ │ │
│ │ │ Content Item 2 (根据业务需求显示不同的预览类型)      │ │ │
│ │ │ ┌─────────────┬─────────────────────────────────┤ │ │
│ │ │ │ 特殊预览    │ 详细信息 + 操作按钮               │ │ │
│ │ │ └─────────────┴─────────────────────────────────┤ │ │
│ │ │                                                     │ │ │
│ │ │ [加载更多/分页控制] (滚动/分页加载)                   │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
├─────────────────────────────────────────────────────────────┤ │
│ Footer/Summary Area ([底部/汇总区域描述])                 │ │
│ │ 统计信息: [统计项1] | [统计项2] | [统计项3]             │ │
└─────────────────────────────────────────────────────────────┘
```

### [SecondaryComponent] 详细布局 (如适用)
```
[SecondaryComponent] ([组件功能描述])
┌─────────────────────────────────────────────────────────────┐
│ Dynamic Display Area ([动态显示区域描述])                  │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ ┌─────────────────────────────────────────────────────┐ │ │
│ │ │ 根据类型动态切换的内容区域                          │ │ │
│ │ │ 类型1: [类型1的具体显示内容]                        │ │ │
│ │ │ 类型2: [类型2的具体显示内容]                        │ │ │
│ │ │ 类型3: [类型3的具体显示内容]                        │ │ │
│ │ └─────────────────────────────────────────────────────┘ │ │
├─────────────────────────────────────────────────────────────┤ │
│ Information Panel ([信息面板描述])                        │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ 标题: [动态标题]                                     │ │
│ │ 属性1: [值] | 属性2: [值] | 属性3: [值]              │ │
│ │ 描述: [详细描述信息]                                   │ │
├─────────────────────────────────────────────────────────────┤ │
│ User Interaction Area ([用户交互区域描述])                 │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ [Tab1] [Tab2] [Tab3] Tab Group                        │ │
│ │                                                         │ │
│ │ Tab页1内容:                                           │ │
│ │ ├─ 列表/表单内容                                       │ │
│ │ ├─ 用户输入控件                                       │ │
│ │ └─ 操作按钮                                           │ │
│ │                                                         │ │
│ │ Tab页2内容: (根据需要添加更多Tab页)                     │ │
├─────────────────────────────────────────────────────────────┤ │
│ Action Buttons Area ([操作按钮区域描述])                   │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ [主要操作1] [主要操作2] [次要操作1] [次要操作2]       │ │
│ │ [高级功能] [设置] [帮助]                               │ │
├─────────────────────────────────────────────────────────────┤ │
│ Background Services ([后台服务描述])                      │ │
│ ├─ 数据同步服务 (实时更新)                               │ │
│ ├─ 用户行为跟踪 (交互记录)                               │ │
│ ├─ 状态管理 (本地/全局状态)                              │ │
│ └─ 缓存管理 (性能优化)                                   │ │
└─────────────────────────────────────────────────────────────┘
```

### 组件间数据流和交互关系
```
用户访问/操作 
    ↓
[Entry Point] + Guards/Services
    ↓
[PrimaryComponent] ←── [Supporting Services]
    ↓ (用户交互/状态变化)
[SecondaryComponent] ←──┐
    ↓                    │
用户操作                  │
    ↓                    │
[Actions/Events]         │
    ↓                    │
API/Data Layer           │
    ↓                    │
State Update ─────────────┘
    ↓
UI Re-render/Update
```

### 响应式布局变化
```
Desktop (多栏布局):
┌─────────────────┬─────────────────────────┬─────────────────┐
│ [侧边栏/导航]   │ [主内容区域]             │ [辅助信息面板]   │
│ (固定宽度)      │ (自适应剩余宽度)         │ (固定/自适应)    │
└─────────────────┴─────────────────────────┴─────────────────┘

Tablet (单栏布局):
┌─────────────────────────────────────────┐
│ [主内容区域] (全宽)                     │
└─────────────────────────────────────────┘
┌─────────────────────────────────────────┐
│ [次级内容区域] (全宽，切换显示)         │
└─────────────────────────────────────────┘

Mobile (优化触摸):
┌─────────────────────────────────────────┐
│ [紧凑导航] (顶部/底部)                 │
├─────────────────────────────────────────┤
│ [主内容] (垂直滚动，大触摸目标)         │
├─────────────────────────────────────────┤
│ [操作栏] (底部固定，易触达)             │
└─────────────────────────────────────────┘
```

### 关键交互模式
1. **主要用户流程**: [描述1-2个核心用户操作流程]
2. **数据更新模式**: [描述数据如何流动和更新]
3. **状态管理模式**: [描述组件内部和全局状态管理]
4. **错误处理模式**: [描述错误状态和恢复机制]

### Route Structure *(Critical for Interface Stability)*

**Source**: [routing/file/path.ts:line]

```typescript
// Exact route configuration from source code
const routes: Routes = [{
  path: "[base-path]", component: [MainComponent], children: [
    { path: "[route-pattern-1]", component: [Component1] },
    { path: "[route-pattern-2]", component: [Component2] },
    { path: "[route-pattern-3]", component: [Component3] }
  ]
}];
```

**Route Patterns**:
1. **[Pattern description]**: `[route-template]` ([parameter meaning])
2. **[Pattern description]**: `[route-template]` ([parameter meaning])
3. **[Pattern description]**: `[route-template]` ([parameter meaning])

**Route Parameters**:
- `[parameter]`: [type] - [description]
- `[parameter]`: [type] - [description]
- `[parameter]`: [type] - [description] (optional)

**User Interaction Flow**:
1. **[用户操作1]** → [系统响应1] → [界面变化1]
2. **[用户操作2]** → [系统响应2] → [界面变化2]
3. **[用户操作3]** → [系统响应3] → [界面变化3]

**Responsive Behavior**:
- **Desktop**: [桌面端布局和交互描述]
- **Tablet**: [平板端布局和交互描述]  
- **Mobile**: [移动端布局和交互描述]

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

### API Integration Tests *(MANDATORY for Refactoring with Existing APIs)*
- **AIT-001**: **API Connectivity Test**: Verify all refactored APIs are reachable and responsive
- **AIT-002**: **API Contract Test**: Verify all API signatures match exactly with existing contracts
- **AIT-003**: **API Data Flow Test**: Verify real data flows through frontend to backend and back
- **AIT-004**: **API Authentication Test**: Verify all authentication mechanisms work with refactored APIs
- **AIT-005**: **API Error Handling Test**: Verify error responses are consistent with existing behavior

### API Test Interface Requirements *(MANDATORY)*
**必须创建API测试界面完成真实API接通测试**:

#### 测试界面要求
1. **端点覆盖**: 包含所有重构后的API端点
2. **真实数据**: 必须调用真实的后端API，禁止使用模拟数据
3. **完整流程**: 测试从前端UI到后端数据库的完整数据流
4. **结果验证**: 验证请求和响应数据的完整性和准确性

#### 测试界面功能
- **API调用测试**: 每个端点的独立调用功能
- **参数配置**: 支持不同参数组合的测试
- **响应验证**: 实时显示API响应和验证结果
- **错误处理**: 测试各种错误场景的处理
- **性能监控**: 显示API响应时间和状态

#### 接通测试检查项
- [ ] 所有GET端点成功返回数据
- [ ] 所有POST端点成功创建/更新数据
- [ ] 所有PUT端点成功修改数据
- [ ] 所有DELETE端点成功删除数据
- [ ] 认证和授权机制正常工作
- [ ] 错误处理符合预期
- [ ] 数据格式和验证正确
- [ ] 前端能正确解析和显示API响应

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

### API Integration Compliance *(MANDATORY for Refactoring with Existing APIs)*
- [ ] **API Test Interface Created**: 完整的API测试界面已创建
- [ ] **All Endpoints Tested**: 所有API端点已完成真实接通测试
- [ ] **Real Data Verified**: 使用真实数据验证了所有数据流
- [ ] **Frontend-Backend Integration**: 前端能正确调用所有后端API
- [ ] **Authentication Working**: 认证机制在重构后正常工作
- [ ] **Error Handling Verified**: 错误处理符合原有行为
- [ ] **Performance Validated**: API性能达到预期要求
- [ ] **Data Consistency Proven**: 数据一致性得到验证

*Full refactoring constitution at `/memory/constitution-refactoring.md`*

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Success criteria are measurable and verifiable
- [ ] Risk assessment is comprehensive
- [ ] Migration path is realistic and safe

---

## Validation Certificate *(新增)*

### 重构合规验证证书
**验证日期**: [DATE]  
**验证状态**: [PENDING/PASSED/FAILED]  
**验证人员**: [VALIDATOR]

#### 合规性检查清单
- [ ] **行为保持性验证** (I): 所有功能行为100%保持不变
- [ ] **接口稳定性验证** (II): 所有公共接口完全保持一致
- [ ] **数据契约完整性** (III): 数据模型和序列化格式无变化
- [ ] **并发一致性验证** (IV): 时序和并发行为保持不变
- [ ] **结构化变更验证** (V): 仅允许的修改类型已使用
- [ ] **禁止修改验证** (VI): 未尝试任何禁止的后端修改
- [ ] **前端优化验证** (VI-A): 组件现代化和UI改进已适当利用
- [ ] **前端约束验证** (VI-B): UI布局和功能行为已保持
- [ ] **完整迁移验证** (VII): 所有依赖关系已正确迁移
- [ ] **即时更新验证** (VIII): 所有引用已立即更新
- [ ] **单一职责验证** (IX): 每次提交具有单一结构焦点
- [ **增量可逆性验证** (X): 每个变更必须独立可验证和可回滚
- [ **API接通测试验证** (XI): 所有API端点已完成真实接通测试
- [ **数据流验证** (XII): 前端到后端完整数据流已验证

#### 验证结果摘要
**验证通过项目**: [数量]/[总数]  
**关键问题**: [描述关键问题，如无则填写"无"]  
**建议措施**: [改进建议，如无则填写"无需"]  
**部署建议**: [✅ 推荐部署 / ⚠️ 需要修复 / ❌ 不推荐部署]

#### 验证签名
**规格负责人**: _________________________  
**实现工程师**: _________________________  
**测试工程师**: _________________________  
**验收人员**: _________________________  

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
- [ ] Validation certificate generated

---

## 需求引用关联 *(可选但推荐)*

### 与App-Flows的关联
本规格中的用户需求与技术流程的映射关系：

| 用户需求ID | 需求描述 | 对应App-Flows流程 | 实现优先级 |
|-----------|----------|-------------------|-----------|
| **US-001** | [需求简要描述] | [app-flows.md中的流程编号] | High/Medium/Low |
| **US-002** | [需求简要描述] | [app-flows.md中的流程编号] | High/Medium/Low |

### 与Test-Cases的关联
需求测试覆盖矩阵：

| 用户需求ID | 测试覆盖 | 验收标准 | 质量门禁 |
|-----------|----------|----------|----------|
| **US-001** | [test-cases.md中的测试用例编号] | [具体验收标准] | [通过条件] |
| **US-002** | [test-cases.md中的测试用例编号] | [具体验收标准] | [通过条件] |

---

*Based on Spec-Driven Development v2.1 - Refactoring Methodology*