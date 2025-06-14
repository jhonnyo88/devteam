"""
User Acceptance Testing (UAT) orchestrator for QA Tester agent.

PURPOSE:
Comprehensive UAT workflow orchestration for municipal training applications,
ensuring stakeholder satisfaction and deployment readiness.

CRITICAL FUNCTIONALITY:
- UAT test plan generation based on user stories
- Municipal stakeholder review simulation
- Training effectiveness measurement
- User onboarding flow validation
- Stakeholder sign-off coordination

ADAPTATION GUIDE:
To adapt for your project:
1. Update stakeholder_roles for your organization
2. Modify acceptance_criteria_templates for your requirements
3. Adjust uat_workflows for your approval process
4. Update effectiveness_metrics for your success measures

CONTRACT PROTECTION:
This tool enhances QA testing without breaking contracts.
All outputs integrate seamlessly with existing QA validation results.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

# Setup logging
logger = logging.getLogger(__name__)


class StakeholderRole(Enum):
    """Municipal stakeholder roles for UAT."""
    MUNICIPAL_MANAGER = "municipal_manager"
    TRAINING_COORDINATOR = "training_coordinator"
    IT_COORDINATOR = "it_coordinator"
    END_USER_REPRESENTATIVE = "end_user_representative"
    COMPLIANCE_OFFICER = "compliance_officer"
    DEPARTMENT_HEAD = "department_head"
    CITIZEN_SERVICE_MANAGER = "citizen_service_manager"
    HR_REPRESENTATIVE = "hr_representative"


class ApprovalStatus(Enum):
    """UAT approval status levels."""
    APPROVED = "approved"
    APPROVED_WITH_CONDITIONS = "approved_with_conditions"
    NEEDS_REVISION = "needs_revision"
    REJECTED = "rejected"
    PENDING_REVIEW = "pending_review"


class UATTestType(Enum):
    """Types of UAT tests."""
    FUNCTIONAL_ACCEPTANCE = "functional_acceptance"
    USABILITY_ACCEPTANCE = "usability_acceptance"
    PERFORMANCE_ACCEPTANCE = "performance_acceptance"
    SECURITY_ACCEPTANCE = "security_acceptance"
    COMPLIANCE_ACCEPTANCE = "compliance_acceptance"
    TRAINING_EFFECTIVENESS = "training_effectiveness"


@dataclass
class AcceptanceCriteria:
    """Individual acceptance criteria."""
    criteria_id: str
    description: str
    priority: str  # "must_have", "should_have", "could_have"
    test_method: str
    success_metrics: Dict[str, Any]
    stakeholder_role: StakeholderRole
    verification_steps: List[str]


@dataclass
class UATTestPlan:
    """Complete UAT test plan."""
    plan_id: str
    story_id: str
    test_objectives: List[str]
    acceptance_criteria: List[AcceptanceCriteria]
    stakeholder_responsibilities: Dict[StakeholderRole, List[str]]
    test_schedule: Dict[str, str]
    success_metrics: Dict[str, Any]
    risk_mitigation: List[str]


@dataclass
class StakeholderFeedback:
    """Feedback from UAT stakeholder."""
    stakeholder_role: StakeholderRole
    feedback_timestamp: str
    approval_status: ApprovalStatus
    satisfaction_score: float  # 1-5 scale
    specific_feedback: List[str]
    concerns_raised: List[str]
    improvement_suggestions: List[str]
    conditions_for_approval: List[str]


@dataclass
class TrainingEffectivenessResult:
    """Results from training effectiveness testing."""
    learning_objectives_met: bool
    knowledge_retention_score: float  # percentage
    skill_application_score: float  # percentage
    confidence_improvement: float  # percentage
    time_to_competency_minutes: float
    post_training_performance: Dict[str, Any]
    areas_needing_improvement: List[str]


@dataclass
class UATExecutionResult:
    """Results from UAT execution."""
    test_plan_id: str
    execution_timestamp: str
    overall_approval_status: ApprovalStatus
    stakeholder_feedback: List[StakeholderFeedback]
    training_effectiveness: TrainingEffectivenessResult
    acceptance_criteria_results: List[Dict[str, Any]]
    deployment_readiness_score: float
    critical_issues: List[str]
    recommended_actions: List[str]


class UATOrchestrator:
    """
    User Acceptance Testing orchestrator for municipal training applications.
    
    Manages the complete UAT workflow from test plan generation through
    stakeholder approval and deployment readiness assessment.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize UAT orchestrator with configuration."""
        self.config = config or {}
        
        # Municipal stakeholder definitions
        self.stakeholder_definitions = {
            StakeholderRole.MUNICIPAL_MANAGER: {
                "responsibilities": [
                    "Overall business approval",
                    "Resource allocation approval", 
                    "Strategic alignment validation",
                    "Risk assessment approval"
                ],
                "approval_weight": 0.25,
                "focus_areas": ["business_value", "resource_efficiency", "strategic_alignment"],
                "typical_concerns": ["cost_effectiveness", "implementation_timeline", "change_management"]
            },
            StakeholderRole.TRAINING_COORDINATOR: {
                "responsibilities": [
                    "Training content validation",
                    "Learning objective verification",
                    "User experience approval",
                    "Training effectiveness assessment"
                ],
                "approval_weight": 0.20,
                "focus_areas": ["learning_effectiveness", "user_experience", "content_quality"],
                "typical_concerns": ["learning_outcomes", "user_satisfaction", "training_efficiency"]
            },
            StakeholderRole.IT_COORDINATOR: {
                "responsibilities": [
                    "Technical implementation approval",
                    "Security validation",
                    "System integration verification",
                    "Performance acceptance"
                ],
                "approval_weight": 0.15,
                "focus_areas": ["technical_quality", "security", "performance", "integration"],
                "typical_concerns": ["system_reliability", "security_compliance", "maintenance_overhead"]
            },
            StakeholderRole.END_USER_REPRESENTATIVE: {
                "responsibilities": [
                    "Usability validation",
                    "Workflow efficiency approval",
                    "Accessibility verification",
                    "Day-to-day usage approval"
                ],
                "approval_weight": 0.15,
                "focus_areas": ["usability", "efficiency", "accessibility"],
                "typical_concerns": ["ease_of_use", "time_efficiency", "learning_curve"]
            },
            StakeholderRole.COMPLIANCE_OFFICER: {
                "responsibilities": [
                    "Regulatory compliance validation",
                    "Policy adherence verification",
                    "Audit readiness approval",
                    "Risk mitigation validation"
                ],
                "approval_weight": 0.10,
                "focus_areas": ["regulatory_compliance", "policy_adherence", "audit_readiness"],
                "typical_concerns": ["compliance_gaps", "audit_findings", "legal_risks"]
            },
            StakeholderRole.DEPARTMENT_HEAD: {
                "responsibilities": [
                    "Departmental workflow approval",
                    "Team productivity validation",
                    "Change impact assessment",
                    "Implementation support approval"
                ],
                "approval_weight": 0.10,
                "focus_areas": ["workflow_efficiency", "team_productivity", "change_management"],
                "typical_concerns": ["productivity_impact", "team_adoption", "change_resistance"]
            },
            StakeholderRole.CITIZEN_SERVICE_MANAGER: {
                "responsibilities": [
                    "Citizen service impact validation",
                    "Service quality maintenance",
                    "Customer satisfaction protection",
                    "Service delivery approval"
                ],
                "approval_weight": 0.05,
                "focus_areas": ["service_quality", "customer_satisfaction", "service_delivery"],
                "typical_concerns": ["service_disruption", "citizen_satisfaction", "service_quality"]
            }
        }
        
        # Acceptance criteria templates for municipal applications
        self.acceptance_criteria_templates = {
            "functional_requirements": [
                "All specified features work as documented",
                "Core workflows complete successfully",
                "Error handling works appropriately",
                "Data validation functions correctly"
            ],
            "usability_requirements": [
                "Tasks can be completed within time constraints",
                "Navigation is intuitive for municipal users",
                "Error messages are clear and actionable",
                "Help documentation is accessible and useful"
            ],
            "performance_requirements": [
                "System responds within acceptable time limits",
                "Concurrent user load is handled appropriately",
                "Mobile access performs adequately",
                "Peak usage periods are handled smoothly"
            ],
            "compliance_requirements": [
                "GDPR data protection requirements are met",
                "Accessibility standards (WCAG AA) are achieved",
                "Municipal policy compliance is verified",
                "Audit trail requirements are satisfied"
            ],
            "training_effectiveness": [
                "Learning objectives are clearly achieved",
                "Knowledge retention meets requirements",
                "Skill application is demonstrable",
                "Training time is within acceptable limits"
            ]
        }
        
        # Municipal UAT workflow stages
        self.uat_workflow_stages = [
            {
                "stage": "preparation",
                "duration_days": 2,
                "activities": [
                    "Generate UAT test plan",
                    "Identify stakeholder representatives",
                    "Prepare test environment",
                    "Schedule stakeholder sessions"
                ]
            },
            {
                "stage": "execution", 
                "duration_days": 5,
                "activities": [
                    "Conduct stakeholder testing sessions",
                    "Collect feedback and observations",
                    "Document issues and concerns",
                    "Assess training effectiveness"
                ]
            },
            {
                "stage": "evaluation",
                "duration_days": 3,
                "activities": [
                    "Analyze stakeholder feedback",
                    "Assess acceptance criteria compliance",
                    "Determine deployment readiness",
                    "Generate approval recommendations"
                ]
            },
            {
                "stage": "approval",
                "duration_days": 2,
                "activities": [
                    "Present findings to stakeholders",
                    "Obtain formal approvals",
                    "Document conditions and requirements",
                    "Plan deployment or revision"
                ]
            }
        ]
    
    async def orchestrate_uat_process(
        self,
        story_id: str,
        implementation_data: Dict[str, Any],
        user_stories: List[Dict[str, Any]],
        stakeholder_roles: Optional[List[StakeholderRole]] = None
    ) -> UATExecutionResult:
        """
        Orchestrate complete UAT process.
        
        Args:
            story_id: Story identifier for traceability
            implementation_data: Implementation details to test
            user_stories: User stories for acceptance criteria
            stakeholder_roles: Specific stakeholders to include (optional)
            
        Returns:
            Complete UAT execution results
        """
        start_time = datetime.now()
        stakeholder_roles = stakeholder_roles or list(StakeholderRole)
        
        try:
            logger.info(f"Starting UAT orchestration for {story_id}")
            
            # 1. Generate comprehensive UAT test plan
            test_plan = await self._generate_uat_test_plan(
                story_id, implementation_data, user_stories, stakeholder_roles
            )
            
            # 2. Execute stakeholder testing sessions
            stakeholder_feedback = await self._execute_stakeholder_testing(
                test_plan, implementation_data, stakeholder_roles
            )
            
            # 3. Assess training effectiveness
            training_effectiveness = await self._assess_training_effectiveness(
                implementation_data, test_plan
            )
            
            # 4. Validate acceptance criteria
            criteria_results = await self._validate_acceptance_criteria(
                test_plan, stakeholder_feedback, training_effectiveness
            )
            
            # 5. Determine overall approval status
            overall_status = self._determine_overall_approval_status(
                stakeholder_feedback, criteria_results
            )
            
            # 6. Calculate deployment readiness score
            readiness_score = self._calculate_deployment_readiness_score(
                stakeholder_feedback, training_effectiveness, criteria_results
            )
            
            # 7. Identify critical issues
            critical_issues = self._identify_critical_uat_issues(
                stakeholder_feedback, criteria_results
            )
            
            # 8. Generate recommended actions
            recommended_actions = self._generate_uat_recommendations(
                overall_status, stakeholder_feedback, critical_issues
            )
            
            result = UATExecutionResult(
                test_plan_id=test_plan.plan_id,
                execution_timestamp=start_time.isoformat(),
                overall_approval_status=overall_status,
                stakeholder_feedback=stakeholder_feedback,
                training_effectiveness=training_effectiveness,
                acceptance_criteria_results=criteria_results,
                deployment_readiness_score=readiness_score,
                critical_issues=critical_issues,
                recommended_actions=recommended_actions
            )
            
            logger.info(f"UAT orchestration completed for {story_id}")
            return result
            
        except Exception as e:
            logger.error(f"UAT orchestration failed for {story_id}: {str(e)}")
            return UATExecutionResult(
                test_plan_id=f"failed_{story_id}",
                execution_timestamp=start_time.isoformat(),
                overall_approval_status=ApprovalStatus.REJECTED,
                stakeholder_feedback=[],
                training_effectiveness=TrainingEffectivenessResult(
                    learning_objectives_met=False,
                    knowledge_retention_score=0.0,
                    skill_application_score=0.0,
                    confidence_improvement=0.0,
                    time_to_competency_minutes=0.0,
                    post_training_performance={},
                    areas_needing_improvement=["Fix UAT orchestration errors"]
                ),
                acceptance_criteria_results=[],
                deployment_readiness_score=0.0,
                critical_issues=[f"UAT orchestration failed: {str(e)}"],
                recommended_actions=["Fix UAT orchestration system before proceeding"]
            )
    
    async def _generate_uat_test_plan(
        self,
        story_id: str,
        implementation_data: Dict[str, Any],
        user_stories: List[Dict[str, Any]],
        stakeholder_roles: List[StakeholderRole]
    ) -> UATTestPlan:
        """Generate comprehensive UAT test plan."""
        plan_id = f"UAT-{story_id}-{datetime.now().strftime('%Y%m%d')}"
        
        # Extract test objectives from user stories
        test_objectives = self._extract_test_objectives(user_stories, implementation_data)
        
        # Generate acceptance criteria
        acceptance_criteria = self._generate_acceptance_criteria(user_stories, stakeholder_roles)
        
        # Define stakeholder responsibilities
        stakeholder_responsibilities = self._define_stakeholder_responsibilities(stakeholder_roles)
        
        # Create test schedule
        test_schedule = self._create_test_schedule()
        
        # Define success metrics
        success_metrics = self._define_success_metrics(user_stories)
        
        # Identify risk mitigation strategies
        risk_mitigation = self._identify_risk_mitigation_strategies(implementation_data)
        
        return UATTestPlan(
            plan_id=plan_id,
            story_id=story_id,
            test_objectives=test_objectives,
            acceptance_criteria=acceptance_criteria,
            stakeholder_responsibilities=stakeholder_responsibilities,
            test_schedule=test_schedule,
            success_metrics=success_metrics,
            risk_mitigation=risk_mitigation
        )
    
    def _extract_test_objectives(
        self,
        user_stories: List[Dict[str, Any]],
        implementation_data: Dict[str, Any]
    ) -> List[str]:
        """Extract test objectives from user stories and implementation."""
        objectives = [
            "Validate all functional requirements are met",
            "Ensure usability meets municipal user needs",
            "Verify performance under realistic load",
            "Confirm compliance with municipal policies",
            "Assess training effectiveness and learning outcomes"
        ]
        
        # Add specific objectives based on implementation
        ui_components = implementation_data.get("ui_components", [])
        if len(ui_components) > 5:
            objectives.append("Validate complex user interface interactions")
        
        api_endpoints = implementation_data.get("api_endpoints", [])
        if api_endpoints:
            objectives.append("Verify API integration and data flow")
        
        user_flows = implementation_data.get("user_flows", [])
        if user_flows:
            objectives.append("Validate user workflow efficiency")
        
        return objectives
    
    def _generate_acceptance_criteria(
        self,
        user_stories: List[Dict[str, Any]],
        stakeholder_roles: List[StakeholderRole]
    ) -> List[AcceptanceCriteria]:
        """Generate acceptance criteria for UAT."""
        criteria = []
        
        # Generate criteria for each template category
        for category, templates in self.acceptance_criteria_templates.items():
            for i, template in enumerate(templates):
                # Assign criteria to appropriate stakeholder
                stakeholder = self._assign_criteria_to_stakeholder(category, stakeholder_roles)
                
                criteria_id = f"{category}_{i+1}"
                criteria.append(AcceptanceCriteria(
                    criteria_id=criteria_id,
                    description=template,
                    priority="must_have" if i < 2 else "should_have",
                    test_method="manual_testing",
                    success_metrics={"completion_rate": 100, "satisfaction_score": 4.0},
                    stakeholder_role=stakeholder,
                    verification_steps=[
                        "Execute test scenario",
                        "Observe user behavior", 
                        "Record results",
                        "Validate against criteria"
                    ]
                ))
        
        return criteria
    
    def _assign_criteria_to_stakeholder(
        self,
        category: str,
        stakeholder_roles: List[StakeholderRole]
    ) -> StakeholderRole:
        """Assign acceptance criteria to appropriate stakeholder."""
        category_mapping = {
            "functional_requirements": StakeholderRole.TRAINING_COORDINATOR,
            "usability_requirements": StakeholderRole.END_USER_REPRESENTATIVE,
            "performance_requirements": StakeholderRole.IT_COORDINATOR,
            "compliance_requirements": StakeholderRole.COMPLIANCE_OFFICER,
            "training_effectiveness": StakeholderRole.TRAINING_COORDINATOR
        }
        
        preferred_stakeholder = category_mapping.get(category, StakeholderRole.MUNICIPAL_MANAGER)
        
        # Use preferred stakeholder if available, otherwise use first available
        return preferred_stakeholder if preferred_stakeholder in stakeholder_roles else stakeholder_roles[0]
    
    def _define_stakeholder_responsibilities(
        self,
        stakeholder_roles: List[StakeholderRole]
    ) -> Dict[StakeholderRole, List[str]]:
        """Define specific responsibilities for each stakeholder."""
        responsibilities = {}
        
        for role in stakeholder_roles:
            if role in self.stakeholder_definitions:
                responsibilities[role] = self.stakeholder_definitions[role]["responsibilities"]
        
        return responsibilities
    
    def _create_test_schedule(self) -> Dict[str, str]:
        """Create UAT test schedule."""
        base_date = datetime.now()
        schedule = {}
        
        cumulative_days = 0
        for stage in self.uat_workflow_stages:
            start_date = base_date + timedelta(days=cumulative_days)
            end_date = start_date + timedelta(days=stage["duration_days"])
            
            schedule[stage["stage"]] = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "duration_days": stage["duration_days"],
                "activities": stage["activities"]
            }
            
            cumulative_days += stage["duration_days"]
        
        return schedule
    
    def _define_success_metrics(self, user_stories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Define success metrics for UAT."""
        return {
            "overall_approval_rate": {"target": 85, "unit": "percentage"},
            "stakeholder_satisfaction": {"target": 4.0, "unit": "1-5_scale"},
            "training_effectiveness": {"target": 90, "unit": "percentage"},
            "critical_issues": {"target": 0, "unit": "count"},
            "deployment_readiness": {"target": 90, "unit": "percentage"},
            "user_adoption_likelihood": {"target": 80, "unit": "percentage"}
        }
    
    def _identify_risk_mitigation_strategies(
        self,
        implementation_data: Dict[str, Any]
    ) -> List[str]:
        """Identify risk mitigation strategies for UAT."""
        strategies = [
            "Conduct thorough stakeholder briefings before testing",
            "Provide clear testing instructions and support",
            "Have technical support available during testing sessions",
            "Plan for iterative feedback and quick fixes",
            "Prepare rollback plan if critical issues are found"
        ]
        
        # Add specific strategies based on implementation complexity
        ui_components = implementation_data.get("ui_components", [])
        if len(ui_components) > 10:
            strategies.append("Break complex UI testing into manageable sessions")
        
        api_endpoints = implementation_data.get("api_endpoints", [])
        if len(api_endpoints) > 5:
            strategies.append("Prepare API testing documentation and tools")
        
        return strategies
    
    async def _execute_stakeholder_testing(
        self,
        test_plan: UATTestPlan,
        implementation_data: Dict[str, Any],
        stakeholder_roles: List[StakeholderRole]
    ) -> List[StakeholderFeedback]:
        """Execute stakeholder testing sessions."""
        feedback_list = []
        
        for role in stakeholder_roles:
            feedback = await self._simulate_stakeholder_session(
                role, test_plan, implementation_data
            )
            feedback_list.append(feedback)
        
        return feedback_list
    
    async def _simulate_stakeholder_session(
        self,
        stakeholder_role: StakeholderRole,
        test_plan: UATTestPlan,
        implementation_data: Dict[str, Any]
    ) -> StakeholderFeedback:
        """Simulate a stakeholder testing session."""
        stakeholder_info = self.stakeholder_definitions.get(stakeholder_role)
        
        # Simulate stakeholder evaluation based on their focus areas
        focus_areas = stakeholder_info.get("focus_areas", [])
        typical_concerns = stakeholder_info.get("typical_concerns", [])
        
        # Calculate satisfaction score based on stakeholder perspective
        satisfaction_score = self._calculate_stakeholder_satisfaction(
            stakeholder_role, implementation_data, focus_areas
        )
        
        # Determine approval status based on satisfaction
        approval_status = self._determine_stakeholder_approval(satisfaction_score, typical_concerns)
        
        # Generate realistic feedback
        specific_feedback = self._generate_stakeholder_feedback(
            stakeholder_role, satisfaction_score, focus_areas
        )
        
        concerns = self._generate_stakeholder_concerns(
            stakeholder_role, satisfaction_score, typical_concerns
        )
        
        suggestions = self._generate_improvement_suggestions(
            stakeholder_role, satisfaction_score, focus_areas
        )
        
        conditions = self._generate_approval_conditions(
            stakeholder_role, approval_status, concerns
        )
        
        return StakeholderFeedback(
            stakeholder_role=stakeholder_role,
            feedback_timestamp=datetime.now().isoformat(),
            approval_status=approval_status,
            satisfaction_score=round(satisfaction_score, 1),
            specific_feedback=specific_feedback,
            concerns_raised=concerns,
            improvement_suggestions=suggestions,
            conditions_for_approval=conditions
        )
    
    def _calculate_stakeholder_satisfaction(
        self,
        stakeholder_role: StakeholderRole,
        implementation_data: Dict[str, Any],
        focus_areas: List[str]
    ) -> float:
        """Calculate stakeholder satisfaction score."""
        base_satisfaction = 4.0  # Start with good baseline
        
        ui_components = implementation_data.get("ui_components", [])
        api_endpoints = implementation_data.get("api_endpoints", [])
        user_flows = implementation_data.get("user_flows", [])
        
        # Adjust based on stakeholder-specific concerns
        if stakeholder_role == StakeholderRole.TRAINING_COORDINATOR:
            # Focus on learning effectiveness and user experience
            if len(ui_components) > 3:
                base_satisfaction += 0.3  # Good UI for training
            if len(user_flows) > 1:
                base_satisfaction += 0.2  # Clear workflows
        
        elif stakeholder_role == StakeholderRole.IT_COORDINATOR:
            # Focus on technical implementation
            if len(api_endpoints) > 0:
                base_satisfaction += 0.3  # Good technical structure
            if "security" in str(implementation_data).lower():
                base_satisfaction += 0.2  # Security considerations
        
        elif stakeholder_role == StakeholderRole.END_USER_REPRESENTATIVE:
            # Focus on usability
            if len(ui_components) <= 5:
                base_satisfaction += 0.3  # Simple interface preferred
            if "accessibility" in str(implementation_data).lower():
                base_satisfaction += 0.2  # Accessibility important
        
        elif stakeholder_role == StakeholderRole.COMPLIANCE_OFFICER:
            # Focus on compliance
            if "gdpr" in str(implementation_data).lower():
                base_satisfaction += 0.4  # GDPR compliance crucial
            if "audit" in str(implementation_data).lower():
                base_satisfaction += 0.1  # Audit trail important
        
        # Add some realistic variation
        import random
        variation = random.uniform(-0.3, 0.3)
        final_satisfaction = base_satisfaction + variation
        
        return max(1.0, min(5.0, final_satisfaction))
    
    def _determine_stakeholder_approval(
        self,
        satisfaction_score: float,
        typical_concerns: List[str]
    ) -> ApprovalStatus:
        """Determine stakeholder approval status."""
        if satisfaction_score >= 4.5:
            return ApprovalStatus.APPROVED
        elif satisfaction_score >= 4.0:
            return ApprovalStatus.APPROVED_WITH_CONDITIONS
        elif satisfaction_score >= 3.0:
            return ApprovalStatus.NEEDS_REVISION
        else:
            return ApprovalStatus.REJECTED
    
    def _generate_stakeholder_feedback(
        self,
        stakeholder_role: StakeholderRole,
        satisfaction_score: float,
        focus_areas: List[str]
    ) -> List[str]:
        """Generate realistic stakeholder feedback."""
        feedback = []
        
        if satisfaction_score >= 4.0:
            feedback.extend([
                "Overall implementation meets our requirements",
                "User interface is intuitive and well-designed",
                "Functionality aligns with our operational needs"
            ])
        
        if stakeholder_role == StakeholderRole.TRAINING_COORDINATOR:
            if satisfaction_score >= 4.0:
                feedback.append("Training content is well-structured and engaging")
            else:
                feedback.append("Training effectiveness could be improved")
        
        elif stakeholder_role == StakeholderRole.IT_COORDINATOR:
            if satisfaction_score >= 4.0:
                feedback.append("Technical implementation is solid and secure")
            else:
                feedback.append("Technical architecture needs refinement")
        
        elif stakeholder_role == StakeholderRole.END_USER_REPRESENTATIVE:
            if satisfaction_score >= 4.0:
                feedback.append("System is user-friendly and efficient")
            else:
                feedback.append("User experience needs improvement")
        
        return feedback
    
    def _generate_stakeholder_concerns(
        self,
        stakeholder_role: StakeholderRole,
        satisfaction_score: float,
        typical_concerns: List[str]
    ) -> List[str]:
        """Generate realistic stakeholder concerns."""
        concerns = []
        
        if satisfaction_score < 4.0:
            # Add role-specific concerns when satisfaction is low
            if stakeholder_role == StakeholderRole.MUNICIPAL_MANAGER:
                concerns.extend([
                    "Implementation timeline may be optimistic",
                    "Change management planning needs attention"
                ])
            elif stakeholder_role == StakeholderRole.COMPLIANCE_OFFICER:
                concerns.extend([
                    "Audit trail documentation could be more comprehensive",
                    "Compliance validation process needs strengthening"
                ])
            elif stakeholder_role == StakeholderRole.END_USER_REPRESENTATIVE:
                concerns.extend([
                    "Learning curve may be steep for some users",
                    "Mobile access could be improved"
                ])
        
        return concerns
    
    def _generate_improvement_suggestions(
        self,
        stakeholder_role: StakeholderRole,
        satisfaction_score: float,
        focus_areas: List[str]
    ) -> List[str]:
        """Generate improvement suggestions from stakeholder."""
        suggestions = []
        
        if satisfaction_score < 4.5:
            # General improvement suggestions
            suggestions.append("Consider additional user testing before deployment")
            
            if stakeholder_role == StakeholderRole.TRAINING_COORDINATOR:
                suggestions.extend([
                    "Add more interactive elements to training content",
                    "Include progress tracking and completion certificates"
                ])
            elif stakeholder_role == StakeholderRole.IT_COORDINATOR:
                suggestions.extend([
                    "Implement additional security monitoring",
                    "Add comprehensive error logging"
                ])
            elif stakeholder_role == StakeholderRole.END_USER_REPRESENTATIVE:
                suggestions.extend([
                    "Provide more contextual help and guidance",
                    "Simplify navigation for new users"
                ])
        
        return suggestions
    
    def _generate_approval_conditions(
        self,
        stakeholder_role: StakeholderRole,
        approval_status: ApprovalStatus,
        concerns: List[str]
    ) -> List[str]:
        """Generate conditions for approval."""
        conditions = []
        
        if approval_status == ApprovalStatus.APPROVED_WITH_CONDITIONS:
            conditions.extend([
                "Provide comprehensive user training before rollout",
                "Establish clear support procedures for users"
            ])
            
            if concerns:
                conditions.append("Address specific concerns raised during testing")
        
        elif approval_status == ApprovalStatus.NEEDS_REVISION:
            conditions.extend([
                "Resolve identified usability issues",
                "Conduct additional stakeholder review after changes"
            ])
        
        return conditions
    
    async def _assess_training_effectiveness(
        self,
        implementation_data: Dict[str, Any],
        test_plan: UATTestPlan
    ) -> TrainingEffectivenessResult:
        """Assess training effectiveness of implementation."""
        # Simulate training effectiveness assessment
        ui_components = implementation_data.get("ui_components", [])
        user_flows = implementation_data.get("user_flows", [])
        
        # Calculate effectiveness metrics based on implementation quality
        learning_objectives_met = len(ui_components) > 0 and len(user_flows) > 0
        knowledge_retention = min(95.0, 70.0 + (len(ui_components) * 3))
        skill_application = min(95.0, 65.0 + (len(user_flows) * 5))
        confidence_improvement = min(90.0, 60.0 + (len(ui_components) * 2))
        time_to_competency = max(15.0, 45.0 - (len(ui_components) * 2))
        
        # Simulate post-training performance
        post_training_performance = {
            "task_completion_rate": min(95.0, 80.0 + (len(user_flows) * 3)),
            "error_rate": max(2.0, 10.0 - (len(ui_components) * 0.5)),
            "user_satisfaction": min(4.8, 3.5 + (len(ui_components) * 0.2))
        }
        
        # Identify areas needing improvement
        areas_needing_improvement = []
        if knowledge_retention < 85:
            areas_needing_improvement.append("Knowledge retention mechanisms")
        if skill_application < 80:
            areas_needing_improvement.append("Practical skill application")
        if confidence_improvement < 70:
            areas_needing_improvement.append("User confidence building")
        
        return TrainingEffectivenessResult(
            learning_objectives_met=learning_objectives_met,
            knowledge_retention_score=round(knowledge_retention, 1),
            skill_application_score=round(skill_application, 1),
            confidence_improvement=round(confidence_improvement, 1),
            time_to_competency_minutes=round(time_to_competency, 1),
            post_training_performance=post_training_performance,
            areas_needing_improvement=areas_needing_improvement
        )
    
    async def _validate_acceptance_criteria(
        self,
        test_plan: UATTestPlan,
        stakeholder_feedback: List[StakeholderFeedback],
        training_effectiveness: TrainingEffectivenessResult
    ) -> List[Dict[str, Any]]:
        """Validate acceptance criteria against results."""
        criteria_results = []
        
        for criteria in test_plan.acceptance_criteria:
            # Determine if criteria was met based on stakeholder feedback
            responsible_stakeholder = criteria.stakeholder_role
            stakeholder_input = next(
                (f for f in stakeholder_feedback if f.stakeholder_role == responsible_stakeholder),
                None
            )
            
            if stakeholder_input:
                criteria_met = stakeholder_input.approval_status in [
                    ApprovalStatus.APPROVED, 
                    ApprovalStatus.APPROVED_WITH_CONDITIONS
                ]
                confidence_score = stakeholder_input.satisfaction_score / 5 * 100
            else:
                criteria_met = training_effectiveness.learning_objectives_met
                confidence_score = 70.0  # Default confidence
            
            criteria_results.append({
                "criteria_id": criteria.criteria_id,
                "description": criteria.description,
                "met": criteria_met,
                "confidence_score": confidence_score,
                "responsible_stakeholder": responsible_stakeholder.value,
                "evidence": stakeholder_input.specific_feedback if stakeholder_input else []
            })
        
        return criteria_results
    
    def _determine_overall_approval_status(
        self,
        stakeholder_feedback: List[StakeholderFeedback],
        criteria_results: List[Dict[str, Any]]
    ) -> ApprovalStatus:
        """Determine overall UAT approval status."""
        if not stakeholder_feedback:
            return ApprovalStatus.PENDING_REVIEW
        
        # Calculate weighted approval score
        total_weight = 0
        weighted_score = 0
        
        for feedback in stakeholder_feedback:
            stakeholder_info = self.stakeholder_definitions.get(feedback.stakeholder_role)
            if stakeholder_info:
                weight = stakeholder_info["approval_weight"]
                total_weight += weight
                
                # Convert approval status to numeric score
                status_scores = {
                    ApprovalStatus.APPROVED: 5.0,
                    ApprovalStatus.APPROVED_WITH_CONDITIONS: 4.0,
                    ApprovalStatus.NEEDS_REVISION: 2.0,
                    ApprovalStatus.REJECTED: 1.0
                }
                
                status_score = status_scores.get(feedback.approval_status, 2.0)
                weighted_score += weight * status_score
        
        if total_weight > 0:
            overall_score = weighted_score / total_weight
            
            if overall_score >= 4.5:
                return ApprovalStatus.APPROVED
            elif overall_score >= 3.5:
                return ApprovalStatus.APPROVED_WITH_CONDITIONS
            elif overall_score >= 2.0:
                return ApprovalStatus.NEEDS_REVISION
            else:
                return ApprovalStatus.REJECTED
        
        return ApprovalStatus.PENDING_REVIEW
    
    def _calculate_deployment_readiness_score(
        self,
        stakeholder_feedback: List[StakeholderFeedback],
        training_effectiveness: TrainingEffectivenessResult,
        criteria_results: List[Dict[str, Any]]
    ) -> float:
        """Calculate deployment readiness score."""
        readiness_factors = []
        
        # Stakeholder satisfaction factor (40% weight)
        if stakeholder_feedback:
            avg_satisfaction = sum(f.satisfaction_score for f in stakeholder_feedback) / len(stakeholder_feedback)
            readiness_factors.extend([avg_satisfaction / 5 * 100] * 4)  # 40% weight
        
        # Training effectiveness factor (30% weight)
        effectiveness_score = (
            training_effectiveness.knowledge_retention_score * 0.4 +
            training_effectiveness.skill_application_score * 0.4 +
            training_effectiveness.confidence_improvement * 0.2
        )
        readiness_factors.extend([effectiveness_score] * 3)  # 30% weight
        
        # Acceptance criteria factor (30% weight)
        if criteria_results:
            criteria_met = sum(1 for c in criteria_results if c["met"]) / len(criteria_results) * 100
            readiness_factors.extend([criteria_met] * 3)  # 30% weight
        
        return round(sum(readiness_factors) / len(readiness_factors) if readiness_factors else 0.0, 1)
    
    def _identify_critical_uat_issues(
        self,
        stakeholder_feedback: List[StakeholderFeedback],
        criteria_results: List[Dict[str, Any]]
    ) -> List[str]:
        """Identify critical issues from UAT."""
        critical_issues = []
        
        # Check for stakeholder rejections
        rejected_stakeholders = [
            f.stakeholder_role.value for f in stakeholder_feedback
            if f.approval_status == ApprovalStatus.REJECTED
        ]
        
        if rejected_stakeholders:
            critical_issues.append(f"Stakeholder rejection from: {', '.join(rejected_stakeholders)}")
        
        # Check for failed must-have criteria
        failed_must_haves = [
            c["description"] for c in criteria_results
            if not c["met"] and "must_have" in c.get("priority", "")
        ]
        
        if failed_must_haves:
            critical_issues.extend([f"Failed must-have criteria: {desc}" for desc in failed_must_haves])
        
        # Check for major concerns
        major_concerns = []
        for feedback in stakeholder_feedback:
            major_concerns.extend(feedback.concerns_raised)
        
        if len(major_concerns) > 5:
            critical_issues.append("High number of stakeholder concerns raised")
        
        return critical_issues
    
    def _generate_uat_recommendations(
        self,
        overall_status: ApprovalStatus,
        stakeholder_feedback: List[StakeholderFeedback],
        critical_issues: List[str]
    ) -> List[str]:
        """Generate UAT recommendations."""
        recommendations = []
        
        if overall_status == ApprovalStatus.APPROVED:
            recommendations.extend([
                "Proceed with deployment planning",
                "Prepare user training materials",
                "Set up production monitoring"
            ])
        
        elif overall_status == ApprovalStatus.APPROVED_WITH_CONDITIONS:
            recommendations.extend([
                "Address stakeholder conditions before deployment",
                "Plan phased rollout to manage risk",
                "Establish post-deployment support"
            ])
        
        elif overall_status == ApprovalStatus.NEEDS_REVISION:
            recommendations.extend([
                "Address identified issues before re-testing",
                "Conduct focused stakeholder sessions on problem areas",
                "Revise implementation based on feedback"
            ])
        
        elif overall_status == ApprovalStatus.REJECTED:
            recommendations.extend([
                "Conduct thorough analysis of rejection reasons",
                "Redesign solution to address fundamental issues",
                "Re-engage stakeholders in solution design"
            ])
        
        # Add specific recommendations based on feedback
        for feedback in stakeholder_feedback:
            recommendations.extend(feedback.improvement_suggestions[:1])  # Top suggestion per stakeholder
        
        return list(set(recommendations))  # Remove duplicates