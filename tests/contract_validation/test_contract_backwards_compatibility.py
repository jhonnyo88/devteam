"""
Contract backwards compatibility tests for DigiNativa AI Team system.

PURPOSE:
Validate that contract versioning and evolution maintains backwards compatibility
across all agent interactions while enabling forward progress.

CRITICAL IMPORTANCE:
Contract breaking changes can destroy the modular architecture foundation.
These tests ensure we can safely evolve contracts without breaking existing agents.

TESTING SCOPE:
- Contract version compatibility validation
- Field addition backwards compatibility  
- Field removal detection and handling
- Contract type consistency across versions
- Agent sequence compatibility preservation
"""

import pytest
import json
import copy
import sys
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import patch

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.shared.contract_validator import ContractValidator, ValidationResult, ContractValidationError


class TestContractBackwardsCompatibility:
    """Test contract backwards compatibility and versioning."""
    
    @pytest.fixture
    def validator(self):
        """Create a ContractValidator instance for testing."""
        return ContractValidator()
    
    @pytest.fixture
    def base_contract_v1(self):
        """Base contract version 1.0 for testing."""
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
                    "github_issue": {
                        "title": "string",
                        "body": "string",
                        "labels": "array"
                    }
                },
                "required_validations": ["github_issue_exists"]
            },
            "output_specifications": {
                "deliverable_files": ["story_analysis.json"],
                "deliverable_data": {
                    "story_analysis": "object",
                    "feature_breakdown": "object"
                },
                "validation_criteria": {
                    "story_completeness": {"min": 95}
                }
            },
            "quality_gates": [
                "github_issue_parsed_successfully",
                "story_requirements_complete"
            ],
            "handoff_criteria": [
                "story_analysis_validated",
                "feature_scope_defined"
            ]
        }
    
    @pytest.fixture
    def enhanced_contract_v1_1(self, base_contract_v1):
        """Enhanced contract version 1.1 with additional fields."""
        contract = copy.deepcopy(base_contract_v1)
        contract["contract_version"] = "1.1"
        
        # Add new optional fields (backwards compatible)
        contract["dna_compliance"]["architecture_api_first_validated"] = True
        contract["dna_compliance"]["architecture_stateless_validated"] = True
        
        # Add new optional input data
        contract["input_requirements"]["required_data"]["priority_hints"] = "object"
        
        # Add new optional quality gate
        contract["quality_gates"].append("dna_architecture_validated")
        
        return contract
    
    @pytest.fixture
    def breaking_contract_v2(self, base_contract_v1):
        """Breaking contract version 2.0 with removed required fields."""
        contract = copy.deepcopy(base_contract_v1)
        contract["contract_version"] = "2.0"
        
        # Remove required field (breaking change)
        del contract["dna_compliance"]["time_respect_validated"]
        
        # Remove required input data (breaking change)
        del contract["input_requirements"]["required_data"]["github_issue"]
        
        return contract

    def test_contract_version_validation(self, validator, base_contract_v1):
        """Test that contract versions are properly validated."""
        # Test valid version format
        result = validator.validate_contract(base_contract_v1)
        assert result.is_valid, f"Valid contract should pass validation: {result.errors}"
        
        # Test invalid version format
        invalid_contract = copy.deepcopy(base_contract_v1)
        invalid_contract["contract_version"] = "invalid"
        
        result = validator.validate_contract(invalid_contract)
        assert not result.is_valid, "Invalid version format should fail validation"
        assert any("version" in error.lower() for error in result.errors)

    def test_field_addition_backwards_compatibility(self, validator, base_contract_v1, enhanced_contract_v1_1):
        """Test that adding optional fields maintains backwards compatibility."""
        # Original contract should still be valid
        result_v1 = validator.validate_contract(base_contract_v1)
        assert result_v1.is_valid, "Original contract should remain valid"
        
        # Enhanced contract should also be valid
        result_v1_1 = validator.validate_contract(enhanced_contract_v1_1)
        assert result_v1_1.is_valid, "Enhanced contract should be valid"
        
        # Both contracts should have same contract type and story_id
        assert base_contract_v1["contract_type"] == enhanced_contract_v1_1["contract_type"]
        assert base_contract_v1["story_id"] == enhanced_contract_v1_1["story_id"]

    def test_field_removal_detection(self, validator, base_contract_v1, breaking_contract_v2):
        """Test that field removals are detected as breaking changes."""
        # Original contract should be valid
        result_v1 = validator.validate_contract(base_contract_v1)
        assert result_v1.is_valid, "Original contract should be valid"
        
        # Breaking contract should fail validation
        result_v2 = validator.validate_contract(breaking_contract_v2)
        assert not result_v2.is_valid, "Contract with removed required fields should fail"
        
        # Should detect specific missing fields
        error_messages = " ".join(result_v2.errors).lower()
        assert "time_respect_validated" in error_messages or "required" in error_messages
        assert "github_issue" in error_messages or "required" in error_messages

    def test_contract_type_consistency(self, validator, base_contract_v1):
        """Test that contract type consistency is maintained across versions."""
        valid_contract_types = [
            "github_to_project_manager",
            "project_manager_to_game_designer",
            "game_designer_to_developer",
            "developer_to_test_engineer",
            "test_engineer_to_qa_tester",
            "qa_tester_to_quality_reviewer"
        ]
        
        for contract_type in valid_contract_types:
            contract = copy.deepcopy(base_contract_v1)
            contract["contract_type"] = contract_type
            
            result = validator.validate_contract(contract)
            assert result.is_valid, f"Contract type {contract_type} should be valid"

    def test_invalid_contract_type_rejection(self, validator, base_contract_v1):
        """Test that invalid contract types are rejected."""
        invalid_contract_types = [
            "invalid_type",
            "developer_to_project_manager",  # Wrong sequence
            "qa_tester_to_game_designer",    # Wrong sequence
            ""  # Empty type
        ]
        
        for invalid_type in invalid_contract_types:
            contract = copy.deepcopy(base_contract_v1)
            contract["contract_type"] = invalid_type
            
            result = validator.validate_contract(contract)
            assert not result.is_valid, f"Invalid contract type {invalid_type} should be rejected"

    def test_agent_sequence_compatibility(self, validator, base_contract_v1):
        """Test that agent sequences remain consistent across contract versions."""
        # Test all valid agent sequences
        valid_sequences = [
            ("github", "project_manager"),
            ("project_manager", "game_designer"),
            ("game_designer", "developer"),
            ("developer", "test_engineer"),
            ("test_engineer", "qa_tester"),
            ("qa_tester", "quality_reviewer")
        ]
        
        for source, target in valid_sequences:
            contract = copy.deepcopy(base_contract_v1)
            contract["source_agent"] = source
            contract["target_agent"] = target
            contract["contract_type"] = f"{source}_to_{target}"
            
            result = validator.validate_contract(contract)
            assert result.is_valid, f"Agent sequence {source} -> {target} should be valid"

    def test_invalid_agent_sequence_rejection(self, validator, base_contract_v1):
        """Test that invalid agent sequences are rejected."""
        # Test invalid sequences (skipping agents or going backwards)
        invalid_sequences = [
            ("github", "developer"),           # Skipping project_manager and game_designer
            ("developer", "project_manager"),  # Going backwards
            ("quality_reviewer", "github"),    # Going backwards
            ("nonexistent", "project_manager") # Non-existent agent
        ]
        
        for source, target in invalid_sequences:
            contract = copy.deepcopy(base_contract_v1)
            contract["source_agent"] = source
            contract["target_agent"] = target
            contract["contract_type"] = f"{source}_to_{target}"
            
            result = validator.validate_contract(contract)
            assert not result.is_valid, f"Invalid agent sequence {source} -> {target} should be rejected"

    def test_dna_compliance_structure_consistency(self, validator, base_contract_v1):
        """Test that DNA compliance structure remains consistent across versions."""
        required_dna_fields = [
            "time_respect_validated",
            "pedagogical_value_validated",
            "professional_tone_validated",
            "policy_to_practice_validated",
            "holistic_thinking_validated"
        ]
        
        # Test that all required DNA fields are validated
        for field in required_dna_fields:
            contract = copy.deepcopy(base_contract_v1)
            del contract["dna_compliance"][field]
            
            result = validator.validate_contract(contract)
            assert not result.is_valid, f"Missing DNA field {field} should cause validation failure"

    def test_quality_gates_backwards_compatibility(self, validator, base_contract_v1):
        """Test that quality gates can be extended without breaking compatibility."""
        # Original contract with basic quality gates
        result = validator.validate_contract(base_contract_v1)
        assert result.is_valid, "Base contract should be valid"
        
        # Add additional quality gates (should maintain compatibility)
        enhanced_contract = copy.deepcopy(base_contract_v1)
        enhanced_contract["quality_gates"].extend([
            "additional_validation_complete",
            "performance_requirements_met"
        ])
        
        result = validator.validate_contract(enhanced_contract)
        assert result.is_valid, "Contract with additional quality gates should be valid"

    def test_handoff_criteria_backwards_compatibility(self, validator, base_contract_v1):
        """Test that handoff criteria can be extended without breaking compatibility."""
        # Original contract with basic handoff criteria
        result = validator.validate_contract(base_contract_v1)
        assert result.is_valid, "Base contract should be valid"
        
        # Add additional handoff criteria (should maintain compatibility)
        enhanced_contract = copy.deepcopy(base_contract_v1)
        enhanced_contract["handoff_criteria"].extend([
            "documentation_complete",
            "stakeholder_approval_received"
        ])
        
        result = validator.validate_contract(enhanced_contract)
        assert result.is_valid, "Contract with additional handoff criteria should be valid"

    def test_story_id_consistency_requirement(self, validator, base_contract_v1):
        """Test that story_id consistency is enforced across contract versions."""
        valid_story_ids = [
            "STORY-GH-1001",
            "STORY-PM-2001", 
            "STORY-GD-3001",
            "ISSUE-12345"
        ]
        
        for story_id in valid_story_ids:
            contract = copy.deepcopy(base_contract_v1)
            contract["story_id"] = story_id
            
            result = validator.validate_contract(contract)
            assert result.is_valid, f"Valid story_id {story_id} should be accepted"

    def test_invalid_story_id_rejection(self, validator, base_contract_v1):
        """Test that invalid story_id formats are rejected."""
        invalid_story_ids = [
            "",           # Empty
            "invalid",    # No proper format
            "123",        # Just numbers
            None          # None value
        ]
        
        for invalid_id in invalid_story_ids:
            contract = copy.deepcopy(base_contract_v1)
            contract["story_id"] = invalid_id
            
            result = validator.validate_contract(contract)
            assert not result.is_valid, f"Invalid story_id {invalid_id} should be rejected"

    def test_contract_evolution_simulation(self, validator):
        """Test a complete contract evolution scenario to ensure backwards compatibility."""
        # Version 1.0: Basic contract
        contract_v1 = {
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
                "required_validations": ["code_quality_passed"]
            },
            "output_specifications": {
                "deliverable_files": ["test_suite.js"],
                "deliverable_data": {
                    "test_results": "object"
                },
                "validation_criteria": {
                    "test_coverage": {"min": 95}
                }
            },
            "quality_gates": ["code_compiled_successfully"],
            "handoff_criteria": ["tests_implemented"]
        }
        
        # Validate version 1.0
        result_v1 = validator.validate_contract(contract_v1)
        assert result_v1.is_valid, "Version 1.0 should be valid"
        
        # Version 1.1: Add DNA architecture validation (backwards compatible)
        contract_v1_1 = copy.deepcopy(contract_v1)
        contract_v1_1["contract_version"] = "1.1"
        contract_v1_1["dna_compliance"]["api_first_validated"] = True
        contract_v1_1["dna_compliance"]["stateless_backend_validated"] = True
        
        result_v1_1 = validator.validate_contract(contract_v1_1)
        assert result_v1_1.is_valid, "Version 1.1 should be valid"
        
        # Version 1.2: Add performance requirements (backwards compatible)
        contract_v1_2 = copy.deepcopy(contract_v1_1)
        contract_v1_2["contract_version"] = "1.2"
        contract_v1_2["input_requirements"]["required_data"]["performance_requirements"] = "object"
        contract_v1_2["quality_gates"].append("performance_requirements_met")
        
        result_v1_2 = validator.validate_contract(contract_v1_2)
        assert result_v1_2.is_valid, "Version 1.2 should be valid"
        
        # Ensure all versions maintain the same core identity
        versions = [contract_v1, contract_v1_1, contract_v1_2]
        for version in versions:
            assert version["contract_type"] == "developer_to_test_engineer"
            assert version["story_id"] == "STORY-DEV-1001"
            assert version["source_agent"] == "developer"
            assert version["target_agent"] == "test_engineer"


class TestContractCompatibilityUtilities:
    """Test utilities for contract compatibility checking."""
    
    @pytest.fixture
    def validator(self):
        """Create a ContractValidator instance for testing."""
        return ContractValidator()
    
    def test_version_comparison_logic(self, validator):
        """Test version comparison logic for compatibility checking."""
        # Test that validator can handle version strings properly
        test_versions = ["1.0", "1.1", "1.2", "2.0", "2.1"]
        
        for version in test_versions:
            contract = {
                "contract_version": version,
                "contract_type": "github_to_project_manager",
                "story_id": "STORY-TEST-001",
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
            
            result = validator.validate_contract(contract)
            assert result.is_valid, f"Version {version} should be valid format"

    def test_contract_migration_readiness(self, validator):
        """Test that contracts are ready for potential migration scenarios."""
        base_contract = {
            "contract_version": "1.0",
            "contract_type": "game_designer_to_developer",
            "story_id": "STORY-MIGRATION-001",
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
                "required_files": ["ux_specs.json"],
                "required_data": {
                    "ui_components": "array",
                    "interaction_flows": "array"
                },
                "required_validations": ["ux_approved"]
            },
            "output_specifications": {
                "deliverable_files": ["implementation.js"],
                "deliverable_data": {
                    "component_implementations": "array"
                },
                "validation_criteria": {
                    "implementation_complete": True
                }
            },
            "quality_gates": ["ux_validated"],
            "handoff_criteria": ["implementation_ready"]
        }
        
        # Test that contract structure supports future extensions
        result = validator.validate_contract(base_contract)
        assert result.is_valid, "Base contract should be valid for migration"
        
        # Verify contract has all required extensibility points
        assert "dna_compliance" in base_contract
        assert "quality_gates" in base_contract
        assert "handoff_criteria" in base_contract
        assert isinstance(base_contract["quality_gates"], list)
        assert isinstance(base_contract["handoff_criteria"], list)