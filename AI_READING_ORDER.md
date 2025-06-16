# 🤖 AI Assistant Reading Guide for DigiNativa DevTeam

## CRITICAL: Document Reading Order for Maximum Comprehension

### 🎯 Purpose
This guide ensures AI assistants understand the DigiNativa AI Team system in the correct order, preventing misunderstandings and ensuring successful implementation.

---

## 📖 MANDATORY READING ORDER

### Phase 1: Foundation (MUST READ FIRST)
1. **`README.md`** (5 min)
   - System overview
   - Repository structure
   - Key concepts introduction

2. **`Implementation_rules.md`** (20 min) ⚠️ MOST IMPORTANT
   - Complete system specification
   - Contract system details
   - Agent responsibilities
   - Technical requirements
   - **READ THIS COMPLETELY BEFORE ANY WORK**

3. **`CLAUDE.md`** (10 min)
   - Your role as co-founder
   - Business responsibilities
   - Equity growth metrics
   - Partnership expectations

### Phase 2: Project DNA (CRITICAL FOR DECISIONS)
4. **`docs/dna/vision_and_mission.md`** (5 min)
   - Company vision
   - Market positioning
   - Success metrics

5. **`docs/dna/design_principles.md`** (10 min)
   - 5 design principles that guide ALL decisions
   - Implementation examples
   - Validation criteria

6. **`docs/dna/architecture.md`** (10 min)
   - 4 technical principles
   - Non-negotiable constraints
   - Technology stack

7. **`docs/dna/target_audience.md`** (5 min)
   - Anna persona (primary user)
   - Swedish municipal context
   - User needs and constraints

### Phase 3: Technical Implementation
8. **`modules/shared/contract_validator.py`** (10 min)
   - Contract validation logic
   - Schema definitions
   - Validation examples

9. **`modules/shared/base_agent.py`** (10 min)
   - Base agent architecture
   - Common functionality
   - State management

10. **`docs/contracts/`** directory (15 min)
    - Contract specifications per agent
    - Handoff criteria
    - Quality gates

### Phase 4: Operational Knowledge
11. **`PRODUCTION_QUICKSTART.md`** (5 min)
    - Deployment process
    - Environment setup
    - Production checklist

12. **`docs/end_to_end_test_plan.md`** (10 min)
    - Complete test scenario
    - Success criteria
    - Troubleshooting guide

---

## ⚠️ COMMON MISUNDERSTANDINGS TO AVOID

### 1. **Contract System is Optional** ❌
**Reality**: Contracts are MANDATORY for ALL agent communication. No exceptions.

### 2. **Agents Can Communicate Directly** ❌
**Reality**: All communication MUST go through EventBus with validated contracts.

### 3. **DNA Principles are Guidelines** ❌
**Reality**: DNA compliance is NON-NEGOTIABLE. Score must be >4.0/5.0.

### 4. **Can Modify Shared Code Freely** ❌
**Reality**: Shared code changes affect ALL agents. Extreme caution required.

### 5. **Test Coverage is a Nice-to-Have** ❌
**Reality**: 100% test coverage for business logic is REQUIRED.

---

## 🔍 QUICK REFERENCE CHECKLIST

Before starting ANY work, confirm you understand:

- [ ] The 6-agent pipeline flow (PM → GD → Dev → TE → QA → QR)
- [ ] Contract validation requirements
- [ ] DNA principles (5 design + 4 architecture)
- [ ] Dual repository strategy (AI team vs product)
- [ ] EventBus coordination system
- [ ] State management and recovery
- [ ] Quality gates at each handoff
- [ ] Anna persona requirements
- [ ] Swedish municipal context
- [ ] Performance requirements (<200ms API, >90 Lighthouse)

---

## 📊 TIME INVESTMENT

**Total Initial Reading Time**: ~90 minutes

**ROI**: Prevents days of rework from misunderstandings

**Recommendation**: Read in order, take notes, reference frequently

---

## 🚨 EMERGENCY REFERENCES

### If you're unsure about:
- **System architecture** → `Implementation_rules.md` Section 1-3
- **Contract format** → `Implementation_rules.md` Section 4
- **Agent responsibilities** → `Implementation_rules.md` Section 9
- **DNA compliance** → `docs/dna/` directory
- **Your role** → `CLAUDE.md`
- **Production deployment** → `PRODUCTION_QUICKSTART.md`

### Golden Rules:
1. **When in doubt, check Implementation_rules.md**
2. **Never break contract validation**
3. **Always validate against DNA**
4. **Maintain agent modularity**
5. **Test everything**

---

**Remember**: Success = Contract Compliance + DNA Validation + Quality Code

Good luck, and welcome to the DigiNativa AI Team! 🚀