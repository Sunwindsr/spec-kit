# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spec Kit** is a comprehensive toolkit for implementing **Spec-Driven Development (SDD)** - a revolutionary methodology that inverts traditional software development by making specifications executable rather than just guiding implementation.

### Core Components

- **Specify CLI** (`src/specify_cli/`) - Python-based command-line tool for bootstrapping SDD projects
- **Template System** (`templates/`) - Structured templates for specifications, implementation plans, and task generation
- **Script Infrastructure** (`scripts/`) - Cross-platform scripts (Bash/PowerShell) for development workflows
- **Documentation** (`docs/`) - Comprehensive documentation built with DocFX

## Architecture

### Spec-Driven Development Methodology

The project implements a four-phase workflow:

1. **`/constitution`** - Establish project governing principles and development guidelines
2. **`/specify`** - Create feature specifications focusing on "what" and "why" (not tech stack)
3. **`/plan`** - Generate technical implementation plans with chosen technology stack
4. **`/tasks`** - Create actionable task lists for implementation
5. **`/implement`** - Execute implementation following TDD principles

### Constitutional Governance

All development follows **9 constitutional principles**:
1. **Library-First**: Every feature starts as a standalone library
2. **CLI Interface**: All functionality exposed via text-based CLI
3. **Test-First**: Strict TDD - tests before implementation
4. **Integration Testing**: Real environments over mocks
5. **Observability**: Text I/O for debuggability
6. **Versioning**: Semantic versioning with clear breaking changes
7. **Simplicity**: YAGNI principles, minimal projects
8. **Anti-Abstraction**: Use frameworks directly
9. **Integration-First**: Contract testing before implementation

## Development Commands

### CLI Development

```bash
# Install dependencies
uv sync

# Test CLI locally
uv run specify --help

# Test with sample project
uv run specify init test-project --ai claude

# Check system requirements
uv run specify check
```

### Key CLI Commands

```bash
# Initialize new project
specify init <project-name> --ai <agent> --script <sh|ps>

# Available AI assistants: claude, gemini, copilot, cursor, qwen, opencode, codex, windsurf
# Available script types: sh (POSIX), ps (PowerShell)

# Examples:
specify init my-project --ai claude
specify init my-project --ai cursor --script ps
specify init --here --ai copilot
```

### Slash Commands (in initialized projects)

After running `specify init`, the following slash commands are available:

- `/constitution` - Create or update project governing principles
- `/specify` - Define feature specifications (requirements and user stories)
- `/plan` - Create technical implementation plans
- `/tasks` - Generate actionable task lists
- `/implement` - Execute implementation following TDD

## Technology Stack

### Core CLI (Python)
- **Language**: Python 3.11+
- **Package Management**: uv
- **CLI Framework**: Typer
- **UI/Output**: Rich (terminal formatting)
- **HTTP Client**: httpx with truststore
- **Build System**: Hatchling

### Supported AI Agents
- Claude Code (Anthropic)
- GitHub Copilot
- Gemini CLI (Google)
- Cursor
- Qwen Code (Alibaba)
- opencode
- Windsurf IDE
- Codex CLI

## Directory Structure

```
spec-kit/
├── src/specify_cli/          # Core CLI implementation
├── templates/               # SDD workflow templates
│   ├── commands/            # Agent-specific command templates
│   ├── spec-template.md     # Feature specification template
│   ├── plan-template.md     # Implementation plan template
│   └── tasks-template.md    # Task generation template
├── scripts/                 # Cross-platform workflow scripts
│   ├── bash/               # Unix/Linux/macOS scripts
│   └── powershell/         # Windows PowerShell scripts
├── memory/                 # Constitutional principles and governance
├── docs/                   # Documentation source (DocFX-based)
└── media/                  # Project branding and demo assets
```

## Development Guidelines

### Code Quality Standards

- **No emojis in PowerShell scripts** - Compatibility requirement for Windows environments
- **Clean git commit messages** - No special characters that affect CI/CD (| & ; $ > < `)
- **Template-driven development** - Use structured templates for consistent output
- **Constitutional compliance** - All architectural decisions must follow the 9 articles

### Script Compatibility

- **POSIX scripts** (`scripts/bash/`) - For Unix/Linux/macOS
- **PowerShell scripts** (`scripts/powershell/`) - For Windows
- **Cross-platform support** - Both script types provide identical functionality

### Multi-Agent Support

The project supports multiple AI coding assistants with:
- Agent-specific directory structures
- Unified workflow across different environments
- Pluggable architecture for new agents

## Key Innovation Points

### Executable Specifications
Transform natural language requirements into working code through structured templates and AI interpretation.

### Multi-Agent Ecosystem
Support for multiple AI coding assistants while maintaining consistent workflows and architectural principles.

### Constitutional Governance
Immutable principles ensure generated code maintains quality, simplicity, and testability across different AI models and time periods.

### Template-Driven Quality
Sophisticated prompts that constrain LLM behavior to produce consistent, maintainable specifications and implementations.

## Cross-Platform Considerations

- **Windows**: PowerShell scripts, no emoji usage
- **macOS/Linux**: Bash scripts with proper execute permissions
- **Universal**: Python-based CLI with consistent behavior

## Testing and Quality Assurance

### CLI Testing
```bash
# Test CLI functionality
uv run specify check

# Test project initialization
uv run specify init test-project --ai claude --no-git

# Verify template extraction
ls test-project/.specify/
```

### Script Validation
- Ensure all POSIX scripts have execute permissions
- Validate PowerShell scripts for Windows compatibility
- Test cross-platform script functionality

## Important Notes

- **Always use the main dispatcher script** for project initialization
- **Follow constitutional principles** in all architectural decisions
- **Maintain template consistency** across different AI agents
- **Preserve cross-platform compatibility** for all scripts
- **Use structured specifications** that are testable and unambiguous