# EventBus Integration Prompts for Agent-Specific AIs

## 🎯 CRITICAL INTEGRATION REQUIREMENT

EventBus integration is **THE BLOCKING ISSUE** preventing DigiNativa AI team from working as a cohesive unit. All 6 agents need EventBus integration to enable real-time team coordination.

**Current Status: 0/6 agents have EventBus integration**
**Result: Team cannot coordinate, no pipeline orchestration possible**

---

## 📋 IMPLEMENTATION INSTRUCTIONS

Each agent-specific AI should implement EventBus integration following this exact pattern:

### 1. Import EventBus in Agent Constructor
```python
from ...shared.event_bus import EventBus

# In __init__ method:
self.event_bus = EventBus(config)
```

### 2. Add Team Coordination Methods
```python
async def _notify_team_progress(self, event_type: str, data: Dict[str, Any]):
    """Notify team of progress via EventBus."""
    await self.event_bus.publish(event_type, {
        "agent": self.agent_type,
        "story_id": data.get("story_id"),
        "status": data.get("status"),
        "timestamp": datetime.now().isoformat(),
        **data
    })

async def _listen_for_team_events(self):
    """Listen for relevant team events."""
    relevant_events = [f"{self.agent_type}_*", "team_*", "pipeline_*"]
    for event_pattern in relevant_events:
        await self.event_bus.subscribe(event_pattern, self._handle_team_event)

async def _handle_team_event(self, event_type: str, data: Dict[str, Any]):
    """Handle incoming team coordination events."""
    self.logger.info(f"Received team event: {event_type}")
    # Agent-specific event handling logic
```

### 3. Integration Points in process_contract()
```python
# At start of processing
await self._notify_team_progress("agent_started", {"story_id": story_id})

# At major milestones
await self._notify_team_progress("agent_milestone", {
    "story_id": story_id, 
    "milestone": "major_step_completed"
})

# At completion
await self._notify_team_progress("agent_completed", {"story_id": story_id})
```

---

## 🚀 AGENT-SPECIFIC PROMPTS

### Project Manager Agent EventBus Integration
```
PROMPT FOR PROJECT MANAGER AI:

Integrate EventBus into Project Manager agent for team coordination. The PM agent needs to:

1. **Team Leadership Events**: Publish "story_assigned", "dependencies_resolved", "priority_updated" events
2. **GitHub Integration Events**: Publish "issue_processed", "story_analyzed", "requirements_clarified"  
3. **Learning Events**: Publish "stakeholder_feedback", "complexity_learned", "estimation_improved"
4. **Team Status Events**: Listen for all agent completion events to track pipeline progress

Critical Implementation:
- Add EventBus to modules/agents/project_manager/agent.py __init__ method
- Integrate team notifications in process_contract() method
- Add EventBus imports and team coordination methods
- Ensure events align with PM's role as team coordinator

Follow the exact pattern above. PM agent is the team leader so needs comprehensive event publishing for downstream agents.
```

### Game Designer Agent EventBus Integration
```
PROMPT FOR GAME DESIGNER AI:

Integrate EventBus into Game Designer agent for UX coordination. The Game Designer needs to:

1. **UX Design Events**: Publish "wireframes_created", "components_mapped", "ux_validated" events
2. **Accessibility Events**: Publish "accessibility_requirements_defined", "anna_persona_validated"
3. **Design Review Events**: Listen for "design_feedback" from QA Tester and Quality Reviewer
4. **Pipeline Events**: Listen for PM handoff events, publish ready events for Developer

Critical Implementation:
- Add EventBus to modules/agents/game_designer/agent.py __init__ method
- Integrate UX milestone notifications in process_contract() method
- Add team coordination methods for design collaboration
- Ensure events align with UX design handoff to Developer

The Game Designer is critical for UX quality - ensure proper event coordination with QA Tester for design validation.
```

### Developer Agent EventBus Integration
```
PROMPT FOR DEVELOPER AI:

Integrate EventBus into Developer agent for implementation coordination. The Developer needs to:

1. **Implementation Events**: Publish "coding_started", "components_implemented", "apis_created" events
2. **Git Operation Events**: Publish "branch_created", "code_committed", "pr_ready" events
3. **Quality Events**: Listen for "code_review_feedback" from Quality Reviewer
4. **Testing Events**: Publish "implementation_complete" for Test Engineer handoff

Critical Implementation:
- Add EventBus to modules/agents/developer/agent.py __init__ method
- Integrate implementation progress notifications in process_contract() method
- Add Git operation event publishing for team visibility
- Ensure events coordinate with Test Engineer for testing handoff

Developer is the core implementation agent - events must provide clear implementation status for testing pipeline.
```

### Test Engineer Agent EventBus Integration
```
PROMPT FOR TEST ENGINEER AI:

Integrate EventBus into Test Engineer agent for testing coordination. The Test Engineer needs to:

1. **Testing Events**: Publish "tests_generated", "coverage_analyzed", "performance_validated" events
2. **Quality Gate Events**: Publish "security_scan_complete", "quality_gates_passed/failed" events
3. **DNA Validation Events**: Publish "dna_validation_complete" with compliance results
4. **Pipeline Events**: Listen for Developer completion, publish ready events for QA Tester

Critical Implementation:
- Add EventBus to modules/agents/test_engineer/agent.py __init__ method
- Integrate testing milestone notifications in process_contract() method
- Add DNA validation event publishing (Test Engineer has active DNA validation)
- Ensure events coordinate testing pipeline with QA Tester handoff

Test Engineer has DNA validation capabilities - ensure DNA compliance events are published for team awareness.
```

### QA Tester Agent EventBus Integration
```
PROMPT FOR QA TESTER AI:

Integrate EventBus into QA Tester agent for quality coordination. The QA Tester needs to:

1. **AI Quality Events**: Publish "quality_intelligence_prediction", "anna_satisfaction_predicted" events
2. **Testing Events**: Publish "persona_testing_complete", "accessibility_validated", "performance_tested" events
3. **Municipal Events**: Publish "municipal_compliance_verified", "swedish_context_validated" events
4. **Quality Review Events**: Publish "qa_complete" for Quality Reviewer final approval

Critical Implementation:
- Add EventBus to modules/agents/qa_tester/agent.py __init__ method
- Integrate AI quality intelligence events from QualityIntelligenceEngine
- Add persona testing and municipal validation event publishing
- Ensure events coordinate with Quality Reviewer for final approval

QA Tester has revolutionary AI capabilities - ensure AI quality prediction events are published for team intelligence.
```

### Quality Reviewer Agent EventBus Integration
```
PROMPT FOR QUALITY REVIEWER AI:

Integrate EventBus into Quality Reviewer agent for final approval coordination. The Quality Reviewer needs to:

1. **Final Review Events**: Publish "final_review_started", "quality_approved/rejected" events
2. **Deployment Events**: Publish "deployment_approved", "story_complete" events
3. **Team Feedback Events**: Publish "revision_required" with specific feedback for relevant agents
4. **Learning Events**: Publish "story_lessons_learned", "quality_insights" for PM learning

Critical Implementation:
- Add EventBus to modules/agents/quality_reviewer/agent.py __init__ method
- Integrate final approval event publishing in process_contract() method
- Add revision feedback events that target specific agents for improvements
- Ensure events complete the pipeline with deployment approval or revision requests

Quality Reviewer is the final gate - events must provide clear approval/rejection with specific feedback for pipeline completion.
```

---

## 📊 TEAM COORDINATION IMPACT

**Before EventBus Integration (Current State):**
- ❌ Agents work in isolation
- ❌ No real-time progress visibility
- ❌ No pipeline orchestration possible
- ❌ No team intelligence sharing
- ❌ Cannot test end-to-end workflow

**After EventBus Integration (Target State):**
- ✅ Real-time team coordination
- ✅ Pipeline progress visibility
- ✅ Automated workflow orchestration
- ✅ AI intelligence sharing across agents
- ✅ End-to-end pipeline testing possible

---

## 🎯 SUCCESS CRITERIA

Each agent integration is complete when:

1. **EventBus Import**: Agent imports and initializes EventBus correctly
2. **Team Events**: Agent publishes relevant progress events
3. **Event Listening**: Agent listens for relevant team coordination events
4. **Contract Integration**: EventBus calls integrated into process_contract() method
5. **No Breaking Changes**: Existing functionality preserved 100%

**CRITICAL**: Test that agents can publish/receive events without breaking existing contract validation or functionality.

---

## 💡 IMPLEMENTATION PRIORITY

**Execute these prompts in parallel - all agents need EventBus integration simultaneously for team coordination to work.**

EventBus integration is the foundation for:
- Pipeline orchestration
- Real-time progress tracking
- Team intelligence sharing
- End-to-end workflow testing
- Production-ready team deployment

**This is the #1 blocking issue for DigiNativa AI team production readiness.**