# QA Tester Agent Tests

This directory contains tests for the QA Tester agent - responsible for validating features through user persona testing and accessibility compliance.

## 👥 AGENT ROLE

The QA Tester agent:
- Performs persona-based user testing (Anna personas)
- Validates accessibility compliance (WCAG AA)
- Conducts user flow validation
- Tests learning effectiveness and pedagogical value
- Ensures feature usability and user experience
- Validates time constraint compliance

## Test Files

### `test_qa_tester_agent.py`
Tests the main QA Tester agent functionality.

**Tests:**
- Agent initialization and configuration
- Contract processing workflow
- Persona testing coordination
- Accessibility validation
- User experience assessment
- Quality reporting

### `test_persona_simulator.py`
Tests user persona simulation and testing.

**Tests:**
- Anna persona simulation
- User behavior modeling
- Task completion testing
- Learning effectiveness measurement
- User satisfaction assessment
- Persona-specific validation

### `test_accessibility_validator.py`
Tests accessibility compliance validation.

**Tests:**
- WCAG AA compliance checking
- Screen reader compatibility
- Keyboard navigation testing
- Color contrast validation
- Alternative text verification
- Focus management testing

### `test_user_flow_validator.py`
Tests user flow validation and optimization.

**Tests:**
- User journey completion testing
- Flow efficiency measurement
- Error handling validation
- Navigation usability testing
- Task completion rate analysis
- User frustration detection

### `test_learning_effectiveness_assessor.py`
Tests learning effectiveness and pedagogical validation.

**Tests:**
- Learning objective achievement
- Knowledge retention assessment
- Engagement level measurement
- Pedagogical effectiveness scoring
- Learning progress tracking
- Educational outcome validation

### `test_contract_compliance.py`
Tests contract validation specific to QA Tester.

**Tests:**
- Input contract validation (from Test Engineer)
- Output contract validation (to Quality Reviewer)
- QA deliverable completeness
- User testing result validation
- Quality metrics validation

### `test_tools.py` ⚠️ NEEDS IMPLEMENTATION
Tests QA Tester specific tools and utilities.

**Should Test:**
- Testing automation tools
- Accessibility scanning tools
- User simulation frameworks
- Quality metrics calculation

### `test_agent.py` ⚠️ NEEDS IMPLEMENTATION
Basic agent functionality tests.

**Should Test:**
- Agent lifecycle management
- Basic contract processing
- Quality gate validation
- Agent configuration

## Running QA Tester Tests

### All QA Tester Tests:
```bash
make test-agent-qa_tester
# or
pytest modules/agents/qa_tester/tests/ -v
```

### Individual Test Files:
```bash
# Main agent tests
pytest modules/agents/qa_tester/tests/test_qa_tester_agent.py -v

# Persona simulation tests
pytest modules/agents/qa_tester/tests/test_persona_simulator.py -v

# Accessibility validation tests
pytest modules/agents/qa_tester/tests/test_accessibility_validator.py -v

# User flow validation tests
pytest modules/agents/qa_tester/tests/test_user_flow_validator.py -v

# Learning effectiveness tests
pytest modules/agents/qa_tester/tests/test_learning_effectiveness_assessor.py -v
```

## Quality Requirements

- **Coverage:** 95% minimum for agent logic
- **Performance:** < 45 seconds per test file
- **Reliability:** Must validate all QA testing functionality

## Test Data

### Sample Test Suite (Input):
```python
sample_test_suite = {
    "unit_tests": {
        "total_tests": 45,
        "passed_tests": 45,
        "coverage_percentage": 96
    },
    "integration_tests": {
        "api_tests": 15,
        "database_tests": 8,
        "all_passed": True
    },
    "e2e_tests": {
        "user_journey_tests": 12,
        "accessibility_tests": 8,
        "performance_tests": 5,
        "all_passed": True
    },
    "security_scan_results": {
        "vulnerabilities_found": 0,
        "scan_passed": True
    }
}
```

### Sample QA Results (Output):
```python
sample_qa_results = {
    "persona_testing": {
        "anna_persona_results": {
            "task_completion_rate": 96,
            "average_completion_time": 8.5,
            "user_satisfaction_score": 4.3,
            "learning_effectiveness": 4.4
        }
    },
    "accessibility_audit": {
        "wcag_compliance_percent": 94,
        "violations": [],
        "keyboard_accessible": True,
        "screen_reader_compatible": True
    },
    "user_flow_validation": {
        "flow_completion_rate": 96,
        "navigation_efficiency": 4.2,
        "error_recovery_rate": 100
    },
    "learning_effectiveness": {
        "objective_achievement_rate": 92,
        "knowledge_retention_score": 4.1,
        "engagement_level": 4.3
    }
}
```

## Contract Flow

QA Tester handles these contract transformations:

### Input (from Test Engineer):
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

### Output (to Quality Reviewer):
```json
{
  "source_agent": "qa_tester",
  "target_agent": "quality_reviewer",
  "input_requirements": {
    "required_data": {
      "persona_testing_results": {...},
      "accessibility_audit": {...},
      "user_flow_validation": {...},
      "learning_effectiveness_assessment": {...},
      "overall_quality_score": 4.2
    }
  }
}
```

## Key Test Scenarios

### Persona Testing:
- Anna persona task completion
- User behavior simulation
- Learning preference accommodation
- Municipal context understanding

### Accessibility Testing:
- WCAG AA compliance validation
- Screen reader compatibility
- Keyboard navigation testing
- Color contrast verification

### User Experience Testing:
- Task completion efficiency
- Error handling effectiveness
- Navigation intuitiveness
- User satisfaction measurement

### Learning Effectiveness Testing:
- Learning objective achievement
- Knowledge retention assessment
- Engagement level measurement
- Pedagogical value validation

### Time Constraint Testing:
- 10-minute completion target
- Task efficiency optimization
- Time pressure handling
- Completion rate under constraints

## User Personas

### Anna - Primary Municipal Employee
```python
anna_persona = {
    "role": "Municipal Administrator",
    "experience": "Intermediate computer skills",
    "goals": [
        "Learn policy applications quickly",
        "Apply knowledge to real situations",
        "Complete training efficiently"
    ],
    "constraints": [
        "Limited time (10 minutes max)",
        "Work interruptions",
        "Varying computer access"
    ],
    "preferences": [
        "Clear instructions",
        "Immediate feedback",
        "Practical examples"
    ]
}
```

### Testing Scenarios for Anna:
- Policy scenario selection and completion
- Learning module navigation
- Progress tracking usage
- Help system utilization
- Error recovery handling

## Accessibility Standards

### WCAG AA Compliance:
- **Perceivable**: Text alternatives, captions, color contrast
- **Operable**: Keyboard accessible, no seizures, navigable
- **Understandable**: Readable, predictable, input assistance
- **Robust**: Compatible with assistive technologies

### Testing Tools:
- **axe-core** - Automated accessibility testing
- **WAVE** - Web accessibility evaluation
- **Screen readers** - NVDA, JAWS, VoiceOver
- **Keyboard testing** - Tab navigation, focus management

## Performance Requirements

### QA Testing Performance:
- Persona testing < 15 minutes per scenario
- Accessibility audit < 5 minutes per feature
- User flow validation < 10 minutes per flow

### Quality Metrics:
- Task completion rate ≥ 90%
- User satisfaction score ≥ 4.0/5.0
- WCAG compliance ≥ 95%
- Learning effectiveness ≥ 4.0/5.0

## Integration Points

QA Tester integrates with:
- **Test Engineer** - Via contract input
- **Quality Reviewer** - Via contract output
- **Accessibility Tools** - For compliance testing
- **User Simulation** - For persona testing

## See Also

- [modules/agents/qa_tester/](../) - Agent implementation
- [TEST_STRATEGY.md](../../../../TEST_STRATEGY.md) - Overall test strategy
- [Implementation_rules.md](../../../../Implementation_rules.md) - Agent specifications

---

👥 **Remember:** QA Tester tests ensure that features truly serve Swedish municipal users like Anna, providing accessible, effective, and engaging learning experiences.