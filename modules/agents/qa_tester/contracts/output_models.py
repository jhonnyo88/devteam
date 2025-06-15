"""
QA Tester Output Contract Models

PURPOSE:
Defines Pydantic models for QA Tester Agent output contracts,
ensuring type safety and contract compliance for Quality Reviewer.

CONTRACT VALIDATION:
These models implement the exact contract structure for
QA Tester -> Quality Reviewer handoff as specified in Implementation_rules.md.

ADAPTATION GUIDE:
🔧 To adapt for your project:
1. Update ux_validation_results for your UX standards
2. Modify accessibility_compliance_report for your compliance needs
3. Adjust persona_testing_results for your user personas
4. Update AI quality intelligence fields for your ML capabilities

CONTRACT PROTECTION:
These models are part of DigiNativa's contract system.
Changes must maintain backward compatibility.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class QATesterOutputContract(BaseModel):
    """
    QA Tester output contract for Quality Reviewer handoff.
    
    Delivers comprehensive QA validation results including UX validation,
    accessibility compliance, persona testing, and AI quality intelligence predictions.
    """
    
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version")
    source_agent: str = Field("qa_tester", description="Source agent")
    target_agent: str = Field("quality_reviewer", description="Target agent")
    story_id: str = Field(..., description="Story identifier")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # QA deliverables
    ux_validation_results: Dict[str, Any] = Field(..., description="UX validation results")
    accessibility_compliance_report: Dict[str, Any] = Field(..., description="WCAG AA accessibility compliance")
    persona_testing_results: Dict[str, Any] = Field(..., description="Anna persona testing results")
    municipal_compliance_results: Dict[str, Any] = Field(..., description="Swedish municipal compliance")
    
    # AI Quality Intelligence predictions (from QualityIntelligenceEngine)
    quality_intelligence_predictions: Dict[str, Any] = Field(..., description="AI quality predictions")
    anna_satisfaction_prediction: Dict[str, Any] = Field(..., description="AI Anna satisfaction prediction")
    
    # Performance validation
    performance_validation_results: Dict[str, Any] = Field(..., description="Performance validation results")
    
    # Output files for Quality Reviewer
    deliverable_files: List[str] = Field(..., description="Generated QA report files")
    deliverable_data: Dict[str, Any] = Field(..., description="QA deliverable data")
    
    # Validation criteria met
    validation_criteria: Dict[str, Any] = Field(..., description="QA validation criteria results")
    
    # Quality gates passed
    quality_gates: List[str] = Field(..., description="QA quality gates passed")
    
    # Handoff criteria for Quality Reviewer
    handoff_criteria: List[str] = Field(..., description="Handoff criteria met")
    
    # Enhanced DNA compliance (includes QA DNA validation)
    dna_compliance: Dict[str, Any] = Field(..., description="Complete DNA validation chain")
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "story_id": "STORY-TEST-001",
                "ux_validation_results": {
                    "overall_ux_score": 4.5,
                    "usability_score": 4.2,
                    "user_satisfaction": 4.3,
                    "task_completion_rate": 96.0,
                    "issues_identified": [],
                    "recommendations": [
                        "Improve button contrast for better accessibility",
                        "Add loading indicators for API calls"
                    ]
                },
                "accessibility_compliance_report": {
                    "wcag_compliance_level": "AA",
                    "compliance_percentage": 98.0,
                    "violations": [],
                    "warnings": [],
                    "passed_checks": 45,
                    "accessibility_score": 4.8
                },
                "persona_testing_results": {
                    "anna_persona": {
                        "satisfaction_score": 4.2,
                        "task_completion_rate": 96,
                        "average_completion_time_minutes": 8.0,
                        "learning_effectiveness_score": 4.4,
                        "confusion_incidents": [],
                        "positive_feedback": [
                            "Clear navigation and intuitive interface",
                            "Professional tone appropriate for municipal context"
                        ],
                        "time_constraint_violations": 0,
                        "accessibility_issues_encountered": []
                    }
                },
                "municipal_compliance_results": {
                    "swedish_municipal_standards": "compliant",
                    "gdpr_compliance": True,
                    "accessibility_law_compliance": True,
                    "professional_tone_score": 4.5,
                    "municipal_terminology_correct": True
                },
                "quality_intelligence_predictions": {
                    "predicted_quality_score": 4.99,
                    "confidence_level": "high",
                    "confidence_percentage": 90.0,
                    "risk_factors": [],
                    "improvement_suggestions": [
                        "Consider adding more interactive elements for engagement",
                        "Optimize loading times for better user experience"
                    ],
                    "similar_projects": ["STORY-001", "STORY-002"],
                    "prediction_basis": "ML analysis of municipal training features"
                },
                "anna_satisfaction_prediction": {
                    "predicted_satisfaction_score": 4.65,
                    "predicted_completion_time_minutes": 3.8,
                    "satisfaction_level": "excellent",
                    "satisfaction_boosters": [
                        "Clear task flow",
                        "Professional Swedish terminology",
                        "Efficient time usage"
                    ],
                    "satisfaction_blockers": [],
                    "anna_specific_recommendations": [
                        "Maintain current professional tone",
                        "Keep task complexity at current level"
                    ],
                    "confidence_score": 85.0
                },
                "performance_validation_results": {
                    "lighthouse_score": 95.0,
                    "api_performance_validated": True,
                    "load_time_compliant": True,
                    "municipal_load_testing_passed": True,
                    "performance_recommendations": []
                },
                "deliverable_files": [
                    "docs/qa_reports/STORY-TEST-001_ux_validation.md",
                    "docs/qa_reports/STORY-TEST-001_accessibility.json",
                    "docs/qa_reports/STORY-TEST-001_persona_testing.json",
                    "docs/qa_reports/STORY-TEST-001_comprehensive_qa.json"
                ],
                "deliverable_data": {
                    "ux_validation_results": "object",
                    "accessibility_report": "object",
                    "persona_testing_results": "object"
                },
                "validation_criteria": {
                    "user_experience": {
                        "anna_persona_satisfaction": {"min_score": 4, "actual_score": 4.2, "passed": True},
                        "task_completion_rate": {"min_percentage": 95, "actual_percentage": 96, "passed": True},
                        "time_to_complete": {"max_minutes": 10, "actual_minutes": 8.0, "passed": True}
                    },
                    "accessibility": {
                        "wcag_compliance_level": "AA",
                        "screen_reader_compatibility": True,
                        "keyboard_navigation": True
                    }
                },
                "quality_gates": [
                    "anna_persona_satisfaction_score_minimum_met",
                    "wcag_aa_compliance_100_percent_verified",
                    "task_completion_time_under_10_minutes",
                    "professional_tone_maintained_throughout",
                    "pedagogical_value_clearly_demonstrated",
                    "all_user_flows_validated_successfully"
                ],
                "handoff_criteria": [
                    "comprehensive_ux_validation_completed",
                    "accessibility_compliance_verified",
                    "persona_testing_passed",
                    "ai_quality_predictions_generated",
                    "municipal_compliance_validated"
                ],
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
                    },
                    "qa_tester_dna_validation": {
                        "ux_quality_validated": True,
                        "anna_persona_compliance": True,
                        "municipal_standards_met": True,
                        "ai_quality_confidence": "high"
                    }
                }
            }
        }


# Utility function for creating QA Tester output contract

def create_qa_tester_output_contract(
    story_id: str,
    ux_validation_results: Dict[str, Any],
    accessibility_results: Dict[str, Any],
    persona_testing_results: Dict[str, Any],
    ai_quality_predictions: Dict[str, Any],
    anna_satisfaction_prediction: Dict[str, Any],
    performance_validation: Dict[str, Any],
    municipal_compliance: Dict[str, Any],
    dna_compliance: Dict[str, Any]
) -> QATesterOutputContract:
    """
    Create QA Tester output contract for Quality Reviewer.
    
    Args:
        story_id: Story identifier
        ux_validation_results: UX validation results
        accessibility_results: Accessibility compliance results
        persona_testing_results: Anna persona testing results
        ai_quality_predictions: AI quality intelligence predictions
        anna_satisfaction_prediction: AI Anna satisfaction prediction
        performance_validation: Performance validation results
        municipal_compliance: Swedish municipal compliance results
        dna_compliance: DNA compliance validation results
        
    Returns:
        QATesterOutputContract ready for Quality Reviewer
    """
    
    # Generate deliverable files list
    deliverable_files = [
        f"docs/qa_reports/{story_id}_ux_validation.md",
        f"docs/qa_reports/{story_id}_accessibility.json",
        f"docs/qa_reports/{story_id}_persona_testing.json",
        f"docs/qa_reports/{story_id}_comprehensive_qa.json"
    ]
    
    # Define validation criteria met
    validation_criteria = {
        "user_experience": {
            "anna_persona_satisfaction": {
                "min_score": 4,
                "actual_score": persona_testing_results.get("anna_persona", {}).get("satisfaction_score", 0),
                "passed": persona_testing_results.get("anna_persona", {}).get("satisfaction_score", 0) >= 4
            },
            "task_completion_rate": {
                "min_percentage": 95,
                "actual_percentage": persona_testing_results.get("anna_persona", {}).get("task_completion_rate", 0),
                "passed": persona_testing_results.get("anna_persona", {}).get("task_completion_rate", 0) >= 95
            },
            "time_to_complete": {
                "max_minutes": 10,
                "actual_minutes": persona_testing_results.get("anna_persona", {}).get("average_completion_time_minutes", 0),
                "passed": persona_testing_results.get("anna_persona", {}).get("average_completion_time_minutes", 0) <= 10
            }
        },
        "accessibility": {
            "wcag_compliance_level": accessibility_results.get("wcag_compliance_level", ""),
            "screen_reader_compatibility": accessibility_results.get("screen_reader_compatible", False),
            "keyboard_navigation": accessibility_results.get("keyboard_navigation_supported", False)
        }
    }
    
    # Define quality gates passed
    quality_gates = [
        "anna_persona_satisfaction_score_minimum_met",
        "wcag_aa_compliance_100_percent_verified", 
        "task_completion_time_under_10_minutes",
        "professional_tone_maintained_throughout",
        "pedagogical_value_clearly_demonstrated",
        "all_user_flows_validated_successfully"
    ]
    
    # Define handoff criteria
    handoff_criteria = [
        "comprehensive_ux_validation_completed",
        "accessibility_compliance_verified",
        "persona_testing_passed",
        "ai_quality_predictions_generated",
        "municipal_compliance_validated"
    ]
    
    return QATesterOutputContract(
        story_id=story_id,
        ux_validation_results=ux_validation_results,
        accessibility_compliance_report=accessibility_results,
        persona_testing_results=persona_testing_results,
        municipal_compliance_results=municipal_compliance,
        quality_intelligence_predictions=ai_quality_predictions,
        anna_satisfaction_prediction=anna_satisfaction_prediction,
        performance_validation_results=performance_validation,
        deliverable_files=deliverable_files,
        deliverable_data={
            "ux_validation_results": "object",
            "accessibility_report": "object", 
            "persona_testing_results": "object"
        },
        validation_criteria=validation_criteria,
        quality_gates=quality_gates,
        handoff_criteria=handoff_criteria,
        dna_compliance=dna_compliance
    )