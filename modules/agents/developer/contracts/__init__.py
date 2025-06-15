"""
Contract models for DeveloperAgent.

This module provides Pydantic models for input and output contract validation
ensuring type safety and compliance with DigiNativa's contract system.
"""

from .input_models import (
    DeveloperInputContract,
    UIComponent,
    APIEndpoint,
    InteractionFlow,
    GameMechanics,
    StateManagement,
    DNACompliance,
    InputRequirements
)

from .output_models import (
    DeveloperOutputContract,
    ComponentImplementation,
    APIImplementation,
    TestSuite,
    ImplementationDocs,
    ValidationCriteria,
    OutputSpecifications,
    InputRequirementsForTestEngineer,
    QualityGate,
    HandoffCriterion
)

__all__ = [
    # Input models
    "DeveloperInputContract",
    "UIComponent",
    "APIEndpoint", 
    "InteractionFlow",
    "GameMechanics",
    "StateManagement",
    "DNACompliance",
    "InputRequirements",
    
    # Output models
    "DeveloperOutputContract",
    "ComponentImplementation",
    "APIImplementation",
    "TestSuite",
    "ImplementationDocs",
    "ValidationCriteria",
    "OutputSpecifications",
    "InputRequirementsForTestEngineer",
    "QualityGate",
    "HandoffCriterion"
]