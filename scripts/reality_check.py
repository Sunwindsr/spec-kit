#!/usr/bin/env python3
"""
真实性验证检查点 - 确保重构过程中的数据真实性

Usage:
    python reality_check.py scan ./my-project
    python reality_check.py validate ./my-project --component ViewAppFile
    python reality_check.py report ./my-project --output report.md
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from specify_cli.commands.refactoring import console

class RealityViolationType(Enum):
    """真实性违规类型"""
    MOCK_DATA = "mock_data"
    PLACEHOLDER_CODE = "placeholder_code"
    FAKE_API = "fake_api"
    MISSING_INTEGRATION = "missing_integration"
    HARDCODED_VALUES = "hardcoded_values"

@dataclass
class RealityViolation:
    """真实性违规记录"""
    file_path: str
    line_number: int
    violation_type: RealityViolationType
    message: str
    code_snippet: str
    severity: str = "error"

class RealityCheckpoint:
    """真实性检查点"""
    
    def __init__(self):
        self.violations: List[RealityViolation] = []
        self.checks_passed = 0
        self.checks_failed = 0
        
        # 定义检查模式
        self.mock_patterns = [
            (r'mockData|fakeData|dummyData', RealityViolationType.MOCK_DATA),
            (r'mockResolvedValue|mockReturnValue', RealityViolationType.FAKE_API),
            (r'const\s+mock\s*=\s*\[', RealityViolationType.MOCK_DATA),
            (r'let\s+mock\s*=\s*\[', RealityViolationType.MOCK_DATA),
            (r'hardcoded|hard-coded', RealityViolationType.HARDCODED_VALUES),
        ]
        
        self.placeholder_patterns = [
            (r'TODO|FIXME', RealityViolationType.PLACEHOLDER_CODE),
            (r'placeholder|占位符', RealityViolationType.PLACEHOLDER_CODE),
            (r'not implemented|未实现', RealityViolationType.PLACEHOLDER_CODE),
            (r'//\s*实现', RealityViolationType.PLACEHOLDER_CODE),
        ]
        
        self.real_data_patterns = [
            (r'await\s+fetch\(', "real_api"),
            (r'axios\.(get|post|put|delete)', "real_api"),
            (r'http\.(get|post|put|delete)', "real_api"),
            (r'api\.|/api/', "real_api"),
            (r'useQuery\(', "real_api"),
            (r'useMutation\(', "real_api"),
        ]
        
        self.business_logic_patterns = [
            (r'if\s*\(', "real_logic"),
            (r'switch\s*\(', "real_logic"),
            (r'for\s*\(', "real_logic"),
            (r'while\s*\(', "real_logic"),
            (r'do\s*\{', "real_logic"),
            (r'function\s+\w+\s*\(', "real_logic"),
            (r'const\s+\w+\s*=\s*\(', "real_logic"),
            (r'class\s+\w+', "real_logic"),
            (r'try\s*\{', "real_logic"),
            (r'catch\s*\(', "real_logic"),
        ]
    
    def scan_file(self, file_path: Path) -> List[RealityViolation]:
        """扫描单个文件"""
        violations = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line_number, line in enumerate(lines, 1):
                violations.extend(self._check_line(line, line_number, file_path))
                
        except Exception as e:
            violations.append(RealityViolation(
                file_path=str(file_path),
                line_number=0,
                violation_type=RealityViolationType.MISSING_INTEGRATION,
                message=f"文件读取失败: {str(e)}",
                code_snippet="",
                severity="error"
            ))
        
        return violations
    
    def _check_line(self, line: str, line_number: int, file_path: Path) -> List[RealityViolation]:
        """检查单行代码"""
        violations = []
        
        # 检查Mock数据模式
        for pattern, violation_type in self.mock_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                violations.append(RealityViolation(
                    file_path=str(file_path),
                    line_number=line_number,
                    violation_type=violation_type,
                    message=f"检测到{violation_type.value}: {match.group()}",
                    code_snippet=line.strip(),
                    severity="error"
                ))
        
        # 检查占位符模式
        for pattern, violation_type in self.placeholder_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                violations.append(RealityViolation(
                    file_path=str(file_path),
                    line_number=line_number,
                    violation_type=violation_type,
                    message=f"检测到{violation_type.value}: {match.group()}",
                    code_snippet=line.strip(),
                    severity="error"
                ))
        
        return violations
    
    def scan_project(self, project_path: Path) -> Dict[str, Any]:
        """扫描整个项目"""
        console.print(f"[cyan]🔍 扫描项目: {project_path}[/cyan]")
        
        # 支持的文件扩展名
        extensions = {'.tsx', '.ts', '.jsx', '.js', '.py'}
        source_files = []
        
        for ext in extensions:
            source_files.extend(project_path.rglob(f'*{ext}'))
        
        console.print(f"[cyan]📁 发现 {len(source_files)} 个源文件[/cyan]")
        
        # 扫描所有文件
        all_violations = []
        files_with_violations = set()
        
        for file_path in source_files:
            file_violations = self.scan_file(file_path)
            if file_violations:
                all_violations.extend(file_violations)
                files_with_violations.add(str(file_path))
        
        self.violations = all_violations
        
        # 统计结果
        error_count = len([v for v in all_violations if v.severity == "error"])
        warning_count = len([v for v in all_violations if v.severity == "warning"])
        
        self.checks_failed = len(files_with_violations)
        self.checks_passed = len(source_files) - len(files_with_violations)
        
        return {
            "total_files": len(source_files),
            "files_with_violations": len(files_with_violations),
            "total_violations": len(all_violations),
            "error_count": error_count,
            "warning_count": warning_count,
            "checks_passed": self.checks_passed,
            "checks_failed": self.checks_failed,
            "violations": [self._violation_to_dict(v) for v in all_violations]
        }
    
    def validate_integration(self, project_path: Path) -> Dict[str, Any]:
        """验证集成真实性"""
        console.print(f"[cyan]🔗 验证集成真实性: {project_path}[/cyan]")
        
        # 支持的文件扩展名
        extensions = {'.tsx', '.ts', '.jsx', '.js', '.py'}
        source_files = []
        
        for ext in extensions:
            source_files.extend(project_path.rglob(f'*{ext}'))
        
        integration_stats = {
            "files_with_real_api": 0,
            "files_with_mock_data": 0,
            "files_with_business_logic": 0,
            "files_with_placeholders": 0,
            "integration_score": 0
        }
        
        for file_path in source_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                has_real_api = any(re.search(pattern, content, re.IGNORECASE) 
                                for pattern, _ in self.real_data_patterns)
                has_mock_data = any(re.search(pattern, content, re.IGNORECASE) 
                                for pattern, _ in self.mock_patterns)
                has_business_logic = any(re.search(pattern, content, re.IGNORECASE) 
                                       for pattern, _ in self.business_logic_patterns)
                has_placeholders = any(re.search(pattern, content, re.IGNORECASE) 
                                     for pattern, _ in self.placeholder_patterns)
                
                if has_real_api:
                    integration_stats["files_with_real_api"] += 1
                if has_mock_data:
                    integration_stats["files_with_mock_data"] += 1
                if has_business_logic:
                    integration_stats["files_with_business_logic"] += 1
                if has_placeholders:
                    integration_stats["files_with_placeholders"] += 1
                
            except Exception:
                continue
        
        # 计算集成得分
        total_files = len(source_files)
        if total_files > 0:
            integration_stats["integration_score"] = int(
                (integration_stats["files_with_real_api"] / total_files) * 100
            )
        
        return integration_stats
    
    def generate_report(self, scan_results: Dict[str, Any], integration_results: Dict[str, Any]) -> str:
        """生成验证报告"""
        report_lines = ["# 真实性验证报告\n"]
        
        # 总体结果
        report_lines.append("## 📊 总体结果")
        report_lines.append(f"- **总文件数**: {scan_results['total_files']}")
        report_lines.append(f"- **通过检查**: {scan_results['checks_passed']}")
        report_lines.append(f"- **失败检查**: {scan_results['checks_failed']}")
        report_lines.append(f"- **违规总数**: {scan_results['total_violations']}")
        report_lines.append(f"- **错误数量**: {scan_results['error_count']}")
        report_lines.append(f"- **警告数量**: {scan_results['warning_count']}")
        report_lines.append(f"- **集成得分**: {integration_results['integration_score']}%\n")
        
        # 集成统计
        report_lines.append("## 🔗 集成统计")
        report_lines.append(f"- **真实API文件**: {integration_results['files_with_real_api']}")
        report_lines.append(f"- **Mock数据文件**: {integration_results['files_with_mock_data']}")
        report_lines.append(f"- **业务逻辑文件**: {integration_results['files_with_business_logic']}")
        report_lines.append(f"- **占位符文件**: {integration_results['files_with_placeholders']}\n")
        
        # 违规详情
        if scan_results['violations']:
            report_lines.append("## 🚫 违规详情")
            
            # 按类型分组
            violations_by_type = {}
            for violation_dict in scan_results['violations']:
                violation_type = violation_dict['violation_type']
                if violation_type not in violations_by_type:
                    violations_by_type[violation_type] = []
                violations_by_type[violation_type].append(violation_dict)
            
            for violation_type, violations in violations_by_type.items():
                report_lines.append(f"### {violation_type}")
                for violation in violations[:10]:  # 最多显示10个
                    report_lines.append(f"**{violation['file_path']}:{violation['line_number']}**")
                    report_lines.append(f"- 违规: {violation['message']}")
                    report_lines.append(f"- 代码: `{violation['code_snippet']}`")
                    report_lines.append("")
                
                if len(violations) > 10:
                    report_lines.append(f"... 还有 {len(violations) - 10} 个类似违规")
                report_lines.append("")
        
        # 建议
        report_lines.append("## 💡 改进建议")
        
        if integration_results['files_with_mock_data'] > 0:
            report_lines.append("### 📝 Mock数据问题")
            report_lines.append("- 将所有Mock数据替换为真实API调用")
            report_lines.append("- 使用真实的数据源和端点")
            report_lines.append("- 确保测试和生产环境使用相同的数据源")
            report_lines.append("")
        
        if integration_results['files_with_placeholders'] > 0:
            report_lines.append("### 🔧 占位符问题")
            report_lines.append("- 实现所有标记为TODO或FIXME的功能")
            report_lines.append("- 确保业务逻辑完整性")
            report_lines.append("- 移除所有占位符代码")
            report_lines.append("")
        
        if integration_results['integration_score'] < 80:
            report_lines.append("### 🎯 集成改进")
            report_lines.append("- 提高真实API集成比例")
            report_lines.append("- 确保所有组件都有真实的数据源")
            report_lines.append("- 实现完整的业务逻辑")
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def _violation_to_dict(self, violation: RealityViolation) -> Dict[str, Any]:
        """将违规对象转换为字典"""
        return {
            "file_path": violation.file_path,
            "line_number": violation.line_number,
            "violation_type": violation.violation_type.value,
            "message": violation.message,
            "code_snippet": violation.code_snippet,
            "severity": violation.severity
        }

def main():
    parser = argparse.ArgumentParser(description="真实性验证检查点")
    parser.add_argument("command", choices=["scan", "validate", "report"], help="执行命令")
    parser.add_argument("project_path", help="项目路径")
    parser.add_argument("--component", help="组件名称（用于validate命令）")
    parser.add_argument("--output", "-o", help="输出文件路径（用于report命令）")
    parser.add_argument("--fail-on-error", action="store_true", help="发现错误时退出")
    
    args = parser.parse_args()
    
    project_path = Path(args.project_path)
    if not project_path.exists():
        console.print(f"[red]❌ 项目路径不存在: {project_path}[/red]")
        sys.exit(1)
    
    checkpoint = RealityCheckpoint()
    
    if args.command == "scan":
        # 扫描项目
        results = checkpoint.scan_project(project_path)
        
        # 显示结果
        console.print(f"\n[green]✅ 扫描完成[/green]")
        console.print(f"📁 总文件数: {results['total_files']}")
        console.print(f"✅ 通过检查: {results['checks_passed']}")
        console.print(f"❌ 失败检查: {results['checks_failed']}")
        console.print(f"🚫 违规总数: {results['total_violations']}")
        
        if results['violations']:
            console.print(f"\n[red]❌ 发现 {len(results['violations'])} 个违规[/red]")
            for violation in results['violations'][:5]:  # 显示前5个
                console.print(f"  • {violation['file_path']}:{violation['line_number']} - {violation['message']}")
            
            if len(results['violations']) > 5:
                console.print(f"  ... 还有 {len(results['violations']) - 5} 个违规")
        
        if args.fail_on_error and results['total_violations'] > 0:
            sys.exit(1)
    
    elif args.command == "validate":
        # 验证集成
        results = checkpoint.validate_integration(project_path)
        
        # 显示结果
        console.print(f"\n[green]✅ 验证完成[/green]")
        console.print(f"🔗 真实API文件: {results['files_with_real_api']}")
        console.print(f"🚫 Mock数据文件: {results['files_with_mock_data']}")
        console.print(f"🧠 业务逻辑文件: {results['files_with_business_logic']}")
        console.print(f"📝 占位符文件: {results['files_with_placeholders']}")
        console.print(f"📊 集成得分: {results['integration_score']}%")
        
        if results['integration_score'] < 80:
            console.print(f"\n[yellow]⚠️ 集成得分低于80%[/yellow]")
            if args.fail_on_error:
                sys.exit(1)
    
    elif args.command == "report":
        # 生成完整报告
        scan_results = checkpoint.scan_project(project_path)
        integration_results = checkpoint.validate_integration(project_path)
        
        report = checkpoint.generate_report(scan_results, integration_results)
        
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            console.print(f"[green]✅ 报告已保存到: {output_path}[/green]")
        else:
            console.print(report)
        
        # 检查是否需要失败退出
        if args.fail_on_error and (scan_results['total_violations'] > 0 or integration_results['integration_score'] < 80):
            sys.exit(1)

if __name__ == "__main__":
    main()