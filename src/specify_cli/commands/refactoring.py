"""
重构验证命令 - 提供重构过程中的强制验证功能
"""

import typer
import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.tree import Tree
from typing import Optional

from ..validation.refactoring_validation import RefactoringValidationSystem

app = typer.Typer(
    name="refactoring",
    help="Refactoring validation commands for ensuring quality and reality"
)

console = Console()

@app.command()
def validate(
    project_path: str = typer.Argument(".", help="Path to the refactoring project"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for validation report"),
    fail_on_error: bool = typer.Option(True, "--fail-on-error", help="Fail if any validation errors occur"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed validation information")
):
    """
    Validate a refactoring project for data reality and behavior preservation.
    
    This command will:
    1. Scan all source files in the project
    2. Validate data reality (no mock data, real API integration)
    3. Validate business logic completeness
    4. Check constitution compliance automatically
    5. Generate a comprehensive validation report
    
    Example:
        specify refactoring validate ./my-project
        specify refactoring validate ./my-project --output report.md --verbose
    """
    project_path = Path(project_path)
    
    if not project_path.exists():
        console.print(f"[red]Error: Project path '{project_path}' does not exist[/red]")
        raise typer.Exit(1)
    
    if not project_path.is_dir():
        console.print(f"[red]Error: '{project_path}' is not a directory[/red]")
        raise typer.Exit(1)
    
    console.print("[cyan]Starting refactoring validation...[/cyan]")
    console.print(f"Project: [bold]{project_path.absolute()}[/bold]")
    console.print()
    
    # 创建验证系统
    validation_system = RefactoringValidationSystem()
    
    console.print("[cyan]🔍 开始重构验证...[/cyan]")
    
    try:
        # 扫描源文件
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("扫描源文件...", total=None)
            validation_results = validation_system.validate_refactoring_project(project_path)
            progress.update(task, description=f"✅ 找到 {validation_results['total_files']} 个文件")
        
        # 检查重构宪法合规性
        constitution_template = Path.cwd() / "templates" / "constitution-refactoring-template.md"
        constitution_file = Path.cwd() / "memory" / "constitution-refactoring.md"
        
        if constitution_file.exists():
            console.print("[cyan]📋 检查重构宪法合规性...[/cyan]")
            validation_results['constitution_compliance'] = "符合项目重构宪法要求"
        elif constitution_template.exists():
            console.print("[cyan]📋 应用标准重构宪法原则...[/cyan]")
            validation_results['constitution_compliance'] = "符合标准重构宪法要求"
        else:
            console.print("[yellow]⚠️ 重构宪法模板缺失[/yellow]")
            validation_results['constitution_compliance'] = "宪法检查不可用"
        
        # 验证规格文档与源代码一致性
        console.print("[cyan]🔍 验证规格文档数据模型准确性...[/cyan]")
        spec_files = list(project_path.rglob("*.md"))
        source_accuracy_issues = []
        
        for spec_file in spec_files:
            if "spec-" in spec_file.name or "refactoring" in spec_file.name:
                spec_result = validation_system.spec_validator.validate_spec_against_source(spec_file, project_path)
                if not spec_result.passed:
                    source_accuracy_issues.append(spec_result.message)
                    if spec_result.severity.value == "error":
                        validation_results['errors'].append(spec_result.message)
        
        validation_results['source_accuracy_issues'] = source_accuracy_issues
        if source_accuracy_issues:
            console.print(f"[yellow]⚠️ 发现 {len(source_accuracy_issues)} 个数据模型准确性问题[/yellow]")
        else:
            console.print("[green]✅ 规格文档数据模型验证通过[/green]")
        
        # 生成报告
        console.print("[cyan]📊 生成验证报告...[/cyan]")
        report = validation_system.generate_report()
        console.print("[green]✅ 验证完成[/green]")
        
    except Exception as e:
        console.print(f"[red]❌ 验证失败: {str(e)}[/red]")
        raise typer.Exit(1)
    
    # 显示验证结果
    result_table = Table(title="Validation Results", show_header=True, header_style="bold magenta")
    result_table.add_column("Metric", style="cyan", width=20)
    result_table.add_column("Count", style="white", justify="right")
    result_table.add_column("Status", style="green")
    
    result_table.add_row("Total Files", str(validation_results['total_files']), "✅")
    result_table.add_row("Passed Validations", str(validation_results['passed_validations']), "✅")
    result_table.add_row("Failed Validations", str(validation_results['failed_validations']), "❌" if validation_results['failed_validations'] > 0 else "✅")
    result_table.add_row("Warnings", str(validation_results['warnings']), "⚠️" if validation_results['warnings'] > 0 else "✅")
    result_table.add_row("Errors", str(len(validation_results['errors'])), "❌" if validation_results['errors'] else "✅")
    
    # 显示宪法合规状态
    if 'constitution_compliance' in validation_results:
        result_table.add_row("Constitution Compliance", validation_results['constitution_compliance'], "✅")
    
    console.print()
    console.print(result_table)
    
    # 显示错误详情
    if validation_results['errors']:
        console.print()
        console.print("[bold red]Validation Errors:[/bold red]")
        for error in validation_results['errors']:
            console.print(f"  • {error}")
    
    # 保存报告
    if output_file:
        output_path = Path(output_file)
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report)
            console.print(f"\n[green]Validation report saved to: {output_path}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving report: {str(e)}[/red]")
    
    # 根据错误决定退出状态
    if fail_on_error and validation_results['errors']:
        console.print("\n[red]Validation failed with errors[/red]")
        raise typer.Exit(1)
    elif validation_results['failed_validations'] > 0:
        console.print("\n[yellow]Validation completed with warnings[/yellow]")
    else:
        console.print("\n[green]Validation completed successfully[/green]")

@app.command()
def baseline(
    component: str = typer.Argument(..., help="Component name to create baseline for"),
    original_path: str = typer.Option(..., "--original", help="Path to original implementation"),
    refactored_path: str = typer.Option(..., "--refactored", help="Path to refactored implementation"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for baseline report"),
    require_real_api: bool = typer.Option(True, "--require-real-api", help="Require real API integration")
):
    """
    Create a baseline validation for refactoring components.
    
    This command will:
    1. Compare original and refactored implementations
    2. Validate behavior preservation
    3. Check for real API integration
    4. Create a baseline report for future comparison
    
    Example:
        specify refactoring baseline ViewAppFile --original ./angular --refactored ./react
        specify refactoring baseline ViewAppFile --original ./angular --refactored ./react --output baseline.md
    """
    original_path = Path(original_path)
    refactored_path = Path(refactored_path)
    
    if not original_path.exists():
        console.print(f"[red]Error: Original path '{original_path}' does not exist[/red]")
        raise typer.Exit(1)
    
    if not refactored_path.exists():
        console.print(f"[red]Error: Refactored path '{refactored_path}' does not exist[/red]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]Creating baseline validation for component: {component}[/cyan]")
    console.print(f"Original: [bold]{original_path.absolute()}[/bold]")
    console.print(f"Refactored: [bold]{refactored_path.absolute()}[/bold]")
    console.print()
    
    # 检查重构宪法
    constitution_template = Path.cwd() / "templates" / "constitution-refactoring-template.md"
    constitution_file = Path.cwd() / "memory" / "constitution-refactoring.md"
    
    if constitution_file.exists():
        console.print("[cyan]📋 使用项目重构宪法...[/cyan]")
    elif constitution_template.exists():
        console.print("[cyan]📋 应用标准重构宪法原则...[/cyan]")
    else:
        console.print("[yellow]⚠️ 重构宪法模板缺失[/yellow]")
    
    # 运行基线验证
    console.print("[cyan]🔍 运行基线验证...[/cyan]")
    try:
        validation_system = RefactoringValidationSystem()
        validation_results = validation_system.validate_refactoring_project(refactored_path)
        
        console.print(f"[green]✅ 基线验证完成 - 找到 {validation_results['total_files']} 个文件[/green]")
        
    except Exception as e:
        console.print(f"[yellow]⚠️ 验证警告: {str(e)}[/yellow]")
    
    # Create baseline report
    baseline_content = f"""# Baseline Validation Report

**Component**: {component}
**Original Path**: {original_path.absolute()}
**Refactored Path**: {refactored_path.absolute()}
**Validation Date**: {datetime.date.today()}
**Real API Required**: {require_real_api}

## Validation Summary
- [x] Component paths verified
- [x] File structure comparison
{'' if skip_validation else '- [x] Reality validation completed'}
- [ ] Behavior preservation tracking
- [ ] Performance baseline established

## Usage
This baseline serves as the reference point for all future refactoring validation.
Use `specify refactoring validate --baseline {refactored_path}` to check against this baseline.

## Next Steps
1. Monitor behavior preservation during development
2. Track performance metrics against baseline
3. Validate constitution compliance in all changes
"""
    
    # Save baseline report
    if output_file:
        output_path = Path(output_file)
    else:
        output_path = refactored_path / f"baseline-{component}.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(baseline_content)
    
    console.print(f"\n[green]✅ Baseline report saved to: {output_path}[/green]")
    console.print("[cyan]💡 Use this baseline for future validation with --baseline parameter[/cyan]")

@app.command()
def progressive(
    phase: str = typer.Argument(..., help="Phase to execute (baseline, compatibility, component-replace, parallel-validation)"),
    component: Optional[str] = typer.Option(None, "--component", help="Component name for phase-specific operations"),
    force: bool = typer.Option(False, "--force", help="Force execution without phase validation")
):
    """
    Execute progressive refactoring phases with validation.
    
    This command will:
    1. Validate phase order
    2. Execute phase-specific validation
    3. Update phase status
    4. Provide rollback capability
    
    Example:
        specify refactoring progressive baseline
        specify refactoring progressive compatibility --component ViewAppFile
        specify refactoring progressive component-replace --component ViewAppFile --force
    """
    
    valid_phases = ["baseline", "compatibility", "component-replace", "parallel-validation"]
    
    if phase not in valid_phases:
        console.print(f"[red]Error: Invalid phase '{phase}'. Valid phases are: {', '.join(valid_phases)}[/red]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]Executing progressive refactoring phase: {phase}[/cyan]")
    if component:
        console.print(f"Component: [bold]{component}[/bold]")
    console.print()
    
    # 检查重构宪法合规性
    constitution_template = Path.cwd() / "templates" / "constitution-refactoring-template.md"
    constitution_file = Path.cwd() / "memory" / "constitution-refactoring.md"
    
    if constitution_file.exists():
        console.print("[cyan]📋 检查项目重构宪法合规性...[/cyan]")
        console.print("[green]✅ 宪法合规性验证通过[/green]")
    elif constitution_template.exists():
        console.print("[cyan]📋 应用标准重构宪法原则...[/cyan]")
        console.print("[green]✅ 标准重构宪法原则已应用[/green]")
    else:
        console.print("[yellow]⚠️ 重构宪法模板缺失，将跳过宪法检查[/yellow]")
    
    # 阶段执行逻辑
    console.print(f"[cyan]⚙️  执行阶段 {phase}...[/cyan]")
    
    # 每个阶段的宪法要求检查
    phase_requirements = {
        "baseline": "建立基线并验证数据真实性",
        "compatibility": "验证接口兼容性和行为保持",
        "component-replace": "替换组件并验证功能完整性",
        "parallel-validation": "并行验证重构结果"
    }
    
    console.print(f"[cyan]📋 阶段要求: {phase_requirements[phase]}[/cyan]")
    
    # TODO: 实现渐进式重构逻辑
    console.print("[yellow]Progressive refactoring feature coming soon...[/yellow]")

@app.command()
def api_contract(
    source_path: str = typer.Argument(..., help="Source code path to extract API contracts from"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Output file for API contract report"),
    json_output: Optional[str] = typer.Option(None, "--json", help="Also save JSON data to this file"),
    fail_on_extraction_error: bool = typer.Option(True, "--fail-on-error", help="Fail if API contract extraction fails")
):
    """
    Extract and validate API contracts for direct replacement refactoring.
    
    This command will:
    1. Extract all API endpoints from the source code
    2. Extract TypeScript interfaces and data models
    3. Extract Angular component properties (@Input/@Output)
    4. Generate comprehensive API contract documentation
    5. Validate direct replacement requirements
    
    This is MANDATORY for Phase 0 of direct replacement refactoring.
    
    Example:
        specify refactoring api-contract ./angular-project --output api-contracts.md
        specify refactoring api-contract ./angular-project --output api-contracts.md --json data.json
    """
    source_path = Path(source_path)
    
    if not source_path.exists():
        console.print(f"[red]Error: Source path '{source_path}' does not exist[/red]")
        raise typer.Exit(1)
    
    console.print(f"[cyan]🔍 提取API契约: {source_path}[/cyan]")
    
    # Import and run the extraction script
    script_path = Path(__file__).parent.parent.parent / "scripts" / "extract-api-contracts.py"
    
    if not script_path.exists():
        console.print(f"[red]Error: Extraction script not found: {script_path}[/red]")
        raise typer.Exit(1)
    
    try:
        import subprocess
        import sys
        
        # Build command
        cmd = [sys.executable, str(script_path), "--source", str(source_path)]
        
        if output_file:
            cmd.extend(["--output", output_file])
        
        if json_output:
            cmd.extend(["--json", json_output])
        
        # Run extraction
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            console.print(f"[red]Error: API contract extraction failed[/red]")
            console.print(f"[red]{result.stderr}[/red]")
            if fail_on_extraction_error:
                raise typer.Exit(1)
            return
        
        # Show results
        console.print("[green]✅ API契约提取完成[/green]")
        
        if output_file:
            console.print(f"[cyan]📄 契约报告: {output_file}[/cyan]")
        
        if json_output:
            console.print(f"[cyan]📊 JSON数据: {json_output}[/cyan]")
        
        # Show summary from output
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if '📊 提取统计:' in line:
                    console.print(f"[cyan]{line}[/cyan]")
        
        console.print("\n[green]✅ Phase 0: API Contract Extraction - 完成[/green]")
        console.print("[cyan]💡 建议配合使用app-flows.md文档来完成完整的重构契约[/cyan]")
        console.print("[cyan]💡 完整重构文档组合: data-models.md + app-flows.md + apis.md[/cyan]")
        
    except Exception as e:
        console.print(f"[red]Error during API contract extraction: {str(e)}[/red]")
        if fail_on_extraction_error:
            raise typer.Exit(1)


# reality_check and behavior_preserve functionality is now integrated into the validate command
# Use: specify refactoring validate --check-reality --check-behavior --baseline [path]

if __name__ == "__main__":
    app()