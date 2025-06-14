"""
Input contract models for DeveloperAgent.

PURPOSE:
Defines Pydantic models for validating input contracts from Game Designer
according to Implementation_rules.md specifications.

CRITICAL VALIDATION:
- Contract structure compliance
- Required data validation
- DNA compliance verification
- Game Designer output format validation
"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum


class UIComponent(BaseModel):
    """UI component specification from Game Designer."""
    
    name: str = Field(..., description="Component name in PascalCase")
    type: str = Field(..., description="Component type (page, component, hook, utility)")
    description: Optional[str] = Field(None, description="Component description")
    ui_library_components: List[str] = Field(default_factory=list, description="Shadcn/UI components used")
    props: Dict[str, str] = Field(default_factory=dict, description="Component props with types")
    state: Dict[str, Any] = Field(default_factory=dict, description="State management requirements")
    interactions: List[Dict[str, Any]] = Field(default_factory=list, description="User interactions")
    accessibility: Dict[str, Any] = Field(default_factory=dict, description="Accessibility requirements")
    performance: Dict[str, Any] = Field(default_factory=dict, description="Performance requirements")
    requires_data: bool = Field(False, description="Whether component requires API data")
    
    @validator('name')
    def validate_component_name(cls, v):
        """Validate component name follows conventions."""
        if not v[0].isupper():
            raise ValueError("Component name must start with uppercase letter (PascalCase)")
        if not v.replace('_', '').isalnum():
            raise ValueError("Component name must be alphanumeric (with underscores allowed)")
        return v
    
    @validator('type')
    def validate_component_type(cls, v):
        """Validate component type is recognized."""
        valid_types = ['page', 'component', 'hook', 'utility', 'form', 'layout']
        if v not in valid_types:
            raise ValueError(f"Component type must be one of: {valid_types}")
        return v


class APIEndpoint(BaseModel):
    """API endpoint specification from Game Designer."""
    
    name: str = Field(..., description="Endpoint function name in snake_case")
    method: str = Field(..., description="HTTP method")
    path: str = Field(..., description="API path")
    description: str = Field(..., description="Endpoint description")
    request_model: Dict[str, Any] = Field(default_factory=dict, description="Request model schema")
    response_model: Dict[str, Any] = Field(default_factory=dict, description="Response model schema")
    business_logic: Dict[str, Any] = Field(default_factory=dict, description="Business logic requirements")
    validation_rules: List[Dict[str, Any]] = Field(default_factory=list, description="Validation rules")
    error_handling: Dict[str, Any] = Field(default_factory=dict, description="Error handling strategy")
    security: Dict[str, Any] = Field(default_factory=dict, description="Security requirements")
    performance: Dict[str, Any] = Field(default_factory=dict, description="Performance requirements")
    dependencies: List[str] = Field(default_factory=list, description="External dependencies")
    
    @validator('method')
    def validate_http_method(cls, v):
        """Validate HTTP method is standard."""
        valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        if v.upper() not in valid_methods:
            raise ValueError(f"HTTP method must be one of: {valid_methods}")
        return v.upper()
    
    @validator('path')
    def validate_api_path(cls, v):
        """Validate API path follows REST conventions."""
        if not v.startswith('/'):
            raise ValueError("API path must start with '/'")
        return v
    
    @root_validator
    def validate_stateless_design(cls, values):
        """Validate endpoint follows stateless design principles."""
        business_logic = values.get('business_logic', {})
        
        # Check for stateful violations
        stateful_keywords = ['session', 'global_state', 'server_cache']
        for keyword in stateful_keywords:
            if keyword in str(business_logic).lower():
                raise ValueError(f"Endpoint violates stateless design: contains '{keyword}'")
        
        return values


class InteractionFlow(BaseModel):
    """Interaction flow specification from Game Designer."""
    
    name: str = Field(..., description="Flow name")
    description: Optional[str] = Field(None, description="Flow description")
    steps: List[str] = Field(..., description="Flow steps in order")
    components_involved: List[str] = Field(default_factory=list, description="Components in flow")
    apis_involved: List[str] = Field(default_factory=list, description="APIs in flow")
    error_scenarios: List[Dict[str, Any]] = Field(default_factory=list, description="Error scenarios")
    success_criteria: List[str] = Field(default_factory=list, description="Success criteria")


class GameMechanics(BaseModel):
    """Game mechanics specification from Game Designer."""
    
    title: str = Field(..., description="Feature title")
    description: str = Field(..., description="Feature description")
    learning_objectives: List[str] = Field(default_factory=list, description="Learning objectives")
    pedagogical_approach: str = Field(..., description="Pedagogical approach")
    difficulty_level: str = Field(..., description="Difficulty level")
    estimated_time_minutes: int = Field(..., ge=1, le=60, description="Estimated completion time")
    game_elements: List[Dict[str, Any]] = Field(default_factory=list, description="Game elements")
    
    @validator('estimated_time_minutes')
    def validate_time_constraint(cls, v):
        """Validate time respects DigiNativa's 10-minute constraint."""
        if v > 10:
            raise ValueError("Feature must respect 10-minute time constraint (DNA principle)")
        return v


class StateManagement(BaseModel):
    """State management specification from Game Designer."""
    
    type: str = Field(..., description="State management type")
    client_state: List[str] = Field(default_factory=list, description="Client-side state")
    shared_state: List[str] = Field(default_factory=list, description="Shared state between components")
    persistence: Dict[str, Any] = Field(default_factory=dict, description="State persistence requirements")
    
    @validator('type')
    def validate_stateless_type(cls, v):
        """Validate state management follows stateless principles."""
        if v.lower() not in ['stateless', 'client-only']:
            raise ValueError("State management must be 'stateless' or 'client-only' (architecture principle)")
        return v


class DNACompliance(BaseModel):
    """DNA compliance validation from Game Designer."""
    
    design_principles_validation: Dict[str, bool] = Field(..., description="Design principles validation")
    architecture_compliance: Dict[str, bool] = Field(..., description="Architecture compliance")
    
    @validator('design_principles_validation')
    def validate_design_principles_complete(cls, v):
        """Validate all 5 design principles are addressed."""
        required_principles = {
            'pedagogical_value', 'policy_to_practice', 'time_respect',
            'holistic_thinking', 'professional_tone'
        }
        
        if not required_principles.issubset(set(v.keys())):
            missing = required_principles - set(v.keys())
            raise ValueError(f"Missing design principles: {missing}")
        
        # All principles must be True
        false_principles = [k for k, val in v.items() if not val]
        if false_principles:
            raise ValueError(f"Design principles not met: {false_principles}")
        
        return v
    
    @validator('architecture_compliance')
    def validate_architecture_principles_complete(cls, v):
        """Validate all 4 architecture principles are addressed."""
        required_principles = {
            'api_first', 'stateless_backend', 
            'separation_of_concerns', 'simplicity_first'
        }
        
        if not required_principles.issubset(set(v.keys())):
            missing = required_principles - set(v.keys())
            raise ValueError(f"Missing architecture principles: {missing}")
        
        # All principles must be True
        false_principles = [k for k, val in v.items() if not val]
        if false_principles:
            raise ValueError(f"Architecture principles not met: {false_principles}")
        
        return v


class InputRequirements(BaseModel):
    """Input requirements from Game Designer contract."""
    
    required_files: List[str] = Field(..., description="Required input files")
    required_data: Dict[str, Any] = Field(..., description="Required input data")
    required_validations: List[str] = Field(..., description="Required validations")
    
    @validator('required_data')
    def validate_required_data_structure(cls, v):
        """Validate required data contains expected Game Designer outputs."""
        required_keys = {
            'game_mechanics', 'ui_components', 'interaction_flows', 
            'api_endpoints', 'state_management'
        }
        
        if not required_keys.issubset(set(v.keys())):
            missing = required_keys - set(v.keys())
            raise ValueError(f"Missing required data keys: {missing}")
        
        return v


class DeveloperInputContract(BaseModel):
    """
    Complete input contract for DeveloperAgent from Game Designer.
    
    This model validates the entire contract structure and ensures
    compatibility with DigiNativa's contract system.
    """
    
    contract_version: str = Field(..., description="Contract version")
    contract_type: str = Field(..., description="Contract type")
    story_id: str = Field(..., description="Story identifier")
    source_agent: str = Field(..., description="Source agent")
    target_agent: str = Field(..., description="Target agent")
    dna_compliance: DNACompliance = Field(..., description="DNA compliance validation")
    input_requirements: InputRequirements = Field(..., description="Input requirements")
    
    @validator('contract_version')
    def validate_contract_version(cls, v):
        """Validate contract version is supported."""
        if v != "1.0":
            raise ValueError("Only contract version 1.0 is currently supported")
        return v
    
    @validator('contract_type')
    def validate_contract_type(cls, v):
        """Validate contract type is correct for Developer agent."""
        if v != "design_to_implementation":
            raise ValueError("Developer agent expects 'design_to_implementation' contract type")
        return v
    
    @validator('source_agent')
    def validate_source_agent(cls, v):
        """Validate source agent is Game Designer."""
        if v != "game_designer":
            raise ValueError("Developer agent only accepts contracts from 'game_designer'")
        return v
    
    @validator('target_agent')
    def validate_target_agent(cls, v):
        """Validate target agent is Developer."""
        if v != "developer":
            raise ValueError("Contract target agent must be 'developer'")
        return v
    
    @validator('story_id')
    def validate_story_id_format(cls, v):
        """Validate story ID follows DigiNativa format."""
        if not v.startswith("STORY-"):
            raise ValueError("Story ID must start with 'STORY-'")
        return v
    
    @root_validator
    def validate_complete_contract(cls, values):
        """Validate complete contract integrity."""
        # Ensure DNA compliance is properly validated
        dna_compliance = values.get('dna_compliance')
        if dna_compliance:
            # Verify both design and architecture compliance
            design_valid = all(dna_compliance.design_principles_validation.values())
            arch_valid = all(dna_compliance.architecture_compliance.values())
            
            if not (design_valid and arch_valid):
                raise ValueError("Contract DNA compliance validation failed")
        
        # Validate input requirements contain proper Game Designer outputs
        input_reqs = values.get('input_requirements')
        if input_reqs:
            required_data = input_reqs.required_data
            
            # Parse and validate game mechanics
            if 'game_mechanics' in required_data:
                GameMechanics(**required_data['game_mechanics'])
            
            # Parse and validate UI components
            if 'ui_components' in required_data:
                for component_data in required_data['ui_components']:
                    UIComponent(**component_data)
            
            # Parse and validate API endpoints
            if 'api_endpoints' in required_data:
                for endpoint_data in required_data['api_endpoints']:
                    APIEndpoint(**endpoint_data)
            
            # Parse and validate interaction flows
            if 'interaction_flows' in required_data:
                for flow_data in required_data['interaction_flows']:
                    InteractionFlow(**flow_data)
            
            # Parse and validate state management
            if 'state_management' in required_data:
                StateManagement(**required_data['state_management'])
        
        return values
    
    class Config:
        """Pydantic configuration."""
        
        extra = "forbid"  # Prevent additional fields
        validate_assignment = True  # Validate on assignment
        schema_extra = {
            "example": {
                "contract_version": "1.0",
                "contract_type": "design_to_implementation",
                "story_id": "STORY-001-001",
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
                        "docs/specs/game_design_STORY-001-001.md",
                        "docs/specs/ux_specification_STORY-001-001.md",
                        "docs/specs/component_mapping_STORY-001-001.json"
                    ],
                    "required_data": {
                        "game_mechanics": {
                            "title": "User Registration",
                            "description": "Enable users to register for DigiNativa",
                            "learning_objectives": ["Understand registration process"],
                            "pedagogical_approach": "guided_practice",
                            "difficulty_level": "beginner",
                            "estimated_time_minutes": 5
                        },
                        "ui_components": [
                            {
                                "name": "RegistrationForm",
                                "type": "form",
                                "ui_library_components": ["Button", "Input", "Card"],
                                "accessibility": {"role": "form"}
                            }
                        ],
                        "interaction_flows": [
                            {
                                "name": "registration_flow",
                                "steps": ["fill_form", "validate", "submit"]
                            }
                        ],
                        "api_endpoints": [
                            {
                                "name": "register_user",
                                "method": "POST",
                                "path": "/register",
                                "description": "Register new user"
                            }
                        ],
                        "state_management": {
                            "type": "stateless",
                            "client_state": ["form_data"]
                        }
                    },
                    "required_validations": [
                        "component_mapping_complete",
                        "technical_specifications_clear",
                        "architecture_constraints_defined"
                    ]
                }
            }
        }