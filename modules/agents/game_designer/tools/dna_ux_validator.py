"""
DNA UX Validator - Active DNA validation for Game Designer agent.

PURPOSE:
Implements active DNA compliance validation for UX design decisions,
ensuring Game Designer output meets DigiNativa DNA principles.

CRITICAL FUNCTIONALITY:
- Time Respect → UI complexity analysis (cognitive load measurement)
- Pedagogical Value → Learning flow validation and educational assessment  
- Professional Tone → UI text analysis and tone consistency

ADAPTATION GUIDE:
To adapt for your project:
1. Update ui_complexity_thresholds for your complexity standards
2. Modify learning_flow_patterns for your pedagogical approach
3. Adjust professional_tone_indicators for your brand voice
4. Update validation_criteria for your quality standards

CONTRACT PROTECTION:
This tool enhances Game Designer DNA validation without breaking contracts.
All outputs integrate seamlessly with existing UX validation results.
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


class ComplexityLevel(Enum):
    """UI complexity levels for time respect validation."""
    MINIMAL = "minimal"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EXCESSIVE = "excessive"


class LearningFlowQuality(Enum):
    """Learning flow quality levels for pedagogical value."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    INADEQUATE = "inadequate"


class ToneConsistency(Enum):
    """Professional tone consistency levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    INCONSISTENT = "inconsistent"
    UNPROFESSIONAL = "unprofessional"


@dataclass
class UIComplexityResult:
    """Result from UI complexity analysis."""
    complexity_level: ComplexityLevel
    cognitive_load_score: float  # 1-10 scale
    ui_elements_count: int
    interaction_steps_count: int
    navigation_depth: int
    completion_time_estimate_minutes: float
    complexity_violations: List[str]
    recommendations: List[str]


@dataclass
class LearningFlowResult:
    """Result from learning flow validation."""
    flow_quality: LearningFlowQuality
    pedagogical_effectiveness_score: float  # 1-5 scale
    learning_objectives_coverage: Dict[str, bool]
    flow_progression_logical: bool
    assessment_opportunities_count: int
    engagement_elements_count: int
    learning_violations: List[str]
    recommendations: List[str]


@dataclass
class ProfessionalToneResult:
    """Result from professional tone analysis."""
    tone_consistency: ToneConsistency
    professional_score: float  # 1-5 scale
    municipal_terminology_usage: Dict[str, int]
    language_complexity_appropriate: bool
    tone_violations: List[str]
    text_elements_analyzed: int
    recommendations: List[str]


@dataclass
class DNAUXValidationResult:
    """Complete DNA UX validation result."""
    overall_dna_compliant: bool
    time_respect_compliant: bool
    pedagogical_value_compliant: bool
    professional_tone_compliant: bool
    ui_complexity_result: UIComplexityResult
    learning_flow_result: LearningFlowResult
    professional_tone_result: ProfessionalToneResult
    validation_timestamp: str
    dna_compliance_score: float  # 1-5 scale


class DNAUXValidator:
    """
    Active DNA validation for Game Designer UX decisions.
    
    Validates UX designs against DigiNativa DNA principles:
    - Time Respect: UI complexity analysis for efficient task completion
    - Pedagogical Value: Learning flow validation and educational effectiveness
    - Professional Tone: UI text analysis for municipal appropriateness
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DNA UX Validator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Time Respect validation thresholds
        self.ui_complexity_thresholds = {
            "max_cognitive_load_score": 6.0,  # 1-10 scale
            "max_ui_elements_per_screen": 8,
            "max_interaction_steps": 5,
            "max_navigation_depth": 3,
            "max_completion_time_minutes": 10.0
        }
        
        # Pedagogical Value validation criteria
        self.learning_flow_criteria = {
            "min_pedagogical_effectiveness": 4.0,  # 1-5 scale
            "min_learning_objectives_coverage": 0.8,  # 80%
            "min_assessment_opportunities": 2,
            "min_engagement_elements": 3
        }
        
        # Professional Tone validation standards
        self.professional_tone_standards = {
            "min_professional_score": 4.0,  # 1-5 scale
            "required_municipal_terminology": [
                "kommun", "förvaltning", "policy", "riktlinje", "process",
                "effektivitet", "kvalitet", "service", "medborgare", "verksamhet"
            ],
            "max_language_complexity_grade": 8,  # Reading grade level
            "forbidden_informal_terms": [
                "typ", "liksom", "bara", "kanske", "ungefär", "lite grann"
            ]
        }
        
        logger.info("DNA UX Validator initialized with municipal focus")
    
    async def validate_ux_dna_compliance(self,
                                       game_mechanics: Dict[str, Any],
                                       ui_components: List[Dict[str, Any]],
                                       interaction_flows: List[Dict[str, Any]],
                                       story_data: Dict[str, Any]) -> DNAUXValidationResult:
        """
        Comprehensive DNA validation for UX design.
        
        Args:
            game_mechanics: Game mechanics specifications
            ui_components: UI component specifications
            interaction_flows: User interaction flows
            story_data: Original story requirements
            
        Returns:
            Complete DNA UX validation result
        """
        try:
            logger.info("Starting comprehensive DNA UX validation")
            
            # Validate Time Respect (UI complexity analysis)
            ui_complexity_result = await self._validate_ui_complexity(
                ui_components, interaction_flows, story_data
            )
            
            # Validate Pedagogical Value (learning flow analysis)
            learning_flow_result = await self._validate_learning_flows(
                game_mechanics, interaction_flows, story_data
            )
            
            # Validate Professional Tone (UI text analysis)
            professional_tone_result = await self._validate_professional_tone(
                ui_components, interaction_flows, story_data
            )
            
            # Calculate overall DNA compliance
            time_respect_compliant = ui_complexity_result.complexity_level in [
                ComplexityLevel.MINIMAL, ComplexityLevel.LOW, ComplexityLevel.MODERATE
            ]
            
            pedagogical_value_compliant = learning_flow_result.flow_quality in [
                LearningFlowQuality.EXCELLENT, LearningFlowQuality.GOOD, LearningFlowQuality.ACCEPTABLE
            ]
            
            professional_tone_compliant = professional_tone_result.tone_consistency in [
                ToneConsistency.EXCELLENT, ToneConsistency.GOOD, ToneConsistency.ACCEPTABLE
            ]
            
            overall_dna_compliant = all([
                time_respect_compliant,
                pedagogical_value_compliant,
                professional_tone_compliant
            ])
            
            # Calculate overall DNA compliance score
            dna_compliance_score = (
                (ui_complexity_result.cognitive_load_score / 10.0 * 2) +  # Invert and scale to 2 points
                learning_flow_result.pedagogical_effectiveness_score +      # 5 points max
                professional_tone_result.professional_score                # 5 points max
            ) / 3.0  # Average to 1-5 scale
            
            validation_result = DNAUXValidationResult(
                overall_dna_compliant=overall_dna_compliant,
                time_respect_compliant=time_respect_compliant,
                pedagogical_value_compliant=pedagogical_value_compliant,
                professional_tone_compliant=professional_tone_compliant,
                ui_complexity_result=ui_complexity_result,
                learning_flow_result=learning_flow_result,
                professional_tone_result=professional_tone_result,
                validation_timestamp=datetime.now().isoformat(),
                dna_compliance_score=dna_compliance_score
            )
            
            logger.info(f"DNA UX validation completed: {dna_compliance_score:.2f}/5.0 score")
            return validation_result
            
        except Exception as e:
            logger.error(f"DNA UX validation failed: {e}")
            raise
    
    async def _validate_ui_complexity(self,
                                    ui_components: List[Dict[str, Any]],
                                    interaction_flows: List[Dict[str, Any]],
                                    story_data: Dict[str, Any]) -> UIComplexityResult:
        """
        Validate UI complexity for Time Respect principle.
        
        Analyzes cognitive load, interaction complexity, and completion time
        to ensure 10-minute task completion constraint is respected.
        """
        try:
            # Count UI elements across all components
            total_ui_elements = 0
            for component in ui_components:
                elements = component.get("elements", [])
                total_ui_elements += len(elements)
                
                # Add nested elements
                for element in elements:
                    if "children" in element:
                        total_ui_elements += len(element["children"])
            
            # Count interaction steps across all flows
            total_interaction_steps = 0
            max_navigation_depth = 0
            
            for flow in interaction_flows:
                user_actions = flow.get("user_actions", [])
                total_interaction_steps += len(user_actions)
                
                # Calculate navigation depth
                navigation_depth = flow.get("navigation_depth", 0)
                max_navigation_depth = max(max_navigation_depth, navigation_depth)
            
            # Calculate cognitive load score (1-10 scale, lower is better)
            cognitive_load_factors = {
                "ui_elements_factor": min(total_ui_elements / 5.0, 3.0),  # Max 3 points
                "interaction_steps_factor": min(total_interaction_steps / 3.0, 2.5),  # Max 2.5 points
                "navigation_depth_factor": min(max_navigation_depth / 2.0, 2.0),  # Max 2 points
                "feature_complexity_factor": self._assess_feature_complexity(story_data) / 2.0  # Max 2.5 points
            }
            
            cognitive_load_score = sum(cognitive_load_factors.values())
            
            # Estimate completion time based on complexity
            base_time = story_data.get("time_constraint_minutes", 10)
            complexity_multiplier = 1.0 + (cognitive_load_score - 5.0) / 10.0  # Scale around baseline
            completion_time_estimate = base_time * complexity_multiplier
            
            # Determine complexity level
            if cognitive_load_score <= 3.0:
                complexity_level = ComplexityLevel.MINIMAL
            elif cognitive_load_score <= 5.0:
                complexity_level = ComplexityLevel.LOW
            elif cognitive_load_score <= 7.0:
                complexity_level = ComplexityLevel.MODERATE
            elif cognitive_load_score <= 9.0:
                complexity_level = ComplexityLevel.HIGH
            else:
                complexity_level = ComplexityLevel.EXCESSIVE
            
            # Identify violations
            violations = []
            if total_ui_elements > self.ui_complexity_thresholds["max_ui_elements_per_screen"]:
                violations.append(f"Too many UI elements: {total_ui_elements} > {self.ui_complexity_thresholds['max_ui_elements_per_screen']}")
            
            if total_interaction_steps > self.ui_complexity_thresholds["max_interaction_steps"]:
                violations.append(f"Too many interaction steps: {total_interaction_steps} > {self.ui_complexity_thresholds['max_interaction_steps']}")
            
            if max_navigation_depth > self.ui_complexity_thresholds["max_navigation_depth"]:
                violations.append(f"Navigation too deep: {max_navigation_depth} > {self.ui_complexity_thresholds['max_navigation_depth']}")
            
            if completion_time_estimate > self.ui_complexity_thresholds["max_completion_time_minutes"]:
                violations.append(f"Estimated completion time too long: {completion_time_estimate:.1f} > {self.ui_complexity_thresholds['max_completion_time_minutes']} minutes")
            
            # Generate recommendations
            recommendations = []
            if complexity_level in [ComplexityLevel.HIGH, ComplexityLevel.EXCESSIVE]:
                recommendations.append("Simplify UI by grouping related elements")
                recommendations.append("Reduce number of interaction steps through progressive disclosure")
                recommendations.append("Consider splitting complex tasks into smaller sub-tasks")
            
            if total_ui_elements > 6:
                recommendations.append("Use tabs or accordion patterns to reduce visual complexity")
            
            if max_navigation_depth > 2:
                recommendations.append("Flatten navigation hierarchy for faster task completion")
            
            return UIComplexityResult(
                complexity_level=complexity_level,
                cognitive_load_score=cognitive_load_score,
                ui_elements_count=total_ui_elements,
                interaction_steps_count=total_interaction_steps,
                navigation_depth=max_navigation_depth,
                completion_time_estimate_minutes=completion_time_estimate,
                complexity_violations=violations,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"UI complexity validation failed: {e}")
            raise
    
    async def _validate_learning_flows(self,
                                     game_mechanics: Dict[str, Any],
                                     interaction_flows: List[Dict[str, Any]],
                                     story_data: Dict[str, Any]) -> LearningFlowResult:
        """
        Validate learning flows for Pedagogical Value principle.
        
        Analyzes learning progression, objective coverage, and educational
        effectiveness to ensure pedagogical value is maximized.
        """
        try:
            # Analyze learning objectives coverage (enhanced)
            story_learning_objectives = story_data.get("learning_objectives", [])
            
            # Check enhanced coverage data first
            if "learning_objectives_coverage" in game_mechanics:
                objectives_coverage = game_mechanics["learning_objectives_coverage"]
                coverage_percentage = sum(objectives_coverage.values()) / len(objectives_coverage) if objectives_coverage else 0.0
            else:
                # Fallback to traditional matching
                game_learning_objectives = game_mechanics.get("learning_objectives_addressed", [])
                
                objectives_coverage = {}
                for objective in story_learning_objectives:
                    objective_covered = any(
                        objective.lower() in game_obj.lower() 
                        for game_obj in game_learning_objectives
                    )
                    objectives_coverage[objective] = objective_covered
                
                coverage_percentage = sum(objectives_coverage.values()) / len(story_learning_objectives) if story_learning_objectives else 0.0
            
            # Count assessment opportunities (enhanced to check both sources)
            assessment_count = 0
            
            # Check game_mechanics for assessment_opportunities (enhanced data)
            if "assessment_opportunities" in game_mechanics:
                assessment_count += len(game_mechanics["assessment_opportunities"])
            
            # Also check interaction flows as fallback
            for flow in interaction_flows:
                flow_actions = flow.get("user_actions", [])
                for action in flow_actions:
                    if any(keyword in action.get("description", "").lower() 
                          for keyword in ["test", "quiz", "validation", "check", "assess", "evaluate"]):
                        assessment_count += 1
            
            # Count engagement elements (enhanced to check both sources)
            engagement_count = 0
            
            # Check game_mechanics for engagement_elements (enhanced data)
            if "engagement_elements" in game_mechanics:
                engagement_count += len(game_mechanics["engagement_elements"])
            
            # Also check mechanics as fallback
            mechanics_list = game_mechanics.get("mechanics", [])
            for mechanic in mechanics_list:
                if mechanic.get("engagement_type") in ["interactive", "gamified", "collaborative"]:
                    engagement_count += 1
            
            # Check flow progression logic (enhanced to use learning_flow_progression)
            flow_progression_logical = True
            
            # Check enhanced flow progression data first
            if "learning_flow_progression" in game_mechanics:
                flow_data = game_mechanics["learning_flow_progression"]
                flow_progression_logical = flow_data.get("flow_quality") == "logical_and_coherent"
            else:
                # Fallback to analyzing interaction flows
                for flow in interaction_flows:
                    steps = flow.get("user_actions", [])
                    if len(steps) < 2:  # Need at least start and end
                        flow_progression_logical = False
                        break
                    
                    # Check for logical learning progression (introduction → practice → assessment)
                    has_introduction = any("intro" in step.get("description", "").lower() for step in steps)
                    has_practice = any("practice" in step.get("description", "").lower() for step in steps)
                    
                    if not (has_introduction or has_practice):
                        flow_progression_logical = False
            
            # Calculate pedagogical effectiveness score (1-5 scale)
            effectiveness_factors = {
                "objectives_coverage": coverage_percentage * 1.5,  # Max 1.5 points
                "assessment_quality": min(assessment_count / 2.0, 1.0),  # Max 1 point
                "engagement_level": min(engagement_count / 3.0, 1.0),  # Max 1 point
                "flow_logic": 1.5 if flow_progression_logical else 0.0  # Max 1.5 points
            }
            
            pedagogical_effectiveness_score = sum(effectiveness_factors.values())
            
            # Determine flow quality
            if pedagogical_effectiveness_score >= 4.5:
                flow_quality = LearningFlowQuality.EXCELLENT
            elif pedagogical_effectiveness_score >= 3.5:
                flow_quality = LearningFlowQuality.GOOD
            elif pedagogical_effectiveness_score >= 2.5:
                flow_quality = LearningFlowQuality.ACCEPTABLE
            elif pedagogical_effectiveness_score >= 1.5:
                flow_quality = LearningFlowQuality.POOR
            else:
                flow_quality = LearningFlowQuality.INADEQUATE
            
            # Identify violations
            violations = []
            if coverage_percentage < self.learning_flow_criteria["min_learning_objectives_coverage"]:
                violations.append(f"Insufficient learning objectives coverage: {coverage_percentage:.0%} < {self.learning_flow_criteria['min_learning_objectives_coverage']:.0%}")
            
            if assessment_count < self.learning_flow_criteria["min_assessment_opportunities"]:
                violations.append(f"Insufficient assessment opportunities: {assessment_count} < {self.learning_flow_criteria['min_assessment_opportunities']}")
            
            if engagement_count < self.learning_flow_criteria["min_engagement_elements"]:
                violations.append(f"Insufficient engagement elements: {engagement_count} < {self.learning_flow_criteria['min_engagement_elements']}")
            
            if not flow_progression_logical:
                violations.append("Learning flow progression is not logical")
            
            # Generate recommendations
            recommendations = []
            if coverage_percentage < 0.8:
                recommendations.append("Add game mechanics that directly address uncovered learning objectives")
            
            if assessment_count < 2:
                recommendations.append("Include more assessment opportunities throughout the learning flow")
            
            if engagement_count < 3:
                recommendations.append("Add interactive or gamified elements to increase engagement")
            
            if not flow_progression_logical:
                recommendations.append("Restructure learning flow: Introduction → Explanation → Practice → Assessment")
            
            return LearningFlowResult(
                flow_quality=flow_quality,
                pedagogical_effectiveness_score=pedagogical_effectiveness_score,
                learning_objectives_coverage=objectives_coverage,
                flow_progression_logical=flow_progression_logical,
                assessment_opportunities_count=assessment_count,
                engagement_elements_count=engagement_count,
                learning_violations=violations,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Learning flow validation failed: {e}")
            raise
    
    async def _validate_professional_tone(self,
                                        ui_components: List[Dict[str, Any]],
                                        interaction_flows: List[Dict[str, Any]],
                                        story_data: Dict[str, Any]) -> ProfessionalToneResult:
        """
        Validate professional tone for Professional Tone principle.
        
        Analyzes UI text content for municipal appropriateness, professional
        language usage, and tone consistency.
        """
        try:
            # Collect all text content from UI components and flows
            all_text_content = []
            
            # Extract text from UI components
            for component in ui_components:
                elements = component.get("elements", [])
                for element in elements:
                    if "text" in element:
                        all_text_content.append(element["text"])
                    if "label" in element:
                        all_text_content.append(element["label"])
                    if "description" in element:
                        all_text_content.append(element["description"])
            
            # Extract text from interaction flows
            for flow in interaction_flows:
                user_actions = flow.get("user_actions", [])
                for action in user_actions:
                    if "description" in action:
                        all_text_content.append(action["description"])
                    if "feedback_text" in action:
                        all_text_content.append(action["feedback_text"])
            
            text_elements_analyzed = len(all_text_content)
            
            # Analyze municipal terminology usage
            municipal_terminology_usage = {}
            for term in self.professional_tone_standards["required_municipal_terminology"]:
                count = sum(text.lower().count(term) for text in all_text_content)
                municipal_terminology_usage[term] = count
            
            total_municipal_terms = sum(municipal_terminology_usage.values())
            
            # Check for forbidden informal terms
            informal_violations = []
            for text in all_text_content:
                for forbidden_term in self.professional_tone_standards["forbidden_informal_terms"]:
                    if forbidden_term in text.lower():
                        informal_violations.append(f"Informal term '{forbidden_term}' found in: '{text[:50]}...'")
            
            # Assess language complexity (simplified reading grade estimation)
            total_words = 0
            total_sentences = 0
            total_syllables = 0
            
            for text in all_text_content:
                words = text.split()
                sentences = text.split('.')
                
                total_words += len(words)
                total_sentences += len(sentences)
                
                # Simple syllable estimation (vowel groups)
                for word in words:
                    syllable_count = max(1, len(re.findall(r'[aeiouyåäö]+', word.lower())))
                    total_syllables += syllable_count
            
            if total_sentences > 0 and total_words > 0:
                avg_sentence_length = total_words / total_sentences
                avg_syllables_per_word = total_syllables / total_words
                # Simplified reading grade (Flesch-style approximation)
                reading_grade = 1.015 * avg_sentence_length + 84.6 * avg_syllables_per_word - 15.59
                language_complexity_appropriate = reading_grade <= self.professional_tone_standards["max_language_complexity_grade"]
            else:
                reading_grade = 0
                language_complexity_appropriate = True
            
            # Calculate professional score (1-5 scale)
            professional_factors = {
                "municipal_terminology": min(total_municipal_terms / 5.0, 1.5),  # Max 1.5 points
                "no_informal_terms": 1.5 if not informal_violations else 0.0,  # Max 1.5 points
                "appropriate_complexity": 1.0 if language_complexity_appropriate else 0.0,  # Max 1 point
                "content_volume": min(text_elements_analyzed / 5.0, 1.0)  # Max 1 point
            }
            
            professional_score = sum(professional_factors.values())
            
            # Determine tone consistency
            if professional_score >= 4.5:
                tone_consistency = ToneConsistency.EXCELLENT
            elif professional_score >= 3.5:
                tone_consistency = ToneConsistency.GOOD
            elif professional_score >= 2.5:
                tone_consistency = ToneConsistency.ACCEPTABLE
            elif professional_score >= 1.5:
                tone_consistency = ToneConsistency.INCONSISTENT
            else:
                tone_consistency = ToneConsistency.UNPROFESSIONAL
            
            # Identify violations
            violations = []
            if total_municipal_terms < 3:
                violations.append(f"Insufficient municipal terminology usage: {total_municipal_terms} terms found")
            
            if informal_violations:
                violations.extend(informal_violations)
            
            if not language_complexity_appropriate:
                violations.append(f"Language too complex: Grade {reading_grade:.1f} > {self.professional_tone_standards['max_language_complexity_grade']}")
            
            # Generate recommendations
            recommendations = []
            if total_municipal_terms < 3:
                recommendations.append("Include more municipal-specific terminology in UI text")
            
            if informal_violations:
                recommendations.append("Replace informal language with professional municipal terminology")
            
            if not language_complexity_appropriate:
                recommendations.append("Simplify language for better accessibility and clarity")
            
            if text_elements_analyzed < 5:
                recommendations.append("Add more descriptive text to improve user guidance")
            
            return ProfessionalToneResult(
                tone_consistency=tone_consistency,
                professional_score=professional_score,
                municipal_terminology_usage=municipal_terminology_usage,
                language_complexity_appropriate=language_complexity_appropriate,
                tone_violations=violations,
                text_elements_analyzed=text_elements_analyzed,
                recommendations=recommendations
            )
            
        except Exception as e:
            logger.error(f"Professional tone validation failed: {e}")
            raise
    
    def _assess_feature_complexity(self, story_data: Dict[str, Any]) -> float:
        """
        Assess feature complexity for cognitive load calculation.
        
        Returns:
            Complexity score (1-5 scale)
        """
        try:
            complexity_indicators = {
                "acceptance_criteria_count": len(story_data.get("acceptance_criteria", [])),
                "learning_objectives_count": len(story_data.get("learning_objectives", [])),
                "has_integrations": bool(story_data.get("integration_requirements")),
                "has_custom_logic": bool(story_data.get("custom_business_logic")),
                "user_role_complexity": story_data.get("user_role_complexity", "simple")
            }
            
            # Calculate complexity score
            base_score = 1.0
            
            # More acceptance criteria = higher complexity
            if complexity_indicators["acceptance_criteria_count"] > 5:
                base_score += 1.0
            elif complexity_indicators["acceptance_criteria_count"] > 3:
                base_score += 0.5
            
            # More learning objectives = higher complexity  
            if complexity_indicators["learning_objectives_count"] > 3:
                base_score += 1.0
            elif complexity_indicators["learning_objectives_count"] > 1:
                base_score += 0.5
            
            # Integrations add complexity
            if complexity_indicators["has_integrations"]:
                base_score += 1.0
            
            # Custom logic adds complexity
            if complexity_indicators["has_custom_logic"]:
                base_score += 0.5
            
            # User role complexity
            role_complexity_map = {
                "simple": 0.0,
                "moderate": 0.5,
                "complex": 1.0,
                "very_complex": 1.5
            }
            base_score += role_complexity_map.get(complexity_indicators["user_role_complexity"], 0.0)
            
            return min(base_score, 5.0)  # Cap at 5.0
            
        except Exception as e:
            logger.error(f"Feature complexity assessment failed: {e}")
            return 2.5  # Default moderate complexity