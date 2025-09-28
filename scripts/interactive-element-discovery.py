#!/usr/bin/env python3
"""
Interactive Element Discovery Script for Refactoring

This script provides tools to help AI discover and analyze interactive elements
in frontend codebases for comprehensive app flow extraction.

Usage:
    python3 scripts/interactive-element-discovery.py --source <source_path> [--output <output_file>]
    python3 scripts/interactive-element-discovery.py --source /path/to/angular/project --output interactive-elements.json
    python3 scripts/interactive-element-discovery.py --source /path/to/angular/project  # interactive mode

The script creates a structured inventory of interactive elements that AI can use
to create comprehensive app flow documentation.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import defaultdict


@dataclass
class InteractiveElement:
    """Interactive element definition"""
    element_type: str  # "button", "menu", "link", "form", "dialog", "media_control", etc.
    element_name: str
    location: str  # "file_path:line_number"
    component_name: str
    event_handlers: List[str]
    data_flow: List[str]
    user_action: str
    system_response: str
    importance: str  # "P0", "P1", "P2"
    category: str  # "navigation", "data_manipulation", "media_control", "ui_interaction", etc.


@dataclass
class ComponentFlow:
    """Component-level flow analysis"""
    component_name: str
    file_path: str
    interactive_elements: List[InteractiveElement]
    entry_points: List[str]
    exit_points: List[str]
    state_changes: List[str]
    external_dependencies: List[str]


class InteractiveElementDiscovery:
    """Interactive element discovery tool for refactoring analysis"""
    
    def __init__(self, source_path: Path):
        self.source_path = source_path
        self.components = {}
        self.interactive_elements = []
        self.patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict[str, re.Pattern]:
        """Load detection patterns for different frameworks"""
        return {
            # Event handler patterns
            'click_handlers': re.compile(r'\((click)\)|\@(click)|onClick|\.click\(|addEventListener\(.*click'),
            'change_handlers': re.compile(r'\((change)\)|\@(change)|onChange|\.change\(|addEventListener\(.*change'),
            'submit_handlers': re.compile(r'\((submit)\)|\@(submit)|onSubmit|\.submit\(|addEventListener\(.*submit'),
            'input_handlers': re.compile(r'\((input)\)|\@(input)|onInput|\.input\(|addEventListener\(.*input'),
            'keydown_handlers': re.compile(r'\((keydown)\)|\@(keydown)|onKeyDown|addEventListener\(.*keydown'),
            'media_handlers': re.compile(r'\((play|pause|ended|timeupdate)\)|\@(play|pause|ended|timeupdate)'),
            
            # UI element patterns
            'buttons': re.compile(r'<button[^>]*>|<mat-button[^>]*>|\.button|Button| MatButtonModule'),
            'links': re.compile(r'<a[^>]*href|routerLink|\.link|Link|RouterLink'),
            'menus': re.compile(r'<mat-menu|dropdown|context-menu|\.menu|Menu'),
            'dialogs': re.compile(r'<mat-dialog|modal|dialog|\.dialog|Dialog| MatDialog'),
            'forms': re.compile(r'<form[^>]*>|FormGroup|FormControl|FormBuilder'),
            'media_elements': re.compile(r'<video[^>]*>|<audio[^>]*>|media|player'),
            
            # Service call patterns
            'service_calls': re.compile(r'\.subscribe\(|\.toPromise\(\)|\.get\(|\.post\(|\.put\(|\.delete\('),
            'method_calls': re.compile(r'(\w+)\.\w+\('),
            'property_access': re.compile(r'(\w+)\.\w+'),
        }
    
    def discover_interactive_elements(self) -> List[InteractiveElement]:
        """Discover all interactive elements in the codebase"""
        print(f"[Discovery] Analyzing interactive elements in {self.source_path}")
        
        # Find all TypeScript/JavaScript component files
        component_files = list(self.source_path.rglob("*.component.ts"))
        component_files.extend(self.source_path.rglob("*.component.js"))
        component_files.extend(self.source_path.rglob("*.ts"))
        component_files.extend(self.source_path.rglob("*.js"))
        
        for file_path in component_files:
            self._analyze_component_file(file_path)
        
        return self.interactive_elements
    
    def _analyze_component_file(self, file_path: Path):
        """Analyze a single component file for interactive elements"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            # Extract component name
            component_name = self._extract_component_name(content, file_path.name)
            
            # Find all interactive elements
            elements = self._find_interactive_elements(content, lines, file_path, component_name)
            
            # Analyze event handlers
            for element in elements:
                element.event_handlers = self._extract_event_handlers(content, element.location)
                element.data_flow = self._extract_data_flow(content, element.location)
            
            self.interactive_elements.extend(elements)
            
        except Exception as e:
            print(f"[Warning] Could not analyze {file_path}: {e}")
    
    def _extract_component_name(self, content: str, filename: str) -> str:
        """Extract component name from file content or filename"""
        # Try to find @Component decorator
        component_match = re.search(r'@Component\([^)]*selector\s*:\s*["\']([^"\']+)["\']', content)
        if component_match:
            return component_match.group(1)
        
        # Try to find class name
        class_match = re.search(r'class\s+(\w+Component)', content)
        if class_match:
            return class_match.group(1)
        
        # Fallback to filename
        return filename.replace('.component.ts', '').replace('.ts', '')
    
    def _find_interactive_elements(self, content: str, lines: List[str], file_path: Path, component_name: str) -> List[InteractiveElement]:
        """Find interactive elements in component content"""
        elements = []
        
        # Template-based elements (check HTML template)
        template_content = self._extract_template_content(content)
        if template_content:
            elements.extend(self._analyze_template_elements(template_content, lines, file_path, component_name))
        
        # Code-based elements (check TypeScript code)
        elements.extend(self._analyze_code_elements(content, lines, file_path, component_name))
        
        return elements
    
    def _extract_template_content(self, content: str) -> str:
        """Extract HTML template content from component"""
        # Look for templateUrl
        template_url_match = re.search(r'templateUrl\s*:\s*["\']([^"\']+)["\']', content)
        if template_url_match:
            template_path = self.source_path / template_url_match.group(1)
            if template_path.exists():
                return template_path.read_text(encoding='utf-8')
        
        # Look for inline template
        template_match = re.search(r'template\s*:\s*["\']`([^`]+)`["\']', content)
        if template_match:
            return template_match.group(1)
        
        return ""
    
    def _analyze_template_elements(self, template_content: str, lines: List[str], file_path: Path, component_name: str) -> List[InteractiveElement]:
        """Analyze HTML template for interactive elements"""
        elements = []
        
        # Find all interactive elements in template
        for i, line in enumerate(template_content.split('\n')):
            # Buttons
            if re.search(self.patterns['buttons'], line, re.IGNORECASE):
                element = self._create_template_element(
                    "button", line, f"{file_path}:{i+1}", component_name
                )
                elements.append(element)
            
            # Links with navigation
            if re.search(r'<a[^>]*routerLink|<a[^>]*\(click\)', line, re.IGNORECASE):
                element = self._create_template_element(
                    "navigation_link", line, f"{file_path}:{i+1}", component_name
                )
                elements.append(element)
            
            # Menu items
            if re.search(self.patterns['menus'], line, re.IGNORECASE):
                element = self._create_template_element(
                    "menu_item", line, f"{file_path}:{i+1}", component_name
                )
                elements.append(element)
            
            # Media controls
            if re.search(self.patterns['media_elements'], line, re.IGNORECASE):
                element = self._create_template_element(
                    "media_control", line, f"{file_path}:{i+1}", component_name
                )
                elements.append(element)
            
            # Form inputs
            if re.search(r'<input[^>]*|<select[^>]*|<textarea[^>]*', line, re.IGNORECASE):
                element = self._create_template_element(
                    "form_input", line, f"{file_path}:{i+1}", component_name
                )
                elements.append(element)
        
        return elements
    
    def _analyze_code_elements(self, content: str, lines: List[str], file_path: Path, component_name: str) -> List[InteractiveElement]:
        """Analyze TypeScript code for interactive elements"""
        elements = []
        
        for i, line in enumerate(lines):
            # Event handler methods
            if re.search(r'\((click|change|submit|input|keydown)\)|\@(click|change|submit|input|keydown)', line):
                element = self._create_code_element(
                    "event_handler", line, f"{file_path}:{i+1}", component_name
                )
                elements.append(element)
            
            # Service method calls
            if re.search(self.patterns['service_calls'], line):
                element = self._create_code_element(
                    "service_call", line, f"{file_path}:{i+1}", component_name
                )
                elements.append(element)
            
            # Router navigation
            if re.search(r'router\.navigate|this\.router\.navigate', line):
                element = self._create_code_element(
                    "navigation", line, f"{file_path}:{i+1}", component_name
                )
                elements.append(element)
        
        return elements
    
    def _create_template_element(self, element_type: str, line: str, location: str, component_name: str) -> InteractiveElement:
        """Create interactive element from template line"""
        # Extract element name/identifier
        name_match = re.search(r'(?:id|name|#|ref)\s*=\s*["\']([^"\']+)["\']', line)
        element_name = name_match.group(1) if name_match else f"{element_type}_{location.split(':')[-1]}"
        
        return InteractiveElement(
            element_type=element_type,
            element_name=element_name,
            location=location,
            component_name=component_name,
            event_handlers=[],
            data_flow=[],
            user_action=self._infer_user_action(element_type, line),
            system_response=self._infer_system_response(element_type, line),
            importance=self._assess_importance(element_type, line),
            category=self._categorize_element(element_type)
        )
    
    def _create_code_element(self, element_type: str, line: str, location: str, component_name: str) -> InteractiveElement:
        """Create interactive element from code line"""
        # Extract method name
        method_match = re.search(r'(\w+)\s*\(', line)
        element_name = method_match.group(1) if method_match else f"{element_type}_{location.split(':')[-1]}"
        
        return InteractiveElement(
            element_type=element_type,
            element_name=element_name,
            location=location,
            component_name=component_name,
            event_handlers=[],
            data_flow=[],
            user_action=self._infer_code_user_action(element_type, line),
            system_response=self._infer_code_system_response(element_type, line),
            importance=self._assess_code_importance(element_type, line),
            category=self._categorize_element(element_type)
        )
    
    def _extract_event_handlers(self, content: str, location: str) -> List[str]:
        """Extract event handlers for an element"""
        handlers = []
        
        # Look for common event binding patterns
        event_patterns = [
            r'\((click)\)\s*=\s*"([^"]*)"',
            r'\@(click)\s*=\s*"([^"]*)"',
            r'addEventListener\([\'"](click)[\'"]',
            r'onClick\s*=\s*[\'"]([^\'"]*)[\'"]',
        ]
        
        for pattern in event_patterns:
            matches = re.findall(pattern, content)
            handlers.extend([match[0] if isinstance(match, tuple) else match for match in matches])
        
        return handlers
    
    def _extract_data_flow(self, content: str, location: str) -> List[str]:
        """Extract data flow information"""
        data_flow = []
        
        # Look for service calls and data manipulations
        flow_patterns = [
            r'(\w+)\.subscribe\(',
            r'this\.(\w+)\s*=',
            r'(\w+)\.emit\(',
            r'(\w+)\.next\(',
        ]
        
        for pattern in flow_patterns:
            matches = re.findall(pattern, content)
            data_flow.extend(matches)
        
        return data_flow
    
    def _infer_user_action(self, element_type: str, line: str) -> str:
        """Infer user action from element type and line content"""
        action_map = {
            "button": "用户点击按钮",
            "navigation_link": "用户点击导航链接", 
            "menu_item": "用户选择菜单项",
            "media_control": "用户操作媒体控制",
            "form_input": "用户输入表单数据",
        }
        
        base_action = action_map.get(element_type, "用户进行交互操作")
        
        # Enhance with context from line
        if "more" in line.lower() or "更多" in line:
            base_action += "（更多菜单）"
        if "switch" in line.lower() or "切换" in line:
            base_action += "（切换功能）"
        if "play" in line.lower() or "播放" in line:
            base_action += "（播放控制）"
        if "pause" in line.lower() or "暂停" in line:
            base_action += "（暂停控制）"
        
        return base_action
    
    def _infer_system_response(self, element_type: str, line: str) -> str:
        """Infer system response from element type and line content"""
        response_map = {
            "button": "触发对应的事件处理函数",
            "navigation_link": "进行页面导航或路由跳转",
            "menu_item": "显示下拉菜单或执行菜单功能",
            "media_control": "控制媒体播放状态",
            "form_input": "更新表单数据状态",
        }
        
        return response_map.get(element_type, "执行相应的系统响应")
    
    def _infer_code_user_action(self, element_type: str, line: str) -> str:
        """Infer user action for code-based elements"""
        if "navigate" in line.lower():
            return "用户触发页面导航"
        if "click" in line.lower():
            return "用户点击触发事件"
        if "change" in line.lower():
            return "用户改变数据状态"
        return "用户交互触发代码执行"
    
    def _infer_code_system_response(self, element_type: str, line: str) -> str:
        """Infer system response for code-based elements"""
        if "service" in line.lower():
            return "调用后端服务API"
        if "router" in line.lower():
            return "执行路由导航"
        if "emit" in line.lower():
            return "发送事件通知"
        return "执行业务逻辑处理"
    
    def _assess_importance(self, element_type: str, line: str) -> str:
        """Assess importance of interactive element"""
        high_importance_keywords = ["submit", "save", "delete", "navigate", "login", "logout"]
        medium_importance_keywords = ["change", "update", "edit", "search"]
        
        line_lower = line.lower()
        
        if any(keyword in line_lower for keyword in high_importance_keywords):
            return "P0"
        elif any(keyword in line_lower for keyword in medium_importance_keywords):
            return "P1"
        else:
            return "P2"
    
    def _assess_code_importance(self, element_type: str, line: str) -> str:
        """Assess importance of code-based elements"""
        if element_type in ["navigation", "service_call"]:
            return "P0"
        elif element_type in ["event_handler"]:
            return "P1"
        else:
            return "P2"
    
    def _categorize_element(self, element_type: str) -> str:
        """Categorize interactive element"""
        category_map = {
            "button": "ui_interaction",
            "navigation_link": "navigation", 
            "menu_item": "ui_interaction",
            "media_control": "media_control",
            "form_input": "data_manipulation",
            "event_handler": "ui_interaction",
            "service_call": "data_manipulation",
            "navigation": "navigation",
        }
        
        return category_map.get(element_type, "general")
    
    def generate_analysis_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report"""
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "source_path": str(self.source_path),
            "total_interactive_elements": len(self.interactive_elements),
            "elements_by_category": defaultdict(list),
            "elements_by_importance": defaultdict(list),
            "components_analysis": defaultdict(list),
            "key_findings": [],
            "recommendations": []
        }
        
        # Categorize elements (store as dicts for JSON serialization)
        for element in self.interactive_elements:
            try:
                element_dict = asdict(element)
                report["elements_by_category"][element.category].append(element_dict)
                report["elements_by_importance"][element.importance].append(element_dict)
                report["components_analysis"][element.component_name].append(element_dict)
            except Exception as e:
                print(f"[Warning] Could not serialize element for report: {e}")
                continue
        
        # Generate key findings
        report["key_findings"] = self._generate_key_findings()
        report["recommendations"] = self._generate_recommendations()
        
        return report
    
    def _generate_key_findings(self) -> List[str]:
        """Generate key findings from analysis"""
        findings = []
        
        # Count by importance
        p0_count = len([e for e in self.interactive_elements if e.importance == "P0"])
        p1_count = len([e for e in self.interactive_elements if e.importance == "P1"])
        p2_count = len([e for e in self.interactive_elements if e.importance == "P2"])
        
        findings.append(f"发现 {p0_count} 个关键交互元素（P0级别），{p1_count} 个重要元素（P1级别），{p2_count} 个一般元素（P2级别）")
        
        # Most interactive component
        component_counts = defaultdict(int)
        for element in self.interactive_elements:
            component_counts[element.component_name] += 1
        
        if component_counts:
            most_active = max(component_counts.items(), key=lambda x: x[1])
            findings.append(f"最复杂的组件是 {most_active[0]}，包含 {most_active[1]} 个交互元素")
        
        # Common interaction patterns
        categories = defaultdict(int)
        for element in self.interactive_elements:
            categories[element.category] += 1
        
        if categories:
            most_common = max(categories.items(), key=lambda x: x[1])
            findings.append(f"最主要的交互类型是 {most_common[0]}，占比 {most_common[1]/len(self.interactive_elements)*100:.1f}%")
        
        return findings
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Check for potential missing interactions
        has_media = any(e.category == "media_control" for e in self.interactive_elements)
        has_forms = any(e.category == "data_manipulation" for e in self.interactive_elements)
        
        if has_media:
            recommendations.append("媒体控制功能需要重点关注播放/暂停/切换等交互的连续性")
        
        if has_forms:
            recommendations.append("表单交互需要验证数据流和错误处理机制")
        
        # Check for navigation complexity
        navigation_elements = [e for e in self.interactive_elements if e.category == "navigation"]
        if len(navigation_elements) > 5:
            recommendations.append("导航逻辑较为复杂，建议重点分析路由状态管理")
        
        return recommendations


def main():
    parser = argparse.ArgumentParser(description='Interactive Element Discovery for Refactoring')
    parser.add_argument('--source', required=True, help='Source code path to analyze')
    parser.add_argument('--output', help='Output file path (JSON format)')
    parser.add_argument('--format', choices=['json', 'report'], default='json', help='Output format')
    
    args = parser.parse_args()
    
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source path {source_path} does not exist")
        return 1
    
    # Run discovery
    discovery = InteractiveElementDiscovery(source_path)
    elements = discovery.discover_interactive_elements()
    
    print(f"[Discovery] Found {len(elements)} interactive elements")
    
    # Generate report
    report = discovery.generate_analysis_report()
    
    # Output results
    if args.format == 'json':
        # Filter out any non-InteractiveElement objects that might have been added
        valid_elements = [element for element in elements if hasattr(element, 'element_type')]
        # Manually convert to dict to handle any serialization issues
        serialized_elements = []
        for element in valid_elements:
            try:
                serialized_elements.append(asdict(element))
            except Exception as e:
                print(f"[Warning] Could not serialize element {element.element_name}: {e}")
                continue
        
        output_data = {
            "interactive_elements": serialized_elements,
            "analysis_report": report
        }
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"[Discovery] Results saved to {args.output}")
        else:
            print(json.dumps(output_data, indent=2, ensure_ascii=False))
    else:
        # Human-readable report
        print("\n" + "="*60)
        print("交互元素发现报告")
        print("="*60)
        print(f"分析时间: {report['analysis_timestamp']}")
        print(f"源代码路径: {report['source_path']}")
        print(f"交互元素总数: {report['total_interactive_elements']}")
        
        print("\n关键发现:")
        for finding in report['key_findings']:
            print(f"  • {finding}")
        
        print("\n建议:")
        for recommendation in report['recommendations']:
            print(f"  • {recommendation}")
        
        print(f"\n按重要性分类:")
        for importance in ['P0', 'P1', 'P2']:
            count = len(report['elements_by_importance'][importance])
            print(f"  {importance}: {count} 个元素")
    
    return 0


if __name__ == '__main__':
    exit(main())