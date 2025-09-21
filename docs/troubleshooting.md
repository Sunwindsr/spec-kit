# Troubleshooting & Lessons Learned

This document captures common issues, solutions, and reusable lessons learned during development.

## Template Integration Issues

### Issue: Template Format Confusion
**Problem**: Initially created documentation-style templates instead of proper Spec Kit templates with placeholders.
**Lesson**: Spec Kit templates must include placeholders for quick application, not just documentation.
**Solution**: Always include structured placeholders that can be easily filled in for actual use.

### Issue: String Replacement Failures
**Problem**: Attempted to use string replacement on content that didn't exist in the target file.
**Lesson**: Verify string content before attempting replacements, or rewrite the file entirely when making substantial changes.
**Solution**: Use `Read` tool to verify content before editing, or use `Write` tool for complete rewrites.

## Script Development Issues

### Issue: Cross-Platform Compatibility
**Problem**: Scripts worked on one platform but failed on others due to path separators and command differences.
**Lesson**: Always test scripts for both bash (Linux/macOS) and PowerShell (Windows) compatibility.
**Solution**: 
- Use `chmod +x` for shell scripts only on non-Windows systems
- Handle path separators appropriately (`/` vs `\`)
- Use platform detection in PowerShell: `$IsLinux`, `$IsMacOS`, `$IsWindows`

### Issue: Missing Function Dependencies
**Problem**: Scripts referenced functions that didn't exist in common utilities.
**Lesson**: When creating new functionality, ensure all required helper functions are available.
**Solution**: Add missing functions to `common.sh` and `common.ps1` before referencing them in other scripts.

## Command Architecture Issues

### Issue: CLI vs Template Commands Confusion
**Problem**: Confused Python CLI commands (`specify init`) with AI agent template commands (`/constitution`).
**Lesson**: Spec Kit has two types of commands:
- CLI commands: Implemented in Python, run in terminal (`specify init`, `specify check`)
- Template commands: Used by AI agents, defined in markdown templates (`/constitution`, `/specify`)

**Solution**: Understand the difference and use appropriate mechanisms for each type.

### Issue: Fork Repository Integration
**Problem**: Need to integrate custom refactoring functionality with standard Spec Kit releases from GitHub.
**Lesson**: When extending an existing project, consider how to integrate with the official release mechanism rather than replacing it.
**Solution**: Create hybrid approach that downloads official releases and adds custom extensions.

## Naming Conventions

### Issue: Consistent Naming Pattern
**Problem**: Initial naming was inconsistent for refactoring commands.
**Lesson**: Establish consistent naming conventions early and stick to them.
**Solution**: Use trailing modifier format (`command-refactoring`) for all refactoring-specific functionality.

### Issue: Path References in Templates
**Problem**: Templates referenced incorrect paths for scripts and files.
**Lesson**: Verify that all referenced paths exist and are correct in the template system.
**Solution**: Use relative paths consistently and verify file locations before referencing.

## Git Integration Issues

### Issue: Git Repository Initialization
**Problem**: Multiple scripts trying to initialize git repositories caused conflicts.
**Lesson**: Coordinate git operations between different scripts to avoid conflicts.
**Solution**: Have one main script handle git initialization, and have others add changes to existing repositories.

### Issue: Commit Message Standards
**Problem**: Inconsistent commit message formats and potentially problematic characters.
**Lesson**: Follow consistent commit message standards and avoid special characters that might break CI/CD.
**Solution**: Use standard format without emojis or special characters, and include proper attribution.

## Development Workflow Issues

### Issue: Task Management
**Problem**: Lost track of complex multi-step tasks and their dependencies.
**Lesson**: Use structured task tracking for complex implementations.
**Solution**: Use `TodoWrite` tool to track progress through multi-step implementations.

### Issue: File Structure Confusion
**Problem**: Unclear about where files should be located and how they relate to each other.
**Lesson**: Document file structure clearly and understand the project layout before making changes.
**Solution**: Create clear documentation of file structure and relationships.

## Refactoring-Specific Issues

### Issue: Behavior Preservation Requirements
**Problem**: Initially unclear about what "behavior preservation" means in refactoring context.
**Lesson**: Be explicit about requirements and constraints, especially for critical concepts like behavior preservation.
**Solution**: Document specific requirements: same inputs → identical outputs, side effects, error types/messages, log levels/content.

### Issue: Frontend vs Backend Refactoring
**Problem**: Unclear about how frontend refactoring differs from backend refactoring.
**Lesson**: Different components have different refactoring constraints and allowances.
**Solution**: Specify that frontend refactoring allows UI component optimization while preserving layout and functionality.

## Release Process Issues

### Issue: Understanding Template Packaging
**Problem**: Unclear about how templates are packaged and released.
**Lesson**: Understand the release process and packaging system before extending it.
**Solution**: Study the existing release workflow and template creation scripts.

### Issue: Integration with Release System
**Problem**: Need to add refactoring templates to the existing release system.
**Lesson**: Extend existing systems rather than creating parallel systems.
**Solution**: Add refactoring templates to the existing template packaging workflow.

## Best Practices

### Template Development
1. Always include placeholders for user input
2. Use YAML frontmatter for metadata
3. Follow existing template structure and patterns
4. Test templates with actual AI agents

### Script Development
1. Support both bash and PowerShell
2. Include proper error handling
3. Use JSON output for machine-readable results
4. Include help text and usage examples

### Command Development
1. Understand the difference between CLI and template commands
2. Follow established naming conventions
3. Document command behavior clearly
4. Test with actual AI agents

### Integration Work
1. Study existing systems before extending them
2. Use hybrid approaches when combining custom and standard functionality
3. Maintain backward compatibility
4. Document integration points clearly

## Common Debugging Steps

1. **Template Issues**: Check YAML frontmatter, verify placeholders exist, test with actual AI agent
2. **Script Issues**: Test on multiple platforms, verify file permissions, check path references
3. **Command Issues**: Verify command registration, check template paths, test with AI agent
4. **Integration Issues**: Verify file structure, check dependencies, test end-to-end workflow