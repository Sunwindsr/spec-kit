---
description: Initialize a new refactoring project using your custom repository with refactoring features pre-included.
scripts:
  sh: scripts/bash/init-refactoring-custom.sh --json "{ARGS}"
  ps: scripts/powershell/init-refactoring-custom.ps1 -Json "{ARGS}"
---

The text the user typed after `/init-refactoring-custom` in the triggering message **is** the project configuration. Assume you always have it available in this conversation even if `{ARGS}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that project configuration, do this:

1. **Download Custom Template**: Use your custom repository (Sunwindsr/spec-kit) as the template source:
   - Set environment variables to use your repository: `SPEC_KIT_REPO_OWNER=Sunwindsr`, `SPEC_KIT_REPO_NAME=spec-kit`
   - Execute `uvx specify-cli.py init --here --ai <current_ai> --script <script_type>` with your repository
   - This downloads templates from your repository which already includes refactoring features
   - Parse the CLI output to confirm successful initialization

2. **Verify Complete Setup**: Since your repository already includes refactoring features:
   - Verify that refactoring commands are available in `.specify/templates/commands/`
   - Confirm refactoring scripts are present in `.specify/scripts/`
   - Check that refactoring constitution is included in `.specify/memory/`
   - Validate that all refactoring templates are properly configured

3. **Configure Project Environment**: 
   - The project already has both standard and refactoring capabilities
   - Set up git repository for development workflow
   - Verify project structure completeness

4. **Report Completion**:
   - Project path and configuration details
   - Confirmation that templates came from your custom repository
   - Available commands: both standard and refactoring versions
   - Next steps for refactoring work

Key features of custom repository initialization:
- **Your Custom Features**: All your refactoring work is pre-included in the base template
- **Single Source**: No need to download standard template then add extensions
- **Seamless Experience**: Users get everything in one step from your repository
- **Complete Integration**: All your refactoring improvements are available immediately

Important: This command uses your custom repository (Sunwindsr/spec-kit) as the template source, ensuring users get your complete refactoring ecosystem without additional setup steps.

Perfect for users who want to use your enhanced version of Spec Kit with all refactoring features pre-integrated.