"""
Quality Reviewer Output Contract Models.

Pydantic models for outgoing contracts from Quality Reviewer agent.
These models define the final approval decision and deployment instructions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class ApprovalDecision(str, Enum):
    """Final approval decision types."""
    APPROVED = "approved"
    REVISION_REQUIRED = "revision_required"
    REJECTED = "rejected"


class QualityReviewerOutputContract(BaseModel):
    """
    Output contract from Quality Reviewer agent for final deployment or revision.
    
    This contract contains the final approval decision, quality assessment,
    client communication data, and next steps for the story.
    """
    
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version for compatibility")
    source_agent: str = Field("quality_reviewer", description="Source agent that created this contract")
    target_agent: str = Field(
        ..., 
        description="Target agent (deployment for approved, developer for revision)"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(), 
        description="Contract creation timestamp"
    )
    
    # Story identification
    story_id: str = Field(..., description="Unique story identifier for tracking")
    
    # Final approval decision
    approval_decision: ApprovalDecision = Field(
        ..., 
        description="Final approval decision: approved, revision_required, or rejected"
    )
    
    quality_score: float = Field(
        ..., 
        ge=0.0, 
        le=100.0, 
        description="Overall quality score (0-100) for the complete story implementation"
    )
    
    approval_reasoning: str = Field(
        ..., 
        min_length=10, 
        description="Detailed reasoning for the approval decision"
    )
    
    # Client communication data from ClientCommunicator
    client_communication_data: Dict[str, Any] = Field(
        ..., 
        description="Complete client communication package including GitHub approval requests and Swedish municipal reports"
    )
    
    # GitHub approval workflow data
    github_approval_request: Optional[Dict[str, Any]] = Field(
        None, 
        description="GitHub approval request data for project owner (when approved)"
    )
    
    staging_notification: Optional[Dict[str, Any]] = Field(
        None, 
        description="Staging environment notification for client testing (when approved)"
    )
    
    quality_report: Dict[str, Any] = Field(
        ..., 
        description="Professional Swedish municipal quality report"
    )
    
    # Deployment instructions (for approved stories)
    deployment_instructions: Optional[Dict[str, Any]] = Field(
        None, 
        description="Complete deployment instructions and environment configuration"
    )
    
    deployment_environment: Optional[str] = Field(
        None, 
        description="Target deployment environment (staging/production)"
    )
    
    monitoring_requirements: Optional[List[str]] = Field(
        None, 
        description="Post-deployment monitoring requirements"
    )
    
    # Revision requirements (for stories needing improvements)
    revision_requirements: Optional[Dict[str, Any]] = Field(
        None, 
        description="Specific requirements for story revision including target agent and issues to address"
    )
    
    quality_issues: Optional[List[Dict[str, Any]]] = Field(
        None, 
        description="Detailed quality issues that need to be addressed"
    )
    
    improvement_recommendations: Optional[List[str]] = Field(
        None, 
        description="Specific recommendations for improving the story implementation"
    )
    
    estimated_revision_time_days: Optional[float] = Field(
        None, 
        description="Estimated time needed for revisions in working days"
    )
    
    # Final DNA compliance summary
    dna_compliance: Dict[str, Any] = Field(
        ..., 
        description="Final DNA validation summary from complete story review including all agent validations"
    )
    
    final_dna_validation: Dict[str, Any] = Field(
        ..., 
        description="Quality Reviewer final DNA validation results"
    )
    
    # Quality metrics summary
    quality_breakdown: Dict[str, Any] = Field(
        ..., 
        description="Detailed breakdown of quality scores across all dimensions"
    )
    
    performance_summary: Dict[str, Any] = Field(
        ..., 
        description="Performance validation summary including API times and Lighthouse scores"
    )
    
    accessibility_summary: Dict[str, Any] = Field(
        ..., 
        description="Accessibility compliance summary for Swedish municipal standards"
    )
    
    # Next actions and follow-up
    next_actions: List[str] = Field(
        ..., 
        description="Clear next actions for project team based on approval decision"
    )
    
    follow_up_date: Optional[str] = Field(
        None, 
        description="Suggested follow-up date for revision review or deployment monitoring"
    )
    
    # Team learning and feedback
    lessons_learned: List[str] = Field(
        default_factory=list, 
        description="Key lessons learned from this story for team improvement"
    )
    
    process_improvements: List[str] = Field(
        default_factory=list, 
        description="Suggested process improvements based on this story review"
    )
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "contract_version": "1.0",
                "source_agent": "quality_reviewer",
                "target_agent": "deployment",
                "story_id": "STORY-QR-001",
                "approval_decision": "approved",
                "quality_score": 94.5,
                "approval_reasoning": "Story meets all quality standards for Swedish municipal deployment. Excellent Anna persona satisfaction, full WCAG AA compliance, and superior performance metrics.",
                "client_communication_data": {
                    "communication_type": "approval_request",
                    "approval_request": {
                        "title": "Godkännande begärs: Funktionalitet QR-001 (Kvalitetspoäng: 94.5/100)",
                        "body": "Kvalitetsgranskningsteamet rekommenderar GODKÄNNANDE för driftsättning."
                    },
                    "quality_report": {
                        "report_id": "QR-STORY-QR-001-20241215",
                        "overall_assessment": "Utmärkt kvalitet för svenska kommunala miljöer"
                    }
                },
                "github_approval_request": {
                    "title": "Godkännande begärs: Funktionalitet QR-001 (Kvalitetspoäng: 94.5/100)",
                    "labels": ["approval-request", "quality-reviewed", "municipal-ready"]
                },
                "staging_notification": {
                    "title": "Testversion redo: Funktionalitet QR-001 (Kvalitet: 94.5/100)",
                    "staging_url": "https://staging.digitativa.se/STORY-QR-001"
                },
                "quality_report": {
                    "report_id": "QR-STORY-QR-001-20241215",
                    "overall_score": 94.5,
                    "deployment_ready": True,
                    "compliance_level": "excellent"
                },
                "deployment_instructions": {
                    "environment": "production",
                    "deployment_strategy": "blue_green",
                    "rollback_plan": "automatic_on_error"
                },
                "deployment_environment": "production",
                "monitoring_requirements": [
                    "API response time monitoring (<200ms)",
                    "User satisfaction tracking",
                    "Accessibility compliance monitoring"
                ],
                "dna_compliance": {
                    "overall_dna_compliant": True,
                    "final_dna_score": 4.7,
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
                "final_dna_validation": {
                    "overall_dna_compliant": True,
                    "final_user_journey_compliant": True,
                    "client_communication_compliant": True,
                    "deployment_ready": True,
                    "dna_compliance_score": 4.7
                },
                "quality_breakdown": {
                    "test_quality": 97.5,
                    "performance": 94.0,
                    "accessibility": 96.5,
                    "user_experience": 92.0,
                    "code_quality": 89.5,
                    "dna_compliance": 94.0
                },
                "performance_summary": {
                    "lighthouse_score": 94,
                    "api_response_time_ms": 145,
                    "meets_performance_requirements": True
                },
                "accessibility_summary": {
                    "wcag_aa_compliance": True,
                    "compliance_percentage": 96.5,
                    "swedish_standards_met": True
                },
                "next_actions": [
                    "Deploy to production environment",
                    "Monitor performance metrics",
                    "Collect user feedback from municipal coordinators"
                ],
                "follow_up_date": "2024-12-22",
                "lessons_learned": [
                    "AI quality predictions proved accurate",
                    "Anna persona testing identified key usability insights"
                ],
                "process_improvements": [
                    "Earlier accessibility validation in Game Designer phase",
                    "Enhanced municipal context validation"
                ]
            }
        }