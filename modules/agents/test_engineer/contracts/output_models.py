"""
Output contract models for TestEngineerAgent.

PURPOSE:
Defines Pydantic models for validating output contracts to QA Tester
according to Implementation_rules.md specifications.

CRITICAL VALIDATION:
- Test results structure compliance
- Quality gate validation
- Coverage metrics verification
- QA Tester input requirements
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class IntegrationTestSuite(BaseModel):
    """Integration test suite results."""
    
    story_id: str = Field(..., description="Story identifier")
    test_type: str = Field("integration", description="Test type")
    total_test_cases: int = Field(..., ge=0, description="Total test cases")
    coverage_percent: float = Field(..., ge=0, le=100, description="Coverage percentage")
    all_tests_passing: bool = Field(True, description="All tests passing status")


class E2ETestSuite(BaseModel):
    """End-to-end test suite results."""
    
    story_id: str = Field(..., description="Story identifier")
    test_type: str = Field("end_to_end", description="Test type")
    total_scenarios: int = Field(..., ge=0, description="Total test scenarios")
    coverage_percent: float = Field(..., ge=0, le=100, description="Coverage percentage")
    all_tests_passing: bool = Field(True, description="All tests passing status")


class PerformanceTestResults(BaseModel):
    """Performance test results."""
    
    story_id: str = Field(..., description="Story identifier")
    average_api_response_time_ms: float = Field(..., le=200, description="Average API response time")
    lighthouse_score: int = Field(..., ge=90, le=100, description="Lighthouse performance score")
    bundle_size_kb: float = Field(..., le=500, description="Bundle size in KB")
    performance_budget_met: bool = Field(True, description="Performance budget compliance")


class SecurityScanResults(BaseModel):
    """Security scan results."""
    
    story_id: str = Field(..., description="Story identifier")
    critical_vulnerabilities: List[Dict[str, Any]] = Field(default=[], description="Critical vulnerabilities")
    high_vulnerabilities: List[Dict[str, Any]] = Field(default=[], description="High severity vulnerabilities")
    medium_vulnerabilities: List[Dict[str, Any]] = Field(default=[], description="Medium severity vulnerabilities")
    security_compliance_met: bool = Field(True, description="Security compliance status")


class CoverageReport(BaseModel):
    """Test coverage report."""
    
    story_id: str = Field(..., description="Story identifier")
    overall_coverage_percent: float = Field(..., ge=90, le=100, description="Overall coverage percentage")
    coverage_quality_met: bool = Field(True, description="Coverage quality requirements met")


class QualityGate(str, Enum):
    """Quality gates for QA Tester validation."""
    
    ALL_TESTS_PASSING = "all_automated_tests_passing"
    PERFORMANCE_VALIDATED = "performance_requirements_validated"
    SECURITY_VERIFIED = "security_compliance_verified"
    ACCESSIBILITY_MET = "accessibility_standards_met"
    COVERAGE_ACHIEVED = "test_coverage_thresholds_met"


class HandoffCriterion(str, Enum):
    """Handoff criteria for QA Tester."""
    
    UX_VALIDATION_READY = "comprehensive_ux_validation_completed"
    ACCESSIBILITY_READY = "accessibility_compliance_verified"
    PERSONA_TESTING_READY = "persona_testing_successful"
    USABILITY_VALIDATED = "usability_requirements_met"
    QUALITY_DOCUMENTED = "quality_metrics_documented"


class TestEngineerOutputContract(BaseModel):
    """
    Complete output contract for TestEngineerAgent to QA Tester.
    
    This model validates the entire contract structure and ensures
    compatibility with DigiNativa's contract system and QA Tester requirements.
    """
    
    contract_version: str = Field("1.0", description="Contract version")
    contract_type: str = Field("testing_to_qa", description="Contract type")
    story_id: str = Field(..., description="Story identifier")
    source_agent: str = Field("test_engineer", description="Source agent")
    target_agent: str = Field("qa_tester", description="Target agent")
    dna_compliance: Dict[str, Any] = Field(..., description="DNA compliance from input contract")
    
    input_requirements: Dict[str, Any] = Field(..., description="Requirements for QA Tester")
    output_specifications: Dict[str, Any] = Field(..., description="Output specifications for QA Tester")
    quality_gates: List[QualityGate] = Field(..., description="Quality gates that must pass")
    handoff_criteria: List[HandoffCriterion] = Field(..., description="Handoff criteria for QA Tester")
    
    @validator('story_id')
    def validate_story_id_format(cls, v):
        """Validate story ID follows DigiNativa format."""
        if not v.startswith("STORY-"):
            raise ValueError("Story ID must start with 'STORY-'")
        return v
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"
        validate_assignment = True
        use_enum_values = True