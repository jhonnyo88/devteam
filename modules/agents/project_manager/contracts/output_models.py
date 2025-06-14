"""
Project Manager Output Contract Models

PURPOSE:
Defines Pydantic models for Project Manager Agent output contracts,
ensuring type safety and contract compliance for downstream agents.

CONTRACT VALIDATION:
These models implement the exact contract structure specified in
Implementation_rules.md for Project Manager -> Game Designer handoff.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ProjectManagerOutputContract(BaseModel):
    """
    Project Manager output contract for Game Designer handoff.
    
    This model ensures the PM -> Game Designer contract compliance
    as specified in Implementation_rules.md.
    """
    
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version")
    source_agent: str = Field("project_manager", description="Source agent type")
    target_agent: str = Field("game_designer", description="Target agent type") 
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Story identification
    story_id: str = Field(..., description="Unique story identifier")
    github_issue_url: Optional[str] = Field(None, description="Source GitHub issue URL")
    
    # Story breakdown
    story_title: str = Field(..., description="Story title")
    story_description: str = Field(..., description="Detailed story description")
    acceptance_criteria: List[str] = Field(..., description="List of acceptance criteria")
    
    # Technical analysis
    complexity_assessment: Dict[str, Any] = Field(..., description="Complexity analysis")
    estimated_effort_hours: float = Field(..., description="Estimated effort in hours")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    
    # Dependencies and relationships
    dependencies: List[str] = Field(default_factory=list, description="Story dependencies")
    related_stories: List[str] = Field(default_factory=list, description="Related stories")
    
    # Priority and timeline
    priority: str = Field(..., description="Story priority level")
    target_deadline: Optional[str] = Field(None, description="Target completion deadline")
    
    # UX requirements for Game Designer
    ux_requirements: Dict[str, Any] = Field(..., description="UX design requirements")
    user_personas: List[str] = Field(default_factory=list, description="Target user personas")
    accessibility_requirements: List[str] = Field(default_factory=list, description="Accessibility needs")
    
    # Municipal context
    municipal_context: Dict[str, Any] = Field(..., description="Swedish municipal context")
    compliance_requirements: List[str] = Field(default_factory=list, description="Compliance needs")
    
    # DNA compliance validation
    dna_compliance: Dict[str, Any] = Field(..., description="DNA principle validation results")
    
    # Quality gates
    quality_gates: Dict[str, Any] = Field(..., description="Quality validation results")
    
    # Handoff instructions
    handoff_notes: str = Field(..., description="Instructions for Game Designer")
    next_steps: List[str] = Field(..., description="Recommended next steps")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "contract_version": "1.0",
                "source_agent": "project_manager",
                "target_agent": "game_designer",
                "story_id": "story-2024-001",
                "story_title": "User Registration System",
                "story_description": "Implement user registration for municipal training platform",
                "acceptance_criteria": [
                    "Users can register with email and password",
                    "Email verification required",
                    "GDPR compliance maintained"
                ],
                "complexity_assessment": {
                    "technical_complexity": 3,
                    "ux_complexity": 2,
                    "integration_complexity": 2
                },
                "estimated_effort_hours": 24.0,
                "priority": "high",
                "ux_requirements": {
                    "max_completion_time_minutes": 5,
                    "accessibility_level": "WCAG AA",
                    "mobile_support": True
                },
                "municipal_context": {
                    "target_municipality": "svenska kommuner",
                    "gdpr_compliance": True,
                    "swedish_language": True
                },
                "dna_compliance": {
                    "pedagogical_value": {"score": 4, "validated": True},
                    "time_respect": {"score": 5, "validated": True},
                    "professional_tone": {"score": 4, "validated": True}
                },
                "quality_gates": {
                    "story_clarity": True,
                    "acceptance_criteria_complete": True,
                    "technical_feasibility": True
                },
                "handoff_notes": "Focus on simplicity and municipal user experience",
                "next_steps": ["Create wireframes", "Design component mapping"]
            }
        }


class ProjectManagerLearningDataContract(BaseModel):
    """
    Contract for Project Manager learning data and insights.
    
    Used for ML model training and continuous improvement.
    """
    
    story_id: str = Field(..., description="Story identifier")
    
    # Historical data
    actual_completion_time: Optional[float] = Field(None, description="Actual completion time in hours")
    complexity_accuracy: Optional[float] = Field(None, description="Complexity prediction accuracy")
    success_factors: List[str] = Field(default_factory=list, description="Success factors identified")
    challenges_encountered: List[str] = Field(default_factory=list, description="Challenges during development")
    
    # Quality metrics
    client_satisfaction: Optional[float] = Field(None, description="Client satisfaction score")
    dna_compliance_score: Optional[float] = Field(None, description="Final DNA compliance score")
    revision_count: Optional[int] = Field(None, description="Number of revisions required")
    
    # Learning insights
    lessons_learned: List[str] = Field(default_factory=list, description="Key lessons learned")
    improvement_recommendations: List[str] = Field(default_factory=list, description="Recommendations for future")
    
    # Metadata
    completion_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "story_id": "story-2024-001",
                "actual_completion_time": 26.5,
                "complexity_accuracy": 0.85,
                "success_factors": ["Clear requirements", "Good stakeholder communication"],
                "client_satisfaction": 4.5,
                "dna_compliance_score": 4.2,
                "revision_count": 1,
                "lessons_learned": ["Municipal users prefer step-by-step guidance"]
            }
        }


class ProjectManagerStakeholderContract(BaseModel):
    """
    Contract for stakeholder interaction and relationship management.
    """
    
    stakeholder_id: str = Field(..., description="Stakeholder identifier")
    interaction_type: str = Field(..., description="Type of interaction")
    
    # Communication data
    message_sent: str = Field(..., description="Message content sent")
    response_received: Optional[str] = Field(None, description="Response received")
    response_time_hours: Optional[float] = Field(None, description="Response time in hours")
    
    # Sentiment and satisfaction
    stakeholder_satisfaction: Optional[float] = Field(None, description="Satisfaction score")
    communication_effectiveness: Optional[float] = Field(None, description="Communication effectiveness")
    
    # Learning data
    preferences_learned: Dict[str, Any] = Field(default_factory=dict, description="Learned preferences")
    approval_decision: Optional[str] = Field(None, description="Approval decision if applicable")
    
    # Metadata
    interaction_timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "stakeholder_id": "anna-kommun-001",
                "interaction_type": "approval_request",
                "message_sent": "Request for approval of user registration feature",
                "response_time_hours": 18.5,
                "stakeholder_satisfaction": 4.2,
                "approval_decision": "approved_with_suggestions"
            }
        }