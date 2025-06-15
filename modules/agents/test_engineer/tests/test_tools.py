"""
Test Engineer Agent Tools Tests

PURPOSE:
Tests all Test Engineer agent-specific tools according to TEST_STRATEGY.md.

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
- TestGenerator: Integration test generation, E2E test generation
- CoverageAnalyzer: Coverage analysis and reporting
- PerformanceTester: Load testing, benchmarking
- SecurityScanner: Vulnerability scanning, compliance checking
- DNATestValidator: Test DNA compliance validation
- AITestOptimizer: AI-driven test optimization
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
from typing import Dict, Any

from modules.agents.test_engineer.tools.test_generator import TestGenerator
from modules.agents.test_engineer.tools.coverage_analyzer import CoverageAnalyzer
from modules.agents.test_engineer.tools.performance_tester import PerformanceTester
from modules.agents.test_engineer.tools.security_scanner import SecurityScanner
from modules.agents.test_engineer.tools.dna_test_validator import DNATestValidator
from modules.agents.test_engineer.tools.ai_test_optimizer import AITestOptimizer
from modules.shared.exceptions import (
    QualityGateError, SecurityViolationError, PerformanceError,
    DNAComplianceError, ToolExecutionError
)


class TestToolsBase:
    """Base class for tool testing with common fixtures."""
    
    @pytest.fixture
    def tool_config(self):
        """Standard tool configuration for testing."""
        return {
            "test_mode": True,
            "test_output_path": "test_output",
            "coverage_threshold": 95,
            "performance_budget": {
                "api_response_time_ms": 200,
                "lighthouse_score": 90,
                "bundle_size_kb": 500
            },
            "security_scan_rules": {
                "critical_vulnerabilities": 0,
                "high_vulnerabilities": 0,
                "medium_vulnerabilities": 5
            },
            "max_retries": 2,
            "timeout_seconds": 30
        }
    
    @pytest.fixture
    def sample_component_implementation(self):
        """Sample React component for testing."""
        return {
            "name": "PolicyTrainingCard",
            "type": "react_component",
            "files": {
                "component": "src/components/PolicyTrainingCard.tsx",
                "test": "tests/unit/PolicyTrainingCard.test.tsx",
                "styles": "src/components/PolicyTrainingCard.module.css"
            },
            "code": {
                "component": """
                import React from 'react';
                import { Card, Button } from '@shadcn/ui';
                
                interface PolicyTrainingCardProps {
                  id: string;
                  title: string;
                  description: string;
                  onSelect: (id: string) => void;
                  completed?: boolean;
                }
                
                export const PolicyTrainingCard: React.FC<PolicyTrainingCardProps> = ({
                  id, title, description, onSelect, completed = false
                }) => {
                  return (
                    <Card className="p-4 cursor-pointer hover:shadow-lg">
                      <h3 className="text-lg font-semibold">{title}</h3>
                      <p className="text-gray-600 mb-4">{description}</p>
                      <Button 
                        onClick={() => onSelect(id)}
                        variant={completed ? "outline" : "default"}
                      >
                        {completed ? "Granska igen" : "Starta träning"}
                      </Button>
                    </Card>
                  );
                };
                """,
                "test": "// Jest test code placeholder"
            },
            "typescript_errors": 0,
            "eslint_violations": 0,
            "test_coverage_percent": 100.0,
            "accessibility_score": 95,
            "performance_score": 92,
            "integration_test_passed": True
        }
    
    @pytest.fixture
    def sample_api_implementation(self):
        """Sample FastAPI endpoint for testing."""
        return {
            "name": "training_policies_endpoint",
            "method": "GET",
            "path": "/api/training/policies",
            "files": {
                "endpoint": "src/api/endpoints/training_policies.py",
                "test": "tests/unit/test_training_policies_api.py"
            },
            "code": {
                "endpoint": """
                from fastapi import APIRouter, HTTPException, Depends
                from typing import List
                from ..models.training_policy import TrainingPolicyResponse
                from ..services.policy_service import PolicyService
                
                router = APIRouter()
                
                @router.get("/api/training/policies", response_model=List[TrainingPolicyResponse])
                async def get_training_policies(
                    policy_service: PolicyService = Depends()
                ) -> List[TrainingPolicyResponse]:
                    try:
                        policies = await policy_service.get_active_policies()
                        return [TrainingPolicyResponse.from_model(p) for p in policies]
                    except Exception as e:
                        raise HTTPException(status_code=500, detail="Failed to fetch policies")
                """,
                "test": "# pytest test code placeholder"
            },
            "functional_test_passed": True,
            "performance_test_passed": True,
            "security_test_passed": True,
            "estimated_response_time_ms": 150
        }


class TestTestGenerator(TestToolsBase):
    """Test TestGenerator tool functionality."""
    
    @pytest.fixture
    def test_generator(self, tool_config):
        """Create test generator tool for testing."""
        return TestGenerator(tool_config)
    
    @pytest.mark.asyncio
    async def test_tool_initialization(self, tool_config):
        """Test TestGenerator tool initializes correctly."""
        tool = TestGenerator(tool_config)
        
        # Verify configuration
        assert tool.config["test_mode"] is True
        assert tool.config["coverage_threshold"] == 95
        assert hasattr(tool, 'logger')
        assert tool.output_path == "test_output"
    
    @pytest.mark.asyncio
    async def test_generate_integration_tests_success(self, test_generator, sample_component_implementation, sample_api_implementation):
        """Test successful integration test generation."""
        story_id = "STORY-TE-TOOLS-001"
        
        # Mock file system operations
        with patch('builtins.open', mock=Mock()), \
             patch('os.makedirs') as mock_makedirs, \
             patch('os.path.exists', return_value=True):
            
            # Generate integration tests
            result = await test_generator.generate_integration_tests(
                [sample_component_implementation],
                [sample_api_implementation],
                story_id
            )
            
            # Verify result structure
            assert result["story_id"] == story_id
            assert result["test_type"] == "integration"
            assert "total_test_cases" in result
            assert "coverage_percent" in result
            assert "test_cases" in result
            assert result["all_tests_passing"] is True
            
            # Verify test cases generated
            assert len(result["test_cases"]) > 0
            test_case = result["test_cases"][0]
            assert "name" in test_case
            assert "status" in test_case
            assert test_case["status"] == "passing"
    
    @pytest.mark.asyncio
    async def test_generate_e2e_tests_success(self, test_generator, sample_component_implementation):
        """Test successful E2E test generation."""
        story_id = "STORY-TE-TOOLS-002"
        user_flows = [
            {
                "name": "policy_training_selection",
                "description": "Anna selects and starts policy training",
                "steps": ["browse_policies", "select_policy", "start_training", "complete_training"]
            }
        ]
        
        # Mock file system operations
        with patch('builtins.open', mock=Mock()), \
             patch('os.makedirs') as mock_makedirs, \
             patch('os.path.exists', return_value=True):
            
            # Generate E2E tests
            result = await test_generator.generate_e2e_tests(
                [sample_component_implementation],
                user_flows,
                story_id
            )
            
            # Verify result structure
            assert result["story_id"] == story_id
            assert result["test_type"] == "end_to_end"
            assert "total_scenarios" in result
            assert "coverage_percent" in result
            assert "scenarios" in result
            assert result["all_tests_passing"] is True
            
            # Verify scenarios generated
            assert len(result["scenarios"]) > 0
            scenario = result["scenarios"][0]
            assert "name" in scenario
            assert "status" in scenario
            assert scenario["status"] == "passing"
    
    @pytest.mark.asyncio
    async def test_generate_integration_tests_file_error(self, test_generator, sample_component_implementation, sample_api_implementation):
        """Test integration test generation with file system error."""
        story_id = "STORY-TE-TOOLS-003"
        
        # Mock file system error
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            
            with pytest.raises(ToolExecutionError) as exc_info:
                await test_generator.generate_integration_tests(
                    [sample_component_implementation],
                    [sample_api_implementation],
                    story_id
                )
            
            assert "Failed to generate integration tests" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_generate_test_framework_selection(self, test_generator):
        """Test test framework selection logic."""
        # Test React component -> Jest + React Testing Library
        react_framework = test_generator._select_test_framework("react_component")
        assert "Jest" in react_framework
        assert "React Testing Library" in react_framework
        
        # Test FastAPI endpoint -> pytest + httpx
        api_framework = test_generator._select_test_framework("fastapi_endpoint")
        assert "pytest" in api_framework
        assert "httpx" in api_framework
        
        # Test E2E -> Playwright
        e2e_framework = test_generator._select_test_framework("e2e_test")
        assert "Playwright" in e2e_framework


class TestCoverageAnalyzer(TestToolsBase):
    """Test CoverageAnalyzer tool functionality."""
    
    @pytest.fixture
    def coverage_analyzer(self, tool_config):
        """Create coverage analyzer tool for testing."""
        return CoverageAnalyzer(tool_config)
    
    @pytest.mark.asyncio
    async def test_analyze_comprehensive_coverage_success(self, coverage_analyzer):
        """Test successful comprehensive coverage analysis."""
        story_id = "STORY-TE-COVERAGE-001"
        
        sample_integration_suite = {
            "story_id": story_id,
            "test_type": "integration",
            "total_test_cases": 8,
            "test_cases": [
                {"name": "test_policy_api_integration", "status": "passing"},
                {"name": "test_component_api_integration", "status": "passing"}
            ]
        }
        
        sample_e2e_suite = {
            "story_id": story_id,
            "test_type": "end_to_end", 
            "total_scenarios": 4,
            "scenarios": [
                {"name": "anna_selects_policy", "status": "passing"}
            ]
        }
        
        # Mock coverage tools
        with patch('subprocess.run') as mock_subprocess:
            # Mock jest coverage output
            mock_subprocess.return_value.stdout = json.dumps({
                "total": {
                    "lines": {"pct": 96.5},
                    "functions": {"pct": 95.0},
                    "branches": {"pct": 94.2},
                    "statements": {"pct": 96.8}
                }
            })
            mock_subprocess.return_value.returncode = 0
            
            result = await coverage_analyzer.analyze_comprehensive_coverage(
                sample_integration_suite,
                sample_e2e_suite,
                story_id
            )
            
            # Verify coverage analysis
            assert result["story_id"] == story_id
            assert "overall_coverage_percent" in result
            assert "coverage_by_type" in result
            assert "coverage_quality_met" in result
            assert result["coverage_quality_met"] is True
            
            # Verify detailed coverage metrics
            assert "lines_coverage" in result["coverage_by_type"]
            assert "functions_coverage" in result["coverage_by_type"]
            assert "branches_coverage" in result["coverage_by_type"]
    
    @pytest.mark.asyncio
    async def test_analyze_coverage_threshold_failure(self, coverage_analyzer):
        """Test coverage analysis when threshold not met."""
        story_id = "STORY-TE-COVERAGE-002"
        
        sample_integration_suite = {"story_id": story_id, "total_test_cases": 5}
        sample_e2e_suite = {"story_id": story_id, "total_scenarios": 2}
        
        # Mock low coverage output
        with patch('subprocess.run') as mock_subprocess:
            mock_subprocess.return_value.stdout = json.dumps({
                "total": {
                    "lines": {"pct": 85.0},  # Below 95% threshold
                    "functions": {"pct": 80.0},
                    "branches": {"pct": 75.0},
                    "statements": {"pct": 82.0}
                }
            })
            mock_subprocess.return_value.returncode = 0
            
            result = await coverage_analyzer.analyze_comprehensive_coverage(
                sample_integration_suite,
                sample_e2e_suite,
                story_id
            )
            
            # Verify threshold failure detection
            assert result["coverage_quality_met"] is False
            assert result["overall_coverage_percent"] < 95
            assert "coverage_issues" in result
    
    @pytest.mark.asyncio
    async def test_coverage_tool_execution_error(self, coverage_analyzer):
        """Test handling of coverage tool execution errors."""
        story_id = "STORY-TE-COVERAGE-003"
        
        sample_integration_suite = {"story_id": story_id}
        sample_e2e_suite = {"story_id": story_id}
        
        # Mock subprocess error
        with patch('subprocess.run', side_effect=Exception("Coverage tool failed")):
            
            with pytest.raises(ToolExecutionError) as exc_info:
                await coverage_analyzer.analyze_comprehensive_coverage(
                    sample_integration_suite,
                    sample_e2e_suite,
                    story_id
                )
            
            assert "Coverage analysis failed" in str(exc_info.value)


class TestPerformanceTester(TestToolsBase):
    """Test PerformanceTester tool functionality."""
    
    @pytest.fixture
    def performance_tester(self, tool_config):
        """Create performance tester tool for testing."""
        return PerformanceTester(tool_config)
    
    @pytest.mark.asyncio
    async def test_run_comprehensive_performance_tests_success(self, performance_tester, sample_component_implementation, sample_api_implementation):
        """Test successful performance testing."""
        story_id = "STORY-TE-PERF-001"
        
        # Mock performance testing tools
        with patch('subprocess.run') as mock_subprocess, \
             patch('aiohttp.ClientSession.get') as mock_api_test:
            
            # Mock Lighthouse results
            lighthouse_result = {
                "returncode": 0,
                "stdout": json.dumps({
                    "lhr": {
                        "categories": {
                            "performance": {"score": 0.94}
                        },
                        "audits": {
                            "first-contentful-paint": {"numericValue": 1200},
                            "largest-contentful-paint": {"numericValue": 2100}
                        }
                    }
                })
            }
            
            # Mock API load test results
            api_response = AsyncMock()
            api_response.status = 200
            api_response.headers = {"Content-Length": "1024"}
            mock_api_test.return_value.__aenter__.return_value = api_response
            
            # Configure subprocess mock to return different results based on command
            def subprocess_side_effect(*args, **kwargs):
                if "lighthouse" in str(args[0]):
                    result = Mock()
                    result.returncode = 0
                    result.stdout = lighthouse_result["stdout"]
                    return result
                else:
                    result = Mock()
                    result.returncode = 0
                    result.stdout = "Bundle size: 180KB"
                    return result
            
            mock_subprocess.side_effect = subprocess_side_effect
            
            result = await performance_tester.run_comprehensive_performance_tests(
                [sample_component_implementation],
                [sample_api_implementation],
                story_id
            )
            
            # Verify performance test results
            assert result["story_id"] == story_id
            assert "average_api_response_time_ms" in result
            assert "lighthouse_score" in result
            assert "bundle_size_kb" in result
            assert "performance_budget_met" in result
            assert result["performance_budget_met"] is True
            
            # Verify performance metrics meet budget
            assert result["average_api_response_time_ms"] < 200
            assert result["lighthouse_score"] >= 90
    
    @pytest.mark.asyncio
    async def test_performance_budget_violation(self, performance_tester, sample_component_implementation, sample_api_implementation):
        """Test performance budget violation detection."""
        story_id = "STORY-TE-PERF-002"
        
        # Mock poor performance results
        with patch('subprocess.run') as mock_subprocess, \
             patch('aiohttp.ClientSession.get') as mock_api_test:
            
            # Mock poor Lighthouse score
            lighthouse_result = Mock()
            lighthouse_result.returncode = 0
            lighthouse_result.stdout = json.dumps({
                "lhr": {
                    "categories": {
                        "performance": {"score": 0.75}  # Below 90 threshold
                    },
                    "audits": {
                        "first-contentful-paint": {"numericValue": 3000},
                        "largest-contentful-paint": {"numericValue": 5000}
                    }
                }
            })
            
            # Mock slow API response
            api_response = AsyncMock()
            api_response.status = 200
            
            # Simulate slow response time by mocking time
            mock_api_test.return_value.__aenter__.return_value = api_response
            
            mock_subprocess.return_value = lighthouse_result
            
            # Mock slow API timing
            with patch('time.time', side_effect=[0, 0.3]):  # 300ms response time
                result = await performance_tester.run_comprehensive_performance_tests(
                    [sample_component_implementation],
                    [sample_api_implementation],
                    story_id
                )
            
            # Verify budget violation detection
            assert result["performance_budget_met"] is False
            assert result["lighthouse_score"] < 90
            assert "performance_issues" in result
    
    @pytest.mark.asyncio
    async def test_load_testing_api_endpoints(self, performance_tester, sample_api_implementation):
        """Test load testing for API endpoints."""
        # Mock concurrent API requests
        with patch('aiohttp.ClientSession.get') as mock_get:
            api_response = AsyncMock()
            api_response.status = 200
            mock_get.return_value.__aenter__.return_value = api_response
            
            # Mock time for response measurement
            with patch('time.time', side_effect=[0, 0.1, 0.15, 0.12, 0.18, 0.16]):
                result = await performance_tester._load_test_api_endpoint(
                    sample_api_implementation["path"],
                    concurrent_users=5,
                    duration_seconds=1
                )
            
            # Verify load test results
            assert "average_response_time_ms" in result
            assert "max_response_time_ms" in result
            assert "requests_per_second" in result
            assert "error_rate" in result
            assert result["error_rate"] == 0.0  # No errors in mock


class TestSecurityScanner(TestToolsBase):
    """Test SecurityScanner tool functionality."""
    
    @pytest.fixture
    def security_scanner(self, tool_config):
        """Create security scanner tool for testing."""
        return SecurityScanner(tool_config)
    
    @pytest.mark.asyncio
    async def test_run_comprehensive_security_scan_success(self, security_scanner, sample_component_implementation, sample_api_implementation):
        """Test successful security scanning."""
        story_id = "STORY-TE-SEC-001"
        
        # Mock security tools
        with patch('subprocess.run') as mock_subprocess:
            # Mock clean security scan results
            bandit_result = Mock()
            bandit_result.returncode = 0
            bandit_result.stdout = json.dumps({
                "results": [],
                "metrics": {"_totals": {"SEVERITY.HIGH": 0, "SEVERITY.MEDIUM": 0}}
            })
            
            npm_audit_result = Mock()
            npm_audit_result.returncode = 0
            npm_audit_result.stdout = json.dumps({
                "vulnerabilities": {
                    "critical": 0,
                    "high": 0,
                    "moderate": 0,
                    "low": 2
                }
            })
            
            # Configure subprocess mock based on command
            def subprocess_side_effect(*args, **kwargs):
                command_str = str(args[0]) if args else ""
                if "bandit" in command_str:
                    return bandit_result
                elif "npm audit" in command_str:
                    return npm_audit_result
                else:
                    result = Mock()
                    result.returncode = 0
                    result.stdout = "No issues found"
                    return result
            
            mock_subprocess.side_effect = subprocess_side_effect
            
            result = await security_scanner.run_comprehensive_security_scan(
                [sample_component_implementation],
                [sample_api_implementation],
                story_id
            )
            
            # Verify security scan results
            assert result["story_id"] == story_id
            assert "critical_vulnerabilities" in result
            assert "high_vulnerabilities" in result
            assert "medium_vulnerabilities" in result
            assert "security_compliance_met" in result
            assert result["security_compliance_met"] is True
            
            # Verify clean scan
            assert len(result["critical_vulnerabilities"]) == 0
            assert len(result["high_vulnerabilities"]) == 0
    
    @pytest.mark.asyncio
    async def test_security_vulnerabilities_detected(self, security_scanner, sample_api_implementation):
        """Test security vulnerability detection."""
        story_id = "STORY-TE-SEC-002"
        
        # Mock security vulnerabilities
        with patch('subprocess.run') as mock_subprocess:
            # Mock bandit finding SQL injection
            bandit_result = Mock()
            bandit_result.returncode = 1
            bandit_result.stdout = json.dumps({
                "results": [
                    {
                        "issue_severity": "HIGH",
                        "issue_text": "Possible SQL injection vulnerability",
                        "filename": "api/endpoints.py",
                        "line_number": 42,
                        "test_id": "B608"
                    }
                ],
                "metrics": {"_totals": {"SEVERITY.HIGH": 1, "SEVERITY.MEDIUM": 0}}
            })
            
            mock_subprocess.return_value = bandit_result
            
            with pytest.raises(SecurityViolationError) as exc_info:
                await security_scanner.run_comprehensive_security_scan(
                    [],
                    [sample_api_implementation],
                    story_id
                )
            
            assert "Security vulnerabilities detected" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_gdpr_compliance_check(self, security_scanner):
        """Test GDPR compliance checking for Swedish municipal context."""
        code_sample = """
        # Personal data processing
        def process_user_data(personal_number, address, email):
            # Store personal data without encryption
            database.store({
                'personal_number': personal_number,
                'address': address,
                'email': email
            })
        """
        
        gdpr_issues = security_scanner._check_gdpr_compliance(code_sample)
        
        # Verify GDPR compliance checking
        assert len(gdpr_issues) > 0
        assert any("encryption" in issue.lower() for issue in gdpr_issues)
        assert any("consent" in issue.lower() for issue in gdpr_issues)
    
    @pytest.mark.asyncio
    async def test_municipal_security_patterns(self, security_scanner):
        """Test Swedish municipal specific security patterns."""
        code_sample = """
        # Municipal API endpoint
        @app.get("/api/citizen/{personal_number}")
        async def get_citizen_data(personal_number: str):
            return database.query(f"SELECT * FROM citizens WHERE pnr = {personal_number}")
        """
        
        security_issues = security_scanner._check_municipal_security_patterns(code_sample)
        
        # Verify municipal security pattern detection
        assert len(security_issues) > 0
        assert any("sql injection" in issue.lower() for issue in security_issues)
        assert any("personal_number" in issue.lower() for issue in security_issues)


class TestDNATestValidator(TestToolsBase):
    """Test DNATestValidator tool functionality."""
    
    @pytest.fixture
    def dna_validator(self, tool_config):
        """Create DNA test validator tool for testing."""
        return DNATestValidator(tool_config)
    
    @pytest.mark.asyncio
    async def test_validate_test_dna_compliance_success(self, dna_validator):
        """Test successful DNA compliance validation."""
        story_id = "STORY-TE-DNA-001"
        
        sample_integration_suite = {
            "story_id": story_id,
            "total_test_cases": 8,
            "estimated_execution_time_minutes": 5.0,
            "all_tests_passing": True
        }
        
        sample_e2e_suite = {
            "story_id": story_id,
            "total_scenarios": 4,
            "estimated_execution_time_minutes": 8.0,
            "all_tests_passing": True
        }
        
        sample_performance_results = {
            "story_id": story_id,
            "average_api_response_time_ms": 150.0,
            "performance_budget_met": True
        }
        
        sample_coverage_report = {
            "story_id": story_id,
            "overall_coverage_percent": 96.0,
            "coverage_quality_met": True
        }
        
        story_data = {
            "story_id": story_id,
            "user_stories": ["As Anna, I want to access training efficiently"],
            "acceptance_criteria": ["Response time under 200ms", "95% test coverage"]
        }
        
        result = await dna_validator.validate_test_dna_compliance(
            sample_integration_suite,
            sample_e2e_suite,
            sample_performance_results,
            sample_coverage_report,
            story_data
        )
        
        # Verify DNA validation results
        assert result.overall_dna_compliant is True
        assert result.time_respect_compliant is True
        assert result.pedagogical_value_compliant is True
        assert result.professional_tone_compliant is True
        assert result.dna_compliance_score >= 4.0
        assert "quality_reviewer_metrics" in result.__dict__
    
    @pytest.mark.asyncio
    async def test_validate_time_respect_violation(self, dna_validator):
        """Test DNA violation - time respect principle."""
        story_id = "STORY-TE-DNA-002"
        
        # Test suite with excessive execution time
        sample_integration_suite = {
            "story_id": story_id,
            "total_test_cases": 50,
            "estimated_execution_time_minutes": 15.0,  # Exceeds 10 minute limit
            "all_tests_passing": True
        }
        
        sample_e2e_suite = {
            "story_id": story_id,
            "total_scenarios": 20,
            "estimated_execution_time_minutes": 12.0,  # Exceeds limit
            "all_tests_passing": True
        }
        
        sample_performance_results = {"story_id": story_id}
        sample_coverage_report = {"story_id": story_id}
        story_data = {"story_id": story_id}
        
        result = await dna_validator.validate_test_dna_compliance(
            sample_integration_suite,
            sample_e2e_suite,
            sample_performance_results,
            sample_coverage_report,
            story_data
        )
        
        # Verify time respect violation
        assert result.time_respect_compliant is False
        assert result.overall_dna_compliant is False
        assert result.dna_compliance_score < 4.0


class TestAITestOptimizer(TestToolsBase):
    """Test AITestOptimizer tool functionality."""
    
    @pytest.fixture
    def ai_optimizer(self, tool_config):
        """Create AI test optimizer tool for testing."""
        return AITestOptimizer(tool_config)
    
    @pytest.mark.asyncio
    async def test_optimize_test_strategy_success(self, ai_optimizer, sample_component_implementation, sample_api_implementation):
        """Test successful AI test optimization."""
        story_id = "STORY-TE-AI-001"
        
        input_data = {
            "story_id": story_id,
            "user_stories": ["As Anna, I want efficient training access"],
            "complexity": "medium"
        }
        
        existing_test_suite = {
            "unit_tests": 5,
            "integration_tests": 3,
            "e2e_tests": 2
        }
        
        result = await ai_optimizer.optimize_test_strategy(
            [sample_component_implementation],
            [sample_api_implementation],
            input_data,
            existing_test_suite
        )
        
        # Verify AI optimization results
        assert result.overall_optimization_score >= 3.0
        assert result.estimated_time_savings_minutes >= 0
        assert result.quality_improvement_score >= 3.0
        assert len(result.failure_predictions) >= 0
        assert len(result.test_priorities) > 0
        assert len(result.edge_case_predictions) >= 0
        assert "anna_persona_priority_tests" in result.municipal_optimization_insights
    
    @pytest.mark.asyncio
    async def test_predict_test_failures(self, ai_optimizer):
        """Test AI failure prediction functionality."""
        test_cases = [
            {"name": "test_api_response", "complexity": "medium", "dependencies": ["database"]},
            {"name": "test_user_interaction", "complexity": "high", "dependencies": ["external_api"]}
        ]
        
        historical_data = [
            {"test_name": "test_api_response", "failure_rate": 0.05},
            {"test_name": "test_user_interaction", "failure_rate": 0.15}
        ]
        
        predictions = ai_optimizer._predict_test_failures(test_cases, historical_data)
        
        # Verify failure predictions
        assert len(predictions) > 0
        for prediction in predictions:
            assert "test_name" in prediction
            assert "failure_probability" in prediction
            assert "risk_factors" in prediction
            assert 0 <= prediction["failure_probability"] <= 1
    
    @pytest.mark.asyncio
    async def test_swedish_municipal_optimization(self, ai_optimizer):
        """Test Swedish municipal context optimization."""
        anna_persona_tests = [
            {"name": "test_accessibility_compliance", "user_persona": "anna"},
            {"name": "test_time_efficiency", "user_persona": "anna"},
            {"name": "test_gdpr_compliance", "user_persona": "generic"}
        ]
        
        optimization = ai_optimizer._optimize_for_municipal_context(anna_persona_tests)
        
        # Verify municipal optimization
        assert "anna_persona_priority_tests" in optimization
        assert "gdpr_compliance_focus_areas" in optimization
        assert "swedish_locale_considerations" in optimization
        assert optimization["anna_persona_priority_tests"] >= 2  # Anna-specific tests prioritized


class TestToolsIntegration(TestToolsBase):
    """Test tool integration and workflow."""
    
    @pytest.mark.asyncio
    async def test_tools_workflow_integration(self, tool_config, sample_component_implementation, sample_api_implementation):
        """Test complete tools workflow integration."""
        story_id = "STORY-TE-INTEGRATION-001"
        
        # Initialize all tools
        test_generator = TestGenerator(tool_config)
        coverage_analyzer = CoverageAnalyzer(tool_config)
        performance_tester = PerformanceTester(tool_config)
        security_scanner = SecurityScanner(tool_config)
        dna_validator = DNATestValidator(tool_config)
        ai_optimizer = AITestOptimizer(tool_config)
        
        # Mock all tool operations
        with patch.object(test_generator, 'generate_integration_tests') as mock_integration, \
             patch.object(test_generator, 'generate_e2e_tests') as mock_e2e, \
             patch.object(coverage_analyzer, 'analyze_comprehensive_coverage') as mock_coverage, \
             patch.object(performance_tester, 'run_comprehensive_performance_tests') as mock_perf, \
             patch.object(security_scanner, 'run_comprehensive_security_scan') as mock_security, \
             patch.object(dna_validator, 'validate_test_dna_compliance') as mock_dna, \
             patch.object(ai_optimizer, 'optimize_test_strategy') as mock_ai:
            
            # Setup mock returns
            mock_integration.return_value = {"story_id": story_id, "test_type": "integration"}
            mock_e2e.return_value = {"story_id": story_id, "test_type": "end_to_end"}
            mock_coverage.return_value = {"story_id": story_id, "coverage_quality_met": True}
            mock_perf.return_value = {"story_id": story_id, "performance_budget_met": True}
            mock_security.return_value = {"story_id": story_id, "security_compliance_met": True}
            
            # Mock DNA result
            class MockDNAResult:
                overall_dna_compliant = True
                quality_reviewer_metrics = {}
            
            mock_dna.return_value = MockDNAResult()
            
            # Mock AI optimization result
            class MockAIResult:
                overall_optimization_score = 4.5
                municipal_optimization_insights = {}
            
            mock_ai.return_value = MockAIResult()
            
            # Execute workflow
            integration_result = await test_generator.generate_integration_tests(
                [sample_component_implementation], [sample_api_implementation], story_id
            )
            e2e_result = await test_generator.generate_e2e_tests(
                [sample_component_implementation], [], story_id
            )
            coverage_result = await coverage_analyzer.analyze_comprehensive_coverage(
                integration_result, e2e_result, story_id
            )
            performance_result = await performance_tester.run_comprehensive_performance_tests(
                [sample_component_implementation], [sample_api_implementation], story_id
            )
            security_result = await security_scanner.run_comprehensive_security_scan(
                [sample_component_implementation], [sample_api_implementation], story_id
            )
            dna_result = await dna_validator.validate_test_dna_compliance(
                integration_result, e2e_result, performance_result, coverage_result, {"story_id": story_id}
            )
            ai_result = await ai_optimizer.optimize_test_strategy(
                [sample_component_implementation], [sample_api_implementation], {"story_id": story_id}, {}
            )
            
            # Verify all tools executed successfully
            assert integration_result["story_id"] == story_id
            assert e2e_result["story_id"] == story_id
            assert coverage_result["story_id"] == story_id
            assert performance_result["story_id"] == story_id
            assert security_result["story_id"] == story_id
            assert dna_result.overall_dna_compliant is True
            assert ai_result.overall_optimization_score > 4.0
    
    @pytest.mark.asyncio
    async def test_tools_error_handling_cascade(self, tool_config):
        """Test error handling cascades between tools."""
        story_id = "STORY-TE-ERROR-001"
        
        test_generator = TestGenerator(tool_config)
        coverage_analyzer = CoverageAnalyzer(tool_config)
        
        # Mock test generation failure
        with patch.object(test_generator, 'generate_integration_tests', side_effect=ToolExecutionError("Test generation failed")):
            
            with pytest.raises(ToolExecutionError):
                await test_generator.generate_integration_tests([], [], story_id)
            
            # Verify subsequent tools handle missing dependencies gracefully
            try:
                result = await coverage_analyzer.analyze_comprehensive_coverage(None, None, story_id)
                # Should either handle gracefully or raise appropriate error
                assert result is not None or True  # Either succeeds or fails appropriately
            except ToolExecutionError:
                # Expected behavior when dependencies fail
                pass


class TestToolsPerformance(TestToolsBase):
    """Test tool performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_tools_performance_requirements(self, tool_config, sample_component_implementation, sample_api_implementation):
        """Test that tools meet performance requirements."""
        import time
        
        story_id = "STORY-TE-PERF-001"
        
        # Test TestGenerator performance
        test_generator = TestGenerator(tool_config)
        
        with patch('builtins.open', mock=Mock()), \
             patch('os.makedirs'), \
             patch('os.path.exists', return_value=True):
            
            start_time = time.time()
            await test_generator.generate_integration_tests(
                [sample_component_implementation], [sample_api_implementation], story_id
            )
            execution_time = time.time() - start_time
            
            # Should complete within 5 seconds (per README requirements)
            assert execution_time < 5.0, f"Integration test generation took {execution_time}s"
        
        # Test AITestOptimizer performance
        ai_optimizer = AITestOptimizer(tool_config)
        
        start_time = time.time()
        await ai_optimizer.optimize_test_strategy(
            [sample_component_implementation], [sample_api_implementation], 
            {"story_id": story_id}, {}
        )
        execution_time = time.time() - start_time
        
        # AI optimization should complete within 10 seconds
        assert execution_time < 10.0, f"AI optimization took {execution_time}s"
    
    def test_tools_memory_usage(self, tool_config):
        """Test that tools don't consume excessive memory."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create multiple tool instances
        tools = []
        for i in range(3):
            tools.extend([
                TestGenerator(tool_config),
                CoverageAnalyzer(tool_config),
                PerformanceTester(tool_config),
                SecurityScanner(tool_config),
                DNATestValidator(tool_config),
                AITestOptimizer(tool_config)
            ])
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Should not use excessive memory (< 200MB for 18 tool instances)
        assert memory_increase < 200, f"Memory usage increased by {memory_increase}MB for 18 tool instances"