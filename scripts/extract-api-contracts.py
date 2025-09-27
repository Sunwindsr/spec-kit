#!/usr/bin/env python3
"""
API Contract Extraction Script for Direct Replacement Refactoring

This script extracts API contracts and data models from existing frontend codebases
to ensure direct replacement compatibility during refactoring.

Usage:
    python3 scripts/extract-api-contracts.py --source <source_path> [--output <output_file>]
    python3 scripts/extract-api-contracts.py --source /path/to/angular/project --output api-contracts.md
    python3 scripts/extract-api-contracts.py --source /path/to/angular/project --output-repos repositories.md --output-apis restful-apis.md

Separate Output Mode:
    --output-repos <path>    Creates frontend repositories template (blank template for AI to populate)
    --output-apis <path>     Creates backend REST APIs template (blank template for AI to populate)

Requirements:
    - Python 3.8+
    - Source code must be TypeScript/JavaScript frontend project
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict, Counter


@dataclass
class APIEndpoint:
    """API端点定义"""
    method: str
    path: str
    description: str = ""
    source_file: str = ""
    line_number: int = 0
    api_type: str = "unknown"  # "backend" or "frontend"
    category: str = "unknown"  # "http", "service", "repository"


@dataclass
class InterfaceProperty:
    """接口属性定义"""
    name: str
    type: str
    optional: bool = False
    default_value: str = ""
    description: str = ""


@dataclass
class InterfaceDefinition:
    """TypeScript接口定义"""
    name: str
    properties: List[InterfaceProperty]
    extends: List[str] = None
    source_file: str = ""
    line_number: int = 0
    description: str = ""
    
    def __post_init__(self):
        if self.extends is None:
            self.extends = []


@dataclass
class ComponentProps:
    """组件属性定义"""
    component_name: str
    inputs: List[InterfaceProperty]
    outputs: List[InterfaceProperty]
    source_file: str = ""
    line_number: int = 0


class APIContractExtractor:
    """API契约提取器"""
    
    def __init__(self, source_path: Path):
        self.source_path = source_path
        self.api_endpoints: List[APIEndpoint] = []
        self.interfaces: Dict[str, InterfaceDefinition] = {}
        self.component_props: Dict[str, ComponentProps] = {}
        
        # TypeScript解析模式
        self.interface_pattern = re.compile(
            r'(?:export\s+)?(?:interface|type)\s+(\w+)(?:\s+extends\s+([^{]+))?\s*\{([^}]*)\}',
            re.MULTILINE | re.DOTALL
        )
        
        # 属性解析模式
        self.property_pattern = re.compile(
            r'(\w+)(\?)?:\s*([^;=\n]+)(?:\s*=\s*([^;\n]+))?',
            re.MULTILINE
        )
        
        # HTTP方法模式
        self.http_methods = ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']
        
        # 后端API调用模式 (真实HTTP请求)
        self.backend_api_patterns = [
            r'\.(?:' + '|'.join(self.http_methods) + r')\([\'"`]([^\'"`]+)[\'"`]',
            r'request\([\'"`]([^\'"`]+)[\'"`]',
            r'fetch\([\'"`]([^\'"`]+)[\'"`]'
        ]
        
        # 前端服务/仓库模式
        self.frontend_service_patterns = [
            r'([A-Z][a-zA-Z]*Service)\.',
            r'([A-Z][a-zA-Z]*Repository)\.',
            r'([A-Z][a-zA-Z]*Api)\.',
            r'([a-zA-Z]*Service)\.',
            r'([a-zA-Z]*Repository)\.'
        ]
        
        # API路径模式
        self.api_path_patterns = [
            r'/api/[a-zA-Z0-9/_-]*',  # 标准API路径
            r'/[a-zA-Z0-9/_-]*',       # 其他路径
            r'http[s]?://[^\s\'"`]+'   # 完整URL
        ]
    
    def extract_all(self) -> Dict[str, Any]:
        """提取所有API契约"""
        print(f"🔍 正在提取API契约: {self.source_path}")
        
        # 查找所有TypeScript/JavaScript文件
        ts_files = list(self.source_path.rglob("*.ts")) + \
                   list(self.source_path.rglob("*.tsx")) + \
                   list(self.source_path.rglob("*.js")) + \
                   list(self.source_path.rglob("*.jsx"))
        
        print(f"📄 找到 {len(ts_files)} 个源文件")
        
        for file_path in ts_files:
            self._extract_from_file(file_path)
        
        return {
            'api_endpoints': [asdict(ep) for ep in self.api_endpoints],
            'interfaces': {name: asdict(iface) for name, iface in self.interfaces.items()},
            'component_props': {name: asdict(props) for name, props in self.component_props.items()},
            'metadata': {
                'source_path': str(self.source_path),
                'extraction_date': datetime.now().isoformat(),
                'total_files': len(ts_files),
                'total_endpoints': len(self.api_endpoints),
                'total_interfaces': len(self.interfaces),
                'total_components': len(self.component_props)
            }
        }
    
    def _extract_from_file(self, file_path: Path):
        """从单个文件提取信息"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # 提取接口定义
            self._extract_interfaces(content, str(file_path), lines)
            
            # 提取API端点
            self._extract_api_endpoints(content, str(file_path), lines)
            
            # 提取组件属性
            self._extract_component_props(content, str(file_path), lines)
            
        except Exception as e:
            print(f"⚠️ 处理文件 {file_path} 时出错: {e}")
    
    def _extract_interfaces(self, content: str, file_path: str, lines: List[str]):
        """提取TypeScript接口定义"""
        matches = self.interface_pattern.finditer(content)
        
        for match in matches:
            interface_name = match.group(1)
            extends_str = match.group(2)
            properties_body = match.group(3)
            
            # 计算行号
            line_number = content[:match.start()].count('\n') + 1
            
            # 解析继承
            extends = []
            if extends_str:
                extends = [ext.strip() for ext in extends_str.split(',')]
            
            # 解析属性
            properties = []
            for prop_match in self.property_pattern.finditer(properties_body):
                prop_name = prop_match.group(1)
                optional = prop_match.group(2) == '?'
                prop_type = prop_match.group(3).strip()
                default_value = prop_match.group(4).strip() if prop_match.group(4) else ""
                
                properties.append(InterfaceProperty(
                    name=prop_name,
                    type=prop_type,
                    optional=optional,
                    default_value=default_value
                ))
            
            # 创建接口定义
            interface = InterfaceDefinition(
                name=interface_name,
                properties=properties,
                extends=extends,
                source_file=file_path,
                line_number=line_number
            )
            
            self.interfaces[interface_name] = interface
    
    def _extract_api_endpoints(self, content: str, file_path: str, lines: List[str]):
        """提取API端点调用"""
        
        # 1. 提取后端API (真实HTTP请求)
        for pattern in self.backend_api_patterns:
            matches = re.finditer(pattern, content)
            
            for match in matches:
                api_path = match.group(1) if len(match.groups()) > 0 else match.group(0)
                
                # 跳过相对路径和非API路径
                if not self._is_api_path(api_path):
                    continue
                
                # 尝试推断HTTP方法
                method = self._infer_http_method(content, match.start(), lines)
                
                # 计算行号
                line_number = content[:match.start()].count('\n') + 1
                
                # 检查是否已存在相同端点
                existing = None
                for ep in self.api_endpoints:
                    if ep.path == api_path and ep.api_type == "backend":
                        existing = ep
                        break
                
                if existing:
                    # 更新现有端点的HTTP方法
                    if method and method not in existing.method:
                        existing.method += f",{method}"
                else:
                    # 创建后端API端点
                    endpoint = APIEndpoint(
                        method=method or "unknown",
                        path=api_path,
                        source_file=file_path,
                        line_number=line_number,
                        api_type="backend",
                        category="http"
                    )
                    self.api_endpoints.append(endpoint)
        
        # 2. 提取前端服务/仓库调用
        for pattern in self.frontend_service_patterns:
            matches = re.finditer(pattern, content)
            
            for match in matches:
                service_name = match.group(1)
                
                # 提取服务方法调用
                service_method_pattern = rf'{service_name}\.(\w+)\('
                method_matches = re.finditer(service_method_pattern, content)
                
                for method_match in method_matches:
                    method_name = method_match.group(1)
                    
                    # 构造前端API路径
                    api_path = f"{service_name}.{method_name}"
                    
                    # 计算行号
                    line_number = content[:method_match.start()].count('\n') + 1
                    
                    # 检查是否已存在相同端点
                    existing = None
                    for ep in self.api_endpoints:
                        if ep.path == api_path and ep.api_type == "frontend":
                            existing = ep
                            break
                    
                    if not existing:
                        # 创建前端API端点
                        endpoint = APIEndpoint(
                            method="FRONTEND",
                            path=api_path,
                            description=f"Frontend service method call",
                            source_file=file_path,
                            line_number=line_number,
                            api_type="frontend",
                            category="service"
                        )
                        self.api_endpoints.append(endpoint)
    
    def _is_api_path(self, path: str) -> bool:
        """判断是否为API路径"""
        if not path:
            return False
        
        # 检查是否匹配API路径模式
        for pattern in self.api_path_patterns:
            if re.match(pattern, path):
                return True
        
        return False
    
    def _infer_http_method(self, content: str, pos: int, lines: List[str]) -> str:
        """推断HTTP方法"""
        # 查找附近的HTTP方法调用
        line_start = content.rfind('\n', 0, pos)
        line_end = content.find('\n', pos)
        
        if line_start == -1:
            line_start = 0
        if line_end == -1:
            line_end = len(content)
        
        current_line = content[line_start:line_end]
        
        # 检查是否包含HTTP方法
        for method in self.http_methods:
            if f'.{method}(' in current_line:
                return method.upper()
        
        return ""
    
    def _extract_component_props(self, content: str, file_path: str, lines: List[str]):
        """提取组件属性定义"""
        # 查找@Component或类似的装饰器
        component_pattern = re.compile(
            r'@Component\s*\(\s*\{[^}]*selector\s*:\s*[\'"`]([^\'"`]+)[\'"`][^}]*\}',
            re.MULTILINE | re.DOTALL
        )
        
        # 查找@Input和@Output装饰器
        input_pattern = re.compile(r'@Input\(\)\s*(\w+)')
        output_pattern = re.compile(r'@Output\(\)\s*(\w+)')
        
        component_matches = component_pattern.finditer(content)
        
        for comp_match in component_matches:
            selector = comp_match.group(1)
            
            # 查找组件类名
            class_match = re.search(r'export\s+class\s+(\w+)', content[comp_match.end():])
            if not class_match:
                continue
                
            component_name = class_match.group(1)
            
            # 提取Input和Output属性
            inputs = []
            outputs = []
            
            # 在整个文件中查找该组件的Input/Output
            component_section = content[comp_match.start():]
            
            for input_match in input_pattern.finditer(component_section):
                prop_name = input_match.group(1)
                # 尝试找到属性类型
                prop_type = self._find_property_type(component_section, prop_name)
                inputs.append(InterfaceProperty(
                    name=prop_name,
                    type=prop_type,
                    optional=True  # Angular Input默认可选
                ))
            
            for output_match in output_pattern.finditer(component_section):
                prop_name = output_match.group(1)
                # Output通常是EventEmitter
                outputs.append(InterfaceProperty(
                    name=prop_name,
                    type="EventEmitter<any>",
                    optional=True
                ))
            
            if inputs or outputs:
                line_number = content[:comp_match.start()].count('\n') + 1
                props = ComponentProps(
                    component_name=component_name,
                    inputs=inputs,
                    outputs=outputs,
                    source_file=file_path,
                    line_number=line_number
                )
                
                self.component_props[component_name] = props
    
    def _find_property_type(self, content: str, prop_name: str) -> str:
        """查找属性类型"""
        # 查找属性定义
        prop_pattern = re.compile(f'{prop_name}\\s*:\\s*([^;\\n]+)')
        match = prop_pattern.search(content)
        
        if match:
            return match.group(1).strip()
        
        return "any"


def generate_data_models_report(extracted_data: Dict[str, Any]) -> str:
    """生成数据模型专用报告"""
    metadata = extracted_data['metadata']
    
    report = f"""# 数据模型提取报告

**源路径**: {metadata['source_path']}  
**提取日期**: {metadata['extraction_date']}  
**文件总数**: {metadata['total_files']}  
**接口定义数**: {metadata['total_interfaces']}  
**组件属性数**: {metadata['total_components']}

---

## 1. TypeScript接口契约

### 接口概览

| 接口名 | 属性数量 | 继承自 | 源文件 | 行号 |
|--------|----------|--------|--------|------|
"""
    
    # 添加接口概览表格
    for interface_name, interface in extracted_data['interfaces'].items():
        prop_count = len(interface['properties'])
        extends = ', '.join(interface['extends']) if interface['extends'] else '-'
        source_file = Path(interface['source_file']).name
        report += f"| {interface_name} | {prop_count} | {extends} | {source_file} | {interface['line_number']} |\n"
    
    report += "\n---\n\n## 2. 详细接口定义\n\n"
    
    # 添加接口详细定义
    for interface_name, interface in extracted_data['interfaces'].items():
        report += f"### {interface_name}\n\n"
        report += f"**源文件**: {Path(interface['source_file']).name}:{interface['line_number']}\n\n"
        
        if interface['extends']:
            report += f"**继承**: {', '.join(interface['extends'])}\n\n"
        
        report += "| 属性名 | 类型 | 可选 | 默认值 |\n"
        report += "|--------|------|------|--------|\n"
        
        for prop in interface['properties']:
            optional_str = "是" if prop['optional'] else "否"
            default_str = prop['default_value'] or "-"
            report += f"| {prop['name']} | {prop['type']} | {optional_str} | {default_str} |\n"
        
        report += "\n"
    
    # 添加组件属性
    if extracted_data['component_props']:
        report += "---\n\n## 3. 组件属性契约\n\n"
        
        for component_name, props in extracted_data['component_props'].items():
            if props['inputs'] or props['outputs']:
                report += f"### {component_name}\n\n"
                report += f"**源文件**: {Path(props['source_file']).name}:{props['line_number']}\n\n"
                
                if props['inputs']:
                    report += "#### Input属性\n\n"
                    report += "| 属性名 | 类型 | 可选 |\n"
                    report += "|--------|------|------|\n"
                    
                    for inp in props['inputs']:
                        optional_str = "是" if inp['optional'] else "否"
                        report += f"| {inp['name']} | {inp['type']} | {optional_str} |\n"
                    
                    report += "\n"
                
                if props['outputs']:
                    report += "#### Output属性\n\n"
                    report += "| 属性名 | 类型 |\n"
                    report += "|--------|------|\n"
                    
                    for outp in props['outputs']:
                        report += f"| {outp['name']} | {outp['type']} |\n"
                    
                    report += "\n"
    
    report += "---\n\n## 4. 重构合规性检查\n\n"
    report += "### ✅ 数据模型重构合规性要求\n\n"
    report += "- [ ] **接口完整性**: 所有TypeScript接口已提取，确保新前端数据结构完全匹配\n"
    report += "- [ ] **类型一致性**: 所有属性类型必须保持一致，严禁修改或自定义定义\n"
    report += "- [ ] **组件属性兼容性**: Angular组件属性已提取，确保React组件对应实现\n"
    report += "- [ ] **源代码可追溯性**: 所有接口都标注源文件位置，便于验证\n"
    report += "- [ ] **无自定义定义**: 严禁在新前端中自定义接口或数据模型\n"
    report += "- [ ] **100%数据保持**: 数据模型必须完全保持，仅UI/UX可优化\n"
    
    return report


def generate_apis_report(extracted_data: Dict[str, Any]) -> str:
    """生成API契约专用报告"""
    metadata = extracted_data['metadata']
    
    report = f"""# API接口契约提取报告

**源路径**: {metadata['source_path']}  
**提取日期**: {metadata['extraction_date']}  
**文件总数**: {metadata['total_files']}  
**API端点数**: {metadata['total_endpoints']}

---

## 1. HTTP端点契约

| 方法 | 路径 | 源文件 | 行号 |
|------|------|--------|------|
"""
    
    # 添加API端点表格
    for endpoint in extracted_data['api_endpoints']:
        report += f"| {endpoint['method']} | {endpoint['path']} | {Path(endpoint['source_file']).name} | {endpoint['line_number']} |\n"
    
    report += "\n---\n\n## 2. 端点分组\n\n"
    
    # 按HTTP方法分组
    method_groups = {}
    for endpoint in extracted_data['api_endpoints']:
        method = endpoint['method']
        if method not in method_groups:
            method_groups[method] = []
        method_groups[method].append(endpoint)
    
    for method, endpoints in method_groups.items():
        report += f"### {method.upper()} 端点\n\n"
        for endpoint in endpoints:
            report += f"- `{endpoint['path']}` ({Path(endpoint['source_file']).name}:{endpoint['line_number']})\n"
        report += "\n"
    
    report += "---\n\n## 3. API重构合规性检查\n\n"
    report += "### ✅ API契约重构合规性要求\n\n"
    report += "- [ ] **API完整性**: 所有HTTP端点已提取，确保新前端调用相同接口\n"
    report += "- [ ] **方法一致性**: 所有HTTP方法必须完全一致，严禁修改\n"
    report += "- [ ] **路径稳定性**: 所有URL路径必须保持稳定，直接替换无感知\n"
    report += "- [ ] **源代码可追溯性**: 所有API端点都标注源文件位置，便于验证\n"
    report += "- [ ] **无适配层**: 新前端必须直接调用相同API，无需适配层\n"
    report += "- [ ] **100%行为保持**: API调用行为必须完全保持，仅UI/UX可优化\n"
    
    return report


def generate_markdown_report(extracted_data: Dict[str, Any]) -> str:
    """生成Markdown格式的API契约报告（综合报告）"""
    metadata = extracted_data['metadata']
    
    report = f"""# API契约提取报告

**源路径**: {metadata['source_path']}  
**提取日期**: {metadata['extraction_date']}  
**文件总数**: {metadata['total_files']}  
**API端点数**: {metadata['total_endpoints']}  
**接口定义数**: {metadata['total_interfaces']}  
**组件属性数**: {metadata['total_components']}

---

## 1. API端点 (HTTP接口契约)

| 方法 | 路径 | 源文件 | 行号 |
|------|------|--------|------|
"""
    
    # 添加API端点
    for endpoint in extracted_data['api_endpoints']:
        report += f"| {endpoint['method']} | {endpoint['path']} | {Path(endpoint['source_file']).name} | {endpoint['line_number']} |\n"
    
    report += "\n---\n\n## 2. 数据模型 (TypeScript接口契约)\n\n"
    
    # 添加接口定义
    for interface_name, interface in extracted_data['interfaces'].items():
        report += f"### {interface_name}\n\n"
        report += f"**源文件**: {Path(interface['source_file']).name}:{interface['line_number']}\n\n"
        
        if interface['extends']:
            report += f"**继承**: {', '.join(interface['extends'])}\n\n"
        
        report += "| 属性名 | 类型 | 可选 | 默认值 |\n"
        report += "|--------|------|------|--------|\n"
        
        for prop in interface['properties']:
            optional_str = "是" if prop['optional'] else "否"
            default_str = prop['default_value'] or "-"
            report += f"| {prop['name']} | {prop['type']} | {optional_str} | {default_str} |\n"
        
        report += "\n"
    
    report += "---\n\n## 3. 组件属性 (Angular组件契约)\n\n"
    
    # 添加组件属性
    for component_name, props in extracted_data['component_props'].items():
        if props['inputs'] or props['outputs']:
            report += f"### {component_name}\n\n"
            report += f"**源文件**: {Path(props['source_file']).name}:{props['line_number']}\n\n"
            
            if props['inputs']:
                report += "#### Input属性\n\n"
                report += "| 属性名 | 类型 | 可选 |\n"
                report += "|--------|------|------|\n"
                
                for inp in props['inputs']:
                    optional_str = "是" if inp['optional'] else "否"
                    report += f"| {inp['name']} | {inp['type']} | {optional_str} |\n"
                
                report += "\n"
            
            if props['outputs']:
                report += "#### Output属性\n\n"
                report += "| 属性名 | 类型 |\n"
                report += "|--------|------|\n"
                
                for outp in props['outputs']:
                    report += f"| {outp['name']} | {outp['type']} |\n"
                
                report += "\n"
    
    report += "---\n\n## 4. 重构合规性检查\n\n"
    
    # 生成合规性检查清单
    report += "### ✅ 直接替换重构合规性要求\n\n"
    report += "- [ ] **API契约完整性**: 所有API端点已提取，确保新前端调用相同接口\n"
    report += "- [ ] **数据模型一致性**: 所有TypeScript接口已提取，确保数据结构完全匹配\n"
    report += "- [ ] **组件属性兼容性**: Angular组件属性已提取，确保React组件对应实现\n"
    report += "- [ ] **源代码可追溯性**: 所有契约都标注源文件位置，便于验证\n"
    report += "- [ ] **无自定义定义**: 严禁在新前端中自定义接口或数据模型\n"
    report += "- [ ] **100%行为保持**: 功能行为必须完全保持，仅UI/UX可优化\n"
    
    report += "\n### ⚠️ 重要提醒\n\n"
    report += "1. **直接替换原则**: 新前端必须直接使用提取的API契约，不得创建适配层\n"
    report += "2. **数据真实性**: 严禁使用假数据，必须调用真实的后端API\n"
    report += "3. **接口稳定性**: 所有HTTP方法和URL路径必须完全一致\n"
    report += "4. **属性映射**: Angular的@Input/@Output必须正确映射到React组件props\n"
    
    return report


def generate_backend_apis_report(backend_apis: List[APIEndpoint], stats: dict) -> str:
    """生成后端API专用报告"""
    report = f"""# Backend REST API Contracts

**提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**API端点总数**: {len(backend_apis)}

## 📊 提取统计

{generate_stats_table(stats)}

## 🔗 Backend API端点详情

以下为真实的后端HTTP API接口调用：

"""
    
    # 按HTTP方法分组
    by_method = defaultdict(list)
    for api in backend_apis:
        by_method[api.method].append(api)
    
    for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
        if method in by_method:
            report += f"\n### {method} 方法\n\n"
            for api in sorted(by_method[method], key=lambda x: x.path):
                report += f"- **{api.path}**\n"
                if api.description:
                    report += f"  - 描述: {api.description}\n"
                report += f"  - 位置: {api.source_file}:{api.line_number}\n\n"
    
    # API路径分析
    paths = [api.path for api in backend_apis]
    if paths:
        report += "### 📈 API路径分析\n\n"
        
        # 路径前缀统计
        prefixes = []
        for path in paths:
            parts = path.split('/')
            if len(parts) > 2:
                prefix = f"/{parts[1]}"
                prefixes.append(prefix)
        
        if prefixes:
            prefix_counts = Counter(prefixes)
            report += "#### API路径前缀分布\n"
            for prefix, count in prefix_counts.most_common():
                report += f"- **{prefix}**: {count} 个接口\n"
    
    return report


def generate_frontend_apis_report(frontend_apis: List[APIEndpoint], stats: dict) -> str:
    """生成前端API专用报告"""
    report = f"""# Frontend TypeScript API Contracts

**提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**API服务总数**: {len(frontend_apis)}

## 📊 提取统计

{generate_stats_table(stats)}

## 🔧 Frontend API服务详情

以下为前端TypeScript服务/仓储层接口定义：

"""
    
    # 按文件分组
    by_file = defaultdict(list)
    for api in frontend_apis:
        file_path = api.source_file
        # 只显示文件名，不显示完整路径
        file_name = Path(file_path).name
        by_file[file_name].append(api)
    
    for file_name, apis in by_file.items():
        report += f"\n### {file_name}\n\n"
        
        # 按类别分组
        by_category = defaultdict(list)
        for api in apis:
            by_category[api.category].append(api)
        
        for category in ['service', 'repository', 'unknown']:
            if category in by_category:
                category_name = {
                    'service': '服务方法',
                    'repository': '仓储方法',
                    'unknown': '未分类方法'
                }[category]
                
                report += f"#### {category_name}\n"
                for api in sorted(by_category[category], key=lambda x: x.method):
                    report += f"- **{api.method}**()\n"
                    if api.description:
                        report += f"  - 描述: {api.description}\n"
                    report += f"  - 位置: 第{api.line_number}行\n\n"
    
    # 服务类型统计
    service_types = [api.category for api in frontend_apis]
    if service_types:
        report += "### 📊 服务类型分布\n\n"
        type_counts = Counter(service_types)
        for service_type, count in type_counts.most_common():
            type_name = {
                'service': 'Service服务层',
                'repository': 'Repository仓储层',
                'unknown': '未分类'
            }[service_type]
            report += f"- **{type_name}**: {count} 个方法\n"
    
    return report


def generate_stats_table(stats: dict) -> str:
    """生成统计表格"""
    table = "| 指标 | 数量 |\n"
    table += "|------|------|\n"
    table += f"| API端点总数 | {stats.get('total_endpoints', 0)} |\n"
    table += f"| 接口定义数 | {stats.get('total_interfaces', 0)} |\n"
    table += f"| 组件属性数 | {stats.get('total_components', 0)} |\n"
    table += f"| 源文件数 | {stats.get('total_files', 0)} |\n"
    return table


def create_repositories_template() -> str:
    """创建前端Repository模板文件"""
    return """# Frontend Repository Contracts (前端仓储层契约)

**项目名称**: [项目名称]  
**重构目标**: Angular → React + TypeScript  
**源系统路径**: [源代码路径]  
**提取日期**: [日期]  
**分析范围**: 前端Repository、Service、状态管理、数据转换逻辑

---

## Phase 0: Repository Interface Analysis - 前端数据访问层契约

### 🔴 Constitution VI-D Compliance: Direct Replacement Principle
**MANDATORY**: 新React前端必须使用完全相同的Repository接口模式，无需适配层。

## 1. Repository接口分析

### Repository Service Contracts
**源位置**: [file_path]:[line_number]  
**业务重要性**: [高/中/低]  
**重构约束**: [完全保持/可优化]

#### Repository: [RepositoryName]
**接口定义**:
```typescript
// Angular Repository接口示例
@Injectable({
  providedIn: 'root'
})
export class AppFilesRepository {
  constructor(private http: HttpClient) {}
  
  // 主要方法列表
  getAppFileById(appIdentityId: number, id: string): Observable<AppFileDTO> {
    return this.http.get<AppFileDTO>(`${this.baseUrl}/api/FeatureModules/AppFiles/GetAppFileById/${appIdentityId}/${id}`);
  }
  
  // 其他方法...
}
```

**方法签名契约**:
| 方法名 | 参数类型 | 返回类型 | HTTP方法 | API路径 | 重构要求 |
|--------|----------|----------|----------|---------|----------|
| [methodName] | [params] | [returnType] | [HTTP method] | [API path] | [保持/优化] |

**数据转换逻辑**:
```typescript
// 现有数据转换代码
transformData(response: any): TargetType {
  // 转换逻辑必须保持
}
```

## 2. State Management Contracts

### BehaviorSubject/Observable模式
**源位置**: [file_path]:[line_number]  
**模式类型**: [BehaviorSubject/Subject/ReplaySubject]  

**状态定义**:
```typescript
// Angular状态管理模式
private $data = new BehaviorSubject<DataType>(null);
data$ = this.$data.asObservable();
```

**状态转换规则**:
- [规则1]: [描述] (位置: [file_path]:[line_number])
- [规则2]: [描述] (位置: [file_path]:[line_number])

## 3. Business Logic Contracts

### 数据验证逻辑
**源位置**: [file_path]:[line_number]  
**验证规则**:
- [验证规则1]: [描述]
- [验证规则2]: [描述]

### 错误处理模式
**源位置**: [file_path]:[line_number]  
**处理方式**:
```typescript
// 现有错误处理逻辑
catchError(error => {
  // 错误处理必须保持一致
  return throwError(() => error);
})
```

## 4. 数据转换契约

### DTO/VO转换
**源位置**: [file_path]:[line_number]  
**转换映射**:
| 源字段 | 目标字段 | 转换逻辑 | 重构要求 |
|--------|----------|----------|----------|
| [field1] | [target1] | [logic] | [保持/优化] |

### 数据格式化
**源位置**: [file_path]:[line_number]  
**格式化规则**:
- [规则1]: [描述]
- [规则2]: [描述]

## 5. 重构合规性要求

### ✅ Frontend Repository重构合规性

- [ ] **Repository接口保持**: 所有Repository方法签名必须完全一致
- [ ] **Observable模式保持**: RxJS Observable模式必须保持
- [ ] **数据转换逻辑保持**: 所有数据转换逻辑必须保持
- [ ] **错误处理保持**: 错误处理模式必须保持
- [ ] **状态管理保持**: BehaviorSubject状态管理必须保持
- [ ] **依赖注入保持**: Angular依赖注入模式在React中对应实现

### ❌ 禁止的操作

- ❌ 修改Repository方法签名
- ❌ 改变Observable返回类型
- ❌ 自定义数据转换逻辑
- ❌ 简化错误处理
- ❌ 改变状态管理模式

### ✅ 允许的优化

- ✅ 使用React hooks替换Angular依赖注入
- ✅ 使用zustand或jotai进行状态管理优化
- ✅ 使用tanstack-query替换HttpClient
- ✅ 优化TypeScript类型定义
- ✅ 改进错误消息显示

---

## 6. 技术实现映射

### Angular → React映射表
| Angular概念 | React对应实现 | 重构要求 |
|-------------|---------------|----------|
| @Injectable() | 自定义hook | 功能对等 |
| HttpClient | fetch/axios | 行为一致 |
| BehaviorSubject | useState+useEffect | 状态管理 |
| Observable | Promise/自定义Observable | 异步处理 |
| catchError | try/catch | 错误处理 |

---

**文档状态**: [草稿/完成/已验证]  
**最后更新**: [更新日期]  
**更新人**: [更新者]  

---

*本文档与restful-apis.md和app-flows.md共同构成重构的完整契约文档*
"""


def create_restful_apis_template() -> str:
    """创建后端REST API模板文件"""
    return """# Backend REST API Contracts (后端REST接口契约)

**项目名称**: [项目名称]  
**重构目标**: Angular → React + TypeScript  
**源系统路径**: [源代码路径]  
**提取日期**: [日期]  
**分析范围**: 后端REST API端点、认证、响应格式、错误处理

---

## Phase 0: REST API Contract Analysis - 后端接口契约

### 🔴 Constitution VI-D Compliance: Direct Replacement Principle
**MANDATORY**: 新React前端必须调用完全相同的后端API，无需适配层。

## 1. API端点分析

### HTTP端点契约
**源位置**: [file_path]:[line_number]  
**API类型**: [REST/WebSocket]  
**重构约束**: [完全保持/可优化]

#### API端点: [EndpointName]
**接口定义**:
```typescript
// Angular HTTP调用示例
getAppFileById(appIdentityId: number, id: string): Observable<AppFileDTO> {
  return this.http.get<AppFileDTO>(`${this.baseUrl}/api/FeatureModules/AppFiles/GetAppFileById/${appIdentityId}/${id}`);
}
```

**端点契约**:
| HTTP方法 | URL路径 | 参数类型 | 返回类型 | 认证要求 | 重构要求 |
|----------|---------|----------|----------|----------|----------|
| [method] | [path] | [params] | [return] | [auth] | [保持] |

**请求头契约**:
```typescript
// 现有请求头配置
headers: {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${token}`
}
```

## 2. 认证与授权契约

### JWT Token处理
**源位置**: [file_path]:[line_number]  
**认证流程**:
1. **Token获取**: [描述]
2. **Token存储**: [描述] 
3. **Token刷新**: [描述]
4. **Token失效**: [描述]

**认证头格式**:
```typescript
// 现有认证逻辑
Authorization: Bearer ${jwtToken}
```

### 权限检查
**源位置**: [file_path]:[line_number]  
**权限规则**:
- [规则1]: [描述] (位置: [file_path]:[line_number])
- [规则2]: [描述] (位置: [file_path]:[line_number])

## 3. 请求/响应格式契约

### 请求格式
**源位置**: [file_path]:[line_number]  
**Content-Type**: [application/json/application/x-www-form-urlencoded]  
**编码方式**: [UTF-8/其他]

**请求参数格式**:
```typescript
// 现有请求参数结构
interface RequestParams {
  // 参数定义必须保持
}
```

### 响应格式
**源位置**: [file_path]:[line_number]  
**响应结构**:
```typescript
// 现有响应结构
interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  errorCode?: string;
}
```

## 4. 错误处理契约

### HTTP状态码处理
**源位置**: [file_path]:[line_number]  
**状态码映射**:
| 状态码 | 含义 | 处理方式 | 重构要求 |
|--------|------|----------|----------|
| 200 | 成功 | [处理逻辑] | 保持 |
| 401 | 未授权 | [处理逻辑] | 保持 |
| 403 | 禁止访问 | [处理逻辑] | 保持 |
| 404 | 未找到 | [处理逻辑] | 保持 |
| 500 | 服务器错误 | [处理逻辑] | 保持 |

**错误响应格式**:
```typescript
// 现有错误响应结构
interface ErrorResponse {
  success: false;
  message: string;
  errorCode?: string;
  details?: any;
}
```

## 5. 数据模型契约

### Request DTOs
**源位置**: [file_path]:[line_number]  
**请求模型**:
```typescript
// 现有请求数据传输对象
interface RequestDTO {
  // 字段定义必须保持
}
```

### Response DTOs
**源位置**: [file_path]:[line_number]  
**响应模型**:
```typescript
// 现有响应数据传输对象
interface ResponseDTO {
  // 字段定义必须保持
}
```

## 6. API调用模式契约

### HTTP客户端配置
**源位置**: [file_path]:[line_number]  
**客户端设置**:
```typescript
// 现有HTTP客户端配置
{
  timeout: 30000,
  withCredentials: true,
  responseType: 'json'
}
```

### 拦截器模式
**源位置**: [file_path]:[line_number]  
**拦截器逻辑**:
```typescript
// 现有拦截器实现
intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
  // 拦截器逻辑必须保持
}
```

## 7. 重构合规性要求

### ✅ Backend API重构合规性

- [ ] **API端点保持**: 所有HTTP方法和URL必须完全一致
- [ ] **认证流程保持**: JWT认证流程必须保持
- [ ] **数据格式保持**: 请求/响应格式必须保持
- [ ] **错误处理保持**: HTTP状态码处理必须保持
- [ ] **超时设置保持**: 网络超时配置必须保持
- [ ] **拦截器逻辑保持**: 请求拦截器必须保持

### ❌ 禁止的操作

- ❌ 修改API端点URL
- ❌ 改变HTTP方法
- ❌ 修改认证头格式
- ❌ 自定义错误处理
- ❌ 改变数据格式
- ❌ 添加适配层

### ✅ 允许的优化

- ✅ 使用fetch/axios替换HttpClient
- ✅ 优化网络请求配置
- ✅ 改进错误消息显示
- ✅ 添加请求重试逻辑
- ✅ 优化TypeScript类型定义

---

## 8. API性能契约

### 超时设置
**源位置**: [file_path]:[line_number]  
**超时配置**:
- 连接超时: [时间]
- 读取超时: [时间]
- 写入超时: [时间]

### 重试机制
**源位置**: [file_path]:[line_number]  
**重试规则**:
- 最大重试次数: [次数]
- 重试间隔: [时间]
- 重试条件: [条件]

---

**文档状态**: [草稿/完成/已验证]  
**最后更新**: [更新日期]  
**更新人**: [更新者]  

---

*本文档与repositories.md和app-flows.md共同构成重构的完整契约文档*
"""


def main():
    parser = argparse.ArgumentParser(description='Extract API contracts from frontend codebase')
    parser.add_argument('--source', required=True, help='Source code path')
    parser.add_argument('--output', help='Output markdown file path (default: api-contracts.md)')
    parser.add_argument('--json', help='Also save JSON data to this file')
    parser.add_argument('--mode', choices=['combined', 'data-models', 'apis', 'backend-apis', 'frontend-apis'], default='combined',
                       help='Extraction mode: combined, data-models-only, apis-only, backend-apis-only, or frontend-apis-only')
    parser.add_argument('--output-repos', help='Output frontend repositories template file path (creates blank template for AI to populate)')
    parser.add_argument('--output-apis', help='Output backend REST APIs template file path (creates blank template for AI to populate)')
    
    args = parser.parse_args()
    
    source_path = Path(args.source)
    
    # Default output file name is api-contracts.md for consistency
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path('api-contracts.md')
    
    if not source_path.exists():
        print(f"❌ 源路径不存在: {source_path}")
        return 1
    
    # 创建提取器
    extractor = APIContractExtractor(source_path)
    
    # 提取数据
    extracted_data = extractor.extract_all()
    
    # 根据模式生成报告
    if args.mode == 'data-models':
        markdown_report = generate_data_models_report(extracted_data)
        print(f"✅ 数据模型报告已生成")
    elif args.mode == 'apis':
        markdown_report = generate_apis_report(extracted_data)
        print(f"✅ API契约报告已生成")
    elif args.mode == 'backend-apis':
        # 过滤出后端API
        backend_apis = [ep for ep in extractor.api_endpoints if ep.api_type == 'backend']
        stats = extracted_data['metadata']
        markdown_report = generate_backend_apis_report(backend_apis, stats)
        print(f"✅ Backend API报告已生成")
    elif args.mode == 'frontend-apis':
        # 过滤出前端API
        frontend_apis = [ep for ep in extractor.api_endpoints if ep.api_type == 'frontend']
        stats = extracted_data['metadata']
        markdown_report = generate_frontend_apis_report(frontend_apis, stats)
        print(f"✅ Frontend API报告已生成")
    else:  # combined
        markdown_report = generate_markdown_report(extracted_data)
        print(f"✅ 综合API契约报告已生成")
    
    # 保存报告
    output_path.write_text(markdown_report, encoding='utf-8')
    print(f"✅ 报告已保存: {output_path}")
    
    # 保存JSON数据（如果指定）
    if args.json:
        json_path = Path(args.json)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON数据已保存: {json_path}")
    
    # 显示统计信息
    metadata = extracted_data['metadata']
    print(f"\n📊 提取统计:")
    print(f"   - API端点: {metadata['total_endpoints']}")
    print(f"   - 接口定义: {metadata['total_interfaces']}")
    print(f"   - 组件属性: {metadata['total_components']}")
    
    # 确保输出文件名符合规范
    if output_path.name != 'api-contracts.md':
        print(f"⚠️ 建议使用标准文件名: api-contracts.md")
        print(f"   当前文件名: {output_path.name}")
    
    # 创建分离的模板文件（如果指定）
    if args.output_repos:
        repos_template_path = Path(args.output_repos)
        repos_template = create_repositories_template()
        repos_template_path.write_text(repos_template, encoding='utf-8')
        print(f"✅ Frontend repositories模板已创建: {repos_template_path}")
    
    if args.output_apis:
        apis_template_path = Path(args.output_apis)
        apis_template = create_restful_apis_template()
        apis_template_path.write_text(apis_template, encoding='utf-8')
        print(f"✅ Backend REST APIs模板已创建: {apis_template_path}")
    
    return 0


if __name__ == '__main__':
    exit(main())