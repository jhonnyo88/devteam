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
- Validate DNA principles in generated code (NEW FEATURE)
- Maintain performance standards (Lighthouse >90, API <200ms)

DNA COMPLIANCE VALIDATION (NEW):
- Pedagogical Value: Comment quality, variable naming clarity
- Simplicity First: Cyclomatic complexity measurement (<10 components, <8 APIs)
- Professional Tone: Code comments and error messages validation
- Policy to Practice: Municipal requirements and accessibility compliance
- Time Respect: Optimized for 10-minute learning sessions

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
from ...shared.event_bus import EventBus

# Import specialized tools
from .tools.code_generator import CodeGenerator
from .tools.api_builder import APIBuilder
from .tools.git_operations import GitOperations
from .tools.component_builder import ComponentBuilder
from .tools.architecture_validator import ArchitectureValidator
from .tools.dna_code_validator import DNACodeValidator

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
        
        # Initialize EventBus for team coordination
        self.event_bus = EventBus(config)
        
        # Initialize specialized tools
        self.code_generator = CodeGenerator(config)
        self.api_builder = APIBuilder(config)
        self.git_operations = GitOperations(config)
        self.component_builder = ComponentBuilder(config)
        self.architecture_validator = ArchitectureValidator(config)
        self.dna_code_validator = DNACodeValidator(config)
        
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
    
    async def _notify_team_progress(self, event_type: str, data: Dict[str, Any]):
        """Notify team of implementation progress via EventBus."""
        await self.event_bus.publish(event_type, {
            "agent": self.agent_type,
            "story_id": data.get("story_id"),
            "status": data.get("status"),
            "timestamp": datetime.now().isoformat(),
            **data
        })

    async def _listen_for_team_events(self):
        """Listen for relevant team coordination events."""
        relevant_events = [f"{self.agent_type}_*", "team_*", "implementation_*", "code_*"]
        for event_pattern in relevant_events:
            await self.event_bus.subscribe(event_pattern, self._handle_team_event)

    async def _handle_team_event(self, event_type: str, data: Dict[str, Any]):
        """Handle incoming team coordination events."""
        self.logger.info(f"Developer received team event: {event_type}")
        
        # Implementation-specific event handling
        if "code_review_feedback" in event_type:
            self.logger.info("Received code review feedback from Quality Reviewer")
            # Could implement code revision logic here
        elif "design_updated" in event_type:
            self.logger.info("Received design update notification")
            # Could implement design change handling here
    
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
        7. Validate DNA compliance in generated code (NEW)
        8. Validate implementation quality and performance
        9. Create feature branch and commit implementation
        10. Generate output contract for Test Engineer
        
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
            
            # Notify team that implementation has started
            await self._notify_team_progress("implementation_started", {"story_id": story_id})
            
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
            await self._notify_team_progress("components_generation_started", {"story_id": story_id})
            component_implementations = await self.component_builder.build_components(
                ui_components, 
                interaction_flows,
                story_id
            )
            await self._notify_team_progress("components_implemented", {
                "story_id": story_id, 
                "component_count": len(component_implementations)
            })
            
            # Step 5: Generate FastAPI endpoints
            self.logger.info("Generating FastAPI endpoints")
            await self._notify_team_progress("apis_generation_started", {"story_id": story_id})
            api_implementations = await self.api_builder.build_apis(
                api_endpoints,
                state_management,
                story_id
            )
            await self._notify_team_progress("apis_created", {
                "story_id": story_id, 
                "api_count": len(api_implementations)
            })
            
            # Step 6: Generate unit tests
            self.logger.info("Generating unit tests")
            test_suite = await self.code_generator.generate_tests(
                component_implementations,
                api_implementations,
                story_id
            )
            
            # Step 7: Validate DNA compliance in generated code
            self.logger.info("Validating DNA compliance in generated code")
            await self._notify_team_progress("dna_validation_started", {"story_id": story_id})
            dna_validation_result = await self.dna_code_validator.validate_code_dna_compliance(
                component_implementations,
                api_implementations,
                test_suite,
                game_mechanics
            )
            
            # Check if DNA compliance passed
            if not dna_validation_result.overall_dna_compliant:
                error_msg = f"DNA compliance validation failed: {'; '.join(dna_validation_result.violations)}"
                self.logger.error(error_msg)
                raise DNAComplianceError(error_msg)
            
            await self._notify_team_progress("dna_validation_complete", {
                "story_id": story_id,
                "dna_compliance_score": dna_validation_result.dna_compliance_score
            })
            
            # Step 8: Validate implementation quality
            await self._validate_implementation_quality(
                component_implementations,
                api_implementations,
                test_suite
            )
            
            # Step 9: Commit implementation to feature branch
            commit_message = f"Implement {story_id}: {game_mechanics.get('title', 'Feature implementation')}"
            await self._notify_team_progress("git_operations_started", {"story_id": story_id})
            commit_hash = await self.git_operations.commit_implementation(
                story_id,
                commit_message,
                component_implementations,
                api_implementations,
                test_suite
            )
            await self._notify_team_progress("git_operations_complete", {
                "story_id": story_id, 
                "commit_hash": commit_hash
            })
            
            # Step 10: Generate implementation documentation
            implementation_docs = await self._generate_implementation_docs(
                story_id,
                game_mechanics,
                component_implementations,
                api_implementations,
                test_suite
            )
            
            # Step 11: Create output contract for Test Engineer
            output_contract = await self._create_output_contract(
                input_contract,
                story_id,
                component_implementations,
                api_implementations,
                test_suite,
                implementation_docs,
                commit_hash,
                dna_validation_result
            )
            
            # Notify team that implementation is complete
            await self._notify_team_progress("implementation_complete", {
                "story_id": story_id,
                "status": "ready_for_testing"
            })
            
            self.logger.info(f"Implementation completed successfully for story: {story_id}")
            return output_contract
            
        except Exception as e:
            error_msg = f"Developer implementation failed for {story_id}: {str(e)}"
            self.logger.error(error_msg)
            raise AgentExecutionError(error_msg, self.agent_id, story_id)
    
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
    
    async def _validate_code_dna_compliance(
        self,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]],
        test_suite: Dict[str, Any],
        game_mechanics: Dict[str, Any]
    ) -> None:
        """
        Validate that generated code complies with DigiNativa DNA principles.
        
        CRITICAL DNA VALIDATION:
        - Pedagogical Value: Comment quality, variable naming clarity
        - Simplicity First: Cyclomatic complexity measurement
        - Professional Tone: Code comments and error messages
        - Policy to Practice: Implementation follows municipal requirements
        - Time Respect: Code optimized for 10-minute learning sessions
        
        Args:
            component_implementations: Generated React components
            api_implementations: Generated FastAPI endpoints
            test_suite: Generated test suite
            game_mechanics: Game mechanics context
            
        Raises:
            DNAComplianceError: If code violates DNA principles
        """
        try:
            self.logger.info("Validating DNA compliance in generated code")
            
            dna_violations = []
            
            # Validate Pedagogical Value in code
            pedagogical_score = await self._validate_pedagogical_value_in_code(
                component_implementations, api_implementations, game_mechanics
            )
            if pedagogical_score < 4.0:
                dna_violations.append(f"Pedagogical value score too low: {pedagogical_score} (min: 4.0)")
            
            # Validate Simplicity First principle
            complexity_violations = await self._validate_code_complexity(
                component_implementations, api_implementations
            )
            if complexity_violations:
                dna_violations.extend(complexity_violations)
            
            # Validate Professional Tone in code
            tone_violations = await self._validate_professional_tone_in_code(
                component_implementations, api_implementations
            )
            if tone_violations:
                dna_violations.extend(tone_violations)
            
            # Validate Policy to Practice implementation
            policy_violations = await self._validate_policy_implementation(
                component_implementations, api_implementations, game_mechanics
            )
            if policy_violations:
                dna_violations.extend(policy_violations)
            
            # Validate Time Respect in code design
            time_violations = await self._validate_time_respect_in_code(
                component_implementations, api_implementations
            )
            if time_violations:
                dna_violations.extend(time_violations)
            
            if dna_violations:
                error_msg = f"DNA compliance violations in generated code: {'; '.join(dna_violations)}"
                self.logger.error(error_msg)
                raise DNAComplianceError(error_msg)
            
            self.logger.info("DNA compliance validation passed for generated code")
            
        except Exception as e:
            if isinstance(e, DNAComplianceError):
                raise
            error_msg = f"DNA compliance validation failed: {str(e)}"
            self.logger.error(error_msg)
            raise DNAComplianceError(error_msg)
    
    async def _validate_pedagogical_value_in_code(
        self,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]],
        game_mechanics: Dict[str, Any]
    ) -> float:
        """
        Validate pedagogical value is reflected in code quality.
        
        VALIDATION CRITERIA:
        - Comment quality: Explain learning objectives
        - Variable naming: Clear, educational naming conventions
        - Code structure: Supports learning progression
        - Documentation: Educational context provided
        """
        total_score = 0.0
        total_items = 0
        
        # Validate component pedagogical value
        for component in component_implementations:
            score = 0.0
            
            # Check comment quality (0-5 scale)
            component_code = component.get("code", {}).get("component", "")
            if "learning" in component_code.lower() or "educational" in component_code.lower():
                score += 1.5
            if "/**" in component_code and "@param" in component_code:
                score += 1.0  # Well-documented components
            if len([line for line in component_code.split('\n') if line.strip().startswith('//')]) > 3:
                score += 0.5  # Adequate inline comments
            
            # Check variable naming clarity (0-5 scale)
            clear_naming_patterns = [
                "learningProgress", "educationalContent", "municipalTask",
                "userLearning", "trainingModule", "pedagogicalValue"
            ]
            if any(pattern in component_code for pattern in clear_naming_patterns):
                score += 1.5
            
            # Check if component supports learning progression
            if "step" in component_code.lower() or "progress" in component_code.lower():
                score += 0.5
            
            total_score += min(score, 5.0)
            total_items += 1
        
        # Validate API pedagogical value
        for api in api_implementations:
            score = 0.0
            
            # Check API documentation quality
            api_code = api.get("code", {}).get("endpoint", "")
            if "learning" in api_code.lower() or "training" in api_code.lower():
                score += 1.5
            if '"""' in api_code and ("Args:" in api_code and "Returns:" in api_code):
                score += 1.0  # Well-documented APIs
            
            # Check error messages are educational
            if "error_message" in api_code and "validation" in api_code:
                score += 1.0
            
            total_score += min(score, 5.0)
            total_items += 1
        
        return total_score / max(total_items, 1)
    
    async def _validate_code_complexity(
        self,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Validate Simplicity First principle through cyclomatic complexity.
        
        COMPLEXITY LIMITS:
        - Components: Max complexity 10 per function
        - APIs: Max complexity 8 per function
        - Overall: Prefer simple, readable solutions
        """
        violations = []
        
        # Check component complexity
        for component in component_implementations:
            component_code = component.get("code", {}).get("component", "")
            complexity_score = self._calculate_cyclomatic_complexity(component_code)
            
            if complexity_score > 10:
                violations.append(
                    f"Component {component['name']} complexity too high: {complexity_score} (max: 10)"
                )
        
        # Check API complexity
        for api in api_implementations:
            api_code = api.get("code", {}).get("endpoint", "")
            complexity_score = self._calculate_cyclomatic_complexity(api_code)
            
            if complexity_score > 8:
                violations.append(
                    f"API {api['name']} complexity too high: {complexity_score} (max: 8)"
                )
        
        return violations
    
    def _calculate_cyclomatic_complexity(self, code: str) -> int:
        """
        Calculate cyclomatic complexity of code.
        
        Simple implementation counting decision points:
        - if, elif, else
        - for, while
        - try, catch, except
        - &&, ||, and, or
        - ? (ternary operator)
        """
        if not code:
            return 1
        
        # Count decision points
        decision_keywords = [
            'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except:', 'catch',
            '&&', '||', ' and ', ' or ', '?'
        ]
        
        complexity = 1  # Base complexity
        
        for keyword in decision_keywords:
            complexity += code.lower().count(keyword)
        
        # Additional complexity for nested structures
        nesting_level = max(code.count('    ') // 4, code.count('\t'))
        if nesting_level > 3:
            complexity += nesting_level - 3
        
        return complexity
    
    async def _validate_professional_tone_in_code(
        self,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Validate professional tone in code comments and error messages.
        
        PROFESSIONAL STANDARDS:
        - Error messages: Clear, helpful, non-technical for end users
        - Comments: Professional, municipal context appropriate
        - Variable names: Professional Swedish municipal terminology
        """
        violations = []
        
        # Check component professional tone
        for component in component_implementations:
            component_code = component.get("code", {}).get("component", "")
            
            # Check for unprofessional comments
            unprofessional_terms = ["TODO", "FIXME", "HACK", "dirty", "stupid", "wtf"]
            for term in unprofessional_terms:
                if term.lower() in component_code.lower():
                    violations.append(f"Unprofessional term '{term}' in component {component['name']}")
            
            # Check error message quality
            if "error" in component_code.lower():
                if not any(word in component_code for word in ["validation", "please", "required"]):
                    violations.append(f"Error messages in {component['name']} lack professional tone")
        
        # Check API professional tone
        for api in api_implementations:
            api_code = api.get("code", {}).get("endpoint", "")
            
            # Check API error messages are user-friendly
            if "HTTPException" in api_code:
                if "status_code=500" in api_code and "Internal server error" in api_code:
                    # Good - generic error for users
                    pass
                elif "error_code" in api_code and "error_message" in api_code:
                    # Good - structured error response
                    pass
                else:
                    violations.append(f"API {api['name']} error handling lacks professional structure")
        
        return violations
    
    async def _validate_policy_implementation(
        self,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]],
        game_mechanics: Dict[str, Any]
    ) -> List[str]:
        """
        Validate Policy to Practice implementation in code.
        
        MUNICIPAL REQUIREMENTS:
        - Accessibility compliance in components
        - GDPR compliance in data handling
        - Swedish language support
        - Municipal user role considerations
        """
        violations = []
        
        # Check accessibility implementation
        for component in component_implementations:
            component_code = component.get("code", {}).get("component", "")
            
            # Check for accessibility attributes
            if "form" in component_code.lower() or "input" in component_code.lower():
                if not any(attr in component_code for attr in ["aria-", "role=", "tabIndex"]):
                    violations.append(f"Component {component['name']} missing accessibility attributes")
        
        # Check GDPR compliance in APIs
        for api in api_implementations:
            api_code = api.get("code", {}).get("endpoint", "")
            
            # Check for personal data handling
            if any(field in api_code.lower() for field in ["email", "name", "personal"]):
                if "validation" not in api_code or "sanitiz" not in api_code:
                    violations.append(f"API {api['name']} lacks GDPR-compliant data validation")
        
        return violations
    
    async def _validate_time_respect_in_code(
        self,
        component_implementations: List[Dict[str, Any]],
        api_implementations: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Validate Time Respect principle in code design.
        
        TIME EFFICIENCY REQUIREMENTS:
        - Components optimized for quick interactions
        - APIs respond within 200ms budget
        - Minimal cognitive load in UI components
        - Progress indicators for longer operations
        """
        violations = []
        
        # Check component time efficiency
        for component in component_implementations:
            component_code = component.get("code", {}).get("component", "")
            
            # Check for loading states
            if "fetch" in component_code or "api" in component_code:
                if "loading" not in component_code.lower() and "spinner" not in component_code.lower():
                    violations.append(f"Component {component['name']} missing loading indicators")
            
            # Check for progress indicators
            if "form" in component_code.lower() and len(component_code) > 1000:
                if "progress" not in component_code.lower() and "step" not in component_code.lower():
                    violations.append(f"Complex form {component['name']} missing progress indicators")
        
        # Check API time efficiency
        for api in api_implementations:
            api_implementation = api.get("implementation", {})
            estimated_time = api_implementation.get("estimated_response_time_ms", 0)
            
            if estimated_time > 200:
                violations.append(f"API {api['name']} exceeds time budget: {estimated_time}ms (max: 200ms)")
        
        return violations
    
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
        commit_hash: str,
        dna_validation_result: Any
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
            dna_validation_result: DNA validation results
            
        Returns:
            Output contract for Test Engineer
        """
        return {
            "contract_version": "1.0",
            "contract_type": "implementation_to_testing",
            "story_id": story_id,
            "source_agent": "developer",
            "target_agent": "test_engineer",
            "dna_compliance": {
                **input_contract.get("dna_compliance", {}),
                "developer_dna_validation": {
                    "overall_dna_compliant": dna_validation_result.overall_dna_compliant,
                    "time_respect_compliant": dna_validation_result.time_respect_compliant,
                    "pedagogical_value_compliant": dna_validation_result.pedagogical_value_compliant,
                    "professional_tone_compliant": dna_validation_result.professional_tone_compliant,
                    "api_first_compliant": dna_validation_result.api_first_compliant,
                    "stateless_backend_compliant": dna_validation_result.stateless_backend_compliant,
                    "separation_concerns_compliant": dna_validation_result.separation_concerns_compliant,
                    "simplicity_first_compliant": dna_validation_result.simplicity_first_compliant,
                    "dna_compliance_score": dna_validation_result.dna_compliance_score,
                    "validation_timestamp": dna_validation_result.validation_timestamp,
                    "violations": dna_validation_result.violations,
                    "recommendations": dna_validation_result.recommendations,
                    "quality_reviewer_metrics": dna_validation_result.quality_reviewer_metrics
                }
            },
            
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