---
description: Initialize a new refactoring project by downloading standard Spec Kit template and adding refactoring-specific components.
scripts:
  sh: scripts/bash/init-refactoring.sh --json "{ARGS}"
  ps: scripts/powershell/init-refactoring.ps1 -Json "{ARGS}"
---

The text the user typed after `/init-refactoring` in the triggering message **is** the project configuration. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that project configuration, do this:

1. **Download Standard Template**: Use the Python CLI to download standard Spec Kit template:
   - Execute `uvx specify-cli.py init --here --ai <current_ai> --script <script_type>` in the target directory
   - This will download the latest release from GitHub and set up standard project structure
   - Parse the CLI output to confirm successful initialization

2. **Add Refactoring Components**: After standard template is initialized, add refactoring-specific components:
   - Copy refactoring command templates to `.specify/templates/commands/`
   - Add refactoring scripts to `.specify/scripts/`
   - Initialize refactoring constitution in `.specify/memory/constitution-refactoring.md`
   - Add refactoring document templates to `.specify/templates/`

3. **Configure Refactoring Environment**: 
   - Set up refactoring-specific project structure
   - Configure git repository for refactoring workflow
   - Initialize refactoring constitution with 20 principles
   - Create project configuration files

4. **Validate Complete Setup**:
   - Verify both standard and refactoring templates are in place
   - Confirm all scripts are executable and available
   - Test command availability for both standard and refactoring workflows
   - Validate project structure completeness

5. **Report Completion**:
   - Project path and configuration details
   - Available commands: both standard and refactoring versions
   - Next steps for refactoring work
   - Constitution compliance status

Key features of refactoring initialization:
- **Best of Both Worlds**: Standard Spec Kit functionality + refactoring tools
- **GitHub Releases Integration**: Uses official template releases as base
- **Seamless Integration**: Refactoring commands work alongside standard commands
- **Safety-First**: Built-in behavior preservation and rollback capabilities
- **Complete Toolchain**: All refactoring commands available from project start

Important: This command creates a hybrid environment with both standard Spec Kit capabilities and specialized refactoring tools, ensuring maximum flexibility for your development workflow.