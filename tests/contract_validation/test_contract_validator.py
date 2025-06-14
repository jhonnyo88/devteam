"""
Basic ContractValidator tests for DigiNativa AI Team system.

PURPOSE:
Validate that our most critical component - ContractValidator - 
works correctly for schema validation and basic functionality.

CRITICAL IMPORTANCE:
These tests protect the foundation of our modular architecture.
"""

import pytest
import json
import sys
from pathlib import Path

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.shared.contract_validator import ContractValidator, ValidationResult, ContractValidationError


class TestContractValidatorBasics:
    """Test basic ContractValidator functionality."""
    
    def test_contract_validator_initialization(self):
        """Test that ContractValidator can be initialized with valid schema."""
        # This should work since we verified the schema exists
        validator = ContractValidator()
        
        # Check that schema was loaded
        assert validator.schema is not None
        assert isinstance(validator.schema, dict)
        assert validator.schema_path.exists()
    
    def test_schema_loading_with_nonexistent_file(self):
        """Test that ContractValidator raises error for missing schema file."""
        with pytest.raises(FileNotFoundError):
            ContractValidator(schema_path="nonexistent/schema.json")
    
    def test_valid_agent_sequences_defined(self):
        """Test that valid agent sequences are properly defined."""
        validator = ContractValidator()
        
        # Check that all required agent sequences are defined
        expected_agents = {
            "github", "project_manager", "game_designer", 
            "developer", "test_engineer", "qa_tester", "quality_reviewer"
        }
        
        defined_agents = set(validator.valid_agent_sequences.keys())
        
        # All agents except github should be in both source and target
        assert "github" in defined_agents
        assert "project_manager" in defined_agents
        
        # Check specific sequences that are critical for workflow
        assert "project_manager" in validator.valid_agent_sequences["github"]
        assert "game_designer" in validator.valid_agent_sequences["project_manager"]
        assert "developer" in validator.valid_agent_sequences["game_designer"]
    
    def test_required_principles_defined(self):
        """Test that required DNA principles are properly defined."""
        validator = ContractValidator()
        
        # Check design principles
        expected_design_principles = {
            "pedagogical_value", "policy_to_practice", "time_respect",
            "holistic_thinking", "professional_tone"
        }
        assert validator.required_design_principles == expected_design_principles
        
        # Check architecture principles  
        expected_architecture_principles = {
            "api_first", "stateless_backend", 
            "separation_of_concerns", "simplicity_first"
        }
        assert validator.required_architecture_principles == expected_architecture_principles


class TestContractSchemaValidation:
    """Test contract schema validation functionality."""
    
    @pytest.fixture
    def validator(self):
        """Provide a ContractValidator instance for tests."""
        return ContractValidator()
    
    @pytest.fixture
    def valid_contract(self):
        """Provide a valid contract for testing."""
        return {
            "contract_version": "1.0",
            "story_id": "STORY-TEST-001",
            "source_agent": "project_manager",
            "target_agent": "game_designer",
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
                "required_files": ["test_file.md"],
                "required_data": {"test": "data"},
                "required_validations": ["test_validation"]
            },
            "output_specifications": {
                "deliverable_files": ["output_file.md"],
                "deliverable_data": {"output": "data"},
                "validation_criteria": {
                    "design_principles": {
                        "pedagogical_value": {"min_score": 4}
                    }
                }
            },
            "quality_gates": ["test_quality_gate"],
            "handoff_criteria": ["test_handoff_criterion"]
        }
    
    def test_schema_validation_with_valid_contract(self, validator, valid_contract):
        """Test that valid contracts pass schema validation."""
        errors = validator._validate_schema(valid_contract)
        assert errors == [], f"Valid contract should pass schema validation, got errors: {errors}"
    
    def test_schema_validation_with_missing_required_field(self, validator, valid_contract):
        """Test that contracts missing required fields fail validation."""
        # Remove required field
        del valid_contract["contract_version"]
        
        errors = validator._validate_schema(valid_contract)
        assert len(errors) > 0, "Contract missing required field should fail validation"
        assert any("contract_version" in error for error in errors), "Error should mention missing contract_version"
    
    def test_schema_validation_with_invalid_agent(self, validator, valid_contract):
        """Test that contracts with invalid agents fail validation."""
        # Set invalid source agent
        valid_contract["source_agent"] = "invalid_agent"
        
        errors = validator._validate_schema(valid_contract)
        assert len(errors) > 0, "Contract with invalid agent should fail validation"
        assert any("invalid_agent" in error for error in errors), "Error should mention invalid agent"
    
    def test_schema_validation_with_invalid_story_id_format(self, validator, valid_contract):
        """Test that contracts with invalid story ID format fail validation."""
        # Set invalid story ID format
        valid_contract["story_id"] = "INVALID-FORMAT"
        
        errors = validator._validate_schema(valid_contract)
        assert len(errors) > 0, "Contract with invalid story ID should fail validation"
    
    def test_schema_validation_with_missing_dna_principles(self, validator, valid_contract):
        """Test that contracts missing DNA principles fail validation."""
        # Remove required design principle
        del valid_contract["dna_compliance"]["design_principles_validation"]["pedagogical_value"]
        
        errors = validator._validate_schema(valid_contract)
        assert len(errors) > 0, "Contract missing DNA principle should fail validation"
        assert any("pedagogical_value" in error for error in errors), "Error should mention missing principle"


class TestUtilityFunctions:
    """Test utility functions for contract validation."""
    
    def test_get_valid_next_agents(self):
        """Test getting valid next agents for a source agent."""
        validator = ContractValidator()
        
        # Test known valid sequences
        pm_targets = validator.get_valid_next_agents("project_manager")
        assert "game_designer" in pm_targets
        
        gd_targets = validator.get_valid_next_agents("game_designer") 
        assert "developer" in gd_targets
        
        # Test unknown agent returns empty list
        unknown_targets = validator.get_valid_next_agents("unknown_agent")
        assert unknown_targets == []


class TestErrorHandling:
    """Test error handling in ContractValidator."""
    
    def test_validation_error_formatting(self):
        """Test that validation errors are properly formatted."""
        validator = ContractValidator()
        
        # Test with a real invalid contract to get proper ValidationError
        invalid_contract = {}  # Missing all required fields
        
        try:
            import jsonschema
            jsonschema.validate(invalid_contract, validator.schema)
        except jsonschema.ValidationError as error:
            # Test formatting with real ValidationError
            formatted = validator._format_validation_error(error)
            assert isinstance(formatted, str)
            assert len(formatted) > 0
        else:
            pytest.fail("Expected ValidationError was not raised")


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])