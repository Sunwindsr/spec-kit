# 交互元素发现工具使用指南

## 概述

`interactive-element-discovery.py` 是专门为重构分析设计的交互元素发现工具，能够系统化地分析前端代码库中的所有交互元素，为应用流程分析提供完整的数据支持。

## 主要功能

### 1. 全面交互元素发现
- **事件处理器**: 自动发现 `click`, `change`, `submit`, `input`, `keydown` 等事件
- **模板交互**: 分析HTML模板中的按钮、链接、表单、菜单等交互元素
- **代码交互**: 识别TypeScript代码中的服务调用、导航、数据操作等
- **媒体控制**: 发现视频/音频播放、暂停、切换等媒体控制元素

### 2. 智能分类和优先级
- **重要性分级**: P0 (关键)、P1 (重要)、P2 (一般)
- **类别分类**: navigation, data_manipulation, media_control, ui_interaction
- **组件复杂度**: 分析每个组件的交互复杂度

### 3. 结构化输出
- **JSON格式**: 便于AI工具处理和分析
- **详细报告**: 包含关键发现和建议
- **位置追踪**: 精确到文件行号的交互元素定位

## 使用方法

### 基本用法
```bash
# 分析指定目录的交互元素
python3 scripts/interactive-element-discovery.py --source /path/to/source/code

# 输出JSON格式到文件
python3 scripts/interactive-element-discovery.py --source /path/to/source/code --output elements.json --format json

# 生成交互式报告
python3 scripts/interactive-element-discovery.py --source /path/to/source/code --output report.md --format report
```

### 在重构项目中使用
```bash
# 1. 在重构项目目录中运行
cd [refactoring-project-directory]

# 2. 执行交互元素发现
python3 .specify/scripts/interactive-element-discovery.py --source [original-source-path] --output .specify/interactive-elements.json

# 3. 基于发现结果完善 app-flows.md
# 4. 识别关键交互元素，确保重构后保持一致
```

## 输出格式

### JSON输出结构
```json
{
  "interactive_elements": [
    {
      "element_type": "button",
      "element_name": "favoriteButton",
      "location": "/path/to/component.ts:120",
      "component_name": "app-view-app-files-owner",
      "event_handlers": ["click"],
      "data_flow": ["serviceEnd", "appIdentityAsOwner"],
      "user_action": "用户点击收藏按钮",
      "system_response": "调用收藏API服务",
      "importance": "P0",
      "category": "data_manipulation"
    }
  ],
  "analysis_report": {
    "total_interactive_elements": 68,
    "elements_by_category": {
      "data_manipulation": [/* ... */],
      "navigation": [/* ... */],
      "media_control": [/* ... */]
    },
    "key_findings": [
      "发现 68 个关键交互元素（P0级别）",
      "最复杂的组件是 app-view-app-file，包含 52 个交互元素"
    ],
    "recommendations": [
      "表单交互需要验证数据流和错误处理机制",
      "导航逻辑较为复杂，建议重点分析路由状态管理"
    ]
  }
}
```

## 重构应用场景

### 1. 应用流程分析
使用工具发现的结果来：
- 识别关键用户交互路径
- 分析组件间的数据流
- 发现状态管理模式
- 提取业务规则和约束

### 2. 重构验证
- 确保所有关键交互元素在重构后保持一致
- 验证用户操作流程没有改变
- 检查数据流路径的正确性

### 3. 风险评估
- 基于交互元素复杂度评估重构风险
- 识别需要重点测试的关键功能
- 发现潜在的兼容性问题

## 工具优势

### 1. 系统化分析
- 相比人工分析，确保不遗漏任何交互元素
- 客观的重要性分级，避免主观判断偏差
- 一致的分析标准，提高重构质量

### 2. AI友好输出
- 结构化数据便于AI工具处理
- 详细的位置信息便于代码定位
- 上下文信息帮助AI理解业务逻辑

### 3. 重构宪法合规
- 确保Constitution I (Behavior Preservation) 的遵循
- 支持Constitution VI-E (Direct Replacement Refactoring) 要求
- 提供完整的行为保持验证依据

## 与其他工具的配合

### 1. 配合 `extract-api-contracts.py`
- 交互元素发现提供用户层面的视角
- API契约提取提供系统层面的视角
- 两者结合形成完整的分析画像

### 2. 配合 `app-flows.md` 模板
- 工具发现的交互元素作为app-flows分析的基础
- 确保流程分析的完整性和准确性
- 提供可验证的分析依据

## 最佳实践

### 1. 分析前准备
- 确保源代码路径正确
- 检查代码的完整性和可访问性
- 了解项目的基本架构和技术栈

### 2. 结果解读
- 重点关注P0级别的交互元素
- 分析复杂度最高的组件
- 注意工具提供的建议和风险提示

### 3. 重构应用
- 基于发现结果制定重构策略
- 确保关键交互元素的行为保持
- 使用工具输出作为验收标准

## 故障排除

### 常见问题
1. **找不到交互元素**: 检查源代码路径是否正确
2. **JSON序列化错误**: 确保脚本版本是最新的
3. **分析结果不完整**: 检查源代码是否有语法错误

### 获取帮助
- 查看工具的 `--help` 输出
- 检查模板文件中的使用说明
- 参考重构项目中的示例用法