#!/usr/bin/env python3
"""
Test Project Manager Agent with Real Feature Request
Test the complete PM workflow with our first revenue feature.
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.shared.exceptions import BusinessLogicError, DNAComplianceError


class MockGitHubIssue:
    """Mock GitHub issue data for testing."""
    
    @staticmethod
    def get_user_registration_issue():
        """Get mock issue data for user registration feature."""
        return {
            "number": 1001,
            "title": "[FEATURE] Secure User Registration System for Municipal Training Platform",
            "body": """# 🎯 Feature Request for DigiNativa

## 📋 Feature Description
**Brief description of the feature:**
Implement a secure user registration system that allows municipal employees to create accounts for the DigiNativa training platform with proper role-based access control.

**Detailed description:**
The user registration system should enable Swedish municipal employees to register for comprehensive pedagogical training accounts with their work email addresses. The system integrates with municipal HR systems, validates against approved government domains, and creates personalized learning pathways based on department and role. The registration process itself serves as the first learning experience, teaching employees about digital security, GDPR compliance, and their role in municipal service delivery. Users complete a guided onboarding that connects their daily work responsibilities to broader municipal goals while setting up their professional development profile.

## 👥 Target User
**Primary Persona:** Anna (Municipal Training Coordinator)
**Alternative Persona:** Municipal employees across all departments

## 🎓 Learning Objectives
- [ ] Understand proper municipal account setup procedures
- [ ] Learn about role-based access to training materials
- [ ] Practice secure password creation and account management
- [ ] Familiarize with GDPR consent and data handling policies

## ✅ Acceptance Criteria
- [ ] User can register with valid municipal email address (@kommun.se domains)
- [ ] System validates email domain against approved municipal domains list
- [ ] Registration form captures: name, email, department, role, municipality
- [ ] System sends email verification link within 2 minutes
- [ ] User can verify email and activate account within 24 hours
- [ ] Profile setup includes accessibility preferences and learning goals
- [ ] System assigns appropriate role permissions based on department
- [ ] Registration process completes within 3 minutes for typical user
- [ ] GDPR consent is properly captured and documented
- [ ] System rejects invalid/non-municipal email addresses with clear messaging
- [ ] Password requirements meet Swedish government security standards
- [ ] Feature works within 10 minutes completion time constraint

## ⏱️ Time Constraints
**Maximum completion time:** 10 minutes
**Target completion time:** 5 minutes for experienced municipal users

## 🏛️ Municipal Context
**Department:** HR, Education, Administration (all departments)
**Use case scenario:** 
Anna coordinates comprehensive professional development for Stockholm municipality's 45,000 employees. She needs a registration system that not only provides platform access but also educates employees about their role in municipal service excellence. The system must integrate with existing municipal workflows, respect employee time constraints, and provide immediate value by connecting individual learning goals to departmental objectives and citizen service improvements.

**Policy alignment:**
- Swedish GDPR implementation (UAVV)
- Government security guidelines for user authentication
- Municipal employment verification procedures
- Accessibility requirements per DOS (Diskrimineringsombudsmannen)

## 🎮 Game Design Requirements
**Interaction type:** Progressive learning journey with gamified milestones
**Pedagogical approach:** Constructivist learning through guided discovery of municipal service connections
**Difficulty level:** Beginner (adaptive to all technical skill levels with professional municipal context)

## 📊 Success Metrics
- User completion rate: >95%
- User satisfaction score: >4.2/5.0
- Average completion time: <5 minutes
- Email verification rate: >90% within 24 hours
- Support ticket reduction: 80% fewer registration-related issues

## 🚨 Priority Justification
**Why is this important?**
This foundational feature transforms routine account creation into meaningful professional development. By integrating holistic municipal service principles into the registration process, employees immediately understand how their learning connects to citizen service excellence. The system respects busy municipal professionals' time while establishing a culture of continuous improvement that supports both individual growth and organizational effectiveness.

**Urgency level:** High - Required foundation enabling municipal service excellence through learning
""",
            "labels": [
                {"name": "feature-request"},
                {"name": "priority-high"}
            ],
            "user": {"login": "johan-municipal-coordinator"},
            "html_url": "https://github.com/digitativa/devteam/issues/1001",
            "created_at": datetime.now().isoformat(),
            "assignees": [],
            "milestone": None,
            "comments_data": []
        }


async def test_pm_agent_processing():
    """Test PM agent with real feature request."""
    
    print("🎯 Testing Project Manager Agent with First Revenue Feature")
    print("=" * 60)
    
    try:
        # Initialize PM agent with mock config
        print("1. Initializing Project Manager Agent...")
        mock_config = {
            "github_token": "test_token",
            "github_repo_owner": "digitativa", 
            "github_repo_name": "devteam"
        }
        pm_agent = ProjectManagerAgent(config=mock_config)
        print("✅ PM Agent initialized successfully")
        
        # Get mock issue data
        print("\n2. Preparing GitHub issue data...")
        issue_data = MockGitHubIssue.get_user_registration_issue()
        print(f"✅ Mock issue created: #{issue_data['number']}")
        print(f"   Title: {issue_data['title']}")
        
        # Convert issue to contract
        print("\n3. Converting GitHub issue to PM contract...")
        # Mock the GitHub API dependency by calling convert_issue_to_contract directly
        pm_contract = pm_agent.github_integration.convert_issue_to_contract(issue_data)
        print("✅ Contract created successfully")
        print(f"   Story ID: {pm_contract['story_id']}")
        print(f"   Source Agent: {pm_contract['source_agent']}")
        print(f"   Target Agent: {pm_contract['target_agent']}")
        
        # Validate contract
        print("\n4. Validating contract compliance...")
        validation_result = pm_agent.contract_validator.validate_contract(pm_contract)
        if validation_result.is_valid:
            print("✅ Contract validation passed")
        else:
            print("❌ Contract validation failed:")
            for error in validation_result.errors:
                print(f"   - {error}")
            return False
        
        # Process contract through PM agent
        print("\n5. Processing contract through PM Agent...")
        pm_result = await pm_agent.process_contract(pm_contract)
        print("✅ PM processing completed successfully")
        print(f"   Output target: {pm_result['target_agent']}")
        print(f"   Story breakdown: {len(pm_result['input_requirements']['required_data']['story_breakdown'])} components")
        
        # Display key results
        print("\n6. PM Analysis Results:")
        required_data = pm_result['input_requirements']['required_data']
        
        # Debug: Show actual keys
        print(f"   🔍 Available data keys: {list(required_data.keys())}")
        
        # Show what we can display
        if 'complexity_assessment' in required_data:
            print(f"   📊 Feature Analysis:")
            complexity = required_data['complexity_assessment']
            print(f"      - Complexity Score: {complexity.get('overall_complexity', 'Not specified')}")
            print(f"      - Estimated Hours: {complexity.get('estimated_hours', 'Not specified')}")
            print(f"      - Risk Level: {complexity.get('risk_level', 'Not specified')}")
        
        if 'dna_analysis' in required_data:
            print(f"   🎯 DNA Compliance:")
            dna_scores = required_data['dna_analysis']
            if 'design_principles' in dna_scores:
                dp = dna_scores['design_principles']
                print(f"      - Pedagogical Value: {dp.get('pedagogical_value', 'N/A')}/5.0")
                print(f"      - Policy to Practice: {dp.get('policy_to_practice', 'N/A')}/5.0")
                print(f"      - Time Respect: {dp.get('time_respect', 'N/A')}/5.0")
            print(f"      - Overall DNA Score: {dna_scores.get('overall_score', 'N/A')}/5.0")
        
        if 'story_breakdown' in required_data:
            print(f"   📋 Story Breakdown:")
            story_components = required_data['story_breakdown']
            if isinstance(story_components, list):
                for i, component in enumerate(story_components[:3], 1):
                    if isinstance(component, dict):
                        print(f"      {i}. {component.get('component_name', 'Unknown')} ({component.get('component_type', 'Unknown')})")
                    else:
                        print(f"      {i}. {component}")
            else:
                print(f"      Story breakdown format: {type(story_components)}")
        
        # Save results for next agent
        output_file = project_root / "pm_test_output.json"
        with open(output_file, 'w') as f:
            json.dump(pm_result, f, indent=2, default=str)
        print(f"\n7. Results saved to: {output_file}")
        
        print("\n🎉 PM Agent Test SUCCESSFUL!")
        print("Ready to hand off to Game Designer Agent...")
        
        return pm_result
        
    except Exception as e:
        print(f"\n❌ PM Agent Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test function."""
    
    print("🚀 DigiNativa AI Team - First Revenue Feature Test")
    print("Testing: Secure User Registration System")
    print("=" * 60)
    
    # Test PM Agent
    pm_result = await test_pm_agent_processing()
    
    if pm_result:
        print("\n✅ Phase 1 COMPLETE: Project Manager Agent")
        print("🔄 Next: Game Designer Agent")
        print("\nTo continue testing:")
        print("1. Review pm_test_output.json")
        print("2. Run Game Designer with this output")
        print("3. Continue through all 6 agents")
    else:
        print("\n❌ Phase 1 FAILED: Project Manager Agent")
        print("Fix issues before proceeding to next agent")


if __name__ == "__main__":
    asyncio.run(main())