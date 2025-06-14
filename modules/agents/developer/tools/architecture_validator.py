"""
ArchitectureValidator - Validates implementation against DigiNativa architecture principles.

PURPOSE:
Ensures all implementations follow DigiNativa's architecture principles:
1. API-first design
2. Stateless backend
3. Separation of concerns
4. Simplicity first

This validator prevents architectural debt and maintains system quality.
"""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ArchitectureValidator:
    """
    Validates architecture compliance for Developer implementations.
    
    ARCHITECTURE PRINCIPLES ENFORCED:
    1. API-First: All communication via REST APIs
    2. Stateless Backend: No server-side sessions
    3. Separation of Concerns: Clean architecture layers
    4. Simplicity First: Minimal complexity
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize ArchitectureValidator."""
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.ArchitectureValidator")
        self.logger.info("ArchitectureValidator initialized")
    
    async def validate_requirements(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate requirements against architecture principles.
        
        Args:
            input_data: Input data from Game Designer
            
        Returns:
            Validation result with errors and warnings
        """
        try:
            errors = []
            warnings = []
            
            # Validate API-first design
            api_errors = self._validate_api_first_design(input_data)
            errors.extend(api_errors)
            
            # Validate stateless backend
            stateless_errors = self._validate_stateless_backend(input_data)
            errors.extend(stateless_errors)
            
            # Validate separation of concerns
            separation_errors = self._validate_separation_of_concerns(input_data)
            errors.extend(separation_errors)
            
            # Validate simplicity
            simplicity_warnings = self._validate_simplicity_first(input_data)
            warnings.extend(simplicity_warnings)
            
            return {
                "is_valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "principles_validated": [
                    "api_first",
                    "stateless_backend", 
                    "separation_of_concerns",
                    "simplicity_first"
                ]
            }
            
        except Exception as e:
            error_msg = f"Architecture validation failed: {str(e)}"
            self.logger.error(error_msg)
            return {
                "is_valid": False,
                "errors": [error_msg],
                "warnings": []
            }