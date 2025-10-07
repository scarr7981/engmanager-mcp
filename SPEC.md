# ENGINEERING MANAGER MCP

*Synopsis:* An MCP that LLMs can reference to conform to established development procedures without having to be reminded. MCPs can use this endpoint to ask "what's next" as they are working on issues.

## Overview of features
- Instructs LLMs on "next steps"
    - For example, see ./EXAMPLE_PROCEDURE.md for an example procedure
- This tool needs to be flexible enough so that a user can write a script for an MCP to follow. Use the variables in EXAMPLE_PROCEDURE.md to create a template.
- This MCP should be able to be flexible enough to handle multiple projects at the same time, so the LLM might send a flag to the MCP telling it which project it is working on, and the MCP will use <projectname-config.json> to offer instructions. 

## Tech notes
- I want this MCP to be available via pypi the same way cargoshipper-mcp is available. Please use cargoshipper-mcp as a template for development.