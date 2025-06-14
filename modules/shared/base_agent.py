"""
BaseAgent - The foundation class for all AI agents in the DigiNativa system.

PURPOSE:
Provides common functionality and enforces contract compliance
for all agents in the team. This is the cornerstone that enables
our modular architecture and prevents agent coupling.

CRITICAL IMPORTANCE:
- Ensures all agents follow the same contract protocols
- Enforces DNA compliance for every agent action
- Provides state management for recovery and monitoring
- Standardizes error handling across the entire system

ADAPTATION GUIDE:
=' To adapt for your project:
1. Update agent_types list for your specific agents
2. Modify validation rules for your quality standards
3. Adjust state management for your persistence needs
4. Customize error handling for your requirements

CONTRACT PROTECTION:
This class is SACRED - it protects our contract system.
NEVER modify without ensuring backward compatibility.
"""

import json
import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, Set
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

# Import our critical shared components
from .contract_validator import ContractValidator, ValidationResult, ContractValidationError
from .exceptions import (
    DNAComplianceError, AgentExecutionError, StateManagementError,
    QualityGateError, HandoffError
)


# Setup logging for this module
logger = logging.getLogger(__name__)


@dataclass
class AgentExecutionResult:
    """
    Structured result from agent execution.
    
    This standardizes how all agents report their execution results,
    enabling consistent monitoring and debugging across the system.
    """
    success: bool
    agent_id: str
    story_id: str
    execution_time_seconds: float
    output_contract: Optional[Dict[str, Any]]
    error_message: Optional[str]
    warnings: List[str]
    quality_gate_results: Dict[str, bool]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses and logging."""
        return asdict(self)


@dataclass
class AgentState:
    """
    Agent work state for persistence and recovery.
    
    Enables agents to resume work after interruptions or crashes,
    critical for maintaining system reliability in production.
    """
    agent_id: str
    story_id: str
    status: str  # 'started', 'in_progress', 'completed', 'error'
    input_contract: Optional[Dict[str, Any]]
    output_contract: Optional[Dict[str, Any]]
    progress_data: Dict[str, Any]
    error_data: Optional[Dict[str, Any]]
    started_at: str
    last_updated: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for persistence."""
        return asdict(self)


class BaseAgent(ABC):
    """
    Base class for all AI agents in the DigiNativa system.
    
    This class provides the foundation that enables:
    - Modular agent development
    - Contract-based communication
    - DNA compliance enforcement
    - Quality gate validation
    - State management and recovery
    - Standardized error handling
    
    NEVER skip the validation methods - they protect system integrity.
    """
    
    def __init__(self, agent_id: str, agent_type: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the base agent.
        
        Args:
            agent_id: Unique identifier for this agent instance
            agent_type: Type of agent (must match valid agent types)
            config: Optional configuration dictionary
            
        Raises:
            ValueError: If agent_type is not valid
            ContractValidationError: If configuration is invalid
        """
        # Validate agent type
        valid_agent_types = {
            "project_manager", "game_designer", "developer",
            "test_engineer", "qa_tester", "quality_reviewer"
        }
        
        if agent_type not in valid_agent_types:
            raise ValueError(f"Invalid agent_type '{agent_type}'. Must be one of: {valid_agent_types}")
        
        # Set core properties
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config or {}
        
        # Setup logging for this agent instance
        self.logger = logging.getLogger(f"{__name__}.{agent_type}.{agent_id}")
        self.logger.info(f"Initializing {agent_type} agent with ID: {agent_id}")
        
        # Initialize critical system components
        try:
            self.contract_validator = ContractValidator()
            self.logger.info("ContractValidator initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize ContractValidator: {e}")
            raise ContractValidationError(f"ContractValidator initialization failed: {e}", [str(e)])
        
        # Initialize state management
        self.state_storage_path = Path(self.config.get("state_storage_path", "data/agent_states"))
        self.state_storage_path.mkdir(parents=True, exist_ok=True)
        
        # Current work state
        self.current_state: Optional[AgentState] = None
        self.execution_start_time: Optional[datetime] = None
        
        # Quality gate tracking
        self.quality_gates_passed: Dict[str, bool] = {}
        
        # DNA compliance requirements (NEVER change these for DigiNativa)
        self.required_design_principles = {
            "pedagogical_value", "policy_to_practice", "time_respect",
            "holistic_thinking", "professional_tone"
        }
        
        self.required_architecture_principles = {
            "api_first", "stateless_backend",
            "separation_of_concerns", "simplicity_first"
        }
        
        self.logger.info(f"BaseAgent {agent_id} initialized successfully")
    
    @abstractmethod
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process work according to input contract and return output contract.
        
        This method must be implemented by each specific agent.
        It contains the core business logic that makes each agent unique.
        
        Args:
            input_contract: Validated input contract from previous agent
            
        Returns:
            Output contract for next agent in the workflow
            
        Raises:
            AgentExecutionError: If processing fails
            DNAComplianceError: If output violates DNA principles
        """
        pass
    
    @abstractmethod
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """
        Check specific quality gate - implemented by each agent.
        
        Each agent defines its own quality gates based on its responsibilities.
        This method validates that specific quality criteria are met.
        
        Args:
            gate: Quality gate identifier to check
            deliverables: Agent deliverables to validate
            
        Returns:
            True if quality gate passes, False otherwise
        """
        pass
    
    async def execute_work(self, input_contract: Dict[str, Any]) -> AgentExecutionResult:
        """
        Main execution method with full validation and state management.
        
        This is the primary entry point for agent work execution.
        It orchestrates the entire agent workflow:
        1. Input validation
        2. State initialization  
        3. Work processing
        4. Output validation
        5. Quality gate checking
        6. State persistence
        
        Args:
            input_contract: Contract defining work to be performed
            
        Returns:
            AgentExecutionResult with execution details and output
            
        Raises:
            ContractValidationError: If input contract is invalid
            DNAComplianceError: If output violates DNA principles
            QualityGateError: If quality gates fail
            AgentExecutionError: If execution fails
        """
        self.execution_start_time = datetime.now()
        story_id = input_contract.get("story_id", "unknown")
        
        try:
            self.logger.info(f"Starting work execution for story: {story_id}")
            
            # Step 1: Validate input contract
            self.logger.debug("Validating input contract")
            validation_result = self.contract_validator.validate_contract(input_contract)
            
            if not validation_result.is_valid:
                error_msg = f"Input contract validation failed: {validation_result.errors}"
                self.logger.error(error_msg)
                raise ContractValidationError(error_msg, validation_result.errors)
            
            if validation_result.warnings:
                self.logger.warning(f"Contract validation warnings: {validation_result.warnings}")
            
            # Step 2: Initialize work state
            self.logger.debug("Initializing agent state")
            await self._initialize_work_state(input_contract)
            
            # Step 3: Process the work (delegate to specific agent implementation)
            self.logger.info("Processing work according to contract")
            output_contract = await self.process_contract(input_contract)
            
            # Step 4: Validate output against DNA principles
            self.logger.debug("Validating DNA compliance")
            if not self._validate_dna_compliance(output_contract):
                error_msg = f"Output violates DNA principles for {self.agent_type}"
                self.logger.error(error_msg)
                raise DNAComplianceError(error_msg)
            
            # Step 5: Validate quality gates
            self.logger.debug("Checking quality gates")
            quality_gates = output_contract.get("quality_gates", [])
            deliverables = output_contract.get("output_specifications", {}).get("deliverable_data", {})
            
            quality_gate_results = {}
            for gate in quality_gates:
                passed = self._check_quality_gate(gate, deliverables)
                quality_gate_results[gate] = passed
                
                if not passed:
                    error_msg = f"Quality gate '{gate}' failed for {self.agent_type}"
                    self.logger.error(error_msg)
                    raise QualityGateError(error_msg, gate)
            
            # Step 6: Validate output contract structure
            self.logger.debug("Validating output contract")
            output_validation = self.contract_validator.validate_contract(output_contract)
            
            if not output_validation.is_valid:
                error_msg = f"Output contract validation failed: {output_validation.errors}"
                self.logger.error(error_msg)
                raise ContractValidationError(error_msg, output_validation.errors)
            
            # Step 7: Save completion state
            await self._complete_work_state(output_contract)
            
            # Step 8: Create execution result
            execution_time = (datetime.now() - self.execution_start_time).total_seconds()
            
            result = AgentExecutionResult(
                success=True,
                agent_id=self.agent_id,
                story_id=story_id,
                execution_time_seconds=execution_time,
                output_contract=output_contract,
                error_message=None,
                warnings=validation_result.warnings + output_validation.warnings,
                quality_gate_results=quality_gate_results,
                timestamp=datetime.now().isoformat()
            )
            
            self.logger.info(f"Work execution completed successfully in {execution_time:.2f}s")
            return result
            
        except Exception as e:
            # Handle any errors during execution
            execution_time = (datetime.now() - self.execution_start_time).total_seconds()
            error_msg = str(e)
            
            # Save error state
            await self._error_work_state(error_msg, type(e).__name__)
            
            # Create error result
            result = AgentExecutionResult(
                success=False,
                agent_id=self.agent_id,
                story_id=story_id,
                execution_time_seconds=execution_time,
                output_contract=None,
                error_message=error_msg,
                warnings=[],
                quality_gate_results={},
                timestamp=datetime.now().isoformat()
            )
            
            self.logger.error(f"Work execution failed after {execution_time:.2f}s: {error_msg}")
            
            # Re-raise the original exception
            raise
    
    async def _initialize_work_state(self, input_contract: Dict[str, Any]) -> None:
        """
        Initialize agent work state for tracking and recovery.
        
        Args:
            input_contract: Input contract for the work
        """
        story_id = input_contract.get("story_id", "unknown")
        
        self.current_state = AgentState(
            agent_id=self.agent_id,
            story_id=story_id,
            status="started",
            input_contract=input_contract,
            output_contract=None,
            progress_data={},
            error_data=None,
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        await self._save_state()
        self.logger.debug(f"Work state initialized for story: {story_id}")
    
    async def _complete_work_state(self, output_contract: Dict[str, Any]) -> None:
        """
        Mark work state as completed with output contract.
        
        Args:
            output_contract: Completed output contract
        """
        if self.current_state:
            self.current_state.status = "completed"
            self.current_state.output_contract = output_contract
            self.current_state.last_updated = datetime.now().isoformat()
            
            await self._save_state()
            self.logger.debug("Work state marked as completed")
    
    async def _error_work_state(self, error_message: str, error_type: str) -> None:
        """
        Mark work state as error with error details.
        
        Args:
            error_message: Error description
            error_type: Type of error that occurred
        """
        if self.current_state:
            self.current_state.status = "error"
            self.current_state.error_data = {
                "error_message": error_message,
                "error_type": error_type,
                "timestamp": datetime.now().isoformat()
            }
            self.current_state.last_updated = datetime.now().isoformat()
            
            await self._save_state()
            self.logger.debug(f"Work state marked as error: {error_message}")
    
    async def _save_state(self) -> None:
        """
        Save current agent state to persistent storage.
        
        Raises:
            StateManagementError: If state cannot be saved
        """
        if not self.current_state:
            return
        
        try:
            state_file = self.state_storage_path / f"{self.agent_id}_{self.current_state.story_id}_state.json"
            
            with open(state_file, 'w') as f:
                json.dump(self.current_state.to_dict(), f, indent=2)
            
            self.logger.debug(f"State saved to: {state_file}")
            
        except Exception as e:
            error_msg = f"Failed to save agent state: {e}"
            self.logger.error(error_msg)
            raise StateManagementError(error_msg)
    
    async def load_state(self, story_id: str) -> Optional[AgentState]:
        """
        Load saved agent state for recovery.
        
        Args:
            story_id: Story ID to load state for
            
        Returns:
            AgentState if found, None otherwise
            
        Raises:
            StateManagementError: If state loading fails
        """
        try:
            state_file = self.state_storage_path / f"{self.agent_id}_{story_id}_state.json"
            
            if not state_file.exists():
                self.logger.debug(f"No saved state found for story: {story_id}")
                return None
            
            with open(state_file, 'r') as f:
                state_data = json.load(f)
            
            # Reconstruct AgentState from dictionary
            state = AgentState(**state_data)
            
            self.logger.info(f"Loaded saved state for story: {story_id}")
            return state
            
        except Exception as e:
            error_msg = f"Failed to load agent state for {story_id}: {e}"
            self.logger.error(error_msg)
            raise StateManagementError(error_msg)
    
    def _validate_dna_compliance(self, output_contract: Dict[str, Any]) -> bool:
        """
        Validate that output contract complies with DNA principles.
        
        This is CRITICAL for maintaining DigiNativa's quality standards.
        Every agent output must validate against DNA principles.
        
        Args:
            output_contract: Contract to validate
            
        Returns:
            True if compliant, False otherwise
        """
        try:
            dna_compliance = output_contract.get("dna_compliance", {})
            
            # Check design principles
            design_validation = dna_compliance.get("design_principles_validation", {})
            for principle in self.required_design_principles:
                if principle not in design_validation:
                    self.logger.error(f"Missing design principle validation: {principle}")
                    return False
                
                if not isinstance(design_validation[principle], bool):
                    self.logger.error(f"Design principle {principle} must be boolean")
                    return False
                
                if not design_validation[principle]:
                    self.logger.error(f"Design principle {principle} validation failed")
                    return False
            
            # Check architecture principles
            arch_validation = dna_compliance.get("architecture_compliance", {})
            for principle in self.required_architecture_principles:
                if principle not in arch_validation:
                    self.logger.error(f"Missing architecture principle validation: {principle}")
                    return False
                
                if not isinstance(arch_validation[principle], bool):
                    self.logger.error(f"Architecture principle {principle} must be boolean")
                    return False
                
                if not arch_validation[principle]:
                    self.logger.error(f"Architecture principle {principle} validation failed")
                    return False
            
            self.logger.debug("DNA compliance validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"DNA compliance validation error: {e}")
            return False
    
    def validate_quality_gates(self, deliverables: Dict[str, Any], quality_gates: List[str]) -> Dict[str, bool]:
        """
        Validate that all quality gates pass for deliverables.
        
        Args:
            deliverables: Agent deliverables to check
            quality_gates: List of quality gates to validate
            
        Returns:
            Dictionary mapping quality gate to pass/fail status
        """
        results = {}
        
        for gate in quality_gates:
            try:
                passed = self._check_quality_gate(gate, deliverables)
                results[gate] = passed
                
                if passed:
                    self.logger.debug(f"Quality gate '{gate}' passed")
                else:
                    self.logger.warning(f"Quality gate '{gate}' failed")
                    
            except Exception as e:
                self.logger.error(f"Error checking quality gate '{gate}': {e}")
                results[gate] = False
        
        return results
    
    def get_agent_info(self) -> Dict[str, Any]:
        """
        Get agent information for monitoring and debugging.
        
        Returns:
            Dictionary with agent details
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "config": self.config,
            "current_state": self.current_state.to_dict() if self.current_state else None,
            "quality_gates_passed": self.quality_gates_passed,
            "state_storage_path": str(self.state_storage_path)
        }
    
    def get_valid_target_agents(self) -> List[str]:
        """
        Get list of valid target agents for this agent type.
        
        Returns:
            List of valid target agent types
        """
        return self.contract_validator.get_valid_next_agents(self.agent_type)
    
    async def cleanup_old_states(self, max_age_days: int = 30) -> int:
        """
        Clean up old state files to prevent storage bloat.
        
        Args:
            max_age_days: Maximum age of state files to keep
            
        Returns:
            Number of files cleaned up
        """
        try:
            cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)
            cleaned_count = 0
            
            for state_file in self.state_storage_path.glob(f"{self.agent_id}_*_state.json"):
                if state_file.stat().st_mtime < cutoff_time:
                    state_file.unlink()
                    cleaned_count += 1
                    self.logger.debug(f"Cleaned up old state file: {state_file}")
            
            self.logger.info(f"Cleaned up {cleaned_count} old state files")
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up old states: {e}")
            return 0


# Utility functions for external use

def create_agent_template(agent_type: str, agent_id: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a template configuration for a new agent.
    
    Useful for development and testing.
    
    Args:
        agent_type: Type of agent to create template for
        agent_id: Unique identifier for the agent
        config: Optional additional configuration
        
    Returns:
        Agent template dictionary
    """
    base_config = {
        "agent_id": agent_id,
        "agent_type": agent_type,
        "state_storage_path": f"data/agent_states/{agent_type}",
        "logging_level": "INFO",
        "quality_gates_enabled": True,
        "dna_validation_enabled": True,
        "state_persistence_enabled": True
    }
    
    if config:
        base_config.update(config)
    
    return base_config


def validate_agent_config(config: Dict[str, Any]) -> List[str]:
    """
    Validate agent configuration for required fields.
    
    Args:
        config: Agent configuration to validate
        
    Returns:
        List of validation errors (empty if valid)
    """
    errors = []
    
    required_fields = ["agent_id", "agent_type"]
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    
    valid_agent_types = {
        "project_manager", "game_designer", "developer",
        "test_engineer", "qa_tester", "quality_reviewer"
    }
    
    if "agent_type" in config and config["agent_type"] not in valid_agent_types:
        errors.append(f"Invalid agent_type: {config['agent_type']}")
    
    return errors