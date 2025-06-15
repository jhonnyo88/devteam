# DNA Compliance Tests

This directory contains tests that ensure all DigiNativa AI Team features comply with the project's DNA principles.

## 🧬 DNA PRINCIPLES

DigiNativa's DNA consists of **9 core principles** that define the project's identity:

### Design Principles (5)
1. **pedagogical_value** - Clear learning objectives and educational value
2. **policy_to_practice** - Direct connection between policy and practical application
3. **time_respect** - Respects user time (≤10 minutes per learning session)
4. **holistic_thinking** - Comprehensive approach to problem-solving
5. **professional_tone** - Maintains professional municipal communication standards

### Architecture Principles (4)
1. **api_first** - API-first design approach
2. **stateless_backend** - Backend services are stateless
3. **separation_of_concerns** - Clear separation between components
4. **simplicity_first** - Simple solutions preferred over complex ones

## Test Files

### `test_dna_validator.py` ⚠️ NEEDS IMPLEMENTATION
Core DNA validation logic testing.

**Should Test:**
- DNA principle validation framework
- Compliance scoring algorithms
- Violation detection and reporting
- Integration with contract system

### `test_design_principles.py` ⚠️ NEEDS IMPLEMENTATION
Tests validation of the 5 design principles.

**Should Test:**
- Pedagogical value assessment
- Policy-to-practice connection validation
- Time constraint compliance (≤10 minutes)
- Holistic thinking evaluation
- Professional tone analysis

### `test_architecture_compliance.py`
Tests validation of the 4 architecture principles.

**Tests:**
- API-first design validation
- Stateless backend verification
- Separation of concerns checking
- Simplicity-first principle adherence

## Running DNA Tests

### All DNA Tests:
```bash
make test-dna
```

### Individual Test Files:
```bash
# Core DNA validator
pytest tests/dna_compliance/test_dna_validator.py -v

# Design principles validation
pytest tests/dna_compliance/test_design_principles.py -v

# Architecture compliance validation  
pytest tests/dna_compliance/test_architecture_compliance.py -v
```

## Quality Requirements

- **Coverage:** 100% (MANDATORY)
- **Performance:** < 2 minutes for full DNA test suite
- **Reliability:** Must catch all DNA violations

## DNA Validation Framework

DNA compliance is validated at multiple levels:

1. **Feature Level** - During story analysis and design
2. **Agent Level** - Each agent validates DNA compliance
3. **Contract Level** - All contracts include DNA compliance structure
4. **System Level** - Overall system adheres to DNA principles

## Expected Test Structure

Each DNA test should validate:

```python
def test_dna_principle_validation():
    """Test DNA principle validation."""
    # Arrange: Create test data
    feature_data = {...}
    
    # Act: Validate DNA compliance
    result = dna_validator.validate_compliance(feature_data)
    
    # Assert: Check compliance results
    assert result.compliant == expected_compliance
    assert result.score >= minimum_score
    assert result.violations == expected_violations
```

## DNA Compliance Scoring

DNA compliance uses a scoring system:

- **Score Range:** 1.0 to 5.0
- **Minimum Threshold:** 3.5 for production features
- **Target Score:** 4.0+ for optimal compliance

## Common DNA Violations

### Design Principle Violations:
- Unclear learning objectives (pedagogical_value)
- Missing policy connection (policy_to_practice)  
- Exceeds 10-minute limit (time_respect)
- Fragmented solutions (holistic_thinking)
- Inappropriate tone (professional_tone)

### Architecture Principle Violations:
- Non-API interfaces (api_first)
- Stateful backend components (stateless_backend)
- Coupled components (separation_of_concerns)
- Over-engineered solutions (simplicity_first)

## Integration with Quality Gates

DNA compliance is enforced through quality gates:

1. **Project Manager** - Initial DNA analysis
2. **Game Designer** - UX DNA compliance validation
3. **Quality Reviewer** - Final DNA compliance verification

## See Also

- [Implementation_rules.md](../../Implementation_rules.md) - DNA principle definitions
- [TEST_STRATEGY.md](../../TEST_STRATEGY.md) - Overall test strategy
- [modules/shared/](../../modules/shared/) - DNA validation implementations

---

🧬 **Remember:** DNA compliance ensures every feature aligns with DigiNativa's core values and delivers value to Swedish municipal users.