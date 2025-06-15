"""
Tests for Game Designer DNA UX Validator.

Tests the enhanced DNA validation functionality for Game Designer agent,
ensuring UX designs comply with DigiNativa DNA principles.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from modules.agents.game_designer.tools.dna_ux_validator import (
    DNAUXValidator, DNAUXValidationResult, ComplexityLevel,
    LearningFlowQuality, ToneConsistency
)


class TestDNAUXValidator:
    """Test suite for DNA UX Validator."""
    
    @pytest.fixture
    def validator(self):
        """Create DNA UX validator instance."""
        return DNAUXValidator()
    
    @pytest.fixture
    def sample_ui_components(self):
        """Sample UI components for testing."""
        return [
            {
                "name": "UserRegistrationForm",
                "elements": [
                    {"type": "input", "text": "Ange ditt namn för kommunal verksamhet", "label": "Namn"},
                    {"type": "input", "text": "Ange din e-post för förvaltning", "label": "E-post"},
                    {"type": "button", "text": "Registrera dig i systemet"}
                ],
                "responsive_design": True,
                "breakpoints": ["mobile", "tablet", "desktop"]
            },
            {
                "name": "LearningProgress",
                "elements": [
                    {"type": "progress", "text": "Din framsteg i kommunal träning med kvalitet och effektivitet"},
                    {"type": "text", "text": "Du har slutfört 3 av 5 policy moduler för medborgare service"}
                ],
                "responsive_design": True,
                "breakpoints": ["mobile", "desktop"]
            }
        ]
    
    @pytest.fixture
    def sample_interaction_flows(self):
        """Sample interaction flows for testing."""
        return [
            {
                "name": "registration_flow",
                "user_actions": [
                    {"description": "Användaren öppnar introduktion till registreringsformuläret"},
                    {"description": "Användaren får practice med att fylla i sina uppgifter"},
                    {"description": "Systemet validerar uppgifterna och ger test feedback"},
                    {"description": "Användaren får bekräftelse och quiz avslutning"}
                ],
                "navigation_depth": 2,
                "start_state": "unregistered",
                "end_state": "registered",
                "system_responses": ["validation", "confirmation"]
            }
        ]
    
    @pytest.fixture
    def sample_game_mechanics(self):
        """Sample game mechanics for testing."""
        return {
            "mechanics": [
                {
                    "name": "progress_tracking",
                    "engagement_type": "interactive",
                    "requires_assets": True,
                    "required_assets": [{"type": "ui_element", "category": "progress"}]
                }
            ],
            "learning_objectives_addressed": [
                "Förstå registreringsprocessen",
                "Lära sig kommunala policyer"
            ],
            "pedagogical_effectiveness_score": 4.2
        }
    
    @pytest.fixture
    def sample_story_data(self):
        """Sample story data for testing."""
        return {
            "feature_description": "Användarregistrering för kommunal träning",
            "learning_objectives": [
                "Förstå registreringsprocessen",
                "Lära sig kommunala policyer"
            ],
            "time_constraint_minutes": 10,
            "user_persona": "Anna"
        }

    @pytest.mark.asyncio
    async def test_validate_ux_dna_compliance_success(self, validator, sample_ui_components, 
                                                    sample_interaction_flows, sample_game_mechanics, 
                                                    sample_story_data):
        """Test successful DNA UX validation."""
        result = await validator.validate_ux_dna_compliance(
            sample_game_mechanics,
            sample_ui_components,
            sample_interaction_flows,
            sample_story_data
        )
        
        assert isinstance(result, DNAUXValidationResult)
        assert result.overall_dna_compliant is True
        assert result.dna_compliance_score > 0
        assert result.validation_timestamp is not None
    
    @pytest.mark.asyncio
    async def test_ui_complexity_validation_low_complexity(self, validator, sample_ui_components,
                                                         sample_interaction_flows, sample_story_data):
        """Test UI complexity validation with low complexity."""
        result = await validator._validate_ui_complexity(
            sample_ui_components,
            sample_interaction_flows,
            sample_story_data
        )
        
        assert result.complexity_level in [ComplexityLevel.MINIMAL, ComplexityLevel.LOW, ComplexityLevel.MODERATE]
        assert result.cognitive_load_score <= 7.0
        assert result.completion_time_estimate_minutes <= 10.0
        assert len(result.complexity_violations) == 0
    
    @pytest.mark.asyncio
    async def test_ui_complexity_validation_high_complexity(self, validator, sample_story_data):
        """Test UI complexity validation with high complexity."""
        # Create complex UI components
        complex_ui_components = [
            {
                "name": "ComplexForm",
                "elements": [{"type": "input"} for _ in range(15)]  # Too many elements
            }
        ]
        
        complex_interaction_flows = [
            {
                "name": "complex_flow",
                "user_actions": [{"description": f"Step {i}"} for i in range(10)],  # Too many steps
                "navigation_depth": 5  # Too deep navigation
            }
        ]
        
        result = await validator._validate_ui_complexity(
            complex_ui_components,
            complex_interaction_flows,
            sample_story_data
        )
        
        assert result.complexity_level in [ComplexityLevel.HIGH, ComplexityLevel.EXCESSIVE]
        assert len(result.complexity_violations) > 0
        assert len(result.recommendations) > 0
    
    @pytest.mark.asyncio
    async def test_learning_flow_validation_excellent(self, validator, sample_interaction_flows, 
                                                    sample_story_data):
        """Test learning flow validation with excellent quality."""
        excellent_game_mechanics = {
            "mechanics": [
                {"engagement_type": "interactive"},
                {"engagement_type": "gamified"},
                {"engagement_type": "collaborative"}
            ],
            "learning_objectives_addressed": [
                "Förstå registreringsprocessen",
                "Lära sig kommunala policyer"
            ],
            "pedagogical_effectiveness_score": 5.0
        }
        
        # Add assessment opportunities
        assessment_flows = sample_interaction_flows + [
            {
                "user_actions": [
                    {"description": "Användaren tar ett test"},
                    {"description": "Användaren får en quiz"}
                ]
            }
        ]
        
        result = await validator._validate_learning_flows(
            excellent_game_mechanics,
            assessment_flows,
            sample_story_data
        )
        
        assert result.flow_quality in [LearningFlowQuality.EXCELLENT, LearningFlowQuality.GOOD]
        assert result.pedagogical_effectiveness_score >= 3.5
        assert result.flow_progression_logical is True
    
    @pytest.mark.asyncio
    async def test_learning_flow_validation_poor(self, validator, sample_story_data):
        """Test learning flow validation with poor quality."""
        poor_game_mechanics = {
            "mechanics": [],  # No mechanics
            "learning_objectives_addressed": [],  # No objectives
            "pedagogical_effectiveness_score": 1.0
        }
        
        poor_interaction_flows = [
            {
                "user_actions": [{"description": "Single action"}]  # Too simple
            }
        ]
        
        result = await validator._validate_learning_flows(
            poor_game_mechanics,
            poor_interaction_flows,
            sample_story_data
        )
        
        assert result.flow_quality in [LearningFlowQuality.POOR, LearningFlowQuality.INADEQUATE]
        assert len(result.learning_violations) > 0
        assert len(result.recommendations) > 0
    
    @pytest.mark.asyncio
    async def test_professional_tone_validation_excellent(self, validator, sample_story_data):
        """Test professional tone validation with excellent tone."""
        professional_ui_components = [
            {
                "elements": [
                    {"text": "Välkommen till kommunens träningssystem"},
                    {"label": "Förvaltning och kvalitet är viktigt"},
                    {"description": "Detta system hjälper medborgare att lära sig policy"}
                ]
            }
        ]
        
        professional_interaction_flows = [
            {
                "user_actions": [
                    {"description": "Användaren navigerar genom verksamheten"},
                    {"feedback_text": "Effektivitet och service är våra prioriteringar"}
                ]
            }
        ]
        
        result = await validator._validate_professional_tone(
            professional_ui_components,
            professional_interaction_flows,
            sample_story_data
        )
        
        assert result.tone_consistency in [ToneConsistency.EXCELLENT, ToneConsistency.GOOD]
        assert result.professional_score >= 3.5
        assert sum(result.municipal_terminology_usage.values()) >= 3
    
    @pytest.mark.asyncio
    async def test_professional_tone_validation_unprofessional(self, validator, sample_story_data):
        """Test professional tone validation with unprofessional tone."""
        unprofessional_ui_components = [
            {
                "elements": [
                    {"text": "Typ, bara fyll i formuläret"},
                    {"label": "Kanske ska du läsa lite grann"},
                    {"description": "Det är ungefär liksom viktigt"}
                ]
            }
        ]
        
        result = await validator._validate_professional_tone(
            unprofessional_ui_components,
            [],
            sample_story_data
        )
        
        assert result.tone_consistency in [ToneConsistency.INCONSISTENT, ToneConsistency.UNPROFESSIONAL]
        assert len(result.tone_violations) > 0
        assert len(result.recommendations) > 0
    
    def test_assess_feature_complexity_simple(self, validator):
        """Test feature complexity assessment for simple features."""
        simple_story_data = {
            "acceptance_criteria": ["Simple criteria"],
            "learning_objectives": ["Single objective"],
            "user_role_complexity": "simple"
        }
        
        complexity = validator._assess_feature_complexity(simple_story_data)
        assert 1.0 <= complexity <= 2.5
    
    def test_assess_feature_complexity_complex(self, validator):
        """Test feature complexity assessment for complex features."""
        complex_story_data = {
            "acceptance_criteria": [f"Criteria {i}" for i in range(8)],  # Many criteria
            "learning_objectives": [f"Objective {i}" for i in range(5)],  # Many objectives
            "integration_requirements": True,
            "custom_business_logic": True,
            "user_role_complexity": "very_complex"
        }
        
        complexity = validator._assess_feature_complexity(complex_story_data)
        assert complexity >= 4.0
    
    @pytest.mark.asyncio
    async def test_dna_validation_score_calculation(self, validator, sample_ui_components,
                                                  sample_interaction_flows, sample_game_mechanics,
                                                  sample_story_data):
        """Test DNA compliance score calculation."""
        result = await validator.validate_ux_dna_compliance(
            sample_game_mechanics,
            sample_ui_components,
            sample_interaction_flows,
            sample_story_data
        )
        
        # Score should be between 1-5
        assert 1.0 <= result.dna_compliance_score <= 5.0
        
        # Score should be calculated from three components
        expected_components = [
            result.ui_complexity_result.cognitive_load_score,
            result.learning_flow_result.pedagogical_effectiveness_score,
            result.professional_tone_result.professional_score
        ]
        
        # All components should contribute to the score
        assert all(component > 0 for component in expected_components)
    
    @pytest.mark.asyncio 
    async def test_dna_validation_with_missing_data(self, validator):
        """Test DNA validation with missing or incomplete data."""
        # Test with empty data
        result = await validator.validate_ux_dna_compliance({}, [], [], {})
        
        # Should still return a result, but with lower scores
        assert isinstance(result, DNAUXValidationResult)
        assert result.dna_compliance_score < 3.0  # Lower score for missing data
    
    def test_validator_configuration(self):
        """Test validator configuration with custom settings."""
        custom_config = {
            "ui_complexity_thresholds": {
                "max_cognitive_load_score": 8.0,
                "max_ui_elements_per_screen": 12
            },
            "learning_flow_criteria": {
                "min_pedagogical_effectiveness": 3.5
            },
            "professional_tone_standards": {
                "min_professional_score": 3.5
            }
        }
        
        validator = DNAUXValidator(config=custom_config)
        
        # Custom thresholds should be preserved
        assert validator.ui_complexity_thresholds["max_cognitive_load_score"] == 8.0
        assert validator.ui_complexity_thresholds["max_ui_elements_per_screen"] == 12
        
        # Other defaults should remain
        assert validator.ui_complexity_thresholds["max_interaction_steps"] == 5
        
        assert validator.learning_flow_criteria["min_pedagogical_effectiveness"] == 3.5
        assert validator.professional_tone_standards["min_professional_score"] == 3.5


if __name__ == "__main__":
    pytest.main([__file__])