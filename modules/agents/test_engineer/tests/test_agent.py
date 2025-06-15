"""
Test Engineer Agent Core Tests

PURPOSE:
Tests core logic and workflow of Test Engineer agent according to TEST_STRATEGY.md.

CRITICAL IMPORTANCE:
- Validates test generation and performance validation
- Ensures DNA compliance validation works correctly
- Tests security scanning and coverage analysis
- Validates contract generation for QA Tester handoff

COVERAGE REQUIREMENTS:
- Agent core logic: 95% minimum
- Contract compliance: 100%
- DNA validation: 100%
- Tool integration: 90% minimum

TEST ENGINEER RESPONSIBILITIES:
- Generate integration tests for React + FastAPI implementations
- Create end-to-end tests with user persona simulation
- Validate performance requirements (API <200ms, Lighthouse >90)
- Execute security vulnerability scanning
- Provide comprehensive coverage analysis and reporting
- Maintain 100% test coverage for business logic
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime
from typing import Dict, Any

from modules.agents.test_engineer.agent import TestEngineerAgent
from modules.shared.exceptions import (
    DNAComplianceError, QualityGateError, AgentExecutionError
)


class TestTestEngineerAgent:
    """Test Test Engineer agent core functionality."""
    
    @pytest.fixture
    def te_config(self):
        """Test configuration for Test Engineer agent."""
        return {
            "test_mode": True,
            "test_output_path": "test_tests",
            "coverage_threshold": 95,
            "performance_budget": {
                "api_response_time_ms": 200,
                "lighthouse_score": 90,
                "bundle_size_kb": 500
            },
            "quality_standards": {
                "integration_test_coverage": {"min": 95},
                "e2e_test_coverage": {"min": 90},
                "performance_test_required": True,
                "security_scan_required": True,
                "automation_required": True,
                "ci_cd_integration": True
            }
        }
    
    @pytest.fixture
    def te_agent(self, te_config):
        """Create Test Engineer agent instance for testing."""
        return TestEngineerAgent(te_config)
    
    @pytest.fixture
    def sample_component_implementation(self):
        """Sample React component implementation from Developer agent."""
        return {
            "name": "PolicyTrainingCard",
            "type": "react_component",
            "files": {
                "component": "src/components/PolicyTrainingCard.tsx",
                "test": "tests/unit/PolicyTrainingCard.test.tsx",
                "styles": "src/components/PolicyTrainingCard.module.css"
            },
            "code": {
                "component": """
                import React from 'react';
                import { Card, Button } from '@shadcn/ui';
                
                interface PolicyTrainingCardProps {
                  id: string;
                  title: string;
                  description: string;
                  onSelect: (id: string) => void;
                  completed?: boolean;
                }
                
                export const PolicyTrainingCard: React.FC<PolicyTrainingCardProps> = ({
                  id, title, description, onSelect, completed = false
                }) => {
                  return (
                    <Card className="p-4 cursor-pointer hover:shadow-lg">
                      <h3 className="text-lg font-semibold">{title}</h3>
                      <p className="text-gray-600 mb-4">{description}</p>
                      <Button 
                        onClick={() => onSelect(id)}
                        variant={completed ? "outline" : "default"}
                      >
                        {completed ? "Granska igen" : "Starta träning"}
                      </Button>
                    </Card>
                  );
                };
                """,
                "test": "// Jest test code placeholder"
            },
            "typescript_errors": 0,
            "eslint_violations": 0,
            "test_coverage_percent": 100.0,
            "accessibility_score": 95,
            "performance_score": 92,
            "integration_test_passed": True
        }
    
    @pytest.fixture
    def sample_api_implementation(self):
        """Sample FastAPI endpoint implementation from Developer agent."""
        return {
            "name": "training_policies_endpoint",
            "method": "GET",
            "path": "/api/training/policies",
            "files": {
                "endpoint": "src/api/endpoints/training_policies.py",
                "test": "tests/unit/test_training_policies_api.py"
            },
            "code": {
                "endpoint": """
                from fastapi import APIRouter, HTTPException, Depends
                from typing import List
                from ..models.training_policy import TrainingPolicyResponse
                from ..services.policy_service import PolicyService
                
                router = APIRouter()
                
                @router.get("/api/training/policies", response_model=List[TrainingPolicyResponse])
                async def get_training_policies(
                    policy_service: PolicyService = Depends()
                ) -> List[TrainingPolicyResponse]:
                    try:
                        policies = await policy_service.get_active_policies()
                        return [TrainingPolicyResponse.from_model(p) for p in policies]
                    except Exception as e:
                        raise HTTPException(status_code=500, detail="Failed to fetch policies")
                """,
                "test": "# pytest test code placeholder"
            },
            "functional_test_passed": True,
            "performance_test_passed": True,
            "security_test_passed": True,
            "estimated_response_time_ms": 150
        }
    
    @pytest.fixture
    def sample_input_contract(self, sample_component_implementation, sample_api_implementation):
        """Sample input contract from Developer agent."""
        story_id = "STORY-TE-CORE-001"
        
        return {
            "contract_version": "1.0",
            "contract_type": "implementation_to_testing",
            "story_id": story_id,
            "source_agent": "developer",
            "target_agent": "test_engineer",
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
                "developer_dna_validation": {
                    "overall_dna_compliant": True,
                    "dna_compliance_score": 4.5,
                    "validation_timestamp": "2025-06-15T10:00:00Z"
                }
            },
            "input_requirements": {
                "required_files": [
                    f"src/components/{story_id}/PolicyTrainingCard.tsx",
                    f"src/api/endpoints/{story_id}/training_policies.py"
                ],
                "required_data": {
                    "component_implementations": [sample_component_implementation],
                    "api_implementations": [sample_api_implementation],
                    "test_suite": {
                        "story_id": story_id,
                        "unit_tests": [
                            {"name": "test_policy_training_card", "status": "passing"},
                            {"name": "test_training_policies_api", "status": "passing"}
                        ],
                        "coverage_percent": 100.0,
                        "total_test_cases": 2,
                        "test_configuration": {
                            "framework": "jest_pytest",
                            "test_runner": "npm_test"
                        }
                    },
                    "implementation_docs": {
                        "story_id": story_id,
                        "user_flows": [
                            {
                                "name": "policy_training_selection",
                                "description": "Anna selects and starts policy training",
                                "steps": ["browse_policies", "select_policy", "start_training", "complete_training"]
                            }
                        ]
                    },
                    "git_commit_hash": "abc123def456"
                },
                "required_validations": [
                    "component_tests_passing",
                    "api_tests_passing",
                    "performance_requirements_met"
                ]
            }
        }


class TestTestEngineerCoreLogic(TestTestEngineerAgent):
    """Test core Test Engineer agent logic and workflows."""
    
    @pytest.mark.asyncio
    async def test_agent_initialization(self, te_config):
        """Test Test Engineer agent initializes correctly with all tools."""
        agent = TestEngineerAgent(te_config)
        
        # Verify agent properties
        assert agent.agent_id == "te-001"
        assert agent.agent_type == "test_engineer"
        assert agent.coverage_threshold == 95
        assert agent.performance_budget["api_response_time_ms"] == 200
        
        # Verify tools are initialized
        assert hasattr(agent, 'test_generator')
        assert hasattr(agent, 'coverage_analyzer')
        assert hasattr(agent, 'performance_tester')
        assert hasattr(agent, 'security_scanner')
        assert hasattr(agent, 'dna_test_validator')
        assert hasattr(agent, 'ai_test_optimizer')
        assert hasattr(agent, 'event_bus')
        
        # Verify quality standards
        assert agent.quality_standards["integration_test_coverage"]["min"] == 95
        assert agent.quality_standards["e2e_test_coverage"]["min"] == 90
        assert agent.quality_standards["performance_test_required"] is True
    
    @pytest.mark.asyncio
    async def test_process_contract_success(self, te_agent, sample_input_contract):
        """Test successful contract processing with complete workflow."""
        # Mock all tool methods to avoid actual execution
        with patch.object(te_agent, '_validate_implementation_testability') as mock_validate, \
             patch.object(te_agent.ai_test_optimizer, 'optimize_test_strategy') as mock_ai_optimizer, \
             patch.object(te_agent.test_generator, 'generate_integration_tests') as mock_integration, \
             patch.object(te_agent.test_generator, 'generate_e2e_tests') as mock_e2e, \
             patch.object(te_agent.performance_tester, 'run_comprehensive_performance_tests') as mock_perf, \
             patch.object(te_agent.security_scanner, 'run_comprehensive_security_scan') as mock_security, \
             patch.object(te_agent.coverage_analyzer, 'analyze_comprehensive_coverage') as mock_coverage, \
             patch.object(te_agent, '_validate_test_quality_gates') as mock_gates, \
             patch.object(te_agent.dna_test_validator, 'validate_test_dna_compliance') as mock_dna, \
             patch.object(te_agent, '_generate_automation_configuration') as mock_automation, \
             patch.object(te_agent, '_notify_team_progress') as mock_notify:
            
            story_id = sample_input_contract["story_id"]
            
            # Setup mock returns
            mock_validate.return_value = None  # Validation passes
            
            # Mock AI optimization result
            class MockAIOptimizationResult:
                def __init__(self):
                    self.overall_optimization_score = 4.5
                    self.estimated_time_savings_minutes = 20.0
                    self.quality_improvement_score = 4.2
                    self.failure_predictions = []
                    self.test_priorities = []
                    self.edge_case_predictions = []
                    self.municipal_optimization_insights = {
                        "anna_persona_priority_tests": 3,
                        "gdpr_compliance_focus_areas": 2
                    }
            
            mock_ai_optimizer.return_value = MockAIOptimizationResult()
            
            mock_integration.return_value = {
                "story_id": story_id,
                "test_type": "integration",
                "total_test_cases": 8,
                "coverage_percent": 96.0,
                "all_tests_passing": True,
                "test_cases": [
                    {"name": "test_policy_card_integration", "status": "passing"},
                    {"name": "test_api_policy_integration", "status": "passing"}
                ]
            }
            
            mock_e2e.return_value = {
                "story_id": story_id,
                "test_type": "end_to_end",
                "total_scenarios": 4,
                "coverage_percent": 92.0,
                "all_tests_passing": True,
                "scenarios": [
                    {"name": "anna_selects_policy_training", "status": "passing"}
                ]
            }
            
            mock_perf.return_value = {
                "story_id": story_id,
                "average_api_response_time_ms": 145.0,
                "lighthouse_score": 94,
                "bundle_size_kb": 180.0,
                "performance_budget_met": True
            }
            
            mock_security.return_value = {
                "story_id": story_id,
                "critical_vulnerabilities": [],
                "high_vulnerabilities": [],
                "medium_vulnerabilities": [],
                "security_compliance_met": True
            }
            
            mock_coverage.return_value = {
                "story_id": story_id,
                "overall_coverage_percent": 96.0,
                "coverage_quality_met": True
            }
            
            mock_gates.return_value = None  # Quality gates pass
            
            # Mock DNA validation result
            class MockDNAResult:
                def __init__(self):
                    self.overall_dna_compliant = True
                    self.time_respect_compliant = True
                    self.pedagogical_value_compliant = True
                    self.professional_tone_compliant = True
                    self.dna_compliance_score = 4.6
                    self.validation_timestamp = "2025-06-15T10:30:00Z"
                    self.quality_reviewer_metrics = {
                        "test_execution_efficiency": 4.5,
                        "test_effectiveness": 4.7,
                        "test_documentation_quality": 4.4
                    }
            
            mock_dna.return_value = MockDNAResult()
            
            mock_automation.return_value = {
                "story_id": story_id,
                "ci_cd_pipeline": {
                    "stages": ["unit_tests", "integration_tests", "e2e_tests", "performance_tests", "security_scan"]
                },
                "quality_gates": {"coverage_threshold": 95},
                "reporting": {"coverage_report": f"docs/test_reports/{story_id}_coverage.html"}
            }
            
            # Execute contract processing
            result = await te_agent.process_contract(sample_input_contract)
            
            # Verify output contract structure
            assert result["contract_version"] == "1.0"
            assert result["source_agent"] == "test_engineer"
            assert result["target_agent"] == "qa_tester"
            assert result["story_id"] == story_id
            
            # Verify required sections exist
            required_sections = [
                "dna_compliance", "input_requirements", "output_specifications",
                "quality_gates", "handoff_criteria"
            ]
            
            for section in required_sections:
                assert section in result, f"Missing required section: {section}"
            
            # Verify AI optimization results are included
            ai_results = result["input_requirements"]["required_data"]["ai_optimization_results"]
            assert ai_results["optimization_score"] == 4.5
            assert ai_results["time_savings_minutes"] == 20.0
            
            # Verify DNA compliance is enhanced
            assert "test_engineer_dna_validation" in result["dna_compliance"]
            assert result["dna_compliance"]["test_engineer_dna_validation"]["overall_dna_compliant"] is True
            
            # Verify team progress notifications were called
            assert mock_notify.call_count >= 5  # testing_started, various completion events
    
    @pytest.mark.asyncio
    async def test_implementation_testability_validation(self, te_agent, sample_component_implementation, sample_api_implementation):
        """Test implementation testability validation logic."""
        # Test with valid implementations
        await te_agent._validate_implementation_testability(
            [sample_component_implementation], 
            [sample_api_implementation]
        )
        # Should not raise exception
        
        # Test with invalid component (TypeScript errors)
        invalid_component = sample_component_implementation.copy()
        invalid_component["typescript_errors"] = 5
        
        with pytest.raises(QualityGateError) as exc_info:
            await te_agent._validate_implementation_testability(
                [invalid_component], 
                [sample_api_implementation]
            )
        assert "TypeScript errors" in str(exc_info.value)
        
        # Test with invalid API (response time too high)
        invalid_api = sample_api_implementation.copy()
        invalid_api["estimated_response_time_ms"] = 250
        
        with pytest.raises(QualityGateError) as exc_info:
            await te_agent._validate_implementation_testability(
                [sample_component_implementation], 
                [invalid_api]
            )
        assert "response time budget" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_test_quality_gates_validation(self, te_agent):
        """Test quality gates validation logic."""
        # Test data that should pass all quality gates
        valid_integration_suite = {
            "coverage_percent": 96.0,
            "all_tests_passing": True
        }
        
        valid_e2e_suite = {
            "coverage_percent": 92.0,
            "all_tests_passing": True
        }
        
        valid_performance_results = {
            "average_api_response_time_ms": 150.0,
            "lighthouse_score": 94
        }
        
        valid_security_results = {
            "critical_vulnerabilities": [],
            "high_vulnerabilities": []
        }
        
        valid_coverage_report = {
            "overall_coverage_percent": 96.0
        }
        
        # Should not raise exception
        await te_agent._validate_test_quality_gates(
            valid_integration_suite,
            valid_e2e_suite,
            valid_performance_results,
            valid_security_results,
            valid_coverage_report
        )
        
        # Test with failing quality gates
        failing_integration_suite = valid_integration_suite.copy()
        failing_integration_suite["coverage_percent"] = 85.0  # Below 95% threshold
        
        with pytest.raises(QualityGateError) as exc_info:
            await te_agent._validate_test_quality_gates(
                failing_integration_suite,
                valid_e2e_suite,
                valid_performance_results,
                valid_security_results,
                valid_coverage_report
            )
        assert "Integration test coverage" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_automation_configuration_generation(self, te_agent):
        """Test CI/CD automation configuration generation."""
        story_id = "STORY-AUTOMATION-001"
        
        integration_suite = {"story_id": story_id, "total_test_cases": 10}
        e2e_suite = {"story_id": story_id, "total_scenarios": 5}
        performance_results = {"story_id": story_id, "average_api_response_time_ms": 160.0}
        
        automation_config = await te_agent._generate_automation_configuration(
            integration_suite,
            e2e_suite,
            performance_results,
            story_id
        )
        
        # Verify automation configuration structure
        assert automation_config["story_id"] == story_id
        assert "ci_cd_pipeline" in automation_config
        assert "quality_gates" in automation_config
        assert "reporting" in automation_config
        
        # Verify CI/CD pipeline stages
        stages = automation_config["ci_cd_pipeline"]["stages"]
        expected_stages = ["unit_tests", "integration_tests", "e2e_tests", "performance_tests", "security_scan"]
        for stage in expected_stages:
            assert stage in stages
        
        # Verify test commands include story_id
        test_commands = automation_config["ci_cd_pipeline"]["test_commands"]
        for command in test_commands.values():
            assert story_id in command
    
    @pytest.mark.asyncio
    async def test_quality_gate_checks(self, te_agent):
        """Test individual quality gate check methods."""
        # Test all tests passing check
        passing_deliverables = {
            "integration_test_suite": {"all_tests_passing": True},
            "e2e_test_suite": {"all_tests_passing": True}
        }
        assert te_agent._check_all_tests_passing(passing_deliverables) is True
        
        failing_deliverables = {
            "integration_test_suite": {"all_tests_passing": False},
            "e2e_test_suite": {"all_tests_passing": True}
        }
        assert te_agent._check_all_tests_passing(failing_deliverables) is False
        
        # Test coverage threshold check
        good_coverage = {"coverage_report": {"overall_coverage_percent": 96.0}}
        assert te_agent._check_coverage_threshold(good_coverage) is True
        
        poor_coverage = {"coverage_report": {"overall_coverage_percent": 85.0}}
        assert te_agent._check_coverage_threshold(poor_coverage) is False
        
        # Test performance targets check
        good_performance = {
            "performance_test_results": {
                "average_api_response_time_ms": 150.0,
                "lighthouse_score": 94
            }
        }
        assert te_agent._check_performance_targets(good_performance) is True
        
        poor_performance = {
            "performance_test_results": {
                "average_api_response_time_ms": 250.0,  # Exceeds 200ms budget
                "lighthouse_score": 85  # Below 90 minimum
            }
        }
        assert te_agent._check_performance_targets(poor_performance) is False
        
        # Test security scan check
        clean_security = {"security_scan_results": {"critical_vulnerabilities": [], "high_vulnerabilities": []}}
        assert te_agent._check_security_scan(clean_security) is True
        
        vulnerable_security = {
            "security_scan_results": {
                "critical_vulnerabilities": [{"type": "sql_injection"}],
                "high_vulnerabilities": []
            }
        }
        assert te_agent._check_security_scan(vulnerable_security) is False


class TestTestEngineerErrorHandling(TestTestEngineerAgent):
    """Test Test Engineer agent error handling and recovery."""
    
    @pytest.mark.asyncio
    async def test_process_contract_tool_failure(self, te_agent, sample_input_contract):
        """Test contract processing when tools fail."""
        # Mock test generator to raise exception
        with patch.object(te_agent.test_generator, 'generate_integration_tests') as mock_integration, \
             patch.object(te_agent, '_validate_implementation_testability') as mock_validate, \
             patch.object(te_agent.ai_test_optimizer, 'optimize_test_strategy') as mock_ai_optimizer:
            
            mock_validate.return_value = None
            
            class MockAIOptimizationResult:
                def __init__(self):
                    self.overall_optimization_score = 4.0
                    self.estimated_time_savings_minutes = 10.0
                    self.quality_improvement_score = 4.0
                    self.failure_predictions = []
                    self.test_priorities = []
                    self.edge_case_predictions = []
                    self.municipal_optimization_insights = {}
            
            mock_ai_optimizer.return_value = MockAIOptimizationResult()
            mock_integration.side_effect = Exception("Test generation failed")
            
            with pytest.raises(AgentExecutionError) as exc_info:
                await te_agent.process_contract(sample_input_contract)
            
            assert "Test Engineer processing failed" in str(exc_info.value)
            assert "Test generation failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_invalid_contract_handling(self, te_agent):
        """Test handling of invalid input contracts."""
        # Contract missing required fields
        invalid_contract = {
            "contract_version": "1.0",
            "story_id": "INVALID-001"
            # Missing other required fields
        }
        
        with pytest.raises(AgentExecutionError):
            await te_agent.process_contract(invalid_contract)
    
    @pytest.mark.asyncio
    async def test_dna_compliance_failure(self, te_agent, sample_input_contract):
        """Test handling when DNA validation fails."""
        with patch.object(te_agent, '_validate_implementation_testability') as mock_validate, \
             patch.object(te_agent.ai_test_optimizer, 'optimize_test_strategy') as mock_ai_optimizer, \
             patch.object(te_agent.test_generator, 'generate_integration_tests') as mock_integration, \
             patch.object(te_agent.test_generator, 'generate_e2e_tests') as mock_e2e, \
             patch.object(te_agent.performance_tester, 'run_comprehensive_performance_tests') as mock_perf, \
             patch.object(te_agent.security_scanner, 'run_comprehensive_security_scan') as mock_security, \
             patch.object(te_agent.coverage_analyzer, 'analyze_comprehensive_coverage') as mock_coverage, \
             patch.object(te_agent, '_validate_test_quality_gates') as mock_gates, \
             patch.object(te_agent.dna_test_validator, 'validate_test_dna_compliance') as mock_dna, \
             patch.object(te_agent, '_generate_automation_configuration') as mock_automation:
            
            # Setup mocks
            story_id = sample_input_contract["story_id"]
            mock_validate.return_value = None
            
            class MockAIOptimizationResult:
                def __init__(self):
                    self.overall_optimization_score = 4.0
                    self.estimated_time_savings_minutes = 10.0
                    self.quality_improvement_score = 4.0
                    self.failure_predictions = []
                    self.test_priorities = []
                    self.edge_case_predictions = []
                    self.municipal_optimization_insights = {}
            
            mock_ai_optimizer.return_value = MockAIOptimizationResult()
            mock_integration.return_value = {"story_id": story_id}
            mock_e2e.return_value = {"story_id": story_id}
            mock_perf.return_value = {"story_id": story_id}
            mock_security.return_value = {"story_id": story_id}
            mock_coverage.return_value = {"story_id": story_id}
            mock_gates.return_value = None
            mock_automation.return_value = {"story_id": story_id}
            
            # Mock DNA validation failure
            mock_dna.side_effect = DNAComplianceError("DNA validation failed")
            
            with pytest.raises(AgentExecutionError) as exc_info:
                await te_agent.process_contract(sample_input_contract)
            
            assert "Test Engineer processing failed" in str(exc_info.value)


class TestTestEngineerPerformance(TestTestEngineerAgent):
    """Test Test Engineer agent performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_contract_processing_performance(self, te_agent, sample_input_contract):
        """Test that contract processing completes within performance requirements."""
        # Mock all tools for fast execution
        with patch.object(te_agent, '_validate_implementation_testability') as mock_validate, \
             patch.object(te_agent.ai_test_optimizer, 'optimize_test_strategy') as mock_ai_optimizer, \
             patch.object(te_agent.test_generator, 'generate_integration_tests') as mock_integration, \
             patch.object(te_agent.test_generator, 'generate_e2e_tests') as mock_e2e, \
             patch.object(te_agent.performance_tester, 'run_comprehensive_performance_tests') as mock_perf, \
             patch.object(te_agent.security_scanner, 'run_comprehensive_security_scan') as mock_security, \
             patch.object(te_agent.coverage_analyzer, 'analyze_comprehensive_coverage') as mock_coverage, \
             patch.object(te_agent, '_validate_test_quality_gates') as mock_gates, \
             patch.object(te_agent.dna_test_validator, 'validate_test_dna_compliance') as mock_dna, \
             patch.object(te_agent, '_generate_automation_configuration') as mock_automation, \
             patch.object(te_agent, '_notify_team_progress') as mock_notify:
            
            # Setup fast-returning mocks
            story_id = sample_input_contract["story_id"]
            mock_validate.return_value = None
            
            class MockAIOptimizationResult:
                def __init__(self):
                    self.overall_optimization_score = 4.0
                    self.estimated_time_savings_minutes = 10.0
                    self.quality_improvement_score = 4.0
                    self.failure_predictions = []
                    self.test_priorities = []
                    self.edge_case_predictions = []
                    self.municipal_optimization_insights = {}
            
            mock_ai_optimizer.return_value = MockAIOptimizationResult()
            mock_integration.return_value = {"story_id": story_id}
            mock_e2e.return_value = {"story_id": story_id}
            mock_perf.return_value = {"story_id": story_id}
            mock_security.return_value = {"story_id": story_id}
            mock_coverage.return_value = {"story_id": story_id}
            mock_gates.return_value = None
            
            class MockDNAResult:
                def __init__(self):
                    self.quality_reviewer_metrics = {}
            
            mock_dna.return_value = MockDNAResult()
            mock_automation.return_value = {"story_id": story_id}
            
            # Measure execution time
            start_time = datetime.now()
            result = await te_agent.process_contract(sample_input_contract)
            end_time = datetime.now()
            
            execution_time = (end_time - start_time).total_seconds()
            
            # Should complete within reasonable time (< 5 seconds for mocked execution)
            assert execution_time < 5.0, f"Contract processing took {execution_time} seconds"
            assert result is not None
    
    def test_agent_memory_usage(self, te_config):
        """Test that agent initialization doesn't consume excessive memory."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create multiple agent instances
        agents = []
        for i in range(5):
            agent = TestEngineerAgent(te_config)
            agents.append(agent)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Should not use excessive memory (< 100MB for 5 instances)
        assert memory_increase < 100, f"Memory usage increased by {memory_increase}MB for 5 agent instances"