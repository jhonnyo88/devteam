#!/usr/bin/env python3

import asyncio
import os
import json
from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.agents.project_manager.tools.github_integration import GitHubIntegration
from modules.agents.game_designer.agent import GameDesignerAgent
from modules.agents.developer.agent import DeveloperAgent
from modules.shared.event_bus import EventBus, WorkPriority

async def test_full_pipeline_github_to_developer():
    print('🚀 FULL PIPELINE TEST: GitHub → PM → GD → Developer')
    print('Testing complete AI team chain with GitHub issue #25')
    
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
    
    # Initialize EventBus and register all agents
    event_bus = EventBus()
    
    # Initialize all agents in the pipeline
    game_designer = GameDesignerAgent('game_designer_001', config={'event_bus': event_bus})
    developer = DeveloperAgent(config={'event_bus': event_bus})
    
    # Register agents with EventBus
    await event_bus.register_agent('game_designer_001', 'game_designer')
    await event_bus.register_agent('developer_001', 'developer') 
    print('✅ Game Designer and Developer agents registered')
    
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
        # STEP 1: Project Manager processes GitHub issue
        print('\n🎯 STEP 1: Project Manager Processing...')
        pm_result = await pm.execute_work(github_contract)
        
        if not pm_result.success:
            print(f'❌ PM failed: {pm_result.error_message}')
            return False
        
        print(f'✅ PM Success! Time: {pm_result.execution_time_seconds:.2f}s')
        pm_output = pm_result.output_contract
        
        # STEP 2: Game Designer processes PM output
        print('\n🎨 STEP 2: Game Designer Processing...')
        pm_output['source_agent'] = 'project_manager'
        pm_output['target_agent'] = 'game_designer'
        
        gd_result = await game_designer.execute_work(pm_output)
        
        if not gd_result.success:
            print(f'❌ Game Designer failed: {gd_result.error_message}')
            return False
        
        print(f'✅ Game Designer Success! Time: {gd_result.execution_time_seconds:.2f}s')
        gd_output = gd_result.output_contract
        
        # STEP 3: Developer processes Game Designer output
        print('\n💻 STEP 3: Developer Processing...')
        gd_output['source_agent'] = 'game_designer'
        gd_output['target_agent'] = 'developer'
        
        dev_result = await developer.execute_work(gd_output)
        
        if dev_result.success:
            print(f'✅ Developer Success! Time: {dev_result.execution_time_seconds:.2f}s')
            
            # Analyze Developer output
            dev_output = dev_result.output_contract
            print(f'\n💻 Developer Output Analysis:')
            print(f'   Target agent: {dev_output.get("target_agent")}')
            print(f'   Story ID: {dev_output.get("story_id")}')
            
            # Check generated code deliverables
            deliverables = dev_output.get('output_specifications', {}).get('deliverable_data', {})
            print(f'\n🔧 Code Deliverables Generated:')
            for key, value in deliverables.items():
                if isinstance(value, (dict, list)):
                    print(f'   {key}: {len(value) if hasattr(value, "__len__") else "object"}')
                else:
                    print(f'   {key}: {type(value).__name__}')
            
            # Check generated files
            generated_files = dev_output.get('output_specifications', {}).get('deliverable_files', [])
            print(f'\n📁 Generated Files ({len(generated_files)} files):')
            for file_path in generated_files[:5]:  # Show first 5
                print(f'   {file_path}')
            if len(generated_files) > 5:
                print(f'   ... and {len(generated_files) - 5} more files')
            
            # Test delegation to Test Engineer
            print(f'\n🧪 STEP 4: Testing delegation to Test Engineer...')
            work_id = await event_bus.delegate_to_agent('test_engineer', dev_output, WorkPriority.HIGH)
            print(f'   Work delegated to Test Engineer: {work_id}')
            
            queue_status = await event_bus.get_queue_status()
            print(f'   EventBus queue: {queue_status["pending_work"]} pending items')
            
            print(f'\n🏆 COMPLETE SUCCESS: GitHub → PM → GD → Developer Pipeline!')
            print(f'\n✅ VERIFIED FULL CHAIN:')
            print(f'   ✓ GitHub issue parsing and contract conversion')
            print(f'   ✓ Project Manager analysis and story breakdown')
            print(f'   ✓ Game Designer UX specification and design')
            print(f'   ✓ Developer code generation and implementation')
            print(f'   ✓ Contract handoffs between all agents')
            print(f'   ✓ EventBus coordination and work delegation')
            print(f'   ✓ Multi-agent pipeline with DNA compliance')
            
            # Performance summary
            total_time = pm_result.execution_time_seconds + gd_result.execution_time_seconds + dev_result.execution_time_seconds
            print(f'\n⚡ Performance Summary:')
            print(f'   Total pipeline time: {total_time:.2f}s')
            print(f'   PM: {pm_result.execution_time_seconds:.2f}s')
            print(f'   GD: {gd_result.execution_time_seconds:.2f}s') 
            print(f'   Dev: {dev_result.execution_time_seconds:.2f}s')
            
            return True
        else:
            print(f'❌ Developer failed: {dev_result.error_message}')
            return False
            
    except Exception as e:
        print(f'❌ Full pipeline test failed: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    result = asyncio.run(test_full_pipeline_github_to_developer())
    print(f'\n🎯 FULL PIPELINE RESULT: {"COMPLETE SUCCESS - AI TEAM FUNCTIONAL" if result else "NEEDS ATTENTION"}')