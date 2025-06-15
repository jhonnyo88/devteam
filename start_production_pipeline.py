#!/usr/bin/env python3
"""
DigiNativa AI Team Production Pipeline Starter

This script starts the AI team to process a real GitHub issue through
the complete development pipeline, from issue analysis to delivered code.

USAGE:
    python start_production_pipeline.py https://github.com/owner/repo/issues/123

REQUIREMENTS:
    - GITHUB_TOKEN environment variable
    - GITHUB_REPO_OWNER environment variable  
    - GITHUB_REPO_NAME environment variable
    - Access to the project repository where code will be delivered
"""

import asyncio
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
import argparse

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from modules.agents.project_manager.agent import ProjectManagerAgent
from modules.shared.event_bus import EventBus
from modules.shared.exceptions import DNAComplianceError, BusinessLogicError

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'production_pipeline_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def validate_environment() -> bool:
    """Validate required environment variables."""
    required_vars = [
        'GITHUB_TOKEN',
        'PROJECT_REPO_OWNER', 
        'PROJECT_REPO_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   {var}")
        print()
        print("💡 Setup instructions:")
        print("   export GITHUB_TOKEN='your_github_token'")
        print("   export PROJECT_REPO_OWNER='your_github_username'")
        print("   export PROJECT_REPO_NAME='your_project_repo_name'")
        return False
    
    return True


def validate_github_url(url: str) -> bool:
    """Validate GitHub issue URL format."""
    if not url.startswith('https://github.com/'):
        print(f"❌ Invalid GitHub URL: {url}")
        print("💡 Expected format: https://github.com/owner/repo/issues/123")
        return False
    
    if '/issues/' not in url:
        print(f"❌ URL must be a GitHub issue: {url}")
        print("💡 Expected format: https://github.com/owner/repo/issues/123")
        return False
    
    return True


async def start_production_pipeline(github_issue_url: str, config: dict) -> bool:
    """
    Start the production pipeline for a GitHub issue.
    
    Args:
        github_issue_url: URL to the GitHub issue
        config: Configuration dictionary
        
    Returns:
        True if pipeline started successfully
    """
    print("🚀 DigiNativa AI Team - Production Pipeline")
    print("=" * 50)
    print(f"⏰ Started at: {datetime.now().isoformat()}")
    print(f"📋 GitHub Issue: {github_issue_url}")
    print()
    
    try:
        # Initialize Project Manager Agent
        print("🤖 Initializing Project Manager Agent...")
        pm_agent = ProjectManagerAgent(config=config)
        print("✅ Project Manager Agent ready")
        
        # Initialize EventBus for monitoring
        event_bus = EventBus(config)
        print("📡 EventBus monitoring active")
        
        print()
        print("🔄 Starting Pipeline Execution...")
        print("-" * 30)
        
        # Process the GitHub issue
        print(f"📋 Processing GitHub issue: {github_issue_url}")
        result = await pm_agent.process_github_issue(github_issue_url)
        
        print()
        print("✅ PROJECT MANAGER COMPLETE!")
        print("-" * 30)
        
        story_id = result.get('story_id', 'N/A')
        target_agent = result.get('target_agent', 'N/A')
        
        print(f"📊 Story ID: {story_id}")
        print(f"🎯 Next Agent: {target_agent}")
        print(f"📈 DNA Compliance: {result.get('dna_compliance', {}).get('project_manager_dna_validation', {}).get('dna_compliance_score', 'N/A')}")
        
        # Check if we have story breakdown files
        output_specs = result.get('output_specifications', {})
        deliverable_files = output_specs.get('deliverable_files', [])
        
        if deliverable_files:
            print()
            print("📄 Generated Documents:")
            for file_path in deliverable_files:
                if Path(file_path).exists():
                    print(f"   ✅ {file_path}")
                else:
                    print(f"   ⏳ {file_path} (will be created)")
        
        print()
        print("🔄 NEXT STEPS:")
        print("1. Game Designer will process UX specifications")
        print("2. Developer will implement the feature")
        print("3. Test Engineer will create comprehensive tests")
        print("4. QA Tester will validate user experience")
        print("5. Quality Reviewer will prepare for your approval")
        
        print()
        print("📊 MONITORING:")
        print(f"   📁 Logs: {Path.cwd()}/production_pipeline_*.log")
        print(f"   📋 Story Files: docs/stories/{story_id}_*.md")
        print(f"   📈 Progress: Monitor EventBus events")
        
        print()
        print("⏱️ ESTIMATED TIMELINE:")
        print("   📋 Game Designer: 2-4 hours")
        print("   💻 Developer: 4-8 hours")
        print("   🧪 Test Engineer: 2-4 hours")
        print("   🔍 QA Tester: 1-2 hours")
        print("   ✅ Quality Reviewer: 1 hour")
        print("   📊 Total: 10-19 hours")
        
        print()
        print("🎯 SUCCESS! Pipeline started successfully")
        print("📬 You will receive a GitHub notification when ready for approval")
        
        return True
        
    except DNAComplianceError as e:
        print()
        print("❌ DNA COMPLIANCE FAILURE")
        print("-" * 25)
        print("The feature request does not meet DigiNativa's quality standards.")
        print()
        print("🚨 Issues found:")
        for error in str(e).split(','):
            print(f"   • {error.strip()}")
        
        print()
        print("💡 How to fix:")
        print("1. Update the GitHub issue with more pedagogical value")
        print("2. Ensure it serves Swedish municipal training needs")
        print("3. Add clear learning objectives") 
        print("4. Specify time constraints (target: 10 minutes)")
        print("5. Reference Anna persona needs")
        
        return False
        
    except BusinessLogicError as e:
        print()
        print("❌ BUSINESS LOGIC ERROR")
        print("-" * 22)
        print(f"Issue: {e}")
        print()
        print("💡 Common fixes:")
        print("1. Check issue has all required fields")
        print("2. Verify acceptance criteria are present")
        print("3. Ensure issue follows the template format")
        print("4. Check labels include 'feature-request'")
        
        return False
        
    except Exception as e:
        print()
        print("❌ PIPELINE STARTUP FAILED")
        print("-" * 25)
        print(f"Error: {e}")
        logger.error(f"Production pipeline failed: {e}", exc_info=True)
        
        print()
        print("🔧 Troubleshooting:")
        print("1. Check GitHub token permissions")
        print("2. Verify repository access")
        print("3. Ensure issue URL is accessible")
        print("4. Check logs for detailed error information")
        
        return False


async def monitor_pipeline_progress(story_id: str, config: dict) -> None:
    """Monitor pipeline progress for a story."""
    # This could be implemented to provide real-time updates
    # For now, it's a placeholder for future enhancement
    pass


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Start DigiNativa AI Team production pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python start_production_pipeline.py https://github.com/owner/repo/issues/123
  
Environment Variables:
  GITHUB_TOKEN        Your GitHub personal access token
  PROJECT_REPO_OWNER  Your GitHub username/organization
  PROJECT_REPO_NAME   Name of your project repository
  
For more info: https://docs.digitativa.se/ai-team/production-pipeline
        """
    )
    
    parser.add_argument(
        'github_issue_url',
        help='GitHub issue URL to process'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Validate setup without starting pipeline'
    )
    
    parser.add_argument(
        '--monitor',
        action='store_true', 
        help='Monitor existing pipeline progress'
    )
    
    args = parser.parse_args()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Validate GitHub URL
    if not validate_github_url(args.github_issue_url):
        sys.exit(1)
    
    # Configuration from environment
    config = {
        "github_token": os.getenv("GITHUB_TOKEN"),
        "github_repo_owner": os.getenv("PROJECT_REPO_OWNER"),
        "github_repo_name": os.getenv("PROJECT_REPO_NAME"),
        "environment": "production",
        "debug": False
    }
    
    if args.dry_run:
        print("✅ Environment validation passed")
        print("✅ GitHub URL format valid")
        print("🚀 Ready to start production pipeline!")
        sys.exit(0)
    
    # Start pipeline
    success = asyncio.run(start_production_pipeline(args.github_issue_url, config))
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()