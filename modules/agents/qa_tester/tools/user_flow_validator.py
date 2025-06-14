"""
UserFlowValidator - User interaction flow validation and testing tool.

PURPOSE:
Validates that user interaction flows work correctly, are intuitive,
and provide optimal user experience for Anna persona and municipal users.

CRITICAL FUNCTIONALITY:
- User journey mapping and validation
- Interaction pattern verification
- Task completion flow testing
- Error handling and recovery validation
- Navigation consistency checking
- User goal achievement assessment

ADAPTATION GUIDE:
=' To adapt for your project:
1. Update user_flows for your specific workflows
2. Modify validation_criteria for your quality standards
3. Adjust flow_patterns for your interface design
4. Update success_metrics for your user goals

CONTRACT PROTECTION:
This tool is critical for DigiNativa's user experience validation.
Changes must maintain flow validation consistency.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from enum import Enum


# Setup logging for this module
logger = logging.getLogger(__name__)


class FlowStepType(Enum):
    """Types of user flow steps."""
    NAVIGATION = "navigation"
    INPUT = "input"
    SELECTION = "selection"
    CONFIRMATION = "confirmation"
    VALIDATION = "validation"
    COMPLETION = "completion"
    ERROR_HANDLING = "error_handling"


class FlowValidationResult(Enum):
    """Flow validation results."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class FlowStep:
    """
    Represents a single step in a user flow.
    """
    step_id: str
    step_type: FlowStepType
    description: str
    expected_elements: List[str]
    required_actions: List[str]
    success_criteria: Dict[str, Any]
    error_conditions: List[str]
    accessibility_requirements: List[str]
    time_limit_seconds: Optional[float] = None
    depends_on: Optional[str] = None


@dataclass
class UserFlow:
    """
    Represents a complete user flow/journey.
    """
    flow_id: str
    name: str
    description: str
    user_goal: str
    persona: str
    priority: str  # "critical", "high", "medium", "low"
    steps: List[FlowStep]
    expected_completion_time_minutes: float
    alternative_paths: List[str]
    error_recovery_paths: List[str]


@dataclass
class FlowValidationIssue:
    """
    Represents an issue found during flow validation.
    """
    issue_id: str
    flow_id: str
    step_id: Optional[str]
    severity: str  # "critical", "high", "medium", "low"
    category: str
    description: str
    impact_on_user: str
    recommended_fix: str
    affects_accessibility: bool
    affects_anna_persona: bool


@dataclass
class FlowStepValidationResult:
    """
    Results from validating a single flow step.
    """
    step_id: str
    validation_result: FlowValidationResult
    completion_time_seconds: float
    issues_found: List[FlowValidationIssue]
    accessibility_score: float
    user_experience_score: float
    success_rate: float
    details: Dict[str, Any]


class UserFlowValidator:
    """
    Validates user interaction flows and journeys for optimal user experience.
    
    Focuses on ensuring that Anna persona and other municipal users can
    complete their tasks efficiently and intuitively.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize UserFlowValidator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Standard municipal user flows for DigiNativa
        self.standard_flows = self._initialize_standard_flows()
        
        # Validation criteria for flows
        self.flow_validation_criteria = {
            "max_steps_per_flow": 7,  # Maximum steps before complexity becomes issue
            "max_completion_time_minutes": 10,  # Anna's time constraint
            "min_success_rate_percentage": 95,
            "max_error_recovery_steps": 3,
            "required_accessibility_score": 90,
            "required_user_experience_score": 4.0
        }
        
        # Anna persona flow requirements
        self.anna_flow_requirements = {
            "max_cognitive_load": 5,  # Scale 1-10
            "clear_progress_indication": True,
            "consistent_navigation": True,
            "predictable_interactions": True,
            "helpful_error_messages": True,
            "quick_task_completion": True,
            "professional_appearance": True
        }
        
        # Common flow patterns to validate
        self.flow_patterns = {
            "linear_progression": {
                "description": "Simple step-by-step progression",
                "suitable_for": ["data_entry", "registration", "simple_tasks"],
                "anna_preference": "high"
            },
            "hub_and_spoke": {
                "description": "Central hub with branching options",
                "suitable_for": ["dashboards", "menu_systems"],
                "anna_preference": "medium"
            },
            "wizard_flow": {
                "description": "Guided multi-step process",
                "suitable_for": ["complex_forms", "setup_processes"],
                "anna_preference": "high"
            },
            "free_form": {
                "description": "Non-linear, user-directed flow",
                "suitable_for": ["content_browsing", "exploration"],
                "anna_preference": "low"
            }
        }
        
        logger.info("UserFlowValidator initialized with DigiNativa flow standards")
    
    def _initialize_standard_flows(self) -> List[UserFlow]:
        """
        Initialize standard user flows for DigiNativa municipal training.
        
        Returns:
            List of standard user flows
        """
        flows = []
        
        # Registration/Login Flow
        registration_flow = UserFlow(
            flow_id="municipal_user_registration",
            name="Municipal User Registration",
            description="New municipal employee registers for training access",
            user_goal="Create account and access training materials",
            persona="Anna",
            priority="critical",
            steps=[
                FlowStep(
                    step_id="navigate_to_registration",
                    step_type=FlowStepType.NAVIGATION,
                    description="Navigate to registration page",
                    expected_elements=["registration_link", "sign_up_button"],
                    required_actions=["click_registration_link"],
                    success_criteria={"page_loads": True, "form_visible": True},
                    error_conditions=["page_not_found", "broken_link"],
                    accessibility_requirements=["keyboard_accessible", "screen_reader_compatible"]
                ),
                FlowStep(
                    step_id="enter_basic_information",
                    step_type=FlowStepType.INPUT,
                    description="Enter name, email, and role information",
                    expected_elements=["name_field", "email_field", "role_dropdown"],
                    required_actions=["fill_name", "fill_email", "select_role"],
                    success_criteria={"all_fields_filled": True, "validation_passes": True},
                    error_conditions=["invalid_email", "missing_required_fields"],
                    accessibility_requirements=["proper_labels", "error_messages_accessible"]
                ),
                FlowStep(
                    step_id="verify_and_submit",
                    step_type=FlowStepType.CONFIRMATION,
                    description="Review information and submit registration",
                    expected_elements=["review_section", "submit_button", "terms_checkbox"],
                    required_actions=["review_info", "accept_terms", "click_submit"],
                    success_criteria={"submission_successful": True, "confirmation_shown": True},
                    error_conditions=["submission_failed", "terms_not_accepted"],
                    accessibility_requirements=["clear_confirmation", "success_message_announced"]
                )
            ],
            expected_completion_time_minutes=3.0,
            alternative_paths=["social_login", "organization_sso"],
            error_recovery_paths=["password_reset", "support_contact"]
        )
        flows.append(registration_flow)
        
        # Training Module Access Flow
        training_access_flow = UserFlow(
            flow_id="training_module_access",
            name="Training Module Access",
            description="User navigates to and accesses specific training module",
            user_goal="Access and begin training module on policy compliance",
            persona="Anna",
            priority="high",
            steps=[
                FlowStep(
                    step_id="login_to_system",
                    step_type=FlowStepType.INPUT,
                    description="Login with credentials",
                    expected_elements=["login_form", "username_field", "password_field"],
                    required_actions=["enter_username", "enter_password", "click_login"],
                    success_criteria={"authentication_successful": True, "dashboard_loaded": True},
                    error_conditions=["invalid_credentials", "account_locked"],
                    accessibility_requirements=["password_masking", "error_announcement"]
                ),
                FlowStep(
                    step_id="navigate_to_training",
                    step_type=FlowStepType.NAVIGATION,
                    description="Navigate to training section",
                    expected_elements=["training_menu", "module_list"],
                    required_actions=["click_training_menu"],
                    success_criteria={"training_section_loaded": True, "modules_visible": True},
                    error_conditions=["menu_broken", "modules_not_loading"],
                    accessibility_requirements=["keyboard_navigation", "focus_management"]
                ),
                FlowStep(
                    step_id="select_module",
                    step_type=FlowStepType.SELECTION,
                    description="Select specific training module",
                    expected_elements=["module_cards", "module_descriptions", "start_button"],
                    required_actions=["review_modules", "select_target_module", "click_start"],
                    success_criteria={"module_selected": True, "content_loading": True},
                    error_conditions=["module_unavailable", "access_denied"],
                    accessibility_requirements=["clear_descriptions", "selection_announced"]
                ),
                FlowStep(
                    step_id="begin_training",
                    step_type=FlowStepType.COMPLETION,
                    description="Begin training module content",
                    expected_elements=["content_area", "progress_indicator", "navigation_controls"],
                    required_actions=["start_content"],
                    success_criteria={"content_displayed": True, "progress_tracking": True},
                    error_conditions=["content_not_loading", "progress_not_tracked"],
                    accessibility_requirements=["content_structure", "progress_announced"]
                )
            ],
            expected_completion_time_minutes=2.5,
            alternative_paths=["direct_module_link", "search_for_module"],
            error_recovery_paths=["retry_login", "password_reset", "contact_support"]
        )
        flows.append(training_access_flow)
        
        # Task Completion and Feedback Flow
        task_completion_flow = UserFlow(
            flow_id="task_completion_feedback",
            name="Task Completion and Feedback",
            description="User completes training task and provides feedback",
            user_goal="Complete exercise and submit feedback for improvement",
            persona="Anna",
            priority="medium",
            steps=[
                FlowStep(
                    step_id="complete_exercise",
                    step_type=FlowStepType.INPUT,
                    description="Complete training exercise or assessment",
                    expected_elements=["exercise_content", "submission_form", "submit_button"],
                    required_actions=["complete_exercise", "submit_responses"],
                    success_criteria={"responses_submitted": True, "validation_passed": True},
                    error_conditions=["incomplete_responses", "validation_failed"],
                    accessibility_requirements=["form_accessibility", "validation_messages"]
                ),
                FlowStep(
                    step_id="provide_feedback",
                    step_type=FlowStepType.INPUT,
                    description="Provide feedback on training experience",
                    expected_elements=["feedback_form", "rating_system", "comment_field"],
                    required_actions=["rate_experience", "provide_comments"],
                    success_criteria={"feedback_submitted": True, "confirmation_received": True},
                    error_conditions=["submission_failed", "missing_required_feedback"],
                    accessibility_requirements=["accessible_rating", "comment_field_labeled"]
                ),
                FlowStep(
                    step_id="view_results",
                    step_type=FlowStepType.COMPLETION,
                    description="View completion results and next steps",
                    expected_elements=["results_summary", "next_steps", "return_link"],
                    required_actions=["review_results"],
                    success_criteria={"results_displayed": True, "next_steps_clear": True},
                    error_conditions=["results_not_available", "unclear_next_steps"],
                    accessibility_requirements=["results_announced", "clear_structure"]
                )
            ],
            expected_completion_time_minutes=5.0,
            alternative_paths=["skip_feedback", "save_for_later"],
            error_recovery_paths=["retry_submission", "contact_instructor"]
        )
        flows.append(task_completion_flow)
        
        return flows
    
    async def validate_user_flows(self, story_id: str, implementation_data: Dict[str, Any],
                                persona_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user flows for implemented feature.
        
        Args:
            story_id: Story identifier
            implementation_data: Feature implementation details
            persona_requirements: Anna persona requirements
            
        Returns:
            Comprehensive user flow validation results
        """
        try:
            logger.info(f"Starting user flow validation for story: {story_id}")
            
            # Extract flow-related data from implementation
            ui_components = implementation_data.get("ui_components", [])
            user_flows = implementation_data.get("user_flows", [])
            navigation_structure = implementation_data.get("navigation_structure", {})
            
            # Identify applicable flows for this feature
            applicable_flows = await self._identify_applicable_flows(
                implementation_data, story_id
            )
            
            # Validate each applicable flow
            flow_validation_results = []
            
            for flow in applicable_flows:
                logger.debug(f"Validating flow: {flow.name}")
                
                flow_result = await self._validate_single_flow(
                    flow=flow,
                    implementation_data=implementation_data,
                    persona_requirements=persona_requirements
                )
                
                flow_validation_results.append(flow_result)
            
            # Analyze overall flow patterns
            pattern_analysis = await self._analyze_flow_patterns(
                flow_validation_results, implementation_data
            )
            
            # Validate navigation consistency
            navigation_validation = await self._validate_navigation_consistency(
                navigation_structure, ui_components
            )
            
            # Assess Anna persona compatibility
            anna_compatibility = await self._assess_anna_persona_compatibility(
                flow_validation_results, persona_requirements
            )
            
            # Calculate overall metrics
            overall_metrics = self._calculate_flow_metrics(flow_validation_results)
            
            # Generate recommendations
            recommendations = await self._generate_flow_recommendations(
                flow_validation_results, pattern_analysis, anna_compatibility
            )
            
            # Create comprehensive validation report
            validation_report = {
                "story_id": story_id,
                "validation_timestamp": datetime.now().isoformat(),
                "flows_tested": len(applicable_flows),
                "overall_metrics": overall_metrics,
                "flow_validation_results": flow_validation_results,
                "pattern_analysis": pattern_analysis,
                "navigation_validation": navigation_validation,
                "anna_persona_compatibility": anna_compatibility,
                "recommendations": recommendations,
                "validation_summary": {
                    "flows_passed": sum(1 for result in flow_validation_results 
                                      if result.get("overall_result") == "passed"),
                    "flows_failed": sum(1 for result in flow_validation_results 
                                      if result.get("overall_result") == "failed"),
                    "critical_issues": sum(len(result.get("critical_issues", [])) 
                                         for result in flow_validation_results),
                    "success_rate_percentage": overall_metrics.get("average_success_rate", 0)
                }
            }
            
            logger.info(f"User flow validation completed for story: {story_id}")
            return validation_report
            
        except Exception as e:
            error_msg = f"User flow validation failed for story {story_id}: {str(e)}"
            logger.error(error_msg)
            return {
                "error": error_msg,
                "story_id": story_id,
                "validation_failed": True,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _identify_applicable_flows(self, implementation_data: Dict[str, Any], 
                                       story_id: str) -> List[UserFlow]:
        """
        Identify which standard flows are applicable to this feature.
        
        Args:
            implementation_data: Implementation details
            story_id: Story identifier
            
        Returns:
            List of applicable user flows
        """
        applicable_flows = []
        
        # Extract feature characteristics
        ui_components = implementation_data.get("ui_components", [])
        api_endpoints = implementation_data.get("api_endpoints", [])
        feature_type = implementation_data.get("feature_type", "")
        
        # Analyze components to determine flow types
        has_forms = any(comp.get("type") in ["input", "form", "select", "textarea"] 
                       for comp in ui_components)
        has_navigation = any(comp.get("type") in ["link", "menu", "button"] 
                            for comp in ui_components)
        has_authentication = any("auth" in str(endpoint).lower() 
                                for endpoint in api_endpoints)
        
        # Match flows based on feature characteristics
        for flow in self.standard_flows:
            should_include = False
            
            # Registration flow - if has authentication or user management
            if flow.flow_id == "municipal_user_registration":
                if has_authentication or "register" in story_id.lower() or "signup" in story_id.lower():
                    should_include = True
            
            # Training access flow - if has navigation and content access
            elif flow.flow_id == "training_module_access":
                if has_navigation or "training" in story_id.lower() or "module" in story_id.lower():
                    should_include = True
            
            # Task completion flow - if has forms or submission
            elif flow.flow_id == "task_completion_feedback":
                if has_forms or "task" in story_id.lower() or "completion" in story_id.lower():
                    should_include = True
            
            if should_include:
                applicable_flows.append(flow)
        
        # If no standard flows match, create a generic flow based on components
        if not applicable_flows:
            generic_flow = await self._create_generic_flow(implementation_data, story_id)
            applicable_flows.append(generic_flow)
        
        return applicable_flows
    
    async def _validate_single_flow(self, flow: UserFlow, implementation_data: Dict[str, Any],
                                  persona_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a single user flow.
        
        Args:
            flow: User flow to validate
            implementation_data: Implementation details
            persona_requirements: Persona requirements
            
        Returns:
            Single flow validation result
        """
        step_results = []
        flow_issues = []
        overall_completion_time = 0.0
        
        # Validate each step in the flow
        for step in flow.steps:
            step_result = await self._validate_flow_step(
                step, implementation_data, persona_requirements
            )
            step_results.append(step_result)
            overall_completion_time += step_result.completion_time_seconds / 60  # Convert to minutes
            
            # Collect issues from step
            flow_issues.extend(step_result.issues_found)
        
        # Check overall flow constraints
        if overall_completion_time > flow.expected_completion_time_minutes:
            flow_issues.append(FlowValidationIssue(
                issue_id=f"{flow.flow_id}_time_exceeded",
                flow_id=flow.flow_id,
                step_id=None,
                severity="high",
                category="performance",
                description=f"Flow completion time ({overall_completion_time:.1f}min) exceeds expected time ({flow.expected_completion_time_minutes}min)",
                impact_on_user="User may become frustrated with slow progress",
                recommended_fix="Optimize flow steps to reduce completion time",
                affects_accessibility=False,
                affects_anna_persona=True
            ))
        
        # Check step count
        if len(flow.steps) > self.flow_validation_criteria["max_steps_per_flow"]:
            flow_issues.append(FlowValidationIssue(
                issue_id=f"{flow.flow_id}_too_many_steps",
                flow_id=flow.flow_id,
                step_id=None,
                severity="medium",
                category="usability",
                description=f"Flow has {len(flow.steps)} steps, exceeding recommended maximum of {self.flow_validation_criteria['max_steps_per_flow']}",
                impact_on_user="Increased cognitive load and potential abandonment",
                recommended_fix="Consolidate or simplify flow steps",
                affects_accessibility=True,
                affects_anna_persona=True
            ))
        
        # Calculate overall flow metrics
        average_ux_score = sum(result.user_experience_score for result in step_results) / len(step_results) if step_results else 0
        average_accessibility_score = sum(result.accessibility_score for result in step_results) / len(step_results) if step_results else 0
        overall_success_rate = sum(result.success_rate for result in step_results) / len(step_results) if step_results else 0
        
        # Determine overall result
        critical_issues = [issue for issue in flow_issues if issue.severity == "critical"]
        high_issues = [issue for issue in flow_issues if issue.severity == "high"]
        
        if critical_issues:
            overall_result = "failed"
        elif high_issues and overall_success_rate < 80:
            overall_result = "failed"
        elif average_ux_score < 3.5 or average_accessibility_score < 80:
            overall_result = "warning"
        else:
            overall_result = "passed"
        
        return {
            "flow_id": flow.flow_id,
            "flow_name": flow.name,
            "overall_result": overall_result,
            "completion_time_minutes": overall_completion_time,
            "expected_time_minutes": flow.expected_completion_time_minutes,
            "step_count": len(flow.steps),
            "step_results": [result.__dict__ for result in step_results],
            "flow_issues": [issue.__dict__ for issue in flow_issues],
            "critical_issues": [issue.__dict__ for issue in critical_issues],
            "metrics": {
                "average_user_experience_score": round(average_ux_score, 2),
                "average_accessibility_score": round(average_accessibility_score, 1),
                "overall_success_rate": round(overall_success_rate, 1),
                "time_efficiency": round((flow.expected_completion_time_minutes / max(overall_completion_time, 0.1)) * 100, 1)
            },
            "anna_persona_compatible": self._check_anna_compatibility(flow_issues, average_ux_score, overall_completion_time)
        }
    
    async def _validate_flow_step(self, step: FlowStep, implementation_data: Dict[str, Any],
                                persona_requirements: Dict[str, Any]) -> FlowStepValidationResult:
        """
        Validate a single flow step.
        
        Args:
            step: Flow step to validate
            implementation_data: Implementation details
            persona_requirements: Persona requirements
            
        Returns:
            Step validation result
        """
        issues_found = []
        ui_components = implementation_data.get("ui_components", [])
        
        # Check if expected elements exist
        for expected_element in step.expected_elements:
            element_found = any(
                expected_element in comp.get("id", "") or 
                expected_element in comp.get("type", "") or
                expected_element in comp.get("class", "")
                for comp in ui_components
            )
            
            if not element_found:
                issues_found.append(FlowValidationIssue(
                    issue_id=f"{step.step_id}_missing_{expected_element}",
                    flow_id="",  # Will be set by parent
                    step_id=step.step_id,
                    severity="high",
                    category="missing_element",
                    description=f"Expected element '{expected_element}' not found in implementation",
                    impact_on_user="User cannot complete required action",
                    recommended_fix=f"Implement missing element: {expected_element}",
                    affects_accessibility=True,
                    affects_anna_persona=True
                ))
        
        # Check accessibility requirements
        accessibility_score = 100.0
        for accessibility_req in step.accessibility_requirements:
            if not self._check_accessibility_requirement(accessibility_req, ui_components):
                accessibility_score -= 15
                issues_found.append(FlowValidationIssue(
                    issue_id=f"{step.step_id}_accessibility_{accessibility_req}",
                    flow_id="",
                    step_id=step.step_id,
                    severity="medium",
                    category="accessibility",
                    description=f"Accessibility requirement not met: {accessibility_req}",
                    impact_on_user="Reduced accessibility for users with disabilities",
                    recommended_fix=f"Implement accessibility requirement: {accessibility_req}",
                    affects_accessibility=True,
                    affects_anna_persona=False
                ))
        
        # Estimate completion time based on step complexity
        base_time = 15.0  # Base 15 seconds per step
        complexity_multiplier = len(step.required_actions) * 0.5
        estimated_time = base_time + (complexity_multiplier * 10)
        
        if step.time_limit_seconds and estimated_time > step.time_limit_seconds:
            issues_found.append(FlowValidationIssue(
                issue_id=f"{step.step_id}_time_limit_exceeded",
                flow_id="",
                step_id=step.step_id,
                severity="medium",
                category="performance",
                description=f"Estimated completion time ({estimated_time}s) exceeds limit ({step.time_limit_seconds}s)",
                impact_on_user="Time pressure may cause user stress",
                recommended_fix="Simplify step or extend time limit",
                affects_accessibility=False,
                affects_anna_persona=True
            ))
        
        # Calculate user experience score
        ux_score = 5.0
        ux_score -= len([i for i in issues_found if i.severity in ["critical", "high"]]) * 0.5
        ux_score -= len([i for i in issues_found if i.severity == "medium"]) * 0.2
        ux_score = max(1.0, min(5.0, ux_score))
        
        # Calculate success rate
        success_rate = 100.0
        success_rate -= len([i for i in issues_found if i.severity == "critical"]) * 25
        success_rate -= len([i for i in issues_found if i.severity == "high"]) * 15
        success_rate = max(0.0, min(100.0, success_rate))
        
        # Determine validation result
        if any(i.severity == "critical" for i in issues_found):
            validation_result = FlowValidationResult.CRITICAL
        elif any(i.severity == "high" for i in issues_found):
            validation_result = FlowValidationResult.FAILED
        elif any(i.severity == "medium" for i in issues_found):
            validation_result = FlowValidationResult.WARNING
        else:
            validation_result = FlowValidationResult.PASSED
        
        return FlowStepValidationResult(
            step_id=step.step_id,
            validation_result=validation_result,
            completion_time_seconds=estimated_time,
            issues_found=issues_found,
            accessibility_score=accessibility_score,
            user_experience_score=ux_score,
            success_rate=success_rate,
            details={
                "step_type": step.step_type.value,
                "required_actions_count": len(step.required_actions),
                "expected_elements_found": len(step.expected_elements) - len([
                    i for i in issues_found if "missing" in i.issue_id
                ]),
                "accessibility_requirements_met": len(step.accessibility_requirements) - len([
                    i for i in issues_found if "accessibility" in i.issue_id
                ])
            }
        )
    
    def _check_accessibility_requirement(self, requirement: str, ui_components: List[Dict[str, Any]]) -> bool:
        """
        Check if an accessibility requirement is met.
        
        Args:
            requirement: Accessibility requirement to check
            ui_components: UI components to check against
            
        Returns:
            True if requirement is met
        """
        # Simplified checks - would be more sophisticated in real implementation
        if requirement == "keyboard_accessible":
            return any(comp.get("keyboard_accessible", True) for comp in ui_components)
        elif requirement == "screen_reader_compatible":
            return any(comp.get("aria_label") or comp.get("alt_text") for comp in ui_components)
        elif requirement == "proper_labels":
            form_elements = [c for c in ui_components if c.get("type") in ["input", "select", "textarea"]]
            return all(elem.get("label") for elem in form_elements)
        elif requirement == "focus_management":
            return any(comp.get("focusable", False) for comp in ui_components)
        else:
            return True  # Default to passing for unknown requirements
    
    def _check_anna_compatibility(self, flow_issues: List[FlowValidationIssue], 
                                ux_score: float, completion_time: float) -> bool:
        """
        Check if flow is compatible with Anna persona requirements.
        
        Args:
            flow_issues: List of issues found
            ux_score: User experience score
            completion_time: Completion time in minutes
            
        Returns:
            True if compatible with Anna persona
        """
        # Anna-specific checks
        anna_affecting_issues = [issue for issue in flow_issues if issue.affects_anna_persona]
        
        # Anna cannot tolerate critical or too many high severity issues
        if any(issue.severity == "critical" for issue in anna_affecting_issues):
            return False
        
        high_severity_count = len([issue for issue in anna_affecting_issues if issue.severity == "high"])
        if high_severity_count > 2:
            return False
        
        # Anna needs good UX score
        if ux_score < 3.5:
            return False
        
        # Anna has strict time constraints
        if completion_time > self.flow_validation_criteria["max_completion_time_minutes"]:
            return False
        
        return True
    
    async def _analyze_flow_patterns(self, flow_validation_results: List[Dict[str, Any]],
                                   implementation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze overall flow patterns for consistency and usability.
        
        Args:
            flow_validation_results: Results from flow validations
            implementation_data: Implementation details
            
        Returns:
            Flow pattern analysis
        """
        try:
            # Analyze navigation patterns
            navigation_structure = implementation_data.get("navigation_structure", {})
            ui_components = implementation_data.get("ui_components", [])
            
            # Check for consistent navigation
            navigation_elements = [comp for comp in ui_components 
                                 if comp.get("type") in ["menu", "nav", "breadcrumb"]]
            
            consistent_navigation = len(set(elem.get("style", "") for elem in navigation_elements)) <= 1
            
            # Analyze flow complexity
            total_steps = sum(result.get("step_count", 0) for result in flow_validation_results)
            average_steps = total_steps / len(flow_validation_results) if flow_validation_results else 0
            
            # Determine predominant flow pattern
            if average_steps <= 3:
                predominant_pattern = "linear_progression"
            elif len(navigation_elements) > 3:
                predominant_pattern = "hub_and_spoke"
            elif average_steps > 5:
                predominant_pattern = "wizard_flow"
            else:
                predominant_pattern = "free_form"
            
            # Assess pattern suitability for Anna
            pattern_info = self.flow_patterns.get(predominant_pattern, {})
            anna_suitability = pattern_info.get("anna_preference", "medium")
            
            return {
                "predominant_pattern": predominant_pattern,
                "pattern_description": pattern_info.get("description", "Unknown pattern"),
                "anna_suitability": anna_suitability,
                "consistent_navigation": consistent_navigation,
                "average_steps_per_flow": round(average_steps, 1),
                "navigation_elements_count": len(navigation_elements),
                "complexity_assessment": "low" if average_steps <= 3 else "medium" if average_steps <= 5 else "high",
                "recommendations": self._generate_pattern_recommendations(
                    predominant_pattern, anna_suitability, consistent_navigation
                )
            }
            
        except Exception as e:
            logger.error(f"Error analyzing flow patterns: {e}")
            return {
                "error": str(e),
                "analysis_failed": True
            }
    
    async def _validate_navigation_consistency(self, navigation_structure: Dict[str, Any],
                                             ui_components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate navigation consistency across the implementation.
        
        Args:
            navigation_structure: Navigation structure data
            ui_components: UI components
            
        Returns:
            Navigation validation results
        """
        issues = []
        
        # Check for consistent navigation elements
        nav_elements = [comp for comp in ui_components if comp.get("type") in ["nav", "menu", "link"]]
        
        if not nav_elements:
            issues.append("No navigation elements found")
        
        # Check for breadcrumbs in multi-step flows
        breadcrumb_elements = [comp for comp in ui_components if "breadcrumb" in comp.get("type", "")]
        
        if len(nav_elements) > 5 and not breadcrumb_elements:
            issues.append("Complex navigation without breadcrumbs")
        
        # Check for consistent styling
        nav_styles = set(elem.get("style", "") for elem in nav_elements)
        if len(nav_styles) > 2:
            issues.append("Inconsistent navigation styling")
        
        consistency_score = max(0, 100 - (len(issues) * 20))
        
        return {
            "consistency_score": consistency_score,
            "navigation_elements_count": len(nav_elements),
            "breadcrumb_elements_count": len(breadcrumb_elements),
            "issues_found": issues,
            "recommendations": [
                "Add breadcrumb navigation for complex flows",
                "Maintain consistent navigation styling",
                "Ensure navigation is keyboard accessible"
            ] if issues else ["Navigation structure looks good"]
        }
    
    async def _assess_anna_persona_compatibility(self, flow_validation_results: List[Dict[str, Any]],
                                               persona_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess compatibility with Anna persona requirements.
        
        Args:
            flow_validation_results: Flow validation results
            persona_requirements: Anna persona requirements
            
        Returns:
            Anna persona compatibility assessment
        """
        try:
            compatibility_score = 100.0
            compatibility_issues = []
            
            for result in flow_validation_results:
                # Check completion time
                completion_time = result.get("completion_time_minutes", 0)
                if completion_time > 10:  # Anna's time limit
                    compatibility_score -= 20
                    compatibility_issues.append(f"Flow '{result.get('flow_name')}' exceeds Anna's 10-minute time limit")
                
                # Check UX score
                ux_score = result.get("metrics", {}).get("average_user_experience_score", 0)
                if ux_score < 4.0:
                    compatibility_score -= 15
                    compatibility_issues.append(f"Flow '{result.get('flow_name')}' has low UX score for Anna")
                
                # Check for Anna-affecting issues
                anna_issues = [issue for issue in result.get("flow_issues", [])
                             if issue.get("affects_anna_persona", False)]
                if anna_issues:
                    compatibility_score -= len(anna_issues) * 5
                    compatibility_issues.extend([issue.get("description") for issue in anna_issues])
            
            # Overall compatibility assessment
            if compatibility_score >= 90:
                compatibility_level = "excellent"
            elif compatibility_score >= 75:
                compatibility_level = "good"
            elif compatibility_score >= 60:
                compatibility_level = "acceptable"
            else:
                compatibility_level = "poor"
            
            return {
                "compatibility_score": max(0, compatibility_score),
                "compatibility_level": compatibility_level,
                "anna_persona_ready": compatibility_score >= 75,
                "compatibility_issues": compatibility_issues,
                "time_constraint_compliance": all(
                    result.get("completion_time_minutes", 0) <= 10 
                    for result in flow_validation_results
                ),
                "user_experience_threshold_met": all(
                    result.get("metrics", {}).get("average_user_experience_score", 0) >= 3.5
                    for result in flow_validation_results
                ),
                "recommendations": self._generate_anna_compatibility_recommendations(
                    compatibility_score, compatibility_issues
                )
            }
            
        except Exception as e:
            logger.error(f"Error assessing Anna persona compatibility: {e}")
            return {
                "error": str(e),
                "compatibility_assessment_failed": True
            }
    
    def _calculate_flow_metrics(self, flow_validation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate overall flow metrics from validation results.
        
        Args:
            flow_validation_results: List of flow validation results
            
        Returns:
            Overall flow metrics
        """
        if not flow_validation_results:
            return {
                "average_success_rate": 0,
                "average_completion_time": 0,
                "average_user_experience_score": 0,
                "average_accessibility_score": 0
            }
        
        total_success_rate = sum(result.get("metrics", {}).get("overall_success_rate", 0) 
                               for result in flow_validation_results)
        total_completion_time = sum(result.get("completion_time_minutes", 0) 
                                  for result in flow_validation_results)
        total_ux_score = sum(result.get("metrics", {}).get("average_user_experience_score", 0)
                           for result in flow_validation_results)
        total_accessibility_score = sum(result.get("metrics", {}).get("average_accessibility_score", 0)
                                      for result in flow_validation_results)
        
        count = len(flow_validation_results)
        
        return {
            "average_success_rate": round(total_success_rate / count, 1),
            "average_completion_time_minutes": round(total_completion_time / count, 1),
            "average_user_experience_score": round(total_ux_score / count, 2),
            "average_accessibility_score": round(total_accessibility_score / count, 1),
            "flows_validated": count,
            "time_efficiency_rating": "excellent" if total_completion_time / count <= 5 else 
                                    "good" if total_completion_time / count <= 8 else "needs_improvement"
        }
    
    async def _generate_flow_recommendations(self, flow_validation_results: List[Dict[str, Any]],
                                           pattern_analysis: Dict[str, Any],
                                           anna_compatibility: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recommendations for improving user flows.
        
        Args:
            flow_validation_results: Flow validation results
            pattern_analysis: Flow pattern analysis
            anna_compatibility: Anna persona compatibility
            
        Returns:
            List of improvement recommendations
        """
        recommendations = []
        
        try:
            # Time-based recommendations
            long_flows = [result for result in flow_validation_results 
                         if result.get("completion_time_minutes", 0) > 8]
            if long_flows:
                recommendations.append({
                    "category": "time_optimization",
                    "priority": "high",
                    "issue": f"{len(long_flows)} flows exceed optimal completion time",
                    "recommendation": "Streamline lengthy flows and reduce required steps",
                    "expected_impact": "Improved user satisfaction and task completion rates",
                    "affects_anna_persona": True
                })
            
            # Pattern-based recommendations
            if pattern_analysis.get("anna_suitability") == "low":
                recommendations.append({
                    "category": "flow_pattern",
                    "priority": "medium",
                    "issue": f"Current flow pattern ({pattern_analysis.get('predominant_pattern')}) not optimal for Anna persona",
                    "recommendation": "Consider restructuring flows to use linear progression or wizard patterns",
                    "expected_impact": "Better alignment with Anna's preferences and work style",
                    "affects_anna_persona": True
                })
            
            # Accessibility recommendations
            accessibility_issues = []
            for result in flow_validation_results:
                accessibility_score = result.get("metrics", {}).get("average_accessibility_score", 100)
                if accessibility_score < 90:
                    accessibility_issues.append(result.get("flow_name"))
            
            if accessibility_issues:
                recommendations.append({
                    "category": "accessibility",
                    "priority": "high",
                    "issue": f"Accessibility issues in flows: {', '.join(accessibility_issues)}",
                    "recommendation": "Address accessibility requirements for screen readers and keyboard navigation",
                    "expected_impact": "Improved accessibility compliance and inclusive user experience",
                    "affects_anna_persona": False
                })
            
            # Navigation consistency recommendations
            if not pattern_analysis.get("consistent_navigation", True):
                recommendations.append({
                    "category": "navigation_consistency",
                    "priority": "medium",
                    "issue": "Inconsistent navigation patterns across flows",
                    "recommendation": "Standardize navigation elements and interaction patterns",
                    "expected_impact": "Reduced cognitive load and improved user confidence",
                    "affects_anna_persona": True
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating flow recommendations: {e}")
            return [{
                "category": "system_error",
                "priority": "high",
                "issue": "Failed to generate flow recommendations",
                "recommendation": "Review flow validation system",
                "error": str(e)
            }]
    
    def _generate_pattern_recommendations(self, pattern: str, anna_suitability: str, 
                                        consistent_navigation: bool) -> List[str]:
        """Generate recommendations based on flow patterns."""
        recommendations = []
        
        if anna_suitability == "low":
            recommendations.append(f"Consider changing from {pattern} to linear_progression or wizard_flow for better Anna compatibility")
        
        if not consistent_navigation:
            recommendations.append("Implement consistent navigation patterns across all flows")
        
        if pattern == "free_form":
            recommendations.append("Add guided navigation or breadcrumbs to help users maintain orientation")
        
        return recommendations
    
    def _generate_anna_compatibility_recommendations(self, compatibility_score: float,
                                                   compatibility_issues: List[str]) -> List[str]:
        """Generate Anna persona compatibility recommendations."""
        recommendations = []
        
        if compatibility_score < 75:
            recommendations.append("Significant improvements needed for Anna persona compatibility")
        
        if any("time limit" in issue for issue in compatibility_issues):
            recommendations.append("Reduce flow complexity to meet Anna's 10-minute time constraint")
        
        if any("UX score" in issue for issue in compatibility_issues):
            recommendations.append("Improve user interface clarity and ease of use")
        
        if not recommendations:
            recommendations.append("Flows are well-suited for Anna persona")
        
        return recommendations
    
    async def _create_generic_flow(self, implementation_data: Dict[str, Any], 
                                 story_id: str) -> UserFlow:
        """
        Create a generic flow based on implementation data when no standard flows match.
        
        Args:
            implementation_data: Implementation details
            story_id: Story identifier
            
        Returns:
            Generic user flow
        """
        ui_components = implementation_data.get("ui_components", [])
        
        # Create basic steps based on component types
        steps = []
        
        # Navigation step if links/menus present
        nav_components = [c for c in ui_components if c.get("type") in ["link", "menu", "nav"]]
        if nav_components:
            steps.append(FlowStep(
                step_id="navigate_to_feature",
                step_type=FlowStepType.NAVIGATION,
                description="Navigate to feature",
                expected_elements=["navigation_elements"],
                required_actions=["click_navigation"],
                success_criteria={"navigation_successful": True},
                error_conditions=["navigation_failed"],
                accessibility_requirements=["keyboard_accessible"]
            ))
        
        # Input step if forms present
        form_components = [c for c in ui_components if c.get("type") in ["input", "form", "select"]]
        if form_components:
            steps.append(FlowStep(
                step_id="complete_input",
                step_type=FlowStepType.INPUT,
                description="Complete required input",
                expected_elements=["input_fields"],
                required_actions=["fill_fields"],
                success_criteria={"input_valid": True},
                error_conditions=["validation_failed"],
                accessibility_requirements=["proper_labels"]
            ))
        
        # Completion step
        steps.append(FlowStep(
            step_id="complete_task",
            step_type=FlowStepType.COMPLETION,
            description="Complete task",
            expected_elements=["completion_indicator"],
            required_actions=["confirm_completion"],
            success_criteria={"task_completed": True},
            error_conditions=["completion_failed"],
            accessibility_requirements=["success_announced"]
        ))
        
        return UserFlow(
            flow_id=f"generic_flow_{story_id}",
            name=f"Generic Flow for {story_id}",
            description="Automatically generated flow based on implementation",
            user_goal="Complete the implemented feature task",
            persona="Anna",
            priority="medium",
            steps=steps,
            expected_completion_time_minutes=5.0,
            alternative_paths=[],
            error_recovery_paths=[]
        )