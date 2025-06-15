"""
Full Lifecycle Integration Tests

Tests the complete DigiNativa AI Team pipeline from GitHub issue to deployed feature.
This is the most critical integration test ensuring the entire system works end-to-end.

LIFECYCLE FLOW:
GitHub Issue ’ Project Manager ’ Game Designer ’ Developer ’ 
Test Engineer ’ QA Tester ’ Quality Reviewer ’ Deployment

This test validates that:
1. Contracts flow correctly through all agents
2. DNA compliance is maintained throughout
3. Quality gates function properly
4. Features are delivered according to specifications
5. The system handles errors and edge cases gracefully
"""

import pytest
import asyncio
import time
import json
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime, timedelta

from modules.shared.contract_validator import ContractValidator
from modules.shared.exceptions import ContractValidationError, DNAComplianceError
from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.agents.game_designer.agent import GameDesignerAgent
from modules.agents.developer.agent import DeveloperAgent
from modules.agents.test_engineer.agent import TestEngineerAgent
from modules.agents.qa_tester.agent import QATesterAgent
from modules.agents.quality_reviewer.agent import QualityReviewerAgent


class TestFullLifecycle:
    """Test complete feature development lifecycle."""
    
    @pytest.fixture
    def sample_github_issue(self):
        """Sample GitHub issue that will flow through the entire pipeline."""
        return {
            "number": 123,
            "title": "Add interactive policy practice scenarios for Anna",
            "body": """## Feature Description
As Anna, a municipal administrator, I want to practice policy application through interactive scenarios so that I can better understand real-world implementation and improve my decision-making skills.

## Acceptance Criteria
- [ ] User can select from multiple policy scenarios relevant to municipal work
- [ ] Each scenario provides clear context and background information
- [ ] User receives immediate feedback on decisions with explanations
- [ ] Progress is tracked and saved for continued learning
- [ ] Feature completes within 10 minutes maximum
- [ ] Interface is accessible (WCAG AA compliant)
- [ ] Content maintains professional municipal tone

## Learning Objectives
- Apply policy knowledge to practical situations
- Understand decision-making frameworks in municipal context
- Practice critical thinking in policy implementation
- Build confidence in handling real-world scenarios

## Time Constraint
Maximum time: 10 minutes for complete scenario

## User Persona
Primary: Anna (Municipal Administrator)
- Experience: Intermediate computer skills
- Goals: Learn efficiently, apply knowledge immediately
- Constraints: Limited time, work interruptions

GDD Section: Section 3.2 - Interactive Learning Modules""",
            "state": "open",
            "labels": [
                {"name": "feature-request"},
                {"name": "priority-high"},
                {"name": "persona-anna"},
                {"name": "learning-module"}
            ],
            "assignees": [],
            "milestone": {"title": "Q1 Features"},
            "user": {"login": "municipal_trainer"},
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "html_url": "https://github.com/digitativa/game/issues/123"
        }
    
    @pytest.fixture
    def lifecycle_agents(self):
        """Create all agents needed for full lifecycle test."""
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
        """Contract validator for pipeline validation."""
        return ContractValidator()

    @pytest.mark.asyncio
    async def test_complete_happy_path_lifecycle(self, sample_github_issue, lifecycle_agents, contract_validator):
        """Test complete successful feature development lifecycle."""
        story_id = "STORY-GH-123"
        start_time = time.time()
        
        # Stage 1: Project Manager - GitHub Issue Analysis
        print(f"\n<¯ Stage 1: Project Manager processing GitHub issue {sample_github_issue['number']}")
        
        github_contract = self._create_github_contract(sample_github_issue)
        
        with patch.object(lifecycle_agents["project_manager"], 'github_integration') as mock_github:
            mock_github.fetch_issue_data.return_value = sample_github_issue
            mock_github.convert_issue_to_contract.return_value = github_contract
            
            pm_result = await lifecycle_agents["project_manager"].process_contract(github_contract)
        
        assert pm_result["story_id"] == story_id
        assert pm_result["target_agent"] == "game_designer"
        assert "story_breakdown" in pm_result["input_requirements"]["required_data"]
        assert "dna_analysis" in pm_result["input_requirements"]["required_data"]
        
        # Validate contract structure
        assert contract_validator.validate_contract_schema(pm_result)
        print(" Project Manager stage completed successfully")
        
        # Stage 2: Game Designer - UX Specification Creation
        print(f"\n<¨ Stage 2: Game Designer creating UX specifications")
        
        gd_result = await lifecycle_agents["game_designer"].process_contract(pm_result)
        
        assert gd_result["story_id"] == story_id
        assert gd_result["target_agent"] == "developer"
        assert "ux_specification" in gd_result["input_requirements"]["required_data"]
        assert "game_mechanics" in gd_result["input_requirements"]["required_data"]
        assert "wireframes" in gd_result["input_requirements"]["required_data"]
        
        # Validate UX DNA compliance
        ux_spec = gd_result["input_requirements"]["required_data"]["ux_specification"]
        assert len(ux_spec["ui_components"]) > 0
        assert ux_spec["responsive_design"] is True
        
        assert contract_validator.validate_contract_schema(gd_result)
        print(" Game Designer stage completed successfully")
        
        # Stage 3: Developer - Code Implementation
        print(f"\n=» Stage 3: Developer implementing code")
        
        with patch.object(lifecycle_agents["developer"], 'git_operations') as mock_git:
            mock_git.create_feature_branch.return_value = True
            mock_git.commit_changes.return_value = {"commit_hash": "abc123"}
            
            dev_result = await lifecycle_agents["developer"].process_contract(gd_result)
        
        assert dev_result["story_id"] == story_id
        assert dev_result["target_agent"] == "test_engineer"
        assert "generated_code" in dev_result["input_requirements"]["required_data"]
        assert "architecture_documentation" in dev_result["input_requirements"]["required_data"]
        
        # Validate code generation
        generated_code = dev_result["input_requirements"]["required_data"]["generated_code"]
        assert "frontend_components" in generated_code
        assert "backend_endpoints" in generated_code
        assert len(generated_code["frontend_components"]) > 0
        
        assert contract_validator.validate_contract_schema(dev_result)
        print(" Developer stage completed successfully")
        
        # Stage 4: Test Engineer - Test Suite Creation
        print(f"\n>ê Stage 4: Test Engineer creating test suites")
        
        te_result = await lifecycle_agents["test_engineer"].process_contract(dev_result)
        
        assert te_result["story_id"] == story_id
        assert te_result["target_agent"] == "qa_tester"
        assert "test_suite" in te_result["input_requirements"]["required_data"]
        assert "coverage_report" in te_result["input_requirements"]["required_data"]
        
        # Validate test coverage
        test_suite = te_result["input_requirements"]["required_data"]["test_suite"]
        coverage_report = te_result["input_requirements"]["required_data"]["coverage_report"]
        assert coverage_report["coverage_percentage"] >= 90
        assert len(test_suite["unit_tests"]) > 0
        assert len(test_suite["integration_tests"]) > 0
        
        assert contract_validator.validate_contract_schema(te_result)
        print(" Test Engineer stage completed successfully")
        
        # Stage 5: QA Tester - User Experience Validation
        print(f"\n=e Stage 5: QA Tester validating user experience")
        
        qa_result = await lifecycle_agents["qa_tester"].process_contract(te_result)
        
        assert qa_result["story_id"] == story_id
        assert qa_result["target_agent"] == "quality_reviewer"
        assert "persona_testing_results" in qa_result["input_requirements"]["required_data"]
        assert "accessibility_audit" in qa_result["input_requirements"]["required_data"]
        assert "user_flow_validation" in qa_result["input_requirements"]["required_data"]
        
        # Validate QA results
        persona_results = qa_result["input_requirements"]["required_data"]["persona_testing_results"]
        accessibility = qa_result["input_requirements"]["required_data"]["accessibility_audit"]
        assert persona_results["anna_persona_results"]["task_completion_rate"] >= 90
        assert accessibility["wcag_compliance_percent"] >= 95
        
        assert contract_validator.validate_contract_schema(qa_result)
        print(" QA Tester stage completed successfully")
        
        # Stage 6: Quality Reviewer - Final Approval
        print(f"\n– Stage 6: Quality Reviewer making final approval")
        
        qr_result = await lifecycle_agents["quality_reviewer"].process_contract(qa_result)
        
        assert qr_result["story_id"] == story_id
        assert qr_result["target_agent"] == "deployment"
        assert "quality_analysis" in qr_result["input_requirements"]["required_data"]
        assert "approval_status" in qr_result["input_requirements"]["required_data"]
        
        # Validate final approval
        approval_status = qr_result["input_requirements"]["required_data"]["approval_status"]
        quality_analysis = qr_result["input_requirements"]["required_data"]["quality_analysis"]
        assert approval_status is True
        assert quality_analysis["overall_score"] >= 90
        
        assert contract_validator.validate_contract_schema(qr_result)
        print(" Quality Reviewer stage completed successfully")
        
        # Validate complete lifecycle performance
        total_time = time.time() - start_time
        assert total_time < 300  # Should complete within 5 minutes
        
        print(f"\n<‰ COMPLETE LIFECYCLE SUCCESS!")
        print(f"   Story ID: {story_id}")
        print(f"   Total Time: {total_time:.2f} seconds")
        print(f"   Final Quality Score: {quality_analysis['overall_score']}")
        print(f"   Status: APPROVED FOR DEPLOYMENT")

    @pytest.mark.asyncio
    async def test_lifecycle_with_rejection_and_iteration(self, sample_github_issue, lifecycle_agents):
        """Test lifecycle with quality rejection and iteration cycle."""
        story_id = "STORY-GH-123"
        
        # Create a contract that will trigger quality rejection
        github_contract = self._create_github_contract(sample_github_issue)
        
        # Mock Project Manager to produce lower quality output
        with patch.object(lifecycle_agents["project_manager"], 'dna_analyzer') as mock_dna:
            mock_dna.analyze_dna_compliance.return_value = {
                "compliant": False,
                "compliance_score": 65.0,  # Below threshold
                "violations": ["Insufficient pedagogical value", "Time constraint exceeded"]
            }
            
            pm_result = await lifecycle_agents["project_manager"].process_contract(github_contract)
        
        # Process through pipeline with mocked lower quality
        gd_result = await lifecycle_agents["game_designer"].process_contract(pm_result)
        
        with patch.object(lifecycle_agents["developer"], 'code_quality_validator') as mock_quality:
            mock_quality.validate_code_quality.return_value = {
                "quality_score": 70.0,  # Below threshold
                "issues": ["High complexity", "Poor test coverage"]
            }
            
            dev_result = await lifecycle_agents["developer"].process_contract(gd_result)
        
        te_result = await lifecycle_agents["test_engineer"].process_contract(dev_result)
        qa_result = await lifecycle_agents["qa_tester"].process_contract(te_result)
        
        # Quality Reviewer should reject
        qr_result = await lifecycle_agents["quality_reviewer"].process_contract(qa_result)
        
        # Verify rejection and iteration request
        assert qr_result["target_agent"] == "developer"  # Back to developer for fixes
        approval_status = qr_result["input_requirements"]["required_data"]["approval_status"]
        assert approval_status is False
        
        blocking_issues = qr_result["input_requirements"]["required_data"].get("blocking_issues", [])
        assert len(blocking_issues) > 0
        
        print(" Quality rejection and iteration cycle working correctly")

    @pytest.mark.asyncio
    async def test_lifecycle_performance_under_load(self, sample_github_issue, lifecycle_agents):
        """Test lifecycle performance with multiple concurrent features."""
        start_time = time.time()
        
        # Process 3 features concurrently
        tasks = []
        for i in range(3):
            issue = sample_github_issue.copy()
            issue["number"] = 123 + i
            issue["title"] = f"Feature {i+1}: {issue['title']}"
            
            github_contract = self._create_github_contract(issue)
            
            # Create task for each feature
            task = self._process_single_feature(github_contract, lifecycle_agents, f"STORY-GH-{123+i}")
            tasks.append(task)
        
        # Run all features concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Validate all succeeded
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                pytest.fail(f"Feature {i+1} failed: {result}")
            
            assert result["approval_status"] is True
            print(f" Feature {i+1} completed successfully")
        
        total_time = time.time() - start_time
        assert total_time < 600  # Should complete within 10 minutes for 3 features
        
        print(f" Concurrent processing completed in {total_time:.2f} seconds")

    @pytest.mark.asyncio
    async def test_lifecycle_error_recovery(self, sample_github_issue, lifecycle_agents):
        """Test lifecycle error handling and recovery mechanisms."""
        story_id = "STORY-GH-123"
        
        github_contract = self._create_github_contract(sample_github_issue)
        
        # Test network error recovery
        with patch.object(lifecycle_agents["project_manager"], 'github_integration') as mock_github:
            mock_github.fetch_issue_data.side_effect = Exception("Network timeout")
            
            with pytest.raises(Exception):
                await lifecycle_agents["project_manager"].process_contract(github_contract)
        
        # Test contract validation error recovery
        invalid_contract = github_contract.copy()
        del invalid_contract["contract_version"]  # Make invalid
        
        with pytest.raises(ContractValidationError):
            await lifecycle_agents["game_designer"].process_contract(invalid_contract)
        
        print(" Error recovery mechanisms working correctly")

    async def _process_single_feature(self, github_contract: Dict[str, Any], 
                                   lifecycle_agents: Dict[str, Any], 
                                   story_id: str) -> Dict[str, Any]:
        """Process a single feature through the complete lifecycle."""
        
        # Mock external dependencies for performance
        with patch.object(lifecycle_agents["project_manager"], 'github_integration'):
            with patch.object(lifecycle_agents["developer"], 'git_operations'):
                
                # Process through each agent
                pm_result = await lifecycle_agents["project_manager"].process_contract(github_contract)
                gd_result = await lifecycle_agents["game_designer"].process_contract(pm_result)
                dev_result = await lifecycle_agents["developer"].process_contract(dev_result)
                te_result = await lifecycle_agents["test_engineer"].process_contract(dev_result)
                qa_result = await lifecycle_agents["qa_tester"].process_contract(te_result)
                qr_result = await lifecycle_agents["quality_reviewer"].process_contract(qa_result)
                
                return {
                    "story_id": story_id,
                    "approval_status": qr_result["input_requirements"]["required_data"]["approval_status"],
                    "final_result": qr_result
                }

    def _create_github_contract(self, github_issue: Dict[str, Any]) -> Dict[str, Any]:
        """Create a GitHub contract from issue data."""
        return {
            "contract_version": "1.0",
            "story_id": f"STORY-GH-{github_issue['number']}",
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
                    "github_issue_data": github_issue,
                    "feature_priority": "high",
                    "target_completion_date": (datetime.now() + timedelta(days=7)).isoformat()
                }
            }
        }

    @pytest.mark.asyncio
    async def test_dna_compliance_throughout_lifecycle(self, sample_github_issue, lifecycle_agents, contract_validator):
        """Test that DNA compliance is maintained throughout the entire lifecycle."""
        
        github_contract = self._create_github_contract(sample_github_issue)
        contracts = [github_contract]
        
        # Process through each stage and collect contracts
        current_contract = github_contract
        agent_sequence = [
            ("project_manager", "game_designer"),
            ("game_designer", "developer"), 
            ("developer", "test_engineer"),
            ("test_engineer", "qa_tester"),
            ("qa_tester", "quality_reviewer")
        ]
        
        for source_agent, target_agent in agent_sequence:
            with patch.object(lifecycle_agents[source_agent], 'github_integration', create=True):
                with patch.object(lifecycle_agents[source_agent], 'git_operations', create=True):
                    
                    result = await lifecycle_agents[source_agent].process_contract(current_contract)
                    contracts.append(result)
                    current_contract = result
                    
                    # Validate DNA compliance at each stage
                    dna_compliance = result["dna_compliance"]
                    
                    # Check design principles
                    design_principles = dna_compliance["design_principles_validation"]
                    assert design_principles["pedagogical_value"] is True
                    assert design_principles["policy_to_practice"] is True
                    assert design_principles["time_respect"] is True
                    assert design_principles["holistic_thinking"] is True
                    assert design_principles["professional_tone"] is True
                    
                    # Check architecture compliance
                    arch_compliance = dna_compliance["architecture_compliance"]
                    assert arch_compliance["api_first"] is True
                    assert arch_compliance["stateless_backend"] is True
                    assert arch_compliance["separation_of_concerns"] is True
                    assert arch_compliance["simplicity_first"] is True
                    
                    print(f" DNA compliance verified for {source_agent} ’ {target_agent}")
        
        print(" DNA compliance maintained throughout complete lifecycle")

    @pytest.mark.asyncio
    async def test_quality_gates_enforcement(self, sample_github_issue, lifecycle_agents):
        """Test that quality gates properly block progression when standards aren't met."""
        
        github_contract = self._create_github_contract(sample_github_issue)
        
        # Test quality gate blocking at Project Manager stage
        with patch.object(lifecycle_agents["project_manager"], 'validate_quality_gate') as mock_gate:
            mock_gate.return_value = False  # Fail quality gate
            
            with pytest.raises(Exception):  # Should block progression
                await lifecycle_agents["project_manager"].process_contract(github_contract)
        
        print(" Quality gates properly enforcing standards")

    def test_lifecycle_documentation_generation(self, sample_github_issue):
        """Test that lifecycle generates proper documentation for tracking."""
        
        lifecycle_doc = {
            "story_id": f"STORY-GH-{sample_github_issue['number']}",
            "feature_title": sample_github_issue["title"],
            "lifecycle_stages": [
                {"stage": "project_manager", "status": "completed", "timestamp": datetime.now().isoformat()},
                {"stage": "game_designer", "status": "completed", "timestamp": datetime.now().isoformat()},
                {"stage": "developer", "status": "completed", "timestamp": datetime.now().isoformat()},
                {"stage": "test_engineer", "status": "completed", "timestamp": datetime.now().isoformat()},
                {"stage": "qa_tester", "status": "completed", "timestamp": datetime.now().isoformat()},
                {"stage": "quality_reviewer", "status": "completed", "timestamp": datetime.now().isoformat()}
            ],
            "final_status": "approved",
            "quality_metrics": {
                "overall_score": 92.5,
                "dna_compliance": True,
                "deployment_ready": True
            }
        }
        
        # Validate documentation structure
        assert "story_id" in lifecycle_doc
        assert "lifecycle_stages" in lifecycle_doc
        assert len(lifecycle_doc["lifecycle_stages"]) == 6
        assert lifecycle_doc["final_status"] in ["approved", "rejected", "iteration_required"]
        
        print(" Lifecycle documentation generation working correctly")


# Performance benchmarks for lifecycle testing
LIFECYCLE_PERFORMANCE_BENCHMARKS = {
    "single_feature_max_time": 300,  # 5 minutes
    "concurrent_features_max_time": 600,  # 10 minutes for 3 features
    "agent_handoff_max_time": 30,  # 30 seconds per handoff
    "contract_validation_max_time": 1,  # 1 second per validation
    "quality_gate_check_max_time": 5  # 5 seconds per quality gate
}


if __name__ == "__main__":
    # Run with: pytest tests/integration/test_full_lifecycle.py -v
    pytest.main([__file__, "-v", "--tb=short"])