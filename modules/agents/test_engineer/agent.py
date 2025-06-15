"""
TestEngineerAgent - Automated testing and performance validation agent.

PURPOSE:
Generates comprehensive test suites and validates performance requirements
for all implemented features from the Developer agent. Ensures code quality
meets DigiNativa's exacting standards.

CRITICAL RESPONSIBILITIES:
- Generate integration tests for React + FastAPI implementations
- Create end-to-end tests with user persona simulation
- Validate performance requirements (API <200ms, Lighthouse >90)
- Execute security vulnerability scanning
- Provide comprehensive coverage analysis and reporting
- Maintain 100% test coverage for business logic

CONTRACT PROTECTION:
This agent receives contracts from Developer and outputs to QA Tester.
NEVER break the contract interface - it enables our modular architecture.
"""

import json
import asyncio
import logging
import time
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Import our foundation
from ...shared.base_agent import BaseAgent, AgentExecutionResult
from ...shared.exceptions import AgentExecutionError, DNAComplianceError, QualityGateError
from ...shared.event_bus import EventBus

# Import specialized tools
from .tools.test_generator import TestGenerator
from .tools.coverage_analyzer import CoverageAnalyzer
from .tools.performance_tester import PerformanceTester
from .tools.security_scanner import SecurityScanner
from .tools.dna_test_validator import DNATestValidator
from .tools.ai_test_optimizer import AITestOptimizer

# Setup logging
logger = logging.getLogger(__name__)


class TestEngineerAgent(BaseAgent):
    """
    Test Engineer agent for automated testing and performance validation.
    
    WORKFLOW:
    1. Receive implementation details from Developer agent
    2. Generate comprehensive integration tests for React + FastAPI
    3. Create end-to-end tests with persona simulation
    4. Execute performance testing (API <200ms, Lighthouse >90)
    5. Run security vulnerability scanning
    6. Analyze test coverage and generate reports
    7. Output contract for QA Tester with test results
    
    QUALITY GATES:
    - All test suites passing: 100%
    - Code coverage minimum: 95% integration, 90% e2e
    - Performance benchmarks: API <200ms, Lighthouse >90
    - Security scan: No high/critical vulnerabilities
    - Automated test pipeline configured
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Test Engineer agent.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__("te-001", "test_engineer", config)
        
        # Initialize EventBus for team coordination
        self.event_bus = EventBus(config)
        
        # Initialize specialized tools
        self.test_generator = TestGenerator(config)
        self.coverage_analyzer = CoverageAnalyzer(config)
        self.performance_tester = PerformanceTester(config)
        self.security_scanner = SecurityScanner(config)
        self.dna_test_validator = DNATestValidator(config)
        self.ai_test_optimizer = AITestOptimizer(config)
        
        # Test Engineer specific configuration
        self.test_output_path = self.config.get("test_output_path", "tests")
        self.coverage_threshold = self.config.get("coverage_threshold", 95)
        self.performance_budget = self.config.get("performance_budget", {
            "api_response_time_ms": 200,
            "lighthouse_score": 90,
            "bundle_size_kb": 500
        })
        
        # Quality standards for DigiNativa
        self.quality_standards = {
            "integration_test_coverage": {"min": 95},
            "e2e_test_coverage": {"min": 90},
            "performance_test_required": True,
            "security_scan_required": True,
            "automation_required": True,
            "ci_cd_integration": True
        }
        
        self.logger.info("TestEngineerAgent initialized successfully")
    
    async def _notify_team_progress(self, event_type: str, data: Dict[str, Any]):
        """Notify team of progress via EventBus."""
        await self.event_bus.publish(event_type, {
            "agent": self.agent_type,
            "story_id": data.get("story_id"),
            "status": data.get("status"),
            "timestamp": datetime.now().isoformat(),
            **data
        })

    async def _listen_for_team_events(self):
        """Listen for relevant team events."""
        relevant_events = ["test_engineer_*", "team_*", "pipeline_*", "testing_*"]
        for event_pattern in relevant_events:
            await self.event_bus.subscribe(event_pattern, self._handle_team_event)

    async def _handle_team_event(self, event_type: str, data: Dict[str, Any]):
        """Handle incoming team coordination events."""
        self.logger.info(f"Test Engineer received team event: {event_type}")
        # Test Engineer specific event handling logic
        if event_type.startswith("implementation_"):
            self.logger.info(f"Developer implementation event: {event_type}")
        elif event_type.startswith("testing_"):
            self.logger.info(f"Testing coordination event: {event_type}")
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Developer contract and generate comprehensive test suite.
        
        TESTING WORKFLOW:
        1. Extract implementation details from Developer agent
        2. Validate implementation meets testability requirements
        3. Generate integration tests for React + FastAPI components
        4. Create end-to-end tests with persona simulation
        5. Execute performance testing and benchmarking
        6. Run security vulnerability scanning
        7. Analyze test coverage and generate reports
        8. Generate output contract for QA Tester
        
        Args:
            input_contract: Contract from Developer with implementation details
            
        Returns:
            Output contract for QA Tester with test results and validations
            
        Raises:
            AgentExecutionError: If test generation fails
            QualityGateError: If quality standards are not met
        """
        try:
            story_id = input_contract.get("story_id")
            self.logger.info(f"Starting comprehensive testing for story: {story_id}")
            
            # Notify team of testing start
            await self._notify_team_progress("testing_started", {"story_id": story_id})
            
            # Step 1: Extract and validate implementation data
            input_data = input_contract.get("input_requirements", {}).get("required_data", {})
            
            component_implementations = input_data.get("component_implementations", [])
            api_implementations = input_data.get("api_implementations", [])
            existing_test_suite = input_data.get("test_suite", {})
            implementation_docs = input_data.get("implementation_docs", {})
            git_commit_hash = input_data.get("git_commit_hash", "")
            
            self.logger.debug(f"Processing {len(component_implementations)} components and {len(api_implementations)} APIs")
            
            # Step 2: Validate implementation testability
            await self._validate_implementation_testability(
                component_implementations, api_implementations
            )
            
            # Step 2.5: AI-driven test optimization and strategy
            self.logger.info("Performing AI test optimization analysis")
            ai_optimization_result = await self.ai_test_optimizer.optimize_test_strategy(
                component_implementations,
                api_implementations,
                input_data,
                existing_test_suite
            )
            await self._notify_team_progress("ai_optimization_complete", {
                "story_id": story_id,
                "optimization_score": ai_optimization_result.overall_optimization_score,
                "time_savings": ai_optimization_result.estimated_time_savings_minutes
            })
            
            # Step 3: Generate integration tests
            self.logger.info("Generating integration tests")
            integration_test_suite = await self.test_generator.generate_integration_tests(
                component_implementations,
                api_implementations,
                story_id
            )
            await self._notify_team_progress("integration_tests_generated", {"story_id": story_id})
            
            # Step 4: Generate end-to-end tests
            self.logger.info("Generating end-to-end tests")
            e2e_test_suite = await self.test_generator.generate_e2e_tests(
                component_implementations,
                api_implementations,
                implementation_docs.get("user_flows", []),
                story_id
            )
            await self._notify_team_progress("e2e_tests_generated", {"story_id": story_id})
            
            # Step 5: Execute performance testing
            self.logger.info("Running performance tests")
            performance_results = await self.performance_tester.run_comprehensive_performance_tests(
                api_implementations,
                component_implementations,
                story_id
            )
            await self._notify_team_progress("performance_tests_complete", {"story_id": story_id})
            
            # Step 6: Execute security scanning
            self.logger.info("Running security vulnerability scan")
            security_scan_results = await self.security_scanner.run_comprehensive_security_scan(
                api_implementations,
                component_implementations,
                story_id
            )
            await self._notify_team_progress("security_scan_complete", {"story_id": story_id})
            
            # Step 7: Analyze test coverage
            self.logger.info("Analyzing test coverage")
            coverage_report = await self.coverage_analyzer.analyze_comprehensive_coverage(
                existing_test_suite,
                integration_test_suite,
                e2e_test_suite,
                component_implementations,
                api_implementations,
                story_id
            )
            await self._notify_team_progress("coverage_analysis_complete", {"story_id": story_id})
            
            # Step 8: Validate all quality gates
            await self._validate_test_quality_gates(
                integration_test_suite,
                e2e_test_suite,
                performance_results,
                security_scan_results,
                coverage_report
            )
            
            # Step 9: Validate DNA compliance (ACTIVE DNA VALIDATION)
            self.logger.info("Performing active DNA validation")
            dna_validation_result = await self.dna_test_validator.validate_test_dna_compliance(
                integration_test_suite,
                e2e_test_suite,
                performance_results,
                coverage_report,
                input_data
            )
            await self._notify_team_progress("dna_validation_complete", {
                "story_id": story_id,
                "dna_compliant": dna_validation_result.overall_dna_compliant,
                "dna_score": dna_validation_result.dna_compliance_score
            })
            
            # Step 10: Generate test automation configuration
            automation_config = await self._generate_automation_configuration(
                integration_test_suite,
                e2e_test_suite,
                performance_results,
                story_id
            )
            
            # Step 11: Create output contract for QA Tester
            output_contract = await self._create_output_contract(
                input_contract,
                story_id,
                integration_test_suite,
                e2e_test_suite,
                performance_results,
                security_scan_results,
                coverage_report,
                automation_config,
                dna_validation_result,
                ai_optimization_result
            )
            
            # Notify team of testing completion
            await self._notify_team_progress("testing_complete", {"story_id": story_id})
            
            self.logger.info(f"Testing completed successfully for story: {story_id}")
            return output_contract
            
        except Exception as e:
            error_msg = f"Test Engineer processing failed for {story_id}: {str(e)}"
            self.logger.error(error_msg)
            raise AgentExecutionError(error_msg)
    
    async def _validate_implementation_testability(
        self,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]]
    ) -> None:
        """
        Validate that implementations are testable and meet quality requirements.
        
        Args:
            component_implementations: React components from Developer
            api_implementations: FastAPI endpoints from Developer
            
        Raises:
            QualityGateError: If implementations don't meet testability requirements
        """
        validation_errors = []
        
        # Validate React components testability
        for component in component_implementations:
            if component.get("typescript_errors", 0) > 0:
                validation_errors.append(f"Component {component['name']} has TypeScript errors")
            
            if component.get("eslint_violations", 0) > 0:
                validation_errors.append(f"Component {component['name']} has ESLint violations")
            
            if not component.get("integration_test_passed", False):
                validation_errors.append(f"Component {component['name']} failed integration tests")
        
        # Validate FastAPI endpoints testability
        for api in api_implementations:
            if not api.get("functional_test_passed", False):
                validation_errors.append(f"API {api['name']} failed functional tests")
            
            if not api.get("performance_test_passed", False):
                validation_errors.append(f"API {api['name']} failed performance tests")
            
            if api.get("estimated_response_time_ms", 999) > 200:
                validation_errors.append(f"API {api['name']} exceeds 200ms response time budget")
        
        if validation_errors:
            error_msg = f"Implementation testability validation failed: {'; '.join(validation_errors)}"
            self.logger.error(error_msg)
            raise QualityGateError(error_msg)
        
        self.logger.info("Implementation testability validation passed")
    
    async def _validate_test_quality_gates(
        self,
        integration_test_suite: Dict[str, Any],
        e2e_test_suite: Dict[str, Any],
        performance_results: Dict[str, Any],
        security_scan_results: Dict[str, Any],
        coverage_report: Dict[str, Any]
    ) -> None:
        """
        Validate all test quality gates meet DigiNativa standards.
        
        Args:
            integration_test_suite: Integration test results
            e2e_test_suite: End-to-end test results
            performance_results: Performance test results
            security_scan_results: Security scan results
            coverage_report: Coverage analysis results
            
        Raises:
            QualityGateError: If any quality gate fails
        """
        quality_gate_errors = []
        
        # Validate integration test coverage
        integration_coverage = integration_test_suite.get("coverage_percent", 0)
        if integration_coverage < self.quality_standards["integration_test_coverage"]["min"]:
            quality_gate_errors.append(
                f"Integration test coverage {integration_coverage}% below minimum "
                f"{self.quality_standards['integration_test_coverage']['min']}%"
            )
        
        # Validate e2e test coverage
        e2e_coverage = e2e_test_suite.get("coverage_percent", 0)
        if e2e_coverage < self.quality_standards["e2e_test_coverage"]["min"]:
            quality_gate_errors.append(
                f"E2E test coverage {e2e_coverage}% below minimum "
                f"{self.quality_standards['e2e_test_coverage']['min']}%"
            )
        
        # Validate performance benchmarks
        api_response_time = performance_results.get("average_api_response_time_ms", 999)
        if api_response_time > self.performance_budget["api_response_time_ms"]:
            quality_gate_errors.append(
                f"API response time {api_response_time}ms exceeds budget "
                f"{self.performance_budget['api_response_time_ms']}ms"
            )
        
        lighthouse_score = performance_results.get("lighthouse_score", 0)
        if lighthouse_score < self.performance_budget["lighthouse_score"]:
            quality_gate_errors.append(
                f"Lighthouse score {lighthouse_score} below minimum "
                f"{self.performance_budget['lighthouse_score']}"
            )
        
        # Validate security scan results
        critical_vulnerabilities = security_scan_results.get("critical_vulnerabilities", [])
        high_vulnerabilities = security_scan_results.get("high_vulnerabilities", [])
        
        if critical_vulnerabilities or high_vulnerabilities:
            quality_gate_errors.append(
                f"Security vulnerabilities found: {len(critical_vulnerabilities)} critical, "
                f"{len(high_vulnerabilities)} high severity"
            )
        
        # Validate overall test coverage
        overall_coverage = coverage_report.get("overall_coverage_percent", 0)
        if overall_coverage < self.coverage_threshold:
            quality_gate_errors.append(
                f"Overall test coverage {overall_coverage}% below threshold {self.coverage_threshold}%"
            )
        
        if quality_gate_errors:
            error_msg = f"Test quality gates failed: {'; '.join(quality_gate_errors)}"
            self.logger.error(error_msg)
            raise QualityGateError(error_msg)
        
        self.logger.info("All test quality gates passed successfully")
    
    async def _generate_automation_configuration(
        self,
        integration_test_suite: Dict[str, Any],
        e2e_test_suite: Dict[str, Any],
        performance_results: Dict[str, Any],
        story_id: str
    ) -> Dict[str, Any]:
        """
        Generate CI/CD automation configuration for test pipeline.
        
        Args:
            integration_test_suite: Integration test configuration
            e2e_test_suite: E2E test configuration
            performance_results: Performance test configuration
            story_id: Story identifier
            
        Returns:
            Automation configuration for CI/CD pipeline
        """
        return {
            "story_id": story_id,
            "ci_cd_pipeline": {
                "stages": [
                    "unit_tests",
                    "integration_tests",
                    "e2e_tests",
                    "performance_tests",
                    "security_scan"
                ],
                "test_commands": {
                    "unit": "npm test",
                    "integration": f"npm run test:integration -- tests/integration/{story_id}/",
                    "e2e": f"npm run test:e2e -- tests/e2e/{story_id}/",
                    "performance": f"npm run test:performance -- {story_id}",
                    "security": f"npm run security:scan -- {story_id}"
                }
            },
            "quality_gates": {
                "coverage_threshold": self.coverage_threshold,
                "performance_budget": self.performance_budget,
                "security_requirements": {
                    "max_critical_vulnerabilities": 0,
                    "max_high_vulnerabilities": 0
                }
            },
            "reporting": {
                "coverage_report": f"docs/test_reports/{story_id}_coverage.html",
                "performance_report": f"docs/performance/{story_id}_benchmarks.json",
                "security_report": f"docs/security/{story_id}_vulnerabilities.json"
            }
        }
    
    async def _create_output_contract(
        self,
        input_contract: Dict[str, Any],
        story_id: str,
        integration_test_suite: Dict[str, Any],
        e2e_test_suite: Dict[str, Any],
        performance_results: Dict[str, Any],
        security_scan_results: Dict[str, Any],
        coverage_report: Dict[str, Any],
        automation_config: Dict[str, Any],
        dna_validation_result: Any = None,
        ai_optimization_result: Any = None
    ) -> Dict[str, Any]:
        """
        Create output contract for QA Tester.
        
        Args:
            input_contract: Original input contract
            story_id: Story identifier
            integration_test_suite: Integration test results
            e2e_test_suite: E2E test results
            performance_results: Performance test results
            security_scan_results: Security scan results
            coverage_report: Coverage analysis results
            automation_config: CI/CD automation configuration
            
        Returns:
            Output contract for QA Tester
        """
        # Enhanced DNA compliance with active validation results
        enhanced_dna_compliance = input_contract.get("dna_compliance", {})
        if dna_validation_result:
            enhanced_dna_compliance.update({
                "test_engineer_dna_validation": {
                    "overall_dna_compliant": dna_validation_result.overall_dna_compliant,
                    "time_respect_compliant": dna_validation_result.time_respect_compliant,
                    "pedagogical_value_compliant": dna_validation_result.pedagogical_value_compliant,
                    "professional_tone_compliant": dna_validation_result.professional_tone_compliant,
                    "dna_compliance_score": dna_validation_result.dna_compliance_score,
                    "validation_timestamp": dna_validation_result.validation_timestamp
                }
            })

        return {
            "contract_version": "1.0",
            "contract_type": "testing_to_qa",
            "story_id": story_id,
            "source_agent": "test_engineer",
            "target_agent": "qa_tester",
            "dna_compliance": enhanced_dna_compliance,
            
            "input_requirements": {
                "required_files": [
                    f"tests/integration/{story_id}/",
                    f"tests/e2e/{story_id}/",
                    f"docs/test_reports/{story_id}_coverage.html",
                    f"docs/performance/{story_id}_benchmarks.json",
                    f"docs/security/{story_id}_vulnerabilities.json"
                ],
                "required_data": {
                    "integration_test_suite": integration_test_suite,
                    "e2e_test_suite": e2e_test_suite,
                    "performance_test_results": performance_results,
                    "security_scan_results": security_scan_results,
                    "coverage_report": coverage_report,
                    "automation_config": automation_config,
                    "dna_validation_results": dna_validation_result.quality_reviewer_metrics if dna_validation_result else {},
                    "ai_optimization_results": {
                        "optimization_score": ai_optimization_result.overall_optimization_score if ai_optimization_result else 0.0,
                        "time_savings_minutes": ai_optimization_result.estimated_time_savings_minutes if ai_optimization_result else 0.0,
                        "quality_improvement_score": ai_optimization_result.quality_improvement_score if ai_optimization_result else 0.0,
                        "failure_predictions": len(ai_optimization_result.failure_predictions) if ai_optimization_result else 0,
                        "test_priorities": len(ai_optimization_result.test_priorities) if ai_optimization_result else 0,
                        "edge_case_predictions": len(ai_optimization_result.edge_case_predictions) if ai_optimization_result else 0,
                        "municipal_insights": ai_optimization_result.municipal_optimization_insights if ai_optimization_result else {}
                    },
                    "original_implementation": {
                        "component_implementations": input_contract.get("input_requirements", {}).get("required_data", {}).get("component_implementations", []),
                        "api_implementations": input_contract.get("input_requirements", {}).get("required_data", {}).get("api_implementations", [])
                    }
                },
                "required_validations": [
                    "all_integration_tests_passing",
                    "all_e2e_tests_passing", 
                    "performance_benchmarks_met",
                    "security_vulnerabilities_resolved",
                    "coverage_thresholds_exceeded"
                ]
            },
            
            "output_specifications": {
                "deliverable_files": [
                    f"docs/qa_reports/{story_id}_ux_validation.md",
                    f"docs/qa_reports/{story_id}_accessibility.json",
                    f"docs/qa_reports/{story_id}_persona_testing.json",
                    f"docs/qa_reports/{story_id}_usability_report.md"
                ],
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
            
            "quality_gates": [
                "all_automated_tests_passing",
                "performance_requirements_validated",
                "security_compliance_verified",
                "accessibility_standards_met",
                "user_experience_validated"
            ],
            
            "handoff_criteria": [
                "comprehensive_ux_validation_completed",
                "accessibility_compliance_verified",
                "persona_testing_successful",
                "usability_requirements_met",
                "quality_metrics_documented"
            ]
        }
    
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """
        Check Test Engineer specific quality gates.
        
        Args:
            gate: Quality gate identifier
            deliverables: Deliverables to validate
            
        Returns:
            True if quality gate passes, False otherwise
        """
        quality_checks = {
            "all_test_suites_passing_100_percent": self._check_all_tests_passing,
            "code_coverage_minimum_threshold_met": self._check_coverage_threshold,
            "performance_benchmarks_within_targets": self._check_performance_targets,
            "security_vulnerability_scan_clean": self._check_security_scan,
            "automated_test_suite_configured": self._check_automation_configured,
            "integration_tests_coverage_adequate": self._check_integration_coverage,
            "e2e_tests_coverage_adequate": self._check_e2e_coverage
        }
        
        checker = quality_checks.get(gate)
        if checker:
            try:
                return checker(deliverables)
            except Exception as e:
                self.logger.error(f"Quality gate check failed for '{gate}': {e}")
                return False
        
        # Default pass for unknown gates (with warning)
        self.logger.warning(f"Unknown quality gate: {gate}")
        return True
    
    def _check_all_tests_passing(self, deliverables: Dict[str, Any]) -> bool:
        """Verify all test suites are passing."""
        integration_suite = deliverables.get("integration_test_suite", {})
        e2e_suite = deliverables.get("e2e_test_suite", {})
        
        # Check integration tests
        integration_passing = integration_suite.get("all_tests_passing", False)
        if not integration_passing:
            self.logger.error("Integration tests not all passing")
            return False
        
        # Check e2e tests
        e2e_passing = e2e_suite.get("all_tests_passing", False)
        if not e2e_passing:
            self.logger.error("E2E tests not all passing")
            return False
        
        return True
    
    def _check_coverage_threshold(self, deliverables: Dict[str, Any]) -> bool:
        """Verify test coverage meets minimum threshold."""
        coverage_report = deliverables.get("coverage_report", {})
        overall_coverage = coverage_report.get("overall_coverage_percent", 0)
        
        if overall_coverage < self.coverage_threshold:
            self.logger.error(f"Coverage {overall_coverage}% below threshold {self.coverage_threshold}%")
            return False
        
        return True
    
    def _check_performance_targets(self, deliverables: Dict[str, Any]) -> bool:
        """Verify performance benchmarks are met."""
        performance_results = deliverables.get("performance_test_results", {})
        
        # Check API response time
        api_response_time = performance_results.get("average_api_response_time_ms", 999)
        if api_response_time > self.performance_budget["api_response_time_ms"]:
            self.logger.error(f"API response time {api_response_time}ms exceeds budget")
            return False
        
        # Check Lighthouse score
        lighthouse_score = performance_results.get("lighthouse_score", 0)
        if lighthouse_score < self.performance_budget["lighthouse_score"]:
            self.logger.error(f"Lighthouse score {lighthouse_score} below minimum")
            return False
        
        return True
    
    def _check_security_scan(self, deliverables: Dict[str, Any]) -> bool:
        """Verify security scan is clean."""
        security_results = deliverables.get("security_scan_results", {})
        
        critical_vulns = security_results.get("critical_vulnerabilities", [])
        high_vulns = security_results.get("high_vulnerabilities", [])
        
        if critical_vulns or high_vulns:
            self.logger.error(f"Security vulnerabilities found: {len(critical_vulns)} critical, {len(high_vulns)} high")
            return False
        
        return True
    
    def _check_automation_configured(self, deliverables: Dict[str, Any]) -> bool:
        """Verify automation pipeline is configured."""
        automation_config = deliverables.get("automation_config", {})
        
        required_keys = ["ci_cd_pipeline", "quality_gates", "reporting"]
        for key in required_keys:
            if key not in automation_config:
                self.logger.error(f"Missing automation configuration: {key}")
                return False
        
        return True
    
    def _check_integration_coverage(self, deliverables: Dict[str, Any]) -> bool:
        """Verify integration test coverage is adequate."""
        integration_suite = deliverables.get("integration_test_suite", {})
        coverage = integration_suite.get("coverage_percent", 0)
        
        min_coverage = self.quality_standards["integration_test_coverage"]["min"]
        if coverage < min_coverage:
            self.logger.error(f"Integration coverage {coverage}% below minimum {min_coverage}%")
            return False
        
        return True
    
    def _check_e2e_coverage(self, deliverables: Dict[str, Any]) -> bool:
        """Verify e2e test coverage is adequate."""
        e2e_suite = deliverables.get("e2e_test_suite", {})
        coverage = e2e_suite.get("coverage_percent", 0)
        
        min_coverage = self.quality_standards["e2e_test_coverage"]["min"]
        if coverage < min_coverage:
            self.logger.error(f"E2E coverage {coverage}% below minimum {min_coverage}%")
            return False
        
        return True