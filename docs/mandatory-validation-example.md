# 强制需求验证流程示例

## 完整工作流程

### 第1步：创建精确的测试用例
```bash
# 为用户认证功能创建测试用例
/test-cases UserAuthenticationSystem
```

这会生成包含以下内容的测试用例文档：
- 精确的需求定义章节
- 具体的测试用例表格
- 可验证的验收标准

### 第2步：完成需求定义
在生成的测试用例文档中，详细填写：

1. **🔍 Precision Requirements Definition** 章节：
   - 业务需求分析
   - 功能需求精确定义
   - 非功能需求精确定义

2. **测试用例表格**：
   - 每个测试用例都有具体的前置条件
   - 详细的测试数据集（包括正例、反例、边界值）
   - 精确的执行步骤
   - 可量化的预期结果
   - 明确的验证标准

### 第3步：强制验证检查
```bash
# 验证需求定义是否达到实现标准
/validate-requirements specs/001-test-user-authentication-system/
```

#### 验证结果示例：

**✅ PASS (≥85分)**：
```
=== VALIDATION RESULTS ===
Status: PASS
Overall Score: 88/100
Breakdown:
  Completeness: 28/30
  Precision: 26/30
  Traceability: 18/20
  Quality: 16/20

Certificate: specs/001-test-user-authentication-system/validation-certificate.md
```

**⚠️ WARNING (70-84分)**：
```
=== VALIDATION RESULTS ===
Status: WARNING
Overall Score: 76/100
Issues Found:
  - PRECISION: Found ambiguous language (fast, good, user-friendly, etc.)
  - COMPLETENESS: Missing performance metrics
```

**❌ FAIL (<70分)**：
```
=== VALIDATION RESULTS ===
Status: FAIL
Overall Score: 62/100
Issues Found:
  - COMPLETENESS: Missing precision requirements definition section
  - PRECISION: Missing specific test data
  - QUALITY: Found placeholder expected results
```

### 第4步：验证证书生成

验证成功后，会自动生成 `validation-certificate.md`：

```markdown
# Requirements Validation Certificate

**Validation Date**: 2025-01-15 10:30:45
**Test Cases File**: test-cases.md
**Overall Score**: 88/100
**Status**: PASS

## Score Breakdown
- **Completeness**: 28/30
- **Precision**: 26/30
- **Traceability**: 18/20
- **Quality**: 16/20

## Validation Status: PASS

### ✅ Requirements Approved for Implementation

The requirements definition has passed mandatory validation and is ready for implementation.

**Next Steps**:
- Proceed to implementation phase
- Use this certificate as approval to begin coding
- All implementations must pass the defined test cases
```

### 第5步：实施阶段（需要验证证书）

现在可以安全地进行实现：

```bash
# 实现用户认证系统
/implement UserAuthenticationSystem
```

在实现过程中，AI会：
1. **检查验证证书**：确保存在有效的PASS证书
2. **遵循精确测试用例**：基于精确定义的需求进行实现
3. **通过测试验证**：确保实现通过所有测试用例

## 验证机制的关键特性

### 1. 强制检查点
- **实现被阻止**：没有PASS状态的验证证书，无法开始实现
- **质量门槛**：必须达到85分以上才能通过验证
- **全面检查**：覆盖完整性、精确性、可追溯性和质量

### 2. 评分标准
- **完整性 (30分)**：测试用例覆盖、需求定义完整性
- **精确性 (30分)**：具体、可衡量的需求定义
- **可追溯性 (20分)**：需求与测试用例的双向链接
- **质量 (20分)**：无歧义、完整覆盖

### 3. 自动检测的问题
- ❌ 模糊语言（"快速"、"良好"、"用户友好"）
- ❌ 占位符内容（`[具体描述]`、`[测试数据]`）
- ❌ 缺失的精度定义部分
- ❌ 未解决的NEEDS CLARIFICATION标记
- ❌ 缺失性能指标
- ❌ 缺失错误处理定义

### 4. 质量保证
- **预防性控制**：在实现开始前发现问题
- **标准强制执行**：确保所有需求都达到相同的质量标准
- **自动验证**：消除人为判断的主观性
- **渐进式改进**：明确指出需要改进的具体方面

## 为什么这能解决4轮失败问题

### 之前的流程
```
模糊需求 → AI理解有偏差 → 错误实现 → 失败
```

### 新的流程
```
模糊需求 → 精确测试用例 → 强制验证 → 质量门槛 → 精确实现 → 成功
```

### 关键改进
1. **精确性**：消除模糊性和解释空间
2. **验证**：强制质量检查，防止不合格的需求进入实现阶段
3. **标准**：统一的质量标准，确保所有需求都达到可实现的精确度
4. **预防**：在实现开始前发现问题，而不是在实现后发现错误

## 实际应用示例

### 用户登录功能

**模糊需求**：
```
REQ-001: When a user submits valid login credentials, the system shall authenticate them and grant access
```

**经过验证的精确需求**：
```
TC-AUTH-001: 用户使用有效凭据登录成功
- 前置条件: 用户test@example.com已注册，系统正常运行
- 测试数据集: 
  * {"email": "test@example.com", "password": "ValidPass123!"}
  * {"email": "invalid", "password": "short"}
  * {"email": "a@b.co", "password": "A1!aaaaa"}
- 执行步骤: 1. 输入邮箱 2. 输入密码 3. 点击登录
- 预期结果: HTTP 200, JWT令牌，24小时有效期
- 验证标准: 响应时间<500ms，令牌验证通过

验证结果: PASS (92/100)
```

有了这样的精确需求定义和验证通过，AI就不再有"自认为完美但实际不可用"的问题了。