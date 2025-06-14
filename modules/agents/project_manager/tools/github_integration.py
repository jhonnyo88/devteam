"""
GitHub Integration Tool for Project Manager Agent.

PURPOSE:
Handles all GitHub API interactions for the Project Manager Agent,
including issue fetching, parsing, and status updates.

CRITICAL IMPORTANCE:
- Primary source of feature requests from clients
- Ensures proper issue tracking and communication
- Maintains transparency with stakeholders
- Enables automated workflow triggers

REVENUE IMPACT:
Direct impact on revenue through:
- Faster response to client feature requests
- Improved client communication and transparency
- Reduced manual overhead in issue management
- Better requirements capture leading to higher satisfaction
"""

import os
import re
import requests
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse

from ....shared.exceptions import ExternalServiceError, BusinessLogicError


class GitHubIntegration:
    """
    GitHub API integration for Project Manager Agent.
    
    Handles fetching, parsing, and updating GitHub issues
    for the DigiNativa AI Team workflow.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize GitHub integration.
        
        Args:
            config: Configuration dictionary with GitHub settings
        """
        self.logger = logging.getLogger(f"{__name__}.GitHubIntegration")
        
        # Load configuration from environment and config
        self.github_token = self._get_github_token(config)
        self.repo_owner = self._get_repo_owner(config)
        self.repo_name = self._get_repo_name(config)
        self.api_timeout = config.get("api_timeout", 30) if config else 30
        
        # GitHub API configuration
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "DigiNativa-AI-Team/1.0"
        }
        
        # Rate limiting configuration
        self.rate_limit_remaining = 5000  # Default GitHub rate limit
        self.rate_limit_reset = None
        
        self.logger.info(f"GitHub integration initialized for {self.repo_owner}/{self.repo_name}")
    
    def _get_github_token(self, config: Optional[Dict[str, Any]]) -> str:
        """Get GitHub token from config or environment."""
        token = None
        
        if config and "github_token" in config:
            token = config["github_token"]
        else:
            token = os.getenv("GITHUB_TOKEN")
        
        if not token:
            raise ExternalServiceError(
                "GitHub token not found. Set GITHUB_TOKEN environment variable or provide in config.",
                service_name="GitHub",
                status_code=401
            )
        
        return token
    
    def _get_repo_owner(self, config: Optional[Dict[str, Any]]) -> str:
        """Get repository owner from config or environment."""
        owner = None
        
        if config and "github_repo_owner" in config:
            owner = config["github_repo_owner"]
        else:
            owner = os.getenv("GITHUB_REPO_OWNER")
        
        if not owner:
            raise ExternalServiceError(
                "GitHub repository owner not configured. Set GITHUB_REPO_OWNER environment variable.",
                service_name="GitHub"
            )
        
        return owner
    
    def _get_repo_name(self, config: Optional[Dict[str, Any]]) -> str:
        """Get repository name from config or environment."""
        name = None
        
        if config and "github_repo_name" in config:
            name = config["github_repo_name"]
        else:
            name = os.getenv("GITHUB_REPO_NAME")
        
        if not name:
            raise ExternalServiceError(
                "GitHub repository name not configured. Set GITHUB_REPO_NAME environment variable.",
                service_name="GitHub"
            )
        
        return name
    
    async def fetch_new_feature_requests(self) -> List[Dict[str, Any]]:
        """
        Fetch new feature requests from GitHub issues.
        
        Returns:
            List of feature request data dictionaries
            
        Raises:
            ExternalServiceError: If GitHub API request fails
        """
        try:
            self.logger.debug("Fetching new feature requests from GitHub")
            
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
            params = {
                "labels": "feature-request",
                "state": "open",
                "sort": "created",
                "direction": "desc",
                "per_page": 10  # Limit to avoid overwhelming the system
            }
            
            response = await self._make_github_request("GET", url, params=params)
            issues = response.json()
            
            # Parse each issue into feature request format
            feature_requests = []
            for issue in issues:
                try:
                    feature_request = self._parse_feature_request(issue)
                    feature_requests.append(feature_request)
                except Exception as e:
                    self.logger.warning(f"Failed to parse issue #{issue.get('number', 'unknown')}: {e}")
                    continue
            
            self.logger.info(f"Fetched {len(feature_requests)} feature requests")
            return feature_requests
            
        except requests.RequestException as e:
            raise ExternalServiceError(
                f"Failed to fetch feature requests from GitHub: {e}",
                service_name="GitHub",
                status_code=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None,
                retry_after=60  # Retry after 1 minute
            )
        except Exception as e:
            raise ExternalServiceError(
                f"Unexpected error fetching feature requests: {e}",
                service_name="GitHub"
            )
    
    async def fetch_issue_data(self, issue_url: str) -> Dict[str, Any]:
        """
        Fetch specific issue data from GitHub.
        
        Args:
            issue_url: GitHub issue URL or issue number
            
        Returns:
            Issue data dictionary
            
        Raises:
            ExternalServiceError: If issue cannot be fetched
            BusinessLogicError: If issue URL is invalid
        """
        try:
            # Extract issue number from URL or use directly
            issue_number = self._extract_issue_number(issue_url)
            
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}"
            response = await self._make_github_request("GET", url)
            
            issue_data = response.json()
            
            # Fetch comments for additional context
            comments_url = f"{url}/comments"
            comments_response = await self._make_github_request("GET", comments_url)
            issue_data["comments_data"] = comments_response.json()
            
            self.logger.debug(f"Fetched issue #{issue_number} data")
            return issue_data
            
        except requests.RequestException as e:
            raise ExternalServiceError(
                f"Failed to fetch issue {issue_url}: {e}",
                service_name="GitHub",
                status_code=getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            )
    
    def convert_issue_to_contract(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert GitHub issue data to standard input contract format.
        
        Args:
            issue_data: Raw GitHub issue data
            
        Returns:
            Standard input contract for Project Manager Agent
        """
        try:
            # Parse the issue into feature request format
            feature_request = self._parse_feature_request(issue_data)
            
            # Generate story ID
            story_id = f"STORY-GH-{issue_data['number']}"
            
            # Create standard input contract
            contract = {
                "contract_version": "1.0",
                "story_id": story_id,
                "source_agent": "github",
                "target_agent": "project_manager",
                "dna_compliance": {
                    "design_principles_validation": {
                        "pedagogical_value": True,  # Will be validated by PM Agent
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
                    "required_data": feature_request,
                    "required_validations": [
                        "github_issue_valid",
                        "feature_request_format_correct"
                    ]
                },
                "output_specifications": {
                    "deliverable_files": [
                        f"docs/stories/{story_id}_description.md",
                        f"docs/analysis/{story_id}_feature_analysis.json"
                    ],
                    "deliverable_data": {
                        "story_breakdown": "object",
                        "acceptance_criteria": ["string"],
                        "complexity_assessment": "object"
                    },
                    "validation_criteria": {}
                },
                "quality_gates": [
                    "github_issue_parsed_correctly",
                    "feature_request_data_complete"
                ],
                "handoff_criteria": [
                    "all_required_data_extracted",
                    "issue_format_validated"
                ]
            }
            
            self.logger.debug(f"Converted GitHub issue #{issue_data['number']} to contract")
            return contract
            
        except Exception as e:
            raise BusinessLogicError(
                f"Failed to convert GitHub issue to contract: {e}",
                business_rule="github_issue_conversion",
                context={"issue_number": issue_data.get("number"), "issue_title": issue_data.get("title")}
            )
    
    def _parse_feature_request(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse GitHub issue into standardized feature request format.
        
        Args:
            issue: Raw GitHub issue data
            
        Returns:
            Standardized feature request dictionary
        """
        try:
            # Extract basic information
            title = issue.get("title", "")
            body = issue.get("body", "")
            labels = [label["name"] for label in issue.get("labels", [])]
            
            # Extract priority from labels
            priority = self._extract_priority(labels)
            
            # Extract acceptance criteria from issue body
            acceptance_criteria = self._extract_acceptance_criteria(body)
            
            # Extract user persona (default to Anna for DigiNativa)
            user_persona = self._extract_user_persona(body, labels)
            
            # Extract time constraint
            time_constraint = self._extract_time_constraint(body)
            
            # Extract learning objectives
            learning_objectives = self._extract_learning_objectives(body)
            
            # Extract GDD section reference
            gdd_section = self._extract_gdd_section(body)
            
            # Build feature request
            feature_request = {
                "feature_description": f"{title}\n\n{body}",
                "acceptance_criteria": acceptance_criteria,
                "user_persona": user_persona,
                "priority_level": priority,
                "time_constraint_minutes": time_constraint,
                "learning_objectives": learning_objectives,
                "gdd_section_reference": gdd_section,
                "github_issue_url": issue.get("html_url", ""),
                "github_issue_number": issue.get("number"),
                "requested_by": issue.get("user", {}).get("login", "unknown"),
                "created_at": issue.get("created_at", datetime.now().isoformat()),
                "labels": labels,
                "assignees": [assignee["login"] for assignee in issue.get("assignees", [])],
                "milestone": issue.get("milestone", {}).get("title") if issue.get("milestone") else None
            }
            
            return feature_request
            
        except Exception as e:
            self.logger.error(f"Failed to parse feature request: {e}")
            raise BusinessLogicError(
                f"Invalid issue format: {e}",
                business_rule="github_issue_parsing",
                context={"issue_number": issue.get("number"), "issue_title": issue.get("title")}
            )
    
    def _extract_priority(self, labels: List[str]) -> str:
        """Extract priority level from issue labels."""
        priority_mapping = {
            "priority-critical": "critical",
            "priority-high": "high",
            "priority-medium": "medium",
            "priority-low": "low",
            "urgent": "high",
            "important": "medium"
        }
        
        for label in labels:
            if label.lower() in priority_mapping:
                return priority_mapping[label.lower()]
        
        return "medium"  # Default priority
    
    def _extract_acceptance_criteria(self, issue_body: str) -> List[str]:
        """
        Extract acceptance criteria from issue body.
        
        Looks for patterns like:
        ## Acceptance Criteria
        - [ ] Criterion 1
        - [ ] Criterion 2
        """
        criteria = []
        
        # Find acceptance criteria section
        criteria_pattern = r"##\s*Acceptance\s*Criteria\s*\n(.*?)(?=\n##|\n$|$)"
        match = re.search(criteria_pattern, issue_body, re.IGNORECASE | re.DOTALL)
        
        if match:
            criteria_text = match.group(1)
            
            # Extract individual criteria (lines starting with - [ ] or - [x])
            criteria_lines = re.findall(r"-\s*\[[x\s]\]\s*(.+)", criteria_text, re.IGNORECASE)
            criteria = [criterion.strip() for criterion in criteria_lines if criterion.strip()]
        
        # If no formal acceptance criteria found, try to extract from description
        if not criteria:
            # Look for bullet points in the description
            bullet_points = re.findall(r"^[-*]\s*(.+)$", issue_body, re.MULTILINE)
            if bullet_points:
                criteria = [point.strip() for point in bullet_points[:5]]  # Limit to first 5
        
        # Ensure we have at least some basic criteria
        if not criteria:
            criteria = [
                "Feature is implemented according to description",
                "Feature works correctly for Anna persona",
                "Feature can be completed within time constraints"
            ]
        
        return criteria
    
    def _extract_user_persona(self, issue_body: str, labels: List[str]) -> str:
        """Extract user persona from issue body or labels."""
        # Check labels first
        persona_labels = {
            "persona-anna": "Anna",
            "anna": "Anna",
            "teacher": "Anna",
            "educator": "Anna"
        }
        
        for label in labels:
            if label.lower() in persona_labels:
                return persona_labels[label.lower()]
        
        # Check issue body for persona mentions
        persona_pattern = r"(?:persona|user|target):\s*(\w+)"
        match = re.search(persona_pattern, issue_body, re.IGNORECASE)
        
        if match:
            return match.group(1).capitalize()
        
        # Default to Anna for DigiNativa
        return "Anna"
    
    def _extract_time_constraint(self, issue_body: str) -> int:
        """Extract time constraint from issue body."""
        # Look for time mentions in minutes
        time_patterns = [
            r"(\d+)\s*minutes?",
            r"(\d+)\s*mins?",
            r"max(?:imum)?\s*time:\s*(\d+)",
            r"time\s*limit:\s*(\d+)"
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, issue_body, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        # Default to 10 minutes for DigiNativa features
        return 10
    
    def _extract_learning_objectives(self, issue_body: str) -> List[str]:
        """Extract learning objectives from issue body."""
        objectives = []
        
        # Look for learning objectives section
        objectives_pattern = r"##\s*Learning\s*Objectives?\s*\n(.*?)(?=\n##|\n$|$)"
        match = re.search(objectives_pattern, issue_body, re.IGNORECASE | re.DOTALL)
        
        if match:
            objectives_text = match.group(1)
            objective_lines = re.findall(r"^[-*]\s*(.+)$", objectives_text, re.MULTILINE)
            objectives = [obj.strip() for obj in objective_lines if obj.strip()]
        
        return objectives
    
    def _extract_gdd_section(self, issue_body: str) -> str:
        """Extract Game Design Document section reference."""
        gdd_patterns = [
            r"GDD\s*[Ss]ection:\s*(.+)",
            r"Game\s*Design\s*Document:\s*(.+)",
            r"Reference:\s*(.+)"
        ]
        
        for pattern in gdd_patterns:
            match = re.search(pattern, issue_body, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_issue_number(self, issue_url: str) -> int:
        """Extract issue number from URL or convert string to int."""
        try:
            # If it's already a number, return it
            if isinstance(issue_url, int):
                return issue_url
            
            # If it's a string that looks like a number
            if issue_url.isdigit():
                return int(issue_url)
            
            # Extract from GitHub URL
            if "github.com" in issue_url:
                # Pattern: https://github.com/owner/repo/issues/123
                match = re.search(r"/issues/(\d+)", issue_url)
                if match:
                    return int(match.group(1))
            
            # Try to extract any number from the string
            numbers = re.findall(r"\d+", issue_url)
            if numbers:
                return int(numbers[-1])  # Take the last number found
            
            raise ValueError(f"Cannot extract issue number from: {issue_url}")
            
        except Exception as e:
            raise BusinessLogicError(
                f"Invalid issue identifier: {issue_url}",
                business_rule="github_issue_number_extraction",
                context={"provided_identifier": issue_url}
            )
    
    async def _make_github_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Make authenticated GitHub API request with error handling.
        
        Args:
            method: HTTP method (GET, POST, PATCH, etc.)
            url: GitHub API URL
            params: Query parameters
            data: Request body data
            
        Returns:
            Response object
            
        Raises:
            ExternalServiceError: If request fails
        """
        try:
            # Check rate limits before making request
            if self.rate_limit_remaining <= 10:
                self.logger.warning("GitHub API rate limit nearly exceeded")
            
            # Make the request
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=self.api_timeout
            )
            
            # Update rate limit tracking
            self.rate_limit_remaining = int(response.headers.get("X-RateLimit-Remaining", 5000))
            self.rate_limit_reset = response.headers.get("X-RateLimit-Reset")
            
            # Check for errors
            response.raise_for_status()
            
            return response
            
        except requests.Timeout:
            raise ExternalServiceError(
                f"GitHub API request timed out after {self.api_timeout} seconds",
                service_name="GitHub",
                retry_after=30
            )
        except requests.HTTPError as e:
            status_code = e.response.status_code
            
            if status_code == 401:
                raise ExternalServiceError(
                    "GitHub authentication failed. Check GITHUB_TOKEN.",
                    service_name="GitHub",
                    status_code=401
                )
            elif status_code == 403:
                raise ExternalServiceError(
                    "GitHub API rate limit exceeded or access forbidden.",
                    service_name="GitHub",
                    status_code=403,
                    retry_after=3600  # Retry after 1 hour
                )
            elif status_code == 404:
                raise ExternalServiceError(
                    "GitHub resource not found. Check repository and permissions.",
                    service_name="GitHub",
                    status_code=404
                )
            else:
                raise ExternalServiceError(
                    f"GitHub API error: {e}",
                    service_name="GitHub",
                    status_code=status_code
                )
        except requests.RequestException as e:
            raise ExternalServiceError(
                f"GitHub API request failed: {e}",
                service_name="GitHub"
            )
    
    async def update_issue_status(
        self,
        issue_number: int,
        status: str,
        comment: Optional[str] = None
    ) -> bool:
        """
        Update GitHub issue with processing status.
        
        Args:
            issue_number: GitHub issue number
            status: Status label to add
            comment: Optional comment to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Add comment if provided
            if comment:
                await self._add_issue_comment(issue_number, comment)
            
            # Add status label
            await self._add_issue_label(issue_number, f"status-{status}")
            
            self.logger.debug(f"Updated issue #{issue_number} status to: {status}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update issue #{issue_number} status: {e}")
            return False
    
    async def _add_issue_comment(self, issue_number: int, comment: str) -> bool:
        """Add comment to GitHub issue."""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/comments"
            data = {"body": comment}
            
            await self._make_github_request("POST", url, data=data)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add comment to issue #{issue_number}: {e}")
            return False
    
    async def _add_issue_label(self, issue_number: int, label: str) -> bool:
        """Add label to GitHub issue."""
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues/{issue_number}/labels"
            data = {"labels": [label]}
            
            await self._make_github_request("POST", url, data=data)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add label to issue #{issue_number}: {e}")
            return False
    
    async def create_approval_request_issue(
        self,
        story_id: str,
        feature_data: Dict[str, Any],
        quality_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create GitHub issue for project owner approval.
        
        Args:
            story_id: Story ID of the completed feature
            feature_data: Feature information and requirements
            quality_metrics: Quality analysis results
            
        Returns:
            Created issue data
        """
        try:
            # Generate approval request body
            approval_body = self._generate_approval_request_body(
                story_id, feature_data, quality_metrics
            )
            
            # Create issue data
            issue_data = {
                "title": f"[APPROVAL] {feature_data.get('feature_title', 'Feature')} - {story_id}",
                "body": approval_body,
                "labels": ["feature-approval", "awaiting-decision", f"story-{story_id}"],
                "assignees": [self._get_project_owner()]
            }
            
            # Create the issue
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
            response = await self._make_github_request("POST", url, data=issue_data)
            
            created_issue = response.json()
            self.logger.info(f"Created approval request issue #{created_issue['number']} for {story_id}")
            
            return created_issue
            
        except Exception as e:
            raise ExternalServiceError(
                f"Failed to create approval request issue for {story_id}: {e}",
                service_name="GitHub"
            )
    
    async def fetch_approval_decisions(self) -> List[Dict[str, Any]]:
        """
        Fetch approval decisions from GitHub issues.
        
        Returns:
            List of approval decision issues
        """
        try:
            url = f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/issues"
            params = {
                "labels": "feature-approval",
                "state": "open",
                "sort": "updated",
                "direction": "desc",
                "per_page": 20
            }
            
            response = await self._make_github_request("GET", url, params=params)
            issues = response.json()
            
            # Filter for issues with actual decisions
            approval_decisions = []
            for issue in issues:
                if self._has_approval_decision(issue):
                    approval_decisions.append(issue)
            
            self.logger.debug(f"Fetched {len(approval_decisions)} approval decisions")
            return approval_decisions
            
        except Exception as e:
            raise ExternalServiceError(
                f"Failed to fetch approval decisions: {e}",
                service_name="GitHub"
            )
    
    def _generate_approval_request_body(
        self,
        story_id: str,
        feature_data: Dict[str, Any],
        quality_metrics: Dict[str, Any]
    ) -> str:
        """Generate approval request body with all necessary information."""
        
        template = f"""# 🎯 Feature Ready for Approval - {story_id}

Hej!

Feature **{feature_data.get('feature_title', 'Feature')}** has been completed and is ready for your review and approval.

## 📊 Delivery Summary
- **Story ID:** {story_id}
- **Completion Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **Overall Quality Score:** {quality_metrics.get('overall_score', 'N/A')}/100
- **Test Coverage:** {quality_metrics.get('test_coverage', 'N/A')}%

## 🎮 Feature Access
- **Staging URL:** {self._generate_staging_url(story_id)}
- **Demo Scenario:** {feature_data.get('demo_scenario', 'Standard user workflow')}

## ✅ Original Acceptance Criteria
{self._format_acceptance_criteria(feature_data.get('acceptance_criteria', []))}

## 📈 Quality Metrics Achieved
- **Performance:** API {quality_metrics.get('api_response_time', 'N/A')}ms, Lighthouse {quality_metrics.get('lighthouse_score', 'N/A')}/100
- **Accessibility:** WCAG AA {quality_metrics.get('accessibility_score', 'N/A')}% compliant  
- **User Experience:** {quality_metrics.get('ux_score', 'N/A')}/5.0 for Anna persona
- **DNA Compliance:** {quality_metrics.get('dna_compliance_score', 'N/A')}/5.0

## ✅ Approval Process
Please create an **Approval Issue** using our template to provide your decision:
- Use template: [Feature Approval](.github/ISSUE_TEMPLATE/feature_approval.md)
- Reference this delivery with Story ID: {story_id}
- Provide detailed feedback if rejected

## ⏱️ Response Timeline
- **Target Response:** Within 48 hours
- **Automatic Reminder:** After 24 hours if no response

Tack så mycket!

Mvh,
DigiNativa AI Team (Project Manager)"""
        
        return template
    
    def _get_project_owner(self) -> str:
        """Get project owner GitHub username."""
        # This could be configured or extracted from environment
        return os.getenv("GITHUB_PROJECT_OWNER", "project-owner")
    
    def _generate_staging_url(self, story_id: str) -> str:
        """Generate staging URL for feature testing."""
        base_staging_url = os.getenv("STAGING_BASE_URL", "https://staging.digitativa.se")
        return f"{base_staging_url}/features/{story_id.lower()}"
    
    def _format_acceptance_criteria(self, criteria: List[str]) -> str:
        """Format acceptance criteria for display."""
        if not criteria:
            return "No specific acceptance criteria provided"
        
        formatted = []
        for i, criterion in enumerate(criteria, 1):
            formatted.append(f"{i}. {criterion}")
        
        return "\n".join(formatted)
    
    def _has_approval_decision(self, issue: Dict[str, Any]) -> bool:
        """Check if issue contains an approval decision."""
        body = issue.get("body", "")
        
        # Look for checked approval boxes
        decision_patterns = [
            r"- \[x\] \*\*APPROVED\*\*",
            r"- \[x\] \*\*REJECTED\*\*", 
            r"- \[x\] \*\*APPROVED WITH MINOR ISSUES\*\*"
        ]
        
        return any(re.search(pattern, body, re.IGNORECASE) for pattern in decision_patterns)
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Get current GitHub API rate limit status.
        
        Returns:
            Rate limit status dictionary
        """
        return {
            "remaining_requests": self.rate_limit_remaining,
            "rate_limit_reset": self.rate_limit_reset,
            "rate_limit_exceeded": self.rate_limit_remaining <= 0
        }