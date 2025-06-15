# Contract Model Implementation Prompts for Agent-Specific AIs

## 🎯 CRITICAL CONTRACT COMPLIANCE REQUIREMENT

Contract models are **ESSENTIAL** for DigiNativa's modular architecture. Only Project Manager has complete contract models - all other agents need Pydantic contract models for type safety and validation.

**Current Status:**
- ✅ **Project Manager**: Complete (input_models.py + output_models.py)
- ❌ **Game Designer**: Missing contract models 
- ❌ **Developer**: Missing contract models
- ❌ **Test Engineer**: Missing contract models
- ❌ **QA Tester**: Missing contract models
- ❌ **Quality Reviewer**: Missing contract models

---

## 📋 CONTRACT MODEL REQUIREMENTS

Each agent needs both input and output contract models following this structure:

### Required Files per Agent:
```
modules/agents/{agent_name}/contracts/
├── input_models.py    # Pydantic models for incoming contracts
├── output_models.py   # Pydantic models for outgoing contracts
└── __init__.py        # Package initialization
```

### Pydantic Model Standards:
- **BaseModel inheritance** with Field validation
- **JSON schema compatibility** matching agent_contract_schema.json
- **DNA compliance structure** embedded in all contracts
- **Contract metadata** (version, source_agent, target_agent)
- **Example schema_extra** for documentation

---

## 🚀 AGENT-SPECIFIC CONTRACT MODEL PROMPTS

### Game Designer Contract Models
```
PROMPT FOR GAME DESIGNER AI:

Create complete Pydantic contract models for Game Designer agent:

1. **INPUT MODEL** (modules/agents/game_designer/contracts/input_models.py):
   - GameDesignerInputContract: Receives Project Manager output
   - Fields: story_id, ux_requirements, municipal_context, accessibility_requirements
   - DNA compliance validation structure
   - Example: PM story breakdown to UX requirements

2. **OUTPUT MODEL** (modules/agents/game_designer/contracts/output_models.py):
   - GameDesignerOutputContract: Sends to Developer agent
   - Fields: component_specifications, wireframes, design_tokens, accessibility_guidelines
   - UX delivery data for implementation
   - Example: Complete UX specs with Shadcn/UI component mapping

CRITICAL REQUIREMENTS:
- Follow exact pattern from modules/agents/project_manager/contracts/output_models.py
- Include DNA compliance structure in both input/output models
- Add Field validation with descriptions for all properties
- Create schema_extra examples matching Game Designer responsibilities
- Ensure compatibility with agent_contract_schema.json structure

Game Designer is critical UX handoff point - contract models must capture complete design specifications.
```

### Developer Agent Contract Models
```
PROMPT FOR DEVELOPER AI:

Create complete Pydantic contract models for Developer agent:

1. **INPUT MODEL** (modules/agents/developer/contracts/input_models.py):
   - DeveloperInputContract: Receives Game Designer output
   - Fields: component_specifications, design_tokens, technical_requirements, api_specifications
   - UX to implementation translation structure
   - Example: Design specs to code generation requirements

2. **OUTPUT MODEL** (modules/agents/developer/contracts/output_models.py):
   - DeveloperOutputContract: Sends to Test Engineer agent
   - Fields: component_implementations, api_implementations, git_commit_hash, test_suite
   - Implementation delivery data with testing requirements
   - Example: React + FastAPI code with Git operations

CRITICAL REQUIREMENTS:
- Include React/TypeScript component generation specs
- Add FastAPI endpoint implementation requirements
- Capture Git workflow data (branch, commit, PR information)
- Include performance data (API response times, bundle sizes)
- Add implementation complexity scoring

Developer is core implementation agent - contracts must capture complete technical delivery data.
```

### Test Engineer Contract Models  
```
PROMPT FOR TEST ENGINEER AI:

Create complete Pydantic contract models for Test Engineer agent:

1. **INPUT MODEL** (modules/agents/test_engineer/contracts/input_models.py):
   - TestEngineerInputContract: Receives Developer output
   - Fields: component_implementations, api_implementations, implementation_docs, git_commit_hash
   - Implementation to testing translation structure
   - Example: Code implementation to test generation requirements

2. **OUTPUT MODEL** (modules/agents/test_engineer/contracts/output_models.py):
   - TestEngineerOutputContract: Sends to QA Tester agent
   - Fields: integration_test_suite, e2e_test_suite, performance_results, security_scan_results, coverage_report
   - Testing delivery data with quality validation
   - Example: Complete test suites with DNA validation results

CRITICAL REQUIREMENTS:
- Include DNA test validation structure (DNATestValidationResult integration)
- Add performance testing data (API <200ms, Lighthouse >90)
- Capture security scan results and vulnerability data
- Include coverage analysis and automation configuration
- Add municipal testing specialization data

Test Engineer has DNA validation - ensure DNA compliance results are properly structured in contracts.
```

### QA Tester Contract Models
```
PROMPT FOR QA TESTER AI:

Create complete Pydantic contract models for QA Tester agent:

1. **INPUT MODEL** (modules/agents/qa_tester/contracts/input_models.py):
   - QATesterInputContract: Receives Test Engineer output  
   - Fields: integration_test_suite, e2e_test_suite, performance_results, coverage_report, automation_config
   - Testing to quality validation translation structure
   - Example: Test results to UX validation requirements

2. **OUTPUT MODEL** (modules/agents/qa_tester/contracts/output_models.py):
   - QATesterOutputContract: Sends to Quality Reviewer agent
   - Fields: ux_validation_results, accessibility_compliance_report, persona_testing_results, quality_intelligence_predictions
   - Quality validation delivery data with AI insights
   - Example: Complete UX validation with AI quality predictions

CRITICAL REQUIREMENTS:
- Include AI Quality Intelligence results (QualityIntelligenceEngine integration)
- Add Anna persona testing results and satisfaction predictions
- Capture municipal compliance validation (Swedish public sector)
- Include accessibility validation (WCAG AA compliance)
- Add performance testing results for municipal scenarios

QA Tester has revolutionary AI capabilities - ensure AI quality predictions are captured in contract models.
```

### Quality Reviewer Contract Models
```
PROMPT FOR QUALITY REVIEWER AI:

Create complete Pydantic contract models for Quality Reviewer agent:

1. **INPUT MODEL** (modules/agents/quality_reviewer/contracts/input_models.py):
   - QualityReviewerInputContract: Receives QA Tester output
   - Fields: ux_validation_results, accessibility_compliance_report, persona_testing_results, quality_metrics
   - Quality validation to final approval translation structure
   - Example: QA results to final approval decision requirements

2. **OUTPUT MODEL** (modules/agents/quality_reviewer/contracts/output_models.py):
   - QualityReviewerOutputContract: Final approval or revision request
   - Fields: approval_decision, quality_score, client_communication_data, deployment_instructions, revision_requirements
   - Final approval delivery data with client communication
   - Example: Deployment approval with Swedish municipal client communication

CRITICAL REQUIREMENTS:
- Include client communication data (ClientCommunicator integration)
- Add Swedish municipal communication templates and workflow
- Capture final approval decision with quality scoring
- Include revision requirements with specific feedback
- Add deployment instructions and staging environment data

Quality Reviewer is final approval gate - contracts must capture complete approval workflow and client communication.
```

---

## 📊 CONTRACT INTEGRATION BENEFITS

**Before Contract Models (Current State):**
- ❌ No type safety for agent handoffs
- ❌ Manual contract validation required
- ❌ Potential runtime errors from contract mismatches
- ❌ Difficult debugging of agent communication issues

**After Contract Models (Target State):**
- ✅ Full type safety with Pydantic validation
- ✅ Automatic contract validation at runtime
- ✅ Clear agent communication interfaces
- ✅ IDE support with auto-completion and type checking
- ✅ Easy debugging with structured data validation

---

## 🎯 IMPLEMENTATION STANDARDS

### Directory Structure per Agent:
```
modules/agents/{agent_name}/contracts/
├── __init__.py                 # Package init with exports
├── input_models.py            # Pydantic input contracts
└── output_models.py           # Pydantic output contracts
```

### Required Imports:
```python
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
```

### Base Contract Structure:
```python
class AgentOutputContract(BaseModel):
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version")
    source_agent: str = Field("agent_name", description="Source agent type")
    target_agent: str = Field("target_agent", description="Target agent type")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    # Story identification
    story_id: str = Field(..., description="Unique story identifier")
    
    # DNA compliance (REQUIRED)
    dna_compliance: Dict[str, Any] = Field(..., description="DNA principle validation results")
    
    # Agent-specific data fields
    # ... add agent-specific contract data
    
    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
        schema_extra = {"example": {}}  # Add example contract
```

### Validation Requirements:
- All fields must have type annotations and Field descriptions
- DNA compliance structure required in all contracts
- Example schema_extra for documentation
- Compatible with agent_contract_schema.json structure

---

## 💡 INTEGRATION PRIORITY

**Execute these prompts in parallel - all agents need contract models for type-safe communication.**

Contract models enable:
- Type-safe agent communication
- Runtime contract validation
- Clear agent interface documentation
- IDE support for development
- Easier debugging and testing

**This is a critical requirement for production-ready agent communication.**