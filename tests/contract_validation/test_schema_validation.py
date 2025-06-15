"""
Test script för schema validation i ContractValidator.

Detta script testar att schema validation fungerar korrekt med både
valid och invalid contracts.

ANVÄNDNING:
1. Se till att du har skapat filerna:
   - docs/contracts/agent_contract_schema.json
   - modules/shared/contract_validator.py

2. Kör scriptet:
   python test_schema_validation.py

FÖRVÄNTAT RESULTAT:
✅ Schema validation tests passed!
"""

import sys
import json
import logging
from pathlib import Path

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Add modules to path so we can import our validator
sys.path.append(str(Path(__file__).parent / "modules"))

try:
    from shared.contract_validator import ContractValidator, ContractValidationError
except ImportError as e:
    print(f"❌ Error importing ContractValidator: {e}")
    print("Make sure you have created modules/shared/contract_validator.py")
    sys.exit(1)


def test_schema_validation():
    """Test schema validation with valid and invalid contracts."""
    
    print("🧪 Testing ContractValidator Schema Validation...")
    
    # Test 1: Valid contract från Implementation_rules.md
    print("\n📋 Test 1: Valid contract should pass schema validation")
    
    valid_contract = {
        "contract_version": "1.0",
        "contract_type": "feature_to_game_design_and_ux",
        "story_id": "STORY-001-001",
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
            "required_files": [
                "docs/stories/story_description_STORY-001-001.md",
                "docs/analysis/feature_analysis_STORY-001-001.json"
            ],
            "required_data": {
                "feature_description": "Add user registration for DigiNativa game",
                "acceptance_criteria": [
                    "User can create account with email and password",
                    "User receives confirmation email",
                    "User can log in after registration"
                ],
                "user_persona": "Anna",
                "time_constraint_minutes": 10,
                "learning_objectives": ["Understanding user registration process"],
                "gdd_section_reference": "section_2_user_management",
                "priority_level": "high",
                "complexity_assessment": {"technical": "medium", "design": "low"}
            },
            "required_validations": [
                "dna_design_principles_alignment_verified",
                "gdd_consistency_checked",
                "technical_feasibility_confirmed"
            ]
        },
        "output_specifications": {
            "deliverable_files": [
                "docs/specs/game_design_STORY-001-001.md",
                "docs/specs/ux_specification_STORY-001-001.md",
                "docs/specs/component_mapping_STORY-001-001.json"
            ],
            "deliverable_data": {
                "game_mechanics": {},
                "ui_components": [],
                "interaction_flows": [],
                "asset_requirements": []
            },
            "validation_criteria": {
                "design_principles": {
                    "pedagogical_value": {"min_score": 4},
                    "time_respect": {"max_duration_minutes": 10},
                    "professional_tone": {"style_guide_compliance": True}
                },
                "design_quality": {
                    "component_library_compliance": {"percentage": 100},
                    "accessibility_considerations": {"included": True},
                    "responsive_design_specified": {"included": True}
                }
            }
        },
        "quality_gates": [
            "component_library_mapping_complete",
            "wireframes_generated_and_validated",
            "game_mechanics_pedagogically_sound",
            "ux_specification_technically_implementable"
        ],
        "handoff_criteria": [
            "all_required_components_mapped",
            "interaction_flows_fully_specified",
            "asset_requirements_clearly_defined",
            "developer_implementation_ready"
        ]
    }
    
    try:
        validator = ContractValidator()
        schema_errors = validator._validate_schema(valid_contract)
        
        if len(schema_errors) == 0:
            print("✅ Valid contract passed schema validation!")
        else:
            print(f"❌ Valid contract failed schema validation: {schema_errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing valid contract: {e}")
        return False
    
    # Test 2: Invalid contract should fail schema validation
    print("\n📋 Test 2: Invalid contract should fail schema validation")
    
    invalid_contract = {
        "invalid": "data",
        "missing": "required fields"
    }
    
    try:
        schema_errors = validator._validate_schema(invalid_contract)
        
        if len(schema_errors) > 0:
            print(f"✅ Invalid contract correctly failed schema validation!")
            print(f"   Error details: {schema_errors[0]}")
        else:
            print("❌ Invalid contract incorrectly passed schema validation!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing invalid contract: {e}")
        return False
    
    # Test 3: Contract with wrong types
    print("\n📋 Test 3: Contract with wrong field types should fail")
    
    wrong_types_contract = {
        "contract_version": "1.0",
        "story_id": "STORY-001-001",
        "source_agent": "project_manager",
        "target_agent": "game_designer",
        "dna_compliance": "this should be an object not a string",  # Wrong type
        "input_requirements": {
            "required_files": "this should be an array",  # Wrong type
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
    
    try:
        schema_errors = validator._validate_schema(wrong_types_contract)
        
        if len(schema_errors) > 0:
            print(f"✅ Contract with wrong types correctly failed schema validation!")
            print(f"   Found {len(schema_errors)} type errors")
        else:
            print("❌ Contract with wrong types incorrectly passed schema validation!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing wrong types contract: {e}")
        return False
    
    # Test 4: Contract with invalid agent sequence
    print("\n📋 Test 4: Contract with invalid agent should fail")
    
    invalid_agent_contract = {
        "contract_version": "1.0",
        "story_id": "STORY-001-001",
        "source_agent": "invalid_agent",  # Invalid agent name
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
    
    try:
        schema_errors = validator._validate_schema(invalid_agent_contract)
        
        if len(schema_errors) > 0:
            print(f"✅ Contract with invalid agent correctly failed schema validation!")
            print(f"   Error details: {schema_errors[0]}")
        else:
            print("❌ Contract with invalid agent incorrectly passed schema validation!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing invalid agent contract: {e}")
        return False
    
    return True


def test_schema_loading():
    """Test schema loading functionality."""
    
    print("\n🧪 Testing Schema Loading...")
    
    # Test schema loading with existing file
    print("\n📋 Test: Schema loading with valid file")
    
    try:
        validator = ContractValidator()
        print("✅ Schema loaded successfully during ContractValidator initialization!")
        
    except FileNotFoundError:
        print("❌ Schema file not found. Make sure docs/contracts/agent_contract_schema.json exists")
        return False
        
    except json.JSONDecodeError as e:
        print(f"❌ Schema file contains invalid JSON: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error loading schema: {e}")
        return False
    
    return True


def main():
    """Run all schema validation tests."""
    
    print("🚀 Starting ContractValidator Schema Validation Tests")
    print("=" * 60)
    
    # Test schema loading first
    if not test_schema_loading():
        print("\n❌ Schema loading tests failed!")
        return False
    
    # Test schema validation functionality
    if not test_schema_validation():
        print("\n❌ Schema validation tests failed!")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All schema validation tests passed!")
    print("\n🎉 ContractValidator schema validation is working correctly!")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)