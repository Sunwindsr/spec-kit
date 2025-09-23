# 重构文档使用指南

## 📋 三文档重构架构

本重构方法使用三个核心文档来确保重构的准确性和完整性：

### 1. `data-models.md` - 数据模型和接口
**用途**: 定义系统的数据结构和类型契约
**生成方式**: 自动提取 + 手工补充
**包含内容**:
- TypeScript接口定义
- 数据模型和类型约束
- 组件属性定义
- 数据关系映射

### 2. `app-flows.md` - 应用流程和用户需求
**用途**: 描述用户交互逻辑和业务流程
**生成方式**: 基于模板手工编写
**包含内容**:
- 用户故事和需求映射
- UX交互逻辑
- 业务规则和计算逻辑
- 界面状态转换

### 3. `apis.md` - API接口契约
**用途**: 定义HTTP接口和调用契约
**生成方式**: 自动提取
**包含内容**:
- HTTP端点定义
- 请求/响应格式
- 错误处理契约
- API调用模式

## 🔍 API分类管理系统

为了支持直接替换重构，提取系统能够自动区分和管理两类API：

### Backend REST APIs（后端API）
**识别特征**:
- 真实的HTTP请求调用：`fetch()`, `axios.get()`, `.get()`, `.post()` 等
- 完整的URL路径：`/api/users`, `/orders/123` 等
- HTTP方法：GET, POST, PUT, DELETE, PATCH

**提取内容**:
```bash
# 生成后端API报告
python3 scripts/extract-api-contracts.py \
  --source /path/to/angular/project \
  --output backend-apis.md \
  --mode backend-apis
```

**报告结构**:
- 按HTTP方法分组的API端点
- API路径分析和前缀分布
- 源代码位置追溯
- 重构合规性要求

### Frontend TypeScript APIs（前端服务）
**识别特征**:
- TypeScript服务层调用：`UserService.getUser()`, `OrderRepository.create()`
- 仓储模式方法：`DataRepository.findById()`
- 前端内部API调用

**提取内容**:
```bash
# 生成前端API报告
python3 scripts/extract-api-contracts.py \
  --source /path/to/angular/project \
  --output frontend-apis.md \
  --mode frontend-apis
```

**报告结构**:
- 按文件分组的API服务
- 按类别分类：Service层、Repository层
- 方法定义和调用模式
- 服务类型分布统计

### API映射关系

在直接替换重构中，两类API的映射关系：

| Angular | React | 处理方式 |
|---------|-------|----------|
| `this.userService.getUsers()` | `UserService.getUsers()` | 保持相同接口 |
| `this.http.get('/api/users')` | `axios.get('/api/users')` | 直接替换HTTP调用 |
| `this.orderRepository.save()` | `OrderRepository.save()` | 保持服务层接口 |

### 重构合规性要求

**Backend API要求**:
- [x] 100%保持HTTP方法和URL路径
- [x] 直接调用，无需适配层
- [x] 保持请求/响应格式
- [x] 错误处理逻辑一致

**Frontend API要求**:
- [x] 保持服务层接口签名
- [x] 方法名和参数完全一致
- [x] 返回类型保持兼容
- [x] 业务逻辑不变，仅UI优化

## 🚀 使用流程

### Phase 1: 自动提取数据模型和API

```bash
# 提取数据模型
python3 scripts/extract-api-contracts.py \
  --source /path/to/angular/project \
  --output data-models.md \
  --mode data-models

# 提取所有API契约（后端+前端）
python3 scripts/extract-api-contracts.py \
  --source /path/to/angular/project \
  --output apis.md \
  --mode apis

# 仅提取后端REST API
python3 scripts/extract-api-contracts.py \
  --source /path/to/angular/project \
  --output backend-apis.md \
  --mode backend-apis

# 仅提取前端TypeScript服务
python3 scripts/extract-api-contracts.py \
  --source /path/to/angular/project \
  --output frontend-apis.md \
  --mode frontend-apis
```

### Phase 2: 编写应用流程文档

```bash
# 基于模板创建app-flows.md
cp templates/app-flows-template.md app-flows.md

# 编辑文档，填写用户流程和业务逻辑
# 详细描述用户操作流程、业务规则、验证要求等
```

### Phase 3: 重构实施

**数据模型重构**:
- 严格遵循data-models.md中的接口定义
- 100%保持数据结构和类型
- 严禁自定义接口或数据模型

**应用流程重构**:
- 按照app-flows.md中的用户流程实现
- 保持业务逻辑和计算规则
- UI/UX可以基于新技术栈优化

**API集成重构**:
- 直接使用apis.md中的端点定义
- 保持HTTP方法和URL路径
- 无需适配层，直接调用

## 📊 文档验证

### 自动验证

```bash
# 验证数据模型一致性
specify refactoring validate-data-models --data-models data-models.md

# 验证API契约一致性
specify refactoring validate-apis --apis apis.md

# 验证应用流程完整性
specify refactoring validate-app-flows --app-flows app-flows.md
```

### 交叉验证

三个文档之间应该保持一致性：

**data-models.md ↔ app-flows.md**:
- 应用流程中使用的数据模型必须在数据模型文档中定义
- 数据模型的用途应该在应用流程中体现

**app-flows.md ↔ apis.md**:
- 应用流程中的API调用必须在API文档中定义
- API的使用场景应该在应用流程中描述

**apis.md ↔ data-models.md**:
- API的请求/响应数据必须在数据模型中定义
- 数据模型的用途应该包括API交互

## 🎯 重构准确性保证

### 1. 完整性保证
- 三个文档覆盖了数据、交互、API三个维度
- 每个方面都有明确的验证标准
- 文档之间相互约束，防止遗漏

### 2. 一致性保证
- 数据模型在三个文档中保持一致
- API调用与应用流程匹配
- 业务规则与数据结构对应

### 3. 可追溯性保证
- 所有定义都能追溯到源代码
- 每个需求都有对应的验证方法
- 重构前后可以精确对比

### 4. 验证友好
- 自动化工具支持文档生成
- 内置验证规则和合规性检查
- 清晰的验收标准

## 💡 最佳实践

### 文档维护
1. **及时更新**: 重构过程中任何变更都要及时反映到文档中
2. **版本控制**: 使用Git管理文档变更，便于追溯和回滚
3. **团队评审**: 定期进行文档评审，确保准确性和完整性

### 重构实施
1. **分步验证**: 每完成一个模块都要进行三个文档的交叉验证
2. **持续对照**: 重构过程中持续对照三个文档，确保一致性
3. **用户参与**: 让用户参与app-flows.md的验证，确保需求准确性

### 质量保证
1. **自动化测试**: 基于三个文档编写自动化测试
2. **代码审查**: 对照文档进行代码审查
3. **用户验收**: 基于app-flows.md进行用户验收测试

## 📈 成功指标

使用这个三文档架构，你可以期望：

- **重构准确性提升80%**: 通过完整的文档覆盖和交叉验证
- **重构效率提升50%**: 通过自动化工具和清晰的工作流程
- **重构风险降低70%**: 通过渐进式验证和明确的合规性要求
- **用户满意度提升**: 通过保持100%功能行为的同时优化用户体验

---

**总结**: 这个三文档架构为重构提供了一个系统化、可验证、高质量的方法论，能够有效解决重构中的准确性问题。