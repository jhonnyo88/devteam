"""
Project Manager Agent - Contract Compliance Tests

PURPOSE:
Validates that Project Manager agent maintains contract compliance
according to TEST_STRATEGY.md requirements.

CRITICAL IMPORTANCE:
These tests ensure the PM agent can work with the team without
breaking the modular architecture that the contract system enables.
"""

import pytest
import asyncio
import json
from typing import Dict, Any
from datetime import datetime

# Import using absolute path to avoid relative import issues
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.agents.project_manager.contracts import ProjectManagerOutputContract
from modules.shared.contract_validator import ContractValidator
from modules.shared.exceptions import ContractValidationError


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
        Valid contract from GitHub as defined in Implementation_rules.md.
        
        This is the EXACT contract specification that GitHub must produce
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
            "input_requirements": {
                "required_files": [],
                "required_data": {
                    "feature_description": "Add user registration for DigiNativa game",
                    "acceptance_criteria": [
                        "User can create account with email and password",
                        "User receives confirmation email", 
                        "User can log in after registration"
                    ],
                    "user_persona": "Anna",
                    "priority_level": "high",
                    "github_issue_id": 42,
                    "github_url": "https://github.com/user/repo/issues/42",
                    "labels": ["feature-request", "priority-high"],
                    "created_at": "2024-01-15T10:00:00Z"
                },
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
    
    def test_contract_structure_validation(self, contract_validator, valid_github_input_contract):
        """Test that GitHub input contract structure is valid."""
        validation_result = contract_validator.validate_contract(valid_github_input_contract)
        
        assert validation_result["is_valid"] is True, f"Contract validation failed: {validation_result['errors']}"
        assert len(validation_result["errors"]) == 0
        
        # Verify agent sequence is correct
        assert valid_github_input_contract["source_agent"] == "github"
        assert valid_github_input_contract["target_agent"] == "project_manager"
    
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
    
    def test_pm_output_contract_structure(self, project_manager_agent, valid_github_input_contract):
        """Test that Project Manager produces correctly structured output contract."""
        # Mock the tools to avoid actual execution
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.story_analyzer, 'create_story_breakdown', new_callable=AsyncMock) as mock_breakdown:
            
            # Setup mock returns
            mock_github.return_value = []
            mock_analyzer.return_value = {
                "dna_compliance": valid_github_input_contract["dna_compliance"],
                "complexity_assessment": {"technical": "medium", "design": "low"}
            }
            mock_breakdown.return_value = {
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
    
    def test_pm_output_deliverable_files_naming(self, project_manager_agent, valid_github_input_contract):
        """Test that PM output files follow naming convention."""
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.story_analyzer, 'create_story_breakdown', new_callable=AsyncMock) as mock_breakdown:
            
            # Setup minimal mock returns
            mock_github.return_value = []
            mock_analyzer.return_value = {"dna_compliance": valid_github_input_contract["dna_compliance"]}
            mock_breakdown.return_value = {"feature_description": "test"}
            
            result = asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
            
            story_id = valid_github_input_contract["story_id"]
            deliverable_files = result["input_requirements"]["required_files"]
            
            # Expected file patterns for Game Designer input
            expected_patterns = [
                f"docs/stories/story_description_{story_id}.md",
                f"docs/analysis/feature_analysis_{story_id}.json"
            ]
            
            for expected in expected_patterns:
                assert expected in deliverable_files, f"Missing expected deliverable file: {expected}"
                
            # All files must contain story_id
            for file_path in deliverable_files:
                assert story_id in file_path, f"Deliverable file {file_path} missing story_id"
    
    def test_pm_quality_gates_compliance(self, project_manager_agent, valid_github_input_contract):
        """Test that Project Manager implements the correct quality gates."""
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.story_analyzer, 'create_story_breakdown', new_callable=AsyncMock) as mock_breakdown:
            
            mock_github.return_value = []
            mock_analyzer.return_value = {"dna_compliance": valid_github_input_contract["dna_compliance"]}
            mock_breakdown.return_value = {"feature_description": "test"}
            
            result = asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
            
            quality_gates = result["quality_gates"]
            
            # Expected quality gates as defined in Implementation_rules.md
            expected_gates = [
                "dna_compliance_verified",
                "story_breakdown_complete", 
                "acceptance_criteria_clear",
                "gdd_consistency_checked"
            ]
            
            for expected_gate in expected_gates:
                assert expected_gate in quality_gates, f"Missing expected quality gate: {expected_gate}"
    
    def test_agent_sequence_validation(self, contract_validator):
        """Test that agent sequence validation works correctly."""
        # Valid sequence: github -> project_manager
        assert contract_validator._validate_agent_sequence("github", "project_manager") is True
        
        # Valid sequence: project_manager -> game_designer  
        assert contract_validator._validate_agent_sequence("project_manager", "game_designer") is True
        
        # Invalid sequences
        assert contract_validator._validate_agent_sequence("project_manager", "developer") is False
        assert contract_validator._validate_agent_sequence("game_designer", "project_manager") is False
    
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
                    "feature_description": "Minimal test feature",
                    "acceptance_criteria": ["Basic functionality works"],
                    "user_persona": "Anna",
                    "priority_level": "low"
                },
                "required_validations": []
            },
            "quality_gates": [],
            "handoff_criteria": []
        }
        
        from unittest.mock import patch, AsyncMock
        
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.story_analyzer, 'create_story_breakdown', new_callable=AsyncMock) as mock_breakdown:
            
            mock_github.return_value = []
            mock_analyzer.return_value = {"dna_compliance": minimal_contract["dna_compliance"]}
            mock_breakdown.return_value = {"feature_description": "Minimal test"}
            
            # Should not raise exception
            result = asyncio.run(project_manager_agent.process_contract(minimal_contract))
            
            # Should still produce valid output structure
            assert result is not None
            assert result["contract_version"] == "1.0"
            assert result["source_agent"] == "project_manager"
            assert result["target_agent"] == "game_designer"
    
    def test_contract_validation_integration(self, contract_validator, project_manager_agent, valid_github_input_contract):
        """Test that contract validation integrates correctly with agent processing."""
        from unittest.mock import patch, AsyncMock
        
        # First validate the input contract
        input_validation = contract_validator.validate_contract(valid_github_input_contract)
        assert input_validation["is_valid"] is True
        
        # Process the contract
        with patch.object(project_manager_agent.github_integration, 'fetch_new_feature_requests', new_callable=AsyncMock) as mock_github, \
             patch.object(project_manager_agent.story_analyzer, 'analyze_feature', new_callable=AsyncMock) as mock_analyzer, \
             patch.object(project_manager_agent.story_analyzer, 'create_story_breakdown', new_callable=AsyncMock) as mock_breakdown:
            
            mock_github.return_value = []
            mock_analyzer.return_value = {"dna_compliance": valid_github_input_contract["dna_compliance"]}
            mock_breakdown.return_value = {"feature_description": "test"}
            
            output_contract = asyncio.run(project_manager_agent.process_contract(valid_github_input_contract))
        
        # Validate the output contract
        output_validation = contract_validator.validate_contract(output_contract)
        assert output_validation["is_valid"] is True, f"Output contract validation failed: {output_validation['errors']}"
        
        # Verify agent sequence is correct for output
        assert output_contract["source_agent"] == "project_manager"
        assert output_contract["target_agent"] == "game_designer"