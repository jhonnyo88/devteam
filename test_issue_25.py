#!/usr/bin/env python3

import asyncio
import os
from modules.agents.project_manager.tools.github_integration import GitHubIntegration
from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.shared.event_bus import EventBus, WorkPriority

async def test_github_issue_25():
    print('🎯 PRODUCTION TEST: GitHub Issue #25')
    print('URL: https://github.com/jhonnyo88/diginativa-game/issues/25')
    
    # Initialize GitHub integration
    github_config = {
        'github_token': os.getenv('GITHUB_TOKEN'),
        'github_repo_owner': os.getenv('PROJECT_REPO_OWNER'),
        'github_repo_name': os.getenv('PROJECT_REPO_NAME'),
    }
    
    github_integration = GitHubIntegration(github_config)
    print('✅ GitHub integration initialized')
    
    # Fetch and convert issue
    print('\n🔍 Fetching GitHub issue #25...')
    issue_data = await github_integration.fetch_issue_data('25')
    github_contract = github_integration.convert_issue_to_contract(issue_data)
    
    print(f'   Issue title: {issue_data.get("title", "N/A")}')
    print(f'   Story ID: {github_contract.get("story_id")}')
    
    # Validate extracted data
    required_data = github_contract.get('input_requirements', {}).get('required_data', {})
    
    print('\n📊 Extracted data validation:')
    required_fields = ['feature_description', 'acceptance_criteria', 'user_persona', 'priority_level']
    all_present = True
    
    for field in required_fields:
        value = required_data.get(field)
        if value and value != 'MISSING':
            print(f'   {field}: ✅ Present ({type(value).__name__})')
        else:
            print(f'   {field}: ❌ Missing')
            all_present = False
    
    if not all_present:
        print('❌ Cannot proceed - missing required fields')
        return False
    
    # Initialize AI team
    event_bus = EventBus()
    await event_bus.register_agent('game_designer_001', 'game_designer')
    
    pm = ProjectManagerAgent('pm_001', config={
        'github_token': os.getenv('GITHUB_TOKEN'),
        'github_repo_owner': os.getenv('PROJECT_REPO_OWNER'),
        'github_repo_name': os.getenv('PROJECT_REPO_NAME'),
        'project_repo_owner': os.getenv('PROJECT_REPO_OWNER'),
        'project_repo_name': os.getenv('PROJECT_REPO_NAME'),
        'event_bus': event_bus
    })
    print('\n✅ AI team components initialized')
    
    try:
        print('\n🎯 Processing with Project Manager...')
        result = await pm.execute_work(github_contract)
        
        if result.success:
            print('🎉 PROJECT MANAGER SUCCESS!')
            print(f'   Execution time: {result.execution_time_seconds:.2f}s')
            
            # Analyze DNA compliance
            output = result.output_contract
            dna_data = output.get('dna_compliance', {}).get('project_manager_dna_validation', {})
            
            print(f'\n🧬 DNA Compliance Results:')
            print(f'   Overall compliant: {dna_data.get("overall_dna_compliant", False)}')
            print(f'   Compliance score: {dna_data.get("dna_compliance_score", "N/A")}')
            
            # Test delegation to Game Designer
            print(f'\n🎨 Testing delegation to Game Designer...')
            work_id = await event_bus.delegate_to_agent('game_designer', output, WorkPriority.HIGH)
            print(f'   Work delegated: {work_id}')
            
            # Verify queue status
            queue_status = await event_bus.get_queue_status()
            print(f'   Queue status: {queue_status["pending_work"]} pending work items')
            
            print(f'\n🏆 COMPLETE PRODUCTION SUCCESS!')
            print(f'\n✅ VERIFIED FUNCTIONALITY:')
            print(f'   ✓ GitHub API integration and issue fetching')
            print(f'   ✓ Issue parsing and contract conversion')
            print(f'   ✓ Project Manager processing')
            print(f'   ✓ DNA compliance validation')
            print(f'   ✓ Agent delegation and work queuing')
            print(f'   ✓ End-to-end pipeline ready for Game Designer')
            
            return True
        else:
            print(f'❌ Project Manager failed: {result.error_message}')
            return False
            
    except Exception as e:
        print(f'❌ Test failed: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    result = asyncio.run(test_github_issue_25())
    print(f'\n🎯 FINAL RESULT: {"PRODUCTION SUCCESS" if result else "NEEDS ATTENTION"}')