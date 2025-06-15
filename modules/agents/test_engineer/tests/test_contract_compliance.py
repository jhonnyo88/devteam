"""
Test Engineer Agent - Contract Compliance Tests

PURPOSE:
Validates that Test Engineer agent maintains contract compliance
according to TEST_STRATEGY.md requirements.

CRITICAL IMPORTANCE:
These tests ensure the Test Engineer agent can work with the team without
breaking the modular architecture that the contract system enables.

VALIDATES:
- Contract schema for Test Engineer input/output according to Implementation_rules.md
- Agent sequence: developer → test_engineer → qa_tester
- DNA compliance structure (5 design + 4 architecture principles)
- File naming conventions (story_id inclusion)
- Quality gates and handoff criteria
- Uses mocks for agent tools to avoid real execution
"""

import pytest
import asyncio
import json
from typing import Dict, Any
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock

# Import using absolute path to avoid relative import issues
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from modules.agents.test_engineer.agent import TestEngineerAgent
from modules.agents.test_engineer.contracts import TestEngineerInputContract, TestEngineerOutputContract
from modules.shared.contract_validator import ContractValidator
from modules.shared.exceptions import ContractValidationError, AgentExecutionError, QualityGateError


@pytest.mark.contract
class TestTestEngineerContractCompliance:
    """Test suite for Test Engineer contract compliance."""
    
    @pytest.fixture
    def contract_validator(self):
        """Create ContractValidator instance."""
        return ContractValidator()
    
    @pytest.fixture
    def test_engineer_agent(self):
        """Create Test Engineer agent instance."""
        config = {
            "test_output_path": "test_tests",
            "coverage_threshold": 95,
            "performance_budget": {
                "api_response_time_ms": 200,
                "lighthouse_score": 90,
                "bundle_size_kb": 500
            }
        }
        return TestEngineerAgent(config)
    
    @pytest.fixture
    def valid_developer_input_contract(self):
        """
        Valid contract from Developer agent as defined in Implementation_rules.md.
        
        This is the EXACT contract specification that Developer must produce
        and Test Engineer must accept.
        """
        story_id = "STORY-TE-CONTRACT-001"
        
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
                    "time_respect_compliant": True,
                    "pedagogical_value_compliant": True,
                    "professional_tone_compliant": True,
                    "dna_compliance_score": 4.5,
                    "validation_timestamp": "2024-01-15T10:00:00Z"
                }
            },
            "input_requirements": {
                "required_files": [
                    f"src/components/{story_id}/UserRegistration.tsx",
                    f"src/api/endpoints/{story_id}/registration.py",
                    f"tests/unit/{story_id}/test_user_registration.py"
                ],
                "required_data": {
                    "component_implementations": [
                        {
                            "name": "UserRegistration",
                            "type": "react_component",
                            "files": {
                                "component": f"src/components/{story_id}/UserRegistration.tsx",
                                "test": f"tests/unit/{story_id}/test_user_registration.tsx",
                                "styles": f"src/components/{story_id}/UserRegistration.module.css"
                            },
                            "code": {
                                "component": "// React component code here",
                                "test": "// Jest test code here"
                            },
                            "typescript_errors": 0,
                            "eslint_violations": 0,
                            "test_coverage_percent": 100.0,
                            "accessibility_score": 95,
                            "performance_score": 90,
                            "integration_test_passed": True
                        }
                    ],
                    "api_implementations": [
                        {
                            "name": "registration_endpoint",
                            "method": "POST",
                            "path": "/api/register",
                            "files": {
                                "endpoint": f"src/api/endpoints/{story_id}/registration.py",
                                "test": f"tests/unit/{story_id}/test_registration_api.py"
                            },
                            "code": {
                                "endpoint": "# FastAPI endpoint code here",
                                "test": "# pytest code here"
                            },
                            "functional_test_passed": True,
                            "performance_test_passed": True,
                            "security_test_passed": True,
                            "estimated_response_time_ms": 150
                        }
                    ],
                    "test_suite": {
                        "story_id": story_id,
                        "unit_tests": [
                            {"name": "test_user_registration_component", "status": "passing"},
                            {"name": "test_registration_api_endpoint", "status": "passing"}
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
                        "implementation_summary": {
                            "components_created": 1,
                            "apis_created": 1,
                            "tests_created": 2
                        },
                        "architecture_compliance": {
                            "api_first": True,
                            "stateless_backend": True,
                            "separation_of_concerns": True,
                            "simplicity_first": True
                        },
                        "performance_metrics": {
                            "api_response_time_ms": 150,
                            "bundle_size_kb": 200,
                            "lighthouse_score": 90
                        },
                        "deployment_instructions": {
                            "build_command": "npm run build",
                            "test_command": "npm test"
                        },
                        "user_flows": [
                            {
                                "name": "user_registration_flow",
                                "description": "User creates account and logs in",
                                "steps": ["open_form", "fill_details", "submit", "verify_email", "login"]
                            }
                        ]
                    },
                    "git_commit_hash": "abc123def456"
                },
                "required_validations": [
                    "component_tests_passing",
                    "api_tests_passing",
                    "performance_requirements_met",
                    "accessibility_standards_met"
                ]
            },
            "output_specifications": {
                "deliverable_files": [],
                "deliverable_data": {},
                "validation_criteria": {}
            },
            "quality_gates": [
                "all_implementation_tests_passing",
                "performance_benchmarks_met",
                "accessibility_requirements_satisfied",
                "security_standards_verified"
            ],
            "handoff_criteria": [
                "code_review_approved",
                "implementation_complete",
                "documentation_updated",
                "deployment_ready"
            ]
        }
    
    def test_contract_structure_validation(self, contract_validator, valid_developer_input_contract):
        """Test that Developer input contract structure is valid."""
        validation_result = contract_validator.validate_contract(valid_developer_input_contract)
        
        assert validation_result["is_valid"] is True, f"Contract validation failed: {validation_result['errors']}"
        assert len(validation_result["errors"]) == 0
        
        # Verify agent sequence is correct
        assert valid_developer_input_contract["source_agent"] == "developer"
        assert valid_developer_input_contract["target_agent"] == "test_engineer"
    
    def test_dna_compliance_structure(self, valid_developer_input_contract):
        """Test DNA compliance structure matches requirements."""
        dna_compliance = valid_developer_input_contract["dna_compliance"]
        
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
        
        # Check developer DNA validation results (from Developer agent)
        developer_dna = dna_compliance["developer_dna_validation"]
        assert "overall_dna_compliant" in developer_dna
        assert "dna_compliance_score" in developer_dna
        assert isinstance(developer_dna["dna_compliance_score"], (int, float))
    
    def test_te_output_contract_structure(self, test_engineer_agent, valid_developer_input_contract):
        """Test that Test Engineer produces correctly structured output contract."""
        # Mock all the tools to avoid actual execution
        with patch.object(test_engineer_agent.test_generator, 'generate_integration_tests', new_callable=AsyncMock) as mock_integration, \
             patch.object(test_engineer_agent.test_generator, 'generate_e2e_tests', new_callable=AsyncMock) as mock_e2e, \
             patch.object(test_engineer_agent.performance_tester, 'run_comprehensive_performance_tests', new_callable=AsyncMock) as mock_perf, \
             patch.object(test_engineer_agent.security_scanner, 'run_comprehensive_security_scan', new_callable=AsyncMock) as mock_security, \
             patch.object(test_engineer_agent.coverage_analyzer, 'analyze_comprehensive_coverage', new_callable=AsyncMock) as mock_coverage, \
             patch.object(test_engineer_agent.dna_test_validator, 'validate_test_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(test_engineer_agent.ai_test_optimizer, 'optimize_test_strategy', new_callable=AsyncMock) as mock_ai_optimizer, \
             patch.object(test_engineer_agent, '_validate_implementation_testability', new_callable=AsyncMock) as mock_validate, \
             patch.object(test_engineer_agent, '_validate_test_quality_gates', new_callable=AsyncMock) as mock_gates, \
             patch.object(test_engineer_agent, '_generate_automation_configuration', new_callable=AsyncMock) as mock_automation:
            
            # Setup mock returns
            story_id = valid_developer_input_contract["story_id"]
            
            mock_integration.return_value = {
                "story_id": story_id,
                "test_type": "integration",
                "total_test_cases": 5,
                "coverage_percent": 95.0,
                "all_tests_passing": True,
                "test_cases": [
                    {"name": "test_user_registration_integration", "status": "passing"}
                ]
            }
            
            mock_e2e.return_value = {
                "story_id": story_id,
                "test_type": "end_to_end",
                "total_scenarios": 3,
                "coverage_percent": 90.0,
                "all_tests_passing": True,
                "scenarios": [
                    {"name": "user_registration_e2e", "status": "passing"}
                ]
            }
            
            mock_perf.return_value = {
                "story_id": story_id,
                "average_api_response_time_ms": 150.0,
                "lighthouse_score": 92,
                "bundle_size_kb": 200.0,
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
                "overall_coverage_percent": 95.0,
                "coverage_quality_met": True
            }
            
            # Mock DNA validation result
            class MockDNAResult:
                def __init__(self):
                    self.overall_dna_compliant = True
                    self.time_respect_compliant = True
                    self.pedagogical_value_compliant = True
                    self.professional_tone_compliant = True
                    self.dna_compliance_score = 4.5
                    self.validation_timestamp = "2024-01-15T10:00:00Z"
                    self.quality_reviewer_metrics = {
                        "test_execution_efficiency": 4.0,
                        "test_effectiveness": 4.5,
                        "test_documentation_quality": 4.2
                    }
            
            mock_dna.return_value = MockDNAResult()
            
            # Mock AI optimization result
            class MockAIOptimizationResult:
                def __init__(self):
                    self.overall_optimization_score = 4.3
                    self.estimated_time_savings_minutes = 15.0
                    self.quality_improvement_score = 4.1
                    self.failure_predictions = []
                    self.test_priorities = []
                    self.edge_case_predictions = []
                    self.municipal_optimization_insights = {}
            
            mock_ai_optimizer.return_value = MockAIOptimizationResult()
            
            mock_automation.return_value = {
                "story_id": story_id,
                "ci_cd_pipeline": {"stages": ["unit_tests", "integration_tests"]},
                "quality_gates": {"coverage_threshold": 95},
                "reporting": {"coverage_report": f"docs/test_reports/{story_id}_coverage.html"}
            }
            
            # Execute contract processing
            result = asyncio.run(test_engineer_agent.process_contract(valid_developer_input_contract))
            
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
    
    def test_te_output_deliverable_files_naming(self, test_engineer_agent, valid_developer_input_contract):
        """Test that Test Engineer output files follow naming convention."""
        with patch.object(test_engineer_agent.test_generator, 'generate_integration_tests', new_callable=AsyncMock) as mock_integration, \
             patch.object(test_engineer_agent.test_generator, 'generate_e2e_tests', new_callable=AsyncMock) as mock_e2e, \
             patch.object(test_engineer_agent.performance_tester, 'run_comprehensive_performance_tests', new_callable=AsyncMock) as mock_perf, \
             patch.object(test_engineer_agent.security_scanner, 'run_comprehensive_security_scan', new_callable=AsyncMock) as mock_security, \
             patch.object(test_engineer_agent.coverage_analyzer, 'analyze_comprehensive_coverage', new_callable=AsyncMock) as mock_coverage, \
             patch.object(test_engineer_agent.dna_test_validator, 'validate_test_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(test_engineer_agent.ai_test_optimizer, 'optimize_test_strategy', new_callable=AsyncMock) as mock_ai_optimizer, \
             patch.object(test_engineer_agent, '_validate_implementation_testability', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_validate_test_quality_gates', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_generate_automation_configuration', new_callable=AsyncMock) as mock_automation:
            
            # Setup minimal mock returns
            story_id = valid_developer_input_contract["story_id"]
            
            mock_integration.return_value = {"story_id": story_id, "total_test_cases": 1}
            mock_e2e.return_value = {"story_id": story_id, "total_scenarios": 1}
            mock_perf.return_value = {"story_id": story_id, "average_api_response_time_ms": 150.0}
            mock_security.return_value = {"story_id": story_id, "critical_vulnerabilities": []}
            mock_coverage.return_value = {"story_id": story_id, "overall_coverage_percent": 95.0}
            
            class MockDNAResult:
                def __init__(self):
                    self.overall_dna_compliant = True
                    self.quality_reviewer_metrics = {}
            
            mock_dna.return_value = MockDNAResult()
            
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
            
            mock_automation.return_value = {"story_id": story_id}
            
            result = asyncio.run(test_engineer_agent.process_contract(valid_developer_input_contract))
            
            deliverable_files = result["input_requirements"]["required_files"]
            
            # Expected file patterns for QA Tester input
            expected_patterns = [
                f"tests/integration/{story_id}/",
                f"tests/e2e/{story_id}/",
                f"docs/test_reports/{story_id}_coverage.html",
                f"docs/performance/{story_id}_benchmarks.json",
                f"docs/security/{story_id}_vulnerabilities.json"
            ]
            
            for expected in expected_patterns:
                assert expected in deliverable_files, f"Missing expected deliverable file: {expected}"
                
            # All files must contain story_id
            for file_path in deliverable_files:
                assert story_id in file_path, f"Deliverable file {file_path} missing story_id"
    
    def test_te_quality_gates_compliance(self, test_engineer_agent, valid_developer_input_contract):
        """Test that Test Engineer implements the correct quality gates."""
        with patch.object(test_engineer_agent.test_generator, 'generate_integration_tests', new_callable=AsyncMock) as mock_integration, \
             patch.object(test_engineer_agent.test_generator, 'generate_e2e_tests', new_callable=AsyncMock) as mock_e2e, \
             patch.object(test_engineer_agent.performance_tester, 'run_comprehensive_performance_tests', new_callable=AsyncMock) as mock_perf, \
             patch.object(test_engineer_agent.security_scanner, 'run_comprehensive_security_scan', new_callable=AsyncMock) as mock_security, \
             patch.object(test_engineer_agent.coverage_analyzer, 'analyze_comprehensive_coverage', new_callable=AsyncMock) as mock_coverage, \
             patch.object(test_engineer_agent.dna_test_validator, 'validate_test_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(test_engineer_agent.ai_test_optimizer, 'optimize_test_strategy', new_callable=AsyncMock) as mock_ai_optimizer, \
             patch.object(test_engineer_agent, '_validate_implementation_testability', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_validate_test_quality_gates', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_generate_automation_configuration', new_callable=AsyncMock) as mock_automation:
            
            story_id = valid_developer_input_contract["story_id"]
            
            mock_integration.return_value = {"story_id": story_id}
            mock_e2e.return_value = {"story_id": story_id}
            mock_perf.return_value = {"story_id": story_id}
            mock_security.return_value = {"story_id": story_id}
            mock_coverage.return_value = {"story_id": story_id}
            
            class MockDNAResult:
                def __init__(self):
                    self.quality_reviewer_metrics = {}
            
            mock_dna.return_value = MockDNAResult()
            
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
            mock_automation.return_value = {"story_id": story_id}
            
            result = asyncio.run(test_engineer_agent.process_contract(valid_developer_input_contract))
            
            quality_gates = result["quality_gates"]
            
            # Expected quality gates as defined in Implementation_rules.md
            expected_gates = [
                "all_automated_tests_passing",
                "performance_requirements_validated", 
                "security_compliance_verified",
                "accessibility_standards_met",
                "user_experience_validated"
            ]
            
            for expected_gate in expected_gates:
                assert expected_gate in quality_gates, f"Missing expected quality gate: {expected_gate}"
    
    def test_te_handoff_criteria_compliance(self, test_engineer_agent, valid_developer_input_contract):
        """Test that Test Engineer implements correct handoff criteria for QA Tester."""
        with patch.object(test_engineer_agent.test_generator, 'generate_integration_tests', new_callable=AsyncMock) as mock_integration, \
             patch.object(test_engineer_agent.test_generator, 'generate_e2e_tests', new_callable=AsyncMock) as mock_e2e, \
             patch.object(test_engineer_agent.performance_tester, 'run_comprehensive_performance_tests', new_callable=AsyncMock) as mock_perf, \
             patch.object(test_engineer_agent.security_scanner, 'run_comprehensive_security_scan', new_callable=AsyncMock) as mock_security, \
             patch.object(test_engineer_agent.coverage_analyzer, 'analyze_comprehensive_coverage', new_callable=AsyncMock) as mock_coverage, \
             patch.object(test_engineer_agent.dna_test_validator, 'validate_test_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(test_engineer_agent.ai_test_optimizer, 'optimize_test_strategy', new_callable=AsyncMock) as mock_ai_optimizer, \
             patch.object(test_engineer_agent, '_validate_implementation_testability', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_validate_test_quality_gates', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_generate_automation_configuration', new_callable=AsyncMock) as mock_automation:
            
            story_id = valid_developer_input_contract["story_id"]
            
            mock_integration.return_value = {"story_id": story_id}
            mock_e2e.return_value = {"story_id": story_id}
            mock_perf.return_value = {"story_id": story_id}
            mock_security.return_value = {"story_id": story_id}
            mock_coverage.return_value = {"story_id": story_id}
            
            class MockDNAResult:
                def __init__(self):
                    self.quality_reviewer_metrics = {}
            
            mock_dna.return_value = MockDNAResult()
            
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
            mock_automation.return_value = {"story_id": story_id}
            
            result = asyncio.run(test_engineer_agent.process_contract(valid_developer_input_contract))
            
            handoff_criteria = result["handoff_criteria"]
            
            # Expected handoff criteria for QA Tester
            expected_criteria = [
                "comprehensive_ux_validation_completed",
                "accessibility_compliance_verified",
                "persona_testing_successful",
                "usability_requirements_met",
                "quality_metrics_documented"
            ]
            
            for expected_criterion in expected_criteria:
                assert expected_criterion in handoff_criteria, f"Missing expected handoff criterion: {expected_criterion}"
    
    def test_agent_sequence_validation(self, contract_validator):
        """Test that agent sequence validation works correctly."""
        # Valid sequence: developer -> test_engineer
        assert contract_validator._validate_agent_sequence("developer", "test_engineer") is True
        
        # Valid sequence: test_engineer -> qa_tester  
        assert contract_validator._validate_agent_sequence("test_engineer", "qa_tester") is True
        
        # Invalid sequences
        assert contract_validator._validate_agent_sequence("test_engineer", "developer") is False
        assert contract_validator._validate_agent_sequence("qa_tester", "test_engineer") is False
        assert contract_validator._validate_agent_sequence("game_designer", "test_engineer") is False
    
    def test_te_ai_optimization_integration(self, test_engineer_agent, valid_developer_input_contract):
        """Test that AI optimization results are properly integrated into output contract."""
        with patch.object(test_engineer_agent.test_generator, 'generate_integration_tests', new_callable=AsyncMock) as mock_integration, \
             patch.object(test_engineer_agent.test_generator, 'generate_e2e_tests', new_callable=AsyncMock) as mock_e2e, \
             patch.object(test_engineer_agent.performance_tester, 'run_comprehensive_performance_tests', new_callable=AsyncMock) as mock_perf, \
             patch.object(test_engineer_agent.security_scanner, 'run_comprehensive_security_scan', new_callable=AsyncMock) as mock_security, \
             patch.object(test_engineer_agent.coverage_analyzer, 'analyze_comprehensive_coverage', new_callable=AsyncMock) as mock_coverage, \
             patch.object(test_engineer_agent.dna_test_validator, 'validate_test_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(test_engineer_agent.ai_test_optimizer, 'optimize_test_strategy', new_callable=AsyncMock) as mock_ai_optimizer, \
             patch.object(test_engineer_agent, '_validate_implementation_testability', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_validate_test_quality_gates', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_generate_automation_configuration', new_callable=AsyncMock) as mock_automation:
            
            story_id = valid_developer_input_contract["story_id"]
            
            # Setup comprehensive AI optimization mock
            class MockAIOptimizationResult:
                def __init__(self):
                    self.overall_optimization_score = 4.7
                    self.estimated_time_savings_minutes = 25.0
                    self.quality_improvement_score = 4.3
                    self.failure_predictions = [{"component": "test1", "probability": 0.3}]
                    self.test_priorities = [{"test_id": "priority1", "score": 85}]
                    self.edge_case_predictions = [{"scenario": "edge1", "likelihood": 0.6}]
                    self.municipal_optimization_insights = {
                        "anna_persona_priority_tests": 3,
                        "gdpr_compliance_focus_areas": 2
                    }
            
            mock_ai_optimizer.return_value = MockAIOptimizationResult()
            
            # Setup other mocks
            mock_integration.return_value = {"story_id": story_id}
            mock_e2e.return_value = {"story_id": story_id}
            mock_perf.return_value = {"story_id": story_id}
            mock_security.return_value = {"story_id": story_id}
            mock_coverage.return_value = {"story_id": story_id}
            
            class MockDNAResult:
                def __init__(self):
                    self.quality_reviewer_metrics = {}
            
            mock_dna.return_value = MockDNAResult()
            mock_automation.return_value = {"story_id": story_id}
            
            result = asyncio.run(test_engineer_agent.process_contract(valid_developer_input_contract))
            
            # Verify AI optimization results are included
            ai_results = result["input_requirements"]["required_data"]["ai_optimization_results"]
            
            assert ai_results["optimization_score"] == 4.7
            assert ai_results["time_savings_minutes"] == 25.0
            assert ai_results["quality_improvement_score"] == 4.3
            assert ai_results["failure_predictions"] == 1
            assert ai_results["test_priorities"] == 1
            assert ai_results["edge_case_predictions"] == 1
            assert "anna_persona_priority_tests" in ai_results["municipal_insights"]
    
    def test_contract_backward_compatibility(self, test_engineer_agent):
        """Test that Test Engineer maintains backward compatibility with contract changes."""
        # Test with minimal valid contract (should not break)
        minimal_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-MINIMAL-TE-001",
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
                }
            },
            "input_requirements": {
                "required_files": [],
                "required_data": {
                    "component_implementations": [],
                    "api_implementations": [],
                    "test_suite": {
                        "story_id": "STORY-MINIMAL-TE-001",
                        "unit_tests": [],
                        "coverage_percent": 100.0,
                        "total_test_cases": 0,
                        "test_configuration": {}
                    },
                    "implementation_docs": {
                        "story_id": "STORY-MINIMAL-TE-001",
                        "user_flows": []
                    },
                    "git_commit_hash": "minimal123"
                },
                "required_validations": []
            },
            "quality_gates": [],
            "handoff_criteria": []
        }
        
        with patch.object(test_engineer_agent.test_generator, 'generate_integration_tests', new_callable=AsyncMock) as mock_integration, \
             patch.object(test_engineer_agent.test_generator, 'generate_e2e_tests', new_callable=AsyncMock) as mock_e2e, \
             patch.object(test_engineer_agent.performance_tester, 'run_comprehensive_performance_tests', new_callable=AsyncMock) as mock_perf, \
             patch.object(test_engineer_agent.security_scanner, 'run_comprehensive_security_scan', new_callable=AsyncMock) as mock_security, \
             patch.object(test_engineer_agent.coverage_analyzer, 'analyze_comprehensive_coverage', new_callable=AsyncMock) as mock_coverage, \
             patch.object(test_engineer_agent.dna_test_validator, 'validate_test_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(test_engineer_agent.ai_test_optimizer, 'optimize_test_strategy', new_callable=AsyncMock) as mock_ai_optimizer, \
             patch.object(test_engineer_agent, '_validate_implementation_testability', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_validate_test_quality_gates', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_generate_automation_configuration', new_callable=AsyncMock) as mock_automation:
            
            # Setup minimal mocks
            mock_integration.return_value = {"story_id": "STORY-MINIMAL-TE-001"}
            mock_e2e.return_value = {"story_id": "STORY-MINIMAL-TE-001"}
            mock_perf.return_value = {"story_id": "STORY-MINIMAL-TE-001"}
            mock_security.return_value = {"story_id": "STORY-MINIMAL-TE-001"}
            mock_coverage.return_value = {"story_id": "STORY-MINIMAL-TE-001"}
            
            class MockDNAResult:
                def __init__(self):
                    self.quality_reviewer_metrics = {}
            
            mock_dna.return_value = MockDNAResult()
            
            class MockAIOptimizationResult:
                def __init__(self):
                    self.overall_optimization_score = 3.0
                    self.estimated_time_savings_minutes = 0.0
                    self.quality_improvement_score = 3.0
                    self.failure_predictions = []
                    self.test_priorities = []
                    self.edge_case_predictions = []
                    self.municipal_optimization_insights = {}
            
            mock_ai_optimizer.return_value = MockAIOptimizationResult()
            mock_automation.return_value = {"story_id": "STORY-MINIMAL-TE-001"}
            
            # Should not raise exception
            result = asyncio.run(test_engineer_agent.process_contract(minimal_contract))
            
            # Should still produce valid output structure
            assert result is not None
            assert result["contract_version"] == "1.0"
            assert result["source_agent"] == "test_engineer"
            assert result["target_agent"] == "qa_tester"
    
    def test_contract_validation_integration(self, contract_validator, test_engineer_agent, valid_developer_input_contract):
        """Test that contract validation integrates correctly with agent processing."""
        # First validate the input contract
        input_validation = contract_validator.validate_contract(valid_developer_input_contract)
        assert input_validation["is_valid"] is True
        
        # Process the contract with mocked tools
        with patch.object(test_engineer_agent.test_generator, 'generate_integration_tests', new_callable=AsyncMock) as mock_integration, \
             patch.object(test_engineer_agent.test_generator, 'generate_e2e_tests', new_callable=AsyncMock) as mock_e2e, \
             patch.object(test_engineer_agent.performance_tester, 'run_comprehensive_performance_tests', new_callable=AsyncMock) as mock_perf, \
             patch.object(test_engineer_agent.security_scanner, 'run_comprehensive_security_scan', new_callable=AsyncMock) as mock_security, \
             patch.object(test_engineer_agent.coverage_analyzer, 'analyze_comprehensive_coverage', new_callable=AsyncMock) as mock_coverage, \
             patch.object(test_engineer_agent.dna_test_validator, 'validate_test_dna_compliance', new_callable=AsyncMock) as mock_dna, \
             patch.object(test_engineer_agent.ai_test_optimizer, 'optimize_test_strategy', new_callable=AsyncMock) as mock_ai_optimizer, \
             patch.object(test_engineer_agent, '_validate_implementation_testability', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_validate_test_quality_gates', new_callable=AsyncMock), \
             patch.object(test_engineer_agent, '_generate_automation_configuration', new_callable=AsyncMock) as mock_automation:
            
            story_id = valid_developer_input_contract["story_id"]
            
            mock_integration.return_value = {"story_id": story_id}
            mock_e2e.return_value = {"story_id": story_id}
            mock_perf.return_value = {"story_id": story_id}
            mock_security.return_value = {"story_id": story_id}
            mock_coverage.return_value = {"story_id": story_id}
            
            class MockDNAResult:
                def __init__(self):
                    self.quality_reviewer_metrics = {}
            
            mock_dna.return_value = MockDNAResult()
            
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
            mock_automation.return_value = {"story_id": story_id}
            
            output_contract = asyncio.run(test_engineer_agent.process_contract(valid_developer_input_contract))
        
        # Validate the output contract
        output_validation = contract_validator.validate_contract(output_contract)
        assert output_validation["is_valid"] is True, f"Output contract validation failed: {output_validation['errors']}"
        
        # Verify agent sequence is correct for output
        assert output_contract["source_agent"] == "test_engineer"
        assert output_contract["target_agent"] == "qa_tester"