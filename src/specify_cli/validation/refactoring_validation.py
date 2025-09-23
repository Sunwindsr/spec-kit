"""
重构验证系统 - 确保重构质量和真实性

该模块提供了强制验证机制，确保重构过程中的数据真实性、
行为保持和渐进式执行的合规性。
"""

import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ValidationSeverity(Enum):
    """验证严重程度"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationResult:
    """验证结果"""
    passed: bool
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any] = None

class RealityValidator:
    """真实性验证器"""
    
    def __init__(self):
        self.mock_patterns = [
            r'mockData|fakeData|dummyData',
            r'mockResolvedValue|mockReturnValue',
            r'const\s+mock\s*=',
            r'let\s+mock\s*=',
            r'hardcoded|hard-coded',
        ]
        
        self.real_data_patterns = [
            r'await\s+fetch\(',
            r'axios\.(get|post|put|delete)',
            r'http\.(get|post|put|delete)',
            r'api\.|/api/',
            r'useQuery\(',
            r'useMutation\(',
        ]
        
        self.placeholder_patterns = [
            r'TODO|FIXME',
            r'placeholder|占位符',
            r'not implemented|未实现',
        ]

    def validate_data_reality(self, code: str, file_path: str) -> ValidationResult:
        """验证数据真实性"""
        mock_matches = []
        real_data_matches = []
        
        # 检查Mock数据模式
        for pattern in self.mock_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                mock_matches.extend(matches)
        
        # 检查真实数据模式
        for pattern in self.real_data_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                real_data_matches.extend(matches)
        
        # 验证结果
        if mock_matches and not real_data_matches:
            return ValidationResult(
                passed=False,
                severity=ValidationSeverity.ERROR,
                message=f"检测到Mock数据但无真实API调用: {file_path}",
                details={
                    "mock_patterns": mock_matches,
                    "real_patterns": real_data_matches,
                    "file": file_path
                }
            )
        
        if not real_data_matches:
            return ValidationResult(
                passed=False,
                severity=ValidationSeverity.WARNING,
                message=f"未检测到真实数据集成: {file_path}",
                details={
                    "mock_patterns": mock_matches,
                    "real_patterns": real_data_matches,
                    "file": file_path
                }
            )
        
        return ValidationResult(
            passed=True,
            severity=ValidationSeverity.INFO,
            message=f"数据真实性验证通过: {file_path}",
            details={
                "mock_patterns": mock_matches,
                "real_patterns": real_data_matches,
                "file": file_path
            }
        )

    def validate_business_logic(self, code: str, file_path: str) -> ValidationResult:
        """验证业务逻辑真实性"""
        placeholder_matches = []
        
        # 检查占位符模式
        for pattern in self.placeholder_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                placeholder_matches.extend(matches)
        
        # 检查是否有实际的业务逻辑
        real_logic_patterns = [
            r'if\s*\(',
            r'switch\s*\(',
            r'for\s*\(',
            r'while\s*\(',
            r'do\s*\{',
            r'function\s+\w+\s*\(',
            r'const\s+\w+\s*=\s*\(',
            r'class\s+\w+',
        ]
        
        real_logic_matches = []
        for pattern in real_logic_patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            if matches:
                real_logic_matches.extend(matches)
        
        # 验证结果
        if placeholder_matches:
            return ValidationResult(
                passed=False,
                severity=ValidationSeverity.ERROR,
                message=f"检测到占位符代码: {file_path}",
                details={
                    "placeholders": placeholder_matches,
                    "real_logic": real_logic_matches,
                    "file": file_path
                }
            )
        
        if not real_logic_matches:
            return ValidationResult(
                passed=False,
                severity=ValidationSeverity.WARNING,
                message=f"未检测到真实业务逻辑: {file_path}",
                details={
                    "placeholders": placeholder_matches,
                    "real_logic": real_logic_matches,
                    "file": file_path
                }
            )
        
        return ValidationResult(
            passed=True,
            severity=ValidationSeverity.INFO,
            message=f"业务逻辑验证通过: {file_path}",
            details={
                "placeholders": placeholder_matches,
                "real_logic": real_logic_matches,
                "file": file_path
            }
        )

class BehaviorPreservationValidator:
    """行为保持验证器"""
    
    def __init__(self):
        self.interface_patterns = [
            r'interface\s+\w+',
            r'type\s+\w+',
            r'class\s+\w+',
            r'function\s+\w+',
            r'const\s+\w+\s*=',
        ]
    
    def validate_interface_stability(self, original_code: str, refactored_code: str, 
                                   file_path: str) -> ValidationResult:
        """验证接口稳定性"""
        try:
            # 提取接口定义
            original_interfaces = self._extract_interfaces(original_code)
            refactored_interfaces = self._extract_interfaces(refactored_code)
            
            # 检查接口是否保持
            missing_interfaces = set(original_interfaces.keys()) - set(refactored_interfaces.keys())
            new_interfaces = set(refactored_interfaces.keys()) - set(original_interfaces.keys())
            
            if missing_interfaces:
                return ValidationResult(
                    passed=False,
                    severity=ValidationSeverity.ERROR,
                    message=f"接口缺失: {file_path}",
                    details={
                        "missing_interfaces": list(missing_interfaces),
                        "new_interfaces": list(new_interfaces),
                        "file": file_path
                    }
                )
            
            if new_interfaces:
                return ValidationResult(
                    passed=False,
                    severity=ValidationSeverity.WARNING,
                    message=f"检测到新接口: {file_path}",
                    details={
                        "missing_interfaces": list(missing_interfaces),
                        "new_interfaces": list(new_interfaces),
                        "file": file_path
                    }
                )
            
            return ValidationResult(
                passed=True,
                severity=ValidationSeverity.INFO,
                message=f"接口稳定性验证通过: {file_path}",
                details={
                    "missing_interfaces": list(missing_interfaces),
                    "new_interfaces": list(new_interfaces),
                    "file": file_path
                }
            )
            
        except Exception as e:
            return ValidationResult(
                passed=False,
                severity=ValidationSeverity.ERROR,
                message=f"接口验证失败: {file_path} - {str(e)}",
                details={"file": file_path, "error": str(e)}
            )
    
    def _extract_interfaces(self, code: str) -> Dict[str, Any]:
        """提取接口定义"""
        interfaces = {}
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # 提取类定义
                    interfaces[node.name] = {
                        "type": "class",
                        "methods": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    }
                elif isinstance(node, ast.FunctionDef):
                    # 提取函数定义
                    interfaces[node.name] = {
                        "type": "function",
                        "args": [arg.arg for arg in node.args.args]
                    }
                
        except SyntaxError:
            # 如果不是Python代码，使用正则表达式提取
            for pattern in self.interface_patterns:
                matches = re.findall(pattern, code, re.IGNORECASE)
                for match in matches:
                    interfaces[match] = {"type": "unknown"}
        
        return interfaces

class ProgressiveRefactoringValidator:
    """渐进式重构验证器"""
    
    def __init__(self):
        self.phases = [
            "baseline",
            "compatibility", 
            "component-replace",
            "parallel-validation"
        ]
        self.current_phase = 0
    
    def validate_phase_order(self, target_phase: str) -> ValidationResult:
        """验证阶段顺序"""
        try:
            phase_index = self.phases.index(target_phase)
            
            if phase_index > self.current_phase:
                return ValidationResult(
                    passed=False,
                    severity=ValidationSeverity.ERROR,
                    message=f"必须先完成阶段{self.phases[self.current_phase]}",
                    details={
                        "current_phase": self.current_phase,
                        "target_phase": phase_index,
                        "required_phase": self.phases[self.current_phase]
                    }
                )
            
            return ValidationResult(
                passed=True,
                severity=ValidationSeverity.INFO,
                message=f"阶段顺序验证通过: {target_phase}",
                details={
                    "current_phase": self.current_phase,
                    "target_phase": phase_index
                }
            )
            
        except ValueError:
            return ValidationResult(
                passed=False,
                severity=ValidationSeverity.ERROR,
                message=f"无效的阶段: {target_phase}",
                details={"available_phases": self.phases}
            )
    
    def complete_phase(self, phase: str) -> None:
        """标记阶段完成"""
        try:
            phase_index = self.phases.index(phase)
            if phase_index == self.current_phase:
                self.current_phase += 1
        except ValueError:
            pass

class RefactoringValidationSystem:
    """重构验证系统"""
    
    def __init__(self):
        self.reality_validator = RealityValidator()
        self.behavior_validator = BehaviorPreservationValidator()
        self.spec_validator = SpecSourceValidator()
        self.progressive_validator = ProgressiveRefactoringValidator()
        self.validation_results: List[ValidationResult] = []
    
    def validate_refactoring_project(self, project_path: Path) -> Dict[str, Any]:
        """验证重构项目"""
        project_path = Path(project_path)
        
        # 扫描项目文件
        source_files = self._scan_source_files(project_path)
        
        # 验证结果统计
        stats = {
            "total_files": len(source_files),
            "passed_validations": 0,
            "failed_validations": 0,
            "warnings": 0,
            "errors": []
        }
        
        # 对每个文件进行验证
        for file_path in source_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # 数据真实性验证
                reality_result = self.reality_validator.validate_data_reality(code, str(file_path))
                self.validation_results.append(reality_result)
                
                if reality_result.passed:
                    stats["passed_validations"] += 1
                else:
                    stats["failed_validations"] += 1
                    if reality_result.severity == ValidationSeverity.ERROR:
                        stats["errors"].append(reality_result.message)
                    else:
                        stats["warnings"] += 1
                
                # 业务逻辑验证
                logic_result = self.reality_validator.validate_business_logic(code, str(file_path))
                self.validation_results.append(logic_result)
                
                if logic_result.passed:
                    stats["passed_validations"] += 1
                else:
                    stats["failed_validations"] += 1
                    if logic_result.severity == ValidationSeverity.ERROR:
                        stats["errors"].append(logic_result.message)
                    else:
                        stats["warnings"] += 1
                
            except Exception as e:
                error_result = ValidationResult(
                    passed=False,
                    severity=ValidationSeverity.ERROR,
                    message=f"验证失败: {file_path} - {str(e)}",
                    details={"file": str(file_path), "error": str(e)}
                )
                self.validation_results.append(error_result)
                stats["failed_validations"] += 1
                stats["errors"].append(error_result.message)
        
        return stats
    
    def _scan_source_files(self, project_path: Path) -> List[Path]:
        """扫描源代码文件"""
        source_files = []
        
        # 支持的文件扩展名
        extensions = {'.tsx', '.ts', '.jsx', '.js', '.py', '.java', '.cs', '.cpp', '.c'}
        
        for ext in extensions:
            source_files.extend(project_path.rglob(f'*{ext}'))
        
        return source_files
    
    def generate_report(self) -> str:
        """生成验证报告"""
        report_lines = ["# 重构验证报告\n"]
        
        # 统计结果
        passed = len([r for r in self.validation_results if r.passed])
        failed = len([r for r in self.validation_results if not r.passed])
        errors = len([r for r in self.validation_results if not r.passed and r.severity == ValidationSeverity.ERROR])
        warnings = len([r for r in self.validation_results if not r.passed and r.severity == ValidationSeverity.WARNING])
        
        report_lines.append(f"## 总体结果")
        report_lines.append(f"- 总验证数: {len(self.validation_results)}")
        report_lines.append(f"- 通过: {passed}")
        report_lines.append(f"- 失败: {failed}")
        report_lines.append(f"- 错误: {errors}")
        report_lines.append(f"- 警告: {warnings}\n")
        
        # 详细结果
        report_lines.append("## 详细结果")
        
        for result in self.validation_results:
            if result.severity == ValidationSeverity.ERROR:
                report_lines.append(f"❌ **{result.message}**")
            elif result.severity == ValidationSeverity.WARNING:
                report_lines.append(f"⚠️ **{result.message}**")
            else:
                report_lines.append(f"✅ {result.message}")
            
            if result.details:
                report_lines.append(f"   详情: {json.dumps(result.details, indent=2, ensure_ascii=False)}")
        
        return "\n".join(report_lines)


class SpecSourceValidator:
    """规格文档与源代码一致性验证器"""
    
    def __init__(self):
        self.data_model_issues = []
        
    def validate_spec_against_source(self, spec_file: Path, source_project_path: Path) -> ValidationResult:
        """验证规格文档中的数据模型是否与源代码一致"""
        try:
            if not spec_file.exists():
                return ValidationResult(
                    passed=False,
                    severity=ValidationSeverity.ERROR,
                    message="规格文档不存在",
                    details={"spec_file": str(spec_file)}
                )
            
            # 读取规格文档
            with open(spec_file, 'r', encoding='utf-8') as f:
                spec_content = f.read()
            
            # 检查是否包含数据模型定义
            if "Data Models" not in spec_content and "数据模型" not in spec_content:
                return ValidationResult(
                    passed=False,
                    severity=ValidationSeverity.ERROR,
                    message="规格文档缺少数据模型定义",
                    details={"spec_file": str(spec_file)}
                )
            
            # 检查是否标注了源代码路径
            if "Source:" not in spec_content and "源代码路径" not in spec_content:
                return ValidationResult(
                    passed=False,
                    severity=ValidationSeverity.WARNING,
                    message="数据模型未标注源代码路径，无法验证准确性",
                    details={"spec_file": str(spec_file)}
                )
            
            # 检查数据模型是否基于假设创建
            assumption_patterns = [
                r'基于假设|假设的|assumed|hypothetical',
                r'可能包含|大概|approximately',
                r'待验证|需要验证|to be validated',
                r'基于文档|based on documentation(?!source)'
            ]
            
            for pattern in assumption_patterns:
                if re.search(pattern, spec_content, re.IGNORECASE):
                    return ValidationResult(
                        passed=False,
                        severity=ValidationSeverity.ERROR,
                        message=f"检测到基于假设创建的数据模型: {pattern}",
                        details={"spec_file": str(spec_file), "pattern": pattern}
                    )
            
            # 验证源代码中是否存在相应的数据模型文件
            ts_files = list(source_project_path.rglob("*.ts"))
            if not ts_files:
                return ValidationResult(
                    passed=False,
                    severity=ValidationSeverity.WARNING,
                    message="源代码中未找到TypeScript文件",
                    details={"source_project_path": str(source_project_path)}
                )
            
            return ValidationResult(
                passed=True,
                severity=ValidationSeverity.INFO,
                message="规格文档数据模型验证通过",
                details={"spec_file": str(spec_file), "ts_files_count": len(ts_files)}
            )
            
        except Exception as e:
            return ValidationResult(
                passed=False,
                severity=ValidationSeverity.ERROR,
                message=f"验证规格文档时发生错误: {str(e)}",
                details={"spec_file": str(spec_file), "error": str(e)}
            )