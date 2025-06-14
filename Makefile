# DigiNativa AI Team - Test Makefile
# Användning: make <target>

.PHONY: test-smoke test-contracts test-agents test-integration test-all test-critical test-dna test-performance

# Snabba röktester - grundläggande funktionalitet
test-smoke:
	@echo "🔥 Running smoke tests..."
	python -m pytest tests/contract_validation/test_contract_validator.py::TestContractValidatorBasics -v
	@echo "✅ Smoke tests completed!"

# Kritiska kontraktstester - skyddar modulär arkitektur
test-contracts:
	@echo "📋 Running contract validation tests..."
	python -m pytest tests/contract_validation/ -v
	python -m pytest modules/agents/*/tests/test_contract_compliance.py -v
	@echo "✅ Contract tests completed!"

# DNA-efterlevnadstester - säkerställer projektprinciper
test-dna:
	@echo "🧬 Running DNA compliance tests..."
	python -m pytest tests/dna_compliance/ -v
	@echo "✅ DNA compliance tests completed!"

# Agent-specifika tester
test-agents:
	@echo "🤖 Running agent-specific tests..."
	python -m pytest modules/agents/*/tests/test_agent.py -v
	python -m pytest modules/agents/*/tests/test_tools.py -v
	@echo "✅ Agent tests completed!"

# Integrationstester mellan agenter
test-integration:
	@echo "🔗 Running integration tests..."
	python -m pytest tests/integration/ -v
	@echo "✅ Integration tests completed!"

# Performance-tester för kontraktsystem
test-performance:
	@echo "⚡ Running performance tests..."
	python -m pytest tests/integration/test_contract_pipeline.py::TestContractPipeline::test_contract_processing_performance -v
	python -m pytest tests/integration/test_contract_pipeline.py::TestContractPipeline::test_contract_memory_usage -v
	@echo "✅ Performance tests completed!"

# Kritiska tester som måste passera före commit
test-critical: test-smoke test-contracts test-dna
	@echo "🚨 All critical tests passed! Safe to commit. 🚨"

# Alla tester - kör före release
test-all: test-smoke test-contracts test-agents test-dna test-integration
	@echo "🎉 All tests passed! Ready for release! 🎉"

# Testa specifik agent (användning: make test-agent-project_manager)
test-agent-%:
	@echo "🤖 Testing agent: $*"
	python -m pytest modules/agents/$*/tests/ -v
	@echo "✅ Agent $* tests completed!"

# Generera HTML coverage report
test-coverage:
	@echo "📊 Generating coverage report..."
	python -m pytest --cov=modules --cov=tests --cov-report=html --cov-report=term-missing tests/
	@echo "✅ Coverage report generated in htmlcov/"

# Kör tester med profiling
test-profile:
	@echo "📈 Running tests with profiling..."
	python -m pytest tests/contract_validation/ --profile --profile-svg
	@echo "✅ Profiling completed!"

# Hjälp - visa alla tillgängliga kommandon
help:
	@echo "DigiNativa AI Team Test Commands:"
	@echo ""
	@echo "Snabba tester:"
	@echo "  make test-smoke        - Grundläggande röktester (< 10s)"
	@echo "  make test-critical     - Kritiska tester före commit (< 2min)"
	@echo ""
	@echo "Kategori-tester:"
	@echo "  make test-contracts    - Kontraktsvalidering (KRITISK)"
	@echo "  make test-dna          - DNA-efterlevnad (KRITISK)" 
	@echo "  make test-agents       - Alla agent-specifika tester"
	@echo "  make test-integration  - Integrationstester mellan agenter"
	@echo "  make test-performance  - Performance-tester"
	@echo ""
	@echo "Specifika agenter:"
	@echo "  make test-agent-project_manager"
	@echo "  make test-agent-game_designer"
	@echo "  make test-agent-developer"
	@echo "  make test-agent-test_engineer"
	@echo "  make test-agent-qa_tester"
	@echo "  make test-agent-quality_reviewer"
	@echo ""
	@echo "Rapporter:"
	@echo "  make test-coverage     - Generera coverage report"
	@echo "  make test-profile      - Kör med profiling"
	@echo ""
	@echo "Komplett:"
	@echo "  make test-all          - Alla tester (< 30min)"

# Standard target
.DEFAULT_GOAL := help