"""
Tests for GitHub Integration tool.

Tests GitHub API interactions, issue parsing,
and contract conversion functionality.
"""

import pytest
import json
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import requests
from datetime import datetime

from modules.agents.project_manager.tools.github_integration import GitHubIntegration
from modules.shared.exceptions import ExternalServiceError, BusinessLogicError


class TestGitHubIntegration:
    """Test suite for GitHub Integration tool."""

    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        return {
            "github_token": "test_token_123",
            "github_repo_owner": "jhonnyo88",
            "github_repo_name": "devteam",
            "api_timeout": 30
        }

    @pytest.fixture
    def sample_github_issue(self):
        """Sample GitHub issue data."""
        return {
            "number": 123,
            "title": "Add interactive policy practice scenarios",
            "body": """## Feature Description
As Anna, I want to practice policy application through interactive scenarios so that I can better understand real-world implementation.

## Acceptance Criteria
- [ ] User can select from multiple policy scenarios
- [ ] Each scenario provides clear context and background
- [ ] User receives immediate feedback on decisions
- [ ] Progress is tracked and saved
- [ ] Feature completes within 10 minutes

## Learning Objectives
- Apply policy knowledge to practical situations
- Understand decision-making frameworks
- Practice critical thinking in policy context

## Time Constraint
Maximum time: 10 minutes

GDD Section: Section 3.2 - Interactive Learning""",
            "state": "open",
            "labels": [
                {"name": "feature-request"},
                {"name": "priority-high"},
                {"name": "persona-anna"}
            ],
            "assignees": [
                {"login": "developer1"}
            ],
            "milestone": {
                "title": "Q1 Features"
            },
            "user": {
                "login": "client_user"
            },
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "html_url": "https://github.com/jhonnyo88/diginativa-game/issues/123",
            "comments_data": []
        }

    @pytest.fixture
    def github_integration(self, mock_config):
        """Create GitHub integration instance."""
        with patch.dict('os.environ', {
            'GITHUB_TOKEN': 'test_token_123',
            'GITHUB_REPO_OWNER': 'jhonnyo88',
            'GITHUB_REPO_NAME': 'devteam'
        }):
            return GitHubIntegration(mock_config)

    # ==========================================
    # INITIALIZATION TESTS
    # ==========================================

    def test_github_integration_initialization_success(self, mock_config):
        """Test successful GitHub integration initialization."""
        with patch.dict('os.environ', {
            'GITHUB_TOKEN': 'test_token_123',
            'GITHUB_REPO_OWNER': 'jhonnyo88', 
            'GITHUB_REPO_NAME': 'devteam'
        }):
            integration = GitHubIntegration(mock_config)
            
            assert integration.github_token == "test_token_123"
            assert integration.repo_owner == "jhonnyo88"
            assert integration.repo_name == "devteam"
            assert integration.api_timeout == 30

    def test_github_integration_missing_token(self):
        """Test initialization with missing GitHub token."""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ExternalServiceError) as exc_info:
                GitHubIntegration()
            
            assert "GitHub token not found" in str(exc_info.value)

    def test_github_integration_missing_repo_owner(self):
        """Test initialization with missing repository owner."""
        config = {
            "github_token": "test_token_123",
            "github_repo_name": "devteam"
            # Missing github_repo_owner
        }
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ExternalServiceError) as exc_info:
                GitHubIntegration(config)
            
            assert "GitHub repository owner not configured" in str(exc_info.value)

    def test_github_integration_from_config(self):
        """Test initialization using config parameters."""
        config = {
            "github_token": "config_token",
            "github_repo_owner": "config_owner",
            "github_repo_name": "config_repo"
        }
        
        integration = GitHubIntegration(config)
        
        assert integration.github_token == "config_token"
        assert integration.repo_owner == "config_owner"
        assert integration.repo_name == "config_repo"

    # ==========================================
    # ISSUE FETCHING TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_fetch_new_feature_requests_success(self, github_integration, sample_github_issue):
        """Test successful feature requests fetching."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = [sample_github_issue]
        mock_response.headers = {
            "X-RateLimit-Remaining": "4999",
            "X-RateLimit-Reset": "1640995200"
        }
        
        with patch.object(github_integration, '_make_github_request', return_value=mock_response):
            feature_requests = await github_integration.fetch_new_feature_requests()
            
            assert len(feature_requests) == 1
            assert feature_requests[0]["feature_description"].startswith("Add interactive policy practice scenarios")
            assert feature_requests[0]["priority_level"] == "high"
            assert feature_requests[0]["user_persona"] == "Anna"

    @pytest.mark.asyncio
    async def test_fetch_new_feature_requests_api_error(self, github_integration):
        """Test feature requests fetching with API error."""
        with patch.object(github_integration, '_make_github_request', side_effect=ExternalServiceError("API Error", "GitHub")):
            with pytest.raises(ExternalServiceError):
                await github_integration.fetch_new_feature_requests()

    @pytest.mark.asyncio
    async def test_fetch_issue_data_success(self, github_integration, sample_github_issue):
        """Test successful issue data fetching."""
        # Mock issue response
        mock_issue_response = Mock()
        mock_issue_response.json.return_value = sample_github_issue
        
        # Mock comments response
        mock_comments_response = Mock()
        mock_comments_response.json.return_value = []
        
        with patch.object(github_integration, '_make_github_request', side_effect=[mock_issue_response, mock_comments_response]):
            issue_data = await github_integration.fetch_issue_data("123")
            
            assert issue_data["number"] == 123
            assert issue_data["title"] == "Add interactive policy practice scenarios"
            assert "comments_data" in issue_data

    @pytest.mark.asyncio
    async def test_fetch_issue_data_with_url(self, github_integration, sample_github_issue):
        """Test issue data fetching with GitHub URL."""
        mock_issue_response = Mock()
        mock_issue_response.json.return_value = sample_github_issue
        
        mock_comments_response = Mock()
        mock_comments_response.json.return_value = []
        
        with patch.object(github_integration, '_make_github_request', side_effect=[mock_issue_response, mock_comments_response]):
            issue_data = await github_integration.fetch_issue_data("https://github.com/jhonnyo88/diginativa-game/issues/123")
            
            assert issue_data["number"] == 123

    # ==========================================
    # ISSUE PARSING TESTS
    # ==========================================

    def test_parse_feature_request_complete_issue(self, github_integration, sample_github_issue):
        """Test parsing a complete GitHub issue."""
        feature_request = github_integration._parse_feature_request(sample_github_issue)
        
        assert "Add interactive policy practice scenarios" in feature_request["feature_description"]
        assert feature_request["priority_level"] == "high"
        assert feature_request["user_persona"] == "Anna"
        assert feature_request["time_constraint_minutes"] == 10
        assert len(feature_request["acceptance_criteria"]) == 5
        assert len(feature_request["learning_objectives"]) == 3
        assert feature_request["gdd_section_reference"] == "Section 3.2 - Interactive Learning"

    def test_parse_feature_request_minimal_issue(self, github_integration):
        """Test parsing a minimal GitHub issue."""
        minimal_issue = {
            "number": 456,
            "title": "Simple feature",
            "body": "Basic description",
            "labels": [],
            "assignees": [],
            "milestone": None,
            "user": {"login": "user123"},
            "created_at": "2024-01-15T10:30:00Z",
            "html_url": "https://github.com/owner/repo/issues/456"
        }
        
        feature_request = github_integration._parse_feature_request(minimal_issue)
        
        assert feature_request["feature_description"] == "Simple feature\n\nBasic description"
        assert feature_request["priority_level"] == "medium"  # Default
        assert feature_request["user_persona"] == "Anna"  # Default
        assert feature_request["time_constraint_minutes"] == 10  # Default
        assert len(feature_request["acceptance_criteria"]) >= 3  # Fallback criteria

    def test_extract_priority_from_labels(self, github_integration):
        """Test priority extraction from issue labels."""
        labels = ["feature-request", "priority-critical", "bug"]
        priority = github_integration._extract_priority(labels)
        assert priority == "critical"
        
        labels = ["feature-request", "urgent"]
        priority = github_integration._extract_priority(labels)
        assert priority == "high"
        
        labels = ["feature-request"]
        priority = github_integration._extract_priority(labels)
        assert priority == "medium"  # Default

    def test_extract_acceptance_criteria_from_body(self, github_integration):
        """Test acceptance criteria extraction from issue body."""
        body_with_criteria = """## Acceptance Criteria
- [ ] User can login
- [x] User can logout
- [ ] User receives confirmation

Some other text."""
        
        criteria = github_integration._extract_acceptance_criteria(body_with_criteria)
        
        assert len(criteria) == 3
        assert "User can login" in criteria
        assert "User can logout" in criteria
        assert "User receives confirmation" in criteria

    def test_extract_acceptance_criteria_fallback(self, github_integration):
        """Test acceptance criteria fallback when none found."""
        body_without_criteria = "Simple feature description without formal criteria."
        
        criteria = github_integration._extract_acceptance_criteria(body_without_criteria)
        
        assert len(criteria) >= 3  # Should have fallback criteria
        assert any("implemented according to description" in criterion for criterion in criteria)

    def test_extract_user_persona_from_labels(self, github_integration):
        """Test user persona extraction from labels."""
        labels = ["feature-request", "persona-anna", "priority-high"]
        persona = github_integration._extract_user_persona("", labels)
        assert persona == "Anna"
        
        labels = ["feature-request", "teacher"]
        persona = github_integration._extract_user_persona("", labels)
        assert persona == "Anna"

    def test_extract_user_persona_from_body(self, github_integration):
        """Test user persona extraction from body text."""
        body = "This feature is for persona: Teacher to help with education."
        persona = github_integration._extract_user_persona(body, [])
        assert persona == "Teacher"

    def test_extract_time_constraint_from_body(self, github_integration):
        """Test time constraint extraction from body text."""
        body = "This feature should complete in 15 minutes maximum."
        time_constraint = github_integration._extract_time_constraint(body)
        assert time_constraint == 15
        
        body = "Time limit: 5 mins for quick completion."
        time_constraint = github_integration._extract_time_constraint(body)
        assert time_constraint == 5
        
        body = "No time mentions here."
        time_constraint = github_integration._extract_time_constraint(body)
        assert time_constraint == 10  # Default

    def test_extract_learning_objectives_from_body(self, github_integration):
        """Test learning objectives extraction from body text."""
        body = """## Learning Objectives
- Learn policy application
- Understand decision making
- Practice critical thinking

Other content."""
        
        objectives = github_integration._extract_learning_objectives(body)
        
        assert len(objectives) == 3
        assert "Learn policy application" in objectives
        assert "Understand decision making" in objectives
        assert "Practice critical thinking" in objectives

    def test_extract_gdd_section_from_body(self, github_integration):
        """Test GDD section extraction from body text."""
        body = "This feature relates to GDD Section: 3.2 - Interactive Learning modules."
        gdd_section = github_integration._extract_gdd_section(body)
        assert gdd_section == "3.2 - Interactive Learning modules."  # Include period
        
        body = "Reference: Module 5 - Assessment Tools"
        gdd_section = github_integration._extract_gdd_section(body)
        assert gdd_section == "Module 5 - Assessment Tools"

    # ==========================================
    # CONTRACT CONVERSION TESTS
    # ==========================================

    def test_convert_issue_to_contract_success(self, github_integration, sample_github_issue):
        """Test successful issue to contract conversion."""
        contract = github_integration.convert_issue_to_contract(sample_github_issue)
        
        assert contract["contract_version"] == "1.0"
        assert contract["story_id"] == "STORY-GH-123"
        assert contract["source_agent"] == "github"
        assert contract["target_agent"] == "project_manager"
        
        # Verify DNA compliance structure
        assert "dna_compliance" in contract
        assert "design_principles_validation" in contract["dna_compliance"]
        assert "architecture_compliance" in contract["dna_compliance"]
        
        # Verify input requirements
        assert "input_requirements" in contract
        assert "required_data" in contract["input_requirements"]
        
        feature_data = contract["input_requirements"]["required_data"]
        assert feature_data["priority_level"] == "high"
        assert feature_data["user_persona"] == "Anna"

    def test_convert_issue_to_contract_failure(self, github_integration):
        """Test issue to contract conversion failure."""
        invalid_issue = {"invalid": "data"}
        
        with pytest.raises(BusinessLogicError) as exc_info:
            github_integration.convert_issue_to_contract(invalid_issue)
        
        assert "Failed to convert GitHub issue to contract" in str(exc_info.value)

    # ==========================================
    # ISSUE NUMBER EXTRACTION TESTS
    # ==========================================

    def test_extract_issue_number_from_integer(self, github_integration):
        """Test issue number extraction from integer."""
        issue_number = github_integration._extract_issue_number(123)
        assert issue_number == 123

    def test_extract_issue_number_from_string(self, github_integration):
        """Test issue number extraction from string."""
        issue_number = github_integration._extract_issue_number("456")
        assert issue_number == 456

    def test_extract_issue_number_from_url(self, github_integration):
        """Test issue number extraction from GitHub URL."""
        url = "https://github.com/owner/repo/issues/789"
        issue_number = github_integration._extract_issue_number(url)
        assert issue_number == 789

    def test_extract_issue_number_from_complex_string(self, github_integration):
        """Test issue number extraction from complex string."""
        string = "Issue #123 needs attention"
        issue_number = github_integration._extract_issue_number(string)
        assert issue_number == 123

    def test_extract_issue_number_failure(self, github_integration):
        """Test issue number extraction failure."""
        with pytest.raises(BusinessLogicError) as exc_info:
            github_integration._extract_issue_number("no numbers here")
        
        assert "Invalid issue identifier" in str(exc_info.value)

    # ==========================================
    # API REQUEST TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_make_github_request_success(self, github_integration):
        """Test successful GitHub API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Remaining": "4999",
            "X-RateLimit-Reset": "1640995200"
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.request', return_value=mock_response):
            response = await github_integration._make_github_request(
                "GET", 
                "https://api.github.com/repos/owner/repo/issues"
            )
            
            assert response.status_code == 200
            assert github_integration.rate_limit_remaining == 4999

    @pytest.mark.asyncio
    async def test_make_github_request_timeout(self, github_integration):
        """Test GitHub API request timeout."""
        with patch('requests.request', side_effect=requests.Timeout()):
            with pytest.raises(ExternalServiceError) as exc_info:
                await github_integration._make_github_request(
                    "GET",
                    "https://api.github.com/repos/owner/repo/issues"
                )
            
            assert "timed out" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_make_github_request_auth_error(self, github_integration):
        """Test GitHub API request authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        
        http_error = requests.HTTPError(response=mock_response)
        http_error.response = mock_response
        
        with patch('requests.request') as mock_request:
            mock_request.return_value.raise_for_status.side_effect = http_error
            
            with pytest.raises(ExternalServiceError) as exc_info:
                await github_integration._make_github_request(
                    "GET",
                    "https://api.github.com/repos/owner/repo/issues"
                )
            
            assert "authentication failed" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_make_github_request_rate_limit(self, github_integration):
        """Test GitHub API request rate limit error."""
        mock_response = Mock()
        mock_response.status_code = 403
        
        http_error = requests.HTTPError(response=mock_response)
        http_error.response = mock_response
        
        with patch('requests.request') as mock_request:
            mock_request.return_value.raise_for_status.side_effect = http_error
            
            with pytest.raises(ExternalServiceError) as exc_info:
                await github_integration._make_github_request(
                    "GET",
                    "https://api.github.com/repos/owner/repo/issues"
                )
            
            assert "rate limit" in str(exc_info.value).lower()

    # ==========================================
    # ISSUE STATUS UPDATE TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_update_issue_status_success(self, github_integration):
        """Test successful issue status update."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.headers = {"X-RateLimit-Remaining": "4999"}
        mock_response.raise_for_status.return_value = None
        
        with patch.object(github_integration, '_make_github_request', return_value=mock_response):
            result = await github_integration.update_issue_status(123, "in-progress", "Processing feature request")
            
            assert result is True

    @pytest.mark.asyncio
    async def test_update_issue_status_failure(self, github_integration):
        """Test issue status update failure."""
        with patch.object(github_integration, '_add_issue_comment', side_effect=Exception("API Error")):
            result = await github_integration.update_issue_status(123, "in-progress", "Test comment")
            
            assert result is False

    # ==========================================
    # RATE LIMIT TESTS
    # ==========================================

    def test_get_rate_limit_status(self, github_integration):
        """Test rate limit status reporting."""
        github_integration.rate_limit_remaining = 1000
        github_integration.rate_limit_reset = "1640995200"
        
        status = github_integration.get_rate_limit_status()
        
        assert status["remaining_requests"] == 1000
        assert status["rate_limit_reset"] == "1640995200"
        assert status["rate_limit_exceeded"] is False
        
        # Test rate limit exceeded
        github_integration.rate_limit_remaining = 0
        status = github_integration.get_rate_limit_status()
        assert status["rate_limit_exceeded"] is True

    @pytest.mark.asyncio
    async def test_rate_limit_warning(self, github_integration):
        """Test rate limit warning when approaching limit."""
        github_integration.rate_limit_remaining = 5  # Low remaining requests
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {
            "X-RateLimit-Remaining": "5",
            "X-RateLimit-Reset": "1640995200"
        }
        mock_response.raise_for_status.return_value = None
        
        with patch('requests.request', return_value=mock_response):
            with patch.object(github_integration.logger, 'warning') as mock_warning:
                await github_integration._make_github_request(
                    "GET",
                    "https://api.github.com/repos/owner/repo/issues"
                )
                
                mock_warning.assert_called_with("GitHub API rate limit nearly exceeded")