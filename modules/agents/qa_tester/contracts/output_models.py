"""
Output contract models for QA Tester agent.

PURPOSE:
Defines the structure and validation for output contracts that the QA Tester
agent produces for the Quality Reviewer agent.

CRITICAL FUNCTIONALITY:
- Output contract structure definition
- QA validation result organization
- Quality metrics calculation
- Production readiness assessment

ADAPTATION GUIDE:
=' To adapt for your project:
1. Update QAValidationResults for your testing scope
2. Modify ProductionReadinessAssessment for your deployment
3. Adjust QualityMetrics for your standards
4. Update validation criteria for your requirements

CONTRACT PROTECTION:
These models are part of DigiNativa's contract system.
Changes must maintain backward compatibility.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ValidationStatus(Enum):
    """QA validation status levels."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    CRITICAL = "critical"


class ProductionReadiness(Enum):
    """Production readiness levels."""
    READY = "ready"
    NEEDS_MINOR_FIXES = "needs_minor_fixes"
    NEEDS_MAJOR_FIXES = "needs_major_fixes"
    NOT_READY = "not_ready"


class PersonaSatisfactionLevel(Enum):
    """Anna persona satisfaction levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    UNACCEPTABLE = "unacceptable"


@dataclass
class PersonaTestingResult:
    """
    Results from Anna persona testing.
    """
    persona_name: str
    satisfaction_score: float  # 1-5 scale
    task_completion_rate: float  # percentage
    average_completion_time_minutes: float
    learning_effectiveness_score: float  # 1-5 scale
    confusion_incidents: List[str]
    positive_feedback: List[str]
    improvement_suggestions: List[str]
    time_constraint_violations: int
    accessibility_issues_encountered: List[str]
    satisfaction_level: PersonaSatisfactionLevel
    
    def meets_requirements(self, requirements: Dict[str, Any]) -> bool:
        """Check if persona testing meets requirements."""
        return (
            self.satisfaction_score >= requirements.get("min_satisfaction_score", 4.0) and
            self.task_completion_rate >= requirements.get("min_completion_rate", 95.0) and
            self.average_completion_time_minutes <= requirements.get("max_completion_time", 10.0) and
            len(self.confusion_incidents) <= requirements.get("max_confusion_incidents", 2)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "persona_name": self.persona_name,
            "satisfaction_score": self.satisfaction_score,
            "task_completion_rate": self.task_completion_rate,
            "average_completion_time_minutes": self.average_completion_time_minutes,
            "learning_effectiveness_score": self.learning_effectiveness_score,
            "confusion_incidents": self.confusion_incidents,
            "positive_feedback": self.positive_feedback,
            "improvement_suggestions": self.improvement_suggestions,
            "time_constraint_violations": self.time_constraint_violations,
            "accessibility_issues_encountered": self.accessibility_issues_encountered,
            "satisfaction_level": self.satisfaction_level.value
        }


@dataclass
class AccessibilityValidationResult:
    """
    Results from accessibility compliance testing.
    """
    wcag_level: str  # "A", "AA", "AAA"
    compliance_percentage: float
    violations_found: List[Dict[str, Any]]
    screen_reader_compatibility: bool
    keyboard_navigation_score: float
    color_contrast_issues: List[str]
    alternative_text_coverage: float
    focus_management_score: float
    assistive_technology_support: Dict[str, Any]
    certification_status: str
    
    def is_compliant(self, target_level: str = "AA") -> bool:
        """Check if accessibility is compliant with target level."""
        level_requirements = {
            "A": 85.0,
            "AA": 95.0,
            "AAA": 98.0
        }
        return self.compliance_percentage >= level_requirements.get(target_level, 95.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "wcag_level": self.wcag_level,
            "compliance_percentage": self.compliance_percentage,
            "violations_found": self.violations_found,
            "screen_reader_compatibility": self.screen_reader_compatibility,
            "keyboard_navigation_score": self.keyboard_navigation_score,
            "color_contrast_issues": self.color_contrast_issues,
            "alternative_text_coverage": self.alternative_text_coverage,
            "focus_management_score": self.focus_management_score,
            "assistive_technology_support": self.assistive_technology_support,
            "certification_status": self.certification_status
        }


@dataclass
class UserFlowValidationResult:
    """
    Results from user flow validation.
    """
    flow_id: str
    flow_name: str
    validation_status: ValidationStatus
    success_rate_percentage: float
    average_completion_time_minutes: float
    critical_issues: List[str]
    usability_issues: List[str]
    navigation_consistency_score: float
    error_recovery_effectiveness: float
    user_guidance_adequacy: float
    anna_persona_compatibility: bool
    
    def is_flow_acceptable(self) -> bool:
        """Check if flow meets acceptable standards."""
        return (
            self.validation_status in [ValidationStatus.PASSED, ValidationStatus.WARNING] and
            self.success_rate_percentage >= 90.0 and
            len(self.critical_issues) == 0
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "flow_id": self.flow_id,
            "flow_name": self.flow_name,
            "validation_status": self.validation_status.value,
            "success_rate_percentage": self.success_rate_percentage,
            "average_completion_time_minutes": self.average_completion_time_minutes,
            "critical_issues": self.critical_issues,
            "usability_issues": self.usability_issues,
            "navigation_consistency_score": self.navigation_consistency_score,
            "error_recovery_effectiveness": self.error_recovery_effectiveness,
            "user_guidance_adequacy": self.user_guidance_adequacy,
            "anna_persona_compatibility": self.anna_persona_compatibility
        }


@dataclass
class ContentQualityAssessment:
    """
    Assessment of content quality and tone.
    """
    professional_tone_score: float  # 1-5 scale
    pedagogical_value_score: float  # 1-5 scale
    policy_relevance_score: float  # 1-5 scale
    clarity_score: float  # 1-5 scale
    consistency_score: float  # 1-5 scale
    language_appropriateness: str  # "excellent", "good", "needs_improvement"
    terminology_accuracy: float  # percentage
    content_completeness: float  # percentage
    municipal_context_alignment: bool
    improvement_areas: List[str]
    
    def meets_dna_standards(self) -> bool:
        """Check if content meets DNA design principles."""
        return (
            self.professional_tone_score >= 4.0 and
            self.pedagogical_value_score >= 4.0 and
            self.policy_relevance_score >= 4.0 and
            self.municipal_context_alignment
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "professional_tone_score": self.professional_tone_score,
            "pedagogical_value_score": self.pedagogical_value_score,
            "policy_relevance_score": self.policy_relevance_score,
            "clarity_score": self.clarity_score,
            "consistency_score": self.consistency_score,
            "language_appropriateness": self.language_appropriateness,
            "terminology_accuracy": self.terminology_accuracy,
            "content_completeness": self.content_completeness,
            "municipal_context_alignment": self.municipal_context_alignment,
            "improvement_areas": self.improvement_areas
        }


@dataclass
class QualityMetrics:
    """
    Overall quality metrics from QA testing.
    """
    overall_quality_score: float  # 1-5 scale
    user_satisfaction_score: float  # 1-5 scale
    technical_performance_score: float  # 1-5 scale
    accessibility_compliance_score: float  # percentage
    content_quality_score: float  # 1-5 scale
    anna_persona_readiness_score: float  # 1-5 scale
    production_readiness_percentage: float
    risk_assessment: str  # "low", "medium", "high"
    deployment_recommendation: str
    
    def calculate_weighted_score(self) -> float:
        """Calculate weighted overall score."""
        weights = {
            "user_satisfaction": 0.25,
            "technical_performance": 0.20,
            "accessibility": 0.20,
            "content_quality": 0.20,
            "anna_readiness": 0.15
        }
        
        weighted_score = (
            self.user_satisfaction_score * weights["user_satisfaction"] +
            self.technical_performance_score * weights["technical_performance"] +
            (self.accessibility_compliance_score / 20) * weights["accessibility"] +  # Convert to 1-5 scale
            self.content_quality_score * weights["content_quality"] +
            self.anna_persona_readiness_score * weights["anna_readiness"]
        )
        
        return round(weighted_score, 2)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "overall_quality_score": self.overall_quality_score,
            "user_satisfaction_score": self.user_satisfaction_score,
            "technical_performance_score": self.technical_performance_score,
            "accessibility_compliance_score": self.accessibility_compliance_score,
            "content_quality_score": self.content_quality_score,
            "anna_persona_readiness_score": self.anna_persona_readiness_score,
            "production_readiness_percentage": self.production_readiness_percentage,
            "risk_assessment": self.risk_assessment,
            "deployment_recommendation": self.deployment_recommendation,
            "weighted_overall_score": self.calculate_weighted_score()
        }


@dataclass
class QARecommendation:
    """
    QA improvement recommendation.
    """
    recommendation_id: str
    category: str  # "performance", "accessibility", "usability", "content", "persona"
    priority: str  # "critical", "high", "medium", "low"
    issue_description: str
    recommended_action: str
    expected_impact: str
    effort_estimate: str  # "low", "medium", "high"
    affects_anna_persona: bool
    affects_accessibility: bool
    implementation_guidance: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "recommendation_id": self.recommendation_id,
            "category": self.category,
            "priority": self.priority,
            "issue_description": self.issue_description,
            "recommended_action": self.recommended_action,
            "expected_impact": self.expected_impact,
            "effort_estimate": self.effort_estimate,
            "affects_anna_persona": self.affects_anna_persona,
            "affects_accessibility": self.affects_accessibility,
            "implementation_guidance": self.implementation_guidance
        }


@dataclass
class QAValidationResults:
    """
    Complete QA validation results.
    """
    story_id: str
    validation_timestamp: str
    validation_duration_minutes: float
    overall_validation_status: ValidationStatus
    persona_testing_results: PersonaTestingResult
    accessibility_validation: AccessibilityValidationResult
    user_flow_validations: List[UserFlowValidationResult]
    content_quality_assessment: ContentQualityAssessment
    quality_metrics: QualityMetrics
    recommendations: List[QARecommendation]
    critical_issues: List[str]
    blocking_issues: List[str]
    
    def has_blocking_issues(self) -> bool:
        """Check if there are blocking issues for production."""
        return len(self.blocking_issues) > 0 or len(self.critical_issues) > 0
    
    def get_priority_recommendations(self) -> List[QARecommendation]:
        """Get high and critical priority recommendations."""
        return [rec for rec in self.recommendations if rec.priority in ["critical", "high"]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "story_id": self.story_id,
            "validation_timestamp": self.validation_timestamp,
            "validation_duration_minutes": self.validation_duration_minutes,
            "overall_validation_status": self.overall_validation_status.value,
            "persona_testing_results": self.persona_testing_results.to_dict(),
            "accessibility_validation": self.accessibility_validation.to_dict(),
            "user_flow_validations": [flow.to_dict() for flow in self.user_flow_validations],
            "content_quality_assessment": self.content_quality_assessment.to_dict(),
            "quality_metrics": self.quality_metrics.to_dict(),
            "recommendations": [rec.to_dict() for rec in self.recommendations],
            "critical_issues": self.critical_issues,
            "blocking_issues": self.blocking_issues
        }


@dataclass
class ProductionReadinessAssessment:
    """
    Production readiness assessment for Quality Reviewer.
    """
    readiness_level: ProductionReadiness
    readiness_percentage: float
    deployment_approval: bool
    rollback_plan_required: bool
    go_live_conditions: List[str]
    pre_deployment_checklist: List[Dict[str, Any]]
    monitoring_requirements: List[str]
    success_criteria_for_launch: List[str]
    risk_mitigation_plan: Dict[str, Any]
    stakeholder_approval_needed: List[str]
    
    def is_ready_for_production(self) -> bool:
        """Check if ready for production deployment."""
        return (
            self.readiness_level in [ProductionReadiness.READY, ProductionReadiness.NEEDS_MINOR_FIXES] and
            self.deployment_approval and
            self.readiness_percentage >= 90.0
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "readiness_level": self.readiness_level.value,
            "readiness_percentage": self.readiness_percentage,
            "deployment_approval": self.deployment_approval,
            "rollback_plan_required": self.rollback_plan_required,
            "go_live_conditions": self.go_live_conditions,
            "pre_deployment_checklist": self.pre_deployment_checklist,
            "monitoring_requirements": self.monitoring_requirements,
            "success_criteria_for_launch": self.success_criteria_for_launch,
            "risk_mitigation_plan": self.risk_mitigation_plan,
            "stakeholder_approval_needed": self.stakeholder_approval_needed
        }


@dataclass
class DNAComplianceValidation:
    """
    DNA compliance validation results from QA perspective.
    """
    design_principles_validation: Dict[str, bool]
    architecture_compliance: Dict[str, bool]
    overall_compliance: bool
    compliance_score: float  # percentage
    non_compliant_areas: List[str]
    compliance_improvements: List[str]
    validation_timestamp: str
    anna_persona_alignment: bool
    municipal_context_validation: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "design_principles_validation": self.design_principles_validation,
            "architecture_compliance": self.architecture_compliance,
            "overall_compliance": self.overall_compliance,
            "compliance_score": self.compliance_score,
            "non_compliant_areas": self.non_compliant_areas,
            "compliance_improvements": self.compliance_improvements,
            "validation_timestamp": self.validation_timestamp,
            "anna_persona_alignment": self.anna_persona_alignment,
            "municipal_context_validation": self.municipal_context_validation
        }


@dataclass
class QATesterOutputContract:
    """
    Complete output contract for Quality Reviewer agent.
    """
    contract_version: str
    story_id: str
    source_agent: str
    target_agent: str
    dna_compliance: DNAComplianceValidation
    
    # Required files for Quality Reviewer
    deliverable_files: List[str]
    
    # Core QA results
    qa_validation_results: QAValidationResults
    production_readiness_assessment: ProductionReadinessAssessment
    final_quality_metrics: QualityMetrics
    stakeholder_signoff_requirements: List[str]
    
    # Output specifications for Quality Reviewer
    quality_reviewer_requirements: Dict[str, Any]
    validation_criteria: Dict[str, Any]
    
    # Quality gates for next phase
    quality_gates: List[str]
    handoff_criteria: List[str]
    
    # Metadata
    contract_timestamp: str
    qa_completion_timestamp: str
    next_phase_ready: bool
    
    def validate_output_completeness(self) -> Dict[str, Any]:
        """
        Validate that output contract is complete and ready for Quality Reviewer.
        
        Returns:
            Validation result
        """
        validation_errors = []
        missing_items = []
        
        # Check QA validation completeness
        if self.qa_validation_results.has_blocking_issues():
            validation_errors.append("Blocking issues prevent handoff to Quality Reviewer")
        
        # Check production readiness
        if not self.production_readiness_assessment.is_ready_for_production():
            validation_errors.append("Feature not ready for production deployment")
        
        # Check DNA compliance
        if not self.dna_compliance.overall_compliance:
            validation_errors.append("DNA compliance not achieved")
        
        # Check Anna persona compatibility
        anna_ready = self.qa_validation_results.persona_testing_results.meets_requirements({
            "min_satisfaction_score": 4.0,
            "min_completion_rate": 95.0,
            "max_completion_time": 10.0,
            "max_confusion_incidents": 2
        })
        
        if not anna_ready:
            validation_errors.append("Anna persona requirements not met")
        
        # Check accessibility compliance
        if not self.qa_validation_results.accessibility_validation.is_compliant("AA"):
            validation_errors.append("WCAG AA accessibility compliance not achieved")
        
        # Check required files
        if not self.deliverable_files:
            missing_items.append("deliverable_files")
        
        is_valid = len(validation_errors) == 0 and len(missing_items) == 0
        
        return {
            "is_valid": is_valid,
            "validation_errors": validation_errors,
            "missing_items": missing_items,
            "ready_for_quality_reviewer": is_valid,
            "completion_score": max(0, 100 - (len(validation_errors) * 15) - (len(missing_items) * 10))
        }
    
    def get_quality_summary(self) -> Dict[str, Any]:
        """
        Get summary of quality metrics for Quality Reviewer.
        
        Returns:
            Quality summary
        """
        return {
            "overall_quality_score": self.final_quality_metrics.overall_quality_score,
            "production_readiness": self.production_readiness_assessment.readiness_percentage,
            "anna_persona_satisfaction": self.qa_validation_results.persona_testing_results.satisfaction_score,
            "accessibility_compliance": self.qa_validation_results.accessibility_validation.compliance_percentage,
            "dna_compliance_score": self.dna_compliance.compliance_score,
            "critical_issues_count": len(self.qa_validation_results.critical_issues),
            "high_priority_recommendations": len([
                rec for rec in self.qa_validation_results.recommendations 
                if rec.priority in ["critical", "high"]
            ]),
            "deployment_recommendation": self.final_quality_metrics.deployment_recommendation,
            "next_phase_ready": self.next_phase_ready
        }
    
    def generate_executive_summary(self) -> str:
        """
        Generate executive summary for stakeholders.
        
        Returns:
            Executive summary text
        """
        quality_score = self.final_quality_metrics.overall_quality_score
        readiness = self.production_readiness_assessment.readiness_percentage
        anna_satisfaction = self.qa_validation_results.persona_testing_results.satisfaction_score
        
        summary = f"""
# Quality Assurance Executive Summary - {self.story_id}

## Overall Assessment
- **Quality Score:** {quality_score}/5.0
- **Production Readiness:** {readiness}%
- **Anna Persona Satisfaction:** {anna_satisfaction}/5.0
- **DNA Compliance:** {' Compliant' if self.dna_compliance.overall_compliance else 'L Non-compliant'}

## Key Findings
- **Accessibility:** {self.qa_validation_results.accessibility_validation.compliance_percentage}% WCAG AA compliance
- **User Experience:** {len(self.qa_validation_results.user_flow_validations)} user flows validated
- **Critical Issues:** {len(self.qa_validation_results.critical_issues)} identified
- **Recommendations:** {len(self.qa_validation_results.get_priority_recommendations())} high-priority items

## Deployment Recommendation
{self.final_quality_metrics.deployment_recommendation}

## Next Steps
{'Ready for Quality Reviewer approval' if self.next_phase_ready else 'Requires additional work before Quality Reviewer'}
        """
        
        return summary.strip()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "contract_version": self.contract_version,
            "story_id": self.story_id,
            "source_agent": self.source_agent,
            "target_agent": self.target_agent,
            "dna_compliance": self.dna_compliance.to_dict(),
            "deliverable_files": self.deliverable_files,
            "qa_validation_results": self.qa_validation_results.to_dict(),
            "production_readiness_assessment": self.production_readiness_assessment.to_dict(),
            "final_quality_metrics": self.final_quality_metrics.to_dict(),
            "stakeholder_signoff_requirements": self.stakeholder_signoff_requirements,
            "quality_reviewer_requirements": self.quality_reviewer_requirements,
            "validation_criteria": self.validation_criteria,
            "quality_gates": self.quality_gates,
            "handoff_criteria": self.handoff_criteria,
            "contract_timestamp": self.contract_timestamp,
            "qa_completion_timestamp": self.qa_completion_timestamp,
            "next_phase_ready": self.next_phase_ready
        }


# Utility functions for creating output contracts

def create_qa_recommendation(category: str, priority: str, issue: str, 
                           action: str, impact: str, affects_anna: bool = False,
                           affects_accessibility: bool = False) -> QARecommendation:
    """Create a standardized QA recommendation."""
    return QARecommendation(
        recommendation_id=f"{category}_{priority}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        category=category,
        priority=priority,
        issue_description=issue,
        recommended_action=action,
        expected_impact=impact,
        effort_estimate="medium",  # Default
        affects_anna_persona=affects_anna,
        affects_accessibility=affects_accessibility,
        implementation_guidance="Follow DigiNativa development standards"
    )


def calculate_production_readiness(qa_results: QAValidationResults) -> ProductionReadinessAssessment:
    """
    Calculate production readiness based on QA results.
    
    Args:
        qa_results: QA validation results
        
    Returns:
        Production readiness assessment
    """
    # Calculate readiness percentage
    readiness_factors = [
        qa_results.quality_metrics.overall_quality_score / 5 * 100,  # Overall quality
        qa_results.accessibility_validation.compliance_percentage,    # Accessibility
        qa_results.persona_testing_results.satisfaction_score / 5 * 100,  # Anna satisfaction
        100 if len(qa_results.critical_issues) == 0 else 0,          # No critical issues
        100 if len(qa_results.blocking_issues) == 0 else 0           # No blocking issues
    ]
    
    readiness_percentage = sum(readiness_factors) / len(readiness_factors)
    
    # Determine readiness level
    if readiness_percentage >= 95 and not qa_results.has_blocking_issues():
        readiness_level = ProductionReadiness.READY
        deployment_approval = True
    elif readiness_percentage >= 85 and len(qa_results.critical_issues) == 0:
        readiness_level = ProductionReadiness.NEEDS_MINOR_FIXES
        deployment_approval = False
    elif readiness_percentage >= 70:
        readiness_level = ProductionReadiness.NEEDS_MAJOR_FIXES
        deployment_approval = False
    else:
        readiness_level = ProductionReadiness.NOT_READY
        deployment_approval = False
    
    # Generate go-live conditions
    go_live_conditions = []
    if qa_results.critical_issues:
        go_live_conditions.extend([f"Resolve: {issue}" for issue in qa_results.critical_issues])
    if qa_results.accessibility_validation.compliance_percentage < 95:
        go_live_conditions.append("Achieve WCAG AA compliance")
    if qa_results.persona_testing_results.satisfaction_score < 4.0:
        go_live_conditions.append("Improve Anna persona satisfaction")
    
    return ProductionReadinessAssessment(
        readiness_level=readiness_level,
        readiness_percentage=round(readiness_percentage, 1),
        deployment_approval=deployment_approval,
        rollback_plan_required=True,  # Always required for DigiNativa
        go_live_conditions=go_live_conditions,
        pre_deployment_checklist=[
            {"item": "Performance testing completed", "status": "pending"},
            {"item": "Security scan clean", "status": "pending"},
            {"item": "Accessibility compliance verified", "status": "pending"},
            {"item": "Anna persona testing passed", "status": "pending"}
        ],
        monitoring_requirements=[
            "User satisfaction tracking",
            "Performance monitoring",
            "Error rate monitoring",
            "Accessibility compliance monitoring"
        ],
        success_criteria_for_launch=[
            "Anna persona satisfaction e 4.0",
            "Task completion rate e 95%",
            "Page load time d 3 seconds",
            "Error rate d 1%"
        ],
        risk_mitigation_plan={
            "rollback_trigger": "User satisfaction < 3.0 or error rate > 5%",
            "rollback_time": "< 15 minutes",
            "communication_plan": "Notify all stakeholders immediately"
        },
        stakeholder_approval_needed=[
            "Product Owner",
            "Technical Lead", 
            "Municipal Training Coordinator",
            "Accessibility Compliance Officer"
        ]
    )