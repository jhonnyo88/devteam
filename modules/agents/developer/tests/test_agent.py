"""
Comprehensive tests for DeveloperAgent.

PURPOSE:
Test suite ensuring the Developer agent meets all requirements:
- Contract processing and validation
- Code generation quality and standards
- Architecture principle compliance
- Performance and quality metrics
- Error handling and recovery
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


class TestDeveloperAgent:
    """
    Comprehensive test suite for DeveloperAgent.
    
    COVERAGE AREAS:
    - Contract processing and validation
    - Code generation (React + FastAPI)
    - Quality gates and compliance
    - Git operations and branch management
    - Error handling and recovery
    - Performance requirements
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