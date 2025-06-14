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
from .tools.github_integration import GitHubIntegration
from .tools.story_analyzer import StoryAnalyzer
from .tools.dna_compliance_checker import DNAComplianceChecker


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
            
            self.logger.info("Project Manager Agent tools initialized successfully")
            
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
            
            # Step 5: Estimate complexity and timeline
            complexity_assessment = await self.story_analyzer.assess_complexity(
                story_breakdown
            )
            
            # Step 6: Create Game Designer handoff contract
            output_contract = self._create_game_designer_contract(
                story_id,
                feature_data,
                story_breakdown,
                acceptance_criteria,
                complexity_assessment,
                dna_analysis
            )
            
            # Step 7: Save story documentation
            await self._save_story_documentation(
                story_id,
                feature_data,
                story_breakdown,
                acceptance_criteria,
                complexity_assessment
            )
            
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
        dna_analysis: Dict[str, Any]
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
                "dna_compliance_checker": "initialized" if hasattr(self, 'dna_compliance_checker') else "error"
            },
            "configuration": {
                "max_concurrent_stories": self.max_concurrent_stories,
                "story_priority_threshold": self.story_priority_threshold
            }
        }