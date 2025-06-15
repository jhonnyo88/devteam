"""
Game Designer Input Contract Models

PURPOSE:
Defines Pydantic models for Game Designer Agent input contracts,
ensuring type safety and contract compliance from Project Manager handoff.

CONTRACT VALIDATION:
These models implement the exact contract structure for receiving
Project Manager output according to Implementation_rules.md.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class GameDesignerInputContract(BaseModel):
    """
    Game Designer input contract for Project Manager handoff.
    
    This model ensures the PM -> Game Designer contract compliance
    and validates all required UX design inputs.
    """
    
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version")
    source_agent: str = Field("project_manager", description="Source agent type")
    target_agent: str = Field("game_designer", description="Target agent type")
    story_id: str = Field(..., description="Unique story identifier")
    timestamp: Optional[str] = Field(None, description="Contract creation timestamp")
    
    # Story context from PM
    story_title: str = Field(..., description="Story title")
    story_description: str = Field(..., description="Detailed story description")
    acceptance_criteria: List[str] = Field(..., description="List of acceptance criteria")
    
    # UX requirements from PM analysis
    ux_requirements: Dict[str, Any] = Field(..., description="UX design requirements")
    user_personas: List[str] = Field(default_factory=list, description="Target user personas (Anna)")
    accessibility_requirements: List[str] = Field(..., description="Accessibility needs (WCAG AA)")
    
    # Municipal context for Swedish public sector
    municipal_context: Dict[str, Any] = Field(..., description="Swedish municipal context")
    compliance_requirements: List[str] = Field(default_factory=list, description="Compliance needs")
    
    # Technical constraints
    complexity_assessment: Dict[str, Any] = Field(..., description="Complexity analysis from PM")
    estimated_effort_hours: float = Field(..., description="Estimated effort in hours")
    priority: str = Field(..., description="Story priority level")
    target_deadline: Optional[str] = Field(None, description="Target completion deadline")
    
    # Learning objectives and pedagogical requirements
    learning_objectives: List[str] = Field(default_factory=list, description="Educational objectives")
    time_constraint_minutes: int = Field(10, description="Maximum completion time for users")
    
    # Dependencies and constraints
    dependencies: List[str] = Field(default_factory=list, description="Story dependencies")
    risk_factors: List[str] = Field(default_factory=list, description="Identified risk factors")
    
    # DNA compliance from PM validation
    dna_compliance: Dict[str, Any] = Field(..., description="DNA principle validation results")
    
    # Quality context
    quality_gates: Dict[str, Any] = Field(..., description="Quality validation results")
    handoff_notes: str = Field(..., description="Instructions from Project Manager")
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
                "story_id": "STORY-GH-123",
                "story_title": "User Registration System",
                "story_description": "Implement user registration for municipal training platform",
                "acceptance_criteria": [
                    "Users can register with email and password",
                    "Email verification required",
                    "GDPR compliance maintained"
                ],
                "ux_requirements": {
                    "max_completion_time_minutes": 10,
                    "accessibility_level": "WCAG AA",
                    "mobile_support": True,
                    "component_library": "shadcn_ui",
                    "design_system": "kenney_ui_assets"
                },
                "user_personas": ["Anna"],
                "accessibility_requirements": [
                    "WCAG 2.1 Level AA compliance",
                    "Screen reader compatibility",
                    "Keyboard navigation support",
                    "High contrast mode support"
                ],
                "municipal_context": {
                    "target_municipality": "svenska kommuner",
                    "gdpr_compliance": True,
                    "swedish_language": True,
                    "government_design_standards": True,
                    "professional_tone_required": True
                },
                "compliance_requirements": [
                    "GDPR data protection",
                    "Swedish accessibility law (DOS)",
                    "Municipal IT security standards"
                ],
                "complexity_assessment": {
                    "technical_complexity": 3,
                    "ux_complexity": 2,
                    "integration_complexity": 2
                },
                "estimated_effort_hours": 24.0,
                "priority": "high",
                "learning_objectives": [
                    "Understand user registration process",
                    "Learn GDPR compliance requirements",
                    "Practice password security"
                ],
                "time_constraint_minutes": 10,
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
                        "simplicity_first": True
                    }
                },
                "quality_gates": {
                    "story_clarity": True,
                    "acceptance_criteria_complete": True,
                    "technical_feasibility": True
                },
                "handoff_notes": "Focus on simplicity and municipal user experience. Ensure Anna persona can complete registration in under 10 minutes.",
                "next_steps": [
                    "Create wireframes for registration flow",
                    "Map components to Shadcn/UI library",
                    "Design pedagogical game mechanics",
                    "Validate accessibility requirements"
                ]
            }
        }


class GameDesignerValidationContract(BaseModel):
    """
    Contract for Game Designer validation requirements and constraints.
    
    Used for validating UX designs against DigiNativa standards.
    """
    
    story_id: str = Field(..., description="Story identifier")
    
    # UX validation requirements
    design_validation_rules: Dict[str, Any] = Field(..., description="Design validation rules")
    component_library_requirements: Dict[str, Any] = Field(..., description="Component library constraints")
    accessibility_standards: Dict[str, Any] = Field(..., description="Accessibility validation standards")
    
    # Municipal UX standards
    municipal_design_standards: Dict[str, Any] = Field(..., description="Swedish municipal design standards")
    professional_tone_requirements: Dict[str, Any] = Field(..., description="Professional tone standards")
    
    # Game mechanics constraints
    pedagogical_effectiveness_requirements: Dict[str, Any] = Field(..., description="Learning effectiveness requirements")
    engagement_standards: Dict[str, Any] = Field(..., description="User engagement standards")
    
    # Performance constraints
    performance_budget: Dict[str, Any] = Field(..., description="Performance requirements")
    technical_constraints: Dict[str, Any] = Field(..., description="Technical limitations")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "story_id": "STORY-GH-123",
                "design_validation_rules": {
                    "max_cognitive_load": 6,
                    "max_ui_elements_per_screen": 12,
                    "required_color_contrast": 4.5
                },
                "component_library_requirements": {
                    "primary_library": "shadcn_ui",
                    "asset_library": "kenney_ui",
                    "library_compliance": "100_percent"
                },
                "municipal_design_standards": {
                    "swedish_government_branding": True,
                    "professional_color_scheme": True,
                    "municipal_typography": True
                },
                "pedagogical_effectiveness_requirements": {
                    "min_learning_objectives_coverage": 0.8,
                    "min_pedagogical_score": 4.0,
                    "assessment_opportunities_required": True
                }
            }
        }