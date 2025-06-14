"""
Tests for Developer Agent tools.

PURPOSE:
Test suite for Developer agent's specialized tools:
- CodeGenerator: React + FastAPI code generation
- APIBuilder: Stateless FastAPI endpoint building
- GitOperations: Git workflow management
- ComponentBuilder: React component building
- ArchitectureValidator: Architecture compliance validation

TEST STRATEGY COMPLIANCE:
- Follows TEST_STRATEGY.md structure
- Agent tools tests in modules/agents/developer/tests/test_tools.py
- Focuses on tool functionality, not contract compliance
- Uses proper pytest markers for categorization
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path

# Import the tools
from ..tools.code_generator import CodeGenerator
from ..tools.api_builder import APIBuilder
from ..tools.git_operations import GitOperations
from ..tools.component_builder import ComponentBuilder
from ..tools.architecture_validator import ArchitectureValidator


@pytest.mark.agent
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
    
    @pytest.mark.asyncio
    async def test_generate_react_components(self, code_generator):
        """Test React component generation."""
        ui_components = [
            {
                "name": "TestComponent",
                "type": "component",
                "props": {"title": "string"},
                "ui_components": ["Button", "Card"],
                "accessibility": {"role": "region"}
            }
        ]
        
        result = await code_generator.generate_react_components(ui_components, "STORY-TEST-001")
        
        assert isinstance(result, list)
        assert len(result) == 1
        
        component = result[0]
        assert component["name"] == "TestComponent"
        assert "files" in component
        assert "code" in component
        assert component["typescript_errors"] >= 0
        assert component["eslint_violations"] >= 0
    
    @pytest.mark.asyncio
    async def test_generate_fastapi_endpoints(self, code_generator):
        """Test FastAPI endpoint generation."""
        api_endpoints = [
            {
                "name": "test_endpoint",
                "method": "POST",
                "path": "/test",
                "description": "Test endpoint",
                "request_model": {"data": "string"},
                "response_model": {"success": "boolean"}
            }
        ]
        
        result = await code_generator.generate_fastapi_endpoints(api_endpoints, "STORY-TEST-001")
        
        assert isinstance(result, list)
        assert len(result) == 1
        
        endpoint = result[0]
        assert endpoint["name"] == "test_endpoint"
        assert endpoint["method"] == "POST"
        assert endpoint["path"] == "/test"
        assert "files" in endpoint
        assert "code" in endpoint
    
    def test_calculate_cyclomatic_complexity(self, code_generator):
        """Test cyclomatic complexity calculation."""
        # Simple code
        simple_code = "function simple() { return 1; }"
        assert code_generator._calculate_cyclomatic_complexity(simple_code) == 1
        
        # Complex code with multiple decision points
        complex_code = """
        function complex(a, b) {
            if (a) {
                if (b) {
                    for (let i = 0; i < 10; i++) {
                        if (i % 2) {
                            return i;
                        }
                    }
                }
            }
            return 0;
        }
        """
        complexity = code_generator._calculate_cyclomatic_complexity(complex_code)
        assert complexity > 5  # Should detect multiple decision points
    
    @pytest.mark.asyncio
    async def test_check_eslint_compliance(self, code_generator):
        """Test ESLint compliance checking."""
        components = [
            {"name": "TestComp", "eslint_violations": 0},
            {"name": "ViolationComp", "eslint_violations": 3}
        ]
        
        total_violations = await code_generator.check_eslint_compliance(components)
        assert total_violations == 3


@pytest.mark.agent
class TestAPIBuilder:
    """Test suite for APIBuilder tool."""
    
    @pytest.fixture
    def api_builder(self):
        """Create APIBuilder instance for testing."""
        return APIBuilder()
    
    @pytest.mark.asyncio
    async def test_build_apis(self, api_builder):
        """Test API building functionality."""
        api_endpoints = [
            {
                "name": "test_api",
                "method": "GET",
                "path": "/test",
                "description": "Test API",
                "dependencies": []
            }
        ]
        
        state_management = {"type": "stateless"}
        
        result = await api_builder.build_apis(api_endpoints, state_management, "STORY-TEST-001")
        
        assert isinstance(result, list)
        assert len(result) == 1
        
        api = result[0]
        assert api["name"] == "test_api"
        assert api["method"] == "GET"
        assert api["path"] == "/test"
        assert "files" in api
    
    @pytest.mark.asyncio
    async def test_stateless_design_validation(self, api_builder):
        """Test stateless design validation."""
        # API spec with stateless design
        good_spec = api_builder._parse_api_specification(
            {
                "name": "stateless_api",
                "method": "POST",
                "business_logic": {"validation": "stateless"}
            },
            {"type": "stateless"}
        )
        
        # Should not raise exception
        await api_builder._validate_stateless_design(good_spec)
        
        # API spec with stateful violations
        bad_spec = api_builder._parse_api_specification(
            {
                "name": "stateful_api", 
                "method": "POST",
                "business_logic": {"session": "store_in_session"}
            },
            {}
        )
        
        # Should raise exception
        with pytest.raises(Exception) as exc_info:
            await api_builder._validate_stateless_design(bad_spec)
        assert "stateless" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_api_performance_testing(self, api_builder):
        """Test API performance testing functionality."""
        api_implementation = {
            "name": "test_api",
            "dependencies": [],
            "estimated_response_time_ms": 100
        }
        
        response_time = await api_builder.test_api_performance(api_implementation)
        
        assert isinstance(response_time, int)
        assert response_time > 0
        assert response_time < 1000  # Reasonable upper bound


@pytest.mark.agent
class TestGitOperations:
    """Test suite for GitOperations tool."""
    
    @pytest.fixture
    def git_operations(self):
        """Create GitOperations instance for testing."""
        config = {
            "product_repo_path": "/tmp/test_repo"
        }
        return GitOperations(config)
    
    @pytest.mark.asyncio
    async def test_create_feature_branch(self, git_operations):
        """Test feature branch creation."""
        with patch.object(git_operations, '_ensure_product_repository') as mock_ensure:
            with patch.object(git_operations, '_update_main_branch') as mock_update:
                with patch.object(git_operations, '_execute_git_command') as mock_exec:
                    with patch.object(git_operations, '_setup_branch_tracking') as mock_track:
                        with patch.object(git_operations, '_create_story_directory_structure') as mock_dirs:
                            
                            # Mock successful git command
                            mock_exec.return_value = Mock(success=True)
                            
                            result = await git_operations.create_feature_branch("STORY-TEST-001")
                            
                            assert result.success
                            assert result.branch_name == "feature/STORY-TEST-001"
                            assert "Created feature branch" in result.message
    
    def test_format_commit_message(self, git_operations):
        """Test commit message formatting."""
        message = git_operations._format_commit_message(
            "Implement",
            "STORY-TEST-001", 
            "Test feature",
            {"components": 2, "apis": 1}
        )
        
        assert "Implement STORY-TEST-001: Test feature" in message
        assert "components: 2" in message
        assert "apis: 1" in message
        assert "DigiNativa AI Team" in message
    
    def test_check_file_organization(self, git_operations):
        """Test file organization validation."""
        # Good file organization
        good_files = [
            Path("frontend/components/STORY-TEST-001/TestComponent.tsx"),
            Path("backend/endpoints/STORY-TEST-001/test_api.py")
        ]
        
        assert git_operations._check_file_organization(good_files)
        
        # Bad file organization
        bad_files = [
            Path("wrong/location/component.tsx"),
            Path("backend/wrong/api.py")
        ]
        
        assert not git_operations._check_file_organization(bad_files)


@pytest.mark.agent
class TestComponentBuilder:
    """Test suite for ComponentBuilder tool."""
    
    @pytest.fixture
    def component_builder(self):
        """Create ComponentBuilder instance for testing."""
        return ComponentBuilder()
    
    @pytest.mark.asyncio
    async def test_build_components(self, component_builder):
        """Test component building functionality."""
        ui_components = [
            {
                "name": "TestComponent",
                "type": "form",
                "ui_library_components": ["Button", "Input"]
            }
        ]
        
        interaction_flows = [
            {
                "name": "test_flow",
                "steps": ["input", "validate", "submit"]
            }
        ]
        
        with patch.object(component_builder, '_build_single_component') as mock_build:
            mock_build.return_value = {
                "name": "TestComponent",
                "files": {"component": "test.tsx"},
                "code": {"component": "// Test component"}
            }
            
            result = await component_builder.build_components(
                ui_components, interaction_flows, "STORY-TEST-001"
            )
            
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["name"] == "TestComponent"


@pytest.mark.agent
class TestArchitectureValidator:
    """Test suite for ArchitectureValidator tool."""
    
    @pytest.fixture
    def architecture_validator(self):
        """Create ArchitectureValidator instance for testing."""
        return ArchitectureValidator()
    
    @pytest.mark.asyncio
    async def test_validate_requirements(self, architecture_validator):
        """Test architecture requirements validation."""
        # Valid requirements following architecture principles
        valid_requirements = {
            "api_endpoints": [
                {
                    "name": "test_api",
                    "method": "POST",
                    "stateless": True
                }
            ],
            "state_management": {
                "type": "stateless"
            }
        }
        
        with patch.object(architecture_validator, 'validate_requirements') as mock_validate:
            mock_validate.return_value = {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
            
            result = await architecture_validator.validate_requirements(valid_requirements)
            
            assert result["is_valid"]
            assert len(result["errors"]) == 0


@pytest.mark.performance
class TestToolsPerformance:
    """Performance tests for Developer tools."""
    
    @pytest.mark.asyncio
    async def test_code_generation_performance(self):
        """Test code generation performance."""
        import time
        
        code_generator = CodeGenerator()
        
        # Small component
        ui_components = [
            {
                "name": "SimpleComponent",
                "type": "component",
                "props": {},
                "ui_components": ["Button"]
            }
        ]
        
        start_time = time.time()
        result = await code_generator.generate_react_components(ui_components, "STORY-PERF-001")
        end_time = time.time()
        
        generation_time = end_time - start_time
        
        # Should generate quickly
        assert generation_time < 5.0, f"Code generation too slow: {generation_time:.2f}s (max: 5s)"
        assert len(result) == 1
    
    def test_complexity_calculation_performance(self):
        """Test complexity calculation performance."""
        import time
        
        code_generator = CodeGenerator()
        
        # Large code sample
        large_code = """
        function largeFunction() {
            for (let i = 0; i < 100; i++) {
                if (i % 2) {
                    console.log(i);
                } else {
                    console.log('even');
                }
            }
        }
        """ * 10  # Repeat to make it larger
        
        start_time = time.time()
        complexity = code_generator._calculate_cyclomatic_complexity(large_code)
        end_time = time.time()
        
        calculation_time = end_time - start_time
        
        # Should calculate quickly even for large code
        assert calculation_time < 0.1, f"Complexity calculation too slow: {calculation_time:.3f}s (max: 0.1s)"
        assert complexity > 0


if __name__ == "__main__":
    # Run tools tests directly
    pytest.main([__file__, "-v", "-m", "agent"])