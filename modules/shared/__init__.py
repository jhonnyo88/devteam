"""
Shared modules for the DigiNativa AI Team system.

This package contains core components used by all agents:
- BaseAgent: Foundation class for all agents
- ContractValidator: Contract validation and compliance
- Exceptions: System-specific exception types
- StateManager: Work state persistence and recovery
"""

from .base_agent import BaseAgent, AgentExecutionResult, AgentState
from .contract_validator import ContractValidator, ValidationResult, ContractValidationError
from .exceptions import (
    DigiNativaError, DNAComplianceError, QualityGateError,
    AgentExecutionError, StateManagementError, HandoffError,
    ConfigurationError, ExternalServiceError, BusinessLogicError,
    SecurityError
)

__all__ = [
    # Base agent functionality
    "BaseAgent",
    "AgentExecutionResult", 
    "AgentState",
    
    # Contract validation
    "ContractValidator",
    "ValidationResult",
    "ContractValidationError",
    
    # Exception types
    "DigiNativaError",
    "DNAComplianceError",
    "QualityGateError", 
    "AgentExecutionError",
    "StateManagementError",
    "HandoffError",
    "ConfigurationError",
    "ExternalServiceError",
    "BusinessLogicError",
    "SecurityError"
]