"""
Comprehensive tests for Project Manager Agent.

Tests all core functionality including GitHub integration,
DNA compliance checking, story analysis, and contract generation.
"""

import pytest
import asyncio
import json
import tempfile
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from pathlib import Path
from datetime import datetime

from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.shared.exceptions import (
    DNAComplianceError, BusinessLogicError, ExternalServiceError,
    AgentExecutionError
)


class TestProjectManagerAgent:
    """Test suite for Project Manager Agent."""

    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        return {
            "github_token": "test_token",
            "github_repo_owner": "jhonnyo88",
            "github_repo_name": "devteam",
            "project_repo_owner": "jhonnyo88", 
            "project_repo_name": "diginativa-game",
            "docs_path": "test_docs",
            "max_concurrent_stories": 3,
            "story_priority_threshold": "medium"
        }

    @pytest.fixture
    def sample_feature_data(self):
        """Sample feature request data for testing."""
        return {
            "feature_description": "As Anna, I want to practice policy application through interactive scenarios so that I can better understand real-world implementation.",
            "acceptance_criteria": [
                "User can select from multiple policy scenarios",
                "Each scenario provides clear context and background",
                "User receives immediate feedback on decisions",
                "Progress is tracked and saved",
                "Feature completes within 10 minutes"
            ],
            "user_persona": "Anna",
            "priority_level": "high",
            "time_constraint_minutes": 10,
            "learning_objectives": [
                "Apply policy knowledge to practical situations",
                "Understand decision-making frameworks",
                "Practice critical thinking in policy context"
            ],
            "gdd_section_reference": "Section 3.2 - Interactive Learning",
            "github_issue_url": "https://github.com/jhonnyo88/diginativa-game/issues/123",
            "github_issue_number": 123,
            "requested_by": "client_user",
            "created_at": "2024-01-15T10:30:00Z"
        }

    @pytest.fixture
    def sample_input_contract(self, sample_feature_data):
        """Sample input contract for PM Agent."""
        return {
            "contract_version": "1.0",
            "story_id": "STORY-GH-123",
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
                "required_data": sample_feature_data,
                "required_validations": [
                    "github_issue_valid",
                    "feature_request_format_correct"
                ]
            },
            "quality_gates": [
                "github_issue_parsed_correctly",
                "feature_request_data_complete"
            ],
            "handoff_criteria": [
                "all_required_data_extracted",
                "issue_format_validated"
            ]
        }

    @pytest.fixture
    def temp_docs_dir(self):
        """Create temporary docs directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def mock_pm_agent(self, mock_config, temp_docs_dir):
        """Create mocked PM Agent for testing."""
        # Update config with temp directory
        mock_config["docs_path"] = temp_docs_dir
        
        with patch.multiple(
            'modules.agents.project_manager.agent',
            GitHubIntegration=MagicMock(),
            StoryAnalyzer=MagicMock(),
            DNAComplianceChecker=MagicMock()
        ):
            agent = ProjectManagerAgent("test-pm-001", mock_config)
            
            # Setup tool mocks
            agent.github_integration = Mock()
            agent.story_analyzer = AsyncMock()
            agent.dna_compliance_checker = AsyncMock()
            
            yield agent

    # ==========================================
    # INITIALIZATION TESTS
    # ==========================================

    def test_pm_agent_initialization_success(self, mock_config):
        """Test successful PM Agent initialization."""
        with patch.multiple(
            'modules.agents.project_manager.agent',
            GitHubIntegration=MagicMock(),
            StoryAnalyzer=MagicMock(), 
            DNAComplianceChecker=MagicMock()
        ):
            agent = ProjectManagerAgent("test-pm-001", mock_config)
            
            assert agent.agent_id == "test-pm-001"
            assert agent.agent_type == "project_manager"
            assert agent.max_concurrent_stories == 3
            assert agent.story_priority_threshold == "medium"

    def test_pm_agent_initialization_with_defaults(self):
        """Test PM Agent initialization with default values."""
        with patch.multiple(
            'modules.agents.project_manager.agent',
            GitHubIntegration=MagicMock(),
            StoryAnalyzer=MagicMock(),
            DNAComplianceChecker=MagicMock()
        ):
            agent = ProjectManagerAgent()
            
            assert agent.agent_id == "pm-001"
            assert agent.agent_type == "project_manager"
            assert agent.max_concurrent_stories == 5
            assert agent.story_priority_threshold == "medium"

    def test_pm_agent_initialization_tool_failure(self, mock_config):
        """Test PM Agent initialization when tools fail."""
        with patch('modules.agents.project_manager.agent.GitHubIntegration', side_effect=Exception("GitHub failed")):
            with pytest.raises(AgentExecutionError) as exc_info:
                ProjectManagerAgent("test-pm-001", mock_config)
            
            assert "PM Agent initialization failed" in str(exc_info.value)

    # ==========================================
    # FEATURE DATA EXTRACTION TESTS  
    # ==========================================

    def test_extract_feature_data_success(self, mock_pm_agent, sample_input_contract):
        """Test successful feature data extraction."""
        feature_data = mock_pm_agent._extract_feature_data(sample_input_contract)
        
        assert feature_data["feature_description"] == sample_input_contract["input_requirements"]["required_data"]["feature_description"]
        assert feature_data["user_persona"] == "Anna"
        assert feature_data["priority_level"] == "high"
        assert feature_data["time_constraint_minutes"] == 10

    def test_extract_feature_data_missing_required_field(self, mock_pm_agent, sample_input_contract):
        """Test feature data extraction with missing required field."""
        # Remove required field
        del sample_input_contract["input_requirements"]["required_data"]["feature_description"]
        
        with pytest.raises(BusinessLogicError) as exc_info:
            mock_pm_agent._extract_feature_data(sample_input_contract)
        
        assert "Missing required field: feature_description" in str(exc_info.value)

    def test_extract_feature_data_invalid_priority(self, mock_pm_agent, sample_input_contract):
        """Test feature data extraction with invalid priority."""
        sample_input_contract["input_requirements"]["required_data"]["priority_level"] = "invalid"
        
        with pytest.raises(BusinessLogicError) as exc_info:
            mock_pm_agent._extract_feature_data(sample_input_contract)
        
        assert "Invalid priority level: invalid" in str(exc_info.value)

    # ==========================================
    # CONTRACT PROCESSING TESTS
    # ==========================================

    async def test_process_contract_success(self, mock_pm_agent, sample_input_contract):
        """Test successful contract processing."""
        # Setup tool mocks
        mock_pm_agent.dna_compliance_checker.analyze_feature_compliance.return_value = {
            "compliant": True,
            "pedagogical_value": True,
            "policy_to_practice": True,
            "time_respect": True,
            "holistic_thinking": True,
            "professional_tone": True
        }
        
        mock_pm_agent.story_analyzer.create_story_breakdown.return_value = {
            "feature_summary": {"title": "Test Feature"},
            "user_stories": [{"story": "Test story"}],
            "technical_requirements": {},
            "design_requirements": {},
            "acceptance_criteria": ["Test criteria"]
        }
        
        mock_pm_agent.story_analyzer.generate_acceptance_criteria.return_value = [
            "Feature works correctly",
            "User can complete task",
            "Performance meets requirements"
        ]
        
        mock_pm_agent.story_analyzer.assess_complexity.return_value = {
            "effort_points": 5,
            "technical_complexity": "Medium",
            "design_complexity": "Low",
            "estimated_duration_hours": 16
        }
        
        result = await mock_pm_agent.process_contract(sample_input_contract)
        
        assert result["target_agent"] == "game_designer"
        assert result["story_id"] == "STORY-GH-123"
        assert "input_requirements" in result
        assert "quality_gates" in result

    async def test_process_contract_dna_compliance_failure(self, mock_pm_agent, sample_input_contract):
        """Test contract processing with DNA compliance failure."""
        mock_pm_agent.dna_compliance_checker.analyze_feature_compliance.return_value = {
            "compliant": False,
            "violations": ["pedagogical_value", "time_respect"]
        }
        
        with pytest.raises(DNAComplianceError) as exc_info:
            await mock_pm_agent.process_contract(sample_input_contract)
        
        assert "Feature violates DNA principles" in str(exc_info.value)

    async def test_process_contract_story_analyzer_failure(self, mock_pm_agent, sample_input_contract):
        """Test contract processing with story analyzer failure."""
        mock_pm_agent.dna_compliance_checker.analyze_feature_compliance.return_value = {
            "compliant": True,
            "pedagogical_value": True,
            "policy_to_practice": True,
            "time_respect": True,
            "holistic_thinking": True,
            "professional_tone": True
        }
        
        mock_pm_agent.story_analyzer.create_story_breakdown.side_effect = Exception("Analysis failed")
        
        with pytest.raises(AgentExecutionError) as exc_info:
            await mock_pm_agent.process_contract(sample_input_contract)
        
        assert "Failed to process feature request" in str(exc_info.value)

    # ==========================================
    # QUALITY GATE TESTS
    # ==========================================

    async def test_quality_gate_dna_compliance_pass(self, mock_pm_agent):
        """Test DNA compliance quality gate passing."""
        deliverables = {
            "dna_analysis": {
                "pedagogical_value": True,
                "policy_to_practice": True,
                "time_respect": True,
                "holistic_thinking": True,
                "professional_tone": True
            }
        }
        
        result = mock_pm_agent._check_quality_gate("dna_compliance_verified", deliverables)
        assert result is True

    async def test_quality_gate_dna_compliance_fail(self, mock_pm_agent):
        """Test DNA compliance quality gate failing."""
        deliverables = {
            "dna_analysis": {
                "pedagogical_value": False,  # Failing principle
                "policy_to_practice": True,
                "time_respect": True,
                "holistic_thinking": True,
                "professional_tone": True
            }
        }
        
        result = mock_pm_agent._check_quality_gate("dna_compliance_verified", deliverables)
        assert result is False

    async def test_quality_gate_story_breakdown_pass(self, mock_pm_agent):
        """Test story breakdown quality gate passing."""
        deliverables = {
            "story_breakdown": {
                "feature_summary": {},
                "user_stories": [],
                "technical_requirements": {},
                "design_requirements": {},
                "acceptance_criteria": []
            }
        }
        
        result = mock_pm_agent._check_quality_gate("story_breakdown_complete", deliverables)
        assert result is True

    async def test_quality_gate_acceptance_criteria_pass(self, mock_pm_agent):
        """Test acceptance criteria quality gate passing."""
        deliverables = {
            "acceptance_criteria": [
                "Feature works correctly for Anna persona",
                "User can complete task within time limit", 
                "All validation rules are met properly"
            ]
        }
        
        result = mock_pm_agent._check_quality_gate("acceptance_criteria_clear", deliverables)
        assert result is True

    async def test_quality_gate_acceptance_criteria_fail_too_few(self, mock_pm_agent):
        """Test acceptance criteria quality gate failing with too few criteria."""
        deliverables = {
            "acceptance_criteria": [
                "Feature works",
                "User happy"
            ]
        }
        
        result = mock_pm_agent._check_quality_gate("acceptance_criteria_clear", deliverables)
        assert result is False

    async def test_quality_gate_acceptance_criteria_fail_too_short(self, mock_pm_agent):
        """Test acceptance criteria quality gate failing with too short criteria."""
        deliverables = {
            "acceptance_criteria": [
                "Feature works correctly for Anna persona",
                "Works",  # Too short
                "All validation rules are met properly"
            ]
        }
        
        result = mock_pm_agent._check_quality_gate("acceptance_criteria_clear", deliverables)
        assert result is False

    async def test_quality_gate_unknown_gate(self, mock_pm_agent):
        """Test handling of unknown quality gate."""
        deliverables = {}
        
        result = mock_pm_agent._check_quality_gate("unknown_gate", deliverables)
        assert result is True  # Unknown gates pass by default

    # ==========================================
    # GITHUB INTEGRATION TESTS
    # ==========================================

    async def test_process_github_issue_success(self, mock_pm_agent):
        """Test successful GitHub issue processing."""
        # Setup mocks
        mock_issue_data = {
            "number": 123,
            "title": "Test Feature",
            "body": "Feature description",
            "html_url": "https://github.com/jhonnyo88/diginativa-game/issues/123"
        }
        
        mock_contract = {
            "story_id": "STORY-GH-123",
            "input_requirements": {
                "required_data": {
                    "feature_description": "Test Feature\n\nFeature description",
                    "acceptance_criteria": [],
                    "user_persona": "Anna",
                    "priority_level": "medium"
                }
            }
        }
        
        mock_pm_agent.github_integration.fetch_issue_data = AsyncMock(return_value=mock_issue_data)
        mock_pm_agent.github_integration.convert_issue_to_contract = AsyncMock(return_value=mock_contract)
        
        # Mock execute_work to return success
        mock_result = Mock()
        mock_result.to_dict.return_value = {"status": "success"}
        mock_pm_agent.execute_work = AsyncMock(return_value=mock_result)
        
        result = await mock_pm_agent.process_github_issue("https://github.com/jhonnyo88/diginativa-game/issues/123")
        
        assert result["status"] == "success"
        mock_pm_agent.github_integration.fetch_issue_data.assert_called_once()
        mock_pm_agent.github_integration.convert_issue_to_contract.assert_called_once()

    async def test_process_github_issue_fetch_failure(self, mock_pm_agent):
        """Test GitHub issue processing with fetch failure."""
        mock_pm_agent.github_integration.fetch_issue_data.side_effect = ExternalServiceError(
            "GitHub API error", service_name="GitHub"
        )
        
        with pytest.raises(ExternalServiceError):
            await mock_pm_agent.process_github_issue("https://github.com/jhonnyo88/diginativa-game/issues/123")

    # ==========================================
    # DOCUMENTATION GENERATION TESTS
    # ==========================================

    async def test_save_story_documentation_success(self, mock_pm_agent, sample_feature_data, temp_docs_dir):
        """Test successful story documentation saving."""
        story_breakdown = {
            "feature_summary": {"title": "Test Feature"},
            "user_stories": [],
            "technical_requirements": {},
            "design_requirements": {}
        }
        
        acceptance_criteria = ["Test criteria 1", "Test criteria 2"]
        complexity_assessment = {"effort_points": 5, "technical_complexity": "Medium"}
        
        # Mock config to use temp directory
        mock_pm_agent.config = {"docs_path": temp_docs_dir}
        
        await mock_pm_agent._save_story_documentation(
            "STORY-TEST-001",
            sample_feature_data,
            story_breakdown,
            acceptance_criteria,
            complexity_assessment
        )
        
        # Verify files were created
        story_file = Path(temp_docs_dir) / "stories" / "STORY-TEST-001_description.md"
        analysis_file = Path(temp_docs_dir) / "analysis" / "STORY-TEST-001_feature_analysis.json"
        breakdown_file = Path(temp_docs_dir) / "breakdown" / "STORY-TEST-001_story_breakdown.json"
        
        assert story_file.exists()
        assert analysis_file.exists()
        assert breakdown_file.exists()
        
        # Verify content
        with open(story_file, 'r') as f:
            content = f.read()
            assert "STORY-TEST-001" in content
            assert "Anna" in content

    async def test_generate_story_markdown(self, mock_pm_agent, sample_feature_data):
        """Test story markdown generation."""
        acceptance_criteria = ["Test criteria 1", "Test criteria 2"]
        complexity_assessment = {
            "effort_points": 5,
            "technical_complexity": "Medium",
            "design_complexity": "Low",
            "estimated_duration_hours": 16
        }
        
        markdown = mock_pm_agent._generate_story_markdown(
            "STORY-TEST-001",
            sample_feature_data,
            acceptance_criteria,
            complexity_assessment
        )
        
        assert "# Story: STORY-TEST-001" in markdown
        assert "**Target User:** Anna" in markdown
        assert "**Priority:** HIGH" in markdown
        assert "**Maximum Duration:** 10 minutes" in markdown
        assert "- [ ] Test criteria 1" in markdown
        assert "**Estimated Effort:** 5 story points" in markdown

    # ==========================================
    # AGENT STATUS TESTS
    # ==========================================

    async def test_get_agent_status(self, mock_pm_agent):
        """Test agent status reporting."""
        status = mock_pm_agent.get_agent_status()
        
        assert status["agent_id"] == "test-pm-001"
        assert status["agent_type"] == "project_manager"
        assert "tools_status" in status
        assert "configuration" in status
        assert status["configuration"]["max_concurrent_stories"] == 3
        assert status["configuration"]["story_priority_threshold"] == "medium"

    # ==========================================
    # GAME DESIGNER CONTRACT CREATION TESTS
    # ==========================================

    async def test_create_game_designer_contract(self, mock_pm_agent, sample_feature_data):
        """Test Game Designer contract creation."""
        story_breakdown = {
            "feature_summary": {"title": "Test Feature"},
            "user_stories": [],
            "technical_requirements": {},
            "design_requirements": {}
        }
        
        acceptance_criteria = ["Test criteria 1", "Test criteria 2"]
        complexity_assessment = {"effort_points": 5}
        dna_analysis = {
            "pedagogical_value": True,
            "policy_to_practice": True,
            "time_respect": True,
            "holistic_thinking": True,
            "professional_tone": True
        }
        
        contract = mock_pm_agent._create_game_designer_contract(
            "STORY-TEST-001",
            sample_feature_data,
            story_breakdown,
            acceptance_criteria,
            complexity_assessment,
            dna_analysis
        )
        
        assert contract["target_agent"] == "game_designer"
        assert contract["source_agent"] == "project_manager"
        assert contract["story_id"] == "STORY-TEST-001"
        assert "input_requirements" in contract
        assert "output_specifications" in contract
        assert "quality_gates" in contract
        assert "handoff_criteria" in contract
        
        # Verify required deliverable files
        deliverable_files = contract["output_specifications"]["deliverable_files"]
        assert any("game_design.md" in file for file in deliverable_files)
        assert any("ux_specification.md" in file for file in deliverable_files)
        assert any("wireframes.png" in file for file in deliverable_files)

    # ==========================================
    # ERROR HANDLING TESTS
    # ==========================================

    async def test_contract_processing_malformed_contract(self, mock_pm_agent):
        """Test contract processing with malformed input contract."""
        malformed_contract = {
            "story_id": "STORY-TEST-001",
            # Missing required fields
        }
        
        with pytest.raises(BusinessLogicError):
            await mock_pm_agent.process_contract(malformed_contract)

    async def test_quality_gate_exception_handling(self, mock_pm_agent):
        """Test quality gate exception handling."""
        deliverables = None  # Will cause exception
        
        result = mock_pm_agent._check_quality_gate("dna_compliance_verified", deliverables)
        assert result is False

    # ==========================================
    # INTEGRATION TESTS
    # ==========================================

    async def test_full_workflow_integration(self, mock_pm_agent, sample_input_contract):
        """Test full PM Agent workflow integration."""
        # Setup all tool mocks for successful workflow
        mock_pm_agent.dna_compliance_checker.analyze_feature_compliance.return_value = {
            "compliant": True,
            "pedagogical_value": True,
            "policy_to_practice": True,
            "time_respect": True,
            "holistic_thinking": True,
            "professional_tone": True,
            "violations": [],
            "compliance_score": 85.0
        }
        
        mock_pm_agent.story_analyzer.create_story_breakdown.return_value = {
            "story_id": "STORY-GH-123",
            "feature_summary": {"title": "Policy Practice Feature"},
            "user_stories": [{"story": "As Anna, I want to practice policy application"}],
            "technical_requirements": {"frontend": {}, "backend": {}},
            "design_requirements": {"ui_components": []},
            "acceptance_criteria": ["User can select scenarios"]
        }
        
        mock_pm_agent.story_analyzer.generate_acceptance_criteria.return_value = [
            "User can select from multiple policy scenarios",
            "Each scenario provides clear context and background",
            "User receives immediate feedback on decisions",
            "Progress is tracked and saved",
            "Feature completes within 10 minutes"
        ]
        
        mock_pm_agent.story_analyzer.assess_complexity.return_value = {
            "overall_complexity": "Medium",
            "effort_points": 5,
            "technical_complexity": "Medium",
            "design_complexity": "Low",
            "estimated_duration_hours": 16,
            "confidence_level": 0.8
        }
        
        # Execute the workflow
        result = await mock_pm_agent.process_contract(sample_input_contract)
        
        # Verify the complete workflow
        assert result["target_agent"] == "game_designer"
        assert result["story_id"] == "STORY-GH-123"
        assert "input_requirements" in result
        assert "required_data" in result["input_requirements"]
        assert len(result["input_requirements"]["required_data"]["acceptance_criteria"]) == 5
        
        # Verify all tools were called
        mock_pm_agent.dna_compliance_checker.analyze_feature_compliance.assert_called_once()
        mock_pm_agent.story_analyzer.create_story_breakdown.assert_called_once()
        mock_pm_agent.story_analyzer.generate_acceptance_criteria.assert_called_once()
        mock_pm_agent.story_analyzer.assess_complexity.assert_called_once()

    # ==========================================
    # CONFIGURATION TESTS
    # ==========================================

    async def test_working_directories_creation(self, temp_docs_dir):
        """Test working directories are created correctly."""
        config = {"docs_path": temp_docs_dir}
        
        with patch.multiple(
            'modules.agents.project_manager.agent',
            GitHubIntegration=MagicMock(),
            StoryAnalyzer=MagicMock(),
            DNAComplianceChecker=MagicMock()
        ):
            agent = ProjectManagerAgent("test-pm-001", config)
            
            # Verify directories were created
            base_path = Path(temp_docs_dir)
            expected_dirs = ["stories", "analysis", "breakdown", "specs", "wireframes"]
            
            for directory in expected_dirs:
                assert (base_path / directory).exists()
                assert (base_path / directory).is_dir()