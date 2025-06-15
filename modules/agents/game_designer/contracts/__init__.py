"""
Game Designer Contract Models Package

PURPOSE:
Exports all Pydantic contract models for Game Designer agent,
enabling type-safe communication with Project Manager (input)
and Developer (output) agents.

USAGE:
from modules.agents.game_designer.contracts import (
    GameDesignerInputContract,
    GameDesignerOutputContract
)
"""

from .input_models import (
    GameDesignerInputContract,
    GameDesignerValidationContract
)

from .output_models import (
    GameDesignerOutputContract,
    GameDesignerComponentSpecification,
    GameDesignerWireframeSpecification
)

__all__ = [
    # Input contracts (from Project Manager)
    "GameDesignerInputContract",
    "GameDesignerValidationContract",
    
    # Output contracts (to Developer)
    "GameDesignerOutputContract",
    "GameDesignerComponentSpecification", 
    "GameDesignerWireframeSpecification"
]