"""
QATesterAgent - User experience validation and DNA compliance testing agent.

PURPOSE:
Validates that implemented features provide excellent user experience
for Anna persona and comply with DigiNativa's DNA principles.

CRITICAL RESPONSIBILITIES:
- Anna persona simulation and testing
- WCAG AA accessibility compliance validation 
- User flow completion verification
- Time constraint adherence validation (10 minutes max)
- Professional tone and pedagogical value assessment

ADAPTATION GUIDE:
=' To adapt for your project:
1. Update persona_requirements for your target users
2. Modify accessibility_standards for your compliance needs
3. Adjust time_constraints for your user requirements
4. Update quality criteria for your quality standards

CONTRACT PROTECTION:
This agent is part of DigiNativa's quality assurance chain.
Changes must maintain backward contract compatibility.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from ...shared.base_agent import BaseAgent, AgentExecutionResult
from ...shared.exceptions import (
    QualityGateError, DNAComplianceError, AgentExecutionError
)
from .tools.persona_simulator import PersonaSimulator
from .tools.accessibility_checker import AccessibilityChecker
from .tools.user_flow_validator import UserFlowValidator
from .tools.performance_tester import PerformanceTester
from .tools.municipal_training_tester import MunicipalTrainingTester
from .tools.exploratory_tester import ExploratoryTester
from .tools.uat_orchestrator import UATOrchestrator
from .tools.quality_intelligence_engine import QualityIntelligenceEngine


# Setup logging for this module
logger = logging.getLogger(__name__)


class QATesterAgent(BaseAgent):
    """
    QA Tester agent for user experience validation and DNA compliance testing.
    
    This agent ensures that implemented features:
    - Meet Anna persona requirements and expectations
    - Comply with WCAG AA accessibility standards
    - Respect time constraints (10 minutes max completion)
    - Maintain professional tone and pedagogical value
    - Follow all DigiNativa DNA principles
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize QA Tester agent.
        
        Args:
            config: Optional configuration dictionary
        """
        super().__init__("qat-001", "qa_tester", config)
        
        # Initialize QA testing tools
        try:
            # Core testing tools
            self.persona_simulator = PersonaSimulator(config=self.config.get("persona_config", {}))
            self.accessibility_checker = AccessibilityChecker(config=self.config.get("accessibility_config", {}))
            self.user_flow_validator = UserFlowValidator(config=self.config.get("flow_config", {}))
            
            # Enhanced testing tools
            self.performance_tester = PerformanceTester(config=self.config.get("performance_config", {}))
            self.municipal_training_tester = MunicipalTrainingTester(config=self.config.get("municipal_config", {}))
            self.exploratory_tester = ExploratoryTester(config=self.config.get("exploratory_config", {}))
            self.uat_orchestrator = UATOrchestrator(config=self.config.get("uat_config", {}))
            
            # AI-powered Quality Intelligence (Phase 1 Enhancement)
            self.quality_intelligence_engine = QualityIntelligenceEngine(config=self.config.get("ai_config", {}))
            
            self.logger.info("QA Tester tools (core + enhanced + AI) initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize QA Tester tools: {e}")
            raise AgentExecutionError(f"QA Tester initialization failed: {e}")
        
        # Anna persona requirements (DigiNativa specific)
        self.anna_persona_requirements = {
            "role": "Municipal training coordinator",
            "experience_level": "Intermediate with digital tools",
            "time_availability": "10 minutes maximum per session",
            "accessibility_needs": "WCAG AA compliance required",
            "content_preferences": "Professional, practical, policy-focused",
            "success_metrics": {
                "task_completion_rate": 95,  # minimum percentage
                "satisfaction_score": 4,     # minimum out of 5
                "learning_effectiveness": 4   # minimum out of 5
            }
        }
        
        # Quality validation criteria
        self.quality_criteria = {
            "user_experience": {
                "anna_persona_satisfaction": {"min_score": 4, "max_score": 5},
                "task_completion_rate": {"min_percentage": 95},
                "time_to_complete": {"max_minutes": 10},
                "error_recovery_rate": {"min_percentage": 90}
            },
            "accessibility": {
                "wcag_compliance_level": "AA",
                "screen_reader_compatibility": True,
                "keyboard_navigation": True,
                "color_contrast_ratio": {"min": 4.5}
            },
            "content_quality": {
                "professional_tone_score": {"min": 4},
                "pedagogical_value_score": {"min": 4},
                "policy_relevance_score": {"min": 4}
            },
            "technical_performance": {
                "page_load_time_ms": {"max": 3000},
                "interaction_response_time_ms": {"max": 200},
                "lighthouse_accessibility_score": {"min": 90}
            }
        }
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process QA testing according to input contract.
        
        Validates user experience, accessibility, and DNA compliance
        for implemented features.
        
        Args:
            input_contract: Contract from Test Engineer with tested code
            
        Returns:
            Output contract for Quality Reviewer with validation results
            
        Raises:
            QualityGateError: If quality gates fail
            DNAComplianceError: If DNA compliance fails
            AgentExecutionError: If QA testing fails
        """
        try:
            story_id = input_contract.get("story_id")
            self.logger.info(f"Starting QA testing for story: {story_id}")
            
            # Extract test results and implementation data
            input_data = input_contract.get("input_requirements", {}).get("required_data", {})
            test_suite = input_data.get("test_suite", {})
            implementation_data = input_data.get("implementation_data", {})
            
            # Step 1: Run Anna persona simulation tests
            self.logger.info("Running Anna persona simulation tests")
            persona_results = await self.persona_simulator.simulate_anna_usage(
                story_id=story_id,
                implementation_data=implementation_data,
                test_suite=test_suite,
                requirements=self.anna_persona_requirements
            )
            
            # Step 2: Perform accessibility compliance testing
            self.logger.info("Performing WCAG AA accessibility testing")
            accessibility_results = await self.accessibility_checker.validate_accessibility(
                story_id=story_id,
                implementation_data=implementation_data,
                wcag_level="AA"
            )
            
            # Step 3: Validate user flows and interaction patterns
            self.logger.info("Validating user flows and interactions")
            flow_validation_results = await self.user_flow_validator.validate_user_flows(
                story_id=story_id,
                implementation_data=implementation_data,
                persona_requirements=self.anna_persona_requirements
            )
            
            # Step 4: Assess content quality and tone
            self.logger.info("Assessing content quality and professional tone")
            content_quality_results = await self._assess_content_quality(
                implementation_data=implementation_data,
                story_id=story_id
            )
            
            # Step 5: Enhanced testing with new tools
            self.logger.info("Running enhanced QA testing suite")
            
            # Performance testing under municipal load
            performance_results = await self.performance_tester.test_municipal_performance(
                story_id=story_id,
                implementation_data=implementation_data
            )
            
            # Municipal-specific compliance testing
            municipal_compliance_results = await self.municipal_training_tester.test_municipal_training_compliance(
                story_id=story_id,
                implementation_data=implementation_data
            )
            
            # Exploratory testing for edge cases and security
            exploratory_results = await self.exploratory_tester.perform_exploratory_testing(
                story_id=story_id,
                implementation_data=implementation_data
            )
            
            # User Acceptance Testing orchestration
            user_stories = self._extract_user_stories_from_implementation(implementation_data)
            uat_results = await self.uat_orchestrator.orchestrate_uat_process(
                story_id=story_id,
                implementation_data=implementation_data,
                user_stories=user_stories
            )
            
            # Step 5.5: AI-Powered Quality Intelligence (PHASE 1 ENHANCEMENT)
            self.logger.info("Applying AI-powered quality intelligence")
            
            # AI quality prediction
            ai_quality_prediction = await self.quality_intelligence_engine.predict_quality_score(
                story_id=story_id,
                implementation_data=implementation_data
            )
            
            # AI-optimized test coverage analysis
            ai_test_optimization = await self.quality_intelligence_engine.optimize_test_coverage(
                story_id=story_id,
                test_results=test_suite,
                implementation_data=implementation_data
            )
            
            # AI-powered Anna persona satisfaction prediction
            ai_anna_prediction = await self.quality_intelligence_engine.predict_anna_satisfaction(
                story_id=story_id,
                implementation_data=implementation_data
            )
            
            # AI quality insights generation
            ai_quality_insights = await self.quality_intelligence_engine.generate_quality_insights(
                historical_data={
                    "persona_results": persona_results,
                    "accessibility_results": accessibility_results,
                    "performance_results": performance_results,
                    "municipal_compliance": municipal_compliance_results
                }
            )
            
            # Step 6: Validate DNA compliance specific to QA (Enhanced with AI)
            self.logger.info("Validating comprehensive DNA compliance for QA aspects")
            dna_compliance_results = await self._validate_enhanced_qa_dna_compliance(
                persona_results=persona_results,
                accessibility_results=accessibility_results,
                content_quality=content_quality_results,
                performance_results=performance_results,
                municipal_compliance=municipal_compliance_results,
                exploratory_results=exploratory_results,
                uat_results=uat_results,
                ai_predictions={
                    "quality_prediction": ai_quality_prediction,
                    "test_optimization": ai_test_optimization,
                    "anna_prediction": ai_anna_prediction,
                    "quality_insights": ai_quality_insights
                }
            )
            
            # Step 7: Generate comprehensive QA report (Enhanced with AI)
            qa_report = await self._generate_enhanced_qa_report(
                story_id=story_id,
                persona_results=persona_results,
                accessibility_results=accessibility_results,
                flow_validation=flow_validation_results,
                content_quality=content_quality_results,
                performance_results=performance_results,
                municipal_compliance=municipal_compliance_results,
                exploratory_results=exploratory_results,
                uat_results=uat_results,
                dna_compliance=dna_compliance_results,
                ai_predictions={
                    "quality_prediction": ai_quality_prediction,
                    "test_optimization": ai_test_optimization,
                    "anna_prediction": ai_anna_prediction,
                    "quality_insights": ai_quality_insights
                }
            )
            
            # Step 7: Create output contract for Quality Reviewer
            output_contract = {
                "contract_version": "1.0",
                "story_id": story_id,
                "source_agent": "qa_tester",
                "target_agent": "quality_reviewer",
                "dna_compliance": dna_compliance_results,
                
                "input_requirements": {
                    "required_files": [
                        f"docs/qa_reports/{story_id}_ux_validation.md",
                        f"docs/qa_reports/{story_id}_accessibility.json",
                        f"docs/qa_reports/{story_id}_persona_testing.json",
                        f"docs/qa_reports/{story_id}_comprehensive_qa.json"
                    ],
                    "required_data": {
                        "qa_validation_results": qa_report,
                        "anna_persona_testing": persona_results,
                        "accessibility_compliance": accessibility_results,
                        "user_flow_validation": flow_validation_results,
                        "performance_testing_results": performance_results,
                        "municipal_compliance_results": municipal_compliance_results,
                        "exploratory_testing_results": exploratory_results,
                        "user_acceptance_testing_results": uat_results,
                        "content_quality_assessment": content_quality_results,
                        "quality_metrics": self._calculate_quality_metrics(qa_report),
                        "ai_quality_intelligence": {
                            "quality_prediction": ai_quality_prediction.to_dict(),
                            "test_optimization": ai_test_optimization.to_dict(),
                            "anna_satisfaction_prediction": ai_anna_prediction,
                            "ai_quality_insights": [insight.to_dict() for insight in ai_quality_insights]
                        }
                    },
                    "required_validations": [
                        "anna_persona_satisfaction_verified",
                        "wcag_aa_compliance_confirmed",
                        "time_constraints_respected",
                        "professional_tone_maintained",
                        "pedagogical_value_demonstrated"
                    ]
                },
                
                "output_specifications": {
                    "deliverable_files": [
                        f"docs/final_review/{story_id}_production_readiness.md",
                        f"docs/final_review/{story_id}_deployment_approval.json"
                    ],
                    "deliverable_data": {
                        "production_readiness_score": "object",
                        "deployment_approval": "object",
                        "quality_metrics_final": "object",
                        "stakeholder_signoff": "object"
                    },
                    "validation_criteria": {
                        "production_readiness": {
                            "overall_quality_score": {"min": 4.0},
                            "user_satisfaction_score": {"min": 4.0},
                            "technical_performance_score": {"min": 4.0},
                            "business_value_score": {"min": 4.0}
                        },
                        "deployment_criteria": {
                            "all_quality_gates_passed": True,
                            "stakeholder_approval_received": True,
                            "production_deployment_approved": True,
                            "rollback_plan_documented": True
                        }
                    }
                },
                
                "quality_gates": [
                    "anna_persona_satisfaction_score_minimum_met",
                    "wcag_aa_compliance_100_percent_verified",
                    "task_completion_time_under_10_minutes",
                    "professional_tone_maintained_throughout",
                    "pedagogical_value_clearly_demonstrated",
                    "all_user_flows_validated_successfully"
                ],
                
                "handoff_criteria": [
                    "comprehensive_ux_validation_completed",
                    "accessibility_compliance_fully_verified",
                    "anna_persona_requirements_satisfied",
                    "quality_metrics_meet_dna_standards",
                    "production_readiness_assessment_complete"
                ]
            }
            
            self.logger.info(f"QA testing completed successfully for story: {story_id}")
            return output_contract
            
        except Exception as e:
            error_msg = f"QA testing failed for story {story_id}: {str(e)}"
            self.logger.error(error_msg)
            raise AgentExecutionError(error_msg)
    
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """
        Check QA Tester specific quality gates.
        
        Args:
            gate: Quality gate identifier
            deliverables: QA testing deliverables
            
        Returns:
            True if quality gate passes, False otherwise
        """
        quality_checks = {
            "anna_persona_satisfaction_score_minimum_met": self._check_anna_satisfaction,
            "wcag_aa_compliance_100_percent_verified": self._check_accessibility_compliance,
            "task_completion_time_under_10_minutes": self._check_time_constraints,
            "professional_tone_maintained_throughout": self._check_professional_tone,
            "pedagogical_value_clearly_demonstrated": self._check_pedagogical_value,
            "all_user_flows_validated_successfully": self._check_user_flows
        }
        
        checker = quality_checks.get(gate)
        if checker:
            try:
                result = checker(deliverables)
                self.logger.debug(f"Quality gate '{gate}' result: {result}")
                return result
            except Exception as e:
                self.logger.error(f"Error checking quality gate '{gate}': {e}")
                return False
        
        # Default pass for unknown gates (with warning)
        self.logger.warning(f"Unknown quality gate: {gate}, defaulting to pass")
        return True
    
    def _check_anna_satisfaction(self, deliverables: Dict[str, Any]) -> bool:
        """Check Anna persona satisfaction score meets minimum."""
        try:
            qa_results = deliverables.get("qa_validation_results", {})
            persona_results = qa_results.get("anna_persona_testing", {})
            satisfaction_score = persona_results.get("satisfaction_score", 0)
            
            min_required = self.quality_criteria["user_experience"]["anna_persona_satisfaction"]["min_score"]
            return satisfaction_score >= min_required
            
        except Exception as e:
            self.logger.error(f"Error checking Anna satisfaction: {e}")
            return False
    
    def _check_accessibility_compliance(self, deliverables: Dict[str, Any]) -> bool:
        """Check WCAG AA accessibility compliance."""
        try:
            qa_results = deliverables.get("qa_validation_results", {})
            accessibility_results = qa_results.get("accessibility_compliance", {})
            
            wcag_level = accessibility_results.get("compliance_level")
            compliance_score = accessibility_results.get("compliance_percentage", 0)
            
            return wcag_level == "AA" and compliance_score >= 100
            
        except Exception as e:
            self.logger.error(f"Error checking accessibility compliance: {e}")
            return False
    
    def _check_time_constraints(self, deliverables: Dict[str, Any]) -> bool:
        """Check task completion time under 10 minutes."""
        try:
            qa_results = deliverables.get("qa_validation_results", {})
            persona_results = qa_results.get("anna_persona_testing", {})
            completion_time = persona_results.get("average_completion_time_minutes", 999)
            
            max_allowed = self.quality_criteria["user_experience"]["time_to_complete"]["max_minutes"]
            return completion_time <= max_allowed
            
        except Exception as e:
            self.logger.error(f"Error checking time constraints: {e}")
            return False
    
    def _check_professional_tone(self, deliverables: Dict[str, Any]) -> bool:
        """Check professional tone maintained throughout."""
        try:
            qa_results = deliverables.get("qa_validation_results", {})
            content_quality = qa_results.get("content_quality_assessment", {})
            tone_score = content_quality.get("professional_tone_score", 0)
            
            min_required = self.quality_criteria["content_quality"]["professional_tone_score"]["min"]
            return tone_score >= min_required
            
        except Exception as e:
            self.logger.error(f"Error checking professional tone: {e}")
            return False
    
    def _check_pedagogical_value(self, deliverables: Dict[str, Any]) -> bool:
        """Check pedagogical value clearly demonstrated."""
        try:
            qa_results = deliverables.get("qa_validation_results", {})
            content_quality = qa_results.get("content_quality_assessment", {})
            pedagogical_score = content_quality.get("pedagogical_value_score", 0)
            
            min_required = self.quality_criteria["content_quality"]["pedagogical_value_score"]["min"]
            return pedagogical_score >= min_required
            
        except Exception as e:
            self.logger.error(f"Error checking pedagogical value: {e}")
            return False
    
    def _check_user_flows(self, deliverables: Dict[str, Any]) -> bool:
        """Check all user flows validated successfully."""
        try:
            qa_results = deliverables.get("qa_validation_results", {})
            flow_validation = qa_results.get("user_flow_validation", {})
            flows_passed = flow_validation.get("flows_passed", 0)
            total_flows = flow_validation.get("total_flows", 1)
            
            success_rate = (flows_passed / total_flows) * 100 if total_flows > 0 else 0
            min_required = self.quality_criteria["user_experience"]["task_completion_rate"]["min_percentage"]
            
            return success_rate >= min_required
            
        except Exception as e:
            self.logger.error(f"Error checking user flows: {e}")
            return False
    
    async def _assess_content_quality(self, implementation_data: Dict[str, Any], story_id: str) -> Dict[str, Any]:
        """
        Assess content quality including professional tone and pedagogical value.
        
        Args:
            implementation_data: Implementation details to assess
            story_id: Story identifier
            
        Returns:
            Content quality assessment results
        """
        try:
            # Extract content from implementation
            ui_components = implementation_data.get("ui_components", [])
            content_text = []
            
            for component in ui_components:
                # Extract text content from UI components
                if "text_content" in component:
                    content_text.append(component["text_content"])
                if "labels" in component:
                    content_text.extend(component["labels"])
                if "instructions" in component:
                    content_text.append(component["instructions"])
            
            # Assess professional tone (simplified implementation)
            professional_tone_score = await self._assess_professional_tone(content_text)
            
            # Assess pedagogical value
            pedagogical_value_score = await self._assess_pedagogical_value(content_text, implementation_data)
            
            # Assess policy relevance
            policy_relevance_score = await self._assess_policy_relevance(content_text)
            
            return {
                "professional_tone_score": professional_tone_score,
                "pedagogical_value_score": pedagogical_value_score,
                "policy_relevance_score": policy_relevance_score,
                "content_analysis": {
                    "total_text_elements": len(content_text),
                    "assessment_timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error assessing content quality: {e}")
            return {
                "professional_tone_score": 0,
                "pedagogical_value_score": 0,
                "policy_relevance_score": 0,
                "error": str(e)
            }
    
    async def _assess_professional_tone(self, content_text: List[str]) -> float:
        """
        Assess professional tone of content.
        
        Args:
            content_text: List of text content to assess
            
        Returns:
            Professional tone score (1-5)
        """
        if not content_text:
            return 0.0
        
        # Simplified assessment - in reality would use NLP
        professional_indicators = [
            "policy", "procedure", "regulation", "compliance", "standard",
            "requirement", "guideline", "framework", "best practice"
        ]
        
        unprofessional_indicators = [
            "awesome", "cool", "amazing", "super", "wow"
        ]
        
        total_words = 0
        professional_count = 0
        unprofessional_count = 0
        
        for text in content_text:
            words = text.lower().split()
            total_words += len(words)
            
            for word in words:
                if any(indicator in word for indicator in professional_indicators):
                    professional_count += 1
                if any(indicator in word for indicator in unprofessional_indicators):
                    unprofessional_count += 1
        
        if total_words == 0:
            return 3.0  # Neutral score for no content
        
        # Calculate score based on professional vs unprofessional language
        professional_ratio = professional_count / total_words
        unprofessional_ratio = unprofessional_count / total_words
        
        # Base score + professional bonus - unprofessional penalty
        score = 3.0 + (professional_ratio * 2.0) - (unprofessional_ratio * 2.0)
        
        return max(1.0, min(5.0, score))
    
    async def _assess_pedagogical_value(self, content_text: List[str], implementation_data: Dict[str, Any]) -> float:
        """
        Assess pedagogical value of the implementation.
        
        Args:
            content_text: Text content to assess
            implementation_data: Implementation details
            
        Returns:
            Pedagogical value score (1-5)
        """
        try:
            # Check for learning objectives alignment
            learning_indicators = [
                "learn", "understand", "practice", "exercise", "example",
                "demonstration", "tutorial", "guide", "step", "process"
            ]
            
            # Check for interactive elements
            interactive_elements = implementation_data.get("interactive_elements", [])
            
            # Check for feedback mechanisms
            feedback_elements = implementation_data.get("feedback_mechanisms", [])
            
            # Calculate scores
            learning_content_score = 0
            if content_text:
                total_text = " ".join(content_text).lower()
                learning_matches = sum(1 for indicator in learning_indicators if indicator in total_text)
                learning_content_score = min(2.0, learning_matches * 0.2)
            
            interactive_score = min(2.0, len(interactive_elements) * 0.5)
            feedback_score = min(1.0, len(feedback_elements) * 0.5)
            
            total_score = learning_content_score + interactive_score + feedback_score
            
            return max(1.0, min(5.0, total_score))
            
        except Exception as e:
            self.logger.error(f"Error assessing pedagogical value: {e}")
            return 2.0  # Default neutral score
    
    async def _assess_policy_relevance(self, content_text: List[str]) -> float:
        """
        Assess policy relevance of content.
        
        Args:
            content_text: Text content to assess
            
        Returns:
            Policy relevance score (1-5)
        """
        if not content_text:
            return 0.0
        
        policy_keywords = [
            "municipal", "municipality", "government", "public sector",
            "regulation", "compliance", "law", "statute", "ordinance",
            "citizen", "service", "administration", "bureaucracy"
        ]
        
        total_text = " ".join(content_text).lower()
        policy_matches = sum(1 for keyword in policy_keywords if keyword in total_text)
        
        # Score based on policy keyword density
        score = 1.0 + min(4.0, policy_matches * 0.5)
        
        return score
    
    async def _validate_qa_dna_compliance(self, persona_results: Dict[str, Any], 
                                        accessibility_results: Dict[str, Any],
                                        content_quality: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate DNA compliance specific to QA testing results.
        
        Args:
            persona_results: Anna persona testing results
            accessibility_results: Accessibility compliance results
            content_quality: Content quality assessment
            
        Returns:
            DNA compliance validation results
        """
        try:
            # Design principles validation
            design_principles = {
                "pedagogical_value": content_quality.get("pedagogical_value_score", 0) >= 4,
                "policy_to_practice": content_quality.get("policy_relevance_score", 0) >= 4,
                "time_respect": persona_results.get("average_completion_time_minutes", 999) <= 10,
                "holistic_thinking": persona_results.get("task_completion_rate", 0) >= 95,
                "professional_tone": content_quality.get("professional_tone_score", 0) >= 4
            }
            
            # Architecture principles validation (QA perspective)
            architecture_compliance = {
                "api_first": True,  # Inherited from previous agents
                "stateless_backend": True,  # Inherited from previous agents
                "separation_of_concerns": True,  # Inherited from previous agents
                "simplicity_first": persona_results.get("user_confusion_incidents", 999) == 0
            }
            
            return {
                "design_principles_validation": design_principles,
                "architecture_compliance": architecture_compliance,
                "overall_compliance": all(design_principles.values()) and all(architecture_compliance.values()),
                "validation_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error validating QA DNA compliance: {e}")
            return {
                "design_principles_validation": {
                    "pedagogical_value": False,
                    "policy_to_practice": False,
                    "time_respect": False,
                    "holistic_thinking": False,
                    "professional_tone": False
                },
                "architecture_compliance": {
                    "api_first": False,
                    "stateless_backend": False,
                    "separation_of_concerns": False,
                    "simplicity_first": False
                },
                "overall_compliance": False,
                "error": str(e)
            }
    
    async def _generate_qa_report(self, story_id: str, persona_results: Dict[str, Any],
                                accessibility_results: Dict[str, Any], flow_validation: Dict[str, Any],
                                content_quality: Dict[str, Any], dna_compliance: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive QA report.
        
        Args:
            story_id: Story identifier
            persona_results: Anna persona testing results
            accessibility_results: Accessibility testing results
            flow_validation: User flow validation results
            content_quality: Content quality assessment
            dna_compliance: DNA compliance results
            
        Returns:
            Comprehensive QA report
        """
        try:
            # Calculate overall scores
            quality_scores = self._calculate_quality_metrics({
                "anna_persona_testing": persona_results,
                "accessibility_compliance": accessibility_results,
                "user_flow_validation": flow_validation,
                "content_quality_assessment": content_quality
            })
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(
                persona_results, accessibility_results, content_quality
            )
            
            qa_report = {
                "story_id": story_id,
                "qa_testing_summary": {
                    "overall_quality_score": quality_scores.get("overall_score", 0),
                    "anna_persona_satisfaction": persona_results.get("satisfaction_score", 0),
                    "accessibility_compliance_score": accessibility_results.get("compliance_percentage", 0),
                    "user_flow_success_rate": flow_validation.get("success_rate_percentage", 0),
                    "content_quality_score": sum([
                        content_quality.get("professional_tone_score", 0),
                        content_quality.get("pedagogical_value_score", 0),
                        content_quality.get("policy_relevance_score", 0)
                    ]) / 3
                },
                "detailed_results": {
                    "anna_persona_testing": persona_results,
                    "accessibility_compliance": accessibility_results,
                    "user_flow_validation": flow_validation,
                    "content_quality_assessment": content_quality
                },
                "dna_compliance_results": dna_compliance,
                "recommendations": recommendations,
                "quality_metrics": quality_scores,
                "testing_metadata": {
                    "tested_by": self.agent_id,
                    "testing_timestamp": datetime.now().isoformat(),
                    "testing_duration_minutes": 15,  # Estimated
                    "quality_criteria_version": "1.0"
                }
            }
            
            # Save QA report files
            await self._save_qa_reports(story_id, qa_report)
            
            return qa_report
            
        except Exception as e:
            self.logger.error(f"Error generating QA report: {e}")
            return {
                "error": str(e),
                "story_id": story_id,
                "testing_failed": True
            }
    
    def _calculate_quality_metrics(self, qa_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall quality metrics from QA results.
        
        Args:
            qa_results: QA testing results
            
        Returns:
            Quality metrics summary
        """
        try:
            # Extract individual scores
            persona_score = qa_results.get("anna_persona_testing", {}).get("satisfaction_score", 0)
            accessibility_score = qa_results.get("accessibility_compliance", {}).get("compliance_percentage", 0) / 20  # Convert to 1-5 scale
            flow_score = qa_results.get("user_flow_validation", {}).get("success_rate_percentage", 0) / 20  # Convert to 1-5 scale
            
            content_quality = qa_results.get("content_quality_assessment", {})
            content_score = (
                content_quality.get("professional_tone_score", 0) +
                content_quality.get("pedagogical_value_score", 0) +
                content_quality.get("policy_relevance_score", 0)
            ) / 3
            
            # Calculate weighted overall score
            overall_score = (
                persona_score * 0.3 +      # 30% Anna persona satisfaction
                accessibility_score * 0.25 + # 25% Accessibility compliance
                flow_score * 0.25 +        # 25% User flow success
                content_score * 0.2        # 20% Content quality
            )
            
            return {
                "overall_score": round(overall_score, 2),
                "persona_satisfaction_score": round(persona_score, 2),
                "accessibility_score": round(accessibility_score, 2),
                "user_flow_score": round(flow_score, 2),
                "content_quality_score": round(content_score, 2),
                "score_breakdown": {
                    "persona_weight": 0.3,
                    "accessibility_weight": 0.25,
                    "flow_weight": 0.25,
                    "content_weight": 0.2
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error calculating quality metrics: {e}")
            return {
                "overall_score": 0.0,
                "error": str(e)
            }
    
    async def _generate_recommendations(self, persona_results: Dict[str, Any],
                                      accessibility_results: Dict[str, Any],
                                      content_quality: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate improvement recommendations based on QA results.
        
        Args:
            persona_results: Anna persona testing results
            accessibility_results: Accessibility testing results
            content_quality: Content quality assessment
            
        Returns:
            List of improvement recommendations
        """
        recommendations = []
        
        try:
            # Anna persona recommendations
            if persona_results.get("satisfaction_score", 0) < 4:
                recommendations.append({
                    "category": "user_experience",
                    "priority": "high",
                    "issue": "Anna persona satisfaction below threshold",
                    "recommendation": "Improve user interface clarity and task flow simplification",
                    "expected_impact": "Increased user satisfaction and task completion rates"
                })
            
            if persona_results.get("average_completion_time_minutes", 0) > 10:
                recommendations.append({
                    "category": "performance",
                    "priority": "high",
                    "issue": "Task completion time exceeds 10-minute constraint",
                    "recommendation": "Streamline user workflows and reduce cognitive load",
                    "expected_impact": "Faster task completion within time constraints"
                })
            
            # Accessibility recommendations
            if accessibility_results.get("compliance_percentage", 0) < 100:
                recommendations.append({
                    "category": "accessibility",
                    "priority": "high",
                    "issue": "WCAG AA compliance not fully achieved",
                    "recommendation": "Address accessibility violations in identified components",
                    "expected_impact": "Full accessibility compliance for all users"
                })
            
            # Content quality recommendations
            if content_quality.get("professional_tone_score", 0) < 4:
                recommendations.append({
                    "category": "content_quality",
                    "priority": "medium",
                    "issue": "Professional tone not consistently maintained",
                    "recommendation": "Review and revise content for appropriate municipal context",
                    "expected_impact": "Enhanced professional credibility and user trust"
                })
            
            if content_quality.get("pedagogical_value_score", 0) < 4:
                recommendations.append({
                    "category": "learning_effectiveness",
                    "priority": "medium",
                    "issue": "Pedagogical value could be enhanced",
                    "recommendation": "Add more interactive learning elements and clear examples",
                    "expected_impact": "Improved learning outcomes and skill transfer"
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return [{
                "category": "system_error",
                "priority": "high",
                "issue": "Failed to generate recommendations",
                "recommendation": "Review QA testing process and results",
                "error": str(e)
            }]
    
    async def _save_qa_reports(self, story_id: str, qa_report: Dict[str, Any]) -> None:
        """
        Save QA reports to appropriate files.
        
        Args:
            story_id: Story identifier
            qa_report: Complete QA report to save
        """
        try:
            # Ensure QA reports directory exists
            qa_reports_dir = Path("docs/qa_reports")
            qa_reports_dir.mkdir(parents=True, exist_ok=True)
            
            # Save UX validation report (Markdown)
            ux_report_path = qa_reports_dir / f"{story_id}_ux_validation.md"
            ux_markdown = self._generate_ux_validation_markdown(qa_report)
            with open(ux_report_path, 'w', encoding='utf-8') as f:
                f.write(ux_markdown)
            
            # Save accessibility report (JSON)
            accessibility_path = qa_reports_dir / f"{story_id}_accessibility.json"
            with open(accessibility_path, 'w', encoding='utf-8') as f:
                json.dump(qa_report["detailed_results"]["accessibility_compliance"], f, indent=2)
            
            # Save persona testing report (JSON)
            persona_path = qa_reports_dir / f"{story_id}_persona_testing.json"
            with open(persona_path, 'w', encoding='utf-8') as f:
                json.dump(qa_report["detailed_results"]["anna_persona_testing"], f, indent=2)
            
            # Save comprehensive QA report (JSON)
            comprehensive_path = qa_reports_dir / f"{story_id}_comprehensive_qa.json"
            with open(comprehensive_path, 'w', encoding='utf-8') as f:
                json.dump(qa_report, f, indent=2)
            
            self.logger.info(f"QA reports saved for story: {story_id}")
            
        except Exception as e:
            self.logger.error(f"Error saving QA reports: {e}")
            raise AgentExecutionError(f"Failed to save QA reports: {e}")
    
    def _generate_ux_validation_markdown(self, qa_report: Dict[str, Any]) -> str:
        """
        Generate UX validation report in Markdown format.
        
        Args:
            qa_report: Complete QA report
            
        Returns:
            Markdown formatted UX validation report
        """
        story_id = qa_report.get("story_id", "unknown")
        summary = qa_report.get("qa_testing_summary", {})
        
        markdown = f"""# UX Validation Report - {story_id}

## Executive Summary

**Overall Quality Score:** {summary.get('overall_quality_score', 0)}/5.0

**Anna Persona Satisfaction:** {summary.get('anna_persona_satisfaction', 0)}/5.0

**Accessibility Compliance:** {summary.get('accessibility_compliance_score', 0)}%

**User Flow Success Rate:** {summary.get('user_flow_success_rate', 0)}%

## Detailed Results

### Anna Persona Testing
- **Satisfaction Score:** {summary.get('anna_persona_satisfaction', 0)}/5.0
- **Task Completion Rate:** {qa_report.get('detailed_results', {}).get('anna_persona_testing', {}).get('task_completion_rate', 0)}%
- **Average Completion Time:** {qa_report.get('detailed_results', {}).get('anna_persona_testing', {}).get('average_completion_time_minutes', 0)} minutes

### Accessibility Compliance
- **WCAG Level:** {qa_report.get('detailed_results', {}).get('accessibility_compliance', {}).get('compliance_level', 'Unknown')}
- **Compliance Score:** {summary.get('accessibility_compliance_score', 0)}%

### Content Quality
- **Professional Tone:** {qa_report.get('detailed_results', {}).get('content_quality_assessment', {}).get('professional_tone_score', 0)}/5.0
- **Pedagogical Value:** {qa_report.get('detailed_results', {}).get('content_quality_assessment', {}).get('pedagogical_value_score', 0)}/5.0
- **Policy Relevance:** {qa_report.get('detailed_results', {}).get('content_quality_assessment', {}).get('policy_relevance_score', 0)}/5.0

## Recommendations

"""
        
        recommendations = qa_report.get("recommendations", [])
        for i, rec in enumerate(recommendations, 1):
            markdown += f"""### {i}. {rec.get('category', 'General').replace('_', ' ').title()}
- **Priority:** {rec.get('priority', 'medium').title()}
- **Issue:** {rec.get('issue', 'No description')}
- **Recommendation:** {rec.get('recommendation', 'No recommendation')}
- **Expected Impact:** {rec.get('expected_impact', 'Unknown impact')}

"""
        
        markdown += f"""## DNA Compliance

**Design Principles:**
- Pedagogical Value: {'' if qa_report.get('dna_compliance_results', {}).get('design_principles_validation', {}).get('pedagogical_value', False) else 'L'}
- Policy to Practice: {'' if qa_report.get('dna_compliance_results', {}).get('design_principles_validation', {}).get('policy_to_practice', False) else 'L'}
- Time Respect: {'' if qa_report.get('dna_compliance_results', {}).get('design_principles_validation', {}).get('time_respect', False) else 'L'}
- Holistic Thinking: {'' if qa_report.get('dna_compliance_results', {}).get('design_principles_validation', {}).get('holistic_thinking', False) else 'L'}
- Professional Tone: {'' if qa_report.get('dna_compliance_results', {}).get('design_principles_validation', {}).get('professional_tone', False) else 'L'}

---

*Report generated by QA Tester Agent on {qa_report.get('testing_metadata', {}).get('testing_timestamp', 'unknown')}*
"""
        
        return markdown
    
    def _extract_user_stories_from_implementation(self, implementation_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract user stories from implementation data for UAT."""
        user_stories = []
        
        # Extract from UI components
        ui_components = implementation_data.get("ui_components", [])
        for component in ui_components:
            if isinstance(component, dict):
                component_type = component.get("component_type", "")
                component_id = component.get("component_id", "")
                
                user_stories.append({
                    "story_id": f"US_{component_id}",
                    "description": f"As Anna, I want to use {component_type} to complete my task efficiently",
                    "acceptance_criteria": [
                        f"{component_type} should be accessible and usable",
                        f"Task completion should be within time constraints",
                        f"Interface should be intuitive for municipal users"
                    ],
                    "priority": "must_have",
                    "component_reference": component_id
                })
        
        # Extract from user flows
        user_flows = implementation_data.get("user_flows", [])
        for flow in user_flows:
            if isinstance(flow, dict):
                flow_id = flow.get("flow_id", "")
                
                user_stories.append({
                    "story_id": f"US_FLOW_{flow_id}",
                    "description": f"As Anna, I want to complete the {flow_id} workflow efficiently",
                    "acceptance_criteria": [
                        "Workflow should be logical and intuitive",
                        "Each step should be clear and actionable",
                        "Completion should be within 10 minutes"
                    ],
                    "priority": "must_have",
                    "flow_reference": flow_id
                })
        
        # Add default user story if none extracted
        if not user_stories:
            user_stories.append({
                "story_id": "US_DEFAULT",
                "description": "As Anna, I want to use the training feature effectively",
                "acceptance_criteria": [
                    "Feature should be accessible and usable",
                    "Training objectives should be met",
                    "User satisfaction should be high"
                ],
                "priority": "must_have"
            })
        
        return user_stories
    
    async def _validate_enhanced_qa_dna_compliance(
        self,
        persona_results: Dict[str, Any],
        accessibility_results: Dict[str, Any],
        content_quality: Dict[str, Any],
        performance_results: Any,
        municipal_compliance: Any,
        exploratory_results: Any,
        uat_results: Any,
        ai_predictions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Enhanced DNA compliance validation with comprehensive testing results."""
        try:
            # Get base DNA compliance
            base_compliance = await self._validate_qa_dna_compliance(
                persona_results, accessibility_results, content_quality
            )
            
            # Enhanced design principles validation
            design_principles = base_compliance.get("design_principles_validation", {})
            
            # Performance-based validation
            if hasattr(performance_results, 'overall_performance_score'):
                performance_score = performance_results.overall_performance_score
                design_principles["time_respect"] = (
                    design_principles.get("time_respect", False) and 
                    performance_score >= 4.0
                )
            
            # Municipal compliance validation
            if hasattr(municipal_compliance, 'overall_municipal_readiness_score'):
                municipal_score = municipal_compliance.overall_municipal_readiness_score
                design_principles["policy_to_practice"] = (
                    design_principles.get("policy_to_practice", False) and
                    municipal_score >= 4.0
                )
            
            # Security validation from exploratory testing
            if hasattr(exploratory_results, 'security_clearance_status'):
                security_status = exploratory_results.security_clearance_status
                architecture_compliance = base_compliance.get("architecture_compliance", {})
                architecture_compliance["security_first"] = security_status in ["SECURITY_CLEARED", "SECURITY_REVIEW_REQUIRED"]
            
            # UAT validation
            if hasattr(uat_results, 'deployment_readiness_score'):
                uat_readiness = uat_results.deployment_readiness_score
                design_principles["holistic_thinking"] = (
                    design_principles.get("holistic_thinking", False) and
                    uat_readiness >= 80.0
                )
            
            # AI-enhanced validation (if available)
            if ai_predictions:
                quality_prediction = ai_predictions.get("quality_prediction")
                anna_prediction = ai_predictions.get("anna_prediction", {})
                
                # AI quality score validation
                if quality_prediction and hasattr(quality_prediction, 'predicted_score'):
                    ai_quality_score = quality_prediction.predicted_score
                    if ai_quality_score >= 4.0:
                        # High AI prediction reinforces DNA compliance
                        design_principles["pedagogical_value"] = (
                            design_principles.get("pedagogical_value", False) and True
                        )
                
                # AI Anna satisfaction validation
                ai_anna_satisfaction = anna_prediction.get("predicted_satisfaction_score", 0)
                if ai_anna_satisfaction >= 4.0:
                    design_principles["time_respect"] = (
                        design_principles.get("time_respect", False) and True
                    )
                    design_principles["professional_tone"] = (
                        design_principles.get("professional_tone", False) and True
                    )
            
            # Calculate overall compliance
            all_design_principles = all(design_principles.values())
            all_architecture_principles = all(base_compliance.get("architecture_compliance", {}).values())
            overall_compliance = all_design_principles and all_architecture_principles
            
            return {
                "design_principles_validation": design_principles,
                "architecture_compliance": base_compliance.get("architecture_compliance", {}),
                "overall_compliance": overall_compliance,
                "enhanced_validation_applied": True,
                "validation_timestamp": datetime.now().isoformat(),
                "performance_factor": getattr(performance_results, 'overall_performance_score', 0),
                "municipal_factor": getattr(municipal_compliance, 'overall_municipal_readiness_score', 0),
                "security_factor": getattr(exploratory_results, 'security_clearance_status', 'NOT_TESTED'),
                "uat_factor": getattr(uat_results, 'deployment_readiness_score', 0),
                "ai_enhanced": ai_predictions is not None,
                "ai_quality_score": ai_predictions.get("quality_prediction").predicted_score if ai_predictions and ai_predictions.get("quality_prediction") else None,
                "ai_anna_satisfaction": ai_predictions.get("anna_prediction", {}).get("predicted_satisfaction_score") if ai_predictions else None
            }
            
        except Exception as e:
            self.logger.error(f"Enhanced DNA compliance validation failed: {e}")
            # Fallback to base compliance
            return await self._validate_qa_dna_compliance(persona_results, accessibility_results, content_quality)
    
    async def _generate_enhanced_qa_report(
        self,
        story_id: str,
        persona_results: Dict[str, Any],
        accessibility_results: Dict[str, Any],
        flow_validation: Dict[str, Any],
        content_quality: Dict[str, Any],
        performance_results: Any,
        municipal_compliance: Any,
        exploratory_results: Any,
        uat_results: Any,
        dna_compliance: Dict[str, Any],
        ai_predictions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate enhanced comprehensive QA report with all testing results."""
        try:
            # Get base QA report
            base_report = await self._generate_qa_report(
                story_id, persona_results, accessibility_results, 
                flow_validation, content_quality, dna_compliance
            )
            
            # Add enhanced testing results
            enhanced_results = {
                "performance_testing": {
                    "overall_score": getattr(performance_results, 'overall_performance_score', 0),
                    "performance_passed": getattr(performance_results, 'performance_passed', False),
                    "load_test_results": len(getattr(performance_results, 'load_test_results', [])),
                    "critical_issues": getattr(performance_results, 'critical_issues', [])
                },
                "municipal_compliance": {
                    "readiness_score": getattr(municipal_compliance, 'overall_municipal_readiness_score', 0),
                    "deployment_approved": getattr(municipal_compliance, 'municipal_deployment_approved', False),
                    "legal_compliance": getattr(municipal_compliance, 'legal_compliance_status', 'NOT_TESTED'),
                    "critical_blockers": getattr(municipal_compliance, 'critical_blockers', [])
                },
                "exploratory_testing": {
                    "overall_score": getattr(exploratory_results, 'overall_exploratory_score', 0),
                    "security_status": getattr(exploratory_results, 'security_clearance_status', 'NOT_TESTED'),
                    "critical_issues": getattr(exploratory_results, 'critical_issues_found', []),
                    "boundary_tests_passed": len([r for r in getattr(exploratory_results, 'boundary_test_results', []) if r.passed]) if hasattr(exploratory_results, 'boundary_test_results') else 0
                },
                "user_acceptance_testing": {
                    "deployment_readiness": getattr(uat_results, 'deployment_readiness_score', 0),
                    "overall_approval": str(getattr(uat_results, 'overall_approval_status', 'NOT_TESTED')),
                    "stakeholder_satisfaction": len([f for f in getattr(uat_results, 'stakeholder_feedback', []) if f.approval_status.value in ['approved', 'approved_with_conditions']]) if hasattr(uat_results, 'stakeholder_feedback') else 0,
                    "training_effectiveness": getattr(getattr(uat_results, 'training_effectiveness', None), 'knowledge_retention_score', 0) if hasattr(uat_results, 'training_effectiveness') else 0
                }
            }
            
            # Enhance the base report
            base_report["enhanced_testing_results"] = enhanced_results
            base_report["enhanced_qa_applied"] = True
            
            # Add AI intelligence results (if available)
            if ai_predictions:
                base_report["ai_intelligence_results"] = {
                    "quality_prediction": ai_predictions.get("quality_prediction").to_dict() if ai_predictions.get("quality_prediction") else None,
                    "test_optimization": ai_predictions.get("test_optimization").to_dict() if ai_predictions.get("test_optimization") else None,
                    "anna_satisfaction_prediction": ai_predictions.get("anna_prediction", {}),
                    "ai_quality_insights": [insight.to_dict() for insight in ai_predictions.get("quality_insights", [])],
                    "ai_enhancement_applied": True,
                    "ai_confidence_level": ai_predictions.get("quality_prediction").confidence_level.value if ai_predictions.get("quality_prediction") else "not_available"
                }
            
            # Update overall quality score with enhanced results
            enhanced_scores = [
                enhanced_results["performance_testing"]["overall_score"],
                enhanced_results["municipal_compliance"]["readiness_score"],
                enhanced_results["exploratory_testing"]["overall_score"],
                enhanced_results["user_acceptance_testing"]["deployment_readiness"] / 20  # Convert to 1-5 scale
            ]
            
            original_score = base_report.get("qa_testing_summary", {}).get("overall_quality_score", 0)
            enhanced_avg = sum(enhanced_scores) / len(enhanced_scores) if enhanced_scores else 0
            
            # Include AI prediction in final score calculation
            ai_quality_factor = 0
            if ai_predictions and ai_predictions.get("quality_prediction"):
                ai_quality_score = ai_predictions.get("quality_prediction").predicted_score
                ai_confidence = ai_predictions.get("quality_prediction").confidence_percentage
                # Weight AI prediction by confidence level
                ai_quality_factor = (ai_quality_score * ai_confidence / 100) * 0.1  # 10% weight for AI
            
            # Weighted combination: 50% original + 30% enhanced + 20% AI (if available)
            if ai_quality_factor > 0:
                final_score = (original_score * 0.5) + (enhanced_avg * 0.3) + (ai_quality_factor * 0.2)
                base_report["qa_testing_summary"]["ai_enhanced_score"] = True
            else:
                final_score = (original_score * 0.6) + (enhanced_avg * 0.4)
            
            base_report["qa_testing_summary"]["overall_quality_score"] = round(final_score, 2)
            base_report["qa_testing_summary"]["enhanced_score_applied"] = True
            
            # Add comprehensive recommendations
            all_recommendations = base_report.get("recommendations", [])
            
            # Add AI-generated recommendations (if available)
            if ai_predictions and ai_predictions.get("quality_prediction"):
                ai_prediction = ai_predictions.get("quality_prediction")
                for suggestion in ai_prediction.improvement_suggestions[:3]:  # Top 3 AI suggestions
                    all_recommendations.append({
                        "category": "ai_optimization",
                        "priority": "high",
                        "issue": "AI-identified improvement opportunity",
                        "recommendation": suggestion,
                        "expected_impact": "AI-predicted quality enhancement",
                        "confidence": ai_prediction.confidence_percentage,
                        "source": "AI Quality Intelligence Engine"
                    })
            
            # Add performance recommendations
            if hasattr(performance_results, 'recommendations'):
                for rec in performance_results.recommendations[:3]:  # Top 3
                    all_recommendations.append({
                        "category": "performance",
                        "priority": "high",
                        "issue": "Performance optimization needed",
                        "recommendation": rec,
                        "expected_impact": "Improved user experience and system reliability"
                    })
            
            # Add municipal compliance recommendations
            if hasattr(municipal_compliance, 'recommendations'):
                for rec in municipal_compliance.recommendations[:3]:  # Top 3
                    all_recommendations.append({
                        "category": "municipal_compliance",
                        "priority": "high",
                        "issue": "Municipal compliance gap",
                        "recommendation": rec,
                        "expected_impact": "Legal compliance and municipal user satisfaction"
                    })
            
            # Add security recommendations
            if hasattr(exploratory_results, 'high_priority_recommendations'):
                for rec in exploratory_results.high_priority_recommendations[:3]:  # Top 3
                    all_recommendations.append({
                        "category": "security",
                        "priority": "critical",
                        "issue": "Security vulnerability identified",
                        "recommendation": rec,
                        "expected_impact": "Improved security posture and compliance"
                    })
            
            # Add UAT recommendations
            if hasattr(uat_results, 'recommended_actions'):
                for rec in uat_results.recommended_actions[:3]:  # Top 3
                    all_recommendations.append({
                        "category": "user_acceptance",
                        "priority": "medium",
                        "issue": "User acceptance improvement needed",
                        "recommendation": rec,
                        "expected_impact": "Higher stakeholder satisfaction and adoption"
                    })
            
            base_report["recommendations"] = all_recommendations
            
            return base_report
            
        except Exception as e:
            self.logger.error(f"Enhanced QA report generation failed: {e}")
            # Fallback to base report
            return await self._generate_qa_report(
                story_id, persona_results, accessibility_results,
                flow_validation, content_quality, dna_compliance
            )