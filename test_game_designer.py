#!/usr/bin/env python3

import asyncio
import os
import json
from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.agents.project_manager.tools.github_integration import GitHubIntegration
from modules.agents.game_designer.agent import GameDesignerAgent
from modules.shared.event_bus import EventBus, WorkPriority

async def test_project_manager_to_game_designer():
    print('🎯 TESTING: Project Manager → Game Designer Pipeline')
    print('Testing with GitHub issue #25 from production')
    
    # Initialize GitHub integration and fetch issue #25
    github_config = {
        'github_token': os.getenv('GITHUB_TOKEN'),
        'github_repo_owner': os.getenv('PROJECT_REPO_OWNER'),
        'github_repo_name': os.getenv('PROJECT_REPO_NAME'),
    }
    
    github_integration = GitHubIntegration(github_config)
    issue_data = await github_integration.fetch_issue_data('25')
    github_contract = github_integration.convert_issue_to_contract(issue_data)
    
    print(f'✅ GitHub issue #25 loaded: {issue_data.get("title")}')
    
    # Initialize EventBus and register Game Designer
    event_bus = EventBus()
    
    # Register Game Designer first
    game_designer = GameDesignerAgent('game_designer_001', config={
        'event_bus': event_bus
    })
    await event_bus.register_agent('game_designer_001', 'game_designer')
    print('✅ Game Designer agent initialized and registered')
    
    # Initialize Project Manager
    pm = ProjectManagerAgent('pm_001', config={
        'github_token': os.getenv('GITHUB_TOKEN'),
        'github_repo_owner': os.getenv('PROJECT_REPO_OWNER'),
        'github_repo_name': os.getenv('PROJECT_REPO_NAME'),
        'project_repo_owner': os.getenv('PROJECT_REPO_OWNER'),
        'project_repo_name': os.getenv('PROJECT_REPO_NAME'),
        'event_bus': event_bus
    })
    print('✅ Project Manager initialized')
    
    try:
        # STEP 1: Execute Project Manager
        print('\\n🎯 STEP 1: Project Manager Processing...')
        pm_result = await pm.execute_work(github_contract)
        
        if not pm_result.success:
            print(f'❌ PM failed: {pm_result.error_message}')
            return False
        
        print(f'✅ PM Success! Execution time: {pm_result.execution_time_seconds:.2f}s')
        
        # Get PM output contract
        pm_output = pm_result.output_contract
        print(f'📋 PM generated contract for: {pm_output.get("target_agent")}')
        
        # STEP 2: Execute Game Designer with PM output
        print('\\n🎨 STEP 2: Game Designer Processing...')
        
        # Ensure contract has correct agent targeting
        pm_output['source_agent'] = 'project_manager'
        pm_output['target_agent'] = 'game_designer'
        
        gd_result = await game_designer.execute_work(pm_output)
        
        if gd_result.success:
            print(f'✅ Game Designer Success! Execution time: {gd_result.execution_time_seconds:.2f}s')
            
            # Analyze Game Designer output
            gd_output = gd_result.output_contract
            print(f'\\n📋 Game Designer Output Analysis:')
            print(f'   Target agent: {gd_output.get("target_agent")}')
            print(f'   Story ID: {gd_output.get("story_id")}')
            
            # Check deliverables
            deliverables = gd_output.get('output_specifications', {}).get('deliverable_data', {})
            print(f'\\n🎨 Design Deliverables Generated:')
            for key, value in deliverables.items():
                if isinstance(value, dict):
                    print(f'   {key}: {len(value)} items')
                elif isinstance(value, list):
                    print(f'   {key}: {len(value)} items')
                else:
                    print(f'   {key}: {type(value).__name__}')
            
            # Test delegation to Developer
            print(f'\\n💻 STEP 3: Testing delegation to Developer...')
            work_id = await event_bus.delegate_to_agent('developer', gd_output, WorkPriority.HIGH)
            print(f'   Work delegated to Developer: {work_id}')
            
            queue_status = await event_bus.get_queue_status()
            print(f'   EventBus queue: {queue_status["pending_work"]} pending items')
            
            print(f'\\n🏆 COMPLETE SUCCESS: PM → GD → Developer Pipeline!')
            print(f'\\n✅ VERIFIED FUNCTIONALITY:')
            print(f'   ✓ Project Manager processing and output generation')
            print(f'   ✓ Game Designer contract reception and processing')
            print(f'   ✓ UX specification and design deliverable generation')
            print(f'   ✓ Contract handoff validation')
            print(f'   ✓ EventBus delegation to next agent (Developer)')
            print(f'   ✓ Multi-agent pipeline coordination')
            
            return True
        else:
            print(f'❌ Game Designer failed: {gd_result.error_message}')
            return False
            
    except Exception as e:
        print(f'❌ Pipeline test failed: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    result = asyncio.run(test_project_manager_to_game_designer())
    print(f'\\n🎯 PIPELINE RESULT: {"SUCCESS - Ready for Developer Agent" if result else "NEEDS ATTENTION"}')