# Developer Agent Tests

This directory contains tests for the Developer agent - responsible for transforming UX specifications into working code.

## 💻 AGENT ROLE

The Developer agent:
- Converts UX specifications to React components
- Implements FastAPI backend endpoints
- Manages Git operations and version control
- Ensures code quality and architecture compliance
- Integrates with existing component libraries
- Implements responsive design and accessibility

## Test Files

### `test_developer_agent.py`
Tests the main Developer agent functionality.

**Tests:**
- Agent initialization and configuration
- Contract processing workflow
- UX-to-code transformation
- Full-stack implementation
- Code quality validation
- Error handling and recovery

### `test_react_component_generator.py`
Tests React component generation from UX specifications.

**Tests:**
- Component code generation
- Props and state management
- Event handling implementation
- Responsive design implementation
- Accessibility features
- Component composition

### `test_fastapi_endpoint_generator.py`
Tests FastAPI backend endpoint generation.

**Tests:**
- API endpoint creation
- Request/response models
- Business logic implementation
- Database integration
- Error handling
- API documentation generation

### `test_git_operations.py`
Tests Git version control operations.

**Tests:**
- Repository cloning and setup
- Branch creation and management
- Commit creation with proper messages
- Pull request preparation
- Merge conflict resolution
- Git workflow automation

### `test_code_quality_validator.py`
Tests code quality validation and enforcement.

**Tests:**
- Code style validation (ESLint, Prettier)
- TypeScript type checking
- Code complexity analysis
- Security vulnerability scanning
- Performance optimization checks
- Architecture compliance validation

### `test_contract_compliance.py`
Tests contract validation specific to Developer.

**Tests:**
- Input contract validation (from Game Designer)
- Output contract validation (to Test Engineer)
- Code deliverable completeness
- Architecture compliance verification
- Quality gate validation

### `test_tools.py` ⚠️ NEEDS IMPLEMENTATION
Tests Developer specific tools and utilities.

**Should Test:**
- Code generation utilities
- Build system integration
- Dependency management
- Development environment setup

### `test_agent.py` ⚠️ NEEDS IMPLEMENTATION
Basic agent functionality tests.

**Should Test:**
- Agent lifecycle management
- Basic contract processing
- Quality gate validation
- Agent configuration

## Running Developer Tests

### All Developer Tests:
```bash
make test-agent-developer
# or
pytest modules/agents/developer/tests/ -v
```

### Individual Test Files:
```bash
# Main agent tests
pytest modules/agents/developer/tests/test_developer_agent.py -v

# React component tests
pytest modules/agents/developer/tests/test_react_component_generator.py -v

# FastAPI endpoint tests
pytest modules/agents/developer/tests/test_fastapi_endpoint_generator.py -v

# Git operations tests
pytest modules/agents/developer/tests/test_git_operations.py -v

# Code quality tests
pytest modules/agents/developer/tests/test_code_quality_validator.py -v
```

## Quality Requirements

- **Coverage:** 95% minimum for agent logic
- **Performance:** < 45 seconds per test file
- **Reliability:** Must validate all code generation functionality

## Test Data

### Sample UX Specification (Input):
```python
sample_ux_specification = {
    "ui_components": [
        {
            "name": "PolicyScenarioCard",
            "type": "interactive_card",
            "props": {
                "scenario_id": "string",
                "title": "string", 
                "description": "string",
                "on_select": "function"
            },
            "responsive_design": True,
            "accessibility": {
                "aria_label": "Policy scenario selection",
                "keyboard_navigation": True
            }
        }
    ],
    "game_mechanics": {
        "progression_system": {
            "type": "linear",
            "steps": 5,
            "completion_tracking": True
        }
    }
}
```

### Sample Code Output:
```python
sample_code_output = {
    "frontend_components": [
        {
            "file_path": "src/components/PolicyScenarioCard.tsx",
            "code": "export const PolicyScenarioCard: React.FC<Props> = ...",
            "tests": "src/components/__tests__/PolicyScenarioCard.test.tsx"
        }
    ],
    "backend_endpoints": [
        {
            "file_path": "api/scenarios.py",
            "code": "@app.get('/api/scenarios') async def get_scenarios():",
            "tests": "tests/api/test_scenarios.py"
        }
    ],
    "git_operations": {
        "branch_name": "feature/policy-scenarios-STORY-GH-123",
        "commits": [...]
    }
}
```

## Contract Flow

Developer handles these contract transformations:

### Input (from Game Designer):
```json
{
  "source_agent": "game_designer",
  "target_agent": "developer", 
  "input_requirements": {
    "required_data": {
      "ux_specification": {...},
      "game_mechanics": {...},
      "wireframes": {...},
      "component_library_mapping": {...}
    }
  }
}
```

### Output (to Test Engineer):
```json
{
  "source_agent": "developer",
  "target_agent": "test_engineer",
  "input_requirements": {
    "required_data": {
      "generated_code": {...},
      "architecture_documentation": {...},
      "api_specifications": {...},
      "component_documentation": {...}
    }
  }
}
```

## Key Test Scenarios

### Frontend Generation Tests:
- UX components → React TypeScript components
- Responsive design → CSS-in-JS implementation
- Accessibility specs → ARIA attributes and keyboard navigation

### Backend Generation Tests:
- API requirements → FastAPI endpoints
- Data models → Pydantic schemas
- Business logic → Service layer implementation

### Full-Stack Integration Tests:
- Frontend-backend communication
- API contract validation
- Database integration
- Authentication and authorization

### Git Workflow Tests:
- Feature branch creation
- Code commit with proper messages
- Pull request preparation
- Merge readiness validation

### Code Quality Tests:
- ESLint and Prettier compliance
- TypeScript type checking
- Security vulnerability scanning
- Performance optimization

## Integration Points

Developer integrates with:
- **Game Designer** - Via contract input
- **Test Engineer** - Via contract output
- **Git Repository** - For version control
- **Component Library** - For consistent UI
- **Build System** - For compilation and optimization

## Performance Requirements

### Code Generation Performance:
- React component generation < 5 seconds per component
- FastAPI endpoint generation < 3 seconds per endpoint
- Full feature implementation < 30 seconds

### Quality Metrics:
- Code coverage ≥ 90%
- TypeScript strict mode compliance
- ESLint zero violations
- Lighthouse performance score ≥ 90

## Mocking Strategy

For Developer tests:

### Real Code Generation:
- Test actual code generation algorithms
- Validate generated code syntax
- Check architectural compliance

### Mock External Services:
- Git operations (during testing)
- File system operations
- External API calls
- Build system operations

## See Also

- [modules/agents/developer/](../) - Agent implementation
- [TEST_STRATEGY.md](../../../../TEST_STRATEGY.md) - Overall test strategy
- [Implementation_rules.md](../../../../Implementation_rules.md) - Agent specifications

---

💻 **Remember:** Developer tests ensure that UX specifications are transformed into high-quality, maintainable, and accessible code that serves Swedish municipal users effectively.