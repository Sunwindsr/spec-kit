"""
重构验证命令 - 提供重构过程中的强制验证功能
"""

import typer
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
    4. Generate a comprehensive validation report
    
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
    console.print(f"[cyan]Creating baseline validation for component: {component}[/cyan]")
    console.print(f"Original: [bold]{original_path}[/bold]")
    console.print(f"Refactored: [bold]{refactored_path}[/bold]")
    console.print()
    
    # TODO: 实现基线验证逻辑
    console.print("[yellow]Baseline validation feature coming soon...[/yellow]")

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
    
    # TODO: 实现渐进式重构逻辑
    console.print("[yellow]Progressive refactoring feature coming soon...[/yellow]")

@app.command()
def reality_check(
    project_path: str = typer.Argument(".", help="Path to the refactoring project"),
    file_pattern: Optional[str] = typer.Option(None, "--pattern", help="File pattern to check (e.g., '*.tsx')"),
    fail_on_mock: bool = typer.Option(True, "--fail-on-mock", help="Fail if mock data is detected")
):
    """
    Perform reality check on refactoring code.
    
    This command will:
    1. Scan for mock data patterns
    2. Check for real API integration
    3. Validate business logic completeness
    4. Report reality violations
    
    Example:
        specify refactoring reality-check ./my-project
        specify refactoring reality-check ./my-project --pattern "*.tsx" --fail-on-mock
    """
    project_path = Path(project_path)
    
    if not project_path.exists():
        console.print(f"[red]Error: Project path '{project_path}' does not exist[/red]")
        raise typer.Exit(1)
    
    console.print("[cyan]Performing reality check...[/cyan]")
    console.print(f"Project: [bold]{project_path.absolute()}[/bold]")
    if file_pattern:
        console.print(f"Pattern: [bold]{file_pattern}[/bold]")
    console.print()
    
    # TODO: 实现现实检查逻辑
    console.print("[yellow]Reality check feature coming soon...[/yellow]")

if __name__ == "__main__":
    app()