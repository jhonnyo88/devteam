"""
Design Principles Tests

Tests validation of DigiNativa's 5 core design principles that guide all
feature development decisions:

1. pedagogical_value - Clear learning objectives and educational value
2. policy_to_practice - Direct connection between policy and practical application  
3. time_respect - Respects user time (d10 minutes per learning session)
4. holistic_thinking - Comprehensive approach to problem-solving
5. professional_tone - Maintains professional municipal communication standards

These principles ensure every feature delivers value to Swedish municipal users.
"""

import pytest
import time
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, patch
from datetime import datetime

from modules.shared.exceptions import DNAComplianceError, ValidationError
from modules.shared.design_principles_validator import (
    DesignPrinciplesValidator,
    PedagogicalValueResult,
    PolicyToPracticeResult,
    TimeRespectResult,
    HolisticThinkingResult,
    ProfessionalToneResult
)


class TestDesignPrinciples:
    """Test design principles validation."""
    
    @pytest.fixture
    def validator(self):
        """Create design principles validator."""
        return DesignPrinciplesValidator()

    @pytest.fixture
    def anna_persona_data(self):
        """Sample data for Anna persona - primary municipal user."""
        return {
            "name": "Anna",
            "role": "Municipal Administrator",
            "experience_level": "intermediate",
            "time_constraints": {
                "available_minutes_per_session": 10,
                "interruption_frequency": "high",
                "task_switching_common": True
            },
            "learning_preferences": {
                "practical_application": True,
                "immediate_feedback": True,
                "real_world_scenarios": True,
                "professional_context": True
            },
            "work_context": {
                "municipal_sector": True,
                "policy_implementation": True,
                "citizen_services": True,
                "administrative_tasks": True
            }
        }

    @pytest.fixture
    def excellent_pedagogical_feature(self):
        """Feature with excellent pedagogical value."""
        return {
            "feature_description": """
            Interactive Policy Decision Trainer for Municipal Administrators
            
            This feature helps Anna practice complex policy decisions through realistic 
            scenarios. Each scenario presents a real municipal situation where policy 
            knowledge must be applied to serve citizens effectively.
            
            Anna will navigate through decision trees, receive immediate feedback on 
            her choices, and learn from expert explanations of optimal approaches.
            """,
            "learning_objectives": [
                "Apply municipal policy knowledge to real citizen service situations",
                "Develop confidence in policy interpretation under time pressure", 
                "Practice ethical decision-making in public sector context",
                "Understand the impact of administrative decisions on citizens",
                "Build skills in balancing policy compliance with practical solutions"
            ],
            "assessment_methods": [
                "Scenario-based decision making",
                "Immediate feedback with explanations", 
                "Progress tracking across multiple scenarios",
                "Self-reflection prompts after decisions",
                "Knowledge retention quizzes"
            ],
            "skill_development_areas": [
                "Critical thinking in policy context",
                "Ethical reasoning in public service",
                "Time-efficient decision making",
                "Citizen-centered service delivery",
                "Professional communication"
            ],
            "practical_application": True,
            "real_world_relevance": True,
            "measurable_outcomes": True,
            "adaptive_difficulty": True
        }

    @pytest.fixture
    def excellent_policy_practice_feature(self):
        """Feature with excellent policy-to-practice connection."""
        return {
            "feature_description": """
            Municipal Policy Implementation Simulator
            
            Transform abstract policy documents into practical action guides. 
            Anna learns by doing - implementing actual municipal policies through 
            simulated citizen interactions and administrative scenarios.
            """,
            "policy_connections": [
                {
                    "policy_document": "Municipal Service Standards Act",
                    "practical_application": "Handling citizen complaints within 24-hour requirement",
                    "real_world_scenario": "Citizen reports streetlight outage affecting safety"
                },
                {
                    "policy_document": "Public Information Access Regulations", 
                    "practical_application": "Processing information requests while protecting privacy",
                    "real_world_scenario": "Journalist requests citizen data for public interest story"
                }
            ],
            "theory_to_practice_mapping": {
                "abstract_concepts": ["Service standards", "Privacy protection", "Response times"],
                "concrete_actions": ["Log complaint", "Schedule repair", "Notify citizen", "Document process"],
                "decision_points": ["Urgency assessment", "Resource allocation", "Communication timing"],
                "real_world_constraints": ["Budget limits", "Staff availability", "Legal requirements"]
            },
            "scenario_based_learning": True,
            "immediate_application": True,
            "contextual_learning": True,
            "bridges_theory_practice": True
        }

    @pytest.fixture
    def excellent_time_respect_feature(self):
        """Feature with excellent time respect."""
        return {
            "feature_description": """
            Quick Decision Support for Busy Municipal Staff
            
            Designed specifically for Anna's hectic work environment with frequent 
            interruptions. Each learning module completes in under 8 minutes with 
            clear progress saves and resume functionality.
            """,
            "time_design": {
                "target_completion_minutes": 8,
                "maximum_completion_minutes": 10,
                "session_breaks_allowed": True,
                "progress_saving": "automatic_every_30_seconds",
                "resume_capability": True,
                "interruption_recovery": "seamless"
            },
            "efficiency_features": [
                "One-click scenario selection",
                "Pre-loaded context to skip setup",
                "Smart defaults to reduce clicking",
                "Keyboard shortcuts for power users",
                "Mobile-optimized for quick access"
            ],
            "cognitive_load_management": {
                "information_chunking": "small_digestible_pieces",
                "visual_hierarchy": "clear_priority_indicators",
                "decision_support": "contextual_hints_available",
                "complexity_progression": "gradual_increase",
                "mental_model_building": "consistent_patterns"
            },
            "respect_user_constraints": True,
            "optimized_for_interruptions": True,
            "efficient_interaction_design": True
        }

    @pytest.fixture
    def excellent_holistic_feature(self):
        """Feature with excellent holistic thinking."""
        return {
            "feature_description": """
            Municipal Decision Impact Analyzer
            
            Helps Anna understand how individual decisions connect to broader 
            organizational goals, citizen outcomes, and municipal effectiveness.
            Each scenario shows ripple effects across departments and stakeholders.
            """,
            "holistic_elements": {
                "stakeholder_perspectives": [
                    "Citizens receiving service",
                    "Municipal colleagues in other departments", 
                    "City council and elected officials",
                    "Budget and resource managers",
                    "Legal and compliance teams"
                ],
                "system_connections": [
                    "Impact on department performance metrics",
                    "Effect on citizen satisfaction scores",
                    "Resource allocation implications",
                    "Legal and regulatory compliance",
                    "Long-term organizational reputation"
                ],
                "broader_context_integration": [
                    "Municipal strategic goals alignment",
                    "Community development objectives",
                    "Intergovernmental coordination needs",
                    "Public trust and transparency",
                    "Sustainable service delivery"
                ]
            },
            "systems_thinking_approach": True,
            "multiple_perspective_consideration": True,
            "long_term_impact_awareness": True,
            "organizational_goal_alignment": True,
            "comprehensive_problem_solving": True
        }

    @pytest.fixture
    def excellent_professional_tone_feature(self):
        """Feature with excellent professional tone."""
        return {
            "feature_description": """
            Professional Communication Excellence for Municipal Staff
            
            Develops Anna's skills in maintaining appropriate professional tone 
            across all municipal communications, from citizen interactions to 
            interdepartmental collaboration.
            """,
            "communication_standards": {
                "tone_characteristics": [
                    "Respectful and courteous",
                    "Clear and precise",
                    "Authoritative yet approachable", 
                    "Culturally sensitive",
                    "Solution-oriented"
                ],
                "language_guidelines": [
                    "Use Swedish municipal terminology correctly",
                    "Avoid jargon when communicating with citizens",
                    "Maintain formal register in official documents",
                    "Show empathy while maintaining boundaries",
                    "Be concise while being complete"
                ],
                "context_appropriateness": [
                    "Citizen service interactions",
                    "Internal departmental communication",
                    "Official document preparation",
                    "Crisis communication protocols",
                    "Media and public relations"
                ]
            },
            "municipal_terminology_usage": {
                "administrative_terms": ["förvaltning", "verksamhet", "medborgare"],
                "policy_terms": ["riktlinjer", "föreskrifter", "tillämpning"],
                "service_terms": ["service", "kvalitet", "effektivitet"],
                "procedural_terms": ["process", "rutin", "dokumentation"]
            },
            "professional_communication_training": True,
            "municipal_context_appropriate": True,
            "respectful_citizen_focus": True,
            "clear_professional_standards": True
        }

    # ================================================
    # PEDAGOGICAL VALUE TESTS
    # ================================================

    def test_pedagogical_value_excellent(self, validator, excellent_pedagogical_feature):
        """Test pedagogical value validation with excellent content."""
        
        result = validator.validate_pedagogical_value(excellent_pedagogical_feature)
        
        assert isinstance(result, PedagogicalValueResult)
        assert result.compliant is True
        assert result.score >= 4.5
        assert len(result.violations) == 0
        
        # Verify specific criteria met
        assert result.has_clear_learning_objectives
        assert result.provides_skill_development
        assert result.includes_assessment_methods
        assert result.enables_practical_application
        assert result.measurable_learning_outcomes
        assert result.adaptive_to_learner_needs
        
        print(f" Excellent pedagogical value: {result.score:.1f}/5.0")

    def test_pedagogical_value_poor(self, validator):
        """Test pedagogical value validation with poor content."""
        
        poor_feature = {
            "feature_description": "Add a button to submit forms",
            "learning_objectives": [],  # No learning objectives
            "assessment_methods": [],   # No assessment
            "skill_development_areas": [],  # No skill development
            "practical_application": False,
            "real_world_relevance": False,
            "measurable_outcomes": False
        }
        
        result = validator.validate_pedagogical_value(poor_feature)
        
        assert result.compliant is False
        assert result.score <= 2.0
        assert len(result.violations) > 0
        
        # Verify specific failures
        assert not result.has_clear_learning_objectives
        assert not result.provides_skill_development
        assert not result.enables_practical_application
        
        violation_types = [v.violation_type for v in result.violations]
        assert "missing_learning_objectives" in violation_types
        assert "no_skill_development" in violation_types
        
        print(f" Poor pedagogical value rejected: {result.score:.1f}/5.0")

    def test_pedagogical_value_municipal_context(self, validator):
        """Test pedagogical value specifically for municipal context."""
        
        municipal_feature = {
            "feature_description": "Municipal policy application training",
            "learning_objectives": [
                "Apply municipal regulations to citizen services",
                "Navigate complex administrative procedures",
                "Balance policy compliance with citizen needs"
            ],
            "municipal_context": True,
            "citizen_service_focus": True,
            "policy_implementation_skills": True,
            "administrative_competence": True,
            "public_sector_ethics": True
        }
        
        result = validator.validate_pedagogical_value(municipal_feature)
        
        assert result.compliant is True
        assert result.municipal_context_relevant is True
        assert result.public_sector_appropriate is True
        assert result.citizen_service_focused is True
        
        print(f" Municipal context pedagogical value: {result.score:.1f}/5.0")

    # ================================================
    # POLICY-TO-PRACTICE TESTS  
    # ================================================

    def test_policy_to_practice_excellent(self, validator, excellent_policy_practice_feature):
        """Test policy-to-practice validation with excellent connection."""
        
        result = validator.validate_policy_to_practice(excellent_policy_practice_feature)
        
        assert isinstance(result, PolicyToPracticeResult)
        assert result.compliant is True
        assert result.score >= 4.5
        assert len(result.violations) == 0
        
        # Verify specific criteria met
        assert result.connects_theory_to_practice
        assert result.provides_real_world_scenarios
        assert result.bridges_abstract_concrete
        assert result.enables_immediate_application
        assert result.contextual_policy_application
        assert result.practical_decision_support
        
        print(f" Excellent policy-to-practice: {result.score:.1f}/5.0")

    def test_policy_to_practice_theoretical_only(self, validator):
        """Test policy-to-practice validation with only theoretical content."""
        
        theoretical_feature = {
            "feature_description": "Display municipal policy documents for reading",
            "policy_connections": [
                {
                    "policy_document": "Municipal Act",
                    "practical_application": None,  # No practical application
                    "real_world_scenario": None     # No scenarios
                }
            ],
            "theory_to_practice_mapping": {},  # Empty mapping
            "scenario_based_learning": False,
            "immediate_application": False,
            "bridges_theory_practice": False
        }
        
        result = validator.validate_policy_to_practice(theoretical_feature)
        
        assert result.compliant is False
        assert result.score <= 2.0
        assert len(result.violations) > 0
        
        # Verify specific failures
        assert not result.provides_real_world_scenarios
        assert not result.enables_immediate_application
        assert not result.bridges_abstract_concrete
        
        violation_types = [v.violation_type for v in result.violations]
        assert "theoretical_only" in violation_types
        assert "missing_practical_application" in violation_types
        
        print(f" Theoretical-only content rejected: {result.score:.1f}/5.0")

    def test_policy_to_practice_municipal_policies(self, validator):
        """Test policy-to-practice with actual municipal policies."""
        
        municipal_policy_feature = {
            "feature_description": "Municipal policy implementation training",
            "policy_connections": [
                {
                    "policy_document": "Kommunallagen (Municipal Act)",
                    "practical_application": "Citizen service delivery standards",
                    "real_world_scenario": "Handling citizen complaint about service delay"
                },
                {
                    "policy_document": "Offentlighets- och sekretesslagen (Public Access Act)",
                    "practical_application": "Information request processing",
                    "real_world_scenario": "Balancing transparency with privacy protection"
                }
            ],
            "swedish_municipal_context": True,
            "legal_framework_application": True,
            "citizen_rights_focus": True,
            "administrative_procedure_training": True
        }
        
        result = validator.validate_policy_to_practice(municipal_policy_feature)
        
        assert result.compliant is True
        assert result.municipal_policy_relevant is True
        assert result.legal_framework_connection is True
        assert result.citizen_rights_consideration is True
        
        print(f" Municipal policy-to-practice: {result.score:.1f}/5.0")

    # ================================================
    # TIME RESPECT TESTS
    # ================================================

    def test_time_respect_excellent(self, validator, excellent_time_respect_feature, anna_persona_data):
        """Test time respect validation with excellent time design."""
        
        combined_data = {**excellent_time_respect_feature, "user_persona": anna_persona_data}
        result = validator.validate_time_respect(combined_data)
        
        assert isinstance(result, TimeRespectResult)
        assert result.compliant is True
        assert result.score >= 4.5
        assert len(result.violations) == 0
        
        # Verify specific criteria met
        assert result.within_time_constraint
        assert result.respects_user_interruptions
        assert result.efficient_interaction_design
        assert result.minimal_cognitive_load
        assert result.optimized_for_busy_users
        assert result.progress_preservation
        
        # Verify specific time metrics
        assert result.estimated_completion_time <= 10
        assert result.target_completion_time <= 8
        assert result.interruption_recovery_time < 30  # seconds
        
        print(f" Excellent time respect: {result.score:.1f}/5.0")

    def test_time_respect_excessive_time(self, validator, anna_persona_data):
        """Test time respect validation with excessive time requirements."""
        
        time_excessive_feature = {
            "feature_description": "Comprehensive municipal law course with 45-minute modules",
            "time_design": {
                "target_completion_minutes": 45,  # Far exceeds limit
                "maximum_completion_minutes": 60,
                "session_breaks_allowed": False,  # No interruption support
                "progress_saving": "manual_only",
                "resume_capability": False
            },
            "efficiency_features": [],  # No efficiency considerations
            "cognitive_load_management": {
                "information_chunking": "large_dense_blocks",
                "complexity_progression": "immediate_high_complexity"
            },
            "user_persona": anna_persona_data,
            "respect_user_constraints": False,
            "optimized_for_interruptions": False
        }
        
        result = validator.validate_time_respect(time_excessive_feature)
        
        assert result.compliant is False
        assert result.score <= 2.0
        assert len(result.violations) > 0
        
        # Verify specific failures
        assert not result.within_time_constraint
        assert not result.respects_user_interruptions
        assert not result.optimized_for_busy_users
        
        # Verify time constraint violations
        assert result.estimated_completion_time > 10
        
        violation_types = [v.violation_type for v in result.violations]
        assert "time_constraint_exceeded" in violation_types
        assert "poor_interruption_support" in violation_types
        
        print(f" Excessive time requirements rejected: {result.score:.1f}/5.0")

    def test_time_respect_anna_persona_specific(self, validator, anna_persona_data):
        """Test time respect validation specifically for Anna's constraints."""
        
        anna_optimized_feature = {
            "feature_description": "Quick policy guidance for busy administrators",
            "time_design": {
                "target_completion_minutes": 5,  # Well within limits
                "interruption_friendly": True,
                "mobile_optimized": True,  # For Anna's on-the-go work
                "quick_resume": True
            },
            "anna_specific_optimizations": {
                "administrative_task_integration": True,
                "citizen_service_context": True,
                "multitasking_support": True,
                "emergency_mode_available": True  # For urgent situations
            },
            "user_persona": anna_persona_data,
            "municipal_work_context": True
        }
        
        result = validator.validate_time_respect(anna_optimized_feature)
        
        assert result.compliant is True
        assert result.persona_specific_optimization is True
        assert result.work_context_appropriate is True
        assert result.emergency_use_supported is True
        
        print(f" Anna-optimized time respect: {result.score:.1f}/5.0")

    # ================================================
    # HOLISTIC THINKING TESTS
    # ================================================

    def test_holistic_thinking_excellent(self, validator, excellent_holistic_feature):
        """Test holistic thinking validation with excellent systems approach."""
        
        result = validator.validate_holistic_thinking(excellent_holistic_feature)
        
        assert isinstance(result, HolisticThinkingResult)
        assert result.compliant is True
        assert result.score >= 4.5
        assert len(result.violations) == 0
        
        # Verify specific criteria met
        assert result.considers_multiple_perspectives
        assert result.addresses_system_connections
        assert result.integrates_broader_context
        assert result.shows_long_term_thinking
        assert result.connects_to_organizational_goals
        assert result.demonstrates_systems_thinking
        
        # Verify stakeholder consideration
        stakeholders = result.stakeholders_considered
        assert "citizens" in stakeholders
        assert "colleagues" in stakeholders
        assert "management" in stakeholders
        
        print(f" Excellent holistic thinking: {result.score:.1f}/5.0")

    def test_holistic_thinking_narrow_focus(self, validator):
        """Test holistic thinking validation with narrow, isolated focus."""
        
        narrow_feature = {
            "feature_description": "Form field validation for single input",
            "holistic_elements": {
                "stakeholder_perspectives": [],  # No stakeholder consideration
                "system_connections": [],        # No system thinking
                "broader_context_integration": []  # No broader context
            },
            "systems_thinking_approach": False,
            "multiple_perspective_consideration": False,
            "organizational_goal_alignment": False,
            "isolated_solution": True,
            "narrow_scope": True
        }
        
        result = validator.validate_holistic_thinking(narrow_feature)
        
        assert result.compliant is False
        assert result.score <= 2.0
        assert len(result.violations) > 0
        
        # Verify specific failures
        assert not result.considers_multiple_perspectives
        assert not result.addresses_system_connections
        assert not result.integrates_broader_context
        
        violation_types = [v.violation_type for v in result.violations]
        assert "narrow_focus" in violation_types
        assert "missing_stakeholder_consideration" in violation_types
        assert "no_systems_thinking" in violation_types
        
        print(f" Narrow focus rejected: {result.score:.1f}/5.0")

    def test_holistic_thinking_municipal_ecosystem(self, validator):
        """Test holistic thinking in municipal ecosystem context."""
        
        municipal_ecosystem_feature = {
            "feature_description": "Municipal decision support considering full ecosystem",
            "holistic_elements": {
                "stakeholder_perspectives": [
                    "Citizens and residents",
                    "Municipal employees across departments",
                    "Elected officials and council members",
                    "Regional and national government",
                    "Local businesses and organizations",
                    "Community groups and NGOs"
                ],
                "system_connections": [
                    "Interdepartmental workflow impacts",
                    "Budget and resource allocation effects",
                    "Legal and regulatory compliance",
                    "Public trust and transparency",
                    "Long-term community development",
                    "Environmental and sustainability goals"
                ]
            },
            "municipal_ecosystem_awareness": True,
            "cross_departmental_thinking": True,
            "community_impact_consideration": True,
            "sustainability_mindset": True
        }
        
        result = validator.validate_holistic_thinking(municipal_ecosystem_feature)
        
        assert result.compliant is True
        assert result.municipal_ecosystem_awareness is True
        assert result.cross_departmental_perspective is True
        assert result.community_impact_consideration is True
        
        print(f" Municipal ecosystem holistic thinking: {result.score:.1f}/5.0")

    # ================================================
    # PROFESSIONAL TONE TESTS
    # ================================================

    def test_professional_tone_excellent(self, validator, excellent_professional_tone_feature):
        """Test professional tone validation with excellent municipal communication."""
        
        result = validator.validate_professional_tone(excellent_professional_tone_feature)
        
        assert isinstance(result, ProfessionalToneResult)
        assert result.compliant is True
        assert result.score >= 4.5
        assert len(result.violations) == 0
        
        # Verify specific criteria met
        assert result.maintains_professional_language
        assert result.appropriate_for_municipal_context
        assert result.uses_correct_terminology
        assert result.respectful_and_clear
        assert result.culturally_sensitive
        assert result.authority_balanced_with_approachability
        
        # Verify Swedish municipal terminology usage
        terminology = result.municipal_terminology_usage
        assert terminology["administrative_terms"] > 0
        assert terminology["policy_terms"] > 0
        assert terminology["service_terms"] > 0
        
        print(f" Excellent professional tone: {result.score:.1f}/5.0")

    def test_professional_tone_inappropriate(self, validator):
        """Test professional tone validation with inappropriate casual language."""
        
        inappropriate_feature = {
            "feature_description": "Awesome app that's gonna help users big time!",
            "communication_standards": {
                "tone_characteristics": [
                    "Super casual and fun",
                    "Uses lots of slang",
                    "Overly familiar with users"
                ],
                "language_guidelines": [
                    "Use casual speech patterns",
                    "Include internet slang and abbreviations",
                    "Be super informal in all contexts"
                ]
            },
            "sample_user_interface_text": [
                "Hey there, buddy! Ready to rock this?",
                "Oops! Something went totally wrong LOL",
                "You're crushing it! Keep going!",
                "No worries, we'll figure this out together"
            ],
            "municipal_terminology_usage": {},  # No proper terminology
            "professional_communication_training": False,
            "municipal_context_appropriate": False,
            "respectful_citizen_focus": False
        }
        
        result = validator.validate_professional_tone(inappropriate_feature)
        
        assert result.compliant is False
        assert result.score <= 2.0
        assert len(result.violations) > 0
        
        # Verify specific failures
        assert not result.maintains_professional_language
        assert not result.appropriate_for_municipal_context
        assert not result.respectful_and_clear
        
        violation_types = [v.violation_type for v in result.violations]
        assert "inappropriate_casual_language" in violation_types
        assert "missing_municipal_terminology" in violation_types
        assert "unprofessional_tone" in violation_types
        
        print(f" Inappropriate tone rejected: {result.score:.1f}/5.0")

    def test_professional_tone_swedish_municipal_context(self, validator):
        """Test professional tone specifically for Swedish municipal context."""
        
        swedish_municipal_feature = {
            "feature_description": "Professionell kommunikation för kommunal förvaltning",
            "communication_standards": {
                "tone_characteristics": [
                    "Respektfull och korrekt",
                    "Tydlig och precis",
                    "Serviceinriktad men professionell",
                    "Kulturellt medveten",
                    "Lösningsorienterad"
                ],
                "swedish_municipal_context": True,
                "citizen_service_excellence": True,
                "administrative_professionalism": True
            },
            "municipal_terminology_usage": {
                "administrative_terms": ["förvaltning", "verksamhet", "administration", "tjänsteman"],
                "policy_terms": ["policy", "riktlinjer", "föreskrifter", "tillämpning"],
                "service_terms": ["service", "kvalitet", "effektivitet", "medborgare"],
                "procedural_terms": ["process", "rutin", "handläggning", "dokumentation"]
            },
            "swedish_language_proficiency": True,
            "cultural_appropriateness": True,
            "government_communication_standards": True
        }
        
        result = validator.validate_professional_tone(swedish_municipal_feature)
        
        assert result.compliant is True
        assert result.swedish_municipal_appropriate is True
        assert result.government_standards_compliant is True
        assert result.cultural_sensitivity_demonstrated is True
        
        # Verify specific Swedish terminology recognition
        terminology = result.municipal_terminology_usage
        assert terminology["administrative_terms"] >= 4
        assert terminology["policy_terms"] >= 4
        assert terminology["service_terms"] >= 4
        
        print(f" Swedish municipal professional tone: {result.score:.1f}/5.0")

    # ================================================
    # INTEGRATION AND PERFORMANCE TESTS
    # ================================================

    def test_design_principles_comprehensive_validation(self, validator, excellent_pedagogical_feature, 
                                                       excellent_policy_practice_feature,
                                                       excellent_time_respect_feature,
                                                       excellent_holistic_feature,
                                                       excellent_professional_tone_feature):
        """Test comprehensive validation of all design principles together."""
        
        comprehensive_feature = {
            **excellent_pedagogical_feature,
            **excellent_policy_practice_feature,
            **excellent_time_respect_feature,
            **excellent_holistic_feature,
            **excellent_professional_tone_feature
        }
        
        results = validator.validate_all_design_principles(comprehensive_feature)
        
        # Verify all principles pass
        assert results["pedagogical_value"].compliant is True
        assert results["policy_to_practice"].compliant is True
        assert results["time_respect"].compliant is True
        assert results["holistic_thinking"].compliant is True
        assert results["professional_tone"].compliant is True
        
        # Verify overall excellent scores
        overall_score = sum(r.score for r in results.values()) / len(results)
        assert overall_score >= 4.5
        
        print(f" Comprehensive design principles validation: {overall_score:.1f}/5.0")

    def test_design_principles_validation_performance(self, validator, excellent_pedagogical_feature):
        """Test design principles validation performance."""
        
        start_time = time.time()
        
        # Run validation multiple times
        for _ in range(20):
            result = validator.validate_pedagogical_value(excellent_pedagogical_feature)
            assert result.compliant is True
        
        total_time = time.time() - start_time
        avg_time = total_time / 20
        
        # Should be fast
        assert avg_time < 0.1, f"Validation too slow: {avg_time:.3f}s average"
        assert total_time < 2.0, f"Total time too slow: {total_time:.3f}s"
        
        print(f" Validation performance: {avg_time:.3f}s average")

    def test_design_principles_error_handling(self, validator):
        """Test design principles validation error handling."""
        
        # Test with None data
        try:
            result = validator.validate_pedagogical_value(None)
            assert result.compliant is False
            print("    None data handled gracefully")
        except Exception as e:
            assert "data" in str(e).lower() or "none" in str(e).lower()
            print("    None data error informative")
        
        # Test with empty data
        result = validator.validate_pedagogical_value({})
        assert result.compliant is False
        assert result.score < 3.0
        print("    Empty data handled gracefully")
        
        # Test with malformed data
        malformed_data = {
            "feature_description": None,
            "learning_objectives": "not_a_list",
            "time_constraint_minutes": "not_a_number"
        }
        
        result = validator.validate_time_respect(malformed_data)
        assert result.compliant is False
        print("    Malformed data handled gracefully")
        
        print(" Error handling working correctly")


# Design principles benchmarks
DESIGN_PRINCIPLES_BENCHMARKS = {
    "minimum_score_per_principle": 3.5,  # Minimum passing score
    "target_score_per_principle": 4.0,   # Target quality score
    "excellent_score_per_principle": 4.5, # Excellent quality score
    "max_validation_time_per_principle": 0.1,  # 100ms max per principle
    "required_principles_count": 5,      # All 5 principles required
    "principle_weights": {               # Weighting for overall score
        "pedagogical_value": 0.25,       # 25%
        "policy_to_practice": 0.25,      # 25%
        "time_respect": 0.20,            # 20%
        "holistic_thinking": 0.15,       # 15%
        "professional_tone": 0.15        # 15%
    }
}


if __name__ == "__main__":
    # Run with: pytest tests/dna_compliance/test_design_principles.py -v
    pytest.main([__file__, "-v", "--tb=short"])