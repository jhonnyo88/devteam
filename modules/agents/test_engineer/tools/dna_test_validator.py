"""
DNA Test Validator - Active DNA validation for Test Engineer agent.

PURPOSE:
Implements active DNA compliance validation for test generation and quality assessment,
ensuring Test Engineer output meets DigiNativa DNA principles.

CRITICAL FUNCTIONALITY:
- Time Respect → Test execution time analysis (test suite completion under 10 minutes)
- Pedagogical Value → Test effectiveness for learning validation  
- Professional Tone → Test content and reporting language analysis

ADAPTATION GUIDE:
To adapt for your project:
1. Update test_execution_thresholds for your performance standards
2. Modify test_effectiveness_criteria for your quality requirements
3. Adjust professional_standards for your documentation style
4. Update validation_criteria for your testing standards

CONTRACT PROTECTION:
This tool enhances Test Engineer DNA validation without breaking contracts.
All outputs integrate seamlessly with existing test validation results.
"""

import asyncio
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Setup logging
logger = logging.getLogger(__name__)


class TestExecutionEfficiency(Enum):
    """Test execution efficiency levels for time respect validation."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    SLOW = "slow"
    EXCESSIVE = "excessive"


class TestEffectivenessLevel(Enum):
    """Test effectiveness levels for pedagogical value validation."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    INADEQUATE = "inadequate"


class TestDocumentationQuality(Enum):
    """Test documentation quality for professional tone."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    UNCLEAR = "unclear"
    UNPROFESSIONAL = "unprofessional"


@dataclass
class TestExecutionResult:
    """Result from test execution time analysis."""
    execution_efficiency: TestExecutionEfficiency
    total_execution_time_minutes: float
    unit_test_time_minutes: float
    integration_test_time_minutes: float
    e2e_test_time_minutes: float
    parallel_execution_possible: bool
    time_violations: List[str]
    optimization_recommendations: List[str]


@dataclass
class TestEffectivenessResult:
    """Result from test effectiveness validation."""
    effectiveness_level: TestEffectivenessLevel
    test_effectiveness_score: float  # 1-5 scale
    learning_validation_coverage: Dict[str, bool]
    critical_paths_covered: bool
    edge_cases_covered: bool
    user_scenarios_validated: bool
    effectiveness_violations: List[str]
    improvement_recommendations: List[str]


@dataclass
class TestDocumentationResult:
    """Result from test documentation analysis."""
    documentation_quality: TestDocumentationQuality
    professional_score: float  # 1-5 scale
    municipal_terminology_present: Dict[str, int]
    test_descriptions_clear: bool
    error_messages_professional: bool
    documentation_violations: List[str]
    test_cases_documented: int
    documentation_recommendations: List[str]


@dataclass
class DNATestValidationResult:
    """Complete DNA test validation result."""
    overall_dna_compliant: bool
    time_respect_compliant: bool
    pedagogical_value_compliant: bool
    professional_tone_compliant: bool
    test_execution_result: TestExecutionResult
    test_effectiveness_result: TestEffectivenessResult
    test_documentation_result: TestDocumentationResult
    validation_timestamp: str
    dna_compliance_score: float  # 1-5 scale
    quality_reviewer_metrics: Dict[str, Any]  # For Quality Reviewer integration


class DNATestValidator:
    """
    Active DNA validation for Test Engineer test generation.
    
    Validates test suites against DigiNativa DNA principles:
    - Time Respect: Test execution time analysis for efficient validation
    - Pedagogical Value: Test effectiveness for learning validation
    - Professional Tone: Test documentation and reporting quality
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DNA Test Validator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Time Respect validation thresholds
        self.test_execution_thresholds = {
            "max_total_execution_minutes": 10.0,  # Total test suite
            "max_unit_test_minutes": 2.0,
            "max_integration_test_minutes": 5.0,
            "max_e2e_test_minutes": 8.0,
            "parallel_execution_threshold": 3.0  # Enable parallel if > 3 minutes
        }
        
        # Pedagogical Value validation criteria
        self.test_effectiveness_criteria = {
            "min_test_effectiveness": 4.0,  # 1-5 scale
            "min_learning_coverage": 0.9,  # 90% of learning objectives
            "required_critical_paths": True,
            "required_edge_cases": True,
            "min_user_scenarios": 3
        }
        
        # Professional Tone validation standards
        self.professional_standards = {
            "min_professional_score": 4.0,  # 1-5 scale
            "required_test_terminology": [
                "validera", "verifiera", "test", "kontroll", "säkerställa",
                "kvalitet", "krav", "acceptanskriterier", "täckning", "scenario"
            ],
            "forbidden_casual_terms": [
                "kolla", "fixa", "funkar", "borde", "kanske", "typ"
            ],
            "min_documentation_ratio": 0.8  # 80% of tests documented
        }
        
        logger.info("DNA Test Validator initialized for Test Engineer")
    
    async def validate_test_dna_compliance(self,
                                         integration_test_suite: Dict[str, Any],
                                         e2e_test_suite: Dict[str, Any],
                                         performance_results: Dict[str, Any],
                                         coverage_report: Dict[str, Any],
                                         story_data: Dict[str, Any]) -> DNATestValidationResult:
        """
        Comprehensive DNA validation for test generation.
        
        Args:
            integration_test_suite: Integration test specifications
            e2e_test_suite: End-to-end test specifications
            performance_results: Performance test results
            coverage_report: Test coverage analysis
            story_data: Original story requirements
            
        Returns:
            Complete DNA test validation result
        """
        try:
            logger.info("Starting comprehensive DNA test validation")
            
            # Validate Time Respect (test execution efficiency)
            test_execution_result = await self._validate_test_execution_time(
                integration_test_suite, e2e_test_suite, performance_results, story_data
            )
            
            # Validate Pedagogical Value (test effectiveness)
            test_effectiveness_result = await self._validate_test_effectiveness(
                integration_test_suite, e2e_test_suite, coverage_report, story_data
            )
            
            # Validate Professional Tone (test documentation)
            test_documentation_result = await self._validate_test_documentation(
                integration_test_suite, e2e_test_suite, story_data
            )
            
            # Calculate overall DNA compliance
            time_respect_compliant = test_execution_result.execution_efficiency in [
                TestExecutionEfficiency.EXCELLENT, TestExecutionEfficiency.GOOD, TestExecutionEfficiency.ACCEPTABLE
            ]
            
            pedagogical_value_compliant = test_effectiveness_result.effectiveness_level in [
                TestEffectivenessLevel.EXCELLENT, TestEffectivenessLevel.GOOD, TestEffectivenessLevel.ACCEPTABLE
            ]
            
            professional_tone_compliant = test_documentation_result.documentation_quality in [
                TestDocumentationQuality.EXCELLENT, TestDocumentationQuality.GOOD, TestDocumentationQuality.ACCEPTABLE
            ]
            
            overall_dna_compliant = all([
                time_respect_compliant,
                pedagogical_value_compliant,
                professional_tone_compliant
            ])
            
            # Calculate overall DNA compliance score (1-5 scale)
            execution_score = self._efficiency_to_score(test_execution_result.execution_efficiency)
            effectiveness_score = test_effectiveness_result.test_effectiveness_score
            documentation_score = test_documentation_result.professional_score
            
            dna_compliance_score = (execution_score + effectiveness_score + documentation_score) / 3.0
            
            # Prepare metrics for Quality Reviewer
            quality_reviewer_metrics = {
                "test_execution_efficiency": execution_score,
                "test_effectiveness": effectiveness_score,
                "test_documentation_quality": documentation_score,
                "total_test_cases": (
                    integration_test_suite.get("total_test_cases", 0) +
                    e2e_test_suite.get("total_scenarios", 0)
                ),
                "coverage_percentage": coverage_report.get("overall_coverage_percent", 0),
                "performance_validated": performance_results.get("performance_budget_met", False)
            }
            
            validation_result = DNATestValidationResult(
                overall_dna_compliant=overall_dna_compliant,
                time_respect_compliant=time_respect_compliant,
                pedagogical_value_compliant=pedagogical_value_compliant,
                professional_tone_compliant=professional_tone_compliant,
                test_execution_result=test_execution_result,
                test_effectiveness_result=test_effectiveness_result,
                test_documentation_result=test_documentation_result,
                validation_timestamp=datetime.now().isoformat(),
                dna_compliance_score=dna_compliance_score,
                quality_reviewer_metrics=quality_reviewer_metrics
            )
            
            logger.info(f"DNA test validation completed: {dna_compliance_score:.2f}/5.0 score")
            return validation_result
            
        except Exception as e:
            logger.error(f"DNA test validation failed: {e}")
            raise
    
    async def _validate_test_execution_time(self,
                                          integration_test_suite: Dict[str, Any],
                                          e2e_test_suite: Dict[str, Any],
                                          performance_results: Dict[str, Any],
                                          story_data: Dict[str, Any]) -> TestExecutionResult:
        """
        Validate test execution time for Time Respect principle.
        
        Analyzes test execution duration to ensure tests complete
        within reasonable time for rapid feedback cycles.
        """
        try:
            # Extract execution time estimates
            integration_time = integration_test_suite.get("estimated_execution_time_ms", 0) / 60000  # Convert to minutes
            e2e_time = e2e_test_suite.get("estimated_execution_time_ms", 0) / 60000
            
            # Unit tests assumed from coverage report (fast)
            unit_test_count = integration_test_suite.get("total_test_cases", 0)
            unit_time = unit_test_count * 0.01  # 0.01 minutes per unit test
            
            total_execution_time = unit_time + integration_time + e2e_time
            
            # Check if parallel execution would help
            parallel_execution_possible = (
                total_execution_time > self.test_execution_thresholds["parallel_execution_threshold"]
            )
            
            # Determine execution efficiency
            if total_execution_time <= 3.0:
                execution_efficiency = TestExecutionEfficiency.EXCELLENT
            elif total_execution_time <= 5.0:
                execution_efficiency = TestExecutionEfficiency.GOOD
            elif total_execution_time <= 10.0:
                execution_efficiency = TestExecutionEfficiency.ACCEPTABLE
            elif total_execution_time <= 15.0:
                execution_efficiency = TestExecutionEfficiency.SLOW
            else:
                execution_efficiency = TestExecutionEfficiency.EXCESSIVE
            
            # Identify violations
            violations = []
            if total_execution_time > self.test_execution_thresholds["max_total_execution_minutes"]:
                violations.append(f"Total test time {total_execution_time:.1f} minutes exceeds {self.test_execution_thresholds['max_total_execution_minutes']} minutes")
            
            if integration_time > self.test_execution_thresholds["max_integration_test_minutes"]:
                violations.append(f"Integration tests {integration_time:.1f} minutes exceed limit")
            
            if e2e_time > self.test_execution_thresholds["max_e2e_test_minutes"]:
                violations.append(f"E2E tests {e2e_time:.1f} minutes exceed limit")
            
            # Generate optimization recommendations
            recommendations = []
            if execution_efficiency in [TestExecutionEfficiency.SLOW, TestExecutionEfficiency.EXCESSIVE]:
                recommendations.append("Enable parallel test execution to reduce total time")
                recommendations.append("Consider test prioritization for critical paths only")
                recommendations.append("Use test data factories to speed up setup/teardown")
            
            if integration_time > 3.0:
                recommendations.append("Mock external dependencies in integration tests")
            
            if e2e_time > 5.0:
                recommendations.append("Reduce E2E test scenarios to critical user paths only")
            
            return TestExecutionResult(
                execution_efficiency=execution_efficiency,
                total_execution_time_minutes=total_execution_time,
                unit_test_time_minutes=unit_time,
                integration_test_time_minutes=integration_time,
                e2e_test_time_minutes=e2e_time,
                parallel_execution_possible=parallel_execution_possible,
                time_violations=violations,
                optimization_recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Test execution time validation failed: {e}")
            raise
    
    async def _validate_test_effectiveness(self,
                                         integration_test_suite: Dict[str, Any],
                                         e2e_test_suite: Dict[str, Any],
                                         coverage_report: Dict[str, Any],
                                         story_data: Dict[str, Any]) -> TestEffectivenessResult:
        """
        Validate test effectiveness for Pedagogical Value principle.
        
        Analyzes test coverage of learning objectives, critical paths,
        and edge cases to ensure comprehensive validation.
        """
        try:
            # Analyze learning objective coverage
            learning_objectives = story_data.get("learning_objectives", [])
            learning_coverage = {}
            
            # Check if tests validate each learning objective
            for objective in learning_objectives:
                # Look for test cases that validate this objective
                covered = self._check_learning_objective_coverage(
                    objective, integration_test_suite, e2e_test_suite
                )
                learning_coverage[objective] = covered
            
            coverage_percentage = sum(learning_coverage.values()) / len(learning_objectives) if learning_objectives else 1.0
            
            # Check critical path coverage
            critical_paths_covered = self._check_critical_paths_coverage(
                integration_test_suite, e2e_test_suite, story_data
            )
            
            # Check edge case coverage
            edge_cases_covered = self._check_edge_cases_coverage(
                integration_test_suite, e2e_test_suite
            )
            
            # Check user scenario validation
            user_scenarios_validated = e2e_test_suite.get("total_scenarios", 0) >= self.test_effectiveness_criteria["min_user_scenarios"]
            
            # Calculate test effectiveness score (1-5 scale)
            effectiveness_factors = {
                "learning_coverage": coverage_percentage * 2.0,  # Max 2 points
                "critical_paths": 1.0 if critical_paths_covered else 0.0,
                "edge_cases": 1.0 if edge_cases_covered else 0.0,
                "user_scenarios": 1.0 if user_scenarios_validated else 0.0
            }
            
            test_effectiveness_score = sum(effectiveness_factors.values())
            
            # Determine effectiveness level
            if test_effectiveness_score >= 4.5:
                effectiveness_level = TestEffectivenessLevel.EXCELLENT
            elif test_effectiveness_score >= 3.5:
                effectiveness_level = TestEffectivenessLevel.GOOD
            elif test_effectiveness_score >= 2.5:
                effectiveness_level = TestEffectivenessLevel.ACCEPTABLE
            elif test_effectiveness_score >= 1.5:
                effectiveness_level = TestEffectivenessLevel.POOR
            else:
                effectiveness_level = TestEffectivenessLevel.INADEQUATE
            
            # Identify violations
            violations = []
            if coverage_percentage < self.test_effectiveness_criteria["min_learning_coverage"]:
                violations.append(f"Learning objective coverage {coverage_percentage:.0%} below minimum {self.test_effectiveness_criteria['min_learning_coverage']:.0%}")
            
            if not critical_paths_covered:
                violations.append("Critical user paths not adequately tested")
            
            if not edge_cases_covered:
                violations.append("Edge cases and error scenarios not covered")
            
            if not user_scenarios_validated:
                violations.append(f"Only {e2e_test_suite.get('total_scenarios', 0)} user scenarios, need {self.test_effectiveness_criteria['min_user_scenarios']}")
            
            # Generate improvement recommendations
            recommendations = []
            if coverage_percentage < 0.9:
                recommendations.append("Add tests specifically targeting uncovered learning objectives")
            
            if not critical_paths_covered:
                recommendations.append("Prioritize testing of critical user workflows")
            
            if not edge_cases_covered:
                recommendations.append("Add negative test cases and boundary value tests")
            
            if not user_scenarios_validated:
                recommendations.append("Create more E2E scenarios covering Anna persona workflows")
            
            return TestEffectivenessResult(
                effectiveness_level=effectiveness_level,
                test_effectiveness_score=test_effectiveness_score,
                learning_validation_coverage=learning_coverage,
                critical_paths_covered=critical_paths_covered,
                edge_cases_covered=edge_cases_covered,
                user_scenarios_validated=user_scenarios_validated,
                effectiveness_violations=violations,
                improvement_recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Test effectiveness validation failed: {e}")
            raise
    
    async def _validate_test_documentation(self,
                                         integration_test_suite: Dict[str, Any],
                                         e2e_test_suite: Dict[str, Any],
                                         story_data: Dict[str, Any]) -> TestDocumentationResult:
        """
        Validate test documentation for Professional Tone principle.
        
        Analyzes test descriptions, error messages, and documentation
        quality for professional municipal communication.
        """
        try:
            # Count documented vs undocumented tests
            integration_tests = integration_test_suite.get("test_cases", [])
            e2e_scenarios = e2e_test_suite.get("scenarios", [])
            
            total_test_cases = len(integration_tests) + len(e2e_scenarios)
            documented_tests = 0
            
            # Collect all test documentation text
            all_documentation = []
            
            # Check integration test documentation
            for test in integration_tests:
                if test.get("description"):
                    documented_tests += 1
                    all_documentation.append(test["description"])
            
            # Check E2E scenario documentation
            for scenario in e2e_scenarios:
                if scenario.get("description"):
                    documented_tests += 1
                    all_documentation.append(scenario["description"])
            
            documentation_ratio = documented_tests / total_test_cases if total_test_cases > 0 else 0.0
            
            # Analyze municipal terminology usage
            municipal_terminology_present = {}
            for term in self.professional_standards["required_test_terminology"]:
                count = sum(doc.lower().count(term) for doc in all_documentation)
                municipal_terminology_present[term] = count
            
            total_professional_terms = sum(municipal_terminology_present.values())
            
            # Check for casual/unprofessional language
            casual_violations = []
            for doc in all_documentation:
                for casual_term in self.professional_standards["forbidden_casual_terms"]:
                    if casual_term in doc.lower():
                        casual_violations.append(f"Casual term '{casual_term}' found in: '{doc[:50]}...'")
            
            # Assess clarity of test descriptions
            test_descriptions_clear = documentation_ratio >= self.professional_standards["min_documentation_ratio"]
            
            # Check error message professionalism (from test cases)
            error_messages_professional = len(casual_violations) == 0
            
            # Calculate professional score (1-5 scale)
            professional_factors = {
                "documentation_completeness": documentation_ratio * 2.0,  # Max 2 points
                "professional_terminology": min(total_professional_terms / 10.0, 1.5),  # Max 1.5 points
                "no_casual_language": 1.0 if not casual_violations else 0.0,
                "clarity": 0.5 if test_descriptions_clear else 0.0
            }
            
            professional_score = sum(professional_factors.values())
            
            # Determine documentation quality
            if professional_score >= 4.5:
                documentation_quality = TestDocumentationQuality.EXCELLENT
            elif professional_score >= 3.5:
                documentation_quality = TestDocumentationQuality.GOOD
            elif professional_score >= 2.5:
                documentation_quality = TestDocumentationQuality.ACCEPTABLE
            elif professional_score >= 1.5:
                documentation_quality = TestDocumentationQuality.UNCLEAR
            else:
                documentation_quality = TestDocumentationQuality.UNPROFESSIONAL
            
            # Identify violations
            violations = []
            if documentation_ratio < self.professional_standards["min_documentation_ratio"]:
                violations.append(f"Only {documentation_ratio:.0%} of tests documented, need {self.professional_standards['min_documentation_ratio']:.0%}")
            
            if total_professional_terms < 5:
                violations.append(f"Insufficient professional terminology: only {total_professional_terms} terms used")
            
            violations.extend(casual_violations)
            
            # Generate documentation recommendations
            recommendations = []
            if documentation_ratio < 0.8:
                recommendations.append("Add clear descriptions to all test cases")
            
            if total_professional_terms < 10:
                recommendations.append("Use more professional testing terminology in descriptions")
            
            if casual_violations:
                recommendations.append("Replace casual language with professional municipal terminology")
            
            if not test_descriptions_clear:
                recommendations.append("Improve test descriptions with clear purpose and expected outcomes")
            
            return TestDocumentationResult(
                documentation_quality=documentation_quality,
                professional_score=professional_score,
                municipal_terminology_present=municipal_terminology_present,
                test_descriptions_clear=test_descriptions_clear,
                error_messages_professional=error_messages_professional,
                documentation_violations=violations,
                test_cases_documented=documented_tests,
                documentation_recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Test documentation validation failed: {e}")
            raise
    
    def _efficiency_to_score(self, efficiency: TestExecutionEfficiency) -> float:
        """Convert execution efficiency to numeric score (1-5)."""
        efficiency_scores = {
            TestExecutionEfficiency.EXCELLENT: 5.0,
            TestExecutionEfficiency.GOOD: 4.0,
            TestExecutionEfficiency.ACCEPTABLE: 3.0,
            TestExecutionEfficiency.SLOW: 2.0,
            TestExecutionEfficiency.EXCESSIVE: 1.0
        }
        return efficiency_scores.get(efficiency, 3.0)
    
    def _check_learning_objective_coverage(self,
                                         objective: str,
                                         integration_suite: Dict[str, Any],
                                         e2e_suite: Dict[str, Any]) -> bool:
        """Check if a learning objective is covered by tests."""
        # Check integration tests
        integration_tests = integration_suite.get("test_cases", [])
        for test in integration_tests:
            if objective.lower() in test.get("description", "").lower():
                return True
        
        # Check E2E scenarios
        e2e_scenarios = e2e_suite.get("scenarios", [])
        for scenario in e2e_scenarios:
            if objective.lower() in scenario.get("description", "").lower():
                return True
        
        # Check if pedagogical tests specifically cover this
        pedagogical_tests = e2e_suite.get("pedagogical_tests", {}).get("scenarios", [])
        for test in pedagogical_tests:
            if objective.lower() in test.get("description", "").lower():
                return True
        
        return False
    
    def _check_critical_paths_coverage(self,
                                     integration_suite: Dict[str, Any],
                                     e2e_suite: Dict[str, Any],
                                     story_data: Dict[str, Any]) -> bool:
        """Check if critical user paths are covered."""
        # Extract critical paths from acceptance criteria
        acceptance_criteria = story_data.get("acceptance_criteria", [])
        if not acceptance_criteria:
            return True  # No specific criteria means basic coverage is enough
        
        # Check if main user flows are tested
        persona_tests = e2e_suite.get("persona_tests", {}).get("scenarios", [])
        critical_scenarios = [s for s in persona_tests if s.get("priority") == "critical"]
        
        # Need at least one critical scenario per acceptance criterion
        return len(critical_scenarios) >= len(acceptance_criteria) * 0.5
    
    def _check_edge_cases_coverage(self,
                                  integration_suite: Dict[str, Any],
                                  e2e_suite: Dict[str, Any]) -> bool:
        """Check if edge cases and error scenarios are covered."""
        # Check for error handling tests
        integration_tests = integration_suite.get("test_cases", [])
        error_tests = [t for t in integration_tests if "error" in t.get("test_type", "").lower()]
        
        # Check for edge case scenarios
        e2e_scenarios = e2e_suite.get("scenarios", [])
        edge_scenarios = [s for s in e2e_scenarios if "error_recovery" in s.get("test_type", "").lower()]
        
        # Need both error handling and edge case coverage
        return len(error_tests) >= 3 and len(edge_scenarios) >= 1