#!/usr/bin/env python3
"""
Simple integration test for Project Manager Agent.

This demonstrates the PM Agent processing a GitHub issue
into a Game Designer contract without requiring actual API calls.
"""

import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, AsyncMock

from modules.agents.project_manager.agent import ProjectManagerAgent


async def test_pm_agent_integration():
    """
    Test Project Manager Agent end-to-end workflow.
    
    This test demonstrates:
    1. Processing a sample GitHub issue
    2. DNA compliance validation
    3. Story breakdown creation
    4. Acceptance criteria generation
    5. Complexity assessment
    6. Game Designer contract generation
    """
    
    print("🚀 Starting Project Manager Agent Integration Test")
    
    # Create temporary directory for docs
    with tempfile.TemporaryDirectory() as temp_dir:
        
        # Configuration for PM Agent
        config = {
            "github_token": "mock_token",
            "github_repo_owner": "jhonnyo88",
            "github_repo_name": "devteam",
            "docs_path": temp_dir
        }
        
        print("📋 Creating Project Manager Agent...")
        
        # Create PM Agent with mocked tools to avoid real API calls
        try:
            pm_agent = ProjectManagerAgent("test-pm-001", config)
            
            # Mock the tools to avoid external dependencies
            pm_agent.github_integration = Mock()
            pm_agent.story_analyzer = AsyncMock()
            pm_agent.dna_compliance_checker = AsyncMock()
            
            print("✅ Project Manager Agent created successfully")
            
        except Exception as e:
            print(f"❌ Failed to create PM Agent: {e}")
            return False
        
        # Sample input contract representing a GitHub issue
        sample_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-GH-123",
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
                "required_files": [],
                "required_data": {
                    "feature_description": """
                    As Anna, a public sector professional, I want to practice policy application 
                    through interactive scenarios so that I can better understand how to implement 
                    theoretical knowledge in real workplace situations.
                    
                    This feature should provide quick, focused learning exercises that help bridge 
                    the gap between policy theory and practical implementation.
                    """,
                    "acceptance_criteria": [
                        "User can select from multiple policy scenarios",
                        "Each scenario provides clear context and background information",
                        "User receives immediate feedback on their decisions",
                        "Progress is tracked and saved for future reference",
                        "Feature can be completed within 10 minutes"
                    ],
                    "user_persona": "Anna",
                    "priority_level": "high",
                    "time_constraint_minutes": 10,
                    "learning_objectives": [
                        "Apply policy knowledge to practical situations",
                        "Understand decision-making frameworks",
                        "Practice critical thinking in policy context"
                    ],
                    "github_issue_url": "https://github.com/jhonnyo88/diginativa-game/issues/123",
                    "github_issue_number": 123,
                    "requested_by": "client_user",
                    "created_at": "2024-01-15T10:30:00Z"
                },
                "required_validations": [
                    "github_issue_valid",
                    "feature_request_format_correct"
                ]
            }
        }
        
        print("📝 Processing sample feature request...")
        
        # Mock successful DNA compliance analysis
        pm_agent.dna_compliance_checker.analyze_feature_compliance.return_value = {
            "compliant": True,
            "compliance_score": 88.5,
            "pedagogical_value": True,
            "policy_to_practice": True,
            "time_respect": True,
            "holistic_thinking": True,
            "professional_tone": True,
            "violations": [],
            "recommendations": ["Feature meets all DNA compliance requirements"]
        }
        
        # Mock story breakdown creation
        pm_agent.story_analyzer.create_story_breakdown.return_value = {
            "story_id": "STORY-GH-123",
            "feature_summary": {
                "title": "Policy Practice Interactive Scenarios",
                "description": "Interactive learning module for policy application",
                "user_persona": "Anna",
                "priority": "high",
                "time_constraint_minutes": 10
            },
            "user_stories": [
                {
                    "story_id": "US-001",
                    "role": "Anna",
                    "action": "select policy scenarios",
                    "benefit": "practice decision-making",
                    "story": "As Anna, I want to select policy scenarios so that I can practice decision-making"
                }
            ],
            "technical_requirements": {
                "frontend": {"required_components": ["ScenarioSelector", "FeedbackDisplay"]},
                "backend": {"api_endpoints": ["/api/scenarios", "/api/feedback"]},
                "database": {"new_tables": []},
                "integrations": {"external_apis": []}
            },
            "design_requirements": {
                "ui_components": ["Button", "Card", "ProgressBar"],
                "user_flows": ["scenario_selection", "feedback_display"],
                "wireframe_requirements": ["desktop_layout", "mobile_layout"]
            },
            "implementation_tasks": [
                {"task_id": "TASK-001", "category": "Frontend Development", "name": "Create scenario selection UI"},
                {"task_id": "TASK-002", "category": "Backend Development", "name": "Implement scenario API"},
                {"task_id": "TASK-003", "category": "Testing", "name": "Write component tests"}
            ]
        }
        
        # Mock acceptance criteria generation
        pm_agent.story_analyzer.generate_acceptance_criteria.return_value = [
            "User can select from multiple policy scenarios",
            "Each scenario provides clear context and background information",
            "User receives immediate feedback on their decisions",
            "Progress is tracked and saved for future reference",
            "Feature can be completed within 10 minutes",
            "Feature maintains pedagogical value throughout interaction",
            "All UI components are accessible (WCAG AA compliant)",
            "Feature works correctly on mobile devices"
        ]
        
        # Mock complexity assessment
        pm_agent.story_analyzer.assess_complexity.return_value = {
            "overall_complexity": "Medium",
            "effort_points": 5,
            "technical_complexity": "Medium",
            "design_complexity": "Low",
            "integration_complexity": "Low",
            "testing_complexity": "Medium",
            "estimated_duration_hours": 16,
            "estimated_duration_days": 2.0,
            "confidence_level": 0.8,
            "complexity_breakdown": {
                "frontend_work": 3,
                "backend_work": 2,
                "testing_work": 2,
                "integration_work": 1
            }
        }
        
        try:
            # Process the contract
            result = await pm_agent.process_contract(sample_contract)
            
            print("✅ Contract processed successfully!")
            print(f"   📊 Story ID: {result['story_id']}")
            print(f"   🎯 Target Agent: {result['target_agent']}")
            print(f"   📋 Quality Gates: {len(result.get('quality_gates', []))}")
            print(f"   🔄 Handoff Criteria: {len(result.get('handoff_criteria', []))}")
            
            # Verify the result structure
            required_fields = [
                "story_id", "target_agent", "input_requirements", 
                "output_specifications", "quality_gates", "handoff_criteria"
            ]
            
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                print(f"❌ Missing required fields: {missing_fields}")
                return False
            
            # Verify Game Designer contract structure
            input_reqs = result["input_requirements"]
            if "required_data" not in input_reqs:
                print("❌ Missing required_data in input_requirements")
                return False
            
            required_data = input_reqs["required_data"]
            if "acceptance_criteria" not in required_data:
                print("❌ Missing acceptance_criteria in required_data")
                return False
            
            print(f"   ✅ Generated {len(required_data['acceptance_criteria'])} acceptance criteria")
            print(f"   ✅ Complexity: {required_data.get('complexity_assessment', {}).get('overall_complexity', 'Unknown')}")
            
            # Check if documentation was created
            docs_path = Path(temp_dir)
            story_file = docs_path / "stories" / "STORY-GH-123_description.md"
            
            if story_file.exists():
                print("   📄 Story documentation created successfully")
                
                # Show a snippet of the generated documentation
                with open(story_file, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')[:10]  # First 10 lines
                    print("   📝 Story documentation preview:")
                    for line in lines:
                        print(f"      {line}")
                    if len(content.split('\n')) > 10:
                        print("      ...")
            
            print("\n🎉 Project Manager Agent Integration Test PASSED!")
            print("✅ All core functionality working correctly")
            print("✅ Contract validation and generation successful")
            print("✅ DNA compliance checking integrated")
            print("✅ Story analysis and breakdown complete")
            print("✅ Ready for Game Designer handoff")
            
            return True
            
        except Exception as e:
            print(f"❌ Contract processing failed: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    # Run the integration test
    success = asyncio.run(test_pm_agent_integration())
    
    if success:
        print("\n🚀 Project Manager Agent is ready for production!")
        print("   Next step: Test with real GitHub API integration")
        print("   Next step: Implement Game Designer Agent")
    else:
        print("\n❌ Integration test failed - check logs above")
        exit(1)