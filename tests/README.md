# DigiNativa AI Team - Tests Directory

This directory contains the core test suites for the DigiNativa AI Team system, organized according to the [TEST_STRATEGY.md](../TEST_STRATEGY.md) document.

## Directory Structure

```
tests/
├── contract_validation/     # Contract system protection tests (CRITICAL)
├── dna_compliance/         # DNA principle validation tests (CRITICAL)
├── integration/           # Agent-to-agent integration tests
└── shared/               # Shared system component tests
```

## Test Categories

### 🛡️ Contract Validation Tests (CRITICAL)
**Location:** `tests/contract_validation/`

These tests protect the contract system that enables modular architecture. They are the most critical tests and MUST pass before any commits.

**Contains:**
- `test_contract_validator.py` - Core contract validation logic
- `test_contract_schemas.py` - JSON schema validation for all contracts
- `test_contract_pipeline.py` - End-to-end contract pipeline tests
- `test_contract_backwards_compatibility.py` - Ensures contract compatibility

**Run with:** `make test-contracts`

### 🧬 DNA Compliance Tests (CRITICAL)  
**Location:** `tests/dna_compliance/`

These tests ensure all features comply with DigiNativa's DNA principles - both design and architecture principles.

**Contains:**
- `test_dna_validator.py` - Core DNA validation logic
- `test_design_principles.py` - Validates 5 design principles
- `test_architecture_compliance.py` - Validates 4 architecture principles

**Run with:** `make test-dna`

### 🔗 Integration Tests
**Location:** `tests/integration/`

These tests verify that agents work together correctly through the contract system.

**Contains:**
- `test_full_lifecycle.py` - Complete feature development flow
- `test_agent_communication.py` - Agent-to-agent communication
- `test_quality_gates.py` - Quality gate validation

**Run with:** `make test-integration`

### ⚙️ Shared System Tests
**Location:** `tests/shared/`

These tests validate core shared components used across all agents.

**Contains:**
- `test_base_agent.py` - Base agent class functionality
- `test_event_bus.py` - Agent communication system
- `test_state_manager.py` - State management system
- `test_contract_validator.py` - Contract validation logic

**Run with:** `pytest tests/shared/ -v`

## Test Execution Order

1. **Smoke Tests** (< 10 seconds): `make test-smoke`
2. **Contract Tests** (< 5 minutes): `make test-contracts`
3. **DNA Tests** (< 2 minutes): `make test-dna`
4. **Integration Tests** (< 10 minutes): `make test-integration`

## Critical Test Requirements

### Before Any Development:
```bash
make test-critical  # Runs smoke + contracts + DNA tests
```

### Before Any Commit:
```bash
make test-critical  # Must pass 100%
```

### Before Release:
```bash
make test-all  # Full test suite
```

## Quality Standards

- **Contract Tests:** 100% coverage (MANDATORY)
- **DNA Tests:** 100% coverage (MANDATORY)
- **Integration Tests:** 85% coverage minimum
- **Performance:** All critical tests < 2 minutes

## See Also

- [TEST_STRATEGY.md](../TEST_STRATEGY.md) - Complete test strategy document
- [Implementation_rules.md](../Implementation_rules.md) - Contract specifications
- [Makefile](../Makefile) - Test automation commands

---

⚠️ **IMPORTANT:** Contract and DNA tests are CRITICAL. Never commit code that breaks these tests, as they protect the core architecture that enables DigiNativa's modular AI team system.