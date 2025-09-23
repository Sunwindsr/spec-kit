#!/usr/bin/env python3
"""
渐进式重构脚本 - 强制执行重构质量标准

Usage:
    python progressive_refactoring.py baseline --component ViewAppFile
    python progressive_refactoring.py compatibility --component ViewAppFile
    python progressive_refactoring.py component-replace --component ViewAppFile
    python progressive_refactoring.py validate --component ViewAppFile
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from specify_cli.validation import RefactoringValidationSystem
from specify_cli.commands.refactoring import console

class ProgressiveRefactoringExecutor:
    """渐进式重构执行器"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.current_phase = 0
        self.phases = [
            "baseline",
            "compatibility", 
            "component-replace",
            "parallel-validation"
        ]
        self.phase_status = {}
        
        # 初始化阶段状态
        for phase in self.phases:
            self.phase_status[phase] = "pending"
    
    def validate_phase_order(self, target_phase: str) -> bool:
        """验证阶段顺序"""
        try:
            phase_index = self.phases.index(target_phase)
            
            if phase_index > self.current_phase:
                console.print(f"[red]❌ 必须先完成阶段 {self.phases[self.current_phase]}[/red]")
                return False
            
            return True
            
        except ValueError:
            console.print(f"[red]❌ 无效的阶段: {target_phase}[/red]")
            console.print(f"[yellow]可用阶段: {', '.join(self.phases)}[/yellow]")
            return False
    
    def execute_baseline(self, component: str) -> bool:
        """执行基线验证阶段"""
        console.print(f"[cyan]🔍 执行基线验证阶段: {component}[/cyan]")
        
        if not self.validate_phase_order("baseline"):
            return False
        
        # TODO: 实现基线验证逻辑
        console.print("[yellow]⚠️ 基线验证功能开发中...[/yellow]")
        
        # 模拟验证
        validation_system = RefactoringValidationSystem()
        
        try:
            results = validation_system.validate_refactoring_project(self.project_path)
            
            if results['failed_validations'] > 0:
                console.print(f"[red]❌ 基线验证失败: {results['failed_validations']} 个错误[/red]")
                return False
            
            console.print(f"[green]✅ 基线验证通过: {results['passed_validations']} 个验证通过[/green]")
            
            # 更新阶段状态
            self.phase_status["baseline"] = "completed"
            self.current_phase = 1
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ 基线验证异常: {str(e)}[/red]")
            return False
    
    def execute_compatibility(self, component: str) -> bool:
        """执行兼容层创建阶段"""
        console.print(f"[cyan]🔧 执行兼容层创建阶段: {component}[/cyan]")
        
        if not self.validate_phase_order("compatibility"):
            return False
        
        # 检查前一阶段是否完成
        if self.phase_status["baseline"] != "completed":
            console.print("[red]❌ 必须先完成基线验证阶段[/red]")
            return False
        
        # TODO: 实现兼容层创建逻辑
        console.print("[yellow]⚠️ 兼容层创建功能开发中...[/yellow]")
        
        # 模拟兼容层检查
        compatibility_files = [
            self.project_path / "compatibility" / f"{component}-adapter.ts",
            self.project_path / "compatibility" / f"{component}-interface.ts",
            self.project_path / "compatibility" / f"{component}-validator.ts"
        ]
        
        missing_files = [f for f in compatibility_files if not f.exists()]
        
        if missing_files:
            console.print(f"[red]❌ 缺少兼容层文件: {missing_files}[/red]")
            return False
        
        console.print("[green]✅ 兼容层创建完成[/green]")
        
        # 更新阶段状态
        self.phase_status["compatibility"] = "completed"
        self.current_phase = 2
        
        return True
    
    def execute_component_replace(self, component: str) -> bool:
        """执行组件替换阶段"""
        console.print(f"[cyan]🔄 执行组件替换阶段: {component}[/cyan]")
        
        if not self.validate_phase_order("component-replace"):
            return False
        
        # 检查前一阶段是否完成
        if self.phase_status["compatibility"] != "completed":
            console.print("[red]❌ 必须先完成兼容层创建阶段[/red]")
            return False
        
        # TODO: 实现组件替换逻辑
        console.print("[yellow]⚠️ 组件替换功能开发中...[/yellow]")
        
        # 模拟组件检查
        component_files = [
            self.project_path / "src" / "components" / f"{component}.tsx",
            self.project_path / "src" / "components" / f"{component}.test.tsx",
            self.project_path / "src" / "hooks" / f"use{component}.ts"
        ]
        
        missing_files = [f for f in component_files if not f.exists()]
        
        if missing_files:
            console.print(f"[red]❌ 缺少组件文件: {missing_files}[/red]")
            return False
        
        console.print("[green]✅ 组件替换完成[/green]")
        
        # 更新阶段状态
        self.phase_status["component-replace"] = "completed"
        self.current_phase = 3
        
        return True
    
    def execute_parallel_validation(self, component: str) -> bool:
        """执行并行验证阶段"""
        console.print(f"[cyan]🔍 执行并行验证阶段: {component}[/cyan]")
        
        if not self.validate_phase_order("parallel-validation"):
            return False
        
        # 检查前一阶段是否完成
        if self.phase_status["component-replace"] != "completed":
            console.print("[red]❌ 必须先完成组件替换阶段[/red]")
            return False
        
        # TODO: 实现并行验证逻辑
        console.print("[yellow]⚠️ 并行验证功能开发中...[/yellow]")
        
        # 执行完整验证
        validation_system = RefactoringValidationSystem()
        
        try:
            results = validation_system.validate_refactoring_project(self.project_path)
            
            if results['failed_validations'] > 0:
                console.print(f"[red]❌ 并行验证失败: {results['failed_validations']} 个错误[/red]")
                return False
            
            console.print(f"[green]✅ 并行验证通过: {results['passed_validations']} 个验证通过[/green]")
            
            # 更新阶段状态
            self.phase_status["parallel-validation"] = "completed"
            self.current_phase = 4
            
            return True
            
        except Exception as e:
            console.print(f"[red]❌ 并行验证异常: {str(e)}[/red]")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        return {
            "current_phase": self.current_phase,
            "phases": self.phases,
            "phase_status": self.phase_status,
            "project_path": str(self.project_path)
        }
    
    def rollback_phase(self, phase: str) -> bool:
        """回滚到指定阶段"""
        try:
            phase_index = self.phases.index(phase)
            
            if phase_index >= self.current_phase:
                console.print(f"[red]❌ 无法回滚到当前或未来阶段: {phase}[/red]")
                return False
            
            # 重置后续阶段状态
            for i in range(phase_index + 1, len(self.phases)):
                self.phase_status[self.phases[i]] = "pending"
            
            self.current_phase = phase_index
            
            console.print(f"[green]✅ 已回滚到阶段: {phase}[/green]")
            return True
            
        except ValueError:
            console.print(f"[red]❌ 无效的阶段: {phase}[/red]")
            return False

def main():
    parser = argparse.ArgumentParser(description="渐进式重构执行器")
    parser.add_argument("phase", choices=["baseline", "compatibility", "component-replace", "parallel-validation", "status", "rollback"])
    parser.add_argument("--component", required=True, help="组件名称")
    parser.add_argument("--project", default=".", help="项目路径")
    parser.add_argument("--rollback-phase", help="回滚到的阶段（仅用于rollback命令）")
    
    args = parser.parse_args()
    
    # 初始化执行器
    executor = ProgressiveRefactoringExecutor(args.project)
    
    if args.phase == "status":
        status = executor.get_status()
        console.print("[cyan]📊 当前状态:[/cyan]")
        console.print(json.dumps(status, indent=2, ensure_ascii=False))
        return
    
    elif args.phase == "rollback":
        if not args.rollback_phase:
            console.print("[red]❌ 回滚操作需要指定 --rollback-phase 参数[/red]")
            return
        
        success = executor.rollback_phase(args.rollback_phase)
        if success:
            console.print("[green]✅ 回滚完成[/green]")
        else:
            console.print("[red]❌ 回滚失败[/red]")
            sys.exit(1)
        return
    
    # 执行对应阶段
    phase_handlers = {
        "baseline": executor.execute_baseline,
        "compatibility": executor.execute_compatibility,
        "component-replace": executor.execute_component_replace,
        "parallel-validation": executor.execute_parallel_validation
    }
    
    handler = phase_handlers.get(args.phase)
    if handler:
        success = handler(args.component)
        if success:
            console.print("[green]✅ 阶段完成[/green]")
        else:
            console.print("[red]❌ 阶段失败[/red]")
            sys.exit(1)
    else:
        console.print(f"[red]❌ 未知的阶段: {args.phase}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()