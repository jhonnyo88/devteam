"""
Unit tests for QA Tester agent.

PURPOSE:
Comprehensive testing of QA Tester agent functionality including
contract processing, quality validation, and DNA compliance checking.

CRITICAL COVERAGE:
- Agent initialization and configuration
- Contract processing and validation
- Quality gate checking
- Anna persona compatibility validation
- Error handling and edge cases

TEST STANDARDS:
- 100% line coverage required
- All edge cases covered
- Mock external dependencies
- Test both success and failure scenarios
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
from pathlib import Path

# Import the agent and related modules
from ..agent import QATesterAgent
from ..contracts.input_models import QATesterInputContract, TestSuiteInput, ImplementationData, PerformanceMetrics, DNAComplianceData
from ..contracts.output_models import QATesterOutputContract, ValidationStatus, ProductionReadiness
from ...shared.exceptions import AgentExecutionError, QualityGateError, DNAComplianceError


class TestQATesterAgent:
    """Test suite for QA Tester agent."""
    
    @pytest.fixture
    def sample_config(self):
        """Sample configuration for testing."""
        return {
            "persona_config": {
                "anna_requirements": {
                    "max_task_duration": 10,
                    "min_satisfaction_score": 4.0
                }
            },
            "accessibility_config": {
                "wcag_level": "AA",
                "compliance_threshold": 90
            },
            "flow_config": {
                "max_flow_steps": 7,
                "max_completion_time": 10
            }
        }
    
    @pytest.fixture
    def qa_tester_agent(self, sample_config):
        """Create QA Tester agent instance for testing."""
        return QATesterAgent(config=sample_config)
    
    @pytest.fixture
    def sample_input_contract(self):
        """Sample input contract for testing."""
        return {
            "contract_version": "1.0",
            "story_id": "STORY-TEST-001",
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
                },
                "overall_compliance": True,
                "validation_timestamp": datetime.now().isoformat()
            },
            "input_requirements": {
                "required_files": [
                    "tests/unit/STORY-TEST-001/",
                    "docs/test_reports/STORY-TEST-001_coverage.html"
                ],
                "required_data": {
                    "test_suite": {
                        "suite_id": "test-suite-001",
                        "story_id": "STORY-TEST-001",
                        "execution_timestamp": datetime.now().isoformat(),
                        "unit_tests": [],
                        "integration_tests": [],
                        "e2e_tests": [],
                        "performance_tests": [],
                        "security_tests": [],
                        "overall_coverage_percentage": 100.0,
                        "test_environment": "testing",
                        "execution_duration_minutes": 5.0
                    },
                    "implementation_data": {
                        "implementation_id": "impl-001",
                        "story_id": "STORY-TEST-001",
                        "ui_components": [
                            {
                                "component_id": "test-button",
                                "component_type": "button",
                                "properties": {"text": "Test Button"},
                                "accessibility_attributes": {"aria-label": "Test Button"},
                                "styling_info": {"color": "#000000", "background_color": "#ffffff"},
                                "interaction_handlers": ["onClick"],
                                "text_content": "Test Button"
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
                    "coverage_report": {"total_coverage": 100},
                    "security_scan_results": {"vulnerabilities": []}
                },
                "required_validations": [
                    "anna_persona_satisfaction_verified",
                    "wcag_aa_compliance_confirmed"
                ]
            },
            "quality_gates": [
                "anna_persona_satisfaction_score_minimum_met",
                "wcag_aa_compliance_100_percent_verified"
            ],
            "handoff_criteria": [
                "comprehensive_ux_validation_completed",
                "accessibility_compliance_fully_verified"
            ]
        }
    
    def test_agent_initialization(self, sample_config):
        """Test QA Tester agent initialization."""
        agent = QATesterAgent(config=sample_config)
        
        assert agent.agent_id == "qat-001"
        assert agent.agent_type == "qa_tester"
        assert agent.config == sample_config
        assert hasattr(agent, 'persona_simulator')
        assert hasattr(agent, 'accessibility_checker')
        assert hasattr(agent, 'user_flow_validator')
        assert agent.anna_persona_requirements["time_availability"] == "10 minutes maximum per session"
    
    def test_agent_initialization_without_config(self):
        """Test agent initialization without configuration."""
        agent = QATesterAgent()
        
        assert agent.agent_id == "qat-001"
        assert agent.agent_type == "qa_tester"
        assert agent.config == {}
        assert hasattr(agent, 'persona_simulator')
        assert hasattr(agent, 'accessibility_checker')
        assert hasattr(agent, 'user_flow_validator')
    
    @pytest.mark.asyncio
    async def test_process_contract_success(self, qa_tester_agent, sample_input_contract):
        """Test successful contract processing."""
        # Mock the tool methods
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', new_callable=AsyncMock) as mock_persona, \
             patch.object(qa_tester_agent.accessibility_checker, 'validate_accessibility', new_callable=AsyncMock) as mock_accessibility, \
             patch.object(qa_tester_agent.user_flow_validator, 'validate_user_flows', new_callable=AsyncMock) as mock_flow, \
             patch.object(qa_tester_agent, '_assess_content_quality', new_callable=AsyncMock) as mock_content, \
             patch.object(qa_tester_agent, '_validate_qa_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(qa_tester_agent, '_generate_qa_report', new_callable=AsyncMock) as mock_report:
            
            # Setup mock returns
            mock_persona.return_value = {
                "satisfaction_score": 4.5,
                "task_completion_rate": 95,
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
            
            mock_content.return_value = {
                "professional_tone_score": 4.2,
                "pedagogical_value_score": 4.1,
                "policy_relevance_score": 4.3
            }
            
            mock_dna.return_value = {
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
                "overall_compliance": True
            }
            
            mock_report.return_value = {
                "story_id": "STORY-TEST-001",
                "qa_testing_summary": {
                    "overall_quality_score": 4.2,
                    "anna_persona_satisfaction": 4.5
                }
            }
            
            # Execute contract processing
            result = await qa_tester_agent.process_contract(sample_input_contract)
            
            # Verify result structure
            assert result is not None
            assert result["contract_version"] == "1.0"
            assert result["story_id"] == "STORY-TEST-001"
            assert result["source_agent"] == "qa_tester"
            assert result["target_agent"] == "quality_reviewer"
            assert "dna_compliance" in result
            assert "input_requirements" in result
            assert "output_specifications" in result
            assert "quality_gates" in result
            assert "handoff_criteria" in result
            
            # Verify all tools were called
            mock_persona.assert_called_once()
            mock_accessibility.assert_called_once()
            mock_flow.assert_called_once()
            mock_content.assert_called_once()
            mock_dna.assert_called_once()
            mock_report.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_contract_with_tool_failure(self, qa_tester_agent, sample_input_contract):
        """Test contract processing with tool failure."""
        # Mock persona simulator to raise exception
        with patch.object(qa_tester_agent.persona_simulator, 'simulate_anna_usage', side_effect=Exception("Persona simulation failed")):
            
            with pytest.raises(AgentExecutionError) as exc_info:
                await qa_tester_agent.process_contract(sample_input_contract)
            
            assert "QA testing failed" in str(exc_info.value)
            assert "Persona simulation failed" in str(exc_info.value)
    
    def test_check_quality_gate_anna_satisfaction(self, qa_tester_agent):
        """Test Anna satisfaction quality gate check."""
        deliverables = {
            "qa_validation_results": {
                "anna_persona_testing": {
                    "satisfaction_score": 4.2
                }
            }
        }
        
        result = qa_tester_agent._check_anna_satisfaction(deliverables)
        assert result is True
        
        # Test with low satisfaction
        deliverables["qa_validation_results"]["anna_persona_testing"]["satisfaction_score"] = 3.5
        result = qa_tester_agent._check_anna_satisfaction(deliverables)
        assert result is False
    
    def test_check_quality_gate_accessibility_compliance(self, qa_tester_agent):
        """Test accessibility compliance quality gate check."""
        deliverables = {
            "qa_validation_results": {
                "accessibility_compliance": {
                    "compliance_level": "AA",
                    "compliance_percentage": 100.0
                }
            }
        }
        
        result = qa_tester_agent._check_accessibility_compliance(deliverables)
        assert result is True
        
        # Test with non-compliance
        deliverables["qa_validation_results"]["accessibility_compliance"]["compliance_percentage"] = 85.0
        result = qa_tester_agent._check_accessibility_compliance(deliverables)
        assert result is False
    
    def test_check_quality_gate_time_constraints(self, qa_tester_agent):
        """Test time constraints quality gate check."""
        deliverables = {
            "qa_validation_results": {
                "anna_persona_testing": {
                    "average_completion_time_minutes": 8.5
                }
            }
        }
        
        result = qa_tester_agent._check_time_constraints(deliverables)
        assert result is True
        
        # Test with time violation
        deliverables["qa_validation_results"]["anna_persona_testing"]["average_completion_time_minutes"] = 12.0
        result = qa_tester_agent._check_time_constraints(deliverables)
        assert result is False
    
    def test_check_quality_gate_professional_tone(self, qa_tester_agent):
        """Test professional tone quality gate check."""
        deliverables = {
            "qa_validation_results": {
                "content_quality_assessment": {
                    "professional_tone_score": 4.2
                }
            }
        }
        
        result = qa_tester_agent._check_professional_tone(deliverables)
        assert result is True
        
        # Test with low tone score
        deliverables["qa_validation_results"]["content_quality_assessment"]["professional_tone_score"] = 3.0
        result = qa_tester_agent._check_professional_tone(deliverables)
        assert result is False
    
    def test_check_quality_gate_pedagogical_value(self, qa_tester_agent):
        """Test pedagogical value quality gate check."""
        deliverables = {
            "qa_validation_results": {
                "content_quality_assessment": {
                    "pedagogical_value_score": 4.3
                }
            }
        }
        
        result = qa_tester_agent._check_pedagogical_value(deliverables)
        assert result is True
        
        # Test with low pedagogical value
        deliverables["qa_validation_results"]["content_quality_assessment"]["pedagogical_value_score"] = 3.2
        result = qa_tester_agent._check_pedagogical_value(deliverables)
        assert result is False
    
    def test_check_quality_gate_user_flows(self, qa_tester_agent):
        """Test user flows quality gate check."""
        deliverables = {
            "qa_validation_results": {
                "user_flow_validation": {
                    "flows_passed": 5,
                    "total_flows": 5
                }
            }
        }
        
        result = qa_tester_agent._check_user_flows(deliverables)
        assert result is True
        
        # Test with flow failures
        deliverables["qa_validation_results"]["user_flow_validation"]["flows_passed"] = 4
        result = qa_tester_agent._check_user_flows(deliverables)
        assert result is False
    
    def test_check_quality_gate_unknown_gate(self, qa_tester_agent):
        """Test unknown quality gate check."""
        deliverables = {}
        
        # Should default to True with warning for unknown gates
        result = qa_tester_agent._check_quality_gate("unknown_gate", deliverables)
        assert result is True
    
    def test_check_quality_gate_with_exception(self, qa_tester_agent):
        """Test quality gate check with exception."""
        deliverables = None  # This will cause an exception
        
        result = qa_tester_agent._check_quality_gate("anna_persona_satisfaction_score_minimum_met", deliverables)
        assert result is False
    
    @pytest.mark.asyncio
    async def test_assess_content_quality(self, qa_tester_agent):
        """Test content quality assessment."""
        implementation_data = {
            "ui_components": [
                {
                    "text_content": "This is a professional policy document for municipal training.",
                    "labels": ["Submit", "Cancel"],
                    "instructions": "Please complete the form to proceed with compliance training."
                }
            ]
        }
        
        with patch.object(qa_tester_agent, '_assess_professional_tone', new_callable=AsyncMock) as mock_tone, \
             patch.object(qa_tester_agent, '_assess_pedagogical_value', new_callable=AsyncMock) as mock_pedagogy, \
             patch.object(qa_tester_agent, '_assess_policy_relevance', new_callable=AsyncMock) as mock_policy:
            
            mock_tone.return_value = 4.2
            mock_pedagogy.return_value = 4.1
            mock_policy.return_value = 4.3
            
            result = await qa_tester_agent._assess_content_quality(implementation_data, "STORY-TEST-001")
            
            assert result["professional_tone_score"] == 4.2
            assert result["pedagogical_value_score"] == 4.1
            assert result["policy_relevance_score"] == 4.3
            assert "content_analysis" in result
            assert result["content_analysis"]["total_text_elements"] == 3
    
    @pytest.mark.asyncio
    async def test_assess_content_quality_with_exception(self, qa_tester_agent):
        """Test content quality assessment with exception."""
        implementation_data = {}
        
        with patch.object(qa_tester_agent, '_assess_professional_tone', side_effect=Exception("Assessment failed")):
            result = await qa_tester_agent._assess_content_quality(implementation_data, "STORY-TEST-001")
            
            assert result["professional_tone_score"] == 0
            assert result["pedagogical_value_score"] == 0
            assert result["policy_relevance_score"] == 0
            assert "error" in result
    
    @pytest.mark.asyncio
    async def test_assess_professional_tone(self, qa_tester_agent):
        """Test professional tone assessment."""
        content_text = [
            "This policy document outlines compliance requirements for municipal procedures.",
            "Please follow the established guidelines for best practice implementation.",
            "Regulatory frameworks must be adhered to in all circumstances."
        ]
        
        result = await qa_tester_agent._assess_professional_tone(content_text)
        
        assert isinstance(result, float)
        assert 1.0 <= result <= 5.0
        assert result > 3.0  # Should be high due to professional language
    
    @pytest.mark.asyncio
    async def test_assess_professional_tone_unprofessional_content(self, qa_tester_agent):
        """Test professional tone assessment with unprofessional content."""
        content_text = [
            "This is awesome and super cool!",
            "Wow, amazing functionality here!",
            "Super duper excellent work!"
        ]
        
        result = await qa_tester_agent._assess_professional_tone(content_text)
        
        assert isinstance(result, float)
        assert 1.0 <= result <= 5.0
        assert result < 3.0  # Should be low due to unprofessional language
    
    @pytest.mark.asyncio
    async def test_assess_professional_tone_empty_content(self, qa_tester_agent):
        """Test professional tone assessment with empty content."""
        result = await qa_tester_agent._assess_professional_tone([])
        assert result == 0.0
    
    @pytest.mark.asyncio
    async def test_assess_pedagogical_value(self, qa_tester_agent):
        """Test pedagogical value assessment."""
        content_text = [
            "Learn about municipal compliance through this interactive tutorial.",
            "This exercise will help you understand policy implementation steps.",
            "Practice these procedures to improve your professional skills."
        ]
        
        implementation_data = {
            "interactive_elements": ["quiz", "simulation"],
            "feedback_mechanisms": ["progress_indicator", "completion_feedback"]
        }
        
        result = await qa_tester_agent._assess_pedagogical_value(content_text, implementation_data)
        
        assert isinstance(result, float)
        assert 1.0 <= result <= 5.0
        assert result > 3.0  # Should be high due to learning content and interactive elements
    
    @pytest.mark.asyncio
    async def test_assess_pedagogical_value_with_exception(self, qa_tester_agent):
        """Test pedagogical value assessment with exception."""
        content_text = ["test"]
        implementation_data = None  # This will cause an exception
        
        result = await qa_tester_agent._assess_pedagogical_value(content_text, implementation_data)
        assert result == 2.0  # Default neutral score
    
    @pytest.mark.asyncio
    async def test_assess_policy_relevance(self, qa_tester_agent):
        """Test policy relevance assessment."""
        content_text = [
            "Municipal regulations require compliance with government standards.",
            "Public sector employees must follow administrative procedures.",
            "Citizens benefit from efficient municipal service delivery."
        ]
        
        result = await qa_tester_agent._assess_policy_relevance(content_text)
        
        assert isinstance(result, float)
        assert 1.0 <= result <= 5.0
        assert result > 3.0  # Should be high due to policy-related keywords
    
    @pytest.mark.asyncio
    async def test_assess_policy_relevance_empty_content(self, qa_tester_agent):
        """Test policy relevance assessment with empty content."""
        result = await qa_tester_agent._assess_policy_relevance([])
        assert result == 0.0
    
    @pytest.mark.asyncio
    async def test_validate_qa_dna_compliance(self, qa_tester_agent):
        """Test QA DNA compliance validation."""
        persona_results = {
            "average_completion_time_minutes": 8.0,
            "task_completion_rate": 96,
            "user_confusion_incidents": 0
        }
        
        accessibility_results = {
            "compliance_level": "AA",
            "compliance_percentage": 98.0
        }
        
        content_quality = {
            "pedagogical_value_score": 4.2,
            "policy_relevance_score": 4.3,
            "professional_tone_score": 4.1
        }
        
        result = await qa_tester_agent._validate_qa_dna_compliance(
            persona_results, accessibility_results, content_quality
        )
        
        assert "design_principles_validation" in result
        assert "architecture_compliance" in result
        assert result["overall_compliance"] is True
        assert "validation_timestamp" in result
        
        # Check individual principle validations
        design_principles = result["design_principles_validation"]
        assert design_principles["pedagogical_value"] is True
        assert design_principles["policy_to_practice"] is True
        assert design_principles["time_respect"] is True
        assert design_principles["holistic_thinking"] is True
        assert design_principles["professional_tone"] is True
    
    @pytest.mark.asyncio
    async def test_validate_qa_dna_compliance_with_failures(self, qa_tester_agent):
        """Test QA DNA compliance validation with failures."""
        persona_results = {
            "average_completion_time_minutes": 12.0,  # Exceeds limit
            "task_completion_rate": 85,  # Below threshold
            "user_confusion_incidents": 5  # Too many incidents
        }
        
        accessibility_results = {
            "compliance_level": "A",  # Below AA
            "compliance_percentage": 80.0  # Below threshold
        }
        
        content_quality = {
            "pedagogical_value_score": 3.0,  # Below threshold
            "policy_relevance_score": 3.5,  # Below threshold
            "professional_tone_score": 3.2  # Below threshold
        }
        
        result = await qa_tester_agent._validate_qa_dna_compliance(
            persona_results, accessibility_results, content_quality
        )
        
        assert result["overall_compliance"] is False
        
        # Check that failing principles are marked as False
        design_principles = result["design_principles_validation"]
        assert design_principles["pedagogical_value"] is False
        assert design_principles["policy_to_practice"] is False
        assert design_principles["time_respect"] is False
        assert design_principles["holistic_thinking"] is False
        assert design_principles["professional_tone"] is False
    
    @pytest.mark.asyncio
    async def test_validate_qa_dna_compliance_with_exception(self, qa_tester_agent):
        """Test QA DNA compliance validation with exception."""
        # Pass None to cause exception
        result = await qa_tester_agent._validate_qa_dna_compliance(None, None, None)
        
        assert result["overall_compliance"] is False
        assert "error" in result
        
        # Check that all principles are marked as False
        design_principles = result["design_principles_validation"]
        assert all(not value for value in design_principles.values())
    
    def test_calculate_quality_metrics(self, qa_tester_agent):
        """Test quality metrics calculation."""
        qa_results = {
            "anna_persona_testing": {
                "satisfaction_score": 4.2
            },
            "accessibility_compliance": {
                "compliance_percentage": 95.0
            },
            "user_flow_validation": {
                "success_rate_percentage": 92.0
            },
            "content_quality_assessment": {
                "professional_tone_score": 4.1,
                "pedagogical_value_score": 4.3,
                "policy_relevance_score": 4.0
            }
        }
        
        result = qa_tester_agent._calculate_quality_metrics(qa_results)
        
        assert "overall_score" in result
        assert "persona_satisfaction_score" in result
        assert "accessibility_score" in result
        assert "user_flow_score" in result
        assert "content_quality_score" in result
        assert "score_breakdown" in result
        
        # Verify score calculation
        assert result["persona_satisfaction_score"] == 4.2
        assert result["accessibility_score"] == 4.75  # 95/20 = 4.75
        assert result["user_flow_score"] == 4.6  # 92/20 = 4.6
        assert result["content_quality_score"] == 4.13  # (4.1+4.3+4.0)/3 H 4.13
        
        # Verify overall score is calculated correctly
        expected_overall = (4.2*0.3 + 4.75*0.25 + 4.6*0.25 + 4.13*0.2)
        assert abs(result["overall_score"] - expected_overall) < 0.01
    
    def test_calculate_quality_metrics_with_empty_results(self, qa_tester_agent):
        """Test quality metrics calculation with empty results."""
        result = qa_tester_agent._calculate_quality_metrics({})
        
        assert result["overall_score"] == 0.0
        assert "error" in result
    
    def test_calculate_quality_metrics_with_exception(self, qa_tester_agent):
        """Test quality metrics calculation with exception."""
        # Pass None to cause exception
        result = qa_tester_agent._calculate_quality_metrics(None)
        
        assert result["overall_score"] == 0.0
        assert "error" in result