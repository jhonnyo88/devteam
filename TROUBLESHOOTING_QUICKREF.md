# 🚨 DigiNativa AI Team - Troubleshooting Quick Reference

## For AI Assistants: Common Issues and Solutions

### 🔴 CRITICAL ISSUES (Fix Immediately)

#### 1. Contract Validation Failure
**Symptom**: `ContractValidationError: Invalid contract structure`
**Solution**:
```python
# Check contract has all required fields
required_fields = ["contract_version", "story_id", "source_agent", "target_agent", "dna_compliance"]
# Ensure story_id format: STORY-{feature_id}-{increment}
# Validate JSON schema in modules/shared/contract_validator.py
```

#### 2. DNA Compliance Score < 4.0
**Symptom**: `DNAValidationError: Score 3.5/5.0 below threshold`
**Solution**:
- Review ALL 5 design principles in `docs/dna/design_principles.md`
- Review ALL 4 architecture principles in `docs/dna/architecture.md`
- Ensure feature aligns with Anna persona needs
- Simplify solution (KISS principle)

#### 3. Agent Communication Failure
**Symptom**: Agents not receiving work or stuck in pipeline
**Solution**:
- Check EventBus is running
- Verify contract handoff criteria met
- Check state persistence in `data/agent_states/`
- Ensure quality gates passed

### 🟡 COMMON ISSUES

#### 4. Test Coverage < 100%
**Symptom**: `Coverage report: 85% (required: 100%)`
**Solution**:
```bash
# Find uncovered lines
pytest --cov=modules --cov-report=term-missing
# Focus on business logic coverage
# UI and boilerplate can be excluded
```

#### 5. Performance Requirements Not Met
**Symptom**: API response >200ms or Lighthouse <90
**Solution**:
- Profile API endpoints with `cProfile`
- Check database queries (use indexes)
- Minimize bundle size (tree-shaking)
- Enable caching where appropriate

#### 6. Import Errors Between Agents
**Symptom**: `ImportError: No module named 'game_designer'`
**Solution**:
```python
# NEVER import between agents directly
# ❌ from modules.agents.game_designer import something
# ✅ Use contracts and EventBus for communication
```

### 🟢 SETUP ISSUES

#### 7. Missing Environment Variables
**Symptom**: `KeyError: 'OPENAI_API_KEY'`
**Solution**:
```bash
cp .env.example .env
# Edit .env with required values:
# - OPENAI_API_KEY
# - GITHUB_TOKEN
# - DATABASE_URL
```

#### 8. Database Connection Failed
**Symptom**: `sqlalchemy.exc.OperationalError`
**Solution**:
- Check DATABASE_URL in .env
- Ensure database exists
- Run migrations: `alembic upgrade head`

### 📋 QUICK CHECKS

Before any debugging, verify:
- [ ] Latest `Implementation_rules.md` read
- [ ] Contract schemas up to date
- [ ] DNA documents unchanged
- [ ] All tests passing locally
- [ ] Environment variables set

### 🔍 DEBUGGING COMMANDS

```bash
# Run specific agent in debug mode
python -m modules.agents.project_manager.agent --debug

# Check contract validation
python -m modules.shared.contract_validator --validate <contract.json>

# Test DNA compliance
python -m modules.shared.dna_validator --check <feature_spec.json>

# View EventBus logs
tail -f logs/eventbus.log

# Check agent state
cat data/agent_states/<story_id>/<agent_name>.json
```

### 📞 ESCALATION PATH

1. **First**: Check this guide
2. **Second**: Read `Implementation_rules.md` relevant section
3. **Third**: Check test files for examples
4. **Fourth**: Review git history for similar issues
5. **Last Resort**: Create detailed GitHub issue with:
   - Error message
   - Contract JSON
   - DNA compliance score
   - Steps to reproduce

### 🎯 GOLDEN RULES

1. **Contracts are sacred** - Never bypass validation
2. **DNA is law** - Must score >4.0
3. **Modularity is key** - No direct agent imports
4. **Test everything** - 100% coverage required
5. **Performance matters** - <200ms API required

---

**Remember**: Most issues stem from contract violations or DNA non-compliance. Start there!