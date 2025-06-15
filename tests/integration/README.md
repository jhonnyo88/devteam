# Integration Tests

This directory contains tests that verify agents work together correctly through the contract system to deliver complete features.

## 🔗 PURPOSE

Integration tests ensure that:
- Agents communicate properly via contracts
- The complete pipeline delivers working features
- Quality gates function correctly
- No regressions occur in agent interactions

## Test Files

### `test_full_lifecycle.py` ⚠️ NEEDS IMPLEMENTATION
Tests the complete feature development lifecycle from GitHub issue to deployment.

**Should Test:**
```
GitHub Issue → Project Manager → Game Designer → Developer → 
Test Engineer → QA Tester → Quality Reviewer → Deployment
```

**Test Scenarios:**
- Successful feature completion (happy path)
- Feature rejection and iteration cycles
- Error handling at each stage
- Performance under load

### `test_agent_communication.py` ⚠️ NEEDS IMPLEMENTATION
Tests direct agent-to-agent communication via contracts.

**Should Test:**
- Contract passing between agents
- Contract validation at handoff points
- Error propagation between agents
- Agent state isolation

### `test_quality_gates.py` ⚠️ NEEDS IMPLEMENTATION
Tests that quality gates properly validate deliverables and block progression when quality standards aren't met.

**Should Test:**
- Quality gate validation logic
- Blocking when standards not met
- Approval when standards exceeded
- Quality scoring accuracy

## Running Integration Tests

### All Integration Tests:
```bash
make test-integration
```

### Individual Test Files:
```bash
# Full lifecycle tests
pytest tests/integration/test_full_lifecycle.py -v

# Agent communication tests
pytest tests/integration/test_agent_communication.py -v

# Quality gate tests
pytest tests/integration/test_quality_gates.py -v
```

## Quality Requirements

- **Coverage:** 85% minimum
- **Performance:** < 10 minutes for full integration suite
- **Reliability:** Must catch integration failures

## Test Data Requirements

Integration tests should use:

### Realistic Test Data:
```python
sample_github_issue = {
    "number": 123,
    "title": "Policy Practice Feature",
    "body": "As Anna, I want to practice policy scenarios...",
    "labels": [{"name": "priority-high"}],
    # ... complete issue structure
}
```

### Valid Contracts:
```python
valid_contract = {
    "contract_version": "1.0",
    "story_id": "STORY-GH-123",
    "source_agent": "project_manager",
    "target_agent": "game_designer",
    "dna_compliance": {...},
    "input_requirements": {...}
}
```

## Agent Pipeline Flow

The complete agent pipeline should be tested:

1. **GitHub** → **Project Manager**
   - Issue parsing and contract creation
   - DNA analysis and story breakdown

2. **Project Manager** → **Game Designer**
   - Story requirements to UX specifications
   - Component and wireframe generation

3. **Game Designer** → **Developer**
   - UX specs to working code
   - React components and FastAPI endpoints

4. **Developer** → **Test Engineer**
   - Code to comprehensive test suite
   - Unit, integration, and E2E tests

5. **Test Engineer** → **QA Tester**
   - Tests to user validation
   - Persona testing and accessibility

6. **QA Tester** → **Quality Reviewer**
   - User validation to final approval
   - Quality scoring and deployment decision

## Mock Strategy

For integration tests, use:

### Real Components When Possible:
- Actual contract validation
- Real DNA compliance checking
- Genuine quality gate logic

### Mocks for External Services:
- GitHub API calls
- File system operations
- Deployment services

### Example Mock Structure:
```python
@pytest.fixture
def mock_external_services():
    with patch('modules.agents.project_manager.tools.github_integration.GitHubIntegration') as mock_github:
        with patch('modules.agents.developer.tools.git_operations.GitOperations') as mock_git:
            yield {
                'github': mock_github,
                'git': mock_git
            }
```

## Performance Testing

Integration tests should verify:

### Pipeline Performance:
- Full lifecycle completion < 5 minutes
- Contract validation < 100ms per contract
- Agent handoffs < 1 second per handoff

### Memory Usage:
- Pipeline memory usage < 512MB
- No memory leaks between iterations
- Efficient contract processing

## Error Scenarios

Test error handling for:

### Contract Failures:
- Invalid contract schemas
- Missing required fields
- DNA compliance violations

### Agent Failures:
- Agent execution errors
- Tool failures
- Resource unavailability

### System Failures:
- Network connectivity issues
- External service failures
- Resource exhaustion

## See Also

- [TEST_STRATEGY.md](../../TEST_STRATEGY.md) - Overall test strategy
- [Implementation_rules.md](../../Implementation_rules.md) - Agent specifications
- [modules/agents/](../../modules/agents/) - Agent implementations

---

🔗 **Remember:** Integration tests ensure the AI team works as a cohesive unit to deliver value to Swedish municipal users.