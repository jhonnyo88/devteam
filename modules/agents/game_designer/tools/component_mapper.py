"""
Component Mapper - Maps story requirements to UI components for DigiNativa.

PURPOSE:
Maps story breakdowns to specific Shadcn/UI and Kenney.UI components,
ensuring design consistency and implementation efficiency.

CRITICAL IMPORTANCE:
- Ensures 100% component library usage
- Reduces development time through standardized components
- Maintains design consistency across features
- Enables rapid prototyping and iteration
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime


logger = logging.getLogger(__name__)


class ComponentMapper:
    """
    Maps story requirements to UI components from component libraries.
    
    This tool analyzes story breakdowns and game mechanics to determine
    the most appropriate UI components from Shadcn/UI and Kenney.UI.
    """
    
    def __init__(self):
        """Initialize component mapper with component libraries."""
        self.logger = logging.getLogger(f"{__name__}.ComponentMapper")
        
        # Shadcn/UI component library mapping
        self.shadcn_components = {
            "forms": {
                "input": {"component": "Input", "variants": ["default", "destructive"]},
                "button": {"component": "Button", "variants": ["default", "destructive", "outline", "secondary", "ghost", "link"]},
                "checkbox": {"component": "Checkbox", "variants": ["default"]},
                "select": {"component": "Select", "variants": ["default"]},
                "textarea": {"component": "Textarea", "variants": ["default"]},
                "form": {"component": "Form", "variants": ["default"]}
            },
            "navigation": {
                "tabs": {"component": "Tabs", "variants": ["default"]},
                "breadcrumb": {"component": "Breadcrumb", "variants": ["default"]},
                "navigation_menu": {"component": "NavigationMenu", "variants": ["default"]}
            },
            "feedback": {
                "alert": {"component": "Alert", "variants": ["default", "destructive"]},
                "toast": {"component": "Toast", "variants": ["default", "destructive"]},
                "progress": {"component": "Progress", "variants": ["default"]},
                "badge": {"component": "Badge", "variants": ["default", "secondary", "destructive", "outline"]}
            },
            "data_display": {
                "card": {"component": "Card", "variants": ["default"]},
                "table": {"component": "Table", "variants": ["default"]},
                "avatar": {"component": "Avatar", "variants": ["default"]},
                "separator": {"component": "Separator", "variants": ["default"]}
            },
            "overlays": {
                "dialog": {"component": "Dialog", "variants": ["default"]},
                "sheet": {"component": "Sheet", "variants": ["default"]},
                "popover": {"component": "Popover", "variants": ["default"]},
                "tooltip": {"component": "Tooltip", "variants": ["default"]}
            }
        }
        
        # Kenney.UI game component library mapping
        self.kenney_components = {
            "game_ui": {
                "health_bar": {"component": "HealthBar", "variants": ["horizontal", "vertical", "circular"]},
                "score_display": {"component": "ScoreDisplay", "variants": ["counter", "stars", "badges"]},
                "level_indicator": {"component": "LevelIndicator", "variants": ["progress", "steps", "tree"]},
                "achievement_badge": {"component": "AchievementBadge", "variants": ["gold", "silver", "bronze"]}
            },
            "interactive": {
                "game_button": {"component": "GameButton", "variants": ["primary", "secondary", "danger", "success"]},
                "drag_drop": {"component": "DragDropArea", "variants": ["target", "source", "both"]},
                "slider": {"component": "GameSlider", "variants": ["horizontal", "vertical"]},
                "wheel": {"component": "SelectionWheel", "variants": ["options", "fortune", "picker"]}
            },
            "educational": {
                "quiz_component": {"component": "QuizWidget", "variants": ["multiple_choice", "true_false", "fill_blank"]},
                "timeline": {"component": "Timeline", "variants": ["horizontal", "vertical", "interactive"]},
                "diagram": {"component": "InteractiveDiagram", "variants": ["flowchart", "mindmap", "hierarchy"]},
                "simulation": {"component": "SimulationArea", "variants": ["scenario", "sandbox", "guided"]}
            }
        }
        
        self.logger.info("Component mapper initialized with library definitions")
    
    async def map_story_to_components(self, story_data: Dict[str, Any], 
                                    game_mechanics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Map story requirements to specific UI components.
        
        Args:
            story_data: Story breakdown from Project Manager
            game_mechanics: Game mechanics from pedagogical design
            
        Returns:
            List of mapped UI components with specifications
        """
        try:
            self.logger.info(f"Mapping components for story with {len(game_mechanics.get('mechanics', []))} mechanics")
            
            components = []
            
            # Analyze story requirements
            feature_type = self._analyze_feature_type(story_data)
            user_interactions = self._extract_user_interactions(story_data)
            data_requirements = self._analyze_data_requirements(story_data)
            
            # Map basic UI components (Shadcn/UI)
            ui_components = await self._map_ui_components(
                feature_type, user_interactions, data_requirements
            )
            components.extend(ui_components)
            
            # Map game-specific components (Kenney.UI)
            game_components = await self._map_game_components(
                game_mechanics, story_data
            )
            components.extend(game_components)
            
            # Add responsive design specifications
            components = self._add_responsive_specifications(components)
            
            # Validate component mapping
            self._validate_component_mapping(components, story_data)
            
            self.logger.info(f"Mapped {len(components)} components for story")
            return components
            
        except Exception as e:
            self.logger.error(f"Failed to map components: {e}")
            raise
    
    def _analyze_feature_type(self, story_data: Dict[str, Any]) -> str:
        """Analyze story to determine primary feature type."""
        feature_description = story_data.get("feature_description", "").lower()
        
        if any(keyword in feature_description for keyword in ["quiz", "question", "test", "assessment"]):
            return "assessment"
        elif any(keyword in feature_description for keyword in ["form", "input", "submit", "register"]):
            return "form"
        elif any(keyword in feature_description for keyword in ["dashboard", "overview", "summary", "status"]):
            return "dashboard"
        elif any(keyword in feature_description for keyword in ["game", "play", "interactive", "simulation"]):
            return "interactive_game"
        elif any(keyword in feature_description for keyword in ["list", "table", "display", "view"]):
            return "data_display"
        else:
            return "general"
    
    def _extract_user_interactions(self, story_data: Dict[str, Any]) -> List[str]:
        """Extract user interaction patterns from story."""
        interactions = []
        
        acceptance_criteria = story_data.get("acceptance_criteria", [])
        
        for criterion in acceptance_criteria:
            criterion_lower = criterion.lower()
            
            if "click" in criterion_lower or "button" in criterion_lower:
                interactions.append("click")
            if "type" in criterion_lower or "input" in criterion_lower:
                interactions.append("input")
            if "select" in criterion_lower or "choose" in criterion_lower:
                interactions.append("select")
            if "drag" in criterion_lower or "drop" in criterion_lower:
                interactions.append("drag_drop")
            if "swipe" in criterion_lower or "scroll" in criterion_lower:
                interactions.append("gesture")
        
        return list(set(interactions))  # Remove duplicates
    
    def _analyze_data_requirements(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data display and management requirements."""
        feature_description = story_data.get("feature_description", "").lower()
        
        requirements = {
            "needs_form": "form" in feature_description or "input" in feature_description,
            "needs_table": "list" in feature_description or "table" in feature_description,
            "needs_charts": "chart" in feature_description or "graph" in feature_description,
            "needs_navigation": "navigate" in feature_description or "menu" in feature_description,
            "needs_feedback": "feedback" in feature_description or "alert" in feature_description
        }
        
        return requirements
    
    async def _map_ui_components(self, feature_type: str, user_interactions: List[str], 
                               data_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map to Shadcn/UI components based on requirements."""
        components = []
        
        # Base layout components
        components.append({
            "name": "main_container",
            "library": "shadcn_ui",
            "component": "Card",
            "variant": "default",
            "purpose": "main_container",
            "library_source": "shadcn_ui",
            "library_compliant": True,
            "responsive_design": True,
            "breakpoints": ["sm", "md", "lg", "xl"],
            "specifications": {
                "className": "w-full max-w-4xl mx-auto p-6",
                "role": "main"
            }
        })
        
        # Form components if needed
        if data_requirements.get("needs_form") or "input" in user_interactions:
            components.extend([
                {
                    "name": "input_field",
                    "library": "shadcn_ui",
                    "component": "Input",
                    "variant": "default",
                    "purpose": "user_input",
                    "library_source": "shadcn_ui",
                    "library_compliant": True,
                    "responsive_design": True,
                    "breakpoints": ["sm", "md", "lg"],
                    "specifications": {
                        "type": "text",
                        "placeholder": "Enter information...",
                        "className": "w-full"
                    }
                },
                {
                    "name": "submit_button",
                    "library": "shadcn_ui", 
                    "component": "Button",
                    "variant": "default",
                    "purpose": "form_submission",
                    "library_source": "shadcn_ui",
                    "library_compliant": True,
                    "responsive_design": True,
                    "breakpoints": ["sm", "md", "lg"],
                    "specifications": {
                        "type": "submit",
                        "className": "w-full sm:w-auto"
                    }
                }
            ])
        
        # Navigation components
        if data_requirements.get("needs_navigation"):
            components.append({
                "name": "navigation_tabs",
                "library": "shadcn_ui",
                "component": "Tabs",
                "variant": "default",
                "purpose": "navigation",
                "library_source": "shadcn_ui",
                "library_compliant": True,
                "responsive_design": True,
                "breakpoints": ["sm", "md", "lg", "xl"],
                "specifications": {
                    "defaultValue": "tab1",
                    "className": "w-full"
                }
            })
        
        # Feedback components
        if data_requirements.get("needs_feedback"):
            components.append({
                "name": "status_alert",
                "library": "shadcn_ui",
                "component": "Alert",
                "variant": "default",
                "purpose": "user_feedback",
                "library_source": "shadcn_ui",
                "library_compliant": True,
                "responsive_design": True,
                "breakpoints": ["sm", "md", "lg"],
                "specifications": {
                    "className": "mb-4"
                }
            })
        
        return components
    
    async def _map_game_components(self, game_mechanics: Dict[str, Any], 
                                 story_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Map to Kenney.UI game components based on mechanics."""
        components = []
        
        mechanics = game_mechanics.get("mechanics", [])
        
        for mechanic in mechanics:
            mechanic_type = mechanic.get("type", "")
            
            if mechanic_type == "quiz":
                components.append({
                    "name": f"quiz_widget_{mechanic['name']}",
                    "library": "kenney_ui",
                    "component": "QuizWidget",
                    "variant": "multiple_choice",
                    "purpose": "assessment",
                    "library_source": "kenney_ui",
                    "library_compliant": True,
                    "responsive_design": True,
                    "breakpoints": ["sm", "md", "lg"],
                    "specifications": {
                        "questions": mechanic.get("questions", []),
                        "scoring": mechanic.get("scoring", "percentage"),
                        "feedback": "immediate"
                    },
                    "requires_assets": True,
                    "required_assets": [
                        {
                            "type": "ui_element",
                            "category": "quiz_background",
                            "specifications": {"style": "professional", "color_scheme": "blue"}
                        }
                    ]
                })
            
            elif mechanic_type == "progress_tracking":
                components.append({
                    "name": f"progress_bar_{mechanic['name']}",
                    "library": "kenney_ui",
                    "component": "HealthBar",  # Repurposed for progress
                    "variant": "horizontal",
                    "purpose": "progress_display",
                    "library_source": "kenney_ui",
                    "library_compliant": True,
                    "responsive_design": True,
                    "breakpoints": ["sm", "md", "lg"],
                    "specifications": {
                        "max_value": mechanic.get("max_progress", 100),
                        "show_percentage": True,
                        "animation": "smooth"
                    }
                })
            
            elif mechanic_type == "interactive_element":
                components.append({
                    "name": f"interactive_area_{mechanic['name']}",
                    "library": "kenney_ui",
                    "component": "SimulationArea",
                    "variant": "scenario",
                    "purpose": "interaction",
                    "library_source": "kenney_ui",
                    "library_compliant": True,
                    "responsive_design": True,
                    "breakpoints": ["md", "lg", "xl"],
                    "specifications": {
                        "interaction_type": mechanic.get("interaction_type", "click"),
                        "feedback_type": "visual_audio",
                        "complexity": mechanic.get("complexity", "medium")
                    }
                })
        
        # Add score display if any scoring mechanics exist
        if any(m.get("includes_scoring") for m in mechanics):
            components.append({
                "name": "score_display",
                "library": "kenney_ui",
                "component": "ScoreDisplay",
                "variant": "counter",
                "purpose": "score_tracking",
                "library_source": "kenney_ui",
                "library_compliant": True,
                "responsive_design": True,
                "breakpoints": ["sm", "md", "lg"],
                "specifications": {
                    "format": "points",
                    "animation": "count_up",
                    "max_digits": 6
                }
            })
        
        return components
    
    def _add_responsive_specifications(self, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add responsive design specifications to all components."""
        for component in components:
            # Ensure all components have responsive design
            component["responsive_design"] = True
            
            # Add default breakpoints if not specified
            if "breakpoints" not in component:
                component["breakpoints"] = ["sm", "md", "lg"]
            
            # Add accessibility specifications
            component["accessibility"] = {
                "aria_label": component["name"].replace("_", " ").title(),
                "keyboard_navigable": True,
                "screen_reader_friendly": True,
                "focus_visible": True
            }
            
            # Add performance considerations
            component["performance_considerations"] = {
                "lazy_load": component.get("purpose") not in ["navigation", "header"],
                "preload_assets": component.get("requires_assets", False),
                "optimize_images": True
            }
        
        return components
    
    def _validate_component_mapping(self, components: List[Dict[str, Any]], 
                                  story_data: Dict[str, Any]) -> None:
        """Validate that component mapping meets requirements."""
        # Check that all components are from approved libraries
        for component in components:
            if component["library_source"] not in ["shadcn_ui", "kenney_ui"]:
                raise ValueError(f"Component {component['name']} uses unapproved library")
        
        # Check minimum component requirements
        component_purposes = [c["purpose"] for c in components]
        
        if not any(purpose == "main_container" for purpose in component_purposes):
            raise ValueError("Missing main container component")
        
        # Check time constraint compliance
        time_limit = story_data.get("time_constraint_minutes", 10)
        if time_limit <= 10:  # For short tasks, ensure simple UI
            complex_components = [c for c in components if c.get("specifications", {}).get("complexity") == "high"]
            if len(complex_components) > 2:
                raise ValueError("Too many complex components for time-constrained task")
        
        self.logger.debug(f"Component mapping validation passed for {len(components)} components")