# DNA Validation Implementation Prompts for Agent-Specific AIs

## 🎯 DNA VALIDATION COMPLIANCE REQUIREMENT

DNA validation ensures all agents follow DigiNativa's 5 design + 4 architecture principles. Currently inconsistent across agents.

**Current DNA Validation Status:**
- ✅ **Project Manager**: Complete DNA validation (active validation)
- ✅ **Game Designer**: Complete DNA validation (active UX validation) 
- ✅ **Test Engineer**: Complete DNA validation (DNATestValidator)
- ❌ **Developer**: Missing active DNA validation
- ❌ **QA Tester**: Has AI capabilities but needs DNA consistency
- ❌ **Quality Reviewer**: Missing active DNA validation

---

## 📋 DNA VALIDATION PRINCIPLES

### 5 Design Principles:
1. **Pedagogical Value**: Educational/learning focus validation
2. **Policy to Practice**: Connects policy to practical application
3. **Time Respect**: User time ≤10 minutes per feature
4. **Holistic Thinking**: Considers full context and implications  
5. **Professional Tone**: Appropriate for Swedish public sector

### 4 Architecture Principles:
1. **API First**: All communication via REST APIs
2. **Stateless Backend**: No server-side sessions
3. **Separation of Concerns**: Frontend/backend completely separate
4. **Simplicity First**: Choose simplest solution that works

---

## 🚀 AGENT-SPECIFIC DNA VALIDATION PROMPTS

### Developer Agent DNA Validation
```
PROMPT FOR DEVELOPER AI:

Implement active DNA validation for Developer agent following Test Engineer pattern:

1. **CREATE** modules/agents/developer/tools/dna_code_validator.py:
   - DNACodeValidator class for implementation validation
   - Time Respect → Code complexity analysis (simple implementation under 10 min to understand)
   - Pedagogical Value → Code learning effectiveness (clear, educational code structure)
   - Professional Tone → Code documentation and naming (Swedish municipal standards)
   - Architecture compliance → API-first, stateless, separation validation

2. **VALIDATION AREAS**:
   - React component complexity scoring (cognitive load analysis)
   - FastAPI endpoint simplicity validation (stateless, <200ms)
   - Code documentation quality (professional Swedish terminology)
   - Architecture pattern compliance (API-first, separation of concerns)

3. **INTEGRATION**:
   - Add DNA validation to process_contract() method
   - Include DNA results in output contract for Test Engineer
   - Follow exact pattern from modules/agents/test_engineer/tools/dna_test_validator.py
   - Ensure DNA compliance enhances existing functionality without breaking changes

CRITICAL: Developer implements the code - DNA validation must ensure implementation quality aligns with DigiNativa principles.
```

### QA Tester DNA Validation Enhancement
```
PROMPT FOR QA TESTER AI:

Enhance QA Tester DNA validation to match Test Engineer standard:

1. **ENHANCE** existing QA validation with formal DNA structure:
   - Create DNAQualityValidator class following Test Engineer pattern
   - Time Respect → Anna persona completion time validation (<10 minutes)
   - Pedagogical Value → Learning objective achievement validation
   - Professional Tone → Municipal communication quality validation
   - Architecture compliance → API response validation, stateless verification

2. **AI INTEGRATION**:
   - Integrate DNA validation with QualityIntelligenceEngine predictions
   - DNA compliance scoring in AI quality predictions
   - Municipal context DNA validation (Swedish public sector standards)
   - Anna persona DNA compliance prediction

3. **CONSISTENCY**:
   - Match DNA validation structure from Test Engineer (DNATestValidationResult pattern)
   - Ensure DNA results integrate with existing AI quality intelligence
   - Maintain revolutionary AI capabilities while adding DNA consistency

QA Tester has AI capabilities - DNA validation must enhance AI intelligence with principled quality assessment.
```

### Quality Reviewer DNA Validation
```
PROMPT FOR QUALITY REVIEWER AI:

Implement comprehensive DNA validation for Quality Reviewer final approval:

1. **CREATE** modules/agents/quality_reviewer/tools/dna_final_validator.py:
   - DNAFinalValidator class for complete story validation
   - Time Respect → End-to-end user journey time validation
   - Pedagogical Value → Overall learning effectiveness validation
   - Professional Tone → Client communication quality validation
   - Architecture compliance → Complete system architecture validation

2. **FINAL VALIDATION SCOPE**:
   - Aggregate DNA compliance from all previous agents
   - Final user experience DNA validation (Anna persona complete journey)
   - Swedish municipal compliance validation (GDPR, accessibility, professional standards)
   - Client communication DNA validation (professional Swedish municipal tone)

3. **INTEGRATION**:
   - Add to final approval process before deployment
   - Include DNA summary in client communication
   - DNA-based approval/rejection decisions
   - DNA compliance reporting for project owners

Quality Reviewer is final gate - DNA validation must ensure complete story compliance with DigiNativa principles.
```

---

## 📊 DNA VALIDATION IMPLEMENTATION PATTERN

### Standard DNA Validator Structure:
```python
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List
from datetime import datetime

class DNAComplianceLevel(Enum):
    EXCELLENT = "excellent"
    GOOD = "good" 
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    INADEQUATE = "inadequate"

@dataclass
class DNAValidationResult:
    overall_dna_compliant: bool
    time_respect_compliant: bool
    pedagogical_value_compliant: bool
    professional_tone_compliant: bool
    api_first_compliant: bool
    stateless_backend_compliant: bool
    separation_concerns_compliant: bool
    simplicity_first_compliant: bool
    dna_compliance_score: float  # 1-5 scale
    validation_timestamp: str
    violations: List[str]
    recommendations: List[str]

class DNAValidator:
    async def validate_dna_compliance(self, data: Dict[str, Any]) -> DNAValidationResult:
        # Implement agent-specific DNA validation
        pass
```

### Integration into Agent process_contract():
```python
# In agent process_contract() method
dna_validation_result = await self.dna_validator.validate_dna_compliance(
    story_data, implementation_data, quality_data
)

# Include in output contract
output_contract["dna_compliance"].update({
    f"{self.agent_type}_dna_validation": {
        "overall_dna_compliant": dna_validation_result.overall_dna_compliant,
        "dna_compliance_score": dna_validation_result.dna_compliance_score,
        "validation_timestamp": dna_validation_result.validation_timestamp,
        "violations": dna_validation_result.violations,
        "recommendations": dna_validation_result.recommendations
    }
})
```

---

## 🎯 DNA VALIDATION CONSISTENCY BENEFITS

**Before Consistent DNA Validation:**
- ❌ Inconsistent quality standards across agents
- ❌ DNA principles not actively enforced
- ❌ No systematic compliance measurement
- ❌ Quality gaps not caught until final review

**After Consistent DNA Validation:**
- ✅ Active DNA enforcement at every agent
- ✅ Consistent quality standards across pipeline
- ✅ Early detection of DNA violations
- ✅ Systematic quality improvement tracking
- ✅ Client confidence in DigiNativa quality

---

## 📋 IMPLEMENTATION REQUIREMENTS

### For Each Agent:
1. **DNA Validator Tool**: Create agent-specific DNA validator class
2. **Validation Integration**: Add to process_contract() method
3. **Result Structure**: Follow DNAValidationResult pattern
4. **Contract Integration**: Include DNA results in output contracts
5. **No Breaking Changes**: Preserve existing functionality

### Validation Scope per Agent:
- **Developer**: Code quality, architecture compliance, implementation simplicity
- **QA Tester**: User experience quality, municipal compliance, AI prediction enhancement
- **Quality Reviewer**: Final story compliance, client communication quality, deployment readiness

### Success Criteria:
- DNA validation active in all 6 agents
- Consistent DNA result structure across agents
- DNA compliance tracked throughout pipeline
- Early detection and correction of DNA violations

**DNA validation ensures DigiNativa delivers consistent, high-quality solutions aligned with our core principles.**