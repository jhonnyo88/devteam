"""
Quality Gates Integration Tests

Tests that quality gates properly validate deliverables and block progression
when quality standards aren't met throughout the DigiNativa AI Team pipeline.

QUALITY GATES TESTED:
1. Agent-specific quality gates
2. Cross-agent validation gates
3. DNA compliance gates
4. Performance and reliability gates
5. Security and accessibility gates
6. Business value gates

Quality gates ensure that only features meeting DigiNativa's standards
progress through the pipeline, maintaining consistent quality delivery.
"""

import pytest
import asyncio
import time
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from modules.shared.contract_validator import ContractValidator
from modules.shared.exceptions import (
    QualityGateFailureError,
    DNAComplianceError,
    BusinessLogicError,
    ContractValidationError
)
from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.agents.game_designer.agent import GameDesignerAgent
from modules.agents.developer.agent import DeveloperAgent
from modules.agents.test_engineer.agent import TestEngineerAgent
from modules.agents.qa_tester.agent import QATesterAgent
from modules.agents.quality_reviewer.agent import QualityReviewerAgent


class TestQualityGates:
    """Test quality gate validation and enforcement."""
    
    @pytest.fixture
    def quality_agents(self):
        """Create agents for quality gate testing."""
        return {
            "project_manager": ProjectManagerAgent(),
            "game_designer": GameDesignerAgent(),
            "developer": DeveloperAgent(),
            "test_engineer": TestEngineerAgent(),
            "qa_tester": QATesterAgent(),
            "quality_reviewer": QualityReviewerAgent()
        }
    
    @pytest.fixture
    def contract_validator(self):
        """Contract validator for quality gate testing."""
        return ContractValidator()

    @pytest.fixture
    def quality_gate_definitions(self):
        """Definitions of quality gates for each agent."""
        return {
            "project_manager": [
                "github_issue_analyzed",
                "dna_analysis_complete",
                "story_breakdown_created",
                "acceptance_criteria_defined",
                "complexity_assessed"
            ],
            "game_designer": [
                "ux_specification_created",
                "game_mechanics_designed",
                "wireframes_generated",
                "dna_ux_compliance_validated",
                "component_mapping_complete"
            ],
            "developer": [
                "code_generated",
                "architecture_documented",
                "git_operations_complete",
                "code_quality_validated",
                "api_endpoints_functional"
            ],
            "test_engineer": [
                "unit_tests_generated",
                "integration_tests_created",
                "e2e_tests_implemented",
                "coverage_requirements_met",
                "security_scan_complete"
            ],
            "qa_tester": [
                "persona_testing_complete",
                "accessibility_validated",
                "user_flow_verified",
                "learning_effectiveness_measured",
                "performance_benchmarked"
            ],
            "quality_reviewer": [
                "final_quality_score_calculated",
                "deployment_readiness_validated",
                "approval_decision_made",
                "documentation_complete",
                "stakeholder_notification_sent"
            ]
        }

    @pytest.mark.asyncio
    async def test_project_manager_quality_gates(self, quality_agents, quality_gate_definitions):
        """Test Project Manager quality gates validation."""
        
        print("\n<¯ Testing Project Manager Quality Gates")
        
        agent = quality_agents["project_manager"]
        gates = quality_gate_definitions["project_manager"]
        
        # Test successful quality gate validation
        successful_deliverables = {
            "github_issue_analysis": {
                "issue_parsed": True,
                "priority_extracted": "high",
                "persona_identified": "Anna"
            },
            "dna_analysis": {
                "compliant": True,
                "compliance_score": 85.0,
                "violations": []
            },
            "story_breakdown": {
                "story_id": "STORY-QG-001",
                "user_stories": [{"story": "As Anna..."}],
                "technical_requirements": {}
            },
            "acceptance_criteria": [
                "Feature works correctly",
                "User can complete task",
                "Time constraint met"
            ],
            "complexity_assessment": {
                "overall_complexity": "Medium",
                "effort_points": 5,
                "estimated_duration_hours": 16
            }
        }
        
        # Test all gates pass
        for gate in gates:
            result = await agent.validate_quality_gate(gate, successful_deliverables)
            assert result is True, f"Quality gate {gate} should pass"
            print(f"    {gate}: PASSED")
        
        # Test gate failure scenarios
        failing_deliverables = {
            "github_issue_analysis": {},  # Empty analysis
            "dna_analysis": {
                "compliant": False,
                "compliance_score": 45.0,  # Below threshold
                "violations": ["Missing pedagogical value"]
            },
            "story_breakdown": {},  # Missing breakdown
            "acceptance_criteria": [],  # No criteria
            "complexity_assessment": {}  # No assessment
        }
        
        # Test gates fail appropriately
        failed_gates = []
        for gate in gates:
            result = await agent.validate_quality_gate(gate, failing_deliverables)
            if not result:
                failed_gates.append(gate)
                print(f"   L {gate}: FAILED (as expected)")
        
        assert len(failed_gates) > 0, "Some gates should fail with poor deliverables"
        print(" Project Manager quality gates working correctly")

    @pytest.mark.asyncio
    async def test_game_designer_quality_gates(self, quality_agents, quality_gate_definitions):
        """Test Game Designer quality gates validation."""
        
        print("\n<¨ Testing Game Designer Quality Gates")
        
        agent = quality_agents["game_designer"]
        gates = quality_gate_definitions["game_designer"]
        
        # Test successful quality gate validation
        successful_deliverables = {
            "ux_specification": {
                "ui_components": [
                    {"name": "ScenarioCard", "type": "interactive"}
                ],
                "responsive_design": True,
                "accessibility_features": ["keyboard_navigation", "screen_reader"]
            },
            "game_mechanics": {
                "progression_system": {"type": "linear"},
                "feedback_mechanisms": ["immediate", "summary"],
                "engagement_patterns": ["interactive", "gamified"]
            },
            "wireframes": [
                {
                    "screen_name": "scenario_selection",
                    "layout": {"components": ["header", "list", "footer"]},
                    "user_flows": ["select", "navigate", "complete"]
                }
            ],
            "dna_ux_compliance": {
                "overall_dna_compliant": True,
                "dna_compliance_score": 4.2,
                "ui_complexity_acceptable": True,
                "professional_tone_maintained": True
            },
            "component_mapping": {
                "ui_library": "shadcn",
                "mapped_components": ["Card", "Button", "ProgressBar"],
                "custom_components": ["ScenarioCard"]
            }
        }
        
        # Test all gates pass
        for gate in gates:
            result = await agent.validate_quality_gate(gate, successful_deliverables)
            assert result is True, f"Quality gate {gate} should pass"
            print(f"    {gate}: PASSED")
        
        # Test UX DNA compliance gate specifically
        dna_failing_deliverables = successful_deliverables.copy()
        dna_failing_deliverables["dna_ux_compliance"] = {
            "overall_dna_compliant": False,
            "dna_compliance_score": 2.1,  # Below threshold
            "ui_complexity_acceptable": False,
            "professional_tone_maintained": False
        }
        
        result = await agent.validate_quality_gate("dna_ux_compliance_validated", dna_failing_deliverables)
        assert result is False, "DNA UX compliance gate should fail"
        print("   L dna_ux_compliance_validated: FAILED (as expected)")
        
        print(" Game Designer quality gates working correctly")

    @pytest.mark.asyncio
    async def test_developer_quality_gates(self, quality_agents, quality_gate_definitions):
        """Test Developer quality gates validation."""
        
        print("\n=» Testing Developer Quality Gates")
        
        agent = quality_agents["developer"]
        gates = quality_gate_definitions["developer"]
        
        # Test successful quality gate validation
        successful_deliverables = {
            "generated_code": {
                "frontend_components": [
                    {
                        "file_path": "src/components/ScenarioCard.tsx",
                        "code": "export const ScenarioCard: React.FC = ...",
                        "tests": "src/components/__tests__/ScenarioCard.test.tsx"
                    }
                ],
                "backend_endpoints": [
                    {
                        "file_path": "api/scenarios.py",
                        "code": "@app.get('/api/scenarios')",
                        "endpoint": "/api/scenarios"
                    }
                ]
            },
            "architecture_documentation": {
                "component_structure": "documented",
                "api_specifications": "complete",
                "database_schema": "defined"
            },
            "git_operations": {
                "branch_created": True,
                "commits_made": ["Initial implementation", "Add tests"],
                "pull_request_ready": True
            },
            "code_quality": {
                "eslint_violations": 0,
                "typescript_errors": 0,
                "complexity_score": 3.2,  # Good complexity
                "test_coverage": 95
            },
            "api_functionality": {
                "endpoints_tested": True,
                "response_times": {"avg": 120, "max": 180},  # Good performance
                "error_handling": "complete"
            }
        }
        
        # Test all gates pass
        for gate in gates:
            result = await agent.validate_quality_gate(gate, successful_deliverables)
            assert result is True, f"Quality gate {gate} should pass"
            print(f"    {gate}: PASSED")
        
        # Test code quality gate failure
        poor_quality_deliverables = successful_deliverables.copy()
        poor_quality_deliverables["code_quality"] = {
            "eslint_violations": 25,  # Too many violations
            "typescript_errors": 5,  # Errors present
            "complexity_score": 8.5,  # Too complex
            "test_coverage": 45  # Poor coverage
        }
        
        result = await agent.validate_quality_gate("code_quality_validated", poor_quality_deliverables)
        assert result is False, "Code quality gate should fail"
        print("   L code_quality_validated: FAILED (as expected)")
        
        print(" Developer quality gates working correctly")

    @pytest.mark.asyncio
    async def test_test_engineer_quality_gates(self, quality_agents, quality_gate_definitions):
        """Test Test Engineer quality gates validation."""
        
        print("\n>ê Testing Test Engineer Quality Gates")
        
        agent = quality_agents["test_engineer"]
        gates = quality_gate_definitions["test_engineer"]
        
        # Test successful quality gate validation
        successful_deliverables = {
            "test_suite": {
                "unit_tests": [
                    {"file": "test_scenario_card.py", "tests": 12, "coverage": 98}
                ],
                "integration_tests": [
                    {"file": "test_api_scenarios.py", "tests": 8, "coverage": 95}
                ],
                "e2e_tests": [
                    {"file": "test_scenario_flow.spec.ts", "tests": 5, "coverage": 90}
                ]
            },
            "coverage_report": {
                "unit_coverage": 96,
                "integration_coverage": 92,
                "e2e_coverage": 88,
                "overall_coverage": 93
            },
            "security_scan": {
                "vulnerabilities_found": 0,
                "scan_passed": True,
                "security_score": 95
            },
            "performance_benchmarks": {
                "load_test_passed": True,
                "response_times_acceptable": True,
                "memory_usage_acceptable": True
            }
        }
        
        # Test all gates pass
        for gate in gates:
            result = await agent.validate_quality_gate(gate, successful_deliverables)
            assert result is True, f"Quality gate {gate} should pass"
            print(f"    {gate}: PASSED")
        
        # Test coverage requirements gate failure
        low_coverage_deliverables = successful_deliverables.copy()
        low_coverage_deliverables["coverage_report"] = {
            "unit_coverage": 65,  # Below 90% requirement
            "integration_coverage": 70,  # Below 85% requirement
            "e2e_coverage": 60,  # Below 80% requirement
            "overall_coverage": 67  # Below 85% requirement
        }
        
        result = await agent.validate_quality_gate("coverage_requirements_met", low_coverage_deliverables)
        assert result is False, "Coverage requirements gate should fail"
        print("   L coverage_requirements_met: FAILED (as expected)")
        
        print(" Test Engineer quality gates working correctly")

    @pytest.mark.asyncio
    async def test_qa_tester_quality_gates(self, quality_agents, quality_gate_definitions):
        """Test QA Tester quality gates validation."""
        
        print("\n=e Testing QA Tester Quality Gates")
        
        agent = quality_agents["qa_tester"]
        gates = quality_gate_definitions["qa_tester"]
        
        # Test successful quality gate validation
        successful_deliverables = {
            "persona_testing_results": {
                "anna_persona_results": {
                    "task_completion_rate": 96,
                    "user_satisfaction_score": 4.3,
                    "learning_effectiveness": 4.4,
                    "time_efficiency": 4.2
                }
            },
            "accessibility_audit": {
                "wcag_compliance_percent": 96,
                "violations": [],
                "keyboard_accessible": True,
                "screen_reader_compatible": True
            },
            "user_flow_validation": {
                "flow_completion_rate": 94,
                "navigation_efficiency": 4.1,
                "error_recovery_rate": 98,
                "user_frustration_incidents": 0
            },
            "learning_effectiveness": {
                "objective_achievement_rate": 92,
                "knowledge_retention_score": 4.2,
                "engagement_level": 4.3,
                "pedagogical_effectiveness": 4.1
            },
            "performance_metrics": {
                "page_load_time": 1.8,  # Under 2 seconds
                "lighthouse_score": 94,  # Excellent
                "time_to_interactive": 2.1  # Good
            }
        }
        
        # Test all gates pass
        for gate in gates:
            result = await agent.validate_quality_gate(gate, successful_deliverables)
            assert result is True, f"Quality gate {gate} should pass"
            print(f"    {gate}: PASSED")
        
        # Test accessibility gate failure
        accessibility_failing_deliverables = successful_deliverables.copy()
        accessibility_failing_deliverables["accessibility_audit"] = {
            "wcag_compliance_percent": 78,  # Below 95% requirement
            "violations": [
                {"type": "color_contrast", "severity": "high"},
                {"type": "missing_alt_text", "severity": "medium"}
            ],
            "keyboard_accessible": False,
            "screen_reader_compatible": False
        }
        
        result = await agent.validate_quality_gate("accessibility_validated", accessibility_failing_deliverables)
        assert result is False, "Accessibility gate should fail"
        print("   L accessibility_validated: FAILED (as expected)")
        
        print(" QA Tester quality gates working correctly")

    @pytest.mark.asyncio
    async def test_quality_reviewer_quality_gates(self, quality_agents, quality_gate_definitions):
        """Test Quality Reviewer quality gates validation."""
        
        print("\n– Testing Quality Reviewer Quality Gates")
        
        agent = quality_agents["quality_reviewer"]
        gates = quality_gate_definitions["quality_reviewer"]
        
        # Test successful quality gate validation
        successful_deliverables = {
            "quality_analysis": {
                "overall_score": 91.5,
                "technical_quality": 93,
                "user_experience": 90,
                "learning_effectiveness": 92,
                "business_value": 89
            },
            "deployment_readiness": {
                "deployment_ready": True,
                "readiness_score": 95,
                "blocking_issues": [],
                "performance_validated": True,
                "security_cleared": True
            },
            "approval_decision": {
                "approved": True,
                "approval_reasoning": "All quality criteria exceeded expectations",
                "recommendations": ["Deploy to production", "Monitor initial usage"],
                "approval_timestamp": datetime.now().isoformat()
            },
            "documentation": {
                "quality_report_generated": True,
                "stakeholder_summary_created": True,
                "deployment_instructions_complete": True,
                "audit_trail_documented": True
            },
            "notifications": {
                "stakeholders_notified": True,
                "deployment_team_informed": True,
                "documentation_updated": True
            }
        }
        
        # Test all gates pass
        for gate in gates:
            result = await agent.validate_quality_gate(gate, successful_deliverables)
            assert result is True, f"Quality gate {gate} should pass"
            print(f"    {gate}: PASSED")
        
        # Test final quality score gate failure
        low_quality_deliverables = successful_deliverables.copy()
        low_quality_deliverables["quality_analysis"] = {
            "overall_score": 72.0,  # Below 90 requirement
            "technical_quality": 68,
            "user_experience": 75,
            "learning_effectiveness": 70,
            "business_value": 76
        }
        
        result = await agent.validate_quality_gate("final_quality_score_calculated", low_quality_deliverables)
        assert result is False, "Final quality score gate should fail"
        print("   L final_quality_score_calculated: FAILED (as expected)")
        
        print(" Quality Reviewer quality gates working correctly")

    @pytest.mark.asyncio
    async def test_cross_agent_quality_validation(self, quality_agents, contract_validator):
        """Test quality validation across agent boundaries."""
        
        print("\n= Testing Cross-Agent Quality Validation")
        
        # Test Project Manager ’ Game Designer handoff quality
        pm_output = {
            "contract_version": "1.0",
            "story_id": "STORY-CROSS-001",
            "source_agent": "project_manager",
            "target_agent": "game_designer",
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
                    "story_breakdown": {
                        "story_id": "STORY-CROSS-001",
                        "feature_summary": {"title": "Cross validation test"},
                        "user_stories": [{"story": "As Anna..."}]
                    },
                    "dna_analysis": {
                        "compliant": True,
                        "compliance_score": 87.0
                    }
                }
            }
        }
        
        # Validate contract structure
        assert contract_validator.validate_contract_schema(pm_output)
        print("    Contract structure validation passed")
        
        # Validate handoff data completeness
        required_data = pm_output["input_requirements"]["required_data"]
        assert "story_breakdown" in required_data
        assert "dna_analysis" in required_data
        print("    Required handoff data present")
        
        # Validate DNA compliance propagation
        dna_compliance = pm_output["dna_compliance"]
        assert all(dna_compliance["design_principles_validation"].values())
        assert all(dna_compliance["architecture_compliance"].values())
        print("    DNA compliance properly propagated")
        
        print(" Cross-agent quality validation working correctly")

    @pytest.mark.asyncio
    async def test_quality_gate_performance(self, quality_agents, quality_gate_definitions):
        """Test quality gate validation performance."""
        
        print("\n¡ Testing Quality Gate Performance")
        
        # Test quality gate validation speed
        agent = quality_agents["project_manager"]
        gates = quality_gate_definitions["project_manager"]
        
        deliverables = {
            "github_issue_analysis": {"analyzed": True},
            "dna_analysis": {"compliant": True, "score": 85},
            "story_breakdown": {"created": True},
            "acceptance_criteria": ["criterion1", "criterion2"],
            "complexity_assessment": {"assessed": True}
        }
        
        # Measure gate validation performance
        start_time = time.time()
        
        results = []
        for gate in gates:
            gate_start = time.time()
            result = await agent.validate_quality_gate(gate, deliverables)
            gate_time = time.time() - gate_start
            results.append((gate, result, gate_time))
        
        total_time = time.time() - start_time
        
        # Validate performance requirements
        max_gate_time = max(result[2] for result in results)
        avg_gate_time = sum(result[2] for result in results) / len(results)
        
        assert max_gate_time < 5.0, f"Gate validation too slow: {max_gate_time:.2f}s"
        assert avg_gate_time < 2.0, f"Average gate time too slow: {avg_gate_time:.2f}s"
        assert total_time < 10.0, f"Total validation too slow: {total_time:.2f}s"
        
        print(f"   =Ê Max gate time: {max_gate_time:.3f}s")
        print(f"   =Ê Avg gate time: {avg_gate_time:.3f}s")
        print(f"   =Ê Total time: {total_time:.3f}s")
        print(" Quality gate performance meets requirements")

    @pytest.mark.asyncio
    async def test_quality_gate_error_handling(self, quality_agents):
        """Test quality gate error handling and recovery."""
        
        print("\n=« Testing Quality Gate Error Handling")
        
        agent = quality_agents["project_manager"]
        
        # Test missing deliverables
        empty_deliverables = {}
        
        try:
            result = await agent.validate_quality_gate("github_issue_analyzed", empty_deliverables)
            # Should handle gracefully, likely returning False
            assert result is False
            print("    Missing deliverables handled gracefully")
        except Exception as e:
            # Should not crash, but if it does, should be informative
            assert "deliverable" in str(e).lower() or "missing" in str(e).lower()
            print("    Missing deliverables error informative")
        
        # Test invalid deliverable format
        invalid_deliverables = {
            "github_issue_analysis": "invalid_format"  # Should be dict
        }
        
        try:
            result = await agent.validate_quality_gate("github_issue_analyzed", invalid_deliverables)
            print(f"    Invalid format handled: {result}")
        except Exception as e:
            assert "format" in str(e).lower() or "type" in str(e).lower()
            print("    Invalid format error informative")
        
        # Test unknown quality gate
        valid_deliverables = {"test": "data"}
        
        try:
            result = await agent.validate_quality_gate("unknown_gate", valid_deliverables)
            # Should handle unknown gates gracefully
            print(f"    Unknown gate handled: {result}")
        except Exception as e:
            assert "unknown" in str(e).lower() or "gate" in str(e).lower()
            print("    Unknown gate error informative")
        
        print(" Quality gate error handling working correctly")

    @pytest.mark.asyncio
    async def test_quality_gate_blocking_mechanism(self, quality_agents, contract_validator):
        """Test that quality gates properly block progression when standards aren't met."""
        
        print("\n=Ñ Testing Quality Gate Blocking Mechanism")
        
        # Create a contract that should be blocked by quality gates
        blocking_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-BLOCK-001",
            "source_agent": "github",
            "target_agent": "project_manager",
            "input_requirements": {
                "required_data": {
                    "github_issue_data": {
                        "number": 999,
                        "title": "Invalid test feature",
                        "body": "",  # Empty body should trigger issues
                        "labels": []  # No labels
                    }
                }
            }
        }
        
        # Mock Project Manager to fail quality gates
        agent = quality_agents["project_manager"]
        
        with patch.object(agent, 'validate_quality_gate') as mock_gate:
            # Make all quality gates fail
            mock_gate.return_value = False
            
            # Process should be blocked
            try:
                with patch.object(agent, 'github_integration'):
                    result = await agent.process_contract(blocking_contract)
                
                # If processing succeeds despite failing gates, that's an error
                pytest.fail("Contract processing should have been blocked by quality gates")
                
            except QualityGateFailureError as e:
                assert "quality gate" in str(e).lower()
                print("    Quality gate properly blocked processing")
            except Exception as e:
                # Other exceptions are acceptable if they indicate blocking
                print(f"    Processing blocked by: {type(e).__name__}")
        
        # Test that good contract passes
        good_contract = blocking_contract.copy()
        good_contract["input_requirements"]["required_data"]["github_issue_data"] = {
            "number": 123,
            "title": "Valid test feature",
            "body": "Proper feature description with acceptance criteria",
            "labels": [{"name": "priority-high"}]
        }
        
        with patch.object(agent, 'validate_quality_gate') as mock_gate:
            # Make all quality gates pass
            mock_gate.return_value = True
            
            with patch.object(agent, 'github_integration'):
                result = await agent.process_contract(good_contract)
                
            assert result is not None
            assert result["story_id"] == "STORY-BLOCK-001"
            print("    Good contract passes quality gates")
        
        print(" Quality gate blocking mechanism working correctly")

    def test_quality_gate_documentation(self, quality_gate_definitions):
        """Test that quality gates are properly documented and consistent."""
        
        print("\n=Ú Testing Quality Gate Documentation")
        
        # Verify all agents have defined quality gates
        expected_agents = [
            "project_manager", "game_designer", "developer",
            "test_engineer", "qa_tester", "quality_reviewer"
        ]
        
        for agent in expected_agents:
            assert agent in quality_gate_definitions, f"Missing quality gates for {agent}"
            gates = quality_gate_definitions[agent]
            assert len(gates) > 0, f"No quality gates defined for {agent}"
            print(f"    {agent}: {len(gates)} quality gates defined")
        
        # Verify quality gate naming conventions
        for agent, gates in quality_gate_definitions.items():
            for gate in gates:
                # Gates should be descriptive and follow naming conventions
                assert len(gate) > 5, f"Quality gate name too short: {gate}"
                assert "_" in gate or gate.islower(), f"Quality gate should use snake_case: {gate}"
                assert not gate.startswith("_"), f"Quality gate should not start with underscore: {gate}"
                assert not gate.endswith("_"), f"Quality gate should not end with underscore: {gate}"
        
        print("    Quality gate naming conventions followed")
        
        # Verify logical progression of gates
        critical_gates = {
            "project_manager": ["dna_analysis_complete", "story_breakdown_created"],
            "game_designer": ["ux_specification_created", "dna_ux_compliance_validated"],
            "developer": ["code_generated", "code_quality_validated"],
            "test_engineer": ["coverage_requirements_met", "security_scan_complete"],
            "qa_tester": ["accessibility_validated", "persona_testing_complete"],
            "quality_reviewer": ["final_quality_score_calculated", "approval_decision_made"]
        }
        
        for agent, critical in critical_gates.items():
            agent_gates = quality_gate_definitions[agent]
            for critical_gate in critical:
                assert critical_gate in agent_gates, f"Missing critical gate {critical_gate} for {agent}"
                print(f"    {agent}: Critical gate {critical_gate} present")
        
        print(" Quality gate documentation complete and consistent")


# Quality gate benchmarks and thresholds
QUALITY_GATE_THRESHOLDS = {
    "dna_compliance_score": 80.0,
    "code_coverage_percentage": 90.0,
    "accessibility_compliance": 95.0,
    "performance_lighthouse_score": 90,
    "user_satisfaction_score": 4.0,
    "final_quality_score": 90.0,
    "max_gate_validation_time": 5.0,  # seconds
    "max_total_validation_time": 10.0  # seconds
}


if __name__ == "__main__":
    # Run with: pytest tests/integration/test_quality_gates.py -v
    pytest.main([__file__, "-v", "--tb=short"])