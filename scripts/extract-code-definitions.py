#!/usr/bin/env python3
"""
强制接口和数据模型提取工具
用于重构规格文档生成时，强制从源代码提取接口和数据模型定义
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class InterfaceDefinition:
    name: str
    file_path: str
    line_number: int
    definition: str
    properties: List[Dict[str, str]]

class CodeExtractor:
    """代码提取器 - 强制从源代码提取接口和数据模型"""
    
    def __init__(self, source_path: Path):
        self.source_path = source_path
        self.ts_files = list(source_path.rglob("*.ts"))
        self.js_files = list(source_path.rglob("*.js"))
        
    def extract_all_interfaces(self) -> Dict[str, InterfaceDefinition]:
        """提取所有TypeScript接口定义"""
        interfaces = {}
        
        for file_path in self.ts_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取接口定义
                interface_pattern = r'(export\s+)?interface\s+(\w+)\s*\{([^}]*)\}'
                matches = re.finditer(interface_pattern, content, re.MULTILINE | re.DOTALL)
                
                for match in matches:
                    interface_name = match.group(2)
                    interface_body = match.group(3)
                    
                    # 解析属性
                    properties = self._parse_properties(interface_body)
                    
                    interfaces[interface_name] = InterfaceDefinition(
                        name=interface_name,
                        file_path=str(file_path),
                        line_number=self._get_line_number(content, match.start()),
                        definition=match.group(0),
                        properties=properties
                    )
                    
            except Exception as e:
                print(f"Warning: Failed to parse {file_path}: {e}")
                
        return interfaces
    
    def extract_api_endpoints(self) -> List[Dict[str, Any]]:
        """提取API端点定义"""
        endpoints = []
        
        for file_path in self.ts_files + self.js_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取HTTP方法调用
                http_patterns = [
                    r'(get|post|put|delete|patch)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
                    r'\.(get|post|put|delete|patch)\s*\(\s*[\'"`]([^\'"`]+)[\'"`]',
                    r'fetch\s*\(\s*[\'"`]([^\'"`]+)[\'"`]'
                ]
                
                for pattern in http_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if len(match.groups()) == 2:
                            method, url = match.groups()
                        else:
                            url = match.group(1)
                            method = "GET"
                        
                        endpoints.append({
                            "method": method.upper(),
                            "url": url,
                            "file_path": str(file_path),
                            "line_number": self._get_line_number(content, match.start())
                        })
                        
            except Exception as e:
                print(f"Warning: Failed to parse {file_path}: {e}")
                
        return endpoints
    
    def extract_component_props(self) -> Dict[str, Any]:
        """提取React组件属性"""
        components = {}
        
        for file_path in self.ts_files + self.js_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取React组件
                component_patterns = [
                    r'(?:export\s+)?(?:const|function)\s+(\w+).*?(?:React\.)?(?:FC|FunctionComponent)',
                    r'class\s+(\w+).*(?:extends\s+React\.)?(Component|PureComponent)'
                ]
                
                for pattern in component_patterns:
                    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
                    for match in matches:
                        component_name = match.group(1)
                        
                        # 提取props接口
                        props_pattern = r'interface\s+' + component_name + 'Props\s*\{([^}]*)\}'
                        props_match = re.search(props_pattern, content, re.MULTILINE | re.DOTALL)
                        
                        props = []
                        if props_match:
                            props = self._parse_properties(props_match.group(1))
                        
                        components[component_name] = {
                            "file_path": str(file_path),
                            "line_number": self._get_line_number(content, match.start()),
                            "props": props
                        }
                        
            except Exception as e:
                print(f"Warning: Failed to parse {file_path}: {e}")
                
        return components
    
    def _parse_properties(self, interface_body: str) -> List[Dict[str, str]]:
        """解析接口属性"""
        properties = []
        
        # 移除注释
        interface_body = re.sub(r'//.*$', '', interface_body, flags=re.MULTILINE)
        interface_body = re.sub(r'/\*.*?\*/', '', interface_body, flags=re.DOTALL)
        
        # 分割属性定义
        lines = [line.strip() for line in interface_body.split('\n') if line.strip()]
        
        for line in lines:
            # 匹配属性定义
            prop_pattern = r'(\w+)\s*:\s*([^;]+)'
            prop_match = re.match(prop_pattern, line)
            if prop_match:
                prop_name = prop_match.group(1)
                prop_type = prop_match.group(2).strip()
                
                properties.append({
                    "name": prop_name,
                    "type": prop_type
                })
                
        return properties
    
    def _get_line_number(self, content: str, position: int) -> int:
        """获取指定位置在文本中的行号"""
        return content[:position].count('\n') + 1
    
    def generate_interface_documentation(self, interfaces: Dict[str, InterfaceDefinition]) -> str:
        """生成接口文档"""
        doc = "## Extracted Interfaces (MANDATORY - DO NOT MODIFY)\n\n"
        doc += "> 警告：以下接口定义从源代码自动提取，任何手动修改都将导致验证失败\n\n"
        
        for interface_name, interface_def in interfaces.items():
            doc += f"### {interface_name} (Source: {interface_def.file_path}:{interface_def.line_number})\n"
            doc += "```typescript\n"
            doc += interface_def.definition + "\n"
            doc += "```\n\n"
            
            if interface_def.properties:
                doc += "**Properties:**\n"
                for prop in interface_def.properties:
                    doc += f"- `{prop['name']}`: {prop['type']}\n"
                doc += "\n"
        
        return doc
    
    def generate_api_documentation(self, endpoints: List[Dict[str, Any]]) -> str:
        """生成API文档"""
        doc = "## Extracted API Endpoints (MANDATORY - DO NOT MODIFY)\n\n"
        doc += "> 警告：以下API端点从源代码自动提取，任何手动修改都将导致验证失败\n\n"
        
        # 按URL分组
        endpoint_groups = {}
        for endpoint in endpoints:
            url = endpoint['url']
            if url not in endpoint_groups:
                endpoint_groups[url] = []
            endpoint_groups[url].append(endpoint)
        
        for url, methods in endpoint_groups.items():
            doc += f"### {url}\n"
            for method_info in methods:
                doc += f"- **{method_info['method']}** (Source: {method_info['file_path']}:{method_info['line_number']})\n"
            doc += "\n"
        
        return doc

def main():
    parser = argparse.ArgumentParser(description='Extract interfaces and APIs from source code')
    parser.add_argument('--source', required=True, help='Source code path')
    parser.add_argument('--output', required=True, help='Output file path')
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown', help='Output format')
    
    args = parser.parse_args()
    
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source path {source_path} does not exist")
        return 1
    
    extractor = CodeExtractor(source_path)
    
    # 提取所有内容
    interfaces = extractor.extract_all_interfaces()
    endpoints = extractor.extract_api_endpoints()
    components = extractor.extract_component_props()
    
    if args.format == 'json':
        output_data = {
            "interfaces": {name: {
                "file_path": iface.file_path,
                "line_number": iface.line_number,
                "definition": iface.definition,
                "properties": iface.properties
            } for name, iface in interfaces.items()},
            "endpoints": endpoints,
            "components": components
        }
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
    else:
        # Markdown格式
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write("# Code Extraction Results\n\n")
            f.write(extractor.generate_interface_documentation(interfaces))
            f.write(extractor.generate_api_documentation(endpoints))
            
            if components:
                f.write("## Extracted Components\n\n")
                for comp_name, comp_info in components.items():
                    f.write(f"### {comp_name} (Source: {comp_info['file_path']}:{comp_info['line_number']})\n")
                    if comp_info['props']:
                        f.write("**Props:**\n")
                        for prop in comp_info['props']:
                            f.write(f"- `{prop['name']}`: {prop['type']}\n")
                    f.write("\n")
    
    print(f"✅ Code extraction completed: {args.output}")
    print(f"   Interfaces: {len(interfaces)}")
    print(f"   API Endpoints: {len(endpoints)}")
    print(f"   Components: {len(components)}")
    
    return 0

if __name__ == "__main__":
    exit(main())