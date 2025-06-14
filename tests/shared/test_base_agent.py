"""
BaseAgent tests for DigiNativa AI Team system.

PURPOSE:
Validate that our BaseAgent foundation works correctly
and provides all required functionality for agent development.

CRITICAL IMPORTANCE:
BaseAgent is the foundation for ALL agents in our system.
These tests protect the core functionality that enables
our modular architecture and revenue generation.
"""

import pytest
import asyncio
import json
import tempfile
import shutil
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.shared.base_agent import BaseAgent, AgentExecutionResult, AgentState
from modules.shared.contract_validator import ContractValidationError
from modules.shared.exceptions import (
    DNAComplianceError, QualityGateError,
    AgentExecutionError, StateManagementError
)


class MockBaseAgent(BaseAgent):
    """
    Concrete implementation of BaseAgent for testing.
    
    This allows us to test BaseAgent functionality without
    needing a full agent implementation.
    """
    
    def __init__(self, agent_id: str = "test-agent-001", config: dict = None):
        super().__init__(agent_id, "project_manager", config)
        self.process_contract_called = False
        self.process_contract_result = None
        self.quality_gates_to_pass = set()
    
    async def process_contract(self, input_contract):
        """Mock implementation of process_contract."""
        self.process_contract_called = True
        
        # Default successful output contract
        if self.process_contract_result is None:
            return {
                "contract_version": "1.0",
                "story_id": input_contract.get("story_id", "TEST-001"),
                "source_agent": "project_manager",
                "target_agent": "game_designer",
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
                    "required_files": [],
                    "required_data": {},
                    "required_validations": []
                },
                "output_specifications": {
                    "deliverable_files": [f"test_output_{input_contract.get('story_id', 'TEST-001')}.md"],
                    "deliverable_data": {"test": "data"},
                    "validation_criteria": {}
                },
                "quality_gates": list(self.quality_gates_to_pass),
                "handoff_criteria": ["test_criterion"]
            }
        else:
            return self.process_contract_result
    
    def _check_quality_gate(self, gate: str, deliverables):
        """Mock implementation of quality gate checking."""
        return gate in self.quality_gates_to_pass


class TestBaseAgentInitialization:
    """Test BaseAgent initialization."""
    
    def test_valid_agent_initialization(self):
        """Test that BaseAgent can be initialized with valid parameters."""
        agent = MockBaseAgent("test-001", {"test": "config"})
        
        assert agent.agent_id == "test-001"
        assert agent.agent_type == "project_manager"
        assert agent.config == {"test": "config"}
        assert agent.contract_validator is not None
        assert agent.current_state is None
    
    def test_invalid_agent_type_raises_error(self):
        """Test that invalid agent type raises ValueError."""
        from modules.shared.base_agent import BaseAgent
        
        # This should fail during initialization
        with pytest.raises(ValueError, match="Invalid agent_type"):
            class InvalidAgent(BaseAgent):
                async def process_contract(self, input_contract):
                    return {}
                def _check_quality_gate(self, gate, deliverables):
                    return True
            
            InvalidAgent("test", "invalid_agent_type")
    
    def test_default_config_handling(self):
        """Test that None config is handled correctly."""
        agent = MockBaseAgent("test-002")
        
        assert agent.config == {}
        assert agent.agent_id == "test-002"
    
    def test_state_storage_path_creation(self):
        """Test that state storage path is created."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = {"state_storage_path": temp_dir + "/test_states"}
            agent = MockBaseAgent("test-003", config)
            
            assert agent.state_storage_path.exists()
            assert agent.state_storage_path.is_dir()


class TestBaseAgentExecution:
    """Test BaseAgent work execution."""
    
    @pytest.fixture
    def valid_input_contract(self):
        """Provide a valid input contract for testing."""
        return {
            "contract_version": "1.0",
            "story_id": "STORY-TEST-001",
            "source_agent": "github",
            "target_agent": "project_manager",
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
                "required_files": [],
                "required_data": {"test": "input"},
                "required_validations": []
            },
            "output_specifications": {
                "deliverable_files": [],
                "deliverable_data": {},
                "validation_criteria": {}
            },
            "quality_gates": [],
            "handoff_criteria": []
        }
    
    @pytest.fixture
    def agent_with_temp_storage(self):
        """Provide agent with temporary storage for testing."""
        temp_dir = tempfile.mkdtemp()
        config = {"state_storage_path": temp_dir}
        agent = MockBaseAgent("test-exec-001", config)
        
        yield agent
        
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.mark.asyncio
    async def test_successful_work_execution(self, agent_with_temp_storage, valid_input_contract):
        """Test successful work execution end-to-end."""
        agent = agent_with_temp_storage
        
        result = await agent.execute_work(valid_input_contract)
        
        assert isinstance(result, AgentExecutionResult)
        assert result.success is True
        assert result.agent_id == "test-exec-001"
        assert result.story_id == "STORY-TEST-001"
        assert result.output_contract is not None
        assert result.error_message is None
        assert agent.process_contract_called is True
    
    @pytest.mark.asyncio
    async def test_contract_validation_failure(self, agent_with_temp_storage):
        """Test that invalid input contract is rejected."""
        agent = agent_with_temp_storage
        
        # Invalid contract missing required fields
        invalid_contract = {"invalid": "contract"}
        
        # This should raise ContractValidationError due to missing required fields
        with pytest.raises(ContractValidationError):
            await agent.execute_work(invalid_contract)
    
    @pytest.mark.asyncio
    async def test_dna_compliance_failure(self, agent_with_temp_storage, valid_input_contract):
        """Test that DNA compliance failures are caught."""
        agent = agent_with_temp_storage
        
        # Set up agent to return non-compliant output
        agent.process_contract_result = {
            "contract_version": "1.0",
            "story_id": "STORY-TEST-001",
            "source_agent": "project_manager",
            "target_agent": "game_designer",
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": False,  # DNA violation!
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
            "input_requirements": {"required_files": [], "required_data": {}, "required_validations": []},
            "output_specifications": {"deliverable_files": [], "deliverable_data": {}, "validation_criteria": {}},
            "quality_gates": [],
            "handoff_criteria": []
        }
        
        with pytest.raises(DNAComplianceError):
            await agent.execute_work(valid_input_contract)
    
    @pytest.mark.asyncio
    async def test_quality_gate_failure(self, agent_with_temp_storage, valid_input_contract):
        """Test that quality gate failures are caught."""
        agent = agent_with_temp_storage
        
        # Set up quality gates that will fail
        agent.quality_gates_to_pass = set()  # Empty set means all gates fail
        
        # Modify the agent to return quality gates in output
        original_process = agent.process_contract
        
        async def process_with_quality_gates(input_contract):
            result = await original_process(input_contract)
            result["quality_gates"] = ["failing_quality_gate"]
            return result
        
        agent.process_contract = process_with_quality_gates
        
        with pytest.raises(QualityGateError):
            await agent.execute_work(valid_input_contract)
    
    @pytest.mark.asyncio
    async def test_agent_execution_error_handling(self, agent_with_temp_storage, valid_input_contract):
        """Test that agent execution errors are handled properly."""
        agent = agent_with_temp_storage
        
        # Set up agent to raise an error during processing
        async def failing_process_contract(input_contract):
            raise AgentExecutionError("Simulated execution failure", agent.agent_id)
        
        agent.process_contract = failing_process_contract
        
        with pytest.raises(AgentExecutionError):
            await agent.execute_work(valid_input_contract)


class TestBaseAgentStateManagement:
    """Test BaseAgent state management functionality."""
    
    @pytest.fixture
    def agent_with_temp_storage(self):
        """Provide agent with temporary storage for testing."""
        temp_dir = tempfile.mkdtemp()
        config = {"state_storage_path": temp_dir}
        agent = MockBaseAgent("state-test-001", config)
        
        yield agent
        
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.mark.asyncio
    async def test_state_initialization_and_saving(self, agent_with_temp_storage):
        """Test that agent state is properly initialized and saved."""
        agent = agent_with_temp_storage
        
        input_contract = {"story_id": "STORY-STATE-001", "test": "data"}
        
        await agent._initialize_work_state(input_contract)
        
        assert agent.current_state is not None
        assert agent.current_state.agent_id == "state-test-001"
        assert agent.current_state.story_id == "STORY-STATE-001"
        assert agent.current_state.status == "started"
        assert agent.current_state.input_contract == input_contract
        
        # Check that state file was created
        state_file = agent.state_storage_path / "state-test-001_STORY-STATE-001_state.json"
        assert state_file.exists()
    
    @pytest.mark.asyncio
    async def test_state_loading(self, agent_with_temp_storage):
        """Test that saved state can be loaded."""
        agent = agent_with_temp_storage
        
        # Create and save a state
        input_contract = {"story_id": "STORY-LOAD-001"}
        await agent._initialize_work_state(input_contract)
        
        # Load the state
        loaded_state = await agent.load_state("STORY-LOAD-001")
        
        assert loaded_state is not None
        assert loaded_state.agent_id == "state-test-001"
        assert loaded_state.story_id == "STORY-LOAD-001"
        assert loaded_state.status == "started"
    
    @pytest.mark.asyncio
    async def test_state_completion(self, agent_with_temp_storage):
        """Test that state can be marked as completed."""
        agent = agent_with_temp_storage
        
        # Initialize state
        input_contract = {"story_id": "STORY-COMPLETE-001"}
        await agent._initialize_work_state(input_contract)
        
        # Complete the state
        output_contract = {"result": "success"}
        await agent._complete_work_state(output_contract)
        
        assert agent.current_state.status == "completed"
        assert agent.current_state.output_contract == output_contract
    
    @pytest.mark.asyncio
    async def test_state_error_handling(self, agent_with_temp_storage):
        """Test that state can be marked as error."""
        agent = agent_with_temp_storage
        
        # Initialize state
        input_contract = {"story_id": "STORY-ERROR-001"}
        await agent._initialize_work_state(input_contract)
        
        # Mark as error
        await agent._error_work_state("Test error", "TestError")
        
        assert agent.current_state.status == "error"
        assert agent.current_state.error_data is not None
        assert agent.current_state.error_data["error_message"] == "Test error"
        assert agent.current_state.error_data["error_type"] == "TestError"


class TestBaseAgentDNAValidation:
    """Test BaseAgent DNA compliance validation."""
    
    @pytest.fixture
    def agent(self):
        return MockBaseAgent("dna-test-001")
    
    def test_valid_dna_compliance(self, agent):
        """Test that valid DNA compliance passes validation."""
        valid_contract = {
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
            }
        }
        
        result = agent._validate_dna_compliance(valid_contract)
        assert result is True
    
    def test_missing_design_principle_fails(self, agent):
        """Test that missing design principle fails validation."""
        invalid_contract = {
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": True,
                    "policy_to_practice": True,
                    "time_respect": True,
                    "holistic_thinking": True,
                    # Missing professional_tone
                },
                "architecture_compliance": {
                    "api_first": True,
                    "stateless_backend": True,
                    "separation_of_concerns": True,
                    "simplicity_first": True
                }
            }
        }
        
        result = agent._validate_dna_compliance(invalid_contract)
        assert result is False
    
    def test_failed_design_principle_fails(self, agent):
        """Test that failed design principle fails validation."""
        invalid_contract = {
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": False,  # Failed principle
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
            }
        }
        
        result = agent._validate_dna_compliance(invalid_contract)
        assert result is False


class TestBaseAgentUtilityMethods:
    """Test BaseAgent utility methods."""
    
    @pytest.fixture
    def agent(self):
        return MockBaseAgent("util-test-001")
    
    def test_get_agent_info(self, agent):
        """Test that agent info is returned correctly."""
        info = agent.get_agent_info()
        
        assert info["agent_id"] == "util-test-001"
        assert info["agent_type"] == "project_manager"
        assert "config" in info
        assert "current_state" in info
        assert "quality_gates_passed" in info
    
    def test_get_valid_target_agents(self, agent):
        """Test that valid target agents are returned."""
        targets = agent.get_valid_target_agents()
        
        assert isinstance(targets, list)
        # For project_manager, should include game_designer
        assert "game_designer" in targets
    
    def test_validate_quality_gates(self, agent):
        """Test quality gate validation."""
        agent.quality_gates_to_pass = {"passing_gate"}
        
        deliverables = {"test": "data"}
        gates = ["passing_gate", "failing_gate"]
        
        results = agent.validate_quality_gates(deliverables, gates)
        
        assert results["passing_gate"] is True
        assert results["failing_gate"] is False


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])