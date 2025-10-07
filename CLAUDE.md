# CLAUDE.md - Engineering Manager MCP

This file provides guidance to Claude Code when working with the Engineering Manager MCP project.

## Project Overview

**Engineering Manager MCP** is a Model Context Protocol (MCP) server that provides LLMs with structured workflow guidance and "next step" instructions for development procedures. It eliminates the need to repeatedly explain development workflows by allowing LLMs to query standardized procedures on demand.

## Tech Stack

- **Python**: 3.11+
- **MCP Framework**: FastMCP (from official MCP SDK)
- **Configuration**: Pydantic + pydantic-settings
- **Packaging**: setuptools with pyproject.toml
- **Distribution**: PyPI via uvx

## Project Structure

```
engmanager-mcp/
├── engmanager_mcp/           # Main package
│   ├── __init__.py
│   ├── server.py            # MCP server entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py      # Configuration loading
│   ├── tools/
│   │   ├── __init__.py
│   │   └── workflow.py      # MCP tools
│   ├── resources/
│   │   ├── __init__.py
│   │   └── procedures.py    # MCP resources
│   └── utils/
│       ├── __init__.py
│       ├── parser.py         # Template parser
│       └── errors.py         # Custom exceptions
├── procedures/               # Example procedures
│   ├── example-workflow.md
│   └── example-config.json
├── pyproject.toml           # Python packaging
├── requirements.txt
├── README.md
├── LICENSE
└── test_server.py           # Test suite
```

## Key Components

### 1. Server (`server.py`)
- FastMCP initialization
- Tool and resource registration
- Transport configuration (stdio/http)
- Logging setup

### 2. Configuration (`config/settings.py`)
- Multi-path configuration loading
- Project discovery
- Settings management via Pydantic

### 3. Parser (`utils/parser.py`)
- Markdown parsing
- Template variable substitution
- Section extraction
- Numbered step extraction

### 4. Tools (`tools/workflow.py`)
- `get_next_step` - Return next workflow step
- `get_workflow_section` - Return specific section
- `list_workflow_steps` - List all steps
- `list_available_projects` - Show configured projects
- `get_project_info` - Show project details

### 5. Resources (`resources/procedures.py`)
- `engmanager://procedures/{project}` - Full procedure
- `engmanager://config/{project}` - Project config
- `engmanager://templates` - Template variable docs
- `engmanager://projects` - Project list

## Development Workflow

### Setting Up Development Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install in editable mode
pip install -e .

# Run tests
python test_server.py
```

### Running the Server

```bash
# Development mode (local)
python -m engmanager_mcp.server

# Or via CLI entry point
engmanager-mcp

# With custom environment
ENGMANAGER_DEFAULT_PROJECT=myproject engmanager-mcp
```

### Testing

```bash
# Run test suite
python test_server.py

# Manual MCP testing
# Configure .mcp.dev.json and test with Claude Desktop or MCP inspector
```

## Configuration

### Project Configuration Format

Files should be named `<project>-config.json` and placed in:
- `./procedures/`
- `~/.config/engmanager-mcp/`
- `/etc/engmanager-mcp/`

```json
{
  "project_name": "myproject",
  "procedure_file": "myproject-workflow.md",
  "variables": {
    "REPO_OWNER": "username",
    "REPO_NAME": "repository",
    "DEFAULT_BRANCH": "main"
  }
}
```

### Procedure File Format

Markdown files with numbered sections for workflow steps:

```markdown
# Project Workflow

## 1. First Step

Instructions for first step...

## 2. Second Step

Instructions for second step...
```

Template variables use `{VARIABLE_NAME}` syntax.

## Common Development Tasks

### Adding a New Tool

1. Add function to `tools/workflow.py`
2. Decorate with `@mcp.tool()`
3. Include docstring with examples
4. Register in `register_tools()`

### Adding a New Resource

1. Add function to `resources/procedures.py`
2. Decorate with `@mcp.resource("uri://path")`
3. Include docstring
4. Register in `register_resources()`

### Adding a New Configuration Option

1. Add field to `Settings` class in `config/settings.py`
2. Use Pydantic `Field` with description
3. Set appropriate default value
4. Update environment variable prefix if needed

### Debugging

```bash
# Increase log level
ENGMANAGER_MCP_LOG_LEVEL=DEBUG engmanager-mcp

# Test with specific project
ENGMANAGER_DEFAULT_PROJECT=test engmanager-mcp
```

## Publishing to PyPI

### Build Package

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build

# Check package
twine check dist/*
```

### Upload to PyPI

```bash
# Test PyPI first (recommended)
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

### GitHub Actions

Can be configured for automatic PyPI publishing on tagged releases. See `cargoshipper-mcp` for reference implementation.

## Design Patterns

### Based on cargoshipper-mcp

This project follows the structure and patterns from `cargoshipper-mcp`:
- FastMCP server initialization
- Tool and resource registration pattern
- Multi-path configuration loading
- Pydantic settings management
- PyPI packaging with uvx compatibility

### Inspired by EXAMPLE_PROCEDURE.md

The workflow guidance features are inspired by the Trowel.io development procedure, which demonstrates:
- Numbered workflow steps
- Tool recommendations
- Protocol enforcement
- Error recovery procedures
- Quality gates

## Best Practices

### Code Style
- Use type hints throughout
- Follow PEP 8 style guide
- Use Black for formatting (line length: 100)
- Use Ruff for linting

### Documentation
- Comprehensive docstrings for all public functions
- Include usage examples in docstrings
- Keep README up to date
- Document configuration options

### Error Handling
- Use custom exceptions from `utils/errors.py`
- Provide helpful error messages
- Log errors with appropriate levels
- Return user-friendly error strings from tools

### Testing
- Test all core functionality
- Include edge cases
- Verify error handling
- Test configuration loading

## Security Considerations

- No secrets in code or repository
- Configuration files may contain sensitive data (exclude from git)
- Template variables allow project-specific values without hardcoding
- Multi-path config allows user-level and system-level separation

## Related Projects

- **CargoShipper MCP**: Infrastructure automation MCP server (template project)
- **Trowel.io**: Project that inspired the workflow guidance features
- **Model Context Protocol**: Official MCP specification

## Environment Variables

- `ENGMANAGER_DEFAULT_PROJECT` - Default project name
- `ENGMANAGER_MCP_LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR)
- `ENGMANAGER_PROCEDURES_DIR` - Custom procedures directory path
- `ENGMANAGER_MCP_TRANSPORT` - Transport mode (stdio/http)
- `ENGMANAGER_CONFIG_PATHS` - Colon-separated config paths

## Troubleshooting

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -e .` to install in editable mode
- Check PYTHONPATH includes project root

### Project Not Found
- Verify config file exists in search paths
- Check filename format: `<project>-config.json`
- Confirm `ENGMANAGER_DEFAULT_PROJECT` matches config

### Procedure File Not Found
- Check `procedure_file` path in config
- Verify markdown file exists in procedures directory
- Ensure file permissions are readable

### Template Variable Errors
- Variables must be UPPERCASE with underscores
- All referenced variables must be in config
- Check for typos in variable names

## Contributing

When working on this project:
1. Follow existing code patterns
2. Update tests for new features
3. Update README for user-facing changes
4. Update CLAUDE.md for developer-facing changes
5. Maintain backward compatibility
6. Use semantic versioning for releases

## Version History

- **1.0.0** - Initial release
  - Core MCP server implementation
  - Template parser with variable substitution
  - Multi-project configuration support
  - Example workflow included
  - Full documentation
