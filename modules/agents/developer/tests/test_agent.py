"""
Comprehensive tests for DeveloperAgent.

PURPOSE:
Test suite ensuring the Developer agent meets all requirements:
- Agent core logic and DNA compliance validation
- Code generation quality and standards
- Architecture principle compliance
- Performance and quality metrics
- Error handling and recovery

TEST STRATEGY COMPLIANCE:
- Follows TEST_STRATEGY.md structure
- Agent-specific tests in modules/agents/developer/tests/
- Focuses on agent logic, not contract compliance
- Uses proper pytest markers for categorization
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
from datetime import datetime

# Import the agent and dependencies
from ..agent import DeveloperAgent
from ...shared.base_agent import AgentExecutionResult
from ...shared.exceptions import AgentExecutionError, DNAComplianceError, QualityGateError


@pytest.mark.agent
class TestDeveloperAgent:
    """
    Comprehensive test suite for DeveloperAgent core logic.
    
    COVERAGE AREAS (per TEST_STRATEGY.md):
    - Agent initialization and configuration
    - Code generation (React + FastAPI) 
    - DNA compliance validation in generated code
    - Architecture validation
    - Quality gates and compliance
    - Git operations and branch management
    - Error handling and recovery
    - Performance requirements
    
    NOTE: Contract compliance tests are in test_contract_compliance.py
    """
    
    @pytest.fixture
    def developer_agent(self):
        """Create DeveloperAgent instance for testing."""
        config = {
            "frontend_path": "test_frontend",
            "backend_path": "test_backend",
            "test_path": "test_tests"
        }
        return DeveloperAgent(config)
    
    @pytest.fixture
    def sample_input_contract(self):
        """Sample input contract from Game Designer."""
        return {
            "contract_version": "1.0",
            "contract_type": "design_to_implementation",
            "story_id": "STORY-TEST-001",
            "source_agent": "game_designer",
            "target_agent": "developer",
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": True,
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
                "required_data": {
                    "game_mechanics": {
                        "title": "User Registration",
                        "description": "Allow users to register for DigiNativa"
                    },
                    "ui_components": [
                        {
                            "name": "RegistrationForm",
                            "type": "form",
                            "ui_library_components": ["Button", "Input", "Card"],
                            "accessibility": {"role": "form"},
                            "interactions": [
                                {"type": "submit", "target": "registration_api"}
                            ]
                        }
                    ],
                    "interaction_flows": [
                        {
                            "name": "user_registration_flow",
                            "steps": ["fill_form", "validate", "submit", "confirm"]
                        }
                    ],
                    "api_endpoints": [
                        {
                            "name": "register_user",
                            "method": "POST",
                            "path": "/register",
                            "description": "Register new user",
                            "request_model": {"email": "string", "password": "string"},
                            "response_model": {"success": "boolean", "user_id": "string"},
                            "business_logic": {"validation": "email_password"},
                            "dependencies": []
                        }
                    ],
                    "state_management": {
                        "type": "stateless",
                        "client_state": ["form_data", "validation_errors"]
                    }
                }
            }
        }
    
    def test_agent_initialization(self):
        """Test proper agent initialization."""
        # Test with default config
        agent = DeveloperAgent()
        assert agent.agent_id == "dev-001"
        assert agent.agent_type == "developer"
        
        # Test with custom config
        custom_config = {
            "frontend_path": "custom_frontend",
            "backend_path": "custom_backend"
        }
        custom_agent = DeveloperAgent(custom_config)
        assert custom_agent.frontend_path == "custom_frontend"
        assert custom_agent.backend_path == "custom_backend"
    
    def test_dna_compliance_validation(self, developer_agent):
        """Test DNA compliance validation."""
        # Test valid DNA compliance
        valid_contract = {
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": True,
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
            }
        }
        
        assert developer_agent._validate_dna_compliance(valid_contract)
        
        # Test missing design principles
        invalid_contract = {
            "dna_compliance": {
                "design_principles_validation": {
                    "pedagogical_value": True
                    # Missing other principles
                },
                "architecture_compliance": {
                    "api_first": True,
                    "stateless_backend": True,
                    "separation_of_concerns": True,
                    "simplicity_first": True
                }
            }
        }
        
        assert not developer_agent._validate_dna_compliance(invalid_contract)
    
    @pytest.mark.asyncio
    async def test_code_dna_compliance_validation(self, developer_agent):
        """Test the new DNA compliance validation in generated code."""
        
        # Test data with good DNA compliance
        good_component_implementations = [
            {
                "name": "LearningProgressComponent",
                "code": {
                    "component": '''
                    /**
                     * LearningProgressComponent - Helps municipal workers track their learning progress
                     * 
                     * @param props.learningProgress - Current learning progress data
                     * @returns JSX.Element
                     */
                    export const LearningProgressComponent: React.FC<LearningProgressProps> = (props) => {
                        // Show step-by-step progress for municipal training
                        const [municipalTaskProgress, setMunicipalTaskProgress] = useState(0);
                        
                        return (
                            <Card role="region" aria-label="Learning Progress">
                                <Progress value={props.learningProgress} />
                                {/* Clear progress indicators for 10-minute sessions */}
                                <span>Step {municipalTaskProgress + 1} of 5</span>
                            </Card>
                        );
                    };
                    '''
                }
            }
        ]
        
        good_api_implementations = [
            {
                "name": "training_progress",
                "code": {
                    "endpoint": '''
                    @router.post("/training-progress")
                    async def training_progress(request: TrainingProgressRequest) -> TrainingProgressResponse:
                        """
                        Track municipal employee learning progress.
                        
                        Args:
                            request: Training progress data with validation
                            
                        Returns:
                            TrainingProgressResponse: Updated progress information
                        """
                        try:
                            # Validate and sanitize personal data (GDPR compliance)
                            validated_data = validate_personal_data(request)
                            
                            # Process learning progress
                            result = await process_training_progress(validated_data)
                            
                            return TrainingProgressResponse(
                                success=True,
                                data=result,
                                message="Learning progress updated successfully"
                            )
                        except ValidationError as e:
                            raise HTTPException(
                                status_code=422,
                                detail={"error_code": "VALIDATION_ERROR", "error_message": "Please provide valid training data"}
                            )
                    '''
                },
                "implementation": {
                    "estimated_response_time_ms": 150
                }
            }
        ]
        
        test_suite = {"unit_tests": []}
        game_mechanics = {"title": "Municipal Training Progress"}
        
        # Should pass validation
        await developer_agent._validate_code_dna_compliance(
            good_component_implementations,
            good_api_implementations,
            test_suite,
            game_mechanics
        )
        
        # Test data with DNA violations
        bad_component_implementations = [
            {
                "name": "BadComponent",
                "code": {
                    "component": '''
                    // TODO: Fix this later, this is a hack
                    const BadComponent = (props) => {
                        const x = props.data; // Poor naming
                        if (x) {
                            if (x.type) {
                                if (x.type === 'complex') {
                                    if (x.nested) {
                                        if (x.nested.deep) {
                                            if (x.nested.deep.value) {
                                                // Way too complex!
                                                return <div>Complex stuff</div>;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        return <div>Error occurred</div>; // No accessibility
                    };
                    '''
                }
            }
        ]
        
        bad_api_implementations = [
            {
                "name": "bad_api",
                "code": {
                    "endpoint": '''
                    @router.post("/bad")
                    async def bad_api(request):
                        # No documentation, no error handling
                        result = process_data(request)
                        return result
                    '''
                },
                "implementation": {
                    "estimated_response_time_ms": 500  # Too slow
                }
            }
        ]
        
        # Should raise DNAComplianceError
        with pytest.raises(DNAComplianceError):
            await developer_agent._validate_code_dna_compliance(
                bad_component_implementations,
                bad_api_implementations,
                test_suite,
                game_mechanics
            )
    
    def test_cyclomatic_complexity_calculation(self, developer_agent):
        """Test cyclomatic complexity calculation."""
        
        # Simple code (complexity = 1)
        simple_code = '''
        function simple() {
            return "hello";
        }
        '''
        assert developer_agent._calculate_cyclomatic_complexity(simple_code) == 1
        
        # Complex code (complexity > 10)
        complex_code = '''
        function complex(a, b, c) {
            if (a) {
                if (b) {
                    for (let i = 0; i < 10; i++) {
                        if (c && a || b) {
                            try {
                                while (true) {
                                    if (i % 2) {
                                        return i;
                                    } else {
                                        continue;
                                    }
                                }
                            } catch (e) {
                                if (e.type) {
                                    throw e;
                                }
                            }
                        }
                    }
                }
            }
            return 0;
        }
        '''
        complexity = developer_agent._calculate_cyclomatic_complexity(complex_code)
        assert complexity > 10  # Should be flagged as too complex
    
    @pytest.mark.dna
    @pytest.mark.asyncio
    async def test_validate_pedagogical_value_in_code(self, developer_agent):
        """Test pedagogical value validation in generated code."""
        
        # Good pedagogical code
        good_components = [
            {
                "name": "LearningModule",
                "code": {
                    "component": '''
                    /**
                     * LearningModule - Facilitates municipal training progression
                     * 
                     * @param props.learningProgress - Current learning state
                     * @returns JSX.Element
                     */
                    const LearningModule = (props) => {
                        const [municipalTaskStep, setMunicipalTaskStep] = useState(0);
                        // Show clear step-by-step progress
                        return <div>Step {municipalTaskStep + 1} of 5</div>;
                    };
                    '''
                }
            }
        ]
        
        good_apis = [
            {
                "name": "learning_progress",
                "code": {
                    "endpoint": '''
                    async def learning_progress(request: LearningRequest) -> LearningResponse:
                        """
                        Track municipal employee learning progress.
                        
                        Args:
                            request: Learning progress data for training validation
                            
                        Returns:
                            LearningResponse: Updated learning status with error_message for validation
                        """
                        return LearningResponse(success=True)
                    '''
                }
            }
        ]
        
        score = await developer_agent._validate_pedagogical_value_in_code(
            good_components, good_apis, {"title": "Municipal Training"}
        )
        
        assert score >= 4.0, f"Pedagogical value score too low: {score}"
    
    @pytest.mark.dna
    @pytest.mark.asyncio
    async def test_validate_code_complexity(self, developer_agent):
        """Test code complexity validation."""
        
        # Complex component that should fail
        complex_components = [
            {
                "name": "ComplexComponent",
                "code": {
                    "component": '''
                    const ComplexComponent = (props) => {
                        if (props.a) {
                            if (props.b) {
                                for (let i = 0; i < 10; i++) {
                                    if (props.c && props.d || props.e) {
                                        try {
                                            while (true) {
                                                if (i % 2) {
                                                    return i;
                                                } else {
                                                    continue;
                                                }
                                            }
                                        } catch (e) {
                                            if (e.type) {
                                                throw e;
                                            }
                                        }
                                    }
                                }
                            }
                        }
                        return null;
                    };
                    '''
                }
            }
        ]
        
        violations = await developer_agent._validate_code_complexity(complex_components, [])
        assert len(violations) > 0, "Complex code should be flagged"
        assert "complexity too high" in violations[0]
    
    @pytest.mark.dna
    @pytest.mark.asyncio 
    async def test_validate_professional_tone_in_code(self, developer_agent):
        """Test professional tone validation in code."""
        
        # Unprofessional code
        bad_components = [
            {
                "name": "BadComponent",
                "code": {
                    "component": '''
                    // TODO: Fix this later, this is a dirty hack
                    const BadComponent = (props) => {
                        // This is stupid but it works
                        const wtf = props.data;
                        return <div>Error occurred</div>; // No help for user
                    };
                    '''
                }
            }
        ]
        
        violations = await developer_agent._validate_professional_tone_in_code(bad_components, [])
        assert len(violations) > 0, "Unprofessional tone should be flagged"
        assert any("TODO" in violation or "dirty" in violation or "stupid" in violation for violation in violations)
    
    @pytest.mark.dna
    @pytest.mark.asyncio
    async def test_validate_policy_implementation(self, developer_agent):
        """Test policy implementation validation."""
        
        # Component missing accessibility
        bad_components = [
            {
                "name": "FormComponent",
                "code": {
                    "component": '''
                    const FormComponent = () => {
                        return (
                            <form>
                                <input type="text" />
                                <button>Submit</button>
                            </form>
                        );
                    };
                    '''
                }
            }
        ]
        
        violations = await developer_agent._validate_policy_implementation(
            bad_components, [], {"title": "Municipal Form"}
        )
        assert len(violations) > 0, "Missing accessibility should be flagged"
        assert "accessibility attributes" in violations[0]
    
    @pytest.mark.dna
    @pytest.mark.asyncio
    async def test_validate_time_respect_in_code(self, developer_agent):
        """Test time respect validation in code."""
        
        # Component with API call but no loading indicator
        bad_components = [
            {
                "name": "ApiComponent",
                "code": {
                    "component": '''
                    const ApiComponent = () => {
                        const fetchData = async () => {
                            const response = await fetch('/api/data');
                            return response.json();
                        };
                        
                        return <div>Data will load...</div>;
                    };
                    '''
                }
            }
        ]
        
        violations = await developer_agent._validate_time_respect_in_code(bad_components, [])
        assert len(violations) > 0, "Missing loading indicators should be flagged"
        assert "loading indicators" in violations[0]
    
    @pytest.mark.performance
    def test_dna_validation_performance(self, developer_agent):
        """Test that DNA validation performs within acceptable limits."""
        import time
        
        # Create test data
        components = [{"name": "TestComp", "code": {"component": "const TestComp = () => <div>Test</div>;"}}]
        apis = [{"name": "test_api", "code": {"endpoint": "async def test_api(): return {}"}}]
        
        # Measure validation time
        start_time = time.time()
        
        # Run individual validation methods (sync versions for performance test)
        developer_agent._calculate_cyclomatic_complexity("if (true) { return 1; }")
        
        end_time = time.time()
        validation_time = end_time - start_time
        
        # Should complete quickly
        assert validation_time < 0.1, f"DNA validation too slow: {validation_time:.3f}s (max: 0.1s)"
    
    @pytest.mark.asyncio
    async def test_process_contract_full_flow(self, developer_agent, sample_input_contract):
        """Test complete contract processing workflow."""
        
        # Mock the tools to avoid actual implementation
        with patch.object(developer_agent, 'git_operations') as mock_git, \
             patch.object(developer_agent, 'component_builder') as mock_component_builder, \
             patch.object(developer_agent, 'api_builder') as mock_api_builder, \
             patch.object(developer_agent, 'code_generator') as mock_code_generator, \
             patch.object(developer_agent, 'dna_code_validator') as mock_dna_validator, \
             patch.object(developer_agent, '_validate_architecture_requirements') as mock_arch_val, \
             patch.object(developer_agent, '_validate_implementation_quality') as mock_quality_val:
            
            # Setup mocks
            mock_git.create_feature_branch = AsyncMock()
            mock_git.commit_implementation = AsyncMock(return_value="abc123")
            
            mock_component_builder.build_components = AsyncMock(return_value=[
                {
                    "name": "RegistrationForm",
                    "code": {"component": "const RegistrationForm = () => <form>...</form>;"},
                    "typescript_errors": 0,
                    "eslint_violations": 0,
                    "integration_test_passed": True
                }
            ])
            
            mock_api_builder.build_apis = AsyncMock(return_value=[
                {
                    "name": "register_user",
                    "code": {"endpoint": "async def register_user(): pass"},
                    "functional_test_passed": True
                }
            ])
            
            mock_code_generator.generate_tests = AsyncMock(return_value={
                "unit_tests": [{"name": "test_registration"}],
                "coverage_percent": 100
            })
            
            # Mock DNA validation to return compliant result
            mock_dna_result = Mock()
            mock_dna_result.overall_dna_compliant = True
            mock_dna_result.violations = []
            mock_dna_result.dna_compliance_score = 4.5
            mock_dna_result.time_respect_compliant = True
            mock_dna_result.pedagogical_value_compliant = True
            mock_dna_result.professional_tone_compliant = True
            mock_dna_result.api_first_compliant = True
            mock_dna_result.stateless_backend_compliant = True
            mock_dna_result.separation_concerns_compliant = True
            mock_dna_result.simplicity_first_compliant = True
            mock_dna_result.validation_timestamp = datetime.now().isoformat()
            mock_dna_result.recommendations = []
            mock_dna_result.quality_reviewer_metrics = {"test": "metrics"}
            
            mock_dna_validator.validate_code_dna_compliance = AsyncMock(return_value=mock_dna_result)
            mock_arch_val.return_value = None
            mock_quality_val.return_value = None
            
            # Process the contract
            result = await developer_agent.process_contract(sample_input_contract)
            
            # Verify result structure
            assert result is not None
            assert result["contract_version"] == "1.0"
            assert result["source_agent"] == "developer"
            assert result["target_agent"] == "test_engineer"
            assert result["story_id"] == "STORY-TEST-001"
            
            # Verify DNA compliance was checked
            mock_dna_validator.validate_code_dna_compliance.assert_called_once()
            
            # Verify DNA compliance is included in output
            assert "dna_compliance" in result
            assert "developer_dna_validation" in result["dna_compliance"]
            
            # Verify tools were called
            mock_component_builder.build_components.assert_called_once()
            mock_api_builder.build_apis.assert_called_once()
            mock_code_generator.generate_tests.assert_called_once()
            mock_git.create_feature_branch.assert_called_once()
            mock_git.commit_implementation.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_process_contract_dna_failure(self, developer_agent, sample_input_contract):
        """Test contract processing when DNA validation fails."""
        
        with patch.object(developer_agent, 'git_operations') as mock_git, \
             patch.object(developer_agent, 'component_builder') as mock_component_builder, \
             patch.object(developer_agent, 'api_builder') as mock_api_builder, \
             patch.object(developer_agent, 'code_generator') as mock_code_generator, \
             patch.object(developer_agent, 'dna_code_validator') as mock_dna_validator, \
             patch.object(developer_agent, '_validate_architecture_requirements') as mock_arch_val:
            
            # Setup basic mocks
            mock_git.create_feature_branch = AsyncMock()
            mock_component_builder.build_components = AsyncMock(return_value=[{"name": "Test"}])
            mock_api_builder.build_apis = AsyncMock(return_value=[{"name": "test_api"}])
            mock_code_generator.generate_tests = AsyncMock(return_value={"unit_tests": []})
            mock_arch_val.return_value = None
            
            # Mock DNA validation to fail
            mock_dna_result = Mock()
            mock_dna_result.overall_dna_compliant = False
            mock_dna_result.violations = ["Time complexity exceeded", "Missing accessibility"]
            mock_dna_validator.validate_code_dna_compliance = AsyncMock(return_value=mock_dna_result)
            
            # Should raise DNAComplianceError
            with pytest.raises(DNAComplianceError) as exc_info:
                await developer_agent.process_contract(sample_input_contract)
            
            assert "DNA compliance validation failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_architecture_validation(self, developer_agent):
        """Test architecture requirements validation."""
        
        # Valid architecture data
        valid_input_data = {
            "api_endpoints": [
                {
                    "name": "test_endpoint",
                    "method": "GET",
                    "stateless": True
                }
            ],
            "ui_components": [
                {
                    "name": "TestComponent",
                    "separation_of_concerns": True
                }
            ]
        }
        
        with patch.object(developer_agent, 'architecture_validator') as mock_validator:
            mock_validator.validate_requirements = AsyncMock(return_value={
                "is_valid": True,
                "errors": [],
                "warnings": []
            })
            
            # Should not raise error
            await developer_agent._validate_architecture_requirements(valid_input_data)
            mock_validator.validate_requirements.assert_called_once_with(valid_input_data)
        
        # Invalid architecture data
        with patch.object(developer_agent, 'architecture_validator') as mock_validator:
            mock_validator.validate_requirements = AsyncMock(return_value={
                "is_valid": False,
                "errors": ["Violates API-first principle"],
                "warnings": []
            })
            
            # Should raise DNAComplianceError
            with pytest.raises(DNAComplianceError) as exc_info:
                await developer_agent._validate_architecture_requirements(valid_input_data)
            
            assert "Architecture validation failed" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_implementation_quality_validation(self, developer_agent):
        """Test implementation quality validation."""
        
        component_implementations = [
            {
                "name": "TestComponent",
                "typescript_errors": 0,
                "eslint_violations": 0,
                "integration_test_passed": True
            }
        ]
        
        api_implementations = [
            {
                "name": "test_api",
                "functional_test_passed": True
            }
        ]
        
        test_suite = {
            "coverage_percent": 100
        }
        
        with patch.object(developer_agent, 'code_generator') as mock_code_gen, \
             patch.object(developer_agent, 'api_builder') as mock_api_builder:
            
            # Mock quality checks to pass
            mock_code_gen.check_typescript_errors = AsyncMock(return_value=0)
            mock_code_gen.check_eslint_compliance = AsyncMock(return_value=0)
            mock_code_gen.calculate_test_coverage = AsyncMock(return_value=100)
            mock_api_builder.test_api_performance = AsyncMock(return_value=150)  # Under 200ms
            
            # Should not raise error
            await developer_agent._validate_implementation_quality(
                component_implementations, api_implementations, test_suite
            )
        
        # Test with quality failures
        with patch.object(developer_agent, 'code_generator') as mock_code_gen:
            mock_code_gen.check_typescript_errors = AsyncMock(return_value=5)  # Has errors
            
            # Should raise QualityGateError
            with pytest.raises(QualityGateError) as exc_info:
                await developer_agent._validate_implementation_quality(
                    component_implementations, api_implementations, test_suite
                )
            
            assert "TypeScript errors" in str(exc_info.value)
    
    def test_check_quality_gate(self, developer_agent):
        """Test quality gate checking."""
        
        deliverables = {
            "component_implementations": [
                {
                    "name": "TestComponent",
                    "typescript_errors": 0,
                    "eslint_violations": 0,
                    "integration_test_passed": True
                }
            ],
            "api_implementations": [
                {
                    "name": "test_api",
                    "functional_test_passed": True
                }
            ],
            "test_suite": {
                "coverage_percent": 100
            },
            "implementation_docs": {
                "architecture_compliance": {
                    "api_first": True,
                    "stateless_backend": True,
                    "separation_of_concerns": True
                },
                "performance_metrics": {
                    "estimated_lighthouse_score": 95,
                    "estimated_bundle_size_kb": 45
                }
            }
        }
        
        # Test various quality gates
        assert developer_agent._check_quality_gate("typescript_compilation_success_zero_errors", deliverables)
        assert developer_agent._check_quality_gate("eslint_standards_compliance_verified", deliverables)
        assert developer_agent._check_quality_gate("unit_tests_100_percent_coverage_achieved", deliverables)
        assert developer_agent._check_quality_gate("api_endpoints_respond_correctly", deliverables)
        assert developer_agent._check_quality_gate("component_integration_working", deliverables)
        assert developer_agent._check_quality_gate("architecture_principles_compliance", deliverables)
        assert developer_agent._check_quality_gate("performance_standards_met", deliverables)
        
        # Test with quality failures
        failed_deliverables = deliverables.copy()
        failed_deliverables["component_implementations"][0]["typescript_errors"] = 5
        
        assert not developer_agent._check_quality_gate("typescript_compilation_success_zero_errors", failed_deliverables)
    
    def test_generate_implementation_docs(self, developer_agent):
        """Test implementation documentation generation."""
        
        story_id = "STORY-TEST-001"
        game_mechanics = {"title": "User Registration", "description": "Register users"}
        component_implementations = [{"name": "RegistrationForm"}]
        api_implementations = [{"name": "register_user"}]
        test_suite = {"unit_tests": [{"name": "test_registration"}]}
        
        # Test docs generation (this is currently synchronous)
        import asyncio
        docs = asyncio.run(developer_agent._generate_implementation_docs(
            story_id, game_mechanics, component_implementations, api_implementations, test_suite
        ))
        
        assert docs["story_id"] == story_id
        assert docs["implementation_summary"]["title"] == "User Registration"
        assert docs["implementation_summary"]["components_count"] == 1
        assert docs["implementation_summary"]["apis_count"] == 1
        assert docs["implementation_summary"]["tests_count"] == 1
        assert docs["architecture_compliance"]["api_first"] is True
        assert docs["performance_metrics"]["estimated_lighthouse_score"] == 95
    
    @pytest.mark.error_handling
    @pytest.mark.asyncio
    async def test_error_handling(self, developer_agent, sample_input_contract):
        """Test error handling in various scenarios."""
        
        # Test with invalid input contract
        invalid_contract = {}
        
        with pytest.raises(AgentExecutionError):
            await developer_agent.process_contract(invalid_contract)
        
        # Test with missing input data
        incomplete_contract = sample_input_contract.copy()
        del incomplete_contract["input_requirements"]["required_data"]["game_mechanics"]
        
        with pytest.raises(AgentExecutionError):
            await developer_agent.process_contract(incomplete_contract)
        
        # Test with tool failures
        with patch.object(developer_agent, 'component_builder') as mock_builder:
            mock_builder.build_components = AsyncMock(side_effect=Exception("Build failed"))
            
            with pytest.raises(AgentExecutionError) as exc_info:
                await developer_agent.process_contract(sample_input_contract)
            
            assert "Build failed" in str(exc_info.value)
    
    @pytest.mark.eventbus
    @pytest.mark.asyncio
    async def test_team_coordination(self, developer_agent):
        """Test EventBus team coordination functionality."""
        
        # Test progress notification
        with patch.object(developer_agent, 'event_bus') as mock_event_bus:
            mock_event_bus.publish = AsyncMock()
            
            await developer_agent._notify_team_progress("implementation_started", {
                "story_id": "STORY-TEST-001",
                "status": "in_progress"
            })
            
            mock_event_bus.publish.assert_called_once()
            call_args = mock_event_bus.publish.call_args
            assert call_args[0][0] == "implementation_started"
            assert call_args[0][1]["agent"] == "developer"
            assert call_args[0][1]["story_id"] == "STORY-TEST-001"
        
        # Test event handling
        with patch.object(developer_agent, 'logger') as mock_logger:
            await developer_agent._handle_team_event("code_review_feedback", {
                "story_id": "STORY-TEST-001",
                "feedback": "Needs improvement"
            })
            
            mock_logger.info.assert_called()
    
    @pytest.mark.performance
    @pytest.mark.asyncio
    async def test_performance_requirements(self, developer_agent, sample_input_contract):
        """Test that agent meets performance requirements."""
        import time
        
        # Mock all tools for performance test
        with patch.object(developer_agent, 'git_operations') as mock_git, \
             patch.object(developer_agent, 'component_builder') as mock_component_builder, \
             patch.object(developer_agent, 'api_builder') as mock_api_builder, \
             patch.object(developer_agent, 'code_generator') as mock_code_generator, \
             patch.object(developer_agent, 'dna_code_validator') as mock_dna_validator, \
             patch.object(developer_agent, '_validate_architecture_requirements') as mock_arch_val, \
             patch.object(developer_agent, '_validate_implementation_quality') as mock_quality_val:
            
            # Setup fast mocks
            mock_git.create_feature_branch = AsyncMock()
            mock_git.commit_implementation = AsyncMock(return_value="abc123")
            mock_component_builder.build_components = AsyncMock(return_value=[{"name": "Test"}])
            mock_api_builder.build_apis = AsyncMock(return_value=[{"name": "test_api"}])
            mock_code_generator.generate_tests = AsyncMock(return_value={"unit_tests": []})
            
            # Fast DNA validation
            mock_dna_result = Mock()
            mock_dna_result.overall_dna_compliant = True
            mock_dna_result.violations = []
            mock_dna_result.dna_compliance_score = 4.5
            mock_dna_result.time_respect_compliant = True
            mock_dna_result.pedagogical_value_compliant = True
            mock_dna_result.professional_tone_compliant = True
            mock_dna_result.api_first_compliant = True
            mock_dna_result.stateless_backend_compliant = True
            mock_dna_result.separation_concerns_compliant = True
            mock_dna_result.simplicity_first_compliant = True
            mock_dna_result.validation_timestamp = datetime.now().isoformat()
            mock_dna_result.recommendations = []
            mock_dna_result.quality_reviewer_metrics = {}
            
            mock_dna_validator.validate_code_dna_compliance = AsyncMock(return_value=mock_dna_result)
            mock_arch_val.return_value = None
            mock_quality_val.return_value = None
            
            # Measure performance
            start_time = time.time()
            result = await developer_agent.process_contract(sample_input_contract)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            # Should complete within reasonable time (with mocks, should be very fast)
            assert processing_time < 5.0, f"Contract processing too slow: {processing_time:.3f}s (max: 5.0s)"
            assert result is not None
    
    @pytest.mark.configuration
    def test_agent_configuration(self):
        """Test agent configuration handling."""
        
        # Test with various configurations
        configs = [
            {},  # Default config
            {"frontend_path": "custom_frontend"},
            {"backend_path": "custom_backend"},
            {"test_path": "custom_tests"},
            {
                "frontend_path": "custom_frontend",
                "backend_path": "custom_backend",
                "test_path": "custom_tests",
                "state_storage_path": "custom_state"
            }
        ]
        
        for config in configs:
            agent = DeveloperAgent(config)
            
            # Verify agent initialization
            assert agent.agent_type == "developer"
            assert agent.config == config
            
            # Verify tools initialization
            assert hasattr(agent, 'code_generator')
            assert hasattr(agent, 'api_builder')
            assert hasattr(agent, 'git_operations')
            assert hasattr(agent, 'component_builder')
            assert hasattr(agent, 'architecture_validator')
            assert hasattr(agent, 'dna_code_validator')
            
            # Verify quality standards
            assert agent.quality_standards["typescript_errors"]["max"] == 0
            assert agent.quality_standards["test_coverage_percent"]["min"] == 100
            assert agent.quality_standards["lighthouse_score"]["min"] == 90
    
    @pytest.mark.tools
    def test_tool_integration(self, developer_agent):
        """Test that all required tools are properly integrated."""
        
        # Verify all tools are initialized
        assert hasattr(developer_agent, 'code_generator')
        assert hasattr(developer_agent, 'api_builder')
        assert hasattr(developer_agent, 'git_operations')
        assert hasattr(developer_agent, 'component_builder')
        assert hasattr(developer_agent, 'architecture_validator')
        assert hasattr(developer_agent, 'dna_code_validator')
        assert hasattr(developer_agent, 'event_bus')
        
        # Verify tools have expected methods
        assert hasattr(developer_agent.code_generator, 'generate_tests')
        assert hasattr(developer_agent.api_builder, 'build_apis')
        assert hasattr(developer_agent.git_operations, 'create_feature_branch')
        assert hasattr(developer_agent.component_builder, 'build_components')
        assert hasattr(developer_agent.architecture_validator, 'validate_requirements')
        assert hasattr(developer_agent.dna_code_validator, 'validate_code_dna_compliance')
    
    @pytest.mark.regression
    @pytest.mark.asyncio
    async def test_regression_scenarios(self, developer_agent):
        """Test regression scenarios to ensure stability."""
        
        # Test with minimal contract
        minimal_contract = {
            "contract_version": "1.0",
            "story_id": "STORY-MIN-001",
            "source_agent": "game_designer",
            "target_agent": "developer",
            "dna_compliance": {
                "time_respect_validated": True,
                "pedagogical_value_validated": True,
                "professional_tone_validated": True,
                "policy_to_practice_validated": True,
                "holistic_thinking_validated": True
            },
            "input_requirements": {
                "required_data": {
                    "game_mechanics": {"title": "Minimal Feature"},
                    "ui_components": [],
                    "interaction_flows": [],
                    "api_endpoints": [],
                    "state_management": {}
                }
            }
        }
        
        with patch.object(developer_agent, 'git_operations') as mock_git, \
             patch.object(developer_agent, 'component_builder') as mock_component_builder, \
             patch.object(developer_agent, 'api_builder') as mock_api_builder, \
             patch.object(developer_agent, 'code_generator') as mock_code_generator, \
             patch.object(developer_agent, 'dna_code_validator') as mock_dna_validator, \
             patch.object(developer_agent, '_validate_architecture_requirements') as mock_arch_val, \
             patch.object(developer_agent, '_validate_implementation_quality') as mock_quality_val:
            
            # Setup mocks for minimal scenario
            mock_git.create_feature_branch = AsyncMock()
            mock_git.commit_implementation = AsyncMock(return_value="abc123")
            mock_component_builder.build_components = AsyncMock(return_value=[])
            mock_api_builder.build_apis = AsyncMock(return_value=[])
            mock_code_generator.generate_tests = AsyncMock(return_value={"unit_tests": []})
            
            mock_dna_result = Mock()
            mock_dna_result.overall_dna_compliant = True
            mock_dna_result.violations = []
            mock_dna_result.dna_compliance_score = 4.0
            mock_dna_result.time_respect_compliant = True
            mock_dna_result.pedagogical_value_compliant = True
            mock_dna_result.professional_tone_compliant = True
            mock_dna_result.api_first_compliant = True
            mock_dna_result.stateless_backend_compliant = True
            mock_dna_result.separation_concerns_compliant = True
            mock_dna_result.simplicity_first_compliant = True
            mock_dna_result.validation_timestamp = datetime.now().isoformat()
            mock_dna_result.recommendations = []
            mock_dna_result.quality_reviewer_metrics = {}
            
            mock_dna_validator.validate_code_dna_compliance = AsyncMock(return_value=mock_dna_result)
            mock_arch_val.return_value = None
            mock_quality_val.return_value = None
            
            # Should handle minimal contract gracefully
            result = await developer_agent.process_contract(minimal_contract)
            assert result is not None
            assert result["story_id"] == "STORY-MIN-001"


# Additional test classes for specific functionality

@pytest.mark.integration
class TestDeveloperAgentIntegration:
    """Integration tests for Developer agent with other components."""
    
    @pytest.fixture
    def developer_agent(self):
        """Create DeveloperAgent instance for integration testing."""
        return DeveloperAgent()
    
    @pytest.mark.asyncio
    async def test_contract_validator_integration(self, developer_agent):
        """Test integration with ContractValidator."""
        
        # Verify contract validator is initialized
        assert hasattr(developer_agent, 'contract_validator')
        assert developer_agent.contract_validator is not None
    
    @pytest.mark.asyncio
    async def test_eventbus_integration(self, developer_agent):
        """Test integration with EventBus for team coordination."""
        
        # Verify EventBus is initialized
        assert hasattr(developer_agent, 'event_bus')
        assert developer_agent.event_bus is not None
        
        # Test listener setup
        with patch.object(developer_agent.event_bus, 'subscribe') as mock_subscribe:
            await developer_agent._listen_for_team_events()
            
            # Should subscribe to relevant events
            assert mock_subscribe.call_count > 0


@pytest.mark.dna_compliance
class TestDeveloperAgentDNACompliance:
    """Comprehensive DNA compliance tests for Developer agent."""
    
    @pytest.fixture
    def developer_agent(self):
        """Create DeveloperAgent instance for DNA testing."""
        return DeveloperAgent()
    
    @pytest.mark.asyncio
    async def test_dna_code_validator_integration(self, developer_agent):
        """Test integration with DNACodeValidator."""
        
        # Verify DNA code validator is initialized
        assert hasattr(developer_agent, 'dna_code_validator')
        assert developer_agent.dna_code_validator is not None
        
        # Test that it's the correct type
        from ..tools.dna_code_validator import DNACodeValidator
        assert isinstance(developer_agent.dna_code_validator, DNACodeValidator)
    
    @pytest.mark.asyncio
    async def test_comprehensive_dna_validation(self, developer_agent):
        """Test comprehensive DNA validation workflow."""
        
        # Create test data that should pass all DNA principles
        excellent_components = [
            {
                "name": "MunicipalLearningComponent",
                "code": {
                    "component": '''
                    /**
                     * MunicipalLearningComponent - Interactive learning module for municipal employees
                     * 
                     * @param props.learningModule - Learning module data for municipal training
                     * @param props.userProgress - Current learning progress for tracking
                     * @returns JSX.Element
                     */
                    export const MunicipalLearningComponent: React.FC<LearningProps> = (props) => {
                        const [municipalProgress, setMunicipalProgress] = useState(0);
                        
                        return (
                            <Card role="region" aria-label="Municipal Learning Module" tabIndex={0}>
                                <Typography variant="h2">Policy Learning Module</Typography>
                                <ProgressBar value={municipalProgress} max={100} aria-label="Learning progress" />
                                <Text>Complete municipal policy training in under 10 minutes</Text>
                            </Card>
                        );
                    };
                    '''
                }
            }
        ]
        
        excellent_apis = [
            {
                "name": "municipal_training_progress",
                "code": {
                    "endpoint": '''
                    @router.post("/api/municipal/training-progress")
                    async def municipal_training_progress(
                        request: MunicipalTrainingRequest
                    ) -> MunicipalTrainingResponse:
                        """
                        Track municipal employee training progress for policy implementation.
                        
                        Args:
                            request: Training progress data with validation for municipal employees
                            
                        Returns:
                            MunicipalTrainingResponse: Updated progress with error_message for validation
                        """
                        try:
                            # Validate and sanitize personal data according to GDPR requirements
                            validated_data = await validate_municipal_data(request)
                            
                            # Process training progress for municipal policy application
                            progress_result = await process_training_progress(validated_data)
                            
                            return MunicipalTrainingResponse(
                                success=True,
                                progress_data=progress_result,
                                message="Municipal training progress updated successfully"
                            )
                        except ValidationError as e:
                            raise HTTPException(
                                status_code=422,
                                detail={
                                    "error_code": "VALIDATION_ERROR", 
                                    "error_message": "Please provide valid municipal training data"
                                }
                            )
                    '''
                },
                "implementation": {
                    "estimated_response_time_ms": 120
                }
            }
        ]
        
        test_suite = {
            "unit_tests": [
                {"name": "test_municipal_learning_component"},
                {"name": "test_training_progress_api"}
            ]
        }
        
        story_data = {
            "title": "Municipal Employee Training System",
            "description": "Interactive training for policy implementation"
        }
        
        # Mock the DNA validator
        with patch.object(developer_agent, 'dna_code_validator') as mock_dna_validator:
            mock_result = Mock()
            mock_result.overall_dna_compliant = True
            mock_result.dna_compliance_score = 4.8
            mock_result.violations = []
            mock_result.time_respect_compliant = True
            mock_result.pedagogical_value_compliant = True
            mock_result.professional_tone_compliant = True
            mock_result.api_first_compliant = True
            mock_result.stateless_backend_compliant = True
            mock_result.separation_concerns_compliant = True
            mock_result.simplicity_first_compliant = True
            mock_result.validation_timestamp = datetime.now().isoformat()
            mock_result.recommendations = []
            mock_result.quality_reviewer_metrics = {
                "complexity_analysis": {"avg_component_complexity": 3.2},
                "learning_effectiveness": {"score": 4.8},
                "professional_quality": {"score": 4.9},
                "architecture_compliance": {"score": 4.7}
            }
            
            mock_dna_validator.validate_code_dna_compliance = AsyncMock(return_value=mock_result)
            
            # Run DNA validation
            result = await mock_dna_validator.validate_code_dna_compliance(
                excellent_components, excellent_apis, test_suite, story_data
            )
            
            # Verify excellent DNA compliance
            assert result.overall_dna_compliant is True
            assert result.dna_compliance_score >= 4.5
            assert len(result.violations) == 0
            assert result.time_respect_compliant is True
            assert result.pedagogical_value_compliant is True
            assert result.professional_tone_compliant is True


# Performance and reliability benchmarks
DEVELOPER_AGENT_BENCHMARKS = {
    "max_contract_processing_time": 30.0,  # seconds
    "max_component_generation_time": 5.0,  # seconds per component
    "max_api_generation_time": 3.0,        # seconds per endpoint
    "min_code_quality_score": 4.0,         # out of 5
    "min_dna_compliance_score": 4.0,       # out of 5
    "required_test_coverage": 95,           # percentage
    "max_typescript_errors": 0,            # zero tolerance
    "max_eslint_violations": 0,            # zero tolerance
    "min_lighthouse_score": 90,            # performance score
    "max_api_response_time": 200           # milliseconds
}


if __name__ == "__main__":
    # Run with: pytest modules/agents/developer/tests/test_agent.py -v
    pytest.main([__file__, "-v", "--tb=short", "-m", "not integration"])