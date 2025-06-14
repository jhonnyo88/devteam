"""
Contract schema validation tests for DigiNativa AI Team system.

PURPOSE:
Validate that our JSON contract schema is well-formed and 
can successfully validate both valid and invalid contracts.

CRITICAL IMPORTANCE:
The schema defines the contract interface that enables
modular agent architecture - it must be bulletproof.
"""

import pytest
import json
import jsonschema
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class TestContractSchema:
    """Test the contract JSON schema itself."""
    
    @pytest.fixture
    def schema(self):
        """Load the contract schema for testing."""
        schema_path = project_root / "docs" / "contracts" / "agent_contract_schema.json"
        
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    def test_schema_is_valid_json_schema(self, schema):
        """Test that our schema is a valid JSON Schema."""
        # This will raise an exception if the schema is invalid
        jsonschema.validators.validator_for(schema).check_schema(schema)
    
    def test_schema_has_required_properties(self, schema):
        """Test that schema defines all required contract properties."""
        required_fields = schema.get("required", [])
        
        expected_required = {
            "contract_version", "story_id", "source_agent", "target_agent",
            "dna_compliance", "input_requirements", "output_specifications",
            "quality_gates", "handoff_criteria"
        }
        
        assert set(required_fields) == expected_required, f"Required fields mismatch: {set(required_fields)} vs {expected_required}"
    
    def test_schema_defines_valid_agents(self, schema):
        """Test that schema defines correct agent types."""
        source_agents = set(schema["properties"]["source_agent"]["enum"])
        target_agents = set(schema["properties"]["target_agent"]["enum"])
        
        # Source agents include github, target agents don't
        expected_source = {
            "github", "project_manager", "game_designer", 
            "developer", "test_engineer", "qa_tester", "quality_reviewer"
        }
        expected_target = {
            "project_manager", "game_designer", "developer", 
            "test_engineer", "qa_tester", "quality_reviewer"  
        }
        
        assert source_agents == expected_source
        assert target_agents == expected_target
    
    def test_schema_defines_dna_principles(self, schema):
        """Test that schema properly defines DNA principles."""
        dna_compliance = schema["properties"]["dna_compliance"]
        
        # Check design principles
        design_principles = dna_compliance["properties"]["design_principles_validation"]["required"]
        expected_design = [
            "pedagogical_value", "policy_to_practice", "time_respect",
            "holistic_thinking", "professional_tone"
        ]
        assert set(design_principles) == set(expected_design)
        
        # Check architecture principles
        arch_principles = dna_compliance["properties"]["architecture_compliance"]["required"] 
        expected_arch = [
            "api_first", "stateless_backend", 
            "separation_of_concerns", "simplicity_first"
        ]
        assert set(arch_principles) == set(expected_arch)
    
    def test_schema_story_id_pattern(self, schema):
        """Test that story ID pattern is correctly defined."""
        story_id_pattern = schema["properties"]["story_id"]["pattern"]
        
        # Test pattern against valid story IDs
        import re
        pattern = re.compile(story_id_pattern)
        
        valid_story_ids = [
            "STORY-001-001",
            "STORY-USER-REG-002", 
            "STORY-DASHBOARD-001",
            "STORY-TEST-999"
        ]
        
        for story_id in valid_story_ids:
            assert pattern.match(story_id), f"Valid story ID {story_id} should match pattern"
        
        # Test pattern against invalid story IDs
        invalid_story_ids = [
            "story-001-001",  # lowercase
            "STORY-001",      # missing increment
            "STORY--001",     # empty feature id
            "STORY-001-",     # missing increment number
            "INVALID"         # completely wrong format
        ]
        
        for story_id in invalid_story_ids:
            assert not pattern.match(story_id), f"Invalid story ID {story_id} should not match pattern"


class TestSchemaValidationExamples:
    """Test schema validation with specific contract examples."""
    
    @pytest.fixture
    def schema(self):
        """Load the contract schema."""
        schema_path = project_root / "docs" / "contracts" / "agent_contract_schema.json"
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    def test_minimal_valid_contract(self, schema):
        """Test that a minimal valid contract passes validation."""
        minimal_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-MINIMAL-001",
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
        
        # This should not raise an exception
        jsonschema.validate(minimal_contract, schema)
    
    def test_contract_with_extra_properties_fails(self, schema):
        """Test that contracts with extra properties are rejected."""
        contract_with_extra = {
            "contract_version": "1.0",
            "story_id": "STORY-EXTRA-001",
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
            "handoff_criteria": [],
            "extra_property": "this should not be allowed"  # Extra property
        }
        
        # This should raise a ValidationError
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(contract_with_extra, schema)


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])