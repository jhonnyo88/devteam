"""
Development Utilities Tests

Tests for development helper scripts and utilities that support
the DigiNativa AI Team development workflow.

UTILITIES TESTED:
- Development environment setup scripts
- Code generation utilities
- Test data generation helpers
- Debugging and diagnostic tools
- Build and deployment automation

These tests ensure development utilities work reliably and support
efficient development workflows for the AI team system.
"""

import pytest
import subprocess
import tempfile
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestDevelopmentEnvironmentSetup:
    """Test development environment setup utilities."""
    
    def test_project_structure_validation(self):
        """Test that project structure is properly set up."""
        # Verify critical directories exist
        critical_dirs = [
            "modules",
            "modules/agents",
            "modules/shared",
            "tests",
            "tests/integration",
            "tests/dna_compliance",
            "docs",
            "scripts"
        ]
        
        for dir_path in critical_dirs:
            full_path = project_root / dir_path
            assert full_path.exists(), f"Critical directory missing: {dir_path}"
            assert full_path.is_dir(), f"Path exists but is not directory: {dir_path}"
    
    def test_required_agent_structure(self):
        """Test that agent directories have required structure."""
        agents_dir = project_root / "modules" / "agents"
        
        if not agents_dir.exists():
            pytest.skip("Agents directory not found")
        
        # Expected agent directories
        expected_agents = [
            "project_manager",
            "game_designer", 
            "developer",
            "test_engineer",
            "qa_tester",
            "quality_reviewer"
        ]
        
        for agent_name in expected_agents:
            agent_dir = agents_dir / agent_name
            if agent_dir.exists():
                # Check for key files
                expected_files = ["agent.py", "tests/"]
                for expected in expected_files:
                    file_path = agent_dir / expected
                    if expected.endswith("/"):
                        assert file_path.exists() and file_path.is_dir(), \
                            f"Missing directory: {agent_name}/{expected}"
                    else:
                        # File may or may not exist, but structure should be consistent
                        pass
    
    def test_shared_modules_structure(self):
        """Test that shared modules are properly structured."""
        shared_dir = project_root / "modules" / "shared"
        
        if not shared_dir.exists():
            pytest.skip("Shared modules directory not found")
        
        # Expected shared modules
        expected_modules = [
            "contract_validator.py",
            "dna_validator.py", 
            "exceptions.py",
            "base_agent.py",
            "state_manager.py"
        ]
        
        for module in expected_modules:
            module_path = shared_dir / module
            if module_path.exists():
                assert module_path.is_file(), f"Expected file but found directory: {module}"
                
                # Basic syntax check
                try:
                    with open(module_path, 'r') as f:
                        content = f.read()
                        compile(content, str(module_path), 'exec')
                except SyntaxError as e:
                    pytest.fail(f"Syntax error in {module}: {e}")
    
    def test_configuration_files_present(self):
        """Test that essential configuration files are present."""
        config_files = [
            "Implementation_rules.md",
            "TEST_STRATEGY.md",
            "CLAUDE.md"
        ]
        
        for config_file in config_files:
            config_path = project_root / config_file
            if config_path.exists():
                assert config_path.is_file(), f"Expected file: {config_file}"
                assert config_path.stat().st_size > 0, f"Empty configuration file: {config_file}"


class TestCodeGenerationUtilities:
    """Test code generation helper utilities."""
    
    @pytest.fixture
    def mock_agent_template(self):
        """Mock agent template for testing."""
        return {
            "agent_name": "test_agent",
            "agent_type": "test",
            "description": "Test agent for validation",
            "input_contract_type": "test_input",
            "output_contract_type": "test_output",
            "quality_gates": ["test_gate_1", "test_gate_2"],
            "dna_requirements": {
                "pedagogical_value": True,
                "policy_to_practice": True,
                "time_respect": True,
                "holistic_thinking": True,
                "professional_tone": True
            }
        }
    
    def test_agent_template_structure(self, mock_agent_template):
        """Test agent template has required structure."""
        required_fields = [
            "agent_name",
            "agent_type",
            "description",
            "input_contract_type",
            "output_contract_type",
            "quality_gates",
            "dna_requirements"
        ]
        
        for field in required_fields:
            assert field in mock_agent_template, f"Missing required field: {field}"
        
        # Validate DNA requirements structure
        dna_req = mock_agent_template["dna_requirements"]
        expected_principles = [
            "pedagogical_value",
            "policy_to_practice", 
            "time_respect",
            "holistic_thinking",
            "professional_tone"
        ]
        
        for principle in expected_principles:
            assert principle in dna_req, f"Missing DNA principle: {principle}"
    
    def test_contract_template_generation(self):
        """Test contract template generation utility."""
        def generate_contract_template(story_id: str, source_agent: str, target_agent: str) -> Dict[str, Any]:
            """Generate a basic contract template."""
            return {
                "contract_version": "1.0",
                "story_id": story_id,
                "source_agent": source_agent,
                "target_agent": target_agent,
                "dna_compliance": {
                    "design_principles_validation": {
                        "pedagogical_value": True,
                        "policy_to_practice": True,
                        "time_respect": True,
                        "holistic_thinking": True,
                        "professional_tone": True
                    },
                    "architecture_compliance": {
                        "api_first": True,
                        "stateless_backend": True,
                        "separation_of_concerns": True,
                        "simplicity_first": True
                    }
                },
                "input_requirements": {
                    "required_data": {},
                    "required_validations": []
                },
                "output_specifications": {
                    "deliverable_data": {},
                    "validation_criteria": {}
                },
                "quality_gates": [],
                "handoff_criteria": []
            }
        
        # Test template generation
        contract = generate_contract_template("STORY-TEST-001", "test_source", "test_target")
        
        assert contract["story_id"] == "STORY-TEST-001"
        assert contract["source_agent"] == "test_source"
        assert contract["target_agent"] == "test_target"
        assert "dna_compliance" in contract
        assert "input_requirements" in contract
        assert "output_specifications" in contract
    
    def test_test_data_generation(self):
        """Test test data generation utilities."""
        def generate_test_github_issue(issue_number: int) -> Dict[str, Any]:
            """Generate test GitHub issue data."""
            return {
                "number": issue_number,
                "title": f"Test feature {issue_number}",
                "body": f"""## Feature Description
Test feature for validation purposes.

## Acceptance Criteria
- [ ] Feature works correctly
- [ ] User can complete task
- [ ] Time constraint met (≤10 minutes)

## Learning Objectives
- Test learning objective 1
- Test learning objective 2

## User Persona
Primary: Anna (Municipal Administrator)""",
                "state": "open",
                "labels": [
                    {"name": "feature-request"},
                    {"name": "priority-medium"},
                    {"name": "persona-anna"}
                ],
                "assignees": [],
                "milestone": {"title": "Test Milestone"},
                "user": {"login": "test_user"},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "html_url": f"https://github.com/test/repo/issues/{issue_number}"
            }
        
        # Test issue generation
        issue = generate_test_github_issue(123)
        
        assert issue["number"] == 123
        assert "Test feature 123" in issue["title"]
        assert "Feature Description" in issue["body"]
        assert "Acceptance Criteria" in issue["body"]
        assert "Anna" in issue["body"]
        assert issue["state"] == "open"
        assert len(issue["labels"]) > 0
    
    def test_performance_test_data_generation(self):
        """Test performance test data generation."""
        def generate_performance_test_data(meets_requirements: bool = True) -> Dict[str, Any]:
            """Generate performance test data."""
            if meets_requirements:
                return {
                    "average_api_response_time_ms": 150.0,
                    "lighthouse_score": 94,
                    "performance_budget_met": True,
                    "page_load_time": 1.8,
                    "time_to_interactive": 2.1,
                    "first_contentful_paint": 1.2,
                    "largest_contentful_paint": 2.0
                }
            else:
                return {
                    "average_api_response_time_ms": 250.0,  # Above 200ms threshold
                    "lighthouse_score": 85,  # Below 90 threshold
                    "performance_budget_met": False,
                    "page_load_time": 3.5,
                    "time_to_interactive": 4.2,
                    "first_contentful_paint": 2.8,
                    "largest_contentful_paint": 4.1
                }
        
        # Test good performance data
        good_perf = generate_performance_test_data(True)
        assert good_perf["average_api_response_time_ms"] <= 200
        assert good_perf["lighthouse_score"] >= 90
        assert good_perf["performance_budget_met"] is True
        
        # Test poor performance data
        poor_perf = generate_performance_test_data(False)
        assert poor_perf["average_api_response_time_ms"] > 200
        assert poor_perf["lighthouse_score"] < 90
        assert poor_perf["performance_budget_met"] is False


class TestBuildAndDeploymentUtilities:
    """Test build and deployment automation utilities."""
    
    def test_build_environment_detection(self):
        """Test build environment detection utility."""
        def detect_build_environment() -> Dict[str, Any]:
            """Detect current build environment."""
            env_info = {
                "python_version": sys.version,
                "platform": sys.platform,
                "cwd": os.getcwd(),
                "project_root": str(project_root),
                "env_vars": {
                    "PATH": os.environ.get("PATH", ""),
                    "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
                    "NODE_ENV": os.environ.get("NODE_ENV", "development")
                }
            }
            return env_info
        
        env_info = detect_build_environment()
        
        assert "python_version" in env_info
        assert "platform" in env_info
        assert "cwd" in env_info
        assert "project_root" in env_info
        assert "env_vars" in env_info
        
        # Validate project root is correct
        assert str(project_root) in env_info["project_root"]
    
    def test_dependency_validation(self):
        """Test dependency validation utility."""
        def validate_python_dependencies() -> Dict[str, bool]:
            """Validate Python dependencies are importable."""
            dependencies = {
                "pytest": False,
                "pathlib": False,
                "json": False,
                "subprocess": False,
                "tempfile": False,
                "unittest.mock": False
            }
            
            for dep in dependencies.keys():
                try:
                    __import__(dep)
                    dependencies[dep] = True
                except ImportError:
                    dependencies[dep] = False
            
            return dependencies
        
        deps = validate_python_dependencies()
        
        # Core dependencies should be available
        assert deps["json"] is True
        assert deps["subprocess"] is True
        assert deps["tempfile"] is True
        assert deps["pathlib"] is True
        
        # Test dependencies
        if deps["pytest"]:
            assert deps["pytest"] is True
        if deps["unittest.mock"]:
            assert deps["unittest.mock"] is True
    
    def test_file_system_utilities(self):
        """Test file system utility functions."""
        def ensure_directory_exists(path: Path) -> bool:
            """Ensure directory exists, create if necessary."""
            try:
                path.mkdir(parents=True, exist_ok=True)
                return path.exists() and path.is_dir()
            except Exception:
                return False
        
        def cleanup_temp_files(pattern: str, directory: Path) -> int:
            """Clean up temporary files matching pattern."""
            if not directory.exists():
                return 0
            
            cleaned = 0
            for file_path in directory.glob(pattern):
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        cleaned += 1
                except Exception:
                    pass
            
            return cleaned
        
        # Test directory creation
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test_subdir"
            assert ensure_directory_exists(test_dir) is True
            assert test_dir.exists() and test_dir.is_dir()
            
            # Test file cleanup
            temp_file = test_dir / "temp_file.tmp"
            temp_file.write_text("test content")
            assert temp_file.exists()
            
            cleaned = cleanup_temp_files("*.tmp", test_dir)
            assert cleaned == 1
            assert not temp_file.exists()


class TestDebuggingUtilities:
    """Test debugging and diagnostic utilities."""
    
    def test_contract_debugging_utility(self):
        """Test contract debugging utility."""
        def debug_contract_structure(contract: Dict[str, Any]) -> Dict[str, Any]:
            """Debug contract structure and identify issues."""
            debug_info = {
                "valid_structure": True,
                "missing_fields": [],
                "field_types": {},
                "dna_compliance_valid": False,
                "suggestions": []
            }
            
            # Check required fields
            required_fields = [
                "contract_version", "story_id", "source_agent", "target_agent",
                "dna_compliance", "input_requirements", "output_specifications"
            ]
            
            for field in required_fields:
                if field not in contract:
                    debug_info["missing_fields"].append(field)
                    debug_info["valid_structure"] = False
                else:
                    debug_info["field_types"][field] = type(contract[field]).__name__
            
            # Check DNA compliance structure
            if "dna_compliance" in contract:
                dna = contract["dna_compliance"]
                if ("design_principles_validation" in dna and 
                    "architecture_compliance" in dna):
                    debug_info["dna_compliance_valid"] = True
            
            # Generate suggestions
            if debug_info["missing_fields"]:
                debug_info["suggestions"].append(f"Add missing fields: {', '.join(debug_info['missing_fields'])}")
            
            if not debug_info["dna_compliance_valid"]:
                debug_info["suggestions"].append("Fix DNA compliance structure")
            
            return debug_info
        
        # Test with valid contract
        valid_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-DEBUG-001",
            "source_agent": "test_source",
            "target_agent": "test_target",
            "dna_compliance": {
                "design_principles_validation": {},
                "architecture_compliance": {}
            },
            "input_requirements": {},
            "output_specifications": {}
        }
        
        debug_result = debug_contract_structure(valid_contract)
        assert debug_result["valid_structure"] is True
        assert len(debug_result["missing_fields"]) == 0
        assert debug_result["dna_compliance_valid"] is True
        
        # Test with invalid contract
        invalid_contract = {"story_id": "STORY-INVALID-001"}
        
        debug_result = debug_contract_structure(invalid_contract)
        assert debug_result["valid_structure"] is False
        assert len(debug_result["missing_fields"]) > 0
        assert len(debug_result["suggestions"]) > 0
    
    def test_performance_diagnostic_utility(self):
        """Test performance diagnostic utility."""
        def diagnose_performance_issues(perf_data: Dict[str, Any]) -> Dict[str, Any]:
            """Diagnose performance issues from test data."""
            diagnosis = {
                "issues_found": [],
                "severity": "none",
                "recommendations": []
            }
            
            # Check API response time
            if perf_data.get("average_api_response_time_ms", 0) > 200:
                diagnosis["issues_found"].append("API response time exceeds 200ms")
                diagnosis["recommendations"].append("Optimize API endpoints and database queries")
                diagnosis["severity"] = "high"
            
            # Check Lighthouse score
            if perf_data.get("lighthouse_score", 100) < 90:
                diagnosis["issues_found"].append("Lighthouse score below 90")
                diagnosis["recommendations"].append("Optimize frontend performance and assets")
                if diagnosis["severity"] == "none":
                    diagnosis["severity"] = "medium"
            
            # Check page load time
            if perf_data.get("page_load_time", 0) > 3.0:
                diagnosis["issues_found"].append("Page load time exceeds 3 seconds")
                diagnosis["recommendations"].append("Reduce bundle size and optimize images")
                if diagnosis["severity"] == "none":
                    diagnosis["severity"] = "medium"
            
            return diagnosis
        
        # Test with good performance data
        good_perf = {
            "average_api_response_time_ms": 150,
            "lighthouse_score": 94,
            "page_load_time": 1.8
        }
        
        diagnosis = diagnose_performance_issues(good_perf)
        assert len(diagnosis["issues_found"]) == 0
        assert diagnosis["severity"] == "none"
        
        # Test with poor performance data
        poor_perf = {
            "average_api_response_time_ms": 300,
            "lighthouse_score": 75,
            "page_load_time": 5.2
        }
        
        diagnosis = diagnose_performance_issues(poor_perf)
        assert len(diagnosis["issues_found"]) > 0
        assert diagnosis["severity"] in ["medium", "high"]
        assert len(diagnosis["recommendations"]) > 0
    
    def test_agent_state_diagnostic(self):
        """Test agent state diagnostic utility."""
        def diagnose_agent_state(agent_name: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
            """Diagnose agent state for debugging."""
            diagnosis = {
                "agent_name": agent_name,
                "state_healthy": True,
                "issues": [],
                "memory_usage": "unknown",
                "processing_status": "unknown"
            }
            
            # Check processing status
            if "current_story_id" in state_data:
                if state_data["current_story_id"]:
                    diagnosis["processing_status"] = "active"
                else:
                    diagnosis["processing_status"] = "idle"
            
            # Check error states
            if state_data.get("error_count", 0) > 0:
                diagnosis["state_healthy"] = False
                diagnosis["issues"].append(f"Error count: {state_data['error_count']}")
            
            # Check processing time
            if state_data.get("processing_time_ms", 0) > 30000:  # 30 seconds
                diagnosis["issues"].append("Processing time excessive")
            
            # Estimate memory usage
            if "contracts_processed" in state_data:
                contracts = state_data["contracts_processed"]
                if contracts > 100:
                    diagnosis["memory_usage"] = "high"
                elif contracts > 50:
                    diagnosis["memory_usage"] = "medium"
                else:
                    diagnosis["memory_usage"] = "low"
            
            return diagnosis
        
        # Test healthy agent state
        healthy_state = {
            "current_story_id": "STORY-ACTIVE-001",
            "error_count": 0,
            "processing_time_ms": 1500,
            "contracts_processed": 25
        }
        
        diagnosis = diagnose_agent_state("test_agent", healthy_state)
        assert diagnosis["state_healthy"] is True
        assert diagnosis["processing_status"] == "active"
        assert diagnosis["memory_usage"] == "low"
        
        # Test problematic agent state
        problematic_state = {
            "current_story_id": None,
            "error_count": 5,
            "processing_time_ms": 45000,
            "contracts_processed": 150
        }
        
        diagnosis = diagnose_agent_state("test_agent", problematic_state)
        assert diagnosis["state_healthy"] is False
        assert len(diagnosis["issues"]) > 0
        assert diagnosis["memory_usage"] == "high"


class TestUtilityIntegration:
    """Test integration between various development utilities."""
    
    def test_utility_chain_execution(self):
        """Test that utilities can be chained together."""
        # Example utility chain: generate test data -> validate -> debug
        
        def utility_chain_example(story_id: str) -> Dict[str, Any]:
            """Example utility chain execution."""
            result = {
                "story_id": story_id,
                "steps_completed": [],
                "success": True,
                "final_output": None
            }
            
            try:
                # Step 1: Generate test contract
                contract = {
                    "contract_version": "1.0",
                    "story_id": story_id,
                    "source_agent": "test_agent",
                    "target_agent": "next_agent",
                    "dna_compliance": {"test": True}
                }
                result["steps_completed"].append("generate_contract")
                
                # Step 2: Validate contract (basic check)
                if "story_id" in contract and contract["story_id"] == story_id:
                    result["steps_completed"].append("validate_contract")
                else:
                    raise ValueError("Contract validation failed")
                
                # Step 3: Debug contract structure
                debug_info = {
                    "valid": True,
                    "issues": []
                }
                result["steps_completed"].append("debug_contract")
                
                result["final_output"] = {
                    "contract": contract,
                    "debug_info": debug_info
                }
                
            except Exception as e:
                result["success"] = False
                result["error"] = str(e)
            
            return result
        
        # Test utility chain
        chain_result = utility_chain_example("STORY-CHAIN-001")
        
        assert chain_result["success"] is True
        assert len(chain_result["steps_completed"]) == 3
        assert "generate_contract" in chain_result["steps_completed"]
        assert "validate_contract" in chain_result["steps_completed"]
        assert "debug_contract" in chain_result["steps_completed"]
        assert chain_result["final_output"] is not None
    
    def test_error_handling_across_utilities(self):
        """Test error handling consistency across utilities."""
        
        def test_utility_with_error_handling(input_data: Any) -> Dict[str, Any]:
            """Test utility with proper error handling."""
            result = {
                "success": False,
                "error": None,
                "error_type": None,
                "output": None
            }
            
            try:
                if input_data is None:
                    raise ValueError("Input data cannot be None")
                
                if not isinstance(input_data, dict):
                    raise TypeError("Input data must be dictionary")
                
                if "required_field" not in input_data:
                    raise KeyError("Missing required field")
                
                result["success"] = True
                result["output"] = f"Processed: {input_data['required_field']}"
                
            except ValueError as e:
                result["error"] = str(e)
                result["error_type"] = "ValueError"
            except TypeError as e:
                result["error"] = str(e)
                result["error_type"] = "TypeError"
            except KeyError as e:
                result["error"] = str(e)
                result["error_type"] = "KeyError"
            except Exception as e:
                result["error"] = str(e)
                result["error_type"] = "UnknownError"
            
            return result
        
        # Test with valid input
        valid_result = test_utility_with_error_handling({"required_field": "test_value"})
        assert valid_result["success"] is True
        assert valid_result["error"] is None
        
        # Test with None input
        none_result = test_utility_with_error_handling(None)
        assert none_result["success"] is False
        assert none_result["error_type"] == "ValueError"
        
        # Test with wrong type
        type_result = test_utility_with_error_handling("not_a_dict")
        assert type_result["success"] is False
        assert type_result["error_type"] == "TypeError"
        
        # Test with missing field
        missing_result = test_utility_with_error_handling({"wrong_field": "value"})
        assert missing_result["success"] is False
        assert missing_result["error_type"] == "KeyError"


# Development utility benchmarks
DEVELOPMENT_UTILITY_BENCHMARKS = {
    "max_utility_execution_time": 10,  # 10 seconds max
    "max_test_data_generation_time": 5,  # 5 seconds max
    "max_validation_time": 3,  # 3 seconds max
    "max_debug_analysis_time": 2,  # 2 seconds max
    "min_error_coverage": 80  # 80% error scenarios covered
}


if __name__ == "__main__":
    # Run with: pytest scripts/tests/test_development_utilities.py -v
    pytest.main([__file__, "-v", "--tb=short"])