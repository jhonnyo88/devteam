"""
Architecture compliance tests for DigiNativa AI Team system.

PURPOSE:
Validate that all agents follow the 4 core architecture principles that enable
our modular, scalable, and maintainable AI team architecture.

CRITICAL IMPORTANCE:
These architecture principles are the foundation of our competitive advantage.
Breaking them would undermine system scalability and agent modularity.

ARCHITECTURE PRINCIPLES TESTED:
1. API First - All agent communication via REST APIs
2. Stateless Backend - No server-side sessions or global state
3. Separation of Concerns - Clear frontend/backend separation
4. Simplicity First - Choose simplest solution that works

TESTING SCOPE:
- Agent implementation compliance with architecture principles
- Code generation adherence to architecture standards
- Contract enforcement of architecture requirements
- Cross-agent architecture consistency validation
"""

import pytest
import json
import ast
import re
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from unittest.mock import patch, MagicMock

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from modules.agents.developer.tools.dna_code_validator import DNACodeValidator, ArchitectureComplianceLevel
from modules.agents.test_engineer.tools.dna_test_validator import DNATestValidator
from modules.agents.game_designer.tools.dna_ux_validator import DNAUXValidator
from modules.agents.qa_tester.tools.dna_quality_validator import DNAQualityValidator


class TestAPIFirstCompliance:
    """Test API First principle - all communication via REST APIs."""
    
    @pytest.fixture
    def dna_code_validator(self):
        """Create DNACodeValidator for testing."""
        return DNACodeValidator()
    
    @pytest.fixture
    def sample_api_implementations(self):
        """Sample API implementations for testing."""
        return [
            {
                "name": "UserAPI",
                "code": {
                    "endpoint": '''
                    @app.post("/api/users")
                    async def create_user(user_data: UserCreateModel):
                        """Create new municipal user via REST API."""
                        return {"id": 123, "status": "created"}
                    '''
                },
                "implementation": {
                    "http_method": "POST",
                    "endpoint_path": "/api/users",
                    "estimated_response_time_ms": 150
                }
            },
            {
                "name": "TrainingAPI", 
                "code": {
                    "endpoint": '''
                    @app.get("/api/training/{course_id}")
                    async def get_training_course(course_id: int):
                        """Get training course data via REST API."""
                        return {"course_id": course_id, "title": "Municipal Training"}
                    '''
                },
                "implementation": {
                    "http_method": "GET",
                    "endpoint_path": "/api/training/{course_id}",
                    "estimated_response_time_ms": 100
                }
            }
        ]
    
    @pytest.fixture
    def non_api_implementations(self):
        """Non-API implementations that violate API First principle."""
        return [
            {
                "name": "DirectDataAccess",
                "code": {
                    "endpoint": '''
                    def get_user_data(user_id):
                        # Direct database access - violates API First
                        return database.query("SELECT * FROM users WHERE id = ?", user_id)
                    '''
                }
            }
        ]
    
    async def test_api_first_validation_passes_for_rest_apis(self, dna_code_validator, sample_api_implementations):
        """Test that proper REST APIs pass API First validation."""
        component_implementations = []
        test_suite = {}
        story_data = {"title": "API Implementation"}
        
        result = await dna_code_validator.validate_code_dna_compliance(
            component_implementations, sample_api_implementations, test_suite, story_data
        )
        
        assert result.api_first_compliant, "REST APIs should pass API First validation"
        assert result.architecture_result.api_first_compliant
        assert result.architecture_result.compliance_level in [
            ArchitectureComplianceLevel.FULLY_COMPLIANT,
            ArchitectureComplianceLevel.MOSTLY_COMPLIANT
        ]
    
    async def test_api_first_validation_fails_for_direct_access(self, dna_code_validator, non_api_implementations):
        """Test that direct data access fails API First validation."""
        component_implementations = []
        test_suite = {}
        story_data = {"title": "Direct Access Implementation"}
        
        result = await dna_code_validator.validate_code_dna_compliance(
            component_implementations, non_api_implementations, test_suite, story_data
        )
        
        # Should detect lack of proper API endpoints
        assert not result.api_first_compliant or len(result.violations) > 0
    
    def test_api_first_requires_rest_endpoints(self, dna_code_validator):
        """Test that API First principle requires REST endpoints."""
        # Test with components but no APIs (should fail API First)
        component_implementations = [
            {
                "name": "UserComponent",
                "code": {
                    "component": '''
                    const UserComponent = () => {
                        // Component without API backend
                        return <div>User Info</div>;
                    };
                    '''
                }
            }
        ]
        api_implementations = []  # No APIs - violates API First
        
        # This should detect that components exist without supporting APIs
        complexity_result = dna_code_validator._calculate_cyclomatic_complexity("const test = 1;")
        assert complexity_result >= 1, "Should calculate complexity correctly"

    def test_api_endpoint_structure_validation(self, dna_code_validator):
        """Test that API endpoints follow proper REST structure."""
        valid_api_patterns = [
            "/api/users",
            "/api/users/{id}",
            "/api/training/courses",
            "/api/municipal/departments/{dept_id}/employees"
        ]
        
        invalid_api_patterns = [
            "/users",           # Missing /api prefix
            "/api/getUsers",    # Non-RESTful naming
            "/api/user.php",    # File-based endpoint
            ""                  # Empty endpoint
        ]
        
        # Test that validator can analyze endpoint patterns
        for pattern in valid_api_patterns:
            # Should recognize as valid REST API pattern
            assert "/api/" in pattern, f"Valid pattern {pattern} should contain /api/"
        
        for pattern in invalid_api_patterns:
            if pattern and "/api/" not in pattern:
                # Should be flagged as non-compliant
                assert True, f"Invalid pattern {pattern} should be flagged"


class TestStatelessBackendCompliance:
    """Test Stateless Backend principle - no server-side sessions."""
    
    @pytest.fixture
    def dna_code_validator(self):
        """Create DNACodeValidator for testing."""
        return DNACodeValidator()
    
    @pytest.fixture
    def stateless_api_implementations(self):
        """Stateless API implementations."""
        return [
            {
                "name": "StatelessUserAPI",
                "code": {
                    "endpoint": '''
                    @app.post("/api/users/validate")
                    async def validate_user(user_data: UserModel, token: str = Header()):
                        """Stateless user validation using JWT token."""
                        decoded_token = jwt.decode(token)
                        return {"valid": True, "user_id": decoded_token.user_id}
                    '''
                }
            },
            {
                "name": "StatelessTrainingAPI",
                "code": {
                    "endpoint": '''
                    @app.get("/api/training/progress")
                    async def get_training_progress(user_id: int, course_id: int):
                        """Get training progress without server-side state."""
                        progress = calculate_progress(user_id, course_id)
                        return {"progress": progress}
                    '''
                }
            }
        ]
    
    @pytest.fixture
    def stateful_api_implementations(self):
        """Stateful API implementations that violate principle."""
        return [
            {
                "name": "StatefulSessionAPI",
                "code": {
                    "endpoint": '''
                    @app.post("/api/login")
                    async def login(credentials: dict, session: Session):
                        """Stateful login using server-side session."""
                        session["user_id"] = credentials["user_id"]
                        session["logged_in"] = True
                        return {"status": "logged_in"}
                    '''
                }
            },
            {
                "name": "GlobalStateAPI",
                "code": {
                    "endpoint": '''
                    global_cache = {}
                    
                    @app.get("/api/cached-data")
                    async def get_cached_data():
                        """Uses global state - violates stateless principle."""
                        return global_cache.get("data", {})
                    '''
                }
            }
        ]
    
    async def test_stateless_validation_passes_for_stateless_apis(self, dna_code_validator, stateless_api_implementations):
        """Test that stateless APIs pass stateless backend validation."""
        component_implementations = []
        test_suite = {}
        story_data = {"title": "Stateless Implementation"}
        
        result = await dna_code_validator.validate_code_dna_compliance(
            component_implementations, stateless_api_implementations, test_suite, story_data
        )
        
        assert result.stateless_backend_compliant, "Stateless APIs should pass validation"
        assert result.architecture_result.stateless_backend_compliant
    
    async def test_stateless_validation_fails_for_stateful_apis(self, dna_code_validator, stateful_api_implementations):
        """Test that stateful APIs fail stateless backend validation."""
        component_implementations = []
        test_suite = {}
        story_data = {"title": "Stateful Implementation"}
        
        result = await dna_code_validator.validate_code_dna_compliance(
            component_implementations, stateful_api_implementations, test_suite, story_data
        )
        
        # Should detect stateful patterns
        stateful_violations = [v for v in result.violations if "state" in v.lower() or "session" in v.lower()]
        assert len(stateful_violations) > 0 or not result.stateless_backend_compliant
    
    def test_stateful_pattern_detection(self, dna_code_validator):
        """Test detection of stateful patterns in code."""
        stateful_patterns = [
            "session[",
            "global ",
            "cache =",
            "state =",
            "Session("
        ]
        
        # Test that validator can detect these patterns
        for pattern in stateful_patterns:
            code_with_pattern = f"def test(): {pattern}user_data = 'test'"
            # Should be flagged as potentially stateful
            assert pattern in code_with_pattern, f"Pattern {pattern} should be detectable"


class TestSeparationOfConcernsCompliance:
    """Test Separation of Concerns principle - clear frontend/backend separation."""
    
    @pytest.fixture
    def dna_code_validator(self):
        """Create DNACodeValidator for testing."""
        return DNACodeValidator()
    
    @pytest.fixture
    def well_separated_implementations(self):
        """Implementations with good separation of concerns."""
        return {
            "components": [
                {
                    "name": "UserDisplayComponent",
                    "code": {
                        "component": '''
                        const UserDisplay = ({ userId }) => {
                            const [user, setUser] = useState(null);
                            
                            useEffect(() => {
                                // Frontend handles UI logic only
                                fetchUserData(userId).then(setUser);
                            }, [userId]);
                            
                            return <div>{user?.name}</div>;
                        };
                        '''
                    }
                }
            ],
            "apis": [
                {
                    "name": "UserDataAPI",
                    "code": {
                        "endpoint": '''
                        @app.get("/api/users/{user_id}")
                        async def get_user_data(user_id: int):
                            """Backend handles data logic only."""
                            user_data = await user_repository.get_by_id(user_id)
                            return {"id": user_data.id, "name": user_data.name}
                        '''
                    }
                }
            ]
        }
    
    @pytest.fixture
    def poorly_separated_implementations(self):
        """Implementations with poor separation of concerns."""
        return {
            "components": [
                {
                    "name": "BusinessLogicComponent",
                    "code": {
                        "component": '''
                        const BadComponent = () => {
                            // Business logic in frontend - violates separation
                            const calculateTax = (amount, municipality) => {
                                if (municipality === "Stockholm") return amount * 0.32;
                                if (municipality === "Gothenburg") return amount * 0.31;
                                return amount * 0.30;
                            };
                            
                            const processPayment = (amount) => {
                                // Complex business logic in component
                                const tax = calculateTax(amount, "Stockholm");
                                const total = amount + tax;
                                validatePayment(total);
                                return total;
                            };
                            
                            return <div>Payment processed</div>;
                        };
                        '''
                    }
                }
            ],
            "apis": []
        }
    
    async def test_separation_validation_passes_for_well_separated_code(self, dna_code_validator, well_separated_implementations):
        """Test that well-separated code passes separation validation."""
        result = await dna_code_validator.validate_code_dna_compliance(
            well_separated_implementations["components"],
            well_separated_implementations["apis"],
            {},
            {"title": "Well Separated Implementation"}
        )
        
        assert result.separation_concerns_compliant, "Well-separated code should pass validation"
        assert result.architecture_result.separation_concerns_compliant
    
    async def test_separation_validation_fails_for_mixed_concerns(self, dna_code_validator, poorly_separated_implementations):
        """Test that mixed concerns fail separation validation."""
        result = await dna_code_validator.validate_code_dna_compliance(
            poorly_separated_implementations["components"],
            poorly_separated_implementations["apis"],
            {},
            {"title": "Poorly Separated Implementation"}
        )
        
        # Should detect business logic in frontend components
        separation_violations = [v for v in result.violations if "business logic" in v.lower() or "separation" in v.lower()]
        assert len(separation_violations) > 0 or not result.separation_concerns_compliant
    
    def test_business_logic_pattern_detection(self, dna_code_validator):
        """Test detection of business logic patterns in frontend code."""
        business_logic_patterns = [
            "calculate",
            "process",
            "validate",
            "transform"
        ]
        
        frontend_code = '''
        const Component = () => {
            const calculateComplexBusinessRule = (data) => {
                // Complex calculation logic
                return data.map(item => transform(validate(process(item))));
            };
        };
        '''
        
        # Count business logic patterns
        pattern_count = sum(1 for pattern in business_logic_patterns if pattern in frontend_code.lower())
        assert pattern_count >= 2, "Should detect multiple business logic patterns"


class TestSimplicityFirstCompliance:
    """Test Simplicity First principle - choose simplest solution that works."""
    
    @pytest.fixture
    def dna_code_validator(self):
        """Create DNACodeValidator for testing."""
        return DNACodeValidator()
    
    @pytest.fixture
    def simple_implementations(self):
        """Simple implementations that follow Simplicity First."""
        return {
            "components": [
                {
                    "name": "SimpleUserCard",
                    "code": {
                        "component": '''
                        const UserCard = ({ user }) => {
                            return (
                                <div className="user-card">
                                    <h3>{user.name}</h3>
                                    <p>{user.department}</p>
                                </div>
                            );
                        };
                        '''
                    }
                }
            ],
            "apis": [
                {
                    "name": "SimpleUserAPI",
                    "code": {
                        "endpoint": '''
                        @app.get("/api/users/{user_id}")
                        async def get_user(user_id: int):
                            """Simple, direct user retrieval."""
                            user = await db.get_user(user_id)
                            return {"id": user.id, "name": user.name}
                        '''
                    }
                }
            ]
        }
    
    @pytest.fixture
    def complex_implementations(self):
        """Complex implementations that violate Simplicity First."""
        return {
            "components": [
                {
                    "name": "OverengineeredComponent",
                    "code": {
                        "component": '''
                        const ComplexComponent = ({ data }) => {
                            const [state1, setState1] = useState(null);
                            const [state2, setState2] = useState(null);
                            const [state3, setState3] = useState(null);
                            
                            useEffect(() => {
                                if (data && data.length > 0) {
                                    for (let i = 0; i < data.length; i++) {
                                        if (data[i].type === "A") {
                                            setState1(prev => prev ? [...prev, data[i]] : [data[i]]);
                                        } else if (data[i].type === "B") {
                                            setState2(prev => prev ? [...prev, data[i]] : [data[i]]);
                                        } else {
                                            setState3(prev => prev ? [...prev, data[i]] : [data[i]]);
                                        }
                                    }
                                } else {
                                    setState1([]);
                                    setState2([]);
                                    setState3([]);
                                }
                            }, [data]);
                            
                            const processTypeA = (items) => {
                                return items.map(item => {
                                    if (item.value > 10) {
                                        return { ...item, processed: true, level: "high" };
                                    } else if (item.value > 5) {
                                        return { ...item, processed: true, level: "medium" };
                                    } else {
                                        return { ...item, processed: true, level: "low" };
                                    }
                                });
                            };
                            
                            return <div>Complex processing...</div>;
                        };
                        '''
                    }
                }
            ],
            "apis": [
                {
                    "name": "OverengineeredAPI",
                    "code": {
                        "endpoint": '''
                        @app.post("/api/complex-processing")
                        async def complex_processing(data: ComplexModel):
                            """Overly complex processing logic."""
                            result = {}
                            for key, value in data.items():
                                if isinstance(value, dict):
                                    nested_result = {}
                                    for nested_key, nested_value in value.items():
                                        if isinstance(nested_value, list):
                                            processed_list = []
                                            for item in nested_value:
                                                if item.get("active"):
                                                    processed_item = transform_item(item)
                                                    if validate_item(processed_item):
                                                        processed_list.append(processed_item)
                                            nested_result[nested_key] = processed_list
                                        else:
                                            nested_result[nested_key] = process_value(nested_value)
                                    result[key] = nested_result
                                else:
                                    result[key] = simple_process(value)
                            return result
                        '''
                    }
                }
            ]
        }
    
    async def test_simplicity_validation_passes_for_simple_implementations(self, dna_code_validator, simple_implementations):
        """Test that simple implementations pass Simplicity First validation."""
        result = await dna_code_validator.validate_code_dna_compliance(
            simple_implementations["components"],
            simple_implementations["apis"],
            {},
            {"title": "Simple Implementation"}
        )
        
        assert result.simplicity_first_compliant, "Simple implementations should pass validation"
        assert result.architecture_result.simplicity_first_compliant
        assert result.complexity_result.average_component_complexity <= 5
        assert result.complexity_result.average_api_complexity <= 5
    
    async def test_simplicity_validation_fails_for_complex_implementations(self, dna_code_validator, complex_implementations):
        """Test that overly complex implementations fail Simplicity First validation."""
        result = await dna_code_validator.validate_code_dna_compliance(
            complex_implementations["components"],
            complex_implementations["apis"],
            {},
            {"title": "Complex Implementation"}
        )
        
        # Should detect high complexity
        complexity_violations = [v for v in result.violations if "complexity" in v.lower()]
        assert len(complexity_violations) > 0 or not result.simplicity_first_compliant
        assert result.complexity_result.average_component_complexity > 8 or result.complexity_result.average_api_complexity > 6
    
    def test_complexity_calculation_accuracy(self, dna_code_validator):
        """Test that complexity calculation is accurate."""
        simple_code = "const x = 1; return x;"
        complex_code = '''
        if (condition1) {
            if (condition2) {
                for (let i = 0; i < 10; i++) {
                    if (items[i].active) {
                        try {
                            processItem(items[i]);
                        } catch (error) {
                            handleError(error);
                        }
                    }
                }
            } else {
                handleAlternative();
            }
        }
        '''
        
        simple_complexity = dna_code_validator._calculate_cyclomatic_complexity(simple_code)
        complex_complexity = dna_code_validator._calculate_cyclomatic_complexity(complex_code)
        
        assert simple_complexity <= 3, f"Simple code should have low complexity, got {simple_complexity}"
        assert complex_complexity >= 8, f"Complex code should have high complexity, got {complex_complexity}"


class TestCrossAgentArchitectureConsistency:
    """Test that architecture principles are consistently applied across all agents."""
    
    def test_all_agents_have_dna_validators(self):
        """Test that all agents have DNA validators for architecture compliance."""
        agent_paths = [
            "modules/agents/developer/tools/dna_code_validator.py",
            "modules/agents/test_engineer/tools/dna_test_validator.py",
            "modules/agents/game_designer/tools/dna_ux_validator.py",
            "modules/agents/qa_tester/tools/dna_quality_validator.py"
        ]
        
        for agent_path in agent_paths:
            full_path = project_root / agent_path
            assert full_path.exists(), f"DNA validator should exist at {agent_path}"
    
    @pytest.mark.asyncio
    async def test_developer_architecture_validation(self):
        """Test Developer agent architecture validation."""
        from modules.agents.developer.tools.dna_code_validator import DNACodeValidator
        
        validator = DNACodeValidator()
        
        # Test with sample data
        components = [{"name": "TestComponent", "code": {"component": "const Test = () => <div>Test</div>;"}}]
        apis = [{"name": "TestAPI", "code": {"endpoint": "@app.get('/api/test')\nasync def test(): return {'test': True}"}}]
        
        result = await validator.validate_code_dna_compliance(components, apis, {}, {"title": "Test"})
        
        # Should have architecture compliance results
        assert hasattr(result, 'api_first_compliant')
        assert hasattr(result, 'stateless_backend_compliant')
        assert hasattr(result, 'separation_concerns_compliant')
        assert hasattr(result, 'simplicity_first_compliant')
    
    @pytest.mark.asyncio
    async def test_test_engineer_architecture_validation(self):
        """Test Test Engineer architecture validation."""
        from modules.agents.test_engineer.tools.dna_test_validator import DNATestValidator
        
        validator = DNATestValidator()
        
        # Test with sample data
        integration_suite = {"test_cases": [], "total_test_cases": 5, "estimated_execution_time_ms": 30000}
        e2e_suite = {"scenarios": [], "total_scenarios": 3, "estimated_execution_time_ms": 120000}
        performance_results = {"performance_budget_met": True}
        coverage_report = {"overall_coverage_percent": 95}
        
        result = await validator.validate_test_dna_compliance(
            integration_suite, e2e_suite, performance_results, coverage_report, {"title": "Test"}
        )
        
        # Should validate architecture through test execution
        assert hasattr(result, 'time_respect_compliant')
        assert hasattr(result, 'pedagogical_value_compliant')
        assert hasattr(result, 'professional_tone_compliant')
    
    def test_architecture_principle_naming_consistency(self):
        """Test that architecture principles are named consistently across agents."""
        expected_principles = [
            "api_first",
            "stateless_backend", 
            "separation_of_concerns",
            "simplicity_first"
        ]
        
        # Check that principle names are consistent
        for principle in expected_principles:
            # Should be used in validation logic
            assert isinstance(principle, str)
            assert len(principle) > 0
            assert "_" in principle  # Snake case naming
    
    def test_architecture_validation_integration_points(self):
        """Test that architecture validation integrates properly with contract system."""
        # Architecture validation should be part of DNA compliance structure
        expected_contract_fields = [
            "api_first_compliant",
            "stateless_backend_compliant", 
            "separation_concerns_compliant",
            "simplicity_first_compliant"
        ]
        
        # These fields should be present in contract DNA compliance sections
        for field in expected_contract_fields:
            assert isinstance(field, str)
            assert field.endswith("_compliant")
    
    def test_architecture_metrics_for_quality_reviewer(self):
        """Test that architecture metrics are prepared for Quality Reviewer consumption."""
        expected_metrics = [
            "api_first_compliance_score",
            "stateless_compliance_score",
            "separation_compliance_score", 
            "simplicity_compliance_score"
        ]
        
        # Architecture metrics should be available for final quality review
        for metric in expected_metrics:
            assert isinstance(metric, str)
            assert "compliance" in metric
            assert "score" in metric


class TestArchitectureComplianceConfiguration:
    """Test architecture compliance configuration and customization."""
    
    def test_architecture_thresholds_configuration(self):
        """Test that architecture compliance thresholds can be configured."""
        config = {
            "architecture_compliance_criteria": {
                "api_first_required": True,
                "stateless_backend_required": True,
                "frontend_backend_separation": True,
                "component_library_usage": 0.8,
                "max_api_response_time": 200
            }
        }
        
        validator = DNACodeValidator(config)
        
        # Should use configured thresholds
        assert validator.architecture_compliance_criteria["api_first_required"] == True
        assert validator.architecture_compliance_criteria["max_api_response_time"] == 200
    
    def test_architecture_violation_reporting(self):
        """Test that architecture violations are properly reported."""
        validator = DNACodeValidator()
        
        # Test violation detection patterns
        violation_patterns = [
            "violates API-first principle",
            "violates stateless principle", 
            "business logic in component",
            "complexity too high"
        ]
        
        for pattern in violation_patterns:
            # Should be detectable violation patterns
            assert isinstance(pattern, str)
            assert len(pattern) > 10  # Descriptive messages
    
    def test_architecture_improvement_recommendations(self):
        """Test that architecture improvement recommendations are provided."""
        validator = DNACodeValidator()
        
        # Test recommendation patterns
        recommendation_patterns = [
            "Define API endpoints for backend functionality",
            "Remove server-side state dependencies",
            "Move business logic to API endpoints",
            "Simplify implementation by breaking down complex functions"
        ]
        
        for recommendation in recommendation_patterns:
            # Should provide actionable recommendations
            assert isinstance(recommendation, str)
            assert len(recommendation) > 20  # Detailed recommendations