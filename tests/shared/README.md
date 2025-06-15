# Shared System Tests

This directory contains tests for core shared components that all agents depend on.

## ⚙️ PURPOSE

These tests validate the foundational components that enable:
- Agent base functionality
- Inter-agent communication
- Contract validation
- State management

## Test Files

### `test_base_agent.py`
Tests the BaseAgent class that all agents inherit from.

**Tests:**
- Agent initialization and configuration
- Contract processing workflow
- Error handling and logging
- Quality gate validation framework
- Agent lifecycle management

### `test_event_bus.py` 
Tests the EventBus system for agent communication.

**Tests:**
- Event publishing and subscription
- Event routing between agents
- Error handling in event processing
- Event persistence and replay

### `test_state_manager.py`
Tests the StateManager for maintaining agent state.

**Tests:**
- State persistence and retrieval
- State isolation between agents
- State cleanup and management
- Concurrent state access

### `test_contract_validator.py`
Tests the ContractValidator that validates all contracts.

**Tests:**
- Contract schema validation
- DNA compliance validation
- Contract transformation validation
- Error reporting and debugging

## Running Shared Tests

### All Shared Tests:
```bash
pytest tests/shared/ -v
```

### Individual Test Files:
```bash
# Base agent tests
pytest tests/shared/test_base_agent.py -v

# Event bus tests
pytest tests/shared/test_event_bus.py -v

# State manager tests
pytest tests/shared/test_state_manager.py -v

# Contract validator tests
pytest tests/shared/test_contract_validator.py -v
```

## Quality Requirements

- **Coverage:** 95% minimum
- **Performance:** < 2 minutes for full shared test suite
- **Reliability:** Foundation for all other tests

## Test Categories

### Core Functionality Tests
Validate basic operations of shared components:

```python
def test_base_agent_initialization():
    """Test agent initializes correctly."""
    agent = BaseAgent("test_agent")
    assert agent.agent_type == "test_agent"
    assert agent.contract_validator is not None
```

### Error Handling Tests
Ensure robust error handling:

```python
def test_contract_validator_invalid_schema():
    """Test contract validator handles invalid schemas."""
    with pytest.raises(ValidationError):
        validator.validate_contract(invalid_contract)
```

### Performance Tests
Verify performance requirements:

```python
def test_contract_validation_performance():
    """Test contract validation meets performance requirements."""
    start_time = time.time()
    validator.validate_contract(large_contract)
    duration = time.time() - start_time
    assert duration < 0.1  # < 100ms
```

## Shared Component Dependencies

### BaseAgent Dependencies:
- ContractValidator for contract validation
- StateManager for state persistence
- EventBus for communication
- Exception classes for error handling

### EventBus Dependencies:
- StateManager for event persistence
- ContractValidator for event validation
- Logger for event tracking

### StateManager Dependencies:
- File system for state persistence
- Locking mechanisms for concurrent access
- Serialization for state storage

### ContractValidator Dependencies:
- JSON Schema for validation
- DNA compliance framework
- Error reporting system

## Mock Strategy

For shared component tests:

### Minimal Mocking:
- Test actual implementations when possible
- Mock only external dependencies (file system, network)
- Use real validation logic

### Example Test Structure:
```python
class TestBaseAgent:
    @pytest.fixture
    def base_agent(self):
        return BaseAgent("test_agent")
    
    def test_contract_processing(self, base_agent):
        """Test contract processing workflow."""
        # Use real contract validation
        contract = create_valid_contract()
        result = base_agent.process_contract(contract)
        assert_valid_result(result)
```

## Integration with Agent Tests

Shared component tests support agent-specific tests:

### Test Utilities:
- Contract creation helpers
- Mock agent implementations
- Test data generators
- Assertion helpers

### Example Utilities:
```python
def create_valid_contract(source_agent="test", target_agent="test"):
    """Create a valid contract for testing."""
    return {
        "contract_version": "1.0",
        "story_id": "STORY-TEST-001",
        "source_agent": source_agent,
        "target_agent": target_agent,
        # ... rest of contract structure
    }
```

## Debugging Support

Shared tests provide debugging utilities:

### Logging Configuration:
- Detailed logging for test failures
- Contract validation tracing
- Event bus message tracking

### Test Helpers:
- Contract comparison utilities
- State inspection tools
- Error analysis helpers

## See Also

- [modules/shared/](../../modules/shared/) - Shared component implementations
- [TEST_STRATEGY.md](../../TEST_STRATEGY.md) - Overall test strategy  
- [Implementation_rules.md](../../Implementation_rules.md) - System specifications

---

⚙️ **Remember:** Shared component tests are the foundation that enables reliable agent testing and system integration.