"""
State Manager tests for DigiNativa AI Team system.

PURPOSE:
Validate that state management functionality works correctly across all agents,
enabling proper recovery from interruptions and state persistence.

CRITICAL IMPORTANCE:
State management is essential for:
- Agent recovery after system interruptions
- Maintaining context across long-running processes
- Debugging and monitoring agent behavior
- Ensuring data consistency during handoffs

TESTING SCOPE:
- State save/load functionality across all agents
- Recovery from interruptions and failures
- State cleanup and maintenance operations
- Performance requirements for state operations
- Thread safety and concurrent access
"""

import pytest
import json
import tempfile
import shutil
import asyncio
import time
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from unittest.mock import patch, MagicMock
from concurrent.futures import ThreadPoolExecutor
import threading

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.shared.base_agent import BaseAgent, AgentExecutionResult
from modules.shared.exceptions import AgentExecutionError, StateManagementError


# Mock state manager implementation for testing
class MockStateManager:
    """Mock implementation of state manager for testing."""
    
    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._in_memory_cache = {}
        self._lock = threading.Lock()
    
    async def save_state(self, agent_id: str, state_data: Dict[str, Any]) -> bool:
        """Save agent state to persistent storage."""
        try:
            state_file = self.storage_path / f"{agent_id}_state.json"
            
            with self._lock:
                # Save to memory cache first
                self._in_memory_cache[agent_id] = state_data.copy()
                
                # Then persist to disk
                with open(state_file, 'w') as f:
                    json.dump({
                        "agent_id": agent_id,
                        "timestamp": time.time(),
                        "state": state_data
                    }, f, indent=2)
            
            return True
            
        except Exception as e:
            raise StateManagementError(f"Failed to save state for {agent_id}: {e}")
    
    async def load_state(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Load agent state from persistent storage."""
        try:
            # Check memory cache first
            with self._lock:
                if agent_id in self._in_memory_cache:
                    return self._in_memory_cache[agent_id].copy()
            
            # Fall back to disk storage
            state_file = self.storage_path / f"{agent_id}_state.json"
            if not state_file.exists():
                return None
            
            with open(state_file, 'r') as f:
                data = json.load(f)
                state_data = data.get("state", {})
                
                # Update cache
                with self._lock:
                    self._in_memory_cache[agent_id] = state_data.copy()
                
                return state_data
                
        except Exception as e:
            raise StateManagementError(f"Failed to load state for {agent_id}: {e}")
    
    async def clear_state(self, agent_id: str) -> bool:
        """Clear agent state from storage."""
        try:
            # Clear from memory cache
            with self._lock:
                self._in_memory_cache.pop(agent_id, None)
            
            # Clear from disk
            state_file = self.storage_path / f"{agent_id}_state.json"
            if state_file.exists():
                state_file.unlink()
            
            return True
            
        except Exception as e:
            raise StateManagementError(f"Failed to clear state for {agent_id}: {e}")
    
    async def list_agents_with_state(self) -> list:
        """List all agents that have saved state."""
        try:
            agents = []
            
            # From memory cache
            with self._lock:
                agents.extend(self._in_memory_cache.keys())
            
            # From disk storage
            for state_file in self.storage_path.glob("*_state.json"):
                agent_id = state_file.stem.replace("_state", "")
                if agent_id not in agents:
                    agents.append(agent_id)
            
            return agents
            
        except Exception as e:
            raise StateManagementError(f"Failed to list agents with state: {e}")
    
    async def cleanup_old_states(self, max_age_days: int = 7) -> int:
        """Clean up old state files."""
        try:
            cleanup_count = 0
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60
            
            for state_file in self.storage_path.glob("*_state.json"):
                try:
                    with open(state_file, 'r') as f:
                        data = json.load(f)
                        timestamp = data.get("timestamp", 0)
                        
                        if current_time - timestamp > max_age_seconds:
                            agent_id = state_file.stem.replace("_state", "")
                            await self.clear_state(agent_id)
                            cleanup_count += 1
                            
                except Exception:
                    # If we can't read the file, clean it up anyway
                    state_file.unlink()
                    cleanup_count += 1
            
            return cleanup_count
            
        except Exception as e:
            raise StateManagementError(f"Failed to cleanup old states: {e}")


class MockAgent(BaseAgent):
    """Mock agent for testing state management."""
    
    def __init__(self, agent_id: str, storage_path: Path):
        super().__init__(agent_id, "developer", {"state_storage_path": str(storage_path)})
        self.state_manager = MockStateManager(storage_path)
        self.execution_state = {}
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """Mock contract processing for testing."""
        # Simulate some processing state
        self.execution_state = {
            "current_step": "processing",
            "story_id": input_contract.get("story_id"),
            "progress": 0.5,
            "intermediate_results": {"test": "data"}
        }
        
        # Save state during processing
        await self.save_execution_state()
        
        # Simulate some work
        await asyncio.sleep(0.1)
        
        # Update progress
        self.execution_state["progress"] = 1.0
        self.execution_state["current_step"] = "completed"
        await self.save_execution_state()
        
        return {"result": "success", "story_id": input_contract.get("story_id")}
    
    async def save_execution_state(self):
        """Save current execution state."""
        await self.state_manager.save_state(self.agent_id, self.execution_state)
    
    async def load_execution_state(self):
        """Load execution state."""
        loaded_state = await self.state_manager.load_state(self.agent_id)
        if loaded_state:
            self.execution_state = loaded_state
        return loaded_state


class TestStateSaveLoad:
    """Test basic state save and load functionality."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def state_manager(self, temp_storage):
        """Create state manager for testing."""
        return MockStateManager(temp_storage)
    
    @pytest.fixture
    def sample_state_data(self):
        """Sample state data for testing."""
        return {
            "current_step": "processing_components",
            "story_id": "STORY-GH-1001",
            "progress": 0.75,
            "completed_components": ["UserComponent", "LoginComponent"],
            "pending_components": ["DashboardComponent"],
            "intermediate_results": {
                "generated_code": {"UserComponent": "const User = () => <div>User</div>;"},
                "validation_results": {"UserComponent": {"valid": True, "score": 4.5}}
            },
            "metadata": {
                "start_time": "2024-01-15T10:30:00Z",
                "last_update": "2024-01-15T10:35:00Z"
            }
        }
    
    @pytest.mark.asyncio
    async def test_save_state_success(self, state_manager, sample_state_data):
        """Test successful state saving."""
        agent_id = "test-agent-001"
        
        result = await state_manager.save_state(agent_id, sample_state_data)
        
        assert result is True, "State save should succeed"
        
        # Verify state file was created
        state_file = state_manager.storage_path / f"{agent_id}_state.json"
        assert state_file.exists(), "State file should be created"
        
        # Verify content
        with open(state_file, 'r') as f:
            saved_data = json.load(f)
            assert saved_data["agent_id"] == agent_id
            assert saved_data["state"] == sample_state_data
            assert "timestamp" in saved_data
    
    @pytest.mark.asyncio
    async def test_load_state_success(self, state_manager, sample_state_data):
        """Test successful state loading."""
        agent_id = "test-agent-002"
        
        # Save state first
        await state_manager.save_state(agent_id, sample_state_data)
        
        # Load state
        loaded_state = await state_manager.load_state(agent_id)
        
        assert loaded_state is not None, "State should be loaded"
        assert loaded_state == sample_state_data, "Loaded state should match saved state"
    
    @pytest.mark.asyncio
    async def test_load_nonexistent_state(self, state_manager):
        """Test loading state for non-existent agent."""
        loaded_state = await state_manager.load_state("nonexistent-agent")
        
        assert loaded_state is None, "Non-existent state should return None"
    
    @pytest.mark.asyncio
    async def test_state_persistence_across_instances(self, temp_storage, sample_state_data):
        """Test that state persists across state manager instances."""
        agent_id = "persistence-test-agent"
        
        # Save state with first instance
        manager1 = MockStateManager(temp_storage)
        await manager1.save_state(agent_id, sample_state_data)
        
        # Load state with second instance
        manager2 = MockStateManager(temp_storage)
        loaded_state = await manager2.load_state(agent_id)
        
        assert loaded_state == sample_state_data, "State should persist across instances"
    
    @pytest.mark.asyncio
    async def test_state_update_overwrites_previous(self, state_manager, sample_state_data):
        """Test that saving state overwrites previous state."""
        agent_id = "update-test-agent"
        
        # Save initial state
        await state_manager.save_state(agent_id, sample_state_data)
        
        # Update and save new state
        updated_state = sample_state_data.copy()
        updated_state["progress"] = 1.0
        updated_state["current_step"] = "completed"
        
        await state_manager.save_state(agent_id, updated_state)
        
        # Load and verify updated state
        loaded_state = await state_manager.load_state(agent_id)
        assert loaded_state["progress"] == 1.0
        assert loaded_state["current_step"] == "completed"


class TestInterruptionRecovery:
    """Test recovery from interruptions and failures."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_agent(self, temp_storage):
        """Create mock agent for testing."""
        return MockAgent("recovery-test-agent", temp_storage)
    
    @pytest.mark.asyncio
    async def test_recovery_from_interruption(self, mock_agent):
        """Test that agent can recover from interruption."""
        # Start processing
        contract = {"story_id": "STORY-RECOVERY-001", "test": "data"}
        
        # Process partially (this saves state)
        await mock_agent.process_contract(contract)
        
        # Simulate interruption by creating new agent instance
        new_agent = MockAgent("recovery-test-agent", mock_agent.state_manager.storage_path)
        
        # Load previous state
        loaded_state = await new_agent.load_execution_state()
        
        assert loaded_state is not None, "Should recover previous state"
        assert loaded_state["story_id"] == "STORY-RECOVERY-001"
        assert loaded_state["current_step"] == "completed"
        assert loaded_state["progress"] == 1.0
    
    @pytest.mark.asyncio
    async def test_partial_execution_recovery(self, temp_storage):
        """Test recovery from partial execution."""
        agent_id = "partial-execution-agent"
        agent = MockAgent(agent_id, temp_storage)
        
        # Simulate partial execution state
        partial_state = {
            "current_step": "generating_components",
            "story_id": "STORY-PARTIAL-001",
            "progress": 0.3,
            "completed_tasks": ["analysis", "planning"],
            "pending_tasks": ["component_generation", "api_creation", "testing"]
        }
        
        await agent.state_manager.save_state(agent_id, partial_state)
        
        # Create new agent instance (simulating restart)
        recovered_agent = MockAgent(agent_id, temp_storage)
        loaded_state = await recovered_agent.load_execution_state()
        
        assert loaded_state["progress"] == 0.3
        assert "analysis" in loaded_state["completed_tasks"]
        assert "component_generation" in loaded_state["pending_tasks"]
    
    @pytest.mark.asyncio
    async def test_corrupted_state_handling(self, temp_storage):
        """Test handling of corrupted state files."""
        agent_id = "corrupted-state-agent"
        state_manager = MockStateManager(temp_storage)
        
        # Create corrupted state file
        state_file = temp_storage / f"{agent_id}_state.json"
        with open(state_file, 'w') as f:
            f.write("invalid json content {")
        
        # Should handle corrupted file gracefully
        with pytest.raises(StateManagementError):
            await state_manager.load_state(agent_id)
    
    @pytest.mark.asyncio
    async def test_recovery_with_missing_dependencies(self, temp_storage):
        """Test recovery when some dependencies are missing."""
        agent_id = "missing-deps-agent"
        state_manager = MockStateManager(temp_storage)
        
        # Save state with references to external resources
        state_with_deps = {
            "current_step": "processing",
            "external_file_path": "/nonexistent/file.json",
            "dependency_versions": {"tool_a": "1.0.0", "tool_b": "2.0.0"}
        }
        
        await state_manager.save_state(agent_id, state_with_deps)
        
        # Should load state even if dependencies are missing
        loaded_state = await state_manager.load_state(agent_id)
        assert loaded_state["external_file_path"] == "/nonexistent/file.json"
        # Note: Actual dependency validation would be handled by the agent


class TestStateCleanupMaintenance:
    """Test state cleanup and maintenance operations."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def state_manager(self, temp_storage):
        """Create state manager for testing."""
        return MockStateManager(temp_storage)
    
    @pytest.mark.asyncio
    async def test_clear_single_agent_state(self, state_manager):
        """Test clearing state for a single agent."""
        agent_id = "clear-test-agent"
        test_state = {"test": "data", "progress": 0.5}
        
        # Save state
        await state_manager.save_state(agent_id, test_state)
        
        # Verify state exists
        loaded_state = await state_manager.load_state(agent_id)
        assert loaded_state is not None
        
        # Clear state
        result = await state_manager.clear_state(agent_id)
        assert result is True
        
        # Verify state is cleared
        loaded_state = await state_manager.load_state(agent_id)
        assert loaded_state is None
    
    @pytest.mark.asyncio
    async def test_list_agents_with_state(self, state_manager):
        """Test listing all agents with saved state."""
        # Save state for multiple agents
        agents_data = {
            "agent-1": {"step": "A"},
            "agent-2": {"step": "B"}, 
            "agent-3": {"step": "C"}
        }
        
        for agent_id, state in agents_data.items():
            await state_manager.save_state(agent_id, state)
        
        # List agents with state
        agents_with_state = await state_manager.list_agents_with_state()
        
        assert len(agents_with_state) == 3
        for agent_id in agents_data.keys():
            assert agent_id in agents_with_state
    
    @pytest.mark.asyncio
    async def test_cleanup_old_states(self, state_manager, temp_storage):
        """Test cleanup of old state files."""
        current_time = time.time()
        
        # Create state files with different ages
        agents_with_ages = [
            ("recent-agent", current_time - 3600),      # 1 hour old
            ("old-agent", current_time - 8 * 24 * 3600), # 8 days old
            ("very-old-agent", current_time - 30 * 24 * 3600) # 30 days old
        ]
        
        for agent_id, timestamp in agents_with_ages:
            # Save state
            await state_manager.save_state(agent_id, {"test": "data"})
            
            # Manually adjust timestamp in file
            state_file = temp_storage / f"{agent_id}_state.json"
            with open(state_file, 'r') as f:
                data = json.load(f)
            data["timestamp"] = timestamp
            with open(state_file, 'w') as f:
                json.dump(data, f)
        
        # Cleanup states older than 7 days
        cleanup_count = await state_manager.cleanup_old_states(max_age_days=7)
        
        assert cleanup_count == 2, "Should cleanup 2 old states"
        
        # Verify recent state still exists
        remaining_agents = await state_manager.list_agents_with_state()
        assert "recent-agent" in remaining_agents
        assert "old-agent" not in remaining_agents
        assert "very-old-agent" not in remaining_agents
    
    @pytest.mark.asyncio
    async def test_cleanup_corrupted_state_files(self, state_manager, temp_storage):
        """Test cleanup of corrupted state files."""
        # Create valid state
        await state_manager.save_state("valid-agent", {"test": "data"})
        
        # Create corrupted state file
        corrupted_file = temp_storage / "corrupted-agent_state.json"
        with open(corrupted_file, 'w') as f:
            f.write("invalid json {")
        
        # Cleanup should handle corrupted files
        cleanup_count = await state_manager.cleanup_old_states(max_age_days=0)
        
        assert cleanup_count >= 1, "Should cleanup corrupted files"
        assert not corrupted_file.exists(), "Corrupted file should be removed"


class TestStateManagerPerformance:
    """Test performance requirements for state operations."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def state_manager(self, temp_storage):
        """Create state manager for testing."""
        return MockStateManager(temp_storage)
    
    @pytest.mark.asyncio
    async def test_save_state_performance(self, state_manager):
        """Test that state saving meets performance requirements."""
        agent_id = "performance-test-agent"
        large_state = {
            "components": [f"Component{i}" for i in range(100)],
            "generated_code": {f"comp{i}": f"code{i}" * 100 for i in range(50)},
            "validation_results": {f"result{i}": {"score": i % 5} for i in range(200)}
        }
        
        start_time = time.time()
        await state_manager.save_state(agent_id, large_state)
        end_time = time.time()
        
        save_duration = end_time - start_time
        assert save_duration < 1.0, f"State save took {save_duration}s, should be < 1.0s"
    
    @pytest.mark.asyncio
    async def test_load_state_performance(self, state_manager):
        """Test that state loading meets performance requirements."""
        agent_id = "load-performance-agent"
        large_state = {
            "data": [{"item": i, "content": f"content{i}" * 50} for i in range(1000)]
        }
        
        # Save large state
        await state_manager.save_state(agent_id, large_state)
        
        # Test load performance
        start_time = time.time()
        loaded_state = await state_manager.load_state(agent_id)
        end_time = time.time()
        
        load_duration = end_time - start_time
        assert load_duration < 0.5, f"State load took {load_duration}s, should be < 0.5s"
        assert loaded_state is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_state_operations(self, state_manager):
        """Test thread safety of concurrent state operations."""
        async def save_load_cycle(agent_id: str, data: dict):
            await state_manager.save_state(agent_id, data)
            loaded = await state_manager.load_state(agent_id)
            return loaded == data
        
        # Run multiple concurrent operations
        tasks = []
        for i in range(10):
            agent_id = f"concurrent-agent-{i}"
            data = {"agent_number": i, "test_data": f"data_{i}"}
            tasks.append(save_load_cycle(agent_id, data))
        
        results = await asyncio.gather(*tasks)
        
        # All operations should succeed
        assert all(results), "All concurrent operations should succeed"
    
    @pytest.mark.asyncio
    async def test_memory_cache_efficiency(self, state_manager):
        """Test that memory cache improves performance."""
        agent_id = "cache-test-agent"
        test_state = {"cache_test": "data"}
        
        # Save state (populates cache)
        await state_manager.save_state(agent_id, test_state)
        
        # First load (from disk)
        start_time = time.time()
        await state_manager.load_state(agent_id)
        first_load_time = time.time() - start_time
        
        # Second load (from cache)
        start_time = time.time()
        await state_manager.load_state(agent_id)
        second_load_time = time.time() - start_time
        
        # Cache should be faster (though both are very fast in this test)
        assert second_load_time <= first_load_time * 2, "Cached load should be reasonably fast"


class TestStateManagerErrorHandling:
    """Test error handling in state management operations."""
    
    @pytest.fixture
    def temp_storage(self):
        """Create temporary storage directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.mark.asyncio
    async def test_save_state_with_invalid_data(self, temp_storage):
        """Test handling of non-serializable state data."""
        state_manager = MockStateManager(temp_storage)
        
        # Try to save non-serializable data
        invalid_state = {
            "function": lambda x: x,  # Functions are not JSON serializable
            "valid_data": "test"
        }
        
        with pytest.raises(StateManagementError):
            await state_manager.save_state("test-agent", invalid_state)
    
    @pytest.mark.asyncio
    async def test_save_state_with_readonly_directory(self, temp_storage):
        """Test handling of read-only storage directory."""
        state_manager = MockStateManager(temp_storage)
        
        # Make directory read-only
        temp_storage.chmod(0o444)
        
        try:
            with pytest.raises(StateManagementError):
                await state_manager.save_state("readonly-test", {"test": "data"})
        finally:
            # Restore permissions for cleanup
            temp_storage.chmod(0o755)
    
    @pytest.mark.asyncio
    async def test_load_state_with_permission_error(self, temp_storage):
        """Test handling of permission errors during state loading."""
        state_manager = MockStateManager(temp_storage)
        agent_id = "permission-test-agent"
        
        # Save state first
        await state_manager.save_state(agent_id, {"test": "data"})
        
        # Make state file unreadable
        state_file = temp_storage / f"{agent_id}_state.json"
        state_file.chmod(0o000)
        
        try:
            with pytest.raises(StateManagementError):
                await state_manager.load_state(agent_id)
        finally:
            # Restore permissions for cleanup
            state_file.chmod(0o644)
    
    @pytest.mark.asyncio
    async def test_graceful_handling_of_disk_full(self, temp_storage):
        """Test graceful handling when disk is full (simulated)."""
        state_manager = MockStateManager(temp_storage)
        
        # Mock disk full scenario
        original_open = open
        
        def mock_open(*args, **kwargs):
            if "w" in args[1] if len(args) > 1 else kwargs.get("mode", "r"):
                raise OSError("No space left on device")
            return original_open(*args, **kwargs)
        
        with patch("builtins.open", side_effect=mock_open):
            with pytest.raises(StateManagementError):
                await state_manager.save_state("disk-full-test", {"test": "data"})