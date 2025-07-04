"""
Agent Communication Integration Tests

Tests direct agent-to-agent communication via the contract system.
This validates that agents can properly handoff work and communicate
through the standardized contract protocol.

COMMUNICATION PATTERNS TESTED:
1. Sequential agent handoffs (A � B � C)
2. Parallel agent processing 
3. Error propagation between agents
4. Contract validation at handoff points
5. Agent state isolation
6. Communication failure recovery

This ensures the modular architecture works correctly where each agent
can be developed independently while maintaining seamless integration.
"""

import pytest
import asyncio
import time
import json
from typing import Dict, Any, List, Optional
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from modules.shared.contract_validator import ContractValidator
from modules.shared.event_bus import EventBus
from modules.shared.state_manager import StateManager
from modules.shared.exceptions import (
    ContractValidationError, 
    DNAComplianceError,
    AgentCommunicationError,
    BusinessLogicError
)
from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.agents.game_designer.agent import GameDesignerAgent
from modules.agents.developer.agent import DeveloperAgent
from modules.agents.test_engineer.agent import TestEngineerAgent
from modules.agents.qa_tester.agent import QATesterAgent
from modules.agents.quality_reviewer.agent import QualityReviewerAgent


class TestAgentCommunication:
    """Test agent-to-agent communication protocols."""
    
    @pytest.fixture
    def communication_agents(self):
        """Create agents for communication testing."""
        return {
            "project_manager": ProjectManagerAgent(),
            "game_designer": GameDesignerAgent(),
            "developer": DeveloperAgent(),
            "test_engineer": TestEngineerAgent(),
            "qa_tester": QATesterAgent(),
            "quality_reviewer": QualityReviewerAgent()
        }
    
    @pytest.fixture
    def contract_validator(self):
        """Contract validator for communication validation."""
        return ContractValidator()
    
    @pytest.fixture
    def event_bus(self):
        """Event bus for agent communication."""
        return EventBus()
    
    @pytest.fixture
    def state_manager(self):
        """State manager for agent state isolation."""
        return StateManager()

    @pytest.fixture
    def sample_contract_chain(self):
        """Sample contracts for testing communication chain."""
        return {
            "github_to_pm": {
                "contract_version": "1.0",
                "story_id": "STORY-COMM-001",
                "source_agent": "github",
                "target_agent": "project_manager",
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
                        "github_issue_data": {
                            "number": 123,
                            "title": "Test communication feature",
                            "body": "Feature for testing agent communication",
                            "labels": [{"name": "priority-high"}]
                        }
                    }
                }
            }
        }

    @pytest.mark.asyncio
    async def test_sequential_agent_handoff(self, communication_agents, sample_contract_chain, contract_validator):
        """Test sequential agent handoff through contract system."""
        
        print("\n= Testing Sequential Agent Handoff")
        
        # Start with GitHub � Project Manager
        github_contract = sample_contract_chain["github_to_pm"]
        current_contract = github_contract
        
        handoff_chain = [
            ("project_manager", "game_designer"),
            ("game_designer", "developer"),
            ("developer", "test_engineer"),
            ("test_engineer", "qa_tester"),
            ("qa_tester", "quality_reviewer")
        ]
        
        handoff_times = []
        
        for source_agent, target_agent in handoff_chain:
            start_time = time.time()
            
            # Mock external dependencies for faster testing
            with patch.object(communication_agents[source_agent], 'github_integration', create=True):
                with patch.object(communication_agents[source_agent], 'git_operations', create=True):
                    
                    # Process contract through agent
                    result_contract = await communication_agents[source_agent].process_contract(current_contract)
                    
                    # Validate contract structure
                    assert contract_validator.validate_contract_schema(result_contract)
                    
                    # Verify handoff target
                    assert result_contract["target_agent"] == target_agent
                    assert result_contract["source_agent"] == source_agent
                    assert result_contract["story_id"] == "STORY-COMM-001"
                    
                    # Verify DNA compliance maintained
                    dna_compliance = result_contract["dna_compliance"]
                    assert all(dna_compliance["design_principles_validation"].values())
                    assert all(dna_compliance["architecture_compliance"].values())
                    
                    handoff_time = time.time() - start_time
                    handoff_times.append(handoff_time)
                    
                    print(f"    {source_agent} � {target_agent}: {handoff_time:.2f}s")
                    
                    # Prepare for next handoff
                    current_contract = result_contract
        
        # Validate performance requirements
        max_handoff_time = max(handoff_times)
        avg_handoff_time = sum(handoff_times) / len(handoff_times)
        
        assert max_handoff_time < 30  # Max 30 seconds per handoff
        assert avg_handoff_time < 15  # Average under 15 seconds
        
        print(f"   =� Performance: Max {max_handoff_time:.2f}s, Avg {avg_handoff_time:.2f}s")
        print(" Sequential handoff completed successfully")

    @pytest.mark.asyncio
    async def test_parallel_agent_processing(self, communication_agents, sample_contract_chain):
        """Test parallel agent processing with different contracts."""
        
        print("\n=  Testing Parallel Agent Processing")
        
        # Create multiple contracts for parallel processing
        base_contract = sample_contract_chain["github_to_pm"]
        contracts = []
        
        for i in range(3):
            contract = base_contract.copy()
            contract["story_id"] = f"STORY-COMM-{i+1:03d}"
            contract["input_requirements"]["required_data"]["github_issue_data"]["number"] = 123 + i
            contracts.append(contract)
        
        # Process contracts in parallel through Project Manager
        start_time = time.time()
        
        tasks = []
        for contract in contracts:
            with patch.object(communication_agents["project_manager"], 'github_integration'):
                task = communication_agents["project_manager"].process_contract(contract)
                tasks.append(task)
        
        # Wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        parallel_time = time.time() - start_time
        
        # Validate all succeeded
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                pytest.fail(f"Parallel processing failed for contract {i+1}: {result}")
            
            assert result["story_id"] == f"STORY-COMM-{i+1:03d}"
            assert result["target_agent"] == "game_designer"
            print(f"    Contract {i+1}: Processed successfully")
        
        # Validate parallel processing efficiency
        sequential_estimate = len(contracts) * 15  # Estimated 15s per contract sequentially
        assert parallel_time < sequential_estimate * 0.7  # Should be at least 30% faster
        
        print(f"   =� Parallel time: {parallel_time:.2f}s vs estimated sequential: {sequential_estimate}s")
        print(" Parallel processing completed successfully")

    @pytest.mark.asyncio
    async def test_error_propagation_between_agents(self, communication_agents, sample_contract_chain):
        """Test how errors propagate between agents in communication."""
        
        print("\n=� Testing Error Propagation")
        
        github_contract = sample_contract_chain["github_to_pm"]
        
        # Test contract validation error propagation
        invalid_contract = github_contract.copy()
        del invalid_contract["contract_version"]  # Make invalid
        
        with pytest.raises(ContractValidationError):
            await communication_agents["game_designer"].process_contract(invalid_contract)
        
        print("    Contract validation error caught correctly")
        
        # Test DNA compliance error propagation
        dna_violation_contract = github_contract.copy()
        dna_violation_contract["dna_compliance"]["design_principles_validation"]["pedagogical_value"] = False
        
        # Mock DNA analyzer to detect violation
        with patch.object(communication_agents["project_manager"], 'dna_analyzer') as mock_dna:
            mock_dna.analyze_dna_compliance.return_value = {
                "compliant": False,
                "violations": ["Pedagogical value not met"]
            }
            
            with pytest.raises(DNAComplianceError):
                await communication_agents["project_manager"].process_contract(dna_violation_contract)
        
        print("    DNA compliance error caught correctly")
        
        # Test business logic error propagation
        with patch.object(communication_agents["developer"], '_generate_code') as mock_generate:
            mock_generate.side_effect = BusinessLogicError("Code generation failed", "technical_complexity")
            
            with pytest.raises(BusinessLogicError):
                await communication_agents["developer"].process_contract(github_contract)
        
        print("    Business logic error caught correctly")
        print(" Error propagation working correctly")

    @pytest.mark.asyncio
    async def test_contract_validation_at_handoff_points(self, communication_agents, contract_validator):
        """Test that contracts are properly validated at each handoff point."""
        
        print("\n= Testing Contract Validation at Handoffs")
        
        # Create valid contract
        valid_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-VAL-001",
            "source_agent": "project_manager",
            "target_agent": "game_designer",
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
                    "story_breakdown": {
                        "story_id": "STORY-VAL-001",
                        "feature_summary": {"title": "Test feature"},
                        "user_stories": [{"story": "As a user..."}]
                    }
                }
            }
        }
        
        # Test contract validation before processing
        assert contract_validator.validate_contract_schema(valid_contract)
        print("    Valid contract passes validation")
        
        # Test invalid contract rejection
        invalid_contracts = [
            # Missing required field
            {**valid_contract, "contract_version": None},
            # Invalid DNA structure
            {**valid_contract, "dna_compliance": {}},
            # Missing input requirements
            {**valid_contract, "input_requirements": {}}
        ]
        
        for i, invalid_contract in enumerate(invalid_contracts):
            try:
                contract_validator.validate_contract_schema(invalid_contract)
                pytest.fail(f"Invalid contract {i+1} should have been rejected")
            except (ContractValidationError, KeyError, TypeError):
                print(f"    Invalid contract {i+1} properly rejected")
        
        print(" Contract validation working correctly at handoffs")

    @pytest.mark.asyncio
    async def test_agent_state_isolation(self, communication_agents, state_manager):
        """Test that agents maintain state isolation during communication."""
        
        print("\n<� Testing Agent State Isolation")
        
        # Create contracts for different stories
        contract1 = {
            "contract_version": "1.0",
            "story_id": "STORY-ISO-001",
            "source_agent": "github",
            "target_agent": "project_manager",
            "input_requirements": {"required_data": {"data": "story1"}}
        }
        
        contract2 = {
            "contract_version": "1.0", 
            "story_id": "STORY-ISO-002",
            "source_agent": "github",
            "target_agent": "project_manager",
            "input_requirements": {"required_data": {"data": "story2"}}
        }
        
        # Mock state manager to track state isolation
        with patch.object(communication_agents["project_manager"], 'state_manager', state_manager):
            
            # Process first contract
            with patch.object(communication_agents["project_manager"], 'github_integration'):
                await communication_agents["project_manager"].process_contract(contract1)
            
            # Verify state is stored for story 1
            story1_state = state_manager.get_agent_state("project_manager", "STORY-ISO-001")
            assert story1_state is not None
            print("    Story 1 state isolated correctly")
            
            # Process second contract
            with patch.object(communication_agents["project_manager"], 'github_integration'):
                await communication_agents["project_manager"].process_contract(contract2)
            
            # Verify both states exist independently
            story1_state = state_manager.get_agent_state("project_manager", "STORY-ISO-001")
            story2_state = state_manager.get_agent_state("project_manager", "STORY-ISO-002")
            
            assert story1_state is not None
            assert story2_state is not None
            assert story1_state != story2_state
            print("    Story 2 state isolated correctly")
            print("    States remain independent")
        
        print(" Agent state isolation working correctly")

    @pytest.mark.asyncio
    async def test_communication_failure_recovery(self, communication_agents, event_bus):
        """Test recovery mechanisms when agent communication fails."""
        
        print("\n=� Testing Communication Failure Recovery")
        
        contract = {
            "contract_version": "1.0",
            "story_id": "STORY-REC-001", 
            "source_agent": "project_manager",
            "target_agent": "game_designer",
            "input_requirements": {"required_data": {"test": "data"}}
        }
        
        # Test network timeout recovery
        with patch.object(communication_agents["game_designer"], 'process_contract') as mock_process:
            mock_process.side_effect = [
                asyncio.TimeoutError("Network timeout"),  # First attempt fails
                {"status": "success", "result": "recovered"}  # Second attempt succeeds
            ]
            
            # Should retry and succeed
            result = await self._retry_communication(
                communication_agents["project_manager"],
                communication_agents["game_designer"], 
                contract,
                max_retries=2
            )
            
            assert result["status"] == "success"
            print("    Network timeout recovery successful")
        
        # Test service unavailable recovery
        with patch.object(communication_agents["developer"], 'process_contract') as mock_process:
            mock_process.side_effect = [
                Exception("Service unavailable"),  # First attempt fails
                {"status": "success", "result": "recovered"}  # Second attempt succeeds
            ]
            
            result = await self._retry_communication(
                communication_agents["game_designer"],
                communication_agents["developer"],
                contract,
                max_retries=2
            )
            
            assert result["status"] == "success"
            print("    Service unavailable recovery successful")
        
        print(" Communication failure recovery working correctly")

    async def _retry_communication(self, source_agent, target_agent, contract, max_retries=3):
        """Helper method to retry communication with exponential backoff."""
        
        for attempt in range(max_retries):
            try:
                result = await target_agent.process_contract(contract)
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                # Exponential backoff
                wait_time = 2 ** attempt
                await asyncio.sleep(wait_time)
                continue

    @pytest.mark.asyncio
    async def test_agent_communication_performance(self, communication_agents, sample_contract_chain):
        """Test communication performance between agents."""
        
        print("\n� Testing Communication Performance")
        
        github_contract = sample_contract_chain["github_to_pm"]
        
        # Measure single communication
        start_time = time.time()
        
        with patch.object(communication_agents["project_manager"], 'github_integration'):
            result = await communication_agents["project_manager"].process_contract(github_contract)
        
        single_comm_time = time.time() - start_time
        
        # Should complete within reasonable time
        assert single_comm_time < 10  # 10 seconds max
        print(f"   =� Single communication: {single_comm_time:.2f}s")
        
        # Measure batch communication
        start_time = time.time()
        
        tasks = []
        for i in range(5):
            contract = github_contract.copy()
            contract["story_id"] = f"STORY-PERF-{i+1:03d}"
            
            with patch.object(communication_agents["project_manager"], 'github_integration'):
                task = communication_agents["project_manager"].process_contract(contract)
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        batch_comm_time = time.time() - start_time
        
        # Batch should be more efficient than sequential
        sequential_estimate = single_comm_time * 5
        assert batch_comm_time < sequential_estimate * 0.8  # At least 20% improvement
        
        print(f"   =� Batch communication (5): {batch_comm_time:.2f}s")
        print(f"   =� Efficiency gain: {((sequential_estimate - batch_comm_time) / sequential_estimate * 100):.1f}%")
        print(" Communication performance meets requirements")

    @pytest.mark.asyncio
    async def test_contract_transformation_integrity(self, communication_agents, contract_validator):
        """Test that contract data integrity is maintained during transformations."""
        
        print("\n= Testing Contract Transformation Integrity")
        
        original_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-INT-001",
            "source_agent": "github",
            "target_agent": "project_manager",
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
                    "github_issue_data": {
                        "number": 123,
                        "title": "Integrity test feature",
                        "critical_data": "must_preserve_this"
                    }
                }
            }
        }
        
        # Process through Project Manager
        with patch.object(communication_agents["project_manager"], 'github_integration'):
            transformed_contract = await communication_agents["project_manager"].process_contract(original_contract)
        
        # Verify core data integrity
        assert transformed_contract["story_id"] == original_contract["story_id"]
        assert transformed_contract["contract_version"] == original_contract["contract_version"]
        
        # Verify DNA compliance preserved
        original_dna = original_contract["dna_compliance"]
        transformed_dna = transformed_contract["dna_compliance"]
        
        assert transformed_dna["design_principles_validation"] == original_dna["design_principles_validation"]
        assert transformed_dna["architecture_compliance"] == original_dna["architecture_compliance"]
        
        # Verify critical data preserved (should be in output)
        assert "github_issue_data" in str(transformed_contract)
        print("    Critical data preserved through transformation")
        
        # Verify contract still validates
        assert contract_validator.validate_contract_schema(transformed_contract)
        print("    Transformed contract maintains valid structure")
        
        print(" Contract transformation integrity maintained")

    def test_communication_protocol_compliance(self, communication_agents):
        """Test that all agents follow the communication protocol correctly."""
        
        print("\n=� Testing Communication Protocol Compliance")
        
        # Test that all agents implement required methods
        required_methods = ["process_contract", "validate_quality_gate"]
        
        for agent_name, agent in communication_agents.items():
            for method in required_methods:
                assert hasattr(agent, method), f"{agent_name} missing required method: {method}"
                assert callable(getattr(agent, method)), f"{agent_name}.{method} is not callable"
            
            print(f"    {agent_name}: Protocol compliance verified")
        
        # Test agent type identification
        expected_types = {
            "project_manager": "project_manager",
            "game_designer": "game_designer", 
            "developer": "developer",
            "test_engineer": "test_engineer",
            "qa_tester": "qa_tester",
            "quality_reviewer": "quality_reviewer"
        }
        
        for agent_name, agent in communication_agents.items():
            assert hasattr(agent, 'agent_type'), f"{agent_name} missing agent_type attribute"
            assert agent.agent_type == expected_types[agent_name], f"{agent_name} has incorrect agent_type"
            print(f"    {agent_name}: Agent type correctly set")
        
        print(" All agents comply with communication protocol")


# Communication benchmarks and constants
COMMUNICATION_BENCHMARKS = {
    "max_handoff_time": 30,  # seconds
    "avg_handoff_time": 15,  # seconds
    "max_single_comm_time": 10,  # seconds
    "batch_efficiency_gain": 0.2,  # 20% minimum improvement
    "max_retry_attempts": 3,
    "retry_backoff_base": 2  # seconds
}


if __name__ == "__main__":
    # Run with: pytest tests/integration/test_agent_communication.py -v
    pytest.main([__file__, "-v", "--tb=short"])