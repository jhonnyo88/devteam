"""
Contract Validation Scripts Tests

Tests for contract validation utilities that ensure the contract system
functions correctly across the DigiNativa AI Team pipeline.

SCRIPTS TESTED:
- validate_contracts.py - Comprehensive contract validation
- simple_contract_test.py - Lightweight contract testing
- Contract validation utilities and functions

These tests ensure that contract validation scripts work reliably
and catch contract issues before they break the AI team integration.
"""

import pytest
import subprocess
import tempfile
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any
from unittest.mock import Mock, patch

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.validate_contracts import ContractValidator
from scripts.simple_contract_test import (
    create_valid_pm_output,
    create_valid_te_output,
    validate_contract_structure,
    test_agent_sequence,
    test_dna_compliance_consistency,
    test_performance_requirements,
    test_security_requirements,
    test_coverage_requirements
)


class TestValidateContractsScript:
    """Test the main contract validation script."""
    
    @pytest.fixture
    def script_path(self):
        """Path to validate_contracts.py script."""
        return project_root / "scripts" / "validate_contracts.py"
    
    @pytest.fixture
    def mock_test_modules(self):
        """Mock test modules to avoid import issues."""
        with patch('scripts.validate_contracts.TestAgentContractFlow') as mock_flow, \
             patch('scripts.validate_contracts.TestContractCompatibility') as mock_compat, \
             patch('scripts.validate_contracts.TestContractPipeline') as mock_pipeline, \
             patch('scripts.validate_contracts.TestContractRegression') as mock_regression:
            
            # Setup mock methods
            mock_flow.return_value.test_complete_contract_chain_compatibility = Mock()
            mock_flow.return_value.test_dna_compliance_preservation = Mock()
            mock_flow.return_value.test_quality_gates_progression = Mock()
            mock_flow.return_value.test_contract_version_compatibility = Mock()
            mock_flow.return_value.test_story_id_propagation = Mock()
            mock_flow.return_value.test_performance_requirements_chain = Mock()
            mock_flow.return_value.test_security_requirements_chain = Mock()
            mock_flow.return_value.test_coverage_requirements_chain = Mock()
            
            yield {
                'flow': mock_flow,
                'compatibility': mock_compat,
                'pipeline': mock_pipeline,
                'regression': mock_regression
            }
    
    def test_script_help_option(self, script_path):
        """Test that script provides help information."""
        result = subprocess.run(
            [sys.executable, str(script_path), "--help"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0
        assert "validate" in result.stdout.lower()
        assert "--verbose" in result.stdout
        assert "--fast" in result.stdout
        assert "--agent" in result.stdout
    
    def test_script_execution_structure(self, script_path):
        """Test script basic execution structure."""
        # Test that script can be imported without errors
        spec = os.path.splitext(os.path.basename(script_path))[0]
        
        # Test script file exists and is executable
        assert script_path.exists()
        assert os.access(script_path, os.R_OK)
        
        # Test script has proper shebang
        with open(script_path, 'r') as f:
            first_line = f.readline().strip()
            assert first_line.startswith('#!/usr/bin/env python3')
    
    def test_contract_validator_initialization(self, mock_test_modules):
        """Test ContractValidator class initialization."""
        validator = ContractValidator(verbose=True, fast=False)
        
        assert validator.verbose is True
        assert validator.fast is False
        assert validator.results["passed"] == 0
        assert validator.results["failed"] == 0
        assert validator.results["skipped"] == 0
        assert isinstance(validator.results["errors"], list)
    
    def test_contract_validator_logging(self, mock_test_modules):
        """Test ContractValidator logging functionality."""
        validator = ContractValidator(verbose=True)
        
        # Test verbose logging
        with patch('builtins.print') as mock_print:
            validator.log("Test message", "INFO")
            mock_print.assert_called()
        
        # Test error logging (always shows)
        validator_quiet = ContractValidator(verbose=False)
        with patch('builtins.print') as mock_print:
            validator_quiet.log("Error message", "ERROR")
            mock_print.assert_called()
    
    def test_run_test_success(self, mock_test_modules):
        """Test successful test execution tracking."""
        validator = ContractValidator()
        
        def dummy_test():
            pass
        
        result = validator.run_test("test_name", dummy_test, "Test description")
        
        assert result is True
        assert validator.results["passed"] == 1
        assert validator.results["failed"] == 0
    
    def test_run_test_failure(self, mock_test_modules):
        """Test failed test execution tracking."""
        validator = ContractValidator()
        
        def failing_test():
            raise ValueError("Test failure")
        
        result = validator.run_test("failing_test", failing_test, "Failing test")
        
        assert result is False
        assert validator.results["passed"] == 0
        assert validator.results["failed"] == 1
        assert len(validator.results["errors"]) == 1
        assert "failing_test failed" in validator.results["errors"][0]
    
    def test_validate_core_contracts(self, mock_test_modules):
        """Test core contract validation."""
        validator = ContractValidator()
        
        # Mock all test methods to succeed
        for mock_obj in mock_test_modules.values():
            for method_name in dir(mock_obj.return_value):
                if method_name.startswith('test_'):
                    setattr(mock_obj.return_value, method_name, Mock())
        
        result = validator.validate_core_contracts()
        
        # Should have run all core tests
        assert validator.results["passed"] >= 5  # At least 5 core tests
    
    def test_validate_specific_agent(self, mock_test_modules):
        """Test agent-specific validation."""
        validator = ContractValidator()
        
        # Test valid agent
        result = validator.validate_specific_agent("project_manager")
        assert isinstance(result, bool)
        
        # Test invalid agent
        result = validator.validate_specific_agent("invalid_agent")
        assert result is False
    
    def test_exit_code_calculation(self, mock_test_modules):
        """Test exit code calculation based on results."""
        validator = ContractValidator()
        
        # No failures
        assert validator.get_exit_code() == 0
        
        # General failure
        validator.results["failed"] = 1
        validator.results["errors"] = ["General error"]
        assert validator.get_exit_code() == 1
        
        # Performance failure
        validator.results["errors"] = ["Performance test failed"]
        assert validator.get_exit_code() == 2
        
        # Security failure
        validator.results["errors"] = ["Security validation failed"]
        assert validator.get_exit_code() == 3
        
        # Quality gate failure
        validator.results["errors"] = ["Quality gate failed"]
        assert validator.get_exit_code() == 4


class TestSimpleContractTestScript:
    """Test the simple contract testing script."""
    
    @pytest.fixture
    def script_path(self):
        """Path to simple_contract_test.py script."""
        return project_root / "scripts" / "simple_contract_test.py"
    
    def test_script_execution(self, script_path):
        """Test simple contract test script execution."""
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True
        )
        
        # Script should run and provide output
        assert "DigiNativa Simple Contract Validation" in result.stdout
        assert "CONTRACT VALIDATION SUMMARY" in result.stdout
        
        # Should show pass/fail counts
        assert "Passed:" in result.stdout
        assert "Failed:" in result.stdout
    
    def test_create_valid_pm_output(self):
        """Test Project Manager contract creation."""
        story_id = "STORY-TEST-001"
        contract = create_valid_pm_output(story_id)
        
        assert contract["story_id"] == story_id
        assert contract["source_agent"] == "project_manager"
        assert contract["target_agent"] == "game_designer"
        assert contract["contract_type"] == "analysis_to_design"
        assert contract["contract_version"] == "1.0"
        
        # Validate DNA compliance structure
        dna = contract["dna_compliance"]
        assert "design_principles_validation" in dna
        assert "architecture_compliance" in dna
        
        # Validate required fields
        assert "input_requirements" in contract
        assert "output_specifications" in contract
        assert "quality_gates" in contract
        assert "handoff_criteria" in contract
    
    def test_create_valid_te_output(self):
        """Test Test Engineer contract creation."""
        story_id = "STORY-TEST-002"
        contract = create_valid_te_output(story_id)
        
        assert contract["story_id"] == story_id
        assert contract["source_agent"] == "test_engineer"
        assert contract["target_agent"] == "qa_tester"
        assert contract["contract_type"] == "testing_to_qa"
        
        # Validate performance data
        required_data = contract["input_requirements"]["required_data"]
        assert "performance_test_results" in required_data
        assert "security_scan_results" in required_data
        assert "coverage_report" in required_data
        
        perf_data = required_data["performance_test_results"]
        assert perf_data["average_api_response_time_ms"] <= 200
        assert perf_data["lighthouse_score"] >= 90
    
    def test_validate_contract_structure(self):
        """Test contract structure validation."""
        story_id = "STORY-STRUCT-001"
        
        # Valid contract should pass
        valid_contract = create_valid_pm_output(story_id)
        validate_contract_structure(valid_contract, "test_contract")  # Should not raise
        
        # Invalid contract should fail
        invalid_contract = valid_contract.copy()
        del invalid_contract["contract_version"]
        
        with pytest.raises(ValueError, match="Missing required field"):
            validate_contract_structure(invalid_contract, "invalid_contract")
    
    def test_agent_sequence_validation(self):
        """Test agent sequence validation."""
        # Should pass with valid sequence
        test_agent_sequence()  # Should not raise
    
    def test_dna_compliance_consistency(self):
        """Test DNA compliance consistency across contracts."""
        # Should pass with consistent DNA
        test_dna_compliance_consistency()  # Should not raise
    
    def test_performance_requirements_validation(self):
        """Test performance requirements validation."""
        # Should pass with valid performance data
        test_performance_requirements()  # Should not raise
    
    def test_security_requirements_validation(self):
        """Test security requirements validation."""
        # Should pass with valid security data
        test_security_requirements()  # Should not raise
    
    def test_coverage_requirements_validation(self):
        """Test coverage requirements validation."""
        # Should pass with valid coverage data
        test_coverage_requirements()  # Should not raise
    
    def test_contract_validation_error_cases(self):
        """Test various contract validation error scenarios."""
        story_id = "STORY-ERROR-001"
        
        # Test invalid story_id format
        invalid_story_contract = create_valid_pm_output(story_id)
        invalid_story_contract["story_id"] = "INVALID-FORMAT"
        
        with pytest.raises(ValueError, match="Invalid story_id format"):
            validate_contract_structure(invalid_story_contract, "invalid_story")
        
        # Test missing DNA structure
        missing_dna_contract = create_valid_pm_output(story_id)
        del missing_dna_contract["dna_compliance"]["design_principles_validation"]
        
        with pytest.raises(ValueError, match="Missing design_principles_validation"):
            validate_contract_structure(missing_dna_contract, "missing_dna")
        
        # Test invalid quality gates
        invalid_gates_contract = create_valid_pm_output(story_id)
        invalid_gates_contract["quality_gates"] = []
        
        with pytest.raises(ValueError, match="Quality gates must be non-empty list"):
            validate_contract_structure(invalid_gates_contract, "invalid_gates")


class TestContractValidationIntegration:
    """Test integration between validation scripts and system."""
    
    def test_script_imports(self):
        """Test that scripts can import required modules."""
        # Test validate_contracts.py imports
        try:
            import scripts.validate_contracts
            assert hasattr(scripts.validate_contracts, 'ContractValidator')
            assert hasattr(scripts.validate_contracts, 'main')
        except ImportError as e:
            pytest.skip(f"Cannot test validate_contracts imports: {e}")
        
        # Test simple_contract_test.py imports
        try:
            import scripts.simple_contract_test
            assert hasattr(scripts.simple_contract_test, 'create_valid_pm_output')
            assert hasattr(scripts.simple_contract_test, 'main')
        except ImportError as e:
            pytest.skip(f"Cannot test simple_contract_test imports: {e}")
    
    def test_contract_creation_consistency(self):
        """Test that contract creation is consistent across scripts."""
        story_id = "STORY-CONSISTENCY-001"
        
        # Create contracts from both scripts
        pm_contract = create_valid_pm_output(story_id)
        te_contract = create_valid_te_output(story_id)
        
        # Both should have same story_id
        assert pm_contract["story_id"] == story_id
        assert te_contract["story_id"] == story_id
        
        # Both should have same contract version
        assert pm_contract["contract_version"] == te_contract["contract_version"]
        
        # Both should have DNA compliance with same structure
        assert "dna_compliance" in pm_contract
        assert "dna_compliance" in te_contract
        assert set(pm_contract["dna_compliance"].keys()) == set(te_contract["dna_compliance"].keys())
    
    def test_validation_script_error_handling(self):
        """Test that validation scripts handle errors gracefully."""
        
        # Test with invalid inputs
        try:
            validate_contract_structure(None, "null_contract")
            assert False, "Should have raised error for None contract"
        except (ValueError, TypeError, AttributeError):
            pass  # Expected
        
        try:
            validate_contract_structure({}, "empty_contract")
            assert False, "Should have raised error for empty contract"
        except ValueError:
            pass  # Expected
    
    def test_performance_validation_thresholds(self):
        """Test that performance validation uses correct thresholds."""
        story_id = "STORY-PERF-001"
        
        # Create contract with performance data at thresholds
        te_contract = create_valid_te_output(story_id)
        perf_data = te_contract["input_requirements"]["required_data"]["performance_test_results"]
        
        # Test API response time threshold
        assert perf_data["average_api_response_time_ms"] <= 200
        
        # Test Lighthouse score threshold
        assert perf_data["lighthouse_score"] >= 90
        
        # Test performance budget
        assert perf_data["performance_budget_met"] is True
    
    def test_security_validation_requirements(self):
        """Test that security validation enforces requirements."""
        story_id = "STORY-SEC-001"
        
        te_contract = create_valid_te_output(story_id)
        security_data = te_contract["input_requirements"]["required_data"]["security_scan_results"]
        
        # Test no critical vulnerabilities
        assert len(security_data["critical_vulnerabilities"]) == 0
        
        # Test no high vulnerabilities
        assert len(security_data["high_vulnerabilities"]) == 0
        
        # Test security compliance
        assert security_data["security_compliance_met"] is True
    
    def test_coverage_validation_standards(self):
        """Test that coverage validation meets standards."""
        story_id = "STORY-COV-001"
        
        te_contract = create_valid_te_output(story_id)
        required_data = te_contract["input_requirements"]["required_data"]
        
        # Test integration test coverage (95% minimum)
        integration_coverage = required_data["integration_test_suite"]["coverage_percent"]
        assert integration_coverage >= 95
        
        # Test E2E test coverage (90% minimum)
        e2e_coverage = required_data["e2e_test_suite"]["coverage_percent"]
        assert e2e_coverage >= 90
        
        # Test overall coverage (90% minimum)
        overall_coverage = required_data["coverage_report"]["overall_coverage_percent"]
        assert overall_coverage >= 90


class TestScriptCommandLineInterface:
    """Test command line interface of validation scripts."""
    
    @pytest.fixture
    def validate_script_path(self):
        return project_root / "scripts" / "validate_contracts.py"
    
    @pytest.fixture
    def simple_script_path(self):
        return project_root / "scripts" / "simple_contract_test.py"
    
    def test_validate_contracts_cli_options(self, validate_script_path):
        """Test validate_contracts.py command line options."""
        # Test help option
        result = subprocess.run(
            [sys.executable, str(validate_script_path), "--help"],
            capture_output=True, text=True
        )
        assert result.returncode == 0
        assert "--verbose" in result.stdout
        assert "--fast" in result.stdout
        assert "--agent" in result.stdout
    
    def test_simple_contract_cli_execution(self, simple_script_path):
        """Test simple_contract_test.py command line execution."""
        result = subprocess.run(
            [sys.executable, str(simple_script_path)],
            capture_output=True, text=True
        )
        
        # Should provide validation output
        assert "DigiNativa Simple Contract Validation" in result.stdout
        assert "CONTRACT VALIDATION SUMMARY" in result.stdout
    
    def test_script_exit_codes(self, simple_script_path):
        """Test that scripts return appropriate exit codes."""
        result = subprocess.run(
            [sys.executable, str(simple_script_path)],
            capture_output=True, text=True
        )
        
        # Simple contract test should succeed
        assert result.returncode in [0, 1]  # 0 for success, 1 for failure
        
        # Exit code should match output
        if "ALL CONTRACT VALIDATIONS PASSED" in result.stdout:
            assert result.returncode == 0
        else:
            assert result.returncode == 1
    
    def test_script_output_format(self, simple_script_path):
        """Test that scripts produce properly formatted output."""
        result = subprocess.run(
            [sys.executable, str(simple_script_path)],
            capture_output=True, text=True
        )
        
        # Should have structured output
        lines = result.stdout.strip().split('\n')
        
        # Should have title
        assert any("DigiNativa" in line for line in lines)
        
        # Should have summary section
        assert any("SUMMARY" in line for line in lines)
        
        # Should have pass/fail indicators
        output = result.stdout
        assert "✅" in output or "❌" in output
        assert "Passed:" in output
        assert "Failed:" in output


# Contract validation benchmarks
CONTRACT_VALIDATION_BENCHMARKS = {
    "max_script_execution_time": 60,  # 1 minute max
    "min_coverage_percentage": 90,    # 90% minimum coverage
    "max_api_response_time": 200,     # 200ms max API response
    "min_lighthouse_score": 90,       # 90 minimum Lighthouse score
    "max_critical_vulnerabilities": 0, # No critical vulnerabilities
    "max_high_vulnerabilities": 0     # No high vulnerabilities
}


if __name__ == "__main__":
    # Run with: pytest scripts/tests/test_contract_validation_scripts.py -v
    pytest.main([__file__, "-v", "--tb=short"])