---
description: "Practical TDD-based refactoring tasks template for system modernization"
scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

# [FEATURE NAME] - Refactoring Development Tasks

**Feature Branch**: `[###-refactoring-name]` | **Date**: [DATE] | **Plan**: [link-to-plan]
**Input**: Refactoring plan from `/specs/[###-refactoring-name]/plan.md`

## 任务概述

### 重构任务分解策略
- **优先级定义**: 基于重构复杂度和业务重要性确定优先级
- **迭代规划**: 按技术层次分阶段实施，每个阶段包含完整的TDD验证流程
- **质量保证**: 每个任务都包含单元测试、集成测试和行为验证

### 开发优先级
- **P0**: 核心基础设施 - 项目架构、数据模型、API层
- **P1**: 核心功能组件 - 主要业务组件、状态管理
- **P2**: 辅助功能组件 - 共享组件、工具函数
- **P3**: 优化和部署 - 性能优化、E2E测试、部署配置

### 重构原则
- **行为保持**: 100%保持原有功能和业务逻辑
- **技术现代化**: 使用目标技术栈的最佳实践
- **测试驱动**: 严格遵循RED-GREEN-REFACTOR流程
- **增量开发**: 每个任务都是独立可交付的

## Summary
[Extract from refactoring plan: key components, interfaces, and refactoring approach]

### **IMPORTANT: Refactoring Scope Principle**
**Functional vs UI/UX Modernization**:
- **100% PRESERVE**: Business logic, data flow, user workflows, functional behavior, API contracts
- **ENCOURAGED TO IMPROVE**: UI layout, styling, interactions, UX patterns, responsiveness, accessibility
- **TECHNOLOGY STACK BENEFITS**: Leverage new framework capabilities to enhance user experience

## 一、核心基础设施开发任务

### 1.1 目标技术栈基础架构搭建

#### 1.1.1 任务：目标项目基础架构搭建 (P0)
```markdown
## 任务：目标项目基础架构搭建

**优先级**：P0  
**预计时间**：4小时  
**负责人**：前端架构师  

### 任务描述
搭建目标技术栈的基础项目架构，配置开发环境和构建工具链。

### EARS验收标准
- **Given**: 需要创建现代化的开发环境
- **When**: 执行项目初始化和配置
- **Then**: 应该创建完整的项目结构
- **And**: 所有开发工具应该正常工作

### RED阶段
1. **编写失败测试**
   ```typescript
   describe('Target Project Setup', () => {
     it('should have correct project structure', () => {
       // 测试项目结构
       expect(fs.existsSync('src/App.tsx')).toBeTruthy();
       expect(fs.existsSync('vite.config.ts')).toBeTruthy();
       expect(fs.existsSync('tsconfig.json')).toBeTruthy();
     });
     
     it('should build successfully', () => {
       // 测试构建过程
       const buildResult = execSync('npm run build', { encoding: 'utf8' });
       expect(buildResult).toContain('built in');
     });
     
     it('should run tests successfully', () => {
       // 测试测试环境
       const testResult = execSync('npm test', { encoding: 'utf8' });
       expect(testResult).toContain('passed');
     });
   });
   ```

### GREEN阶段
1. **实现功能代码**
   ```bash
   # 创建项目
   [TARGET_INIT_COMMAND]
   cd [PROJECT_NAME]
   
   # 安装依赖
   [DEPENDENCY_INSTALL_COMMANDS]
   
   # 配置构建工具
   [BUILD_TOOL_CONFIG]
   
   # 配置测试环境
   [TEST_ENV_CONFIG]
   ```

### REFACTOR阶段
1. **优化重构**
   - 优化构建配置
   - 配置路径别名
   - 添加环境变量配置
   - 优化开发服务器配置

### 验收标准
- [ ] 项目结构正确创建
- [ ] 开发服务器正常启动
- [ ] 构建过程成功完成
- [ ] 测试环境配置正确
- [ ] 代码格式化工具正常工作
- [ ] Hook验证Agent集成完成
- [ ] Task-Testcase关联机制就绪
```

### 1.2 数据模型和类型定义迁移

#### 1.2.1 任务：数据模型和类型定义迁移 (P0)
```markdown
## 任务：数据模型和类型定义迁移

**优先级**：P0  
**预计时间**：6小时  
**负责人**：前端开发工程师  

### 任务描述
将现有系统的数据模型迁移到目标技术栈的类型定义，确保100%类型匹配。

### EARS验收标准
- **Given**: 需要迁移数据模型定义
- **When**: 创建类型定义
- **Then**: 应该与现有系统完全匹配
- **And**: 应该通过所有类型检查

### RED阶段
1. **编写失败测试**
   ```typescript
   describe('Data Models Migration', () => {
     it('should match existing system model structure', () => {
       // 测试数据模型匹配
       const existingModel = getExistingModel();
       const targetModel = createTargetModel();
       
       expect(Object.keys(targetModel)).toEqual(Object.keys(existingModel));
       expect(targetModel.id).toEqual(existingModel.id);
       expect(targetModel.name).toEqual(existingModel.name);
     });
     
     it('should handle business logic correctly', () => {
       // 测试业务逻辑保持
       const result = transformData(mockData);
       expect(result).toBe(expectedResult);
     });
   });
   ```

### GREEN阶段
1. **实现功能代码**
   ```typescript
   // src/models/[ModelName].ts
   export interface [ModelName] {
     id: string;
     name: string;
     descriptions?: string;
     specialNotes?: string;
     tags: string;
     createdDate: Date;
     creatorId: number;
     // ... 其他属性
   }
   ```

### REFACTOR阶段
1. **优化重构**
   - 添加类型工具函数
   - 优化类型继承结构
   - 添加类型守卫函数
   - 完善类型文档

### 验收标准
- [ ] 所有数据模型100%匹配
- [ ] 类型检查无错误
- [ ] 与现有测试用例兼容
- [ ] 业务逻辑正确保持
- [ ] 类型定义文档完整
- [ ] Hook Agent验证数据模型一致性
- [ ] Testcase覆盖所有数据转换场景
```

### 1.3 API契约提取和文档生成

#### 1.3.1 任务：API契约提取和文档生成 (P0)
```markdown
## 任务：API契约提取和文档生成

**优先级**：P0  
**预计时间**：3小时  
**负责人**：前端架构师  

### 任务描述
从现有系统中提取API契约，生成分离的repositories.md（前端Repository）和restful-apis.md（后端REST API）文档。

### EARS验收标准
- **Given**: 需要从现有系统提取API契约
- **When**: 执行API提取脚本
- **Then**: 应该生成分离的Repository和REST API文档
- **And**: 文档应该准确反映现有系统的接口定义

### RED阶段
1. **编写失败测试**
   ```typescript
   describe('API Contract Extraction', () => {
     it('should generate separated repository and API docs', () => {
       // 测试文档生成
       const reposExists = fs.existsSync('specs/repositories.md');
       const apisExists = fs.existsSync('specs/restful-apis.md');
       
       expect(reposExists).toBe(true);
       expect(apisExists).toBe(true);
     });
     
     it('should contain correct API contract structure', () => {
       const reposContent = fs.readFileSync('specs/repositories.md', 'utf8');
       const apisContent = fs.readFileSync('specs/restful-apis.md', 'utf8');
       
       expect(reposContent).toContain('Repository');
       expect(apisContent).toContain('RESTful API');
     });
   });
   ```

### GREEN阶段
1. **实现功能代码**
   ```bash
   # 执行API契约提取
   python3 scripts/extract-api-contracts.py \
     --source [SOURCE_PROJECT_PATH] \
     --output-repos specs/[BRANCH_NAME]/repositories.md \
     --output-apis specs/[BRANCH_NAME]/restful-apis.md
   ```

### REFACTOR阶段
1. **优化重构**
   - 验证提取的API契约准确性
   - 确保Repository和REST API文档分离清晰
   - 添加必要的业务规则说明
   - 完善文档结构和格式

### 验收标准
- [ ] 成功生成repositories.md文档
- [ ] 成功生成restful-apis.md文档
- [ ] 前端Repository接口提取完整
- [ ] 后端REST API端点提取完整
- [ ] 数据模型定义准确
- [ ] 业务规则文档化完整
- [ ] Hook Agent验证API契约准确性
- [ ] Testcase覆盖所有关键API场景
```

---

## 二、核心工具和服务开发任务

### 2.1 数据转换工具函数

#### 2.1.1 任务：数据转换工具函数实现 (P1)
```markdown
## 任务：数据转换工具函数实现

**优先级**：P1  
**预计时间**：4小时  
**负责人**：前端开发工程师  

### 任务描述
实现数据转换工具函数，确保与现有系统行为完全一致。

### EARS验收标准
- **Given**: 需要转换数据格式
- **When**: 调用转换函数
- **Then**: 应该返回正确的转换结果
- **And**: 应该保持业务逻辑一致性

### RED阶段
1. **编写失败测试**
   ```typescript
   describe('Data Transformations', () => {
     it('should transform data correctly', () => {
       const mockData = {
         id: 'test-id',
         name: 'Test Document',
         tags: '500',
         createdDate: new Date('2023-01-01'),
         creatorId: 123,
       };
       
       const result = transformData(mockData);
       expect(result).toBe(expectedResult);
     });
     
     it('should handle edge cases gracefully', () => {
       const edgeCaseData = { ...mockData, tags: '0' };
       const result = transformData(edgeCaseData);
       expect(result).toBe(expectedEdgeCaseResult);
     });
   });
   ```

### GREEN阶段
1. **实现功能代码**
   ```typescript
   // src/utils/transformations.ts
   export const transformData = (data: ExistingModel | null): number => {
     if (!data) return 0;
     
     const baseCount = parseInt(data.tags || '0', 10);
     const businessLogicValue = [BUSINESS_LOGIC_CONSTANT];
     return baseCount + businessLogicValue;
   };
   ```

### REFACTOR阶段
1. **优化重构**
   - 添加错误处理
   - 优化性能
   - 添加缓存机制
   - 完善类型定义

### 验收标准
- [ ] 所有转换函数正常工作
- [ ] 业务逻辑正确保持
- [ ] 边界情况处理正确
- [ ] 性能优化完成
- [ ] 现有测试用例通过
- [ ] Hook Agent验证转换逻辑一致性
- [ ] 独立Testcase验证所有边界情况
```

### 2.2 状态管理实现

#### 2.2.1 任务：状态管理实现 (P1)
```markdown
## 任务：状态管理实现

**优先级**：P1  
**预计时间**：6小时  
**负责人**：前端开发工程师  

### 任务描述
实现基于目标技术栈的状态管理系统，确保行为完全一致。

### EARS验收标准
- **Given**: 需要管理应用状态
- **When**: 组件订阅状态变化
- **Then**: 应该正确更新和同步状态
- **And**: 异步操作应该正常工作

### RED阶段
1. **编写失败测试**
   ```typescript
   describe('State Management', () => {
     it('should manage app state correctly', () => {
       const store = createAppStore();
       
       // 测试状态更新
       store.setAppData(mockAppData);
       expect(store.appData).toEqual(mockAppData);
       
       // 测试异步操作
       store.fetchAppData('test-id');
       expect(store.loading).toBe(true);
     });
   });
   ```

### GREEN阶段
1. **实现功能代码**
   ```typescript
   // src/stores/AppStore.ts
   import { create } from '[STATE_MANAGEMENT_LIB]';
   import { AppModel } from '@/models';
   
   interface AppStore {
     appData: AppModel | null;
     loading: boolean;
     error: string | null;
     setAppData: (appData: AppModel) => void;
     fetchAppData: (id: string) => Promise<void>;
     clearAppData: () => void;
   }
   
   export const useAppStore = create<AppStore>((set, get) => ({
     appData: null,
     loading: false,
     error: null,
     
     setAppData: (appData) => set({ appData }),
     
     fetchAppData: async (id: string) => {
       set({ loading: true, error: null });
       try {
         const response = await fetch(`/api/data/${id}`);
         const appData = await response.json();
         set({ appData, loading: false });
       } catch (error) {
         set({ error: error.message, loading: false });
       }
     },
     
     clearAppData: () => set({ appData: null, error: null })
   }));
   ```

### REFACTOR阶段
1. **优化重构**
   - 添加状态持久化
   - 优化性能
   - 添加状态中间件
   - 完善错误处理

### 验收标准
- [ ] 状态管理正常工作
- [ ] 异步操作正确处理
- [ ] 组件状态同步正常
- [ ] 错误处理完善
- [ ] 性能优化完成
- [ ] Hook Agent验证状态管理一致性
- [ ] Testcase覆盖所有状态场景
```

---

## 三、核心业务组件开发任务

### 3.1 主要业务组件实现

#### 3.1.1 任务：主要业务组件实现 (P1)
```markdown
## 任务：主要业务组件实现

**优先级**：P1  
**预计时间**：8小时  
**负责人**：前端开发工程师  

### 任务描述
实现主要的业务组件，包括核心功能，确保与现有系统行为100%一致。

### EARS验收标准
- **Given**: 用户需要使用核心功能
- **When**: 组件加载完成
- **Then**: 应该正确显示和处理业务逻辑
- **And**: 所有交互功能应该正常工作

### RED阶段
1. **编写失败测试**
   ```typescript
   describe('Main Business Component', () => {
     let component: MainBusinessComponent;
     let store: MockAppStore;
     
     beforeEach(() => {
       store = createMockAppStore();
       render(
         <AppStoreProvider store={store}>
           <MainBusinessComponent id="test-id" />
         </AppStoreProvider>
       );
       component = screen.getByTestId('main-business-component');
     });
     
     it('should display business information correctly', () => {
       expect(screen.getByText('Test Business Item')).toBeInTheDocument();
       expect(screen.getByText('Business Category')).toBeInTheDocument();
     });
     
     it('should handle core interactions', async () => {
       const actionButton = screen.getByRole('button', { name: /action/i });
       await userEvent.click(actionButton);
       
       expect(store.performAction).toHaveBeenCalledWith('test-id');
     });
   });
   ```

### GREEN阶段
1. **实现功能代码**
   ```typescript
   // src/components/MainBusinessComponent.tsx
   import React, { useEffect } from 'react';
   import { useAppStore } from '@/stores';
   import { transformData } from '@/utils';
   
   interface MainBusinessComponentProps {
     id: string;
   }
   
   export const MainBusinessComponent: React.FC<MainBusinessComponentProps> = ({ id }) => {
     const { appData, loading, error, fetchAppData } = useAppStore();
     
     useEffect(() => {
       fetchAppData(id);
     }, [id]);
     
     if (loading) return <div>Loading...</div>;
     if (error) return <div>Error: {error}</div>;
     if (!appData) return <div>Data not found</div>;
     
     const transformedValue = transformData(appData);
     
     return (
       <div className="main-business-component" data-testid="main-business-component">
         <div className="business-header">
           <h1>{appData.name}</h1>
           <div className="business-meta">
             <span>Category: {appData.category}</span>
             <span>Value: {transformedValue}</span>
           </div>
         </div>
         
         <div className="business-content">
           {/* Business logic implementation */}
         </div>
         
         <div className="business-actions">
           <button onClick={() => handleAction(id)}>
             Action
           </button>
         </div>
       </div>
     );
   };
   ```

### REFACTOR阶段
1. **优化重构**
   - 添加错误边界
   - 优化性能
   - 添加加载状态
   - 完善无障碍性

### 验收标准
- [ ] 业务信息正确显示
- [ ] 核心功能正常工作
- [ ] 交互功能正常工作
- [ ] 数据转换逻辑正确
- [ ] 性能优化完成
- [ ] Hook Agent验证组件行为一致性
- [ ] Testcase覆盖所有用户交互场景
```

## 四、测试和优化任务

### 4.1 单元测试和集成测试

#### 4.1.1 任务：单元测试和集成测试 (P1)
```markdown
## 任务：单元测试和集成测试

**优先级**：P1  
**预计时间**：8小时  
**负责人**：测试工程师  

### 任务描述
编写全面的单元测试和集成测试，确保测试覆盖率达到90%以上。

### EARS验收标准
- **Given**: 需要验证代码质量
- **When**: 运行测试套件
- **Then**: 应该所有测试通过
- **And**: 测试覆盖率应该达标

### RED阶段
1. **编写测试用例**
   ```typescript
   // src/components/__tests__/MainBusinessComponent.test.tsx
   describe('MainBusinessComponent', () => {
     it('should render loading state initially', () => {
       render(<MainBusinessComponent id="test-id" />);
       expect(screen.getByText('Loading...')).toBeInTheDocument();
     });
     
     it('should render business information when loaded', async () => {
       const mockData = createMockBusinessData();
       mockAppStore.getState().setAppData(mockData);
       
       render(<MainBusinessComponent id="test-id" />);
       
       await waitFor(() => {
         expect(screen.getByText(mockData.name)).toBeInTheDocument();
       });
     });
   });
   ```

### GREEN阶段
1. **实现测试代码**
   ```typescript
   // 继续编写更多测试用例
   // 配置测试框架
   // 设置测试覆盖率
   ```

### REFACTOR阶段
1. **优化重构**
   - 优化测试性能
   - 添加Mock数据
   - 完善测试工具函数
   - 优化测试配置

### 验收标准
- [ ] 所有单元测试通过
- [ ] 测试覆盖率≥90%
- [ ] 集成测试通过
- [ ] E2E测试通过
- [ ] 性能测试通过
- [ ] Hook Agent验证测试完整性
- [ ] Testcase与Task关联100%覆盖
```

## 五、任务执行计划

### 5.1 时间安排

| 阶段 | 任务 | 预计时间 | 负责人 |
|------|------|----------|--------|
| 第一阶段 | 基础设施搭建 | 10小时 | 前端架构师 |
| 第二阶段 | 工具和服务实现 | 10小时 | 前端开发工程师 |
| 第三阶段 | 核心组件开发 | 14小时 | 前端开发工程师 |
| 第四阶段 | 测试和优化 | 16小时 | 测试工程师 |
| 第五阶段 | 部署配置 | 4小时 | DevOps工程师 |

**总计**: 54小时 (约1.5周)

### 5.2 依赖关系

```
基础设施搭建 → 工具和服务实现 → 核心组件开发 → 测试和优化 → 部署配置
```

## 六、任务验收标准

### 6.1 功能验收标准
- [ ] 所有功能与现有系统100%一致
- [ ] 用户界面响应正常
- [ ] 数据转换逻辑正确
- [ ] 错误处理完善

### 6.2 技术验收标准
- [ ] 代码质量通过检查
- [ ] 测试覆盖率≥90%
- [ ] 性能指标满足要求
- [ ] 无障碍性合规

### 6.3 业务验收标准
- [ ] 用户满意度≥85%
- [ ] 系统稳定性≥99.9%
- [ ] 移动端兼容性100%
- [ ] 第三方集成正常

---

**重构任务文档说明**: 本任务文档基于重构需求制定，严格遵循TDD开发流程，确保代码质量和功能完整性。所有任务都包含完整的RED-GREEN-REFACTOR步骤和验收标准。

---

## 七、开发指南

### 7.1 技术栈要求
- **目标框架**: [TARGET_FRAMEWORK] 
- **状态管理**: [STATE_MANAGEMENT_LIB]
- **构建工具**: [BUILD_TOOL]
- **测试框架**: [TESTING_FRAMEWORK]
- **样式方案**: [STYLING_SOLUTION]

### 7.2 代码规范
- **TypeScript**: 严格模式，所有类型必须明确定义
- **组件模式**: 函数组件 + Hooks
- **样式**: [STYLING_APPROACH]
- **测试**: [TESTING_APPROACH]

### 7.3 质量保证
- **测试覆盖率**: ≥90%
- **类型检查**: 0错误
- **代码风格**: [LINTING_TOOL]
- **性能**: [PERFORMANCE_REQUIREMENTS]

### 7.4 任务执行顺序
```
1. API-EXTRACT-001 → API契约提取（分离生成repositories.md和restful-apis.md）
2. SETUP-001 → 项目基础架构
3. MODELS-001 → 数据模型定义
4. UTILS-001 → 工具函数实现
5. STORE-001 → 状态管理实现
6. COMPONENTS-001 → 核心组件开发
7. TESTS-001 → 测试用例编写
8. DEPLOY-001 → 部署配置
```

## 八、验证机制集成

### 8.1 Task-Testcase关联机制

每个Task必须通过以下验证机制：

#### 强验证规则
- **Task创建时**: 必须关联FR/UserRequirement和至少一个Testcase
- **Task执行时**: Hook Agent实时监控执行过程
- **Task完成时**: 所有关联Testcase必须通过验证
- **自验证禁止**: AI不能验证自己创建的Task

#### 验证流程
```typescript
// Task创建验证
const taskValidation = await hookAgent.validateTaskCreation(task, context);
if (!taskValidation.isValid) {
  throw new Error('Task validation failed: ' + taskValidation.errors.map(e => e.message).join(', '));
}

// Task执行验证
const executionValidation = await hookAgent.validateTaskExecution(taskId, execution);
if (!executionValidation.isValid) {
  await handleValidationFailure(executionValidation);
}

// Task完成验证
const completionValidation = await hookAgent.validateTaskCompletion(taskId, results);
if (!completionValidation.isValid) {
  throw new Error('Task completion validation failed');
}
```

### 8.2 Hook验证Agent配置

#### Agent启用配置
```yaml
# .specify/hook-validation-config.yaml
validation:
  enabled: true
  strict_mode: true
  agents:
    task_creation: Hook-Validation-Agent-v1
    task_execution: Hook-Validation-Agent-v1
    task_completion: Hook-Validation-Agent-v1
  
rules:
  # 强验证规则
  task_must_have_testcase: true
  testcase_must_have_expected_result: true
  independent_validation_required: true
  complete_verification_required: true
  
  # 纠正机制
  auto_correction: false
  detailed_suggestions: true
  failure_escalation: true
```

### 8.3 验证失败处理机制

#### 失败处理流程
1. **问题识别**: Hook Agent识别验证失败的具体原因
2. **根本原因分析**: 分析失败的技术或业务原因
3. **纠正建议生成**: 提供具体的纠正措施
4. **重新验证**: 执行纠正后重新验证

#### 纠正建议示例
```typescript
interface CorrectionPlan {
  taskId: string;
  issues: ValidationIssue[];
  corrections: CorrectionAction[];
  verificationSteps: string[];
}

interface CorrectionAction {
  type: 'ADD_TESTCASE' | 'MODIFY_IMPLEMENTATION' | 'UPDATE_REQUIREMENTS';
  description: string;
  priority: 'HIGH' | 'MEDIUM' | 'LOW';
  estimatedTime: number;
}
```

### 8.4 验证报告生成

#### 自动验证报告
每个Task完成后生成详细验证报告：
- **Task信息**: ID、描述、关联的FR/UserRequirement
- **验证结果**: 总体状态、详细验证项
- **Testcase结果**: 所有关联Testcase的执行情况
- **问题分析**: 失败原因和影响范围
- **纠正建议**: 具体的改进措施

#### 报告格式
```markdown
# Task验证报告：[TASK_ID]

## 基本信息
- **Task ID**: [TASK_ID]
- **Task描述**: [TASK_DESCRIPTION]
- **FR ID**: [FR_ID]
- **UserRequirement ID**: [UR_ID]
- **验证时间**: [TIMESTAMP]
- **验证Agent**: [AGENT_NAME]

## 验证结果
- **总体状态**: ✅ PASS / ❌ FAIL
- **Testcase数量**: [COUNT]
- **通过数量**: [COUNT]
- **失败数量**: [COUNT]
- **通过率**: [PERCENTAGE]%

## Testcase详情
| Testcase_ID | 状态 | 预期结果 | 实际结果 | 验证时间 |
|-------------|------|----------|----------|----------|
| [TC_ID] | ✅/❌ | [EXPECTED] | [ACTUAL] | [TIME] |

## 问题分析
[详细的问题分析]

## 纠正建议
[具体的纠正建议]
```

---

**重构模板说明**: 本模板已更新为实用的TDD开发模式，去除了理论化的验证命令，专注于实际开发任务和可执行的代码实现。每个任务都包含完整的RED-GREEN-REFACTOR步骤和明确的验收标准。