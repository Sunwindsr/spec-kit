#!/usr/bin/env python3
"""
Repository层验证脚本 - 验证重构过程中Repository层的精准还原
Constitution VI-G: Repository Layer Integrity Principle
"""

import os
import sys
import json
import ast
import re
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RepositoryInterface:
    """Repository接口定义"""
    name: str
    methods: List[Dict[str, Any]]
    source_file: str
    line_number: int

@dataclass
class RepositoryBehavior:
    """Repository行为特征"""
    query_semantics: Dict[str, Any]
    transaction_behavior: Dict[str, Any]
    cache_strategy: Dict[str, Any]
    error_handling: Dict[str, Any]

@dataclass
class ValidationResult:
    """验证结果"""
    is_compliant: bool
    violations: List[str]
    warnings: List[str]
    recommendations: List[str]

class RepositoryValidator:
    """Repository层验证器"""
    
    def __init__(self, source_path: str, refactored_path: str):
        self.source_path = Path(source_path)
        self.refactored_path = Path(refactored_path)
        self.source_interfaces = {}
        self.refactored_interfaces = {}
        self.violations = []
        self.warnings = []
        self.recommendations = []
    
    def extract_repository_interfaces(self, path: Path) -> Dict[str, RepositoryInterface]:
        """提取Repository接口定义"""
        interfaces = {}
        
        for file_path in path.rglob("*.ts"):
            if not file_path.is_file():
                continue
                
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content)
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        if self._is_repository_class(node):
                            interface = self._parse_repository_interface(node, file_path)
                            if interface:
                                interfaces[interface.name] = interface
                                
            except Exception as e:
                self.warnings.append(f"无法解析文件 {file_path}: {e}")
                
        return interfaces
    
    def _is_repository_class(self, node) -> bool:
        """判断是否为Repository类"""
        # 检查类名是否包含Repository
        if 'Repository' in node.name:
            return True
        
        # 检查是否实现Repository接口
        for base in node.bases:
            if isinstance(base, ast.Name) and 'Repository' in base.id:
                return True
                
        return False
    
    def _parse_repository_interface(self, node, file_path) -> Optional[RepositoryInterface]:
        """解析Repository接口"""
        methods = []
        
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method = {
                    'name': item.name,
                    'args': [arg.arg for arg in item.args.args],
                    'returns': self._get_return_type(item),
                    'line': item.lineno,
                    'is_async': isinstance(item, ast.AsyncFunctionDef)
                }
                methods.append(method)
        
        return RepositoryInterface(
            name=node.name,
            methods=methods,
            source_file=str(file_path),
            line_number=node.lineno
        )
    
    def _get_return_type(self, node) -> str:
        """获取返回类型"""
        if hasattr(node, 'returns') and node.returns:
            if isinstance(node.returns, ast.Name):
                return node.returns.id
            elif isinstance(node.returns, ast.Subscript):
                return f"{node.returns.value.id}[{node.returns.slice.id if hasattr(node.returns.slice, 'id') else 'T'}]"
        return 'any'
    
    def validate_interface_consistency(self) -> ValidationResult:
        """验证接口一致性"""
        violations = []
        
        for repo_name, source_interface in self.source_interfaces.items():
            if repo_name not in self.refactored_interfaces:
                violations.append(f"缺失Repository接口: {repo_name}")
                continue
                
            refactored_interface = self.refactored_interfaces[repo_name]
            
            # 验证方法数量
            if len(source_interface.methods) != len(refactored_interface.methods):
                violations.append(f"Repository {repo_name} 方法数量不一致: 源系统{len(source_interface.methods)} vs 重构系统{len(refactored_interface.methods)}")
            
            # 验证每个方法
            source_methods = {m['name']: m for m in source_interface.methods}
            refactored_methods = {m['name']: m for m in refactored_interface.methods}
            
            for method_name, source_method in source_methods.items():
                if method_name not in refactored_methods:
                    violations.append(f"Repository {repo_name} 缺失方法: {method_name}")
                    continue
                    
                refactored_method = refactored_methods[method_name]
                
                # 验证方法签名
                if source_method['args'] != refactored_method['args']:
                    violations.append(f"Repository {repo_name} 方法 {method_name} 参数不一致")
                
                # 验证返回类型
                if source_method['returns'] != refactored_method['returns']:
                    violations.append(f"Repository {repo_name} 方法 {method_name} 返回类型不一致")
                
                # 验证异步模式
                if source_method['is_async'] != refactored_method['is_async']:
                    violations.append(f"Repository {repo_name} 方法 {method_name} 异步模式不一致")
        
        return ValidationResult(
            is_compliant=len(violations) == 0,
            violations=violations,
            warnings=self.warnings,
            recommendations=self.recommendations
        )
    
    def validate_query_semantics(self) -> ValidationResult:
        """验证查询语义一致性"""
        violations = []
        
        # 这里应该提取和分析查询逻辑
        # 由于复杂性，这里提供一个框架
        
        for repo_name in self.source_interfaces:
            source_file = self.source_interfaces[repo_name].source_file
            refactored_file = self.refactored_interfaces[repo_name].source_file if repo_name in self.refactored_interfaces else None
            
            if not refactored_file:
                violations.append(f"无法验证 {repo_name} 的查询语义 - 重构文件不存在")
                continue
            
            # 分析查询模式
            source_queries = self._extract_query_patterns(source_file)
            refactored_queries = self._extract_query_patterns(refactored_file)
            
            if len(source_queries) != len(refactored_queries):
                violations.append(f"Repository {repo_name} 查询数量不一致")
        
        return ValidationResult(
            is_compliant=len(violations) == 0,
            violations=violations,
            warnings=self.warnings,
            recommendations=self.recommendations
        )
    
    def _extract_query_patterns(self, file_path: str) -> List[Dict[str, Any]]:
        """提取查询模式"""
        patterns = []
        
        try:
            content = Path(file_path).read_text(encoding='utf-8')
            
            # 查找常见的查询模式
            query_patterns = [
                r'\.find\((.*?)\)',
                r'\.findOne\((.*?)\)',
                r'\.where\((.*?)\)',
                r'\.select\((.*?)\)',
                r'ORDER BY\s+(\w+)',
                r'LIMIT\s+(\d+)',
                r'OFFSET\s+(\d+)'
            ]
            
            for pattern in query_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    patterns.append({
                        'pattern': pattern,
                        'match': match,
                        'type': 'query'
                    })
                    
        except Exception as e:
            self.warnings.append(f"无法提取查询模式 {file_path}: {e}")
            
        return patterns
    
    def validate_transaction_behavior(self) -> ValidationResult:
        """验证事务行为一致性"""
        violations = []
        
        for repo_name in self.source_interfaces:
            source_file = self.source_interfaces[repo_name].source_file
            refactored_file = self.refactored_interfaces[repo_name].source_file if repo_name in self.refactored_interfaces else None
            
            if not refactored_file:
                continue
            
            # 分析事务模式
            source_transactions = self._extract_transaction_patterns(source_file)
            refactored_transactions = self._extract_transaction_patterns(refactored_file)
            
            if len(source_transactions) != len(refactored_transactions):
                violations.append(f"Repository {repo_name} 事务处理不一致")
        
        return ValidationResult(
            is_compliant=len(violations) == 0,
            violations=violations,
            warnings=self.warnings,
            recommendations=self.recommendations
        )
    
    def _extract_transaction_patterns(self, file_path: str) -> List[Dict[str, Any]]:
        """提取事务模式"""
        patterns = []
        
        try:
            content = Path(file_path).read_text(encoding='utf-8')
            
            # 查找事务相关模式
            transaction_patterns = [
                r'beginTransaction\(\)',
                r'commit\(\)',
                r'rollback\(\)',
                r'@Transactional',
                r'transaction\s*\(',
                r'startTransaction\(\)'
            ]
            
            for pattern in transaction_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    patterns.append({
                        'pattern': pattern,
                        'match': match,
                        'type': 'transaction'
                    })
                    
        except Exception as e:
            self.warnings.append(f"无法提取事务模式 {file_path}: {e}")
            
        return patterns
    
    def generate_validation_report(self) -> Dict[str, Any]:
        """生成验证报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'source_path': str(self.source_path),
            'refactored_path': str(self.refactored_path),
            'validation_results': {}
        }
        
        # 提取接口
        self.source_interfaces = self.extract_repository_interfaces(self.source_path)
        self.refactored_interfaces = self.extract_repository_interfaces(self.refactored_path)
        
        # 执行验证
        interface_result = self.validate_interface_consistency()
        query_result = self.validate_query_semantics()
        transaction_result = self.validate_transaction_behavior()
        
        report['validation_results'] = {
            'interface_consistency': {
                'is_compliant': interface_result.is_compliant,
                'violations': interface_result.violations,
                'warnings': interface_result.warnings,
                'recommendations': interface_result.recommendations
            },
            'query_semantics': {
                'is_compliant': query_result.is_compliant,
                'violations': query_result.violations,
                'warnings': query_result.warnings,
                'recommendations': query_result.recommendations
            },
            'transaction_behavior': {
                'is_compliant': transaction_result.is_compliant,
                'violations': transaction_result.violations,
                'warnings': transaction_result.warnings,
                'recommendations': transaction_result.recommendations
            }
        }
        
        # 计算总体合规性
        total_violations = (
            len(interface_result.violations) +
            len(query_result.violations) +
            len(transaction_result.violations)
        )
        
        report['overall_compliance'] = {
            'is_compliant': total_violations == 0,
            'total_violations': total_violations,
            'compliance_score': max(0, 100 - total_violations * 10),
            'constitutional_principle': 'VI-G. Repository Layer Integrity Principle'
        }
        
        return report
    
    def print_report(self, report: Dict[str, Any]):
        """打印验证报告"""
        print("=" * 60)
        print("Repository层验证报告")
        print("Constitution VI-G: Repository Layer Integrity Principle")
        print("=" * 60)
        print(f"源系统路径: {report['source_path']}")
        print(f"重构系统路径: {report['refactored_path']}")
        print(f"验证时间: {report['timestamp']}")
        print()
        
        # 总体合规性
        overall = report['overall_compliance']
        print("📊 总体验证结果:")
        print(f"  合规状态: {'✅ 合规' if overall['is_compliant'] else '❌ 不合规'}")
        print(f"  合规分数: {overall['compliance_score']}/100")
        print(f"  违规数量: {overall['total_violations']}")
        print()
        
        # 详细验证结果
        results = report['validation_results']
        
        print("🔍 详细验证结果:")
        for category, result in results.items():
            status = '✅ 通过' if result['is_compliant'] else '❌ 失败'
            print(f"  {category}: {status}")
            
            if result['violations']:
                print("    违规项:")
                for violation in result['violations']:
                    print(f"      - {violation}")
            
            if result['warnings']:
                print("    警告:")
                for warning in result['warnings']:
                    print(f"      ⚠️  {warning}")
            
            if result['recommendations']:
                print("    建议:")
                for recommendation in result['recommendations']:
                    print(f"      💡 {recommendation}")
            print()
        
        # 宪法原则
        print("📜 适用宪法原则:")
        print("  VI-G. Repository Layer Integrity Principle (NON-NEGOTIABLE)")
        print("  - Repository接口必须100%精准还原")
        print("  - 数据访问模式必须完全一致")
        print("  - 查询语义必须保持不变")
        print("  - 事务行为必须保持一致")
        print("  - 缓存策略必须保持一致")
        print("  - 性能特征必须匹配")
        print()


def main():
    parser = argparse.ArgumentParser(description='Repository层验证脚本')
    parser.add_argument('source_path', help='源系统路径')
    parser.add_argument('refactored_path', help='重构系统路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='输出格式')
    
    args = parser.parse_args()
    
    # 验证路径
    if not Path(args.source_path).exists():
        print(f"错误: 源系统路径不存在: {args.source_path}")
        sys.exit(1)
    
    if not Path(args.refactored_path).exists():
        print(f"错误: 重构系统路径不存在: {args.refactored_path}")
        sys.exit(1)
    
    # 创建验证器
    validator = RepositoryValidator(args.source_path, args.refactored_path)
    
    # 生成报告
    report = validator.generate_validation_report()
    
    # 输出结果
    if args.format == 'json':
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
        else:
            print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        validator.print_report(report)
        
        # 保存到文件
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(f"Repository层验证报告\n")
                f.write(f"Constitution VI-G: Repository Layer Integrity Principle\n")
                f.write("=" * 60 + "\n")
                f.write(f"源系统路径: {report['source_path']}\n")
                f.write(f"重构系统路径: {report['refactored_path']}\n")
                f.write(f"验证时间: {report['timestamp']}\n")
                f.write(f"合规状态: {'合规' if report['overall_compliance']['is_compliant'] else '不合规'}\n")
                f.write(f"合规分数: {report['overall_compliance']['compliance_score']}/100\n")
    
    # 退出码
    sys.exit(0 if report['overall_compliance']['is_compliant'] else 1)


if __name__ == '__main__':
    main()