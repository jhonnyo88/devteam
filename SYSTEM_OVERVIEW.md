# DigiNativa AI Team - System Overview

## 🎯 One-Page Mental Model for AI Assistants

### What This System Does
**Transforms GitHub issues into production-ready features using 6 specialized AI agents working in sequence.**

### The Pipeline
```
GitHub Issue → Project Manager → Game Designer → Developer → Test Engineer → QA Tester → Quality Reviewer → Production
```

### Core Concepts (In Order of Importance)

#### 1. **Contracts** (THE FOUNDATION)
- Every agent communication uses JSON contracts
- Contracts define inputs, outputs, and validation criteria
- No agent can talk to another without a valid contract
- Think: "API specifications between microservices"

#### 2. **DNA** (THE DECISION FRAMEWORK)
- 5 Design Principles + 4 Architecture Principles
- Every decision must score >4.0/5.0 on DNA compliance
- DNA prevents agents from drifting apart
- Think: "Constitution that all agents follow"

#### 3. **Modularity** (THE ARCHITECTURE)
- Each agent is completely independent
- Can swap out any agent without affecting others
- Shared code only in `modules/shared/`
- Think: "Microservices, not monolith"

#### 4. **EventBus** (THE COORDINATOR)
- Manages all agent communication
- Handles contract validation
- Provides error recovery
- Think: "Air traffic control for agents"

#### 5. **Dual Repositories** (THE SEPARATION)
- This repo: AI team infrastructure
- Product repo: Actual game code
- Agents create branches in product repo
- Think: "Factory (this) vs Products (game repo)"

### Agent Responsibilities

| Agent | Input | Output | Key Responsibility |
|-------|-------|--------|-------------------|
| **Project Manager** | GitHub Issue | Story Breakdown | Validates against DNA, assigns work |
| **Game Designer** | Story | UX Specification | Creates wireframes, maps components |
| **Developer** | UX Spec | Working Code | Implements React/FastAPI solution |
| **Test Engineer** | Code | Test Suite | Ensures 100% coverage, performance |
| **QA Tester** | Tested Code | UX Validation | Validates Anna persona experience |
| **Quality Reviewer** | QA Report | Approval/Rejection | Final quality gate before production |

### Success Metrics
- **Contract Compliance**: 100% (no exceptions)
- **DNA Score**: >4.0/5.0 (all features)
- **Test Coverage**: 100% (business logic)
- **Performance**: <200ms API, >90 Lighthouse
- **Time**: <4 hours per feature

### Common Patterns

#### Successful Feature Flow:
```python
# 1. PM receives GitHub issue
contract = pm.analyze_issue(github_issue)
contract.validate()  # Must pass

# 2. Each agent processes in sequence
for agent in [game_designer, developer, test_engineer, qa_tester, quality_reviewer]:
    output_contract = agent.process(input_contract)
    output_contract.validate()  # Must pass at each step
    input_contract = output_contract

# 3. Final approval creates PR in product repo
if quality_reviewer.approved:
    create_pull_request(product_repo)
```

#### Error Recovery:
```python
# If any agent fails validation
if not contract.validate():
    # Rollback to previous agent
    return_to_previous_agent(contract.errors)
    # Previous agent must fix and resubmit
```

### Key Files to Understand

1. **`Implementation_rules.md`** - Complete system specification
2. **`modules/shared/contract_validator.py`** - How contracts work
3. **`modules/shared/base_agent.py`** - Agent foundation
4. **`docs/dna/`** - Decision framework

### Mental Checklist
Before implementing anything, ask:
- [ ] Does this maintain contract compatibility?
- [ ] Does this score >4.0 on DNA compliance?
- [ ] Does this keep agents modular?
- [ ] Does this have 100% test coverage?
- [ ] Does this meet performance requirements?

### The Prime Directive
**"Maintain contract integrity and DNA compliance above all else."**

Without these, the autonomous team falls apart.

---

**Read Time**: 5 minutes
**Understanding Level Required**: CRITICAL
**Next Step**: Read `Implementation_rules.md` for complete details