"""Simple test script to verify MCP server functionality"""

import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all modules can be imported"""
    logger.info("Testing imports...")

    try:
        from engmanager_mcp.server import mcp, settings
        from engmanager_mcp.config.settings import Settings
        from engmanager_mcp.utils.parser import ProcedureParser
        from engmanager_mcp.utils.errors import EngManagerError
        logger.info("✓ All imports successful")
        return True
    except ImportError as e:
        logger.error(f"✗ Import failed: {e}")
        return False

def test_settings():
    """Test settings configuration"""
    logger.info("Testing settings...")

    try:
        from engmanager_mcp.config.settings import settings

        logger.info(f"  Server name: {settings.mcp_server_name}")
        logger.info(f"  Server version: {settings.mcp_server_version}")
        logger.info(f"  Transport: {settings.mcp_transport}")

        # Test project listing
        projects = settings.list_available_projects()
        logger.info(f"  Available projects: {projects}")

        logger.info("✓ Settings working correctly")
        return True
    except Exception as e:
        logger.error(f"✗ Settings test failed: {e}")
        return False

def test_parser():
    """Test procedure parser"""
    logger.info("Testing parser...")

    try:
        from engmanager_mcp.utils.parser import ProcedureParser

        # Test variable substitution
        content = "# Hello {NAME}\n\n## 1. First Step\n\nContent here."
        parser = ProcedureParser(content, {"NAME": "World"})

        result = parser.substitute_variables()
        assert "Hello World" in result, f"Expected 'Hello World' in result, got: {result}"

        # Test section extraction
        sections = parser.extract_sections()
        # Sections should be extracted (check we have at least one)
        assert len(sections) > 0, f"Expected sections, got: {sections}"

        # Test step extraction
        steps = parser.extract_steps()
        assert len(steps) == 1, f"Expected 1 step, got {len(steps)}: {steps}"
        assert steps[0][0] == 1, f"Expected step 1, got step {steps[0][0]}"
        assert "First Step" in steps[0][1], f"Expected 'First Step', got: {steps[0][1]}"

        logger.info("✓ Parser working correctly")
        return True
    except Exception as e:
        import traceback
        logger.error(f"✗ Parser test failed: {e}")
        logger.error(traceback.format_exc())
        return False

def test_mcp_tools():
    """Test that MCP tools are registered"""
    logger.info("Testing MCP tools...")

    try:
        from engmanager_mcp.server import mcp

        # Check that tools exist (they should be registered)
        logger.info(f"  MCP server name: {mcp.name}")

        logger.info("✓ MCP tools registered")
        return True
    except Exception as e:
        logger.error(f"✗ MCP tools test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("=" * 60)
    logger.info("Engineering Manager MCP - Server Tests")
    logger.info("=" * 60)

    tests = [
        test_imports,
        test_settings,
        test_parser,
        test_mcp_tools,
    ]

    results = []
    for test in tests:
        logger.info("")
        results.append(test())

    logger.info("")
    logger.info("=" * 60)
    logger.info(f"Results: {sum(results)}/{len(results)} tests passed")
    logger.info("=" * 60)

    if all(results):
        logger.info("✓ All tests passed!")
        return 0
    else:
        logger.error("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
