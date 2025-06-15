# Contract Validation Tests

This directory contains tests that protect the contract system - the foundation of DigiNativa's modular AI team architecture.

## ⚠️ CRITICAL IMPORTANCE

These tests are **SACRED** and protect the contract system that enables:
- Modular agent development
- Independent agent testing
- Scalable team architecture
- Agent handoff protocols

**NEVER** break these tests. They must pass 100% before any commit.

## Test Files

### `test_contract_validator.py`
Tests the core ContractValidator class that validates all agent contracts.

**Tests:**
- Contract schema validation
- Required field validation
- DNA compliance structure validation
- Contract version compatibility

### `test_contract_schemas.py`
Validates JSON schemas for all agent contracts.

**Tests:**
- Schema structure validation
- Field type validation
- Required vs optional fields
- Cross-agent contract compatibility

### `test_contract_pipeline.py`
Tests the complete contract pipeline between agents.

**Tests:**
- Agent sequence validation (GitHub → PM → GD → Dev → TE → QA → QR)
- Contract transformation validation
- Pipeline performance testing
- Memory usage validation

### `test_contract_backwards_compatibility.py`
Ensures contract changes maintain backwards compatibility.

**Tests:**
- Schema version compatibility
- Legacy contract support
- Migration path validation
- Breaking change detection

## Running Contract Tests

### Quick Validation (< 10 seconds):
```bash
make test-smoke
```

### Complete Contract Tests (< 5 minutes):
```bash
make test-contracts
```

### Individual Test Files:
```bash
# Core validator tests
pytest tests/contract_validation/test_contract_validator.py -v

# Schema validation tests  
pytest tests/contract_validation/test_contract_schemas.py -v

# Pipeline tests
pytest tests/contract_validation/test_contract_pipeline.py -v

# Backwards compatibility tests
pytest tests/contract_validation/test_contract_backwards_compatibility.py -v
```

## Quality Requirements

- **Coverage:** 100% (MANDATORY)
- **Performance:** < 100ms per contract validation
- **Reliability:** 0% failure rate allowed

## Contract Protection Rules

1. **NEVER** modify contract schemas without updating all dependent tests
2. **ALWAYS** run contract tests before any commit
3. **ENSURE** backwards compatibility with existing contracts
4. **VALIDATE** that contract changes don't break agent handoffs
5. **PROTECT** the contract system at all costs

## DNA Compliance Validation

All contracts must validate DNA compliance structure:

```json
{
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
  }
}
```

## Error Handling

Contract validation failures should:
- Provide clear error messages
- Identify specific validation failures
- Suggest remediation steps
- Prevent invalid contracts from propagating

## See Also

- [Implementation_rules.md](../../Implementation_rules.md) - Contract specifications
- [TEST_STRATEGY.md](../../TEST_STRATEGY.md) - Overall test strategy
- [modules/shared/contract_validator.py](../../modules/shared/contract_validator.py) - Contract validator implementation

---

🛡️ **Remember:** These tests are the guardians of DigiNativa's modular architecture. Treat them with the respect they deserve.