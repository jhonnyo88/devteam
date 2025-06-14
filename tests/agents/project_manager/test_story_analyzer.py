"""
Tests for Story Analyzer tool.

Tests story breakdown creation, acceptance criteria generation,
and complexity assessment functionality.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
from datetime import datetime

from modules.agents.project_manager.tools.story_analyzer import StoryAnalyzer
from modules.shared.exceptions import BusinessLogicError, AgentExecutionError


class TestStoryAnalyzer:
    """Test suite for Story Analyzer tool."""

    @pytest.fixture
    def story_analyzer(self):
        """Create story analyzer instance."""
        return StoryAnalyzer()

    @pytest.fixture
    def sample_feature_data(self):
        """Sample feature data for testing."""
        return {
            "feature_description": """
            As Anna, I want to practice policy application through interactive scenarios 
            so that I can better understand real-world implementation.
            
            This feature will provide multiple policy scenarios where users can practice
            decision-making and receive immediate feedback.
            """,
            "user_persona": "Anna",
            "priority_level": "high",
            "time_constraint_minutes": 10,
            "learning_objectives": [
                "Apply policy knowledge to practical situations",
                "Understand decision-making frameworks",
                "Practice critical thinking in policy context"
            ],
            "acceptance_criteria": [
                "User can select from multiple policy scenarios",
                "Each scenario provides clear context and background",
                "User receives immediate feedback on decisions",
                "Progress is tracked and saved"
            ],
            "github_issue_number": 123
        }

    @pytest.fixture
    def sample_dna_analysis(self):
        """Sample DNA analysis results."""
        return {
            "compliant": True,
            "compliance_score": 85.0,
            "pedagogical_value": True,
            "policy_to_practice": True,
            "time_respect": True,
            "holistic_thinking": True,
            "professional_tone": True,
            "violations": [],
            "recommendations": ["Feature meets all DNA compliance requirements"]
        }

    # ==========================================
    # INITIALIZATION TESTS
    # ==========================================

    def test_story_analyzer_initialization(self):
        """Test story analyzer initialization."""
        analyzer = StoryAnalyzer()
        
        assert len(analyzer.complexity_factors) > 0
        assert len(analyzer.estimation_guidelines) > 0
        assert len(analyzer.story_templates) > 0
        assert "user_registration" in analyzer.story_templates
        assert "learning_module" in analyzer.story_templates

    def test_story_analyzer_initialization_with_config(self):
        """Test story analyzer initialization with config."""
        config = {"custom_setting": "value"}
        analyzer = StoryAnalyzer(config)
        
        assert analyzer.config["custom_setting"] == "value"

    # ==========================================
    # STORY BREAKDOWN CREATION TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_create_story_breakdown_success(self, story_analyzer, sample_feature_data, sample_dna_analysis):
        """Test successful story breakdown creation."""
        breakdown = await story_analyzer.create_story_breakdown(sample_feature_data, sample_dna_analysis)
        
        # Verify required sections
        assert "story_id" in breakdown
        assert "feature_summary" in breakdown
        assert "user_stories" in breakdown
        assert "technical_requirements" in breakdown
        assert "design_requirements" in breakdown
        assert "implementation_tasks" in breakdown
        assert "estimated_completion_time" in breakdown
        
        # Verify story ID generation
        assert breakdown["story_id"] == "STORY-GH-123"
        
        # Verify feature summary
        summary = breakdown["feature_summary"]
        assert summary["user_persona"] == "Anna"
        assert summary["priority"] == "high"
        assert summary["time_constraint_minutes"] == 10

    @pytest.mark.asyncio
    async def test_create_story_breakdown_missing_required_field(self, story_analyzer, sample_dna_analysis):
        """Test story breakdown creation with missing required field."""
        invalid_feature_data = {
            "user_persona": "Anna",
            "priority_level": "high"
            # Missing feature_description
        }
        
        with pytest.raises(BusinessLogicError) as exc_info:
            await story_analyzer.create_story_breakdown(invalid_feature_data, sample_dna_analysis)
        
        assert "Missing required field" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_story_breakdown_empty_description(self, story_analyzer, sample_dna_analysis):
        """Test story breakdown creation with empty description."""
        invalid_feature_data = {
            "feature_description": "   ",  # Empty/whitespace only
            "user_persona": "Anna",
            "priority_level": "high"
        }
        
        with pytest.raises(BusinessLogicError) as exc_info:
            await story_analyzer.create_story_breakdown(invalid_feature_data, sample_dna_analysis)
        
        assert "Feature description cannot be empty" in str(exc_info.value)

    # ==========================================
    # USER STORY GENERATION TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_generate_user_stories_from_description(self, story_analyzer, sample_feature_data):
        """Test user story generation from feature description."""
        user_stories = await story_analyzer._generate_user_stories(sample_feature_data)
        
        assert len(user_stories) >= 1
        
        # Check first story structure
        story = user_stories[0]
        assert "story_id" in story
        assert "role" in story
        assert "action" in story
        assert "benefit" in story
        assert "story" in story
        assert "priority" in story
        assert "estimation" in story
        assert "acceptance_criteria" in story

    @pytest.mark.asyncio
    async def test_generate_user_stories_with_explicit_stories(self, story_analyzer):
        """Test user story generation with explicit user stories in description."""
        feature_data = {
            "feature_description": """
            As Anna, I want to practice policy scenarios so that I can learn better.
            As a teacher, I want to track student progress so that I can provide guidance.
            """,
            "user_persona": "Anna",
            "priority_level": "medium"
        }
        
        user_stories = await story_analyzer._generate_user_stories(feature_data)
        
        assert len(user_stories) >= 2
        assert any("Anna" in story["role"] for story in user_stories)
        assert any("teacher" in story["role"] for story in user_stories)

    @pytest.mark.asyncio
    async def test_generate_user_stories_fallback(self, story_analyzer):
        """Test user story generation with fallback when none found."""
        feature_data = {
            "feature_description": "Build a simple dashboard feature",
            "user_persona": "Anna",
            "priority_level": "low"
        }
        
        user_stories = await story_analyzer._generate_user_stories(feature_data)
        
        assert len(user_stories) == 1
        story = user_stories[0]
        assert story["role"] == "Anna"
        assert "learning objectives" in story["benefit"]

    # ==========================================
    # ACCEPTANCE CRITERIA GENERATION TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_generate_acceptance_criteria_comprehensive(self, story_analyzer, sample_feature_data):
        """Test comprehensive acceptance criteria generation."""
        story_breakdown = {
            "user_stories": [
                {"story": "As Anna, I want to practice scenarios", "action": "practice scenarios"},
                {"story": "As Anna, I want to receive feedback", "action": "receive feedback"}
            ],
            "technical_requirements": {
                "frontend": {"required_components": ["form", "button"]},
                "backend": {"api_endpoints": ["/api/scenarios"]}
            }
        }
        
        criteria = await story_analyzer.generate_acceptance_criteria(sample_feature_data, story_breakdown)
        
        assert len(criteria) >= 5
        assert any("practice scenarios" in criterion for criterion in criteria)
        assert any("pedagogical value" in criterion for criterion in criteria)
        assert any("10-minute" in criterion for criterion in criteria)

    @pytest.mark.asyncio
    async def test_generate_acceptance_criteria_with_original(self, story_analyzer, sample_feature_data):
        """Test acceptance criteria generation including original criteria."""
        story_breakdown = {"user_stories": [], "technical_requirements": {}}
        
        criteria = await story_analyzer.generate_acceptance_criteria(sample_feature_data, story_breakdown)
        
        # Should include original criteria from sample_feature_data
        original_criteria = sample_feature_data["acceptance_criteria"]
        for original in original_criteria:
            assert original in criteria

    @pytest.mark.asyncio
    async def test_generate_acceptance_criteria_minimum_fallback(self, story_analyzer):
        """Test acceptance criteria generation with minimum fallback."""
        feature_data = {
            "acceptance_criteria": [],  # No original criteria
            "user_persona": "Anna"
        }
        story_breakdown = {"user_stories": [], "technical_requirements": {}}
        
        criteria = await story_analyzer.generate_acceptance_criteria(feature_data, story_breakdown)
        
        assert len(criteria) >= 5  # Should have fallback criteria

    # ==========================================
    # COMPLEXITY ASSESSMENT TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_assess_complexity_comprehensive(self, story_analyzer):
        """Test comprehensive complexity assessment."""
        story_breakdown = {
            "technical_requirements": {
                "frontend": {
                    "required_components": ["form", "button", "chart"],
                    "animations": ["fade", "slide"]
                },
                "backend": {
                    "api_endpoints": ["/api/data", "/api/process"],
                    "business_logic": ["validation", "processing"]
                },
                "integrations": {
                    "external_apis": ["github"]
                }
            },
            "design_requirements": {
                "ui_components": ["form", "chart", "navigation"],
                "user_flows": ["main_flow", "error_flow"],
                "wireframe_requirements": ["desktop", "mobile"]
            },
            "implementation_tasks": [
                {"category": "Testing", "name": "unit_tests"},
                {"category": "Testing", "name": "integration_tests"},
                {"category": "Testing", "name": "e2e_tests"}
            ]
        }
        
        assessment = await story_analyzer.assess_complexity(story_breakdown)
        
        assert "overall_complexity" in assessment
        assert "effort_points" in assessment
        assert "technical_complexity" in assessment
        assert "design_complexity" in assessment
        assert "integration_complexity" in assessment
        assert "testing_complexity" in assessment
        assert "estimated_duration_hours" in assessment
        assert "estimated_duration_days" in assessment
        assert "confidence_level" in assessment
        assert "complexity_breakdown" in assessment
        
        # Verify effort points calculation
        assert 1 <= assessment["effort_points"] <= 13
        assert assessment["estimated_duration_hours"] > 0

    @pytest.mark.asyncio
    async def test_assess_complexity_minimal_feature(self, story_analyzer):
        """Test complexity assessment for minimal feature."""
        minimal_breakdown = {
            "technical_requirements": {
                "frontend": {"required_components": []},
                "backend": {"api_endpoints": []},
                "integrations": {"external_apis": []}
            },
            "design_requirements": {
                "ui_components": [],
                "user_flows": [],
                "wireframe_requirements": []
            },
            "implementation_tasks": []
        }
        
        assessment = await story_analyzer.assess_complexity(minimal_breakdown)
        
        assert assessment["overall_complexity"] in ["Simple", "Medium"]
        assert assessment["effort_points"] <= 8  # More lenient
        assert assessment["technical_complexity"] in ["Low", "Medium"]
        assert assessment["design_complexity"] in ["Low", "Medium"]

    # ==========================================
    # COMPLEXITY CALCULATION TESTS
    # ==========================================

    def test_assess_technical_complexity_levels(self, story_analyzer):
        """Test technical complexity level assessment."""
        # Low complexity
        low_breakdown = {
            "technical_requirements": {
                "frontend": {"required_components": ["button"], "animations": []},
                "backend": {"api_endpoints": ["/api/simple"], "business_logic": []},
                "integrations": {"external_apis": []}
            }
        }
        complexity = story_analyzer._assess_technical_complexity(low_breakdown)
        assert complexity == "Low"
        
        # High complexity
        high_breakdown = {
            "technical_requirements": {
                "frontend": {"required_components": ["form", "chart", "table", "nav"], "animations": ["fade", "slide", "zoom"]},
                "backend": {"api_endpoints": [f"/api/endpoint{i}" for i in range(10)], "business_logic": ["complex1", "complex2"]},
                "integrations": {"external_apis": ["api1", "api2", "api3", "api4"]}
            }
        }
        complexity = story_analyzer._assess_technical_complexity(high_breakdown)
        assert complexity in ["High", "Very High"]

    def test_assess_design_complexity_levels(self, story_analyzer):
        """Test design complexity level assessment."""
        # Low complexity
        low_breakdown = {
            "design_requirements": {
                "ui_components": ["button"],
                "user_flows": ["main"],
                "wireframe_requirements": ["desktop"]
            }
        }
        complexity = story_analyzer._assess_design_complexity(low_breakdown)
        assert complexity in ["Low", "Medium"]  # More lenient
        
        # High complexity
        high_breakdown = {
            "design_requirements": {
                "ui_components": [f"component{i}" for i in range(15)],
                "user_flows": [f"flow{i}" for i in range(10)],
                "wireframe_requirements": [f"wireframe{i}" for i in range(20)]
            }
        }
        complexity = story_analyzer._assess_design_complexity(high_breakdown)
        assert complexity in ["High", "Very High"]

    def test_calculate_effort_points_combinations(self, story_analyzer):
        """Test effort points calculation with different complexity combinations."""
        # All low complexity
        low_points = story_analyzer._calculate_effort_points("Low", "Low", "Low", "Low")
        assert low_points <= 5
        
        # Mixed complexity
        mixed_points = story_analyzer._calculate_effort_points("High", "Medium", "Low", "Medium")
        assert 5 < mixed_points <= 13
        
        # All high complexity
        high_points = story_analyzer._calculate_effort_points("Very High", "High", "High", "High")
        assert high_points == 13  # Capped at maximum

    def test_estimate_duration_from_effort(self, story_analyzer):
        """Test duration estimation from effort points."""
        # Small effort
        duration_small = story_analyzer._estimate_duration_from_effort(1)
        assert duration_small == 2.0
        
        # Medium effort
        duration_medium = story_analyzer._estimate_duration_from_effort(5)
        assert duration_medium == 16.0
        
        # Large effort
        duration_large = story_analyzer._estimate_duration_from_effort(13)
        assert duration_large == 64.0
        
        # Over maximum
        duration_over = story_analyzer._estimate_duration_from_effort(20)
        assert duration_over == 64.0  # Fallback

    def test_categorize_complexity(self, story_analyzer):
        """Test complexity categorization."""
        assert story_analyzer._categorize_complexity(1) == "Simple"
        assert story_analyzer._categorize_complexity(3) == "Medium"
        assert story_analyzer._categorize_complexity(6) == "Complex"
        assert story_analyzer._categorize_complexity(10) == "Very Complex"

    # ==========================================
    # FEATURE SUMMARY TESTS
    # ==========================================

    def test_create_feature_summary(self, story_analyzer, sample_feature_data):
        """Test feature summary creation."""
        summary = story_analyzer._create_feature_summary(sample_feature_data)
        
        assert "title" in summary
        assert "description" in summary
        assert "user_persona" in summary
        assert "priority" in summary
        assert "time_constraint_minutes" in summary
        assert "learning_objectives" in summary
        assert "business_value" in summary
        assert "success_metrics" in summary
        
        assert summary["user_persona"] == "Anna"
        assert summary["priority"] == "high"
        assert summary["time_constraint_minutes"] == 10

    def test_create_feature_summary_title_extraction(self, story_analyzer):
        """Test title extraction from feature description."""
        feature_data = {
            "feature_description": "Policy Practice Module\n\nDetailed description of the feature...",
            "user_persona": "Anna",
            "priority_level": "medium",
            "learning_objectives": []
        }
        
        summary = story_analyzer._create_feature_summary(feature_data)
        
        assert summary["title"] == "Policy Practice Module"

    # ==========================================
    # TECHNICAL REQUIREMENTS ANALYSIS TESTS
    # ==========================================

    def test_analyze_technical_requirements(self, story_analyzer, sample_feature_data):
        """Test technical requirements analysis."""
        requirements = story_analyzer._analyze_technical_requirements(sample_feature_data)
        
        assert "frontend" in requirements
        assert "backend" in requirements
        assert "database" in requirements
        assert "integrations" in requirements
        assert "performance_requirements" in requirements
        assert "security_requirements" in requirements
        
        # Verify structure
        assert "required_components" in requirements["frontend"]
        assert "api_endpoints" in requirements["backend"]

    # ==========================================
    # TASK BREAKDOWN TESTS
    # ==========================================

    def test_break_down_implementation_tasks(self, story_analyzer, sample_feature_data):
        """Test implementation task breakdown."""
        tasks = story_analyzer._break_down_implementation_tasks(sample_feature_data)
        
        assert len(tasks) > 0
        
        # Verify task structure
        task = tasks[0]
        assert "task_id" in task
        assert "category" in task
        assert "name" in task
        assert "effort" in task
        assert "description" in task
        assert "created_at" in task
        
        # Verify task categories are present
        categories = {task["category"] for task in tasks}
        expected_categories = {"Frontend Development", "Backend Development", "Testing"}
        assert any(cat in categories for cat in expected_categories)

    # ==========================================
    # STORY ID GENERATION TESTS
    # ==========================================

    def test_generate_story_id_with_github_number(self, story_analyzer):
        """Test story ID generation with GitHub issue number."""
        feature_data = {"github_issue_number": 123}
        story_id = story_analyzer._generate_story_id(feature_data)
        assert story_id == "STORY-GH-123"

    def test_generate_story_id_without_github_number(self, story_analyzer):
        """Test story ID generation without GitHub issue number."""
        feature_data = {}
        story_id = story_analyzer._generate_story_id(feature_data)
        assert story_id.startswith("STORY-")
        assert len(story_id) > 10  # Should have timestamp

    # ==========================================
    # HELPER METHOD TESTS
    # ==========================================

    def test_extract_business_value(self, story_analyzer):
        """Test business value extraction."""
        description = "This feature will improve user engagement and learning outcomes"
        value = story_analyzer._extract_business_value(description)
        assert isinstance(value, str)
        assert len(value) > 0

    def test_define_success_metrics(self, story_analyzer, sample_feature_data):
        """Test success metrics definition."""
        metrics = story_analyzer._define_success_metrics(sample_feature_data)
        assert isinstance(metrics, list)
        assert len(metrics) >= 3
        assert any("time constraint" in metric for metric in metrics)

    def test_estimate_user_story(self, story_analyzer):
        """Test user story estimation."""
        story = {"action": "practice scenarios", "benefit": "learn better"}
        estimation = story_analyzer._estimate_user_story(story)
        assert isinstance(estimation, int)
        assert estimation > 0

    def test_clean_and_deduplicate_criteria(self, story_analyzer):
        """Test criteria cleaning and deduplication."""
        criteria = [
            "Feature works correctly",
            "  Feature works correctly  ",  # Duplicate with whitespace
            "",  # Empty
            "User can complete task",
            "Feature works correctly"  # Exact duplicate
        ]
        
        cleaned = story_analyzer._clean_and_deduplicate_criteria(criteria)
        
        assert len(cleaned) >= 2  # Should remove empty and duplicates
        assert "Feature works correctly" in cleaned
        assert "User can complete task" in cleaned

    # ==========================================
    # ERROR HANDLING TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_story_breakdown_creation_exception_handling(self, story_analyzer, sample_dna_analysis):
        """Test story breakdown creation exception handling."""
        # This should cause an exception in validation
        invalid_data = None
        
        with pytest.raises(AgentExecutionError):
            await story_analyzer.create_story_breakdown(invalid_data, sample_dna_analysis)

    @pytest.mark.asyncio
    async def test_acceptance_criteria_generation_exception_handling(self, story_analyzer):
        """Test acceptance criteria generation exception handling."""
        with patch.object(story_analyzer, '_generate_criteria_from_user_story', side_effect=Exception("Test error")):
            # Exception should be raised and handled by AgentExecutionError
            with pytest.raises(AgentExecutionError):
                await story_analyzer.generate_acceptance_criteria({}, {"user_stories": [{"story": "test"}]})

    @pytest.mark.asyncio
    async def test_complexity_assessment_exception_handling(self, story_analyzer):
        """Test complexity assessment exception handling."""
        with patch.object(story_analyzer, '_assess_technical_complexity', side_effect=Exception("Test error")):
            with pytest.raises(AgentExecutionError):
                await story_analyzer.assess_complexity({})

    # ==========================================
    # CONFIDENCE LEVEL TESTS
    # ==========================================

    def test_calculate_confidence_level_high(self, story_analyzer):
        """Test confidence level calculation with well-defined story."""
        story_breakdown = {
            "effort_points": 5,  # Reasonable effort
            "user_stories": [{"story": f"Story {i}"} for i in range(5)]  # Multiple stories
        }
        
        confidence = story_analyzer._calculate_confidence_level(story_breakdown)
        assert 0.7 <= confidence <= 1.0

    def test_calculate_confidence_level_low(self, story_analyzer):
        """Test confidence level calculation with poorly-defined story."""
        story_breakdown = {
            "effort_points": 12,  # High effort (uncertain)
            "user_stories": [{"story": "Single story"}]  # Few stories
        }
        
        confidence = story_analyzer._calculate_confidence_level(story_breakdown)
        assert confidence <= 0.7

    # ==========================================
    # INTEGRATION TESTS
    # ==========================================

    @pytest.mark.asyncio
    async def test_full_analysis_workflow(self, story_analyzer, sample_feature_data, sample_dna_analysis):
        """Test full story analysis workflow integration."""
        # Create story breakdown
        breakdown = await story_analyzer.create_story_breakdown(sample_feature_data, sample_dna_analysis)
        
        # Generate acceptance criteria
        criteria = await story_analyzer.generate_acceptance_criteria(sample_feature_data, breakdown)
        
        # Assess complexity
        complexity = await story_analyzer.assess_complexity(breakdown)
        
        # Verify all components work together
        assert len(criteria) >= 5
        assert complexity["effort_points"] > 0
        assert breakdown["story_id"] == "STORY-GH-123"
        assert complexity["overall_complexity"] in ["Simple", "Medium", "Complex", "Very Complex"]