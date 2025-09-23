# 增强重构模板 - 强制验证和渐进式重构

**模板版本**: 2.0  
**改进重点**: 强制验证、渐进式重构、真实性保证  
**适用场景**: 任何需要高质量重构的项目

## 🎯 核心改进

### 1. 强制验证机制
- **数据真实性验证**: 禁止Mock数据，强制真实API集成
- **行为保持验证**: 确保新旧系统行为100%一致
- **接口稳定性验证**: 防止不兼容的接口变更

### 2. 渐进式重构强制执行
- **阶段锁机制**: 必须按顺序执行各个阶段
- **API契约要求**: 必须提取API契约才能开始重构
- **并行验证**: 新旧系统必须并行运行验证

### 3. 真实性检查点
- **API集成验证**: 检测真实API调用
- **业务逻辑验证**: 验证逻辑完整性
- **用户交互验证**: 确保真实用户交互

## 📋 重构流程

### 阶段1: 基线验证（强制）
```bash
# 必须执行的基线验证
specify refactoring baseline --component ViewAppFile --original ./angular --refactored ./react
specify refactoring reality-check --fail-on-mock
```

**验证内容**:
- [ ] 数据真实性验证（100%真实API）
- [ ] 行为基线测试
- [ ] 接口稳定性检查
- [ ] 性能基准建立

### 阶段2: 兼容层创建（强制）
```bash
# 必须创建兼容层
specify refactoring progressive compatibility --component ViewAppFile
```

**验证内容**:
- [ ] API兼容层实现
- [ ] 组件接口包装器
- [ ] 状态管理桥接
- [ ] 错误处理兼容

### 阶段3: 组件替换（渐进式）
```bash
# 逐个组件替换
specify refactoring progressive component-replace --component ViewAppFile
specify refactoring progressive component-replace --component ViewAppFilesOwner
```

**验证内容**:
- [ ] 单个组件替换
- [ ] 行为一致性验证
- [ ] 性能回归测试
- [ ] 集成测试通过

### 阶段4: 并行验证（强制）
```bash
# 强制并行验证
specify refactoring progressive parallel-validation --duration 7days
```

**验证内容**:
- [ ] 新旧系统并行运行
- [ ] 行为一致性监控
- [ ] 性能对比验证
- [ ] 用户反馈收集

## 🔧 验证机制

### 自动验证检查点
```python
# 数据真实性验证
def validate_data_reality(code):
    mock_patterns = ['mockData', 'fakeData', 'dummyData']
    real_patterns = ['await fetch', 'axios.', 'api.']
    
    if has_mock_patterns(code) and not has_real_patterns(code):
        raise ValidationError("检测到Mock数据但无真实API调用")
    
    return True
```

### 强制验证命令
```bash
# 完整验证流程
specify refactoring validate ./my-project --fail-on-error --verbose

# 现实检查
specify refactoring reality-check ./my-project --pattern "*.tsx" --fail-on-mock

# 基线对比
specify refactoring baseline --component ViewAppFile --original ./angular --refactored ./react
```

## 📊 验证报告

### 自动生成的验证报告
```markdown
# 重构验证报告

## 总体结果
- 总验证数: 45
- 通过: 42
- 失败: 3
- 错误: 1
- 警告: 2

## 详细结果
❌ **检测到Mock数据但无真实API调用: src/components/ViewAppFile.tsx**
   详情: {"mock_patterns": ["mockData"], "real_patterns": []}

⚠️ **未检测到真实业务逻辑: src/services/ApiService.ts**
   详情: {"placeholders": ["TODO"], "real_logic": []}

✅ 数据真实性验证通过: src/components/ViewAppFilesOwner.tsx
   详情: {"mock_patterns": [], "real_patterns": ["await fetch"]}
```

## 🚫 禁止的模式

### Mock数据模式（严格禁止）
```typescript
// ❌ 禁止
const mockAppFiles: AppFileDL[] = [
  { id: 1, name: "术后康复指导", /*...全部假数据 */ }
]

// ❌ 禁止
const mockApi = vi.spyOn(api, 'GetAllSharedAppFiles')
mockApi.mockResolvedValue(mockData)

// ✅ 允许（仅用于测试）
const realApiResponse = await fetch('/api/FeatureModules/AppFiles/GetAllSharedAppFiles/7')
```

### 占位符模式（严格禁止）
```typescript
// ❌ 禁止
const GoToShareIt = () => {
  // TODO: 实现分享功能
  alert("分享功能已触发")
}

// ❌ 禁止
if (isValid) {
  // TODO: 实现验证逻辑
  return true
}

// ✅ 允许
const GoToShareIt = async () => {
  try {
    const result = await WeChatService.shareToWeChat(shareData)
    return result
  } catch (error) {
    ErrorHandler.handle(error)
  }
}
```

## 🛡️ 质量保证

### 自动化质量检查
1. **代码扫描**: 自动检测Mock数据和占位符
2. **API验证**: 确保所有API调用都是真实的
3. **行为对比**: 新旧系统行为一致性检查
4. **性能监控**: 重构前后性能对比

### 持续集成验证
```yaml
# CI/CD 配置示例
validation_steps:
  - name: "Reality Check"
    command: "specify refactoring reality-check --fail-on-mock"
  
  - name: "Behavior Validation"
    command: "specify refactoring validate --fail-on-error"
  
  - name: "Performance Test"
    command: "specify refactoring baseline --component ViewAppFile"
```

## 📈 成功指标

### 量化目标
- **数据真实性**: 100% 真实API调用
- **行为保持**: 100% 行为一致性
- **验证通过率**: > 95%
- **重构失败率**: < 5%

### 质量目标
- **用户满意度**: > 90%
- **系统稳定性**: > 99.9%
- **性能回归**: < 2%
- **错误率**: < 0.1%

## 🔄 回滚机制

### 自动回滚触发条件
1. **验证失败**: 任何关键验证失败时自动回滚
2. **性能下降**: 性能下降超过阈值时回滚
3. **用户投诉**: 用户反馈问题时回滚

### 回滚命令
```bash
# 紧急回滚
specify refactoring progressive --phase rollback --component ViewAppFile

# 部分回滚
specify refactoring progressive --phase partial-rollback --component ViewAppFile
```

---

**重要提醒**: 此模板强制执行重构质量标准，任何违反验证规则的重构都将被阻止。请确保遵循渐进式重构流程，保证重构质量。

*基于 ViewAppFilesBiz 重构失败经验教训设计*