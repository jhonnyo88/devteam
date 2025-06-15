# Test Engineer Agent Tests

This directory contains tests for the Test Engineer agent - responsible for creating comprehensive test suites for generated code.

## 🧪 AGENT ROLE

The Test Engineer agent:
- Generates unit tests for React components
- Creates integration tests for API endpoints
- Implements end-to-end user journey tests
- Performs security vulnerability scanning
- Conducts performance testing
- Ensures comprehensive test coverage

## Test Files

### `test_test_engineer_agent.py`
Tests the main Test Engineer agent functionality.

**Tests:**
- Agent initialization and configuration
- Contract processing workflow
- Test suite generation
- Coverage analysis
- Test execution coordination
- Error handling and reporting

### `test_unit_test_generator.py`
Tests unit test generation for React components and backend functions.

**Tests:**
- React component test generation
- Backend function test creation
- Test case identification and coverage
- Mock generation and dependency injection
- Assertion library integration
- Test data generation

### `test_integration_test_generator.py`
Tests integration test generation for APIs and services.

**Tests:**
- API endpoint integration tests
- Database integration testing
- Service layer integration tests
- External API integration tests
- Error scenario testing
- Performance integration tests

### `test_e2e_test_generator.py`
Tests end-to-end test generation for complete user journeys.

**Tests:**
- User journey test creation
- Playwright/Cypress test generation
- Cross-browser compatibility tests
- Accessibility testing automation
- Visual regression testing
- Mobile responsiveness tests

### `test_security_scanner.py`
Tests security vulnerability scanning functionality.

**Tests:**
- Dependency vulnerability scanning
- Code security analysis
- SQL injection detection
- XSS vulnerability testing
- Authentication/authorization testing
- Security compliance reporting

### `test_performance_tester.py`
Tests performance testing and analysis.

**Tests:**
- Load testing implementation
- Performance benchmarking
- Memory usage analysis
- API response time testing
- Frontend performance metrics
- Performance regression detection

### `test_contract_compliance.py`
Tests contract validation specific to Test Engineer.

**Tests:**
- Input contract validation (from Developer)
- Output contract validation (to QA Tester)
- Test deliverable completeness
- Coverage requirement validation
- Quality gate compliance

### `test_tools.py` ⚠️ NEEDS IMPLEMENTATION
Tests Test Engineer specific tools and utilities.

**Should Test:**
- Test framework integration
- Coverage reporting tools
- Test data management
- Test environment setup

### `test_agent.py` ⚠️ NEEDS IMPLEMENTATION
Basic agent functionality tests.

**Should Test:**
- Agent lifecycle management
- Basic contract processing
- Quality gate validation
- Agent configuration

## Running Test Engineer Tests

### All Test Engineer Tests:
```bash
make test-agent-test_engineer
# or
pytest modules/agents/test_engineer/tests/ -v
```

### Individual Test Files:
```bash
# Main agent tests
pytest modules/agents/test_engineer/tests/test_test_engineer_agent.py -v

# Unit test generation tests
pytest modules/agents/test_engineer/tests/test_unit_test_generator.py -v

# Integration test generation tests
pytest modules/agents/test_engineer/tests/test_integration_test_generator.py -v

# E2E test generation tests
pytest modules/agents/test_engineer/tests/test_e2e_test_generator.py -v

# Security scanner tests
pytest modules/agents/test_engineer/tests/test_security_scanner.py -v

# Performance tester tests
pytest modules/agents/test_engineer/tests/test_performance_tester.py -v
```

## Quality Requirements

- **Coverage:** 95% minimum for agent logic
- **Performance:** < 45 seconds per test file
- **Reliability:** Must validate all test generation functionality

## Test Data

### Sample Generated Code (Input):
```python
sample_generated_code = {
    "frontend_components": [
        {
            "file_path": "src/components/PolicyScenarioCard.tsx",
            "code": "export const PolicyScenarioCard: React.FC<Props> = ...",
            "component_type": "interactive_card",
            "props": ["scenario_id", "title", "description", "on_select"]
        }
    ],
    "backend_endpoints": [
        {
            "file_path": "api/scenarios.py", 
            "code": "@app.get('/api/scenarios') async def get_scenarios():",
            "endpoint_type": "GET",
            "path": "/api/scenarios",
            "response_model": "ScenarioListResponse"
        }
    ],
    "architecture_documentation": {...}
}
```

### Sample Test Suite (Output):
```python
sample_test_suite = {
    "unit_tests": [
        {
            "file_path": "src/components/__tests__/PolicyScenarioCard.test.tsx",
            "test_framework": "Jest + React Testing Library",
            "test_cases": [
                "renders with required props",
                "handles click events",
                "displays accessibility attributes"
            ],
            "coverage_percentage": 95
        }
    ],
    "integration_tests": [
        {
            "file_path": "tests/api/test_scenarios.py",
            "test_framework": "pytest + httpx",
            "test_cases": [
                "GET /api/scenarios returns scenario list",
                "handles empty scenario list",
                "handles server errors"
            ]
        }
    ],
    "e2e_tests": [
        {
            "file_path": "e2e/policy-scenarios.spec.ts",
            "test_framework": "Playwright",
            "test_cases": [
                "user can select policy scenario",
                "scenario selection updates progress"
            ]
        }
    ]
}
```

## Contract Flow

Test Engineer handles these contract transformations:

### Input (from Developer):
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

### Output (to QA Tester):
```json
{
  "source_agent": "test_engineer",
  "target_agent": "qa_tester",
  "input_requirements": {
    "required_data": {
      "test_suite": {...},
      "coverage_report": {...},
      "security_scan_results": {...},
      "performance_benchmarks": {...}
    }
  }
}
```

## Key Test Scenarios

### Unit Test Generation:
- React components → Jest + React Testing Library tests
- Backend functions → pytest unit tests
- Utility functions → Comprehensive test coverage

### Integration Test Generation:
- API endpoints → httpx integration tests
- Database operations → Database integration tests
- External services → Mock-based integration tests

### E2E Test Generation:
- User journeys → Playwright tests
- Cross-browser compatibility → Multi-browser test suites
- Accessibility → Automated accessibility tests

### Security Testing:
- Code vulnerability scanning
- Dependency security analysis
- Authentication flow testing
- Input validation testing

### Performance Testing:
- Load testing for APIs
- Frontend performance metrics
- Memory usage analysis
- Response time benchmarking

## Testing Frameworks Integration

### Frontend Testing:
- **Jest** - Unit testing framework
- **React Testing Library** - Component testing
- **Playwright** - E2E testing
- **Lighthouse CI** - Performance testing

### Backend Testing:
- **pytest** - Python unit/integration testing
- **httpx** - API testing
- **SQLAlchemy** - Database testing
- **locust** - Load testing

### Security Testing:
- **bandit** - Python security analysis
- **npm audit** - Node.js dependency scanning
- **OWASP ZAP** - Web application security

## Performance Requirements

### Test Generation Performance:
- Unit test generation < 3 seconds per component
- Integration test generation < 5 seconds per endpoint
- E2E test generation < 10 seconds per user journey

### Coverage Targets:
- Unit test coverage ≥ 90%
- Integration test coverage ≥ 85%
- E2E test coverage ≥ 80% of critical paths

## Integration Points

Test Engineer integrates with:
- **Developer** - Via contract input
- **QA Tester** - Via contract output
- **Test Frameworks** - For test execution
- **CI/CD Pipeline** - For automated testing

## See Also

- [modules/agents/test_engineer/](../) - Agent implementation
- [TEST_STRATEGY.md](../../../../TEST_STRATEGY.md) - Overall test strategy
- [Implementation_rules.md](../../../../Implementation_rules.md) - Agent specifications

---

🧪 **Remember:** Test Engineer tests ensure that generated code is thoroughly tested, secure, and performant, providing confidence in the quality delivered to Swedish municipal users.