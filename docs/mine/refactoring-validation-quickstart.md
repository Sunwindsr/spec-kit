# 重构验证工具快速开始指南

## 🚀 快速开始

### 安装和设置

1. **确保依赖已安装**：
```bash
pip install typer rich httpx
```

2. **验证工具可用性**：
```bash
python -m specify_cli check
```

### 基本使用

#### 1. 扫描项目真实性
```bash
# 扫描整个项目
python scripts/reality_check.py scan ./my-project

# 发现错误时退出
python scripts/reality_check.py scan ./my-project --fail-on-error
```

#### 2. 验证集成真实性
```bash
# 验证API集成
python scripts/reality_check.py validate ./my-project

# 生成详细报告
python scripts/reality_check.py report ./my-project --output reality_report.md
```

#### 3. 执行渐进式重构
```bash
# 基线验证
python scripts/progressive_refactoring.py baseline --component ViewAppFile --project ./my-project

# 兼容层创建
python scripts/progressive_refactoring.py compatibility --component ViewAppFile --project ./my-project

# 组件替换
python scripts/progressive_refactoring.py component-replace --component ViewAppFile --project ./my-project

# 并行验证
python scripts/progressive_refactoring.py parallel-validation --component ViewAppFile --project ./my-project
```

#### 4. 使用CLI命令
```bash
# 验证重构项目
python -m specify_cli refactoring validate ./my-project --fail-on-error --verbose

# 现实检查
python -m specify_cli refactoring reality-check ./my-project --pattern "*.tsx" --fail-on-mock

# 创建基线
python -m specify_cli refactoring baseline --component ViewAppFile --original ./angular --refactored ./react
```

## 📋 验证流程

### 完整验证流程示例

```bash
# 1. 首先进行现实检查
python scripts/reality_check.py scan ./my-project --fail-on-error

# 2. 验证集成真实性
python scripts/reality_check.py validate ./my-project --fail-on-error

# 3. 开始渐进式重构
python scripts/progressive_refactoring.py baseline --component ViewAppFile --project ./my-project

# 4. 创建兼容层
python scripts/progressive_refactoring.py compatibility --component ViewAppFile --project ./my-project

# 5. 替换组件
python scripts/progressive_refactoring.py component-replace --component ViewAppFile --project ./my-project

# 6. 并行验证
python scripts/progressive_refactoring.py parallel-validation --component ViewAppFile --project ./my-project

# 7. 最终验证
python -m specify_cli refactoring validate ./my-project --fail-on-error --verbose
```

## 🚨 常见问题和解决方案

### 问题1: 检测到Mock数据
```bash
# 错误信息
❌ 检测到mock_data: mockData

# 解决方案
# 将Mock数据替换为真实API调用
const mockData = [...]  // ❌ 错误
const realData = await fetch('/api/data')  // ✅ 正确
```

### 问题2: 检测到占位符
```bash
# 错误信息
❌ 检测到placeholder_code: TODO

# 解决方案
// 实现占位符功能
const handleShare = () => {
  // TODO: 实现分享功能  // ❌ 错误
  alert("分享功能已触发")   // ❌ 错误
}

const handleShare = async () => {
  try {
    await WeChatService.share(data)  // ✅ 正确
  } catch (error) {
    ErrorHandler.handle(error)
  }
}
```

### 问题3: 阶段顺序错误
```bash
# 错误信息
❌ 必须先完成阶段 baseline

# 解决方案
# 按正确顺序执行阶段
python scripts/progressive_refactoring.py baseline --component ViewAppFile
python scripts/progressive_refactoring.py compatibility --component ViewAppFile
python scripts/progressive_refactoring.py component-replace --component ViewAppFile
```

## 📊 输出示例

### 现实检查输出
```
🔍 扫描项目: ./my-project
📁 发现 45 个源文件

✅ 扫描完成
📁 总文件数: 45
✅ 通过检查: 42
❌ 失败检查: 3
🚫 违规总数: 5

❌ 发现 5 个违规
  • src/components/ViewAppFile.tsx:15 - 检测到mock_data: mockData
  • src/services/ApiService.ts:23 - 检测到placeholder_code: TODO
  • src/hooks/useData.ts:8 - 检测到hardcoded_values: hardcoded
```

### 渐进式重构输出
```
🔧 执行兼容层创建阶段: ViewAppFile
✅ 兼容层创建完成

🔄 执行组件替换阶段: ViewAppFile
✅ 组件替换完成

🔍 执行并行验证阶段: ViewAppFile
✅ 并行验证通过: 43 个验证通过

✅ 阶段完成
```

## 🛠️ 集成到CI/CD

### GitHub Actions 示例
```yaml
name: Refactoring Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install typer rich httpx
    
    - name: Reality Check
      run: |
        python scripts/reality_check.py scan . --fail-on-error
    
    - name: Integration Validation
      run: |
        python scripts/reality_check.py validate . --fail-on-error
    
    - name: Refactoring Validation
      run: |
        python -m specify_cli refactoring validate . --fail-on-error
```

### GitLab CI 示例
```yaml
stages:
  - validate

reality_check:
  stage: validate
  script:
    - pip install typer rich httpx
    - python scripts/reality_check.py scan . --fail-on-error
    - python scripts/reality_check.py validate . --fail-on-error

refactoring_validation:
  stage: validate
  script:
    - pip install typer rich httpx
    - python -m specify_cli refactoring validate . --fail-on-error
```

## 📚 高级用法

### 自定义验证规则
```python
# 在 reality_check.py 中添加自定义模式
self.custom_patterns = [
    (r'console\.log\(".*"\)', RealityViolationType.DEBUG_CODE),
    (r'alert\(".*"\)', RealityViolationType.USER_EXPERIENCE),
]
```

### 批量处理多个组件
```bash
# 批量处理多个组件
for component in ViewAppFile ViewAppFilesOwner ViewAppFilesBizNavi; do
    python scripts/progressive_refactoring.py baseline --component $component --project ./my-project
done
```

### 生成自定义报告
```bash
# 生成详细报告
python scripts/reality_check.py report ./my-project --output detailed_report.md

# 生成JSON格式报告
python scripts/reality_check.py scan ./my-project --output json_report.json
```

## 🎯 最佳实践

1. **定期验证**: 在开发过程中定期运行验证工具
2. **CI/CD集成**: 将验证工具集成到持续集成流程中
3. **渐进式重构**: 严格按照阶段顺序执行重构
4. **及时修复**: 发现问题后立即修复，不要累积
5. **团队协作**: 确保团队成员都了解验证工具的使用

---

**记住**: 这些工具的目的是确保重构质量，防止再次出现ViewAppFilesBiz重构失败的情况。