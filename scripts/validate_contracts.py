#!/usr/bin/env python3
"""
Contract Validation Script

PURPOSE:
Automated script that validates all agent contracts and ensures team integration
remains intact. Run this before any agent modifications or commits.

USAGE:
python scripts/validate_contracts.py [--verbose] [--fast] [--agent AGENT_NAME]

CRITICAL VALIDATION:
- Complete agent chain compatibility
- DNA compliance preservation
- Performance requirements validation
- Security requirements validation
- Quality gates validation

EXIT CODES:
0 - All validations passed
1 - Contract validation failed
2 - Performance requirements not met
3 - Security requirements not met
4 - Quality gates failed
"""

import sys
import os
import argparse
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from tests.integration.test_agent_contracts import TestAgentContractFlow, TestContractCompatibility
    from tests.integration.test_contract_pipeline import TestContractPipeline, TestContractRegression
except ImportError as e:
    print(f"❌ Failed to import test modules: {e}")
    print("Ensure you're running from the project root directory")
    sys.exit(1)


class ContractValidator:
    """Main contract validation orchestrator."""
    
    def __init__(self, verbose: bool = False, fast: bool = False):
        self.verbose = verbose
        self.fast = fast
        self.test_flow = TestAgentContractFlow()
        self.test_compatibility = TestContractCompatibility()
        self.test_pipeline = TestContractPipeline()
        self.test_regression = TestContractRegression()
        
        self.results = {
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "errors": []
        }
    
    def log(self, message: str, level: str = "INFO"):
        """Log message if verbose mode is enabled."""
        if self.verbose or level in ["ERROR", "CRITICAL"]:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
    
    def run_test(self, test_name: str, test_func, description: str = ""):
        """Run a single test and track results."""
        self.log(f"Running {test_name}... {description}")
        
        try:
            start_time = time.time()
            test_func()
            end_time = time.time()
            
            self.results["passed"] += 1
            self.log(f"✅ {test_name} passed ({end_time - start_time:.3f}s)")
            return True
            
        except Exception as e:
            self.results["failed"] += 1
            error_msg = f"❌ {test_name} failed: {str(e)}"
            self.results["errors"].append(error_msg)
            self.log(error_msg, "ERROR")
            return False
    
    def validate_core_contracts(self) -> bool:
        """Validate core contract functionality."""
        self.log("=" * 60)
        self.log("VALIDATING CORE CONTRACTS")
        self.log("=" * 60)
        
        tests = [
            ("complete_contract_chain", self.test_flow.test_complete_contract_chain_compatibility, 
             "Full PM → Game Designer → Developer → Test Engineer → QA Tester → Quality Reviewer chain"),
            ("dna_compliance_preservation", self.test_flow.test_dna_compliance_preservation,
             "DNA compliance preserved throughout chain"),
            ("quality_gates_progression", self.test_flow.test_quality_gates_progression,
             "Quality gates properly validated at each stage"),
            ("contract_version_compatibility", self.test_flow.test_contract_version_compatibility,
             "All contracts use compatible versions"),
            ("story_id_propagation", self.test_flow.test_story_id_propagation,
             "Story ID correctly propagated through all contracts")
        ]
        
        all_passed = True
        for test_name, test_func, description in tests:
            if not self.run_test(test_name, test_func, description):
                all_passed = False
                
        return all_passed
    
    def validate_requirements_chains(self) -> bool:
        """Validate requirements are maintained through contract chains."""
        self.log("=" * 60)
        self.log("VALIDATING REQUIREMENTS CHAINS")
        self.log("=" * 60)
        
        tests = [
            ("performance_requirements", self.test_flow.test_performance_requirements_chain,
             "Performance requirements (API <200ms, Lighthouse ≥90) maintained"),
            ("security_requirements", self.test_flow.test_security_requirements_chain,
             "Security requirements (no critical/high vulns) maintained"),
            ("coverage_requirements", self.test_flow.test_coverage_requirements_chain,
             "Coverage requirements (95% integration, 90% E2E) maintained")
        ]
        
        all_passed = True
        for test_name, test_func, description in tests:
            if not self.run_test(test_name, test_func, description):
                all_passed = False
                
        return all_passed
    
    def validate_compatibility(self) -> bool:
        """Validate contract compatibility and regression."""
        self.log("=" * 60)
        self.log("VALIDATING COMPATIBILITY")
        self.log("=" * 60)
        
        tests = [
            ("schema_stability", self.test_compatibility.test_contract_schema_stability,
             "Contract schemas remain stable"),
            ("agent_sequence", self.test_compatibility.test_agent_sequence_validation,
             "Agent sequence correctly maintained"),
            ("performance_budget_consistency", self.test_compatibility.test_performance_budget_consistency,
             "Performance budgets consistent across contracts")
        ]
        
        all_passed = True
        for test_name, test_func, description in tests:
            if not self.run_test(test_name, test_func, description):
                all_passed = False
                
        return all_passed
    
    def validate_pipeline(self) -> bool:
        """Validate pipeline performance and regression."""
        if self.fast:
            self.log("Skipping pipeline tests (fast mode)")
            self.results["skipped"] += 4
            return True
            
        self.log("=" * 60)
        self.log("VALIDATING PIPELINE")
        self.log("=" * 60)
        
        tests = [
            ("processing_performance", self.test_pipeline.test_contract_processing_performance,
             "Contract processing remains performant"),
            ("memory_usage", self.test_pipeline.test_contract_memory_usage,
             "No memory leaks in contract processing"),
            ("error_handling", self.test_pipeline.test_contract_validation_error_handling,
             "Contract validation error handling works"),
            ("dna_consistency", self.test_pipeline.test_dna_compliance_consistency,
             "DNA compliance consistently formatted")
        ]
        
        all_passed = True
        for test_name, test_func, description in tests:
            if not self.run_test(test_name, test_func, description):
                all_passed = False
                
        return all_passed
    
    def validate_regression(self) -> bool:
        """Validate regression safety."""
        self.log("=" * 60)
        self.log("VALIDATING REGRESSION SAFETY")
        self.log("=" * 60)
        
        tests = [
            ("field_addition_safety", self.test_regression.test_contract_field_addition_safety,
             "Adding fields doesn't break contracts"),
            ("field_removal_detection", self.test_regression.test_contract_field_removal_detection,
             "Removing required fields is detected"),
            ("type_consistency", self.test_regression.test_contract_type_consistency,
             "Contract types remain consistent")
        ]
        
        all_passed = True
        for test_name, test_func, description in tests:
            if not self.run_test(test_name, test_func, description):
                all_passed = False
                
        return all_passed
    
    def validate_specific_agent(self, agent_name: str) -> bool:
        """Validate contracts for a specific agent."""
        self.log(f"=" * 60)
        self.log(f"VALIDATING {agent_name.upper()} AGENT CONTRACTS")
        self.log(f"=" * 60)
        
        # Map agent names to their contract validation methods
        agent_validators = {
            "project_manager": self._validate_pm_contracts,
            "game_designer": self._validate_gd_contracts,
            "developer": self._validate_dev_contracts,
            "test_engineer": self._validate_te_contracts,
            "qa_tester": self._validate_qa_contracts,
            "quality_reviewer": self._validate_qr_contracts
        }
        
        if agent_name not in agent_validators:
            self.log(f"Unknown agent: {agent_name}", "ERROR")
            return False
            
        return agent_validators[agent_name]()
    
    def _validate_pm_contracts(self) -> bool:
        """Validate Project Manager contracts."""
        story_id = "STORY-PM-VALIDATION-001"
        
        try:
            pm_output = self.test_flow._create_valid_pm_output(story_id)
            assert pm_output["source_agent"] == "project_manager"
            assert pm_output["target_agent"] == "game_designer"
            assert pm_output["contract_type"] == "analysis_to_design"
            self.log("✅ Project Manager contracts validated")
            return True
        except Exception as e:
            self.log(f"❌ Project Manager contract validation failed: {e}", "ERROR")
            return False
    
    def _validate_gd_contracts(self) -> bool:
        """Validate Game Designer contracts."""
        story_id = "STORY-GD-VALIDATION-001"
        
        try:
            gd_output = self.test_flow._create_valid_gd_output(story_id)
            assert gd_output["source_agent"] == "game_designer"
            assert gd_output["target_agent"] == "developer"
            assert gd_output["contract_type"] == "design_to_implementation"
            self.log("✅ Game Designer contracts validated")
            return True
        except Exception as e:
            self.log(f"❌ Game Designer contract validation failed: {e}", "ERROR")
            return False
    
    def _validate_dev_contracts(self) -> bool:
        """Validate Developer contracts."""
        story_id = "STORY-DEV-VALIDATION-001"
        
        try:
            dev_output = self.test_flow._create_valid_dev_output(story_id)
            assert dev_output["source_agent"] == "developer"
            assert dev_output["target_agent"] == "test_engineer"
            assert dev_output["contract_type"] == "implementation_to_testing"
            self.log("✅ Developer contracts validated")
            return True
        except Exception as e:
            self.log(f"❌ Developer contract validation failed: {e}", "ERROR")
            return False
    
    def _validate_te_contracts(self) -> bool:
        """Validate Test Engineer contracts."""
        story_id = "STORY-TE-VALIDATION-001"
        
        try:
            te_output = self.test_flow._create_valid_te_output(story_id)
            assert te_output["source_agent"] == "test_engineer"
            assert te_output["target_agent"] == "qa_tester"
            assert te_output["contract_type"] == "testing_to_qa"
            self.log("✅ Test Engineer contracts validated")
            return True
        except Exception as e:
            self.log(f"❌ Test Engineer contract validation failed: {e}", "ERROR")
            return False
    
    def _validate_qa_contracts(self) -> bool:
        """Validate QA Tester contracts."""
        story_id = "STORY-QA-VALIDATION-001"
        
        try:
            qa_output = self.test_flow._create_valid_qa_output(story_id)
            assert qa_output["source_agent"] == "qa_tester"
            assert qa_output["target_agent"] == "quality_reviewer"
            assert qa_output["contract_type"] == "qa_to_quality_review"
            self.log("✅ QA Tester contracts validated")
            return True
        except Exception as e:
            self.log(f"❌ QA Tester contract validation failed: {e}", "ERROR")
            return False
    
    def _validate_qr_contracts(self) -> bool:
        """Validate Quality Reviewer contracts."""
        story_id = "STORY-QR-VALIDATION-001"
        
        try:
            qr_output = self.test_flow._create_valid_qr_output(story_id)
            assert qr_output["source_agent"] == "quality_reviewer"
            assert qr_output["target_agent"] == "deployment"
            assert qr_output["contract_type"] == "quality_review_to_deployment"
            self.log("✅ Quality Reviewer contracts validated")
            return True
        except Exception as e:
            self.log(f"❌ Quality Reviewer contract validation failed: {e}", "ERROR")
            return False
    
    def print_summary(self):
        """Print validation summary."""
        total_tests = self.results["passed"] + self.results["failed"] + self.results["skipped"]
        
        print("\n" + "=" * 60)
        print("CONTRACT VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total tests: {total_tests}")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"⏭️  Skipped: {self.results['skipped']}")
        
        if self.results["errors"]:
            print("\nERRORS:")
            for error in self.results["errors"]:
                print(f"  {error}")
        
        if self.results["failed"] == 0:
            print("\n🎉 ALL CONTRACT VALIDATIONS PASSED!")
            print("✅ Team integration is safe - proceed with confidence!")
        else:
            print(f"\n❌ {self.results['failed']} VALIDATION(S) FAILED!")
            print("🚨 Do not proceed with agent modifications until contracts are fixed!")
    
    def get_exit_code(self) -> int:
        """Get appropriate exit code based on results."""
        if self.results["failed"] == 0:
            return 0  # Success
        else:
            # Determine specific failure type for more specific exit codes
            for error in self.results["errors"]:
                if "performance" in error.lower():
                    return 2  # Performance failure
                elif "security" in error.lower():
                    return 3  # Security failure
                elif "quality" in error.lower():
                    return 4  # Quality gate failure
            return 1  # General contract failure


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate DigiNativa agent contracts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate_contracts.py                    # Full validation
  python scripts/validate_contracts.py --verbose          # Verbose output
  python scripts/validate_contracts.py --fast             # Skip performance tests
  python scripts/validate_contracts.py --agent developer  # Validate specific agent
        """
    )
    
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--fast", "-f", action="store_true",
                       help="Skip performance and memory tests")
    parser.add_argument("--agent", "-a", type=str,
                       help="Validate specific agent only",
                       choices=["project_manager", "game_designer", "developer", 
                               "test_engineer", "qa_tester", "quality_reviewer"])
    
    args = parser.parse_args()
    
    print("🔄 DigiNativa Contract Validation")
    print("🎯 Ensuring AI team integration remains intact")
    print()
    
    validator = ContractValidator(verbose=args.verbose, fast=args.fast)
    
    start_time = time.time()
    
    if args.agent:
        # Validate specific agent
        success = validator.validate_specific_agent(args.agent)
    else:
        # Full validation suite
        core_passed = validator.validate_core_contracts()
        requirements_passed = validator.validate_requirements_chains()
        compatibility_passed = validator.validate_compatibility()
        pipeline_passed = validator.validate_pipeline()
        regression_passed = validator.validate_regression()
        
        success = all([core_passed, requirements_passed, compatibility_passed, 
                      pipeline_passed, regression_passed])
    
    end_time = time.time()
    
    validator.print_summary()
    print(f"\nValidation completed in {end_time - start_time:.2f} seconds")
    
    exit_code = validator.get_exit_code()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()