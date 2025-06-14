"""
Unit tests for QA Tester tools.

PURPOSE:
Comprehensive testing of QA Tester tool functionality including
PersonaSimulator, AccessibilityChecker, and UserFlowValidator.

CRITICAL COVERAGE:
- Tool initialization and configuration
- Core functionality testing
- Edge case handling
- Error scenarios
- Integration testing

TEST STANDARDS:
- 100% line coverage required
- All edge cases covered
- Mock external dependencies
- Test both success and failure scenarios
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Import the tools
from ..tools.persona_simulator import PersonaSimulator, SimulationScenario, PersonaSimulationResult, FlowStepType
from ..tools.accessibility_checker import AccessibilityChecker, AccessibilityViolation, AccessibilityTestResult
from ..tools.user_flow_validator import UserFlowValidator, UserFlow, FlowStep, FlowValidationResult


class TestPersonaSimulator:
    """Test suite for PersonaSimulator tool."""
    
    @pytest.fixture
    def persona_simulator(self):
        """Create PersonaSimulator instance for testing."""
        config = {
            "anna_requirements": {
                "max_task_duration": 10,
                "min_satisfaction_score": 4.0
            }
        }
        return PersonaSimulator(config=config)
    
    @pytest.fixture
    def sample_implementation_data(self):
        """Sample implementation data for testing."""
        return {
            "ui_components": [
                {
                    "id": "test-button",
                    "type": "button",
                    "text_content": "Submit Form",
                    "keyboard_accessible": True,
                    "focusable": True
                },
                {
                    "id": "test-input",
                    "type": "input",
                    "label": "Email Address",
                    "required": True
                }
            ],
            "user_flows": [
                {
                    "flow_id": "registration",
                    "steps": ["navigate", "fill_form", "submit"]
                }
            ]
        }
    
    def test_persona_simulator_initialization(self):
        """Test PersonaSimulator initialization."""
        simulator = PersonaSimulator()
        
        assert simulator.config == {}
        assert simulator.anna_characteristics["role"] == "Municipal training coordinator"
        assert simulator.max_task_duration_minutes == 10
        assert len(simulator.standard_scenarios) > 0
    
    def test_persona_simulator_initialization_with_config(self):
        """Test PersonaSimulator initialization with config."""
        config = {"test_setting": "value"}
        simulator = PersonaSimulator(config=config)
        
        assert simulator.config == config
        assert simulator.anna_characteristics["role"] == "Municipal training coordinator"
    
    @pytest.mark.asyncio
    async def test_simulate_anna_usage_success(self, persona_simulator, sample_implementation_data):
        """Test successful Anna usage simulation."""
        test_suite = {
            "unit_tests": [],
            "integration_tests": [],
            "e2e_tests": []
        }
        
        requirements = {
            "success_metrics": {
                "task_completion_rate": 95,
                "satisfaction_score": 4,
                "learning_effectiveness": 4
            }
        }
        
        with patch.object(persona_simulator, '_simulate_scenario', new_callable=AsyncMock) as mock_simulate:
            # Mock scenario simulation results
            mock_result = PersonaSimulationResult(
                scenario_id="test_scenario",
                completed_successfully=True,
                completion_time_minutes=8.0,
                satisfaction_score=4.2,
                learning_effectiveness_score=4.1,
                confusion_incidents=[],
                error_recovery_attempts=0,
                positive_feedback=["Clear interface"],
                improvement_suggestions=[],
                timestamp=datetime.now().isoformat()
            )
            mock_simulate.return_value = mock_result
            
            result = await persona_simulator.simulate_anna_usage(
                story_id="STORY-TEST-001",
                implementation_data=sample_implementation_data,
                test_suite=test_suite,
                requirements=requirements
            )
            
            assert result is not None
            assert result["story_id"] == "STORY-TEST-001"
            assert result["persona"] == "Anna - Municipal Training Coordinator"
            assert "overall_metrics" in result
            assert "scenario_results" in result
            assert "detailed_analysis" in result
            assert "recommendations" in result
            assert "anna_characteristics_validation" in result
    
    @pytest.mark.asyncio
    async def test_simulate_anna_usage_with_exception(self, persona_simulator, sample_implementation_data):
        """Test Anna usage simulation with exception."""
        test_suite = {}
        requirements = {}
        
        with patch.object(persona_simulator, '_simulate_scenario', side_effect=Exception("Simulation failed")):
            result = await persona_simulator.simulate_anna_usage(
                story_id="STORY-TEST-001",
                implementation_data=sample_implementation_data,
                test_suite=test_suite,
                requirements=requirements
            )
            
            assert "error" in result
            assert "Simulation failed" in result["error"]
            assert result["simulation_failed"] is True
    
    @pytest.mark.asyncio
    async def test_simulate_scenario(self, persona_simulator):
        """Test individual scenario simulation."""
        scenario = SimulationScenario(
            scenario_id="test_scenario",
            name="Test Scenario",
            description="Test scenario description",
            expected_completion_time_minutes=5.0,
            required_actions=["navigate", "click_button"],
            success_criteria={"task_completion": True},
            difficulty_level="medium",
            persona_context={"stress_level": "low"}
        )
        
        implementation_data = {
            "ui_components": [{"type": "button", "id": "test-btn"}],
            "user_flows": []
        }
        
        with patch.object(persona_simulator, '_simulate_action', new_callable=AsyncMock) as mock_action:
            mock_action.return_value = {
                "time_taken_minutes": 1.0,
                "satisfaction_impact": 4.5,
                "confusion_detected": False,
                "error_occurred": False,
                "positive_experience": True,
                "positive_reason": "Simple interface"
            }
            
            result = await persona_simulator._simulate_scenario(
                scenario, implementation_data, "STORY-TEST-001"
            )
            
            assert isinstance(result, PersonaSimulationResult)
            assert result.scenario_id == "test_scenario"
            assert result.completion_time_minutes == 2.0  # 2 actions * 1 minute each
            assert result.satisfaction_score >= 4.0
            assert len(result.positive_feedback) > 0
    
    @pytest.mark.asyncio
    async def test_simulate_action(self, persona_simulator):
        """Test action simulation."""
        ui_components = [
            {"type": "button", "id": "simple-btn"},
            {"type": "input", "id": "text-input"}
        ]
        persona_context = {"stress_level": "medium", "prior_knowledge": "good"}
        
        result = await persona_simulator._simulate_action("navigate", ui_components, persona_context)
        
        assert "time_taken_minutes" in result
        assert "satisfaction_impact" in result
        assert "confusion_detected" in result
        assert "error_occurred" in result
        assert isinstance(result["time_taken_minutes"], float)
        assert isinstance(result["satisfaction_impact"], float)
    
    def test_assess_action_complexity(self, persona_simulator):
        """Test action complexity assessment."""
        # Simple action with few components
        simple_components = [{"type": "button"}, {"type": "text"}]
        complexity = persona_simulator._assess_action_complexity("click", simple_components)
        assert 1 <= complexity <= 5
        
        # Complex action with many components
        complex_components = [
            {"type": "input"}, {"type": "select"}, {"type": "textarea"},
            {"type": "button"}, {"type": "checkbox"}, {"type": "radio"},
            {"type": "input"}, {"type": "select"}, {"type": "textarea"}
        ]
        complexity = persona_simulator._assess_action_complexity("fill_form", complex_components)
        assert complexity > 2
    
    def test_check_success_criteria(self, persona_simulator):
        """Test success criteria checking."""
        success_criteria = {
            "time_under_limit": True,
            "no_external_help": True,
            "minimal_errors": True
        }
        
        # Test passing scenario
        result = persona_simulator._check_success_criteria(
            success_criteria, 8.0, [], 0
        )
        assert result is True
        
        # Test failing scenario (time exceeded)
        result = persona_simulator._check_success_criteria(
            success_criteria, 12.0, [], 0
        )
        assert result is False
        
        # Test failing scenario (too many confusion incidents)
        result = persona_simulator._check_success_criteria(
            success_criteria, 8.0, ["confusion1", "confusion2", "confusion3"], 0
        )
        assert result is False


class TestAccessibilityChecker:
    """Test suite for AccessibilityChecker tool."""
    
    @pytest.fixture
    def accessibility_checker(self):
        """Create AccessibilityChecker instance for testing."""
        config = {
            "wcag_level": "AA",
            "compliance_threshold": 90
        }
        return AccessibilityChecker(config=config)
    
    @pytest.fixture
    def sample_implementation_data(self):
        """Sample implementation data for accessibility testing."""
        return {
            "ui_components": [
                {
                    "id": "test-image",
                    "type": "image",
                    "alt_text": "Test image description",
                    "src": "test.jpg"
                },
                {
                    "id": "test-button",
                    "type": "button",
                    "aria_label": "Submit form",
                    "keyboard_accessible": True,
                    "focusable": True,
                    "focus_visible": True
                },
                {
                    "id": "test-input",
                    "type": "input",
                    "label": "Email address",
                    "required": True,
                    "aria_required": "true"
                }
            ],
            "html_structure": {
                "semantic_elements": ["header", "nav", "main", "footer"],
                "headings": [
                    {"type": "heading", "level": "1", "text": "Main Title"},
                    {"type": "heading", "level": "2", "text": "Section Title"}
                ],
                "lang": "en"
            },
            "css_styles": {
                "focus_indicators": {
                    "button:focus": {"outline": "2px solid blue"},
                    "input:focus": {"border": "2px solid blue"}
                }
            }
        }
    
    def test_accessibility_checker_initialization(self):
        """Test AccessibilityChecker initialization."""
        checker = AccessibilityChecker()
        
        assert checker.config == {}
        assert "1.1.1" in checker.wcag_aa_criteria  # Non-text Content
        assert "2.4.7" in checker.wcag_aa_criteria  # Focus Visible
        assert checker.compliance_thresholds["critical_violations"] == 0
    
    def test_accessibility_checker_initialization_with_config(self):
        """Test AccessibilityChecker initialization with config."""
        config = {"test_setting": "value"}
        checker = AccessibilityChecker(config=config)
        
        assert checker.config == config
    
    @pytest.mark.asyncio
    async def test_validate_accessibility_success(self, accessibility_checker, sample_implementation_data):
        """Test successful accessibility validation."""
        with patch.object(accessibility_checker, '_run_automated_wcag_tests', new_callable=AsyncMock) as mock_wcag, \
             patch.object(accessibility_checker, '_validate_color_contrast', new_callable=AsyncMock) as mock_contrast, \
             patch.object(accessibility_checker, '_test_keyboard_navigation', new_callable=AsyncMock) as mock_keyboard, \
             patch.object(accessibility_checker, '_test_screen_reader_compatibility', new_callable=AsyncMock) as mock_screen_reader, \
             patch.object(accessibility_checker, '_test_focus_management', new_callable=AsyncMock) as mock_focus, \
             patch.object(accessibility_checker, '_validate_alternative_text', new_callable=AsyncMock) as mock_alt_text, \
             patch.object(accessibility_checker, '_test_form_accessibility', new_callable=AsyncMock) as mock_forms:
            
            # Setup mock returns
            mock_test_result = AccessibilityTestResult(
                test_name="Mock Test",
                passed=True,
                score=95.0,
                violations=[],
                recommendations=[],
                details={}
            )
            
            mock_wcag.return_value = [mock_test_result]
            mock_contrast.return_value = mock_test_result
            mock_keyboard.return_value = mock_test_result
            mock_screen_reader.return_value = mock_test_result
            mock_focus.return_value = mock_test_result
            mock_alt_text.return_value = mock_test_result
            mock_forms.return_value = mock_test_result
            
            result = await accessibility_checker.validate_accessibility(
                story_id="STORY-TEST-001",
                implementation_data=sample_implementation_data,
                wcag_level="AA"
            )
            
            assert result is not None
            assert result["story_id"] == "STORY-TEST-001"
            assert result["wcag_level"] == "AA"
            assert "compliance_summary" in result
            assert "test_results" in result
            assert "violations" in result
            assert "recommendations" in result
            assert "compliance_score" in result
            assert "certification_status" in result
    
    @pytest.mark.asyncio
    async def test_validate_accessibility_with_exception(self, accessibility_checker, sample_implementation_data):
        """Test accessibility validation with exception."""
        with patch.object(accessibility_checker, '_run_automated_wcag_tests', side_effect=Exception("WCAG test failed")):
            result = await accessibility_checker.validate_accessibility(
                story_id="STORY-TEST-001",
                implementation_data=sample_implementation_data,
                wcag_level="AA"
            )
            
            assert "error" in result
            assert "WCAG test failed" in result["error"]
            assert result["validation_failed"] is True
    
    @pytest.mark.asyncio
    async def test_validate_color_contrast(self, accessibility_checker):
        """Test color contrast validation."""
        ui_components = [
            {
                "id": "text1",
                "type": "text",
                "color": "#000000",
                "background_color": "#ffffff",
                "font_size": "16px",
                "font_weight": "normal"
            },
            {
                "id": "text2",
                "type": "text",
                "color": "#cccccc",  # Low contrast
                "background_color": "#ffffff",
                "font_size": "14px",
                "font_weight": "normal"
            }
        ]
        
        css_styles = {}
        
        with patch.object(accessibility_checker, '_calculate_contrast_ratio') as mock_contrast:
            # First element has good contrast, second has poor contrast
            mock_contrast.side_effect = [6.0, 2.0]
            
            result = await accessibility_checker._validate_color_contrast(ui_components, css_styles)
            
            assert isinstance(result, AccessibilityTestResult)
            assert result.test_name == "Color Contrast Validation"
            assert len(result.violations) == 1  # One low contrast violation
            assert result.violations[0].wcag_criterion == "1.4.3"
    
    @pytest.mark.asyncio
    async def test_test_keyboard_navigation(self, accessibility_checker):
        """Test keyboard navigation testing."""
        ui_components = [
            {
                "id": "btn1",
                "type": "button",
                "keyboard_accessible": True,
                "tabindex": "0"
            },
            {
                "id": "btn2",
                "type": "button",
                "keyboard_accessible": False,  # Violation
                "tabindex": "1"  # Positive tabindex violation
            }
        ]
        
        html_structure = {}
        
        result = await accessibility_checker._test_keyboard_navigation(ui_components, html_structure)
        
        assert isinstance(result, AccessibilityTestResult)
        assert result.test_name == "Keyboard Navigation Testing"
        assert len(result.violations) == 2  # Not accessible + positive tabindex
        assert any("not keyboard accessible" in v.description for v in result.violations)
        assert any("tabindex" in v.description for v in result.violations)
    
    @pytest.mark.asyncio
    async def test_test_screen_reader_compatibility(self, accessibility_checker):
        """Test screen reader compatibility testing."""
        ui_components = [
            {
                "id": "btn1",
                "type": "button",
                "aria_label": "Submit form",
                "text_content": "Submit"
            },
            {
                "id": "btn2",
                "type": "button",
                # Missing aria_label and text_content - violation
            }
        ]
        
        html_structure = {
            "semantic_elements": ["header", "main", "footer"]
        }
        
        result = await accessibility_checker._test_screen_reader_compatibility(ui_components, html_structure)
        
        assert isinstance(result, AccessibilityTestResult)
        assert result.test_name == "Screen Reader Compatibility"
        assert len(result.violations) == 1  # Missing accessible name
        assert "accessible name" in result.violations[0].description
    
    def test_calculate_contrast_ratio(self, accessibility_checker):
        """Test color contrast ratio calculation."""
        # Test high contrast (black on white)
        ratio1 = accessibility_checker._calculate_contrast_ratio("#000000", "#ffffff")
        assert ratio1 > 10.0  # Should be very high contrast
        
        # Test low contrast (light gray on white)
        ratio2 = accessibility_checker._calculate_contrast_ratio("#cccccc", "#ffffff")
        assert ratio2 < 5.0  # Should be lower contrast
        
        # Test with invalid colors (should not crash)
        ratio3 = accessibility_checker._calculate_contrast_ratio("invalid", "invalid")
        assert ratio3 == 1.0  # Default failing ratio
    
    def test_is_large_text(self, accessibility_checker):
        """Test large text detection."""
        # Large text cases
        assert accessibility_checker._is_large_text("18px", "normal") is True
        assert accessibility_checker._is_large_text("14px", "bold") is True
        assert accessibility_checker._is_large_text("14pt", "normal") is True
        
        # Small text cases
        assert accessibility_checker._is_large_text("14px", "normal") is False
        assert accessibility_checker._is_large_text("12px", "bold") is False
        
        # Invalid format (should not crash)
        assert accessibility_checker._is_large_text("invalid", "normal") is False


class TestUserFlowValidator:
    """Test suite for UserFlowValidator tool."""
    
    @pytest.fixture
    def flow_validator(self):
        """Create UserFlowValidator instance for testing."""
        config = {
            "max_flow_steps": 7,
            "max_completion_time": 10
        }
        return UserFlowValidator(config=config)
    
    @pytest.fixture
    def sample_implementation_data(self):
        """Sample implementation data for flow testing."""
        return {
            "ui_components": [
                {
                    "id": "nav-menu",
                    "type": "menu",
                    "items": ["Home", "Training", "Profile"]
                },
                {
                    "id": "login-form",
                    "type": "form",
                    "fields": ["username", "password"]
                },
                {
                    "id": "submit-btn",
                    "type": "button",
                    "text": "Login"
                }
            ],
            "user_flows": [
                {
                    "flow_id": "login_flow",
                    "flow_name": "User Login",
                    "steps": ["navigate_to_login", "enter_credentials", "submit_form"]
                }
            ],
            "navigation_structure": {
                "menu_items": ["Home", "Training", "Profile"],
                "breadcrumbs": True
            }
        }
    
    @pytest.fixture
    def sample_persona_requirements(self):
        """Sample Anna persona requirements."""
        return {
            "max_task_duration_minutes": 10,
            "min_satisfaction_score": 4.0,
            "accessibility_needs": ["keyboard_navigation", "screen_reader"],
            "complexity_tolerance": "medium"
        }
    
    def test_flow_validator_initialization(self):
        """Test UserFlowValidator initialization."""
        validator = UserFlowValidator()
        
        assert validator.config == {}
        assert len(validator.standard_flows) > 0
        assert validator.flow_validation_criteria["max_steps_per_flow"] == 7
        assert validator.anna_flow_requirements["max_cognitive_load"] == 5
    
    def test_flow_validator_initialization_with_config(self):
        """Test UserFlowValidator initialization with config."""
        config = {"test_setting": "value"}
        validator = UserFlowValidator(config=config)
        
        assert validator.config == config
    
    @pytest.mark.asyncio
    async def test_validate_user_flows_success(self, flow_validator, sample_implementation_data, sample_persona_requirements):
        """Test successful user flow validation."""
        with patch.object(flow_validator, '_identify_applicable_flows', new_callable=AsyncMock) as mock_identify, \
             patch.object(flow_validator, '_validate_single_flow', new_callable=AsyncMock) as mock_validate, \
             patch.object(flow_validator, '_analyze_flow_patterns', new_callable=AsyncMock) as mock_analyze, \
             patch.object(flow_validator, '_validate_navigation_consistency', new_callable=AsyncMock) as mock_nav, \
             patch.object(flow_validator, '_assess_anna_persona_compatibility', new_callable=AsyncMock) as mock_anna:
            
            # Setup mock returns
            mock_flow = UserFlow(
                flow_id="test_flow",
                name="Test Flow",
                description="Test flow description",
                user_goal="Complete test task",
                persona="Anna",
                priority="high",
                steps=[],
                expected_completion_time_minutes=5.0,
                alternative_paths=[],
                error_recovery_paths=[]
            )
            
            mock_identify.return_value = [mock_flow]
            mock_validate.return_value = {
                "flow_id": "test_flow",
                "overall_result": "passed",
                "metrics": {"average_user_experience_score": 4.2}
            }
            mock_analyze.return_value = {"predominant_pattern": "linear_progression"}
            mock_nav.return_value = {"consistency_score": 95}
            mock_anna.return_value = {"compatibility_score": 85, "anna_persona_ready": True}
            
            result = await flow_validator.validate_user_flows(
                story_id="STORY-TEST-001",
                implementation_data=sample_implementation_data,
                persona_requirements=sample_persona_requirements
            )
            
            assert result is not None
            assert result["story_id"] == "STORY-TEST-001"
            assert result["flows_tested"] == 1
            assert "overall_metrics" in result
            assert "flow_validation_results" in result
            assert "pattern_analysis" in result
            assert "navigation_validation" in result
            assert "anna_persona_compatibility" in result
            assert "validation_summary" in result
    
    @pytest.mark.asyncio
    async def test_validate_user_flows_with_exception(self, flow_validator, sample_implementation_data, sample_persona_requirements):
        """Test user flow validation with exception."""
        with patch.object(flow_validator, '_identify_applicable_flows', side_effect=Exception("Flow identification failed")):
            result = await flow_validator.validate_user_flows(
                story_id="STORY-TEST-001",
                implementation_data=sample_implementation_data,
                persona_requirements=sample_persona_requirements
            )
            
            assert "error" in result
            assert "Flow identification failed" in result["error"]
            assert result["validation_failed"] is True
    
    @pytest.mark.asyncio
    async def test_identify_applicable_flows(self, flow_validator):
        """Test identification of applicable flows."""
        implementation_data = {
            "ui_components": [
                {"type": "input", "id": "email"},
                {"type": "button", "id": "submit"}
            ],
            "api_endpoints": [
                {"path": "/auth/login", "method": "POST"}
            ],
            "feature_type": "authentication"
        }
        
        with patch.object(flow_validator, '_create_generic_flow', new_callable=AsyncMock) as mock_generic:
            mock_generic.return_value = UserFlow(
                flow_id="generic_flow",
                name="Generic Flow",
                description="Auto-generated flow",
                user_goal="Complete task",
                persona="Anna",
                priority="medium",
                steps=[],
                expected_completion_time_minutes=5.0,
                alternative_paths=[],
                error_recovery_paths=[]
            )
            
            flows = await flow_validator._identify_applicable_flows(implementation_data, "STORY-AUTH-001")
            
            assert len(flows) >= 1  # Should find registration flow or create generic
            
            # Test with authentication-related story
            if any("auth" in str(endpoint).lower() for endpoint in implementation_data["api_endpoints"]):
                # Should include registration flow
                flow_ids = [flow.flow_id for flow in flows]
                assert any("registration" in flow_id for flow_id in flow_ids)
    
    def test_check_accessibility_requirement(self, flow_validator):
        """Test accessibility requirement checking."""
        ui_components = [
            {"keyboard_accessible": True, "aria_label": "Test button"},
            {"label": "Email", "type": "input"}
        ]
        
        # Test keyboard accessibility
        assert flow_validator._check_accessibility_requirement("keyboard_accessible", ui_components) is True
        
        # Test screen reader compatibility
        assert flow_validator._check_accessibility_requirement("screen_reader_compatible", ui_components) is True
        
        # Test proper labels
        assert flow_validator._check_accessibility_requirement("proper_labels", ui_components) is True
        
        # Test unknown requirement (should default to True)
        assert flow_validator._check_accessibility_requirement("unknown_requirement", ui_components) is True
    
    def test_check_anna_compatibility(self, flow_validator):
        """Test Anna persona compatibility checking."""
        # Compatible scenario
        flow_issues = []
        ux_score = 4.2
        completion_time = 8.0
        
        result = flow_validator._check_anna_compatibility(flow_issues, ux_score, completion_time)
        assert result is True
        
        # Incompatible scenario - critical issue
        from ..tools.user_flow_validator import FlowValidationIssue
        critical_issue = FlowValidationIssue(
            issue_id="test_critical",
            flow_id="test_flow",
            step_id="test_step",
            severity="critical",
            category="usability",
            description="Critical usability issue",
            impact_on_user="Cannot complete task",
            recommended_fix="Fix critical issue",
            affects_accessibility=False,
            affects_anna_persona=True
        )
        
        result = flow_validator._check_anna_compatibility([critical_issue], ux_score, completion_time)
        assert result is False
        
        # Incompatible scenario - time exceeded
        result = flow_validator._check_anna_compatibility([], ux_score, 12.0)
        assert result is False
        
        # Incompatible scenario - low UX score
        result = flow_validator._check_anna_compatibility([], 3.0, completion_time)
        assert result is False
    
    def test_calculate_flow_metrics(self, flow_validator):
        """Test flow metrics calculation."""
        flow_validation_results = [
            {
                "metrics": {
                    "overall_success_rate": 95.0,
                    "average_user_experience_score": 4.2,
                    "average_accessibility_score": 92.0
                },
                "completion_time_minutes": 6.0
            },
            {
                "metrics": {
                    "overall_success_rate": 90.0,
                    "average_user_experience_score": 4.0,
                    "average_accessibility_score": 88.0
                },
                "completion_time_minutes": 8.0
            }
        ]
        
        metrics = flow_validator._calculate_flow_metrics(flow_validation_results)
        
        assert metrics["average_success_rate"] == 92.5  # (95 + 90) / 2
        assert metrics["average_completion_time_minutes"] == 7.0  # (6 + 8) / 2
        assert metrics["average_user_experience_score"] == 4.1  # (4.2 + 4.0) / 2
        assert metrics["average_accessibility_score"] == 90.0  # (92 + 88) / 2
        assert metrics["flows_validated"] == 2
        assert metrics["time_efficiency_rating"] in ["excellent", "good", "needs_improvement"]
    
    def test_calculate_flow_metrics_empty_results(self, flow_validator):
        """Test flow metrics calculation with empty results."""
        metrics = flow_validator._calculate_flow_metrics([])
        
        assert metrics["average_success_rate"] == 0
        assert metrics["average_completion_time_minutes"] == 0
        assert metrics["average_user_experience_score"] == 0
        assert metrics["average_accessibility_score"] == 0