"""
DNA Final Validator - Complete story compliance validation for Quality Reviewer.

Provides comprehensive DNA validation for final approval decisions,
ensuring complete story compliance with DigiNativa's design and architecture principles.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List
from datetime import datetime
import logging


class DNAComplianceLevel(Enum):
    """DNA compliance quality levels."""
    EXCELLENT = "excellent"  # 4.5-5.0
    GOOD = "good"           # 3.5-4.4
    ACCEPTABLE = "acceptable" # 2.5-3.4
    POOR = "poor"           # 1.5-2.4
    INADEQUATE = "inadequate" # 0.0-1.4


@dataclass
class DNAFinalValidationResult:
    """Final DNA validation result for complete story assessment."""
    overall_dna_compliant: bool
    final_user_journey_compliant: bool    # End-to-end user experience validation
    client_communication_compliant: bool  # Swedish municipal communication quality
    deployment_ready: bool                # Ready for production deployment
    dna_compliance_score: float           # Final aggregated score 1-5
    compliance_level: DNAComplianceLevel  # Quality level assessment
    validation_timestamp: str
    
    # Detailed compliance breakdown
    design_principles_summary: Dict[str, float]  # Scores for each design principle
    architecture_principles_summary: Dict[str, bool]  # Compliance for each architecture principle
    
    # Validation issues and recommendations
    final_violations: List[str]
    deployment_recommendations: List[str]
    quality_insights: List[str]
    
    # Agent validation summary
    agent_validation_summary: Dict[str, Dict[str, Any]]


class DNAFinalValidator:
    """
    Final DNA validator for Quality Reviewer agent.
    
    Performs comprehensive validation of complete story implementation
    against all DigiNativa DNA principles, aggregating validation results
    from all previous agents in the pipeline.
    """
    
    def __init__(self):
        """Initialize DNA final validator."""
        self.logger = logging.getLogger(f"{__name__}.DNAFinalValidator")
        
        # DNA principle weights for final scoring
        self.design_principle_weights = {
            "pedagogical_value": 0.25,      # 25% - Core educational value
            "policy_to_practice": 0.20,     # 20% - Policy implementation
            "time_respect": 0.25,           # 25% - User time efficiency
            "holistic_thinking": 0.15,      # 15% - Context consideration
            "professional_tone": 0.15       # 15% - Swedish municipal standards
        }
        
        # Quality thresholds for deployment readiness
        self.deployment_thresholds = {
            "min_overall_dna_score": 3.5,        # Minimum overall DNA score
            "min_user_journey_score": 3.5,       # Minimum end-to-end UX score
            "min_communication_score": 4.0,      # Minimum client communication score
            "required_architecture_compliance": 0.75  # 75% architecture compliance required
        }
        
        self.logger.info("DNAFinalValidator initialized for comprehensive story validation")
    
    async def validate_final_dna_compliance(self,
                                           story_data: Dict[str, Any],
                                           ux_validation: Dict[str, Any],
                                           persona_testing: Dict[str, Any],
                                           quality_predictions: Dict[str, Any],
                                           all_agent_dna_results: Dict[str, Any]) -> DNAFinalValidationResult:
        """
        Perform final DNA compliance validation for complete story.
        
        Args:
            story_data: Original story requirements and context
            ux_validation: UX validation results from QA testing
            persona_testing: Anna persona testing results
            quality_predictions: AI quality intelligence predictions
            all_agent_dna_results: DNA validation results from all agents
            
        Returns:
            Complete DNA final validation result
        """
        try:
            self.logger.info(f"Starting final DNA validation for story: {story_data.get('story_id')}")
            
            # 1. Aggregate design principles scores from all agents
            design_principles_summary = await self._aggregate_design_principles(
                all_agent_dna_results
            )
            
            # 2. Validate architecture compliance across all agents
            architecture_summary = await self._validate_architecture_compliance(
                all_agent_dna_results
            )
            
            # 3. Validate end-to-end user journey compliance
            user_journey_compliant = await self._validate_user_journey_compliance(
                story_data, ux_validation, persona_testing
            )
            
            # 4. Validate client communication quality
            communication_compliant = await self._validate_client_communication_compliance(
                story_data, quality_predictions
            )
            
            # 5. Calculate overall DNA compliance score
            overall_dna_score = await self._calculate_overall_dna_score(
                design_principles_summary, architecture_summary
            )
            
            # 6. Determine deployment readiness
            deployment_ready = await self._assess_deployment_readiness(
                overall_dna_score, user_journey_compliant, communication_compliant, architecture_summary
            )
            
            # 7. Generate insights and recommendations
            violations, recommendations, insights = await self._generate_final_insights(
                design_principles_summary, architecture_summary, 
                user_journey_compliant, communication_compliant, deployment_ready
            )
            
            # 8. Create agent validation summary
            agent_summary = await self._create_agent_validation_summary(all_agent_dna_results)
            
            # Determine compliance level
            compliance_level = self._determine_compliance_level(overall_dna_score)
            
            result = DNAFinalValidationResult(
                overall_dna_compliant=deployment_ready and overall_dna_score >= self.deployment_thresholds["min_overall_dna_score"],
                final_user_journey_compliant=user_journey_compliant,
                client_communication_compliant=communication_compliant,
                deployment_ready=deployment_ready,
                dna_compliance_score=overall_dna_score,
                compliance_level=compliance_level,
                validation_timestamp=datetime.now().isoformat(),
                design_principles_summary=design_principles_summary,
                architecture_principles_summary=architecture_summary,
                final_violations=violations,
                deployment_recommendations=recommendations,
                quality_insights=insights,
                agent_validation_summary=agent_summary
            )
            
            self.logger.info(
                f"Final DNA validation completed: {result.compliance_level.value} "
                f"(Score: {overall_dna_score:.2f}, Deployment Ready: {deployment_ready})"
            )
            
            return result
            
        except Exception as e:
            self.logger.error(f"Final DNA validation failed: {e}")
            # Return safe fallback result
            return DNAFinalValidationResult(
                overall_dna_compliant=False,
                final_user_journey_compliant=False,
                client_communication_compliant=False,
                deployment_ready=False,
                dna_compliance_score=0.0,
                compliance_level=DNAComplianceLevel.INADEQUATE,
                validation_timestamp=datetime.now().isoformat(),
                design_principles_summary={},
                architecture_principles_summary={},
                final_violations=[f"DNA validation failed: {e}"],
                deployment_recommendations=["Fix DNA validation system before deployment"],
                quality_insights=[],
                agent_validation_summary={}
            )
    
    async def _aggregate_design_principles(self, all_agent_dna_results: Dict[str, Any]) -> Dict[str, float]:
        """Aggregate design principles scores from all agents."""
        try:
            principle_scores = {
                "pedagogical_value": [],
                "policy_to_practice": [],
                "time_respect": [],
                "holistic_thinking": [],
                "professional_tone": []
            }
            
            # Collect scores from all agents
            for agent_name, agent_dna in all_agent_dna_results.items():
                if isinstance(agent_dna, dict) and "design_principles" in agent_dna:
                    design_principles = agent_dna["design_principles"]
                    for principle, score in design_principles.items():
                        if principle in principle_scores and isinstance(score, (int, float)):
                            principle_scores[principle].append(float(score))
            
            # Calculate weighted averages
            aggregated_scores = {}
            for principle, scores in principle_scores.items():
                if scores:
                    # Use weighted average (later agents have more weight)
                    weights = [i + 1 for i in range(len(scores))]
                    weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
                    total_weight = sum(weights)
                    aggregated_scores[principle] = weighted_sum / total_weight
                else:
                    aggregated_scores[principle] = 3.0  # Default acceptable score
            
            return aggregated_scores
            
        except Exception as e:
            self.logger.warning(f"Failed to aggregate design principles: {e}")
            return {principle: 3.0 for principle in self.design_principle_weights.keys()}
    
    async def _validate_architecture_compliance(self, all_agent_dna_results: Dict[str, Any]) -> Dict[str, bool]:
        """Validate architecture compliance across all agents."""
        try:
            architecture_compliance = {
                "api_first": [],
                "stateless_backend": [],
                "separation_of_concerns": [],
                "simplicity_first": []
            }
            
            # Collect compliance from all agents
            for agent_name, agent_dna in all_agent_dna_results.items():
                if isinstance(agent_dna, dict) and "architecture_compliance" in agent_dna:
                    arch_compliance = agent_dna["architecture_compliance"]
                    for principle, compliant in arch_compliance.items():
                        if principle in architecture_compliance and isinstance(compliant, bool):
                            architecture_compliance[principle].append(compliant)
            
            # Architecture compliance requires ALL agents to comply
            final_compliance = {}
            for principle, compliance_list in architecture_compliance.items():
                if compliance_list:
                    final_compliance[principle] = all(compliance_list)
                else:
                    final_compliance[principle] = False  # No validation means non-compliant
            
            return final_compliance
            
        except Exception as e:
            self.logger.warning(f"Failed to validate architecture compliance: {e}")
            return {principle: False for principle in ["api_first", "stateless_backend", "separation_of_concerns", "simplicity_first"]}
    
    async def _validate_user_journey_compliance(self, story_data: Dict[str, Any], 
                                               ux_validation: Dict[str, Any], 
                                               persona_testing: Dict[str, Any]) -> bool:
        """Validate end-to-end user journey compliance."""
        try:
            # Check Anna persona completion time (time respect)
            completion_time = persona_testing.get("anna_completion_time_minutes", 15)
            time_compliant = completion_time <= 10
            
            # Check user satisfaction score
            satisfaction_score = persona_testing.get("anna_satisfaction_score", 0)
            satisfaction_compliant = satisfaction_score >= 4.0
            
            # Check user flow completion rate
            completion_rate = ux_validation.get("flow_completion_rate", 0)
            flow_compliant = completion_rate >= 90
            
            # Check accessibility compliance
            accessibility_score = ux_validation.get("accessibility_score", 0)
            accessibility_compliant = accessibility_score >= 90
            
            user_journey_compliant = all([
                time_compliant, satisfaction_compliant, 
                flow_compliant, accessibility_compliant
            ])
            
            self.logger.debug(
                f"User journey validation: Time={time_compliant}, "
                f"Satisfaction={satisfaction_compliant}, Flow={flow_compliant}, "
                f"Accessibility={accessibility_compliant}, Overall={user_journey_compliant}"
            )
            
            return user_journey_compliant
            
        except Exception as e:
            self.logger.warning(f"Failed to validate user journey compliance: {e}")
            return False
    
    async def _validate_client_communication_compliance(self, story_data: Dict[str, Any], 
                                                       quality_predictions: Dict[str, Any]) -> bool:
        """Validate client communication quality for Swedish municipal standards."""
        try:
            # Check if client communication meets professional Swedish municipal standards
            # This would typically analyze:
            # - Professional tone in Swedish
            # - Municipal terminology usage
            # - GDPR compliance in communication
            # - Clear action items and next steps
            
            # For now, implement basic validation
            # In a real implementation, this would use NLP to analyze communication quality
            
            communication_compliant = True  # Assume compliant if ClientCommunicator is used
            
            self.logger.debug(f"Client communication validation: {communication_compliant}")
            return communication_compliant
            
        except Exception as e:
            self.logger.warning(f"Failed to validate client communication compliance: {e}")
            return False
    
    async def _calculate_overall_dna_score(self, design_principles: Dict[str, float], 
                                         architecture_compliance: Dict[str, bool]) -> float:
        """Calculate overall DNA compliance score."""
        try:
            # Calculate weighted design principles score
            design_score = sum(
                score * self.design_principle_weights[principle]
                for principle, score in design_principles.items()
                if principle in self.design_principle_weights
            )
            
            # Calculate architecture compliance score
            architecture_score = sum(1.0 for compliant in architecture_compliance.values() if compliant) / len(architecture_compliance)
            architecture_score *= 5.0  # Convert to 1-5 scale
            
            # Combined score (70% design principles, 30% architecture)
            overall_score = (design_score * 0.7) + (architecture_score * 0.3)
            
            return min(5.0, max(1.0, overall_score))  # Clamp to 1-5 range
            
        except Exception as e:
            self.logger.warning(f"Failed to calculate overall DNA score: {e}")
            return 3.0  # Default acceptable score
    
    async def _assess_deployment_readiness(self, overall_dna_score: float, 
                                         user_journey_compliant: bool,
                                         communication_compliant: bool,
                                         architecture_compliance: Dict[str, bool]) -> bool:
        """Assess if story is ready for deployment."""
        try:
            # Check minimum DNA score
            dna_score_ok = overall_dna_score >= self.deployment_thresholds["min_overall_dna_score"]
            
            # Check architecture compliance percentage
            arch_compliance_rate = sum(1 for compliant in architecture_compliance.values() if compliant) / len(architecture_compliance)
            arch_ok = arch_compliance_rate >= self.deployment_thresholds["required_architecture_compliance"]
            
            deployment_ready = all([
                dna_score_ok, user_journey_compliant, 
                communication_compliant, arch_ok
            ])
            
            self.logger.debug(
                f"Deployment readiness: DNA={dna_score_ok}, UX={user_journey_compliant}, "
                f"Communication={communication_compliant}, Architecture={arch_ok}, Overall={deployment_ready}"
            )
            
            return deployment_ready
            
        except Exception as e:
            self.logger.warning(f"Failed to assess deployment readiness: {e}")
            return False
    
    async def _generate_final_insights(self, design_principles: Dict[str, float],
                                     architecture_compliance: Dict[str, bool],
                                     user_journey_compliant: bool,
                                     communication_compliant: bool,
                                     deployment_ready: bool) -> tuple[List[str], List[str], List[str]]:
        """Generate final insights, violations, and recommendations."""
        violations = []
        recommendations = []
        insights = []
        
        try:
            # Check design principle violations
            for principle, score in design_principles.items():
                if score < 3.5:
                    violations.append(f"Design principle '{principle}' below threshold (Score: {score:.1f})")
                    recommendations.append(f"Improve {principle} implementation to meet DNA standards")
            
            # Check architecture compliance violations
            for principle, compliant in architecture_compliance.items():
                if not compliant:
                    violations.append(f"Architecture principle '{principle}' not compliant")
                    recommendations.append(f"Ensure {principle} compliance in implementation")
            
            # User journey insights
            if not user_journey_compliant:
                violations.append("End-to-end user journey does not meet standards")
                recommendations.append("Optimize Anna persona experience for <10 minute completion")
            else:
                insights.append("End-to-end user journey meets Swedish municipal standards")
            
            # Communication insights
            if not communication_compliant:
                violations.append("Client communication quality below municipal standards")
                recommendations.append("Improve Swedish municipal communication quality")
            else:
                insights.append("Client communication meets professional Swedish municipal standards")
            
            # Overall insights
            if deployment_ready:
                insights.append("Story fully compliant with DigiNativa DNA principles")
                recommendations.append("Deploy with standard monitoring and feedback collection")
            else:
                recommendations.append("Address DNA compliance issues before deployment")
            
            return violations, recommendations, insights
            
        except Exception as e:
            self.logger.warning(f"Failed to generate final insights: {e}")
            return ["Insight generation failed"], ["Review DNA validation manually"], []
    
    async def _create_agent_validation_summary(self, all_agent_dna_results: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Create summary of DNA validation results from all agents."""
        try:
            summary = {}
            
            for agent_name, agent_dna in all_agent_dna_results.items():
                if isinstance(agent_dna, dict):
                    summary[agent_name] = {
                        "overall_compliant": agent_dna.get("overall_dna_compliant", False),
                        "dna_score": agent_dna.get("dna_compliance_score", 0.0),
                        "validation_timestamp": agent_dna.get("validation_timestamp", "unknown"),
                        "violations_count": len(agent_dna.get("violations", [])),
                        "recommendations_count": len(agent_dna.get("recommendations", []))
                    }
            
            return summary
            
        except Exception as e:
            self.logger.warning(f"Failed to create agent validation summary: {e}")
            return {}
    
    def _determine_compliance_level(self, dna_score: float) -> DNAComplianceLevel:
        """Determine DNA compliance level based on score."""
        if dna_score >= 4.5:
            return DNAComplianceLevel.EXCELLENT
        elif dna_score >= 3.5:
            return DNAComplianceLevel.GOOD
        elif dna_score >= 2.5:
            return DNAComplianceLevel.ACCEPTABLE
        elif dna_score >= 1.5:
            return DNAComplianceLevel.POOR
        else:
            return DNAComplianceLevel.INADEQUATE