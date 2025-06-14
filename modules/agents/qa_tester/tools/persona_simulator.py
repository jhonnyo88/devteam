"""
PersonaSimulator - Anna persona simulation and testing tool.

PURPOSE:
Simulates Anna (municipal training coordinator) using the implemented features
to validate user experience, satisfaction, and task completion rates.

CRITICAL FUNCTIONALITY:
- Anna persona behavioral simulation
- Task completion time measurement
- User satisfaction scoring
- Learning effectiveness assessment
- User confusion and error tracking

ADAPTATION GUIDE:
=' To adapt for your project:
1. Update persona_characteristics for your target user
2. Modify simulation_scenarios for your use cases
3. Adjust satisfaction_metrics for your quality standards
4. Update time_constraints for your user requirements

CONTRACT PROTECTION:
This tool is critical for DigiNativa's user experience validation.
Changes must maintain consistency with Anna persona requirements.
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path


# Setup logging for this module
logger = logging.getLogger(__name__)


@dataclass
class SimulationScenario:
    """
    Represents a specific usage scenario for Anna persona testing.
    """
    scenario_id: str
    name: str
    description: str
    expected_completion_time_minutes: float
    required_actions: List[str]
    success_criteria: Dict[str, Any]
    difficulty_level: str  # "easy", "medium", "hard"
    persona_context: Dict[str, Any]


@dataclass
class PersonaSimulationResult:
    """
    Results from Anna persona simulation testing.
    """
    scenario_id: str
    completed_successfully: bool
    completion_time_minutes: float
    satisfaction_score: float  # 1-5 scale
    learning_effectiveness_score: float  # 1-5 scale
    confusion_incidents: List[str]
    error_recovery_attempts: int
    positive_feedback: List[str]
    improvement_suggestions: List[str]
    timestamp: str


class PersonaSimulator:
    """
    Simulates Anna persona usage patterns and validates user experience.
    
    Anna is a municipal training coordinator with intermediate digital skills
    who needs to complete training tasks within 10 minutes while maintaining
    professional efficiency and learning new policy implementations.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize PersonaSimulator.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        
        # Anna persona characteristics (DigiNativa specific)
        self.anna_characteristics = {
            "role": "Municipal training coordinator",
            "experience_level": "Intermediate with digital tools",
            "age_range": "35-50",
            "technology_comfort": "Comfortable but not expert",
            "time_constraints": "Very limited - max 10 minutes per task",
            "stress_tolerance": "Medium - handles normal workplace pressure",
            "multitasking_ability": "High - often interrupted during tasks",
            "learning_style": "Visual and hands-on learner",
            "motivation_factors": [
                "Professional efficiency",
                "Compliance requirements", 
                "Career development",
                "Team support"
            ],
            "frustration_triggers": [
                "Complex navigation",
                "Unclear instructions",
                "Time pressure",
                "Technical jargon",
                "Non-intuitive interfaces"
            ],
            "success_indicators": [
                "Quick task completion",
                "Clear understanding",
                "Confident usage",
                "Practical application"
            ],
            "accessibility_needs": [
                "Screen reader compatibility",
                "Keyboard navigation",
                "High contrast options",
                "Text scaling support"
            ]
        }
        
        # Simulation parameters
        self.max_task_duration_minutes = 10
        self.satisfaction_thresholds = {
            "excellent": 4.5,
            "good": 4.0,
            "acceptable": 3.5,
            "poor": 2.5
        }
        
        # Standard simulation scenarios for DigiNativa
        self.standard_scenarios = self._initialize_standard_scenarios()
        
        logger.info("PersonaSimulator initialized with Anna characteristics")
    
    def _initialize_standard_scenarios(self) -> List[SimulationScenario]:
        """
        Initialize standard simulation scenarios for Anna persona.
        
        Returns:
            List of standard simulation scenarios
        """
        scenarios = [
            SimulationScenario(
                scenario_id="anna_first_time_user",
                name="First-time User Experience",
                description="Anna's initial interaction with a new feature",
                expected_completion_time_minutes=8.0,
                required_actions=[
                    "Navigate to feature",
                    "Understand purpose",
                    "Complete primary task",
                    "Verify results"
                ],
                success_criteria={
                    "task_completion": True,
                    "time_under_limit": True,
                    "no_external_help": True,
                    "confidence_gained": True
                },
                difficulty_level="medium",
                persona_context={
                    "stress_level": "medium",
                    "time_pressure": "high",
                    "prior_knowledge": "minimal"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_routine_usage",
                name="Routine Task Completion",
                description="Anna using the feature as part of regular workflow",
                expected_completion_time_minutes=5.0,
                required_actions=[
                    "Quick navigation",
                    "Efficient task completion",
                    "Review and confirm"
                ],
                success_criteria={
                    "fast_completion": True,
                    "minimal_errors": True,
                    "workflow_integration": True
                },
                difficulty_level="easy",
                persona_context={
                    "stress_level": "low",
                    "time_pressure": "medium",
                    "prior_knowledge": "good"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_error_recovery",
                name="Error Recovery Scenario", 
                description="Anna recovering from mistakes or system errors",
                expected_completion_time_minutes=9.0,
                required_actions=[
                    "Encounter error",
                    "Understand error message",
                    "Take corrective action",
                    "Complete original task"
                ],
                success_criteria={
                    "error_understanding": True,
                    "successful_recovery": True,
                    "maintained_confidence": True
                },
                difficulty_level="hard",
                persona_context={
                    "stress_level": "high",
                    "time_pressure": "high",
                    "frustration_level": "medium"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_accessibility_usage",
                name="Accessibility-focused Usage",
                description="Anna using feature with accessibility aids",
                expected_completion_time_minutes=7.0,
                required_actions=[
                    "Enable accessibility features",
                    "Navigate with keyboard only",
                    "Complete task with screen reader",
                    "Verify accessibility compliance"
                ],
                success_criteria={
                    "accessibility_features_work": True,
                    "keyboard_navigation_complete": True,
                    "screen_reader_compatible": True
                },
                difficulty_level="medium",
                persona_context={
                    "accessibility_mode": True,
                    "assistive_technology": "screen_reader"
                }
            )
        ]
        
        # Add enhanced stress testing scenarios
        enhanced_scenarios = self._initialize_enhanced_stress_scenarios()
        scenarios.extend(enhanced_scenarios)
        
        return scenarios
    
    def _initialize_enhanced_stress_scenarios(self) -> List[SimulationScenario]:
        """
        Initialize enhanced stress testing scenarios for Anna persona.
        
        These scenarios test Anna under realistic municipal workplace stress
        conditions to ensure the system performs well under pressure.
        
        Returns:
            List of enhanced stress testing scenarios
        """
        scenarios = [
            SimulationScenario(
                scenario_id="anna_budget_deadline_stress",
                name="Budget Deadline Pressure",
                description="Anna completing training during budget season with urgent deadlines",
                expected_completion_time_minutes=6.0,
                required_actions=[
                    "Quick login under time pressure",
                    "Navigate directly to critical information",
                    "Complete training while monitoring time",
                    "Submit results before deadline"
                ],
                success_criteria={
                    "task_completion": True,
                    "time_under_limit": True,
                    "accuracy_maintained": True,
                    "stress_management": True
                },
                difficulty_level="hard",
                persona_context={
                    "stress_level": "very_high",
                    "time_pressure": "critical",
                    "interruptions": "high",
                    "external_pressure": "management_oversight"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_multiple_interruptions",
                name="Multiple Workplace Interruptions",
                description="Anna attempting to complete training while being frequently interrupted",
                expected_completion_time_minutes=12.0,  # Extended due to interruptions
                required_actions=[
                    "Start training task",
                    "Handle phone call interruption",
                    "Resume from where left off",
                    "Respond to colleague question",
                    "Complete original task",
                    "Verify nothing was missed"
                ],
                success_criteria={
                    "task_completion": True,
                    "resumption_success": True,
                    "data_integrity": True,
                    "patience_maintained": True
                },
                difficulty_level="very_hard",
                persona_context={
                    "stress_level": "high",
                    "concentration_level": "fragmented",
                    "interruption_frequency": "every_2_minutes",
                    "multitasking_demand": "high"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_system_slowdown_frustration",
                name="System Performance Issues",
                description="Anna dealing with slow system response during peak usage",
                expected_completion_time_minutes=10.0,
                required_actions=[
                    "Attempt normal navigation",
                    "Wait for slow page loads",
                    "Retry failed actions",
                    "Find alternative workflow",
                    "Complete task despite delays"
                ],
                success_criteria={
                    "task_completion": True,
                    "patience_demonstrated": True,
                    "alternative_strategy": True,
                    "maintained_professionalism": True
                },
                difficulty_level="hard",
                persona_context={
                    "stress_level": "high",
                    "frustration_level": "rising",
                    "time_pressure": "high",
                    "system_performance": "poor"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_crisis_management_training",
                name="Emergency Training Under Pressure",
                description="Anna completing crisis management training during actual emergency preparation",
                expected_completion_time_minutes=8.0,
                required_actions=[
                    "Access emergency procedures quickly",
                    "Learn new crisis protocols",
                    "Practice decision-making scenarios",
                    "Complete certification",
                    "Apply knowledge immediately"
                ],
                success_criteria={
                    "rapid_learning": True,
                    "knowledge_retention": True,
                    "practical_application": True,
                    "confidence_building": True
                },
                difficulty_level="very_hard",
                persona_context={
                    "stress_level": "critical",
                    "urgency": "immediate",
                    "stakes": "public_safety",
                    "pressure_source": "crisis_situation"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_monday_morning_rush",
                name="Monday Morning Information Overload",
                description="Anna catching up on weekend policy changes during Monday morning rush",
                expected_completion_time_minutes=9.0,
                required_actions=[
                    "Review weekend notifications",
                    "Prioritize urgent policy updates",
                    "Complete multiple training modules",
                    "Brief team on changes",
                    "Update procedures documentation"
                ],
                success_criteria={
                    "information_processing": True,
                    "prioritization_skills": True,
                    "team_communication": True,
                    "procedure_compliance": True
                },
                difficulty_level="hard",
                persona_context={
                    "stress_level": "high",
                    "information_overload": "high",
                    "time_pressure": "high",
                    "cognitive_load": "maximum"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_public_scrutiny_pressure",
                name="Training Under Public Scrutiny",
                description="Anna completing training while knowing public/media attention is on municipal compliance",
                expected_completion_time_minutes=7.0,
                required_actions=[
                    "Complete training with high attention to detail",
                    "Ensure full compliance understanding",
                    "Document completion properly",
                    "Verify all requirements met",
                    "Prepare for potential audit questions"
                ],
                success_criteria={
                    "perfect_completion": True,
                    "audit_readiness": True,
                    "documentation_quality": True,
                    "confidence_in_knowledge": True
                },
                difficulty_level="very_hard",
                persona_context={
                    "stress_level": "very_high",
                    "scrutiny_level": "public",
                    "accuracy_requirement": "perfect",
                    "consequences": "political_reputation"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_technology_adaptation_challenge",
                name="New Technology Adaptation",
                description="Anna learning to use updated interface while maintaining productivity",
                expected_completion_time_minutes=11.0,
                required_actions=[
                    "Explore new interface layout",
                    "Find familiar functions in new locations",
                    "Learn new workflow patterns",
                    "Complete tasks with new tools",
                    "Adapt existing knowledge"
                ],
                success_criteria={
                    "adaptation_success": True,
                    "workflow_efficiency": True,
                    "knowledge_transfer": True,
                    "continued_productivity": True
                },
                difficulty_level="medium",
                persona_context={
                    "stress_level": "medium",
                    "learning_curve": "steep",
                    "familiarity": "disrupted",
                    "support_available": "limited"
                }
            ),
            
            SimulationScenario(
                scenario_id="anna_concurrent_training_modules",
                name="Multiple Training Requirements",
                description="Anna managing multiple mandatory training deadlines simultaneously",
                expected_completion_time_minutes=15.0,  # Longer scenario
                required_actions=[
                    "Track multiple training requirements",
                    "Prioritize based on deadlines",
                    "Switch between different training types",
                    "Maintain progress across modules",
                    "Complete all requirements on time"
                ],
                success_criteria={
                    "multi_module_completion": True,
                    "deadline_management": True,
                    "context_switching": True,
                    "progress_tracking": True
                },
                difficulty_level="very_hard",
                persona_context={
                    "stress_level": "high",
                    "complexity": "multi_dimensional",
                    "cognitive_switching": "frequent",
                    "deadline_pressure": "multiple"
                }
            )
        ]
        
        return scenarios
    
    async def simulate_anna_usage(self, story_id: str, implementation_data: Dict[str, Any],
                                test_suite: Dict[str, Any], requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate Anna persona using the implemented feature.
        
        Args:
            story_id: Story identifier
            implementation_data: Feature implementation details
            test_suite: Test suite results
            requirements: Anna persona requirements
            
        Returns:
            Anna persona simulation results
        """
        try:
            logger.info(f"Starting Anna persona simulation for story: {story_id}")
            
            # Extract feature details
            ui_components = implementation_data.get("ui_components", [])
            api_endpoints = implementation_data.get("api_endpoints", [])
            user_flows = implementation_data.get("user_flows", [])
            
            # Run simulations for each scenario
            simulation_results = []
            
            for scenario in self.standard_scenarios:
                logger.debug(f"Running simulation scenario: {scenario.name}")
                
                result = await self._simulate_scenario(
                    scenario=scenario,
                    implementation_data=implementation_data,
                    story_id=story_id
                )
                
                simulation_results.append(result)
            
            # Calculate overall metrics
            overall_metrics = self._calculate_overall_metrics(simulation_results)
            
            # Generate detailed analysis
            detailed_analysis = await self._analyze_simulation_results(
                simulation_results, implementation_data, story_id
            )
            
            # Create comprehensive results
            anna_simulation_report = {
                "story_id": story_id,
                "persona": "Anna - Municipal Training Coordinator",
                "simulation_timestamp": datetime.now().isoformat(),
                "overall_metrics": overall_metrics,
                "scenario_results": [result.__dict__ for result in simulation_results],
                "detailed_analysis": detailed_analysis,
                "recommendations": await self._generate_persona_recommendations(
                    simulation_results, overall_metrics
                ),
                "anna_characteristics_validation": self._validate_anna_characteristics(
                    overall_metrics, requirements
                )
            }
            
            logger.info(f"Anna persona simulation completed for story: {story_id}")
            return anna_simulation_report
            
        except Exception as e:
            error_msg = f"Anna persona simulation failed for story {story_id}: {str(e)}"
            logger.error(error_msg)
            return {
                "error": error_msg,
                "story_id": story_id,
                "simulation_failed": True,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _simulate_scenario(self, scenario: SimulationScenario, 
                               implementation_data: Dict[str, Any], story_id: str) -> PersonaSimulationResult:
        """
        Simulate a specific scenario with Anna persona.
        
        Args:
            scenario: Simulation scenario to execute
            implementation_data: Implementation details
            story_id: Story identifier
            
        Returns:
            Simulation result for the scenario
        """
        try:
            start_time = datetime.now()
            
            # Simulate Anna's interaction patterns
            ui_components = implementation_data.get("ui_components", [])
            user_flows = implementation_data.get("user_flows", [])
            
            # Track simulation metrics
            completion_time = 0.0
            satisfaction_score = 5.0  # Start optimistic
            learning_effectiveness = 5.0
            confusion_incidents = []
            error_recovery_attempts = 0
            positive_feedback = []
            improvement_suggestions = []
            
            # Simulate each required action
            for action in scenario.required_actions:
                action_result = await self._simulate_action(
                    action, ui_components, scenario.persona_context
                )
                
                # Update metrics based on action result
                completion_time += action_result.get("time_taken_minutes", 1.0)
                satisfaction_score = min(satisfaction_score, action_result.get("satisfaction_impact", 5.0))
                
                if action_result.get("confusion_detected"):
                    confusion_incidents.append(action_result.get("confusion_reason", "Unknown"))
                
                if action_result.get("error_occurred"):
                    error_recovery_attempts += 1
                
                if action_result.get("positive_experience"):
                    positive_feedback.append(action_result.get("positive_reason", "Good experience"))
                
                if action_result.get("improvement_needed"):
                    improvement_suggestions.append(action_result.get("improvement_suggestion", "General improvement"))
            
            # Check success criteria
            completed_successfully = self._check_success_criteria(
                scenario.success_criteria, completion_time, confusion_incidents, error_recovery_attempts
            )
            
            # Calculate learning effectiveness
            learning_effectiveness = self._calculate_learning_effectiveness(
                scenario, completed_successfully, confusion_incidents, positive_feedback
            )
            
            # Adjust satisfaction based on Anna's characteristics
            satisfaction_score = self._adjust_satisfaction_for_anna(
                satisfaction_score, completion_time, confusion_incidents, scenario.persona_context
            )
            
            return PersonaSimulationResult(
                scenario_id=scenario.scenario_id,
                completed_successfully=completed_successfully,
                completion_time_minutes=completion_time,
                satisfaction_score=satisfaction_score,
                learning_effectiveness_score=learning_effectiveness,
                confusion_incidents=confusion_incidents,
                error_recovery_attempts=error_recovery_attempts,
                positive_feedback=positive_feedback,
                improvement_suggestions=improvement_suggestions,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            logger.error(f"Error simulating scenario {scenario.scenario_id}: {e}")
            return PersonaSimulationResult(
                scenario_id=scenario.scenario_id,
                completed_successfully=False,
                completion_time_minutes=999.0,
                satisfaction_score=1.0,
                learning_effectiveness_score=1.0,
                confusion_incidents=[f"Simulation error: {str(e)}"],
                error_recovery_attempts=99,
                positive_feedback=[],
                improvement_suggestions=["Fix simulation system"],
                timestamp=datetime.now().isoformat()
            )
    
    async def _simulate_action(self, action: str, ui_components: List[Dict[str, Any]], 
                             persona_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate Anna performing a specific action.
        
        Args:
            action: Action to simulate
            ui_components: Available UI components
            persona_context: Anna's current context
            
        Returns:
            Action simulation result
        """
        # Simplified simulation - in reality would be more sophisticated
        base_time = 1.0  # Base time for any action
        satisfaction_impact = 5.0
        confusion_detected = False
        error_occurred = False
        positive_experience = False
        improvement_needed = False
        
        # Analyze action complexity based on UI components
        action_complexity = self._assess_action_complexity(action, ui_components)
        
        # Adjust time based on Anna's characteristics and context
        if persona_context.get("stress_level") == "high":
            base_time *= 1.5
            satisfaction_impact -= 0.5
        
        if persona_context.get("prior_knowledge") == "minimal":
            base_time *= 2.0
            satisfaction_impact -= 1.0
            
        if action_complexity > 3:  # Scale 1-5
            confusion_detected = True
            satisfaction_impact -= 1.5
            improvement_needed = True
        
        # Anna appreciates clear, simple interfaces
        if action_complexity <= 2 and len(ui_components) <= 5:
            positive_experience = True
            satisfaction_impact += 0.5
        
        # Time pressure effects (Anna has max 10 minutes)
        if persona_context.get("time_pressure") == "high":
            if base_time > 2.0:
                satisfaction_impact -= 2.0
                confusion_detected = True
        
        return {
            "time_taken_minutes": base_time,
            "satisfaction_impact": satisfaction_impact,
            "confusion_detected": confusion_detected,
            "confusion_reason": "Complex interface" if confusion_detected else None,
            "error_occurred": error_occurred,
            "positive_experience": positive_experience,
            "positive_reason": "Clear and simple design" if positive_experience else None,
            "improvement_needed": improvement_needed,
            "improvement_suggestion": "Simplify interface" if improvement_needed else None
        }
    
    def _assess_action_complexity(self, action: str, ui_components: List[Dict[str, Any]]) -> int:
        """
        Assess complexity of an action based on UI components.
        
        Args:
            action: Action to assess
            ui_components: Available UI components
            
        Returns:
            Complexity score (1-5, where 1 is simple and 5 is complex)
        """
        # Simplified complexity assessment
        complexity = 1
        
        # Number of UI components adds complexity
        if len(ui_components) > 10:
            complexity += 2
        elif len(ui_components) > 5:
            complexity += 1
        
        # Form inputs add complexity
        form_components = [c for c in ui_components if c.get("type") in ["input", "select", "textarea"]]
        if len(form_components) > 5:
            complexity += 2
        elif len(form_components) > 2:
            complexity += 1
        
        # Navigation complexity
        if "navigate" in action.lower():
            if len(ui_components) > 7:
                complexity += 1
        
        return min(5, complexity)
    
    def _check_success_criteria(self, success_criteria: Dict[str, Any], completion_time: float,
                              confusion_incidents: List[str], error_recovery_attempts: int) -> bool:
        """
        Check if scenario success criteria are met.
        
        Args:
            success_criteria: Criteria to check
            completion_time: Total completion time
            confusion_incidents: List of confusion incidents
            error_recovery_attempts: Number of error recovery attempts
            
        Returns:
            True if all criteria are met
        """
        # Time limit check
        if success_criteria.get("time_under_limit", False):
            if completion_time > self.max_task_duration_minutes:
                return False
        
        # Fast completion check
        if success_criteria.get("fast_completion", False):
            if completion_time > 5.0:
                return False
        
        # No external help check
        if success_criteria.get("no_external_help", False):
            if len(confusion_incidents) > 2:
                return False
        
        # Minimal errors check
        if success_criteria.get("minimal_errors", False):
            if error_recovery_attempts > 1:
                return False
        
        # Error understanding check
        if success_criteria.get("error_understanding", False):
            if error_recovery_attempts > 0 and len(confusion_incidents) > error_recovery_attempts:
                return False
        
        return True
    
    def _calculate_learning_effectiveness(self, scenario: SimulationScenario, completed_successfully: bool,
                                        confusion_incidents: List[str], positive_feedback: List[str]) -> float:
        """
        Calculate learning effectiveness score for Anna.
        
        Args:
            scenario: Simulation scenario
            completed_successfully: Whether task was completed successfully
            confusion_incidents: List of confusion incidents
            positive_feedback: List of positive experiences
            
        Returns:
            Learning effectiveness score (1-5)
        """
        base_score = 3.0
        
        # Successful completion boosts learning
        if completed_successfully:
            base_score += 1.0
        
        # Positive experiences enhance learning
        base_score += len(positive_feedback) * 0.3
        
        # Confusion reduces learning effectiveness
        base_score -= len(confusion_incidents) * 0.5
        
        # Difficulty level affects learning potential
        if scenario.difficulty_level == "easy":
            base_score += 0.5  # Easy tasks build confidence
        elif scenario.difficulty_level == "hard":
            if completed_successfully:
                base_score += 1.0  # Successful hard tasks are very educational
            else:
                base_score -= 1.0  # Failed hard tasks are discouraging
        
        return max(1.0, min(5.0, base_score))
    
    def _adjust_satisfaction_for_anna(self, base_satisfaction: float, completion_time: float,
                                    confusion_incidents: List[str], persona_context: Dict[str, Any]) -> float:
        """
        Adjust satisfaction score based on Anna's specific characteristics.
        
        Args:
            base_satisfaction: Base satisfaction score
            completion_time: Task completion time
            confusion_incidents: List of confusion incidents
            persona_context: Anna's context
            
        Returns:
            Adjusted satisfaction score for Anna
        """
        satisfaction = base_satisfaction
        
        # Anna values efficiency - time is critical
        if completion_time <= 5.0:
            satisfaction += 1.0  # Quick completion makes Anna very happy
        elif completion_time <= 8.0:
            satisfaction += 0.5  # Reasonable time
        elif completion_time > 10.0:
            satisfaction -= 2.0  # Over time limit is very frustrating
        
        # Anna gets frustrated with confusion
        satisfaction -= len(confusion_incidents) * 0.8
        
        # Anna's stress level affects satisfaction
        if persona_context.get("stress_level") == "high":
            satisfaction -= 0.5
        elif persona_context.get("stress_level") == "low":
            satisfaction += 0.3
        
        # Anna appreciates accessibility features
        if persona_context.get("accessibility_mode"):
            if len(confusion_incidents) == 0:
                satisfaction += 0.5  # Accessibility working well
            else:
                satisfaction -= 1.0  # Accessibility issues are very frustrating
        
        return max(1.0, min(5.0, satisfaction))
    
    def _calculate_overall_metrics(self, simulation_results: List[PersonaSimulationResult]) -> Dict[str, Any]:
        """
        Calculate overall metrics from all simulation results.
        
        Args:
            simulation_results: List of simulation results
            
        Returns:
            Overall metrics summary
        """
        if not simulation_results:
            return {
                "error": "No simulation results available",
                "overall_satisfaction": 0.0,
                "average_completion_time": 0.0,
                "task_completion_rate": 0.0
            }
        
        # Calculate averages
        total_satisfaction = sum(result.satisfaction_score for result in simulation_results)
        total_completion_time = sum(result.completion_time_minutes for result in simulation_results)
        total_learning_effectiveness = sum(result.learning_effectiveness_score for result in simulation_results)
        
        successful_completions = sum(1 for result in simulation_results if result.completed_successfully)
        total_confusion_incidents = sum(len(result.confusion_incidents) for result in simulation_results)
        total_error_recoveries = sum(result.error_recovery_attempts for result in simulation_results)
        
        num_results = len(simulation_results)
        
        return {
            "satisfaction_score": round(total_satisfaction / num_results, 2),
            "average_completion_time_minutes": round(total_completion_time / num_results, 2),
            "learning_effectiveness_score": round(total_learning_effectiveness / num_results, 2),
            "task_completion_rate": round((successful_completions / num_results) * 100, 1),
            "total_confusion_incidents": total_confusion_incidents,
            "total_error_recovery_attempts": total_error_recoveries,
            "scenarios_tested": num_results,
            "time_constraint_violations": sum(1 for result in simulation_results 
                                            if result.completion_time_minutes > self.max_task_duration_minutes)
        }
    
    async def _analyze_simulation_results(self, simulation_results: List[PersonaSimulationResult],
                                        implementation_data: Dict[str, Any], story_id: str) -> Dict[str, Any]:
        """
        Analyze simulation results for detailed insights.
        
        Args:
            simulation_results: List of simulation results
            implementation_data: Implementation details
            story_id: Story identifier
            
        Returns:
            Detailed analysis of simulation results
        """
        try:
            # Identify patterns in Anna's experience
            time_violations = [r for r in simulation_results if r.completion_time_minutes > self.max_task_duration_minutes]
            confusion_patterns = {}
            satisfaction_issues = [r for r in simulation_results if r.satisfaction_score < self.satisfaction_thresholds["acceptable"]]
            
            # Analyze confusion patterns
            for result in simulation_results:
                for incident in result.confusion_incidents:
                    confusion_patterns[incident] = confusion_patterns.get(incident, 0) + 1
            
            # Identify most problematic areas
            most_confusing_elements = sorted(confusion_patterns.items(), 
                                           key=lambda x: x[1], reverse=True)[:3]
            
            # Analyze positive feedback patterns
            positive_patterns = {}
            for result in simulation_results:
                for feedback in result.positive_feedback:
                    positive_patterns[feedback] = positive_patterns.get(feedback, 0) + 1
            
            strongest_features = sorted(positive_patterns.items(), 
                                      key=lambda x: x[1], reverse=True)[:3]
            
            return {
                "time_constraint_analysis": {
                    "violations_count": len(time_violations),
                    "average_violation_time": round(
                        sum(r.completion_time_minutes for r in time_violations) / len(time_violations), 2
                    ) if time_violations else 0,
                    "scenarios_with_violations": [r.scenario_id for r in time_violations]
                },
                "confusion_analysis": {
                    "total_incidents": sum(confusion_patterns.values()),
                    "most_confusing_elements": most_confusing_elements,
                    "confusion_free_scenarios": [r.scenario_id for r in simulation_results 
                                                if len(r.confusion_incidents) == 0]
                },
                "satisfaction_analysis": {
                    "low_satisfaction_scenarios": [r.scenario_id for r in satisfaction_issues],
                    "average_satisfaction_by_scenario": {
                        r.scenario_id: r.satisfaction_score for r in simulation_results
                    },
                    "satisfaction_distribution": self._calculate_satisfaction_distribution(simulation_results)
                },
                "positive_experience_analysis": {
                    "strongest_features": strongest_features,
                    "scenarios_with_positive_feedback": [
                        r.scenario_id for r in simulation_results if r.positive_feedback
                    ]
                },
                "anna_specific_insights": {
                    "time_pressure_impact": self._analyze_time_pressure_impact(simulation_results),
                    "learning_curve_assessment": self._analyze_learning_curve(simulation_results),
                    "accessibility_performance": self._analyze_accessibility_performance(simulation_results)
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing simulation results: {e}")
            return {
                "error": str(e),
                "analysis_failed": True
            }
    
    def _calculate_satisfaction_distribution(self, simulation_results: List[PersonaSimulationResult]) -> Dict[str, int]:
        """Calculate distribution of satisfaction scores."""
        distribution = {"excellent": 0, "good": 0, "acceptable": 0, "poor": 0, "very_poor": 0}
        
        for result in simulation_results:
            score = result.satisfaction_score
            if score >= self.satisfaction_thresholds["excellent"]:
                distribution["excellent"] += 1
            elif score >= self.satisfaction_thresholds["good"]:
                distribution["good"] += 1
            elif score >= self.satisfaction_thresholds["acceptable"]:
                distribution["acceptable"] += 1
            elif score >= self.satisfaction_thresholds["poor"]:
                distribution["poor"] += 1
            else:
                distribution["very_poor"] += 1
        
        return distribution
    
    def _analyze_time_pressure_impact(self, simulation_results: List[PersonaSimulationResult]) -> Dict[str, Any]:
        """Analyze how time pressure affects Anna's performance."""
        time_pressure_scenarios = [r for r in simulation_results 
                                 if r.completion_time_minutes > 7.0]  # High time pressure threshold
        
        if not time_pressure_scenarios:
            return {"no_time_pressure_detected": True}
        
        avg_satisfaction_under_pressure = sum(r.satisfaction_score for r in time_pressure_scenarios) / len(time_pressure_scenarios)
        avg_errors_under_pressure = sum(r.error_recovery_attempts for r in time_pressure_scenarios) / len(time_pressure_scenarios)
        
        return {
            "scenarios_with_time_pressure": len(time_pressure_scenarios),
            "average_satisfaction_under_pressure": round(avg_satisfaction_under_pressure, 2),
            "average_errors_under_pressure": round(avg_errors_under_pressure, 2),
            "time_pressure_impact_severity": "high" if avg_satisfaction_under_pressure < 3.0 else "medium"
        }
    
    def _analyze_learning_curve(self, simulation_results: List[PersonaSimulationResult]) -> Dict[str, Any]:
        """Analyze Anna's learning effectiveness across scenarios."""
        learning_scores = [r.learning_effectiveness_score for r in simulation_results]
        
        if not learning_scores:
            return {"no_learning_data": True}
        
        avg_learning = sum(learning_scores) / len(learning_scores)
        learning_improvement = learning_scores[-1] - learning_scores[0] if len(learning_scores) > 1 else 0
        
        return {
            "average_learning_effectiveness": round(avg_learning, 2),
            "learning_improvement_trend": round(learning_improvement, 2),
            "strong_learning_scenarios": [
                r.scenario_id for r in simulation_results 
                if r.learning_effectiveness_score >= 4.0
            ],
            "learning_challenges": [
                r.scenario_id for r in simulation_results
                if r.learning_effectiveness_score < 3.0
            ]
        }
    
    def _analyze_accessibility_performance(self, simulation_results: List[PersonaSimulationResult]) -> Dict[str, Any]:
        """Analyze accessibility-related performance."""
        accessibility_scenarios = [r for r in simulation_results 
                                 if "accessibility" in r.scenario_id.lower()]
        
        if not accessibility_scenarios:
            return {"no_accessibility_testing": True}
        
        accessibility_satisfaction = sum(r.satisfaction_score for r in accessibility_scenarios) / len(accessibility_scenarios)
        accessibility_completion_rate = sum(1 for r in accessibility_scenarios 
                                          if r.completed_successfully) / len(accessibility_scenarios) * 100
        
        return {
            "accessibility_satisfaction_score": round(accessibility_satisfaction, 2),
            "accessibility_completion_rate": round(accessibility_completion_rate, 1),
            "accessibility_specific_issues": [
                incident for r in accessibility_scenarios 
                for incident in r.confusion_incidents
            ]
        }
    
    async def _generate_persona_recommendations(self, simulation_results: List[PersonaSimulationResult],
                                              overall_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on Anna persona simulation results.
        
        Args:
            simulation_results: List of simulation results
            overall_metrics: Overall metrics
            
        Returns:
            List of recommendations for improving Anna's experience
        """
        recommendations = []
        
        try:
            # Time constraint recommendations
            if overall_metrics.get("time_constraint_violations", 0) > 0:
                recommendations.append({
                    "category": "time_optimization",
                    "priority": "high",
                    "issue": f"Anna exceeded 10-minute time limit in {overall_metrics.get('time_constraint_violations')} scenarios",
                    "recommendation": "Streamline user workflows and reduce cognitive load to respect Anna's time constraints",
                    "expected_impact": "Improved task completion within time limits",
                    "anna_specific": True
                })
            
            # Satisfaction recommendations
            if overall_metrics.get("satisfaction_score", 0) < self.satisfaction_thresholds["good"]:
                recommendations.append({
                    "category": "user_satisfaction",
                    "priority": "high",
                    "issue": f"Anna's satisfaction score ({overall_metrics.get('satisfaction_score')}) below target (4.0)",
                    "recommendation": "Improve interface clarity and reduce complexity for intermediate users like Anna",
                    "expected_impact": "Higher user satisfaction and confidence",
                    "anna_specific": True
                })
            
            # Confusion incident recommendations
            if overall_metrics.get("total_confusion_incidents", 0) > 3:
                recommendations.append({
                    "category": "usability",
                    "priority": "medium",
                    "issue": f"Anna experienced {overall_metrics.get('total_confusion_incidents')} confusion incidents",
                    "recommendation": "Simplify navigation and provide clearer instructions for municipal users",
                    "expected_impact": "Reduced confusion and faster task completion",
                    "anna_specific": True
                })
            
            # Learning effectiveness recommendations
            if overall_metrics.get("learning_effectiveness_score", 0) < 4.0:
                recommendations.append({
                    "category": "learning_experience",
                    "priority": "medium",
                    "issue": f"Learning effectiveness score ({overall_metrics.get('learning_effectiveness_score')}) below target",
                    "recommendation": "Add more contextual help and practical examples relevant to municipal training",
                    "expected_impact": "Enhanced learning outcomes for training coordinators",
                    "anna_specific": True
                })
            
            # Error recovery recommendations
            if overall_metrics.get("total_error_recovery_attempts", 0) > 2:
                recommendations.append({
                    "category": "error_handling",
                    "priority": "medium",
                    "issue": f"Anna required {overall_metrics.get('total_error_recovery_attempts')} error recovery attempts",
                    "recommendation": "Improve error messages and recovery paths for non-technical users",
                    "expected_impact": "Smoother error recovery and maintained user confidence",
                    "anna_specific": True
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating persona recommendations: {e}")
            return [{
                "category": "system_error",
                "priority": "high",
                "issue": "Failed to generate persona recommendations",
                "recommendation": "Review persona simulation system",
                "error": str(e)
            }]
    
    def _validate_anna_characteristics(self, overall_metrics: Dict[str, Any], 
                                     requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that feature meets Anna's specific characteristics and requirements.
        
        Args:
            overall_metrics: Overall simulation metrics
            requirements: Anna persona requirements
            
        Returns:
            Validation results for Anna's characteristics
        """
        validation_results = {}
        
        # Time availability validation (10 minutes max)
        time_compliance = overall_metrics.get("average_completion_time_minutes", 999) <= 10
        validation_results["time_availability_respected"] = time_compliance
        
        # Technology comfort validation (intermediate level)
        satisfaction_meets_intermediate = overall_metrics.get("satisfaction_score", 0) >= 3.5
        validation_results["technology_comfort_appropriate"] = satisfaction_meets_intermediate
        
        # Professional efficiency validation
        task_completion_rate = overall_metrics.get("task_completion_rate", 0)
        efficiency_acceptable = task_completion_rate >= 90
        validation_results["professional_efficiency_maintained"] = efficiency_acceptable
        
        # Learning effectiveness validation
        learning_score = overall_metrics.get("learning_effectiveness_score", 0)
        learning_effective = learning_score >= requirements.get("success_metrics", {}).get("learning_effectiveness", 4)
        validation_results["learning_effectiveness_achieved"] = learning_effective
        
        # Overall Anna persona compatibility
        validation_results["anna_persona_compatible"] = all([
            time_compliance,
            satisfaction_meets_intermediate,
            efficiency_acceptable,
            learning_effective
        ])
        
        validation_results["validation_summary"] = {
            "total_criteria": 4,
            "criteria_met": sum([time_compliance, satisfaction_meets_intermediate, 
                               efficiency_acceptable, learning_effective]),
            "validation_percentage": round(sum([time_compliance, satisfaction_meets_intermediate,
                                              efficiency_acceptable, learning_effective]) / 4 * 100, 1)
        }
        
        return validation_results