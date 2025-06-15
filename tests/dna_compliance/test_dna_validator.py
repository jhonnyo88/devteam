"""
DNA Validator Tests

Tests the core DNA validation framework that ensures all DigiNativa AI Team
features comply with the project's DNA principles.

DNA VALIDATION FRAMEWORK:
1. Design Principles (5): pedagogical_value, policy_to_practice, time_respect, 
   holistic_thinking, professional_tone
2. Architecture Principles (4): api_first, stateless_backend, 
   separation_of_concerns, simplicity_first

This validator is CRITICAL for maintaining DigiNativa's identity and ensuring
all features deliver value to Swedish municipal users like Anna.
"""

import pytest
import time
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, patch
from datetime import datetime

from modules.shared.exceptions import DNAComplianceError, ValidationError
from modules.shared.dna_validator import DNAValidator, DNAValidationResult
from modules.shared.contract_validator import ContractValidator


class TestDNAValidator:
    """Test DNA validation framework functionality."""
    
    @pytest.fixture
    def dna_validator(self):
        """Create DNA validator instance."""
        return DNAValidator()
    
    @pytest.fixture
    def contract_validator(self):
        """Contract validator for testing integration."""
        return ContractValidator()

    @pytest.fixture
    def sample_feature_data(self):
        """Sample feature data for DNA validation testing."""
        return {
            "feature_description": """
            As Anna, a municipal administrator, I want to practice policy application 
            through interactive scenarios so that I can better understand real-world 
            implementation and improve my decision-making skills.
            
            This feature provides guided policy scenarios with immediate feedback,
            helping municipal employees apply theoretical knowledge to practical situations.
            Each scenario is designed to be completed within 10 minutes to respect
            users' busy schedules while maintaining professional municipal tone throughout.
            """,
            "learning_objectives": [
                "Apply policy knowledge to practical municipal situations",
                "Understand decision-making frameworks in public sector context",
                "Practice critical thinking in policy implementation",
                "Build confidence in handling real-world scenarios"
            ],
            "acceptance_criteria": [
                "User can select from multiple policy scenarios relevant to municipal work",
                "Each scenario provides clear context and background information",
                "User receives immediate feedback on decisions with explanations",
                "Feature completes within 10 minutes maximum",
                "Interface maintains professional municipal tone",
                "Content directly connects policy theory to practice"
            ],
            "user_persona": "Anna",
            "time_constraint_minutes": 10,
            "municipal_context": True,
            "professional_tone_required": True
        }

    @pytest.fixture
    def sample_architectural_data(self):
        """Sample architectural data for testing."""
        return {
            "api_endpoints": [
                {
                    "endpoint": "/api/scenarios",
                    "method": "GET",
                    "stateless": True,
                    "response_format": "json"
                },
                {
                    "endpoint": "/api/scenarios/{id}/feedback",
                    "method": "POST", 
                    "stateless": True,
                    "response_format": "json"
                }
            ],
            "frontend_components": [
                {
                    "name": "ScenarioCard",
                    "responsibility": "Display scenario information",
                    "dependencies": ["Button", "Card"],
                    "complexity": "low"
                },
                {
                    "name": "FeedbackPanel",
                    "responsibility": "Show immediate feedback",
                    "dependencies": ["Alert", "Typography"],
                    "complexity": "low"
                }
            ],
            "backend_services": [
                {
                    "name": "ScenarioService",
                    "responsibility": "Manage policy scenarios",
                    "stateless": True,
                    "complexity": "medium"
                }
            ],
            "simplicity_indicators": {
                "total_components": 2,
                "max_dependency_depth": 1,
                "cyclomatic_complexity": 3.2,
                "code_duplication": 0.05
            }
        }

    def test_dna_validator_initialization(self, dna_validator):
        """Test DNA validator initialization."""
        
        assert dna_validator is not None
        
        # Check design principles are loaded
        design_principles = dna_validator.design_principles
        expected_principles = [
            "pedagogical_value", "policy_to_practice", "time_respect",
            "holistic_thinking", "professional_tone"
        ]
        for principle in expected_principles:
            assert principle in design_principles
        
        # Check architecture principles are loaded
        arch_principles = dna_validator.architecture_principles
        expected_arch = [
            "api_first", "stateless_backend", 
            "separation_of_concerns", "simplicity_first"
        ]
        for principle in expected_arch:
            assert principle in arch_principles
        
        print(" DNA validator initialized with all principles")

    def test_validate_pedagogical_value_success(self, dna_validator, sample_feature_data):
        """Test successful pedagogical value validation."""
        
        result = dna_validator.validate_pedagogical_value(sample_feature_data)
        
        assert result.compliant is True
        assert result.score >= 4.0  # High pedagogical value
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.has_clear_learning_objectives
        assert result.provides_practical_application
        assert result.enables_skill_development
        assert result.municipal_context_relevant
        
        print(f" Pedagogical value validation: {result.score:.1f}/5.0")

    def test_validate_pedagogical_value_failure(self, dna_validator):
        """Test pedagogical value validation with poor content."""
        
        poor_feature_data = {
            "feature_description": "Add a button to the interface",
            "learning_objectives": [],  # No learning objectives
            "acceptance_criteria": ["Button works"],
            "user_persona": "Anna",
            "municipal_context": False  # Not municipal-relevant
        }
        
        result = dna_validator.validate_pedagogical_value(poor_feature_data)
        
        assert result.compliant is False
        assert result.score < 3.0  # Poor pedagogical value
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.has_clear_learning_objectives
        assert not result.municipal_context_relevant
        
        print(f" Pedagogical value rejection: {result.score:.1f}/5.0 (expected low)")

    def test_validate_policy_to_practice_success(self, dna_validator, sample_feature_data):
        """Test successful policy-to-practice validation."""
        
        result = dna_validator.validate_policy_to_practice(sample_feature_data)
        
        assert result.compliant is True
        assert result.score >= 4.0
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.connects_theory_to_practice
        assert result.provides_real_world_scenarios
        assert result.enables_practical_application
        assert result.municipal_policy_relevant
        
        print(f" Policy-to-practice validation: {result.score:.1f}/5.0")

    def test_validate_policy_to_practice_failure(self, dna_validator):
        """Test policy-to-practice validation with theoretical-only content."""
        
        theoretical_feature_data = {
            "feature_description": "Display policy documentation for reading",
            "learning_objectives": ["Read policy documents"],
            "acceptance_criteria": ["User can view policy text"],
            "practical_application": False,  # No practical application
            "real_world_scenarios": False,   # No scenarios
            "municipal_context": False
        }
        
        result = dna_validator.validate_policy_to_practice(theoretical_feature_data)
        
        assert result.compliant is False
        assert result.score < 3.0
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.provides_real_world_scenarios
        assert not result.enables_practical_application
        
        print(f" Policy-to-practice rejection: {result.score:.1f}/5.0 (expected low)")

    def test_validate_time_respect_success(self, dna_validator, sample_feature_data):
        """Test successful time respect validation."""
        
        result = dna_validator.validate_time_respect(sample_feature_data)
        
        assert result.compliant is True
        assert result.score >= 4.0
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.within_time_constraint
        assert result.efficient_task_flow
        assert result.minimal_cognitive_load
        assert result.estimated_completion_time <= 10  # Minutes
        
        print(f" Time respect validation: {result.score:.1f}/5.0")

    def test_validate_time_respect_failure(self, dna_validator):
        """Test time respect validation with excessive time requirements."""
        
        time_excessive_data = {
            "feature_description": "Complex multi-step process requiring extensive training",
            "time_constraint_minutes": 45,  # Exceeds 10-minute limit
            "task_complexity": "high",
            "cognitive_load": "excessive",
            "user_persona": "Anna",
            "estimated_steps": 25  # Too many steps
        }
        
        result = dna_validator.validate_time_respect(time_excessive_data)
        
        assert result.compliant is False
        assert result.score < 3.0
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.within_time_constraint
        assert not result.efficient_task_flow
        assert result.estimated_completion_time > 10
        
        print(f" Time respect rejection: {result.score:.1f}/5.0 (expected low)")

    def test_validate_holistic_thinking_success(self, dna_validator, sample_feature_data):
        """Test successful holistic thinking validation."""
        
        result = dna_validator.validate_holistic_thinking(sample_feature_data)
        
        assert result.compliant is True
        assert result.score >= 4.0
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.considers_multiple_perspectives
        assert result.integrates_various_contexts
        assert result.addresses_broader_implications
        assert result.connects_to_organizational_goals
        
        print(f" Holistic thinking validation: {result.score:.1f}/5.0")

    def test_validate_holistic_thinking_failure(self, dna_validator):
        """Test holistic thinking validation with narrow focus."""
        
        narrow_feature_data = {
            "feature_description": "Simple form field validation",
            "learning_objectives": ["Validate input"],  # Very narrow
            "broader_context": False,
            "organizational_impact": False,
            "multiple_perspectives": False,
            "user_persona": "Anna"
        }
        
        result = dna_validator.validate_holistic_thinking(narrow_feature_data)
        
        assert result.compliant is False
        assert result.score < 3.0
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.considers_multiple_perspectives
        assert not result.addresses_broader_implications
        
        print(f" Holistic thinking rejection: {result.score:.1f}/5.0 (expected low)")

    def test_validate_professional_tone_success(self, dna_validator, sample_feature_data):
        """Test successful professional tone validation."""
        
        result = dna_validator.validate_professional_tone(sample_feature_data)
        
        assert result.compliant is True
        assert result.score >= 4.0
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.maintains_professional_language
        assert result.appropriate_for_municipal_context
        assert result.respectful_and_clear_communication
        assert result.consistent_terminology
        
        print(f" Professional tone validation: {result.score:.1f}/5.0")

    def test_validate_professional_tone_failure(self, dna_validator):
        """Test professional tone validation with inappropriate language."""
        
        unprofessional_data = {
            "feature_description": "Cool app that's gonna be awesome for users",
            "ui_text": [
                "Hey there! Let's get started!",
                "Oops, something went wrong lol",
                "You're totally done now!"
            ],
            "tone_analysis": {
                "formality_level": "casual",
                "municipal_appropriate": False,
                "professional_terminology": False
            },
            "user_persona": "Anna"
        }
        
        result = dna_validator.validate_professional_tone(unprofessional_data)
        
        assert result.compliant is False
        assert result.score < 3.0
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.maintains_professional_language
        assert not result.appropriate_for_municipal_context
        
        print(f" Professional tone rejection: {result.score:.1f}/5.0 (expected low)")

    def test_validate_api_first_success(self, dna_validator, sample_architectural_data):
        """Test successful API-first validation."""
        
        result = dna_validator.validate_api_first(sample_architectural_data)
        
        assert result.compliant is True
        assert result.score >= 4.0
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.has_well_defined_apis
        assert result.apis_documented
        assert result.consistent_api_design
        assert result.api_first_development_approach
        
        print(f" API-first validation: {result.score:.1f}/5.0")

    def test_validate_api_first_failure(self, dna_validator):
        """Test API-first validation with poor API design."""
        
        poor_api_data = {
            "api_endpoints": [],  # No APIs defined
            "frontend_components": [
                {
                    "name": "Component",
                    "data_access": "direct_database",  # Bypasses API
                    "coupling": "tight"
                }
            ],
            "api_documentation": False,
            "api_consistency": False
        }
        
        result = dna_validator.validate_api_first(poor_api_data)
        
        assert result.compliant is False
        assert result.score < 3.0
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.has_well_defined_apis
        assert not result.apis_documented
        
        print(f" API-first rejection: {result.score:.1f}/5.0 (expected low)")

    def test_validate_stateless_backend_success(self, dna_validator, sample_architectural_data):
        """Test successful stateless backend validation."""
        
        result = dna_validator.validate_stateless_backend(sample_architectural_data)
        
        assert result.compliant is True
        assert result.score >= 4.0
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.services_are_stateless
        assert result.no_server_side_sessions
        assert result.scalable_architecture
        assert result.proper_state_management
        
        print(f" Stateless backend validation: {result.score:.1f}/5.0")

    def test_validate_stateless_backend_failure(self, dna_validator):
        """Test stateless backend validation with stateful design."""
        
        stateful_data = {
            "backend_services": [
                {
                    "name": "SessionService",
                    "stateless": False,  # Maintains state
                    "session_storage": "server_memory",
                    "scalability": "limited"
                }
            ],
            "state_management": "server_side",
            "session_handling": "in_memory",
            "scalability_issues": True
        }
        
        result = dna_validator.validate_stateless_backend(stateful_data)
        
        assert result.compliant is False
        assert result.score < 3.0
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.services_are_stateless
        assert not result.scalable_architecture
        
        print(f" Stateless backend rejection: {result.score:.1f}/5.0 (expected low)")

    def test_validate_separation_of_concerns_success(self, dna_validator, sample_architectural_data):
        """Test successful separation of concerns validation."""
        
        result = dna_validator.validate_separation_of_concerns(sample_architectural_data)
        
        assert result.compliant is True
        assert result.score >= 4.0
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.clear_component_responsibilities
        assert result.minimal_coupling
        assert result.proper_layer_separation
        assert result.single_responsibility_principle
        
        print(f" Separation of concerns validation: {result.score:.1f}/5.0")

    def test_validate_separation_of_concerns_failure(self, dna_validator):
        """Test separation of concerns validation with poor separation."""
        
        coupled_data = {
            "frontend_components": [
                {
                    "name": "MonolithicComponent",
                    "responsibilities": [
                        "ui_rendering", "business_logic", "data_access", 
                        "validation", "error_handling", "logging"
                    ],  # Too many responsibilities
                    "dependencies": ["Database", "EmailService", "PaymentAPI", "Logger"],
                    "coupling": "high"
                }
            ],
            "layer_separation": False,
            "responsibility_overlap": True,
            "tight_coupling": True
        }
        
        result = dna_validator.validate_separation_of_concerns(coupled_data)
        
        assert result.compliant is False
        assert result.score < 3.0
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.clear_component_responsibilities
        assert not result.minimal_coupling
        
        print(f" Separation of concerns rejection: {result.score:.1f}/5.0 (expected low)")

    def test_validate_simplicity_first_success(self, dna_validator, sample_architectural_data):
        """Test successful simplicity-first validation."""
        
        result = dna_validator.validate_simplicity_first(sample_architectural_data)
        
        assert result.compliant is True
        assert result.score >= 4.0
        assert len(result.violations) == 0
        
        # Verify specific criteria
        assert result.simple_solution_chosen
        assert result.minimal_complexity
        assert result.easy_to_understand
        assert result.maintainable_codebase
        
        print(f" Simplicity-first validation: {result.score:.1f}/5.0")

    def test_validate_simplicity_first_failure(self, dna_validator):
        """Test simplicity-first validation with over-engineered solution."""
        
        complex_data = {
            "architecture_pattern": "microservices_with_event_sourcing_and_cqrs",
            "simplicity_indicators": {
                "total_components": 25,  # Too many
                "max_dependency_depth": 8,  # Too deep
                "cyclomatic_complexity": 12.5,  # Too complex
                "code_duplication": 0.35,  # High duplication
                "abstraction_layers": 7  # Over-abstracted
            },
            "over_engineered": True,
            "unnecessary_patterns": ["Factory", "AbstractFactory", "Observer", "Command"],
            "simple_solution_available": True
        }
        
        result = dna_validator.validate_simplicity_first(complex_data)
        
        assert result.compliant is False
        assert result.score < 3.0
        assert len(result.violations) > 0
        
        # Check specific failures
        assert not result.simple_solution_chosen
        assert not result.minimal_complexity
        
        print(f" Simplicity-first rejection: {result.score:.1f}/5.0 (expected low)")

    def test_comprehensive_dna_validation(self, dna_validator, sample_feature_data, sample_architectural_data):
        """Test comprehensive DNA validation of both design and architecture."""
        
        combined_data = {**sample_feature_data, **sample_architectural_data}
        
        result = dna_validator.validate_complete_dna_compliance(combined_data)
        
        assert isinstance(result, DNAValidationResult)
        assert result.overall_compliant is True
        assert result.overall_score >= 4.0
        
        # Verify all principle results are present
        assert result.design_principle_results is not None
        assert result.architecture_principle_results is not None
        
        # Verify individual principle compliance
        design_results = result.design_principle_results
        assert design_results["pedagogical_value"].compliant
        assert design_results["policy_to_practice"].compliant
        assert design_results["time_respect"].compliant
        assert design_results["holistic_thinking"].compliant
        assert design_results["professional_tone"].compliant
        
        arch_results = result.architecture_principle_results
        assert arch_results["api_first"].compliant
        assert arch_results["stateless_backend"].compliant
        assert arch_results["separation_of_concerns"].compliant
        assert arch_results["simplicity_first"].compliant
        
        print(f" Comprehensive DNA validation: {result.overall_score:.1f}/5.0")
        print(f"   Design principles avg: {result.design_principles_avg_score:.1f}/5.0")
        print(f"   Architecture principles avg: {result.architecture_principles_avg_score:.1f}/5.0")

    def test_dna_validation_performance(self, dna_validator, sample_feature_data, sample_architectural_data):
        """Test DNA validation performance requirements."""
        
        combined_data = {**sample_feature_data, **sample_architectural_data}
        
        # Measure validation performance
        start_time = time.time()
        
        for _ in range(10):  # Run 10 validations
            result = dna_validator.validate_complete_dna_compliance(combined_data)
            assert result.overall_compliant is True
        
        total_time = time.time() - start_time
        avg_time = total_time / 10
        
        # Should complete quickly
        assert avg_time < 1.0, f"DNA validation too slow: {avg_time:.3f}s average"
        assert total_time < 5.0, f"Total validation time too slow: {total_time:.3f}s"
        
        print(f" DNA validation performance: {avg_time:.3f}s average, {total_time:.3f}s total")

    def test_dna_validation_error_handling(self, dna_validator):
        """Test DNA validation error handling with invalid data."""
        
        # Test with None data
        try:
            result = dna_validator.validate_complete_dna_compliance(None)
            assert result.overall_compliant is False
            print("    None data handled gracefully")
        except Exception as e:
            assert "data" in str(e).lower()
            print("    None data error informative")
        
        # Test with empty data
        result = dna_validator.validate_complete_dna_compliance({})
        assert result.overall_compliant is False
        assert result.overall_score < 3.0
        print("    Empty data handled gracefully")
        
        # Test with malformed data
        malformed_data = {
            "feature_description": None,
            "learning_objectives": "not_a_list",
            "time_constraint_minutes": "not_a_number"
        }
        
        result = dna_validator.validate_complete_dna_compliance(malformed_data)
        assert result.overall_compliant is False
        print("    Malformed data handled gracefully")
        
        print(" DNA validation error handling working correctly")

    def test_dna_validation_with_contract_integration(self, dna_validator, contract_validator):
        """Test DNA validation integration with contract validation."""
        
        # Create a contract with DNA compliance data
        contract_with_dna = {
            "contract_version": "1.0",
            "story_id": "STORY-DNA-001",
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
                "required_data": {
                    "feature_data": {
                        "learning_objectives": ["Learn policy application"],
                        "time_constraint_minutes": 8,
                        "municipal_context": True
                    }
                }
            }
        }
        
        # Validate contract structure
        assert contract_validator.validate_contract_schema(contract_with_dna)
        print("    Contract structure valid")
        
        # Extract feature data for DNA validation
        feature_data = contract_with_dna["input_requirements"]["required_data"]["feature_data"]
        
        # Validate DNA compliance
        dna_result = dna_validator.validate_complete_dna_compliance(feature_data)
        
        # Verify DNA compliance matches contract claims
        dna_compliance = contract_with_dna["dna_compliance"]
        
        # Design principles should match
        design_validation = dna_compliance["design_principles_validation"]
        if dna_result.overall_compliant:
            for principle, claimed_compliant in design_validation.items():
                if claimed_compliant:
                    principle_result = dna_result.design_principle_results.get(principle)
                    if principle_result:
                        assert principle_result.compliant, f"Claimed {principle} compliance but validation failed"
        
        print("    DNA compliance consistent with contract claims")
        print(" DNA validation contract integration working correctly")

    def test_dna_validation_scoring_algorithms(self, dna_validator):
        """Test DNA validation scoring algorithms consistency."""
        
        # Test with known good data
        excellent_data = {
            "feature_description": "Interactive municipal policy training with immediate feedback",
            "learning_objectives": [
                "Apply policy knowledge practically",
                "Understand municipal decision frameworks",
                "Practice real-world scenario handling"
            ],
            "time_constraint_minutes": 8,
            "municipal_context": True,
            "professional_tone_required": True,
            "practical_application": True,
            "api_endpoints": [{"endpoint": "/api/test", "stateless": True}],
            "simplicity_indicators": {"total_components": 3, "complexity": 2.1}
        }
        
        result = dna_validator.validate_complete_dna_compliance(excellent_data)
        
        # Should score highly
        assert result.overall_score >= 4.0, f"Excellent data should score high: {result.overall_score}"
        assert result.design_principles_avg_score >= 4.0
        assert result.architecture_principles_avg_score >= 4.0
        
        # Test with known poor data
        poor_data = {
            "feature_description": "Simple button",
            "learning_objectives": [],  # No objectives
            "time_constraint_minutes": 30,  # Too long
            "municipal_context": False,
            "professional_tone_required": False,
            "practical_application": False,
            "api_endpoints": [],  # No APIs
            "simplicity_indicators": {"total_components": 20, "complexity": 9.5}  # Too complex
        }
        
        poor_result = dna_validator.validate_complete_dna_compliance(poor_data)
        
        # Should score poorly
        assert poor_result.overall_score < 3.0, f"Poor data should score low: {poor_result.overall_score}"
        
        # Excellent should significantly outscore poor
        score_difference = result.overall_score - poor_result.overall_score
        assert score_difference >= 1.5, f"Score difference too small: {score_difference}"
        
        print(f" Scoring consistency: Excellent {result.overall_score:.1f} vs Poor {poor_result.overall_score:.1f}")


# DNA validation benchmarks and thresholds
DNA_VALIDATION_BENCHMARKS = {
    "minimum_compliance_score": 3.5,  # Minimum to pass
    "target_compliance_score": 4.0,   # Target for quality
    "excellent_compliance_score": 4.5, # Excellent quality
    "max_validation_time": 1.0,       # Maximum time in seconds
    "design_principles_weight": 0.6,  # 60% weight
    "architecture_principles_weight": 0.4,  # 40% weight
}


if __name__ == "__main__":
    # Run with: pytest tests/dna_compliance/test_dna_validator.py -v
    pytest.main([__file__, "-v", "--tb=short"])