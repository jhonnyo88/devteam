# Game Designer Agent Tests

This directory contains tests for the Game Designer agent - responsible for transforming story requirements into UX specifications.

## 🎨 AGENT ROLE

The Game Designer agent:
- Converts story breakdowns to UX specifications
- Designs game mechanics and interactions
- Creates UI component specifications
- Generates wireframes and user flows
- Validates UX against DNA principles
- Ensures pedagogical effectiveness

## Test Files

### `test_game_designer_agent.py`
Tests the main Game Designer agent functionality.

**Tests:**
- Agent initialization and configuration
- Contract processing workflow
- Story-to-UX transformation
- Game mechanics generation
- UX specification creation
- Error handling and validation

### `test_ux_specification_generator.py`
Tests UX specification generation tools.

**Tests:**
- Component specification generation
- User flow design
- Interaction pattern creation
- Responsive design specifications
- Accessibility compliance
- UX validation against requirements

### `test_game_mechanics_designer.py`
Tests game mechanics design functionality.

**Tests:**
- Game mechanics selection and design
- Engagement pattern creation
- Pedagogical effectiveness optimization
- Learning objective mapping
- Progress tracking mechanisms
- Reward system design

### `test_wireframe_generator.py`
Tests wireframe and prototype generation.

**Tests:**
- Wireframe creation from specifications
- Layout optimization for different devices
- User flow visualization
- Interactive prototype generation
- Design system integration
- Accessibility considerations

### `test_dna_ux_validator.py`
Tests UX validation against DNA principles.

**Tests:**
- UI complexity validation
- Learning flow assessment
- Professional tone validation
- Time constraint compliance
- Pedagogical value measurement
- DNA compliance scoring

### `test_contract_compliance.py`
Tests contract validation specific to Game Designer.

**Tests:**
- Input contract validation (from Project Manager)
- Output contract validation (to Developer)
- UX specification completeness
- Game mechanics validation
- DNA compliance verification

### `test_tools.py` ⚠️ NEEDS IMPLEMENTATION
Tests Game Designer specific tools and utilities.

**Should Test:**
- Tool initialization and configuration
- Tool integration with agent
- Design pattern libraries
- Component mapping utilities

### `test_agent.py` ⚠️ NEEDS IMPLEMENTATION
Basic agent functionality tests.

**Should Test:**
- Agent lifecycle management
- Basic contract processing
- Quality gate validation
- Agent configuration

## Running Game Designer Tests

### All Game Designer Tests:
```bash
make test-agent-game_designer
# or
pytest modules/agents/game_designer/tests/ -v
```

### Individual Test Files:
```bash
# Main agent tests
pytest modules/agents/game_designer/tests/test_game_designer_agent.py -v

# UX specification tests
pytest modules/agents/game_designer/tests/test_ux_specification_generator.py -v

# Game mechanics tests
pytest modules/agents/game_designer/tests/test_game_mechanics_designer.py -v

# Wireframe generation tests
pytest modules/agents/game_designer/tests/test_wireframe_generator.py -v

# DNA UX validation tests
pytest modules/agents/game_designer/tests/test_dna_ux_validator.py -v
```

## Quality Requirements

- **Coverage:** 95% minimum for agent logic
- **Performance:** < 30 seconds per test file
- **Reliability:** Must validate all UX design functionality

## Test Data

### Sample Story Breakdown (Input):
```python
sample_story_breakdown = {
    "story_id": "STORY-GH-123",
    "feature_summary": {
        "title": "Policy Practice Scenarios",
        "user_persona": "Anna",
        "time_constraint_minutes": 10
    },
    "user_stories": [
        {
            "story": "As Anna, I want to practice policy scenarios",
            "acceptance_criteria": [...]
        }
    ],
    "learning_objectives": [
        "Apply policy knowledge to practical situations"
    ]
}
```

### Sample UX Specification (Output):
```python
sample_ux_specification = {
    "ui_components": [
        {
            "name": "ScenarioSelector",
            "type": "interactive_list",
            "props": {...},
            "responsive_design": True
        }
    ],
    "game_mechanics": {
        "progression_system": {...},
        "feedback_mechanisms": {...},
        "engagement_patterns": [...]
    },
    "wireframes": [
        {
            "screen_name": "scenario_selection",
            "layout": {...},
            "user_flows": [...]
        }
    ]
}
```

## Contract Flow

Game Designer handles these contract transformations:

### Input (from Project Manager):
```json
{
  "source_agent": "project_manager",
  "target_agent": "game_designer",
  "input_requirements": {
    "required_data": {
      "story_breakdown": {...},
      "dna_analysis": {...},
      "complexity_assessment": {...}
    }
  }
}
```

### Output (to Developer):
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

## Key Test Scenarios

### UX Design Tests:
- Complex learning scenarios → Intuitive UI design
- Multiple user personas → Adaptive interface design
- Accessibility requirements → WCAG compliant designs

### Game Mechanics Tests:
- Learning objectives → Engaging game mechanics
- Time constraints → Optimized progression systems
- Pedagogical effectiveness → Evidence-based designs

### DNA Compliance Tests:
- Professional tone → Appropriate UI language
- Time respect → Efficient user flows
- Pedagogical value → Learning-focused interactions

### Error Handling Tests:
- Incomplete story breakdowns
- Invalid learning objectives
- Design constraint conflicts

## Integration Points

Game Designer integrates with:
- **Project Manager** - Via contract input
- **Developer** - Via contract output
- **Component Library** - For UI specifications
- **Design System** - For consistent styling

## Performance Requirements

### UX Generation Performance:
- Component specification < 2 seconds
- Wireframe generation < 5 seconds
- Complete UX specification < 10 seconds

### Quality Metrics:
- DNA compliance score ≥ 4.0
- Accessibility compliance ≥ 95%
- User flow efficiency ≥ 90%

## See Also

- [modules/agents/game_designer/](../) - Agent implementation
- [TEST_STRATEGY.md](../../../../TEST_STRATEGY.md) - Overall test strategy
- [Implementation_rules.md](../../../../Implementation_rules.md) - Agent specifications

---

🎨 **Remember:** Game Designer tests ensure that story requirements are transformed into compelling, educational, and accessible user experiences.