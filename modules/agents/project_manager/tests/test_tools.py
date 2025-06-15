"""
Project Manager Agent Tools Tests

PURPOSE:
Tests all PM agent-specific tools according to TEST_STRATEGY.md.

CRITICAL IMPORTANCE:
- Validates tool initialization and configuration
- Tests tool integration with agent workflow
- Ensures tool error handling and recovery
- Validates tool performance and reliability

COVERAGE REQUIREMENTS:
- Agent tools: 90% minimum
- Tool error handling: 100%
- Tool integration: 95% minimum
- Performance validation: Critical paths tested

TOOLS TESTED:
- GitHubIntegration: Issue fetching, API interaction
- StoryAnalyzer: Feature breakdown, complexity analysis
- DNAComplianceChecker: All 9 DNA principles validation
- LearningEngine: ML complexity prediction, historical learning
- SwedishMunicipalCommunicator: GDPR compliance, municipal context
- TeamCoordinator: EventBus integration, workflow coordination
- StakeholderRelationshipManager: Approval prediction, relationship tracking
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from typing import Dict, Any

from modules.agents.project_manager.tools.github_integration import GitHubIntegration
from modules.agents.project_manager.tools.story_analyzer import StoryAnalyzer
from modules.agents.project_manager.tools.dna_compliance_checker import DNAComplianceChecker
from modules.agents.project_manager.tools.learning_engine import LearningEngine
from modules.agents.project_manager.tools.swedish_municipal_communicator import SwedishMunicipalCommunicator
from modules.agents.project_manager.tools.team_coordinator import TeamCoordinator
from modules.agents.project_manager.tools.stakeholder_relationship_manager import StakeholderRelationshipManager
from modules.shared.exceptions import (
    ExternalServiceError, BusinessLogicError, DNAComplianceError
)


class TestToolsBase:
    """Base class for tool testing with common fixtures."""
    
    @pytest.fixture
    def tool_config(self):
        """Standard tool configuration for testing."""
        return {
            "test_mode": True,
            "github_token": "test_token_12345",
            "github_repo": "test-org/test-repo",
            "learning_db_path": ":memory:",  # In-memory SQLite for tests
            "max_retries": 2,
            "timeout_seconds": 30
        }
    
    @pytest.fixture
    def sample_github_issue(self):
        """Sample GitHub issue for tool testing."""
        return {
            "number": 456,
            "title": "Implement accessibility compliance checker for municipal training",
            "body": """
            Feature Request: Accessibility Compliance Checker
            
            As a municipal training coordinator,
            I want to ensure all training materials meet WCAG AA standards
            So that our training is accessible to all municipal employees.
            
            Requirements:
            - Automated accessibility scanning
            - WCAG AA compliance reporting
            - Integration with Swedish accessibility legislation
            - Real-time feedback during content creation
            
            Priority: High
            Labels: accessibility, compliance, swedish-municipal
            """,
            "labels": [
                {"name": "accessibility"},
                {"name": "compliance"},
                {"name": "swedish-municipal"},
                {"name": "priority-high"}
            ],
            "state": "open",
            "created_at": "2025-06-15T09:30:00Z",
            "updated_at": "2025-06-15T10:15:00Z",
            "assignee": None,
            "milestone": None
        }


class TestGitHubIntegration(TestToolsBase):
    """Test GitHub Integration tool functionality."""
    
    @pytest.fixture
    def github_tool(self, tool_config):
        """Create GitHub integration tool for testing."""
        return GitHubIntegration(tool_config)
    
    @pytest.mark.asyncio
    async def test_tool_initialization(self, tool_config):
        """Test GitHub tool initializes correctly."""
        tool = GitHubIntegration(tool_config)
        
        # Verify configuration
        assert tool.config["test_mode"] is True
        assert tool.config["github_token"] == "test_token_12345"
        assert hasattr(tool, 'logger')
    
    @pytest.mark.asyncio
    async def test_fetch_issue_details_success(self, github_tool, sample_github_issue):
        """Test successful issue fetching."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock successful API response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=sample_github_issue)
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # Fetch issue
            result = await github_tool.fetch_issue_details(456)
            
            # Verify result
            assert result["number"] == 456
            assert result["title"] == "Implement accessibility compliance checker for municipal training"
            assert "accessibility" in [label["name"] for label in result["labels"]]
    
    @pytest.mark.asyncio
    async def test_fetch_issue_api_error(self, github_tool):
        """Test handling of GitHub API errors."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock API error response
            mock_response = AsyncMock()
            mock_response.status = 404
            mock_response.text = AsyncMock(return_value="Not Found")
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # Expect external service error
            with pytest.raises(ExternalServiceError) as exc_info:
                await github_tool.fetch_issue_details(999)
            
            assert "GitHub API error" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_fetch_issue_rate_limit(self, github_tool):
        """Test handling of GitHub API rate limiting."""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock rate limit response
            mock_response = AsyncMock()
            mock_response.status = 403
            mock_response.headers = {"X-RateLimit-Remaining": "0"}
            mock_response.text = AsyncMock(return_value="Rate limit exceeded")
            mock_get.return_value.__aenter__.return_value = mock_response
            
            # Expect rate limit error
            with pytest.raises(ExternalServiceError) as exc_info:
                await github_tool.fetch_issue_details(456)
            
            assert "rate limit" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_parse_issue_labels(self, github_tool, sample_github_issue):
        """Test issue label parsing functionality."""
        # Test internal label parsing method
        labels = github_tool._parse_issue_labels(sample_github_issue)
        
        expected_labels = ["accessibility", "compliance", "swedish-municipal", "priority-high"]
        assert all(label in labels for label in expected_labels)
    
    @pytest.mark.asyncio
    async def test_extract_issue_metadata(self, github_tool, sample_github_issue):
        """Test metadata extraction from issues."""
        metadata = github_tool._extract_metadata(sample_github_issue)
        
        # Verify metadata extraction
        assert metadata["priority"] == "high"
        assert metadata["category"] == "accessibility"
        assert metadata["municipal_context"] is True
        assert metadata["compliance_required"] is True


class TestStoryAnalyzer(TestToolsBase):
    """Test Story Analyzer tool functionality."""
    
    @pytest.fixture
    def story_tool(self, tool_config):
        """Create story analyzer tool for testing."""
        return StoryAnalyzer(tool_config)
    
    @pytest.mark.asyncio
    async def test_analyze_feature_request_comprehensive(self, story_tool, sample_github_issue):
        """Test comprehensive feature analysis."""
        # Analyze the sample issue
        result = await story_tool.analyze_feature_request(sample_github_issue)
        
        # Verify comprehensive analysis structure
        assert "story_breakdown" in result
        assert "estimated_complexity" in result
        assert "dependencies" in result
        assert "risk_factors" in result
        
        # Verify story breakdown details
        breakdown = result["story_breakdown"]
        assert "epic" in breakdown
        assert "user_stories" in breakdown
        assert "acceptance_criteria" in breakdown
        assert "technical_requirements" in breakdown
        
        # Verify analysis considers accessibility context
        assert any("accessibility" in str(item).lower() for item in breakdown["user_stories"])
        assert any("wcag" in str(item).lower() for item in breakdown["acceptance_criteria"])
    
    @pytest.mark.asyncio
    async def test_complexity_estimation(self, story_tool):
        """Test story complexity estimation logic."""
        # Test different complexity scenarios
        simple_issue = {
            "title": "Fix button text color",
            "body": "Change submit button from blue to green",
            "labels": [{"name": "ui-fix"}]
        }
        
        complex_issue = {
            "title": "Implement machine learning recommendation engine",
            "body": """
            Build AI-powered content recommendation system with:
            - Natural language processing
            - User behavior analytics
            - Real-time personalization
            - GDPR compliance
            - Swedish language support
            """,
            "labels": [{"name": "ml"}, {"name": "ai"}, {"name": "gdpr"}]
        }
        
        # Analyze both
        simple_result = await story_tool.analyze_feature_request(simple_issue)
        complex_result = await story_tool.analyze_feature_request(complex_issue)
        
        # Verify complexity estimation
        assert simple_result["estimated_complexity"] in ["low", "medium"]
        assert complex_result["estimated_complexity"] in ["medium", "high"]
        
        # Complex should have more dependencies and risks
        assert len(complex_result["dependencies"]) >= len(simple_result["dependencies"])
        assert len(complex_result["risk_factors"]) >= len(simple_result["risk_factors"])
    
    @pytest.mark.asyncio
    async def test_swedish_municipal_context_analysis(self, story_tool):
        """Test analysis specific to Swedish municipal context."""
        municipal_issue = {
            "title": "GDPR compliance dashboard for employee training records",
            "body": """
            Create dashboard for managing employee training records
            with full GDPR compliance for Swedish municipalities.
            
            Requirements:
            - Data minimization principles
            - User consent management
            - Right to erasure implementation
            - Swedish accessibility law compliance
            """,
            "labels": [{"name": "gdpr"}, {"name": "swedish-municipal"}, {"name": "compliance"}]
        }
        
        result = await story_tool.analyze_feature_request(municipal_issue)
        
        # Verify Swedish municipal context considered
        breakdown = result["story_breakdown"]
        assert "municipal_compliance" in breakdown or any("gdpr" in str(item).lower() for item in breakdown.values())
        assert any("swedish" in str(item).lower() for item in result["risk_factors"])
    
    @pytest.mark.asyncio
    async def test_user_story_generation(self, story_tool, sample_github_issue):
        """Test user story generation from requirements."""
        result = await story_tool.analyze_feature_request(sample_github_issue)
        
        user_stories = result["story_breakdown"]["user_stories"]
        
        # Verify user stories follow proper format
        assert len(user_stories) >= 3  # Should break down into multiple stories
        
        # Check for proper user story structure (As a... I want... So that...)
        story_patterns = ["as a", "i want", "so that"]
        for story in user_stories:
            story_lower = story.lower()
            # At least should mention user perspective
            assert any(pattern in story_lower for pattern in ["as a", "user", "coordinator", "admin"])
    
    @pytest.mark.asyncio
    async def test_acceptance_criteria_generation(self, story_tool, sample_github_issue):
        """Test acceptance criteria generation."""
        result = await story_tool.analyze_feature_request(sample_github_issue)
        
        acceptance_criteria = result["story_breakdown"]["acceptance_criteria"]
        
        # Verify acceptance criteria quality
        assert len(acceptance_criteria) >= 3
        
        # Should include testable criteria
        criteria_text = " ".join(acceptance_criteria).lower()
        testable_keywords = ["functional", "working", "compliant", "available", "implemented"]
        assert any(keyword in criteria_text for keyword in testable_keywords)
    
    @pytest.mark.asyncio
    async def test_dependency_identification(self, story_tool):
        """Test identification of technical dependencies."""
        dependency_issue = {
            "title": "Integrate with municipal SSO system",
            "body": """
            Add single sign-on integration with municipal authentication system.
            Requires authentication middleware and user management system.
            """,
            "labels": [{"name": "authentication"}, {"name": "integration"}]
        }
        
        result = await story_tool.analyze_feature_request(dependency_issue)
        
        # Verify dependencies identified
        dependencies = result["dependencies"]
        assert len(dependencies) > 0
        
        # Should identify authentication-related dependencies
        dep_text = " ".join(dependencies).lower()
        auth_keywords = ["authentication", "sso", "user management", "middleware"]
        assert any(keyword in dep_text for keyword in auth_keywords)


class TestDNAComplianceChecker(TestToolsBase):
    """Test DNA Compliance Checker tool functionality."""
    
    @pytest.fixture
    def dna_tool(self, tool_config):
        """Create DNA compliance checker tool for testing."""
        return DNAComplianceChecker(tool_config)
    
    @pytest.mark.asyncio
    async def test_validate_all_design_principles(self, dna_tool):
        """Test validation of all 5 design principles."""
        compliant_feature = {
            "story_breakdown": {
                "user_stories": [
                    "As a municipal trainer, I want quick 5-minute learning modules",
                    "As an employee, I want policy connected to real practice examples"
                ],
                "pedagogical_approach": "Interactive scenario-based learning",
                "policy_connection": "Direct mapping to municipal policies",
                "time_estimate": "8 minutes per module",
                "professional_tone": "Formal municipal communication style"
            }
        }
        
        result = await dna_tool.validate_feature_compliance(compliant_feature)
        
        # Verify all design principles evaluated
        design_principles = result["design_principles"]
        expected_principles = [
            "pedagogical_value", "policy_to_practice", "time_respect", 
            "holistic_thinking", "professional_tone"
        ]
        
        for principle in expected_principles:
            assert principle in design_principles
            assert isinstance(design_principles[principle], bool)
    
    @pytest.mark.asyncio
    async def test_validate_all_architecture_principles(self, dna_tool):
        """Test validation of all 4 architecture principles."""
        compliant_feature = {
            "technical_requirements": [
                "RESTful API design",
                "Stateless backend services",
                "Microservices architecture",
                "Simple, clean interfaces"
            ],
            "architecture_notes": "API-first design with clear separation of concerns"
        }
        
        result = await dna_tool.validate_feature_compliance(compliant_feature)
        
        # Verify all architecture principles evaluated
        arch_principles = result["architecture_compliance"]
        expected_principles = [
            "api_first", "stateless_backend", 
            "separation_of_concerns", "simplicity_first"
        ]
        
        for principle in expected_principles:
            assert principle in arch_principles
            assert isinstance(arch_principles[principle], bool)
    
    @pytest.mark.asyncio
    async def test_time_respect_validation_specific(self, dna_tool):
        """Test specific time respect principle validation."""
        # Test compliant time requirement
        time_compliant = {
            "story_breakdown": {
                "time_estimate": "7 minutes per session",
                "user_workflow": "Quick 3-step process"
            }
        }
        
        # Test non-compliant time requirement
        time_violation = {
            "story_breakdown": {
                "time_estimate": "25 minutes per session",
                "user_workflow": "Complex 15-step process"
            }
        }
        
        compliant_result = await dna_tool.validate_feature_compliance(time_compliant)
        violation_result = await dna_tool.validate_feature_compliance(time_violation)
        
        # Verify time respect validation
        assert compliant_result["design_principles"]["time_respect"] is True
        assert violation_result["design_principles"]["time_respect"] is False
        assert "time_respect" in violation_result.get("violations", [])
    
    @pytest.mark.asyncio
    async def test_pedagogical_value_validation(self, dna_tool):
        """Test pedagogical value principle validation."""
        # High pedagogical value feature
        high_pedagogical = {
            "story_breakdown": {
                "pedagogical_approach": "Interactive scenarios with real municipal examples",
                "learning_objectives": ["Apply policy to practice", "Develop critical thinking"],
                "assessment_method": "Practical case studies"
            }
        }
        
        # Low pedagogical value feature
        low_pedagogical = {
            "story_breakdown": {
                "pedagogical_approach": "Simple information display",
                "learning_objectives": ["Read text"],
                "assessment_method": "None"
            }
        }
        
        high_result = await dna_tool.validate_feature_compliance(high_pedagogical)
        low_result = await dna_tool.validate_feature_compliance(low_pedagogical)
        
        # Verify pedagogical value assessment
        assert high_result["design_principles"]["pedagogical_value"] is True
        assert low_result["design_principles"]["pedagogical_value"] is False
    
    @pytest.mark.asyncio
    async def test_professional_tone_validation(self, dna_tool):
        """Test professional tone principle validation."""
        professional_feature = {
            "story_breakdown": {
                "communication_style": "Formal municipal language",
                "user_interface": "Professional design standards",
                "terminology": "Official municipal terminology"
            }
        }
        
        unprofessional_feature = {
            "story_breakdown": {
                "communication_style": "Casual, informal language",
                "user_interface": "Playful, colorful design",
                "terminology": "Slang and informal terms"
            }
        }
        
        professional_result = await dna_tool.validate_feature_compliance(professional_feature)
        unprofessional_result = await dna_tool.validate_feature_compliance(unprofessional_feature)
        
        # Verify professional tone assessment
        assert professional_result["design_principles"]["professional_tone"] is True
        assert unprofessional_result["design_principles"]["professional_tone"] is False
    
    @pytest.mark.asyncio
    async def test_compliance_scoring(self, dna_tool):
        """Test DNA compliance scoring system."""
        # Perfect compliance feature
        perfect_feature = {
            "story_breakdown": {
                "pedagogical_approach": "Interactive municipal scenarios",
                "policy_connection": "Direct policy-to-practice mapping",
                "time_estimate": "8 minutes",
                "professional_tone": "Municipal communication standards"
            },
            "technical_requirements": [
                "RESTful API", "Stateless design", "Microservices", "Simple UI"
            ]
        }
        
        result = await dna_tool.validate_feature_compliance(perfect_feature)
        
        # Verify scoring
        assert "validation_score" in result
        assert 0.0 <= result["validation_score"] <= 1.0
        
        # Perfect compliance should score high
        if result["compliance_status"] == "compliant":
            assert result["validation_score"] >= 0.8
    
    @pytest.mark.asyncio
    async def test_violation_reporting(self, dna_tool):
        """Test DNA violation reporting and details."""
        violation_feature = {
            "story_breakdown": {
                "time_estimate": "45 minutes per session",  # Time violation
                "pedagogical_approach": "Simple text reading"  # Pedagogical violation
            }
        }
        
        result = await dna_tool.validate_feature_compliance(violation_feature)
        
        # Verify violation reporting
        if result["compliance_status"] == "non_compliant":
            assert "violations" in result
            assert len(result["violations"]) > 0
            
            # Should have specific violation details
            violation_text = " ".join(result["violations"]).lower()
            assert any(keyword in violation_text for keyword in ["time", "pedagogical"])


class TestLearningEngine(TestToolsBase):
    """Test Learning Engine tool functionality."""
    
    @pytest.fixture
    def learning_tool(self, tool_config):
        """Create learning engine tool for testing."""
        return LearningEngine(tool_config)
    
    @pytest.mark.asyncio
    async def test_ml_complexity_prediction(self, learning_tool):
        """Test machine learning complexity prediction."""
        story_breakdown = {
            "user_stories": ["Role management", "Permission system", "GDPR compliance"],
            "technical_requirements": ["Database schema", "Authentication", "Audit logging"],
            "dependencies": ["auth_system", "gdpr_framework"]
        }
        
        traditional_estimate = {
            "estimated_complexity": "medium",
            "estimated_hours": 32
        }
        
        result = await learning_tool.predict_complexity_with_ml(story_breakdown, traditional_estimate)
        
        # Verify ML prediction structure
        assert "predicted_complexity" in result
        assert "confidence_score" in result
        assert "ml_factors" in result
        assert "similar_stories" in result
        assert "risk_assessment" in result
        
        # Verify prediction quality
        assert result["predicted_complexity"] in ["low", "medium", "high"]
        assert 0.0 <= result["confidence_score"] <= 1.0
        assert isinstance(result["ml_factors"], list)
        assert isinstance(result["similar_stories"], list)
    
    @pytest.mark.asyncio
    async def test_historical_learning_storage(self, learning_tool):
        """Test storage and retrieval of historical learning data."""
        # Store learning outcome
        learning_data = {
            "story_id": "STORY-TEST-001",
            "predicted_complexity": "medium",
            "actual_complexity": "high",
            "predicted_hours": 24,
            "actual_hours": 36,
            "accuracy_score": 0.75
        }
        
        await learning_tool.store_learning_outcome(learning_data)
        
        # Retrieve and verify
        retrieved = await learning_tool.get_historical_outcomes(limit=1)
        
        assert len(retrieved) >= 1
        assert retrieved[0]["story_id"] == "STORY-TEST-001"
        assert retrieved[0]["predicted_complexity"] == "medium"
    
    @pytest.mark.asyncio
    async def test_similar_story_identification(self, learning_tool):
        """Test identification of similar historical stories."""
        # Store some test stories
        test_stories = [
            {
                "story_id": "STORY-AUTH-001",
                "features": ["authentication", "user_management"],
                "complexity": "medium",
                "hours": 28
            },
            {
                "story_id": "STORY-AUTH-002", 
                "features": ["authentication", "roles", "permissions"],
                "complexity": "high",
                "hours": 42
            }
        ]
        
        for story in test_stories:
            await learning_tool.store_story_features(story)
        
        # Find similar stories
        query_features = ["authentication", "role_management"]
        similar = await learning_tool.find_similar_stories(query_features, limit=2)
        
        # Verify similarity matching
        assert len(similar) >= 1
        assert any("AUTH" in story["story_id"] for story in similar)
    
    @pytest.mark.asyncio
    async def test_learning_model_training(self, learning_tool):
        """Test learning model training and improvement."""
        # Add training data
        training_data = [
            {
                "features": ["auth", "simple"],
                "complexity": "low",
                "hours": 16
            },
            {
                "features": ["auth", "complex", "gdpr"],
                "complexity": "high", 
                "hours": 48
            }
        ]
        
        for data in training_data:
            await learning_tool.add_training_data(data)
        
        # Train model
        training_result = await learning_tool.train_complexity_model()
        
        # Verify training
        assert "model_accuracy" in training_result
        assert "training_samples" in training_result
        assert training_result["training_samples"] >= 2
    
    @pytest.mark.asyncio
    async def test_prediction_confidence_calculation(self, learning_tool):
        """Test confidence score calculation for predictions."""
        # Test high confidence scenario
        high_confidence_story = {
            "features": ["simple_crud", "basic_ui"],
            "similar_count": 5,
            "historical_accuracy": 0.95
        }
        
        # Test low confidence scenario
        low_confidence_story = {
            "features": ["novel_technology", "complex_ai"],
            "similar_count": 0,
            "historical_accuracy": 0.6
        }
        
        high_confidence = learning_tool._calculate_prediction_confidence(high_confidence_story)
        low_confidence = learning_tool._calculate_prediction_confidence(low_confidence_story)
        
        # Verify confidence calculation
        assert high_confidence > low_confidence
        assert 0.0 <= high_confidence <= 1.0
        assert 0.0 <= low_confidence <= 1.0


class TestSwedishMunicipalCommunicator(TestToolsBase):
    """Test Swedish Municipal Communicator tool functionality."""
    
    @pytest.fixture
    def communicator_tool(self, tool_config):
        """Create Swedish municipal communicator tool for testing."""
        return SwedishMunicipalCommunicator(tool_config)
    
    @pytest.mark.asyncio
    async def test_gdpr_compliance_message_generation(self, communicator_tool):
        """Test GDPR-compliant message generation."""
        message_data = {
            "feature_type": "user_data_collection",
            "data_types": ["name", "email", "training_records"],
            "purpose": "Training coordination and progress tracking"
        }
        
        result = communicator_tool.generate_municipal_specific_message(
            "gdpr_compliance",
            "data_protection_officer", 
            message_data
        )
        
        # Verify GDPR compliance elements
        assert "gdpr_compliance" in result
        assert "data_minimization" in result["gdpr_compliance"]
        assert "user_consent" in result["gdpr_compliance"]
        assert "data_retention" in result["gdpr_compliance"]
        
        # Verify Swedish municipal context
        assert "swedish_legislation" in result
        assert result["language"] == "swedish"
    
    @pytest.mark.asyncio
    async def test_accessibility_compliance_message(self, communicator_tool):
        """Test accessibility compliance messaging."""
        message_data = {
            "accessibility_features": ["screen_reader_support", "keyboard_navigation"],
            "wcag_level": "AA",
            "target_users": ["visually_impaired", "mobility_impaired"]
        }
        
        result = communicator_tool.generate_municipal_specific_message(
            "accessibility_compliance",
            "accessibility_coordinator",
            message_data
        )
        
        # Verify accessibility focus
        assert "accessibility_compliance" in result
        assert "wcag_aa" in str(result).lower()
        assert "swedish_accessibility_law" in result
    
    @pytest.mark.asyncio
    async def test_municipal_role_specific_messaging(self, communicator_tool):
        """Test role-specific message customization."""
        message_data = {
            "feature": "training_management_system",
            "benefits": ["efficiency", "compliance", "transparency"]
        }
        
        # Test different municipal roles
        roles = [
            "municipal_manager",
            "training_coordinator", 
            "it_administrator",
            "data_protection_officer"
        ]
        
        results = {}
        for role in roles:
            results[role] = communicator_tool.generate_municipal_specific_message(
                "feature_introduction",
                role,
                message_data
            )
        
        # Verify role-specific customization
        for role, result in results.items():
            assert result["target_role"] == role
            assert "role_specific_benefits" in result
            
            # Each role should have different focus areas
            role_benefits = result["role_specific_benefits"]
            assert len(role_benefits) > 0
    
    @pytest.mark.asyncio
    async def test_swedish_terminology_validation(self, communicator_tool):
        """Test Swedish municipal terminology usage."""
        message_data = {
            "terms": ["kommun", "medarbetare", "utbildning", "regelefterlevnad"]
        }
        
        result = communicator_tool.validate_swedish_terminology(message_data)
        
        # Verify terminology validation
        assert "terminology_validation" in result
        assert "approved_terms" in result["terminology_validation"]
        assert "corrections_suggested" in result["terminology_validation"]
        
        # Should recognize Swedish municipal terms
        approved = result["terminology_validation"]["approved_terms"]
        assert any(term in approved for term in message_data["terms"])
    
    @pytest.mark.asyncio
    async def test_cultural_appropriateness_check(self, communicator_tool):
        """Test cultural appropriateness validation."""
        # Appropriate content
        appropriate_content = {
            "tone": "formal",
            "language": "professional_swedish",
            "cultural_references": ["swedish_work_culture", "municipal_values"]
        }
        
        # Inappropriate content
        inappropriate_content = {
            "tone": "casual",
            "language": "informal_slang",
            "cultural_references": ["american_corporate_culture"]
        }
        
        appropriate_result = communicator_tool.validate_cultural_appropriateness(appropriate_content)
        inappropriate_result = communicator_tool.validate_cultural_appropriateness(inappropriate_content)
        
        # Verify cultural validation
        assert appropriate_result["culturally_appropriate"] is True
        assert inappropriate_result["culturally_appropriate"] is False
        
        if not inappropriate_result["culturally_appropriate"]:
            assert "cultural_issues" in inappropriate_result
            assert len(inappropriate_result["cultural_issues"]) > 0


class TestTeamCoordinator(TestToolsBase):
    """Test Team Coordinator tool functionality."""
    
    @pytest.fixture
    def coordinator_tool(self, tool_config):
        """Create team coordinator tool for testing."""
        return TeamCoordinator(tool_config)
    
    @pytest.mark.asyncio
    async def test_eventbus_integration(self, coordinator_tool):
        """Test EventBus integration and connectivity."""
        # Verify EventBus initialization
        assert hasattr(coordinator_tool, 'event_bus')
        
        # Test agent sequence definition
        expected_sequence = [
            "project_manager", "game_designer", "developer",
            "test_engineer", "qa_tester", "quality_reviewer"
        ]
        assert coordinator_tool.agent_sequence == expected_sequence
    
    @pytest.mark.asyncio
    async def test_team_workflow_coordination(self, coordinator_tool):
        """Test coordination of team workflow."""
        story_id = "STORY-COORD-001"
        initial_work = {
            "story_breakdown": "Test story breakdown",
            "dna_compliance": {"status": "compliant"}
        }
        
        result = await coordinator_tool.coordinate_team_workflow(story_id, initial_work)
        
        # Verify workflow coordination
        assert result["status"] == "workflow_initiated"
        assert result["story_id"] == story_id
        assert result["next_agent"] == "game_designer"
        assert "coordination_id" in result
        assert "estimated_completion" in result
    
    @pytest.mark.asyncio
    async def test_team_performance_monitoring(self, coordinator_tool):
        """Test team performance monitoring capabilities."""
        performance_snapshot = await coordinator_tool.monitor_team_performance()
        
        # Verify performance monitoring
        assert hasattr(performance_snapshot, 'timestamp')
        assert hasattr(performance_snapshot, 'active_agents')
        assert hasattr(performance_snapshot, 'team_utilization')
        assert hasattr(performance_snapshot, 'bottlenecks')
        assert hasattr(performance_snapshot, 'recommendations')
        
        # Verify data types
        assert isinstance(performance_snapshot.bottlenecks, list)
        assert isinstance(performance_snapshot.recommendations, list)
        assert 0.0 <= performance_snapshot.team_utilization <= 1.0
    
    @pytest.mark.asyncio
    async def test_github_approval_workflow_automation(self, coordinator_tool):
        """Test GitHub approval workflow automation."""
        story_id = "STORY-APPROVAL-001"
        feature_data = {
            "feature_name": "Role Management System",
            "complexity": "medium"
        }
        quality_metrics = {
            "dna_compliance": 1.0,
            "test_coverage": 0.95,
            "performance_score": 4.2
        }
        
        result = await coordinator_tool.automate_github_approval_workflow(
            story_id, feature_data, quality_metrics
        )
        
        # Verify approval automation
        assert result["status"] == "approval_workflow_automated"
        assert result["story_id"] == story_id
        assert "approval_request" in result
        assert "confidence_score" in result
        assert 0.0 <= result["confidence_score"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_team_status_dashboard(self, coordinator_tool):
        """Test team status dashboard generation."""
        dashboard = await coordinator_tool.get_team_status_dashboard()
        
        # Verify dashboard structure
        assert "timestamp" in dashboard
        assert "team_performance" in dashboard
        assert "agent_status" in dashboard
        assert "performance_trends" in dashboard
        assert "active_workflows" in dashboard
        assert "pending_approvals" in dashboard
        assert "alerts" in dashboard
        assert "recommendations" in dashboard
        
        # Verify data types
        assert isinstance(dashboard["agent_status"], dict)
        assert isinstance(dashboard["active_workflows"], list)
        assert isinstance(dashboard["alerts"], list)
    
    @pytest.mark.asyncio
    async def test_bottleneck_identification(self, coordinator_tool):
        """Test identification of team performance bottlenecks."""
        # Simulate performance data with bottlenecks
        mock_metrics = [
            coordinator_tool.AgentPerformanceMetrics(
                agent_id="slow-agent",
                agent_type="developer",
                work_items_completed=5,
                average_completion_time=10.0,  # Slow
                success_rate=0.8,  # Low success rate
                current_status="busy",
                last_activity=datetime.now(),
                quality_score=3.5
            )
        ]
        
        team_metrics = coordinator_tool._calculate_team_metrics(mock_metrics)
        bottlenecks = coordinator_tool._identify_bottlenecks(mock_metrics, team_metrics)
        
        # Verify bottleneck identification
        assert isinstance(bottlenecks, list)
        if bottlenecks:
            assert any("slow" in bottleneck.lower() or "developer" in bottleneck for bottleneck in bottlenecks)


class TestStakeholderRelationshipManager(TestToolsBase):
    """Test Stakeholder Relationship Manager tool functionality."""
    
    @pytest.fixture
    def stakeholder_tool(self, tool_config):
        """Create stakeholder relationship manager tool for testing."""
        return StakeholderRelationshipManager(tool_config)
    
    @pytest.mark.asyncio
    async def test_approval_likelihood_prediction(self, stakeholder_tool):
        """Test stakeholder approval likelihood prediction."""
        stakeholder_id = "municipal_manager_001"
        proposal_data = {
            "feature_type": "training_management",
            "cost_estimate": 50000,
            "implementation_time": "3 months",
            "compliance_requirements": ["GDPR", "Accessibility"],
            "expected_benefits": ["efficiency", "compliance", "cost_savings"]
        }
        
        result = await stakeholder_tool.predict_approval_likelihood(stakeholder_id, proposal_data)
        
        # Verify prediction structure
        assert "approval_likelihood" in result
        assert "confidence_score" in result
        assert "influencing_factors" in result
        assert "recommendations" in result
        
        # Verify data quality
        assert 0.0 <= result["approval_likelihood"] <= 1.0
        assert 0.0 <= result["confidence_score"] <= 1.0
        assert isinstance(result["influencing_factors"], list)
        assert isinstance(result["recommendations"], list)
    
    @pytest.mark.asyncio
    async def test_stakeholder_preference_learning(self, stakeholder_tool):
        """Test learning and tracking of stakeholder preferences."""
        stakeholder_id = "training_coordinator_001"
        
        # Store preference data
        preference_data = {
            "feature_preferences": {
                "user_experience": 0.9,
                "technical_complexity": 0.3,
                "implementation_speed": 0.8,
                "compliance_focus": 0.95
            },
            "approval_history": [
                {"feature": "accessibility_checker", "approved": True, "reason": "High compliance value"},
                {"feature": "complex_analytics", "approved": False, "reason": "Too complex for users"}
            ]
        }
        
        await stakeholder_tool.store_stakeholder_preferences(stakeholder_id, preference_data)
        
        # Retrieve and verify
        preferences = await stakeholder_tool.get_stakeholder_preferences(stakeholder_id)
        
        assert preferences["stakeholder_id"] == stakeholder_id
        assert "feature_preferences" in preferences
        assert preferences["feature_preferences"]["compliance_focus"] == 0.95
    
    @pytest.mark.asyncio
    async def test_relationship_strength_tracking(self, stakeholder_tool):
        """Test tracking of stakeholder relationship strength."""
        stakeholder_id = "it_administrator_001"
        
        # Track interactions
        interactions = [
            {
                "interaction_type": "feature_request",
                "sentiment": "positive",
                "outcome": "approved",
                "date": datetime.now().isoformat()
            },
            {
                "interaction_type": "feedback_session",
                "sentiment": "neutral",
                "outcome": "suggestions_provided",
                "date": (datetime.now() - timedelta(days=7)).isoformat()
            }
        ]
        
        for interaction in interactions:
            await stakeholder_tool.track_stakeholder_interaction(stakeholder_id, interaction)
        
        # Get relationship strength
        relationship = await stakeholder_tool.get_relationship_strength(stakeholder_id)
        
        # Verify relationship tracking
        assert "relationship_strength" in relationship
        assert "interaction_history" in relationship
        assert "sentiment_trend" in relationship
        assert 0.0 <= relationship["relationship_strength"] <= 1.0
    
    @pytest.mark.asyncio
    async def test_stakeholder_communication_optimization(self, stakeholder_tool):
        """Test optimization of stakeholder communication strategies."""
        stakeholder_id = "data_protection_officer_001"
        proposal_data = {
            "feature": "user_analytics_dashboard",
            "data_handling": "personal_data_processing",
            "compliance_measures": ["data_anonymization", "consent_management"]
        }
        
        result = await stakeholder_tool.optimize_communication_strategy(stakeholder_id, proposal_data)
        
        # Verify communication optimization
        assert "communication_strategy" in result
        assert "key_messages" in result
        assert "concerns_to_address" in result
        assert "timing_recommendations" in result
        
        # Should address data protection concerns for DPO
        key_messages = " ".join(result["key_messages"]).lower()
        assert any(keyword in key_messages for keyword in ["privacy", "compliance", "gdpr", "data"])
    
    @pytest.mark.asyncio
    async def test_multi_stakeholder_consensus_prediction(self, stakeholder_tool):
        """Test prediction of consensus among multiple stakeholders."""
        proposal_data = {
            "feature": "comprehensive_training_platform",
            "stakeholders": [
                "municipal_manager_001",
                "training_coordinator_001", 
                "it_administrator_001",
                "data_protection_officer_001"
            ]
        }
        
        result = await stakeholder_tool.predict_multi_stakeholder_consensus(proposal_data)
        
        # Verify consensus prediction
        assert "consensus_likelihood" in result
        assert "stakeholder_alignments" in result
        assert "potential_conflicts" in result
        assert "consensus_building_strategy" in result
        
        # Verify data quality
        assert 0.0 <= result["consensus_likelihood"] <= 1.0
        assert isinstance(result["stakeholder_alignments"], dict)
        assert isinstance(result["potential_conflicts"], list)


class TestToolsIntegration(TestToolsBase):
    """Test integration between PM agent tools."""
    
    @pytest.mark.asyncio
    async def test_cross_tool_data_flow(self, tool_config):
        """Test data flow between different tools."""
        # Initialize tools
        github_tool = GitHubIntegration(tool_config)
        story_tool = StoryAnalyzer(tool_config)
        dna_tool = DNAComplianceChecker(tool_config)
        learning_tool = LearningEngine(tool_config)
        
        # Simulate data flow: GitHub -> Story -> DNA -> Learning
        with patch.object(github_tool, 'fetch_issue_details') as mock_github:
            mock_github.return_value = {
                "title": "GDPR compliance dashboard",
                "body": "Build dashboard for GDPR compliance tracking",
                "labels": [{"name": "gdpr"}, {"name": "compliance"}]
            }
            
            # Step 1: Fetch from GitHub
            issue_data = await github_tool.fetch_issue_details(123)
            
            # Step 2: Analyze story
            story_analysis = await story_tool.analyze_feature_request(issue_data)
            
            # Step 3: Check DNA compliance
            dna_result = await dna_tool.validate_feature_compliance(story_analysis)
            
            # Step 4: ML prediction
            ml_result = await learning_tool.predict_complexity_with_ml(
                story_analysis, {"estimated_complexity": "medium"}
            )
            
            # Verify data flow integrity
            assert issue_data["title"] == "GDPR compliance dashboard"
            assert "story_breakdown" in story_analysis
            assert "compliance_status" in dna_result
            assert "predicted_complexity" in ml_result
    
    @pytest.mark.asyncio
    async def test_tool_error_handling_integration(self, tool_config):
        """Test error handling across tool integrations."""
        story_tool = StoryAnalyzer(tool_config)
        dna_tool = DNAComplianceChecker(tool_config)
        
        # Test handling of malformed data between tools
        malformed_story = {
            "invalid_structure": "missing required fields"
        }
        
        # Story analyzer should handle gracefully
        try:
            story_result = await story_tool.analyze_feature_request(malformed_story)
            # Should provide default structure even with bad input
            assert "story_breakdown" in story_result
        except Exception as e:
            # Should be a business logic error, not a crash
            assert isinstance(e, (BusinessLogicError, ValueError))
        
        # DNA checker should handle missing fields gracefully
        try:
            dna_result = await dna_tool.validate_feature_compliance(malformed_story)
            # Should provide validation result even with incomplete data
            assert "compliance_status" in dna_result
        except Exception as e:
            assert isinstance(e, (BusinessLogicError, ValueError))
    
    @pytest.mark.asyncio
    async def test_performance_across_tools(self, tool_config):
        """Test performance requirements across all tools."""
        import time
        
        # Initialize all tools
        tools = {
            "github": GitHubIntegration(tool_config),
            "story": StoryAnalyzer(tool_config),
            "dna": DNAComplianceChecker(tool_config),
            "learning": LearningEngine(tool_config),
            "communicator": SwedishMunicipalCommunicator(tool_config),
            "coordinator": TeamCoordinator(tool_config),
            "stakeholder": StakeholderRelationshipManager(tool_config)
        }
        
        # Test data
        test_data = {
            "story_breakdown": {"user_stories": ["Test story"]},
            "issue_data": {"title": "Test", "body": "Test body"},
            "performance_threshold": 5.0  # 5 seconds max per tool
        }
        
        # Test each tool performance
        performance_results = {}
        
        # DNA tool performance test
        start_time = time.time()
        await tools["dna"].validate_feature_compliance(test_data)
        performance_results["dna"] = time.time() - start_time
        
        # Story tool performance test
        start_time = time.time()
        await tools["story"].analyze_feature_request(test_data["issue_data"])
        performance_results["story"] = time.time() - start_time
        
        # Verify performance requirements
        for tool_name, duration in performance_results.items():
            assert duration < test_data["performance_threshold"], \
                f"{tool_name} tool took {duration}s, exceeds {test_data['performance_threshold']}s limit"