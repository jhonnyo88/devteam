"""
Tests for Developer agent tools.

PURPOSE:
Test suite for all Developer agent tools:
- CodeGenerator
- APIBuilder
- GitOperations
- ComponentBuilder
- ArchitectureValidator
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

# Import tools
from ..tools.code_generator import CodeGenerator
from ..tools.api_builder import APIBuilder
from ..tools.git_operations import GitOperations
from ..tools.component_builder import ComponentBuilder
from ..tools.architecture_validator import ArchitectureValidator


class TestCodeGenerator:
    """Test suite for CodeGenerator tool."""
    
    @pytest.fixture
    def code_generator(self):
        """Create CodeGenerator instance for testing."""
        return CodeGenerator()
    
    def test_initialization(self, code_generator):
        """Test CodeGenerator initialization."""
        assert code_generator is not None
        assert hasattr(code_generator, 'code_standards')
        assert hasattr(code_generator, 'performance_budgets')
    
    @pytest.mark.asyncio
    async def test_typescript_error_check(self, code_generator):
        """Test TypeScript error checking."""
        components = [
            {"name": "Component1", "typescript_errors": 0},
            {"name": "Component2", "typescript_errors": 2}
        ]
        
        total_errors = await code_generator.check_typescript_errors(components)
        assert total_errors == 2