"""
EventBus tests for DigiNativa AI Team system.

PURPOSE:
Validate that our EventBus coordination system works correctly
and provides all required functionality for agent communication.

CRITICAL IMPORTANCE:
EventBus is the coordination hub for ALL agents in our system.
These tests protect the functionality that enables our
modular architecture and workflow management.
"""

import pytest
import asyncio
import tempfile
import shutil
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock
import json

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.shared.event_bus import (
    EventBus, WorkItem, WorkPriority, WorkStatus, AgentRegistry,
    create_eventbus_config, create_work_contract
)
from modules.shared.exceptions import (
    EventBusError, WorkflowError
)


class TestEventBusInitialization:
    """Test EventBus initialization and configuration."""
    
    def test_default_initialization(self):
        """Test EventBus initializes with default configuration."""
        event_bus = EventBus()
        
        assert event_bus.work_queue == []
        assert event_bus.active_work == {}
        assert event_bus.completed_work == {}
        assert event_bus.agents == {}
        assert event_bus.agent_types == {}
        assert event_bus.max_concurrent_work == 10
        assert event_bus.work_timeout_minutes == 60
    
    def test_custom_configuration(self):
        """Test EventBus initializes with custom configuration."""
        config = {
            "max_concurrent_work": 5,
            "work_timeout_minutes": 30
        }
        
        event_bus = EventBus(config)
        
        assert event_bus.max_concurrent_work == 5
        assert event_bus.work_timeout_minutes == 30
    
    def test_valid_agent_sequences(self):
        """Test that valid agent sequences are correctly configured."""
        event_bus = EventBus()
        
        expected_sequences = {
            "project_manager": ["game_designer"],
            "game_designer": ["developer"],
            "developer": ["test_engineer"],
            "test_engineer": ["qa_tester"],
            "qa_tester": ["quality_reviewer"],
            "quality_reviewer": ["project_manager"]
        }
        
        assert event_bus.valid_agent_sequences == expected_sequences


class TestAgentRegistration:
    """Test agent registration and management."""
    
    @pytest.fixture
    def event_bus(self):
        """Create EventBus instance for testing."""
        return EventBus()
    
    @pytest.mark.asyncio
    async def test_register_agent_success(self, event_bus):
        """Test successful agent registration."""
        result = await event_bus.register_agent(
            "pm-001", 
            "project_manager", 
            {"story_analysis", "github_integration"}
        )
        
        assert result == True
        assert "pm-001" in event_bus.agents
        
        agent = event_bus.agents["pm-001"]
        assert agent.agent_id == "pm-001"
        assert agent.agent_type == "project_manager"
        assert agent.status == "available"
        assert "story_analysis" in agent.capabilities
        assert "github_integration" in agent.capabilities
        
        # Check agent type mapping
        assert "project_manager" in event_bus.agent_types
        assert "pm-001" in event_bus.agent_types["project_manager"]
    
    @pytest.mark.asyncio
    async def test_register_invalid_agent_type(self, event_bus):
        """Test registration fails with invalid agent type."""
        with pytest.raises(EventBusError) as exc_info:
            await event_bus.register_agent("invalid-001", "invalid_type")
        
        assert "Invalid agent_type" in str(exc_info.value)
        assert "invalid-001" not in event_bus.agents
    
    @pytest.mark.asyncio
    async def test_register_multiple_agents_same_type(self, event_bus):
        """Test registering multiple agents of the same type."""
        await event_bus.register_agent("pm-001", "project_manager")
        await event_bus.register_agent("pm-002", "project_manager")
        
        assert len(event_bus.agent_types["project_manager"]) == 2
        assert "pm-001" in event_bus.agent_types["project_manager"]
        assert "pm-002" in event_bus.agent_types["project_manager"]
    
    @pytest.mark.asyncio
    async def test_unregister_agent_success(self, event_bus):
        """Test successful agent unregistration."""
        await event_bus.register_agent("pm-001", "project_manager")
        
        result = await event_bus.unregister_agent("pm-001")
        
        assert result == True
        assert "pm-001" not in event_bus.agents
        assert "project_manager" not in event_bus.agent_types
    
    @pytest.mark.asyncio
    async def test_unregister_unknown_agent(self, event_bus):
        """Test unregistering unknown agent returns False."""
        result = await event_bus.unregister_agent("unknown-001")
        
        assert result == False


class TestWorkDelegation:
    """Test work delegation and management."""
    
    @pytest.fixture
    def event_bus_with_agents(self):
        """Create EventBus with registered agents."""
        event_bus = EventBus({"persistence_enabled": False})
        return event_bus
    
    @pytest.mark.asyncio
    async def test_delegate_work_success(self, event_bus_with_agents):
        """Test successful work delegation."""
        event_bus = event_bus_with_agents
        
        # Register an agent
        await event_bus.register_agent("gd-001", "game_designer")
        
        # Create work contract
        contract = await create_work_contract(
            "STORY-001",
            "project_manager",
            "game_designer",
            {"feature": "user_registration"}
        )
        
        # Delegate work
        work_id = await event_bus.delegate_to_agent(
            "game_designer",
            contract,
            WorkPriority.HIGH
        )
        
        assert work_id.startswith("WORK-")
        assert len(event_bus.work_queue) == 1
        
        work_item = event_bus.work_queue[0]
        assert work_item.story_id == "STORY-001"
        assert work_item.source_agent == "project_manager"
        assert work_item.target_agent == "game_designer"
        assert work_item.priority == WorkPriority.HIGH
        assert work_item.status == WorkStatus.PENDING
    
    @pytest.mark.asyncio
    async def test_delegate_to_nonexistent_agent_type(self, event_bus_with_agents):
        """Test delegation fails when no agents of target type exist."""
        event_bus = event_bus_with_agents
        
        contract = await create_work_contract(
            "STORY-001",
            "project_manager", 
            "game_designer",
            {"feature": "test"}
        )
        
        with pytest.raises(EventBusError) as exc_info:
            await event_bus.delegate_to_agent("game_designer", contract)
        
        assert "No agents available" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_invalid_agent_sequence(self, event_bus_with_agents):
        """Test delegation fails with invalid agent sequence."""
        event_bus = event_bus_with_agents
        
        await event_bus.register_agent("te-001", "test_engineer")
        
        contract = await create_work_contract(
            "STORY-001",
            "project_manager",  # project_manager can't go directly to test_engineer
            "test_engineer",
            {"feature": "test"}
        )
        
        with pytest.raises(EventBusError) as exc_info:
            await event_bus.delegate_to_agent("test_engineer", contract)
        
        assert "Invalid sequence" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_work_priority_ordering(self, event_bus_with_agents):
        """Test that work is queued in priority order."""
        event_bus = event_bus_with_agents
        
        await event_bus.register_agent("gd-001", "game_designer")
        
        # Add work items with different priorities
        contract_low = await create_work_contract("STORY-001", "system", "game_designer", {"priority": "low"})
        contract_high = await create_work_contract("STORY-002", "system", "game_designer", {"priority": "high"})
        contract_medium = await create_work_contract("STORY-003", "system", "game_designer", {"priority": "medium"})
        
        await event_bus.delegate_to_agent("game_designer", contract_low, WorkPriority.LOW)
        await event_bus.delegate_to_agent("game_designer", contract_high, WorkPriority.HIGH)
        await event_bus.delegate_to_agent("game_designer", contract_medium, WorkPriority.MEDIUM)
        
        # Verify order is HIGH, MEDIUM, LOW
        priorities = [item.priority for item in event_bus.work_queue]
        assert priorities == [WorkPriority.HIGH, WorkPriority.MEDIUM, WorkPriority.LOW]


class TestWorkStatusTracking:
    """Test work status tracking and monitoring."""
    
    @pytest.fixture
    def event_bus(self):
        """Create EventBus instance for testing."""
        return EventBus()
    
    @pytest.mark.asyncio
    async def test_get_work_status_pending(self, event_bus):
        """Test getting status of pending work."""
        await event_bus.register_agent("gd-001", "game_designer")
        
        contract = await create_work_contract("STORY-001", "system", "game_designer", {"test": "data"})
        work_id = await event_bus.delegate_to_agent("game_designer", contract)
        
        status = await event_bus.get_work_status(work_id)
        
        assert status is not None
        assert status["work_id"] == work_id
        assert status["status"] == "pending"
        assert status["story_id"] == "STORY-001"
    
    @pytest.mark.asyncio
    async def test_get_work_status_nonexistent(self, event_bus):
        """Test getting status of nonexistent work returns None."""
        status = await event_bus.get_work_status("WORK-NONEXISTENT")
        
        assert status is None
    
    @pytest.mark.asyncio
    async def test_cancel_pending_work(self, event_bus):
        """Test cancelling pending work."""
        await event_bus.register_agent("gd-001", "game_designer")
        
        contract = await create_work_contract("STORY-001", "system", "game_designer", {"test": "data"})
        work_id = await event_bus.delegate_to_agent("game_designer", contract)
        
        result = await event_bus.cancel_work(work_id, "Test cancellation")
        
        assert result == True
        assert len(event_bus.work_queue) == 0
        assert work_id in event_bus.completed_work
        
        cancelled_work = event_bus.completed_work[work_id]
        assert cancelled_work.status == WorkStatus.CANCELLED
        assert cancelled_work.error_message == "Test cancellation"
    
    @pytest.mark.asyncio
    async def test_get_queue_status(self, event_bus):
        """Test getting queue status information."""
        await event_bus.register_agent("pm-001", "project_manager")
        await event_bus.register_agent("gd-001", "game_designer")
        
        # Add some work
        contract = await create_work_contract("STORY-001", "system", "game_designer", {"test": "data"})
        await event_bus.delegate_to_agent("game_designer", contract)
        
        status = await event_bus.get_queue_status()
        
        assert status["pending_work"] == 1
        assert status["active_work"] == 0
        assert status["completed_work"] == 0
        assert status["registered_agents"] == 2
        assert status["available_agents"] == 2
        assert status["busy_agents"] == 0
        assert status["offline_agents"] == 0
        assert status["agent_types"]["project_manager"] == 1
        assert status["agent_types"]["game_designer"] == 1




class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_create_eventbus_config(self):
        """Test EventBus configuration creation."""
        config = create_eventbus_config(
            max_concurrent_work=5,
            work_timeout_minutes=30
        )
        
        assert config["max_concurrent_work"] == 5
        assert config["work_timeout_minutes"] == 30
    
    @pytest.mark.asyncio
    async def test_create_work_contract(self):
        """Test work contract creation."""
        contract = await create_work_contract(
            "STORY-001",
            "project_manager",
            "game_designer",
            {"feature": "user_registration"}
        )
        
        assert contract["contract_version"] == "1.0"
        assert contract["story_id"] == "STORY-001"
        assert contract["source_agent"] == "project_manager"
        assert contract["target_agent"] == "game_designer"
        assert contract["input_requirements"]["required_data"]["feature"] == "user_registration"
        
        # Check DNA compliance
        dna = contract["dna_compliance"]
        assert dna["design_principles_validation"]["pedagogical_value"] == True
        assert dna["architecture_compliance"]["api_first"] == True
    
    @pytest.mark.asyncio
    async def test_create_work_contract_custom_dna(self):
        """Test work contract creation with custom DNA compliance."""
        custom_dna = {
            "design_principles_validation": {
                "pedagogical_value": False,
                "policy_to_practice": True,
                "time_respect": True,
                "holistic_thinking": True,
                "professional_tone": True
            },
            "architecture_compliance": {
                "api_first": True,
                "stateless_backend": True,
                "separation_of_concerns": True,
                "simplicity_first": False
            }
        }
        
        contract = await create_work_contract(
            "STORY-001",
            "project_manager",
            "game_designer",
            {"feature": "test"},
            custom_dna
        )
        
        assert contract["dna_compliance"]["design_principles_validation"]["pedagogical_value"] == False
        assert contract["dna_compliance"]["architecture_compliance"]["simplicity_first"] == False


class TestDataStructures:
    """Test data structure functionality."""
    
    def test_work_item_creation(self):
        """Test WorkItem creation and conversion."""
        work_item = WorkItem(
            work_id="WORK-001",
            story_id="STORY-001",
            source_agent="project_manager",
            target_agent="game_designer",
            contract={"test": "data"},
            priority=WorkPriority.HIGH,
            status=WorkStatus.PENDING,
            created_at="2024-01-01T00:00:00"
        )
        
        assert work_item.work_id == "WORK-001"
        assert work_item.priority == WorkPriority.HIGH
        assert work_item.status == WorkStatus.PENDING
        
        # Test dictionary conversion
        work_dict = work_item.to_dict()
        assert work_dict["work_id"] == "WORK-001"
        assert work_dict["priority"] == 2  # HIGH priority value
        assert work_dict["status"] == "pending"
    
    def test_agent_registry_creation(self):
        """Test AgentRegistry creation."""
        registry = AgentRegistry(
            agent_id="pm-001",
            agent_type="project_manager",
            status="available",
            capabilities={"story_analysis"}
        )
        
        assert registry.agent_id == "pm-001"
        assert registry.agent_type == "project_manager"
        assert registry.status == "available"
        assert "story_analysis" in registry.capabilities
    
    def test_agent_registry_default_capabilities(self):
        """Test AgentRegistry with default capabilities."""
        registry = AgentRegistry(
            agent_id="pm-001",
            agent_type="project_manager",
            status="available"
        )
        
        assert registry.capabilities == set()


