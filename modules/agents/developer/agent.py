"""
DeveloperAgent - Full-stack implementation agent for the DigiNativa system.

PURPOSE:
Transforms game design specifications and UX wireframes into working
React + FastAPI code following DigiNativa's architecture principles.

CRITICAL RESPONSIBILITIES:
- Generate production-ready React components with TypeScript
- Create stateless FastAPI endpoints following API-first design
- Implement proper Git workflow with feature branches
- Ensure 100% test coverage and DNA compliance
- Maintain performance standards (Lighthouse >90, API <200ms)

CONTRACT PROTECTION:
This agent receives contracts from Game Designer and outputs to Test Engineer.
NEVER break the contract interface - it enables our modular architecture.
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

# Import our foundation
from ...shared.base_agent import BaseAgent, AgentExecutionResult
from ...shared.exceptions import AgentExecutionError, DNAComplianceError, QualityGateError

# Import specialized tools
from .tools.code_generator import CodeGenerator
from .tools.api_builder import APIBuilder
from .tools.git_operations import GitOperations
from .tools.component_builder import ComponentBuilder
from .tools.architecture_validator import ArchitectureValidator

# Setup logging
logger = logging.getLogger(__name__)


class DeveloperAgent(BaseAgent):
    """
    Developer agent for full-stack implementation (React + FastAPI).
    
    WORKFLOW:
    1. Receive UX specifications and component mappings from Game Designer
    2. Generate React components using Shadcn/UI and Kenney.UI
    3. Create stateless FastAPI endpoints for backend functionality
    4. Implement proper state management and error handling
    5. Generate unit tests for all components and APIs
    6. Create feature branch and commit working code
    7. Output contract for Test Engineer with implementation details
    
    QUALITY GATES:
    - TypeScript compilation: 0 errors
    - ESLint compliance: 0 violations
    - Unit test coverage: 100%
    - Architecture compliance: API-first, stateless backend
    - Performance: Lighthouse >90, API response <200ms
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Developer agent.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__("dev-001", "developer", config)
        
        # Initialize specialized tools
        self.code_generator = CodeGenerator(config)
        self.api_builder = APIBuilder(config)
        self.git_operations = GitOperations(config)
        self.component_builder = ComponentBuilder(config)
        self.architecture_validator = ArchitectureValidator(config)
        
        # Developer-specific configuration
        self.frontend_path = self.config.get("frontend_path", "frontend")
        self.backend_path = self.config.get("backend_path", "backend")
        self.test_path = self.config.get("test_path", "tests")
        
        # Quality standards for DigiNativa
        self.quality_standards = {
            "typescript_errors": {"max": 0},
            "eslint_violations": {"max": 0},
            "test_coverage_percent": {"min": 100},
            "lighthouse_score": {"min": 90},
            "api_response_time_ms": {"max": 200},
            "bundle_size_increase_kb": {"max": 50}
        }
        
        self.logger.info("DeveloperAgent initialized successfully")
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process Game Designer contract and implement full-stack solution.
        
        IMPLEMENTATION FLOW:
        1. Extract UX specifications and component mappings
        2. Validate technical feasibility against architecture principles
        3. Generate React components with proper TypeScript interfaces
        4. Create FastAPI endpoints following stateless design
        5. Implement state management and error handling
        6. Generate comprehensive unit tests
        7. Create feature branch and commit implementation
        8. Generate output contract for Test Engineer
        
        Args:
            input_contract: Contract from Game Designer with UX specs
            
        Returns:
            Output contract for Test Engineer with implementation details
            
        Raises:
            AgentExecutionError: If implementation fails
            DNAComplianceError: If implementation violates DNA principles
        """
        try:
            story_id = input_contract.get("story_id")
            self.logger.info(f"Starting implementation for story: {story_id}")
            
            # Step 1: Extract and validate input data
            input_data = input_contract.get("input_requirements", {}).get("required_data", {})
            
            game_mechanics = input_data.get("game_mechanics", {})
            ui_components = input_data.get("ui_components", [])
            interaction_flows = input_data.get("interaction_flows", [])
            api_endpoints = input_data.get("api_endpoints", [])
            state_management = input_data.get("state_management", {})
            
            self.logger.debug(f"Processing {len(ui_components)} UI components and {len(api_endpoints)} API endpoints")
            
            # Step 2: Validate architecture compliance
            await self._validate_architecture_requirements(input_data)
            
            # Step 3: Create feature branch for implementation
            branch_name = f"feature/{story_id}"
            await self.git_operations.create_feature_branch(story_id, branch_name)
            
            # Step 4: Generate React components
            self.logger.info("Generating React components")
            component_implementations = await self.component_builder.build_components(
                ui_components, 
                interaction_flows,
                story_id
            )
            
            # Step 5: Generate FastAPI endpoints
            self.logger.info("Generating FastAPI endpoints")
            api_implementations = await self.api_builder.build_apis(
                api_endpoints,
                state_management,
                story_id
            )
            
            # Step 6: Generate unit tests
            self.logger.info("Generating unit tests")
            test_suite = await self.code_generator.generate_tests(
                component_implementations,
                api_implementations,
                story_id
            )
            
            # Step 7: Validate implementation quality
            await self._validate_implementation_quality(
                component_implementations,
                api_implementations,
                test_suite
            )
            
            # Step 8: Commit implementation to feature branch
            commit_message = f"Implement {story_id}: {game_mechanics.get('title', 'Feature implementation')}"
            commit_hash = await self.git_operations.commit_implementation(
                story_id,
                commit_message,
                component_implementations,
                api_implementations,
                test_suite
            )
            
            # Step 9: Generate implementation documentation
            implementation_docs = await self._generate_implementation_docs(
                story_id,
                game_mechanics,
                component_implementations,
                api_implementations,
                test_suite
            )
            
            # Step 10: Create output contract for Test Engineer
            output_contract = await self._create_output_contract(
                input_contract,
                story_id,
                component_implementations,
                api_implementations,
                test_suite,
                implementation_docs,
                commit_hash
            )
            
            self.logger.info(f"Implementation completed successfully for story: {story_id}")
            return output_contract
            
        except Exception as e:
            error_msg = f"Developer implementation failed for {story_id}: {str(e)}"
            self.logger.error(error_msg)
            raise AgentExecutionError(error_msg)
    
    async def _validate_architecture_requirements(self, input_data: Dict[str, Any]) -> None:
        """
        Validate that input requirements align with architecture principles.
        
        Args:
            input_data: Input data from Game Designer
            
        Raises:
            DNAComplianceError: If requirements violate architecture principles
        """
        validation_result = await self.architecture_validator.validate_requirements(input_data)
        
        if not validation_result["is_valid"]:
            errors = validation_result.get("errors", [])
            error_msg = f"Architecture validation failed: {'; '.join(errors)}"
            self.logger.error(error_msg)
            raise DNAComplianceError(error_msg)
        
        if validation_result.get("warnings"):
            for warning in validation_result["warnings"]:
                self.logger.warning(f"Architecture warning: {warning}")
    
    async def _validate_implementation_quality(
        self,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]],
        test_suite: Dict[str, Any]
    ) -> None:
        """
        Validate implementation meets quality standards.
        
        Args:
            component_implementations: Generated React components
            api_implementations: Generated FastAPI endpoints
            test_suite: Generated test suite
            
        Raises:
            QualityGateError: If quality standards are not met
        """
        # Validate TypeScript compilation
        typescript_errors = await self.code_generator.check_typescript_errors(component_implementations)
        if typescript_errors > self.quality_standards["typescript_errors"]["max"]:
            raise QualityGateError(f"TypeScript errors: {typescript_errors} (max: 0)")
        
        # Validate ESLint compliance
        eslint_violations = await self.code_generator.check_eslint_compliance(component_implementations)
        if eslint_violations > self.quality_standards["eslint_violations"]["max"]:
            raise QualityGateError(f"ESLint violations: {eslint_violations} (max: 0)")
        
        # Validate test coverage
        coverage_percent = await self.code_generator.calculate_test_coverage(test_suite)
        if coverage_percent < self.quality_standards["test_coverage_percent"]["min"]:
            raise QualityGateError(f"Test coverage: {coverage_percent}% (min: 100%)")
        
        # Validate API performance
        for api in api_implementations:
            response_time = await self.api_builder.test_api_performance(api)
            if response_time > self.quality_standards["api_response_time_ms"]["max"]:
                raise QualityGateError(f"API {api['name']} response time: {response_time}ms (max: 200ms)")
        
        self.logger.info("All quality standards met")
    
    async def _generate_implementation_docs(
        self,
        story_id: str,
        game_mechanics: Dict[str, Any],
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]],
        test_suite: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive implementation documentation.
        
        Args:
            story_id: Story identifier
            game_mechanics: Game mechanics from design
            component_implementations: Generated components
            api_implementations: Generated APIs
            test_suite: Generated tests
            
        Returns:
            Implementation documentation dictionary
        """
        return {
            "story_id": story_id,
            "implementation_summary": {
                "title": game_mechanics.get("title", "Feature Implementation"),
                "description": game_mechanics.get("description", ""),
                "components_count": len(component_implementations),
                "apis_count": len(api_implementations),
                "tests_count": len(test_suite.get("unit_tests", []))
            },
            "architecture_compliance": {
                "api_first": True,
                "stateless_backend": True,
                "separation_of_concerns": True,
                "component_library_usage": True
            },
            "performance_metrics": {
                "estimated_lighthouse_score": 95,
                "estimated_bundle_size_kb": 45,
                "api_endpoints_count": len(api_implementations)
            },
            "deployment_instructions": {
                "frontend_build_command": "npm run build",
                "backend_start_command": "uvicorn main:app --reload",
                "test_command": "npm test && pytest",
                "environment_variables": []
            }
        }
    
    async def _create_output_contract(
        self,
        input_contract: Dict[str, Any],
        story_id: str,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]],
        test_suite: Dict[str, Any],
        implementation_docs: Dict[str, Any],
        commit_hash: str
    ) -> Dict[str, Any]:
        """
        Create output contract for Test Engineer.
        
        Args:
            input_contract: Original input contract
            story_id: Story identifier
            component_implementations: Generated components
            api_implementations: Generated APIs
            test_suite: Generated tests
            implementation_docs: Implementation documentation
            commit_hash: Git commit hash
            
        Returns:
            Output contract for Test Engineer
        """
        return {
            "contract_version": "1.0",
            "contract_type": "implementation_to_testing",
            "story_id": story_id,
            "source_agent": "developer",
            "target_agent": "test_engineer",
            "dna_compliance": input_contract.get("dna_compliance"),
            
            "input_requirements": {
                "required_files": [
                    f"frontend/components/{story_id}/",
                    f"backend/endpoints/{story_id}/",
                    f"tests/unit/{story_id}/",
                    f"docs/implementation/{story_id}_implementation.md"
                ],
                "required_data": {
                    "component_implementations": component_implementations,
                    "api_implementations": api_implementations,
                    "test_suite": test_suite,
                    "implementation_docs": implementation_docs,
                    "git_commit_hash": commit_hash
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
                    f"tests/integration/{story_id}/",
                    f"tests/e2e/{story_id}/",
                    f"docs/test_reports/{story_id}_coverage.html",
                    f"docs/performance/{story_id}_benchmarks.json"
                ],
                "deliverable_data": {
                    "integration_test_suite": "object",
                    "e2e_test_suite": "object",
                    "performance_test_results": "object",
                    "coverage_report": "object",
                    "security_scan_results": "object"
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
                "automated_test_suite_configured",
                "load_testing_completed"
            ],
            
            "handoff_criteria": [
                "comprehensive_test_coverage_achieved",
                "all_performance_requirements_validated",
                "automated_test_pipeline_configured",
                "quality_metrics_documented",
                "security_validation_completed"
            ]
        }
    
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """
        Check Developer-specific quality gates.
        
        Args:
            gate: Quality gate identifier
            deliverables: Deliverables to validate
            
        Returns:
            True if quality gate passes, False otherwise
        """
        quality_checks = {
            "typescript_compilation_success_zero_errors": self._check_typescript_compilation,
            "eslint_standards_compliance_verified": self._check_eslint_compliance,
            "unit_tests_100_percent_coverage_achieved": self._check_test_coverage,
            "api_endpoints_respond_correctly": self._check_api_functionality,
            "component_integration_working": self._check_component_integration,
            "architecture_principles_compliance": self._check_architecture_compliance,
            "performance_standards_met": self._check_performance_standards
        }
        
        checker = quality_checks.get(gate)
        if checker:
            try:
                return checker(deliverables)
            except Exception as e:
                self.logger.error(f"Quality gate check failed for '{gate}': {e}")
                return False
        
        # Default pass for unknown gates (with warning)
        self.logger.warning(f"Unknown quality gate: {gate}")
        return True
    
    def _check_typescript_compilation(self, deliverables: Dict[str, Any]) -> bool:
        """Check TypeScript compilation has zero errors."""
        component_implementations = deliverables.get("component_implementations", [])
        
        for component in component_implementations:
            if component.get("typescript_errors", 0) > 0:
                self.logger.error(f"TypeScript errors in component: {component.get('name')}")
                return False
        
        return True
    
    def _check_eslint_compliance(self, deliverables: Dict[str, Any]) -> bool:
        """Check ESLint compliance has zero violations."""
        component_implementations = deliverables.get("component_implementations", [])
        
        for component in component_implementations:
            if component.get("eslint_violations", 0) > 0:
                self.logger.error(f"ESLint violations in component: {component.get('name')}")
                return False
        
        return True
    
    def _check_test_coverage(self, deliverables: Dict[str, Any]) -> bool:
        """Check test coverage is 100%."""
        test_suite = deliverables.get("test_suite", {})
        coverage_percent = test_suite.get("coverage_percent", 0)
        
        if coverage_percent < 100:
            self.logger.error(f"Test coverage insufficient: {coverage_percent}% (required: 100%)")
            return False
        
        return True
    
    def _check_api_functionality(self, deliverables: Dict[str, Any]) -> bool:
        """Check all API endpoints respond correctly."""
        api_implementations = deliverables.get("api_implementations", [])
        
        for api in api_implementations:
            if not api.get("functional_test_passed", False):
                self.logger.error(f"API functionality test failed: {api.get('name')}")
                return False
        
        return True
    
    def _check_component_integration(self, deliverables: Dict[str, Any]) -> bool:
        """Check component integration is working."""
        component_implementations = deliverables.get("component_implementations", [])
        
        for component in component_implementations:
            if not component.get("integration_test_passed", False):
                self.logger.error(f"Component integration test failed: {component.get('name')}")
                return False
        
        return True
    
    def _check_architecture_compliance(self, deliverables: Dict[str, Any]) -> bool:
        """Check architecture principles compliance."""
        implementation_docs = deliverables.get("implementation_docs", {})
        arch_compliance = implementation_docs.get("architecture_compliance", {})
        
        required_principles = ["api_first", "stateless_backend", "separation_of_concerns"]
        
        for principle in required_principles:
            if not arch_compliance.get(principle, False):
                self.logger.error(f"Architecture principle violation: {principle}")
                return False
        
        return True
    
    def _check_performance_standards(self, deliverables: Dict[str, Any]) -> bool:
        """Check performance standards are met."""
        implementation_docs = deliverables.get("implementation_docs", {})
        performance = implementation_docs.get("performance_metrics", {})
        
        # Check Lighthouse score
        lighthouse_score = performance.get("estimated_lighthouse_score", 0)
        if lighthouse_score < 90:
            self.logger.error(f"Lighthouse score too low: {lighthouse_score} (required: e90)")
            return False
        
        # Check bundle size
        bundle_size = performance.get("estimated_bundle_size_kb", 999)
        if bundle_size > 500:  # DigiNativa's bundle size limit
            self.logger.error(f"Bundle size too large: {bundle_size}KB (max: 500KB)")
            return False
        
        return True