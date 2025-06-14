"""
Test Client Communication functionality for Quality Reviewer Agent.

Tests the ClientCommunicator tool and its integration with Quality Reviewer
for professional Swedish municipal communication workflows.
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from ..tools.client_communicator import ClientCommunicator
from ..agent import QualityReviewerAgent


class TestClientCommunicator:
    """Test suite for ClientCommunicator tool."""
    
    @pytest.fixture
    def client_communicator(self):
        """Create ClientCommunicator for testing."""
        return ClientCommunicator()
    
    @pytest.fixture
    def sample_quality_analysis(self):
        """Sample quality analysis data."""
        return {
            "overall_score": 92.5,
            "test_quality": {"score": 95, "issues": []},
            "performance": {"score": 90, "lighthouse_score": 92, "api_response_time_ms": 150},
            "accessibility": {"score": 94, "wcag_compliance_percent": 95, "violations_count": 0},
            "user_experience": {"score": 88, "flow_completion_rate": 96, "user_satisfaction_score": 4.4},
            "code_quality": {"score": 85, "typescript_errors": 0, "eslint_violations": 1},
            "dna_compliance": {
                "score": 89,
                "design_principles": {
                    "pedagogical_value": 4.5,
                    "policy_to_practice": 4.3,
                    "time_respect": 4.6,
                    "holistic_thinking": 4.2,
                    "professional_tone": 4.4
                },
                "architecture_principles": {"compliance_percent": 92}
            },
            "quality_issues": []
        }
    
    @pytest.fixture
    def sample_deployment_readiness(self):
        """Sample deployment readiness data."""
        return {
            "deployment_ready": True,
            "readiness_score": 95,
            "blocking_issues": [],
            "readiness_checks": {
                "performance": {"passed": True, "issues": []},
                "security": {"passed": True, "issues": []},
                "accessibility": {"passed": True, "issues": []},
                "dna_compliance": {"passed": True, "issues": []},
                "test_coverage": {"passed": True, "issues": []},
                "compatibility": {"passed": True, "issues": []}
            }
        }
    
    @pytest.mark.asyncio
    async def test_create_approval_request_success(self, client_communicator, sample_quality_analysis, sample_deployment_readiness):
        """Test successful approval request creation."""
        story_id = "STORY-TEST-001"
        staging_url = "https://staging.digitativa.se/STORY-TEST-001"
        
        approval_request = await client_communicator.create_approval_request(
            story_id, sample_quality_analysis, sample_deployment_readiness, staging_url
        )
        
        # Verify approval request structure
        assert approval_request["title"].startswith("Godkännande begärs:")
        assert "92.5/100" in approval_request["title"]
        assert "approval-request" in approval_request["labels"]
        assert "municipal-ready" in approval_request["labels"]
        assert approval_request["project_data"]["story_id"] == story_id
        assert approval_request["project_data"]["staging_url"] == staging_url
        assert approval_request["project_data"]["deployment_ready"] is True
        
        # Verify Swedish content
        assert "Kvalitetspoäng" in approval_request["title"]
        assert "DigiNativa" in approval_request["body"]
        assert "svenska kommunala miljöer" in approval_request["body"]
    
    @pytest.mark.asyncio
    async def test_handle_rejection_feedback(self, client_communicator):
        """Test rejection feedback handling."""
        story_id = "STORY-TEST-002"
        quality_issues = [
            {"type": "critical", "category": "performance", "message": "API response time too slow", "blocking": True},
            {"type": "warning", "category": "accessibility", "message": "Minor WCAG violations found", "blocking": False}
        ]
        recommendations = [
            "Optimize API queries",
            "Fix accessibility violations"
        ]
        blocking_issues = ["Performance requirements not met"]
        
        rejection_feedback = await client_communicator.handle_rejection_feedback(
            story_id, quality_issues, recommendations, blocking_issues
        )
        
        # Verify rejection feedback structure
        assert rejection_feedback["title"].startswith("Kvalitetsgranskning - Förbättringar krävs:")
        assert "quality-rejected" in rejection_feedback["labels"]
        assert "improvements-needed" in rejection_feedback["labels"]
        assert rejection_feedback["project_data"]["story_id"] == story_id
        assert rejection_feedback["project_data"]["critical_issues_count"] == 1
        
        # Verify improvement plan
        improvement_plan = rejection_feedback["improvement_plan"]
        assert "priority_1_critical" in improvement_plan
        assert "recommendations" in improvement_plan
        assert len(improvement_plan["priority_1_critical"]) == 1
    
    @pytest.mark.asyncio
    async def test_generate_quality_report_swedish(self, client_communicator, sample_quality_analysis, sample_deployment_readiness):
        """Test Swedish quality report generation."""
        story_id = "STORY-TEST-003"
        
        quality_report = await client_communicator.generate_quality_report(
            story_id, sample_quality_analysis, sample_deployment_readiness
        )
        
        # Verify report structure
        assert quality_report["report_id"].startswith("QR-STORY-TEST-003")
        assert quality_report["story_id"] == story_id
        assert quality_report["report_language"] == "sv"
        assert quality_report["target_audience"] == "swedish_municipal_coordinators"
        
        # Verify sections
        sections = quality_report["sections"]
        assert "executive_summary" in sections
        assert "quality_metrics" in sections
        assert "compliance_status" in sections
        assert "recommendations" in sections
        assert "next_steps" in sections
        
        # Verify metadata
        metadata = quality_report["metadata"]
        assert metadata["overall_score"] == 92.5
        assert metadata["deployment_ready"] is True
        assert metadata["reviewer_agent"] == "quality_reviewer"
    
    @pytest.mark.asyncio
    async def test_create_staging_notification(self, client_communicator):
        """Test staging notification creation."""
        story_id = "STORY-TEST-004"
        staging_url = "https://staging.digitativa.se/STORY-TEST-004"
        quality_score = 91.0
        test_instructions = [
            "Logga in med testuppgifter",
            "Testa grundläggande flöden",
            "Rapportera problem"
        ]
        
        staging_notification = await client_communicator.create_staging_notification(
            story_id, staging_url, quality_score, test_instructions
        )
        
        # Verify notification structure
        assert staging_notification["title"].startswith("Testversion redo:")
        assert "91.0/100" in staging_notification["title"]
        assert "staging-ready" in staging_notification["labels"]
        assert "client-testing" in staging_notification["labels"]
        
        # Verify staging data
        staging_data = staging_notification["staging_data"]
        assert staging_data["story_id"] == story_id
        assert staging_data["staging_url"] == staging_url
        assert staging_data["quality_score"] == quality_score
        assert "test_deadline" in staging_data
    
    @pytest.mark.asyncio
    async def test_municipal_quality_categories_translation(self, client_communicator):
        """Test that quality categories are properly translated to Swedish."""
        categories = client_communicator.municipal_quality_categories
        
        assert categories["accessibility"] == "Tillgänglighet (WCAG)"
        assert categories["performance"] == "Prestanda"
        assert categories["security"] == "Säkerhet"
        assert categories["usability"] == "Användarvänlighet"
        assert categories["pedagogical"] == "Pedagogisk effektivitet"
        assert categories["compliance"] == "Regelefterlevnad"
    
    def test_extract_feature_name(self, client_communicator):
        """Test feature name extraction from story ID."""
        assert client_communicator._extract_feature_name("STORY-001-002") == "Funktionalitet 001-002"
        assert client_communicator._extract_feature_name("CUSTOM-ID") == "CUSTOM-ID"
    
    def test_estimate_fix_time(self, client_communicator):
        """Test fix time estimation."""
        critical_issues = [
            {"blocking": True}, 
            {"blocking": True}
        ]
        minor_issues = [
            {"blocking": False},
            {"blocking": False},
            {"blocking": False}
        ]
        
        # 2 critical (2 days each) + 3 minor (0.5 days each) = 5.5 days
        time_estimate = client_communicator._estimate_fix_time(critical_issues + minor_issues)
        assert time_estimate == "5+"
        
        # 1 critical = 2 days
        time_estimate = client_communicator._estimate_fix_time([{"blocking": True}])
        assert time_estimate == "2-3"
        
        # 1 minor = 0.5 days
        time_estimate = client_communicator._estimate_fix_time([{"blocking": False}])
        assert time_estimate == "1"


class TestQualityReviewerClientCommunicationIntegration:
    """Test integration of client communication with Quality Reviewer agent."""
    
    @pytest.fixture
    def quality_reviewer_agent(self):
        """Create Quality Reviewer agent for testing."""
        return QualityReviewerAgent()
    
    @pytest.fixture
    def sample_qa_contract_high_quality(self):
        """High quality QA contract for approval testing."""
        return {
            "contract_version": "1.0",
            "story_id": "STORY-CLIENT-001",
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
                        "coverage_percent": 98,
                        "tests_passed": 50,
                        "total_tests": 50,
                        "unit_tests": 35,
                        "integration_tests": 15
                    },
                    "performance_metrics": {
                        "lighthouse_score": 94,
                        "api_response_time_ms": 120,
                        "page_load_time_ms": 1500
                    },
                    "accessibility_audit": {
                        "wcag_compliance_percent": 96,
                        "violations": [],
                        "keyboard_accessible": True
                    },
                    "user_flow_validation": {
                        "flow_completion_rate": 98,
                        "user_satisfaction_score": 4.6,
                        "average_task_completion_minutes": 8,
                        "target_completion_minutes": 10
                    },
                    "code_quality_metrics": {
                        "typescript_errors": 0,
                        "eslint_violations": 0,
                        "complexity_score": 2.8,
                        "documentation_coverage_percent": 90
                    },
                    "pedagogical_effectiveness_score": 4.7,
                    "policy_practice_alignment_score": 4.5,
                    "time_efficiency_score": 4.8,
                    "holistic_design_score": 4.4,
                    "professional_tone_score": 4.6,
                    "architecture_compliance_percent": 95
                }
            }
        }
    
    @pytest.fixture
    def sample_qa_contract_low_quality(self):
        """Low quality QA contract for rejection testing."""
        return {
            "contract_version": "1.0",
            "story_id": "STORY-CLIENT-002",
            "source_agent": "qa_tester",
            "target_agent": "quality_reviewer",
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": False,
                    "policy_to_practice": False,
                    "time_respect": True,
                    "holistic_thinking": False,
                    "professional_tone": True
                },
                "architecture_compliance": {
                    "api_first": False,
                    "stateless_backend": True,
                    "separation_of_concerns": False,
                    "simplicity_first": True
                }
            },
            "input_requirements": {
                "required_data": {
                    "test_results": {
                        "coverage_percent": 75,
                        "tests_passed": 20,
                        "total_tests": 25,
                        "unit_tests": 15,
                        "integration_tests": 5
                    },
                    "performance_metrics": {
                        "lighthouse_score": 65,
                        "api_response_time_ms": 450,
                        "page_load_time_ms": 4500
                    },
                    "accessibility_audit": {
                        "wcag_compliance_percent": 70,
                        "violations": [
                            {"type": "color_contrast", "severity": "high"},
                            {"type": "missing_alt_text", "severity": "medium"}
                        ],
                        "keyboard_accessible": False
                    },
                    "user_flow_validation": {
                        "flow_completion_rate": 78,
                        "user_satisfaction_score": 3.2,
                        "average_task_completion_minutes": 15,
                        "target_completion_minutes": 10
                    },
                    "code_quality_metrics": {
                        "typescript_errors": 5,
                        "eslint_violations": 12,
                        "complexity_score": 7.2,
                        "documentation_coverage_percent": 40
                    },
                    "pedagogical_effectiveness_score": 3.0,
                    "policy_practice_alignment_score": 2.8,
                    "time_efficiency_score": 2.5,
                    "holistic_design_score": 3.1,
                    "professional_tone_score": 3.3,
                    "architecture_compliance_percent": 60
                }
            }
        }
    
    @pytest.mark.asyncio
    async def test_process_contract_with_approval_communication(self, quality_reviewer_agent, sample_qa_contract_high_quality):
        """Test complete contract processing with approval and client communication."""
        # Mock all quality analysis to return high scores
        with patch.object(quality_reviewer_agent, '_perform_quality_analysis',
                         return_value={
                             "overall_score": 93.5,
                             "test_quality": {"score": 98, "issues": []},
                             "performance": {"score": 94, "lighthouse_score": 94, "api_response_time_ms": 120},
                             "accessibility": {"score": 96, "wcag_compliance_percent": 96, "violations_count": 0},
                             "user_experience": {"score": 92, "flow_completion_rate": 98, "user_satisfaction_score": 4.6},
                             "code_quality": {"score": 90, "typescript_errors": 0, "eslint_violations": 0},
                             "dna_compliance": {
                                 "score": 91,
                                 "design_principles": {
                                     "pedagogical_value": 4.7,
                                     "policy_to_practice": 4.5,
                                     "time_respect": 4.8,
                                     "holistic_thinking": 4.4,
                                     "professional_tone": 4.6
                                 },
                                 "architecture_principles": {"compliance_percent": 95}
                             },
                             "quality_issues": []
                         }):
            with patch.object(quality_reviewer_agent, '_validate_deployment_readiness',
                             return_value={"deployment_ready": True, "readiness_score": 95, "blocking_issues": []}):
                with patch.object(quality_reviewer_agent, '_make_approval_decision',
                                 return_value={
                                     "approved": True,
                                     "reasoning": "All quality standards met",
                                     "recommendations": ["Deploy with monitoring"],
                                     "blocking_issues": []
                                 }):
                    
                    result = await quality_reviewer_agent.process_contract(sample_qa_contract_high_quality)
                    
                    # Verify contract structure
                    assert result["contract_version"] == "1.0"
                    assert result["story_id"] == "STORY-CLIENT-001"
                    assert result["source_agent"] == "quality_reviewer"
                    assert result["target_agent"] == "deployment"
                    
                    # Verify client communication data
                    client_communication = result["input_requirements"]["required_data"]["client_communication"]
                    assert client_communication["communication_type"] == "approval_request"
                    assert "approval_request" in client_communication
                    assert "staging_notification" in client_communication
                    assert "quality_report" in client_communication
                    
                    # Verify approval request contains Swedish content
                    approval_request = client_communication["approval_request"]
                    assert "Godkännande begärs:" in approval_request["title"]
                    assert "svenska kommunala miljöer" in approval_request["body"]
                    assert approval_request["project_data"]["deployment_ready"] is True
    
    @pytest.mark.asyncio
    async def test_process_contract_with_rejection_communication(self, quality_reviewer_agent, sample_qa_contract_low_quality):
        """Test complete contract processing with rejection and client communication."""
        # Mock quality analysis to return low scores
        with patch.object(quality_reviewer_agent, '_perform_quality_analysis',
                         return_value={
                             "overall_score": 68.5,
                             "test_quality": {"score": 75, "issues": ["Low test coverage"]},
                             "performance": {"score": 65, "lighthouse_score": 65, "api_response_time_ms": 450},
                             "accessibility": {"score": 70, "wcag_compliance_percent": 70, "violations_count": 2},
                             "user_experience": {"score": 72, "flow_completion_rate": 78, "user_satisfaction_score": 3.2},
                             "code_quality": {"score": 60, "typescript_errors": 5, "eslint_violations": 12},
                             "dna_compliance": {
                                 "score": 65,
                                 "design_principles": {
                                     "pedagogical_value": 3.0,
                                     "policy_to_practice": 2.8,
                                     "time_respect": 2.5,
                                     "holistic_thinking": 3.1,
                                     "professional_tone": 3.3
                                 },
                                 "architecture_principles": {"compliance_percent": 60}
                             },
                             "quality_issues": [
                                 {"type": "critical", "category": "performance", "message": "API too slow", "blocking": True},
                                 {"type": "critical", "category": "accessibility", "message": "WCAG violations", "blocking": True}
                             ]
                         }):
            with patch.object(quality_reviewer_agent, '_validate_deployment_readiness',
                             return_value={
                                 "deployment_ready": False, 
                                 "readiness_score": 60, 
                                 "blocking_issues": ["Performance issues", "Accessibility violations"]
                             }):
                with patch.object(quality_reviewer_agent, '_make_approval_decision',
                                 return_value={
                                     "approved": False,
                                     "reasoning": "Quality standards not met",
                                     "recommendations": ["Fix performance issues", "Address accessibility violations"],
                                     "blocking_issues": ["Performance issues", "Accessibility violations"]
                                 }):
                    
                    result = await quality_reviewer_agent.process_contract(sample_qa_contract_low_quality)
                    
                    # Verify rejection contract structure
                    assert result["target_agent"] == "developer"
                    assert result["input_requirements"]["required_data"]["approval_status"] is False
                    
                    # Verify client communication data
                    client_communication = result["input_requirements"]["required_data"]["client_communication"]
                    assert client_communication["communication_type"] == "rejection_feedback"
                    assert "rejection_feedback" in client_communication
                    assert "quality_report" in client_communication
                    
                    # Verify rejection feedback contains Swedish content
                    rejection_feedback = client_communication["rejection_feedback"]
                    assert "Kvalitetsgranskning - Förbättringar krävs:" in rejection_feedback["title"]
                    assert rejection_feedback["project_data"]["critical_issues_count"] > 0
    
    @pytest.mark.asyncio
    async def test_client_communication_quality_gate(self, quality_reviewer_agent):
        """Test client communication quality gate validation."""
        # Test successful client communication gate
        deliverables_with_communication = {
            "client_communication": {
                "communication_type": "approval_request",
                "approval_request": {"title": "Test approval"},
                "quality_report": {"report_id": "QR-TEST-001"}
            }
        }
        
        assert await quality_reviewer_agent.validate_quality_gate(
            "client_communication_sent", deliverables_with_communication
        ) is True
        
        # Test failed client communication gate
        deliverables_without_communication = {
            "client_communication": {}
        }
        
        assert await quality_reviewer_agent.validate_quality_gate(
            "client_communication_sent", deliverables_without_communication
        ) is False
        
        # Test missing client communication
        deliverables_missing_communication = {}
        
        assert await quality_reviewer_agent.validate_quality_gate(
            "client_communication_sent", deliverables_missing_communication
        ) is False
    
    @pytest.mark.asyncio
    async def test_error_handling_in_client_communication(self, quality_reviewer_agent):
        """Test error handling in client communication."""
        story_id = "STORY-ERROR-001"
        quality_analysis = {"overall_score": 90}
        deployment_readiness = {"deployment_ready": True}
        approval_decision = {"approved": True}
        
        # Mock ClientCommunicator to raise an exception
        with patch.object(quality_reviewer_agent.client_communicator, 'create_approval_request',
                         side_effect=Exception("Communication service unavailable")):
            
            client_communication = await quality_reviewer_agent._handle_client_communication(
                story_id, quality_analysis, deployment_readiness, approval_decision
            )
            
            # Verify error handling
            assert client_communication["communication_type"] == "error"
            assert "Communication service unavailable" in client_communication["error_message"]