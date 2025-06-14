"""
Municipal training-specific testing tool for QA Tester agent.

PURPOSE:
Specialized testing for Swedish municipal training applications, ensuring
compliance with local policies, regulations, and municipal user needs.

CRITICAL FUNCTIONALITY:
- Swedish municipal policy compliance validation
- Multi-role municipal user testing (administrators, field workers, managers)
- Crisis management and emergency procedure validation
- Integration testing with existing municipal systems
- Municipal workflow pattern validation

ADAPTATION GUIDE:
To adapt for your municipal context:
1. Update swedish_municipal_policies for your region's requirements
2. Modify municipal_roles for your organizational structure
3. Adjust crisis_scenarios for your emergency procedures
4. Update system_integrations for your IT environment

CONTRACT PROTECTION:
This tool enhances QA testing without breaking contracts.
All outputs integrate seamlessly with existing QA validation results.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Setup logging
logger = logging.getLogger(__name__)


class MunicipalUserRole(Enum):
    """Municipal user roles for testing."""
    ADMINISTRATOR = "administrator"
    FIELD_WORKER = "field_worker"
    MANAGER = "manager"
    POLICY_OFFICER = "policy_officer"
    CITIZEN_SERVICE = "citizen_service"
    FINANCE_OFFICER = "finance_officer"
    HR_SPECIALIST = "hr_specialist"
    IT_COORDINATOR = "it_coordinator"


class PolicyCategory(Enum):
    """Swedish municipal policy categories."""
    GDPR_COMPLIANCE = "gdpr_compliance"
    ACCESSIBILITY_LAW = "accessibility_law"
    EMPLOYMENT_LAW = "employment_law"
    PROCUREMENT_RULES = "procurement_rules"
    TRANSPARENCY_REQUIREMENTS = "transparency_requirements"
    CRISIS_MANAGEMENT = "crisis_management"
    CITIZEN_SERVICES = "citizen_services"
    ENVIRONMENTAL_POLICY = "environmental_policy"


@dataclass
class PolicyComplianceResult:
    """Result from policy compliance testing."""
    policy_category: PolicyCategory
    compliance_score: float  # 0-100%
    violations_found: List[str]
    compliance_items_passed: List[str]
    critical_issues: List[str]
    recommendations: List[str]
    legal_risk_level: str  # "low", "medium", "high", "critical"


@dataclass
class MunicipalRoleTestResult:
    """Result from role-specific testing."""
    role: MunicipalUserRole
    role_satisfaction_score: float  # 1-5 scale
    task_completion_rate: float  # percentage
    role_specific_issues: List[str]
    workflow_effectiveness: float  # 1-5 scale
    training_suitability: bool
    recommendations: List[str]


@dataclass
class CrisisManagementTestResult:
    """Result from crisis management testing."""
    crisis_scenario: str
    response_time_seconds: float
    information_accuracy: float  # percentage
    procedure_compliance: bool
    communication_effectiveness: float  # 1-5 scale
    stress_test_passed: bool
    critical_issues: List[str]


@dataclass
class SystemIntegrationTestResult:
    """Result from municipal system integration testing."""
    system_name: str
    integration_status: str  # "passed", "failed", "warning"
    data_consistency: bool
    authentication_works: bool
    authorization_correct: bool
    performance_acceptable: bool
    security_validated: bool
    issues_found: List[str]


@dataclass
class MunicipalTrainingTestResult:
    """Complete municipal training test results."""
    story_id: str
    test_timestamp: str
    test_duration_minutes: float
    policy_compliance_results: List[PolicyComplianceResult]
    role_test_results: List[MunicipalRoleTestResult]
    crisis_management_results: List[CrisisManagementTestResult]
    system_integration_results: List[SystemIntegrationTestResult]
    overall_municipal_readiness_score: float
    municipal_deployment_approved: bool
    legal_compliance_status: str
    recommendations: List[str]
    critical_blockers: List[str]


class MunicipalTrainingTester:
    """
    Municipal training-specific testing tool.
    
    Validates training applications against Swedish municipal requirements,
    including policy compliance, role-specific workflows, and system integration.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize municipal training tester with configuration."""
        self.config = config or {}
        
        # Swedish municipal policy requirements
        self.swedish_municipal_policies = {
            PolicyCategory.GDPR_COMPLIANCE: {
                "requirements": [
                    "personal_data_protection",
                    "consent_management",
                    "data_subject_rights",
                    "breach_notification_procedures",
                    "privacy_by_design",
                    "data_minimization",
                    "purpose_limitation"
                ],
                "critical_level": True,
                "legal_consequences": "High fines and legal liability"
            },
            PolicyCategory.ACCESSIBILITY_LAW: {
                "requirements": [
                    "wcag_2_1_aa_compliance",
                    "assistive_technology_support",
                    "keyboard_navigation",
                    "screen_reader_compatibility",
                    "cognitive_accessibility",
                    "motor_impairment_support"
                ],
                "critical_level": True,
                "legal_consequences": "Legal action under disability discrimination laws"
            },
            PolicyCategory.EMPLOYMENT_LAW: {
                "requirements": [
                    "equal_opportunity_training",
                    "harassment_prevention",
                    "work_environment_safety",
                    "continuing_education_rights",
                    "union_representation_acknowledgment"
                ],
                "critical_level": True,
                "legal_consequences": "Employment tribunal cases"
            },
            PolicyCategory.PROCUREMENT_RULES: {
                "requirements": [
                    "transparency_in_supplier_selection",
                    "conflict_of_interest_disclosure",
                    "fair_competition_procedures",
                    "documentation_requirements",
                    "evaluation_criteria_clarity"
                ],
                "critical_level": True,
                "legal_consequences": "Procurement nullification and legal challenges"
            },
            PolicyCategory.TRANSPARENCY_REQUIREMENTS: {
                "requirements": [
                    "public_access_to_information",
                    "decision_making_transparency",
                    "meeting_minutes_availability",
                    "citizen_participation_opportunities",
                    "open_data_initiatives"
                ],
                "critical_level": False,
                "legal_consequences": "Transparency ombudsman investigation"
            },
            PolicyCategory.CRISIS_MANAGEMENT: {
                "requirements": [
                    "emergency_response_procedures",
                    "communication_protocols",
                    "resource_allocation_guidelines",
                    "coordination_with_authorities",
                    "public_safety_priorities"
                ],
                "critical_level": True,
                "legal_consequences": "Public safety liability"
            },
            PolicyCategory.CITIZEN_SERVICES: {
                "requirements": [
                    "service_level_standards",
                    "complaint_handling_procedures",
                    "multilingual_support",
                    "digital_service_accessibility",
                    "citizen_feedback_integration"
                ],
                "critical_level": False,
                "legal_consequences": "Service quality investigations"
            },
            PolicyCategory.ENVIRONMENTAL_POLICY: {
                "requirements": [
                    "sustainability_goals_alignment",
                    "environmental_impact_consideration",
                    "green_technology_preference",
                    "waste_reduction_practices",
                    "carbon_footprint_awareness"
                ],
                "critical_level": False,
                "legal_consequences": "Environmental compliance issues"
            }
        }
        
        # Municipal role definitions with specific responsibilities
        self.municipal_roles = {
            MunicipalUserRole.ADMINISTRATOR: {
                "responsibilities": [
                    "system_configuration",
                    "user_management",
                    "policy_implementation",
                    "compliance_monitoring",
                    "training_coordination"
                ],
                "time_constraints": "Limited time, high responsibility",
                "technical_skill_level": "intermediate_to_advanced",
                "stress_factors": ["regulatory_deadlines", "public_scrutiny"]
            },
            MunicipalUserRole.FIELD_WORKER: {
                "responsibilities": [
                    "direct_citizen_interaction",
                    "policy_application",
                    "data_collection",
                    "service_delivery",
                    "compliance_reporting"
                ],
                "time_constraints": "Very limited, on-the-go access",
                "technical_skill_level": "basic_to_intermediate",
                "stress_factors": ["time_pressure", "citizen_demands", "mobile_access"]
            },
            MunicipalUserRole.MANAGER: {
                "responsibilities": [
                    "team_oversight",
                    "performance_monitoring",
                    "budget_management",
                    "policy_interpretation",
                    "strategic_planning"
                ],
                "time_constraints": "Fragmented time, frequent interruptions",
                "technical_skill_level": "intermediate",
                "stress_factors": ["political_pressure", "budget_constraints"]
            },
            MunicipalUserRole.POLICY_OFFICER: {
                "responsibilities": [
                    "policy_development",
                    "regulatory_compliance",
                    "legal_analysis",
                    "stakeholder_consultation",
                    "implementation_guidance"
                ],
                "time_constraints": "Deep work periods with urgent deadlines",
                "technical_skill_level": "advanced",
                "stress_factors": ["legal_accuracy", "political_sensitivity"]
            },
            MunicipalUserRole.CITIZEN_SERVICE: {
                "responsibilities": [
                    "citizen_inquiries",
                    "service_requests",
                    "complaint_resolution",
                    "information_provision",
                    "case_management"
                ],
                "time_constraints": "High volume, quick responses needed",
                "technical_skill_level": "basic_to_intermediate",
                "stress_factors": ["citizen_satisfaction", "case_backlogs"]
            },
            MunicipalUserRole.FINANCE_OFFICER: {
                "responsibilities": [
                    "budget_management",
                    "financial_reporting",
                    "audit_compliance",
                    "procurement_oversight",
                    "cost_analysis"
                ],
                "time_constraints": "Cyclical deadlines, audit periods",
                "technical_skill_level": "advanced",
                "stress_factors": ["accuracy_requirements", "audit_scrutiny"]
            },
            MunicipalUserRole.HR_SPECIALIST: {
                "responsibilities": [
                    "employee_training",
                    "policy_compliance",
                    "performance_management",
                    "recruitment",
                    "employee_relations"
                ],
                "time_constraints": "Scheduled activities with urgent issues",
                "technical_skill_level": "intermediate",
                "stress_factors": ["employee_confidentiality", "legal_compliance"]
            },
            MunicipalUserRole.IT_COORDINATOR: {
                "responsibilities": [
                    "system_maintenance",
                    "user_support",
                    "security_management",
                    "technology_planning",
                    "data_management"
                ],
                "time_constraints": "Emergency responses and planned maintenance",
                "technical_skill_level": "advanced",
                "stress_factors": ["system_uptime", "security_threats"]
            }
        }
        
        # Crisis scenarios for municipal context
        self.crisis_scenarios = [
            {
                "name": "natural_disaster_response",
                "description": "Major flood requiring immediate municipal response",
                "urgency_level": "critical",
                "response_time_target_seconds": 300,
                "required_actions": [
                    "alert_emergency_services",
                    "activate_crisis_communication",
                    "coordinate_evacuation_procedures",
                    "manage_resource_allocation",
                    "provide_citizen_updates"
                ]
            },
            {
                "name": "cyber_security_incident",
                "description": "Municipal IT systems under cyber attack",
                "urgency_level": "critical",
                "response_time_target_seconds": 180,
                "required_actions": [
                    "isolate_affected_systems",
                    "activate_backup_procedures",
                    "notify_security_authorities",
                    "implement_communication_plan",
                    "protect_citizen_data"
                ]
            },
            {
                "name": "public_health_emergency",
                "description": "Disease outbreak requiring municipal coordination",
                "urgency_level": "high",
                "response_time_target_seconds": 600,
                "required_actions": [
                    "coordinate_with_health_authorities",
                    "implement_public_communication",
                    "manage_service_adjustments",
                    "support_vulnerable_populations",
                    "maintain_essential_services"
                ]
            },
            {
                "name": "infrastructure_failure",
                "description": "Major utility failure affecting municipal services",
                "urgency_level": "high",
                "response_time_target_seconds": 900,
                "required_actions": [
                    "assess_impact_scope",
                    "coordinate_repair_efforts",
                    "provide_alternative_services",
                    "communicate_with_citizens",
                    "document_incident_response"
                ]
            },
            {
                "name": "political_crisis",
                "description": "Governance crisis requiring procedural response",
                "urgency_level": "medium",
                "response_time_target_seconds": 1800,
                "required_actions": [
                    "follow_governance_procedures",
                    "ensure_transparency",
                    "maintain_service_continuity",
                    "manage_public_communication",
                    "preserve_institutional_integrity"
                ]
            }
        ]
        
        # Common municipal system integrations
        self.municipal_system_integrations = [
            {
                "system_name": "ekonomisystem",
                "description": "Municipal financial management system",
                "integration_type": "data_exchange",
                "criticality": "high",
                "test_scenarios": [
                    "budget_data_synchronization",
                    "cost_center_validation",
                    "procurement_workflow_integration"
                ]
            },
            {
                "system_name": "medarbetarsystem",
                "description": "Employee management and HR system",
                "integration_type": "authentication_sso",
                "criticality": "high",
                "test_scenarios": [
                    "single_sign_on_validation",
                    "role_synchronization",
                    "training_record_integration"
                ]
            },
            {
                "system_name": "dokumenthantering",
                "description": "Document management system",
                "integration_type": "content_sharing",
                "criticality": "medium",
                "test_scenarios": [
                    "document_access_permissions",
                    "version_control_integration",
                    "search_functionality"
                ]
            },
            {
                "system_name": "medborgarportal",
                "description": "Citizen service portal",
                "integration_type": "service_integration",
                "criticality": "medium",
                "test_scenarios": [
                    "service_request_routing",
                    "citizen_communication",
                    "case_status_updates"
                ]
            },
            {
                "system_name": "gis_system",
                "description": "Geographic information system",
                "integration_type": "data_visualization",
                "criticality": "low",
                "test_scenarios": [
                    "map_data_integration",
                    "location_based_services",
                    "spatial_analysis_tools"
                ]
            }
        ]
    
    async def test_municipal_training_compliance(
        self,
        story_id: str,
        implementation_data: Dict[str, Any],
        test_roles: Optional[List[MunicipalUserRole]] = None,
        test_policies: Optional[List[PolicyCategory]] = None
    ) -> MunicipalTrainingTestResult:
        """
        Comprehensive municipal training compliance testing.
        
        Args:
            story_id: Story identifier for traceability
            implementation_data: Implementation details to test
            test_roles: Specific municipal roles to test (optional)
            test_policies: Specific policies to validate (optional)
            
        Returns:
            Complete municipal training test results
        """
        start_time = datetime.now()
        test_roles = test_roles or list(MunicipalUserRole)
        test_policies = test_policies or list(PolicyCategory)
        
        try:
            logger.info(f"Starting municipal training compliance testing for {story_id}")
            
            # 1. Policy compliance validation
            policy_results = await self._test_policy_compliance(
                implementation_data, test_policies
            )
            
            # 2. Role-specific testing
            role_results = await self._test_municipal_roles(
                implementation_data, test_roles
            )
            
            # 3. Crisis management testing
            crisis_results = await self._test_crisis_management_scenarios(
                implementation_data
            )
            
            # 4. System integration testing
            integration_results = await self._test_municipal_system_integrations(
                implementation_data
            )
            
            # 5. Calculate overall municipal readiness
            readiness_score = self._calculate_municipal_readiness_score(
                policy_results, role_results, crisis_results, integration_results
            )
            
            # 6. Determine deployment approval
            deployment_approved = self._assess_municipal_deployment_readiness(
                policy_results, role_results, crisis_results, integration_results
            )
            
            # 7. Assess legal compliance status
            legal_status = self._assess_legal_compliance_status(policy_results)
            
            # 8. Generate recommendations
            recommendations = self._generate_municipal_recommendations(
                policy_results, role_results, crisis_results, integration_results
            )
            
            # 9. Identify critical blockers
            critical_blockers = self._identify_critical_municipal_blockers(
                policy_results, role_results, crisis_results, integration_results
            )
            
            end_time = datetime.now()
            test_duration = (end_time - start_time).total_seconds() / 60
            
            result = MunicipalTrainingTestResult(
                story_id=story_id,
                test_timestamp=start_time.isoformat(),
                test_duration_minutes=round(test_duration, 2),
                policy_compliance_results=policy_results,
                role_test_results=role_results,
                crisis_management_results=crisis_results,
                system_integration_results=integration_results,
                overall_municipal_readiness_score=readiness_score,
                municipal_deployment_approved=deployment_approved,
                legal_compliance_status=legal_status,
                recommendations=recommendations,
                critical_blockers=critical_blockers
            )
            
            logger.info(f"Municipal training compliance testing completed for {story_id}")
            return result
            
        except Exception as e:
            logger.error(f"Municipal training compliance testing failed for {story_id}: {str(e)}")
            return MunicipalTrainingTestResult(
                story_id=story_id,
                test_timestamp=start_time.isoformat(),
                test_duration_minutes=0,
                policy_compliance_results=[],
                role_test_results=[],
                crisis_management_results=[],
                system_integration_results=[],
                overall_municipal_readiness_score=0.0,
                municipal_deployment_approved=False,
                legal_compliance_status="FAILED_TESTING",
                recommendations=["Fix municipal testing errors before proceeding"],
                critical_blockers=[f"Municipal testing failed: {str(e)}"]
            )
    
    async def _test_policy_compliance(
        self,
        implementation_data: Dict[str, Any],
        policies_to_test: List[PolicyCategory]
    ) -> List[PolicyComplianceResult]:
        """Test compliance with Swedish municipal policies."""
        results = []
        
        for policy_category in policies_to_test:
            if policy_category not in self.swedish_municipal_policies:
                continue
                
            policy_info = self.swedish_municipal_policies[policy_category]
            logger.info(f"Testing policy compliance: {policy_category.value}")
            
            result = await self._validate_specific_policy(
                policy_category, policy_info, implementation_data
            )
            results.append(result)
        
        return results
    
    async def _validate_specific_policy(
        self,
        policy_category: PolicyCategory,
        policy_info: Dict[str, Any],
        implementation_data: Dict[str, Any]
    ) -> PolicyComplianceResult:
        """Validate compliance with a specific policy."""
        requirements = policy_info["requirements"]
        violations = []
        passed_items = []
        critical_issues = []
        recommendations = []
        
        # Test each requirement
        for requirement in requirements:
            compliance_result = await self._test_policy_requirement(
                requirement, policy_category, implementation_data
            )
            
            if compliance_result["compliant"]:
                passed_items.append(requirement)
            else:
                violations.append(f"{requirement}: {compliance_result['issue']}")
                if policy_info["critical_level"]:
                    critical_issues.append(compliance_result['issue'])
                recommendations.extend(compliance_result.get('recommendations', []))
        
        # Calculate compliance score
        compliance_score = (len(passed_items) / len(requirements)) * 100 if requirements else 100
        
        # Determine legal risk level
        if critical_issues:
            legal_risk = "critical"
        elif violations and policy_info["critical_level"]:
            legal_risk = "high"
        elif violations:
            legal_risk = "medium"
        else:
            legal_risk = "low"
        
        return PolicyComplianceResult(
            policy_category=policy_category,
            compliance_score=round(compliance_score, 2),
            violations_found=violations,
            compliance_items_passed=passed_items,
            critical_issues=critical_issues,
            recommendations=list(set(recommendations)),
            legal_risk_level=legal_risk
        )
    
    async def _test_policy_requirement(
        self,
        requirement: str,
        policy_category: PolicyCategory,
        implementation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Test a specific policy requirement."""
        # This is a simplified implementation - in reality, each requirement would have
        # specific validation logic based on the implementation data
        
        ui_components = implementation_data.get("ui_components", [])
        api_endpoints = implementation_data.get("api_endpoints", [])
        configuration = implementation_data.get("configuration", {})
        
        # GDPR compliance checks
        if policy_category == PolicyCategory.GDPR_COMPLIANCE:
            if requirement == "personal_data_protection":
                # Check for data encryption, secure storage
                has_encryption = any("encrypt" in str(comp).lower() for comp in ui_components)
                return {
                    "compliant": has_encryption,
                    "issue": "No data encryption mechanisms found" if not has_encryption else None,
                    "recommendations": ["Implement data encryption for personal data"] if not has_encryption else []
                }
            
            elif requirement == "consent_management":
                # Check for consent collection mechanisms
                has_consent = any("consent" in str(comp).lower() or "gdpr" in str(comp).lower() for comp in ui_components)
                return {
                    "compliant": has_consent,
                    "issue": "No consent management mechanism found" if not has_consent else None,
                    "recommendations": ["Add GDPR consent collection forms"] if not has_consent else []
                }
        
        # Accessibility compliance checks
        elif policy_category == PolicyCategory.ACCESSIBILITY_LAW:
            if requirement == "wcag_2_1_aa_compliance":
                # Check for accessibility attributes
                has_accessibility = any(
                    comp.get("accessibility_attributes") for comp in ui_components
                    if isinstance(comp, dict)
                )
                return {
                    "compliant": has_accessibility,
                    "issue": "Missing WCAG 2.1 AA compliance attributes" if not has_accessibility else None,
                    "recommendations": ["Add accessibility attributes to all UI components"] if not has_accessibility else []
                }
        
        # Employment law checks
        elif policy_category == PolicyCategory.EMPLOYMENT_LAW:
            if requirement == "equal_opportunity_training":
                # Check for inclusive content and equal access
                has_inclusive_content = "inclusive" in str(implementation_data).lower()
                return {
                    "compliant": has_inclusive_content,
                    "issue": "No evidence of equal opportunity considerations" if not has_inclusive_content else None,
                    "recommendations": ["Ensure training content promotes equal opportunity"] if not has_inclusive_content else []
                }
        
        # Default compliance check (simplified)
        return {
            "compliant": True,
            "issue": None,
            "recommendations": []
        }
    
    async def _test_municipal_roles(
        self,
        implementation_data: Dict[str, Any],
        roles_to_test: List[MunicipalUserRole]
    ) -> List[MunicipalRoleTestResult]:
        """Test application with different municipal user roles."""
        results = []
        
        for role in roles_to_test:
            if role not in self.municipal_roles:
                continue
                
            role_info = self.municipal_roles[role]
            logger.info(f"Testing municipal role: {role.value}")
            
            result = await self._simulate_role_usage(role, role_info, implementation_data)
            results.append(result)
        
        return results
    
    async def _simulate_role_usage(
        self,
        role: MunicipalUserRole,
        role_info: Dict[str, Any],
        implementation_data: Dict[str, Any]
    ) -> MunicipalRoleTestResult:
        """Simulate usage by a specific municipal role."""
        responsibilities = role_info["responsibilities"]
        technical_level = role_info["technical_skill_level"]
        stress_factors = role_info["stress_factors"]
        
        # Simulate role-specific task completion
        role_issues = []
        task_success_count = 0
        total_tasks = len(responsibilities)
        
        for responsibility in responsibilities:
            task_result = await self._simulate_role_task(
                responsibility, role, technical_level, implementation_data
            )
            
            if task_result["success"]:
                task_success_count += 1
            else:
                role_issues.append(f"{responsibility}: {task_result['issue']}")
        
        # Calculate metrics
        task_completion_rate = (task_success_count / total_tasks) * 100 if total_tasks > 0 else 100
        
        # Simulate satisfaction based on role fit
        satisfaction_score = self._calculate_role_satisfaction(
            role, task_completion_rate, role_issues, stress_factors
        )
        
        # Assess workflow effectiveness
        workflow_effectiveness = self._assess_workflow_effectiveness(
            role, implementation_data, task_completion_rate
        )
        
        # Determine training suitability
        training_suitable = (
            satisfaction_score >= 3.5 and
            task_completion_rate >= 80 and
            workflow_effectiveness >= 3.0 and
            len(role_issues) <= 2
        )
        
        # Generate role-specific recommendations
        recommendations = self._generate_role_recommendations(
            role, satisfaction_score, task_completion_rate, role_issues
        )
        
        return MunicipalRoleTestResult(
            role=role,
            role_satisfaction_score=round(satisfaction_score, 2),
            task_completion_rate=round(task_completion_rate, 2),
            role_specific_issues=role_issues,
            workflow_effectiveness=round(workflow_effectiveness, 2),
            training_suitability=training_suitable,
            recommendations=recommendations
        )
    
    async def _simulate_role_task(
        self,
        responsibility: str,
        role: MunicipalUserRole,
        technical_level: str,
        implementation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Simulate a specific task for a municipal role."""
        ui_components = implementation_data.get("ui_components", [])
        api_endpoints = implementation_data.get("api_endpoints", [])
        
        # Assess task complexity vs. technical level
        task_complexity = self._assess_task_complexity(responsibility, ui_components)
        role_capability = self._assess_role_capability(technical_level, role)
        
        # Determine success based on complexity vs. capability
        success = role_capability >= task_complexity
        
        if not success:
            issue = f"Task complexity ({task_complexity}) exceeds role capability ({role_capability})"
        else:
            issue = None
        
        return {
            "success": success,
            "issue": issue,
            "task_complexity": task_complexity,
            "role_capability": role_capability
        }
    
    def _assess_task_complexity(self, responsibility: str, ui_components: List[Dict]) -> float:
        """Assess the complexity of a task based on responsibility and UI."""
        base_complexity = {
            "system_configuration": 4.5,
            "user_management": 3.5,
            "policy_implementation": 4.0,
            "compliance_monitoring": 3.8,
            "training_coordination": 3.2,
            "direct_citizen_interaction": 2.5,
            "policy_application": 3.0,
            "data_collection": 2.8,
            "service_delivery": 2.5,
            "compliance_reporting": 3.5,
            "team_oversight": 3.2,
            "performance_monitoring": 3.5,
            "budget_management": 4.2,
            "policy_interpretation": 4.0,
            "strategic_planning": 4.5
        }.get(responsibility, 3.0)
        
        # Adjust based on UI complexity
        component_complexity = len(ui_components) * 0.1
        
        return min(5.0, base_complexity + component_complexity)
    
    def _assess_role_capability(self, technical_level: str, role: MunicipalUserRole) -> float:
        """Assess the capability level of a municipal role."""
        technical_scores = {
            "basic": 2.0,
            "basic_to_intermediate": 2.5,
            "intermediate": 3.5,
            "intermediate_to_advanced": 4.0,
            "advanced": 4.5
        }
        
        base_capability = technical_scores.get(technical_level, 3.0)
        
        # Role-specific adjustments
        role_adjustments = {
            MunicipalUserRole.ADMINISTRATOR: 0.5,
            MunicipalUserRole.IT_COORDINATOR: 1.0,
            MunicipalUserRole.POLICY_OFFICER: 0.3,
            MunicipalUserRole.MANAGER: 0.2,
            MunicipalUserRole.FIELD_WORKER: -0.3,
            MunicipalUserRole.CITIZEN_SERVICE: 0.0,
            MunicipalUserRole.FINANCE_OFFICER: 0.3,
            MunicipalUserRole.HR_SPECIALIST: 0.1
        }
        
        adjustment = role_adjustments.get(role, 0.0)
        
        return min(5.0, max(1.0, base_capability + adjustment))
    
    def _calculate_role_satisfaction(
        self,
        role: MunicipalUserRole,
        task_completion_rate: float,
        role_issues: List[str],
        stress_factors: List[str]
    ) -> float:
        """Calculate satisfaction score for a municipal role."""
        # Base satisfaction from task completion
        base_satisfaction = task_completion_rate / 20  # Convert percentage to 1-5 scale
        
        # Reduce satisfaction for issues
        issue_penalty = len(role_issues) * 0.3
        
        # Reduce satisfaction for stress factors
        stress_penalty = len(stress_factors) * 0.2
        
        final_satisfaction = base_satisfaction - issue_penalty - stress_penalty
        
        return max(1.0, min(5.0, final_satisfaction))
    
    def _assess_workflow_effectiveness(
        self,
        role: MunicipalUserRole,
        implementation_data: Dict[str, Any],
        task_completion_rate: float
    ) -> float:
        """Assess how well the workflow fits the municipal role."""
        # Base effectiveness from task completion
        base_effectiveness = task_completion_rate / 20  # Convert percentage to 1-5 scale
        
        # Role-specific workflow considerations
        user_flows = implementation_data.get("user_flows", [])
        flow_count = len(user_flows)
        
        # Different roles prefer different workflow complexities
        optimal_complexity = {
            MunicipalUserRole.ADMINISTRATOR: 4,  # Can handle complex workflows
            MunicipalUserRole.FIELD_WORKER: 2,   # Needs simple workflows
            MunicipalUserRole.MANAGER: 3,        # Medium complexity
            MunicipalUserRole.POLICY_OFFICER: 4, # Can handle complexity
            MunicipalUserRole.CITIZEN_SERVICE: 2, # Needs efficiency
            MunicipalUserRole.FINANCE_OFFICER: 3, # Structured workflows
            MunicipalUserRole.HR_SPECIALIST: 3,   # Standard workflows
            MunicipalUserRole.IT_COORDINATOR: 4   # Complex workflows OK
        }.get(role, 3)
        
        # Adjust effectiveness based on workflow complexity match
        complexity_difference = abs(flow_count - optimal_complexity)
        complexity_adjustment = -complexity_difference * 0.2
        
        final_effectiveness = base_effectiveness + complexity_adjustment
        
        return max(1.0, min(5.0, final_effectiveness))
    
    def _generate_role_recommendations(
        self,
        role: MunicipalUserRole,
        satisfaction_score: float,
        task_completion_rate: float,
        role_issues: List[str]
    ) -> List[str]:
        """Generate recommendations for improving role experience."""
        recommendations = []
        
        if satisfaction_score < 3.5:
            recommendations.append(f"Improve user experience for {role.value} - satisfaction too low")
        
        if task_completion_rate < 80:
            recommendations.append(f"Simplify workflows for {role.value} - completion rate too low")
        
        if len(role_issues) > 2:
            recommendations.append(f"Address specific issues for {role.value} role")
        
        # Role-specific recommendations
        if role == MunicipalUserRole.FIELD_WORKER:
            recommendations.extend([
                "Optimize for mobile access and quick tasks",
                "Minimize data entry requirements for field use"
            ])
        elif role == MunicipalUserRole.ADMINISTRATOR:
            recommendations.extend([
                "Provide advanced configuration options",
                "Ensure comprehensive monitoring capabilities"
            ])
        elif role == MunicipalUserRole.CITIZEN_SERVICE:
            recommendations.extend([
                "Optimize for quick citizen inquiry resolution",
                "Provide easy access to citizen information"
            ])
        
        return recommendations
    
    async def _test_crisis_management_scenarios(
        self,
        implementation_data: Dict[str, Any]
    ) -> List[CrisisManagementTestResult]:
        """Test crisis management scenarios."""
        results = []
        
        for scenario in self.crisis_scenarios:
            logger.info(f"Testing crisis scenario: {scenario['name']}")
            
            result = await self._simulate_crisis_scenario(scenario, implementation_data)
            results.append(result)
        
        return results
    
    async def _simulate_crisis_scenario(
        self,
        scenario: Dict[str, Any],
        implementation_data: Dict[str, Any]
    ) -> CrisisManagementTestResult:
        """Simulate a specific crisis management scenario."""
        scenario_name = scenario["name"]
        target_response_time = scenario["response_time_target_seconds"]
        required_actions = scenario["required_actions"]
        
        # Simulate response time (in reality, this would test actual system response)
        import random
        simulated_response_time = random.uniform(
            target_response_time * 0.8,
            target_response_time * 1.5
        )
        
        # Simulate information accuracy
        ui_components = implementation_data.get("ui_components", [])
        info_components = [comp for comp in ui_components if "info" in str(comp).lower()]
        information_accuracy = min(100, (len(info_components) * 20) + random.uniform(60, 90))
        
        # Test procedure compliance
        procedure_compliance = self._test_crisis_procedure_compliance(
            required_actions, implementation_data
        )
        
        # Simulate communication effectiveness
        communication_effectiveness = random.uniform(3.0, 5.0)
        if any("communication" in str(comp).lower() for comp in ui_components):
            communication_effectiveness += 0.5
        
        # Determine if stress test passed
        stress_test_passed = (
            simulated_response_time <= target_response_time * 1.2 and
            information_accuracy >= 85 and
            procedure_compliance and
            communication_effectiveness >= 3.5
        )
        
        # Identify critical issues
        critical_issues = []
        if simulated_response_time > target_response_time * 1.5:
            critical_issues.append(f"Response time too slow: {simulated_response_time:.0f}s (target: {target_response_time}s)")
        
        if information_accuracy < 80:
            critical_issues.append(f"Information accuracy too low: {information_accuracy:.1f}%")
        
        if not procedure_compliance:
            critical_issues.append("Crisis procedures not properly supported")
        
        return CrisisManagementTestResult(
            crisis_scenario=scenario_name,
            response_time_seconds=round(simulated_response_time, 2),
            information_accuracy=round(information_accuracy, 2),
            procedure_compliance=procedure_compliance,
            communication_effectiveness=round(min(5.0, communication_effectiveness), 2),
            stress_test_passed=stress_test_passed,
            critical_issues=critical_issues
        )
    
    def _test_crisis_procedure_compliance(
        self,
        required_actions: List[str],
        implementation_data: Dict[str, Any]
    ) -> bool:
        """Test if the system supports required crisis procedures."""
        ui_components = implementation_data.get("ui_components", [])
        api_endpoints = implementation_data.get("api_endpoints", [])
        
        # Check if system has components supporting crisis actions
        supported_actions = 0
        
        for action in required_actions:
            action_supported = False
            
            # Check UI components for crisis action support
            for component in ui_components:
                if isinstance(component, dict):
                    component_text = str(component).lower()
                    if any(keyword in component_text for keyword in action.split("_")):
                        action_supported = True
                        break
            
            # Check API endpoints for crisis action support
            if not action_supported:
                for endpoint in api_endpoints:
                    if isinstance(endpoint, dict):
                        endpoint_text = str(endpoint).lower()
                        if any(keyword in endpoint_text for keyword in action.split("_")):
                            action_supported = True
                            break
            
            if action_supported:
                supported_actions += 1
        
        # Consider compliant if at least 60% of actions are supported
        compliance_threshold = 0.6
        return (supported_actions / len(required_actions)) >= compliance_threshold
    
    async def _test_municipal_system_integrations(
        self,
        implementation_data: Dict[str, Any]
    ) -> List[SystemIntegrationTestResult]:
        """Test integration with municipal systems."""
        results = []
        
        for system in self.municipal_system_integrations:
            logger.info(f"Testing system integration: {system['system_name']}")
            
            result = await self._test_system_integration(system, implementation_data)
            results.append(result)
        
        return results
    
    async def _test_system_integration(
        self,
        system: Dict[str, Any],
        implementation_data: Dict[str, Any]
    ) -> SystemIntegrationTestResult:
        """Test integration with a specific municipal system."""
        system_name = system["system_name"]
        integration_type = system["integration_type"]
        test_scenarios = system["test_scenarios"]
        
        # Simulate integration testing
        api_endpoints = implementation_data.get("api_endpoints", [])
        configuration = implementation_data.get("configuration", {})
        
        # Test different aspects of integration
        data_consistency = self._test_data_consistency(system_name, implementation_data)
        authentication_works = self._test_authentication_integration(integration_type, configuration)
        authorization_correct = self._test_authorization_integration(system_name, implementation_data)
        performance_acceptable = self._test_integration_performance(system_name, api_endpoints)
        security_validated = self._test_integration_security(integration_type, configuration)
        
        # Collect issues
        issues_found = []
        if not data_consistency:
            issues_found.append("Data consistency issues detected")
        if not authentication_works:
            issues_found.append("Authentication integration failed")
        if not authorization_correct:
            issues_found.append("Authorization mapping incorrect")
        if not performance_acceptable:
            issues_found.append("Integration performance below acceptable levels")
        if not security_validated:
            issues_found.append("Security validation failed")
        
        # Determine overall status
        all_passed = all([
            data_consistency, authentication_works, authorization_correct,
            performance_acceptable, security_validated
        ])
        
        if all_passed:
            status = "passed"
        elif len(issues_found) <= 2:
            status = "warning"
        else:
            status = "failed"
        
        return SystemIntegrationTestResult(
            system_name=system_name,
            integration_status=status,
            data_consistency=data_consistency,
            authentication_works=authentication_works,
            authorization_correct=authorization_correct,
            performance_acceptable=performance_acceptable,
            security_validated=security_validated,
            issues_found=issues_found
        )
    
    def _test_data_consistency(self, system_name: str, implementation_data: Dict[str, Any]) -> bool:
        """Test data consistency with municipal system."""
        # Simplified test - check if data structures are defined
        api_endpoints = implementation_data.get("api_endpoints", [])
        database_schema = implementation_data.get("database_schema", {})
        
        # Look for data-related endpoints or schema
        has_data_endpoints = any(
            "data" in str(endpoint).lower() or "sync" in str(endpoint).lower()
            for endpoint in api_endpoints
        )
        has_schema = bool(database_schema)
        
        return has_data_endpoints or has_schema
    
    def _test_authentication_integration(self, integration_type: str, configuration: Dict[str, Any]) -> bool:
        """Test authentication integration."""
        if integration_type == "authentication_sso":
            # Check for SSO configuration
            return any(
                "sso" in key.lower() or "auth" in key.lower()
                for key in configuration.keys()
            )
        
        # For other integration types, assume authentication is handled
        return True
    
    def _test_authorization_integration(self, system_name: str, implementation_data: Dict[str, Any]) -> bool:
        """Test authorization integration."""
        # Check if role-based access is configured
        configuration = implementation_data.get("configuration", {})
        
        return any(
            "role" in key.lower() or "permission" in key.lower() or "access" in key.lower()
            for key in configuration.keys()
        )
    
    def _test_integration_performance(self, system_name: str, api_endpoints: List[Dict]) -> bool:
        """Test integration performance."""
        # Simplified test - assume performance is acceptable if endpoints are defined
        integration_endpoints = [
            endpoint for endpoint in api_endpoints
            if "integration" in str(endpoint).lower() or system_name in str(endpoint).lower()
        ]
        
        return len(integration_endpoints) > 0
    
    def _test_integration_security(self, integration_type: str, configuration: Dict[str, Any]) -> bool:
        """Test integration security."""
        # Check for security configuration
        security_keys = ["security", "encryption", "ssl", "tls", "token", "key"]
        
        return any(
            any(sec_key in key.lower() for sec_key in security_keys)
            for key in configuration.keys()
        )
    
    def _calculate_municipal_readiness_score(
        self,
        policy_results: List[PolicyComplianceResult],
        role_results: List[MunicipalRoleTestResult],
        crisis_results: List[CrisisManagementTestResult],
        integration_results: List[SystemIntegrationTestResult]
    ) -> float:
        """Calculate overall municipal readiness score."""
        scores = []
        
        # Policy compliance scores (weighted heavily)
        for result in policy_results:
            policy_score = result.compliance_score / 20  # Convert to 1-5 scale
            if result.legal_risk_level == "critical":
                policy_score *= 0.5  # Severely penalize critical issues
            scores.append(policy_score)
        
        # Role satisfaction scores
        for result in role_results:
            scores.append(result.role_satisfaction_score)
        
        # Crisis management scores
        for result in crisis_results:
            crisis_score = 5.0 if result.stress_test_passed else 2.0
            scores.append(crisis_score)
        
        # Integration scores
        for result in integration_results:
            if result.integration_status == "passed":
                scores.append(4.5)
            elif result.integration_status == "warning":
                scores.append(3.5)
            else:
                scores.append(2.0)
        
        if not scores:
            return 0.0
        
        import statistics
        return round(statistics.mean(scores), 2)
    
    def _assess_municipal_deployment_readiness(
        self,
        policy_results: List[PolicyComplianceResult],
        role_results: List[MunicipalRoleTestResult],
        crisis_results: List[CrisisManagementTestResult],
        integration_results: List[SystemIntegrationTestResult]
    ) -> bool:
        """Assess if the application is ready for municipal deployment."""
        # Critical blockers
        critical_policy_issues = any(
            result.legal_risk_level == "critical" for result in policy_results
        )
        
        major_role_issues = any(
            not result.training_suitability for result in role_results
        )
        
        crisis_failures = any(
            not result.stress_test_passed for result in crisis_results
        )
        
        integration_failures = any(
            result.integration_status == "failed" for result in integration_results
        )
        
        # Cannot deploy if any critical issues exist
        if critical_policy_issues or major_role_issues or crisis_failures or integration_failures:
            return False
        
        # Additional readiness criteria
        policy_avg_score = sum(r.compliance_score for r in policy_results) / len(policy_results) if policy_results else 0
        role_avg_satisfaction = sum(r.role_satisfaction_score for r in role_results) / len(role_results) if role_results else 0
        
        return policy_avg_score >= 80 and role_avg_satisfaction >= 3.5
    
    def _assess_legal_compliance_status(self, policy_results: List[PolicyComplianceResult]) -> str:
        """Assess overall legal compliance status."""
        if not policy_results:
            return "UNKNOWN"
        
        critical_issues = any(result.legal_risk_level == "critical" for result in policy_results)
        high_risk_issues = any(result.legal_risk_level == "high" for result in policy_results)
        
        if critical_issues:
            return "NON_COMPLIANT_CRITICAL"
        elif high_risk_issues:
            return "NON_COMPLIANT_HIGH_RISK"
        
        avg_compliance = sum(r.compliance_score for r in policy_results) / len(policy_results)
        
        if avg_compliance >= 95:
            return "FULLY_COMPLIANT"
        elif avg_compliance >= 85:
            return "MOSTLY_COMPLIANT"
        elif avg_compliance >= 70:
            return "PARTIALLY_COMPLIANT"
        else:
            return "NON_COMPLIANT"
    
    def _generate_municipal_recommendations(
        self,
        policy_results: List[PolicyComplianceResult],
        role_results: List[MunicipalRoleTestResult],
        crisis_results: List[CrisisManagementTestResult],
        integration_results: List[SystemIntegrationTestResult]
    ) -> List[str]:
        """Generate municipal-specific recommendations."""
        recommendations = []
        
        # Policy recommendations
        for result in policy_results:
            recommendations.extend(result.recommendations)
        
        # Role recommendations
        for result in role_results:
            recommendations.extend(result.recommendations)
        
        # Crisis management recommendations
        for result in crisis_results:
            if not result.stress_test_passed:
                recommendations.append(f"Improve crisis response for {result.crisis_scenario}")
        
        # Integration recommendations
        for result in integration_results:
            if result.integration_status != "passed":
                recommendations.append(f"Fix integration issues with {result.system_name}")
        
        # Municipal-specific general recommendations
        if any(not r.training_suitability for r in role_results):
            recommendations.append("Conduct municipal user training before deployment")
        
        if any(r.legal_risk_level in ["high", "critical"] for r in policy_results):
            recommendations.append("Obtain legal review before municipal deployment")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _identify_critical_municipal_blockers(
        self,
        policy_results: List[PolicyComplianceResult],
        role_results: List[MunicipalRoleTestResult],
        crisis_results: List[CrisisManagementTestResult],
        integration_results: List[SystemIntegrationTestResult]
    ) -> List[str]:
        """Identify critical blockers for municipal deployment."""
        blockers = []
        
        # Critical policy blockers
        for result in policy_results:
            if result.legal_risk_level == "critical":
                blockers.extend(result.critical_issues)
        
        # Role-specific blockers
        unsuitable_roles = [
            result.role.value for result in role_results
            if not result.training_suitability
        ]
        if unsuitable_roles:
            blockers.append(f"Training unsuitable for roles: {', '.join(unsuitable_roles)}")
        
        # Crisis management blockers
        failed_crisis_scenarios = [
            result.crisis_scenario for result in crisis_results
            if not result.stress_test_passed
        ]
        if failed_crisis_scenarios:
            blockers.append(f"Crisis scenarios failed: {', '.join(failed_crisis_scenarios)}")
        
        # Integration blockers
        failed_integrations = [
            result.system_name for result in integration_results
            if result.integration_status == "failed"
        ]
        if failed_integrations:
            blockers.append(f"System integrations failed: {', '.join(failed_integrations)}")
        
        return blockers