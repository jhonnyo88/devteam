"""
Custom exceptions for the DigiNativa AI Team system.

PURPOSE:
Provides specific exception types that enable precise error handling
and debugging across the entire agent system.

CRITICAL IMPORTANCE:
- Enables specific error handling for different failure modes
- Provides clear error messages for debugging and monitoring
- Maintains system stability by handling errors gracefully
- Supports automated error recovery and notification

ADAPTATION GUIDE:
=' To adapt for your project:
1. Add project-specific exception types as needed
2. Customize error messages for your domain
3. Add additional context fields for your monitoring needs
"""

from typing import List, Optional, Dict, Any


class DigiNativaError(Exception):
    """
    Base exception for all DigiNativa AI Team system errors.
    
    All other exceptions inherit from this to enable catching
    all system errors with a single exception type.
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.details = details or {}
        self.timestamp = self._get_timestamp()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for error tracking."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging and APIs."""
        return {
            "error_type": self.__class__.__name__,
            "message": str(self),
            "details": self.details,
            "timestamp": self.timestamp
        }


class ContractValidationError(DigiNativaError):
    """
    Raised when contract validation fails.
    
    This is critical - contract validation failures indicate
    system integrity issues that must be resolved immediately.
    """
    
    def __init__(self, message: str, validation_errors: List[str], contract_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.validation_errors = validation_errors
        self.contract_data = contract_data
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["validation_errors"] = self.validation_errors
        if self.contract_data:
            result["contract_summary"] = {
                "story_id": self.contract_data.get("story_id", "unknown"),
                "source_agent": self.contract_data.get("source_agent", "unknown"),
                "target_agent": self.contract_data.get("target_agent", "unknown")
            }
        return result


class DNAComplianceError(DigiNativaError):
    """
    Raised when agent output violates DNA principles.
    
    DNA compliance is NON-NEGOTIABLE for DigiNativa.
    These errors indicate fundamental quality issues.
    """
    
    def __init__(self, message: str, violated_principles: Optional[List[str]] = None, agent_type: Optional[str] = None):
        super().__init__(message)
        self.violated_principles = violated_principles or []
        self.agent_type = agent_type
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["violated_principles"] = self.violated_principles
        result["agent_type"] = self.agent_type
        return result


class QualityGateError(DigiNativaError):
    """
    Raised when quality gates fail during agent execution.
    
    Quality gates protect our client satisfaction metrics.
    These errors must be resolved before handoff to next agent.
    """
    
    def __init__(self, message: str, failed_gate: str, gate_details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.failed_gate = failed_gate
        self.gate_details = gate_details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["failed_gate"] = self.failed_gate
        result["gate_details"] = self.gate_details
        return result


class AgentExecutionError(DigiNativaError):
    """
    Raised when agent execution fails unexpectedly.
    
    This covers general execution failures that don't fit
    other specific error categories.
    """
    
    def __init__(self, message: str, agent_id: str, story_id: Optional[str] = None, 
                 execution_context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.agent_id = agent_id
        self.story_id = story_id
        self.execution_context = execution_context or {}
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["agent_id"] = self.agent_id
        result["story_id"] = self.story_id
        result["execution_context"] = self.execution_context
        return result


class StateManagementError(DigiNativaError):
    """
    Raised when agent state management operations fail.
    
    State management is critical for recovery and monitoring.
    These errors indicate storage or serialization issues.
    """
    
    def __init__(self, message: str, operation: Optional[str] = None, state_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.operation = operation  # 'save', 'load', 'cleanup', etc.
        self.state_data = state_data
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["operation"] = self.operation
        if self.state_data:
            result["state_summary"] = {
                "agent_id": self.state_data.get("agent_id", "unknown"),
                "story_id": self.state_data.get("story_id", "unknown"),
                "status": self.state_data.get("status", "unknown")
            }
        return result


class HandoffError(DigiNativaError):
    """
    Raised when agent handoff fails.
    
    Handoffs are critical transition points in our workflow.
    These errors indicate agent communication or sequencing issues.
    """
    
    def __init__(self, message: str, source_agent: str, target_agent: str, 
                 handoff_criteria: Optional[List[str]] = None):
        super().__init__(message)
        self.source_agent = source_agent
        self.target_agent = target_agent
        self.handoff_criteria = handoff_criteria or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["source_agent"] = self.source_agent
        result["target_agent"] = self.target_agent
        result["handoff_criteria"] = self.handoff_criteria
        return result


class ConfigurationError(DigiNativaError):
    """
    Raised when agent or system configuration is invalid.
    
    Configuration errors prevent agents from initializing
    or operating correctly.
    """
    
    def __init__(self, message: str, config_section: Optional[str] = None, 
                 invalid_fields: Optional[List[str]] = None):
        super().__init__(message)
        self.config_section = config_section
        self.invalid_fields = invalid_fields or []
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["config_section"] = self.config_section
        result["invalid_fields"] = self.invalid_fields
        return result


class ExternalServiceError(DigiNativaError):
    """
    Raised when external services (GitHub, APIs, etc.) fail.
    
    External service failures require different handling
    strategies like retries and fallbacks.
    """
    
    def __init__(self, message: str, service_name: str, status_code: Optional[int] = None,
                 retry_after: Optional[int] = None):
        super().__init__(message)
        self.service_name = service_name
        self.status_code = status_code
        self.retry_after = retry_after  # Seconds to wait before retry
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["service_name"] = self.service_name
        result["status_code"] = self.status_code
        result["retry_after"] = self.retry_after
        return result


class BusinessLogicError(DigiNativaError):
    """
    Raised when business logic validation fails.
    
    Business logic errors indicate violations of domain-specific
    rules that are not covered by contract or DNA validation.
    """
    
    def __init__(self, message: str, business_rule: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.business_rule = business_rule
        self.context = context or {}
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["business_rule"] = self.business_rule
        result["context"] = self.context
        return result


class SecurityError(DigiNativaError):
    """
    Raised when security validations fail.
    
    Security errors require immediate attention and may
    indicate malicious activity or configuration issues.
    """
    
    def __init__(self, message: str, security_check: str, severity: str = "high"):
        super().__init__(message)
        self.security_check = security_check
        self.severity = severity  # 'low', 'medium', 'high', 'critical'
    
    def to_dict(self) -> Dict[str, Any]:
        result = super().to_dict()
        result["security_check"] = self.security_check
        result["severity"] = self.severity
        return result


# Utility functions for error handling

def format_error_for_logging(error: Exception) -> Dict[str, Any]:
    """
    Format any exception for structured logging.
    
    Args:
        error: Exception to format
        
    Returns:
        Dictionary suitable for structured logging
    """
    if isinstance(error, DigiNativaError):
        return error.to_dict()
    else:
        return {
            "error_type": type(error).__name__,
            "message": str(error),
            "details": {},
            "timestamp": None
        }


def is_retryable_error(error: Exception) -> bool:
    """
    Determine if an error should trigger a retry.
    
    Args:
        error: Exception to check
        
    Returns:
        True if error is retryable, False otherwise
    """
    # External service errors are often retryable
    if isinstance(error, ExternalServiceError):
        return True
    
    # State management errors might be retryable
    if isinstance(error, StateManagementError):
        return True
    
    # Contract, DNA, and quality gate errors are NOT retryable
    # They indicate fundamental problems that need fixing
    if isinstance(error, (ContractValidationError, DNAComplianceError, QualityGateError)):
        return False
    
    # Security errors are NOT retryable
    if isinstance(error, SecurityError):
        return False
    
    # Configuration errors are NOT retryable
    if isinstance(error, ConfigurationError):
        return False
    
    # General execution errors might be retryable depending on cause
    if isinstance(error, AgentExecutionError):
        # Check if it's a temporary issue
        return "timeout" in str(error).lower() or "connection" in str(error).lower()
    
    # Unknown errors are not retryable by default
    return False


def get_error_recovery_strategy(error: Exception) -> str:
    """
    Get recommended recovery strategy for an error.
    
    Args:
        error: Exception to analyze
        
    Returns:
        Recovery strategy string
    """
    if isinstance(error, ContractValidationError):
        return "fix_contract_and_retry"
    
    elif isinstance(error, DNAComplianceError):
        return "review_dna_principles_and_fix"
    
    elif isinstance(error, QualityGateError):
        return "improve_deliverables_and_retry"
    
    elif isinstance(error, ExternalServiceError):
        return "retry_with_backoff"
    
    elif isinstance(error, StateManagementError):
        return "check_storage_and_retry"
    
    elif isinstance(error, ConfigurationError):
        return "fix_configuration"
    
    elif isinstance(error, SecurityError):
        return "investigate_security_issue"
    
    else:
        return "manual_investigation_required"