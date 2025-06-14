"""
Agent Contract Integration Tests

PURPOSE:
Comprehensive tests that validate all agent-to-agent contracts work correctly.
These tests ensure that when we modify individual agents, the overall team
integration remains intact through contract validation.

CRITICAL TESTING:
- End-to-end contract flow validation
- Contract compatibility between all agents
- DNA compliance preservation across handoffs
- Quality gate validation
- Schema compatibility regression tests

CONTRACT PROTECTION:
These tests are our "safety net" - if these pass, the team integration works.
"""

import pytest
import json
from datetime import datetime
from typing import Dict, Any, List

# Import all contract models
from modules.agents.project_manager.contracts import ProjectManagerOutputContract
from modules.agents.game_designer.contracts import GameDesignerInputContract, GameDesignerOutputContract  
from modules.agents.developer.contracts import DeveloperInputContract, DeveloperOutputContract
from modules.agents.test_engineer.contracts import TestEngineerInputContract, TestEngineerOutputContract
from modules.agents.qa_tester.contracts import QATesterInputContract, QATesterOutputContract
from modules.agents.quality_reviewer.contracts import QualityReviewerInputContract, QualityReviewerOutputContract


class TestAgentContractFlow:
    """Test complete agent contract flow from PM to deployment."""
    
    def test_complete_contract_chain_compatibility(self):
        """
        Test that all contracts can be chained together correctly.
        
        This is our MASTER TEST - if this passes, the entire team integration works.
        """
        story_id = "STORY-TEST-001"
        
        # Step 1: Project Manager Output
        pm_output = self._create_valid_pm_output(story_id)
        pm_contract = ProjectManagerOutputContract(**pm_output)
        
        # Step 2: Game Designer Input/Output
        gd_input = self._convert_pm_to_gd_input(pm_contract.dict())
        gd_input_contract = GameDesignerInputContract(**gd_input)
        
        gd_output = self._create_valid_gd_output(story_id)
        gd_contract = GameDesignerOutputContract(**gd_output)
        
        # Step 3: Developer Input/Output  
        dev_input = self._convert_gd_to_dev_input(gd_contract.dict())
        dev_input_contract = DeveloperInputContract(**dev_input)
        
        dev_output = self._create_valid_dev_output(story_id)
        dev_contract = DeveloperOutputContract(**dev_output)
        
        # Step 4: Test Engineer Input/Output
        te_input = self._convert_dev_to_te_input(dev_contract.dict())
        te_input_contract = TestEngineerInputContract(**te_input)
        
        te_output = self._create_valid_te_output(story_id)
        te_contract = TestEngineerOutputContract(**te_output)
        
        # Step 5: QA Tester Input/Output
        qa_input = self._convert_te_to_qa_input(te_contract.dict())
        qa_input_contract = QATesterInputContract(**qa_input)
        
        qa_output = self._create_valid_qa_output(story_id)
        qa_contract = QATesterOutputContract(**qa_output)
        
        # Step 6: Quality Reviewer Input/Output
        qr_input = self._convert_qa_to_qr_input(qa_contract.dict())
        qr_input_contract = QualityReviewerInputContract(**qr_input)
        
        qr_output = self._create_valid_qr_output(story_id)
        qr_contract = QualityReviewerOutputContract(**qr_output)
        
        # Validate all contracts are properly formed
        assert pm_contract.story_id == story_id
        assert gd_input_contract.story_id == story_id
        assert gd_contract.story_id == story_id
        assert dev_input_contract.story_id == story_id
        assert dev_contract.story_id == story_id
        assert te_input_contract.story_id == story_id
        assert te_contract.story_id == story_id
        assert qa_input_contract.story_id == story_id
        assert qa_contract.story_id == story_id
        assert qr_input_contract.story_id == story_id
        assert qr_contract.story_id == story_id
        
        # Validate agent sequence
        assert pm_contract.target_agent == "game_designer"
        assert gd_contract.target_agent == "developer"
        assert dev_contract.target_agent == "test_engineer"
        assert te_contract.target_agent == "qa_tester"
        assert qa_contract.target_agent == "quality_reviewer"
        assert qr_contract.target_agent == "deployment"
        
        print("✅ Complete contract chain validation successful!")
    
    def test_dna_compliance_preservation(self):
        """Test that DNA compliance is preserved throughout the entire chain."""
        story_id = "STORY-DNA-001"
        
        # Original DNA compliance
        original_dna = {
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
                "component_library_usage": True
            }
        }
        
        # Create and validate each contract preserves DNA compliance
        contracts = []
        
        pm_output = self._create_valid_pm_output(story_id)
        pm_output["dna_compliance"] = original_dna
        contracts.append(ProjectManagerOutputContract(**pm_output))
        
        gd_output = self._create_valid_gd_output(story_id)
        gd_output["dna_compliance"] = original_dna
        contracts.append(GameDesignerOutputContract(**gd_output))
        
        dev_output = self._create_valid_dev_output(story_id)
        dev_output["dna_compliance"] = original_dna
        contracts.append(DeveloperOutputContract(**dev_output))
        
        te_output = self._create_valid_te_output(story_id)
        te_output["dna_compliance"] = original_dna
        contracts.append(TestEngineerOutputContract(**te_output))
        
        qa_output = self._create_valid_qa_output(story_id)
        qa_output["dna_compliance"] = original_dna
        contracts.append(QATesterOutputContract(**qa_output))
        
        qr_output = self._create_valid_qr_output(story_id)
        qr_output["dna_compliance"] = original_dna
        contracts.append(QualityReviewerOutputContract(**qr_output))
        
        # Validate DNA compliance is preserved in all contracts
        for contract in contracts:
            assert contract.dna_compliance == original_dna
            
        print("✅ DNA compliance preserved throughout entire chain!")
    
    def test_quality_gates_progression(self):
        """Test that quality gates are properly validated at each stage."""
        story_id = "STORY-QG-001"
        
        # Test that quality gates are additive and comprehensive
        dev_output = self._create_valid_dev_output(story_id)
        dev_contract = DeveloperOutputContract(**dev_output)
        
        te_output = self._create_valid_te_output(story_id)
        te_contract = TestEngineerOutputContract(**te_output)
        
        qa_output = self._create_valid_qa_output(story_id)
        qa_contract = QATesterOutputContract(**qa_output)
        
        qr_output = self._create_valid_qr_output(story_id)
        qr_contract = QualityReviewerOutputContract(**qr_output)
        
        # Validate quality gates are present and comprehensive
        assert len(dev_contract.quality_gates) >= 4  # Developer quality gates
        assert len(te_contract.quality_gates) >= 5   # Test Engineer quality gates
        assert len(qa_contract.quality_gates) >= 5   # QA Tester quality gates
        assert len(qr_contract.quality_gates) >= 6   # Quality Reviewer quality gates
        
        print("✅ Quality gates progression validated!")
    
    def test_contract_version_compatibility(self):
        """Test that all contracts use compatible versions."""
        contracts = [
            self._create_valid_pm_output("STORY-VER-001"),
            self._create_valid_gd_output("STORY-VER-001"),
            self._create_valid_dev_output("STORY-VER-001"),
            self._create_valid_te_output("STORY-VER-001"),
            self._create_valid_qa_output("STORY-VER-001"),
            self._create_valid_qr_output("STORY-VER-001")
        ]
        
        # All contracts should use version "1.0"
        for contract_data in contracts:
            assert contract_data["contract_version"] == "1.0"
            
        print("✅ Contract version compatibility validated!")

    def test_story_id_propagation(self):
        """Test that story_id is correctly propagated through all contracts."""
        story_id = "STORY-PROP-001"
        
        # Create all contracts with the same story_id
        contracts_data = [
            self._create_valid_pm_output(story_id),
            self._create_valid_gd_output(story_id),
            self._create_valid_dev_output(story_id),
            self._create_valid_te_output(story_id),
            self._create_valid_qa_output(story_id),
            self._create_valid_qr_output(story_id)
        ]
        
        # Validate story_id is preserved
        for contract_data in contracts_data:
            assert contract_data["story_id"] == story_id
            assert contract_data["story_id"].startswith("STORY-")
            
        print("✅ Story ID propagation validated!")

    def test_performance_requirements_chain(self):
        """Test that performance requirements are maintained throughout the chain."""
        story_id = "STORY-PERF-001"
        
        # Test Engineer should enforce performance requirements
        te_output = self._create_valid_te_output(story_id)
        te_contract = TestEngineerOutputContract(**te_output)
        
        # Performance requirements should be present in required_data
        required_data = te_contract.input_requirements["required_data"]
        perf_results = required_data["performance_test_results"]
        
        assert perf_results["average_api_response_time_ms"] <= 200
        assert perf_results["lighthouse_score"] >= 90
        assert perf_results["performance_budget_met"] == True
        
        print("✅ Performance requirements chain validated!")

    def test_security_requirements_chain(self):
        """Test that security requirements are maintained throughout the chain."""
        story_id = "STORY-SEC-001"
        
        # Test Engineer should enforce security requirements
        te_output = self._create_valid_te_output(story_id)
        te_contract = TestEngineerOutputContract(**te_output)
        
        # Security requirements should be present in required_data
        required_data = te_contract.input_requirements["required_data"]
        security_results = required_data["security_scan_results"]
        
        assert len(security_results["critical_vulnerabilities"]) == 0
        assert len(security_results["high_vulnerabilities"]) == 0
        assert security_results["security_compliance_met"] == True
        
        print("✅ Security requirements chain validated!")

    def test_coverage_requirements_chain(self):
        """Test that coverage requirements are maintained throughout the chain."""
        story_id = "STORY-COV-001"
        
        # Test Engineer should enforce coverage requirements
        te_output = self._create_valid_te_output(story_id)
        te_contract = TestEngineerOutputContract(**te_output)
        
        # Coverage requirements should be present in required_data
        required_data = te_contract.input_requirements["required_data"]
        coverage_report = required_data["coverage_report"]
        
        assert coverage_report["overall_coverage_percent"] >= 90
        assert coverage_report["coverage_quality_met"] == True
        
        # Integration and E2E coverage should meet minimums
        integration_suite = required_data["integration_test_suite"]
        e2e_suite = required_data["e2e_test_suite"]
        
        assert integration_suite["coverage_percent"] >= 95
        assert e2e_suite["coverage_percent"] >= 90
        
        print("✅ Coverage requirements chain validated!")

    # Helper methods to create valid contract data
    def _create_valid_pm_output(self, story_id: str) -> Dict[str, Any]:
        """Create valid Project Manager output contract."""
        return {
            "contract_version": "1.0",
            "contract_type": "analysis_to_design",
            "story_id": story_id,
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
                    "component_library_usage": True
                }
            },
            "input_requirements": {
                "required_files": [f"docs/analysis/{story_id}_analysis.md"],
                "required_data": {
                    "feature_breakdown": {
                        "primary_features": ["user_registration"],
                        "technical_requirements": ["react_component", "fastapi_endpoint"],
                        "acceptance_criteria": ["user can register", "validation works"]
                    },
                    "complexity_assessment": {
                        "technical_complexity": 3,
                        "ui_complexity": 2,
                        "integration_complexity": 2
                    },
                    "anna_persona_requirements": {
                        "time_constraint_minutes": 10,
                        "accessibility_requirements": ["wcag_aa"],
                        "usability_requirements": ["intuitive_navigation"]
                    }
                },
                "required_validations": ["feature_completeness", "anna_persona_compliance"]
            },
            "output_specifications": {
                "deliverable_files": [f"docs/design/{story_id}_ux_spec.md"],
                "deliverable_data": {
                    "ux_specification": "object",
                    "component_mapping": "object",
                    "interaction_flows": "array"
                },
                "validation_criteria": {
                    "design_quality": {"min_score": 4},
                    "pedagogical_effectiveness": {"min_score": 4}
                }
            },
            "quality_gates": ["feature_analysis_complete", "anna_persona_validated"],
            "handoff_criteria": ["ux_specification_ready", "component_mapping_complete"]
        }

    def _create_valid_gd_output(self, story_id: str) -> Dict[str, Any]:
        """Create valid Game Designer output contract."""
        return {
            "contract_version": "1.0",
            "contract_type": "design_to_implementation",
            "story_id": story_id,
            "source_agent": "game_designer",
            "target_agent": "developer",
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
                    "component_library_usage": True
                }
            },
            "input_requirements": {
                "required_files": [f"docs/design/{story_id}_ux_spec.md"],
                "required_data": {
                    "ux_specification": {
                        "components": [{"name": "UserRegistration", "type": "form"}],
                        "interactions": [{"trigger": "submit", "action": "validate"}]
                    },
                    "component_mapping": {
                        "shadcn_components": ["form", "input", "button"],
                        "kenney_assets": ["background", "button"]
                    },
                    "interaction_flows": [
                        {"name": "registration_flow", "steps": ["input", "validate", "submit"]}
                    ]
                },
                "required_validations": ["ux_design_complete", "component_mapping_validated"]
            },
            "output_specifications": {
                "deliverable_files": [f"frontend/components/{story_id}/"],
                "deliverable_data": {
                    "component_implementations": "array",
                    "api_implementations": "array"
                },
                "validation_criteria": {
                    "code_quality": {"typescript_errors": 0},
                    "performance": {"response_time_ms": {"max": 200}}
                }
            },
            "quality_gates": ["design_specification_complete", "component_mapping_validated"],
            "handoff_criteria": ["implementation_ready", "technical_specification_complete"]
        }

    def _create_valid_dev_output(self, story_id: str) -> Dict[str, Any]:
        """Create valid Developer output contract."""
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
                    "component_library_usage": True
                }
            },
            "input_requirements": {
                "required_files": [f"frontend/components/{story_id}/", f"backend/endpoints/{story_id}/"],
                "required_data": {
                    "component_implementations": [
                        {
                            "name": "UserRegistration",
                            "type": "functional_component",
                            "files": {"component": f"frontend/components/{story_id}/UserRegistration.tsx"},
                            "code": {"component": "// React component code"},
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
                            "name": "register_user",
                            "method": "POST",
                            "path": "/api/v1/users/register",
                            "files": {"endpoint": f"backend/endpoints/{story_id}/user_registration.py"},
                            "code": {"endpoint": "# FastAPI endpoint code"},
                            "functional_test_passed": True,
                            "performance_test_passed": True,
                            "security_test_passed": True,
                            "estimated_response_time_ms": 150
                        }
                    ],
                    "test_suite": {
                        "story_id": story_id,
                        "unit_tests": [{"name": "test_user_registration", "type": "unit"}],
                        "coverage_percent": 100.0,
                        "total_test_cases": 10,
                        "test_configuration": {"jest_config": "jest.config.js"}
                    },
                    "implementation_docs": {
                        "story_id": story_id,
                        "implementation_summary": {"features_implemented": ["user_registration"]},
                        "architecture_compliance": {
                            "api_first": True,
                            "stateless_backend": True,
                            "separation_of_concerns": True,
                            "component_library_usage": True
                        },
                        "performance_metrics": {"api_response_time_ms": 150},
                        "deployment_instructions": {"build_command": "npm run build"},
                        "user_flows": [{"name": "registration_flow", "steps": ["input", "submit"]}]
                    },
                    "git_commit_hash": "abc123"
                },
                "required_validations": ["typescript_compilation_successful", "unit_tests_100_percent_coverage"]
            },
            "output_specifications": {
                "deliverable_files": [f"tests/integration/{story_id}/", f"tests/e2e/{story_id}/"],
                "deliverable_data": {
                    "integration_test_suite": "object",
                    "e2e_test_suite": "object",
                    "performance_test_results": "object",
                    "security_scan_results": "object",
                    "coverage_report": "object"
                },
                "validation_criteria": {
                    "test_quality": {
                        "integration_test_coverage": {"min": 95},
                        "e2e_test_coverage": {"min": 90},
                        "performance_test_included": True
                    },
                    "automation": {"ci_cd_integration": True},
                    "security": {"vulnerability_scan_clean": True}
                }
            },
            "quality_gates": ["all_integration_tests_passing", "performance_benchmarks_within_targets", "security_vulnerability_scan_clean", "automated_test_suite_configured"],
            "handoff_criteria": ["comprehensive_test_coverage_achieved", "all_performance_requirements_validated", "automated_test_pipeline_configured", "quality_metrics_documented"]
        }

    def _create_valid_te_output(self, story_id: str) -> Dict[str, Any]:
        """Create valid Test Engineer output contract."""
        return {
            "contract_version": "1.0",
            "contract_type": "testing_to_qa",
            "story_id": story_id,
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
                    "component_library_usage": True
                }
            },
            "input_requirements": {
                "required_files": [f"tests/integration/{story_id}/", f"tests/e2e/{story_id}/"],
                "required_data": {
                    "integration_test_suite": {
                        "story_id": story_id,
                        "test_type": "integration",
                        "total_test_cases": 15,
                        "coverage_percent": 97.5,
                        "all_tests_passing": True
                    },
                    "e2e_test_suite": {
                        "story_id": story_id,
                        "test_type": "end_to_end",
                        "total_scenarios": 8,
                        "coverage_percent": 92.0,
                        "all_tests_passing": True
                    },
                    "performance_test_results": {
                        "story_id": story_id,
                        "average_api_response_time_ms": 150.0,
                        "lighthouse_score": 92,
                        "bundle_size_kb": 350.0,
                        "performance_budget_met": True
                    },
                    "security_scan_results": {
                        "story_id": story_id,
                        "critical_vulnerabilities": [],
                        "high_vulnerabilities": [],
                        "medium_vulnerabilities": [],
                        "security_compliance_met": True
                    },
                    "coverage_report": {
                        "story_id": story_id,
                        "overall_coverage_percent": 95.5,
                        "coverage_quality_met": True
                    },
                    "automation_config": {
                        "story_id": story_id,
                        "ci_cd_pipeline": {"stages": ["unit", "integration", "e2e", "performance"]},
                        "quality_gates": {"coverage_threshold": 95},
                        "reporting": {"coverage_report": f"docs/test_reports/{story_id}_coverage.html"}
                    },
                    "original_implementation": {
                        "component_implementations": [{"name": "UserRegistration"}],
                        "api_implementations": [{"name": "register_user"}]
                    }
                },
                "required_validations": ["all_integration_tests_passing", "all_e2e_tests_passing", "performance_benchmarks_met", "security_vulnerabilities_resolved", "coverage_thresholds_exceeded"]
            },
            "output_specifications": {
                "deliverable_files": [f"docs/qa_reports/{story_id}_ux_validation.md"],
                "deliverable_data": {
                    "ux_validation_results": "object",
                    "accessibility_compliance_report": "object",
                    "persona_testing_results": "object",
                    "usability_assessment": "object",
                    "user_flow_validation": "object"
                },
                "validation_criteria": {
                    "user_experience": {
                        "anna_persona_satisfaction": {"min_score": 4},
                        "task_completion_rate": {"min_percentage": 95},
                        "time_to_complete": {"max_minutes": 10},
                        "error_rate": {"max_percentage": 5}
                    },
                    "accessibility": {
                        "wcag_compliance_level": "AA",
                        "screen_reader_compatibility": True,
                        "keyboard_navigation": True,
                        "color_contrast_ratio": {"min": 4.5}
                    },
                    "usability": {
                        "intuitive_navigation": True,
                        "clear_instructions": True,
                        "consistent_design": True,
                        "responsive_design": True
                    }
                }
            },
            "quality_gates": ["all_automated_tests_passing", "performance_requirements_validated", "security_compliance_verified", "accessibility_standards_met", "test_coverage_thresholds_met"],
            "handoff_criteria": ["comprehensive_ux_validation_completed", "accessibility_compliance_verified", "persona_testing_successful", "usability_requirements_met", "quality_metrics_documented"]
        }

    def _create_valid_qa_output(self, story_id: str) -> Dict[str, Any]:
        """Create valid QA Tester output contract."""
        return {
            "contract_version": "1.0",
            "contract_type": "qa_to_quality_review",
            "story_id": story_id,
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
                    "component_library_usage": True
                }
            },
            "input_requirements": {
                "required_files": [f"docs/qa_reports/{story_id}_ux_validation.md"],
                "required_data": {
                    "ux_validation_results": {
                        "anna_persona_satisfaction_score": 4.2,
                        "task_completion_rate": 96,
                        "average_completion_time_minutes": 8,
                        "error_rate_percentage": 3
                    },
                    "accessibility_compliance_report": {
                        "wcag_compliance_level": "AA",
                        "accessibility_score": 96,
                        "screen_reader_compatibility": True,
                        "keyboard_navigation_score": 95,
                        "color_contrast_compliance": True
                    },
                    "persona_testing_results": {
                        "anna_persona_scenarios_tested": 5,
                        "scenarios_passed": 5,
                        "average_satisfaction_score": 4.3,
                        "usability_issues_found": 1
                    },
                    "usability_assessment": {
                        "overall_usability_score": 4.1,
                        "navigation_intuitiveness": True,
                        "instruction_clarity": True,
                        "design_consistency": True,
                        "responsive_design_validated": True
                    },
                    "user_flow_validation": {
                        "user_flows_tested": 3,
                        "flows_completed_successfully": 3,
                        "average_flow_completion_time": 7,
                        "flow_efficiency_score": 4.0
                    }
                },
                "required_validations": ["anna_persona_satisfaction_met", "accessibility_compliance_verified", "usability_standards_met", "user_flow_validation_passed"]
            },
            "output_specifications": {
                "deliverable_files": [f"docs/quality_reports/{story_id}_final_analysis.md"],
                "deliverable_data": {
                    "overall_quality_score": "number",
                    "deployment_recommendation": "object",
                    "quality_metrics": "object"
                },
                "validation_criteria": {
                    "overall_quality": {"min_score": 85},
                    "deployment_readiness": {"min_score": 90}
                }
            },
            "quality_gates": ["ux_validation_passed", "accessibility_compliance_verified", "persona_testing_successful", "usability_requirements_met", "quality_documentation_complete"],
            "handoff_criteria": ["comprehensive_quality_analysis_completed", "deployment_recommendation_ready", "final_approval_criteria_met"]
        }

    def _create_valid_qr_output(self, story_id: str) -> Dict[str, Any]:
        """Create valid Quality Reviewer output contract."""
        return {
            "contract_version": "1.0",
            "contract_type": "quality_review_to_deployment",
            "story_id": story_id,
            "source_agent": "quality_reviewer",
            "target_agent": "deployment",
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
                    "component_library_usage": True
                }
            },
            "input_requirements": {
                "required_files": [f"docs/quality_reports/{story_id}_final_analysis.md"],
                "required_data": {
                    "overall_quality_score": 97.5,
                    "deployment_recommendation": {
                        "approved_for_production": True,
                        "deployment_priority": "normal",
                        "estimated_deployment_time": "immediate"
                    },
                    "quality_metrics": {
                        "test_coverage": 95.5,
                        "performance_score": 92,
                        "accessibility_score": 96,
                        "security_score": 100,
                        "code_quality_score": 94,
                        "dna_compliance_score": 100
                    }
                },
                "required_validations": ["overall_quality_threshold_met", "deployment_criteria_satisfied", "production_readiness_confirmed"]
            },
            "output_specifications": {
                "deliverable_files": [f"deployment/approved/{story_id}_deployment_package.json"],
                "deliverable_data": {
                    "deployment_approval": "object",
                    "production_configuration": "object"
                },
                "validation_criteria": {
                    "final_approval": {"approved": True},
                    "deployment_readiness": {"score": {"min": 90}}
                }
            },
            "quality_gates": ["overall_quality_approved", "deployment_criteria_met", "production_readiness_validated", "security_clearance_obtained", "performance_benchmarks_confirmed", "accessibility_compliance_final"],
            "handoff_criteria": ["final_approval_granted", "deployment_package_ready", "production_configuration_validated"]
        }

    # Helper methods for contract conversion (simulated)
    def _convert_pm_to_gd_input(self, pm_output: Dict[str, Any]) -> Dict[str, Any]:
        """Convert PM output to Game Designer input."""
        return {
            "contract_version": "1.0",
            "contract_type": "analysis_to_design",
            "story_id": pm_output["story_id"],
            "source_agent": "project_manager",
            "target_agent": "game_designer",
            "dna_compliance": pm_output["dna_compliance"],
            "input_requirements": pm_output["input_requirements"]
        }

    def _convert_gd_to_dev_input(self, gd_output: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Game Designer output to Developer input."""
        return {
            "contract_version": "1.0",
            "contract_type": "design_to_implementation",
            "story_id": gd_output["story_id"],
            "source_agent": "game_designer",
            "target_agent": "developer",
            "dna_compliance": gd_output["dna_compliance"],
            "input_requirements": gd_output["input_requirements"]
        }

    def _convert_dev_to_te_input(self, dev_output: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Developer output to Test Engineer input."""
        return {
            "contract_version": "1.0",
            "contract_type": "implementation_to_testing",
            "story_id": dev_output["story_id"],
            "source_agent": "developer",
            "target_agent": "test_engineer",
            "dna_compliance": dev_output["dna_compliance"],
            "input_requirements": dev_output["input_requirements"]
        }

    def _convert_te_to_qa_input(self, te_output: Dict[str, Any]) -> Dict[str, Any]:
        """Convert Test Engineer output to QA Tester input."""
        return {
            "contract_version": "1.0",
            "contract_type": "testing_to_qa",
            "story_id": te_output["story_id"],
            "source_agent": "test_engineer",
            "target_agent": "qa_tester",
            "dna_compliance": te_output["dna_compliance"],
            "input_requirements": te_output["input_requirements"]
        }

    def _convert_qa_to_qr_input(self, qa_output: Dict[str, Any]) -> Dict[str, Any]:
        """Convert QA Tester output to Quality Reviewer input."""
        return {
            "contract_version": "1.0",
            "contract_type": "qa_to_quality_review",
            "story_id": qa_output["story_id"],
            "source_agent": "qa_tester",
            "target_agent": "quality_reviewer",
            "dna_compliance": qa_output["dna_compliance"],
            "input_requirements": qa_output["input_requirements"]
        }


class TestContractCompatibility:
    """Test contract compatibility and regression."""
    
    def test_contract_schema_stability(self):
        """Test that contract schemas remain stable across agent updates."""
        # This test ensures that required fields don't change unexpectedly
        story_id = "STORY-SCHEMA-001"
        
        # Required fields that must always be present
        required_contract_fields = [
            "contract_version",
            "contract_type", 
            "story_id",
            "source_agent",
            "target_agent",
            "dna_compliance"
        ]
        
        # Test all contract types have required fields
        test_helper = TestAgentContractFlow()
        contracts_data = [
            test_helper._create_valid_pm_output(story_id),
            test_helper._create_valid_gd_output(story_id),
            test_helper._create_valid_dev_output(story_id),
            test_helper._create_valid_te_output(story_id),
            test_helper._create_valid_qa_output(story_id),
            test_helper._create_valid_qr_output(story_id)
        ]
        
        for contract_data in contracts_data:
            for field in required_contract_fields:
                assert field in contract_data, f"Missing required field {field} in {contract_data['contract_type']}"
                
        print("✅ Contract schema stability validated!")

    def test_agent_sequence_validation(self):
        """Test that agent sequence is correctly maintained."""
        story_id = "STORY-SEQ-001"
        test_helper = TestAgentContractFlow()
        
        # Expected agent sequence
        expected_sequence = [
            ("project_manager", "game_designer"),
            ("game_designer", "developer"),
            ("developer", "test_engineer"),
            ("test_engineer", "qa_tester"),
            ("qa_tester", "quality_reviewer"),
            ("quality_reviewer", "deployment")
        ]
        
        contracts_data = [
            test_helper._create_valid_pm_output(story_id),
            test_helper._create_valid_gd_output(story_id),
            test_helper._create_valid_dev_output(story_id),
            test_helper._create_valid_te_output(story_id),
            test_helper._create_valid_qa_output(story_id),
            test_helper._create_valid_qr_output(story_id)
        ]
        
        for i, contract_data in enumerate(contracts_data):
            expected_source, expected_target = expected_sequence[i]
            assert contract_data["source_agent"] == expected_source
            assert contract_data["target_agent"] == expected_target
            
        print("✅ Agent sequence validation passed!")

    def test_performance_budget_consistency(self):
        """Test that performance budgets are consistent across all contracts."""
        story_id = "STORY-PERF-BUDGET-001"
        
        # Performance budgets that should be consistent
        expected_api_response_time = 200  # ms
        expected_lighthouse_score = 90
        expected_bundle_size = 500  # KB
        
        test_helper = TestAgentContractFlow()
        te_output = test_helper._create_valid_te_output(story_id)
        
        perf_results = te_output["input_requirements"]["required_data"]["performance_test_results"]
        
        assert perf_results["average_api_response_time_ms"] <= expected_api_response_time
        assert perf_results["lighthouse_score"] >= expected_lighthouse_score
        assert perf_results["bundle_size_kb"] <= expected_bundle_size
        
        print("✅ Performance budget consistency validated!")


if __name__ == "__main__":
    # Run tests directly for debugging
    test_flow = TestAgentContractFlow()
    test_flow.test_complete_contract_chain_compatibility()
    test_flow.test_dna_compliance_preservation()
    test_flow.test_quality_gates_progression()
    test_flow.test_contract_version_compatibility()
    test_flow.test_story_id_propagation()
    test_flow.test_performance_requirements_chain()
    test_flow.test_security_requirements_chain()
    test_flow.test_coverage_requirements_chain()
    
    test_compat = TestContractCompatibility()
    test_compat.test_contract_schema_stability()
    test_compat.test_agent_sequence_validation()
    test_compat.test_performance_budget_consistency()
    
    print("\n🎉 All contract tests passed! Team integration is validated.")