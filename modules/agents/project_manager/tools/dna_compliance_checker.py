"""
DNA Compliance Checker for Project Manager Agent.

PURPOSE:
Validates all feature requests against DigiNativa's Project DNA principles
to ensure consistency and quality across all development work.

CRITICAL IMPORTANCE:
- Ensures all features align with DigiNativa's core values
- Prevents scope creep and feature drift
- Maintains consistent user experience
- Protects brand integrity and educational effectiveness

REVENUE IMPACT:
Direct impact on revenue through:
- Consistent quality leading to higher client satisfaction
- Reduced rework by catching misalignment early
- Brand protection maintaining premium positioning
- Educational effectiveness driving user retention
"""

import logging
import re
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from ....shared.exceptions import DNAComplianceError, BusinessLogicError


class DNAComplianceChecker:
    """
    DNA compliance validation tool for Project Manager Agent.
    
    Validates feature requests against DigiNativa's 5 design principles
    and 4 architecture principles to ensure system-wide consistency.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DNA Compliance Checker.
        
        Args:
            config: Configuration dictionary
        """
        self.logger = logging.getLogger(f"{__name__}.DNAComplianceChecker")
        self.config = config or {}
        
        # DigiNativa DNA Principles (from Implementation_rules.md)
        self.design_principles = self._initialize_design_principles()
        self.architecture_principles = self._initialize_architecture_principles()
        
        # Validation rules and patterns
        self.validation_rules = self._initialize_validation_rules()
        self.compliance_thresholds = self._initialize_compliance_thresholds()
        
        self.logger.info("DNA Compliance Checker initialized with DigiNativa principles")
    
    async def analyze_feature_compliance(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive DNA compliance analysis for a feature request.
        
        Args:
            feature_data: Feature request data to analyze
            
        Returns:
            Complete DNA compliance analysis
            
        Raises:
            DNAComplianceError: If feature fundamentally violates DNA principles
        """
        try:
            self.logger.debug("Starting DNA compliance analysis")
            
            # Validate each design principle
            design_analysis = await self._validate_design_principles(feature_data)
            
            # Validate architecture principles
            architecture_analysis = self._validate_architecture_principles(feature_data)
            
            # Calculate overall compliance score
            compliance_score = self._calculate_compliance_score(design_analysis, architecture_analysis)
            
            # Identify violations and recommendations
            violations = self._identify_violations(design_analysis, architecture_analysis)
            recommendations = self._generate_recommendations(violations, feature_data)
            
            # Determine if feature is compliant
            is_compliant = len(violations) == 0 and compliance_score >= self.compliance_thresholds["minimum_score"]
            
            analysis_result = {
                "compliant": is_compliant,
                "compliance_score": compliance_score,
                "design_principles_analysis": design_analysis,
                "architecture_principles_analysis": architecture_analysis,
                "violations": violations,
                "recommendations": recommendations,
                "analysis_timestamp": datetime.now().isoformat(),
                "analyzer_version": "1.0",
                
                # Individual principle results (for contract validation)
                "pedagogical_value": design_analysis["pedagogical_value"]["compliant"],
                "policy_to_practice": design_analysis["policy_to_practice"]["compliant"],
                "time_respect": design_analysis["time_respect"]["compliant"],
                "holistic_thinking": design_analysis["holistic_thinking"]["compliant"],
                "professional_tone": design_analysis["professional_tone"]["compliant"],
                
                "api_first": architecture_analysis["api_first"]["compliant"],
                "stateless_backend": architecture_analysis["stateless_backend"]["compliant"],
                "separation_of_concerns": architecture_analysis["separation_of_concerns"]["compliant"],
                "simplicity_first": architecture_analysis["simplicity_first"]["compliant"]
            }
            
            if not is_compliant:
                self.logger.warning(f"Feature failed DNA compliance: {len(violations)} violations")
            else:
                self.logger.debug(f"Feature passed DNA compliance with score: {compliance_score}")
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"DNA compliance analysis failed: {e}")
            raise DNAComplianceError(
                f"Failed to analyze DNA compliance: {e}",
                agent_type="project_manager"
            )
    
    async def _validate_design_principles(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate feature against DigiNativa's 5 design principles.
        
        Args:
            feature_data: Feature request data
            
        Returns:
            Design principles validation results
        """
        description = feature_data.get("feature_description", "").lower()
        learning_objectives = feature_data.get("learning_objectives", [])
        user_persona = feature_data.get("user_persona", "")
        time_constraint = feature_data.get("time_constraint_minutes", 10)
        
        analysis = {}
        
        # 1. Pedagogical Value
        analysis["pedagogical_value"] = self._validate_pedagogical_value(
            description, learning_objectives
        )
        
        # 2. Policy to Practice
        analysis["policy_to_practice"] = self._validate_policy_to_practice(
            description, learning_objectives
        )
        
        # 3. Time Respect
        analysis["time_respect"] = self._validate_time_respect(
            description, time_constraint
        )
        
        # 4. Holistic Thinking
        analysis["holistic_thinking"] = self._validate_holistic_thinking(
            description, feature_data
        )
        
        # 5. Professional Tone
        analysis["professional_tone"] = self._validate_professional_tone(
            description, user_persona
        )
        
        return analysis
    
    def _validate_architecture_principles(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate feature against DigiNativa's 4 architecture principles.
        
        Args:
            feature_data: Feature request data
            
        Returns:
            Architecture principles validation results
        """
        description = feature_data.get("feature_description", "").lower()
        
        analysis = {}
        
        # 1. API First
        analysis["api_first"] = self._validate_api_first(description)
        
        # 2. Stateless Backend
        analysis["stateless_backend"] = self._validate_stateless_backend(description)
        
        # 3. Separation of Concerns
        analysis["separation_of_concerns"] = self._validate_separation_of_concerns(description)
        
        # 4. Simplicity First
        analysis["simplicity_first"] = self._validate_simplicity_first(description, feature_data)
        
        return analysis
    
    def _validate_pedagogical_value(self, description: str, learning_objectives: List[str]) -> Dict[str, Any]:
        """Validate pedagogical value principle."""
        score = 0
        evidence = []
        issues = []
        
        # Check for learning-related keywords
        learning_keywords = [
            "learn", "education", "training", "skill", "knowledge", "competence",
            "objective", "goal", "assessment", "practice", "exercise", "tutorial"
        ]
        
        keyword_matches = sum(1 for keyword in learning_keywords if keyword in description)
        if keyword_matches >= 3:
            score += 30
            evidence.append(f"Contains {keyword_matches} learning-related terms")
        elif keyword_matches >= 1:
            score += 15
            evidence.append(f"Contains {keyword_matches} learning-related terms")
        else:
            issues.append("No clear learning-related terminology found")
        
        # Check for explicit learning objectives
        if learning_objectives and len(learning_objectives) > 0:
            score += 40
            evidence.append(f"Includes {len(learning_objectives)} explicit learning objectives")
        else:
            issues.append("No explicit learning objectives specified")
        
        # Check for assessment or evaluation mentions
        assessment_keywords = ["assessment", "evaluate", "test", "quiz", "feedback", "progress"]
        if any(keyword in description for keyword in assessment_keywords):
            score += 20
            evidence.append("Includes assessment or evaluation elements")
        
        # Check for practical application
        practice_keywords = ["apply", "practice", "implement", "use", "real-world", "scenario"]
        if any(keyword in description for keyword in practice_keywords):
            score += 10
            evidence.append("Includes practical application elements")
        
        return {
            "principle": "pedagogical_value",
            "score": min(score, 100),
            "compliant": score >= 60,
            "evidence": evidence,
            "issues": issues,
            "recommendation": self._get_pedagogical_recommendation(score, issues)
        }
    
    def _validate_policy_to_practice(self, description: str, learning_objectives: List[str]) -> Dict[str, Any]:
        """Validate policy to practice principle."""
        score = 0
        evidence = []
        issues = []
        
        # Check for policy/theory keywords
        policy_keywords = [
            "policy", "regulation", "law", "guideline", "standard", "principle",
            "theory", "concept", "framework", "methodology"
        ]
        
        policy_matches = sum(1 for keyword in policy_keywords if keyword in description)
        if policy_matches >= 2:
            score += 25
            evidence.append(f"References {policy_matches} policy/theory concepts")
        elif policy_matches >= 1:
            score += 15
            evidence.append(f"References {policy_matches} policy/theory concepts")
        
        # Check for practical application keywords
        practice_keywords = [
            "apply", "implement", "practice", "example", "case study", "scenario",
            "real-world", "workplace", "situation", "experience"
        ]
        
        practice_matches = sum(1 for keyword in practice_keywords if keyword in description)
        if practice_matches >= 2:
            score += 25
            evidence.append(f"Includes {practice_matches} practical application elements")
        elif practice_matches >= 1:
            score += 15
            evidence.append(f"Includes {practice_matches} practical application elements")
        
        # Check for bridging language
        bridge_keywords = [
            "connect", "link", "relate", "bridge", "transfer", "demonstrate",
            "show how", "illustrate", "exemplify"
        ]
        
        if any(keyword in description for keyword in bridge_keywords):
            score += 30
            evidence.append("Includes language that bridges theory and practice")
        
        # Check learning objectives for policy-practice connection
        objectives_text = " ".join(learning_objectives).lower()
        if any(keyword in objectives_text for keyword in policy_keywords) and \
           any(keyword in objectives_text for keyword in practice_keywords):
            score += 20
            evidence.append("Learning objectives connect policy and practice")
        
        if score < 40:
            issues.append("Limited connection between policy/theory and practical application")
        
        return {
            "principle": "policy_to_practice",
            "score": min(score, 100),
            "compliant": score >= 50,
            "evidence": evidence,
            "issues": issues,
            "recommendation": self._get_policy_practice_recommendation(score, issues)
        }
    
    def _validate_time_respect(self, description: str, time_constraint: int) -> Dict[str, Any]:
        """Validate time respect principle."""
        score = 0
        evidence = []
        issues = []
        
        # Check time constraint value
        if time_constraint <= 10:
            score += 50
            evidence.append(f"Respects 10-minute constraint ({time_constraint} minutes)")
        elif time_constraint <= 15:
            score += 30
            evidence.append(f"Reasonable time constraint ({time_constraint} minutes)")
            issues.append("Time constraint exceeds recommended 10 minutes")
        else:
            score += 10
            issues.append(f"Time constraint too long ({time_constraint} minutes)")
        
        # Check for efficiency language
        efficiency_keywords = [
            "quick", "fast", "efficient", "streamlined", "concise", "brief",
            "focused", "direct", "immediate", "instant"
        ]
        
        efficiency_matches = sum(1 for keyword in efficiency_keywords if keyword in description)
        if efficiency_matches >= 2:
            score += 30
            evidence.append(f"Emphasizes efficiency ({efficiency_matches} related terms)")
        elif efficiency_matches >= 1:
            score += 15
            evidence.append(f"Mentions efficiency ({efficiency_matches} related terms)")
        
        # Check for time-awareness language
        time_keywords = [
            "time", "minute", "hour", "schedule", "deadline", "duration",
            "length", "period", "session"
        ]
        
        if any(keyword in description for keyword in time_keywords):
            score += 20
            evidence.append("Shows awareness of time constraints")
        
        return {
            "principle": "time_respect",
            "score": min(score, 100),
            "compliant": score >= 70,
            "evidence": evidence,
            "issues": issues,
            "recommendation": self._get_time_respect_recommendation(score, time_constraint)
        }
    
    def _validate_holistic_thinking(self, description: str, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate holistic thinking principle."""
        score = 0
        evidence = []
        issues = []
        
        # Check for systems thinking keywords
        systems_keywords = [
            "integrate", "connect", "relationship", "system", "holistic", "comprehensive",
            "overall", "complete", "whole", "entire", "context", "environment"
        ]
        
        systems_matches = sum(1 for keyword in systems_keywords if keyword in description)
        if systems_matches >= 3:
            score += 30
            evidence.append(f"Shows systems thinking ({systems_matches} related terms)")
        elif systems_matches >= 1:
            score += 15
            evidence.append(f"Some systems thinking ({systems_matches} related terms)")
        
        # Check for consideration of multiple perspectives
        perspective_keywords = [
            "perspective", "viewpoint", "stakeholder", "user", "audience", "participant",
            "various", "different", "multiple", "diverse"
        ]
        
        if any(keyword in description for keyword in perspective_keywords):
            score += 25
            evidence.append("Considers multiple perspectives")
        
        # Check for impact awareness
        impact_keywords = [
            "impact", "effect", "consequence", "result", "outcome", "influence",
            "affect", "change", "benefit", "value"
        ]
        
        impact_matches = sum(1 for keyword in impact_keywords if keyword in description)
        if impact_matches >= 2:
            score += 25
            evidence.append(f"Shows impact awareness ({impact_matches} related terms)")
        elif impact_matches >= 1:
            score += 15
            evidence.append(f"Some impact awareness ({impact_matches} related terms)")
        
        # Check for broader context consideration
        if "organization" in description or "workplace" in description or "team" in description:
            score += 20
            evidence.append("Considers organizational context")
        
        # Check acceptance criteria for holistic elements
        acceptance_criteria = feature_data.get("acceptance_criteria", [])
        criteria_text = " ".join(acceptance_criteria).lower()
        if any(keyword in criteria_text for keyword in systems_keywords + perspective_keywords):
            score += 10
            evidence.append("Acceptance criteria include holistic elements")
        
        if score < 50:
            issues.append("Limited evidence of holistic thinking and systems perspective")
        
        return {
            "principle": "holistic_thinking",
            "score": min(score, 100),
            "compliant": score >= 60,
            "evidence": evidence,
            "issues": issues,
            "recommendation": self._get_holistic_thinking_recommendation(score, issues)
        }
    
    def _validate_professional_tone(self, description: str, user_persona: str) -> Dict[str, Any]:
        """Validate professional tone principle."""
        score = 0
        evidence = []
        issues = []
        
        # Check for professional language
        professional_indicators = [
            "professional", "workplace", "organization", "colleague", "team",
            "development", "growth", "improvement", "excellence", "quality"
        ]
        
        prof_matches = sum(1 for indicator in professional_indicators if indicator in description)
        if prof_matches >= 3:
            score += 30
            evidence.append(f"Uses professional terminology ({prof_matches} terms)")
        elif prof_matches >= 1:
            score += 20
            evidence.append(f"Some professional terminology ({prof_matches} terms)")
        
        # Check for appropriate complexity for Anna persona
        if user_persona.lower() == "anna":
            # Anna is a professional educator, so content should be sophisticated but accessible
            complex_words = len([word for word in description.split() if len(word) > 8])
            total_words = len(description.split())
            
            if total_words > 0:
                complexity_ratio = complex_words / total_words
                if 0.1 <= complexity_ratio <= 0.3:
                    score += 25
                    evidence.append("Appropriate complexity level for Anna persona")
                elif complexity_ratio > 0.3:
                    score += 10
                    issues.append("May be too complex for target audience")
                else:
                    score += 15
                    evidence.append("Simple language appropriate for accessibility")
        
        # Check for respectful and inclusive language
        inclusive_keywords = [
            "inclusive", "accessible", "diverse", "all users", "everyone",
            "participant", "learner", "individual"
        ]
        
        if any(keyword in description for keyword in inclusive_keywords):
            score += 20
            evidence.append("Uses inclusive language")
        
        # Check for educational/learning tone
        educational_tone = [
            "understand", "learn", "discover", "explore", "develop", "gain",
            "master", "practice", "improve", "enhance"
        ]
        
        edu_matches = sum(1 for keyword in educational_tone if keyword in description)
        if edu_matches >= 2:
            score += 25
            evidence.append(f"Maintains educational tone ({edu_matches} terms)")
        elif edu_matches >= 1:
            score += 15
            evidence.append(f"Some educational tone ({edu_matches} terms)")
        
        return {
            "principle": "professional_tone",
            "score": min(score, 100),
            "compliant": score >= 70,
            "evidence": evidence,
            "issues": issues,
            "recommendation": self._get_professional_tone_recommendation(score, issues)
        }
    
    def _validate_api_first(self, description: str) -> Dict[str, Any]:
        """Validate API first architecture principle."""
        score = 80  # Default score since this is architectural
        evidence = ["Feature will follow DigiNativa's API-first architecture"]
        issues = []
        
        # Check if feature mentions direct database access (red flag)
        database_direct = ["direct database", "database connection", "sql query", "orm direct"]
        if any(term in description for term in database_direct):
            score -= 30
            issues.append("Feature may bypass API layer")
        
        # Check for API-friendly language
        api_keywords = ["api", "endpoint", "service", "interface", "rest", "http"]
        if any(keyword in description for keyword in api_keywords):
            score += 20
            evidence.append("Explicitly mentions API components")
        
        return {
            "principle": "api_first",
            "score": min(score, 100),
            "compliant": score >= 70,
            "evidence": evidence,
            "issues": issues,
            "recommendation": "Ensure all data access goes through API layer"
        }
    
    def _validate_stateless_backend(self, description: str) -> Dict[str, Any]:
        """Validate stateless backend architecture principle."""
        score = 80  # Default score since this is architectural
        evidence = ["Feature will follow stateless backend design"]
        issues = []
        
        # Check for session-related language (red flag)
        session_keywords = ["session", "state", "memory", "cache", "store"]
        session_mentions = sum(1 for keyword in session_keywords if keyword in description)
        
        if session_mentions >= 2:
            score -= 20
            issues.append("Feature may require server-side state management")
        elif session_mentions == 1:
            score -= 10
            issues.append("Consider stateless alternatives for any state management")
        
        return {
            "principle": "stateless_backend",
            "score": min(score, 100),
            "compliant": score >= 70,
            "evidence": evidence,
            "issues": issues,
            "recommendation": "Ensure all state is managed client-side or via API parameters"
        }
    
    def _validate_separation_of_concerns(self, description: str) -> Dict[str, Any]:
        """Validate separation of concerns architecture principle."""
        score = 80  # Default score since this is architectural
        evidence = ["Feature will maintain separation between frontend and backend"]
        issues = []
        
        # Check for mixed concerns language
        mixed_keywords = ["frontend backend", "client server mixed", "monolithic"]
        if any(term in description for term in mixed_keywords):
            score -= 20
            issues.append("Feature may mix frontend and backend concerns")
        
        return {
            "principle": "separation_of_concerns",
            "score": min(score, 100),
            "compliant": score >= 70,
            "evidence": evidence,
            "issues": issues,
            "recommendation": "Keep frontend (React) and backend (FastAPI) completely separate"
        }
    
    def _validate_simplicity_first(self, description: str, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate simplicity first architecture principle."""
        score = 70  # Start with good score
        evidence = []
        issues = []
        
        # Check for simplicity language
        simplicity_keywords = [
            "simple", "easy", "straightforward", "minimal", "basic", "clean",
            "clear", "direct", "focused"
        ]
        
        simplicity_matches = sum(1 for keyword in simplicity_keywords if keyword in description)
        if simplicity_matches >= 2:
            score += 20
            evidence.append(f"Emphasizes simplicity ({simplicity_matches} terms)")
        elif simplicity_matches >= 1:
            score += 10
            evidence.append(f"Mentions simplicity ({simplicity_matches} terms)")
        
        # Check for complexity indicators (red flags)
        complexity_keywords = [
            "complex", "complicated", "advanced", "sophisticated", "elaborate",
            "intricate", "comprehensive", "extensive"
        ]
        
        complexity_matches = sum(1 for keyword in complexity_keywords if keyword in description)
        if complexity_matches >= 3:
            score -= 30
            issues.append(f"High complexity indicators ({complexity_matches} terms)")
        elif complexity_matches >= 1:
            score -= 10
            issues.append(f"Some complexity indicators ({complexity_matches} terms)")
        
        # Check acceptance criteria count (too many may indicate complexity)
        acceptance_criteria = feature_data.get("acceptance_criteria", [])
        if len(acceptance_criteria) > 10:
            score -= 15
            issues.append("Large number of acceptance criteria may indicate complexity")
        elif len(acceptance_criteria) <= 5:
            score += 10
            evidence.append("Focused set of acceptance criteria")
        
        return {
            "principle": "simplicity_first",
            "score": min(score, 100),
            "compliant": score >= 60,
            "evidence": evidence,
            "issues": issues,
            "recommendation": self._get_simplicity_recommendation(score, issues)
        }
    
    def _calculate_compliance_score(
        self,
        design_analysis: Dict[str, Any],
        architecture_analysis: Dict[str, Any]
    ) -> float:
        """Calculate overall compliance score."""
        # Weight design principles more heavily (60%) than architecture (40%)
        design_scores = [result["score"] for result in design_analysis.values()]
        architecture_scores = [result["score"] for result in architecture_analysis.values()]
        
        design_average = sum(design_scores) / len(design_scores) if design_scores else 0
        architecture_average = sum(architecture_scores) / len(architecture_scores) if architecture_scores else 0
        
        overall_score = (design_average * 0.6) + (architecture_average * 0.4)
        return round(overall_score, 1)
    
    def _identify_violations(
        self,
        design_analysis: Dict[str, Any],
        architecture_analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify principle violations."""
        violations = []
        
        # Check design principle violations
        for principle, result in design_analysis.items():
            if not result["compliant"]:
                violations.append(f"Design principle violation: {principle}")
        
        # Check architecture principle violations
        for principle, result in architecture_analysis.items():
            if not result["compliant"]:
                violations.append(f"Architecture principle violation: {principle}")
        
        return violations
    
    def _generate_recommendations(
        self,
        violations: List[str],
        feature_data: Dict[str, Any]
    ) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        if not violations:
            recommendations.append("Feature meets all DNA compliance requirements")
            return recommendations
        
        # General recommendations based on violations
        if any("pedagogical_value" in v for v in violations):
            recommendations.append("Add explicit learning objectives and educational outcomes")
        
        if any("policy_to_practice" in v for v in violations):
            recommendations.append("Strengthen connection between theory and practical application")
        
        if any("time_respect" in v for v in violations):
            recommendations.append("Reduce scope or improve efficiency to meet 10-minute constraint")
        
        if any("holistic_thinking" in v for v in violations):
            recommendations.append("Consider broader organizational and systemic impacts")
        
        if any("professional_tone" in v for v in violations):
            recommendations.append("Adjust language for professional public sector audience")
        
        # Architecture recommendations
        if any("api_first" in v for v in violations):
            recommendations.append("Ensure all data access goes through API endpoints")
        
        if any("stateless_backend" in v for v in violations):
            recommendations.append("Remove server-side state dependencies")
        
        if any("separation_of_concerns" in v for v in violations):
            recommendations.append("Clearly separate frontend and backend responsibilities")
        
        if any("simplicity_first" in v for v in violations):
            recommendations.append("Simplify feature scope and implementation approach")
        
        return recommendations
    
    def _initialize_design_principles(self) -> Dict[str, Any]:
        """Initialize DigiNativa design principles."""
        return {
            "pedagogical_value": {
                "description": "Educational and learning focus",
                "weight": 1.2
            },
            "policy_to_practice": {
                "description": "Connects policy to practical application",
                "weight": 1.1
            },
            "time_respect": {
                "description": "Respects user's time (d10 minutes per feature)",
                "weight": 1.0
            },
            "holistic_thinking": {
                "description": "Considers full context and implications",
                "weight": 1.0
            },
            "professional_tone": {
                "description": "Appropriate for public sector professionals",
                "weight": 0.9
            }
        }
    
    def _initialize_architecture_principles(self) -> Dict[str, Any]:
        """Initialize DigiNativa architecture principles."""
        return {
            "api_first": {
                "description": "All communication via REST APIs",
                "weight": 1.0
            },
            "stateless_backend": {
                "description": "No server-side sessions, all state from client",
                "weight": 1.0
            },
            "separation_of_concerns": {
                "description": "Frontend and backend completely separate",
                "weight": 1.0
            },
            "simplicity_first": {
                "description": "Choose simplest solution that works",
                "weight": 1.1
            }
        }
    
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules and patterns."""
        return {
            "learning_keywords": [
                "learn", "education", "training", "skill", "knowledge", "competence",
                "objective", "goal", "assessment", "practice", "exercise", "tutorial"
            ],
            "policy_keywords": [
                "policy", "regulation", "law", "guideline", "standard", "principle",
                "theory", "concept", "framework", "methodology"
            ],
            "practice_keywords": [
                "apply", "implement", "practice", "example", "case study", "scenario",
                "real-world", "workplace", "situation", "experience"
            ]
        }
    
    def _initialize_compliance_thresholds(self) -> Dict[str, Any]:
        """Initialize compliance scoring thresholds."""
        return {
            "minimum_score": 70.0,
            "excellent_score": 90.0,
            "principle_pass_threshold": 60
        }
    
    # Recommendation helper methods
    def _get_pedagogical_recommendation(self, score: int, issues: List[str]) -> str:
        if score >= 80:
            return "Strong pedagogical value - maintain focus on learning outcomes"
        elif score >= 60:
            return "Good pedagogical foundation - consider adding more explicit learning objectives"
        else:
            return "Strengthen pedagogical value by adding clear learning objectives and educational outcomes"
    
    def _get_policy_practice_recommendation(self, score: int, issues: List[str]) -> str:
        if score >= 80:
            return "Excellent connection between policy and practice"
        elif score >= 50:
            return "Good policy-practice connection - consider adding more practical examples"
        else:
            return "Strengthen connection between policy/theory and practical workplace application"
    
    def _get_time_respect_recommendation(self, score: int, time_constraint: int) -> str:
        if time_constraint > 15:
            return f"Reduce scope significantly - {time_constraint} minutes exceeds 10-minute target"
        elif time_constraint > 10:
            return f"Consider reducing scope to meet 10-minute target (currently {time_constraint} minutes)"
        else:
            return "Good time management - maintain focus on efficiency"
    
    def _get_holistic_thinking_recommendation(self, score: int, issues: List[str]) -> str:
        if score >= 80:
            return "Strong systems thinking and holistic perspective"
        elif score >= 60:
            return "Good holistic thinking - consider broader organizational impacts"
        else:
            return "Expand perspective to include organizational context and systemic impacts"
    
    def _get_professional_tone_recommendation(self, score: int, issues: List[str]) -> str:
        if score >= 80:
            return "Excellent professional tone for target audience"
        elif score >= 70:
            return "Good professional tone - ensure accessibility for all users"
        else:
            return "Adjust language to be more professional and appropriate for public sector audience"
    
    def _get_simplicity_recommendation(self, score: int, issues: List[str]) -> str:
        if score >= 80:
            return "Good focus on simplicity - maintain lean approach"
        elif score >= 60:
            return "Consider simplifying scope and implementation approach"
        else:
            return "Significantly reduce complexity - focus on core essential functionality"