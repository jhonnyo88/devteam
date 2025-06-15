"""
DNA Story Validator - Active DNA validation for Project Manager agent.

PURPOSE:
Implements active DNA compliance validation for story analysis and breakdown,
ensuring Project Manager output meets DigiNativa DNA principles.

CRITICAL FUNCTIONALITY:
- Time Respect → Story complexity analysis (feature completable within 10 minutes)
- Pedagogical Value → Learning objective effectiveness validation  
- Professional Tone → Swedish municipal communication analysis
- Policy to Practice → Municipal requirement alignment validation
- Holistic Thinking → Story context and implications analysis

CONTRACT PROTECTION:
This tool enhances Project Manager DNA validation without breaking contracts.
All outputs integrate seamlessly with existing story validation results.
"""

import asyncio
import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# Setup logging
logger = logging.getLogger(__name__)


class StoryComplexityLevel(Enum):
    """Story complexity levels for time respect validation."""
    EXCELLENT = "excellent"  # Very simple, 5-7 minute features
    GOOD = "good"           # Simple, 7-10 minute features  
    ACCEPTABLE = "acceptable" # Moderate, exactly 10 minute features
    COMPLEX = "complex"     # Difficult, >10 minute features
    EXCESSIVE = "excessive" # Too complex, >15 minute features


class LearningEffectivenessLevel(Enum):
    """Learning effectiveness levels for pedagogical value validation."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    INADEQUATE = "inadequate"


class CommunicationQuality(Enum):
    """Communication quality for professional tone."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    UNCLEAR = "unclear"
    UNPROFESSIONAL = "unprofessional"


@dataclass
class StoryComplexityResult:
    """Result from story complexity analysis."""
    complexity_level: StoryComplexityLevel
    estimated_completion_time_minutes: float
    acceptance_criteria_count: int
    technical_complexity_score: float  # 1-5 scale
    ux_complexity_score: float       # 1-5 scale
    integration_complexity_score: float # 1-5 scale
    complexity_violations: List[str]
    simplification_recommendations: List[str]


@dataclass
class LearningEffectivenessResult:
    """Result from learning effectiveness validation."""
    effectiveness_level: LearningEffectivenessLevel
    learning_effectiveness_score: float  # 1-5 scale
    learning_objectives_quality: Dict[str, bool]
    pedagogical_approach_suitable: bool
    municipal_relevance_score: float    # 1-5 scale
    knowledge_transfer_potential: float # 1-5 scale
    effectiveness_violations: List[str]
    learning_improvement_recommendations: List[str]


@dataclass
class CommunicationQualityResult:
    """Result from communication quality analysis."""
    communication_quality: CommunicationQuality
    professional_score: float  # 1-5 scale
    swedish_municipal_terminology_present: Dict[str, int]
    tone_consistency: bool
    stakeholder_appropriateness: bool
    communication_violations: List[str]
    communication_improvement_recommendations: List[str]


@dataclass
class DNAStoryValidationResult:
    """Complete DNA story validation result."""
    overall_dna_compliant: bool
    time_respect_compliant: bool
    pedagogical_value_compliant: bool
    professional_tone_compliant: bool
    policy_to_practice_compliant: bool
    holistic_thinking_compliant: bool
    story_complexity_result: StoryComplexityResult
    learning_effectiveness_result: LearningEffectivenessResult
    communication_quality_result: CommunicationQualityResult
    validation_timestamp: str
    dna_compliance_score: float  # 1-5 scale
    quality_reviewer_metrics: Dict[str, Any]  # For Quality Reviewer integration


class DNAStoryValidator:
    """
    Active DNA validation for Project Manager story analysis.
    
    Validates story breakdowns against DigiNativa DNA principles:
    - Time Respect: Story complexity analysis for 10-minute completion
    - Pedagogical Value: Learning objective effectiveness validation
    - Professional Tone: Swedish municipal communication quality
    - Policy to Practice: Municipal requirement alignment
    - Holistic Thinking: Context and implications analysis
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DNA Story Validator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Time Respect validation thresholds
        self.story_complexity_thresholds = {
            "max_completion_time_minutes": 10.0,  # Total user completion time
            "max_acceptance_criteria": 5,         # Maximum criteria per story
            "max_technical_complexity": 3.0,      # 1-5 scale
            "max_ux_complexity": 3.0,             # 1-5 scale
            "max_integration_complexity": 3.0     # 1-5 scale
        }
        
        # Pedagogical Value validation criteria
        self.learning_effectiveness_criteria = {
            "min_learning_effectiveness": 4.0,    # 1-5 scale
            "min_learning_objectives": 2,         # Minimum learning objectives
            "min_municipal_relevance": 4.0,       # Municipal context relevance
            "min_knowledge_transfer": 4.0,        # Knowledge transfer potential
            "required_pedagogical_approach": True
        }
        
        # Professional Tone validation standards
        self.communication_standards = {
            "min_professional_score": 4.0,        # 1-5 scale
            "required_swedish_municipal_terms": [
                "kommun", "förvaltning", "medarbetare", "policy", "riktlinje",
                "utbildning", "kompetens", "utveckling", "service", "kvalitet"
            ],
            "forbidden_casual_terms": [
                "kolla", "fixa", "grejer", "typ", "liksom", "bara"
            ],
            "min_tone_consistency": 0.9           # 90% consistency required
        }
        
        logger.info("DNA Story Validator initialized for Project Manager")
    
    async def validate_story_dna_compliance(self,
                                          story_data: Dict[str, Any],
                                          story_breakdown: Dict[str, Any],
                                          acceptance_criteria: List[str],
                                          learning_objectives: List[str]) -> DNAStoryValidationResult:
        """
        Comprehensive DNA validation for story analysis.
        
        Args:
            story_data: Original story requirements
            story_breakdown: PM story breakdown
            acceptance_criteria: Story acceptance criteria
            learning_objectives: Learning objectives defined
            
        Returns:
            Complete DNA story validation result
        """
        try:
            logger.info("Starting comprehensive DNA story validation")
            
            # Validate Time Respect (story complexity)
            story_complexity_result = await self._validate_story_complexity(
                story_breakdown, acceptance_criteria, story_data
            )
            
            # Validate Pedagogical Value (learning effectiveness)
            learning_effectiveness_result = await self._validate_learning_effectiveness(
                learning_objectives, story_breakdown, story_data
            )
            
            # Validate Professional Tone (communication quality)
            communication_quality_result = await self._validate_communication_quality(
                story_breakdown, acceptance_criteria, learning_objectives
            )
            
            # Calculate overall DNA compliance
            time_respect_compliant = story_complexity_result.complexity_level in [
                StoryComplexityLevel.EXCELLENT, StoryComplexityLevel.GOOD, StoryComplexityLevel.ACCEPTABLE
            ]
            
            pedagogical_value_compliant = learning_effectiveness_result.effectiveness_level in [
                LearningEffectivenessLevel.EXCELLENT, LearningEffectivenessLevel.GOOD, LearningEffectivenessLevel.ACCEPTABLE
            ]
            
            professional_tone_compliant = communication_quality_result.communication_quality in [
                CommunicationQuality.EXCELLENT, CommunicationQuality.GOOD, CommunicationQuality.ACCEPTABLE
            ]
            
            # Additional DNA principle validations
            policy_to_practice_compliant = await self._validate_policy_to_practice_alignment(story_data, story_breakdown)
            holistic_thinking_compliant = await self._validate_holistic_thinking(story_breakdown, story_data)
            
            overall_dna_compliant = all([
                time_respect_compliant,
                pedagogical_value_compliant,
                professional_tone_compliant,
                policy_to_practice_compliant,
                holistic_thinking_compliant
            ])
            
            # Calculate overall DNA compliance score (1-5 scale)
            complexity_score = self._complexity_to_score(story_complexity_result.complexity_level)
            effectiveness_score = learning_effectiveness_result.learning_effectiveness_score
            communication_score = communication_quality_result.professional_score
            policy_score = 4.0 if policy_to_practice_compliant else 2.0
            holistic_score = 4.0 if holistic_thinking_compliant else 2.0
            
            dna_compliance_score = (complexity_score + effectiveness_score + communication_score + policy_score + holistic_score) / 5.0
            
            # Prepare metrics for Quality Reviewer
            quality_reviewer_metrics = {
                "story_complexity_score": complexity_score,
                "learning_effectiveness_score": effectiveness_score,
                "communication_quality_score": communication_score,
                "policy_alignment_score": policy_score,
                "holistic_thinking_score": holistic_score,
                "total_acceptance_criteria": len(acceptance_criteria),
                "total_learning_objectives": len(learning_objectives),
                "estimated_completion_time": story_complexity_result.estimated_completion_time_minutes
            }
            
            validation_result = DNAStoryValidationResult(
                overall_dna_compliant=overall_dna_compliant,
                time_respect_compliant=time_respect_compliant,
                pedagogical_value_compliant=pedagogical_value_compliant,
                professional_tone_compliant=professional_tone_compliant,
                policy_to_practice_compliant=policy_to_practice_compliant,
                holistic_thinking_compliant=holistic_thinking_compliant,
                story_complexity_result=story_complexity_result,
                learning_effectiveness_result=learning_effectiveness_result,
                communication_quality_result=communication_quality_result,
                validation_timestamp=datetime.now().isoformat(),
                dna_compliance_score=dna_compliance_score,
                quality_reviewer_metrics=quality_reviewer_metrics
            )
            
            logger.info(f"DNA story validation completed: {dna_compliance_score:.2f}/5.0 score")
            return validation_result
            
        except Exception as e:
            logger.error(f"DNA story validation failed: {e}")
            raise
    
    async def _validate_story_complexity(self,
                                       story_breakdown: Dict[str, Any],
                                       acceptance_criteria: List[str],
                                       story_data: Dict[str, Any]) -> StoryComplexityResult:
        """
        Validate story complexity for Time Respect principle.
        
        Analyzes story complexity to ensure features can be completed
        within 10 minutes by municipal end users.
        """
        try:
            # Analyze acceptance criteria complexity
            criteria_count = len(acceptance_criteria)
            
            # Estimate completion time based on complexity factors
            base_time = 3.0  # Base 3 minutes for any feature
            criteria_time = criteria_count * 1.5  # 1.5 minutes per criterion
            
            # Technical complexity factor
            technical_complexity = story_breakdown.get("complexity_assessment", {}).get("technical_complexity", 2)
            ux_complexity = story_breakdown.get("complexity_assessment", {}).get("ux_complexity", 2)
            integration_complexity = story_breakdown.get("complexity_assessment", {}).get("integration_complexity", 2)
            
            complexity_multiplier = (technical_complexity + ux_complexity + integration_complexity) / 9.0  # Normalized
            
            estimated_completion_time = (base_time + criteria_time) * (1 + complexity_multiplier)
            
            # Determine complexity level
            if estimated_completion_time <= 5.0:
                complexity_level = StoryComplexityLevel.EXCELLENT
            elif estimated_completion_time <= 7.0:
                complexity_level = StoryComplexityLevel.GOOD
            elif estimated_completion_time <= 10.0:
                complexity_level = StoryComplexityLevel.ACCEPTABLE
            elif estimated_completion_time <= 15.0:
                complexity_level = StoryComplexityLevel.COMPLEX
            else:
                complexity_level = StoryComplexityLevel.EXCESSIVE
            
            # Identify violations
            violations = []
            if estimated_completion_time > self.story_complexity_thresholds["max_completion_time_minutes"]:
                violations.append(f"Estimated completion time {estimated_completion_time:.1f} minutes exceeds 10 minute limit")
            
            if criteria_count > self.story_complexity_thresholds["max_acceptance_criteria"]:
                violations.append(f"Too many acceptance criteria: {criteria_count} > {self.story_complexity_thresholds['max_acceptance_criteria']}")
            
            if technical_complexity > self.story_complexity_thresholds["max_technical_complexity"]:
                violations.append(f"Technical complexity too high: {technical_complexity}")
            
            # Generate simplification recommendations
            recommendations = []
            if complexity_level in [StoryComplexityLevel.COMPLEX, StoryComplexityLevel.EXCESSIVE]:
                recommendations.append("Break story into smaller, simpler sub-features")
                recommendations.append("Reduce technical complexity by using existing components")
                recommendations.append("Simplify user interaction patterns")
                
            if criteria_count > 3:
                recommendations.append("Reduce acceptance criteria to 3 or fewer essential requirements")
            
            return StoryComplexityResult(
                complexity_level=complexity_level,
                estimated_completion_time_minutes=estimated_completion_time,
                acceptance_criteria_count=criteria_count,
                technical_complexity_score=float(technical_complexity),
                ux_complexity_score=float(ux_complexity),
                integration_complexity_score=float(integration_complexity),
                complexity_violations=violations,
                simplification_recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Story complexity validation failed: {e}")
            raise
    
    async def _validate_learning_effectiveness(self,
                                             learning_objectives: List[str],
                                             story_breakdown: Dict[str, Any],
                                             story_data: Dict[str, Any]) -> LearningEffectivenessResult:
        """
        Validate learning effectiveness for Pedagogical Value principle.
        
        Analyzes learning objectives and pedagogical approach to ensure
        effective knowledge transfer for municipal professionals.
        """
        try:
            # Analyze learning objectives quality
            objectives_count = len(learning_objectives)
            
            # Check learning objective quality
            learning_objectives_quality = {}
            for objective in learning_objectives:
                # Check if objective is specific and measurable
                is_specific = len(objective.split()) >= 5  # At least 5 words
                is_measurable = any(word in objective.lower() for word in ["kan", "ska", "förstå", "använda", "tillämpa"])
                learning_objectives_quality[objective] = is_specific and is_measurable
            
            objectives_quality_score = sum(learning_objectives_quality.values()) / len(learning_objectives_quality) if learning_objectives_quality else 0.0
            
            # Municipal relevance analysis
            municipal_context = story_data.get("municipal_context", {})
            municipal_keywords = ["kommun", "förvaltning", "policy", "service", "medarbetare"]
            municipal_relevance = sum(1 for keyword in municipal_keywords if keyword in str(municipal_context).lower()) / len(municipal_keywords)
            
            # Pedagogical approach assessment
            pedagogical_approach = story_breakdown.get("pedagogical_approach", "")
            pedagogical_approaches = ["storytelling", "problem-solving", "practice", "simulation", "gamification"]
            pedagogical_approach_suitable = any(approach in pedagogical_approach.lower() for approach in pedagogical_approaches)
            
            # Knowledge transfer potential
            complexity = story_breakdown.get("complexity_assessment", {}).get("ux_complexity", 3)
            knowledge_transfer_potential = max(1.0, 6.0 - complexity)  # Simpler = better transfer
            
            # Calculate overall learning effectiveness score
            effectiveness_factors = {
                "objectives_quality": objectives_quality_score * 2.0,  # Max 2 points
                "municipal_relevance": municipal_relevance * 1.5,      # Max 1.5 points
                "pedagogical_approach": 1.0 if pedagogical_approach_suitable else 0.0,
                "knowledge_transfer": min(knowledge_transfer_potential / 5.0, 0.5)  # Max 0.5 points
            }
            
            learning_effectiveness_score = sum(effectiveness_factors.values())
            
            # Determine effectiveness level
            if learning_effectiveness_score >= 4.5:
                effectiveness_level = LearningEffectivenessLevel.EXCELLENT
            elif learning_effectiveness_score >= 3.5:
                effectiveness_level = LearningEffectivenessLevel.GOOD
            elif learning_effectiveness_score >= 2.5:
                effectiveness_level = LearningEffectivenessLevel.ACCEPTABLE
            elif learning_effectiveness_score >= 1.5:
                effectiveness_level = LearningEffectivenessLevel.POOR
            else:
                effectiveness_level = LearningEffectivenessLevel.INADEQUATE
            
            # Identify violations
            violations = []
            if objectives_count < self.learning_effectiveness_criteria["min_learning_objectives"]:
                violations.append(f"Too few learning objectives: {objectives_count} < {self.learning_effectiveness_criteria['min_learning_objectives']}")
            
            if municipal_relevance < 0.6:
                violations.append(f"Insufficient municipal relevance: {municipal_relevance:.1%}")
            
            if not pedagogical_approach_suitable:
                violations.append("No suitable pedagogical approach identified")
            
            # Generate improvement recommendations
            recommendations = []
            if objectives_quality_score < 0.8:
                recommendations.append("Improve learning objectives specificity and measurability")
            
            if municipal_relevance < 0.8:
                recommendations.append("Strengthen municipal context and policy alignment")
            
            if not pedagogical_approach_suitable:
                recommendations.append("Define clear pedagogical approach (storytelling, problem-solving, etc.)")
            
            if learning_effectiveness_score < 3.0:
                recommendations.append("Add more specific learning outcomes for municipal professionals")
            
            return LearningEffectivenessResult(
                effectiveness_level=effectiveness_level,
                learning_effectiveness_score=learning_effectiveness_score,
                learning_objectives_quality=learning_objectives_quality,
                pedagogical_approach_suitable=pedagogical_approach_suitable,
                municipal_relevance_score=municipal_relevance * 5.0,
                knowledge_transfer_potential=knowledge_transfer_potential,
                effectiveness_violations=violations,
                learning_improvement_recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Learning effectiveness validation failed: {e}")
            raise
    
    async def _validate_communication_quality(self,
                                            story_breakdown: Dict[str, Any],
                                            acceptance_criteria: List[str],
                                            learning_objectives: List[str]) -> CommunicationQualityResult:
        """
        Validate communication quality for Professional Tone principle.
        
        Analyzes story breakdown language and communication style for
        appropriate Swedish municipal professional standards.
        """
        try:
            # Collect all text for analysis
            all_text = []
            all_text.append(story_breakdown.get("story_description", ""))
            all_text.extend(acceptance_criteria)
            all_text.extend(learning_objectives)
            all_text.append(story_breakdown.get("municipal_context", {}).get("use_case_scenario", ""))
            
            combined_text = " ".join(all_text).lower()
            
            # Analyze Swedish municipal terminology usage
            municipal_terminology_present = {}
            for term in self.communication_standards["required_swedish_municipal_terms"]:
                count = combined_text.count(term)
                municipal_terminology_present[term] = count
            
            total_municipal_terms = sum(municipal_terminology_present.values())
            
            # Check for casual/unprofessional language
            casual_violations = []
            for casual_term in self.communication_standards["forbidden_casual_terms"]:
                if casual_term in combined_text:
                    casual_violations.append(f"Casual term '{casual_term}' found in story breakdown")
            
            # Assess tone consistency
            professional_indicators = ["ska", "måste", "krävs", "säkerställa", "validera", "implementera"]
            professional_term_count = sum(1 for term in professional_indicators if term in combined_text)
            tone_consistency = professional_term_count >= 3  # At least 3 professional terms
            
            # Stakeholder appropriateness assessment
            stakeholder_context = story_breakdown.get("user_personas", [])
            stakeholder_appropriateness = "anna" in str(stakeholder_context).lower() or "municipal" in combined_text
            
            # Calculate professional score (1-5 scale)
            professional_factors = {
                "municipal_terminology": min(total_municipal_terms / 5.0, 2.0),  # Max 2 points
                "no_casual_language": 1.5 if not casual_violations else 0.0,
                "tone_consistency": 1.0 if tone_consistency else 0.0,
                "stakeholder_appropriateness": 0.5 if stakeholder_appropriateness else 0.0
            }
            
            professional_score = sum(professional_factors.values())
            
            # Determine communication quality
            if professional_score >= 4.5:
                communication_quality = CommunicationQuality.EXCELLENT
            elif professional_score >= 3.5:
                communication_quality = CommunicationQuality.GOOD
            elif professional_score >= 2.5:
                communication_quality = CommunicationQuality.ACCEPTABLE
            elif professional_score >= 1.5:
                communication_quality = CommunicationQuality.UNCLEAR
            else:
                communication_quality = CommunicationQuality.UNPROFESSIONAL
            
            # Identify violations
            violations = []
            if professional_score < self.communication_standards["min_professional_score"]:
                violations.append(f"Professional score {professional_score:.1f} below minimum {self.communication_standards['min_professional_score']}")
            
            if total_municipal_terms < 3:
                violations.append(f"Insufficient Swedish municipal terminology: only {total_municipal_terms} terms used")
            
            violations.extend(casual_violations)
            
            if not tone_consistency:
                violations.append("Inconsistent professional tone")
            
            # Generate improvement recommendations
            recommendations = []
            if total_municipal_terms < 5:
                recommendations.append("Use more Swedish municipal terminology (kommun, förvaltning, policy, etc.)")
            
            if casual_violations:
                recommendations.append("Replace casual language with professional municipal terminology")
            
            if not tone_consistency:
                recommendations.append("Maintain consistent professional tone throughout story breakdown")
            
            if not stakeholder_appropriateness:
                recommendations.append("Ensure story clearly addresses municipal stakeholder needs")
            
            return CommunicationQualityResult(
                communication_quality=communication_quality,
                professional_score=professional_score,
                swedish_municipal_terminology_present=municipal_terminology_present,
                tone_consistency=tone_consistency,
                stakeholder_appropriateness=stakeholder_appropriateness,
                communication_violations=violations,
                communication_improvement_recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Communication quality validation failed: {e}")
            raise
    
    async def _validate_policy_to_practice_alignment(self, 
                                                   story_data: Dict[str, Any], 
                                                   story_breakdown: Dict[str, Any]) -> bool:
        """Validate policy to practice alignment."""
        municipal_context = story_breakdown.get("municipal_context", {})
        policy_alignment = municipal_context.get("policy_alignment", "")
        
        # Check if story connects policy to practical implementation
        policy_keywords = ["policy", "riktlinje", "föreskrift", "regel", "krav"]
        practice_keywords = ["använda", "tillämpa", "implementera", "utföra", "praktik"]
        
        has_policy = any(keyword in policy_alignment.lower() for keyword in policy_keywords)
        has_practice = any(keyword in policy_alignment.lower() for keyword in practice_keywords)
        
        return has_policy and has_practice
    
    async def _validate_holistic_thinking(self, 
                                        story_breakdown: Dict[str, Any], 
                                        story_data: Dict[str, Any]) -> bool:
        """Validate holistic thinking in story analysis."""
        # Check if story considers broader context
        context_indicators = [
            story_breakdown.get("dependencies", []),
            story_breakdown.get("related_stories", []),
            story_breakdown.get("risk_factors", []),
            story_breakdown.get("municipal_context", {}).get("integration_concerns", "")
        ]
        
        # Story shows holistic thinking if it identifies dependencies, risks, or integration concerns
        return any(bool(indicator) for indicator in context_indicators)
    
    def _complexity_to_score(self, complexity: StoryComplexityLevel) -> float:
        """Convert complexity level to numeric score (1-5)."""
        complexity_scores = {
            StoryComplexityLevel.EXCELLENT: 5.0,
            StoryComplexityLevel.GOOD: 4.0,
            StoryComplexityLevel.ACCEPTABLE: 3.0,
            StoryComplexityLevel.COMPLEX: 2.0,
            StoryComplexityLevel.EXCESSIVE: 1.0
        }
        return complexity_scores.get(complexity, 3.0)