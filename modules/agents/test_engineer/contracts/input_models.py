"""
Input contract models for TestEngineerAgent.

PURPOSE:
Defines Pydantic models for validating input contracts from Developer agent
according to Implementation_rules.md specifications.

CRITICAL VALIDATION:
- Contract structure compliance
- Implementation data validation
- Required files verification
- Quality gate specifications
"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum


class ComponentImplementation(BaseModel):
    """React component implementation from Developer agent."""
    
    name: str = Field(..., description="Component name")
    type: str = Field(..., description="Component type")
    files: Dict[str, str] = Field(..., description="Generated file paths")
    code: Dict[str, str] = Field(..., description="Generated code content")
    typescript_errors: int = Field(0, ge=0, description="TypeScript compilation errors")
    eslint_violations: int = Field(0, ge=0, description="ESLint violations")
    test_coverage_percent: float = Field(100.0, ge=0, le=100, description="Test coverage percentage")
    accessibility_score: int = Field(95, ge=0, le=100, description="Accessibility compliance score")
    performance_score: int = Field(90, ge=0, le=100, description="Performance score")
    integration_test_passed: bool = Field(True, description="Integration test status")


class APIImplementation(BaseModel):
    """FastAPI endpoint implementation from Developer agent."""
    
    name: str = Field(..., description="API endpoint name")
    method: str = Field(..., description="HTTP method")
    path: str = Field(..., description="API path")
    files: Dict[str, str] = Field(..., description="Generated file paths")
    code: Dict[str, str] = Field(..., description="Generated code content")
    functional_test_passed: bool = Field(True, description="Functional test status")
    performance_test_passed: bool = Field(True, description="Performance test status")
    security_test_passed: bool = Field(True, description="Security test status")
    estimated_response_time_ms: int = Field(..., le=200, description="Estimated response time")


class TestSuite(BaseModel):
    """Test suite from Developer agent."""
    
    story_id: str = Field(..., description="Story identifier")
    unit_tests: List[Dict[str, Any]] = Field(..., description="Unit test details")
    coverage_percent: float = Field(100.0, ge=0, le=100, description="Overall test coverage")
    total_test_cases: int = Field(..., ge=0, description="Total number of test cases")
    test_configuration: Dict[str, Any] = Field(..., description="Test framework configuration")


class ImplementationDocs(BaseModel):
    """Implementation documentation from Developer agent."""
    
    story_id: str = Field(..., description="Story identifier")
    implementation_summary: Dict[str, Any] = Field(..., description="Implementation summary")
    architecture_compliance: Dict[str, bool] = Field(..., description="Architecture compliance verification")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    deployment_instructions: Dict[str, Any] = Field(..., description="Deployment instructions")
    user_flows: List[Dict[str, Any]] = Field(default=[], description="User flows for E2E testing")


class RequiredData(BaseModel):
    """Required data from Developer agent."""
    
    component_implementations: List[ComponentImplementation] = Field(..., description="React components")
    api_implementations: List[APIImplementation] = Field(..., description="FastAPI endpoints")
    test_suite: TestSuite = Field(..., description="Unit test suite")
    implementation_docs: ImplementationDocs = Field(..., description="Implementation documentation")
    git_commit_hash: str = Field(..., description="Git commit hash")


class InputRequirements(BaseModel):
    """Input requirements for Test Engineer agent."""
    
    required_files: List[str] = Field(..., description="Files required for testing")
    required_data: RequiredData = Field(..., description="Implementation data")
    required_validations: List[str] = Field(..., description="Required validations")


class TestEngineerInputContract(BaseModel):
    """
    Complete input contract for TestEngineerAgent from Developer.
    
    This model validates the entire contract structure and ensures
    compatibility with DigiNativa's contract system.
    """
    
    contract_version: str = Field("1.0", description="Contract version")
    contract_type: str = Field("implementation_to_testing", description="Contract type")
    story_id: str = Field(..., description="Story identifier")
    source_agent: str = Field("developer", description="Source agent")
    target_agent: str = Field("test_engineer", description="Target agent")
    dna_compliance: Dict[str, Any] = Field(..., description="DNA compliance validation")
    
    input_requirements: InputRequirements = Field(..., description="Implementation data for testing")
    
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