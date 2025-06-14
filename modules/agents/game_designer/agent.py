"""
Game Designer Agent - UX specification and pedagogical game design for DigiNativa.

PURPOSE:
Transforms story breakdowns into detailed UX specifications and pedagogical
game designs using component libraries (Shadcn/UI + Kenney.UI).

CRITICAL IMPORTANCE:
- Bridges gap between feature requirements and implementation
- Ensures pedagogical value in all game mechanics
- Creates implementable UX specifications for developers
- Maintains design consistency across the platform

REVENUE IMPACT:
This agent directly impacts revenue by:
- Creating engaging game designs that improve user retention
- Ensuring pedagogical effectiveness for client satisfaction
- Producing implementable specs that reduce development time
- Maintaining design quality that enables premium pricing
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
from .tools.component_mapper import ComponentMapper
from .tools.wireframe_generator import WireframeGenerator
from .tools.ux_validator import UXValidator
from .tools.pedagogical_design_helper import PedagogicalDesignHelper


class GameDesignerAgent(BaseAgent):
    """
    Game Designer agent for UX specification and pedagogical game design.
    
    This agent transforms Project Manager story breakdowns into detailed
    UX specifications and game mechanics that developers can implement.
    
    RESPONSIBILITIES:
    1. Analyze story breakdowns for design requirements
    2. Create pedagogical game mechanics aligned with learning objectives
    3. Generate UX specifications using Shadcn/UI + Kenney.UI components
    4. Create wireframes and interaction flows
    5. Validate designs against DNA principles
    """
    
    def __init__(self, agent_id: str = "gd-001", config: Optional[Dict[str, Any]] = None):
        """Initialize Game Designer agent."""
        super().__init__(agent_id, "game_designer", config)
        
        # Initialize design tools
        try:
            self.component_mapper = ComponentMapper()
            self.wireframe_generator = WireframeGenerator()
            self.ux_validator = UXValidator()
            self.pedagogical_helper = PedagogicalDesignHelper()
            
            self.logger.info("Game Designer agent tools initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Game Designer tools: {e}")
            raise AgentExecutionError(f"Tool initialization failed: {e}", agent_id)
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform story breakdown into UX specification and game design.
        
        This is the core business logic that creates implementable designs
        from Project Manager story breakdowns.
        
        Args:
            input_contract: Contract containing story breakdown from Project Manager
            
        Returns:
            Output contract for Developer with UX specifications
            
        Raises:
            BusinessLogicError: If story breakdown is invalid or incomplete
            DNAComplianceError: If design violates DNA principles
            AgentExecutionError: If design generation fails
        """
        try:
            story_id = input_contract.get("story_id")
            self.logger.info(f"Processing design request for story: {story_id}")
            
            # Step 1: Extract and validate story breakdown
            story_data = self._extract_story_data(input_contract)
            
            # Step 2: Create pedagogical game mechanics
            self.logger.debug("Creating pedagogical game mechanics")
            game_mechanics = await self.pedagogical_helper.create_game_mechanics(
                story_data
            )
            
            # Step 3: Generate UI component specifications
            self.logger.debug("Generating UI component specifications")
            ui_components = await self.component_mapper.map_story_to_components(
                story_data,
                game_mechanics
            )
            
            # Step 4: Create interaction flows and wireframes
            self.logger.debug("Creating interaction flows and wireframes")
            interaction_flows = await self.wireframe_generator.create_interaction_flows(
                story_data,
                ui_components
            )
            
            wireframes = await self.wireframe_generator.generate_wireframes(
                ui_components,
                interaction_flows
            )
            
            # Step 5: Validate UX design against DNA principles
            self.logger.debug("Validating UX design against DNA principles")
            ux_validation = await self.ux_validator.validate_design(
                game_mechanics,
                ui_components,
                interaction_flows,
                story_data.get("user_persona", "Anna")
            )
            
            if not ux_validation["valid"]:
                raise DNAComplianceError(
                    f"UX design violates DNA principles: {ux_validation['violations']}",
                    violated_principles=ux_validation["violations"],
                    agent_type=self.agent_type
                )
            
            # Step 6: Generate asset requirements
            asset_requirements = await self._generate_asset_requirements(
                game_mechanics,
                ui_components
            )
            
            # Step 7: Create Developer handoff contract
            output_contract = self._create_developer_contract(
                story_id,
                story_data,
                game_mechanics,
                ui_components,
                interaction_flows,
                wireframes,
                asset_requirements,
                ux_validation
            )
            
            # Step 8: Save design documentation
            await self._save_design_documentation(
                story_id,
                game_mechanics,
                ui_components,
                interaction_flows,
                wireframes,
                asset_requirements
            )
            
            self.logger.info(f"Successfully processed design for story: {story_id}")
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
            self.logger.error(f"Unexpected error processing design: {e}")
            raise AgentExecutionError(
                f"Failed to process design request: {e}",
                agent_id=self.agent_id,
                story_id=input_contract.get("story_id"),
                execution_context={"input_contract": input_contract}
            )
    
    def _extract_story_data(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and validate story data from input contract."""
        input_requirements = input_contract.get("input_requirements", {})
        required_data = input_requirements.get("required_data", {})
        
        # Validate required fields
        required_fields = [
            "feature_description", "acceptance_criteria", "user_persona",
            "learning_objectives", "time_constraint_minutes"
        ]
        
        for field in required_fields:
            if field not in required_data:
                raise BusinessLogicError(
                    f"Missing required field: {field}",
                    business_rule="story_data_completeness"
                )
        
        # Extract story data
        story_data = {
            "feature_description": required_data["feature_description"],
            "acceptance_criteria": required_data["acceptance_criteria"],
            "user_persona": required_data["user_persona"],
            "learning_objectives": required_data["learning_objectives"],
            "time_constraint_minutes": required_data["time_constraint_minutes"],
            "priority_level": required_data.get("priority_level", "medium"),
            "complexity_assessment": required_data.get("complexity_assessment", {}),
            "story_breakdown": required_data.get("story_breakdown", {}),
            "gdd_section_reference": required_data.get("gdd_section_reference", "")
        }
        
        self.logger.debug(f"Extracted story data for {story_data['user_persona']}")
        return story_data
    
    async def _generate_asset_requirements(self, 
                                         game_mechanics: Dict[str, Any],
                                         ui_components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate asset requirements for the design."""
        asset_requirements = []
        
        # Extract asset needs from game mechanics
        for mechanic in game_mechanics.get("mechanics", []):
            if mechanic.get("requires_assets"):
                for asset in mechanic["required_assets"]:
                    asset_requirements.append({
                        "type": asset["type"],
                        "category": asset["category"],
                        "source": "kenney_ui" if asset["type"] == "ui_element" else "custom",
                        "specifications": asset.get("specifications", {}),
                        "mechanic_reference": mechanic["name"]
                    })
        
        # Extract asset needs from UI components
        for component in ui_components:
            if component.get("requires_assets"):
                for asset in component["required_assets"]:
                    asset_requirements.append({
                        "type": asset["type"],
                        "category": asset["category"],
                        "source": "shadcn_ui" if asset["type"] == "component" else "kenney_ui",
                        "specifications": asset.get("specifications", {}),
                        "component_reference": component["name"]
                    })
        
        return asset_requirements
    
    def _create_developer_contract(self,
                                 story_id: str,
                                 story_data: Dict[str, Any],
                                 game_mechanics: Dict[str, Any],
                                 ui_components: List[Dict[str, Any]],
                                 interaction_flows: List[Dict[str, Any]],
                                 wireframes: Dict[str, Any],
                                 asset_requirements: List[Dict[str, Any]],
                                 ux_validation: Dict[str, Any]) -> Dict[str, Any]:
        """Create contract for Developer agent handoff."""
        
        return {
            "contract_version": "1.0",
            "story_id": story_id,
            "source_agent": "game_designer",
            "target_agent": "developer",
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": True,
                    "policy_to_practice": True,
                    "time_respect": True,
                    "holistic_thinking": True,
                    "professional_tone": True
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
                    f"docs/specs/game_design_{story_id}.md",
                    f"docs/specs/ux_specification_{story_id}.md",
                    f"docs/specs/component_mapping_{story_id}.json",
                    f"docs/wireframes/{story_id}_wireframes.json"
                ],
                "required_data": {
                    "game_mechanics": game_mechanics,
                    "ui_components": ui_components,
                    "interaction_flows": interaction_flows,
                    "wireframes": wireframes,
                    "asset_requirements": asset_requirements,
                    "ux_validation": ux_validation,
                    "story_context": story_data
                },
                "required_validations": [
                    "component_library_compliance_verified",
                    "game_mechanics_pedagogically_sound",
                    "ux_design_implementable"
                ]
            },
            "output_specifications": {
                "deliverable_files": [
                    f"frontend/components/{story_id}/",
                    f"backend/endpoints/{story_id}/",
                    f"tests/unit/{story_id}/",
                    f"docs/implementation/{story_id}_implementation.md"
                ],
                "deliverable_data": {
                    "component_implementations": "List[ComponentImplementation]",
                    "api_implementations": "List[APIEndpoint]",
                    "game_mechanics_implementation": "GameMechanicsCode",
                    "asset_integration": "AssetIntegrationPlan"
                },
                "validation_criteria": {
                    "code_quality": {
                        "typescript_errors": {"max": 0},
                        "eslint_violations": {"max": 0},
                        "test_coverage_percent": {"min": 100}
                    },
                    "performance": {
                        "lighthouse_score": {"min": 90},
                        "api_response_time_ms": {"max": 200},
                        "bundle_size_increase_kb": {"max": 50}
                    },
                    "functionality": {
                        "game_mechanics_working": {"required": True},
                        "ui_components_responsive": {"required": True},
                        "interaction_flows_complete": {"required": True}
                    }
                }
            },
            "quality_gates": [
                "component_library_usage_100_percent",
                "game_mechanics_pedagogical_effectiveness_validated",
                "ui_components_responsive_design_verified",
                "interaction_flows_user_tested",
                "performance_benchmarks_met"
            ],
            "handoff_criteria": [
                "all_ui_components_implementable",
                "game_mechanics_clearly_specified",
                "api_requirements_documented",
                "asset_requirements_complete",
                "developer_ready_specifications"
            ]
        }
    
    async def _save_design_documentation(self,
                                       story_id: str,
                                       game_mechanics: Dict[str, Any],
                                       ui_components: List[Dict[str, Any]],
                                       interaction_flows: List[Dict[str, Any]],
                                       wireframes: Dict[str, Any],
                                       asset_requirements: List[Dict[str, Any]]) -> None:
        """Save design documentation for developer reference."""
        try:
            # Create documentation directory
            docs_path = Path("docs/specs")
            docs_path.mkdir(parents=True, exist_ok=True)
            
            wireframes_path = Path("docs/wireframes")
            wireframes_path.mkdir(parents=True, exist_ok=True)
            
            # Save game design specification
            game_design_doc = self._create_game_design_document(
                story_id, game_mechanics, ui_components
            )
            
            with open(docs_path / f"game_design_{story_id}.md", 'w') as f:
                f.write(game_design_doc)
            
            # Save UX specification
            ux_spec_doc = self._create_ux_specification_document(
                story_id, ui_components, interaction_flows
            )
            
            with open(docs_path / f"ux_specification_{story_id}.md", 'w') as f:
                f.write(ux_spec_doc)
            
            # Save component mapping as JSON
            component_mapping = {
                "story_id": story_id,
                "ui_components": ui_components,
                "asset_requirements": asset_requirements,
                "generated_at": datetime.now().isoformat()
            }
            
            with open(docs_path / f"component_mapping_{story_id}.json", 'w') as f:
                json.dump(component_mapping, f, indent=2)
            
            # Save wireframes
            wireframes_data = {
                "story_id": story_id,
                "wireframes": wireframes,
                "interaction_flows": interaction_flows,
                "generated_at": datetime.now().isoformat()
            }
            
            with open(wireframes_path / f"{story_id}_wireframes.json", 'w') as f:
                json.dump(wireframes_data, f, indent=2)
            
            self.logger.debug(f"Design documentation saved for story: {story_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to save design documentation: {e}")
            # Don't raise exception - documentation save shouldn't block workflow
    
    def _create_game_design_document(self, story_id: str, game_mechanics: Dict[str, Any], 
                                   ui_components: List[Dict[str, Any]]) -> str:
        """Create markdown game design document."""
        return f"""# Game Design Specification - {story_id}

## Overview
This document specifies the game mechanics and design for story {story_id}.

## Game Mechanics
{json.dumps(game_mechanics, indent=2)}

## UI Components
{json.dumps(ui_components, indent=2)}

## Implementation Notes
- All components must use Shadcn/UI base components
- Game assets should utilize Kenney.UI library
- Maintain pedagogical focus throughout implementation
- Ensure accessibility compliance (WCAG AA)

Generated by Game Designer Agent at {datetime.now().isoformat()}
"""
    
    def _create_ux_specification_document(self, story_id: str, 
                                        ui_components: List[Dict[str, Any]],
                                        interaction_flows: List[Dict[str, Any]]) -> str:
        """Create markdown UX specification document."""
        return f"""# UX Specification - {story_id}

## User Experience Requirements

### UI Components
{json.dumps(ui_components, indent=2)}

### Interaction Flows
{json.dumps(interaction_flows, indent=2)}

## Design Guidelines
- Follow DigiNativa design principles
- Maintain 10-minute task completion constraint
- Ensure professional tone throughout interface
- Focus on pedagogical value in all interactions

Generated by Game Designer Agent at {datetime.now().isoformat()}
"""
    
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """Check Game Designer specific quality gates."""
        quality_checks = {
            "component_library_usage_100_percent": self._check_component_library_usage,
            "game_mechanics_pedagogical_effectiveness_validated": self._check_pedagogical_effectiveness,
            "ui_components_responsive_design_verified": self._check_responsive_design,
            "interaction_flows_user_tested": self._check_interaction_flows,
            "performance_benchmarks_met": self._check_performance_benchmarks
        }
        
        checker = quality_checks.get(gate)
        if checker:
            return checker(deliverables)
        
        return True  # Default pass for unknown gates
    
    def _check_component_library_usage(self, deliverables: Dict[str, Any]) -> bool:
        """Verify 100% component library usage."""
        ui_components = deliverables.get("ui_components", [])
        
        for component in ui_components:
            if not component.get("library_source") in ["shadcn_ui", "kenney_ui"]:
                return False
            
            if not component.get("library_compliant", False):
                return False
        
        return True
    
    def _check_pedagogical_effectiveness(self, deliverables: Dict[str, Any]) -> bool:
        """Verify game mechanics are pedagogically effective."""
        game_mechanics = deliverables.get("game_mechanics", {})
        
        # Check that learning objectives are addressed
        learning_objectives = game_mechanics.get("learning_objectives_addressed", [])
        if not learning_objectives:
            return False
        
        # Check pedagogical score
        pedagogical_score = game_mechanics.get("pedagogical_effectiveness_score", 0)
        if pedagogical_score < 4:  # Minimum score out of 5
            return False
        
        return True
    
    def _check_responsive_design(self, deliverables: Dict[str, Any]) -> bool:
        """Verify responsive design considerations."""
        ui_components = deliverables.get("ui_components", [])
        
        for component in ui_components:
            if not component.get("responsive_design", False):
                return False
            
            breakpoints = component.get("breakpoints", [])
            if not breakpoints:
                return False
        
        return True
    
    def _check_interaction_flows(self, deliverables: Dict[str, Any]) -> bool:
        """Verify interaction flows are complete."""
        interaction_flows = deliverables.get("interaction_flows", [])
        
        if not interaction_flows:
            return False
        
        for flow in interaction_flows:
            # Check required flow elements
            required_elements = ["start_state", "end_state", "user_actions", "system_responses"]
            for element in required_elements:
                if element not in flow:
                    return False
        
        return True
    
    def _check_performance_benchmarks(self, deliverables: Dict[str, Any]) -> bool:
        """Verify performance benchmarks are considered."""
        performance_considerations = deliverables.get("performance_considerations", {})
        
        # Check that performance targets are defined
        if not performance_considerations.get("lighthouse_target"):
            return False
        
        if not performance_considerations.get("load_time_target"):
            return False
        
        return True