"""
Contract Validator - The most critical component of the DigiNativa AI Team system.

PURPOSE:
Validates all agent-to-agent contracts against schema, business rules, 
DNA compliance, and quality gates to prevent integration failures 
and maintain system modularity.

CRITICAL IMPORTANCE:
This is the foundation that enables:
- Modular agent development
- Prevention of invalid handoffs  
- DNA compliance enforcement
- Quality gate validation

ADAPTATION GUIDE:
🔧 To adapt for your project:
1. Update agent_sequences for your workflow
2. Modify quality_gate_checkers for your quality standards
3. Adjust dna_validation for your principles
"""

import json
import jsonschema
import logging
from typing import Dict, List, Any, Optional, Set
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass


# Setup logging
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Structured result from contract validation."""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    validation_timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for API responses."""
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "validation_timestamp": self.validation_timestamp
        }


class ContractValidationError(Exception):
    """Raised when contract validation fails critically."""
    
    def __init__(self, message: str, errors: List[str]):
        super().__init__(message)
        self.errors = errors


class ContractValidator:
    """
    Validates agent contracts against schema and business rules.
    
    This class is the cornerstone of the entire AI team system.
    ALL agent interactions must pass through this validator.
    
    NEVER skip validation - it will break the system's modularity.
    """
    
    def __init__(self, schema_path: str = "docs/contracts/agent_contract_schema.json"):
        """
        Initialize the contract validator.
        
        Args:
            schema_path: Path to the JSON schema file for contract validation
            
        Raises:
            FileNotFoundError: If schema file doesn't exist
            json.JSONDecodeError: If schema file contains invalid JSON
        """
        self.schema_path = Path(schema_path)
        
        # Setup logging for this validator instance
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.info(f"Initializing ContractValidator with schema: {schema_path}")
        
        # Load and validate the JSON schema
        try:
            self.schema = self._load_schema()
            self.logger.info("JSON schema loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load schema from {schema_path}: {e}")
            raise
        
        # Define valid agent sequences (CRITICAL - these enforce workflow)
        self.valid_agent_sequences = {
            "github": ["project_manager"],  # GitHub issues start the workflow
            "project_manager": ["game_designer"],
            "game_designer": ["developer"],
            "developer": ["test_engineer"],
            "test_engineer": ["qa_tester"],
            "qa_tester": ["quality_reviewer"],
            "quality_reviewer": ["project_manager"]  # For next iteration
        }
        
        # Required design principles (NEVER change these for DigiNativa)
        self.required_design_principles = {
            "pedagogical_value",
            "policy_to_practice", 
            "time_respect",
            "holistic_thinking",
            "professional_tone"
        }
        
        # Required architecture principles (NEVER change these for DigiNativa)
        self.required_architecture_principles = {
            "api_first",
            "stateless_backend",
            "separation_of_concerns",
            "simplicity_first"
        }
        
        # Known machine-readable quality gate patterns
        self.machine_readable_quality_patterns = {
            "test_coverage", "eslint", "typescript", "lighthouse", 
            "api_response_time", "bundle_size", "security_scan",
            "wcag_compliance", "performance_benchmark", "dna_compliance"
        }
    
    def _load_schema(self) -> Dict[str, Any]:
        """
        Load and parse the JSON schema for contract validation.
        
        Returns:
            Parsed JSON schema dictionary
            
        Raises:
            FileNotFoundError: If schema file doesn't exist
            json.JSONDecodeError: If schema file is invalid JSON
            PermissionError: If schema file cannot be read
        """
        try:
            # Check if schema file exists
            if not self.schema_path.exists():
                raise FileNotFoundError(
                    f"Schema file not found: {self.schema_path}. "
                    f"Make sure to create the schema file at {self.schema_path.absolute()}"
                )
            
            # Check if file is readable
            if not self.schema_path.is_file():
                raise FileNotFoundError(
                    f"Schema path exists but is not a file: {self.schema_path}"
                )
            
            # Read and parse the JSON schema
            with open(self.schema_path, 'r', encoding='utf-8') as schema_file:
                schema_content = schema_file.read()
                
                if not schema_content.strip():
                    raise json.JSONDecodeError(
                        "Schema file is empty", 
                        str(self.schema_path), 
                        0
                    )
                
                schema = json.loads(schema_content)
                
                # Basic validation that this looks like a JSON schema
                if not isinstance(schema, dict):
                    raise ValueError("Schema must be a JSON object (dictionary)")
                
                if "$schema" not in schema:
                    self.logger.warning(
                        "Schema file doesn't contain $schema property - "
                        "this may not be a valid JSON Schema"
                    )
                
                self.logger.debug(f"Successfully loaded schema with {len(schema)} top-level properties")
                return schema
                
        except FileNotFoundError:
            self.logger.error(f"Schema file not found: {self.schema_path}")
            raise
        
        except PermissionError as e:
            self.logger.error(f"Permission denied reading schema file {self.schema_path}: {e}")
            raise
            
        except json.JSONDecodeError as e:
            self.logger.error(
                f"Invalid JSON in schema file {self.schema_path}: {e.msg} "
                f"at line {e.lineno}, column {e.colno}"
            )
            raise
            
        except Exception as e:
            self.logger.error(f"Unexpected error loading schema {self.schema_path}: {e}")
            raise
    
    def validate_contract(self, contract: Dict[str, Any]) -> ValidationResult:
        """
        Complete contract validation including schema, business rules, and DNA compliance.
        
        This is the main entry point for all contract validation.
        NEVER bypass this method - it enforces system integrity.
        
        Args:
            contract: The contract dictionary to validate
            
        Returns:
            ValidationResult with validation status, errors, and warnings
            
        Raises:
            ContractValidationError: For critical validation failures
        """
        pass  # TODO: Implement main validation logic
    
    def _validate_schema(self, contract: Dict[str, Any]) -> List[str]:
        """
        Validate contract against JSON schema.
        
        Args:
            contract: Contract to validate
            
        Returns:
            List of schema validation errors (empty if valid)
        """
        errors = []
        
        try:
            # Perform JSON schema validation
            jsonschema.validate(instance=contract, schema=self.schema)
            
            # If we get here, validation passed
            self.logger.debug("Contract passed JSON schema validation")
            return []
            
        except jsonschema.ValidationError as e:
            # Convert validation error to human-readable format
            error_message = self._format_validation_error(e)
            errors.append(error_message)
            
            self.logger.warning(f"Schema validation failed: {error_message}")
            
        except jsonschema.SchemaError as e:
            # This indicates a problem with our schema file itself
            schema_error = f"JSON Schema itself is invalid: {e.message}"
            errors.append(schema_error)
            
            self.logger.error(f"Schema file error: {schema_error}")
            
        except Exception as e:
            # Catch any other unexpected errors during validation
            unexpected_error = f"Unexpected error during schema validation: {str(e)}"
            errors.append(unexpected_error)
            
            self.logger.error(f"Unexpected schema validation error: {e}")
        
        return errors
    
    def _format_validation_error(self, error: jsonschema.ValidationError) -> str:
        """
        Format a jsonschema ValidationError into a human-readable error message.
        
        Args:
            error: The ValidationError from jsonschema
            
        Returns:
            Formatted error message string
        """
        # Build path to the problematic field
        if error.absolute_path:
            field_path = ".".join(str(part) for part in error.absolute_path)
            location = f"at field '{field_path}'"
        else:
            location = "at root level"
        
        # Get the validation error type and message
        validator = error.validator
        message = error.message
        
        # Create descriptive error message based on validator type
        if validator == "required":
            missing_field = error.message.split("'")[1] if "'" in error.message else "unknown"
            return f"Missing required field '{missing_field}' {location}"
            
        elif validator == "enum":
            return f"Invalid value {location}: {message}"
            
        elif validator == "pattern":
            return f"Field {location} does not match required pattern: {message}"
            
        elif validator == "type":
            return f"Field {location} has wrong type: {message}"
            
        elif validator == "additionalProperties":
            return f"Unexpected additional property {location}: {message}"
            
        else:
            # Generic error message for other validation types
            return f"Schema validation error {location}: {message}"
    
    def _validate_business_rules(self, contract: Dict[str, Any]) -> List[str]:
        """
        Validate contract against business rules.
        
        Business rules include:
        - Valid agent sequence
        - Story ID format validation
        - File path traceability
        - Required field presence
        
        Args:
            contract: Contract to validate
            
        Returns:
            List of business rule validation errors
        """
        pass  # TODO: Implement business rules validation
    
    def _validate_dna_compliance(self, contract: Dict[str, Any]) -> List[str]:
        """
        Validate DNA compliance section completeness and correctness.
        
        This ensures all contracts explicitly validate against:
        - All 5 design principles
        - All 4 architecture principles
        
        Args:
            contract: Contract to validate
            
        Returns:
            List of DNA compliance errors
        """
        pass  # TODO: Implement DNA compliance validation
    
    def _validate_quality_gates(self, contract: Dict[str, Any]) -> List[str]:
        """
        Validate quality gates are properly defined and machine-readable.
        
        Args:
            contract: Contract to validate
            
        Returns:
            List of quality gate warnings (not errors - these are suggestions)
        """
        pass  # TODO: Implement quality gates validation
    
    def _validate_agent_sequence(self, source_agent: str, target_agent: str) -> bool:
        """
        Validate that agent handoff sequence follows defined workflow.
        
        This is CRITICAL for maintaining proper workflow order.
        Invalid sequences indicate system design errors.
        
        Args:
            source_agent: Agent creating the contract
            target_agent: Agent receiving the contract
            
        Returns:
            True if sequence is valid, False otherwise
        """
        pass  # TODO: Implement agent sequence validation
    
    def _validate_story_id_format(self, story_id: str) -> bool:
        """
        Validate story ID follows required format: STORY-{feature_id}-{increment}
        
        Examples of valid story IDs:
        - STORY-001-001
        - STORY-USER-REG-002
        - STORY-DASHBOARD-001
        
        Args:
            story_id: Story ID to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        pass  # TODO: Implement story ID format validation
    
    def _validate_file_paths(self, contract: Dict[str, Any]) -> bool:
        """
        Validate that file paths follow project conventions.
        
        Rules:
        - All file paths must contain story_id for traceability
        - Paths can use {story_id} template format
        - Input and output files must be traceable
        
        Args:
            contract: Contract to validate
            
        Returns:
            True if all file paths are valid, False otherwise
        """
        pass  # TODO: Implement file path validation
    
    def _validate_design_principles_completeness(self, design_principles: Dict[str, Any]) -> List[str]:
        """
        Validate that all required design principles are present and correctly typed.
        
        Args:
            design_principles: Design principles section from contract
            
        Returns:
            List of missing or invalid design principles
        """
        pass  # TODO: Implement design principles validation
    
    def _validate_architecture_principles_completeness(self, architecture_compliance: Dict[str, Any]) -> List[str]:
        """
        Validate that all required architecture principles are present and correctly typed.
        
        Args:
            architecture_compliance: Architecture compliance section from contract
            
        Returns:
            List of missing or invalid architecture principles
        """
        pass  # TODO: Implement architecture principles validation
    
    def _is_valid_quality_gate_format(self, gate: str) -> bool:
        """
        Check if quality gate follows machine-readable format.
        
        Machine-readable gates can be automatically checked by the system.
        Non-machine-readable gates require manual verification.
        
        Args:
            gate: Quality gate string to validate
            
        Returns:
            True if gate appears to be machine-readable
        """
        pass  # TODO: Implement quality gate format validation
    
    def get_valid_next_agents(self, source_agent: str) -> List[str]:
        """
        Get list of valid target agents for a given source agent.
        
        Useful for UI components and debugging.
        
        Args:
            source_agent: Source agent to get valid targets for
            
        Returns:
            List of valid target agent names
        """
        return self.valid_agent_sequences.get(source_agent, [])
    
    def validate_contract_chain(self, contracts: List[Dict[str, Any]]) -> ValidationResult:
        """
        Validate a chain of contracts to ensure they form a valid workflow.
        
        This method validates:
        - Each individual contract
        - Proper handoff sequence
        - Data flow continuity
        - Story ID consistency
        
        Args:
            contracts: List of contracts in execution order
            
        Returns:
            ValidationResult for the entire chain
        """
        pass  # TODO: Implement contract chain validation


# Utility functions for external use

def validate_single_contract(contract: Dict[str, Any], 
                           schema_path: str = "docs/contracts/agent_contract_schema.json") -> Dict[str, Any]:
    """
    Convenience function for validating a single contract.
    
    Args:
        contract: Contract dictionary to validate
        schema_path: Path to schema file
        
    Returns:
        Validation result dictionary
    """
    validator = ContractValidator(schema_path)
    result = validator.validate_contract(contract)
    return result.to_dict()


def get_contract_template(source_agent: str, target_agent: str, story_id: str) -> Dict[str, Any]:
    """
    Generate a contract template for the given agent pair.
    
    Useful for development and testing.
    
    Args:
        source_agent: Agent creating the contract
        target_agent: Agent receiving the contract  
        story_id: Story ID for the work
        
    Returns:
        Contract template dictionary
    """
    pass  # TODO: Implement contract template generation


# Module-level constants for external use
REQUIRED_DESIGN_PRINCIPLES = {
    "pedagogical_value",
    "policy_to_practice", 
    "time_respect",
    "holistic_thinking",
    "professional_tone"
}

REQUIRED_ARCHITECTURE_PRINCIPLES = {
    "api_first",
    "stateless_backend",
    "separation_of_concerns",
    "simplicity_first"
}

VALID_AGENT_SEQUENCES = {
    "github": ["project_manager"],
    "project_manager": ["game_designer"],
    "game_designer": ["developer"],
    "developer": ["test_engineer"],
    "test_engineer": ["qa_tester"],
    "qa_tester": ["quality_reviewer"],
    "quality_reviewer": ["project_manager"]
}