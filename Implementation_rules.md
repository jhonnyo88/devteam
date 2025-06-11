# Complete AI Team Implementation Guide v2.0

*Authoritative documentation for AI assistants to understand and implement the DigiNativa AI Team system - Enhanced with integrated contract system and glossary*

---

## 📋 **OVERVIEW: WHAT YOU'RE BUILDING**

You are helping implement a **fully autonomous AI development team** that builds the DigiNativa learning game. This team consists of 6 specialized AI agents that work together to develop features from GitHub issue to deployed code.

### **System Architecture Overview**

```
GitHub Issue (Feature Request)
        ↓
   Project Manager (analyzes & breaks down)
        ↓
   Game Designer (creates UX specification)
        ↓
   Developer (implements React + FastAPI code)
        ↓
   Test Engineer (creates automated tests)
        ↓
   QA Tester (validates user experience)
        ↓
   Quality Reviewer (final approval)
        ↓
   Deployed Feature (in production)
```

### **Dual Repository Strategy**

- **AI-Team Repository:** Contains agent implementations, contracts, and coordination (this repo)
- **Product Repository:** Contains game code, feature branches, and production deployment (separate repo)

---

## 📚 **GLOSSARY OF TERMS**

**Critical Definitions for AI Understanding:**

- **Project DNA:** The shared decision-making framework consisting of 5 design principles and 4 architecture principles that guides all agent decisions
- **Contract:** A machine-readable JSON specification that defines exact input/output requirements between agents
- **Quality Gate:** An automated check that must pass before work can proceed to the next agent
- **Handoff Criteria:** Specific conditions that must be met for successful transfer of work between agents
- **Story ID:** Unique identifier format: STORY-{feature_id}-{increment} linking work to GitHub issues
- **DNA Compliance:** Boolean validation that agent output follows all project DNA principles
- **Validation Criteria:** Specific, measurable requirements that define successful completion of work
- **Rollback Conditions:** Situations that trigger automatic return of work to previous agent for revision
- **State Management:** System for preserving and recovering agent work in progress
- **Agent Modularity:** Architecture principle ensuring each agent can be developed and tested independently

---

## 🧬 **PROJECT DNA: THE FOUNDATION**

Before implementing ANY code, you must understand the Project DNA. This is the **shared decision-making framework** that ensures all agents work cohesively.

### **DNA Documents Location: `docs/dna/`**

1. **`design_principles.md`** - The 5 core principles guiding all decisions
2. **`architecture.md`** - Technical constraints and patterns
3. **`target_audience.md`** - User personas and context
4. **`game_design_document.md`** - Complete product vision
5. **`component_library.md`** - UI/UX standards (Shadcn/UI + Kenney.UI)

### **How DNA Functions as Team Coordinator**

**Critical Understanding:** DNA isn't just documentation - it's an **automated decision framework** that prevents agent drift.

```python
# Every agent decision must validate against DNA
def make_agent_decision(options: List[Any]) -> Any:
    # 1. Filter by design principles
    valid_options = [opt for opt in options if validates_all_5_principles(opt)]
    
    # 2. Apply architecture constraints  
    compliant_options = [opt for opt in valid_options if follows_architecture(opt)]
    
    # 3. Choose simplest solution (KISS principle)
    return choose_simplest_solution(compliant_options)
```

**DNA Prevents Team Fragmentation:**
- Without DNA: Each agent makes assumptions → fragmented product
- With DNA: All agents use same criteria → cohesive product

---

## 🔗 **AGENT CONTRACT SYSTEM: THE CRITICAL FOUNDATION**

**THIS IS THE MOST IMPORTANT PART:** Every agent interaction MUST use strict, machine-readable contracts. This enables modular development where each agent can be improved independently.

### **Standard Contract Format**

```json
{
  "contract_version": "1.0",
  "story_id": "STORY-{feature_id}-{increment}",
  "source_agent": "{agent_role}",
  "target_agent": "{agent_role}",
  "dna_compliance": {
    "design_principles_validation": {
      "pedagogical_value": true,
      "policy_to_practice": true,
      "time_respect": true,
      "holistic_thinking": true,
      "professional_tone": true
    },
    "architecture_compliance": {
      "api_first": true,
      "stateless_backend": true,
      "separation_of_concerns": true,
      "simplicity_first": true
    }
  },
  "input_requirements": {
    "required_files": ["string"],
    "required_data": "object",
    "required_validations": ["string"]
  },
  "output_specifications": {
    "deliverable_files": ["string"],
    "deliverable_data": "object",
    "validation_criteria": {
      "design_principles": {
        "pedagogical_value": {"min_score": 4},
        "time_respect": {"max_duration_minutes": 10}
      },
      "code_quality": {
        "test_coverage_percent": {"min": 100},
        "lighthouse_score": {"min": 90}
      }
    }
  },
  "quality_gates": ["string"],
  "handoff_criteria": ["string"]
}
```

### **Enhanced Validation Criteria Structure**

**Problem:** Original format used strings like "all_5_design_principles_addressed" requiring interpretation.

**Solution:** Structured validation objects for automated compliance checking:

```json
"validation_criteria": {
  "design_principles": {
    "pedagogical_value": {"min_score": 4, "max_score": 5},
    "time_respect": {"max_duration_minutes": 10},
    "professional_tone": {"vocabulary_complexity": "appropriate"}
  },
  "code_quality": {
    "test_coverage_percent": {"min": 100},
    "typescript_errors": {"max": 0},
    "eslint_violations": {"max": 0}
  },
  "performance": {
    "lighthouse_score": {"min": 90},
    "api_response_time_ms": {"max": 200},
    "bundle_size_kb": {"max": 500}
  }
}
```

### **Why Contracts Are Critical**

**Problem without contracts:**
```python
# ❌ This creates tight coupling - can't develop agents independently
spec = await game_designer.create_spec(story)
code = await developer.implement(spec)  # Direct dependency!
```

**Solution with contracts:**
```python
# ✅ Loose coupling via standardized contracts
contract = StandardContract.from_story(story)
await event_bus.delegate_to_agent("game_designer", contract)
completed_work = await event_bus.wait_for_completion(story_id)
```

---

## 🎯 **CONTRACT VALIDATION FRAMEWORK**

### **ContractValidator Implementation**

```python
import json
import jsonschema
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

class ContractValidator:
    """
    Validates agent contracts against schema and business rules.
    
    PURPOSE:
    Ensures all agent handoffs follow strict contract specifications,
    preventing integration failures and maintaining system modularity.
    
    ADAPTATION GUIDE:
    🔧 To adapt for your project:
    1. Update agent_sequences for your workflow
    2. Modify quality_gate_checkers for your quality standards
    3. Adjust dna_validation for your principles
    """
    
    def __init__(self, schema_path: str = "docs/contracts/agent_contract_schema.json"):
        self.schema_path = Path(schema_path)
        self.schema = self._load_schema()
        self.dna_validator = DNAValidator()
    
    def validate_contract(self, contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete contract validation including schema, business rules, and DNA compliance.
        
        Returns:
        {
            "is_valid": boolean,
            "errors": [string],
            "warnings": [string],
            "validation_timestamp": string
        }
        """
        errors = []
        warnings = []
        
        # 1. Schema validation
        schema_errors = self._validate_schema(contract)
        errors.extend(schema_errors)
        
        # 2. Business rule validation
        business_errors = self._validate_business_rules(contract)
        errors.extend(business_errors)
        
        # 3. DNA compliance validation
        dna_errors = self._validate_dna_compliance(contract)
        errors.extend(dna_errors)
        
        # 4. Quality gates validation
        quality_warnings = self._validate_quality_gates(contract)
        warnings.extend(quality_warnings)
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "validation_timestamp": datetime.now().isoformat()
        }
    
    def _validate_schema(self, contract: Dict[str, Any]) -> List[str]:
        """Validate contract against JSON schema."""
        try:
            jsonschema.validate(instance=contract, schema=self.schema)
            return []
        except jsonschema.ValidationError as e:
            return [f"Schema validation error: {e.message}"]
        except Exception as e:
            return [f"Contract validation failed: {str(e)}"]
    
    def _validate_business_rules(self, contract: Dict[str, Any]) -> List[str]:
        """Validate contract against business rules."""
        errors = []
        
        # Validate agent sequence
        source = contract.get("source_agent")
        target = contract.get("target_agent")
        if not self._validate_agent_sequence(source, target):
            errors.append(f"Invalid agent sequence: {source} → {target}")
        
        # Validate story ID format
        story_id = contract.get("story_id", "")
        if not story_id.startswith("STORY-"):
            errors.append(f"Invalid story ID format: {story_id}")
        
        # Validate file paths contain story_id
        if not self._validate_file_paths(contract):
            errors.append("File paths must contain story_id for traceability")
        
        return errors
    
    def _validate_dna_compliance(self, contract: Dict[str, Any]) -> List[str]:
        """Validate DNA compliance section completeness."""
        dna_compliance = contract.get("dna_compliance", {})
        errors = []
        
        # Check required sections exist
        required_sections = ["design_principles_validation", "architecture_compliance"]
        for section in required_sections:
            if section not in dna_compliance:
                errors.append(f"Missing DNA compliance section: {section}")
        
        # Validate design principles
        design_principles = dna_compliance.get("design_principles_validation", {})
        required_principles = [
            "pedagogical_value", "policy_to_practice", "time_respect",
            "holistic_thinking", "professional_tone"
        ]
        
        for principle in required_principles:
            if principle not in design_principles:
                errors.append(f"Missing design principle validation: {principle}")
        
        # Validate architecture compliance
        architecture = dna_compliance.get("architecture_compliance", {})
        required_architecture = [
            "api_first", "stateless_backend", 
            "separation_of_concerns", "simplicity_first"
        ]
        
        for arch_principle in required_architecture:
            if arch_principle not in architecture:
                errors.append(f"Missing architecture principle: {arch_principle}")
        
        return errors
    
    def _validate_agent_sequence(self, source_agent: str, target_agent: str) -> bool:
        """Validate that agent handoff sequence follows defined workflow."""
        valid_sequences = {
            "project_manager": ["game_designer"],
            "game_designer": ["developer"],
            "developer": ["test_engineer"],
            "test_engineer": ["qa_tester"],
            "qa_tester": ["quality_reviewer"],
            "quality_reviewer": ["project_manager"]  # For next iteration
        }
        
        valid_targets = valid_sequences.get(source_agent, [])
        return target_agent in valid_targets
    
    def _validate_file_paths(self, contract: Dict[str, Any]) -> bool:
        """Validate that file paths follow project conventions."""
        story_id = contract.get("story_id", "")
        
        # Check input files reference story_id
        input_files = contract.get("input_requirements", {}).get("required_files", [])
        for file_path in input_files:
            if "{story_id}" in file_path:
                continue  # Template format is valid
            if story_id not in file_path:
                return False  # Must contain story_id for traceability
        
        # Check output files reference story_id
        output_files = contract.get("output_specifications", {}).get("deliverable_files", [])
        for file_path in output_files:
            if "{story_id}" in file_path:
                continue  # Template format is valid
            if story_id not in file_path:
                return False  # Must contain story_id for traceability
        
        return True
    
    def _validate_quality_gates(self, contract: Dict[str, Any]) -> List[str]:
        """Validate quality gates are properly defined."""
        warnings = []
        
        quality_gates = contract.get("quality_gates", [])
        if not quality_gates:
            warnings.append("No quality gates defined - consider adding automated checks")
        
        # Validate known quality gate formats
        for gate in quality_gates:
            if not self._is_valid_quality_gate_format(gate):
                warnings.append(f"Quality gate may not be machine-readable: {gate}")
        
        return warnings
    
    def _is_valid_quality_gate_format(self, gate: str) -> bool:
        """Check if quality gate follows machine-readable format."""
        # Quality gates should be descriptive and specific
        machine_readable_patterns = [
            "test_coverage", "eslint", "typescript", "lighthouse", 
            "api_response_time", "bundle_size", "security_scan"
        ]
        
        return any(pattern in gate.lower() for pattern in machine_readable_patterns)
```

---

## 📄 **DETAILED CONTRACT SPECIFICATIONS**

### **1. Project Manager → Game Designer Contract**

```json
{
  "contract_version": "1.0",
  "contract_type": "feature_to_game_design_and_ux",
  "story_id": "STORY-001-001",
  "source_agent": "project_manager",
  "target_agent": "game_designer",
  
  "input_requirements": {
    "required_files": [
      "docs/stories/story_description_{story_id}.md",
      "docs/analysis/feature_analysis_{story_id}.json"
    ],
    "required_data": {
      "feature_description": "string",
      "acceptance_criteria": ["string"],
      "user_persona": "Anna",
      "time_constraint_minutes": 10,
      "learning_objectives": ["string"],
      "gdd_section_reference": "string",
      "priority_level": "high|medium|low",
      "complexity_assessment": "object"
    },
    "required_validations": [
      "dna_design_principles_alignment_verified",
      "gdd_consistency_checked",
      "technical_feasibility_confirmed"
    ]
  },
  
  "output_specifications": {
    "deliverable_files": [
      "docs/specs/game_design_{story_id}.md",
      "docs/specs/ux_specification_{story_id}.md",
      "docs/specs/component_mapping_{story_id}.json"
    ],
    "deliverable_data": {
      "game_mechanics": "object",
      "ui_components": ["object"],
      "interaction_flows": ["object"],
      "asset_requirements": ["object"]
    },
    "validation_criteria": {
      "design_principles": {
        "pedagogical_value": {"min_score": 4},
        "time_respect": {"max_duration_minutes": 10},
        "professional_tone": {"style_guide_compliance": true}
      },
      "design_quality": {
        "component_library_compliance": {"percentage": 100},
        "accessibility_considerations": {"included": true},
        "responsive_design_specified": {"included": true}
      }
    }
  },
  
  "quality_gates": [
    "component_library_mapping_complete",
    "wireframes_generated_and_validated",
    "game_mechanics_pedagogically_sound",
    "ux_specification_technically_implementable"
  ],
  
  "handoff_criteria": [
    "all_required_components_mapped",
    "interaction_flows_fully_specified",
    "asset_requirements_clearly_defined",
    "developer_implementation_ready"
  ]
}
```

### **2. Game Designer → Developer Contract**

```json
{
  "contract_version": "1.0",
  "contract_type": "design_to_implementation",
  "story_id": "STORY-001-001",
  "source_agent": "game_designer",
  "target_agent": "developer",
  
  "input_requirements": {
    "required_files": [
      "docs/specs/game_design_{story_id}.md",
      "docs/specs/ux_specification_{story_id}.md",
      "docs/specs/component_mapping_{story_id}.json"
    ],
    "required_data": {
      "game_mechanics": "object",
      "ui_components": ["object"],
      "interaction_flows": ["object"],
      "api_endpoints": ["object"],
      "state_management": "object"
    },
    "required_validations": [
      "component_mapping_complete",
      "technical_specifications_clear",
      "architecture_constraints_defined"
    ]
  },
  
  "output_specifications": {
    "deliverable_files": [
      "frontend/components/{story_id}/",
      "backend/endpoints/{story_id}/", 
      "tests/unit/{story_id}/",
      "docs/implementation/{story_id}_implementation.md"
    ],
    "deliverable_data": {
      "component_implementations": ["object"],
      "api_implementations": ["object"],
      "test_suite": "object",
      "deployment_instructions": "object"
    },
    "validation_criteria": {
      "code_quality": {
        "typescript_errors": {"max": 0},
        "eslint_violations": {"max": 0},
        "test_coverage_percent": {"min": 100}
      },
      "performance": {
        "lighthouse_score": {"min": 90},
        "api_response_time_ms": {"max": 200},
        "bundle_size_increase_kb": {"max": 50}
      },
      "architecture": {
        "api_first_compliance": true,
        "stateless_backend_maintained": true,
        "component_library_usage": {"percentage": 100}
      }
    }
  },
  
  "quality_gates": [
    "typescript_compilation_success_zero_errors",
    "eslint_standards_compliance_verified", 
    "unit_tests_100_percent_coverage_achieved",
    "api_endpoints_respond_correctly",
    "component_integration_working"
  ],
  
  "handoff_criteria": [
    "all_game_mechanics_functionally_complete",
    "ui_matches_wireframes_and_specifications",
    "api_endpoints_tested_and_documented",
    "error_handling_implemented_comprehensively",
    "code_ready_for_qa_testing"
  ]
}
```

### **3. Developer → Test Engineer Contract**

```json
{
  "contract_version": "1.0",
  "contract_type": "implementation_to_testing",
  "story_id": "STORY-001-001", 
  "source_agent": "developer",
  "target_agent": "test_engineer",
  
  "validation_criteria": {
    "test_quality": {
      "integration_test_coverage": {"min": 95},
      "end_to_end_test_coverage": {"min": 90},
      "performance_test_included": true
    },
    "automation": {
      "ci_cd_integration": true,
      "automated_regression_tests": true,
      "load_testing_configured": true
    }
  },
  
  "quality_gates": [
    "all_integration_tests_passing",
    "performance_benchmarks_within_targets",
    "security_vulnerability_scan_clean",
    "automated_test_suite_configured"
  ]
}
```

---

## 🗂️ **ENHANCED MODULAR REPOSITORY STRUCTURE**

### **Recommended File Organization**

```
/
├── modules/
│   ├── agents/
│   │   ├── project_manager/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py               # Agent core logic
│   │   │   ├── contracts/             # Input/output models
│   │   │   │   ├── input_models.py
│   │   │   │   └── output_models.py
│   │   │   ├── tools/                 # Agent-specific tools
│   │   │   │   ├── __init__.py
│   │   │   │   ├── github_integration.py
│   │   │   │   └── story_analyzer.py
│   │   │   └── tests/                 # Agent-specific tests
│   │   │       ├── test_agent.py
│   │   │       └── test_tools.py
│   │   │
│   │   ├── game_designer/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── contracts/
│   │   │   ├── tools/
│   │   │   │   ├── component_mapper.py
│   │   │   │   ├── wireframe_generator.py
│   │   │   │   └── ux_validator.py
│   │   │   └── tests/
│   │   │
│   │   ├── developer/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── contracts/
│   │   │   ├── tools/
│   │   │   │   ├── code_generator.py
│   │   │   │   ├── api_builder.py
│   │   │   │   └── git_operations.py
│   │   │   └── tests/
│   │   │
│   │   ├── test_engineer/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── contracts/
│   │   │   ├── tools/
│   │   │   │   ├── test_generator.py
│   │   │   │   ├── coverage_analyzer.py
│   │   │   │   └── performance_tester.py
│   │   │   └── tests/
│   │   │
│   │   ├── qa_tester/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py
│   │   │   ├── contracts/
│   │   │   ├── tools/
│   │   │   │   ├── persona_simulator.py
│   │   │   │   ├── accessibility_checker.py
│   │   │   │   └── user_flow_validator.py
│   │   │   └── tests/
│   │   │
│   │   └── quality_reviewer/
│   │       ├── __init__.py
│   │       ├── agent.py
│   │       ├── contracts/
│   │       ├── tools/
│   │       │   ├── quality_scorer.py
│   │       │   ├── deployment_validator.py
│   │       │   └── final_approver.py
│   │       └── tests/
│   │
│   └── shared/                        # System-wide shared components
│       ├── __init__.py
│       ├── base_agent.py              # Base class for all agents
│       ├── contract_validator.py      # Contract validation framework
│       ├── dna_validator.py           # DNA compliance checker
│       ├── event_bus.py               # Agent communication system
│       ├── state_manager.py           # Work state persistence
│       └── exceptions.py              # System-wide exception types
│
├── docs/
│   ├── dna/                          # Project DNA documents
│   ├── contracts/                    # Contract schemas and examples
│   ├── setup_guides/                 # Development environment setup
│   └── adaptation_guides/            # How to adapt for other projects
│
├── config/
│   ├── settings.py                   # Main configuration
│   ├── agent_configs/               # Agent-specific configurations
│   └── environments/                # Environment-specific settings
│
├── workflows/
│   ├── github_integration.py        # GitHub workflow automation
│   ├── deployment_pipeline.py       # Deployment automation
│   └── monitoring.py                # System monitoring
│
└── tests/
    ├── integration/                  # Cross-agent integration tests
    │   ├── test_full_lifecycle.py
    │   └── test_contract_compliance.py
    ├── contract_validation/          # Contract system tests
    └── dna_compliance/               # DNA validation tests
```

### **Modularity Decision Rules**

**When determining code placement:**

1. **Single Agent Usage:** Place in agent's own `tools/` directory
2. **Multiple Agent Usage (but not all):** Duplicate code in each relevant agent's `tools/` directory
3. **System-wide Core Functionality:** Place in `modules/shared/`

**Examples:**
- `github_integration.py` → Only Project Manager uses → `modules/agents/project_manager/tools/`
- `component_mapper.py` → Only Game Designer uses → `modules/agents/game_designer/tools/`
- `contract_validator.py` → All agents use → `modules/shared/`
- `base_agent.py` → All agents inherit from → `modules/shared/`

---

## 📊 **STATE MANAGEMENT & RECOVERY**

### **State Management Implementation**

```python
class StateManager:
    """
    Manages agent work state for recovery and monitoring.
    
    PURPOSE:
    Preserves work progress and enables automatic recovery if agents
    crash or are interrupted during task execution.
    
    ADAPTATION GUIDE:
    🔧 To adapt for your project:
    1. Update state_storage_path for your environment
    2. Modify backup_interval for your performance needs
    3. Add custom state validation for your agent types
    """
    
    def __init__(self, state_storage_path: str = "data/agent_states/"):
        self.storage_path = Path(state_storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.active_states = {}
    
    def save_agent_state(self, agent_id: str, story_id: str, state_data: Dict[str, Any]) -> None:
        """Save current agent work state."""
        state_record = {
            "agent_id": agent_id,
            "story_id": story_id,
            "state_data": state_data,
            "timestamp": datetime.now().isoformat(),
            "checkpoint_type": "progress_save"
        }
        
        state_file = self.storage_path / f"{agent_id}_{story_id}_state.json"
        with open(state_file, 'w') as f:
            json.dump(state_record, f, indent=2)
    
    def load_agent_state(self, agent_id: str, story_id: str) -> Optional[Dict[str, Any]]:
        """Load saved agent work state."""
        state_file = self.storage_path / f"{agent_id}_{story_id}_state.json"
        
        if not state_file.exists():
            return None
        
        try:
            with open(state_file, 'r') as f:
                state_record = json.load(f)
            return state_record.get("state_data")
        except Exception as e:
            print(f"Error loading state for {agent_id}/{story_id}: {e}")
            return None
    
    def recover_interrupted_work(self, agent_id: str, story_id: str) -> bool:
        """Attempt to recover from interrupted work state."""
        saved_state = self.load_agent_state(agent_id, story_id)
        
        if not saved_state:
            return False
        
        # Validate state is recent enough to be useful
        timestamp = saved_state.get("timestamp")
        if self._is_state_too_old(timestamp):
            return False
        
        # Restore agent to saved state
        return self._restore_agent_state(agent_id, saved_state)
    
    def _is_state_too_old(self, timestamp: str, max_age_hours: int = 24) -> bool:
        """Check if saved state is too old to be useful."""
        try:
            saved_time = datetime.fromisoformat(timestamp)
            age = datetime.now() - saved_time
            return age.total_seconds() > (max_age_hours * 3600)
        except:
            return True  # If we can't parse timestamp, consider it too old
    
    def _restore_agent_state(self, agent_id: str, state_data: Dict[str, Any]) -> bool:
        """Restore agent to saved state."""
        # Implementation would depend on specific agent architecture
        # This is a placeholder for the actual restoration logic
        try:
            # Restore agent's internal state
            # Validate state is still valid
            # Resume work from checkpoint
            return True
        except Exception as e:
            print(f"Failed to restore state for {agent_id}: {e}")
            return False
```

### **Recovery Scenarios**

**Agent Crash Recovery:**
1. Detect agent failure
2. Load last saved state
3. Validate state integrity  
4. Resume from last checkpoint
5. Notify other agents of recovery

**System Restart Recovery:**
1. Scan for incomplete work states
2. Prioritize by story importance
3. Restore agents in dependency order
4. Resume work automatically

---

## 🏗️ **TECHNICAL IMPLEMENTATION REQUIREMENTS**

### **Technology Stack**

**Frontend:**
- React with TypeScript
- Tailwind CSS for styling
- Shadcn/UI component library
- Kenney.UI game assets

**Backend:**
- FastAPI (Python)
- SQLite (MVP) → PostgreSQL (Production)
- Stateless design (no server-side sessions)

**Deployment:**
- Netlify for frontend hosting
- Netlify Functions for backend
- GitHub Actions for CI/CD

### **Architecture Principles (Non-Negotiable)**

1. **API-First:** All communication via REST APIs, no direct database calls from frontend
2. **Stateless Backend:** All state passed from client, no server-side sessions
3. **Separation of Concerns:** Frontend and backend remain completely separate
4. **Simplicity First:** Choose simplest solution that works, optimize only when needed

---

## 🔄 **WORKFLOW IMPLEMENTATION**

### **Feature Development Lifecycle**

1. **GitHub Issue Created** by project owner using feature request template
2. **Project Manager analyzes** issue against DNA principles and creates story breakdown
3. **Stories delegated** to appropriate agents via standardized contracts
4. **Each agent processes** their assigned work according to contract specifications
5. **Quality gates enforced** automatically at each handoff
6. **Feature branch created** in product repository with implemented code
7. **Project owner approval** required before merge to main branch

### **Dual Repository Workflow**

**AI-Team Repository (Development):**
- Agent code and configurations
- Contract definitions and validation
- Team coordination workflows
- DNA documentation

**Product Repository (Delivery):**
- Feature branch creation by agents
- Game implementation code
- Production deployment pipeline
- Project owner approval workflow

### **Branch Management**

**Naming Convention:**
```
feature/STORY-{story_id}-{short-description}
Example: feature/STORY-001-user-registration
```

**Approval Process:**
1. Agent creates feature branch in product repo
2. Agent implements code according to contract
3. All quality gates pass automatically
4. Agent creates PR for project owner review
5. Project owner tests in preview environment
6. Project owner approves/rejects via GitHub interface
7. Approved features merged to main branch

---

## 👥 **AGENT ROLES AND RESPONSIBILITIES**

### **1. Project Manager**
- **Function:** Team orchestration and story breakdown
- **Input:** GitHub feature requests from project owner
- **Output:** DNA-validated story breakdowns with agent assignments
- **Key Responsibility:** Ensures all work aligns with project DNA
- **Tools:** GitHub integration, story analyzer, DNA validator

### **2. Game Designer**
- **Function:** Game mechanics design + UX specification using component libraries
- **Input:** DNA-validated stories from Project Manager
- **Output:** Game design specifications + UX specifications with Shadcn/UI and Kenney.UI component mappings
- **Key Responsibility:** Designs pedagogical game mechanics AND translates them into implementable UX specs
- **Tools:** Component mapper, wireframe generator, UX validator

### **3. Developer**
- **Function:** Full-stack implementation (React + FastAPI)
- **Input:** UX specifications with component mappings
- **Output:** Working code in feature branch (in product repository)
- **Key Responsibility:** Implements code following architecture constraints
- **Tools:** Code generator, API builder, Git operations

### **4. Test Engineer**
- **Function:** Automated testing and performance validation
- **Input:** Working code from Developer
- **Output:** Complete test suite with performance benchmarks
- **Key Responsibility:** Ensures code quality and performance standards
- **Tools:** Test generator, coverage analyzer, performance tester

### **5. QA Tester**
- **Function:** User experience validation and DNA compliance testing
- **Input:** Tested code from Test Engineer
- **Output:** UX validation report with Anna persona testing results
- **Key Responsibility:** Validates user experience meets design goals
- **Tools:** Persona simulator, accessibility checker, user flow validator

### **6. Quality Reviewer**
- **Function:** Final quality scoring and production readiness validation
- **Input:** QA-validated code and reports
- **Output:** Production deployment approval with quality metrics
- **Key Responsibility:** Final gate before production deployment
- **Tools:** Quality scorer, deployment validator, final approver

---

## 🛠️ **IMPLEMENTATION STEPS**

### **Phase 1: Foundation (Week 1)**

#### **Step 1: Create Contract Framework**
```powershell
# PowerShell commands for Windows setup
mkdir modules\shared
New-Item -ItemType File -Path "modules\shared\__init__.py"
New-Item -ItemType File -Path "modules\shared\base_agent.py"
New-Item -ItemType File -Path "modules\shared\contract_validator.py"
New-Item -ItemType File -Path "modules\shared\dna_validator.py"
New-Item -ItemType File -Path "modules\shared\state_manager.py"
```

#### **Step 2: Implement Base Agent Class**
```python
# modules/shared/base_agent.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .contract_validator import ContractValidator
from .dna_validator import DNAValidator
from .state_manager import StateManager

class BaseAgent(ABC):
    """
    Base class for all AI agents in the system.
    
    PURPOSE:
    Provides common functionality and enforces contract compliance
    for all agents in the team.
    
    ADAPTATION GUIDE:
    🔧 To adapt for your project:
    1. Update agent_types list for your specific agents
    2. Modify validation rules for your quality standards
    3. Adjust state management for your persistence needs
    """
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.contract_validator = ContractValidator()
        self.dna_validator = DNAValidator()
        self.state_manager = StateManager()
        self.current_work_state = {}
    
    @abstractmethod
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process work according to input contract and return output contract.
        
        This method must be implemented by each specific agent.
        """
        pass
    
    async def execute_work(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method with full validation and state management.
        """
        try:
            # 1. Validate input contract
            validation_result = self.contract_validator.validate_contract(input_contract)
            if not validation_result["is_valid"]:
                raise ContractValidationError(validation_result["errors"])
            
            # 2. Save initial state
            story_id = input_contract.get("story_id")
            self.state_manager.save_agent_state(
                self.agent_id, 
                story_id, 
                {"status": "started", "input_contract": input_contract}
            )
            
            # 3. Process the work
            output_contract = await self.process_contract(input_contract)
            
            # 4. Validate output against DNA
            if not self.dna_validator.validate_output(output_contract, self.agent_type):
                raise DNAComplianceError("Output violates project DNA principles")
            
            # 5. Save completion state
            self.state_manager.save_agent_state(
                self.agent_id,
                story_id,
                {"status": "completed", "output_contract": output_contract}
            )
            
            return output_contract
            
        except Exception as e:
            # Save error state for debugging
            self.state_manager.save_agent_state(
                self.agent_id,
                story_id,
                {"status": "error", "error": str(e)}
            )
            raise
    
    def validate_quality_gates(self, deliverables: Dict[str, Any], quality_gates: list) -> bool:
        """Validate that all quality gates pass for deliverables."""
        for gate in quality_gates:
            if not self._check_quality_gate(gate, deliverables):
                return False
        return True
    
    @abstractmethod
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """Check specific quality gate - implemented by each agent."""
        pass

class ContractValidationError(Exception):
    """Raised when contract validation fails."""
    pass

class DNAComplianceError(Exception):
    """Raised when output violates DNA principles."""
    pass
```

#### **Step 3: Create Agent Directory Structure**
```powershell
# Create all agent directories
$agents = @("project_manager", "game_designer", "developer", "test_engineer", "qa_tester", "quality_reviewer")

foreach ($agent in $agents) {
    mkdir "modules\agents\$agent"
    mkdir "modules\agents\$agent\contracts"
    mkdir "modules\agents\$agent\tools"
    mkdir "modules\agents\$agent\tests"
    
    New-Item -ItemType File -Path "modules\agents\$agent\__init__.py"
    New-Item -ItemType File -Path "modules\agents\$agent\agent.py"
    New-Item -ItemType File -Path "modules\agents\$agent\contracts\__init__.py"
    New-Item -ItemType File -Path "modules\agents\$agent\contracts\input_models.py"
    New-Item -ItemType File -Path "modules\agents\$agent\contracts\output_models.py"
    New-Item -ItemType File -Path "modules\agents\$agent\tools\__init__.py"
    New-Item -ItemType File -Path "modules\agents\$agent\tests\__init__.py"
}
```

### **Phase 2: Core Agents (Week 2-3)**

#### **Step 1: Implement Project Manager Agent**
```python
# modules/agents/project_manager/agent.py
from typing import Dict, Any
from ...shared.base_agent import BaseAgent
from .tools.github_integration import GitHubIntegration
from .tools.story_analyzer import StoryAnalyzer

class ProjectManagerAgent(BaseAgent):
    """
    Project Manager agent for story breakdown and team coordination.
    
    PURPOSE:
    Analyzes GitHub feature requests and creates DNA-compliant
    story breakdowns for the development team.
    """
    
    def __init__(self):
        super().__init__("pm-001", "project_manager")
        self.github_integration = GitHubIntegration()
        self.story_analyzer = StoryAnalyzer()
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process GitHub feature request into story breakdown.
        """
        # 1. Extract feature requirements
        feature_data = input_contract.get("input_requirements", {}).get("required_data", {})
        
        # 2. Analyze against DNA principles
        analysis_result = await self.story_analyzer.analyze_feature(
            feature_data,
            self.dna_validator
        )
        
        # 3. Create story breakdown
        story_breakdown = await self.story_analyzer.create_story_breakdown(
            analysis_result
        )
        
        # 4. Generate output contract for Game Designer
        output_contract = {
            "contract_version": "1.0",
            "story_id": input_contract.get("story_id"),
            "source_agent": "project_manager", 
            "target_agent": "game_designer",
            "dna_compliance": analysis_result["dna_compliance"],
            "input_requirements": {
                "required_files": [
                    f"docs/stories/story_description_{input_contract.get('story_id')}.md",
                    f"docs/analysis/feature_analysis_{input_contract.get('story_id')}.json"
                ],
                "required_data": story_breakdown,
                "required_validations": [
                    "dna_design_principles_alignment_verified",
                    "gdd_consistency_checked",
                    "technical_feasibility_confirmed"
                ]
            },
            "output_specifications": {
                "deliverable_files": [
                    f"docs/specs/game_design_{input_contract.get('story_id')}.md",
                    f"docs/specs/ux_specification_{input_contract.get('story_id')}.md"
                ],
                "deliverable_data": {
                    "game_mechanics": "object",
                    "ui_components": ["object"],
                    "interaction_flows": ["object"]
                },
                "validation_criteria": {
                    "design_principles": {
                        "pedagogical_value": {"min_score": 4},
                        "time_respect": {"max_duration_minutes": 10}
                    }
                }
            },
            "quality_gates": [
                "component_library_mapping_complete",
                "wireframes_generated_and_validated",
                "game_mechanics_pedagogically_sound"
            ],
            "handoff_criteria": [
                "all_required_components_mapped",
                "interaction_flows_fully_specified",
                "developer_implementation_ready"
            ]
        }
        
        return output_contract
    
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """Check Project Manager specific quality gates."""
        quality_checks = {
            "dna_compliance_verified": self._check_dna_compliance,
            "story_breakdown_complete": self._check_story_breakdown,
            "acceptance_criteria_clear": self._check_acceptance_criteria
        }
        
        checker = quality_checks.get(gate)
        if checker:
            return checker(deliverables)
        
        return True  # Default pass for unknown gates
    
    def _check_dna_compliance(self, deliverables: Dict[str, Any]) -> bool:
        """Verify all deliverables comply with DNA principles."""
        return self.dna_validator.validate_output(deliverables, "project_manager")
    
    def _check_story_breakdown(self, deliverables: Dict[str, Any]) -> bool:
        """Verify story breakdown is complete and actionable."""
        required_fields = [
            "feature_description", "acceptance_criteria", 
            "user_persona", "learning_objectives"
        ]
        
        story_data = deliverables.get("story_breakdown", {})
        return all(field in story_data for field in required_fields)
    
    def _check_acceptance_criteria(self, deliverables: Dict[str, Any]) -> bool:
        """Verify acceptance criteria are clear and testable."""
        criteria = deliverables.get("story_breakdown", {}).get("acceptance_criteria", [])
        return len(criteria) > 0 and all(len(criterion) > 10 for criterion in criteria)
```

#### **Step 2: Create Project Manager Tools**
```python
# modules/agents/project_manager/tools/github_integration.py
import requests
from typing import Dict, Any, List
from pathlib import Path

class GitHubIntegration:
    """
    GitHub integration tools for Project Manager.
    
    PURPOSE:
    Handles GitHub issue monitoring, feature request parsing,
    and project status updates.
    
    ADAPTATION GUIDE:
    🔧 To adapt for your project:
    1. Update GITHUB_REPO for your repository
    2. Modify issue_template_fields for your issue format
    3. Adjust status_labels for your workflow
    """
    
    def __init__(self, github_token: str = None):
        self.github_token = github_token or self._get_github_token()
        self.base_url = "https://api.github.com"
        self.repo_owner = "jhonnyo88"  # 🔧 ADAPT: Your GitHub username
        self.repo_name = "multi-agent-setup"  # 🔧 ADAPT: Your repo name
    
    def _get_github_token(self) -> str:
        """Get GitHub token from environment or config."""
        import os
        return os.getenv("GITHUB_TOKEN", "")
    
    async def fetch_new_feature_requests(self) -> List[Dict[str, Any]]:
        """
        Fetch new feature requests from GitHub issues.
        
        Returns list of feature request data.
        """
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        params = {
            "labels": "feature-request",  # 🔧 ADAPT: Your feature label
            "state": "open",
            "sort": "created",
            "direction": "desc"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            issues = response.json()
            return [self._parse_feature_request(issue) for issue in issues]
        
        except requests.RequestException as e:
            print(f"Error fetching GitHub issues: {e}")
            return []
    
    def _parse_feature_request(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse GitHub issue into standardized feature request format.
        """
        return {
            "issue_id": issue["number"],
            "title": issue["title"],
            "description": issue["body"],
            "labels": [label["name"] for label in issue["labels"]],
            "created_at": issue["created_at"],
            "priority": self._extract_priority(issue),
            "acceptance_criteria": self._extract_acceptance_criteria(issue["body"]),
            "user_persona": "Anna",  # Default for DigiNativa
            "github_url": issue["html_url"]
        }
    
    def _extract_priority(self, issue: Dict[str, Any]) -> str:
        """Extract priority from issue labels."""
        priority_labels = {
            "priority-high": "high",
            "priority-medium": "medium", 
            "priority-low": "low"
        }
        
        for label in issue["labels"]:
            if label["name"] in priority_labels:
                return priority_labels[label["name"]]
        
        return "medium"  # Default priority
    
    def _extract_acceptance_criteria(self, issue_body: str) -> List[str]:
        """
        Extract acceptance criteria from issue body.
        
        Looks for sections like:
        ## Acceptance Criteria
        - [ ] Criterion 1
        - [ ] Criterion 2
        """
        import re
        
        # Find acceptance criteria section
        criteria_pattern = r"##\s*Acceptance\s*Criteria\s*\n(.*?)(?=\n##|\n$|$)"
        match = re.search(criteria_pattern, issue_body, re.IGNORECASE | re.DOTALL)
        
        if not match:
            return []
        
        criteria_text = match.group(1)
        
        # Extract individual criteria (lines starting with - [ ])
        criteria_lines = re.findall(r"-\s*\[\s*\]\s*(.+)", criteria_text)
        
        return [criterion.strip() for criterion in criteria_lines if criterion.strip()]
    
    async def update_issue_status(self, issue_id: int, status: str, comment: str = None) -> bool:
        """
        Update GitHub issue with current processing status.
        """
        if comment:
            await self._add_issue_comment(issue_id, comment)
        
        # Add status label
        await self._add_issue_label(issue_id, f"status-{status}")
        
        return True
    
    async def _add_issue_comment(self, issue_id: int, comment: str) -> bool:
        """Add comment to GitHub issue."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_id}/comments"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {"body": comment}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error adding comment to issue {issue_id}: {e}")
            return False
    
    async def _add_issue_label(self, issue_id: int, label: str) -> bool:
        """Add label to GitHub issue."""
        url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_id}/labels"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {"labels": [label]}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Error adding label to issue {issue_id}: {e}")
            return False
```

### **Phase 3: Quality Assurance Agents (Week 4)**

#### **Step 1: Implement Test Engineer**
```python
# modules/agents/test_engineer/agent.py
from typing import Dict, Any
from ...shared.base_agent import BaseAgent
from .tools.test_generator import TestGenerator
from .tools.coverage_analyzer import CoverageAnalyzer
from .tools.performance_tester import PerformanceTester

class TestEngineerAgent(BaseAgent):
    """
    Test Engineer agent for automated testing and performance validation.
    
    PURPOSE:
    Generates comprehensive test suites and validates performance
    requirements for all implemented features.
    """
    
    def __init__(self):
        super().__init__("te-001", "test_engineer")
        self.test_generator = TestGenerator()
        self.coverage_analyzer = CoverageAnalyzer()
        self.performance_tester = PerformanceTester()
    
    async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive test suite for implemented code.
        """
        # 1. Extract implementation details
        implementation_data = input_contract.get("input_requirements", {}).get("required_data", {})
        
        # 2. Generate unit tests
        unit_tests = await self.test_generator.generate_unit_tests(
            implementation_data.get("component_implementations", [])
        )
        
        # 3. Generate integration tests
        integration_tests = await self.test_generator.generate_integration_tests(
            implementation_data.get("api_implementations", [])
        )
        
        # 4. Generate end-to-end tests
        e2e_tests = await self.test_generator.generate_e2e_tests(
            implementation_data.get("user_flows", [])
        )
        
        # 5. Run performance tests
        performance_results = await self.performance_tester.run_performance_tests(
            implementation_data.get("api_implementations", [])
        )
        
        # 6. Analyze test coverage
        coverage_report = await self.coverage_analyzer.analyze_coverage(
            unit_tests + integration_tests
        )
        
        # 7. Generate output contract for QA Tester
        output_contract = {
            "contract_version": "1.0",
            "story_id": input_contract.get("story_id"),
            "source_agent": "test_engineer",
            "target_agent": "qa_tester",
            "dna_compliance": input_contract.get("dna_compliance"),
            "input_requirements": {
                "required_files": [
                    f"tests/unit/{input_contract.get('story_id')}/",
                    f"tests/integration/{input_contract.get('story_id')}/",
                    f"tests/e2e/{input_contract.get('story_id')}/",
                    f"docs/test_reports/{input_contract.get('story_id')}_coverage.html"
                ],
                "required_data": {
                    "test_suite": {
                        "unit_tests": unit_tests,
                        "integration_tests": integration_tests,
                        "e2e_tests": e2e_tests
                    },
                    "performance_results": performance_results,
                    "coverage_report": coverage_report
                },
                "required_validations": [
                    "all_tests_passing",
                    "coverage_above_threshold",
                    "performance_requirements_met"
                ]
            },
            "output_specifications": {
                "deliverable_files": [
                    f"docs/qa_reports/{input_contract.get('story_id')}_ux_validation.md",
                    f"docs/qa_reports/{input_contract.get('story_id')}_accessibility.json"
                ],
                "deliverable_data": {
                    "ux_validation_results": "object",
                    "accessibility_report": "object",
                    "persona_testing_results": "object"
                },
                "validation_criteria": {
                    "user_experience": {
                        "anna_persona_satisfaction": {"min_score": 4},
                        "task_completion_rate": {"min_percentage": 95},
                        "time_to_complete": {"max_minutes": 10}
                    },
                    "accessibility": {
                        "wcag_compliance_level": "AA",
                        "screen_reader_compatibility": true,
                        "keyboard_navigation": true
                    }
                }
            },
            "quality_gates": [
                "all_test_suites_passing_100_percent",
                "code_coverage_minimum_threshold_met",
                "performance_benchmarks_within_targets",
                "security_vulnerability_scan_clean"
            ],
            "handoff_criteria": [
                "comprehensive_test_coverage_achieved",
                "all_performance_requirements_validated",
                "automated_test_pipeline_configured",
                "quality_metrics_documented"
            ]
        }
        
        return output_contract
    
    def _check_quality_gate(self, gate: str, deliverables: Dict[str, Any]) -> bool:
        """Check Test Engineer specific quality gates."""
        quality_checks = {
            "all_test_suites_passing_100_percent": self._check_all_tests_passing,
            "code_coverage_minimum_threshold_met": self._check_coverage_threshold,
            "performance_benchmarks_within_targets": self._check_performance_targets,
            "security_vulnerability_scan_clean": self._check_security_scan
        }
        
        checker = quality_checks.get(gate)
        if checker:
            return checker(deliverables)
        
        return True
    
    def _check_all_tests_passing(self, deliverables: Dict[str, Any]) -> bool:
        """Verify all tests are passing."""
        test_results = deliverables.get("test_suite", {})
        
        for test_type in ["unit_tests", "integration_tests", "e2e_tests"]:
            tests = test_results.get(test_type, [])
            for test in tests:
                if not test.get("passing", False):
                    return False
        
        return True
    
    def _check_coverage_threshold(self, deliverables: Dict[str, Any]) -> bool:
        """Verify code coverage meets minimum threshold."""
        coverage_report = deliverables.get("coverage_report", {})
        coverage_percentage = coverage_report.get("total_coverage", 0)
        
        return coverage_percentage >= 100  # DigiNativa requires 100% coverage
    
    def _check_performance_targets(self, deliverables: Dict[str, Any]) -> bool:
        """Verify performance benchmarks are met."""
        performance_results = deliverables.get("performance_results", {})
        
        # Check API response times
        api_response_time = performance_results.get("avg_response_time_ms", 999)
        if api_response_time > 200:
            return False
        
        # Check frontend performance
        lighthouse_score = performance_results.get("lighthouse_score", 0)
        if lighthouse_score < 90:
            return False
        
        return True
    
    def _check_security_scan(self, deliverables: Dict[str, Any]) -> bool:
        """Verify security vulnerability scan is clean."""
        security_report = deliverables.get("security_scan", {})
        vulnerabilities = security_report.get("vulnerabilities", [])
        
        # No high or critical vulnerabilities allowed
        critical_vulns = [v for v in vulnerabilities if v.get("severity") in ["high", "critical"]]
        
        return len(critical_vulns) == 0
```

### **Phase 4: Integration & Deployment (Week 5)**

#### **Step 1: Create End-to-End Integration Test**
```python
# tests/integration/test_full_lifecycle.py
import pytest
import asyncio
from typing import Dict, Any
from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.agents.game_designer.agent import GameDesignerAgent
from modules.agents.developer.agent import DeveloperAgent
from modules.agents.test_engineer.agent import TestEngineerAgent
from modules.agents.qa_tester.agent import QATesterAgent
from modules.agents.quality_reviewer.agent import QualityReviewerAgent

class TestFullLifecycle:
    """
    Integration test for complete feature development lifecycle.
    
    PURPOSE:
    Validates that a feature can flow through all agents successfully
    with proper contract validation and quality gates.
    """
    
    @pytest.mark.asyncio
    async def test_complete_feature_development_flow(self):
        """
        Test complete flow from GitHub issue to deployed feature.
        """
        # 1. Setup test data - simulated GitHub feature request
        initial_feature_request = {
            "contract_version": "1.0",
            "story_id": "STORY-TEST-001",
            "source_agent": "github",
            "target_agent": "project_manager",
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": True,
                    "policy_to_practice": True,
                    "time_respect": True,
                    "holistic_thinking": True,
                    "professional_tone": True
                },
                "architecture_compliance": {
                    "api_first": True,
                    "stateless_backend": True,
                    "separation_of_concerns": True,
                    "simplicity_first": True
                }
            },
            "input_requirements": {
                "required_files": [],
                "required_data": {
                    "feature_description": "Add user registration for DigiNativa game",
                    "acceptance_criteria": [
                        "User can create account with email and password",
                        "User receives confirmation email",
                        "User can log in after registration"
                    ],
                    "user_persona": "Anna",
                    "priority_level": "high"
                },
                "required_validations": []
            },
            "output_specifications": {
                "deliverable_files": [],
                "deliverable_data": {},
                "validation_criteria": {}
            },
            "quality_gates": [],
            "handoff_criteria": []
        }
        
        # 2. Initialize all agents
        agents = {
            "project_manager": ProjectManagerAgent(),
            "game_designer": GameDesignerAgent(),
            "developer": DeveloperAgent(),
            "test_engineer": TestEngineerAgent(),
            "qa_tester": QATesterAgent(),
            "quality_reviewer": QualityReviewerAgent()
        }
        
        # 3. Execute complete workflow
        current_contract = initial_feature_request
        agent_sequence = [
            "project_manager", "game_designer", "developer", 
            "test_engineer", "qa_tester", "quality_reviewer"
        ]
        
        for agent_name in agent_sequence:
            print(f"Processing with {agent_name}