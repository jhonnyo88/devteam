"""
Test Quality Reviewer Agent implementation.

Tests the Quality Reviewer agent's core functionality including
quality analysis, deployment validation, and approval decisions.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from modules.agents.quality_reviewer.agent import QualityReviewerAgent
from modules.shared.exceptions import BusinessLogicError, DNAComplianceError


class TestQualityReviewerAgent:
    """Test suite for Quality Reviewer Agent."""
    
    @pytest.fixture
    def quality_reviewer_agent(self):
        """Create Quality Reviewer agent for testing."""
        return QualityReviewerAgent()
    
    @pytest.fixture
    def sample_qa_contract(self):
        """Sample QA contract from QA Tester agent."""
        return {
            "contract_version": "1.0",
            "story_id": "STORY-TEST-001",
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
            "input_requirements": {
                "required_data": {
                    "test_results": {
                        "coverage_percent": 96,
                        "tests_passed": 45,
                        "total_tests": 45,
                        "unit_tests": 30,
                        "integration_tests": 15
                    },
                    "performance_metrics": {
                        "lighthouse_score": 92,
                        "api_response_time_ms": 150,
                        "page_load_time_ms": 1800
                    },
                    "accessibility_audit": {
                        "wcag_compliance_percent": 94,
                        "violations": [],
                        "keyboard_accessible": True
                    },
                    "user_flow_validation": {
                        "flow_completion_rate": 96,
                        "user_satisfaction_score": 4.3,
                        "average_task_completion_minutes": 9,
                        "target_completion_minutes": 10
                    },
                    "code_quality_metrics": {
                        "typescript_errors": 0,
                        "eslint_violations": 2,
                        "complexity_score": 3.2,
                        "documentation_coverage_percent": 85
                    },
                    "pedagogical_effectiveness_score": 4.4,
                    "policy_practice_alignment_score": 4.2,
                    "time_efficiency_score": 4.5,
                    "holistic_design_score": 4.1,
                    "professional_tone_score": 4.3,
                    "architecture_compliance_percent": 92
                }
            }
        }
    
    @pytest.mark.asyncio
    async def test_quality_reviewer_initialization(self, quality_reviewer_agent):
        """Test Quality Reviewer agent initialization."""
        assert quality_reviewer_agent.agent_type == "quality_reviewer"
        assert quality_reviewer_agent.quality_scorer is not None
        assert quality_reviewer_agent.deployment_validator is not None
        assert quality_reviewer_agent.final_approver is not None
        assert quality_reviewer_agent.quality_thresholds["overall_score"] == 90
    
    @pytest.mark.asyncio
    async def test_extract_qa_data_success(self, quality_reviewer_agent, sample_qa_contract):
        """Test successful QA data extraction."""
        qa_data = quality_reviewer_agent._extract_qa_data(sample_qa_contract)
        
        assert "test_results" in qa_data
        assert "performance_metrics" in qa_data
        assert "accessibility_audit" in qa_data
        assert "user_flow_validation" in qa_data
        assert "code_quality_metrics" in qa_data
        assert qa_data["test_results"]["coverage_percent"] == 96
    
    @pytest.mark.asyncio
    async def test_extract_qa_data_missing_field(self, quality_reviewer_agent):
        """Test QA data extraction with missing required field."""
        incomplete_contract = {
            "input_requirements": {
                "required_data": {
                    "test_results": {"coverage_percent": 90},
                    # Missing other required fields
                }
            }
        }
        
        with pytest.raises(BusinessLogicError) as exc_info:
            quality_reviewer_agent._extract_qa_data(incomplete_contract)
        
        assert "Missing required QA field" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_quality_analysis_high_quality(self, quality_reviewer_agent, sample_qa_contract):
        """Test quality analysis with high-quality QA data."""
        qa_data = quality_reviewer_agent._extract_qa_data(sample_qa_contract)
        
        # Mock the quality scorer methods
        with patch.object(quality_reviewer_agent.quality_scorer, 'analyze_test_quality', 
                         return_value={"score": 95, "issues": []}):
            with patch.object(quality_reviewer_agent.quality_scorer, 'analyze_performance',
                             return_value={"score": 92, "issues": []}):
                with patch.object(quality_reviewer_agent.quality_scorer, 'analyze_accessibility',
                                 return_value={"score": 94, "issues": []}):
                    with patch.object(quality_reviewer_agent.quality_scorer, 'analyze_user_experience',
                                     return_value={"score": 90, "issues": []}):
                        with patch.object(quality_reviewer_agent.quality_scorer, 'analyze_code_quality',
                                         return_value={"score": 88, "issues": []}):
                            with patch.object(quality_reviewer_agent.quality_scorer, 'analyze_dna_compliance',
                                             return_value={"score": 87, "issues": []}):
                                with patch.object(quality_reviewer_agent.quality_scorer, 'calculate_overall_score',
                                                 return_value=91.2):
                                    with patch.object(quality_reviewer_agent.quality_scorer, 'identify_quality_issues',
                                                     return_value=[]):
                                        
                                        analysis = await quality_reviewer_agent._perform_quality_analysis(qa_data)
                                        
                                        assert analysis["overall_score"] == 91.2
                                        assert analysis["test_quality"]["score"] == 95
                                        assert analysis["performance"]["score"] == 92
                                        assert len(analysis["quality_issues"]) == 0
    
    @pytest.mark.asyncio
    async def test_deployment_validation_ready(self, quality_reviewer_agent, sample_qa_contract):
        """Test deployment readiness validation for ready deployment."""
        qa_data = quality_reviewer_agent._extract_qa_data(sample_qa_contract)
        quality_analysis = {
            "performance": {"lighthouse_score": 92, "api_response_time_ms": 150},
            "accessibility": {"wcag_compliance_percent": 94, "violations_count": 0, "keyboard_accessible": True},
            "dna_compliance": {"design_principles_avg": 4.3, "architecture_principles": {"compliance_percent": 92}},
            "test_quality": {"coverage_percent": 96, "pass_rate": 100}
        }
        
        # Mock the deployment validator methods
        with patch.object(quality_reviewer_agent.deployment_validator, 'validate_performance_requirements',
                         return_value={"passed": True, "issues": []}):
            with patch.object(quality_reviewer_agent.deployment_validator, 'validate_security_requirements',
                             return_value={"passed": True, "issues": []}):
                with patch.object(quality_reviewer_agent.deployment_validator, 'validate_accessibility_requirements',
                                 return_value={"passed": True, "issues": []}):
                    with patch.object(quality_reviewer_agent.deployment_validator, 'validate_dna_requirements',
                                     return_value={"passed": True, "issues": []}):
                        with patch.object(quality_reviewer_agent.deployment_validator, 'validate_test_coverage_requirements',
                                         return_value={"passed": True, "issues": []}):
                            with patch.object(quality_reviewer_agent.deployment_validator, 'validate_compatibility_requirements',
                                             return_value={"passed": True, "issues": []}):
                                
                                readiness = await quality_reviewer_agent._validate_deployment_readiness(qa_data, quality_analysis)
                                
                                assert readiness["deployment_ready"] is True
                                assert len(readiness["blocking_issues"]) == 0
                                assert readiness["readiness_score"] == 100
    
    @pytest.mark.asyncio
    async def test_approval_decision_approved(self, quality_reviewer_agent):
        """Test approval decision for high-quality feature."""
        quality_analysis = {
            "overall_score": 91.5,
            "dna_compliance": {"score": 87},
            "quality_issues": []
        }
        deployment_readiness = {
            "deployment_ready": True,
            "readiness_score": 95,
            "blocking_issues": []
        }
        
        # Mock the final approver
        with patch.object(quality_reviewer_agent.final_approver, 'make_approval_decision',
                         return_value={
                             "approved": True,
                             "reasoning": "All quality criteria met",
                             "recommendations": ["Deploy to production"],
                             "blocking_issues": []
                         }):
            
            decision = await quality_reviewer_agent._make_approval_decision(quality_analysis, deployment_readiness)
            
            assert decision["approved"] is True
            assert "decision_timestamp" in decision
            assert decision["reviewer_agent"] == "quality_reviewer"
    
    @pytest.mark.asyncio
    async def test_process_contract_full_approval_flow(self, quality_reviewer_agent, sample_qa_contract):
        """Test full contract processing flow with approval."""
        # Mock all the dependencies to return successful results
        with patch.object(quality_reviewer_agent, '_perform_quality_analysis',
                         return_value={
                             "overall_score": 91.5,
                             "dna_compliance": {
                                 "design_principles": {
                                     "pedagogical_value": 4.5,
                                     "policy_to_practice": 4.3,
                                     "time_respect": 4.7,
                                     "holistic_thinking": 4.2,
                                     "professional_tone": 4.4
                                 },
                                 "architecture_principles": {"compliance_percent": 94}
                             },
                             "quality_issues": []
                         }):
            with patch.object(quality_reviewer_agent, '_validate_deployment_readiness',
                             return_value={"deployment_ready": True, "blocking_issues": []}):
                with patch.object(quality_reviewer_agent, '_make_approval_decision',
                                 return_value={
                                     "approved": True,
                                     "reasoning": "Quality standards met",
                                     "recommendations": ["Deploy to production"]
                                 }):
                    
                    result = await quality_reviewer_agent.process_contract(sample_qa_contract)
                    
                    assert result["contract_version"] == "1.0"
                    assert result["story_id"] == "STORY-TEST-001"
                    assert result["source_agent"] == "quality_reviewer"
                    assert result["target_agent"] == "deployment"
                    assert "quality_analysis" in result["input_requirements"]["required_data"]
                    assert result["input_requirements"]["required_data"]["approval_status"] is True
    
    @pytest.mark.asyncio
    async def test_process_contract_rejection_flow(self, quality_reviewer_agent, sample_qa_contract):
        """Test full contract processing flow with rejection."""
        # Mock dependencies to return rejection results
        with patch.object(quality_reviewer_agent, '_perform_quality_analysis',
                         return_value={
                             "overall_score": 75.0,
                             "dna_compliance": {
                                 "design_principles": {
                                     "pedagogical_value": 3.0,
                                     "policy_to_practice": 3.2,
                                     "time_respect": 2.8,
                                     "holistic_thinking": 3.1,
                                     "professional_tone": 3.3
                                 },
                                 "architecture_principles": {"compliance_percent": 65}
                             },
                             "quality_issues": [{"type": "critical", "blocking": True}]
                         }):
            with patch.object(quality_reviewer_agent, '_validate_deployment_readiness',
                             return_value={"deployment_ready": False, "blocking_issues": ["Performance issues"]}):
                with patch.object(quality_reviewer_agent, '_make_approval_decision',
                                 return_value={
                                     "approved": False,
                                     "reasoning": "Quality standards not met",
                                     "recommendations": ["Fix issues and resubmit"],
                                     "blocking_issues": ["Performance issues"]
                                 }):
                    
                    result = await quality_reviewer_agent.process_contract(sample_qa_contract)
                    
                    assert result["target_agent"] == "developer"
                    assert result["input_requirements"]["required_data"]["approval_status"] is False
                    assert len(result["input_requirements"]["required_data"]["blocking_issues"]) > 0
    
    @pytest.mark.asyncio
    async def test_quality_gate_validation(self, quality_reviewer_agent):
        """Test quality gate validation."""
        deliverables = {
            "quality_analysis": {"overall_score": 91.5},
            "deployment_readiness": {
                "deployment_ready": True,
                "readiness_checks": {},
                "readiness_score": 95
            },
            "approval_status": True,
            "approval_reasoning": "All criteria met",
            "quality_score": 91.5
        }
        
        # Test individual quality gates
        assert await quality_reviewer_agent.validate_quality_gate("final_quality_score_calculated", deliverables) is True
        assert await quality_reviewer_agent.validate_quality_gate("deployment_readiness_validated", deliverables) is True
        assert await quality_reviewer_agent.validate_quality_gate("approval_decision_made", deliverables) is True
        assert await quality_reviewer_agent.validate_quality_gate("documentation_complete", deliverables) is True
        
        # Test unknown gate (should pass with warning)
        assert await quality_reviewer_agent.validate_quality_gate("unknown_gate", deliverables) is True
    
    @pytest.mark.asyncio
    async def test_quality_gate_validation_failures(self, quality_reviewer_agent):
        """Test quality gate validation with failures."""
        incomplete_deliverables = {
            "quality_analysis": {},  # Missing overall_score
            "approval_status": None,  # Invalid approval status
        }
        
        # Test failed quality gates
        assert await quality_reviewer_agent.validate_quality_gate("final_quality_score_calculated", incomplete_deliverables) is False
        assert await quality_reviewer_agent.validate_quality_gate("approval_decision_made", incomplete_deliverables) is False
        assert await quality_reviewer_agent.validate_quality_gate("deployment_readiness_validated", incomplete_deliverables) is False
        assert await quality_reviewer_agent.validate_quality_gate("documentation_complete", incomplete_deliverables) is False
    
    @pytest.mark.asyncio
    async def test_error_handling_in_contract_processing(self, quality_reviewer_agent):
        """Test error handling during contract processing."""
        invalid_contract = {
            "story_id": "STORY-TEST-001",
            "input_requirements": {"required_data": {}}  # Missing required QA fields
        }
        
        with pytest.raises(BusinessLogicError) as exc_info:
            await quality_reviewer_agent.process_contract(invalid_contract)
        
        assert "Missing required QA field" in str(exc_info.value)
        assert exc_info.value.business_rule == "qa_data_completeness"