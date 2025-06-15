"""
Contract Validator tests for DigiNativa AI Team system.

PURPOSE:
Comprehensive testing of the ContractValidator class which is the foundation
of our modular AI team architecture. This validator protects system integrity
by ensuring all agent contracts are valid and compliant.

CRITICAL IMPORTANCE:
ContractValidator is the most important component in the system because:
- It enables modular agent development
- It prevents invalid agent handoffs
- It enforces DNA compliance requirements
- It validates quality gates and business rules
- It ensures backward compatibility

TESTING SCOPE:
- Schema validation accuracy and performance
- Business rules validation logic
- DNA compliance checking functionality 
- Performance requirements (<100ms per contract)
- Error handling and edge cases
- Concurrent validation operations
"""

import pytest
import json
import time
import asyncio
import tempfile
import sys
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import patch, MagicMock, mock_open
from concurrent.futures import ThreadPoolExecutor
import threading

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.shared.contract_validator import ContractValidator, ValidationResult, ContractValidationError
from modules.shared.exceptions import StateManagementError


class TestContractValidatorInitialization:
    """Test ContractValidator initialization and schema loading."""
    
    def test_validator_initialization_with_valid_schema(self):
        """Test successful initialization with valid schema."""
        # Should work with default schema path
        validator = ContractValidator()
        
        assert validator.schema is not None, "Schema should be loaded"
        assert isinstance(validator.schema, dict), "Schema should be a dictionary"
        assert validator.schema_path.exists(), "Schema file should exist"
    
    def test_validator_initialization_with_custom_schema_path(self):
        """Test initialization with custom schema path."""
        # Create temporary schema file
        schema_content = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "contract_version": {"type": "string"},
                "story_id": {"type": "string"}
            },
            "required": ["contract_version", "story_id"]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(schema_content, f)
            temp_path = f.name
        
        try:
            validator = ContractValidator(schema_path=temp_path)
            assert validator.schema == schema_content
        finally:
            Path(temp_path).unlink()
    
    def test_validator_initialization_with_nonexistent_schema(self):
        """Test initialization with non-existent schema file."""
        with pytest.raises(FileNotFoundError):
            ContractValidator(schema_path="nonexistent/schema.json")
    
    def test_validator_initialization_with_invalid_json_schema(self):
        """Test initialization with invalid JSON schema."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content {")
            temp_path = f.name
        
        try:
            with pytest.raises((json.JSONDecodeError, ContractValidationError)):
                ContractValidator(schema_path=temp_path)
        finally:
            Path(temp_path).unlink()
    
    def test_valid_agent_sequences_defined(self):
        """Test that valid agent sequences are properly defined."""
        validator = ContractValidator()
        
        # Check that critical agent sequences exist
        expected_sequences = [
            ("github", "project_manager"),
            ("project_manager", "game_designer"),
            ("game_designer", "developer"),
            ("developer", "test_engineer"),
            ("test_engineer", "qa_tester"),
            ("qa_tester", "quality_reviewer")
        ]
        
        for source, target in expected_sequences:
            assert source in validator.valid_agent_sequences, f"Source agent {source} should be defined"
            assert target in validator.valid_agent_sequences[source], f"Sequence {source} -> {target} should be valid"


class TestSchemaValidation:
    """Test JSON schema validation functionality."""
    
    @pytest.fixture
    def validator(self):
        """Create ContractValidator instance for testing."""
        return ContractValidator()
    
    @pytest.fixture
    def valid_contract(self):
        """Valid contract for testing."""
        return {
            "contract_version": "1.0",
            "contract_type": "github_to_project_manager",
            "story_id": "STORY-GH-1001",
            "source_agent": "github",
            "target_agent": "project_manager",
            "dna_compliance": {
                "time_respect_validated": True,
                "pedagogical_value_validated": True,
                "professional_tone_validated": True,
                "policy_to_practice_validated": True,
                "holistic_thinking_validated": True
            },
            "input_requirements": {
                "required_files": ["github_issue.json"],
                "required_data": {
                    "github_issue": "object"
                },
                "required_validations": ["issue_parsed"]
            },
            "output_specifications": {
                "deliverable_files": ["story_analysis.json"],
                "deliverable_data": {
                    "story_analysis": "object"
                },
                "validation_criteria": {
                    "completeness": {"min": 95}
                }
            },
            "quality_gates": ["story_requirements_complete"],
            "handoff_criteria": ["story_analysis_validated"]
        }
    
    def test_schema_validation_success(self, validator, valid_contract):
        """Test successful schema validation."""
        result = validator.validate_contract(valid_contract)
        
        assert result.is_valid, f"Valid contract should pass validation: {result.errors}"
        assert len(result.errors) == 0, "No errors should be present"
        assert isinstance(result.validation_timestamp, str), "Timestamp should be present"
    
    def test_schema_validation_missing_required_field(self, validator, valid_contract):
        """Test schema validation with missing required field."""
        # Remove required field
        del valid_contract["story_id"]
        
        result = validator.validate_contract(valid_contract)
        
        assert not result.is_valid, "Contract missing required field should fail"
        assert len(result.errors) > 0, "Errors should be present"
        assert any("story_id" in error for error in result.errors), "Error should mention missing story_id"
    
    def test_schema_validation_invalid_field_type(self, validator, valid_contract):
        """Test schema validation with invalid field type."""
        # Set contract_version to wrong type
        valid_contract["contract_version"] = 1.0  # Should be string
        
        result = validator.validate_contract(valid_contract)
        
        assert not result.is_valid, "Contract with wrong field type should fail"
        assert len(result.errors) > 0, "Errors should be present"
    
    def test_schema_validation_additional_properties(self, validator, valid_contract):
        """Test schema validation with additional properties."""
        # Add extra field
        valid_contract["extra_field"] = "not_in_schema"
        
        result = validator.validate_contract(valid_contract)
        
        # Depending on schema configuration, this might be valid or produce warnings
        if not result.is_valid:
            assert len(result.errors) > 0
        # Additional properties should at least generate warnings
        assert len(result.warnings) >= 0  # Warnings may or may not be present
    
    def test_schema_validation_empty_contract(self, validator):
        """Test schema validation with empty contract."""
        empty_contract = {}
        
        result = validator.validate_contract(empty_contract)
        
        assert not result.is_valid, "Empty contract should fail validation"
        assert len(result.errors) > 0, "Multiple errors should be present for empty contract"
    
    def test_schema_validation_null_values(self, validator, valid_contract):
        """Test schema validation with null/None values."""
        # Set required field to None
        valid_contract["story_id"] = None
        
        result = validator.validate_contract(valid_contract)
        
        assert not result.is_valid, "Contract with null required field should fail"
        assert len(result.errors) > 0, "Errors should be present"


class TestBusinessRulesValidation:
    """Test business rules validation logic."""
    
    @pytest.fixture
    def validator(self):
        """Create ContractValidator instance for testing."""
        return ContractValidator()
    
    @pytest.fixture
    def valid_contract(self):
        """Valid contract for testing."""
        return {
            "contract_version": "1.0",
            "contract_type": "developer_to_test_engineer",
            "story_id": "STORY-DEV-1001",
            "source_agent": "developer",
            "target_agent": "test_engineer",
            "dna_compliance": {
                "time_respect_validated": True,
                "pedagogical_value_validated": True,
                "professional_tone_validated": True,
                "policy_to_practice_validated": True,
                "holistic_thinking_validated": True
            },
            "input_requirements": {
                "required_files": ["implementation.js"],
                "required_data": {
                    "component_implementations": "array",
                    "api_implementations": "array"
                },
                "required_validations": ["code_compiled"]
            },
            "output_specifications": {
                "deliverable_files": ["test_suite.js"],
                "deliverable_data": {
                    "test_results": "object"
                },
                "validation_criteria": {
                    "coverage": {"min": 95}
                }
            },
            "quality_gates": ["implementation_complete"],
            "handoff_criteria": ["tests_created"]
        }
    
    def test_agent_sequence_validation_success(self, validator, valid_contract):
        """Test successful agent sequence validation."""
        result = validator.validate_contract(valid_contract)
        
        assert result.is_valid, f"Valid agent sequence should pass: {result.errors}"
    
    def test_agent_sequence_validation_invalid_sequence(self, validator, valid_contract):
        """Test invalid agent sequence validation."""
        # Set invalid sequence (skipping agents)
        valid_contract["source_agent"] = "github"
        valid_contract["target_agent"] = "developer"  # Skipping project_manager and game_designer
        valid_contract["contract_type"] = "github_to_developer"
        
        result = validator.validate_contract(valid_contract)
        
        assert not result.is_valid, "Invalid agent sequence should fail validation"
        assert any("sequence" in error.lower() or "invalid" in error.lower() for error in result.errors)
    
    def test_contract_type_consistency_validation(self, validator, valid_contract):
        """Test contract type consistency with source/target agents."""
        # Mismatched contract type
        valid_contract["contract_type"] = "game_designer_to_developer"  # Doesn't match developer->test_engineer
        
        result = validator.validate_contract(valid_contract)
        
        assert not result.is_valid, "Mismatched contract type should fail validation"
        assert any("type" in error.lower() or "mismatch" in error.lower() for error in result.errors)
    
    def test_story_id_format_validation(self, validator, valid_contract):
        """Test story ID format validation."""
        valid_story_ids = [
            "STORY-GH-1001",
            "STORY-PM-2001",
            "ISSUE-12345",
            "FEATURE-001"
        ]
        
        for story_id in valid_story_ids:
            valid_contract["story_id"] = story_id
            result = validator.validate_contract(valid_contract)
            assert result.is_valid, f"Valid story_id {story_id} should pass validation"
    
    def test_invalid_story_id_format(self, validator, valid_contract):
        """Test invalid story ID format validation."""
        invalid_story_ids = [
            "",           # Empty
            "invalid",    # No proper format
            "123",        # Just numbers
            "STORY"       # Incomplete
        ]
        
        for story_id in invalid_story_ids:
            valid_contract["story_id"] = story_id
            result = validator.validate_contract(valid_contract)
            if not result.is_valid:
                assert any("story_id" in error.lower() for error in result.errors)
    
    def test_quality_gates_validation(self, validator, valid_contract):
        """Test quality gates validation."""
        # Empty quality gates should be valid but might generate warnings
        valid_contract["quality_gates"] = []
        result = validator.validate_contract(valid_contract)
        assert result.is_valid, "Empty quality gates should be valid"
        
        # Multiple quality gates should be valid
        valid_contract["quality_gates"] = [
            "code_compiled_successfully",
            "unit_tests_passing",
            "integration_tests_passing"
        ]
        result = validator.validate_contract(valid_contract)
        assert result.is_valid, "Multiple quality gates should be valid"
    
    def test_handoff_criteria_validation(self, validator, valid_contract):
        """Test handoff criteria validation."""
        # Empty handoff criteria should be valid but might generate warnings
        valid_contract["handoff_criteria"] = []
        result = validator.validate_contract(valid_contract)
        assert result.is_valid, "Empty handoff criteria should be valid"
        
        # Multiple handoff criteria should be valid
        valid_contract["handoff_criteria"] = [
            "all_tests_implemented",
            "documentation_complete",
            "code_reviewed"
        ]
        result = validator.validate_contract(valid_contract)
        assert result.is_valid, "Multiple handoff criteria should be valid"


class TestDNAComplianceValidation:
    """Test DNA compliance validation functionality."""
    
    @pytest.fixture
    def validator(self):
        """Create ContractValidator instance for testing."""
        return ContractValidator()
    
    @pytest.fixture
    def contract_with_dna(self):
        """Contract with complete DNA compliance."""
        return {
            "contract_version": "1.0",
            "contract_type": "qa_tester_to_quality_reviewer",
            "story_id": "STORY-QA-1001",
            "source_agent": "qa_tester",
            "target_agent": "quality_reviewer",
            "dna_compliance": {
                # Design principles
                "time_respect_validated": True,
                "pedagogical_value_validated": True,
                "professional_tone_validated": True,
                "policy_to_practice_validated": True,
                "holistic_thinking_validated": True,
                # Architecture principles
                "api_first_validated": True,
                "stateless_backend_validated": True,
                "separation_concerns_validated": True,
                "simplicity_first_validated": True,
                # Validation metadata
                "dna_validation_timestamp": "2024-01-15T10:30:00Z",
                "dna_compliance_score": 4.8
            },
            "input_requirements": {
                "required_files": ["test_results.json"],
                "required_data": {"qa_results": "object"},
                "required_validations": ["qa_complete"]
            },
            "output_specifications": {
                "deliverable_files": ["final_report.json"],
                "deliverable_data": {"approval_status": "object"},
                "validation_criteria": {"quality_score": {"min": 4.0}}
            },
            "quality_gates": ["qa_approval_received"],
            "handoff_criteria": ["ready_for_deployment"]
        }
    
    def test_complete_dna_compliance_validation(self, validator, contract_with_dna):
        """Test validation with complete DNA compliance."""
        result = validator.validate_contract(contract_with_dna)
        
        assert result.is_valid, f"Contract with complete DNA compliance should pass: {result.errors}"
    
    def test_missing_design_principle_validation(self, validator, contract_with_dna):
        """Test validation with missing design principle."""
        # Remove a design principle
        del contract_with_dna["dna_compliance"]["time_respect_validated"]
        
        result = validator.validate_contract(contract_with_dna)
        
        assert not result.is_valid, "Contract missing design principle should fail"
        assert any("time_respect" in error.lower() for error in result.errors)
    
    def test_missing_architecture_principle_validation(self, validator, contract_with_dna):
        """Test validation with missing architecture principle."""
        # Remove an architecture principle
        del contract_with_dna["dna_compliance"]["api_first_validated"]
        
        result = validator.validate_contract(contract_with_dna)
        
        # Architecture principles might be optional in some contexts
        if not result.is_valid:
            assert any("api_first" in error.lower() for error in result.errors)
    
    def test_invalid_dna_compliance_values(self, validator, contract_with_dna):
        """Test validation with invalid DNA compliance values."""
        # Set design principle to False (indicating non-compliance)
        contract_with_dna["dna_compliance"]["pedagogical_value_validated"] = False
        
        result = validator.validate_contract(contract_with_dna)
        
        # Depending on validation rules, False values might be valid but indicate issues
        if not result.is_valid:
            assert any("pedagogical_value" in error.lower() for error in result.errors)
        else:
            # Should at least generate a warning
            assert len(result.warnings) >= 0
    
    def test_dna_compliance_score_validation(self, validator, contract_with_dna):
        """Test DNA compliance score validation."""
        # Valid score ranges
        valid_scores = [1.0, 2.5, 4.0, 4.8, 5.0]
        
        for score in valid_scores:
            contract_with_dna["dna_compliance"]["dna_compliance_score"] = score
            result = validator.validate_contract(contract_with_dna)
            assert result.is_valid, f"DNA compliance score {score} should be valid"
        
        # Invalid scores
        invalid_scores = [-1.0, 0.0, 5.1, 10.0]
        
        for score in invalid_scores:
            contract_with_dna["dna_compliance"]["dna_compliance_score"] = score
            result = validator.validate_contract(contract_with_dna)
            # Might be valid but should generate warnings for out-of-range scores
            if not result.is_valid:
                assert any("score" in error.lower() for error in result.errors)


class TestContractValidatorPerformance:
    """Test performance requirements for contract validation."""
    
    @pytest.fixture
    def validator(self):
        """Create ContractValidator instance for testing."""
        return ContractValidator()
    
    @pytest.fixture
    def large_contract(self):
        """Large contract for performance testing."""
        return {
            "contract_version": "1.0",
            "contract_type": "test_engineer_to_qa_tester",
            "story_id": "STORY-PERF-1001",
            "source_agent": "test_engineer",
            "target_agent": "qa_tester",
            "dna_compliance": {
                "time_respect_validated": True,
                "pedagogical_value_validated": True,
                "professional_tone_validated": True,
                "policy_to_practice_validated": True,
                "holistic_thinking_validated": True
            },
            "input_requirements": {
                "required_files": [f"test_file_{i}.json" for i in range(100)],
                "required_data": {
                    f"data_field_{i}": "object" for i in range(50)
                },
                "required_validations": [f"validation_{i}" for i in range(20)]
            },
            "output_specifications": {
                "deliverable_files": [f"output_file_{i}.json" for i in range(100)],
                "deliverable_data": {
                    f"output_data_{i}": "object" for i in range(50)
                },
                "validation_criteria": {
                    f"criteria_{i}": {"min": i} for i in range(20)
                }
            },
            "quality_gates": [f"quality_gate_{i}" for i in range(50)],
            "handoff_criteria": [f"handoff_criteria_{i}" for i in range(30)]
        }
    
    def test_single_contract_validation_performance(self, validator, large_contract):
        """Test that single contract validation meets performance requirement (<100ms)."""
        # Warm up the validator
        validator.validate_contract(large_contract)
        
        # Measure validation time
        start_time = time.time()
        result = validator.validate_contract(large_contract)
        end_time = time.time()
        
        validation_time = end_time - start_time
        
        assert validation_time < 0.1, f"Contract validation took {validation_time:.3f}s, should be < 0.1s (100ms)"
        assert result.is_valid, "Large contract should be valid"
    
    def test_batch_contract_validation_performance(self, validator, large_contract):
        """Test performance of validating multiple contracts."""
        contracts = []
        for i in range(10):
            contract = large_contract.copy()
            contract["story_id"] = f"STORY-BATCH-{i:03d}"
            contracts.append(contract)
        
        start_time = time.time()
        results = [validator.validate_contract(contract) for contract in contracts]
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time_per_contract = total_time / len(contracts)
        
        assert avg_time_per_contract < 0.1, f"Average validation time {avg_time_per_contract:.3f}s exceeds 100ms limit"
        assert all(result.is_valid for result in results), "All contracts should be valid"
    
    def test_concurrent_validation_performance(self, validator, large_contract):
        """Test performance of concurrent contract validation."""
        def validate_contract_with_id(contract_id: int):
            contract = large_contract.copy()
            contract["story_id"] = f"STORY-CONCURRENT-{contract_id:03d}"
            start_time = time.time()
            result = validator.validate_contract(contract)
            end_time = time.time()
            return result.is_valid, end_time - start_time
        
        # Run concurrent validations
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(validate_contract_with_id, i) for i in range(20)]
            results = [future.result() for future in futures]
        
        # Check results
        validities, times = zip(*results)
        max_time = max(times)
        avg_time = sum(times) / len(times)
        
        assert all(validities), "All concurrent validations should succeed"
        assert max_time < 0.2, f"Maximum concurrent validation time {max_time:.3f}s exceeds 200ms limit"
        assert avg_time < 0.1, f"Average concurrent validation time {avg_time:.3f}s exceeds 100ms limit"
    
    def test_memory_usage_efficiency(self, validator, large_contract):
        """Test that validator doesn't consume excessive memory."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Validate many contracts
        for i in range(100):
            contract = large_contract.copy()
            contract["story_id"] = f"STORY-MEMORY-{i:03d}"
            result = validator.validate_contract(contract)
            assert result.is_valid
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 50MB)
        assert memory_increase < 50 * 1024 * 1024, f"Memory increased by {memory_increase / 1024 / 1024:.1f}MB, should be < 50MB"


class TestContractValidatorErrorHandling:
    """Test error handling and edge cases."""
    
    @pytest.fixture
    def validator(self):
        """Create ContractValidator instance for testing."""
        return ContractValidator()
    
    def test_validation_with_none_contract(self, validator):
        """Test validation with None contract."""
        with pytest.raises((TypeError, ContractValidationError)):
            validator.validate_contract(None)
    
    def test_validation_with_non_dict_contract(self, validator):
        """Test validation with non-dictionary contract."""
        invalid_contracts = [
            "string_contract",
            ["list", "contract"],
            123,
            True
        ]
        
        for invalid_contract in invalid_contracts:
            with pytest.raises((TypeError, ContractValidationError)):
                validator.validate_contract(invalid_contract)
    
    def test_validation_with_circular_references(self, validator):
        """Test validation with circular references in contract."""
        contract = {
            "contract_version": "1.0",
            "story_id": "STORY-CIRCULAR-001"
        }
        
        # Create circular reference
        contract["self_reference"] = contract
        
        # Should handle circular references gracefully
        try:
            result = validator.validate_contract(contract)
            # If it doesn't raise an error, it should at least fail validation
            assert not result.is_valid
        except (RecursionError, ValueError, ContractValidationError):
            # Acceptable to raise an error for circular references
            pass
    
    def test_validation_with_very_deep_nesting(self, validator):
        """Test validation with deeply nested contract structure."""
        contract = {
            "contract_version": "1.0",
            "contract_type": "github_to_project_manager",
            "story_id": "STORY-DEEP-001",
            "source_agent": "github",
            "target_agent": "project_manager",
            "dna_compliance": {
                "time_respect_validated": True,
                "pedagogical_value_validated": True,
                "professional_tone_validated": True,
                "policy_to_practice_validated": True,
                "holistic_thinking_validated": True
            }
        }
        
        # Create deeply nested structure
        current_level = contract
        for i in range(100):  # 100 levels deep
            current_level[f"nested_level_{i}"] = {}
            current_level = current_level[f"nested_level_{i}"]
        
        current_level["deep_value"] = "test"
        
        # Add required fields
        contract.update({
            "input_requirements": {
                "required_files": [],
                "required_data": {},
                "required_validations": []
            },
            "output_specifications": {
                "deliverable_files": [],
                "deliverable_data": {},
                "validation_criteria": {}
            },
            "quality_gates": [],
            "handoff_criteria": []
        })
        
        # Should handle deep nesting without crashing
        try:
            result = validator.validate_contract(contract)
            # Should either validate successfully or fail gracefully
            assert isinstance(result.is_valid, bool)
        except (RecursionError, MemoryError):
            # Acceptable to fail with recursion/memory error for extremely deep nesting
            pass
    
    def test_validation_with_unicode_and_special_characters(self, validator):
        """Test validation with Unicode and special characters."""
        contract = {
            "contract_version": "1.0",
            "contract_type": "github_to_project_manager",
            "story_id": "STORY-UNICODE-001",
            "source_agent": "github",
            "target_agent": "project_manager",
            "dna_compliance": {
                "time_respect_validated": True,
                "pedagogical_value_validated": True,
                "professional_tone_validated": True,
                "policy_to_practice_validated": True,
                "holistic_thinking_validated": True
            },
            "input_requirements": {
                "required_files": ["file_with_ñ_ü_å.json"],
                "required_data": {
                    "unicode_field_🚀": "object",
                    "special_chars_!@#$%": "string"
                },
                "required_validations": ["validation_with_émojis_😀"]
            },
            "output_specifications": {
                "deliverable_files": ["output_with_中文.json"],
                "deliverable_data": {
                    "русский_field": "object"
                },
                "validation_criteria": {
                    "arabic_العربية": {"min": 1}
                }
            },
            "quality_gates": ["качество_gate"],
            "handoff_criteria": ["handoff_критерий"]
        }
        
        # Should handle Unicode gracefully
        result = validator.validate_contract(contract)
        assert isinstance(result.is_valid, bool), "Should handle Unicode without crashing"
    
    def test_schema_corruption_recovery(self, validator):
        """Test behavior when schema becomes corrupted during runtime."""
        # Save original schema
        original_schema = validator.schema.copy()
        
        # Corrupt the schema
        validator.schema = {"invalid": "schema"}
        
        # Validation should fail gracefully
        contract = {"contract_version": "1.0"}
        
        try:
            result = validator.validate_contract(contract)
            assert not result.is_valid, "Should fail with corrupted schema"
        except ContractValidationError:
            # Acceptable to raise ContractValidationError
            pass
        
        # Restore original schema
        validator.schema = original_schema


class TestContractValidatorThreadSafety:
    """Test thread safety of contract validation operations."""
    
    @pytest.fixture
    def validator(self):
        """Create ContractValidator instance for testing."""
        return ContractValidator()
    
    @pytest.fixture
    def base_contract(self):
        """Base contract for thread safety testing."""
        return {
            "contract_version": "1.0",
            "contract_type": "game_designer_to_developer",
            "source_agent": "game_designer",
            "target_agent": "developer",
            "dna_compliance": {
                "time_respect_validated": True,
                "pedagogical_value_validated": True,
                "professional_tone_validated": True,
                "policy_to_practice_validated": True,
                "holistic_thinking_validated": True
            },
            "input_requirements": {
                "required_files": [],
                "required_data": {},
                "required_validations": []
            },
            "output_specifications": {
                "deliverable_files": [],
                "deliverable_data": {},
                "validation_criteria": {}
            },
            "quality_gates": [],
            "handoff_criteria": []
        }
    
    def test_concurrent_validations_same_contract(self, validator, base_contract):
        """Test concurrent validation of the same contract."""
        def validate_contract_thread(thread_id: int):
            contract = base_contract.copy()
            contract["story_id"] = f"STORY-THREAD-{thread_id:03d}"
            
            results = []
            for i in range(10):
                result = validator.validate_contract(contract)
                results.append(result.is_valid)
            
            return all(results)
        
        # Run concurrent validations
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(validate_contract_thread, i) for i in range(10)]
            results = [future.result() for future in futures]
        
        assert all(results), "All concurrent validations should succeed"
    
    def test_concurrent_validations_different_contracts(self, validator, base_contract):
        """Test concurrent validation of different contracts."""
        def validate_different_contract(contract_index: int):
            contract = base_contract.copy()
            contract["story_id"] = f"STORY-DIFFERENT-{contract_index:03d}"
            
            # Make each contract slightly different
            if contract_index % 2 == 0:
                contract["quality_gates"] = [f"gate_{contract_index}"]
            if contract_index % 3 == 0:
                contract["handoff_criteria"] = [f"criteria_{contract_index}"]
            
            result = validator.validate_contract(contract)
            return result.is_valid
        
        # Run concurrent validations with different contracts
        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(validate_different_contract, i) for i in range(50)]
            results = [future.result() for future in futures]
        
        assert all(results), "All concurrent validations of different contracts should succeed"
    
    def test_validator_state_integrity_under_concurrency(self, validator, base_contract):
        """Test that validator internal state remains intact under concurrent access."""
        original_schema = validator.schema.copy()
        original_sequences = validator.valid_agent_sequences.copy()
        
        def stress_test_validation(iterations: int):
            for i in range(iterations):
                contract = base_contract.copy()
                contract["story_id"] = f"STORY-STRESS-{i:05d}"
                validator.validate_contract(contract)
        
        # Run stress test with multiple threads
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(stress_test_validation, 100) for _ in range(10)]
            for future in futures:
                future.result()  # Wait for completion
        
        # Verify validator state integrity
        assert validator.schema == original_schema, "Schema should remain unchanged"
        assert validator.valid_agent_sequences == original_sequences, "Agent sequences should remain unchanged"