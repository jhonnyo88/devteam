"""
DNA Code Validator - Active DNA validation for Developer agent.

PURPOSE:
Implements active DNA compliance validation for code generation and implementation,
ensuring Developer output meets DigiNativa DNA principles.

CRITICAL FUNCTIONALITY:
- Time Respect → Code complexity analysis (simple implementation under 10 min to understand)
- Pedagogical Value → Code learning effectiveness (clear, educational code structure)  
- Professional Tone → Code documentation and naming (Swedish municipal standards)
- Architecture compliance → API-first, stateless, separation validation

ADAPTATION GUIDE:
To adapt for your project:
1. Update complexity_thresholds for your performance standards
2. Modify learning_effectiveness_criteria for your quality requirements
3. Adjust professional_standards for your documentation style
4. Update architecture_compliance_criteria for your design patterns

CONTRACT PROTECTION:
This tool enhances Developer DNA validation without breaking contracts.
All outputs integrate seamlessly with existing implementation validation results.
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


class CodeComplexityLevel(Enum):
    """Code complexity levels for time respect validation."""
    EXCELLENT = "excellent"  # Very simple, clear code
    GOOD = "good"           # Simple, understandable
    ACCEPTABLE = "acceptable" # Moderately complex
    COMPLEX = "complex"     # Hard to understand
    EXCESSIVE = "excessive" # Too complex


class CodeLearningEffectiveness(Enum):
    """Code learning effectiveness levels for pedagogical value validation."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    INADEQUATE = "inadequate"


class CodeProfessionalQuality(Enum):
    """Code professional quality for professional tone."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    UNCLEAR = "unclear"
    UNPROFESSIONAL = "unprofessional"


class ArchitectureComplianceLevel(Enum):
    """Architecture compliance levels."""
    FULLY_COMPLIANT = "fully_compliant"
    MOSTLY_COMPLIANT = "mostly_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"


@dataclass
class CodeComplexityResult:
    """Result from code complexity analysis."""
    complexity_level: CodeComplexityLevel
    component_complexity_scores: Dict[str, int]  # Cyclomatic complexity per component
    api_complexity_scores: Dict[str, int]        # Cyclomatic complexity per API
    average_component_complexity: float
    average_api_complexity: float
    complexity_violations: List[str]
    simplification_recommendations: List[str]


@dataclass
class CodeLearningResult:
    """Result from code learning effectiveness validation."""
    learning_effectiveness: CodeLearningEffectiveness
    learning_effectiveness_score: float  # 1-5 scale
    comment_quality_score: float
    variable_naming_clarity: float
    code_structure_educational: bool
    documentation_completeness: float
    learning_violations: List[str]
    educational_improvements: List[str]


@dataclass
class CodeProfessionalResult:
    """Result from code professional tone analysis."""
    professional_quality: CodeProfessionalQuality
    professional_score: float  # 1-5 scale
    swedish_municipal_terminology: Dict[str, int]
    documentation_professional: bool
    error_messages_appropriate: bool
    naming_conventions_followed: bool
    professional_violations: List[str]
    professional_improvements: List[str]


@dataclass
class ArchitectureComplianceResult:
    """Result from architecture compliance validation."""
    compliance_level: ArchitectureComplianceLevel
    api_first_compliant: bool
    stateless_backend_compliant: bool
    separation_concerns_compliant: bool
    simplicity_first_compliant: bool
    compliance_score: float  # 1-5 scale
    architecture_violations: List[str]
    architecture_improvements: List[str]


@dataclass
class DNACodeValidationResult:
    """Complete DNA code validation result."""
    overall_dna_compliant: bool
    time_respect_compliant: bool        # Code complexity under 10 min to understand
    pedagogical_value_compliant: bool   # Code structure teaches good practices
    professional_tone_compliant: bool   # Professional naming, documentation
    api_first_compliant: bool          # API-first architecture
    stateless_backend_compliant: bool  # No server-side sessions
    separation_concerns_compliant: bool # Frontend/backend separate
    simplicity_first_compliant: bool   # Simplest solution chosen
    complexity_result: CodeComplexityResult
    learning_result: CodeLearningResult
    professional_result: CodeProfessionalResult
    architecture_result: ArchitectureComplianceResult
    validation_timestamp: str
    dna_compliance_score: float        # 1-5 scale
    violations: List[str]
    recommendations: List[str]
    quality_reviewer_metrics: Dict[str, Any]  # For Quality Reviewer integration


class DNACodeValidator:
    """
    Active DNA validation for Developer code generation.
    
    Validates generated code against DigiNativa DNA principles:
    - Time Respect: Code complexity analysis for maintainability
    - Pedagogical Value: Code learning effectiveness and clarity  
    - Professional Tone: Code documentation and naming quality
    - Architecture Compliance: API-first, stateless, separation, simplicity
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize DNA Code Validator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Time Respect validation thresholds (complexity limits)
        self.complexity_thresholds = {
            "max_component_complexity": 10,  # Cyclomatic complexity for React components
            "max_api_complexity": 8,         # Cyclomatic complexity for API endpoints
            "max_function_complexity": 5,    # Individual function complexity
            "max_nesting_depth": 3,          # Maximum nesting depth
            "max_file_lines": 200            # Maximum lines per file
        }
        
        # Pedagogical Value validation criteria
        self.learning_effectiveness_criteria = {
            "min_learning_score": 4.0,       # 1-5 scale
            "min_comment_ratio": 0.3,        # 30% comment coverage
            "min_variable_clarity": 4.0,     # Variable naming clarity score
            "required_documentation": True,  # Function documentation required
            "min_educational_structure": 4.0 # Code structure educational value
        }
        
        # Professional Tone validation standards
        self.professional_standards = {
            "min_professional_score": 4.0,   # 1-5 scale
            "required_municipal_terms": [
                "kommun", "förvaltning", "tjänst", "medarbetare", "utbildning",
                "policy", "riktlinje", "process", "kvalitet", "säkerhet"
            ],
            "forbidden_casual_terms": [
                "fixar", "funkar", "grejer", "typ", "kanske", "borde"
            ],
            "naming_conventions": {
                "components": "PascalCase",
                "functions": "camelCase", 
                "variables": "camelCase",
                "constants": "UPPER_CASE"
            }
        }
        
        # Architecture Compliance validation criteria
        self.architecture_compliance_criteria = {
            "api_first_required": True,
            "stateless_backend_required": True,
            "frontend_backend_separation": True,
            "component_library_usage": 0.8,  # 80% UI library usage
            "max_api_response_time": 200      # milliseconds
        }
        
        logger.info("DNA Code Validator initialized for Developer Agent")
    
    async def validate_code_dna_compliance(self,
                                         component_implementations: List[Dict[str, Any]],
                                         api_implementations: List[Dict[str, Any]], 
                                         test_suite: Dict[str, Any],
                                         story_data: Dict[str, Any]) -> DNACodeValidationResult:
        """
        Comprehensive DNA validation for code implementation.
        
        Args:
            component_implementations: Generated React components
            api_implementations: Generated FastAPI endpoints
            test_suite: Generated test suite
            story_data: Original story requirements
            
        Returns:
            Complete DNA code validation result
        """
        try:
            logger.info("Starting comprehensive DNA code validation")
            
            # Validate Time Respect (code complexity)
            complexity_result = await self._validate_code_complexity(
                component_implementations, api_implementations, story_data
            )
            
            # Validate Pedagogical Value (code learning effectiveness)
            learning_result = await self._validate_code_learning_effectiveness(
                component_implementations, api_implementations, story_data
            )
            
            # Validate Professional Tone (code documentation and naming)
            professional_result = await self._validate_code_professional_tone(
                component_implementations, api_implementations, story_data
            )
            
            # Validate Architecture Compliance
            architecture_result = await self._validate_architecture_compliance(
                component_implementations, api_implementations, story_data
            )
            
            # Calculate overall compliance
            time_respect_compliant = complexity_result.complexity_level in [
                CodeComplexityLevel.EXCELLENT, CodeComplexityLevel.GOOD, CodeComplexityLevel.ACCEPTABLE
            ]
            pedagogical_value_compliant = learning_result.learning_effectiveness_score >= 4.0
            professional_tone_compliant = professional_result.professional_score >= 4.0
            architecture_compliant = architecture_result.compliance_score >= 4.0
            
            overall_compliant = all([
                time_respect_compliant, pedagogical_value_compliant,
                professional_tone_compliant, architecture_compliant
            ])
            
            # Calculate overall DNA compliance score
            dna_score = (
                self._complexity_to_score(complexity_result.complexity_level) +
                learning_result.learning_effectiveness_score +
                professional_result.professional_score +
                architecture_result.compliance_score
            ) / 4.0
            
            # Collect all violations and recommendations
            all_violations = (
                complexity_result.complexity_violations +
                learning_result.learning_violations +
                professional_result.professional_violations +
                architecture_result.architecture_violations
            )
            
            all_recommendations = (
                complexity_result.simplification_recommendations +
                learning_result.educational_improvements +
                professional_result.professional_improvements +
                architecture_result.architecture_improvements
            )
            
            # Create metrics for Quality Reviewer
            quality_reviewer_metrics = {
                "complexity_analysis": {
                    "avg_component_complexity": complexity_result.average_component_complexity,
                    "avg_api_complexity": complexity_result.average_api_complexity,
                    "complexity_level": complexity_result.complexity_level.value
                },
                "learning_effectiveness": {
                    "score": learning_result.learning_effectiveness_score,
                    "comment_quality": learning_result.comment_quality_score,
                    "naming_clarity": learning_result.variable_naming_clarity
                },
                "professional_quality": {
                    "score": professional_result.professional_score,
                    "documentation_professional": professional_result.documentation_professional,
                    "naming_conventions": professional_result.naming_conventions_followed
                },
                "architecture_compliance": {
                    "score": architecture_result.compliance_score,
                    "api_first": architecture_result.api_first_compliant,
                    "stateless": architecture_result.stateless_backend_compliant
                }
            }
            
            return DNACodeValidationResult(
                overall_dna_compliant=overall_compliant,
                time_respect_compliant=time_respect_compliant,
                pedagogical_value_compliant=pedagogical_value_compliant,
                professional_tone_compliant=professional_tone_compliant,
                api_first_compliant=architecture_result.api_first_compliant,
                stateless_backend_compliant=architecture_result.stateless_backend_compliant,
                separation_concerns_compliant=architecture_result.separation_concerns_compliant,
                simplicity_first_compliant=architecture_result.simplicity_first_compliant,
                complexity_result=complexity_result,
                learning_result=learning_result,
                professional_result=professional_result,
                architecture_result=architecture_result,
                validation_timestamp=datetime.now().isoformat(),
                dna_compliance_score=dna_score,
                violations=all_violations,
                recommendations=all_recommendations,
                quality_reviewer_metrics=quality_reviewer_metrics
            )
            
        except Exception as e:
            logger.error(f"DNA code validation failed: {str(e)}")
            raise
    
    async def _validate_code_complexity(self,
                                      component_implementations: List[Dict[str, Any]],
                                      api_implementations: List[Dict[str, Any]],
                                      story_data: Dict[str, Any]) -> CodeComplexityResult:
        """
        Validate Time Respect principle through code complexity analysis.
        
        Ensures code is simple enough to understand within 10 minutes.
        """
        component_scores = {}
        api_scores = {}
        violations = []
        recommendations = []
        
        # Analyze React component complexity
        for component in component_implementations:
            component_code = component.get("code", {}).get("component", "")
            complexity = self._calculate_cyclomatic_complexity(component_code)
            component_scores[component["name"]] = complexity
            
            if complexity > self.complexity_thresholds["max_component_complexity"]:
                violations.append(f"Component {component['name']} complexity too high: {complexity} (max: {self.complexity_thresholds['max_component_complexity']})")
                recommendations.append(f"Break down {component['name']} into smaller sub-components")
        
        # Analyze FastAPI endpoint complexity
        for api in api_implementations:
            api_code = api.get("code", {}).get("endpoint", "")
            complexity = self._calculate_cyclomatic_complexity(api_code)
            api_scores[api["name"]] = complexity
            
            if complexity > self.complexity_thresholds["max_api_complexity"]:
                violations.append(f"API {api['name']} complexity too high: {complexity} (max: {self.complexity_thresholds['max_api_complexity']})")
                recommendations.append(f"Simplify {api['name']} by extracting business logic to separate functions")
        
        # Calculate averages
        avg_component_complexity = sum(component_scores.values()) / len(component_scores) if component_scores else 0
        avg_api_complexity = sum(api_scores.values()) / len(api_scores) if api_scores else 0
        
        # Determine overall complexity level
        max_complexity = max([avg_component_complexity, avg_api_complexity])
        if max_complexity <= 3:
            complexity_level = CodeComplexityLevel.EXCELLENT
        elif max_complexity <= 5:
            complexity_level = CodeComplexityLevel.GOOD
        elif max_complexity <= 8:
            complexity_level = CodeComplexityLevel.ACCEPTABLE
        elif max_complexity <= 12:
            complexity_level = CodeComplexityLevel.COMPLEX
        else:
            complexity_level = CodeComplexityLevel.EXCESSIVE
        
        return CodeComplexityResult(
            complexity_level=complexity_level,
            component_complexity_scores=component_scores,
            api_complexity_scores=api_scores,
            average_component_complexity=avg_component_complexity,
            average_api_complexity=avg_api_complexity,
            complexity_violations=violations,
            simplification_recommendations=recommendations
        )
    
    async def _validate_code_learning_effectiveness(self,
                                                  component_implementations: List[Dict[str, Any]],
                                                  api_implementations: List[Dict[str, Any]],
                                                  story_data: Dict[str, Any]) -> CodeLearningResult:
        """
        Validate Pedagogical Value principle through code learning effectiveness.
        
        Ensures code structure supports learning and understanding.
        """
        total_score = 0.0
        comment_scores = []
        naming_scores = []
        structure_educational = True
        documentation_complete = True
        violations = []
        improvements = []
        
        # Analyze React components for learning effectiveness
        for component in component_implementations:
            component_code = component.get("code", {}).get("component", "")
            
            # Check comment quality for learning
            comment_score = self._analyze_comment_quality(component_code, "component")
            comment_scores.append(comment_score)
            
            if comment_score < 3.0:
                violations.append(f"Component {component['name']} lacks educational comments")
                improvements.append(f"Add learning-focused comments explaining the purpose and usage of {component['name']}")
            
            # Check variable naming clarity
            naming_score = self._analyze_variable_naming_clarity(component_code)
            naming_scores.append(naming_score)
            
            if naming_score < 3.0:
                violations.append(f"Component {component['name']} has unclear variable naming")
                improvements.append(f"Use more descriptive variable names in {component['name']} that explain their educational purpose")
            
            # Check if documentation exists
            if "/**" not in component_code and "@param" not in component_code:
                documentation_complete = False
                improvements.append(f"Add JSDoc documentation to {component['name']} explaining its learning objectives")
        
        # Analyze FastAPI endpoints for learning effectiveness
        for api in api_implementations:
            api_code = api.get("code", {}).get("endpoint", "")
            
            # Check comment quality for learning
            comment_score = self._analyze_comment_quality(api_code, "api")
            comment_scores.append(comment_score)
            
            if comment_score < 3.0:
                violations.append(f"API {api['name']} lacks educational documentation")
                improvements.append(f"Add learning-focused documentation explaining the municipal context of {api['name']}")
            
            # Check variable naming clarity
            naming_score = self._analyze_variable_naming_clarity(api_code)
            naming_scores.append(naming_score)
            
            if naming_score < 3.0:
                violations.append(f"API {api['name']} has unclear parameter naming")
                improvements.append(f"Use more descriptive parameter names in {api['name']} that explain their purpose")
        
        # Calculate overall learning effectiveness
        avg_comment_quality = sum(comment_scores) / len(comment_scores) if comment_scores else 0
        avg_naming_clarity = sum(naming_scores) / len(naming_scores) if naming_scores else 0
        
        learning_score = (avg_comment_quality + avg_naming_clarity) / 2.0
        
        # Determine learning effectiveness level
        if learning_score >= 4.5:
            effectiveness = CodeLearningEffectiveness.EXCELLENT
        elif learning_score >= 4.0:
            effectiveness = CodeLearningEffectiveness.GOOD
        elif learning_score >= 3.0:
            effectiveness = CodeLearningEffectiveness.ACCEPTABLE
        elif learning_score >= 2.0:
            effectiveness = CodeLearningEffectiveness.POOR
        else:
            effectiveness = CodeLearningEffectiveness.INADEQUATE
        
        return CodeLearningResult(
            learning_effectiveness=effectiveness,
            learning_effectiveness_score=learning_score,
            comment_quality_score=avg_comment_quality,
            variable_naming_clarity=avg_naming_clarity,
            code_structure_educational=structure_educational,
            documentation_completeness=1.0 if documentation_complete else 0.5,
            learning_violations=violations,
            educational_improvements=improvements
        )
    
    async def _validate_code_professional_tone(self,
                                             component_implementations: List[Dict[str, Any]],
                                             api_implementations: List[Dict[str, Any]],
                                             story_data: Dict[str, Any]) -> CodeProfessionalResult:
        """
        Validate Professional Tone principle in code documentation and naming.
        
        Ensures code follows Swedish municipal professional standards.
        """
        municipal_term_counts = {}
        professional_scores = []
        documentation_professional = True
        error_messages_appropriate = True
        naming_conventions_followed = True
        violations = []
        improvements = []
        
        # Analyze all code for professional tone
        all_code = []
        for component in component_implementations:
            all_code.append(component.get("code", {}).get("component", ""))
        for api in api_implementations:
            all_code.append(api.get("code", {}).get("endpoint", ""))
        
        combined_code = "\n".join(all_code)
        
        # Check for Swedish municipal terminology
        for term in self.professional_standards["required_municipal_terms"]:
            count = len(re.findall(rf'\b{term}\b', combined_code.lower()))
            municipal_term_counts[term] = count
        
        # Check for forbidden casual terms
        for term in self.professional_standards["forbidden_casual_terms"]:
            if term in combined_code.lower():
                violations.append(f"Unprofessional term '{term}' found in code")
                improvements.append(f"Replace '{term}' with more professional terminology")
        
        # Check naming conventions in components
        for component in component_implementations:
            component_code = component.get("code", {}).get("component", "")
            
            # Check component naming (should be PascalCase)
            if not component["name"][0].isupper():
                naming_conventions_followed = False
                violations.append(f"Component {component['name']} should use PascalCase")
            
            # Check professional documentation
            if "TODO" in component_code or "FIXME" in component_code:
                documentation_professional = False
                violations.append(f"Component {component['name']} contains unprofessional TODO/FIXME comments")
        
        # Check error messages in APIs
        for api in api_implementations:
            api_code = api.get("code", {}).get("endpoint", "")
            
            # Check for professional error messages
            if "error" in api_code.lower():
                if any(casual in api_code.lower() for casual in ["oops", "failed", "broken"]):
                    error_messages_appropriate = False
                    violations.append(f"API {api['name']} has unprofessional error messages")
                    improvements.append(f"Use professional error messages in {api['name']} suitable for municipal users")
        
        # Calculate professional score
        municipal_usage = sum(1 for count in municipal_term_counts.values() if count > 0) / len(self.professional_standards["required_municipal_terms"])
        casual_penalty = len([v for v in violations if "Unprofessional term" in v]) * 0.5
        
        professional_score = max(0, 5.0 * municipal_usage - casual_penalty)
        professional_score = min(5.0, professional_score)
        
        # Determine professional quality
        if professional_score >= 4.5:
            quality = CodeProfessionalQuality.EXCELLENT
        elif professional_score >= 4.0:
            quality = CodeProfessionalQuality.GOOD
        elif professional_score >= 3.0:
            quality = CodeProfessionalQuality.ACCEPTABLE
        elif professional_score >= 2.0:
            quality = CodeProfessionalQuality.UNCLEAR
        else:
            quality = CodeProfessionalQuality.UNPROFESSIONAL
        
        return CodeProfessionalResult(
            professional_quality=quality,
            professional_score=professional_score,
            swedish_municipal_terminology=municipal_term_counts,
            documentation_professional=documentation_professional,
            error_messages_appropriate=error_messages_appropriate,
            naming_conventions_followed=naming_conventions_followed,
            professional_violations=violations,
            professional_improvements=improvements
        )
    
    async def _validate_architecture_compliance(self,
                                              component_implementations: List[Dict[str, Any]],
                                              api_implementations: List[Dict[str, Any]],
                                              story_data: Dict[str, Any]) -> ArchitectureComplianceResult:
        """
        Validate Architecture Compliance principles.
        
        Ensures code follows API-first, stateless, separation, and simplicity principles.
        """
        api_first_compliant = True
        stateless_backend_compliant = True
        separation_concerns_compliant = True
        simplicity_first_compliant = True
        violations = []
        improvements = []
        
        # Check API-first compliance
        api_count = len(api_implementations)
        component_count = len(component_implementations)
        
        if component_count > 0 and api_count == 0:
            api_first_compliant = False
            violations.append("No API endpoints defined - violates API-first principle")
            improvements.append("Define API endpoints for backend functionality")
        
        # Check stateless backend compliance
        for api in api_implementations:
            api_code = api.get("code", {}).get("endpoint", "")
            
            # Check for stateful patterns
            stateful_patterns = ["session", "global", "cache", "state"]
            for pattern in stateful_patterns:
                if pattern in api_code.lower() and "stateless" not in api_code.lower():
                    stateless_backend_compliant = False
                    violations.append(f"API {api['name']} may violate stateless principle (contains '{pattern}')")
                    improvements.append(f"Ensure {api['name']} doesn't rely on server-side state")
        
        # Check separation of concerns
        for component in component_implementations:
            component_code = component.get("code", {}).get("component", "")
            
            # Check if component contains business logic that should be in API
            business_logic_patterns = ["validate", "process", "calculate", "transform"]
            complex_logic_count = sum(1 for pattern in business_logic_patterns if pattern in component_code.lower())
            
            if complex_logic_count > 2:
                separation_concerns_compliant = False
                violations.append(f"Component {component['name']} contains business logic that should be in API")
                improvements.append(f"Move business logic from {component['name']} to API endpoints")
        
        # Check simplicity first
        total_complexity = 0
        implementation_count = len(component_implementations) + len(api_implementations)
        
        if implementation_count > 0:
            for component in component_implementations:
                component_code = component.get("code", {}).get("component", "")
                total_complexity += self._calculate_cyclomatic_complexity(component_code)
            
            for api in api_implementations:
                api_code = api.get("code", {}).get("endpoint", "")
                total_complexity += self._calculate_cyclomatic_complexity(api_code)
            
            avg_complexity = total_complexity / implementation_count
            
            if avg_complexity > 8:
                simplicity_first_compliant = False
                violations.append(f"Average implementation complexity too high: {avg_complexity:.1f} (max: 8)")
                improvements.append("Simplify implementations by breaking down complex functions")
        
        # Calculate compliance score
        compliance_scores = [
            5.0 if api_first_compliant else 2.0,
            5.0 if stateless_backend_compliant else 2.0,
            5.0 if separation_concerns_compliant else 2.0,
            5.0 if simplicity_first_compliant else 2.0
        ]
        compliance_score = sum(compliance_scores) / len(compliance_scores)
        
        # Determine compliance level
        if compliance_score >= 4.5:
            compliance_level = ArchitectureComplianceLevel.FULLY_COMPLIANT
        elif compliance_score >= 3.5:
            compliance_level = ArchitectureComplianceLevel.MOSTLY_COMPLIANT
        elif compliance_score >= 2.5:
            compliance_level = ArchitectureComplianceLevel.PARTIALLY_COMPLIANT
        else:
            compliance_level = ArchitectureComplianceLevel.NON_COMPLIANT
        
        return ArchitectureComplianceResult(
            compliance_level=compliance_level,
            api_first_compliant=api_first_compliant,
            stateless_backend_compliant=stateless_backend_compliant,
            separation_concerns_compliant=separation_concerns_compliant,
            simplicity_first_compliant=simplicity_first_compliant,
            compliance_score=compliance_score,
            architecture_violations=violations,
            architecture_improvements=improvements
        )
    
    def _calculate_cyclomatic_complexity(self, code: str) -> int:
        """
        Calculate cyclomatic complexity of code.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Cyclomatic complexity score
        """
        complexity = 1  # Base complexity
        
        # Decision points that increase complexity
        decision_keywords = [
            'if', 'elif', 'else if', 'while', 'for', 'forEach', 'switch', 'case',
            'try', 'catch', 'finally', '&&', '||', '?', 'break', 'continue'
        ]
        
        code_lower = code.lower()
        for keyword in decision_keywords:
            complexity += code_lower.count(keyword)
        
        return complexity
    
    def _analyze_comment_quality(self, code: str, code_type: str) -> float:
        """
        Analyze comment quality for learning effectiveness.
        
        Args:
            code: Source code to analyze
            code_type: Type of code (component, api)
            
        Returns:
            Comment quality score (1-5)
        """
        lines = code.split('\n')
        total_lines = len([line for line in lines if line.strip()])
        comment_lines = len([line for line in lines if '//' in line or '/*' in line or '*' in line or '"""' in line])
        
        if total_lines == 0:
            return 0.0
        
        comment_ratio = comment_lines / total_lines
        
        # Check for educational keywords in comments
        educational_keywords = ['learn', 'understand', 'example', 'purpose', 'why', 'how', 'municipal', 'training']
        educational_score = sum(1 for keyword in educational_keywords if keyword in code.lower()) * 0.5
        
        # Base score from comment ratio
        base_score = min(5.0, comment_ratio * 10)  # 10% comments = score 1, 50% = score 5
        
        # Bonus for educational content
        final_score = min(5.0, base_score + educational_score)
        
        return final_score
    
    def _analyze_variable_naming_clarity(self, code: str) -> float:
        """
        Analyze variable naming clarity.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Naming clarity score (1-5)
        """
        # Extract variable names (simplified pattern)
        variable_patterns = [
            r'\bconst\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\blet\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\bvar\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'([a-zA-Z_][a-zA-Z0-9_]*)\s*='
        ]
        
        variables = []
        for pattern in variable_patterns:
            matches = re.findall(pattern, code)
            variables.extend(matches)
        
        if not variables:
            return 3.0  # Neutral score if no variables found
        
        # Analyze naming quality
        clear_names = 0
        for var in variables:
            # Check if name is descriptive (longer than 3 chars, not abbreviations)
            if len(var) > 3 and not var.isupper() and '_' not in var[:3]:
                clear_names += 1
            # Bonus for descriptive words
            if any(word in var.lower() for word in ['user', 'data', 'result', 'value', 'config', 'option']):
                clear_names += 0.5
        
        clarity_ratio = clear_names / len(variables)
        return min(5.0, clarity_ratio * 5.0)
    
    def _complexity_to_score(self, complexity_level: CodeComplexityLevel) -> float:
        """Convert complexity level to numeric score."""
        complexity_scores = {
            CodeComplexityLevel.EXCELLENT: 5.0,
            CodeComplexityLevel.GOOD: 4.0,
            CodeComplexityLevel.ACCEPTABLE: 3.0,
            CodeComplexityLevel.COMPLEX: 2.0,
            CodeComplexityLevel.EXCESSIVE: 1.0
        }
        return complexity_scores.get(complexity_level, 3.0)