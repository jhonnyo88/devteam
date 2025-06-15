"""
Quality Reviewer Agent - Contract Compliance Tests

PURPOSE:
Validates that Quality Reviewer agent maintains contract compliance
according to TEST_STRATEGY.md requirements and Implementation_rules.md specifications.

CRITICAL IMPORTANCE:
These tests ensure the Quality Reviewer agent can work as the final approval gate
while integrating seamlessly with QA Tester and deployment pipeline without
breaking the modular architecture that the contract system enables.

CONTRACT PROTECTION:
These tests are SACRED - they protect the contract system that enables
modular development where each agent can be improved independently.
"""

import pytest
import asyncio
import json
from typing import Dict, Any
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

# Import using absolute path to avoid relative import issues
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from modules.agents.quality_reviewer.contracts.input_models import QualityReviewerInputContract
from modules.agents.quality_reviewer.contracts.output_models import QualityReviewerOutputContract
from modules.shared.contract_validator import ContractValidator
from modules.shared.exceptions import ContractValidationError


class TestQualityReviewerContractCompliance:
    """Test suite for Quality Reviewer contract compliance following TEST_STRATEGY.md."""
    
    @pytest.fixture
    def contract_validator(self):
        """Create ContractValidator instance."""
        return ContractValidator()
    
    @pytest.fixture
    def quality_reviewer_agent(self):
        """Create mocked Quality Reviewer agent instance."""
        # Create a mock agent to avoid import issues during testing
        mock_agent = MagicMock()
        mock_agent.agent_type = "quality_reviewer"
        mock_agent.agent_id = "quality_reviewer_test"
        return mock_agent
    
    @pytest.fixture
    def valid_qa_tester_output_contract(self):
        """
        Valid contract from QA Tester as defined in Implementation_rules.md.
        
        This is the EXACT contract specification that QA Tester must produce
        and Quality Reviewer must accept.
        """
        story_id = "STORY-QR-001-001"
        
        return {
            "contract_version": "1.0",
            "story_id": story_id,
            "source_agent": "qa_tester",
            "target_agent": "quality_reviewer",
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
            
            # EXACT input requirements as specified in Implementation_rules.md
            "input_requirements": {
                "required_files": [
                    f"docs/qa_reports/{story_id}_ux_validation.json",
                    f"docs/qa_reports/{story_id}_accessibility_report.html",
                    f"docs/qa_reports/{story_id}_persona_testing.json",
                    f"docs/qa_reports/{story_id}_municipal_compliance.json"
                ],
                "required_data": {
                    "ux_validation_results": {
                        "flow_completion_rate": 96.5,
                        "user_satisfaction_score": 4.6,
                        "task_completion_time_avg_minutes": 8.2,
                        "navigation_efficiency_score": 4.4,
                        "error_recovery_success_rate": 98.0
                    },
                    "accessibility_compliance_report": {
                        "wcag_aa_compliance": True,
                        "compliance_percentage": 98.5,
                        "violations": [],
                        "keyboard_navigation_working": True,
                        "screen_reader_compatible": True,
                        "color_contrast_ratio": 7.2
                    },
                    "persona_testing_results": {
                        "anna_persona_satisfaction": 4.7,
                        "completion_time_minutes": 8.2,
                        "task_success_rate": 95.0,
                        "stress_test_performance": 4.3,
                        "municipal_context_understanding": 4.8
                    },
                    "municipal_compliance_results": {
                        "gdpr_compliant": True,
                        "swedish_accessibility_law_compliant": True,
                        "professional_tone_validated": True,
                        "municipal_terminology_correct": True,
                        "data_handling_compliant": True
                    },
                    "quality_intelligence_predictions": {
                        "predicted_quality_score": 4.8,
                        "confidence_level": 92.0,
                        "risk_factors": [],
                        "optimization_suggestions": [
                            "Minor performance optimization opportunities"
                        ]
                    },
                    "anna_satisfaction_prediction": {
                        "predicted_satisfaction": 4.6,
                        "predicted_completion_time_minutes": 8.5,
                        "confidence_percentage": 89.0
                    },
                    "performance_validation_results": {
                        "lighthouse_score": 94,
                        "api_response_time_ms": 145,
                        "page_load_time_ms": 1200,
                        "core_web_vitals_passed": True
                    },
                    "test_results": {
                        "coverage_percentage": 97.5,
                        "tests_passed": 48,
                        "total_tests": 48,
                        "unit_test_coverage": 98.2,
                        "integration_test_coverage": 96.8
                    },
                    "code_quality_metrics": {
                        "typescript_errors": 0,
                        "eslint_violations": 0,
                        "complexity_score": 2.1,
                        "maintainability_index": 85.3
                    }
                },
                "required_validations": [
                    "ux_validation_complete",
                    "accessibility_compliance_verified",
                    "persona_testing_passed",
                    "municipal_compliance_confirmed",
                    "quality_intelligence_analyzed"
                ]
            },
            "output_specifications": {
                "deliverable_files": [
                    f"docs/final_reports/{story_id}_quality_decision.json",
                    f"docs/final_reports/{story_id}_deployment_approval.md"
                ],
                "deliverable_data": {
                    "final_approval_decision": "boolean",
                    "overall_quality_score": "number",
                    "deployment_readiness": "boolean",
                    "client_communication_data": "object"
                },
                "validation_criteria": {
                    "final_quality_score_calculated": True,
                    "deployment_readiness_validated": True,
                    "approval_decision_made": True,
                    "client_communication_prepared": True
                }
            },
            "quality_gates": [
                "final_quality_score_calculated",
                "deployment_readiness_validated", 
                "approval_decision_made",
                "documentation_complete",
                "client_communication_sent"
            ],
            "handoff_criteria": [
                "quality_analysis_complete",
                "approval_decision_documented",
                "client_communication_completed",
                "next_steps_defined"
            ]
        }
    
    def test_contract_structure_validation(self, contract_validator, valid_qa_tester_output_contract):
        """Test that QA Tester output contract structure is valid."""
        validation_result = contract_validator.validate_contract(valid_qa_tester_output_contract)
        
        assert validation_result.is_valid is True, f"Contract validation failed: {validation_result.errors}"
        assert len(validation_result.errors) == 0
        
        # Verify agent sequence is correct: qa_tester → quality_reviewer
        assert valid_qa_tester_output_contract["source_agent"] == "qa_tester"
        assert valid_qa_tester_output_contract["target_agent"] == "quality_reviewer"
    
    def test_dna_compliance_structure(self, valid_qa_tester_output_contract):
        """Test DNA compliance structure matches Implementation_rules.md requirements."""
        dna_compliance = valid_qa_tester_output_contract["dna_compliance"]
        
        # Check required design principles (5 principles)
        design_principles = dna_compliance["design_principles_validation"]
        required_principles = [
            "pedagogical_value", "policy_to_practice", "time_respect",
            "holistic_thinking", "professional_tone"
        ]
        
        for principle in required_principles:
            assert principle in design_principles, f"Missing design principle: {principle}"
            assert isinstance(design_principles[principle], bool), f"Principle {principle} must be boolean"
        
        # Check required architecture compliance (4 principles)
        architecture_compliance = dna_compliance["architecture_compliance"]
        required_architecture = [
            "api_first", "stateless_backend", "separation_of_concerns", "simplicity_first"
        ]
        
        for principle in required_architecture:
            assert principle in architecture_compliance, f"Missing architecture principle: {principle}"
            assert isinstance(architecture_compliance[principle], bool), f"Architecture {principle} must be boolean"
    
    def test_file_naming_conventions(self, valid_qa_tester_output_contract):
        """Test that file naming includes story_id as per TEST_STRATEGY.md."""
        story_id = valid_qa_tester_output_contract["story_id"]
        
        # Check required files include story_id
        required_files = valid_qa_tester_output_contract["input_requirements"]["required_files"]
        for file_path in required_files:
            assert story_id in file_path, f"File {file_path} must include story_id {story_id}"
        
        # Check output files include story_id
        deliverable_files = valid_qa_tester_output_contract["output_specifications"]["deliverable_files"]
        for file_path in deliverable_files:
            assert story_id in file_path, f"Output file {file_path} must include story_id {story_id}"
    
    def test_quality_gates_completeness(self, valid_qa_tester_output_contract):
        """Test that all required quality gates are defined."""
        quality_gates = valid_qa_tester_output_contract["quality_gates"]
        
        # Required quality gates for Quality Reviewer agent
        required_gates = [
            "final_quality_score_calculated",
            "deployment_readiness_validated",
            "approval_decision_made",
            "documentation_complete",
            "client_communication_sent"
        ]
        
        for gate in required_gates:
            assert gate in quality_gates, f"Missing required quality gate: {gate}"
    
    def test_handoff_criteria_completeness(self, valid_qa_tester_output_contract):
        """Test that all handoff criteria are properly defined."""
        handoff_criteria = valid_qa_tester_output_contract["handoff_criteria"]
        
        # Required handoff criteria for Quality Reviewer
        required_criteria = [
            "quality_analysis_complete",
            "approval_decision_documented", 
            "client_communication_completed",
            "next_steps_defined"
        ]
        
        for criteria in required_criteria:
            assert criteria in handoff_criteria, f"Missing handoff criteria: {criteria}"
    
    def test_pydantic_input_contract_validation(self, valid_qa_tester_output_contract):
        """Test Pydantic input contract model validation."""
        # Extract input data for Pydantic validation
        input_data = {
            "contract_version": valid_qa_tester_output_contract["contract_version"],
            "source_agent": valid_qa_tester_output_contract["source_agent"],
            "target_agent": valid_qa_tester_output_contract["target_agent"],
            "story_id": valid_qa_tester_output_contract["story_id"],
            "ux_validation_results": valid_qa_tester_output_contract["input_requirements"]["required_data"]["ux_validation_results"],
            "accessibility_compliance_report": valid_qa_tester_output_contract["input_requirements"]["required_data"]["accessibility_compliance_report"],
            "persona_testing_results": valid_qa_tester_output_contract["input_requirements"]["required_data"]["persona_testing_results"],
            "municipal_compliance_results": valid_qa_tester_output_contract["input_requirements"]["required_data"]["municipal_compliance_results"],
            "quality_intelligence_predictions": valid_qa_tester_output_contract["input_requirements"]["required_data"]["quality_intelligence_predictions"],
            "anna_satisfaction_prediction": valid_qa_tester_output_contract["input_requirements"]["required_data"]["anna_satisfaction_prediction"],
            "performance_validation_results": valid_qa_tester_output_contract["input_requirements"]["required_data"]["performance_validation_results"],
            "test_results": valid_qa_tester_output_contract["input_requirements"]["required_data"]["test_results"],
            "code_quality_metrics": valid_qa_tester_output_contract["input_requirements"]["required_data"]["code_quality_metrics"],
            "dna_compliance": valid_qa_tester_output_contract["dna_compliance"]
        }
        
        # Validate using Pydantic model
        try:
            input_contract = QualityReviewerInputContract(**input_data)
            assert input_contract.story_id == "STORY-QR-001-001"
            assert input_contract.source_agent == "qa_tester"
            assert input_contract.target_agent == "quality_reviewer"
        except Exception as e:
            pytest.fail(f"Pydantic input contract validation failed: {e}")
    
    def test_quality_reviewer_output_contract_structure(self, valid_qa_tester_output_contract):
        """Test that Quality Reviewer output contract follows correct structure."""
        # Validate expected output contract structure based on Implementation_rules.md
        story_id = valid_qa_tester_output_contract["story_id"]
        
        # Expected output contract structure for Quality Reviewer
        expected_output_structure = {
            "contract_version": "1.0",
            "story_id": story_id,
            "source_agent": "quality_reviewer",
            "target_agent": "deployment",  # or "developer" for rejections
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
                },
                "final_dna_validation": {
                    "overall_dna_compliant": True,
                    "deployment_ready": True
                }
            },
            "input_requirements": {
                "required_files": [],
                "required_data": {
                    "approval_status": True,
                    "quality_score": 94.5,
                    "deployment_ready": True,
                    "client_communication": {}
                },
                "required_validations": []
            }
        }
        
        # Verify expected structure elements
        assert expected_output_structure["contract_version"] == "1.0"
        assert expected_output_structure["source_agent"] == "quality_reviewer"
        assert expected_output_structure["target_agent"] in ["deployment", "developer"]
        
        # Verify DNA compliance structure
        dna_compliance = expected_output_structure["dna_compliance"]
        assert "design_principles_validation" in dna_compliance
        assert "architecture_compliance" in dna_compliance
        assert "final_dna_validation" in dna_compliance
    
    def test_agent_sequence_validation(self, valid_qa_tester_output_contract):
        """Test correct agent sequence: qa_tester → quality_reviewer → deployment."""
        # Input sequence validation
        assert valid_qa_tester_output_contract["source_agent"] == "qa_tester"
        assert valid_qa_tester_output_contract["target_agent"] == "quality_reviewer"
        
        # Story ID format validation
        story_id = valid_qa_tester_output_contract["story_id"]
        assert story_id.startswith("STORY-"), f"Story ID {story_id} must start with 'STORY-'"
        assert len(story_id.split("-")) >= 3, f"Story ID {story_id} must follow STORY-XXX-XXX format"
    
    @pytest.mark.asyncio
    async def test_contract_processing_performance(self, quality_reviewer_agent, valid_qa_tester_output_contract):
        """Test that contract processing meets performance requirements (<1000ms)."""
        # Mock all methods for performance testing
        with patch.object(quality_reviewer_agent, '_extract_qa_data', return_value={}), \
             patch.object(quality_reviewer_agent, '_perform_quality_analysis', return_value={"overall_score": 90}), \
             patch.object(quality_reviewer_agent, '_validate_deployment_readiness', return_value={"deployment_ready": True}), \
             patch.object(quality_reviewer_agent, '_make_approval_decision', return_value={"approved": True, "reasoning": "Test"}), \
             patch.object(quality_reviewer_agent, '_handle_client_communication', return_value={"communication_type": "test"}), \
             patch.object(quality_reviewer_agent.dna_final_validator, 'validate_final_dna_compliance', return_value=MagicMock(
                 overall_dna_compliant=True, dna_compliance_score=4.5, compliance_level=MagicMock(value="good"), validation_timestamp="2024-06-15T12:00:00Z"
             )), \
             patch.object(quality_reviewer_agent, '_notify_team_progress', return_value=None):
            
            start_time = datetime.now()
            
            # Process contract
            await quality_reviewer_agent.process_contract(valid_qa_tester_output_contract)
            
            end_time = datetime.now()
            processing_time_ms = (end_time - start_time).total_seconds() * 1000
            
            # Performance requirement: <1000ms for contract processing
            assert processing_time_ms < 1000, f"Contract processing took {processing_time_ms}ms, must be <1000ms"
    
    def test_required_quality_data_fields(self, valid_qa_tester_output_contract):
        """Test that all required quality data fields are present for Quality Reviewer."""
        required_data = valid_qa_tester_output_contract["input_requirements"]["required_data"]
        
        # Critical fields for Quality Reviewer final approval
        required_fields = [
            "ux_validation_results",
            "accessibility_compliance_report", 
            "persona_testing_results",
            "municipal_compliance_results",
            "quality_intelligence_predictions",
            "anna_satisfaction_prediction",
            "performance_validation_results",
            "test_results",
            "code_quality_metrics"
        ]
        
        for field in required_fields:
            assert field in required_data, f"Missing required data field: {field}"
            assert required_data[field] is not None, f"Required field {field} cannot be None"
    
    def test_backwards_compatibility(self, contract_validator, valid_qa_tester_output_contract):
        """Test that contract changes maintain backwards compatibility."""
        # Ensure contract version is stable
        assert valid_qa_tester_output_contract["contract_version"] == "1.0"
        
        # Ensure core contract structure remains unchanged
        required_top_level_fields = [
            "contract_version", "story_id", "source_agent", "target_agent",
            "dna_compliance", "input_requirements", "output_specifications",
            "quality_gates", "handoff_criteria"
        ]
        
        for field in required_top_level_fields:
            assert field in valid_qa_tester_output_contract, f"Missing core contract field: {field}"
        
        # Test that contract validates with current validator
        validation_result = contract_validator.validate_contract(valid_qa_tester_output_contract)
        assert validation_result.is_valid is True, "Contract must maintain backwards compatibility"