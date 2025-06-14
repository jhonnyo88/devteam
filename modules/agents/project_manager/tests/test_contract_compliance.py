"""
Contract compliance tests for Project Manager agent.

PURPOSE:
Validates that Project Manager agent strictly follows the contract specifications
defined in Implementation_rules.md to ensure modular architecture integrity.

CRITICAL IMPORTANCE:
This test ensures that Project Manager can work completely independently while
still integrating seamlessly with Game Designer and other downstream agents.

CONTRACT PROTECTION:
These tests are SACRED - they protect the contract system that enables
modular development where each agent can be improved independently.
"""

import pytest
import asyncio
import json
from datetime import datetime

# Import the agent and contract models
from ..agent import ProjectManagerAgent
from ..contracts.input_models import parse_project_manager_input_contract
from ...shared.contract_validator import ContractValidator, ContractValidationError


class TestProjectManagerContractCompliance:
    """Test suite for Project Manager contract compliance."""
    
    @pytest.fixture
    def contract_validator(self):
        """Create ContractValidator instance."""
        return ContractValidator()
    
    @pytest.fixture
    def project_manager_agent(self):
        """Create Project Manager agent instance."""
        return ProjectManagerAgent()
    
    @pytest.fixture
    def valid_github_input_contract(self):
        """
        Valid contract from GitHub issue as defined in Implementation_rules.md.
        
        This is the EXACT contract specification that GitHub integration must produce
        and Project Manager must accept.
        """
        story_id = "STORY-001-001"
        
        return {
            "contract_version": "1.0",
            "story_id": story_id,
            "source_agent": "github",
            "target_agent": "project_manager",
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
                "required_files": [],
                "required_data": {
                    "github_issue": {
                        "issue_id": 1001,
                        "title": "Add user registration functionality",
                        "description": "Users need ability to register for DigiNativa training",
                        "labels": ["feature-request", "priority-high"],
                        "created_at": "2024-01-15T10:00:00Z",
                        "priority": "high",
                        "acceptance_criteria": [
                            "User can enter personal information",
                            "User receives confirmation email",
                            "User account is created in system"
                        ],
                        "user_persona": "Anna",
                        "github_url": "https://github.com/owner/repo/issues/1001"
                    }
                },
                "required_validations": [
                    "github_issue_format_valid",
                    "acceptance_criteria_present"
                ]
            },
            
            # EXACT output specifications as defined in Implementation_rules.md
            "output_specifications": {
                "deliverable_files": [
                    f"docs/stories/{story_id}_description.md",
                    f"docs/breakdown/{story_id}_story_breakdown.json",
                    f"docs/analysis/{story_id}_feature_analysis.json"
                ],
                "deliverable_data": {
                    "story_breakdown": "object",
                    "dna_analysis": "object",
                    "agent_assignments": "object"
                },
                "validation_criteria": {
                    "story_quality": {
                        "dna_compliance_score": {"min_score": 4},
                        "acceptance_criteria_clarity": {"min_score": 4},
                        "technical_feasibility": {"min_score": 4}
                    },
                    "breakdown_completeness": {
                        "all_acceptance_criteria_covered": True,
                        "implementation_approach_defined": True,
                        "dependencies_identified": True
                    }
                }
            },
            
            # EXACT quality gates from Implementation_rules.md  
            "quality_gates": [
                "all_5_design_principles_validated",
                "all_4_architecture_principles_validated",
                "acceptance_criteria_100_percent_covered",
                "technical_approach_clearly_defined",
                "story_breakdown_logically_structured"
            ],
            
            # EXACT handoff criteria from Implementation_rules.md
            "handoff_criteria": [
                "comprehensive_story_breakdown_created",
                "dna_compliance_fully_validated",
                "next_agent_assignments_clearly_defined",
                "acceptance_criteria_parsed_and_structured"
            ]
        }
    
    def test_contract_structure_validation(self, contract_validator, valid_github_input_contract):
        """Test that GitHub input contract structure is valid."""
        validation_result = contract_validator.validate_contract(valid_github_input_contract)
        
        assert validation_result["is_valid"] is True, f"Contract validation failed: {validation_result['errors']}"
        assert len(validation_result["errors"]) == 0
        
        # Verify agent sequence is correct
        assert valid_github_input_contract["source_agent"] == "github"
        assert valid_github_input_contract["target_agent"] == "project_manager"
    
    def test_required_files_follow_convention(self, valid_github_input_contract):
        """Test that required output files follow story_id naming convention."""
        story_id = valid_github_input_contract["story_id"]
        deliverable_files = valid_github_input_contract["output_specifications"]["deliverable_files"]
        
        # All files must contain story_id for traceability
        for file_path in deliverable_files:
            assert story_id in file_path, f"File path {file_path} does not contain story_id {story_id}"
        
        # Check expected file patterns from Implementation_rules.md
        expected_patterns = [
            f"docs/stories/{story_id}_description.md",
            f"docs/breakdown/{story_id}_story_breakdown.json",
            f"docs/analysis/{story_id}_feature_analysis.json"
        ]
        
        for expected in expected_patterns:
            assert expected in deliverable_files, f"Missing required file pattern: {expected}"
    
    def test_dna_compliance_structure(self, valid_github_input_contract):
        """Test DNA compliance structure matches requirements."""
        dna_compliance = valid_github_input_contract["dna_compliance"]
        
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
    
    def test_project_manager_output_contract_structure(self, project_manager_agent, valid_github_input_contract):
        """Test that Project Manager produces correctly structured output contract."""
        # Mock the tools to avoid actual execution
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature_request', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.dna_compliance_checker, 'validate_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(project_manager_agent, '_save_analysis_reports', new_callable=AsyncMock) as mock_save:
            
            # Setup mock returns
            mock_analyzer.return_value = {
                "story_breakdown": {
                    "main_story": {
                        "title": "Add user registration functionality",
                        "description": "Users need ability to register for DigiNativa training",
                        "acceptance_criteria": [
                            "User can enter personal information",
                            "User receives confirmation email", 
                            "User account is created in system"
                        ],
                        "technical_approach": "React form with FastAPI backend",
                        "complexity_score": 3
                    },
                    "sub_stories": []
                },
                "dna_analysis": {
                    "design_score": 4.2,
                    "architecture_score": 4.5,
                    "overall_compliance": 4.35
                }
            }
            
            mock_dna.return_value = {
                "is_compliant": True,
                "compliance_score": 4.35,
                "validation_details": {}
            }
            
            # Execute contract processing
            result = asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
            
            # Verify output contract structure
            assert result["contract_version"] == "1.0"
            assert result["source_agent"] == "project_manager"
            assert result["target_agent"] == "game_designer"
            assert result["story_id"] == valid_github_input_contract["story_id"]
            
            # Verify required sections exist
            required_sections = [
                "dna_compliance", "input_requirements", "output_specifications",
                "quality_gates", "handoff_criteria"
            ]
            
            for section in required_sections:
                assert section in result, f"Missing required section: {section}"
    
    def test_project_manager_output_deliverable_files_naming(self, project_manager_agent, valid_github_input_contract):
        """Test that Project Manager output files follow naming convention."""
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature_request', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.dna_compliance_checker, 'validate_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(project_manager_agent, '_save_analysis_reports', new_callable=AsyncMock) as mock_save:
            
            # Setup minimal mock returns
            mock_analyzer.return_value = {
                "story_breakdown": {"main_story": {"title": "Test"}},
                "dna_analysis": {"design_score": 4.2}
            }
            mock_dna.return_value = {"is_compliant": True}
            
            result = asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
            
            story_id = valid_github_input_contract["story_id"]
            deliverable_files = result["input_requirements"]["required_files"]
            
            # Expected file patterns for Game Designer input
            expected_patterns = [
                f"docs/stories/{story_id}_description.md",
                f"docs/breakdown/{story_id}_story_breakdown.json",
                f"docs/analysis/{story_id}_feature_analysis.json"
            ]
            
            for expected in expected_patterns:
                assert expected in deliverable_files, f"Missing expected deliverable file: {expected}"
                
            # All files must contain story_id
            for file_path in deliverable_files:
                assert story_id in file_path, f"Deliverable file {file_path} missing story_id"
    
    def test_project_manager_quality_gates_compliance(self, project_manager_agent, valid_github_input_contract):
        """Test that Project Manager implements the correct quality gates."""
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature_request', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.dna_compliance_checker, 'validate_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(project_manager_agent, '_save_analysis_reports', new_callable=AsyncMock) as mock_save:
            
            mock_analyzer.return_value = {
                "story_breakdown": {"main_story": {"title": "Test"}},
                "dna_analysis": {"design_score": 4.2}
            }
            mock_dna.return_value = {"is_compliant": True}
            
            result = asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
            
            quality_gates = result["quality_gates"]
            
            # Expected quality gates as defined in Implementation_rules.md and agent specification
            expected_gates = [
                "all_5_design_principles_validated",
                "all_4_architecture_principles_validated", 
                "acceptance_criteria_100_percent_covered",
                "technical_approach_clearly_defined",
                "story_breakdown_logically_structured",
                "dna_compliance_score_minimum_met"
            ]
            
            for expected_gate in expected_gates:
                assert expected_gate in quality_gates, f"Missing expected quality gate: {expected_gate}"
    
    def test_validation_criteria_compliance(self, project_manager_agent, valid_github_input_contract):
        """Test that validation criteria match Implementation_rules.md specification."""
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature_request', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.dna_compliance_checker, 'validate_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(project_manager_agent, '_save_analysis_reports', new_callable=AsyncMock) as mock_save:
            
            mock_analyzer.return_value = {
                "story_breakdown": {"main_story": {"title": "Test"}},
                "dna_analysis": {"design_score": 4.2}
            }
            mock_dna.return_value = {"is_compliant": True}
            
            result = asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
            
            validation_criteria = result["output_specifications"]["validation_criteria"]
            
            # Check game design criteria match Implementation_rules.md
            design_criteria = validation_criteria["game_design"]
            assert design_criteria["pedagogical_elements"]["min_count"] == 2
            assert design_criteria["anna_persona_alignment"]["min_score"] == 4
            assert design_criteria["component_mappings"]["shadcn_components_specified"] is True
            
            # Check technical feasibility criteria match Implementation_rules.md  
            technical_criteria = validation_criteria["technical_feasibility"]
            assert technical_criteria["implementation_complexity"]["max_score"] == 3
            assert technical_criteria["api_design"]["endpoints_clearly_defined"] is True
            assert technical_criteria["component_reusability"]["existing_components_preferred"] is True
    
    def test_agent_sequence_validation(self, contract_validator):
        """Test that agent sequence validation works correctly."""
        # Valid sequence: github -> project_manager
        assert contract_validator._validate_agent_sequence("github", "project_manager") is True
        
        # Valid sequence: project_manager -> game_designer  
        assert contract_validator._validate_agent_sequence("project_manager", "game_designer") is True
        
        # Invalid sequences
        assert contract_validator._validate_agent_sequence("project_manager", "developer") is False
        assert contract_validator._validate_agent_sequence("test_engineer", "project_manager") is False
        assert contract_validator._validate_agent_sequence("project_manager", "qa_tester") is False
    
    def test_contract_backward_compatibility(self, project_manager_agent):
        """Test that Project Manager maintains backward compatibility with contract changes."""
        # Test with minimal valid contract (should not break)
        minimal_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-MINIMAL-001",
            "source_agent": "github",
            "target_agent": "project_manager",
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
                    "github_issue": {
                        "issue_id": 1,
                        "title": "Minimal test",
                        "description": "Test description", 
                        "labels": ["feature-request"],
                        "created_at": "2024-01-15T10:00:00Z",
                        "priority": "medium",
                        "acceptance_criteria": ["Basic criterion"],
                        "user_persona": "Anna",
                        "github_url": "https://github.com/test/test/issues/1"
                    }
                },
                "required_validations": []
            },
            "quality_gates": [],
            "handoff_criteria": []
        }
        
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature_request', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.dna_compliance_checker, 'validate_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(project_manager_agent, '_save_analysis_reports', new_callable=AsyncMock) as mock_save:
            
            mock_analyzer.return_value = {
                "story_breakdown": {"main_story": {"title": "Test"}},
                "dna_analysis": {"design_score": 4.0}
            }
            mock_dna.return_value = {"is_compliant": True}
            
            # Should not raise exception
            result = asyncio.run(project_manager_agent.process_contract(minimal_contract))
            
            # Should still produce valid output structure
            assert result is not None
            assert result["contract_version"] == "1.0"
            assert result["source_agent"] == "project_manager"
            assert result["target_agent"] == "game_designer"
    
    def test_error_handling_maintains_contract_structure(self, project_manager_agent, valid_github_input_contract):
        """Test that even when errors occur, contract structure is maintained or proper exceptions are raised."""
        from unittest.mock import patch, AsyncMock
        from ...shared.exceptions import AgentExecutionError
        
        # Test with tool failure
        with patch.object(project_manager_agent.story_analyzer, 'analyze_feature_request', side_effect=Exception("Analysis failure")):
            
            with pytest.raises(AgentExecutionError) as exc_info:
                asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
            
            # Should raise proper exception with story_id context
            assert "STORY-001-001" in str(exc_info.value)
            assert "Analysis failure" in str(exc_info.value)
    
    def test_contract_validation_integration(self, contract_validator, project_manager_agent, valid_github_input_contract):
        """Test that contract validation integrates correctly with agent processing."""
        from unittest.mock import patch, AsyncMock
        
        # First validate the input contract
        input_validation = contract_validator.validate_contract(valid_github_input_contract)
        assert input_validation["is_valid"] is True
        
        # Process the contract
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature_request', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.dna_compliance_checker, 'validate_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(project_manager_agent, '_save_analysis_reports', new_callable=AsyncMock) as mock_save:
            
            mock_analyzer.return_value = {
                "story_breakdown": {"main_story": {"title": "Test"}},
                "dna_analysis": {"design_score": 4.2}
            }
            mock_dna.return_value = {"is_compliant": True}
            
            output_contract = asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
        
        # Validate the output contract
        output_validation = contract_validator.validate_contract(output_contract)
        assert output_validation["is_valid"] is True, f"Output contract validation failed: {output_validation['errors']}"
        
        # Verify agent sequence is correct for output
        assert output_contract["source_agent"] == "project_manager"
        assert output_contract["target_agent"] == "game_designer"