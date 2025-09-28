#!/usr/bin/env python3
"""
Refactoring Template Validation Script

This script validates that refactoring templates are using the new tool-assisted approach
and provides guidance on improving template quality.
"""

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any


def validate_app_flows_template(template_path: Path) -> Dict[str, Any]:
    """Validate app-flows template for tool-assisted approach"""
    result = {
        "template": "app-flows-refactoring-template.md",
        "issues": [],
        "recommendations": [],
        "score": 0
    }
    
    try:
        content = template_path.read_text(encoding='utf-8')
        
        # Check for tool-assisted approach
        if "interactive-element-discovery.py" in content:
            result["score"] += 30
        else:
            result["issues"].append("Missing reference to interactive-element-discovery.py tool")
            result["recommendations"].append("Add tool execution section with interactive-element-discovery.py")
        
        # Check for structured analysis sections
        if "交互元素发现分析" in content:
            result["score"] += 20
        else:
            result["issues"].append("Missing interactive element discovery section")
        
        # Check for importance levels
        if "P0" in content and "P1" in content and "P2" in content:
            result["score"] += 20
        else:
            result["issues"].append("Missing importance level classification (P0/P1/P2)")
        
        # Check for command examples
        if "python3 .specify/scripts/interactive-element-discovery.py" in content:
            result["score"] += 15
        else:
            result["recommendations"].append("Add tool execution command examples")
        
        # Check for component complexity analysis
        if "复杂度" in content or "复杂" in content:
            result["score"] += 15
        else:
            result["recommendations"].append("Add component complexity analysis guidance")
        
    except Exception as e:
        result["issues"].append(f"Error reading template: {e}")
    
    return result


def validate_api_contracts_template(template_path: Path) -> Dict[str, Any]:
    """Validate api-contracts template for tool-assisted approach"""
    result = {
        "template": "api-contracts-refactoring-template.md",
        "issues": [],
        "recommendations": [],
        "score": 0
    }
    
    try:
        content = template_path.read_text(encoding='utf-8')
        
        # Check for tool-assisted approach
        if "工具辅助" in content:
            result["score"] += 30
        else:
            result["issues"].append("Missing tool-assisted approach description")
            result["recommendations"].append("Add tool-assisted analysis section")
        
        # Check for API extraction tools
        if "extract-api-contracts.py" in content:
            result["score"] += 20
        else:
            result["issues"].append("Missing reference to API extraction tools")
        
        # Check for structured analysis sections
        if "工具辅助的API分析" in content:
            result["score"] += 20
        else:
            result["recommendations"].append("Add tool-assisted API analysis section")
        
        # Check for execution steps
        if "执行步骤" in content:
            result["score"] += 15
        else:
            result["recommendations"].append("Add tool execution steps")
        
        # Check for risk identification
        if "风险识别" in content:
            result["score"] += 15
        else:
            result["recommendations"].append("Add risk identification guidance")
        
    except Exception as e:
        result["issues"].append(f"Error reading template: {e}")
    
    return result


def check_interactive_element_script(script_path: Path) -> Dict[str, Any]:
    """Check if interactive-element-discovery.py script exists and is executable"""
    result = {
        "script": "interactive-element-discovery.py",
        "exists": False,
        "executable": False,
        "issues": [],
        "recommendations": []
    }
    
    if script_path.exists():
        result["exists"] = True
        if script_path.stat().st_mode & 0o111:
            result["executable"] = True
        else:
            result["issues"].append("Script is not executable")
            result["recommendations"].append("Run: chmod +x scripts/interactive-element-discovery.py")
    else:
        result["issues"].append("Script does not exist")
        result["recommendations"].append("Create the interactive-element-discovery.py script")
    
    return result


def generate_validation_report(results: List[Dict[str, Any]], script_check: Dict[str, Any]) -> str:
    """Generate a comprehensive validation report"""
    report = []
    
    report.append("# Refactoring Template Validation Report")
    report.append(f"Generated: {__import__('datetime').datetime.now().isoformat()}")
    report.append("")
    
    # Overall score
    total_score = sum(r.get("score", 0) for r in results)
    max_score = len(results) * 100
    overall_percentage = (total_score / max_score) * 100 if max_score > 0 else 0
    
    report.append(f"## Overall Score: {overall_percentage:.1f}%")
    report.append("")
    
    # Script check
    report.append("## Script Availability")
    report.append(f"- interactive-element-discovery.py: {'✓' if script_check['exists'] else '✗'}")
    report.append(f"- Executable: {'✓' if script_check['executable'] else '✗'}")
    if script_check["issues"]:
        for issue in script_check["issues"]:
            report.append(f"  - ⚠️ {issue}")
    report.append("")
    
    # Template results
    for result in results:
        report.append(f"## {result['template']}")
        report.append(f"Score: {result.get('score', 0)}/100")
        report.append("")
        
        if result["issues"]:
            report.append("### Issues:")
            for issue in result["issues"]:
                report.append(f"- ❌ {issue}")
            report.append("")
        
        if result["recommendations"]:
            report.append("### Recommendations:")
            for rec in result["recommendations"]:
                report.append(f"- 💡 {rec}")
            report.append("")
    
    # Summary
    report.append("## Summary")
    if overall_percentage >= 80:
        report.append("🎉 Templates are well-structured for tool-assisted refactoring!")
    elif overall_percentage >= 60:
        report.append("👍 Templates are mostly good but need some improvements.")
    else:
        report.append("🚨 Templates need significant updates to support tool-assisted refactoring.")
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description='Validate refactoring templates for tool-assisted approach')
    parser.add_argument('--output', help='Output file for validation report')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    # Check templates
    templates_dir = Path("templates")
    results = []
    
    app_flows_template = templates_dir / "app-flows-refactoring-template.md"
    if app_flows_template.exists():
        results.append(validate_app_flows_template(app_flows_template))
    
    api_contracts_template = templates_dir / "api-contracts-refactoring-template.md"
    if api_contracts_template.exists():
        results.append(validate_api_contracts_template(api_contracts_template))
    
    # Check script
    script_check = check_interactive_element_script(Path("scripts/interactive-element-discovery.py"))
    
    # Generate report
    if args.format == 'json':
        output_data = {
            "validation_results": results,
            "script_check": script_check,
            "overall_score": sum(r.get("score", 0) for r in results) / len(results) if results else 0
        }
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            print(f"Validation report saved to {args.output}")
        else:
            print(json.dumps(output_data, indent=2, ensure_ascii=False))
    else:
        report = generate_validation_report(results, script_check)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Validation report saved to {args.output}")
        else:
            print(report)


if __name__ == "__main__":
    main()