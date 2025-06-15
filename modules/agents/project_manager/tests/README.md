# Project Manager Agent Tests

This directory contains tests for the Project Manager agent - the first agent in the DigiNativa AI Team pipeline.

## 🎯 AGENT ROLE

The Project Manager agent:
- Fetches and analyzes GitHub issues
- Performs DNA compliance analysis
- Creates detailed story breakdowns
- Generates acceptance criteria
- Assesses feature complexity
- Initiates the development pipeline

## Test Files

### `test_project_manager_agent.py`
Tests the main Project Manager agent functionality.

**Tests:**
- Agent initialization and configuration
- Contract processing workflow
- GitHub issue processing
- DNA analysis integration
- Story breakdown creation
- Error handling and edge cases

### `test_github_integration.py`
Tests GitHub API integration and issue parsing.

**Tests:**
- GitHub API authentication and connection
- Issue fetching and parsing
- Priority and persona extraction
- Acceptance criteria parsing
- Rate limit handling
- Error handling for API failures

### `test_story_analyzer.py`
Tests story analysis and breakdown creation.

**Tests:**
- Story breakdown generation
- User story extraction
- Acceptance criteria generation
- Complexity assessment
- Technical requirements analysis
- Implementation task breakdown

### `test_dna_analyzer.py`
Tests DNA compliance analysis functionality.

**Tests:**
- Design principle validation
- Architecture compliance checking
- DNA scoring algorithms
- Violation detection and reporting
- Compliance recommendations

### `test_contract_compliance.py`
Tests contract validation specific to Project Manager.

**Tests:**
- Input contract validation (from GitHub)
- Output contract validation (to Game Designer)
- DNA compliance structure validation
- Contract transformation correctness

### `test_tools.py` ⚠️ NEEDS IMPLEMENTATION
Tests Project Manager specific tools and utilities.

**Should Test:**
- Tool initialization and configuration
- Tool integration with agent
- Tool error handling
- Tool performance requirements

### `test_agent.py` ⚠️ NEEDS IMPLEMENTATION  
Basic agent functionality tests.

**Should Test:**
- Agent lifecycle management
- Basic contract processing
- Quality gate validation
- Agent configuration

## Running Project Manager Tests

### All Project Manager Tests:
```bash
make test-agent-project_manager
# or
pytest modules/agents/project_manager/tests/ -v
```

### Individual Test Files:
```bash
# Main agent tests
pytest modules/agents/project_manager/tests/test_project_manager_agent.py -v

# GitHub integration tests
pytest modules/agents/project_manager/tests/test_github_integration.py -v

# Story analyzer tests
pytest modules/agents/project_manager/tests/test_story_analyzer.py -v

# DNA analyzer tests
pytest modules/agents/project_manager/tests/test_dna_analyzer.py -v

# Contract compliance tests
pytest modules/agents/project_manager/tests/test_contract_compliance.py -v
```

## Quality Requirements

- **Coverage:** 95% minimum for agent logic
- **Performance:** < 30 seconds per test file
- **Reliability:** Must validate all Project Manager functionality

## Test Data

### Sample GitHub Issue:
```python
sample_github_issue = {
    "number": 123,
    "title": "Add interactive policy practice scenarios",
    "body": """
    ## Feature Description
    As Anna, I want to practice policy application...
    
    ## Acceptance Criteria
    - [ ] User can select scenarios
    - [ ] User receives feedback
    
    ## Learning Objectives
    - Apply policy knowledge
    - Understand decision frameworks
    """,
    "labels": [{"name": "priority-high"}, {"name": "persona-anna"}],
    # ... complete structure
}
```

### Sample DNA Analysis:
```python
sample_dna_analysis = {
    "compliant": True,
    "compliance_score": 85.0,
    "pedagogical_value": True,
    "policy_to_practice": True,
    "time_respect": True,
    "holistic_thinking": True,
    "professional_tone": True,
    "violations": [],
    "recommendations": []
}
```

## Contract Flow

Project Manager handles these contract transformations:

### Input (from GitHub):
```json
{
  "contract_version": "1.0",
  "story_id": "STORY-GH-123",
  "source_agent": "github",
  "target_agent": "project_manager",
  "input_requirements": {
    "required_data": {
      "github_issue_data": {...}
    }
  }
}
```

### Output (to Game Designer):
```json
{
  "contract_version": "1.0", 
  "story_id": "STORY-GH-123",
  "source_agent": "project_manager",
  "target_agent": "game_designer",
  "dna_compliance": {...},
  "input_requirements": {
    "required_data": {
      "story_breakdown": {...},
      "dna_analysis": {...},
      "complexity_assessment": {...}
    }
  }
}
```

## Key Test Scenarios

### Happy Path Tests:
- Valid GitHub issue → Complete story breakdown
- High-quality feature → DNA compliance approval
- Complex feature → Detailed breakdown with accurate estimation

### Error Handling Tests:
- Invalid GitHub issue format
- Missing required fields
- DNA compliance violations
- External service failures

### Edge Case Tests:
- Minimal issue information
- Very complex features
- Rate limit scenarios
- Network connectivity issues

## Integration Points

Project Manager integrates with:
- **GitHub API** - For issue fetching
- **Game Designer** - Via contract handoff
- **ContractValidator** - For validation
- **EventBus** - For communication

## See Also

- [modules/agents/project_manager/](../) - Agent implementation
- [TEST_STRATEGY.md](../../../../TEST_STRATEGY.md) - Overall test strategy
- [Implementation_rules.md](../../../../Implementation_rules.md) - Agent specifications

---

🎯 **Remember:** Project Manager tests ensure the pipeline starts correctly and all features are properly analyzed before development begins.