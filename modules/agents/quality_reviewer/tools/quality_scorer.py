"""
Quality Scorer - Comprehensive quality analysis for DigiNativa features.

Analyzes test results, performance metrics, accessibility, user experience,
code quality, and DNA compliance to provide overall quality scoring.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime


class QualityScorer:
    """Analyzes quality metrics and provides comprehensive scoring."""
    
    def __init__(self):
        """Initialize quality scorer."""
        self.logger = logging.getLogger(f"{__name__}.QualityScorer")
        
        # Quality weights for overall score calculation
        self.quality_weights = {
            "test_quality": 0.25,      # 25% - Test coverage and reliability
            "performance": 0.20,       # 20% - Performance metrics
            "accessibility": 0.15,     # 15% - Accessibility compliance
            "user_experience": 0.15,   # 15% - UX validation
            "code_quality": 0.15,      # 15% - Code quality metrics
            "dna_compliance": 0.10     # 10% - DNA principle compliance
        }
        
        self.logger.info("Quality scorer initialized with weights: {}".format(self.quality_weights))
    
    async def analyze_test_quality(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze test quality metrics."""
        try:
            score = 0
            issues = []
            
            # Test coverage analysis
            coverage = test_results.get("coverage_percent", 0)
            if coverage >= 95:
                score += 40
            elif coverage >= 90:
                score += 30
                issues.append(f"Test coverage below 95% ({coverage}%)")
            elif coverage >= 80:
                score += 20
                issues.append(f"Test coverage below 90% ({coverage}%)")
            else:
                score += 10
                issues.append(f"Test coverage critically low ({coverage}%)")
            
            # Test results analysis
            passed_tests = test_results.get("tests_passed", 0)
            total_tests = test_results.get("total_tests", 1)
            pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            
            if pass_rate == 100:
                score += 40
            elif pass_rate >= 95:
                score += 30
                issues.append(f"Some tests failing ({pass_rate:.1f}% pass rate)")
            else:
                score += 10
                issues.append(f"Significant test failures ({pass_rate:.1f}% pass rate)")
            
            # Test quality indicators
            unit_tests = test_results.get("unit_tests", 0)
            integration_tests = test_results.get("integration_tests", 0)
            
            if unit_tests > 0 and integration_tests > 0:
                score += 20
            elif unit_tests > 0 or integration_tests > 0:
                score += 10
                issues.append("Missing either unit or integration tests")
            else:
                issues.append("No comprehensive test suite")
            
            return {
                "score": min(score, 100),
                "coverage_percent": coverage,
                "pass_rate": pass_rate,
                "issues": issues,
                "recommendations": self._get_test_recommendations(issues)
            }
            
        except Exception as e:
            self.logger.error(f"Test quality analysis failed: {e}")
            return {"score": 0, "issues": [f"Analysis failed: {e}"], "recommendations": []}
    
    async def analyze_performance(self, performance_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics."""
        try:
            score = 0
            issues = []
            
            # Lighthouse score analysis
            lighthouse_score = performance_metrics.get("lighthouse_score", 0)
            if lighthouse_score >= 90:
                score += 40
            elif lighthouse_score >= 80:
                score += 30
                issues.append(f"Lighthouse score below 90 ({lighthouse_score})")
            elif lighthouse_score >= 70:
                score += 20
                issues.append(f"Lighthouse score below 80 ({lighthouse_score})")
            else:
                score += 10
                issues.append(f"Poor Lighthouse score ({lighthouse_score})")
            
            # API response time analysis
            api_response_time = performance_metrics.get("api_response_time_ms", 1000)
            if api_response_time <= 200:
                score += 30
            elif api_response_time <= 500:
                score += 20
                issues.append(f"API response time above 200ms ({api_response_time}ms)")
            else:
                score += 10
                issues.append(f"Slow API response time ({api_response_time}ms)")
            
            # Page load time analysis
            page_load_time = performance_metrics.get("page_load_time_ms", 5000)
            if page_load_time <= 2000:
                score += 30
            elif page_load_time <= 3000:
                score += 20
                issues.append(f"Page load time above 2s ({page_load_time}ms)")
            else:
                score += 10
                issues.append(f"Slow page load time ({page_load_time}ms)")
            
            return {
                "score": min(score, 100),
                "lighthouse_score": lighthouse_score,
                "api_response_time_ms": api_response_time,
                "page_load_time_ms": page_load_time,
                "issues": issues,
                "recommendations": self._get_performance_recommendations(issues)
            }
            
        except Exception as e:
            self.logger.error(f"Performance analysis failed: {e}")
            return {"score": 0, "issues": [f"Analysis failed: {e}"], "recommendations": []}
    
    async def analyze_accessibility(self, accessibility_audit: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze accessibility compliance."""
        try:
            score = 0
            issues = []
            
            # WCAG compliance analysis
            wcag_score = accessibility_audit.get("wcag_compliance_percent", 0)
            if wcag_score >= 95:
                score += 50
            elif wcag_score >= 90:
                score += 40
                issues.append(f"WCAG compliance below 95% ({wcag_score}%)")
            elif wcag_score >= 80:
                score += 30
                issues.append(f"WCAG compliance below 90% ({wcag_score}%)")
            else:
                score += 15
                issues.append(f"Poor WCAG compliance ({wcag_score}%)")
            
            # Accessibility violations
            violations = accessibility_audit.get("violations", [])
            if len(violations) == 0:
                score += 30
            elif len(violations) <= 3:
                score += 20
                issues.append(f"{len(violations)} accessibility violations found")
            elif len(violations) <= 10:
                score += 10
                issues.append(f"{len(violations)} accessibility violations found")
            else:
                issues.append(f"Many accessibility violations ({len(violations)})")
            
            # Keyboard navigation
            keyboard_accessible = accessibility_audit.get("keyboard_accessible", False)
            if keyboard_accessible:
                score += 20
            else:
                issues.append("Keyboard navigation issues")
            
            return {
                "score": min(score, 100),
                "wcag_compliance_percent": wcag_score,
                "violations_count": len(violations),
                "keyboard_accessible": keyboard_accessible,
                "issues": issues,
                "recommendations": self._get_accessibility_recommendations(issues)
            }
            
        except Exception as e:
            self.logger.error(f"Accessibility analysis failed: {e}")
            return {"score": 0, "issues": [f"Analysis failed: {e}"], "recommendations": []}
    
    async def analyze_user_experience(self, user_flow_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user experience validation results."""
        try:
            score = 0
            issues = []
            
            # User flow completion rate
            completion_rate = user_flow_validation.get("flow_completion_rate", 0)
            if completion_rate >= 95:
                score += 40
            elif completion_rate >= 90:
                score += 30
                issues.append(f"Flow completion rate below 95% ({completion_rate}%)")
            elif completion_rate >= 80:
                score += 20
                issues.append(f"Flow completion rate below 90% ({completion_rate}%)")
            else:
                score += 10
                issues.append(f"Poor flow completion rate ({completion_rate}%)")
            
            # User satisfaction score
            satisfaction_score = user_flow_validation.get("user_satisfaction_score", 0)
            if satisfaction_score >= 4.5:
                score += 30
            elif satisfaction_score >= 4.0:
                score += 25
                issues.append(f"User satisfaction below 4.5 ({satisfaction_score})")
            elif satisfaction_score >= 3.5:
                score += 15
                issues.append(f"User satisfaction below 4.0 ({satisfaction_score})")
            else:
                score += 5
                issues.append(f"Poor user satisfaction ({satisfaction_score})")
            
            # Time to complete tasks
            avg_task_time = user_flow_validation.get("average_task_completion_minutes", 15)
            target_time = user_flow_validation.get("target_completion_minutes", 10)
            
            if avg_task_time <= target_time:
                score += 30
            elif avg_task_time <= target_time * 1.2:
                score += 20
                issues.append(f"Task completion time slightly above target ({avg_task_time}min vs {target_time}min)")
            else:
                score += 10
                issues.append(f"Task completion time too high ({avg_task_time}min vs {target_time}min)")
            
            return {
                "score": min(score, 100),
                "flow_completion_rate": completion_rate,
                "user_satisfaction_score": satisfaction_score,
                "average_task_completion_minutes": avg_task_time,
                "issues": issues,
                "recommendations": self._get_ux_recommendations(issues)
            }
            
        except Exception as e:
            self.logger.error(f"User experience analysis failed: {e}")
            return {"score": 0, "issues": [f"Analysis failed: {e}"], "recommendations": []}
    
    async def analyze_code_quality(self, code_quality_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code quality metrics."""
        try:
            score = 0
            issues = []
            
            # TypeScript/ESLint errors
            ts_errors = code_quality_metrics.get("typescript_errors", 0)
            eslint_violations = code_quality_metrics.get("eslint_violations", 0)
            
            if ts_errors == 0 and eslint_violations == 0:
                score += 40
            elif ts_errors + eslint_violations <= 5:
                score += 30
                issues.append(f"{ts_errors + eslint_violations} linting issues found")
            elif ts_errors + eslint_violations <= 15:
                score += 20
                issues.append(f"{ts_errors + eslint_violations} linting issues found")
            else:
                score += 10
                issues.append(f"Many linting issues ({ts_errors + eslint_violations})")
            
            # Code complexity
            complexity_score = code_quality_metrics.get("complexity_score", 5)
            if complexity_score <= 3:
                score += 30
            elif complexity_score <= 5:
                score += 20
                issues.append(f"Code complexity above ideal ({complexity_score})")
            else:
                score += 10
                issues.append(f"High code complexity ({complexity_score})")
            
            # Documentation coverage
            doc_coverage = code_quality_metrics.get("documentation_coverage_percent", 0)
            if doc_coverage >= 80:
                score += 30
            elif doc_coverage >= 60:
                score += 20
                issues.append(f"Documentation coverage below 80% ({doc_coverage}%)")
            else:
                score += 10
                issues.append(f"Poor documentation coverage ({doc_coverage}%)")
            
            return {
                "score": min(score, 100),
                "typescript_errors": ts_errors,
                "eslint_violations": eslint_violations,
                "complexity_score": complexity_score,
                "documentation_coverage_percent": doc_coverage,
                "issues": issues,
                "recommendations": self._get_code_quality_recommendations(issues)
            }
            
        except Exception as e:
            self.logger.error(f"Code quality analysis failed: {e}")
            return {"score": 0, "issues": [f"Analysis failed: {e}"], "recommendations": []}
    
    async def analyze_dna_compliance(self, qa_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze DNA compliance throughout the implementation."""
        try:
            score = 0
            issues = []
            
            # Design principles compliance
            design_principles = {
                "pedagogical_value": qa_data.get("pedagogical_effectiveness_score", 0),
                "policy_to_practice": qa_data.get("policy_practice_alignment_score", 0),
                "time_respect": qa_data.get("time_efficiency_score", 0),
                "holistic_thinking": qa_data.get("holistic_design_score", 0),
                "professional_tone": qa_data.get("professional_tone_score", 0)
            }
            
            design_score = sum(design_principles.values()) / len(design_principles)
            if design_score >= 4.0:
                score += 50
            elif design_score >= 3.5:
                score += 40
                issues.append(f"Design principles score below 4.0 ({design_score:.1f})")
            elif design_score >= 3.0:
                score += 30
                issues.append(f"Design principles score below 3.5 ({design_score:.1f})")
            else:
                score += 15
                issues.append(f"Poor design principles compliance ({design_score:.1f})")
            
            # Architecture principles compliance
            architecture_compliance = qa_data.get("architecture_compliance_percent", 0)
            if architecture_compliance >= 95:
                score += 50
            elif architecture_compliance >= 90:
                score += 40
                issues.append(f"Architecture compliance below 95% ({architecture_compliance}%)")
            elif architecture_compliance >= 80:
                score += 30
                issues.append(f"Architecture compliance below 90% ({architecture_compliance}%)")
            else:
                score += 15
                issues.append(f"Poor architecture compliance ({architecture_compliance}%)")
            
            return {
                "score": min(score, 100),
                "design_principles": design_principles,
                "design_principles_avg": design_score,
                "architecture_principles": {"compliance_percent": architecture_compliance},
                "issues": issues,
                "recommendations": self._get_dna_recommendations(issues)
            }
            
        except Exception as e:
            self.logger.error(f"DNA compliance analysis failed: {e}")
            return {"score": 0, "issues": [f"Analysis failed: {e}"], "recommendations": []}
    
    async def calculate_overall_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate weighted overall quality score."""
        try:
            total_score = 0
            
            for dimension, weight in self.quality_weights.items():
                dimension_score = analysis_results.get(dimension, {}).get("score", 0)
                weighted_score = dimension_score * weight
                total_score += weighted_score
                
                self.logger.debug(f"{dimension}: {dimension_score} * {weight} = {weighted_score}")
            
            return round(total_score, 1)
            
        except Exception as e:
            self.logger.error(f"Overall score calculation failed: {e}")
            return 0.0
    
    async def identify_quality_issues(self, analysis_results: Dict[str, Any], thresholds: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify critical quality issues that need attention."""
        issues = []
        
        try:
            # Check overall score
            overall_score = analysis_results.get("overall_score", 0)
            if overall_score < thresholds.get("overall_score", 90):
                issues.append({
                    "type": "critical",
                    "category": "overall_quality",
                    "message": f"Overall quality score below threshold ({overall_score} < {thresholds['overall_score']})",
                    "impact": "high",
                    "blocking": True
                })
            
            # Check individual dimensions
            for dimension in self.quality_weights.keys():
                dimension_result = analysis_results.get(dimension, {})
                dimension_issues = dimension_result.get("issues", [])
                
                for issue in dimension_issues:
                    issues.append({
                        "type": "warning",
                        "category": dimension,
                        "message": issue,
                        "impact": "medium",
                        "blocking": False
                    })
            
            return issues
            
        except Exception as e:
            self.logger.error(f"Quality issues identification failed: {e}")
            return [{
                "type": "error",
                "category": "analysis",
                "message": f"Quality analysis failed: {e}",
                "impact": "high",
                "blocking": True
            }]
    
    def _get_test_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations for test quality improvements."""
        recommendations = []
        
        if any("coverage" in issue.lower() for issue in issues):
            recommendations.append("Increase test coverage by adding unit tests for uncovered code")
            recommendations.append("Add integration tests for critical user flows")
        
        if any("failing" in issue.lower() for issue in issues):
            recommendations.append("Fix failing tests before deployment")
            recommendations.append("Review test stability and remove flaky tests")
        
        if any("missing" in issue.lower() for issue in issues):
            recommendations.append("Implement comprehensive test suite with unit and integration tests")
        
        return recommendations
    
    def _get_performance_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations for performance improvements."""
        recommendations = []
        
        if any("lighthouse" in issue.lower() for issue in issues):
            recommendations.append("Optimize images and assets for better Lighthouse score")
            recommendations.append("Implement code splitting and lazy loading")
        
        if any("api" in issue.lower() for issue in issues):
            recommendations.append("Optimize API queries and reduce database calls")
            recommendations.append("Implement API response caching")
        
        if any("page load" in issue.lower() for issue in issues):
            recommendations.append("Optimize bundle size and remove unused dependencies")
            recommendations.append("Implement progressive loading strategies")
        
        return recommendations
    
    def _get_accessibility_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations for accessibility improvements."""
        recommendations = []
        
        if any("wcag" in issue.lower() for issue in issues):
            recommendations.append("Review and fix WCAG compliance violations")
            recommendations.append("Add proper ARIA labels and semantic HTML")
        
        if any("keyboard" in issue.lower() for issue in issues):
            recommendations.append("Implement proper keyboard navigation support")
            recommendations.append("Add focus indicators for interactive elements")
        
        if any("violations" in issue.lower() for issue in issues):
            recommendations.append("Use accessibility testing tools to identify and fix violations")
        
        return recommendations
    
    def _get_ux_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations for UX improvements."""
        recommendations = []
        
        if any("completion" in issue.lower() for issue in issues):
            recommendations.append("Simplify user flows and reduce cognitive load")
            recommendations.append("Add clearer instructions and guidance")
        
        if any("satisfaction" in issue.lower() for issue in issues):
            recommendations.append("Improve visual design and user feedback")
            recommendations.append("Conduct user research to identify pain points")
        
        if any("time" in issue.lower() for issue in issues):
            recommendations.append("Streamline workflows to reduce task completion time")
            recommendations.append("Remove unnecessary steps from user flows")
        
        return recommendations
    
    def _get_code_quality_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations for code quality improvements."""
        recommendations = []
        
        if any("linting" in issue.lower() for issue in issues):
            recommendations.append("Fix TypeScript and ESLint violations")
            recommendations.append("Set up pre-commit hooks to prevent linting issues")
        
        if any("complexity" in issue.lower() for issue in issues):
            recommendations.append("Refactor complex functions into smaller, focused functions")
            recommendations.append("Extract reusable components and utilities")
        
        if any("documentation" in issue.lower() for issue in issues):
            recommendations.append("Add comprehensive code documentation and comments")
            recommendations.append("Create usage examples and API documentation")
        
        return recommendations
    
    def _get_dna_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations for DNA compliance improvements."""
        recommendations = []
        
        if any("design principles" in issue.lower() for issue in issues):
            recommendations.append("Review implementation against DigiNativa design principles")
            recommendations.append("Enhance pedagogical value and policy-to-practice alignment")
        
        if any("architecture" in issue.lower() for issue in issues):
            recommendations.append("Ensure API-first design and stateless backend compliance")
            recommendations.append("Review separation of concerns and simplicity principles")
        
        return recommendations