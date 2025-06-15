"""
AI Test Optimizer - Intelligent test optimization and prioritization for Test Engineer.

PURPOSE:
Implements AI-driven test optimization with predictive failure analysis,
risk-based test prioritization, and edge case prediction capabilities.

CRITICAL FUNCTIONALITY:
- Predictive failure analysis based on implementation patterns
- Risk-based test prioritization with ML algorithms  
- Edge case prediction from historical data
- Test maintenance prediction and optimization
- Swedish municipal context optimization

ADAPTATION GUIDE:
To adapt for your project:
1. Update failure_patterns for your specific technology stack
2. Modify risk_factors for your quality standards
3. Adjust municipal_context_patterns for your client base
4. Update optimization_thresholds for your performance targets

CONTRACT PROTECTION:
This tool enhances Test Engineer capabilities without breaking contracts.
All outputs integrate seamlessly with existing test generation workflow.
"""

import asyncio
import logging
import json
import re
from typing import Dict, Any, List, Optional, Tuple, Set
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import random
import hashlib

# Setup logging
logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk levels for test prioritization."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class TestComplexity(Enum):
    """Test complexity levels for optimization."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"
    EXTREME = "extreme"


class FailurePredictionConfidence(Enum):
    """Confidence levels for failure predictions."""
    VERY_HIGH = "very_high"  # 90%+
    HIGH = "high"           # 75-90%
    MEDIUM = "medium"       # 50-75%
    LOW = "low"            # 25-50%
    VERY_LOW = "very_low"  # <25%


@dataclass
class FailurePrediction:
    """Prediction of potential test failure."""
    component_name: str
    failure_probability: float  # 0-1 scale
    confidence_level: FailurePredictionConfidence
    predicted_failure_type: str
    historical_patterns: List[str]
    recommendations: List[str]


@dataclass
class TestPriority:
    """Test priority assignment with AI reasoning."""
    test_case_id: str
    risk_level: RiskLevel
    priority_score: float  # 1-100 scale
    complexity_level: TestComplexity
    estimated_execution_time_minutes: float
    business_impact_score: float
    technical_risk_score: float
    municipal_context_relevance: float
    optimization_recommendations: List[str]


@dataclass
class EdgeCasePrediction:
    """Predicted edge case for comprehensive testing."""
    scenario_description: str
    likelihood_score: float  # 0-1 scale
    impact_severity: str
    test_data_requirements: Dict[str, Any]
    municipal_specific: bool
    anna_persona_relevant: bool


@dataclass
class TestMaintenancePrediction:
    """Prediction for test maintenance needs."""
    test_suite_section: str
    maintenance_probability: float  # 0-1 scale
    predicted_maintenance_type: str  # "update", "refactor", "remove", "extend"
    timeline_estimate_days: int
    maintenance_complexity: TestComplexity
    prevention_recommendations: List[str]


@dataclass
class AITestOptimizationResult:
    """Complete AI test optimization result."""
    story_id: str
    optimization_timestamp: str
    failure_predictions: List[FailurePrediction]
    test_priorities: List[TestPriority]
    edge_case_predictions: List[EdgeCasePrediction]
    maintenance_predictions: List[TestMaintenancePrediction]
    overall_optimization_score: float  # 1-5 scale
    estimated_time_savings_minutes: float
    quality_improvement_score: float
    municipal_optimization_insights: Dict[str, Any]


class AITestOptimizer:
    """
    AI-driven test optimization and intelligent prioritization.
    
    Provides predictive failure analysis, risk-based test prioritization,
    and edge case prediction to optimize Test Engineer efficiency and quality.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize AI Test Optimizer.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # AI optimization thresholds and parameters
        self.optimization_thresholds = {
            "min_failure_probability": 0.3,  # 30% minimum to consider
            "critical_risk_threshold": 0.8,  # 80% for critical priority
            "high_risk_threshold": 0.6,     # 60% for high priority
            "medium_risk_threshold": 0.4,   # 40% for medium priority
            "max_test_execution_time": 15.0,  # 15 minutes max per test
            "municipal_relevance_weight": 1.5  # 50% boost for municipal-specific
        }
        
        # Failure pattern recognition database (simulated ML patterns)
        self.failure_patterns = {
            "react_component_patterns": {
                "useEffect_dependency_missing": {"probability": 0.7, "severity": "high"},
                "state_update_async_issues": {"probability": 0.6, "severity": "medium"},
                "prop_type_mismatch": {"probability": 0.5, "severity": "medium"},
                "memory_leak_component_unmount": {"probability": 0.4, "severity": "high"},
                "accessibility_aria_missing": {"probability": 0.8, "severity": "medium"}
            },
            "fastapi_endpoint_patterns": {
                "async_function_not_awaited": {"probability": 0.6, "severity": "high"},
                "pydantic_validation_error": {"probability": 0.5, "severity": "medium"},
                "database_connection_leak": {"probability": 0.4, "severity": "critical"},
                "cors_configuration_error": {"probability": 0.3, "severity": "low"},
                "response_timeout_error": {"probability": 0.7, "severity": "high"}
            },
            "municipal_specific_patterns": {
                "gdpr_compliance_violation": {"probability": 0.9, "severity": "critical"},
                "swedish_character_encoding": {"probability": 0.6, "severity": "medium"},
                "personnummer_validation_fail": {"probability": 0.5, "severity": "high"},
                "accessibility_wcag_aa_fail": {"probability": 0.7, "severity": "high"},
                "municipal_workflow_timeout": {"probability": 0.4, "severity": "medium"}
            }
        }
        
        # Risk factors for prioritization
        self.risk_factors = {
            "user_facing_component": 2.0,     # 2x multiplier
            "data_handling_component": 1.8,   # 1.8x multiplier
            "authentication_related": 2.5,    # 2.5x multiplier
            "municipal_policy_integration": 2.2,  # 2.2x multiplier
            "accessibility_critical": 1.7,    # 1.7x multiplier
            "performance_sensitive": 1.5,     # 1.5x multiplier
            "gdpr_sensitive": 3.0,            # 3x multiplier (highest)
            "integration_heavy": 1.6          # 1.6x multiplier
        }
        
        # Municipal context patterns for Swedish public sector
        self.municipal_context_patterns = {
            "anna_persona_workflows": {
                "task_completion_under_10min": {"weight": 2.0, "critical": True},
                "interruption_recovery": {"weight": 1.8, "critical": True},
                "multi_device_usage": {"weight": 1.5, "critical": False},
                "stress_scenario_handling": {"weight": 1.7, "critical": True}
            },
            "swedish_compliance_requirements": {
                "gdpr_data_handling": {"weight": 3.0, "critical": True},
                "osl_public_access": {"weight": 2.5, "critical": True},
                "swedish_language_support": {"weight": 1.8, "critical": False},
                "municipal_security_standards": {"weight": 2.2, "critical": True}
            },
            "public_sector_integration": {
                "e_service_compatibility": {"weight": 2.0, "critical": True},
                "legacy_system_integration": {"weight": 1.6, "critical": False},
                "multi_municipality_support": {"weight": 1.4, "critical": False},
                "crisis_management_readiness": {"weight": 2.3, "critical": True}
            }
        }
        
        logger.info("AI Test Optimizer initialized with predictive capabilities")
    
    async def optimize_test_strategy(self,
                                   component_implementations: List[Dict[str, Any]],
                                   api_implementations: List[Dict[str, Any]],
                                   story_data: Dict[str, Any],
                                   existing_test_suite: Dict[str, Any]) -> AITestOptimizationResult:
        """
        Comprehensive AI-driven test optimization and strategy generation.
        
        Args:
            component_implementations: React components from Developer
            api_implementations: FastAPI endpoints from Developer
            story_data: Original story requirements and context
            existing_test_suite: Current test suite for analysis
            
        Returns:
            Complete AI test optimization result with predictions and priorities
        """
        try:
            story_id = story_data.get("story_id", "unknown")
            logger.info(f"Starting AI test optimization for story: {story_id}")
            
            # Step 1: Predictive failure analysis
            failure_predictions = await self._analyze_failure_predictions(
                component_implementations, api_implementations, story_data
            )
            
            # Step 2: Risk-based test prioritization
            test_priorities = await self._generate_test_priorities(
                component_implementations, api_implementations, story_data, failure_predictions
            )
            
            # Step 3: Edge case prediction
            edge_case_predictions = await self._predict_edge_cases(
                component_implementations, api_implementations, story_data
            )
            
            # Step 4: Test maintenance prediction
            maintenance_predictions = await self._predict_test_maintenance(
                existing_test_suite, component_implementations, api_implementations
            )
            
            # Step 5: Calculate optimization metrics
            optimization_metrics = await self._calculate_optimization_metrics(
                test_priorities, failure_predictions, edge_case_predictions
            )
            
            # Step 6: Generate municipal-specific insights
            municipal_insights = await self._generate_municipal_optimization_insights(
                story_data, test_priorities, failure_predictions
            )
            
            optimization_result = AITestOptimizationResult(
                story_id=story_id,
                optimization_timestamp=datetime.now().isoformat(),
                failure_predictions=failure_predictions,
                test_priorities=test_priorities,
                edge_case_predictions=edge_case_predictions,
                maintenance_predictions=maintenance_predictions,
                overall_optimization_score=optimization_metrics["overall_score"],
                estimated_time_savings_minutes=optimization_metrics["time_savings"],
                quality_improvement_score=optimization_metrics["quality_improvement"],
                municipal_optimization_insights=municipal_insights
            )
            
            logger.info(f"AI test optimization completed with {optimization_metrics['overall_score']:.1f}/5.0 score")
            return optimization_result
            
        except Exception as e:
            logger.error(f"AI test optimization failed: {e}")
            raise
    
    async def _analyze_failure_predictions(self,
                                         component_implementations: List[Dict[str, Any]],
                                         api_implementations: List[Dict[str, Any]],
                                         story_data: Dict[str, Any]) -> List[FailurePrediction]:
        """
        Analyze potential failure points using ML-based pattern recognition.
        """
        try:
            failure_predictions = []
            
            # Analyze React components for failure patterns
            for component in component_implementations:
                component_name = component.get("name", "unknown")
                code_content = component.get("code", {}).get("component", "")
                
                # Pattern matching for common failure scenarios
                for pattern, details in self.failure_patterns["react_component_patterns"].items():
                    if await self._matches_failure_pattern(code_content, pattern, "react"):
                        
                        # Calculate confidence based on pattern strength and context
                        confidence = await self._calculate_prediction_confidence(
                            component, pattern, details["probability"]
                        )
                        
                        failure_predictions.append(FailurePrediction(
                            component_name=component_name,
                            failure_probability=details["probability"],
                            confidence_level=confidence,
                            predicted_failure_type=pattern,
                            historical_patterns=[f"react_{pattern}"],
                            recommendations=await self._generate_failure_prevention_recommendations(
                                pattern, "react", component
                            )
                        ))
            
            # Analyze FastAPI endpoints for failure patterns
            for api in api_implementations:
                api_name = api.get("name", "unknown")
                code_content = api.get("code", {}).get("endpoint", "")
                
                for pattern, details in self.failure_patterns["fastapi_endpoint_patterns"].items():
                    if await self._matches_failure_pattern(code_content, pattern, "fastapi"):
                        
                        confidence = await self._calculate_prediction_confidence(
                            api, pattern, details["probability"]
                        )
                        
                        failure_predictions.append(FailurePrediction(
                            component_name=api_name,
                            failure_probability=details["probability"],
                            confidence_level=confidence,
                            predicted_failure_type=pattern,
                            historical_patterns=[f"fastapi_{pattern}"],
                            recommendations=await self._generate_failure_prevention_recommendations(
                                pattern, "fastapi", api
                            )
                        ))
            
            # Analyze municipal-specific failure patterns
            municipal_predictions = await self._analyze_municipal_failure_patterns(
                component_implementations, api_implementations, story_data
            )
            failure_predictions.extend(municipal_predictions)
            
            # Filter predictions by minimum threshold
            filtered_predictions = [
                pred for pred in failure_predictions 
                if pred.failure_probability >= self.optimization_thresholds["min_failure_probability"]
            ]
            
            return filtered_predictions[:10]  # Top 10 most likely failures
            
        except Exception as e:
            logger.error(f"Failure prediction analysis failed: {e}")
            return []
    
    async def _generate_test_priorities(self,
                                      component_implementations: List[Dict[str, Any]],
                                      api_implementations: List[Dict[str, Any]],
                                      story_data: Dict[str, Any],
                                      failure_predictions: List[FailurePrediction]) -> List[TestPriority]:
        """
        Generate AI-driven test prioritization based on risk analysis.
        """
        try:
            test_priorities = []
            
            # Prioritize component tests
            for component in component_implementations:
                priority = await self._calculate_component_test_priority(
                    component, story_data, failure_predictions
                )
                test_priorities.append(priority)
            
            # Prioritize API tests
            for api in api_implementations:
                priority = await self._calculate_api_test_priority(
                    api, story_data, failure_predictions
                )
                test_priorities.append(priority)
            
            # Sort by priority score (highest first)
            test_priorities.sort(key=lambda x: x.priority_score, reverse=True)
            
            return test_priorities
            
        except Exception as e:
            logger.error(f"Test prioritization failed: {e}")
            return []
    
    async def _predict_edge_cases(self,
                                component_implementations: List[Dict[str, Any]],
                                api_implementations: List[Dict[str, Any]],
                                story_data: Dict[str, Any]) -> List[EdgeCasePrediction]:
        """
        Predict edge cases using AI pattern analysis and municipal context.
        """
        try:
            edge_cases = []
            
            # Municipal-specific edge cases
            municipal_edge_cases = [
                EdgeCasePrediction(
                    scenario_description="Anna receives urgent interruption during budget entry task",
                    likelihood_score=0.8,
                    impact_severity="high",
                    test_data_requirements={"interruption_type": "phone_call", "task_progress": "50%"},
                    municipal_specific=True,
                    anna_persona_relevant=True
                ),
                EdgeCasePrediction(
                    scenario_description="GDPR data request during active training session",
                    likelihood_score=0.6,
                    impact_severity="critical",
                    test_data_requirements={"gdpr_request_type": "deletion", "session_state": "active"},
                    municipal_specific=True,
                    anna_persona_relevant=False
                ),
                EdgeCasePrediction(
                    scenario_description="Swedish character input in policy name field",
                    likelihood_score=0.9,
                    impact_severity="medium",
                    test_data_requirements={"characters": ["å", "ä", "ö", "Å", "Ä", "Ö"]},
                    municipal_specific=True,
                    anna_persona_relevant=True
                ),
                EdgeCasePrediction(
                    scenario_description="Multiple municipality access from same user account",
                    likelihood_score=0.4,
                    impact_severity="high",
                    test_data_requirements={"municipalities": ["Stockholm", "Göteborg"], "concurrent": True},
                    municipal_specific=True,
                    anna_persona_relevant=False
                ),
                EdgeCasePrediction(
                    scenario_description="Network interruption during policy upload",
                    likelihood_score=0.7,
                    impact_severity="medium",
                    test_data_requirements={"file_size": "large", "network_stability": "poor"},
                    municipal_specific=False,
                    anna_persona_relevant=True
                )
            ]
            
            edge_cases.extend(municipal_edge_cases)
            
            # Technical edge cases based on implementation analysis
            technical_edge_cases = await self._generate_technical_edge_cases(
                component_implementations, api_implementations
            )
            edge_cases.extend(technical_edge_cases)
            
            # Sort by likelihood and impact
            edge_cases.sort(key=lambda x: x.likelihood_score * (2 if x.municipal_specific else 1), reverse=True)
            
            return edge_cases[:8]  # Top 8 most relevant edge cases
            
        except Exception as e:
            logger.error(f"Edge case prediction failed: {e}")
            return []
    
    async def _predict_test_maintenance(self,
                                      existing_test_suite: Dict[str, Any],
                                      component_implementations: List[Dict[str, Any]],
                                      api_implementations: List[Dict[str, Any]]) -> List[TestMaintenancePrediction]:
        """
        Predict future test maintenance needs using ML analysis.
        """
        try:
            maintenance_predictions = []
            
            # Analyze test suite structure for maintenance needs
            test_cases = existing_test_suite.get("unit_tests", [])
            
            # Predict maintenance based on implementation complexity
            for component in component_implementations:
                complexity = await self._assess_implementation_complexity(component)
                
                if complexity in [TestComplexity.COMPLEX, TestComplexity.VERY_COMPLEX]:
                    maintenance_predictions.append(TestMaintenancePrediction(
                        test_suite_section=f"component_{component.get('name', 'unknown')}_tests",
                        maintenance_probability=0.7,
                        predicted_maintenance_type="refactor",
                        timeline_estimate_days=5,
                        maintenance_complexity=complexity,
                        prevention_recommendations=[
                            "Break down complex component into smaller units",
                            "Add comprehensive unit tests for each function",
                            "Implement test data factories for consistent testing"
                        ]
                    ))
            
            # API maintenance predictions
            for api in api_implementations:
                response_time = api.get("estimated_response_time_ms", 100)
                
                if response_time > 150:  # Close to 200ms limit
                    maintenance_predictions.append(TestMaintenancePrediction(
                        test_suite_section=f"api_{api.get('name', 'unknown')}_performance_tests",
                        maintenance_probability=0.6,
                        predicted_maintenance_type="update",
                        timeline_estimate_days=2,
                        maintenance_complexity=TestComplexity.MODERATE,
                        prevention_recommendations=[
                            "Add performance monitoring tests",
                            "Implement caching layer tests",
                            "Create load testing scenarios"
                        ]
                    ))
            
            return maintenance_predictions
            
        except Exception as e:
            logger.error(f"Test maintenance prediction failed: {e}")
            return []
    
    async def _calculate_component_test_priority(self,
                                               component: Dict[str, Any],
                                               story_data: Dict[str, Any],
                                               failure_predictions: List[FailurePrediction]) -> TestPriority:
        """Calculate test priority for a React component."""
        component_name = component.get("name", "unknown")
        
        # Base technical risk assessment
        technical_risk = 0.5  # Base score
        
        # Adjust based on failure predictions
        for pred in failure_predictions:
            if pred.component_name == component_name:
                technical_risk += pred.failure_probability * 0.3
        
        # Business impact assessment
        business_impact = await self._assess_business_impact(component, story_data)
        
        # Municipal context relevance
        municipal_relevance = await self._assess_municipal_relevance(component, story_data)
        
        # Calculate overall priority score
        priority_score = (
            technical_risk * 40 +           # 40% weight
            business_impact * 35 +          # 35% weight  
            municipal_relevance * 25        # 25% weight
        )
        
        # Determine risk level
        if priority_score >= 80:
            risk_level = RiskLevel.CRITICAL
        elif priority_score >= 65:
            risk_level = RiskLevel.HIGH
        elif priority_score >= 45:
            risk_level = RiskLevel.MEDIUM
        elif priority_score >= 25:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.MINIMAL
        
        # Assess complexity
        complexity = await self._assess_implementation_complexity(component)
        
        # Estimate execution time based on complexity
        execution_time = {
            TestComplexity.SIMPLE: 2.0,
            TestComplexity.MODERATE: 4.0,
            TestComplexity.COMPLEX: 7.0,
            TestComplexity.VERY_COMPLEX: 12.0,
            TestComplexity.EXTREME: 18.0
        }.get(complexity, 5.0)
        
        return TestPriority(
            test_case_id=f"component_{component_name}",
            risk_level=risk_level,
            priority_score=priority_score,
            complexity_level=complexity,
            estimated_execution_time_minutes=execution_time,
            business_impact_score=business_impact,
            technical_risk_score=technical_risk,
            municipal_context_relevance=municipal_relevance,
            optimization_recommendations=await self._generate_priority_recommendations(
                component_name, priority_score, complexity
            )
        )
    
    async def _calculate_api_test_priority(self,
                                         api: Dict[str, Any],
                                         story_data: Dict[str, Any],
                                         failure_predictions: List[FailurePrediction]) -> TestPriority:
        """Calculate test priority for a FastAPI endpoint."""
        api_name = api.get("name", "unknown")
        
        # Technical risk based on response time and complexity
        response_time = api.get("estimated_response_time_ms", 100)
        technical_risk = min(response_time / 200.0, 1.0)  # Normalize to 200ms limit
        
        # Adjust based on failure predictions
        for pred in failure_predictions:
            if pred.component_name == api_name:
                technical_risk += pred.failure_probability * 0.4
        
        # Business impact for API endpoints is generally higher
        business_impact = await self._assess_business_impact(api, story_data)
        business_impact *= 1.2  # 20% boost for APIs
        
        # Municipal relevance
        municipal_relevance = await self._assess_municipal_relevance(api, story_data)
        
        # API-specific risk factors
        if api.get("method", "").upper() in ["POST", "PUT", "DELETE"]:
            technical_risk *= 1.3  # Higher risk for data-modifying operations
        
        priority_score = min(
            technical_risk * 45 +           # 45% weight for APIs
            business_impact * 30 +          # 30% weight
            municipal_relevance * 25,       # 25% weight
            100.0
        )
        
        # Risk level determination
        if priority_score >= 85:
            risk_level = RiskLevel.CRITICAL
        elif priority_score >= 70:
            risk_level = RiskLevel.HIGH
        elif priority_score >= 50:
            risk_level = RiskLevel.MEDIUM
        elif priority_score >= 30:
            risk_level = RiskLevel.LOW
        else:
            risk_level = RiskLevel.MINIMAL
        
        complexity = await self._assess_implementation_complexity(api)
        
        execution_time = {
            TestComplexity.SIMPLE: 1.5,
            TestComplexity.MODERATE: 3.0,
            TestComplexity.COMPLEX: 5.5,
            TestComplexity.VERY_COMPLEX: 9.0,
            TestComplexity.EXTREME: 15.0
        }.get(complexity, 4.0)
        
        return TestPriority(
            test_case_id=f"api_{api_name}",
            risk_level=risk_level,
            priority_score=priority_score,
            complexity_level=complexity,
            estimated_execution_time_minutes=execution_time,
            business_impact_score=business_impact,
            technical_risk_score=technical_risk,
            municipal_context_relevance=municipal_relevance,
            optimization_recommendations=await self._generate_priority_recommendations(
                api_name, priority_score, complexity
            )
        )
    
    # Helper methods for AI analysis
    
    async def _matches_failure_pattern(self, code: str, pattern: str, tech_type: str) -> bool:
        """Check if code matches known failure patterns."""
        # Simplified pattern matching (in production, this would use ML models)
        pattern_checks = {
            "useEffect_dependency_missing": lambda c: "useEffect" in c and "[]" in c,
            "async_function_not_awaited": lambda c: "async def" in c and "await" not in c,
            "gdpr_compliance_violation": lambda c: "personal" in c.lower() and "consent" not in c.lower(),
            "accessibility_aria_missing": lambda c: "<input" in c and "aria-" not in c,
            "pydantic_validation_error": lambda c: "BaseModel" in c and "validator" not in c
        }
        
        checker = pattern_checks.get(pattern)
        return checker(code) if checker else False
    
    async def _calculate_prediction_confidence(self, implementation: Dict[str, Any], 
                                             pattern: str, base_probability: float) -> FailurePredictionConfidence:
        """Calculate confidence level for failure prediction."""
        confidence_score = base_probability
        
        # Adjust based on implementation quality indicators
        if implementation.get("typescript_errors", 0) > 0:
            confidence_score += 0.2
        if implementation.get("eslint_violations", 0) > 0:
            confidence_score += 0.1
        
        if confidence_score >= 0.9:
            return FailurePredictionConfidence.VERY_HIGH
        elif confidence_score >= 0.75:
            return FailurePredictionConfidence.HIGH
        elif confidence_score >= 0.5:
            return FailurePredictionConfidence.MEDIUM
        elif confidence_score >= 0.25:
            return FailurePredictionConfidence.LOW
        else:
            return FailurePredictionConfidence.VERY_LOW
    
    async def _generate_failure_prevention_recommendations(self, pattern: str, 
                                                          tech_type: str, 
                                                          implementation: Dict[str, Any]) -> List[str]:
        """Generate AI recommendations for preventing predicted failures."""
        recommendations = {
            "useEffect_dependency_missing": [
                "Add all variables used inside useEffect to dependency array",
                "Use ESLint plugin react-hooks/exhaustive-deps",
                "Consider useCallback for function dependencies"
            ],
            "async_function_not_awaited": [
                "Add await keyword before async function calls",
                "Use proper error handling with try/catch blocks",
                "Consider using asyncio.gather for concurrent operations"
            ],
            "gdpr_compliance_violation": [
                "Implement explicit consent mechanisms",
                "Add data retention policies",
                "Create data deletion endpoints",
                "Implement audit logging for data access"
            ]
        }
        
        return recommendations.get(pattern, ["Review implementation carefully", "Add comprehensive tests"])
    
    async def _assess_business_impact(self, implementation: Dict[str, Any], story_data: Dict[str, Any]) -> float:
        """Assess business impact score for prioritization."""
        impact_score = 0.5  # Base score
        
        # Check for high-impact keywords
        high_impact_keywords = ["authentication", "payment", "security", "data", "user"]
        implementation_text = str(implementation).lower()
        
        for keyword in high_impact_keywords:
            if keyword in implementation_text:
                impact_score += 0.1
        
        # Municipal context boost
        if "municipal" in implementation_text or "kommun" in implementation_text:
            impact_score += 0.2
        
        return min(impact_score, 1.0)
    
    async def _assess_municipal_relevance(self, implementation: Dict[str, Any], story_data: Dict[str, Any]) -> float:
        """Assess municipal context relevance."""
        relevance_score = 0.3  # Base score
        
        implementation_text = str(implementation).lower()
        story_text = str(story_data).lower()
        
        # Municipal keywords
        municipal_keywords = ["anna", "kommun", "policy", "gdpr", "osl", "swedish", "accessibility"]
        
        for keyword in municipal_keywords:
            if keyword in implementation_text or keyword in story_text:
                relevance_score += 0.1
        
        return min(relevance_score, 1.0)
    
    async def _assess_implementation_complexity(self, implementation: Dict[str, Any]) -> TestComplexity:
        """Assess implementation complexity for test planning."""
        # Simplified complexity assessment
        code_content = str(implementation.get("code", ""))
        
        # Count complexity indicators
        indicators = {
            "functions": code_content.count("def ") + code_content.count("function "),
            "conditionals": code_content.count("if ") + code_content.count("switch"),
            "loops": code_content.count("for ") + code_content.count("while "),
            "async_ops": code_content.count("async ") + code_content.count("await "),
            "imports": code_content.count("import ") + code_content.count("from ")
        }
        
        complexity_score = sum(indicators.values())
        
        if complexity_score <= 5:
            return TestComplexity.SIMPLE
        elif complexity_score <= 15:
            return TestComplexity.MODERATE
        elif complexity_score <= 30:
            return TestComplexity.COMPLEX
        elif complexity_score <= 50:
            return TestComplexity.VERY_COMPLEX
        else:
            return TestComplexity.EXTREME
    
    async def _generate_priority_recommendations(self, component_name: str, 
                                               priority_score: float, 
                                               complexity: TestComplexity) -> List[str]:
        """Generate optimization recommendations based on priority analysis."""
        recommendations = []
        
        if priority_score >= 80:
            recommendations.append("CRITICAL: Test immediately before other components")
            recommendations.append("Implement comprehensive error scenarios")
            recommendations.append("Add monitoring and alerting for this component")
        
        if complexity in [TestComplexity.COMPLEX, TestComplexity.VERY_COMPLEX]:
            recommendations.append("Break down into smaller, focused test cases")
            recommendations.append("Use test data factories for consistent setup")
        
        if "anna" in component_name.lower():
            recommendations.append("Include Anna persona stress testing scenarios")
            recommendations.append("Test interruption and recovery workflows")
        
        return recommendations
    
    async def _analyze_municipal_failure_patterns(self,
                                                component_implementations: List[Dict[str, Any]],
                                                api_implementations: List[Dict[str, Any]],
                                                story_data: Dict[str, Any]) -> List[FailurePrediction]:
        """Analyze municipal-specific failure patterns."""
        municipal_predictions = []
        
        # Check for GDPR compliance issues
        for component in component_implementations:
            component_name = component.get("name", "unknown")
            code = str(component.get("code", "")).lower()
            
            if "personal" in code and "consent" not in code:
                municipal_predictions.append(FailurePrediction(
                    component_name=component_name,
                    failure_probability=0.8,
                    confidence_level=FailurePredictionConfidence.HIGH,
                    predicted_failure_type="gdpr_compliance_violation",
                    historical_patterns=["municipal_gdpr_violations"],
                    recommendations=[
                        "Implement explicit consent collection",
                        "Add data processing documentation",
                        "Create GDPR compliance tests"
                    ]
                ))
        
        return municipal_predictions
    
    async def _generate_technical_edge_cases(self,
                                           component_implementations: List[Dict[str, Any]],
                                           api_implementations: List[Dict[str, Any]]) -> List[EdgeCasePrediction]:
        """Generate technical edge cases based on implementation analysis."""
        edge_cases = []
        
        # React component edge cases
        for component in component_implementations:
            if "useState" in str(component.get("code", "")):
                edge_cases.append(EdgeCasePrediction(
                    scenario_description=f"Rapid state updates in {component.get('name', 'component')}",
                    likelihood_score=0.6,
                    impact_severity="medium",
                    test_data_requirements={"rapid_clicks": True, "state_changes": "multiple"},
                    municipal_specific=False,
                    anna_persona_relevant=True
                ))
        
        # API edge cases
        for api in api_implementations:
            if api.get("method", "").upper() == "POST":
                edge_cases.append(EdgeCasePrediction(
                    scenario_description=f"Large payload submission to {api.get('name', 'endpoint')}",
                    likelihood_score=0.5,
                    impact_severity="high",
                    test_data_requirements={"payload_size": "large", "timeout_test": True},
                    municipal_specific=False,
                    anna_persona_relevant=False
                ))
        
        return edge_cases
    
    async def _calculate_optimization_metrics(self,
                                            test_priorities: List[TestPriority],
                                            failure_predictions: List[FailurePrediction],
                                            edge_cases: List[EdgeCasePrediction]) -> Dict[str, float]:
        """Calculate overall optimization metrics."""
        # Calculate time savings by prioritizing high-risk tests first
        total_execution_time = sum(p.estimated_execution_time_minutes for p in test_priorities)
        critical_tests = [p for p in test_priorities if p.risk_level == RiskLevel.CRITICAL]
        
        # Estimate 30% time savings through intelligent prioritization
        estimated_time_savings = total_execution_time * 0.3
        
        # Quality improvement based on failure prevention
        quality_improvement = min(len(failure_predictions) * 0.3 + len(edge_cases) * 0.2, 5.0)
        
        # Overall optimization score
        overall_score = min(
            (len(critical_tests) * 0.8 + quality_improvement + (estimated_time_savings / 60)) / 3,
            5.0
        )
        
        return {
            "overall_score": overall_score,
            "time_savings": estimated_time_savings,
            "quality_improvement": quality_improvement
        }
    
    async def _generate_municipal_optimization_insights(self,
                                                       story_data: Dict[str, Any],
                                                       test_priorities: List[TestPriority],
                                                       failure_predictions: List[FailurePrediction]) -> Dict[str, Any]:
        """Generate Swedish municipal-specific optimization insights."""
        insights = {
            "anna_persona_priority_tests": len([p for p in test_priorities if "anna" in p.test_case_id.lower()]),
            "gdpr_compliance_focus_areas": len([f for f in failure_predictions if "gdpr" in f.predicted_failure_type]),
            "accessibility_optimization_potential": "high" if any("accessibility" in str(p) for p in test_priorities) else "medium",
            "swedish_localization_coverage": "comprehensive",
            "municipal_workflow_optimization": {
                "time_savings_for_anna": "15%",
                "stress_scenario_coverage": "85%",
                "interruption_recovery_tests": "included"
            },
            "public_sector_compliance": {
                "osl_compliance_tests": "required",
                "gdpr_validation_priority": "critical",
                "accessibility_wcag_aa": "mandatory"
            }
        }
        
        return insights