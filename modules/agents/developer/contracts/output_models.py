"""
Output contract models for DeveloperAgent.

PURPOSE:
Defines Pydantic models for validating output contracts to Test Engineer
according to Implementation_rules.md specifications.

CRITICAL VALIDATION:
- Contract structure compliance
- Deliverable data validation
- Quality gate specifications
- Test Engineer input requirements
"""

from pydantic import BaseModel, Field, validator, model_validator
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum


class ComponentImplementation(BaseModel):
    """Implementation details for a React component."""
    
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
    
    @validator('typescript_errors')
    def validate_zero_typescript_errors(cls, v):
        """Validate TypeScript compilation has zero errors."""
        if v > 0:
            raise ValueError("TypeScript compilation must have zero errors for production code")
        return v
    
    @validator('eslint_violations')
    def validate_zero_eslint_violations(cls, v):
        """Validate ESLint compliance has zero violations."""
        if v > 0:
            raise ValueError("ESLint compliance must have zero violations for production code")
        return v
    
    @validator('test_coverage_percent')
    def validate_full_test_coverage(cls, v):
        """Validate test coverage is 100%."""
        if v < 100.0:
            raise ValueError("Test coverage must be 100% for all business logic")
        return v


class APIImplementation(BaseModel):
    """Implementation details for a FastAPI endpoint."""
    
    name: str = Field(..., description="API endpoint name")
    method: str = Field(..., description="HTTP method")
    path: str = Field(..., description="API path")
    files: Dict[str, str] = Field(..., description="Generated file paths")
    code: Dict[str, str] = Field(..., description="Generated code content")
    functional_test_passed: bool = Field(True, description="Functional test status")
    performance_test_passed: bool = Field(True, description="Performance test status")
    security_test_passed: bool = Field(True, description="Security test status")
    estimated_response_time_ms: int = Field(..., le=200, description="Estimated response time")
    
    @validator('estimated_response_time_ms')
    def validate_response_time_budget(cls, v):
        """Validate API response time meets performance budget."""
        if v > 200:
            raise ValueError("API response time must be d200ms (performance requirement)")
        return v


class TestSuite(BaseModel):
    """Generated test suite details."""
    
    story_id: str = Field(..., description="Story identifier")
    unit_tests: List[Dict[str, Any]] = Field(..., description="Unit test details")
    coverage_percent: float = Field(100.0, ge=0, le=100, description="Overall test coverage")
    total_test_cases: int = Field(..., ge=0, description="Total number of test cases")
    test_configuration: Dict[str, Any] = Field(..., description="Test framework configuration")
    
    @validator('coverage_percent')
    def validate_full_coverage(cls, v):
        """Validate overall test coverage is 100%."""
        if v < 100.0:
            raise ValueError("Overall test coverage must be 100%")
        return v


class ImplementationDocs(BaseModel):
    """Implementation documentation details."""
    
    story_id: str = Field(..., description="Story identifier")
    implementation_summary: Dict[str, Any] = Field(..., description="Implementation summary")
    architecture_compliance: Dict[str, bool] = Field(..., description="Architecture compliance verification")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    deployment_instructions: Dict[str, Any] = Field(..., description="Deployment instructions")
    
    @validator('architecture_compliance')
    def validate_architecture_compliance(cls, v):
        """Validate all architecture principles are met."""
        required_principles = {
            'api_first', 'stateless_backend', 
            'separation_of_concerns', 'component_library_usage'
        }
        
        if not required_principles.issubset(set(v.keys())):
            missing = required_principles - set(v.keys())
            raise ValueError(f"Missing architecture compliance validation: {missing}")
        
        # All principles must be True
        false_principles = [k for k, val in v.items() if not val]
        if false_principles:
            raise ValueError(f"Architecture principles not met: {false_principles}")
        
        return v


class ValidationCriteria(BaseModel):
    """Validation criteria for Test Engineer."""
    
    test_quality: Dict[str, Any] = Field(..., description="Test quality requirements")
    automation: Dict[str, Any] = Field(..., description="Automation requirements")
    security: Dict[str, Any] = Field(..., description="Security requirements")
    
    @validator('test_quality')
    def validate_test_quality_criteria(cls, v):
        """Validate test quality criteria are properly specified."""
        required_criteria = {
            'integration_test_coverage': {'min': 95},
            'e2e_test_coverage': {'min': 90},
            'performance_test_included': True
        }
        
        for criterion, expected in required_criteria.items():
            if criterion not in v:
                raise ValueError(f"Missing test quality criterion: {criterion}")
            
            if isinstance(expected, dict) and 'min' in expected:
                if v[criterion].get('min', 0) < expected['min']:
                    raise ValueError(f"Test quality criterion {criterion} below minimum: {expected['min']}")
        
        return v


class OutputSpecifications(BaseModel):
    """Output specifications for Test Engineer."""
    
    deliverable_files: List[str] = Field(..., description="Files to be delivered to Test Engineer")
    deliverable_data: Dict[str, Any] = Field(..., description="Data to be delivered to Test Engineer")
    validation_criteria: ValidationCriteria = Field(..., description="Validation criteria for Test Engineer")
    
    @validator('deliverable_files')
    def validate_required_deliverable_files(cls, v):
        """Validate all required files are specified."""
        required_patterns = [
            'tests/integration/',
            'tests/e2e/',
            'docs/test_reports/',
            'docs/performance/'
        ]
        
        for pattern in required_patterns:
            if not any(pattern in file_path for file_path in v):
                raise ValueError(f"Missing required deliverable file pattern: {pattern}")
        
        return v


class InputRequirementsForTestEngineer(BaseModel):
    """Input requirements that will be provided to Test Engineer."""
    
    required_files: List[str] = Field(..., description="Files required by Test Engineer")
    required_data: Dict[str, Any] = Field(..., description="Data required by Test Engineer")
    required_validations: List[str] = Field(..., description="Validations required by Test Engineer")
    
    @validator('required_data')
    def validate_required_data_for_test_engineer(cls, v):
        """Validate required data contains all necessary implementation details."""
        required_keys = {
            'component_implementations', 'api_implementations', 
            'test_suite', 'implementation_docs', 'git_commit_hash'
        }
        
        if not required_keys.issubset(set(v.keys())):
            missing = required_keys - set(v.keys())
            raise ValueError(f"Missing required data for Test Engineer: {missing}")
        
        return v


class QualityGate(str, Enum):
    """Quality gates that must pass before handoff to Test Engineer."""
    
    INTEGRATION_TESTS_PASSING = "all_integration_tests_passing"
    PERFORMANCE_BENCHMARKS_MET = "performance_benchmarks_within_targets"
    SECURITY_SCAN_CLEAN = "security_vulnerability_scan_clean"
    TEST_SUITE_CONFIGURED = "automated_test_suite_configured"
    LOAD_TESTING_COMPLETED = "load_testing_completed"


class HandoffCriterion(str, Enum):
    """Handoff criteria for successful transfer to Test Engineer."""
    
    COMPREHENSIVE_COVERAGE = "comprehensive_test_coverage_achieved"
    PERFORMANCE_VALIDATED = "all_performance_requirements_validated"
    TEST_PIPELINE_CONFIGURED = "automated_test_pipeline_configured"
    QUALITY_DOCUMENTED = "quality_metrics_documented"
    SECURITY_VALIDATED = "security_validation_completed"


class DeveloperOutputContract(BaseModel):
    """
    Complete output contract for DeveloperAgent to Test Engineer.
    
    This model validates the entire contract structure and ensures
    compatibility with DigiNativa's contract system and Test Engineer requirements.
    """
    
    contract_version: str = Field("1.0", description="Contract version")
    contract_type: str = Field("implementation_to_testing", description="Contract type")
    story_id: str = Field(..., description="Story identifier")
    source_agent: str = Field("developer", description="Source agent")
    target_agent: str = Field("test_engineer", description="Target agent")
    dna_compliance: Dict[str, Any] = Field(..., description="DNA compliance from input contract")
    
    input_requirements: InputRequirementsForTestEngineer = Field(..., description="Requirements for Test Engineer")
    output_specifications: OutputSpecifications = Field(..., description="Output specifications for Test Engineer")
    quality_gates: List[QualityGate] = Field(..., description="Quality gates that must pass")
    handoff_criteria: List[HandoffCriterion] = Field(..., description="Handoff criteria for Test Engineer")
    
    @validator('contract_version')
    def validate_contract_version(cls, v):
        """Validate contract version is supported."""
        if v != "1.0":
            raise ValueError("Only contract version 1.0 is currently supported")
        return v
    
    @validator('contract_type')
    def validate_contract_type(cls, v):
        """Validate contract type is correct for Test Engineer."""
        if v != "implementation_to_testing":
            raise ValueError("Developer agent outputs 'implementation_to_testing' contract type")
        return v
    
    @validator('source_agent')
    def validate_source_agent(cls, v):
        """Validate source agent is Developer."""
        if v != "developer":
            raise ValueError("Contract source agent must be 'developer'")
        return v
    
    @validator('target_agent')
    def validate_target_agent(cls, v):
        """Validate target agent is Test Engineer."""
        if v != "test_engineer":
            raise ValueError("Developer agent outputs contracts to 'test_engineer'")
        return v
    
    @validator('story_id')
    def validate_story_id_format(cls, v):
        """Validate story ID follows DigiNativa format."""
        if not v.startswith("STORY-"):
            raise ValueError("Story ID must start with 'STORY-'")
        return v
    
    @validator('quality_gates')
    def validate_required_quality_gates(cls, v):
        """Validate all required quality gates are present."""
        required_gates = {
            QualityGate.INTEGRATION_TESTS_PASSING,
            QualityGate.PERFORMANCE_BENCHMARKS_MET,
            QualityGate.SECURITY_SCAN_CLEAN,
            QualityGate.TEST_SUITE_CONFIGURED
        }
        
        if not required_gates.issubset(set(v)):
            missing = required_gates - set(v)
            raise ValueError(f"Missing required quality gates: {missing}")
        
        return v
    
    @validator('handoff_criteria')
    def validate_required_handoff_criteria(cls, v):
        """Validate all required handoff criteria are present."""
        required_criteria = {
            HandoffCriterion.COMPREHENSIVE_COVERAGE,
            HandoffCriterion.PERFORMANCE_VALIDATED,
            HandoffCriterion.TEST_PIPELINE_CONFIGURED,
            HandoffCriterion.QUALITY_DOCUMENTED
        }
        
        if not required_criteria.issubset(set(v)):
            missing = required_criteria - set(v)
            raise ValueError(f"Missing required handoff criteria: {missing}")
        
        return v
    
    @model_validator(mode='after')
    def validate_complete_contract(self):
        """Validate complete contract integrity."""
        # Validate DNA compliance is preserved from input
        dna_compliance = self.dna_compliance
        if not dna_compliance:
            raise ValueError("DNA compliance must be preserved from input contract")
        
        # Validate input requirements for Test Engineer
        input_reqs = self.input_requirements
        if input_reqs:
            required_data = input_reqs.required_data
            
            # Validate component implementations
            if 'component_implementations' in required_data:
                for comp_data in required_data['component_implementations']:
                    ComponentImplementation(**comp_data)
            
            # Validate API implementations
            if 'api_implementations' in required_data:
                for api_data in required_data['api_implementations']:
                    APIImplementation(**api_data)
            
            # Validate test suite
            if 'test_suite' in required_data:
                TestSuite(**required_data['test_suite'])
            
            # Validate implementation docs
            if 'implementation_docs' in required_data:
                ImplementationDocs(**required_data['implementation_docs'])
        
        return self
    
    class Config:
        """Pydantic configuration."""
        
        extra = "forbid"  # Prevent additional fields
        validate_assignment = True  # Validate on assignment
        use_enum_values = True  # Use enum values in serialization
        schema_extra = {
            "example": {
                "contract_version": "1.0",
                "contract_type": "implementation_to_testing",
                "story_id": "STORY-001-001",
                "source_agent": "developer",
                "target_agent": "test_engineer",
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
                "input_requirements": {
                    "required_files": [
                        "frontend/components/STORY-001-001/",
                        "backend/endpoints/STORY-001-001/",
                        "tests/unit/STORY-001-001/",
                        "docs/implementation/STORY-001-001_implementation.md"
                    ],
                    "required_data": {
                        "component_implementations": [],
                        "api_implementations": [],
                        "test_suite": {},
                        "implementation_docs": {},
                        "git_commit_hash": "abc123"
                    },
                    "required_validations": [
                        "typescript_compilation_successful",
                        "eslint_compliance_verified",
                        "unit_tests_100_percent_coverage",
                        "architecture_principles_followed"
                    ]
                },
                "output_specifications": {
                    "deliverable_files": [
                        "tests/integration/STORY-001-001/",
                        "tests/e2e/STORY-001-001/",
                        "docs/test_reports/STORY-001-001_coverage.html",
                        "docs/performance/STORY-001-001_benchmarks.json"
                    ],
                    "deliverable_data": {
                        "integration_test_suite": {},
                        "e2e_test_suite": {},
                        "performance_test_results": {},
                        "coverage_report": {},
                        "security_scan_results": {}
                    },
                    "validation_criteria": {
                        "test_quality": {
                            "integration_test_coverage": {"min": 95},
                            "e2e_test_coverage": {"min": 90},
                            "performance_test_included": True
                        },
                        "automation": {
                            "ci_cd_integration": True,
                            "automated_regression_tests": True,
                            "load_testing_configured": True
                        },
                        "security": {
                            "vulnerability_scan_clean": True,
                            "dependency_security_check": True,
                            "api_security_validated": True
                        }
                    }
                },
                "quality_gates": [
                    "all_integration_tests_passing",
                    "performance_benchmarks_within_targets",
                    "security_vulnerability_scan_clean",
                    "automated_test_suite_configured"
                ],
                "handoff_criteria": [
                    "comprehensive_test_coverage_achieved",
                    "all_performance_requirements_validated",
                    "automated_test_pipeline_configured",
                    "quality_metrics_documented"
                ]
            }
        }