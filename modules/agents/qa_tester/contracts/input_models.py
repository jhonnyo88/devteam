"""
QA Tester Input Contract Models

PURPOSE:
Defines Pydantic models for QA Tester Agent input contracts,
ensuring type safety and contract compliance from Test Engineer.

CONTRACT VALIDATION:
These models implement the exact contract structure for
Test Engineer -> QA Tester handoff as specified in Implementation_rules.md.

ADAPTATION GUIDE:
🔧 To adapt for your project:
1. Update test_suite structure for your test frameworks
2. Modify implementation_data for your tech stack
3. Adjust validation_criteria for your quality standards
4. Update AI integration fields for your ML requirements

CONTRACT PROTECTION:
These models are part of DigiNativa's contract system.
Changes must maintain backward compatibility.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class QATesterInputContract(BaseModel):
    """
    QA Tester input contract receiving Test Engineer output.
    
    Receives comprehensive testing data for QA validation including
    test results, implementation data, performance metrics, and AI integration.
    """
    
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version")
    source_agent: str = Field("test_engineer", description="Source agent")
    target_agent: str = Field("qa_tester", description="Target agent")
    story_id: str = Field(..., description="Story identifier")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Test results from Test Engineer
    integration_test_suite: Dict[str, Any] = Field(..., description="Integration tests")
    e2e_test_suite: Dict[str, Any] = Field(..., description="E2E tests") 
    performance_results: Dict[str, Any] = Field(..., description="Performance results")
    security_scan_results: Dict[str, Any] = Field(..., description="Security scan")
    coverage_report: Dict[str, Any] = Field(..., description="Coverage report")
    automation_config: Dict[str, Any] = Field(..., description="Automation config")
    
    # Original implementation data for testing
    original_implementation: Dict[str, Any] = Field(..., description="Implementation data for QA testing")
    
    # DNA compliance from Test Engineer
    dna_compliance: Dict[str, Any] = Field(..., description="Test Engineer DNA validation")
    
    # Required files and validations
    required_files: List[str] = Field(default_factory=list, description="Required test files")
    required_validations: List[str] = Field(default_factory=list, description="Required validations")
    quality_gates: List[str] = Field(default_factory=list, description="Quality gates")
    handoff_criteria: List[str] = Field(default_factory=list, description="Handoff criteria")
    
    # Processing metadata
    processing_deadline: Optional[str] = Field(None, description="Processing deadline")
    priority_level: str = Field("medium", description="Priority level")
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {
            "example": {
                "story_id": "STORY-TEST-001",
                "integration_test_suite": {
                    "unit_tests": [
                        {
                            "test_id": "unit_001",
                            "test_name": "Test Component Rendering",
                            "test_type": "unit",
                            "status": "passed",
                            "execution_time_ms": 150.0,
                            "coverage_percentage": 95.0
                        }
                    ],
                    "integration_tests": [
                        {
                            "test_id": "integration_001",
                            "test_name": "Test API Integration",
                            "test_type": "integration",
                            "status": "passed",
                            "execution_time_ms": 500.0,
                            "coverage_percentage": 90.0
                        }
                    ],
                    "e2e_tests": [
                        {
                            "test_id": "e2e_001",
                            "test_name": "Test User Flow",
                            "test_type": "e2e",
                            "status": "passed",
                            "execution_time_ms": 2000.0,
                            "coverage_percentage": 85.0
                        }
                    ]
                },
                "performance_results": {
                    "lighthouse_score": 95.0,
                    "api_response_time_ms": 150.0,
                    "page_load_time_ms": 2000.0,
                    "time_to_interactive_ms": 2500.0,
                    "first_contentful_paint_ms": 1000.0,
                    "largest_contentful_paint_ms": 1500.0,
                    "cumulative_layout_shift": 0.05,
                    "bundle_size_kb": 400.0,
                    "memory_usage_mb": 50.0,
                    "cpu_usage_percentage": 15.0
                },
                "security_scan_results": {
                    "vulnerabilities": [],
                    "scan_status": "clean"
                },
                "coverage_report": {
                    "total_coverage": 100.0,
                    "line_coverage": 100.0,
                    "branch_coverage": 95.0,
                    "function_coverage": 100.0
                },
                "original_implementation": {
                    "implementation_id": "impl_001",
                    "story_id": "STORY-TEST-001",
                    "ui_components": [
                        {
                            "component_id": "test-button",
                            "component_type": "button",
                            "properties": {"text": "Submit"},
                            "accessibility_attributes": {"aria-label": "Submit form"},
                            "styling_info": {"color": "#000000", "background_color": "#ffffff"},
                            "interaction_handlers": ["onClick"],
                            "text_content": "Submit"
                        }
                    ],
                    "api_endpoints": [],
                    "user_flows": [],
                    "database_schema": {},
                    "configuration": {},
                    "deployment_info": {},
                    "documentation_links": [],
                    "feature_flags": {}
                },
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
                }
            }
        }


# Utility function for parsing QA Tester input contract

def parse_qa_tester_input_contract(contract_data: Dict[str, Any]) -> QATesterInputContract:
    """
    Parse QA Tester input contract from Test Engineer output.
    
    Args:
        contract_data: Test Engineer output contract data
        
    Returns:
        Parsed QATesterInputContract with full type validation
    """
    return QATesterInputContract(**contract_data)