"""
Quality Reviewer Agent for DigiNativa AI Team.

PURPOSE:
Final quality scoring and production readiness validation.
The last gate before deployment ensuring code quality,
performance standards, and DNA compliance.

CRITICAL IMPORTANCE:
- Final approval authority for production deployment
- Ensures all quality standards are met
- Validates DNA compliance end-to-end
- Protects client reputation through quality gates

REVENUE IMPACT:
Direct impact on revenue through:
- Preventing quality issues that damage client relationships
- Ensuring deployments meet SLA requirements
- Maintaining DigiNativa's reputation for excellence
- Reducing post-deployment support costs
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from ...shared.base_agent import BaseAgent
from ...shared.exceptions import (
    BusinessLogicError, 
    DNAComplianceError,
    QualityGateError
)
from .tools.quality_scorer import QualityScorer
from .tools.deployment_validator import DeploymentValidator
from .tools.final_approver import FinalApprover
from .tools.client_communicator import ClientCommunicator


class QualityReviewerAgent(BaseAgent):
    """
    Quality Reviewer Agent for DigiNativa AI Team.
    
    Responsible for final quality scoring and production readiness validation.
    Acts as the final gate before deployment to ensure all quality standards
    are met and DNA compliance is maintained.
    """
    
    def __init__(self, agent_id: str = "quality_reviewer_001", config: Optional[Dict[str, Any]] = None):
        """
        Initialize Quality Reviewer Agent.
        
        Args:
            agent_id: Unique identifier for this agent instance
            config: Configuration dictionary for agent settings
        """
        super().__init__(agent_id=agent_id, agent_type="quality_reviewer", config=config)
        
        # Initialize tools
        self.quality_scorer = QualityScorer()
        self.deployment_validator = DeploymentValidator()
        self.final_approver = FinalApprover()
        self.client_communicator = ClientCommunicator()
        
        # Quality thresholds from DNA principles
        self.quality_thresholds = {
            "overall_score": 90,  # Minimum overall quality score
            "lighthouse_score": 90,  # Performance requirement
            "api_response_time_ms": 200,  # API performance
            "test_coverage_percent": 95,  # Test coverage requirement
            "dna_compliance_score": 85,  # DNA compliance threshold
            "accessibility_score": 90,  # Accessibility requirement
            "security_score": 95  # Security requirement
        }
        
        self.logger.info(f"Quality Reviewer Agent initialized with thresholds: {self.quality_thresholds}")
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process quality review contract from QA tester.
        
        Performs final quality analysis, validates deployment readiness,
        and provides production approval decision.
        
        Args:
            input_contract: Input contract from QA tester agent
            
        Returns:
            Output contract for deployment or rejection
        """
        try:
            self.logger.info(f"Starting quality review for story: {input_contract.get('story_id')}")
            
            # Extract QA data from contract
            qa_data = self._extract_qa_data(input_contract)
            
            # Perform comprehensive quality analysis
            quality_analysis = await self._perform_quality_analysis(qa_data)
            
            # Validate deployment readiness
            deployment_readiness = await self._validate_deployment_readiness(qa_data, quality_analysis)
            
            # Make final approval decision
            approval_decision = await self._make_approval_decision(quality_analysis, deployment_readiness)
            
            # Handle client communication based on approval decision
            client_communication = await self._handle_client_communication(
                input_contract.get("story_id"), 
                quality_analysis, 
                deployment_readiness, 
                approval_decision
            )
            
            # Create output contract
            output_contract = await self._create_output_contract(
                input_contract, 
                quality_analysis, 
                deployment_readiness, 
                approval_decision,
                client_communication
            )
            
            # Log decision
            decision = approval_decision["approved"]
            score = quality_analysis["overall_score"]
            self.logger.info(f"Quality review completed: {'APPROVED' if decision else 'REJECTED'} (Score: {score})")
            
            return output_contract
            
        except Exception as e:
            self.logger.error(f"Quality review failed: {e}")
            # Re-raise business logic errors as-is
            if isinstance(e, (BusinessLogicError, DNAComplianceError, QualityGateError)):
                raise
            
            raise BusinessLogicError(
                f"Quality review process failed: {e}",
                business_rule="quality_review_execution",
                context={"story_id": input_contract.get("story_id")}
            )
    
    def _extract_qa_data(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and validate QA data from input contract.
        
        Args:
            input_contract: Input contract from QA tester
            
        Returns:
            Structured QA data dictionary
            
        Raises:
            BusinessLogicError: If required QA data is missing
        """
        try:
            required_data = input_contract.get("input_requirements", {}).get("required_data", {})
            
            # Validate required QA fields
            required_fields = [
                "test_results", "performance_metrics", "accessibility_audit",
                "user_flow_validation", "code_quality_metrics"
            ]
            
            for field in required_fields:
                if field not in required_data:
                    raise BusinessLogicError(
                        f"Missing required QA field: {field}",
                        business_rule="qa_data_completeness",
                        context={"missing_field": field}
                    )
            
            return required_data
            
        except Exception as e:
            if isinstance(e, BusinessLogicError):
                raise
            
            raise BusinessLogicError(
                f"Failed to extract QA data: {e}",
                business_rule="qa_data_extraction",
                context={"contract_keys": list(input_contract.keys())}
            )
    
    async def _perform_quality_analysis(self, qa_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive quality analysis on QA data.
        
        Args:
            qa_data: QA test results and metrics
            
        Returns:
            Comprehensive quality analysis results
        """
        try:
            self.logger.debug("Performing comprehensive quality analysis")
            
            # Analyze each quality dimension
            analysis_results = {}
            
            # 1. Test Quality Analysis
            test_analysis = await self.quality_scorer.analyze_test_quality(
                qa_data.get("test_results", {})
            )
            analysis_results["test_quality"] = test_analysis
            
            # 2. Performance Analysis
            performance_analysis = await self.quality_scorer.analyze_performance(
                qa_data.get("performance_metrics", {})
            )
            analysis_results["performance"] = performance_analysis
            
            # 3. Accessibility Analysis
            accessibility_analysis = await self.quality_scorer.analyze_accessibility(
                qa_data.get("accessibility_audit", {})
            )
            analysis_results["accessibility"] = accessibility_analysis
            
            # 4. User Experience Analysis
            ux_analysis = await self.quality_scorer.analyze_user_experience(
                qa_data.get("user_flow_validation", {})
            )
            analysis_results["user_experience"] = ux_analysis
            
            # 5. Code Quality Analysis
            code_analysis = await self.quality_scorer.analyze_code_quality(
                qa_data.get("code_quality_metrics", {})
            )
            analysis_results["code_quality"] = code_analysis
            
            # 6. DNA Compliance Analysis
            dna_analysis = await self.quality_scorer.analyze_dna_compliance(
                qa_data
            )
            analysis_results["dna_compliance"] = dna_analysis
            
            # Calculate overall quality score
            overall_score = await self.quality_scorer.calculate_overall_score(analysis_results)
            analysis_results["overall_score"] = overall_score
            
            # Identify quality issues
            quality_issues = await self.quality_scorer.identify_quality_issues(
                analysis_results, self.quality_thresholds
            )
            analysis_results["quality_issues"] = quality_issues
            
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"Quality analysis failed: {e}")
            raise BusinessLogicError(
                f"Quality analysis failed: {e}",
                business_rule="quality_analysis_execution"
            )
    
    async def _validate_deployment_readiness(self, qa_data: Dict[str, Any], quality_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate deployment readiness against production requirements.
        
        Args:
            qa_data: QA test results and metrics
            quality_analysis: Quality analysis results
            
        Returns:
            Deployment readiness validation results
        """
        try:
            self.logger.debug("Validating deployment readiness")
            
            # Check production requirements
            readiness_checks = {}
            
            # 1. Performance Requirements
            readiness_checks["performance"] = await self.deployment_validator.validate_performance_requirements(
                quality_analysis["performance"]
            )
            
            # 2. Security Requirements
            readiness_checks["security"] = await self.deployment_validator.validate_security_requirements(
                qa_data
            )
            
            # 3. Accessibility Requirements
            readiness_checks["accessibility"] = await self.deployment_validator.validate_accessibility_requirements(
                quality_analysis["accessibility"]
            )
            
            # 4. DNA Compliance Requirements
            readiness_checks["dna_compliance"] = await self.deployment_validator.validate_dna_requirements(
                quality_analysis["dna_compliance"]
            )
            
            # 5. Test Coverage Requirements
            readiness_checks["test_coverage"] = await self.deployment_validator.validate_test_coverage_requirements(
                quality_analysis["test_quality"]
            )
            
            # 6. Browser Compatibility
            readiness_checks["compatibility"] = await self.deployment_validator.validate_compatibility_requirements(
                qa_data
            )
            
            # Calculate overall readiness
            overall_readiness = all(check["passed"] for check in readiness_checks.values())
            
            # Identify blocking issues
            blocking_issues = [
                f"{check_name}: {check['issue']}"
                for check_name, check in readiness_checks.items()
                if not check["passed"]
            ]
            
            return {
                "deployment_ready": overall_readiness,
                "readiness_checks": readiness_checks,
                "blocking_issues": blocking_issues,
                "readiness_score": sum(1 for check in readiness_checks.values() if check["passed"]) / len(readiness_checks) * 100
            }
            
        except Exception as e:
            self.logger.error(f"Deployment readiness validation failed: {e}")
            raise BusinessLogicError(
                f"Deployment readiness validation failed: {e}",
                business_rule="deployment_readiness_validation"
            )
    
    async def _make_approval_decision(self, quality_analysis: Dict[str, Any], deployment_readiness: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make final approval decision based on quality analysis and deployment readiness.
        
        Args:
            quality_analysis: Quality analysis results
            deployment_readiness: Deployment readiness validation
            
        Returns:
            Approval decision with reasoning
        """
        try:
            self.logger.debug("Making final approval decision")
            
            # Use FinalApprover tool for decision logic
            approval_decision = await self.final_approver.make_approval_decision(
                quality_analysis,
                deployment_readiness,
                self.quality_thresholds
            )
            
            # Add decision timestamp
            approval_decision["decision_timestamp"] = datetime.now().isoformat()
            approval_decision["reviewer_agent"] = "quality_reviewer"
            
            return approval_decision
            
        except Exception as e:
            self.logger.error(f"Approval decision failed: {e}")
            raise BusinessLogicError(
                f"Approval decision failed: {e}",
                business_rule="approval_decision_logic"
            )
    
    async def _handle_client_communication(self, story_id: str, quality_analysis: Dict[str, Any],
                                          deployment_readiness: Dict[str, Any], approval_decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle client communication based on approval decision.
        
        Args:
            story_id: Story identifier
            quality_analysis: Quality analysis results
            deployment_readiness: Deployment readiness validation
            approval_decision: Final approval decision
            
        Returns:
            Client communication data
        """
        try:
            self.logger.info(f"Handling client communication for {story_id}")
            
            approved = approval_decision["approved"]
            
            if approved:
                # Create approval request for staging/production
                staging_url = f"https://staging.digitativa.se/{story_id}"  # Mock staging URL
                
                approval_request = await self.client_communicator.create_approval_request(
                    story_id, quality_analysis, deployment_readiness, staging_url
                )
                
                # Create staging notification for client testing
                test_instructions = [
                    "Logga in med dina testuppgifter",
                    "Navigera till den nya funktionen", 
                    "Testa grundläggande användarflöden",
                    "Kontrollera att allt fungerar som förväntat",
                    "Rapportera eventuella problem i GitHub-ärendet"
                ]
                
                staging_notification = await self.client_communicator.create_staging_notification(
                    story_id, staging_url, quality_analysis["overall_score"], test_instructions
                )
                
                return {
                    "communication_type": "approval_request",
                    "approval_request": approval_request,
                    "staging_notification": staging_notification,
                    "quality_report": await self.client_communicator.generate_quality_report(
                        story_id, quality_analysis, deployment_readiness
                    )
                }
            else:
                # Create rejection feedback
                quality_issues = quality_analysis.get("quality_issues", [])
                recommendations = approval_decision.get("recommendations", [])
                blocking_issues = approval_decision.get("blocking_issues", [])
                
                rejection_feedback = await self.client_communicator.handle_rejection_feedback(
                    story_id, quality_issues, recommendations, blocking_issues
                )
                
                return {
                    "communication_type": "rejection_feedback",
                    "rejection_feedback": rejection_feedback,
                    "quality_report": await self.client_communicator.generate_quality_report(
                        story_id, quality_analysis, deployment_readiness
                    )
                }
                
        except Exception as e:
            self.logger.error(f"Client communication failed for {story_id}: {e}")
            return {
                "communication_type": "error",
                "error_message": f"Client communication failed: {e}"
            }
    
    async def _create_output_contract(self, input_contract: Dict[str, Any], quality_analysis: Dict[str, Any], 
                                    deployment_readiness: Dict[str, Any], approval_decision: Dict[str, Any],
                                    client_communication: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create output contract for deployment or rejection.
        
        Args:
            input_contract: Original input contract
            quality_analysis: Quality analysis results
            deployment_readiness: Deployment readiness validation
            approval_decision: Final approval decision
            
        Returns:
            Output contract for next stage
        """
        try:
            story_id = input_contract.get("story_id")
            approved = approval_decision["approved"]
            
            # Quality Reviewer is the final agent in the AI team
            # For approved features: hand off to deployment pipeline
            # For rejected features: return to developer for fixes
            target_agent = "deployment" if approved else "developer"
            
            # Create output contract
            output_contract = {
                "contract_version": "1.0",
                "story_id": story_id,
                "source_agent": "quality_reviewer",
                "target_agent": target_agent,
                "dna_compliance": {
                    "design_principles_validation": self._convert_design_principles_to_boolean(
                        quality_analysis["dna_compliance"]["design_principles"]
                    ),
                    "architecture_compliance": self._convert_architecture_compliance_to_boolean(
                        quality_analysis["dna_compliance"]["architecture_principles"]
                    )
                },
                "input_requirements": {
                    "required_files": [
                        f"releases/{story_id}_production_ready.zip" if approved else f"feedback/{story_id}_quality_issues.json"
                    ],
                    "required_data": {
                        "approval_status": approval_decision["approved"],
                        "quality_score": quality_analysis["overall_score"],
                        "deployment_ready": deployment_readiness["deployment_ready"],
                        "quality_analysis": quality_analysis,
                        "deployment_readiness": deployment_readiness,
                        "approval_reasoning": approval_decision["reasoning"],
                        "blocking_issues": approval_decision.get("blocking_issues", []),
                        "recommendations": approval_decision.get("recommendations", []),
                        "client_communication": client_communication
                    },
                    "required_validations": [
                        "quality_score_validated",
                        "deployment_readiness_confirmed",
                        "dna_compliance_verified"
                    ]
                },
                "output_specifications": {
                    "deliverable_files": [
                        f"docs/quality_reports/{story_id}_final_quality_report.json",
                        f"docs/approvals/{story_id}_approval_decision.md"
                    ] if approved else [
                        f"docs/feedback/{story_id}_quality_feedback.md",
                        f"docs/improvements/{story_id}_improvement_plan.json"
                    ],
                    "deliverable_data": {
                        "final_quality_score": "number",
                        "deployment_approval": "boolean",
                        "quality_breakdown": "object",
                        "next_actions": ["string"]
                    },
                    "validation_criteria": {
                        "approval_decision_documented": True,
                        "quality_metrics_complete": True,
                        "recommendations_provided": True
                    }
                },
                "quality_gates": [
                    "final_quality_score_calculated",
                    "deployment_readiness_validated",
                    "approval_decision_made",
                    "documentation_complete",
                    "client_communication_sent"
                ],
                "handoff_criteria": [
                    "quality_analysis_complete",
                    "approval_decision_documented",
                    "client_communication_completed",
                    "next_steps_defined"
                ]
            }
            
            self.logger.debug(f"Created output contract for {'deployment' if approved else 'rework'}")
            return output_contract
            
        except Exception as e:
            self.logger.error(f"Failed to create output contract: {e}")
            raise BusinessLogicError(
                f"Failed to create output contract: {e}",
                business_rule="output_contract_creation"
            )
    
    async def validate_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """
        Validate specific quality gate for Quality Reviewer agent.
        
        Args:
            gate: Quality gate name to validate
            deliverables: Deliverables to validate against gate
            
        Returns:
            True if quality gate passes, False otherwise
        """
        quality_checks = {
            "final_quality_score_calculated": self._check_quality_score_gate,
            "deployment_readiness_validated": self._check_deployment_readiness_gate,
            "approval_decision_made": self._check_approval_decision_gate,
            "documentation_complete": self._check_documentation_gate,
            "client_communication_sent": self._check_client_communication_gate
        }
        
        checker = quality_checks.get(gate)
        if checker:
            try:
                return checker(deliverables)
            except Exception as e:
                self.logger.error(f"Quality gate check failed for '{gate}': {e}")
                return False
        
        # Unknown gates pass by default (with warning)
        self.logger.warning(f"Unknown quality gate: {gate}")
        return True
    
    def _check_quality_score_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Check if final quality score has been calculated."""
        quality_analysis = deliverables.get("quality_analysis", {})
        overall_score = quality_analysis.get("overall_score")
        
        return (
            overall_score is not None and 
            isinstance(overall_score, (int, float)) and 
            0 <= overall_score <= 100
        )
    
    def _check_deployment_readiness_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Check if deployment readiness has been validated."""
        deployment_readiness = deliverables.get("deployment_readiness", {})
        
        return (
            "deployment_ready" in deployment_readiness and
            "readiness_checks" in deployment_readiness and
            "readiness_score" in deployment_readiness
        )
    
    def _check_approval_decision_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Check if approval decision has been made."""
        approval_status = deliverables.get("approval_status")
        reasoning = deliverables.get("approval_reasoning")
        
        return (
            approval_status is not None and
            isinstance(approval_status, bool) and
            reasoning is not None and
            len(reasoning) > 0
        )
    
    def _check_documentation_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Check if all required documentation is complete."""
        required_docs = [
            "quality_analysis", "deployment_readiness", 
            "approval_reasoning", "quality_score"
        ]
        
        return all(
            doc in deliverables and deliverables[doc] is not None
            for doc in required_docs
        )
    
    def _check_client_communication_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Check if client communication has been sent."""
        client_communication = deliverables.get("client_communication", {})
        
        return (
            "communication_type" in client_communication and
            client_communication["communication_type"] in ["approval_request", "rejection_feedback"] and
            "quality_report" in client_communication
        )
    
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """
        Check specific quality gate - required by BaseAgent abstract method.
        
        Args:
            gate: Quality gate name to validate
            deliverables: Deliverables to validate against gate
            
        Returns:
            True if quality gate passes, False otherwise
        """
        # Delegate to the async validate_quality_gate method
        import asyncio
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.validate_quality_gate(gate, deliverables))
    
    def _convert_design_principles_to_boolean(self, design_principles: Dict[str, Any]) -> Dict[str, bool]:
        """Convert design principles scores to boolean compliance values."""
        return {
            "pedagogical_value": design_principles.get("pedagogical_value", 0) >= 3.5,
            "policy_to_practice": design_principles.get("policy_to_practice", 0) >= 3.5,
            "time_respect": design_principles.get("time_respect", 0) >= 3.5,
            "holistic_thinking": design_principles.get("holistic_thinking", 0) >= 3.5,
            "professional_tone": design_principles.get("professional_tone", 0) >= 3.5
        }
    
    def _convert_architecture_compliance_to_boolean(self, architecture_principles: Dict[str, Any]) -> Dict[str, bool]:
        """Convert architecture compliance percentages to boolean values."""
        compliance_percent = architecture_principles.get("compliance_percent", 0)
        return {
            "api_first": compliance_percent >= 80,
            "stateless_backend": compliance_percent >= 80,
            "separation_of_concerns": compliance_percent >= 80,
            "simplicity_first": compliance_percent >= 80
        }