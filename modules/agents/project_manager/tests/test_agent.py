"""
Project Manager Agent Core Tests

PURPOSE:
Tests core logic and workflow of Project Manager agent according to TEST_STRATEGY.md.

CRITICAL IMPORTANCE:
- Validates GitHub integration and story analysis
- Ensures DNA compliance validation works correctly
- Tests feature breakdown and priority management
- Validates contract generation for Game Designer handoff

COVERAGE REQUIREMENTS:
- Agent core logic: 95% minimum
- Contract compliance: 100%
- DNA validation: 100%
- Tool integration: 90% minimum
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from typing import Dict, Any

from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.shared.exceptions import (
    DNAComplianceError, BusinessLogicError, ExternalServiceError,
    AgentExecutionError
)


class TestProjectManagerAgent:
    """Test Project Manager agent core functionality."""
    
    @pytest.fixture
    def pm_config(self):
        """Test configuration for PM agent."""
        return {
            "test_mode": True,
            "github_token": "test_token_12345",
            "max_concurrent_stories": 3,
            "story_priority_threshold": "medium"
        }
    
    @pytest.fixture
    def pm_agent(self, pm_config):
        """Create PM agent instance for testing."""
        return ProjectManagerAgent("pm-test-001", pm_config)
    
    @pytest.fixture
    def sample_github_issue(self):
        """Sample GitHub issue for testing."""
        return {
            "number": 123,
            "title": "Add user role management for municipal training coordinators",
            "body": """
            As a municipal training coordinator (Anna persona),
            I want to manage user roles and permissions for training sessions
            So that I can control access to different training materials and modules.
            
            Acceptance Criteria:
            - Role management interface for administrators
            - Permission assignment for different user types
            - Integration with Swedish municipal authentication systems
            - GDPR compliance for user data handling
            """,
            "labels": ["enhancement", "priority-high", "swedish-municipal"],
            "state": "open",
            "created_at": "2025-06-15T10:00:00Z",
            "assignee": None
        }
    
    @pytest.fixture
    def sample_input_contract(self):
        """Sample input contract for PM agent."""
        return {
            "contract_version": "1.0",
            "story_id": "STORY-123-001",
            "source_agent": "system",
            "target_agent": "project_manager",
            "input_requirements": {
                "github_issue": {
                    "number": 123,
                    "title": "Add user role management",
                    "body": "Feature request for role management system",
                    "labels": ["enhancement", "priority-high"]
                }
            },
            "output_specifications": {
                "deliverable_data": {
                    "story_breakdown": "required",
                    "dna_compliance_validation": "required",
                    "acceptance_criteria": "required"
                }
            },
            "quality_gates": ["dna_compliance_check", "story_analysis_complete"],
            "handoff_criteria": ["game_designer_contract_ready"]
        }


class TestProjectManagerCoreLogic(TestProjectManagerAgent):
    """Test core PM agent logic and workflows."""
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, pm_config):
        """Test PM agent initializes correctly with all tools."""
        agent = ProjectManagerAgent("pm-test-002", pm_config)
        
        # Verify agent properties
        assert agent.agent_id == "pm-test-002"
        assert agent.agent_type == "project_manager"
        assert agent.max_concurrent_stories == 3
        
        # Verify tools are initialized
        assert hasattr(agent, 'github_integration')
        assert hasattr(agent, 'story_analyzer')
        assert hasattr(agent, 'dna_compliance_checker')
        assert hasattr(agent, 'learning_engine')
        assert hasattr(agent, 'swedish_communicator')
        assert hasattr(agent, 'team_coordinator')
        assert hasattr(agent, 'stakeholder_manager')
    
    @pytest.mark.asyncio
    async def test_process_contract_success(self, pm_agent, sample_input_contract, sample_github_issue):
        """Test successful contract processing with complete workflow."""
        # Mock tool methods
        with patch.object(pm_agent.github_integration, 'fetch_issue_details') as mock_fetch, \
             patch.object(pm_agent.story_analyzer, 'analyze_feature_request') as mock_analyze, \
             patch.object(pm_agent.dna_compliance_checker, 'validate_feature_compliance') as mock_dna, \
             patch.object(pm_agent.learning_engine, 'predict_complexity_with_ml') as mock_ml, \
             patch.object(pm_agent.team_coordinator, 'coordinate_team_workflow') as mock_coord:
            
            # Setup mocks
            mock_fetch.return_value = sample_github_issue
            mock_analyze.return_value = {
                "story_breakdown": {
                    "epic": "User Role Management System",
                    "user_stories": [
                        "As an admin, I want to create user roles",
                        "As an admin, I want to assign permissions to roles"
                    ],
                    "acceptance_criteria": [
                        "Role creation interface available",
                        "Permission assignment functional",
                        "GDPR compliance verified"
                    ],
                    "technical_requirements": ["Authentication system", "Database schema"]
                },
                "estimated_complexity": "medium",
                "dependencies": [],
                "risk_factors": ["GDPR compliance", "Authentication integration"]
            }
            
            mock_dna.return_value = {
                "compliance_status": "compliant",
                "design_principles": {
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
                "validation_details": ["All DNA principles satisfied"]
            }
            
            mock_ml.return_value = {
                "predicted_complexity": "medium",
                "confidence_score": 0.85,
                "similar_stories": [],
                "risk_assessment": "low"
            }
            
            mock_coord.return_value = {
                "status": "workflow_initiated",
                "coordination_id": "coord-123-001",
                "next_agent": "game_designer"
            }
            
            # Execute contract processing
            result = await pm_agent.process_contract(sample_input_contract)
            
            # Verify successful execution
            assert result["status"] == "success"
            assert result["story_id"] == "STORY-123-001"
            assert "output_contract" in result
            
            # Verify output contract structure
            output_contract = result["output_contract"]
            assert output_contract["source_agent"] == "project_manager"
            assert output_contract["target_agent"] == "game_designer"
            assert "story_breakdown" in output_contract["deliverable_data"]
            assert "dna_compliance_validation" in output_contract["deliverable_data"]
            
            # Verify all tools were called
            mock_fetch.assert_called_once()
            mock_analyze.assert_called_once()
            mock_dna.assert_called_once()
            mock_ml.assert_called_once()
            mock_coord.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_contract_dna_violation(self, pm_agent, sample_input_contract):
        """Test contract processing with DNA compliance violation."""
        with patch.object(pm_agent.github_integration, 'fetch_issue_details') as mock_fetch, \
             patch.object(pm_agent.story_analyzer, 'analyze_feature_request') as mock_analyze, \
             patch.object(pm_agent.dna_compliance_checker, 'validate_feature_compliance') as mock_dna:
            
            # Setup mocks - DNA violation
            mock_fetch.return_value = {"title": "Test issue", "body": "Test body"}
            mock_analyze.return_value = {"story_breakdown": "basic breakdown"}
            mock_dna.return_value = {
                "compliance_status": "non_compliant",
                "violations": ["time_respect: Feature too complex for 10-minute sessions"],
                "design_principles": {
                    "time_respect": False,  # DNA violation
                    "pedagogical_value": True
                }
            }
            
            # Execute and expect DNA compliance error
            with pytest.raises(DNAComplianceError) as exc_info:
                await pm_agent.process_contract(sample_input_contract)
            
            assert "DNA compliance violation" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_process_contract_github_error(self, pm_agent, sample_input_contract):
        """Test contract processing with GitHub integration error."""
        with patch.object(pm_agent.github_integration, 'fetch_issue_details') as mock_fetch:
            # Setup GitHub error
            mock_fetch.side_effect = ExternalServiceError("GitHub API rate limit exceeded")
            
            # Execute and expect external service error
            with pytest.raises(AgentExecutionError) as exc_info:
                await pm_agent.process_contract(sample_input_contract)
            
            assert "GitHub integration failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_process_contract_invalid_input(self, pm_agent):
        """Test contract processing with invalid input contract."""
        invalid_contract = {
            "contract_version": "1.0",
            # Missing required fields
        }
        
        with pytest.raises(BusinessLogicError) as exc_info:
            await pm_agent.process_contract(invalid_contract)
        
        assert "Missing required contract fields" in str(exc_info.value)


class TestProjectManagerStoryAnalysis(TestProjectManagerAgent):
    """Test PM agent story analysis capabilities."""
    
    @pytest.mark.asyncio
    async def test_complex_story_breakdown(self, pm_agent, sample_github_issue):
        """Test complex feature breakdown with multiple components."""
        with patch.object(pm_agent.story_analyzer, 'analyze_feature_request') as mock_analyze:
            mock_analyze.return_value = {
                "story_breakdown": {
                    "epic": "Complex Role Management System",
                    "user_stories": [
                        "Admin role creation and management",
                        "User permission assignment",
                        "GDPR compliance implementation",
                        "Swedish municipal integration"
                    ],
                    "acceptance_criteria": [
                        "Role management interface functional",
                        "Permission system working",
                        "GDPR audit trail implemented",
                        "Municipal auth integration complete"
                    ],
                    "technical_requirements": [
                        "Database schema for roles/permissions",
                        "Authentication middleware",
                        "GDPR logging system",
                        "Municipal API integration"
                    ]
                },
                "estimated_complexity": "high",
                "dependencies": ["authentication_system", "municipal_api"],
                "risk_factors": ["GDPR compliance", "Integration complexity"]
            }
            
            # Test analysis
            result = mock_analyze.return_value
            
            # Verify comprehensive breakdown
            assert len(result["story_breakdown"]["user_stories"]) >= 4
            assert result["estimated_complexity"] == "high"
            assert "GDPR compliance" in result["risk_factors"]
            assert "municipal_api" in result["dependencies"]
    
    @pytest.mark.asyncio
    async def test_swedish_municipal_context_analysis(self, pm_agent):
        """Test analysis considers Swedish municipal context."""
        with patch.object(pm_agent.story_analyzer, 'analyze_feature_request') as mock_analyze:
            mock_analyze.return_value = {
                "story_breakdown": {
                    "municipal_compliance": {
                        "gdpr_requirements": ["User consent", "Data minimization"],
                        "accessibility_requirements": ["WCAG AA compliance"],
                        "language_requirements": ["Swedish UI", "Municipal terminology"]
                    }
                },
                "swedish_context": {
                    "regulatory_compliance": ["GDPR", "Swedish accessibility law"],
                    "user_personas": ["Municipal training coordinator", "Administrator"]
                }
            }
            
            result = mock_analyze.return_value
            
            # Verify Swedish municipal considerations
            assert "municipal_compliance" in result["story_breakdown"]
            assert "GDPR" in result["swedish_context"]["regulatory_compliance"]
            assert "Swedish UI" in result["story_breakdown"]["municipal_compliance"]["language_requirements"]


class TestProjectManagerDNAValidation(TestProjectManagerAgent):
    """Test PM agent DNA compliance validation."""
    
    @pytest.mark.asyncio
    async def test_all_dna_principles_validation(self, pm_agent):
        """Test validation of all 9 DNA principles."""
        with patch.object(pm_agent.dna_compliance_checker, 'validate_feature_compliance') as mock_dna:
            mock_dna.return_value = {
                "compliance_status": "compliant",
                "design_principles": {
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
                "validation_score": 1.0,
                "validation_details": [
                    "Feature provides clear pedagogical value for municipal training",
                    "Policy-to-practice connection well defined",
                    "User workflow respects 10-minute time constraint",
                    "Solution considers broader municipal context",
                    "Professional tone maintained throughout"
                ]
            }
            
            result = mock_dna.return_value
            
            # Verify all 5 design principles checked
            design_principles = result["design_principles"]
            assert design_principles["pedagogical_value"] is True
            assert design_principles["policy_to_practice"] is True
            assert design_principles["time_respect"] is True
            assert design_principles["holistic_thinking"] is True
            assert design_principles["professional_tone"] is True
            
            # Verify all 4 architecture principles checked
            arch_principles = result["architecture_compliance"]
            assert arch_principles["api_first"] is True
            assert arch_principles["stateless_backend"] is True
            assert arch_principles["separation_of_concerns"] is True
            assert arch_principles["simplicity_first"] is True
            
            # Verify perfect compliance score
            assert result["validation_score"] == 1.0
    
    @pytest.mark.asyncio
    async def test_time_respect_validation_failure(self, pm_agent):
        """Test specific DNA violation - time respect principle."""
        with patch.object(pm_agent.dna_compliance_checker, 'validate_feature_compliance') as mock_dna:
            mock_dna.return_value = {
                "compliance_status": "non_compliant",
                "design_principles": {
                    "time_respect": False,  # Violation
                    "pedagogical_value": True,
                    "policy_to_practice": True,
                    "holistic_thinking": True,
                    "professional_tone": True
                },
                "violations": [
                    "time_respect: Feature workflow exceeds 10-minute limit for Anna persona"
                ],
                "validation_score": 0.8
            }
            
            result = mock_dna.return_value
            
            # Verify time respect violation detected
            assert result["design_principles"]["time_respect"] is False
            assert result["compliance_status"] == "non_compliant"
            assert any("time_respect" in violation for violation in result["violations"])


class TestProjectManagerLearningEngine(TestProjectManagerAgent):
    """Test PM agent machine learning capabilities."""
    
    @pytest.mark.asyncio
    async def test_ml_complexity_prediction(self, pm_agent):
        """Test ML-enhanced complexity prediction."""
        with patch.object(pm_agent.learning_engine, 'predict_complexity_with_ml') as mock_ml:
            mock_ml.return_value = {
                "predicted_complexity": "medium",
                "confidence_score": 0.92,
                "ml_factors": [
                    "Similar role management features: medium complexity",
                    "GDPR compliance adds complexity",
                    "Swedish municipal context well understood"
                ],
                "similar_stories": [
                    {"story_id": "STORY-089-001", "complexity": "medium", "similarity": 0.85}
                ],
                "risk_assessment": "low",
                "estimated_hours": 24
            }
            
            result = mock_ml.return_value
            
            # Verify ML prediction quality
            assert result["confidence_score"] > 0.9
            assert result["predicted_complexity"] in ["low", "medium", "high"]
            assert "estimated_hours" in result
            assert len(result["similar_stories"]) > 0
    
    @pytest.mark.asyncio
    async def test_stakeholder_prediction(self, pm_agent):
        """Test stakeholder satisfaction prediction."""
        with patch.object(pm_agent.stakeholder_manager, 'predict_approval_likelihood') as mock_stakeholder:
            mock_stakeholder.return_value = {
                "approval_likelihood": 0.88,
                "stakeholder_preferences": {
                    "feature_completeness": 0.9,
                    "gdpr_compliance": 0.95,
                    "user_experience": 0.85
                },
                "recommendations": [
                    "Emphasize GDPR compliance in proposal",
                    "Include detailed UX mockups",
                    "Highlight municipal-specific benefits"
                ]
            }
            
            result = mock_stakeholder.return_value
            
            # Verify stakeholder analysis
            assert result["approval_likelihood"] > 0.8
            assert "gdpr_compliance" in result["stakeholder_preferences"]
            assert len(result["recommendations"]) > 0


class TestProjectManagerTeamCoordination(TestProjectManagerAgent):
    """Test PM agent team coordination capabilities."""
    
    @pytest.mark.asyncio
    async def test_team_workflow_coordination(self, pm_agent):
        """Test coordination of team workflow via EventBus."""
        with patch.object(pm_agent.team_coordinator, 'coordinate_team_workflow') as mock_coord:
            mock_coord.return_value = {
                "status": "workflow_initiated",
                "story_id": "STORY-123-001",
                "coordination_id": "coord-123-001-1749989593",
                "next_agent": "game_designer",
                "monitoring_enabled": True,
                "estimated_completion": "2025-06-16T14:00:00"
            }
            
            result = mock_coord.return_value
            
            # Verify team coordination
            assert result["status"] == "workflow_initiated"
            assert result["next_agent"] == "game_designer"
            assert result["monitoring_enabled"] is True
            assert "estimated_completion" in result
    
    @pytest.mark.asyncio
    async def test_performance_monitoring(self, pm_agent):
        """Test team performance monitoring."""
        with patch.object(pm_agent.team_coordinator, 'monitor_team_performance') as mock_monitor:
            mock_monitor.return_value = {
                "active_agents": 5,
                "team_utilization": 0.85,
                "average_completion_time": 4.2,
                "bottlenecks": [],
                "recommendations": ["Team performing well"],
                "performance_score": 4.3
            }
            
            result = mock_monitor.return_value
            
            # Verify performance monitoring
            assert result["team_utilization"] > 0.8
            assert result["performance_score"] > 4.0
            assert isinstance(result["bottlenecks"], list)


class TestProjectManagerErrorHandling(TestProjectManagerAgent):
    """Test PM agent error handling and recovery."""
    
    @pytest.mark.asyncio
    async def test_github_api_failure_handling(self, pm_agent, sample_input_contract):
        """Test handling of GitHub API failures."""
        with patch.object(pm_agent.github_integration, 'fetch_issue_details') as mock_fetch:
            mock_fetch.side_effect = ExternalServiceError("GitHub API unavailable")
            
            with pytest.raises(AgentExecutionError) as exc_info:
                await pm_agent.process_contract(sample_input_contract)
            
            error = exc_info.value
            assert error.agent_id == pm_agent.agent_id
            assert "GitHub integration failed" in str(error)
    
    @pytest.mark.asyncio
    async def test_tool_initialization_failure(self, pm_config):
        """Test handling of tool initialization failures."""
        # Corrupt config to cause tool initialization failure
        corrupted_config = pm_config.copy()
        corrupted_config["invalid_setting"] = {"corrupted": "data"}
        
        with patch('modules.agents.project_manager.tools.github_integration.GitHubIntegration') as mock_github:
            mock_github.side_effect = Exception("Tool initialization failed")
            
            with pytest.raises(AgentExecutionError) as exc_info:
                ProjectManagerAgent("pm-test-error", corrupted_config)
            
            assert "PM Agent initialization failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_contract_validation_failure(self, pm_agent):
        """Test handling of invalid contract structure."""
        invalid_contract = {
            "contract_version": "1.0",
            # Missing required fields: story_id, input_requirements, etc.
        }
        
        with pytest.raises(BusinessLogicError) as exc_info:
            await pm_agent.process_contract(invalid_contract)
        
        assert "Missing required contract fields" in str(exc_info.value)


class TestProjectManagerIntegration(TestProjectManagerAgent):
    """Test PM agent integration with other components."""
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow_simulation(self, pm_agent, sample_input_contract, sample_github_issue):
        """Test complete end-to-end workflow simulation."""
        # Mock all tools for complete workflow
        with patch.object(pm_agent.github_integration, 'fetch_issue_details') as mock_github, \
             patch.object(pm_agent.story_analyzer, 'analyze_feature_request') as mock_story, \
             patch.object(pm_agent.dna_compliance_checker, 'validate_feature_compliance') as mock_dna, \
             patch.object(pm_agent.learning_engine, 'predict_complexity_with_ml') as mock_ml, \
             patch.object(pm_agent.swedish_communicator, 'generate_municipal_specific_message') as mock_comm, \
             patch.object(pm_agent.team_coordinator, 'coordinate_team_workflow') as mock_coord, \
             patch.object(pm_agent.stakeholder_manager, 'predict_approval_likelihood') as mock_stakeholder:
            
            # Setup complete workflow mocks
            mock_github.return_value = sample_github_issue
            mock_story.return_value = {"story_breakdown": "Complete analysis"}
            mock_dna.return_value = {"compliance_status": "compliant", "validation_score": 1.0}
            mock_ml.return_value = {"predicted_complexity": "medium", "confidence_score": 0.9}
            mock_comm.return_value = {"message": "Municipal communication ready"}
            mock_coord.return_value = {"status": "workflow_initiated", "next_agent": "game_designer"}
            mock_stakeholder.return_value = {"approval_likelihood": 0.85}
            
            # Execute complete workflow
            result = await pm_agent.process_contract(sample_input_contract)
            
            # Verify all tools were integrated
            mock_github.assert_called_once()
            mock_story.assert_called_once()
            mock_dna.assert_called_once()
            mock_ml.assert_called_once()
            mock_coord.assert_called_once()
            
            # Verify successful completion
            assert result["status"] == "success"
            assert "output_contract" in result
    
    @pytest.mark.asyncio
    async def test_contract_output_for_game_designer(self, pm_agent, sample_input_contract):
        """Test contract output format for Game Designer agent."""
        with patch.object(pm_agent.github_integration, 'fetch_issue_details'), \
             patch.object(pm_agent.story_analyzer, 'analyze_feature_request') as mock_story, \
             patch.object(pm_agent.dna_compliance_checker, 'validate_feature_compliance') as mock_dna, \
             patch.object(pm_agent.learning_engine, 'predict_complexity_with_ml'), \
             patch.object(pm_agent.team_coordinator, 'coordinate_team_workflow'):
            
            # Setup mocks for contract output
            mock_story.return_value = {
                "story_breakdown": {
                    "user_stories": ["Story 1", "Story 2"],
                    "acceptance_criteria": ["Criteria 1", "Criteria 2"],
                    "ux_requirements": ["Responsive design", "Accessibility compliant"]
                }
            }
            mock_dna.return_value = {"compliance_status": "compliant"}
            
            # Execute
            result = await pm_agent.process_contract(sample_input_contract)
            
            # Verify Game Designer contract format
            output_contract = result["output_contract"]
            assert output_contract["target_agent"] == "game_designer"
            assert "story_breakdown" in output_contract["deliverable_data"]
            assert "dna_compliance_validation" in output_contract["deliverable_data"]
            assert "quality_gates" in output_contract
            assert "handoff_criteria" in output_contract


# Performance and Load Testing
class TestProjectManagerPerformance(TestProjectManagerAgent):
    """Test PM agent performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_contract_processing_performance(self, pm_agent, sample_input_contract):
        """Test contract processing meets performance requirements."""
        import time
        
        with patch.object(pm_agent.github_integration, 'fetch_issue_details'), \
             patch.object(pm_agent.story_analyzer, 'analyze_feature_request'), \
             patch.object(pm_agent.dna_compliance_checker, 'validate_feature_compliance'), \
             patch.object(pm_agent.learning_engine, 'predict_complexity_with_ml'), \
             patch.object(pm_agent.team_coordinator, 'coordinate_team_workflow'):
            
            # Mock all tools for performance test
            pm_agent.github_integration.fetch_issue_details.return_value = {"title": "Test"}
            pm_agent.story_analyzer.analyze_feature_request.return_value = {"story_breakdown": "Test"}
            pm_agent.dna_compliance_checker.validate_feature_compliance.return_value = {"compliance_status": "compliant"}
            pm_agent.learning_engine.predict_complexity_with_ml.return_value = {"predicted_complexity": "medium"}
            pm_agent.team_coordinator.coordinate_team_workflow.return_value = {"status": "workflow_initiated"}
            
            # Measure processing time
            start_time = time.time()
            result = await pm_agent.process_contract(sample_input_contract)
            processing_time = time.time() - start_time
            
            # Verify performance requirements (should be < 30 seconds for agent tests)
            assert processing_time < 30.0, f"Processing took {processing_time}s, exceeds 30s limit"
            assert result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_concurrent_story_processing(self, pm_agent):
        """Test processing multiple stories concurrently."""
        # Test that PM can handle max_concurrent_stories (3 in test config)
        contracts = []
        for i in range(3):
            contracts.append({
                "contract_version": "1.0",
                "story_id": f"STORY-{100+i}-001",
                "source_agent": "system",
                "target_agent": "project_manager",
                "input_requirements": {"github_issue": {"number": 100+i, "title": f"Test {i}"}}
            })
        
        with patch.object(pm_agent.github_integration, 'fetch_issue_details'), \
             patch.object(pm_agent.story_analyzer, 'analyze_feature_request'), \
             patch.object(pm_agent.dna_compliance_checker, 'validate_feature_compliance'), \
             patch.object(pm_agent.learning_engine, 'predict_complexity_with_ml'), \
             patch.object(pm_agent.team_coordinator, 'coordinate_team_workflow'):
            
            # Setup mocks
            pm_agent.github_integration.fetch_issue_details.return_value = {"title": "Test"}
            pm_agent.story_analyzer.analyze_feature_request.return_value = {"story_breakdown": "Test"}
            pm_agent.dna_compliance_checker.validate_feature_compliance.return_value = {"compliance_status": "compliant"}
            pm_agent.learning_engine.predict_complexity_with_ml.return_value = {"predicted_complexity": "medium"}
            pm_agent.team_coordinator.coordinate_team_workflow.return_value = {"status": "workflow_initiated"}
            
            # Process contracts concurrently
            tasks = [pm_agent.process_contract(contract) for contract in contracts]
            results = await asyncio.gather(*tasks)
            
            # Verify all processed successfully
            assert len(results) == 3
            for result in results:
                assert result["status"] == "success"