"""
Final Approver - Makes final deployment approval decisions for DigiNativa features.

Combines quality analysis and deployment readiness validation to make
intelligent approval decisions with detailed reasoning.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime


class FinalApprover:
    """Makes final approval decisions for production deployment."""
    
    def __init__(self):
        """Initialize final approver."""
        self.logger = logging.getLogger(f"{__name__}.FinalApprover")
        
        # Decision criteria weights
        self.decision_weights = {
            "quality_score": 0.40,        # 40% - Overall quality score
            "deployment_readiness": 0.30, # 30% - Deployment readiness score
            "critical_issues": 0.20,      # 20% - Critical issues impact
            "dna_compliance": 0.10        # 10% - DNA compliance score
        }
        
        # Approval thresholds
        self.approval_thresholds = {
            "minimum_overall_score": 85,
            "minimum_readiness_score": 90,
            "maximum_critical_issues": 0,
            "minimum_dna_score": 80
        }
        
        self.logger.info(f"Final approver initialized with decision weights: {self.decision_weights}")
    
    async def make_approval_decision(self, quality_analysis: Dict[str, Any], 
                                   deployment_readiness: Dict[str, Any],
                                   quality_thresholds: Dict[str, Any]) -> Dict[str, Any]:
        """Make final approval decision based on all analysis results."""
        try:
            self.logger.debug("Making final approval decision")
            
            # Extract key metrics
            overall_score = quality_analysis.get("overall_score", 0)
            readiness_score = deployment_readiness.get("readiness_score", 0)
            blocking_issues = deployment_readiness.get("blocking_issues", [])
            dna_score = quality_analysis.get("dna_compliance", {}).get("score", 0)
            
            # Analyze critical factors
            decision_factors = await self._analyze_decision_factors(
                quality_analysis, deployment_readiness, quality_thresholds
            )
            
            # Calculate weighted decision score
            decision_score = await self._calculate_decision_score(decision_factors)
            
            # Determine approval status
            approved = await self._determine_approval_status(
                decision_factors, decision_score, blocking_issues
            )
            
            # Generate approval reasoning
            reasoning = await self._generate_approval_reasoning(
                approved, decision_factors, decision_score
            )
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(
                approved, quality_analysis, deployment_readiness
            )
            
            # Create approval decision
            approval_decision = {
                "approved": approved,
                "decision_score": decision_score,
                "confidence_level": self._calculate_confidence_level(decision_factors),
                "reasoning": reasoning,
                "recommendations": recommendations,
                "decision_factors": decision_factors,
                "blocking_issues": blocking_issues if not approved else [],
                "approval_conditions": self._get_approval_conditions(approved, decision_factors),
                "next_actions": self._get_next_actions(approved, quality_analysis, deployment_readiness)
            }
            
            self.logger.info(f"Approval decision made: {'APPROVED' if approved else 'REJECTED'} (Score: {decision_score})")
            return approval_decision
            
        except Exception as e:
            self.logger.error(f"Approval decision failed: {e}")
            return {
                "approved": False,
                "decision_score": 0,
                "reasoning": f"Approval decision failed due to error: {e}",
                "recommendations": ["Fix approval decision process before retrying"],
                "blocking_issues": [f"Decision process error: {e}"]
            }
    
    async def _analyze_decision_factors(self, quality_analysis: Dict[str, Any], 
                                      deployment_readiness: Dict[str, Any],
                                      quality_thresholds: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze all factors that influence the approval decision."""
        factors = {}
        
        # Quality score factor
        overall_score = quality_analysis.get("overall_score", 0)
        factors["quality_score"] = {
            "value": overall_score,
            "threshold": quality_thresholds.get("overall_score", 90),
            "meets_threshold": overall_score >= quality_thresholds.get("overall_score", 90),
            "impact": "high" if overall_score >= 90 else "medium" if overall_score >= 80 else "low"
        }
        
        # Deployment readiness factor
        readiness_score = deployment_readiness.get("readiness_score", 0)
        factors["deployment_readiness"] = {
            "value": readiness_score,
            "threshold": self.approval_thresholds["minimum_readiness_score"],
            "meets_threshold": readiness_score >= self.approval_thresholds["minimum_readiness_score"],
            "impact": "high" if readiness_score >= 95 else "medium" if readiness_score >= 85 else "low"
        }
        
        # Critical issues factor
        critical_issues_count = len([
            issue for issue in quality_analysis.get("quality_issues", [])
            if issue.get("type") == "critical" or issue.get("blocking", False)
        ])
        factors["critical_issues"] = {
            "value": critical_issues_count,
            "threshold": self.approval_thresholds["maximum_critical_issues"],
            "meets_threshold": critical_issues_count <= self.approval_thresholds["maximum_critical_issues"],
            "impact": "high" if critical_issues_count == 0 else "low"
        }
        
        # DNA compliance factor
        dna_score = quality_analysis.get("dna_compliance", {}).get("score", 0)
        factors["dna_compliance"] = {
            "value": dna_score,
            "threshold": self.approval_thresholds["minimum_dna_score"],
            "meets_threshold": dna_score >= self.approval_thresholds["minimum_dna_score"],
            "impact": "high" if dna_score >= 90 else "medium" if dna_score >= 80 else "low"
        }
        
        # Performance factor
        performance_score = quality_analysis.get("performance", {}).get("score", 0)
        factors["performance"] = {
            "value": performance_score,
            "threshold": 85,
            "meets_threshold": performance_score >= 85,
            "impact": "high" if performance_score >= 90 else "medium" if performance_score >= 80 else "low"
        }
        
        # Test quality factor
        test_score = quality_analysis.get("test_quality", {}).get("score", 0)
        factors["test_quality"] = {
            "value": test_score,
            "threshold": 90,
            "meets_threshold": test_score >= 90,
            "impact": "high" if test_score >= 95 else "medium" if test_score >= 85 else "low"
        }
        
        return factors
    
    async def _calculate_decision_score(self, decision_factors: Dict[str, Any]) -> float:
        """Calculate weighted decision score from all factors."""
        total_score = 0
        
        # Calculate weighted scores for primary factors
        for factor_name, weight in self.decision_weights.items():
            factor_data = decision_factors.get(factor_name, {})
            factor_value = factor_data.get("value", 0)
            
            # Normalize factor values to 0-100 scale
            if factor_name == "critical_issues":
                # For critical issues, 0 issues = 100 score, more issues = lower score
                normalized_value = max(0, 100 - (factor_value * 25))
            else:
                # For other factors, use value directly (assuming 0-100 scale)
                normalized_value = min(100, max(0, factor_value))
            
            weighted_score = normalized_value * weight
            total_score += weighted_score
            
            self.logger.debug(f"{factor_name}: {factor_value} -> {normalized_value} * {weight} = {weighted_score}")
        
        return round(total_score, 1)
    
    async def _determine_approval_status(self, decision_factors: Dict[str, Any], 
                                       decision_score: float, 
                                       blocking_issues: List[str]) -> bool:
        """Determine approval status based on decision factors and blocking issues."""
        # Hard blockers - automatically reject
        if blocking_issues:
            self.logger.info(f"Rejecting due to {len(blocking_issues)} blocking issues")
            return False
        
        # Check critical factors
        critical_failures = []
        
        for factor_name, factor_data in decision_factors.items():
            if not factor_data.get("meets_threshold", False):
                if factor_name in ["critical_issues", "deployment_readiness"]:
                    critical_failures.append(factor_name)
        
        if critical_failures:
            self.logger.info(f"Rejecting due to critical failures: {critical_failures}")
            return False
        
        # Check overall decision score
        if decision_score < self.approval_thresholds["minimum_overall_score"]:
            self.logger.info(f"Rejecting due to low decision score: {decision_score}")
            return False
        
        # All checks passed
        self.logger.info(f"Approving with decision score: {decision_score}")
        return True
    
    async def _generate_approval_reasoning(self, approved: bool, 
                                         decision_factors: Dict[str, Any], 
                                         decision_score: float) -> str:
        """Generate detailed reasoning for the approval decision."""
        reasoning_parts = []
        
        if approved:
            reasoning_parts.append(f" APPROVED for production deployment (Decision Score: {decision_score}/100)")
            reasoning_parts.append("")
            reasoning_parts.append(" **Approval Criteria Met:**")
            
            # List met criteria
            for factor_name, factor_data in decision_factors.items():
                if factor_data.get("meets_threshold", False):
                    value = factor_data.get("value")
                    threshold = factor_data.get("threshold")
                    reasoning_parts.append(f"  - {factor_name.replace('_', ' ').title()}: {value} meets threshold of {threshold}")
        else:
            reasoning_parts.append(f"L REJECTED for production deployment (Decision Score: {decision_score}/100)")
            reasoning_parts.append("")
            reasoning_parts.append("L **Blocking Issues:**")
            
            # List unmet criteria
            for factor_name, factor_data in decision_factors.items():
                if not factor_data.get("meets_threshold", False):
                    value = factor_data.get("value")
                    threshold = factor_data.get("threshold")
                    reasoning_parts.append(f"  - {factor_name.replace('_', ' ').title()}: {value} below threshold of {threshold}")
        
        return "\n".join(reasoning_parts)
    
    async def _generate_recommendations(self, approved: bool, 
                                      quality_analysis: Dict[str, Any], 
                                      deployment_readiness: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on approval decision and analysis."""
        recommendations = []
        
        if approved:
            # Recommendations for approved deployments
            recommendations.append("Deploy to production with monitoring")
            recommendations.append("Set up production health checks and alerting")
            recommendations.append("Monitor user feedback and performance metrics post-deployment")
            
            # Check for areas of improvement
            overall_score = quality_analysis.get("overall_score", 0)
            if overall_score < 95:
                recommendations.append("Consider further optimization for even higher quality in future releases")
            
        else:
            # Recommendations for rejected deployments
            recommendations.append("Address all blocking issues before resubmission")
            
            # Specific recommendations based on failing areas
            quality_issues = quality_analysis.get("quality_issues", [])
            for issue in quality_issues:
                if issue.get("blocking", False):
                    category = issue.get("category", "general")
                    if category == "performance":
                        recommendations.append("Optimize performance: reduce API response times and improve Lighthouse scores")
                    elif category == "test_quality":
                        recommendations.append("Improve test coverage and fix failing tests")
                    elif category == "accessibility":
                        recommendations.append("Fix accessibility violations and ensure WCAG compliance")
                    elif category == "dna_compliance":
                        recommendations.append("Review implementation against DigiNativa DNA principles")
            
            # General improvement recommendations
            recommendations.append("Run comprehensive quality checks before resubmission")
            recommendations.append("Consider additional testing and validation")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _calculate_confidence_level(self, decision_factors: Dict[str, Any]) -> str:
        """Calculate confidence level in the approval decision."""
        factors_met = sum(1 for factor in decision_factors.values() if factor.get("meets_threshold", False))
        total_factors = len(decision_factors)
        confidence_ratio = factors_met / total_factors if total_factors > 0 else 0
        
        if confidence_ratio >= 0.9:
            return "high"
        elif confidence_ratio >= 0.7:
            return "medium"
        else:
            return "low"
    
    def _get_approval_conditions(self, approved: bool, decision_factors: Dict[str, Any]) -> List[str]:
        """Get conditions that must be met for approval."""
        if approved:
            return []
        
        conditions = []
        for factor_name, factor_data in decision_factors.items():
            if not factor_data.get("meets_threshold", False):
                value = factor_data.get("value")
                threshold = factor_data.get("threshold")
                
                if factor_name == "critical_issues":
                    conditions.append(f"Resolve all {value} critical issues")
                else:
                    conditions.append(f"Improve {factor_name.replace('_', ' ')} from {value} to at least {threshold}")
        
        return conditions
    
    def _get_next_actions(self, approved: bool, quality_analysis: Dict[str, Any], 
                         deployment_readiness: Dict[str, Any]) -> List[str]:
        """Get specific next actions based on approval decision."""
        if approved:
            return [
                "Initiate production deployment pipeline",
                "Notify stakeholders of deployment approval",
                "Prepare production monitoring and rollback procedures",
                "Document deployment decision and quality metrics"
            ]
        else:
            actions = [
                "Return to development team with feedback",
                "Address all blocking issues identified",
                "Re-run quality assurance testing",
                "Resubmit for quality review when ready"
            ]
            
            # Add specific actions based on failing areas
            blocking_issues = deployment_readiness.get("blocking_issues", [])
            if any("performance" in issue.lower() for issue in blocking_issues):
                actions.append("Focus on performance optimization and testing")
            
            if any("security" in issue.lower() for issue in blocking_issues):
                actions.append("Conduct security review and implement fixes")
            
            if any("accessibility" in issue.lower() for issue in blocking_issues):
                actions.append("Perform accessibility audit and remediation")
            
            return actions