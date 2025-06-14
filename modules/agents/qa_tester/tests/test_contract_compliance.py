"""
Contract compliance tests for QA Tester agent.

PURPOSE:
Validates that QA Tester agent strictly follows the contract specifications
defined in Implementation_rules.md to ensure modular architecture integrity.

CRITICAL IMPORTANCE:
This test ensures that QA Tester can work completely independently while
still integrating seamlessly with Test Engineer and Quality Reviewer agents.

CONTRACT PROTECTION:
These tests are SACRED - they protect the contract system that enables
modular development where each agent can be improved independently.
"""

import pytest
import asyncio
import json
from datetime import datetime

# Import the agent and contract models
from ..agent import QATesterAgent
from ..contracts.input_models import parse_qa_tester_input_contract
from ...shared.contract_validator import ContractValidator, ContractValidationError


class TestQATesterContractCompliance:
    """Test suite for QA Tester contract compliance."""
    
    @pytest.fixture
    def contract_validator(self):
        """Create ContractValidator instance."""
        return ContractValidator()
    
    @pytest.fixture
    def qa_tester_agent(self):
        """Create QA Tester agent instance with AI config for testing."""
        # Use in-memory database for testing to avoid file system dependencies
        config = {
            "ai_config": {
                "db_path": ":memory:",
                "learning_enabled": True,
                "confidence_threshold": 70.0
            }
        }
        return QATesterAgent(config=config)
    
    @pytest.fixture
    def valid_test_engineer_output_contract(self):
        """
        Valid contract from Test Engineer as defined in Implementation_rules.md.
        
        This is the EXACT contract specification that Test Engineer must produce
        and QA Tester must accept.
        """
        story_id = "STORY-001-001"
        
        return {
            "contract_version": "1.0",
            "story_id": story_id,
            "source_agent": "test_engineer",
            "target_agent": "qa_tester",
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
                    f"tests/unit/{story_id}/",
                    f"tests/integration/{story_id}/",
                    f"tests/e2e/{story_id}/",
                    f"docs/test_reports/{story_id}_coverage.html"
                ],
                "required_data": {
                    "test_suite": {
                        "unit_tests": [
                            {
                                "test_id": "unit_001",
                                "test_name": "Test Component Rendering",
                                "test_type": "unit",
                                "status": "passed",
                                "execution_time_ms": 150.0,
                                "coverage_percentage": 95.0
                            }
                        ],
                        "integration_tests": [
                            {
                                "test_id": "integration_001",
                                "test_name": "Test API Integration",
                                "test_type": "integration",
                                "status": "passed",
                                "execution_time_ms": 500.0,
                                "coverage_percentage": 90.0
                            }
                        ],
                        "e2e_tests": [
                            {
                                "test_id": "e2e_001",
                                "test_name": "Test User Flow",
                                "test_type": "e2e",
                                "status": "passed",
                                "execution_time_ms": 2000.0,
                                "coverage_percentage": 85.0
                            }
                        ]
                    },
                    "performance_results": {
                        "lighthouse_score": 95.0,
                        "api_response_time_ms": 150.0,
                        "page_load_time_ms": 2000.0,
                        "time_to_interactive_ms": 2500.0,
                        "first_contentful_paint_ms": 1000.0,
                        "largest_contentful_paint_ms": 1500.0,
                        "cumulative_layout_shift": 0.05,
                        "bundle_size_kb": 400.0,
                        "memory_usage_mb": 50.0,
                        "cpu_usage_percentage": 15.0
                    },
                    "coverage_report": {
                        "total_coverage": 100.0,
                        "line_coverage": 100.0,
                        "branch_coverage": 95.0,
                        "function_coverage": 100.0
                    },
                    "implementation_data": {
                        "implementation_id": "impl_001",
                        "story_id": story_id,
                        "ui_components": [
                            {
                                "component_id": "test-button",
                                "component_type": "button",
                                "properties": {"text": "Submit"},
                                "accessibility_attributes": {"aria-label": "Submit form"},
                                "styling_info": {"color": "#000000", "background_color": "#ffffff"},
                                "interaction_handlers": ["onClick"],
                                "text_content": "Submit"
                            }
                        ],
                        "api_endpoints": [],
                        "user_flows": [],
                        "database_schema": {},
                        "configuration": {},
                        "deployment_info": {},
                        "documentation_links": [],
                        "feature_flags": {}
                    },
                    "security_scan_results": {
                        "vulnerabilities": [],
                        "scan_status": "clean"
                    }
                },
                "required_validations": [
                    "all_tests_passing",
                    "coverage_above_threshold", 
                    "performance_requirements_met"
                ]
            },
            
            # EXACT output specifications as defined in Implementation_rules.md
            "output_specifications": {
                "deliverable_files": [
                    f"docs/qa_reports/{story_id}_ux_validation.md",
                    f"docs/qa_reports/{story_id}_accessibility.json"
                ],
                "deliverable_data": {
                    "ux_validation_results": "object",
                    "accessibility_report": "object", 
                    "persona_testing_results": "object"
                },
                "validation_criteria": {
                    "user_experience": {
                        "anna_persona_satisfaction": {"min_score": 4},
                        "task_completion_rate": {"min_percentage": 95},
                        "time_to_complete": {"max_minutes": 10}
                    },
                    "accessibility": {
                        "wcag_compliance_level": "AA",
                        "screen_reader_compatibility": True,
                        "keyboard_navigation": True
                    }
                }
            },
            
            # EXACT quality gates from Implementation_rules.md  
            "quality_gates": [
                "all_test_suites_passing_100_percent",
                "code_coverage_minimum_threshold_met",
                "performance_benchmarks_within_targets",
                "security_vulnerability_scan_clean"
            ],
            
            # EXACT handoff criteria from Implementation_rules.md
            "handoff_criteria": [
                "comprehensive_test_coverage_achieved",
                "all_performance_requirements_validated", 
                "automated_test_pipeline_configured",
                "quality_metrics_documented"
            ]
        }
    
    def test_contract_structure_validation(self, contract_validator, valid_test_engineer_output_contract):
        """Test that Test Engineer output contract structure is valid."""
        validation_result = contract_validator.validate_contract(valid_test_engineer_output_contract)
        
        assert validation_result["is_valid"] is True, f"Contract validation failed: {validation_result['errors']}"
        assert len(validation_result["errors"]) == 0
        
        # Verify agent sequence is correct
        assert valid_test_engineer_output_contract["source_agent"] == "test_engineer"
        assert valid_test_engineer_output_contract["target_agent"] == "qa_tester"
    
    def test_required_files_follow_convention(self, valid_test_engineer_output_contract):
        """Test that required files follow story_id naming convention."""
        story_id = valid_test_engineer_output_contract["story_id"]
        required_files = valid_test_engineer_output_contract["input_requirements"]["required_files"]
        
        # All files must contain story_id for traceability
        for file_path in required_files:
            assert story_id in file_path, f"File path {file_path} does not contain story_id {story_id}"
        
        # Check expected file patterns from Implementation_rules.md
        expected_patterns = [
            f"tests/unit/{story_id}/",
            f"tests/integration/{story_id}/", 
            f"tests/e2e/{story_id}/",
            f"docs/test_reports/{story_id}_coverage.html"
        ]
        
        for expected in expected_patterns:
            assert expected in required_files, f"Missing required file pattern: {expected}"
    
    def test_dna_compliance_structure(self, valid_test_engineer_output_contract):
        """Test DNA compliance structure matches requirements."""
        dna_compliance = valid_test_engineer_output_contract["dna_compliance"]
        
        # Check required design principles
        design_principles = dna_compliance["design_principles_validation"]
        required_principles = [
            "pedagogical_value", "policy_to_practice", "time_respect",
            "holistic_thinking", "professional_tone"
        ]
        
        for principle in required_principles:
            assert principle in design_principles, f"Missing design principle: {principle}"
            assert isinstance(design_principles[principle], bool), f"Design principle {principle} must be boolean"
        
        # Check required architecture principles
        architecture_compliance = dna_compliance["architecture_compliance"]
        required_architecture = [
            "api_first", "stateless_backend", 
            "separation_of_concerns", "simplicity_first"
        ]
        
        for principle in required_architecture:
            assert principle in architecture_compliance, f"Missing architecture principle: {principle}"
            assert isinstance(architecture_compliance[principle], bool), f"Architecture principle {principle} must be boolean"
    
    def test_qa_output_contract_structure(self, qa_tester_agent, valid_test_engineer_output_contract):
        """Test that QA Tester produces correctly structured output contract."""
        # Mock the tools to avoid actual execution
        from unittest.mock import patch, AsyncMock
        
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', new_callable=AsyncMock) as mock_persona, \
             patch.object(qa_tester_agent.accessibility_checker, 'validate_accessibility', new_callable=AsyncMock) as mock_accessibility, \
             patch.object(qa_tester_agent.user_flow_validator, 'validate_user_flows', new_callable=AsyncMock) as mock_flow, \
             patch.object(qa_tester_agent, '_save_qa_reports', new_callable=AsyncMock) as mock_save:
            
            # Setup mock returns
            mock_persona.return_value = {
                "satisfaction_score": 4.2,
                "task_completion_rate": 96,
                "average_completion_time_minutes": 8.0
            }
            
            mock_accessibility.return_value = {
                "compliance_level": "AA",
                "compliance_percentage": 98.0
            }
            
            mock_flow.return_value = {
                "success_rate_percentage": 95.0,
                "flows_passed": 3,
                "total_flows": 3
            }
            
            # Execute contract processing
            result = asyncio.run(qa_tester_agent.process_contract(valid_test_engineer_output_contract))
            
            # Verify output contract structure
            assert result["contract_version"] == "1.0"
            assert result["source_agent"] == "qa_tester"
            assert result["target_agent"] == "quality_reviewer"
            assert result["story_id"] == valid_test_engineer_output_contract["story_id"]
            
            # Verify required sections exist
            required_sections = [
                "dna_compliance", "input_requirements", "output_specifications",
                "quality_gates", "handoff_criteria"
            ]
            
            for section in required_sections:
                assert section in result, f"Missing required section: {section}"
    
    def test_qa_output_deliverable_files_naming(self, qa_tester_agent, valid_test_engineer_output_contract):
        """Test that QA output files follow naming convention."""
        from unittest.mock import patch, AsyncMock
        
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', new_callable=AsyncMock) as mock_persona, \
             patch.object(qa_tester_agent.accessibility_checker, 'validate_accessibility', new_callable=AsyncMock) as mock_accessibility, \
             patch.object(qa_tester_agent.user_flow_validator, 'validate_user_flows', new_callable=AsyncMock) as mock_flow, \
             patch.object(qa_tester_agent, '_save_qa_reports', new_callable=AsyncMock) as mock_save:
            
            # Setup minimal mock returns
            mock_persona.return_value = {"satisfaction_score": 4.2}
            mock_accessibility.return_value = {"compliance_level": "AA"}
            mock_flow.return_value = {"success_rate_percentage": 95.0}
            
            result = asyncio.run(qa_tester_agent.process_contract(valid_test_engineer_output_contract))
            
            story_id = valid_test_engineer_output_contract["story_id"]
            deliverable_files = result["input_requirements"]["required_files"]
            
            # Expected file patterns for Quality Reviewer input
            expected_patterns = [
                f"docs/qa_reports/{story_id}_ux_validation.md",
                f"docs/qa_reports/{story_id}_accessibility.json",
                f"docs/qa_reports/{story_id}_persona_testing.json",
                f"docs/qa_reports/{story_id}_comprehensive_qa.json"
            ]
            
            for expected in expected_patterns:
                assert expected in deliverable_files, f"Missing expected deliverable file: {expected}"
                
            # All files must contain story_id
            for file_path in deliverable_files:
                assert story_id in file_path, f"Deliverable file {file_path} missing story_id"
    
    def test_qa_quality_gates_compliance(self, qa_tester_agent, valid_test_engineer_output_contract):
        """Test that QA Tester implements the correct quality gates."""
        from unittest.mock import patch, AsyncMock
        
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', new_callable=AsyncMock) as mock_persona, \
             patch.object(qa_tester_agent.accessibility_checker, 'validate_accessibility', new_callable=AsyncMock) as mock_accessibility, \
             patch.object(qa_tester_agent.user_flow_validator, 'validate_user_flows', new_callable=AsyncMock) as mock_flow, \
             patch.object(qa_tester_agent, '_save_qa_reports', new_callable=AsyncMock) as mock_save:
            
            mock_persona.return_value = {"satisfaction_score": 4.2}
            mock_accessibility.return_value = {"compliance_level": "AA"}
            mock_flow.return_value = {"success_rate_percentage": 95.0}
            
            result = asyncio.run(qa_tester_agent.process_contract(valid_test_engineer_output_contract))
            
            quality_gates = result["quality_gates"]
            
            # Expected quality gates as defined in Implementation_rules.md and agent specification
            expected_gates = [
                "anna_persona_satisfaction_score_minimum_met",
                "wcag_aa_compliance_100_percent_verified",
                "task_completion_time_under_10_minutes", 
                "professional_tone_maintained_throughout",
                "pedagogical_value_clearly_demonstrated",
                "all_user_flows_validated_successfully"
            ]
            
            for expected_gate in expected_gates:
                assert expected_gate in quality_gates, f"Missing expected quality gate: {expected_gate}"
    
    def test_validation_criteria_compliance(self, qa_tester_agent, valid_test_engineer_output_contract):
        """Test that validation criteria match Implementation_rules.md specification."""
        from unittest.mock import patch, AsyncMock
        
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', new_callable=AsyncMock) as mock_persona, \
             patch.object(qa_tester_agent.accessibility_checker, 'validate_accessibility', new_callable=AsyncMock) as mock_accessibility, \
             patch.object(qa_tester_agent.user_flow_validator, 'validate_user_flows', new_callable=AsyncMock) as mock_flow, \
             patch.object(qa_tester_agent, '_save_qa_reports', new_callable=AsyncMock) as mock_save:
            
            mock_persona.return_value = {"satisfaction_score": 4.2}
            mock_accessibility.return_value = {"compliance_level": "AA"} 
            mock_flow.return_value = {"success_rate_percentage": 95.0}
            
            result = asyncio.run(qa_tester_agent.process_contract(valid_test_engineer_output_contract))
            
            validation_criteria = result["output_specifications"]["validation_criteria"]
            
            # Check user experience criteria match Implementation_rules.md
            ux_criteria = validation_criteria["user_experience"]
            assert ux_criteria["anna_persona_satisfaction"]["min_score"] == 4
            assert ux_criteria["task_completion_rate"]["min_percentage"] == 95
            assert ux_criteria["time_to_complete"]["max_minutes"] == 10
            
            # Check accessibility criteria match Implementation_rules.md  
            accessibility_criteria = validation_criteria["accessibility"]
            assert accessibility_criteria["wcag_compliance_level"] == "AA"
            assert accessibility_criteria["screen_reader_compatibility"] is True
            assert accessibility_criteria["keyboard_navigation"] is True
    
    def test_agent_sequence_validation(self, contract_validator):
        """Test that agent sequence validation works correctly."""
        # Valid sequence: test_engineer -> qa_tester
        assert contract_validator._validate_agent_sequence("test_engineer", "qa_tester") is True
        
        # Valid sequence: qa_tester -> quality_reviewer  
        assert contract_validator._validate_agent_sequence("qa_tester", "quality_reviewer") is True
        
        # Invalid sequences
        assert contract_validator._validate_agent_sequence("test_engineer", "quality_reviewer") is False
        assert contract_validator._validate_agent_sequence("developer", "qa_tester") is False
        assert contract_validator._validate_agent_sequence("qa_tester", "developer") is False
    
    def test_contract_backward_compatibility(self, qa_tester_agent):
        """Test that QA Tester maintains backward compatibility with contract changes."""
        # Test with minimal valid contract (should not break)
        minimal_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-MINIMAL-001",
            "source_agent": "test_engineer",
            "target_agent": "qa_tester",
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
                "required_data": {
                    "test_suite": {"unit_tests": [], "integration_tests": [], "e2e_tests": []},
                    "performance_results": {
                        "lighthouse_score": 90.0,
                        "api_response_time_ms": 200.0,
                        "page_load_time_ms": 3000.0,
                        "time_to_interactive_ms": 3000.0,
                        "first_contentful_paint_ms": 1500.0,
                        "largest_contentful_paint_ms": 2000.0,
                        "cumulative_layout_shift": 0.1,
                        "bundle_size_kb": 500.0,
                        "memory_usage_mb": 100.0,
                        "cpu_usage_percentage": 20.0
                    },
                    "coverage_report": {},
                    "implementation_data": {
                        "implementation_id": "minimal",
                        "story_id": "STORY-MINIMAL-001",
                        "ui_components": [],
                        "api_endpoints": [],
                        "user_flows": [],
                        "database_schema": {},
                        "configuration": {},
                        "deployment_info": {},
                        "documentation_links": [],
                        "feature_flags": {}
                    },
                    "security_scan_results": {"vulnerabilities": []}
                },
                "required_validations": []
            },
            "quality_gates": [],
            "handoff_criteria": []
        }
        
        from unittest.mock import patch, AsyncMock
        
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', new_callable=AsyncMock) as mock_persona, \
             patch.object(qa_tester_agent.accessibility_checker, 'validate_accessibility', new_callable=AsyncMock) as mock_accessibility, \
             patch.object(qa_tester_agent.user_flow_validator, 'validate_user_flows', new_callable=AsyncMock) as mock_flow, \
             patch.object(qa_tester_agent, '_save_qa_reports', new_callable=AsyncMock) as mock_save:
            
            mock_persona.return_value = {"satisfaction_score": 4.0}
            mock_accessibility.return_value = {"compliance_level": "AA"}
            mock_flow.return_value = {"success_rate_percentage": 95.0}
            
            # Should not raise exception
            result = asyncio.run(qa_tester_agent.process_contract(minimal_contract))
            
            # Should still produce valid output structure
            assert result is not None
            assert result["contract_version"] == "1.0"
            assert result["source_agent"] == "qa_tester"
            assert result["target_agent"] == "quality_reviewer"
    
    def test_error_handling_maintains_contract_structure(self, qa_tester_agent, valid_test_engineer_output_contract):
        """Test that even when errors occur, contract structure is maintained or proper exceptions are raised."""
        from unittest.mock import patch, AsyncMock
        from ...shared.exceptions import AgentExecutionError
        
        # Test with tool failure
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', side_effect=Exception("Tool failure")):
            
            with pytest.raises(AgentExecutionError) as exc_info:
                asyncio.run(qa_tester_agent.process_contract(valid_test_engineer_output_contract))
            
            # Should raise proper exception with story_id context
            assert "STORY-001-001" in str(exc_info.value)
            assert "Tool failure" in str(exc_info.value)
    
    def test_contract_validation_integration(self, contract_validator, qa_tester_agent, valid_test_engineer_output_contract):
        """Test that contract validation integrates correctly with agent processing."""
        from unittest.mock import patch, AsyncMock
        
        # First validate the input contract
        input_validation = contract_validator.validate_contract(valid_test_engineer_output_contract)
        assert input_validation["is_valid"] is True
        
        # Process the contract
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', new_callable=AsyncMock) as mock_persona, \
             patch.object(qa_tester_agent.accessibility_checker, 'validate_accessibility', new_callable=AsyncMock) as mock_accessibility, \
             patch.object(qa_tester_agent.user_flow_validator, 'validate_user_flows', new_callable=AsyncMock) as mock_flow, \
             patch.object(qa_tester_agent, '_save_qa_reports', new_callable=AsyncMock) as mock_save:
            
            mock_persona.return_value = {"satisfaction_score": 4.2}
            mock_accessibility.return_value = {"compliance_level": "AA"}
            mock_flow.return_value = {"success_rate_percentage": 95.0}
            
            output_contract = asyncio.run(qa_tester_agent.process_contract(valid_test_engineer_output_contract))
        
        # Validate the output contract
        output_validation = contract_validator.validate_contract(output_contract)
        assert output_validation["is_valid"] is True, f"Output contract validation failed: {output_validation['errors']}"
        
        # Verify agent sequence is correct for output
        assert output_contract["source_agent"] == "qa_tester"
        assert output_contract["target_agent"] == "quality_reviewer"