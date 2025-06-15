"""
Game Designer Output Contract Models

PURPOSE:
Defines Pydantic models for Game Designer Agent output contracts,
ensuring type safety and contract compliance for Developer handoff.

CONTRACT VALIDATION:
These models implement the exact contract structure for Game Designer -> Developer
handoff according to Implementation_rules.md and enhanced DNA validation.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class GameDesignerOutputContract(BaseModel):
    """
    Game Designer output contract for Developer handoff.
    
    This model ensures the Game Designer -> Developer contract compliance
    and provides complete UX specifications for implementation.
    """
    
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version")
    source_agent: str = Field("game_designer", description="Source agent type")
    target_agent: str = Field("developer", description="Target agent type")
    story_id: str = Field(..., description="Unique story identifier")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Component specifications for Developer
    component_specifications: List[Dict[str, Any]] = Field(..., description="Shadcn/UI component specifications")
    ui_component_mapping: Dict[str, Any] = Field(..., description="Component to library mapping")
    
    # Design specifications
    wireframes: Dict[str, Any] = Field(..., description="Wireframe specifications and flows")
    design_tokens: Dict[str, Any] = Field(..., description="Design system tokens and variables")
    interaction_flows: List[Dict[str, Any]] = Field(..., description="User interaction flow specifications")
    
    # Game mechanics for pedagogical implementation
    game_mechanics: Dict[str, Any] = Field(..., description="Pedagogical game mechanics specification")
    learning_objectives_mapping: Dict[str, Any] = Field(..., description="Learning objectives to UI mapping")
    
    # Asset requirements
    asset_requirements: List[Dict[str, Any]] = Field(..., description="Required assets from Kenney.UI and custom")
    design_assets: Dict[str, Any] = Field(..., description="Design asset specifications")
    
    # Accessibility implementation guide
    accessibility_guidelines: Dict[str, Any] = Field(..., description="WCAG AA implementation guidelines")
    aria_specifications: Dict[str, Any] = Field(..., description="ARIA label and role specifications")
    keyboard_navigation: Dict[str, Any] = Field(..., description="Keyboard navigation specifications")
    
    # Municipal context for implementation
    municipal_implementation_guide: Dict[str, Any] = Field(..., description="Swedish municipal implementation guide")
    professional_tone_guide: Dict[str, Any] = Field(..., description="Professional tone implementation guide")
    
    # Technical specifications
    responsive_design_specifications: Dict[str, Any] = Field(..., description="Responsive design breakpoints and behavior")
    performance_requirements: Dict[str, Any] = Field(..., description="Performance requirements for implementation")
    
    # Quality validation results
    ux_validation_results: Dict[str, Any] = Field(..., description="UX validation against design principles")
    component_library_compliance: Dict[str, Any] = Field(..., description="Component library compliance validation")
    
    # DNA compliance with enhanced validation
    dna_compliance: Dict[str, Any] = Field(..., description="Enhanced DNA validation results")
    
    # Implementation guidance
    developer_implementation_notes: str = Field(..., description="Specific implementation guidance for Developer")
    technical_constraints: List[str] = Field(..., description="Technical constraints and limitations")
    testing_requirements: List[str] = Field(..., description="Testing requirements for implementation")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "contract_version": "1.0",
                "source_agent": "game_designer",
                "target_agent": "developer",
                "story_id": "STORY-GH-123",
                "component_specifications": [
                    {
                        "name": "RegistrationForm",
                        "library_source": "shadcn_ui",
                        "component_type": "form",
                        "props": {
                            "fields": ["email", "password", "confirmPassword"],
                            "validation": "zod_schema",
                            "accessibility": "aria_labels_included"
                        },
                        "styling": {
                            "variant": "municipal",
                            "size": "default",
                            "color_scheme": "professional"
                        }
                    },
                    {
                        "name": "ProgressIndicator",
                        "library_source": "kenney_ui",
                        "component_type": "progress",
                        "game_mechanic": "progress_tracking",
                        "pedagogical_value": "completion_motivation"
                    }
                ],
                "ui_component_mapping": {
                    "shadcn_components": ["Form", "Input", "Button", "Card"],
                    "kenney_assets": ["progress_bar", "success_icon", "warning_icon"],
                    "custom_components": []
                },
                "wireframes": {
                    "screens": [
                        {
                            "name": "registration_start",
                            "layout": "centered_card",
                            "components": ["welcome_message", "start_button"],
                            "flow_position": 1
                        },
                        {
                            "name": "registration_form",
                            "layout": "form_layout",
                            "components": ["form_fields", "progress_indicator", "submit_button"],
                            "flow_position": 2
                        }
                    ]
                },
                "design_tokens": {
                    "colors": {
                        "primary": "#0066CC",
                        "secondary": "#666666",
                        "success": "#00AA00",
                        "error": "#CC0000"
                    },
                    "typography": {
                        "font_family": "Inter",
                        "heading_size": "1.5rem",
                        "body_size": "1rem"
                    },
                    "spacing": {
                        "unit": "0.25rem",
                        "container_padding": "1rem",
                        "component_gap": "0.75rem"
                    }
                },
                "interaction_flows": [
                    {
                        "name": "registration_flow",
                        "steps": [
                            {
                                "step": 1,
                                "action": "display_welcome",
                                "trigger": "page_load",
                                "response": "show_welcome_message"
                            },
                            {
                                "step": 2,
                                "action": "start_registration",
                                "trigger": "button_click",
                                "response": "show_form"
                            },
                            {
                                "step": 3,
                                "action": "submit_form",
                                "trigger": "form_submit",
                                "response": "validate_and_process"
                            }
                        ],
                        "completion_time_estimate": "8 minutes",
                        "complexity_level": "low"
                    }
                ],
                "game_mechanics": {
                    "mechanics": [
                        {
                            "name": "progress_tracking",
                            "type": "visual_feedback",
                            "implementation": "progress_bar_component",
                            "pedagogical_value": "completion_motivation"
                        },
                        {
                            "name": "validation_feedback",
                            "type": "immediate_response",
                            "implementation": "real_time_validation",
                            "pedagogical_value": "learning_reinforcement"
                        }
                    ],
                    "learning_objectives_addressed": [
                        "Understand registration process",
                        "Learn password security",
                        "Practice form completion"
                    ],
                    "pedagogical_effectiveness_score": 4.2
                },
                "accessibility_guidelines": {
                    "wcag_level": "AA",
                    "screen_reader_support": True,
                    "keyboard_navigation": True,
                    "color_contrast_ratio": 4.5,
                    "aria_labels": {
                        "registration_form": "Registreringsformul�r f�r kommunal utbildningsplattform",
                        "email_field": "E-postadress f�r ditt konto",
                        "password_field": "V�lj ett s�kert l�senord"
                    }
                },
                "municipal_implementation_guide": {
                    "swedish_language": True,
                    "government_branding": "subtle",
                    "professional_tone": "formal_but_friendly",
                    "municipal_terminology": [
                        "kommun",
                        "f�rvaltning",
                        "medarbetare",
                        "utbildningsplattform"
                    ]
                },
                "performance_requirements": {
                    "lighthouse_score_min": 90,
                    "api_response_time_max_ms": 200,
                    "bundle_size_increase_max_kb": 50,
                    "first_contentful_paint_max_ms": 1500
                },
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
                    },
                    "enhanced_dna_validation": {
                        "overall_dna_compliant": True,
                        "dna_compliance_score": 4.3,
                        "ui_complexity_level": "low",
                        "learning_flow_quality": "good",
                        "professional_tone_consistency": "good",
                        "validation_timestamp": "2024-06-14T21:00:00.000000"
                    }
                },
                "developer_implementation_notes": "Implement using React with TypeScript. Use Shadcn/UI components for consistent styling. Integrate Kenney.UI assets for game mechanics. Ensure WCAG AA compliance throughout. Focus on simplicity and professional municipal tone.",
                "technical_constraints": [
                    "Must use Shadcn/UI component library",
                    "Kenney.UI assets for game elements only",
                    "React + TypeScript implementation required",
                    "API response time under 200ms",
                    "Mobile-first responsive design"
                ],
                "testing_requirements": [
                    "Unit tests for all components",
                    "Integration tests for form submission",
                    "Accessibility testing with screen readers",
                    "Performance testing for mobile devices",
                    "Municipal user persona testing"
                ]
            }
        }


class GameDesignerComponentSpecification(BaseModel):
    """
    Detailed specification for individual UI components.
    
    Used for precise component implementation guidance.
    """
    
    component_id: str = Field(..., description="Unique component identifier")
    story_id: str = Field(..., description="Associated story identifier")
    
    # Component definition
    component_name: str = Field(..., description="Component name")
    component_type: str = Field(..., description="Component type (form, button, etc.)")
    library_source: str = Field(..., description="Source library (shadcn_ui, kenney_ui, custom)")
    
    # Implementation details
    props_specification: Dict[str, Any] = Field(..., description="Component props and configuration")
    styling_specification: Dict[str, Any] = Field(..., description="Styling and theming details")
    behavior_specification: Dict[str, Any] = Field(..., description="Interaction behavior")
    
    # Accessibility
    accessibility_specification: Dict[str, Any] = Field(..., description="Accessibility implementation details")
    
    # Game mechanics integration
    game_mechanic_integration: Optional[Dict[str, Any]] = Field(None, description="Game mechanics integration")
    pedagogical_function: Optional[str] = Field(None, description="Pedagogical purpose")
    
    # Quality requirements
    performance_requirements: Dict[str, Any] = Field(..., description="Performance requirements")
    testing_requirements: List[str] = Field(..., description="Testing requirements")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "component_id": "registration_form_001",
                "story_id": "STORY-GH-123",
                "component_name": "RegistrationForm",
                "component_type": "form",
                "library_source": "shadcn_ui",
                "props_specification": {
                    "fields": ["email", "password", "confirmPassword"],
                    "validation_schema": "zod",
                    "submit_behavior": "async_validation"
                },
                "styling_specification": {
                    "variant": "municipal",
                    "size": "default",
                    "responsive_breakpoints": ["mobile", "tablet", "desktop"]
                },
                "accessibility_specification": {
                    "aria_label": "Registreringsformular",
                    "keyboard_navigation": True,
                    "screen_reader_announcements": True
                },
                "performance_requirements": {
                    "render_time_max_ms": 100,
                    "bundle_size_impact_kb": 15
                }
            }
        }


class GameDesignerWireframeSpecification(BaseModel):
    """
    Detailed wireframe and user flow specifications.
    
    Used for layout and interaction implementation.
    """
    
    wireframe_id: str = Field(..., description="Unique wireframe identifier")
    story_id: str = Field(..., description="Associated story identifier")
    
    # Wireframe definition
    screen_name: str = Field(..., description="Screen or view name")
    layout_type: str = Field(..., description="Layout type (grid, flex, etc.)")
    
    # Layout specification
    component_layout: List[Dict[str, Any]] = Field(..., description="Component positioning and layout")
    responsive_behavior: Dict[str, Any] = Field(..., description="Responsive design behavior")
    
    # User flow integration
    flow_position: int = Field(..., description="Position in user flow")
    navigation_options: List[Dict[str, Any]] = Field(..., description="Navigation possibilities")
    
    # Interaction design
    user_interactions: List[Dict[str, Any]] = Field(..., description="User interaction specifications")
    feedback_mechanisms: List[Dict[str, Any]] = Field(..., description="User feedback mechanisms")
    
    # Municipal context
    municipal_adaptations: Dict[str, Any] = Field(..., description="Municipal-specific adaptations")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "wireframe_id": "registration_form_wireframe",
                "story_id": "STORY-GH-123",
                "screen_name": "registration_form",
                "layout_type": "centered_card",
                "component_layout": [
                    {
                        "component": "header",
                        "position": "top",
                        "span": "full_width"
                    },
                    {
                        "component": "form_fields",
                        "position": "center",
                        "span": "content_width"
                    },
                    {
                        "component": "submit_button",
                        "position": "bottom_center",
                        "span": "button_width"
                    }
                ],
                "flow_position": 2,
                "user_interactions": [
                    {
                        "interaction": "form_input",
                        "trigger": "field_focus",
                        "feedback": "validation_highlight"
                    }
                ]
            }
        }