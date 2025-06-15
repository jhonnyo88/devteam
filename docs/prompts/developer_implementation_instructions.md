# Utvecklarinstruktioner för DigiNativa AI-Team Integration

## 🎯 ÖVERSIKT

DigiNativa AI-teamet behöver kritiska integrations för att fungera som ett sammanhållet team. Varje agent behöver implementera EventBus integration, contract models och DNA validation för att möjliggöra end-to-end feature delivery.

**Nuvarande Status:**
- ✅ **Project Manager**: Komplett implementation med alla integrations
- ❌ **Game Designer**: Saknar contract models + EventBus integration  
- ❌ **Developer**: Saknar contract models + EventBus + DNA validation
- ❌ **Test Engineer**: Saknar contract models + EventBus integration
- ❌ **QA Tester**: Saknar contract models + EventBus integration
- ❌ **Quality Reviewer**: Saknar contract models + EventBus + DNA validation

---

## 🚀 GAME DESIGNER AGENT UTVECKLINGSINSTRUKTIONER

### Prompt för Game Designer utvecklare:

```
KRITISK IMPLEMENTATION: Game Designer Agent Integration

Du ansvarar för att göra Game Designer agenten komplett för team-integration. Följande komponenter MÅSTE implementeras:

1. **CONTRACT MODELS IMPLEMENTATION** (KRITISK PRIORITET)

Skapa dessa filer:
- `modules/agents/game_designer/contracts/__init__.py`
- `modules/agents/game_designer/contracts/input_models.py` 
- `modules/agents/game_designer/contracts/output_models.py`

**input_models.py struktur:**
```python
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime

class GameDesignerInputContract(BaseModel):
    # Contract metadata
    contract_version: str = Field("1.0", description="Contract version")
    source_agent: str = Field("project_manager", description="Source agent")
    target_agent: str = Field("game_designer", description="Target agent")
    story_id: str = Field(..., description="Story identifier")
    
    # UX Requirements från PM
    ux_requirements: Dict[str, Any] = Field(..., description="UX design requirements")
    accessibility_requirements: List[str] = Field(..., description="Accessibility needs")
    municipal_context: Dict[str, Any] = Field(..., description="Swedish municipal context")
    user_personas: List[str] = Field(..., description="Target personas (Anna)")
    
    # DNA compliance från PM
    dna_compliance: Dict[str, Any] = Field(..., description="DNA validation from PM")
    
    class Config:
        schema_extra = {
            "example": {
                "story_id": "STORY-GH-123",
                "ux_requirements": {
                    "max_completion_time_minutes": 10,
                    "accessibility_level": "WCAG AA",
                    "mobile_support": True
                },
                "municipal_context": {
                    "target_municipality": "svenska kommuner",
                    "gdpr_compliance": True
                }
            }
        }
```

**output_models.py struktur:**
```python
class GameDesignerOutputContract(BaseModel):
    # Contract metadata
    contract_version: str = Field("1.0")
    source_agent: str = Field("game_designer")
    target_agent: str = Field("developer")
    story_id: str = Field(..., description="Story identifier")
    
    # UX Deliverables för Developer
    component_specifications: List[Dict[str, Any]] = Field(..., description="Shadcn/UI component specs")
    wireframes: Dict[str, Any] = Field(..., description="Wireframe specifications")
    design_tokens: Dict[str, Any] = Field(..., description="Design system tokens")
    user_flows: List[Dict[str, Any]] = Field(..., description="User interaction flows")
    
    # Accessibility guidelines
    accessibility_guidelines: Dict[str, Any] = Field(..., description="WCAG AA implementation guide")
    
    # DNA compliance med Game Designer validation
    dna_compliance: Dict[str, Any] = Field(..., description="Enhanced DNA validation")
```

2. **EVENTBUS INTEGRATION** (KRITISK PRIORITET)

Integrera EventBus i `modules/agents/game_designer/agent.py`:

```python
from ...shared.event_bus import EventBus

# I __init__ metoden:
self.event_bus = EventBus(config)

# Lägg till team coordination metoder:
async def _notify_team_progress(self, event_type: str, data: Dict[str, Any]):
    await self.event_bus.publish(event_type, {
        "agent": "game_designer",
        "story_id": data.get("story_id"),
        "status": data.get("status"),
        "timestamp": datetime.now().isoformat(),
        **data
    })

async def _listen_for_team_events(self):
    relevant_events = ["game_designer_*", "team_*", "ux_*"]
    for event_pattern in relevant_events:
        await self.event_bus.subscribe(event_pattern, self._handle_team_event)

async def _handle_team_event(self, event_type: str, data: Dict[str, Any]):
    self.logger.info(f"Game Designer received team event: {event_type}")
    # UX-specific event handling
```

3. **PROCESS_CONTRACT INTEGRATION**

Uppdatera process_contract() metoden:
```python
async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
    story_id = input_contract.get("story_id")
    
    # Notifiera team start
    await self._notify_team_progress("ux_design_started", {"story_id": story_id})
    
    # ... existing UX processing logic ...
    
    # Notifiera milestones
    await self._notify_team_progress("wireframes_complete", {"story_id": story_id})
    await self._notify_team_progress("components_mapped", {"story_id": story_id})
    
    # Notifiera completion
    await self._notify_team_progress("ux_design_complete", {"story_id": story_id})
    
    return output_contract
```

**KRITISKA KRAV:**
- Följ exakt samma pattern som Project Manager agent
- Alla contract models måste vara Pydantic-kompatibla
- EventBus integration får INTE bryta befintlig funktionalitet
- DNA compliance struktur måste inkluderas i alla contracts

**TESTNING:**
- Verifiera att Game Designer kan ta emot PM output
- Testa att UX specs kan skickas till Developer agent
- Kontrollera att EventBus events publiceras korrekt

**DEADLINE:** Kritisk prioritet för team pipeline funktionalitet
```

---

## 🚀 DEVELOPER AGENT UTVECKLINGSINSTRUKTIONER

### Prompt för Developer utvecklare:

```
KRITISK IMPLEMENTATION: Developer Agent Integration

Du ansvarar för Developer agenten som är KÄRNAN i implementation pipeline. Följande komponenter MÅSTE implementeras:

1. **CONTRACT MODELS IMPLEMENTATION** (KRITISK PRIORITET)

Skapa:
- `modules/agents/developer/contracts/__init__.py`
- `modules/agents/developer/contracts/input_models.py`
- `modules/agents/developer/contracts/output_models.py`

**input_models.py:**
```python
class DeveloperInputContract(BaseModel):
    contract_version: str = Field("1.0")
    source_agent: str = Field("game_designer")
    target_agent: str = Field("developer")
    story_id: str = Field(..., description="Story identifier")
    
    # UX Specs från Game Designer
    component_specifications: List[Dict[str, Any]] = Field(..., description="Component specs")
    wireframes: Dict[str, Any] = Field(..., description="Wireframes")
    design_tokens: Dict[str, Any] = Field(..., description="Design system")
    user_flows: List[Dict[str, Any]] = Field(..., description="User flows")
    accessibility_guidelines: Dict[str, Any] = Field(..., description="WCAG AA guidelines")
    
    # Technical requirements
    technical_requirements: Dict[str, Any] = Field(..., description="Tech specs")
    performance_budget: Dict[str, Any] = Field(default_factory=dict, description="Performance targets")
    
    dna_compliance: Dict[str, Any] = Field(..., description="DNA validation results")
```

**output_models.py:**
```python
class DeveloperOutputContract(BaseModel):
    contract_version: str = Field("1.0")
    source_agent: str = Field("developer") 
    target_agent: str = Field("test_engineer")
    story_id: str = Field(..., description="Story identifier")
    
    # Implementation deliverables
    component_implementations: List[Dict[str, Any]] = Field(..., description="React components")
    api_implementations: List[Dict[str, Any]] = Field(..., description="FastAPI endpoints")
    
    # Git information
    git_commit_hash: str = Field(..., description="Commit hash")
    branch_name: str = Field(..., description="Feature branch")
    pull_request_url: Optional[str] = Field(None, description="PR URL")
    
    # Implementation docs
    implementation_docs: Dict[str, Any] = Field(..., description="Implementation documentation")
    test_suite: Dict[str, Any] = Field(..., description="Basic test suite")
    
    # Performance data
    estimated_performance: Dict[str, Any] = Field(..., description="Performance estimates")
    
    dna_compliance: Dict[str, Any] = Field(..., description="Developer DNA validation")
```

2. **DNA VALIDATION IMPLEMENTATION** (KRITISK)

Skapa `modules/agents/developer/tools/dna_code_validator.py`:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List
from datetime import datetime

class CodeComplexityLevel(Enum):
    EXCELLENT = "excellent"  # Very simple, clear code
    GOOD = "good"           # Simple, understandable
    ACCEPTABLE = "acceptable" # Moderately complex
    COMPLEX = "complex"     # Hard to understand
    EXCESSIVE = "excessive" # Too complex

@dataclass
class DNACodeValidationResult:
    overall_dna_compliant: bool
    time_respect_compliant: bool        # Code complexity under 10 min to understand
    pedagogical_value_compliant: bool   # Code structure teaches good practices
    professional_tone_compliant: bool   # Professional naming, documentation
    api_first_compliant: bool          # API-first architecture
    stateless_backend_compliant: bool  # No server-side sessions
    separation_concerns_compliant: bool # Frontend/backend separate
    simplicity_first_compliant: bool   # Simplest solution chosen
    dna_compliance_score: float        # 1-5 scale
    validation_timestamp: str
    violations: List[str]
    recommendations: List[str]

class DNACodeValidator:
    async def validate_code_dna_compliance(self, 
                                         component_implementations: List[Dict], 
                                         api_implementations: List[Dict],
                                         story_data: Dict[str, Any]) -> DNACodeValidationResult:
        
        # Time Respect: Code complexity analysis
        complexity_score = await self._analyze_code_complexity(component_implementations, api_implementations)
        
        # Pedagogical Value: Code learning effectiveness
        learning_score = await self._analyze_code_learning_value(component_implementations, api_implementations)
        
        # Professional Tone: Documentation and naming
        professional_score = await self._analyze_professional_standards(component_implementations, api_implementations)
        
        # Architecture Compliance: API-first, stateless, separation, simplicity
        architecture_score = await self._analyze_architecture_compliance(api_implementations)
        
        # Calculate overall compliance
        time_respect_compliant = complexity_score >= 3.0
        pedagogical_value_compliant = learning_score >= 3.0  
        professional_tone_compliant = professional_score >= 3.0
        architecture_compliant = architecture_score >= 3.0
        
        overall_compliant = all([
            time_respect_compliant, pedagogical_value_compliant, 
            professional_tone_compliant, architecture_compliant
        ])
        
        dna_score = (complexity_score + learning_score + professional_score + architecture_score) / 4.0
        
        return DNACodeValidationResult(
            overall_dna_compliant=overall_compliant,
            time_respect_compliant=time_respect_compliant,
            pedagogical_value_compliant=pedagogical_value_compliant,
            professional_tone_compliant=professional_tone_compliant,
            api_first_compliant=architecture_compliant,
            stateless_backend_compliant=architecture_compliant,
            separation_concerns_compliant=architecture_compliant,
            simplicity_first_compliant=architecture_compliant,
            dna_compliance_score=dna_score,
            validation_timestamp=datetime.now().isoformat(),
            violations=[],
            recommendations=[]
        )

    async def _analyze_code_complexity(self, components: List[Dict], apis: List[Dict]) -> float:
        # Analyze cognitive complexity of generated code
        # Return score 1-5 where 5 = very simple, 1 = too complex
        return 4.0  # Placeholder - implement actual complexity analysis

    async def _analyze_code_learning_value(self, components: List[Dict], apis: List[Dict]) -> float:
        # Analyze if code structure teaches good practices
        # Return score 1-5 where 5 = excellent learning value
        return 4.0  # Placeholder

    async def _analyze_professional_standards(self, components: List[Dict], apis: List[Dict]) -> float:
        # Analyze variable naming, documentation, code style
        # Return score 1-5 where 5 = professional standards
        return 4.0  # Placeholder

    async def _analyze_architecture_compliance(self, apis: List[Dict]) -> float:
        # Analyze API-first, stateless, separation, simplicity
        # Return score 1-5 where 5 = fully compliant
        return 4.0  # Placeholder
```

3. **EVENTBUS INTEGRATION**

I `modules/agents/developer/agent.py`:
```python
from ...shared.event_bus import EventBus
from .tools.dna_code_validator import DNACodeValidator

# I __init__:
self.event_bus = EventBus(config)
self.dna_code_validator = DNACodeValidator(config)

# I process_contract():
async def process_contract(self, input_contract: Dict[str, Any]) -> Dict[str, Any]:
    story_id = input_contract.get("story_id")
    
    await self._notify_team_progress("implementation_started", {"story_id": story_id})
    
    # ... existing implementation logic ...
    
    await self._notify_team_progress("components_implemented", {"story_id": story_id})
    await self._notify_team_progress("apis_created", {"story_id": story_id})
    await self._notify_team_progress("git_operations_complete", {"story_id": story_id})
    
    # DNA validation
    dna_result = await self.dna_code_validator.validate_code_dna_compliance(
        component_implementations, api_implementations, story_data
    )
    
    await self._notify_team_progress("implementation_complete", {"story_id": story_id})
    
    return output_contract
```

**KRITISKA KRAV:**
- React + TypeScript components med Shadcn/UI
- FastAPI endpoints (stateless, <200ms)
- Git workflow automation (branch, commit, PR)
- DNA validation av kod kvalitet och arkitektur
- EventBus integration för team coordination

**TESTNING:**
- Testa med Game Designer output som input
- Verifiera att kod genereras korrekt
- Kontrollera Git operations
- Validera DNA compliance
- Testa EventBus events

**DEADLINE:** Absolut kritisk för implementation pipeline
```

---

## 🚀 TEST ENGINEER AGENT UTVECKLINGSINSTRUKTIONER

### Prompt för Test Engineer utvecklare:

```
KRITISK IMPLEMENTATION: Test Engineer Agent Integration

Test Engineer har redan DNA validation implementerat men saknar contract models och EventBus integration.

1. **CONTRACT MODELS** (KRITISK PRIORITET)

Skapa:
- `modules/agents/test_engineer/contracts/__init__.py`
- `modules/agents/test_engineer/contracts/input_models.py`
- `modules/agents/test_engineer/contracts/output_models.py`

**input_models.py:**
```python
class TestEngineerInputContract(BaseModel):
    contract_version: str = Field("1.0")
    source_agent: str = Field("developer")
    target_agent: str = Field("test_engineer")
    story_id: str = Field(..., description="Story identifier")
    
    # Implementation data från Developer
    component_implementations: List[Dict[str, Any]] = Field(..., description="React components")
    api_implementations: List[Dict[str, Any]] = Field(..., description="FastAPI endpoints")
    git_commit_hash: str = Field(..., description="Git commit")
    implementation_docs: Dict[str, Any] = Field(..., description="Implementation docs")
    test_suite: Dict[str, Any] = Field(..., description="Basic tests")
    
    dna_compliance: Dict[str, Any] = Field(..., description="Developer DNA validation")
```

**output_models.py:**
```python
class TestEngineerOutputContract(BaseModel):
    contract_version: str = Field("1.0")
    source_agent: str = Field("test_engineer")
    target_agent: str = Field("qa_tester")
    story_id: str = Field(..., description="Story identifier")
    
    # Test deliverables
    integration_test_suite: Dict[str, Any] = Field(..., description="Integration tests")
    e2e_test_suite: Dict[str, Any] = Field(..., description="E2E tests")
    performance_results: Dict[str, Any] = Field(..., description="Performance test results")
    security_scan_results: Dict[str, Any] = Field(..., description="Security scan")
    coverage_report: Dict[str, Any] = Field(..., description="Coverage analysis")
    automation_config: Dict[str, Any] = Field(..., description="CI/CD config")
    
    # DNA validation results (Test Engineer har redan DNATestValidator)
    dna_compliance: Dict[str, Any] = Field(..., description="Test DNA validation")
```

2. **EVENTBUS INTEGRATION**

I `modules/agents/test_engineer/agent.py`:
```python
from ...shared.event_bus import EventBus

# I __init__:
self.event_bus = EventBus(config)

# I process_contract():
await self._notify_team_progress("testing_started", {"story_id": story_id})
await self._notify_team_progress("integration_tests_complete", {"story_id": story_id})
await self._notify_team_progress("e2e_tests_complete", {"story_id": story_id})
await self._notify_team_progress("performance_tests_complete", {"story_id": story_id})
await self._notify_team_progress("security_scan_complete", {"story_id": story_id})
await self._notify_team_progress("testing_complete", {"story_id": story_id})
```

**KRITISKA KRAV:**
- Använd befintlig DNATestValidator (redan implementerad)
- Contract models måste matcha befintlig agent functionality
- EventBus integration för testing progress
- Behåll alla befintliga testing capabilities

**TESTNING:**
- Testa med Developer output som input
- Verifiera att alla test suites genereras
- Kontrollera DNA validation fungerar
- Testa EventBus events för testing progress
```

---

## 🚀 QA TESTER AGENT UTVECKLINGSINSTRUKTIONER

### Prompt för QA Tester utvecklare:

```
KRITISK IMPLEMENTATION: QA Tester Agent Integration

QA Tester har redan AI capabilities (QualityIntelligenceEngine) men saknar contract models och EventBus.

1. **CONTRACT MODELS** (KRITISK PRIORITET)

Skapa:
- `modules/agents/qa_tester/contracts/__init__.py`
- `modules/agents/qa_tester/contracts/input_models.py`
- `modules/agents/qa_tester/contracts/output_models.py`

**input_models.py:**
```python
class QATesterInputContract(BaseModel):
    contract_version: str = Field("1.0")
    source_agent: str = Field("test_engineer")
    target_agent: str = Field("qa_tester")
    story_id: str = Field(..., description="Story identifier")
    
    # Test results från Test Engineer
    integration_test_suite: Dict[str, Any] = Field(..., description="Integration tests")
    e2e_test_suite: Dict[str, Any] = Field(..., description="E2E tests") 
    performance_results: Dict[str, Any] = Field(..., description="Performance results")
    security_scan_results: Dict[str, Any] = Field(..., description="Security scan")
    coverage_report: Dict[str, Any] = Field(..., description="Coverage report")
    automation_config: Dict[str, Any] = Field(..., description="Automation config")
    
    # Original implementation data för testing
    original_implementation: Dict[str, Any] = Field(..., description="Implementation data")
    
    dna_compliance: Dict[str, Any] = Field(..., description="Test Engineer DNA validation")
```

**output_models.py:**
```python
class QATesterOutputContract(BaseModel):
    contract_version: str = Field("1.0")
    source_agent: str = Field("qa_tester")
    target_agent: str = Field("quality_reviewer")
    story_id: str = Field(..., description="Story identifier")
    
    # QA deliverables
    ux_validation_results: Dict[str, Any] = Field(..., description="UX validation")
    accessibility_compliance_report: Dict[str, Any] = Field(..., description="Accessibility")
    persona_testing_results: Dict[str, Any] = Field(..., description="Anna persona testing")
    municipal_compliance_results: Dict[str, Any] = Field(..., description="Municipal compliance")
    
    # AI Quality Intelligence predictions (från QualityIntelligenceEngine)
    quality_intelligence_predictions: Dict[str, Any] = Field(..., description="AI predictions")
    anna_satisfaction_prediction: Dict[str, Any] = Field(..., description="Anna satisfaction")
    
    # Performance validation
    performance_validation_results: Dict[str, Any] = Field(..., description="Performance validation")
    
    dna_compliance: Dict[str, Any] = Field(..., description="QA DNA validation")
```

2. **EVENTBUS INTEGRATION**

I `modules/agents/qa_tester/agent.py`:
```python
from ...shared.event_bus import EventBus

# I __init__:
self.event_bus = EventBus(config)

# I process_contract() - integrera med befintlig QualityIntelligenceEngine:
await self._notify_team_progress("qa_testing_started", {"story_id": story_id})
await self._notify_team_progress("persona_testing_complete", {"story_id": story_id})
await self._notify_team_progress("accessibility_validated", {"story_id": story_id})
await self._notify_team_progress("ai_quality_prediction_complete", {"story_id": story_id})
await self._notify_team_progress("municipal_compliance_validated", {"story_id": story_id})
await self._notify_team_progress("qa_testing_complete", {"story_id": story_id})
```

**KRITISKA KRAV:**
- Behåll alla befintliga AI capabilities (QualityIntelligenceEngine)
- Integrera AI predictions i contract output
- Anna persona testing results
- Municipal compliance validation
- EventBus integration för AI quality events

**TESTNING:**
- Testa med Test Engineer output som input
- Verifiera AI quality predictions fungerar
- Kontrollera Anna persona testing
- Testa municipal compliance validation
- Validera EventBus AI events
```

---

## 🚀 QUALITY REVIEWER AGENT UTVECKLINGSINSTRUKTIONER

### Prompt för Quality Reviewer utvecklare:

```
KRITISK IMPLEMENTATION: Quality Reviewer Agent Integration

Quality Reviewer har redan ClientCommunicator men saknar contract models, EventBus och DNA validation.

1. **CONTRACT MODELS** (KRITISK PRIORITET)

Skapa:
- `modules/agents/quality_reviewer/contracts/__init__.py`
- `modules/agents/quality_reviewer/contracts/input_models.py`
- `modules/agents/quality_reviewer/contracts/output_models.py`

**input_models.py:**
```python
class QualityReviewerInputContract(BaseModel):
    contract_version: str = Field("1.0")
    source_agent: str = Field("qa_tester")
    target_agent: str = Field("quality_reviewer")
    story_id: str = Field(..., description="Story identifier")
    
    # QA results från QA Tester
    ux_validation_results: Dict[str, Any] = Field(..., description="UX validation")
    accessibility_compliance_report: Dict[str, Any] = Field(..., description="Accessibility")
    persona_testing_results: Dict[str, Any] = Field(..., description="Persona testing")
    municipal_compliance_results: Dict[str, Any] = Field(..., description="Municipal compliance")
    quality_intelligence_predictions: Dict[str, Any] = Field(..., description="AI predictions")
    performance_validation_results: Dict[str, Any] = Field(..., description="Performance")
    
    dna_compliance: Dict[str, Any] = Field(..., description="Complete DNA validation chain")
```

**output_models.py:**
```python
class QualityReviewerOutputContract(BaseModel):
    contract_version: str = Field("1.0")
    source_agent: str = Field("quality_reviewer")
    target_agent: str = Field("deployment")  # eller "project_owner"
    story_id: str = Field(..., description="Story identifier")
    
    # Final approval decision
    approval_decision: str = Field(..., description="approved/revision_required/rejected")
    quality_score: float = Field(..., description="Overall quality score")
    
    # Client communication data (från ClientCommunicator)
    client_communication_data: Dict[str, Any] = Field(..., description="Swedish municipal communication")
    approval_request_message: str = Field(..., description="Approval request for project owner")
    
    # Deployment instructions
    deployment_instructions: Optional[Dict[str, Any]] = Field(None, description="Deploy instructions")
    revision_requirements: Optional[Dict[str, Any]] = Field(None, description="Revision requirements")
    
    # Final DNA compliance summary
    dna_compliance: Dict[str, Any] = Field(..., description="Final DNA validation")
```

2. **DNA VALIDATION IMPLEMENTATION**

Skapa `modules/agents/quality_reviewer/tools/dna_final_validator.py`:

```python
@dataclass
class DNAFinalValidationResult:
    overall_dna_compliant: bool
    final_user_journey_compliant: bool    # End-to-end user experience
    client_communication_compliant: bool  # Swedish municipal communication
    deployment_ready: bool                # Ready for production
    dna_compliance_score: float           # Final score 1-5
    validation_timestamp: str
    final_violations: List[str]
    deployment_recommendations: List[str]

class DNAFinalValidator:
    async def validate_final_dna_compliance(self,
                                           story_data: Dict[str, Any],
                                           ux_validation: Dict[str, Any],
                                           persona_testing: Dict[str, Any],
                                           quality_predictions: Dict[str, Any]) -> DNAFinalValidationResult:
        
        # Aggregate DNA compliance från alla agenter
        # Validera end-to-end user journey
        # Kontrollera client communication quality
        # Bedöm deployment readiness
        
        return DNAFinalValidationResult(
            overall_dna_compliant=True,  # Implement actual validation
            final_user_journey_compliant=True,
            client_communication_compliant=True,
            deployment_ready=True,
            dna_compliance_score=4.5,
            validation_timestamp=datetime.now().isoformat(),
            final_violations=[],
            deployment_recommendations=[]
        )
```

3. **EVENTBUS INTEGRATION**

I `modules/agents/quality_reviewer/agent.py`:
```python
from ...shared.event_bus import EventBus
from .tools.dna_final_validator import DNAFinalValidator

# I __init__:
self.event_bus = EventBus(config)  
self.dna_final_validator = DNAFinalValidator(config)

# I process_contract() - integrera med befintlig ClientCommunicator:
await self._notify_team_progress("final_review_started", {"story_id": story_id})
await self._notify_team_progress("quality_assessment_complete", {"story_id": story_id})
await self._notify_team_progress("client_communication_prepared", {"story_id": story_id})

# DNA final validation
dna_final_result = await self.dna_final_validator.validate_final_dna_compliance(...)

if approved:
    await self._notify_team_progress("feature_approved", {"story_id": story_id})
    await self._notify_team_progress("deployment_ready", {"story_id": story_id})
else:
    await self._notify_team_progress("revision_required", {"story_id": story_id})
```

**KRITISKA KRAV:**
- Behåll alla befintliga ClientCommunicator capabilities
- Integrera Swedish municipal client communication
- Final DNA validation av hela feature delivery
- EventBus integration för final approval events
- GitHub approval workflow integration

**TESTNING:**
- Testa med QA Tester output som input
- Verifiera final approval/rejection logic
- Kontrollera client communication generation
- Testa DNA final validation
- Validera EventBus approval events
```

---

## 📊 SAMMANFATTNING AV UTVECKLINGSPRIORITET

**KRITISK ORDNING (parallell implementation möjlig):**

1. **Contract Models**: Alla agenter behöver detta för communication
2. **EventBus Integration**: Kritisk för team coordination  
3. **DNA Validation**: Developer och Quality Reviewer saknar detta
4. **Testing**: Validera att alla integrations fungerar tillsammans

**FRAMGÅNGSKRITERIER:**
- Alla agenter kan ta emot input från föregående agent
- Alla agenter kan skicka valid output till nästa agent
- EventBus events publiceras och tas emot korrekt
- DNA validation fungerar konsekvent genom hela pipeline
- End-to-end test från GitHub issue till deployment approval fungerar

**TESTNING:**
Efter implementation av alla agenter, använd det befintliga GitHub issue systemet för att testa hela flödet från feature request till project owner approval.

Dessa instruktioner ger utvecklarna allt de behöver för att göra DigiNativa AI-teamet produktionsklart för end-to-end feature delivery.