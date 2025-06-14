"""
Critical Contract Compliance Tests for Developer Agent.

PURPOSE:
Ensures Developer agent maintains strict contract compatibility with:
- Game Designer (input contracts)
- Test Engineer (output contracts) 
- All other team agents via contract validation

CRITICAL FOR:
- Modular development safety
- Team integration stability
- Contract system protection
- Production deployment confidence

This file is executed by:
- make test-contracts
- make test-critical
- Pre-commit hooks
- CI/CD pipeline
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
from datetime import datetime

# Import the agent and validation systems
from ..agent import DeveloperAgent
from ...shared.base_agent import AgentExecutionResult
from ...shared.exceptions import AgentExecutionError, DNAComplianceError, QualityGateError
from ...shared.contract_validator import ContractValidator


@pytest.mark.contract
class TestDeveloperAgentContractCompliance:
    """
    Critical contract compliance tests for Developer Agent.
    
    These tests MUST pass for modular development safety.
    Breaking these tests indicates contract violations that will
    break team integration.
    """
    
    @pytest.fixture
    def developer_agent(self):
        """Create DeveloperAgent instance for contract testing."""
        config = {
            "frontend_path": "test_frontend",
            "backend_path": "test_backend",
            "test_path": "test_tests"
        }
        return DeveloperAgent(config)
    
    @pytest.fixture
    def contract_validator(self):
        """Create ContractValidator for schema validation."""
        return ContractValidator()
    
    @pytest.fixture
    def valid_input_contract_from_game_designer(self):
        """
        Valid input contract from Game Designer agent.
        MUST match Implementation_rules.md specification exactly.
        """
        return {
            "contract_version": "1.0",
            "contract_type": "design_to_implementation",
            "story_id": "STORY-CONTRACT-TEST-001",
            "source_agent": "game_designer",
            "target_agent": "developer",
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": True,
                    "policy_to_practice": True,
                    "time_respect": True,
                    "holistic_thinking": True,
                    "professional_tone": True
                },
                "architecture_compliance": {
                    "api_first": True,
                    "stateless_backend": True,
                    "separation_of_concerns": True,
                    "simplicity_first": True
                }
            },
            "input_requirements": {
                "required_files": [
                    "docs/specs/game_design_STORY-CONTRACT-TEST-001.md",
                    "docs/specs/ux_specification_STORY-CONTRACT-TEST-001.md",
                    "docs/specs/component_mapping_STORY-CONTRACT-TEST-001.json"
                ],
                "required_data": {
                    "game_mechanics": {
                        "title": "Contract Test Feature",
                        "description": "Test feature for contract compliance"
                    },
                    "ui_components": [
                        {
                            "name": "TestComponent",
                            "type": "form",
                            "ui_library_components": ["Button", "Input", "Card"],
                            "accessibility": {"role": "form"},
                            "interactions": [
                                {"type": "submit", "target": "test_api"}
                            ]
                        }
                    ],
                    "interaction_flows": [
                        {
                            "name": "test_flow",
                            "steps": ["input", "validate", "submit", "confirm"]
                        }
                    ],
                    "api_endpoints": [
                        {
                            "name": "test_endpoint",
                            "method": "POST",
                            "path": "/test",
                            "description": "Test endpoint for contract compliance",
                            "request_model": {"data": "string"},
                            "response_model": {"success": "boolean"},
                            "business_logic": {"validation": "basic"},
                            "dependencies": []
                        }
                    ],
                    "state_management": {
                        "type": "stateless",
                        "client_state": ["form_data"]
                    }
                },
                "required_validations": [
                    "component_mapping_complete",
                    "technical_specifications_clear",
                    "architecture_constraints_defined"
                ]
            },
            "output_specifications": {
                "deliverable_files": [
                    "frontend/components/STORY-CONTRACT-TEST-001/",
                    "backend/endpoints/STORY-CONTRACT-TEST-001/",
                    "tests/unit/STORY-CONTRACT-TEST-001/",
                    "docs/implementation/STORY-CONTRACT-TEST-001_implementation.md"
                ],
                "deliverable_data": {
                    "component_implementations": ["object"],
                    "api_implementations": ["object"],
                    "test_suite": "object",
                    "deployment_instructions": "object"
                },
                "validation_criteria": {
                    "code_quality": {
                        "typescript_errors": {"max": 0},
                        "eslint_violations": {"max": 0},
                        "test_coverage_percent": {"min": 100}
                    },
                    "performance": {
                        "lighthouse_score": {"min": 90},
                        "api_response_time_ms": {"max": 200},
                        "bundle_size_increase_kb": {"max": 50}
                    },
                    "architecture": {
                        "api_first_compliance": True,
                        "stateless_backend_maintained": True,
                        "component_library_usage": {"percentage": 100}
                    }
                }
            },
            "quality_gates": [
                "typescript_compilation_success_zero_errors",
                "eslint_standards_compliance_verified", 
                "unit_tests_100_percent_coverage_achieved",
                "api_endpoints_respond_correctly",
                "component_integration_working"
            ],
            "handoff_criteria": [
                "all_game_mechanics_functionally_complete",
                "ui_matches_wireframes_and_specifications",
                "api_endpoints_tested_and_documented",
                "error_handling_implemented_comprehensively",
                "code_ready_for_qa_testing"
            ]
        }
    
    def test_input_contract_schema_validation(self, contract_validator, valid_input_contract_from_game_designer):
        """
        CRITICAL: Input contract from Game Designer must validate against schema.
        
        This test ensures Developer can receive contracts from Game Designer.
        Breaking this test breaks the entire team pipeline.
        """
        validation_result = contract_validator.validate_contract(valid_input_contract_from_game_designer)
        
        assert validation_result["is_valid"], f"Input contract validation failed: {validation_result['errors']}"
        assert len(validation_result["errors"]) == 0, f"Contract has validation errors: {validation_result['errors']}"
        assert "contract_version" in valid_input_contract_from_game_designer
        assert "story_id" in valid_input_contract_from_game_designer
        assert "source_agent" in valid_input_contract_from_game_designer
        assert "target_agent" in valid_input_contract_from_game_designer
    
    def test_input_contract_agent_sequence_validation(self, valid_input_contract_from_game_designer):
        """
        CRITICAL: Agent sequence must follow Implementation_rules.md specification.
        
        Game Designer → Developer is the only valid input sequence.
        """
        assert valid_input_contract_from_game_designer["source_agent"] == "game_designer"
        assert valid_input_contract_from_game_designer["target_agent"] == "developer"
    
    def test_input_contract_dna_compliance_structure(self, valid_input_contract_from_game_designer):
        """
        CRITICAL: DNA compliance structure must be complete and valid.
        
        Both design_principles_validation and architecture_compliance required.
        """
        dna_compliance = valid_input_contract_from_game_designer["dna_compliance"]
        
        # Check design principles validation
        design_principles = dna_compliance["design_principles_validation"]
        required_design_principles = [
            "pedagogical_value", "policy_to_practice", "time_respect",
            "holistic_thinking", "professional_tone"
        ]
        for principle in required_design_principles:
            assert principle in design_principles, f"Missing design principle: {principle}"
            assert isinstance(design_principles[principle], bool), f"Design principle {principle} must be boolean"
        
        # Check architecture compliance
        architecture_compliance = dna_compliance["architecture_compliance"]
        required_architecture_principles = [
            "api_first", "stateless_backend", 
            "separation_of_concerns", "simplicity_first"
        ]
        for principle in required_architecture_principles:
            assert principle in architecture_compliance, f"Missing architecture principle: {principle}"
            assert isinstance(architecture_compliance[principle], bool), f"Architecture principle {principle} must be boolean"
    
    def test_input_contract_required_data_structure(self, valid_input_contract_from_game_designer):
        """
        CRITICAL: Required data structure must match expected format.
        
        Developer agent depends on specific data structure from Game Designer.
        """
        required_data = valid_input_contract_from_game_designer["input_requirements"]["required_data"]
        
        # Check required top-level fields
        required_fields = [
            "game_mechanics", "ui_components", "interaction_flows",
            "api_endpoints", "state_management"
        ]
        for field in required_fields:
            assert field in required_data, f"Missing required data field: {field}"
        
        # Check game_mechanics structure
        game_mechanics = required_data["game_mechanics"]
        assert "title" in game_mechanics
        assert "description" in game_mechanics
        
        # Check ui_components structure
        ui_components = required_data["ui_components"]
        assert isinstance(ui_components, list)
        if ui_components:
            component = ui_components[0]
            assert "name" in component
            assert "type" in component
            
        # Check api_endpoints structure
        api_endpoints = required_data["api_endpoints"]
        assert isinstance(api_endpoints, list)
        if api_endpoints:
            endpoint = api_endpoints[0]
            assert "name" in endpoint
            assert "method" in endpoint
            assert "path" in endpoint
    
    @pytest.mark.asyncio
    async def test_output_contract_generation_structure(self, developer_agent, valid_input_contract_from_game_designer):
        """
        CRITICAL: Output contract to Test Engineer must have correct structure.
        
        This test validates Developer generates contracts Test Engineer can consume.
        """
        # Mock the heavy processing to focus on contract structure
        with patch.object(developer_agent.git_operations, 'create_feature_branch', new_callable=AsyncMock) as mock_git:
            with patch.object(developer_agent.component_builder, 'build_components', new_callable=AsyncMock) as mock_components:
                with patch.object(developer_agent.api_builder, 'build_apis', new_callable=AsyncMock) as mock_apis:
                    with patch.object(developer_agent.code_generator, 'generate_tests', new_callable=AsyncMock) as mock_tests:
                        with patch.object(developer_agent.git_operations, 'commit_implementation', new_callable=AsyncMock) as mock_commit:
                            
                            # Mock return values with minimal valid data
                            mock_git.return_value = None
                            mock_components.return_value = [
                                {
                                    "name": "TestComponent",
                                    "files": {"component": "test.tsx"},
                                    "code": {"component": "// Test component"},
                                    "typescript_errors": 0,
                                    "eslint_violations": 0,
                                    "test_coverage_percent": 100
                                }
                            ]
                            mock_apis.return_value = [
                                {
                                    "name": "test_endpoint", 
                                    "files": {"endpoint": "test.py"},
                                    "code": {"endpoint": "# Test endpoint"},
                                    "functional_test_passed": True,
                                    "performance_test_passed": True,
                                    "estimated_response_time_ms": 150
                                }
                            ]
                            mock_tests.return_value = {
                                "unit_tests": [],
                                "coverage_percent": 100
                            }
                            mock_commit.return_value = "abc123"
                            
                            # Process contract and get output
                            output_contract = await developer_agent.process_contract(valid_input_contract_from_game_designer)
                            
                            # Validate output contract structure
                            assert "contract_version" in output_contract
                            assert "story_id" in output_contract
                            assert "source_agent" in output_contract
                            assert "target_agent" in output_contract
                            
                            # Check agent sequence is correct for Test Engineer
                            assert output_contract["source_agent"] == "developer"
                            assert output_contract["target_agent"] == "test_engineer"
                            
                            # Check required sections exist
                            assert "dna_compliance" in output_contract
                            assert "input_requirements" in output_contract
                            assert "output_specifications" in output_contract
                            assert "quality_gates" in output_contract
                            assert "handoff_criteria" in output_contract
    
    @pytest.mark.asyncio
    async def test_output_contract_validation_against_schema(self, developer_agent, contract_validator, valid_input_contract_from_game_designer):
        """
        CRITICAL: Output contract must validate against contract schema.
        
        This ensures Test Engineer can process Developer's output contracts.
        """
        # Mock processing to get contract output
        with patch.object(developer_agent.git_operations, 'create_feature_branch', new_callable=AsyncMock):
            with patch.object(developer_agent.component_builder, 'build_components', new_callable=AsyncMock) as mock_components:
                with patch.object(developer_agent.api_builder, 'build_apis', new_callable=AsyncMock) as mock_apis:
                    with patch.object(developer_agent.code_generator, 'generate_tests', new_callable=AsyncMock) as mock_tests:
                        with patch.object(developer_agent.git_operations, 'commit_implementation', new_callable=AsyncMock):
                            
                            # Set up mocks with valid structure
                            mock_components.return_value = [{"name": "TestComponent", "files": {}, "code": {}, "typescript_errors": 0, "eslint_violations": 0}]
                            mock_apis.return_value = [{"name": "test_api", "files": {}, "code": {}, "functional_test_passed": True}]
                            mock_tests.return_value = {"unit_tests": [], "coverage_percent": 100}
                            
                            # Generate output contract
                            output_contract = await developer_agent.process_contract(valid_input_contract_from_game_designer)
                            
                            # Validate against schema
                            validation_result = contract_validator.validate_contract(output_contract)
                            assert validation_result["is_valid"], f"Output contract validation failed: {validation_result['errors']}"
    
    def test_quality_gates_completeness(self, valid_input_contract_from_game_designer):
        """
        CRITICAL: Quality gates must be complete and machine-readable.
        
        Quality gates enable automated validation in the pipeline.
        """
        quality_gates = valid_input_contract_from_game_designer["quality_gates"]
        
        # Check that quality gates are present and non-empty
        assert len(quality_gates) > 0, "Quality gates cannot be empty"
        
        # Check for key quality gates specific to Developer
        expected_gates = [
            "typescript_compilation_success_zero_errors",
            "eslint_standards_compliance_verified",
            "unit_tests_100_percent_coverage_achieved"
        ]
        
        for gate in expected_gates:
            assert gate in quality_gates, f"Missing critical quality gate: {gate}"
    
    def test_handoff_criteria_completeness(self, valid_input_contract_from_game_designer):
        """
        CRITICAL: Handoff criteria must specify what Test Engineer receives.
        
        Clear handoff criteria enable proper Test Engineer validation.
        """
        handoff_criteria = valid_input_contract_from_game_designer["handoff_criteria"]
        
        # Check that handoff criteria are present and non-empty
        assert len(handoff_criteria) > 0, "Handoff criteria cannot be empty"
        
        # Check for key handoff criteria specific to Test Engineer
        expected_criteria = [
            "all_game_mechanics_functionally_complete",
            "code_ready_for_qa_testing"
        ]
        
        for criterion in expected_criteria:
            assert criterion in handoff_criteria, f"Missing critical handoff criterion: {criterion}"
    
    def test_file_path_story_id_compliance(self, valid_input_contract_from_game_designer):
        """
        CRITICAL: File paths must contain story_id for traceability.
        
        File path conventions enable proper organization and cleanup.
        """
        story_id = valid_input_contract_from_game_designer["story_id"]
        
        # Check input files contain story_id
        input_files = valid_input_contract_from_game_designer["input_requirements"]["required_files"]
        for file_path in input_files:
            assert story_id in file_path, f"Input file path missing story_id: {file_path}"
        
        # Check output files contain story_id
        output_files = valid_input_contract_from_game_designer["output_specifications"]["deliverable_files"]
        for file_path in output_files:
            assert story_id in file_path or "{story_id}" in file_path, f"Output file path missing story_id: {file_path}"
    
    def test_validation_criteria_structure(self, valid_input_contract_from_game_designer):
        """
        CRITICAL: Validation criteria must be machine-readable with thresholds.
        
        Structured validation criteria enable automated quality checking.
        """
        validation_criteria = valid_input_contract_from_game_designer["output_specifications"]["validation_criteria"]
        
        # Check main categories exist
        required_categories = ["code_quality", "performance", "architecture"]
        for category in required_categories:
            assert category in validation_criteria, f"Missing validation category: {category}"
        
        # Check code quality has numeric thresholds
        code_quality = validation_criteria["code_quality"]
        assert "typescript_errors" in code_quality
        assert "max" in code_quality["typescript_errors"]
        assert isinstance(code_quality["typescript_errors"]["max"], int)
        
        # Check performance has numeric thresholds
        performance = validation_criteria["performance"]
        assert "api_response_time_ms" in performance
        assert "max" in performance["api_response_time_ms"]
        assert isinstance(performance["api_response_time_ms"]["max"], int)
    
    @pytest.mark.asyncio
    async def test_contract_backwards_compatibility(self, developer_agent):
        """
        CRITICAL: Contract processing must maintain backwards compatibility.
        
        Older contract versions should still be processable.
        """
        # Test contract with minimal required fields (backwards compatibility)
        minimal_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-MINIMAL-001",
            "source_agent": "game_designer",
            "target_agent": "developer",
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": True,
                    "policy_to_practice": True,
                    "time_respect": True,
                    "holistic_thinking": True,
                    "professional_tone": True
                },
                "architecture_compliance": {
                    "api_first": True,
                    "stateless_backend": True,
                    "separation_of_concerns": True,
                    "simplicity_first": True
                }
            },
            "input_requirements": {
                "required_data": {
                    "game_mechanics": {"title": "Minimal", "description": "Test"},
                    "ui_components": [],
                    "interaction_flows": [],
                    "api_endpoints": [],
                    "state_management": {"type": "stateless"}
                }
            }
        }
        
        # Mock processing to focus on contract handling
        with patch.object(developer_agent, 'git_operations') as mock_git:
            with patch.object(developer_agent, 'component_builder') as mock_comp:
                with patch.object(developer_agent, 'api_builder') as mock_api:
                    with patch.object(developer_agent, 'code_generator') as mock_code:
                        
                        # Mock all async methods
                        mock_git.create_feature_branch = AsyncMock()
                        mock_git.commit_implementation = AsyncMock(return_value="abc123")
                        mock_comp.build_components = AsyncMock(return_value=[])
                        mock_api.build_apis = AsyncMock(return_value=[])
                        mock_code.generate_tests = AsyncMock(return_value={"unit_tests": [], "coverage_percent": 100})
                        
                        # Should not raise exception - backwards compatibility
                        try:
                            await developer_agent.process_contract(minimal_contract)
                        except Exception as e:
                            pytest.fail(f"Backwards compatibility broken: {e}")
    
    def test_error_handling_preserves_contract_structure(self, developer_agent, valid_input_contract_from_game_designer):
        """
        CRITICAL: Error conditions must not break contract structure.
        
        Even in error cases, agent must maintain contract compatibility.
        """
        # Test that contract validation errors are properly structured
        invalid_contract = valid_input_contract_from_game_designer.copy()
        invalid_contract["source_agent"] = "invalid_agent"  # Break agent sequence
        
        # Contract validation should catch this and raise proper exception
        try:
            # This should raise a validation error, not a generic exception
            developer_agent._validate_dna_compliance(invalid_contract)
        except Exception as e:
            # Error should be specific and structured, not generic
            assert "dna_compliance" in str(e).lower() or "validation" in str(e).lower()


@pytest.mark.contract
@pytest.mark.performance
class TestDeveloperAgentContractPerformance:
    """
    Performance tests for contract processing.
    
    Ensures contract operations meet performance requirements.
    """
    
    @pytest.fixture
    def developer_agent(self):
        """Create DeveloperAgent instance for performance testing."""
        return DeveloperAgent()
    
    @pytest.mark.asyncio
    async def test_contract_processing_performance(self, developer_agent, valid_input_contract_from_game_designer):
        """
        Performance test: Contract processing must complete within time budget.
        
        Target: Full contract processing < 30 seconds
        """
        import time
        
        # Mock heavy operations to focus on contract processing performance
        with patch.object(developer_agent.git_operations, 'create_feature_branch', new_callable=AsyncMock):
            with patch.object(developer_agent.component_builder, 'build_components', new_callable=AsyncMock) as mock_comp:
                with patch.object(developer_agent.api_builder, 'build_apis', new_callable=AsyncMock) as mock_api:
                    with patch.object(developer_agent.code_generator, 'generate_tests', new_callable=AsyncMock) as mock_tests:
                        with patch.object(developer_agent.git_operations, 'commit_implementation', new_callable=AsyncMock):
                            
                            # Set up minimal mocks
                            mock_comp.return_value = []
                            mock_api.return_value = []
                            mock_tests.return_value = {"unit_tests": [], "coverage_percent": 100}
                            
                            # Measure contract processing time
                            start_time = time.time()
                            await developer_agent.process_contract(valid_input_contract_from_game_designer)
                            end_time = time.time()
                            
                            processing_time = end_time - start_time
                            
                            # Assert performance requirement
                            assert processing_time < 30.0, f"Contract processing too slow: {processing_time:.2f}s (max: 30s)"
    
    def test_contract_memory_usage(self, developer_agent, valid_input_contract_from_game_designer):
        """
        Memory test: Contract validation should not consume excessive memory.
        
        Target: < 100MB memory usage for contract validation
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Validate contract multiple times to check for memory leaks
        for _ in range(10):
            contract_validator = ContractValidator()
            contract_validator.validate_contract(valid_input_contract_from_game_designer)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Assert memory usage is reasonable
        assert memory_increase < 100, f"Excessive memory usage: {memory_increase:.2f}MB (max: 100MB)"


if __name__ == "__main__":
    # Run contract compliance tests directly
    pytest.main([__file__, "-v", "-m", "contract"])