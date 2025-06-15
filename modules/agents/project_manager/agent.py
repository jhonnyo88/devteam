"""
Project Manager Agent - First working agent in the DigiNativa AI Team system.

PURPOSE:
Analyzes GitHub feature requests and creates DNA-compliant story breakdowns
that guide the entire development team workflow.

CRITICAL IMPORTANCE:
- Entry point for all feature development
- Ensures DNA compliance from the start
- Creates structured work breakdown for downstream agents
- Monitors and coordinates team progress

REVENUE IMPACT:
This agent directly impacts revenue by:
- Processing client feature requests efficiently
- Ensuring high-quality story breakdown that reduces rework
- Maintaining client satisfaction through proper requirements analysis
- Enabling predictable delivery timelines
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from ...shared.base_agent import BaseAgent, AgentExecutionResult
from ...shared.exceptions import (
    DNAComplianceError, BusinessLogicError, ExternalServiceError,
    AgentExecutionError
)
from ...shared.event_bus import EventBus
from .tools.github_integration import GitHubIntegration
from .tools.story_analyzer import StoryAnalyzer
from .tools.dna_compliance_checker import DNAComplianceChecker
from .tools.learning_engine import LearningEngine
from .tools.swedish_municipal_communicator import SwedishMunicipalCommunicator
from .tools.team_coordinator import TeamCoordinator
from .tools.stakeholder_relationship_manager import StakeholderRelationshipManager
from .tools.dna_story_validator import DNAStoryValidator


class ProjectManagerAgent(BaseAgent):
    """
    Project Manager agent for GitHub issue analysis and story breakdown.
    
    This agent serves as the entry point for all feature development,
    transforming GitHub issues into structured work breakdown that
    guides the entire AI team workflow.
    
    RESPONSIBILITIES:
    1. Monitor GitHub repositories for new feature requests
    2. Analyze feature requests against DNA principles
    3. Create detailed story breakdowns with acceptance criteria
    4. Generate contracts for Game Designer handoff
    5. Track feature progress throughout development lifecycle
    6. Ensure client requirements are properly captured and maintained
    """
    
    def __init__(self, agent_id: str = "pm-001", config: Optional[Dict[str, Any]] = None):
        """
        Initialize Project Manager Agent.
        
        Args:
            agent_id: Unique identifier for this agent instance
            config: Optional configuration dictionary
        """
        # Initialize with project_manager agent type
        super().__init__(agent_id, "project_manager", config)
        
        # Initialize specialized tools
        try:
            self.github_integration = GitHubIntegration(config)
            self.story_analyzer = StoryAnalyzer(config)
            self.dna_compliance_checker = DNAComplianceChecker(config)
            self.learning_engine = LearningEngine(config)
            self.swedish_communicator = SwedishMunicipalCommunicator(config)
            self.team_coordinator = TeamCoordinator(config)
            self.stakeholder_manager = StakeholderRelationshipManager(config)
            self.dna_story_validator = DNAStoryValidator(config)
            
            # Initialize EventBus for team coordination
            self.event_bus = EventBus(config)
            
            self.logger.info("Project Manager Agent tools (including EventBus) initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize PM Agent tools: {e}")
            raise AgentExecutionError(
                f"PM Agent initialization failed: {e}",
                agent_id=agent_id,
                execution_context={"config": config}
            )
        
        # Agent-specific configuration
        self.max_concurrent_stories = config.get("max_concurrent_stories", 5) if config else 5
        self.story_priority_threshold = config.get("story_priority_threshold", "medium") if config else "medium"
        
        # Initialize working directories
        self._ensure_working_directories()
        
        self.logger.info(f"Project Manager Agent {agent_id} initialized and ready")
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process GitHub feature request into structured story breakdown.
        
        This is the core business logic that transforms raw feature requests
        into actionable development work for the AI team.
        
        Args:
            input_contract: Contract containing GitHub feature request data
            
        Returns:
            Output contract for Game Designer with story breakdown
            
        Raises:
            BusinessLogicError: If feature request is invalid or incomplete
            DNAComplianceError: If feature violates DNA principles
            ExternalServiceError: If GitHub integration fails
        """
        try:
            story_id = input_contract.get("story_id")
            self.logger.info(f"Processing feature request for story: {story_id}")
            
            # Notify team that PM processing has started
            await self._notify_team_progress("story_analysis_started", {"story_id": story_id})
            
            # Step 1: Extract and validate feature request data
            feature_data = self._extract_feature_data(input_contract)
            
            # Step 2: Analyze against DNA principles
            self.logger.debug("Analyzing feature against DNA principles")
            dna_analysis = await self.dna_compliance_checker.analyze_feature_compliance(
                feature_data
            )
            
            if not dna_analysis["compliant"]:
                raise DNAComplianceError(
                    f"Feature violates DNA principles: {dna_analysis['violations']}",
                    violated_principles=dna_analysis["violations"],
                    agent_type=self.agent_type
                )
            
            # Step 3: Create comprehensive story breakdown
            self.logger.debug("Creating story breakdown")
            story_breakdown = await self.story_analyzer.create_story_breakdown(
                feature_data,
                dna_analysis
            )
            
            # Step 4: Generate acceptance criteria
            acceptance_criteria = await self.story_analyzer.generate_acceptance_criteria(
                feature_data,
                story_breakdown
            )
            
            # Notify GitHub issue processed
            await self._notify_team_progress("github_issue_processed", {"story_id": story_id})
            await self._notify_team_progress("story_breakdown_complete", {"story_id": story_id})
            
            # Step 5: Estimate complexity and timeline (Enhanced with ML)
            traditional_complexity = await self.story_analyzer.assess_complexity(
                story_breakdown
            )
            
            # Step 5b: Get ML-enhanced complexity prediction
            try:
                ml_prediction = await self.learning_engine.predict_complexity_with_ml(
                    story_breakdown, traditional_complexity
                )
                complexity_assessment = self._merge_complexity_predictions(
                    traditional_complexity, ml_prediction
                )
            except Exception as e:
                self.logger.warning(f"ML complexity prediction failed, using traditional: {e}")
                complexity_assessment = traditional_complexity
            
            await self._notify_team_progress("complexity_analysis_complete", {"story_id": story_id})
            
            # Step 5c: Validate story DNA compliance (NEW)
            self.logger.info("Validating story DNA compliance")
            learning_objectives = feature_data.get("learning_objectives", [])
            dna_validation_result = await self.dna_story_validator.validate_story_dna_compliance(
                feature_data,
                story_breakdown,
                acceptance_criteria,
                learning_objectives
            )
            
            # Log DNA compliance violations but don't fail - allow for revision workflow
            if not dna_validation_result.overall_dna_compliant:
                self.logger.warning(f"Story DNA compliance validation found violations")
                for violation in dna_validation_result.story_complexity_result.complexity_violations:
                    self.logger.warning(f"DNA violation: {violation}")
                for violation in dna_validation_result.learning_effectiveness_result.effectiveness_violations:
                    self.logger.warning(f"DNA violation: {violation}")
                for violation in dna_validation_result.communication_quality_result.communication_violations:
                    self.logger.warning(f"DNA violation: {violation}")
            
            # Step 6: Create Game Designer handoff contract
            output_contract = self._create_game_designer_contract(
                story_id,
                feature_data,
                story_breakdown,
                acceptance_criteria,
                complexity_assessment,
                dna_analysis,
                dna_validation_result
            )
            
            # Step 7: Save story documentation
            await self._save_story_documentation(
                story_id,
                feature_data,
                story_breakdown,
                acceptance_criteria,
                complexity_assessment
            )
            
            # Step 8: Coordinate team workflow (NEW)
            try:
                team_coordination = await self.team_coordinator.coordinate_team_workflow(
                    story_id, output_contract
                )
                output_contract['team_coordination'] = team_coordination
            except Exception as e:
                self.logger.warning(f"Team coordination failed, continuing without: {e}")
            
            await self._notify_team_progress("stakeholder_communication_sent", {"story_id": story_id})
            
            # Final completion notification
            await self._notify_team_progress("pm_processing_complete", {
                "story_id": story_id,
                "status": "ready_for_game_designer"
            })
            
            self.logger.info(f"Successfully processed story: {story_id}")
            return output_contract
            
        except DNAComplianceError:
            # Re-raise DNA compliance errors as-is
            raise
            
        except ExternalServiceError:
            # Re-raise external service errors as-is  
            raise
            
        except BusinessLogicError:
            # Re-raise business logic errors as-is
            raise
            
        except Exception as e:
            # Notify team of failure
            await self._notify_team_progress("pm_processing_failed", {
                "story_id": story_id,
                "error": str(e)
            })
            
            # Wrap unexpected errors
            self.logger.error(f"Unexpected error processing contract: {e}")
            raise AgentExecutionError(
                f"Failed to process feature request: {e}",
                agent_id=self.agent_id,
                story_id=input_contract.get("story_id"),
                execution_context={"input_contract": input_contract}
            )
    
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """
        Check Project Manager specific quality gates.
        
        Args:
            gate: Quality gate identifier
            deliverables: Deliverable data to validate
            
        Returns:
            True if quality gate passes, False otherwise
        """
        quality_checks = {
            "dna_compliance_verified": self._check_dna_compliance_gate,
            "story_breakdown_complete": self._check_story_breakdown_gate,
            "acceptance_criteria_clear": self._check_acceptance_criteria_gate,
            "game_designer_handoff_ready": self._check_handoff_ready_gate,
            "technical_feasibility_confirmed": self._check_technical_feasibility_gate
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
    
    def _extract_feature_data(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract and validate feature data from input contract.
        
        Args:
            input_contract: Input contract from GitHub or external source
            
        Returns:
            Structured feature data dictionary
            
        Raises:
            BusinessLogicError: If required data is missing or invalid
        """
        try:
            required_data = input_contract.get("input_requirements", {}).get("required_data", {})
            
            # Validate required fields
            required_fields = [
                "feature_description", "acceptance_criteria", "user_persona",
                "priority_level"
            ]
            
            for field in required_fields:
                if field not in required_data:
                    raise BusinessLogicError(
                        f"Missing required field: {field}",
                        business_rule="feature_data_completeness",
                        context={"missing_field": field, "available_fields": list(required_data.keys())}
                    )
            
            # Extract and structure feature data
            feature_data = {
                "feature_description": required_data["feature_description"],
                "acceptance_criteria": required_data["acceptance_criteria"],
                "user_persona": required_data["user_persona"],
                "priority_level": required_data["priority_level"],
                "time_constraint_minutes": required_data.get("time_constraint_minutes", 10),
                "learning_objectives": required_data.get("learning_objectives", []),
                "gdd_section_reference": required_data.get("gdd_section_reference", ""),
                "github_issue_url": required_data.get("github_issue_url", ""),
                "requested_by": required_data.get("requested_by", "unknown"),
                "created_at": required_data.get("created_at", datetime.now().isoformat())
            }
            
            # Validate priority level
            valid_priorities = ["low", "medium", "high", "critical"]
            if feature_data["priority_level"] not in valid_priorities:
                raise BusinessLogicError(
                    f"Invalid priority level: {feature_data['priority_level']}",
                    business_rule="valid_priority_levels",
                    context={"provided": feature_data["priority_level"], "valid": valid_priorities}
                )
            
            # Validate user persona
            valid_personas = ["Anna"]  # DigiNativa's primary persona
            if feature_data["user_persona"] not in valid_personas:
                self.logger.warning(f"Unknown user persona: {feature_data['user_persona']}")
            
            return feature_data
            
        except BusinessLogicError:
            # Re-raise business logic errors as-is
            raise
            
        except Exception as e:
            raise BusinessLogicError(
                f"Failed to extract feature data: {e}",
                business_rule="feature_data_extraction",
                context={"input_contract": input_contract}
            )
    
    def _create_game_designer_contract(
        self,
        story_id: str,
        feature_data: Dict[str, Any],
        story_breakdown: Dict[str, Any],
        acceptance_criteria: List[str],
        complexity_assessment: Dict[str, Any],
        dna_analysis: Dict[str, Any],
        dna_validation_result: Any = None
    ) -> Dict[str, Any]:
        """
        Create output contract for Game Designer handoff.
        
        Args:
            story_id: Story identifier
            feature_data: Original feature request data
            story_breakdown: Analyzed story breakdown
            acceptance_criteria: Generated acceptance criteria
            complexity_assessment: Complexity and timeline assessment
            dna_analysis: DNA compliance analysis
            
        Returns:
            Complete contract for Game Designer agent
        """
        return {
            "contract_version": "1.0",
            "story_id": story_id,
            "source_agent": "project_manager",
            "target_agent": "game_designer",
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": dna_analysis.get("pedagogical_value", True),
                    "policy_to_practice": dna_analysis.get("policy_to_practice", True),
                    "time_respect": dna_analysis.get("time_respect", True),
                    "holistic_thinking": dna_analysis.get("holistic_thinking", True),
                    "professional_tone": dna_analysis.get("professional_tone", True)
                },
                "architecture_compliance": {
                    "api_first": True,
                    "stateless_backend": True,
                    "separation_of_concerns": True,
                    "simplicity_first": True
                },
                "project_manager_dna_validation": {
                    "overall_dna_compliant": dna_validation_result.overall_dna_compliant if dna_validation_result else True,
                    "time_respect_compliant": dna_validation_result.time_respect_compliant if dna_validation_result else True,
                    "pedagogical_value_compliant": dna_validation_result.pedagogical_value_compliant if dna_validation_result else True,
                    "professional_tone_compliant": dna_validation_result.professional_tone_compliant if dna_validation_result else True,
                    "policy_to_practice_compliant": dna_validation_result.policy_to_practice_compliant if dna_validation_result else True,
                    "holistic_thinking_compliant": dna_validation_result.holistic_thinking_compliant if dna_validation_result else True,
                    "dna_compliance_score": dna_validation_result.dna_compliance_score if dna_validation_result else 5.0,
                    "validation_timestamp": dna_validation_result.validation_timestamp if dna_validation_result else datetime.now().isoformat(),
                    "quality_reviewer_metrics": dna_validation_result.quality_reviewer_metrics if dna_validation_result else {}
                }
            },
            "input_requirements": {
                "required_files": [
                    f"docs/stories/{story_id}_description.md",
                    f"docs/analysis/{story_id}_feature_analysis.json",
                    f"docs/breakdown/{story_id}_story_breakdown.json"
                ],
                "required_data": {
                    "feature_description": feature_data["feature_description"],
                    "acceptance_criteria": acceptance_criteria,
                    "user_persona": feature_data["user_persona"],
                    "time_constraint_minutes": feature_data["time_constraint_minutes"],
                    "learning_objectives": feature_data["learning_objectives"],
                    "priority_level": feature_data["priority_level"],
                    "complexity_assessment": complexity_assessment,
                    "story_breakdown": story_breakdown,
                    "dna_analysis": dna_analysis
                },
                "required_validations": [
                    "dna_design_principles_alignment_verified",
                    "gdd_consistency_checked",
                    "technical_feasibility_confirmed",
                    "acceptance_criteria_testable"
                ]
            },
            "output_specifications": {
                "deliverable_files": [
                    f"docs/specs/{story_id}_game_design.md",
                    f"docs/specs/{story_id}_ux_specification.md",
                    f"docs/specs/{story_id}_component_mapping.json",
                    f"docs/wireframes/{story_id}_wireframes.png"
                ],
                "deliverable_data": {
                    "game_mechanics": "object",
                    "ui_components": ["object"],
                    "interaction_flows": ["object"],
                    "asset_requirements": ["object"],
                    "component_library_mappings": ["object"]
                },
                "validation_criteria": {
                    "design_principles": {
                        "pedagogical_value": {"min_score": 4},
                        "time_respect": {"max_duration_minutes": feature_data["time_constraint_minutes"]},
                        "professional_tone": {"style_guide_compliance": True}
                    },
                    "design_quality": {
                        "component_library_compliance": {"percentage": 100},
                        "accessibility_considerations": {"included": True},
                        "responsive_design_specified": {"included": True},
                        "anna_persona_optimized": {"validated": True}
                    },
                    "technical_specifications": {
                        "implementable_with_react": {"validated": True},
                        "fastapi_backend_compatible": {"validated": True},
                        "shadcn_ui_components_mapped": {"percentage": 90},
                        "kenney_ui_assets_specified": {"included": True}
                    }
                }
            },
            "quality_gates": [
                "component_library_mapping_complete",
                "wireframes_generated_and_validated",
                "game_mechanics_pedagogically_sound",
                "ux_specification_technically_implementable",
                "accessibility_requirements_specified",
                "anna_persona_experience_optimized"
            ],
            "handoff_criteria": [
                "all_required_components_mapped_to_shadcn_ui",
                "interaction_flows_fully_specified_with_state_management",
                "asset_requirements_clearly_defined_with_kenney_ui",
                "developer_implementation_ready_with_technical_specs",
                "game_mechanics_align_with_learning_objectives",
                "ux_meets_10_minute_completion_constraint"
            ]
        }
    
    async def _save_story_documentation(
        self,
        story_id: str,
        feature_data: Dict[str, Any],
        story_breakdown: Dict[str, Any],
        acceptance_criteria: List[str],
        complexity_assessment: Dict[str, Any]
    ) -> None:
        """
        Save comprehensive story documentation for team reference.
        
        Args:
            story_id: Story identifier
            feature_data: Original feature request data
            story_breakdown: Analyzed story breakdown
            acceptance_criteria: Generated acceptance criteria
            complexity_assessment: Complexity assessment
        """
        try:
            # Save story description
            story_doc_path = self.config.get("docs_path", "docs") if self.config else "docs"
            story_file = Path(story_doc_path) / "stories" / f"{story_id}_description.md"
            story_file.parent.mkdir(parents=True, exist_ok=True)
            
            story_content = self._generate_story_markdown(
                story_id, feature_data, acceptance_criteria, complexity_assessment
            )
            
            with open(story_file, 'w', encoding='utf-8') as f:
                f.write(story_content)
            
            # Save analysis data
            analysis_file = Path(story_doc_path) / "analysis" / f"{story_id}_feature_analysis.json"
            analysis_file.parent.mkdir(parents=True, exist_ok=True)
            
            analysis_data = {
                "story_id": story_id,
                "feature_data": feature_data,
                "acceptance_criteria": acceptance_criteria,
                "complexity_assessment": complexity_assessment,
                "created_at": datetime.now().isoformat(),
                "created_by": self.agent_id
            }
            
            with open(analysis_file, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2, ensure_ascii=False)
            
            # Save story breakdown
            breakdown_file = Path(story_doc_path) / "breakdown" / f"{story_id}_story_breakdown.json"
            breakdown_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(breakdown_file, 'w', encoding='utf-8') as f:
                json.dump(story_breakdown, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Story documentation saved for {story_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to save story documentation for {story_id}: {e}")
            # Don't raise - this is not critical for agent execution
    
    def _generate_story_markdown(
        self,
        story_id: str,
        feature_data: Dict[str, Any],
        acceptance_criteria: List[str],
        complexity_assessment: Dict[str, Any]
    ) -> str:
        """
        Generate comprehensive story documentation in Markdown format.
        
        Args:
            story_id: Story identifier
            feature_data: Feature request data
            acceptance_criteria: Acceptance criteria
            complexity_assessment: Complexity assessment
            
        Returns:
            Formatted Markdown documentation
        """
        return f"""# Story: {story_id}

## Feature Description
{feature_data['feature_description']}

## User Persona
**Target User:** {feature_data['user_persona']}

## Priority Level
**Priority:** {feature_data['priority_level'].upper()}

## Time Constraint
**Maximum Duration:** {feature_data['time_constraint_minutes']} minutes

## Learning Objectives
{chr(10).join(f"- {obj}" for obj in feature_data.get('learning_objectives', []))}

## Acceptance Criteria
{chr(10).join(f"- [ ] {criteria}" for criteria in acceptance_criteria)}

## Complexity Assessment
- **Estimated Effort:** {complexity_assessment.get('effort_points', 'TBD')} story points
- **Technical Complexity:** {complexity_assessment.get('technical_complexity', 'Medium')}
- **Design Complexity:** {complexity_assessment.get('design_complexity', 'Medium')}
- **Estimated Duration:** {complexity_assessment.get('estimated_duration_hours', 'TBD')} hours

## Implementation Notes
{complexity_assessment.get('implementation_notes', 'No specific notes.')}

## References
- **GitHub Issue:** {feature_data.get('github_issue_url', 'N/A')}
- **GDD Section:** {feature_data.get('gdd_section_reference', 'N/A')}
- **Requested By:** {feature_data.get('requested_by', 'Unknown')}
- **Created:** {feature_data.get('created_at', 'Unknown')}

---
*Generated by Project Manager Agent {self.agent_id} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    def _ensure_working_directories(self) -> None:
        """Ensure all required working directories exist."""
        try:
            docs_path = self.config.get("docs_path", "docs") if self.config else "docs"
            base_path = Path(docs_path)
            
            directories = [
                "stories", "analysis", "breakdown", "specs", "wireframes"
            ]
            
            for directory in directories:
                dir_path = base_path / directory
                dir_path.mkdir(parents=True, exist_ok=True)
            
            self.logger.debug("Working directories ensured")
            
        except Exception as e:
            self.logger.warning(f"Failed to create working directories: {e}")
    
    # Quality gate implementations
    def _check_dna_compliance_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Verify DNA compliance for all deliverables."""
        try:
            dna_analysis = deliverables.get("dna_analysis", {})
            required_principles = [
                "pedagogical_value", "policy_to_practice", "time_respect",
                "holistic_thinking", "professional_tone"
            ]
            
            return all(dna_analysis.get(principle, False) for principle in required_principles)
            
        except Exception as e:
            self.logger.error(f"DNA compliance gate check failed: {e}")
            return False
    
    def _check_story_breakdown_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Verify story breakdown is complete and actionable."""
        try:
            story_breakdown = deliverables.get("story_breakdown", {})
            required_sections = [
                "feature_summary", "user_stories", "technical_requirements",
                "design_requirements", "acceptance_criteria"
            ]
            
            return all(section in story_breakdown for section in required_sections)
            
        except Exception as e:
            self.logger.error(f"Story breakdown gate check failed: {e}")
            return False
    
    def _check_acceptance_criteria_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Verify acceptance criteria are clear and testable."""
        try:
            acceptance_criteria = deliverables.get("acceptance_criteria", [])
            
            # Must have at least 3 acceptance criteria
            if len(acceptance_criteria) < 3:
                return False
            
            # Each criterion must be substantial (more than 10 characters)
            return all(len(criterion.strip()) > 10 for criterion in acceptance_criteria)
            
        except Exception as e:
            self.logger.error(f"Acceptance criteria gate check failed: {e}")
            return False
    
    def _check_handoff_ready_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Verify all required data is ready for Game Designer handoff."""
        try:
            required_keys = [
                "feature_description", "acceptance_criteria", "user_persona",
                "story_breakdown", "complexity_assessment", "dna_analysis"
            ]
            
            return all(key in deliverables for key in required_keys)
            
        except Exception as e:
            self.logger.error(f"Handoff ready gate check failed: {e}")
            return False
    
    def _check_technical_feasibility_gate(self, deliverables: Dict[str, Any]) -> bool:
        """Verify technical feasibility has been assessed."""
        try:
            complexity_assessment = deliverables.get("complexity_assessment", {})
            
            required_fields = [
                "technical_complexity", "estimated_duration_hours", "effort_points"
            ]
            
            return all(field in complexity_assessment for field in required_fields)
            
        except Exception as e:
            self.logger.error(f"Technical feasibility gate check failed: {e}")
            return False
    
    def _merge_complexity_predictions(
        self,
        traditional_complexity: Dict[str, Any],
        ml_prediction
    ) -> Dict[str, Any]:
        """
        Merge traditional complexity assessment with ML prediction.
        
        Args:
            traditional_complexity: Traditional complexity assessment
            ml_prediction: ML-based complexity prediction
            
        Returns:
            Enhanced complexity assessment with ML insights
        """
        try:
            # Start with traditional assessment
            enhanced_complexity = traditional_complexity.copy()
            
            # Update with ML predictions if confidence is high enough
            if ml_prediction.confidence_level > 0.6:
                enhanced_complexity.update({
                    'ml_predicted_hours': ml_prediction.predicted_hours,
                    'ml_confidence_interval': ml_prediction.confidence_interval,
                    'ml_confidence_level': ml_prediction.confidence_level,
                    'ml_risk_factors': ml_prediction.risk_factors,
                    'similar_projects': ml_prediction.similar_projects,
                    'prediction_method': 'ml_enhanced'
                })
                
                # Use ML prediction if significantly different and high confidence
                if (ml_prediction.confidence_level > 0.8 and 
                    abs(ml_prediction.predicted_hours - traditional_complexity.get('estimated_duration_hours', 8)) > 4):
                    enhanced_complexity['estimated_duration_hours'] = ml_prediction.predicted_hours
                    enhanced_complexity['estimation_notes'] = (
                        f"ML prediction ({ml_prediction.predicted_hours:.1f}h) differs significantly from "
                        f"traditional estimate ({traditional_complexity.get('estimated_duration_hours', 8)}h). "
                        f"Using ML prediction with {ml_prediction.confidence_level:.0%} confidence based on "
                        f"{len(ml_prediction.similar_projects)} similar projects."
                    )
            else:
                enhanced_complexity.update({
                    'prediction_method': 'traditional_with_ml_insight',
                    'ml_confidence_low': True,
                    'ml_insights': ml_prediction.risk_factors
                })
            
            return enhanced_complexity
            
        except Exception as e:
            self.logger.error(f"Failed to merge complexity predictions: {e}")
            return traditional_complexity
    
    # Public API methods for external integrations
    async def process_github_issue(self, issue_url: str) -> Dict[str, Any]:
        """
        Process a GitHub issue into a story breakdown.
        
        This is a convenience method for direct GitHub integration.
        
        Args:
            issue_url: GitHub issue URL to process
            
        Returns:
            Story breakdown result
        """
        try:
            # Fetch issue data from GitHub
            issue_data = await self.github_integration.fetch_issue_data(issue_url)
            
            # Convert to standard input contract format
            input_contract = self.github_integration.convert_issue_to_contract(issue_data)
            
            # Process through normal workflow
            result = await self.execute_work(input_contract)
            
            return result.to_dict()
            
        except Exception as e:
            self.logger.error(f"Failed to process GitHub issue {issue_url}: {e}")
            raise
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get current agent status and metrics.
        
        Returns:
            Agent status dictionary
        """
        return {
            **self.get_agent_info(),
            "tools_status": {
                "github_integration": "initialized" if hasattr(self, 'github_integration') else "error",
                "story_analyzer": "initialized" if hasattr(self, 'story_analyzer') else "error",
                "dna_compliance_checker": "initialized" if hasattr(self, 'dna_compliance_checker') else "error",
                "learning_engine": "initialized" if hasattr(self, 'learning_engine') else "error",
                "swedish_communicator": "initialized" if hasattr(self, 'swedish_communicator') else "error",
                "team_coordinator": "initialized" if hasattr(self, 'team_coordinator') else "error",
                "stakeholder_manager": "initialized" if hasattr(self, 'stakeholder_manager') else "error"
            },
            "configuration": {
                "max_concurrent_stories": self.max_concurrent_stories,
                "story_priority_threshold": self.story_priority_threshold
            }
        }
    
    async def learn_from_project_completion(
        self,
        story_id: str,
        original_story_data: Dict[str, Any],
        actual_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Learn from completed project to improve future predictions.
        
        This method enables the Learning Engine to continuously improve
        by analyzing the difference between predictions and actual results.
        
        Args:
            story_id: Completed story identifier
            original_story_data: Original story breakdown and estimates
            actual_results: Actual completion metrics and results
            
        Returns:
            Learning summary and insights
        """
        try:
            self.logger.info(f"Learning from completed project: {story_id}")
            
            # Use Learning Engine to process completion data
            await self.learning_engine.learn_from_completion(
                story_id, original_story_data, actual_results
            )
            
            # Get updated learning insights
            learning_insights = await self.learning_engine.get_learning_insights()
            
            # Log key improvements
            if 'recommendations' in learning_insights:
                for recommendation in learning_insights['recommendations'][:3]:
                    self.logger.info(f"Learning recommendation: {recommendation}")
            
            return {
                'status': 'learning_completed',
                'story_id': story_id,
                'learning_insights': learning_insights,
                'improvement_areas': learning_insights.get('next_improvement_opportunities', [])
            }
            
        except Exception as e:
            self.logger.error(f"Failed to learn from project completion {story_id}: {e}")
            return {
                'status': 'learning_failed',
                'story_id': story_id,
                'error': str(e)
            }
    
    async def get_learning_status(self) -> Dict[str, Any]:
        """
        Get current learning status and insights.
        
        Returns:
            Learning engine status and insights
        """
        try:
            if hasattr(self, 'learning_engine'):
                return await self.learning_engine.get_learning_insights()
            else:
                return {'status': 'learning_engine_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to get learning status: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def generate_swedish_municipal_message(
        self,
        message_type: str,
        recipient_role: str,
        content_data: Dict[str, Any],
        urgency_level: str = "normal"
    ) -> Dict[str, Any]:
        """
        Generate culturally appropriate Swedish municipal message.
        
        Args:
            message_type: Type of communication (formal_request, status_update, etc.)
            recipient_role: Swedish municipal role (kommunchef, utbildningskoordinator, etc.)
            content_data: Message content and context
            urgency_level: Message urgency level
            
        Returns:
            Generated Swedish municipal message
        """
        try:
            if hasattr(self, 'swedish_communicator'):
                from .tools.swedish_municipal_communicator import CommunicationType, MunicipalRole
                
                # Convert string parameters to enums
                comm_type = CommunicationType(message_type)
                role = MunicipalRole(recipient_role)
                
                return self.swedish_communicator.generate_municipal_specific_message(
                    comm_type, role, content_data, urgency_level
                )
            else:
                return {'status': 'swedish_communicator_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to generate Swedish municipal message: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def get_team_status_dashboard(self) -> Dict[str, Any]:
        """
        Get comprehensive team status dashboard.
        
        Returns:
            Team status dashboard with performance metrics and coordination status
        """
        try:
            if hasattr(self, 'team_coordinator'):
                return await self.team_coordinator.get_team_status_dashboard()
            else:
                return {'status': 'team_coordinator_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to get team status dashboard: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def automate_feature_approval_workflow(
        self,
        story_id: str,
        feature_data: Dict[str, Any],
        quality_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Automate GitHub approval workflow for completed features.
        
        Args:
            story_id: Story identifier
            feature_data: Feature information and requirements
            quality_metrics: Quality analysis results
            
        Returns:
            Approval workflow automation result
        """
        try:
            if hasattr(self, 'team_coordinator'):
                return await self.team_coordinator.automate_github_approval_workflow(
                    story_id, feature_data, quality_metrics
                )
            else:
                return {'status': 'team_coordinator_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to automate approval workflow: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def validate_municipal_communication(
        self,
        message: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate message for Swedish municipal cultural appropriateness.
        
        Args:
            message: Message text to validate
            context: Communication context
            
        Returns:
            Validation results with cultural appropriateness feedback
        """
        try:
            if hasattr(self, 'swedish_communicator'):
                return self.swedish_communicator.validate_cultural_appropriateness(message, context)
            else:
                return {'status': 'swedish_communicator_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to validate municipal communication: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def learn_stakeholder_preferences(
        self,
        stakeholder_id: str,
        interaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Learn and update stakeholder preferences from interaction data.
        
        Args:
            stakeholder_id: Stakeholder identifier
            interaction_data: Data from recent interaction
            
        Returns:
            Learning results and updated preferences
        """
        try:
            if hasattr(self, 'stakeholder_manager'):
                return await self.stakeholder_manager.learn_stakeholder_preferences(
                    stakeholder_id, interaction_data
                )
            else:
                return {'status': 'stakeholder_manager_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to learn stakeholder preferences: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def predict_stakeholder_approval(
        self,
        stakeholder_id: str,
        proposal_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict likelihood of stakeholder approval for a proposal.
        
        Args:
            stakeholder_id: Stakeholder identifier
            proposal_data: Proposal/feature data for approval prediction
            
        Returns:
            Approval prediction with confidence and recommendations
        """
        try:
            if hasattr(self, 'stakeholder_manager'):
                return await self.stakeholder_manager.predict_approval_likelihood(
                    stakeholder_id, proposal_data
                )
            else:
                return {'status': 'stakeholder_manager_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to predict stakeholder approval: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def generate_stakeholder_communication(
        self,
        stakeholder_id: str,
        communication_type: str,
        content_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate personalized communication for specific stakeholder.
        
        Args:
            stakeholder_id: Stakeholder identifier
            communication_type: Type of communication
            content_data: Content to be communicated
            
        Returns:
            Personalized communication optimized for stakeholder
        """
        try:
            if hasattr(self, 'stakeholder_manager'):
                return await self.stakeholder_manager.generate_personalized_communication(
                    stakeholder_id, communication_type, content_data
                )
            else:
                return {'status': 'stakeholder_manager_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to generate stakeholder communication: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def optimize_stakeholder_relationships(self) -> Dict[str, Any]:
        """
        Analyze and optimize all stakeholder relationships.
        
        Returns:
            Optimization recommendations and relationship insights
        """
        try:
            if hasattr(self, 'stakeholder_manager'):
                return await self.stakeholder_manager.optimize_stakeholder_relationships()
            else:
                return {'status': 'stakeholder_manager_not_initialized'}
                
        except Exception as e:
            self.logger.error(f"Failed to optimize stakeholder relationships: {e}")
            return {'status': 'error', 'message': str(e)}
    
    # EventBus Team Coordination Methods
    
    async def _notify_team_progress(self, event_type: str, data: Dict[str, Any]):
        """Notify team of Project Manager progress via EventBus."""
        try:
            await self.event_bus.publish(event_type, {
                "agent": "project_manager",
                "story_id": data.get("story_id"),
                "status": data.get("status"),
                "timestamp": datetime.now().isoformat(),
                **data
            })
        except Exception as e:
            self.logger.warning(f"Failed to publish team event {event_type}: {e}")

    async def _listen_for_team_events(self):
        """Listen for relevant team coordination events."""
        try:
            relevant_events = ["project_manager_*", "team_*", "pipeline_*", "story_*"]
            for event_pattern in relevant_events:
                await self.event_bus.subscribe(event_pattern, self._handle_team_event)
        except Exception as e:
            self.logger.warning(f"Failed to setup team event listeners: {e}")

    async def _handle_team_event(self, event_type: str, data: Dict[str, Any]):
        """Handle incoming team coordination events."""
        try:
            self.logger.info(f"Project Manager received team event: {event_type}")
            
            # Handle story-related events
            if "story_complete" in event_type:
                await self._handle_story_completion(data)
            elif "revision_required" in event_type:
                await self._handle_revision_request(data)
            elif "approval_decision" in event_type:
                await self._handle_approval_decision(data)
            elif "pipeline_error" in event_type:
                await self._handle_pipeline_error(data)
        except Exception as e:
            self.logger.error(f"Error handling team event {event_type}: {e}")

    async def _handle_story_completion(self, data: Dict[str, Any]):
        """Handle story completion events."""
        story_id = data.get("story_id")
        self.logger.info(f"Story {story_id} completed, initiating project owner approval workflow")
        # Integration with existing feedback processing

    async def _handle_revision_request(self, data: Dict[str, Any]):
        """Handle revision request events."""
        story_id = data.get("story_id")
        self.logger.info(f"Revision requested for story {story_id}, processing feedback")
        # Integration with existing FeedbackProcessor

    async def _handle_approval_decision(self, data: Dict[str, Any]):
        """Handle project owner approval decisions."""
        story_id = data.get("story_id")
        decision = data.get("decision")
        self.logger.info(f"Approval decision for story {story_id}: {decision}")
        # Integration with PriorityQueueManager

    async def _handle_pipeline_error(self, data: Dict[str, Any]):
        """Handle pipeline error events."""
        story_id = data.get("story_id")
        error = data.get("error")
        self.logger.error(f"Pipeline error for story {story_id}: {error}")
        # Error handling and recovery logic