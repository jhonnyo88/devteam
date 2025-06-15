"""
Quality Reviewer Input Contract Models.

Pydantic models for incoming contracts from QA Tester agent to Quality Reviewer.
These models ensure type safety and validation for final quality review process.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class QualityReviewerInputContract(BaseModel):
    """
    Input contract for Quality Reviewer agent from QA Tester.
    
    This contract contains all quality validation results from QA testing
    that need final review before deployment approval.
    """
    
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version for compatibility")
    source_agent: str = Field("qa_tester", description="Source agent that created this contract")
    target_agent: str = Field("quality_reviewer", description="Target agent to receive this contract")
    timestamp: str = Field(
        default_factory=lambda: datetime.now().isoformat(), 
        description="Contract creation timestamp"
    )
    
    # Story identification
    story_id: str = Field(..., description="Unique story identifier for tracking")
    
    # QA validation results from QA Tester
    ux_validation_results: Dict[str, Any] = Field(
        ..., 
        description="Complete UX validation results including user flows and Anna persona testing"
    )
    
    accessibility_compliance_report: Dict[str, Any] = Field(
        ..., 
        description="WCAG AA compliance validation results for Swedish municipal standards"
    )
    
    persona_testing_results: Dict[str, Any] = Field(
        ..., 
        description="Anna persona testing results with completion times and satisfaction scores"
    )
    
    municipal_compliance_results: Dict[str, Any] = Field(
        ..., 
        description="Swedish municipal compliance validation (GDPR, accessibility law, etc.)"
    )
    
    # AI Quality Intelligence predictions from QA Tester
    quality_intelligence_predictions: Dict[str, Any] = Field(
        ..., 
        description="AI-powered quality predictions and insights from QualityIntelligenceEngine"
    )
    
    anna_satisfaction_prediction: Dict[str, Any] = Field(
        ..., 
        description="AI prediction of Anna persona satisfaction with completion time estimates"
    )
    
    # Performance validation results
    performance_validation_results: Dict[str, Any] = Field(
        ..., 
        description="Performance testing results including API response times and Lighthouse scores"
    )
    
    # Test coverage and quality metrics
    test_results: Dict[str, Any] = Field(
        ..., 
        description="Complete test suite results from Test Engineer including coverage analysis"
    )
    
    # Code quality metrics
    code_quality_metrics: Dict[str, Any] = Field(
        ..., 
        description="Code quality analysis including TypeScript errors and complexity scores"
    )
    
    # DNA compliance chain from all previous agents
    dna_compliance: Dict[str, Any] = Field(
        ..., 
        description="Complete DNA validation results from PM, Game Designer, Developer, Test Engineer, and QA Tester"
    )
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "contract_version": "1.0",
                "source_agent": "qa_tester",
                "target_agent": "quality_reviewer",
                "story_id": "STORY-QR-001",
                "ux_validation_results": {
                    "user_flows_validated": True,
                    "completion_rate": 96.5,
                    "user_satisfaction_score": 4.6
                },
                "accessibility_compliance_report": {
                    "wcag_aa_compliance": True,
                    "compliance_percentage": 98.5,
                    "violations": []
                },
                "persona_testing_results": {
                    "anna_persona_satisfaction": 4.7,
                    "completion_time_minutes": 8.2,
                    "task_success_rate": 95.0
                },
                "municipal_compliance_results": {
                    "gdpr_compliant": True,
                    "swedish_accessibility_law_compliant": True,
                    "professional_tone_validated": True
                },
                "quality_intelligence_predictions": {
                    "predicted_quality_score": 4.8,
                    "confidence_level": 92.0,
                    "risk_factors": []
                },
                "anna_satisfaction_prediction": {
                    "predicted_satisfaction": 4.6,
                    "predicted_completion_time_minutes": 8.5,
                    "confidence_percentage": 89.0
                },
                "performance_validation_results": {
                    "lighthouse_score": 94,
                    "api_response_time_ms": 145,
                    "page_load_time_ms": 1200
                },
                "test_results": {
                    "coverage_percentage": 97.5,
                    "tests_passed": 48,
                    "total_tests": 48
                },
                "code_quality_metrics": {
                    "typescript_errors": 0,
                    "eslint_violations": 0,
                    "complexity_score": 2.1
                },
                "dna_compliance": {
                    "overall_dna_compliant": True,
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
                }
            }
        }