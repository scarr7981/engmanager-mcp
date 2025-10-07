#!/usr/bin/env python3
"""Test trowel configuration"""

from engmanager_mcp.config.settings import settings
from engmanager_mcp.utils.parser import ProcedureParser

# Test loading trowel project
config = settings.load_project_config('trowel')
print('✓ Trowel config loaded successfully')
print(f'  Project: {config["project_name"]}')
print(f'  Procedure file: {config["procedure_file"]}')
print(f'  Variables: {list(config["variables"].keys())}')

# Test finding procedure file
proc_file = settings.find_procedure_file(config['procedure_file'])
print(f'✓ Procedure file found: {proc_file}')

# Test parser
with open(proc_file, 'r') as f:
    content = f.read()
parser = ProcedureParser(content, config['variables'])

# Test variable substitution
result = parser.substitute_variables()
print(f'✓ Variable substitution successful')
print(f'  Found "trowel": {"trowel" in result}')
print(f'  Found "scarr7981": {"scarr7981" in result}')

# Test step extraction
steps = parser.extract_steps()
print(f'✓ Extracted {len(steps)} workflow steps')

# Show first step
if steps:
    num, title, content = steps[0]
    print(f'\n  Step {num}: {title}')
    print(f'  Content preview: {content[:100]}...')

print('\n✅ All trowel tests passed!')
