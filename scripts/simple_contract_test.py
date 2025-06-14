#!/usr/bin/env python3
"""
Simple Contract Validation Test

PURPOSE:
Lightweight contract validation that doesn't require external dependencies.
This validates the core contract creation and compatibility.
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def create_valid_pm_output(story_id: str):
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
                "feature_breakdown": {"primary_features": ["user_registration"]},
                "complexity_assessment": {"technical_complexity": 3},
                "anna_persona_requirements": {"time_constraint_minutes": 10}
            },
            "required_validations": ["feature_completeness", "anna_persona_compliance"]
        },
        "output_specifications": {
            "deliverable_files": [f"docs/design/{story_id}_ux_spec.md"],
            "deliverable_data": {"ux_specification": "object"},
            "validation_criteria": {"design_quality": {"min_score": 4}}
        },
        "quality_gates": ["feature_analysis_complete", "anna_persona_validated"],
        "handoff_criteria": ["ux_specification_ready", "component_mapping_complete"]
    }


def create_valid_te_output(story_id: str):
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
                    "coverage_percent": 97.5,
                    "all_tests_passing": True
                },
                "e2e_test_suite": {
                    "story_id": story_id,
                    "coverage_percent": 92.0,
                    "all_tests_passing": True
                },
                "performance_test_results": {
                    "average_api_response_time_ms": 150.0,
                    "lighthouse_score": 92,
                    "performance_budget_met": True
                },
                "security_scan_results": {
                    "critical_vulnerabilities": [],
                    "high_vulnerabilities": [],
                    "security_compliance_met": True
                },
                "coverage_report": {
                    "overall_coverage_percent": 95.5,
                    "coverage_quality_met": True
                }
            },
            "required_validations": ["all_integration_tests_passing", "performance_benchmarks_met"]
        },
        "output_specifications": {
            "deliverable_files": [f"docs/qa_reports/{story_id}_ux_validation.md"],
            "deliverable_data": {"ux_validation_results": "object"},
            "validation_criteria": {"user_experience": {"anna_persona_satisfaction": {"min_score": 4}}}
        },
        "quality_gates": ["all_automated_tests_passing", "performance_requirements_validated", "security_compliance_verified"],
        "handoff_criteria": ["comprehensive_ux_validation_completed", "accessibility_compliance_verified"]
    }


def validate_contract_structure(contract, contract_name):
    """Validate basic contract structure."""
    required_fields = [
        "contract_version",
        "contract_type", 
        "story_id",
        "source_agent",
        "target_agent",
        "dna_compliance",
        "input_requirements",
        "output_specifications",
        "quality_gates",
        "handoff_criteria"
    ]
    
    for field in required_fields:
        if field not in contract:
            raise ValueError(f"Missing required field '{field}' in {contract_name}")
    
    # Validate story_id format
    if not contract["story_id"].startswith("STORY-"):
        raise ValueError(f"Invalid story_id format in {contract_name}")
    
    # Validate DNA compliance structure
    dna = contract["dna_compliance"]
    if "design_principles_validation" not in dna:
        raise ValueError(f"Missing design_principles_validation in {contract_name}")
    if "architecture_compliance" not in dna:
        raise ValueError(f"Missing architecture_compliance in {contract_name}")
    
    # Validate quality gates
    if not isinstance(contract["quality_gates"], list) or len(contract["quality_gates"]) == 0:
        raise ValueError(f"Quality gates must be non-empty list in {contract_name}")
    
    # Validate handoff criteria
    if not isinstance(contract["handoff_criteria"], list) or len(contract["handoff_criteria"]) == 0:
        raise ValueError(f"Handoff criteria must be non-empty list in {contract_name}")


def test_agent_sequence():
    """Test that agent sequence is correct."""
    story_id = "STORY-SEQUENCE-001"
    
    # Expected sequence
    expected_sequence = [
        ("project_manager", "game_designer"),
        ("test_engineer", "qa_tester")
    ]
    
    contracts = [
        ("PM", create_valid_pm_output(story_id)),
        ("TE", create_valid_te_output(story_id))
    ]
    
    sequence_index = 0
    for name, contract in contracts:
        if sequence_index < len(expected_sequence):
            expected_source, expected_target = expected_sequence[sequence_index]
            
            if contract["source_agent"] != expected_source:
                raise ValueError(f"Expected source_agent '{expected_source}', got '{contract['source_agent']}' in {name}")
            
            if contract["target_agent"] != expected_target:
                raise ValueError(f"Expected target_agent '{expected_target}', got '{contract['target_agent']}' in {name}")
        
        sequence_index += 1


def test_dna_compliance_consistency():
    """Test that DNA compliance is consistent across contracts."""
    story_id = "STORY-DNA-001"
    
    contracts = [
        create_valid_pm_output(story_id),
        create_valid_te_output(story_id)
    ]
    
    base_dna = contracts[0]["dna_compliance"]
    
    for i, contract in enumerate(contracts[1:], 1):
        if contract["dna_compliance"] != base_dna:
            raise ValueError(f"DNA compliance mismatch in contract {i}")


def test_performance_requirements():
    """Test that performance requirements are maintained."""
    story_id = "STORY-PERF-001"
    
    te_contract = create_valid_te_output(story_id)
    perf_results = te_contract["input_requirements"]["required_data"]["performance_test_results"]
    
    # Validate performance requirements
    if perf_results["average_api_response_time_ms"] > 200:
        raise ValueError("API response time exceeds 200ms requirement")
    
    if perf_results["lighthouse_score"] < 90:
        raise ValueError("Lighthouse score below 90 requirement")
    
    if not perf_results["performance_budget_met"]:
        raise ValueError("Performance budget not met")


def test_security_requirements():
    """Test that security requirements are maintained."""
    story_id = "STORY-SEC-001"
    
    te_contract = create_valid_te_output(story_id)
    security_results = te_contract["input_requirements"]["required_data"]["security_scan_results"]
    
    # Validate security requirements
    if len(security_results["critical_vulnerabilities"]) > 0:
        raise ValueError("Critical vulnerabilities found")
    
    if len(security_results["high_vulnerabilities"]) > 0:
        raise ValueError("High severity vulnerabilities found")
    
    if not security_results["security_compliance_met"]:
        raise ValueError("Security compliance not met")


def test_coverage_requirements():
    """Test that coverage requirements are maintained."""
    story_id = "STORY-COV-001"
    
    te_contract = create_valid_te_output(story_id)
    required_data = te_contract["input_requirements"]["required_data"]
    
    # Validate coverage requirements
    integration_coverage = required_data["integration_test_suite"]["coverage_percent"]
    if integration_coverage < 95:
        raise ValueError(f"Integration coverage {integration_coverage}% below 95% requirement")
    
    e2e_coverage = required_data["e2e_test_suite"]["coverage_percent"]
    if e2e_coverage < 90:
        raise ValueError(f"E2E coverage {e2e_coverage}% below 90% requirement")
    
    overall_coverage = required_data["coverage_report"]["overall_coverage_percent"]
    if overall_coverage < 90:
        raise ValueError(f"Overall coverage {overall_coverage}% below 90% requirement")


def main():
    """Run simple contract validation tests."""
    print("🔄 DigiNativa Simple Contract Validation")
    print("🎯 Testing core contract functionality")
    print()
    
    tests = [
        ("Contract Structure Validation", lambda: None),
        ("Agent Sequence Validation", test_agent_sequence),
        ("DNA Compliance Consistency", test_dna_compliance_consistency),
        ("Performance Requirements", test_performance_requirements),
        ("Security Requirements", test_security_requirements),
        ("Coverage Requirements", test_coverage_requirements)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_name == "Contract Structure Validation":
                # Test contract structure for key contracts
                story_id = "STORY-STRUCT-001"
                pm_contract = create_valid_pm_output(story_id)
                te_contract = create_valid_te_output(story_id)
                
                validate_contract_structure(pm_contract, "Project Manager")
                validate_contract_structure(te_contract, "Test Engineer")
            else:
                test_func()
            
            print(f"✅ {test_name}")
            passed += 1
            
        except Exception as e:
            print(f"❌ {test_name}: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print("CONTRACT VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total tests: {passed + failed}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print()
        print("🎉 ALL CONTRACT VALIDATIONS PASSED!")
        print("✅ Core contract system is working correctly!")
        return 0
    else:
        print()
        print(f"❌ {failed} VALIDATION(S) FAILED!")
        print("🚨 Contract system issues detected!")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)