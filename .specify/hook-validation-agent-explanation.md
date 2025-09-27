# Hook验证Agent实现说明

## 概念理解

Hook验证Agent是基于Claude Code的hook机制，**不是**独立的Node.js应用。它的核心作用是：

1. **规范约束**: 通过配置文件和模板约束AI的行为
2. **自动触发**: 在任务执行过程中自动触发验证
3. **独立验证**: 防止AI自验证，确保质量
4. **纠错机制**: 验证失败时自动提供纠正建议

## 实现方式

### 1. 基于Claude Code的Hook机制

Hook验证Agent通过以下方式工作：

- **配置驱动**: 通过`.specify/hook-validation-config.yaml`配置验证规则
- **模板约束**: 通过模板系统约束AI生成内容的质量
- **工作流集成**: 在Task-Testcase工作流中集成验证点
- **独立验证**: 确保验证逻辑独立于业务逻辑

### 2. 配置文件结构

```yaml
# .specify/hook-validation-config.yaml
validation:
  enabled: true
  strict_mode: true
  auto_correction: true
  
rules:
  task_must_have_testcase: true
  testcase_must_have_expected_result: true
  independent_validation_required: true
```

### 3. 在Claude Code中的使用方式

Hook验证Agent在Claude Code中通过以下方式触发：

1. **Task创建时**: 验证Task是否有关联的Testcase
2. **Task执行时**: 验证执行过程是否符合规范
3. **Task完成时**: 验证Testcase结果是否通过

### 4. 验证流程

```typescript
// 在Claude Code中的验证逻辑
async function validateTaskWithHook(task: Task) {
  // 1. 检查配置
  const config = loadHookValidationConfig();
  
  // 2. 执行验证
  const validationResult = await hookAgent.validateTaskCreation(task, context);
  
  // 3. 处理验证结果
  if (!validationResult.isValid) {
    const correctionPlan = await hookAgent.generateCorrectionPlan(validationResult);
    // 自动或手动纠正
  }
  
  return validationResult;
}
```

## 与传统验证的区别

### 传统验证（已废弃）
- 独立的Node.js应用
- 需要额外的运行时环境
- 复杂的部署和配置
- 与Claude Code分离

### Hook验证Agent（正确方式）
- 基于Claude Code的hook机制
- 无需额外运行时环境
- 配置驱动，简单易用
- 深度集成到开发流程

## 实际应用场景

### 1. Task创建验证
当AI创建Task时，Hook验证Agent会：
- 检查Task是否有关联的Testcase
- 验证Task描述的完整性
- 确保Task与FR/UserRequirement关联

### 2. Task执行验证
当AI执行Task时，Hook验证Agent会：
- 监控执行过程
- 检查是否符合TDD原则
- 验证代码质量

### 3. Task完成验证
当AI完成Task时，Hook验证Agent会：
- 验证Testcase是否通过
- 检查功能实现是否完整
- 生成验证报告

## 配置示例

### 基础配置
```yaml
validation:
  enabled: true
  strict_mode: true
  
rules:
  task_must_have_testcase: true
  testcase_must_have_expected_result: true
```

### 高级配置
```yaml
validation:
  enabled: true
  strict_mode: true
  auto_correction: true
  
rules:
  task_must_have_testcase: true
  testcase_must_have_expected_result: true
  independent_validation_required: true
  complete_verification_required: true
  
correction:
  enabled: true
  max_retries: 3
  auto_fix_missing_testcases: true
```

## 总结

Hook验证Agent的核心是：
1. **基于Claude Code hook机制**
2. **配置驱动的验证**
3. **防止AI自验证**
4. **深度集成到开发流程**

这种实现方式符合"少脚本、多规范+AI"的理念，不需要额外的运行时环境，通过规范和配置来约束AI行为。