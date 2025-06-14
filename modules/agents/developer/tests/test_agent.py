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