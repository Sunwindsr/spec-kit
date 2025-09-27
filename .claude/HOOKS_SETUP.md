# Enhanced TDD Validation System - Claude Code Hooks Setup

这个配置脚本为 Claude Code 配置了增强的 TDD 验证系统 hooks，可以防止 AI 自欺欺人地标记任务完成。

## 🎯 功能概述

系统通过以下机制防止 AI 自欺欺人：

1. **Pre-Task Completion Hook**: 在任务完成前进行强制验证
2. **Pre-Commit Hook**: 提交前进行全面验证
3. **Task Status Change Hook**: 验证任务状态变更
4. **Phase Transition Hook**: 验证阶段转换

## 🚀 快速配置

### 方法 1: 使用配置脚本（推荐）

```bash
# 运行自动化配置脚本
./scripts/bash/configure-claude-code-hooks.sh

# 验证安装
./.claude/verify-installation.sh
```

### 方法 2: 手动配置

1. **创建 hooks 配置文件**：
   ```json
   {
     "hooks": {
       "pre_task_completion": "python3 /home/sd_dev/projects/spec-kit/src/specify_cli/enhanced_tdd_validation_system.py --validate-task ${TASK_ID} --task-data '${TASK_DATA}'",
       "pre_commit": "python3 /home/sd_dev/projects/spec-kit/src/specify_cli/enhanced_tdd_validation_system.py --comprehensive",
       "task_status_change": "python3 /home/sd_dev/projects/spec-kit/src/specify_cli/hooks/claude_code_hooks.py task_status_change --task-id ${TASK_ID} --old-status ${OLD_STATUS} --new-status ${NEW_STATUS} --project-path ${PROJECT_PATH}",
       "phase_transition": "python3 /home/sd_dev/projects/spec-kit/src/specify_cli/hooks/claude_code_hooks.py phase_transition --from-phase ${FROM_PHASE} --to-phase ${TO_PHASE} --project-path ${PROJECT_PATH}"
     }
   }
   ```

2. **重启 Claude Code** 以加载 hooks

## 🔍 验证流程

### Pre-Task Completion 验证
当尝试标记任务完成时，系统会进行以下验证：

1. **任务流验证**: 检查依赖关系和阶段规则
2. **增强审查**: 运行代码质量检查和行为验证
3. **现实测试**: 验证测试结果和证据
4. **质量门禁**: 运行代码质量和安全扫描
5. **行为一致性**: 验证实际行为与期望行为

### 示例验证数据
```json
{
  "requires_tests": true,
  "test_results": [
    {
      "test_id": "test_user_creation",
      "status": "passed",
      "evidence_link": "test-reports/user_creation.log",
      "execution_time": 1.2
    }
  ],
  "expected_behavior": "User can be created successfully",
  "validation_requirements": ["test_results", "quality_gates"]
}
```

## 📊 验证阈值

系统使用以下严格阈值：

- **测试通过率**: 95% (最低要求)
- **代码覆盖率**: 80% (建议)
- **性能基准**: 不超过基线 1.0x
- **安全扫描**: 零严重和高危问题

## 🛡️ 质量门禁

系统包含以下质量门禁：

1. **代码检查**: Linting 和格式化
2. **类型安全**: 类型检查
3. **测试覆盖率**: 代码覆盖率分析
4. **安全扫描**: 安全漏洞检测
5. **性能基准**: 性能回归检测

## 🔧 配置选项

### 严格模式 (推荐)
```json
{
  "validation": {
    "strict_mode": true,
    "auto_rollback_enabled": true,
    "require_evidence": true
  }
}
```

### 开发模式
```json
{
  "validation": {
    "strict_mode": false,
    "auto_rollback_enabled": false,
    "require_evidence": true
  }
}
```

## 📋 使用示例

### 1. 测试任务验证
```bash
# 测试单个任务验证
python3 src/specify_cli/enhanced_tdd_validation_system.py \
  --validate-task T001 \
  --task-data '{"requires_tests": true, "test_results": [...]}'
```

### 2. 全面验证
```bash
# 运行全面项目验证
python3 src/specify_cli/enhanced_tdd_validation_system.py --comprehensive
```

### 3. 系统状态
```bash
# 检查系统状态
python3 src/specify_cli/enhanced_tdd_validation_system.py --status
```

## 🚨 验证失败处理

当验证失败时，系统会：

1. **阻止任务完成**: 防止标记未经验证的任务为完成
2. **提供详细错误**: 列出所有验证失败的原因
3. **建议解决方案**: 提供修复建议
4. **自动回滚**: 在严格模式下回滚到稳定状态

## 📈 监控和报告

系统提供：

- **实时验证状态**: 每个任务的验证进度
- **详细报告**: JSON 格式的验证结果
- **历史记录**: 验证历史和趋势分析
- **指标收集**: 验证时间和成功率统计

## 🔄 集成工作流

### 标准 TDD 工作流
1. **编写测试**: 创建失败的测试
2. **实现功能**: 编写代码使测试通过
3. **验证完成**: 通过 hook 验证任务完成
4. **提交代码**: 通过 pre-commit hook 验证

### 验证工作流
```
开始任务 → 编写测试 → 实现功能 → 
  ↓                              ↑
验证 ←─ Hook 验证 ←─ 尝试完成 ←─┘
  ↓
通过 → 提交 → 下一阶段
  ↓
失败 → 修复 → 重新验证
```

## 🛠️ 故障排除

### 常见问题

1. **Hooks 未加载**: 重启 Claude Code
2. **Python 路径错误**: 确保 python3 可用
3. **权限问题**: 确保 hooks 脚本有执行权限
4. **配置文件错误**: 检查 JSON 格式

### 调试命令

```bash
# 检查 hooks 配置
cat .claude/hooks.json

# 测试验证系统
python3 src/specify_cli/enhanced_tdd_validation_system.py --help

# 运行安装验证
./.claude/verify-installation.sh
```

## 📚 相关文档

- [任务模板](../templates/tasks-template.md) - 包含验证要求的任务模板
- [验证系统](../src/specify_cli/validation/) - 验证系统源代码
- [Hook 系统](../src/specify_cli/hooks/) - Hook 系统源代码
- [流程控制](../src/specify_cli/flow_control/) - 任务流程控制

---

## ⚠️ 重要提醒

1. **重启 Claude Code**: 配置 hooks 后需要重启 Claude Code
2. **测试验证**: 在生产环境使用前先测试验证功能
3. **监控日志**: 查看 Claude Code 输出以了解验证结果
4. **定期更新**: 保持验证系统为最新版本

这个配置确保了 AI 无法再通过生成大量文档来"自欺欺人"，每个任务完成都必须经过严格的验证，包括测试结果验证、证据检查、质量门禁等多重保障。