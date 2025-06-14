"""
Input contract models for QA Tester agent.

PURPOSE:
Defines the structure and validation for input contracts that the QA Tester
agent receives from the Test Engineer agent.

CRITICAL FUNCTIONALITY:
- Input contract structure validation
- Test suite result parsing
- Implementation data extraction
- Quality criteria enforcement

ADAPTATION GUIDE:
=' To adapt for your project:
1. Update TestSuiteInput for your test frameworks
2. Modify ImplementationData for your tech stack
3. Adjust QATesterInput for your workflow
4. Update validation rules for your standards

CONTRACT PROTECTION:
These models are part of DigiNativa's contract system.
Changes must maintain backward compatibility.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TestType(Enum):
    """Types of tests in the test suite."""
    UNIT = "unit"
    INTEGRATION = "integration"
    END_TO_END = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"


class ComplianceLevel(Enum):
    """DNA compliance levels."""
    FULL = "full"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"


@dataclass
class TestResult:
    """
    Individual test result structure.
    """
    test_id: str
    test_name: str
    test_type: TestType
    status: str  # "passed", "failed", "skipped"
    execution_time_ms: float
    error_message: Optional[str] = None
    coverage_percentage: Optional[float] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "test_id": self.test_id,
            "test_name": self.test_name,
            "test_type": self.test_type.value,
            "status": self.status,
            "execution_time_ms": self.execution_time_ms,
            "error_message": self.error_message,
            "coverage_percentage": self.coverage_percentage,
            "performance_metrics": self.performance_metrics
        }


@dataclass
class TestSuiteInput:
    """
    Test suite results from Test Engineer.
    """
    suite_id: str
    story_id: str
    execution_timestamp: str
    unit_tests: List[TestResult]
    integration_tests: List[TestResult]
    e2e_tests: List[TestResult]
    performance_tests: List[TestResult]
    security_tests: List[TestResult]
    overall_coverage_percentage: float
    test_environment: str
    execution_duration_minutes: float
    
    def get_all_tests(self) -> List[TestResult]:
        """Get all test results combined."""
        return (self.unit_tests + self.integration_tests + 
                self.e2e_tests + self.performance_tests + self.security_tests)
    
    def get_failed_tests(self) -> List[TestResult]:
        """Get all failed tests."""
        return [test for test in self.get_all_tests() if test.status == "failed"]
    
    def get_test_summary(self) -> Dict[str, Any]:
        """Get summary statistics of test results."""
        all_tests = self.get_all_tests()
        passed_tests = [t for t in all_tests if t.status == "passed"]
        failed_tests = self.get_failed_tests()
        
        return {
            "total_tests": len(all_tests),
            "passed_tests": len(passed_tests),
            "failed_tests": len(failed_tests),
            "success_rate": (len(passed_tests) / len(all_tests) * 100) if all_tests else 0,
            "coverage_percentage": self.overall_coverage_percentage,
            "execution_duration_minutes": self.execution_duration_minutes
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "suite_id": self.suite_id,
            "story_id": self.story_id,
            "execution_timestamp": self.execution_timestamp,
            "unit_tests": [test.to_dict() for test in self.unit_tests],
            "integration_tests": [test.to_dict() for test in self.integration_tests],
            "e2e_tests": [test.to_dict() for test in self.e2e_tests],
            "performance_tests": [test.to_dict() for test in self.performance_tests],
            "security_tests": [test.to_dict() for test in self.security_tests],
            "overall_coverage_percentage": self.overall_coverage_percentage,
            "test_environment": self.test_environment,
            "execution_duration_minutes": self.execution_duration_minutes
        }


@dataclass
class UIComponent:
    """
    UI component information for testing.
    """
    component_id: str
    component_type: str  # "button", "input", "link", "form", etc.
    properties: Dict[str, Any]
    accessibility_attributes: Dict[str, Any]
    styling_info: Dict[str, Any]
    interaction_handlers: List[str]
    text_content: Optional[str] = None
    children: Optional[List['UIComponent']] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "component_id": self.component_id,
            "component_type": self.component_type,
            "properties": self.properties,
            "accessibility_attributes": self.accessibility_attributes,
            "styling_info": self.styling_info,
            "interaction_handlers": self.interaction_handlers,
            "text_content": self.text_content,
            "children": [child.to_dict() for child in self.children] if self.children else None
        }


@dataclass
class APIEndpoint:
    """
    API endpoint information for testing.
    """
    endpoint_id: str
    method: str  # "GET", "POST", "PUT", "DELETE"
    path: str
    parameters: Dict[str, Any]
    request_schema: Dict[str, Any]
    response_schema: Dict[str, Any]
    authentication_required: bool
    rate_limits: Dict[str, Any]
    error_responses: Dict[str, Any]
    performance_requirements: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "endpoint_id": self.endpoint_id,
            "method": self.method,
            "path": self.path,
            "parameters": self.parameters,
            "request_schema": self.request_schema,
            "response_schema": self.response_schema,
            "authentication_required": self.authentication_required,
            "rate_limits": self.rate_limits,
            "error_responses": self.error_responses,
            "performance_requirements": self.performance_requirements
        }


@dataclass
class UserFlow:
    """
    User flow information for validation.
    """
    flow_id: str
    flow_name: str
    description: str
    steps: List[Dict[str, Any]]
    entry_points: List[str]
    exit_points: List[str]
    expected_duration_minutes: float
    user_goals: List[str]
    success_criteria: Dict[str, Any]
    error_scenarios: List[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "flow_id": self.flow_id,
            "flow_name": self.flow_name,
            "description": self.description,
            "steps": self.steps,
            "entry_points": self.entry_points,
            "exit_points": self.exit_points,
            "expected_duration_minutes": self.expected_duration_minutes,
            "user_goals": self.user_goals,
            "success_criteria": self.success_criteria,
            "error_scenarios": self.error_scenarios
        }


@dataclass
class ImplementationData:
    """
    Implementation details from Developer agent.
    """
    implementation_id: str
    story_id: str
    ui_components: List[UIComponent]
    api_endpoints: List[APIEndpoint]
    user_flows: List[UserFlow]
    database_schema: Dict[str, Any]
    configuration: Dict[str, Any]
    deployment_info: Dict[str, Any]
    documentation_links: List[str]
    feature_flags: Dict[str, bool]
    
    def get_component_by_type(self, component_type: str) -> List[UIComponent]:
        """Get UI components by type."""
        return [comp for comp in self.ui_components if comp.component_type == component_type]
    
    def get_endpoint_by_method(self, method: str) -> List[APIEndpoint]:
        """Get API endpoints by HTTP method."""
        return [endpoint for endpoint in self.api_endpoints if endpoint.method == method]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "implementation_id": self.implementation_id,
            "story_id": self.story_id,
            "ui_components": [comp.to_dict() for comp in self.ui_components],
            "api_endpoints": [endpoint.to_dict() for endpoint in self.api_endpoints],
            "user_flows": [flow.to_dict() for flow in self.user_flows],
            "database_schema": self.database_schema,
            "configuration": self.configuration,
            "deployment_info": self.deployment_info,
            "documentation_links": self.documentation_links,
            "feature_flags": self.feature_flags
        }


@dataclass
class PerformanceMetrics:
    """
    Performance metrics from testing.
    """
    lighthouse_score: float
    api_response_time_ms: float
    page_load_time_ms: float
    time_to_interactive_ms: float
    first_contentful_paint_ms: float
    largest_contentful_paint_ms: float
    cumulative_layout_shift: float
    bundle_size_kb: float
    memory_usage_mb: float
    cpu_usage_percentage: float
    
    def meets_requirements(self, requirements: Dict[str, float]) -> bool:
        """Check if metrics meet performance requirements."""
        checks = [
            self.lighthouse_score >= requirements.get("min_lighthouse_score", 90),
            self.api_response_time_ms <= requirements.get("max_api_response_time", 200),
            self.page_load_time_ms <= requirements.get("max_page_load_time", 3000),
            self.bundle_size_kb <= requirements.get("max_bundle_size", 500)
        ]
        return all(checks)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "lighthouse_score": self.lighthouse_score,
            "api_response_time_ms": self.api_response_time_ms,
            "page_load_time_ms": self.page_load_time_ms,
            "time_to_interactive_ms": self.time_to_interactive_ms,
            "first_contentful_paint_ms": self.first_contentful_paint_ms,
            "largest_contentful_paint_ms": self.largest_contentful_paint_ms,
            "cumulative_layout_shift": self.cumulative_layout_shift,
            "bundle_size_kb": self.bundle_size_kb,
            "memory_usage_mb": self.memory_usage_mb,
            "cpu_usage_percentage": self.cpu_usage_percentage
        }


@dataclass
class DNAComplianceData:
    """
    DNA compliance validation data.
    """
    design_principles_validation: Dict[str, bool]
    architecture_compliance: Dict[str, bool]
    validation_timestamp: str
    compliance_level: ComplianceLevel
    non_compliant_areas: List[str]
    recommendations: List[str]
    
    def is_fully_compliant(self) -> bool:
        """Check if fully DNA compliant."""
        return (self.compliance_level == ComplianceLevel.FULL and
                all(self.design_principles_validation.values()) and
                all(self.architecture_compliance.values()))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "design_principles_validation": self.design_principles_validation,
            "architecture_compliance": self.architecture_compliance,
            "validation_timestamp": self.validation_timestamp,
            "compliance_level": self.compliance_level.value,
            "non_compliant_areas": self.non_compliant_areas,
            "recommendations": self.recommendations
        }


@dataclass
class QATesterInputContract:
    """
    Complete input contract for QA Tester agent from Test Engineer.
    """
    contract_version: str
    story_id: str
    source_agent: str
    target_agent: str
    dna_compliance: DNAComplianceData
    
    # Required files
    required_files: List[str]
    
    # Core data from Test Engineer
    test_suite_results: TestSuiteInput
    implementation_data: ImplementationData
    performance_metrics: PerformanceMetrics
    coverage_report: Dict[str, Any]
    security_scan_results: Dict[str, Any]
    
    # Validation requirements
    required_validations: List[str]
    quality_gates: List[str]
    handoff_criteria: List[str]
    
    # Metadata
    contract_timestamp: str
    processing_deadline: Optional[str] = None
    priority_level: str = "medium"
    
    def validate_input_completeness(self) -> Dict[str, Any]:
        """
        Validate that input contract has all required data.
        
        Returns:
            Validation result with any missing requirements
        """
        missing_items = []
        validation_errors = []
        
        # Check required files
        if not self.required_files:
            missing_items.append("required_files")
        
        # Check test suite completeness
        if not self.test_suite_results.get_all_tests():
            missing_items.append("test_results")
        
        # Check implementation data
        if not self.implementation_data.ui_components and not self.implementation_data.api_endpoints:
            missing_items.append("implementation_components")
        
        # Check DNA compliance
        if not self.dna_compliance.is_fully_compliant():
            validation_errors.append("DNA compliance not fully validated")
        
        # Check performance metrics
        performance_requirements = {
            "min_lighthouse_score": 90,
            "max_api_response_time": 200,
            "max_page_load_time": 3000,
            "max_bundle_size": 500
        }
        
        if not self.performance_metrics.meets_requirements(performance_requirements):
            validation_errors.append("Performance metrics do not meet requirements")
        
        # Check coverage requirements
        if self.test_suite_results.overall_coverage_percentage < 100:
            validation_errors.append(f"Test coverage ({self.test_suite_results.overall_coverage_percentage}%) below required 100%")
        
        is_valid = len(missing_items) == 0 and len(validation_errors) == 0
        
        return {
            "is_valid": is_valid,
            "missing_items": missing_items,
            "validation_errors": validation_errors,
            "completeness_score": max(0, 100 - (len(missing_items) * 20) - (len(validation_errors) * 10))
        }
    
    def get_anna_persona_requirements(self) -> Dict[str, Any]:
        """
        Extract Anna persona specific requirements from contract.
        
        Returns:
            Anna persona requirements
        """
        return {
            "max_task_duration_minutes": 10,
            "min_satisfaction_score": 4.0,
            "min_accessibility_score": 90,
            "professional_tone_required": True,
            "pedagogical_value_required": True,
            "policy_relevance_required": True,
            "time_pressure_sensitivity": "high",
            "complexity_tolerance": "medium"
        }
    
    def extract_testing_priorities(self) -> List[str]:
        """
        Extract testing priorities based on contract data.
        
        Returns:
            List of testing priorities
        """
        priorities = []
        
        # High priority items
        if not self.dna_compliance.is_fully_compliant():
            priorities.append("DNA compliance validation")
        
        if self.test_suite_results.get_failed_tests():
            priorities.append("Failed test investigation")
        
        if self.performance_metrics.lighthouse_score < 90:
            priorities.append("Performance optimization")
        
        # Medium priority items
        if self.test_suite_results.overall_coverage_percentage < 100:
            priorities.append("Test coverage improvement")
        
        if len(self.implementation_data.ui_components) > 10:
            priorities.append("Complex UI validation")
        
        # Standard priorities
        priorities.extend([
            "Anna persona testing",
            "Accessibility compliance",
            "User flow validation",
            "Professional tone assessment"
        ])
        
        return priorities
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "contract_version": self.contract_version,
            "story_id": self.story_id,
            "source_agent": self.source_agent,
            "target_agent": self.target_agent,
            "dna_compliance": self.dna_compliance.to_dict(),
            "required_files": self.required_files,
            "test_suite_results": self.test_suite_results.to_dict(),
            "implementation_data": self.implementation_data.to_dict(),
            "performance_metrics": self.performance_metrics.to_dict(),
            "coverage_report": self.coverage_report,
            "security_scan_results": self.security_scan_results,
            "required_validations": self.required_validations,
            "quality_gates": self.quality_gates,
            "handoff_criteria": self.handoff_criteria,
            "contract_timestamp": self.contract_timestamp,
            "processing_deadline": self.processing_deadline,
            "priority_level": self.priority_level
        }


# Utility functions for contract parsing

def parse_test_result_from_dict(data: Dict[str, Any]) -> TestResult:
    """Parse TestResult from dictionary."""
    return TestResult(
        test_id=data["test_id"],
        test_name=data["test_name"],
        test_type=TestType(data["test_type"]),
        status=data["status"],
        execution_time_ms=data["execution_time_ms"],
        error_message=data.get("error_message"),
        coverage_percentage=data.get("coverage_percentage"),
        performance_metrics=data.get("performance_metrics")
    )


def parse_ui_component_from_dict(data: Dict[str, Any]) -> UIComponent:
    """Parse UIComponent from dictionary."""
    children = None
    if data.get("children"):
        children = [parse_ui_component_from_dict(child) for child in data["children"]]
    
    return UIComponent(
        component_id=data["component_id"],
        component_type=data["component_type"],
        properties=data["properties"],
        accessibility_attributes=data["accessibility_attributes"],
        styling_info=data["styling_info"],
        interaction_handlers=data["interaction_handlers"],
        text_content=data.get("text_content"),
        children=children
    )


def parse_api_endpoint_from_dict(data: Dict[str, Any]) -> APIEndpoint:
    """Parse APIEndpoint from dictionary."""
    return APIEndpoint(
        endpoint_id=data["endpoint_id"],
        method=data["method"],
        path=data["path"],
        parameters=data["parameters"],
        request_schema=data["request_schema"],
        response_schema=data["response_schema"],
        authentication_required=data["authentication_required"],
        rate_limits=data["rate_limits"],
        error_responses=data["error_responses"],
        performance_requirements=data["performance_requirements"]
    )


def parse_user_flow_from_dict(data: Dict[str, Any]) -> UserFlow:
    """Parse UserFlow from dictionary."""
    return UserFlow(
        flow_id=data["flow_id"],
        flow_name=data["flow_name"],
        description=data["description"],
        steps=data["steps"],
        entry_points=data["entry_points"],
        exit_points=data["exit_points"],
        expected_duration_minutes=data["expected_duration_minutes"],
        user_goals=data["user_goals"],
        success_criteria=data["success_criteria"],
        error_scenarios=data["error_scenarios"]
    )


def parse_qa_tester_input_contract(contract_data: Dict[str, Any]) -> QATesterInputContract:
    """
    Parse complete QA Tester input contract from dictionary.
    
    Args:
        contract_data: Contract data dictionary
        
    Returns:
        Parsed QATesterInputContract
    """
    # Parse test suite results
    test_suite_data = contract_data["input_requirements"]["required_data"]["test_suite"]
    test_suite = TestSuiteInput(
        suite_id=test_suite_data["suite_id"],
        story_id=test_suite_data["story_id"],
        execution_timestamp=test_suite_data["execution_timestamp"],
        unit_tests=[parse_test_result_from_dict(test) for test in test_suite_data["unit_tests"]],
        integration_tests=[parse_test_result_from_dict(test) for test in test_suite_data["integration_tests"]],
        e2e_tests=[parse_test_result_from_dict(test) for test in test_suite_data["e2e_tests"]],
        performance_tests=[parse_test_result_from_dict(test) for test in test_suite_data["performance_tests"]],
        security_tests=[parse_test_result_from_dict(test) for test in test_suite_data["security_tests"]],
        overall_coverage_percentage=test_suite_data["overall_coverage_percentage"],
        test_environment=test_suite_data["test_environment"],
        execution_duration_minutes=test_suite_data["execution_duration_minutes"]
    )
    
    # Parse implementation data
    impl_data = contract_data["input_requirements"]["required_data"]["implementation_data"]
    implementation = ImplementationData(
        implementation_id=impl_data["implementation_id"],
        story_id=impl_data["story_id"],
        ui_components=[parse_ui_component_from_dict(comp) for comp in impl_data["ui_components"]],
        api_endpoints=[parse_api_endpoint_from_dict(endpoint) for endpoint in impl_data["api_endpoints"]],
        user_flows=[parse_user_flow_from_dict(flow) for flow in impl_data["user_flows"]],
        database_schema=impl_data["database_schema"],
        configuration=impl_data["configuration"],
        deployment_info=impl_data["deployment_info"],
        documentation_links=impl_data["documentation_links"],
        feature_flags=impl_data["feature_flags"]
    )
    
    # Parse performance metrics
    perf_data = contract_data["input_requirements"]["required_data"]["performance_results"]
    performance = PerformanceMetrics(
        lighthouse_score=perf_data["lighthouse_score"],
        api_response_time_ms=perf_data["api_response_time_ms"],
        page_load_time_ms=perf_data["page_load_time_ms"],
        time_to_interactive_ms=perf_data["time_to_interactive_ms"],
        first_contentful_paint_ms=perf_data["first_contentful_paint_ms"],
        largest_contentful_paint_ms=perf_data["largest_contentful_paint_ms"],
        cumulative_layout_shift=perf_data["cumulative_layout_shift"],
        bundle_size_kb=perf_data["bundle_size_kb"],
        memory_usage_mb=perf_data["memory_usage_mb"],
        cpu_usage_percentage=perf_data["cpu_usage_percentage"]
    )
    
    # Parse DNA compliance
    dna_data = contract_data["dna_compliance"]
    dna_compliance = DNAComplianceData(
        design_principles_validation=dna_data["design_principles_validation"],
        architecture_compliance=dna_data["architecture_compliance"],
        validation_timestamp=dna_data["validation_timestamp"],
        compliance_level=ComplianceLevel(dna_data["compliance_level"]),
        non_compliant_areas=dna_data.get("non_compliant_areas", []),
        recommendations=dna_data.get("recommendations", [])
    )
    
    return QATesterInputContract(
        contract_version=contract_data["contract_version"],
        story_id=contract_data["story_id"],
        source_agent=contract_data["source_agent"],
        target_agent=contract_data["target_agent"],
        dna_compliance=dna_compliance,
        required_files=contract_data["input_requirements"]["required_files"],
        test_suite_results=test_suite,
        implementation_data=implementation,
        performance_metrics=performance,
        coverage_report=contract_data["input_requirements"]["required_data"]["coverage_report"],
        security_scan_results=contract_data["input_requirements"]["required_data"]["security_scan_results"],
        required_validations=contract_data["input_requirements"]["required_validations"],
        quality_gates=contract_data["quality_gates"],
        handoff_criteria=contract_data["handoff_criteria"],
        contract_timestamp=datetime.now().isoformat(),
        processing_deadline=contract_data.get("processing_deadline"),
        priority_level=contract_data.get("priority_level", "medium")
    )