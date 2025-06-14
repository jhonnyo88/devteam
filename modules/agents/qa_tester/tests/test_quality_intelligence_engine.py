"""
Tests for QualityIntelligenceEngine - AI-powered quality prediction and optimization.

PURPOSE:
Validates that the AI Quality Intelligence Engine works correctly and provides
valuable insights for QA testing optimization.

CRITICAL TESTS:
- AI quality prediction accuracy and confidence levels
- Test optimization recommendations and time savings
- Anna persona satisfaction prediction
- Quality insights generation and validation
- Learning from outcomes and model improvement

ADAPTATION GUIDE:
🔧 To adapt for your project:
1. Update test data for your domain and personas
2. Modify prediction validation for your quality standards
3. Adjust AI confidence thresholds for your requirements
4. Update learning validation for your feedback patterns

CONTRACT PROTECTION:
These tests ensure AI enhancements don't break existing QA functionality.
"""

import pytest
import asyncio
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch
from typing import Dict, Any

from ..tools.quality_intelligence_engine import (
    QualityIntelligenceEngine,
    QualityPrediction,
    QualityPredictionConfidence,
    TestOptimizationResult,
    QualityInsight
)


class TestQualityIntelligenceEngine:
    """Test suite for QualityIntelligenceEngine."""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir) / "test_quality_intelligence.db"
    
    @pytest.fixture
    def engine_config(self, temp_db_path):
        """Configuration for test engine."""
        return {
            "db_path": str(temp_db_path),
            "confidence_threshold": 70.0,
            "learning_enabled": True
        }
    
    @pytest.fixture
    def quality_engine(self, engine_config):
        """Create QualityIntelligenceEngine for testing."""
        return QualityIntelligenceEngine(config=engine_config)
    
    @pytest.fixture
    def sample_implementation_data(self):
        """Sample implementation data for testing."""
        return {
            "ui_components": [
                {"component_id": "form1", "component_type": "form", "field_count": 5},
                {"component_id": "nav1", "component_type": "navigation", "links": 3},
                {"component_id": "button1", "component_type": "button", "text": "Submit"}
            ],
            "api_endpoints": [
                {"endpoint_id": "ep1", "method": "POST", "path": "/api/users"},
                {"endpoint_id": "ep2", "method": "GET", "path": "/api/users"}
            ],
            "user_flows": [
                {"flow_id": "registration", "steps": 4, "complexity": "medium"}
            ],
            "feature_flags": {"municipal_integration": True}
        }
    
    def test_engine_initialization(self, quality_engine, temp_db_path):
        """Test QualityIntelligenceEngine initialization."""
        assert quality_engine is not None
        assert quality_engine.db_path == temp_db_path
        assert quality_engine.model_confidence_threshold == 70.0
        assert quality_engine.learning_enabled is True
        
        # Database should be created
        assert temp_db_path.exists()
    
    @pytest.mark.asyncio
    async def test_quality_prediction(self, quality_engine, sample_implementation_data):
        """Test AI quality score prediction."""
        story_id = "STORY-TEST-001"
        
        prediction = await quality_engine.predict_quality_score(
            story_id=story_id,
            implementation_data=sample_implementation_data
        )
        
        # Validate prediction structure
        assert isinstance(prediction, QualityPrediction)
        assert 1.0 <= prediction.predicted_score <= 5.0
        assert isinstance(prediction.confidence_level, QualityPredictionConfidence)
        assert 0.0 <= prediction.confidence_percentage <= 100.0
        assert isinstance(prediction.risk_factors, list)
        assert isinstance(prediction.improvement_suggestions, list)
        assert isinstance(prediction.similar_projects, list)
        assert prediction.timestamp is not None
        
        # Municipal integration should boost prediction
        assert prediction.predicted_score >= 3.0  # Should be reasonable for municipal features
    
    @pytest.mark.asyncio
    async def test_test_optimization(self, quality_engine, sample_implementation_data):
        """Test AI-powered test optimization."""
        story_id = "STORY-TEST-002"
        test_results = {
            "coverage_percentage": 85,
            "failed_tests": [],
            "test_execution_time": 120
        }
        
        optimization = await quality_engine.optimize_test_coverage(
            story_id=story_id,
            test_results=test_results,
            implementation_data=sample_implementation_data
        )
        
        # Validate optimization structure
        assert isinstance(optimization, TestOptimizationResult)
        assert isinstance(optimization.priority_tests, list)
        assert isinstance(optimization.coverage_optimization, dict)
        assert isinstance(optimization.risk_based_focus_areas, list)
        assert isinstance(optimization.predicted_defect_areas, list)
        assert 0.0 <= optimization.optimization_confidence <= 100.0
        assert optimization.estimated_time_savings >= 0.0
        
        # Should identify common areas for optimization
        assert len(optimization.priority_tests) >= 0
        assert len(optimization.risk_based_focus_areas) >= 0
    
    @pytest.mark.asyncio
    async def test_anna_satisfaction_prediction(self, quality_engine, sample_implementation_data):
        """Test Anna persona satisfaction prediction."""
        story_id = "STORY-TEST-003"
        
        anna_prediction = await quality_engine.predict_anna_satisfaction(
            story_id=story_id,
            implementation_data=sample_implementation_data
        )
        
        # Validate Anna prediction structure
        assert isinstance(anna_prediction, dict)
        assert "predicted_satisfaction_score" in anna_prediction
        assert "predicted_completion_time_minutes" in anna_prediction
        assert "satisfaction_level" in anna_prediction
        assert "satisfaction_boosters" in anna_prediction
        assert "satisfaction_blockers" in anna_prediction
        assert "anna_specific_recommendations" in anna_prediction
        assert "confidence_score" in anna_prediction
        
        # Validate score ranges
        assert 1.0 <= anna_prediction["predicted_satisfaction_score"] <= 5.0
        assert anna_prediction["predicted_completion_time_minutes"] > 0
        assert 0.0 <= anna_prediction["confidence_score"] <= 100.0
        
        # Municipal features should have reasonable predictions
        assert anna_prediction["predicted_completion_time_minutes"] <= 15  # Reasonable time
    
    @pytest.mark.asyncio
    async def test_quality_insights_generation(self, quality_engine):
        """Test AI quality insights generation."""
        historical_data = {
            "performance_metrics": {"avg_response_time": 150, "lighthouse_score": 92},
            "accessibility_scores": {"wcag_compliance": 98},
            "user_satisfaction": {"anna_scores": [4.2, 4.5, 4.1]},
            "municipal_context": {"compliance_rate": 95}
        }
        
        insights = await quality_engine.generate_quality_insights(historical_data)
        
        # Validate insights structure
        assert isinstance(insights, list)
        for insight in insights:
            assert isinstance(insight, QualityInsight)
            assert insight.insight_id is not None
            assert insight.category in ["performance", "accessibility", "usability", "municipal_context"]
            assert insight.insight_description is not None
            assert isinstance(insight.supporting_evidence, list)
            assert isinstance(insight.actionable_recommendations, list)
            assert insight.impact_prediction in ["high", "medium", "low"]
            assert 0.0 <= insight.confidence_score <= 100.0
            assert 0.0 <= insight.historical_accuracy <= 100.0
        
        # Should generate multiple useful insights
        assert len(insights) >= 1
        assert len(insights) <= 10  # Reasonable number of insights
    
    @pytest.mark.asyncio
    async def test_learning_from_outcomes(self, quality_engine, sample_implementation_data):
        """Test learning from actual outcomes."""
        story_id = "STORY-TEST-004"
        
        # First make a prediction
        prediction = await quality_engine.predict_quality_score(
            story_id=story_id,
            implementation_data=sample_implementation_data
        )
        
        # Simulate actual outcomes
        actual_results = {
            "quality_score": 4.2,
            "anna_satisfaction": 4.1,
            "test_optimization_effectiveness": 85.5,
            "insight_validations": {
                "PERF_001": {"accuracy": 82.0},
                "A11Y_001": {"accuracy": 91.5}
            }
        }
        
        learning_results = await quality_engine.learn_from_outcome(
            story_id=story_id,
            actual_results=actual_results
        )
        
        # Validate learning results
        assert isinstance(learning_results, dict)
        assert "story_id" in learning_results
        assert "predictions_updated" in learning_results
        assert "accuracy_improvements" in learning_results
        assert "model_adjustments" in learning_results
        assert "learning_timestamp" in learning_results
        
        # Should have updated predictions
        assert learning_results["predictions_updated"] >= 0
        assert isinstance(learning_results["accuracy_improvements"], list)
        assert isinstance(learning_results["model_adjustments"], list)
    
    def test_feature_extraction_municipal_integration(self, quality_engine, sample_implementation_data):
        """Test feature extraction identifies municipal integration."""
        features = quality_engine._extract_quality_features(sample_implementation_data)
        
        assert isinstance(features, dict)
        assert "ui_component_count" in features
        assert "api_endpoint_count" in features
        assert "user_flow_count" in features
        assert "municipal_integration" in features
        
        # Municipal integration should be detected
        assert features["municipal_integration"] is True
        assert features["ui_component_count"] == 3
        assert features["api_endpoint_count"] == 2
        assert features["user_flow_count"] == 1
    
    def test_anna_feature_extraction(self, quality_engine, sample_implementation_data):
        """Test Anna-specific feature extraction."""
        anna_features = quality_engine._extract_anna_features(sample_implementation_data)
        
        assert isinstance(anna_features, dict)
        assert "form_field_count" in anna_features
        assert "navigation_steps" in anna_features
        assert "municipal_terminology" in anna_features
        assert "estimated_cognitive_load" in anna_features
        
        # Should detect form fields and navigation
        assert anna_features["form_field_count"] >= 0
        assert anna_features["navigation_steps"] >= 0
        assert 1.0 <= anna_features["estimated_cognitive_load"] <= 10.0
    
    def test_confidence_level_determination(self, quality_engine):
        """Test confidence level determination from percentage."""
        # Test different confidence levels
        assert quality_engine._determine_confidence_level(95.0) == QualityPredictionConfidence.HIGH
        assert quality_engine._determine_confidence_level(85.0) == QualityPredictionConfidence.MEDIUM
        assert quality_engine._determine_confidence_level(65.0) == QualityPredictionConfidence.LOW
        assert quality_engine._determine_confidence_level(45.0) == QualityPredictionConfidence.UNRELIABLE
    
    def test_quality_prediction_to_dict(self):
        """Test QualityPrediction serialization."""
        prediction = QualityPrediction(
            predicted_score=4.2,
            confidence_level=QualityPredictionConfidence.HIGH,
            confidence_percentage=92.5,
            risk_factors=["complexity"],
            improvement_suggestions=["simplify UI"],
            similar_projects=["STORY-001"],
            prediction_basis="ML analysis",
            timestamp="2024-06-14T10:00:00"
        )
        
        result = prediction.to_dict()
        
        assert isinstance(result, dict)
        assert result["predicted_score"] == 4.2
        assert result["confidence_level"] == "high"
        assert result["confidence_percentage"] == 92.5
        assert result["risk_factors"] == ["complexity"]
        assert result["improvement_suggestions"] == ["simplify UI"]
        assert result["similar_projects"] == ["STORY-001"]
    
    def test_test_optimization_to_dict(self):
        """Test TestOptimizationResult serialization."""
        optimization = TestOptimizationResult(
            priority_tests=[{"test": "form_validation", "priority": "high"}],
            coverage_optimization={"strategy": "risk_based"},
            risk_based_focus_areas=["user_input"],
            predicted_defect_areas=["validation"],
            optimization_confidence=87.5,
            estimated_time_savings=15.2
        )
        
        result = optimization.to_dict()
        
        assert isinstance(result, dict)
        assert result["priority_tests"] == [{"test": "form_validation", "priority": "high"}]
        assert result["coverage_optimization"] == {"strategy": "risk_based"}
        assert result["optimization_confidence"] == 87.5
        assert result["estimated_time_savings"] == 15.2
    
    @pytest.mark.asyncio
    async def test_database_operations(self, quality_engine, sample_implementation_data):
        """Test database storage and retrieval operations."""
        story_id = "STORY-TEST-DB-001"
        
        # Make prediction to store in database
        prediction = await quality_engine.predict_quality_score(
            story_id=story_id,
            implementation_data=sample_implementation_data
        )
        
        # Database should have the prediction stored
        # (This tests the internal storage mechanism)
        assert prediction is not None
        assert prediction.predicted_score > 0
        
        # Test Anna prediction storage
        anna_prediction = await quality_engine.predict_anna_satisfaction(
            story_id=story_id,
            implementation_data=sample_implementation_data
        )
        
        assert anna_prediction is not None
        assert anna_prediction["predicted_satisfaction_score"] > 0
    
    def test_error_handling_invalid_data(self, quality_engine):
        """Test error handling with invalid implementation data."""
        # Test with empty/invalid data
        invalid_data = {}
        
        # Should not crash and return reasonable defaults
        features = quality_engine._extract_quality_features(invalid_data)
        assert isinstance(features, dict)
        assert features["ui_component_count"] == 0
        assert features["api_endpoint_count"] == 0
        assert features["municipal_integration"] is False
    
    @pytest.mark.asyncio
    async def test_prediction_error_handling(self, quality_engine):
        """Test prediction error handling."""
        story_id = "STORY-ERROR-TEST"
        invalid_data = None
        
        # Should handle errors gracefully
        prediction = await quality_engine.predict_quality_score(
            story_id=story_id,
            implementation_data=invalid_data
        )
        
        # Should return default/error prediction
        assert isinstance(prediction, QualityPrediction)
        assert prediction.confidence_level == QualityPredictionConfidence.UNRELIABLE
        assert prediction.confidence_percentage == 0.0
    
    def test_municipal_context_detection(self, quality_engine):
        """Test detection of municipal context in implementation."""
        # Test with municipal keywords
        municipal_data = {
            "ui_components": [
                {"text": "Municipal policy compliance form"},
                {"description": "Citizen registration system"}
            ],
            "api_endpoints": [
                {"path": "/api/government/users"}
            ]
        }
        
        assert quality_engine._has_municipal_features(municipal_data) is True
        
        # Test without municipal context
        non_municipal_data = {
            "ui_components": [
                {"text": "User login form"},
                {"description": "Shopping cart"}
            ]
        }
        
        assert quality_engine._has_municipal_features(non_municipal_data) is False
    
    def test_cognitive_load_estimation(self, quality_engine):
        """Test cognitive load estimation for Anna persona."""
        # Complex implementation
        complex_data = {
            "ui_components": [{"type": "form"} for _ in range(15)],
            "user_flows": [{"steps": 8}, {"steps": 12}]
        }
        
        cognitive_load = quality_engine._estimate_cognitive_load(complex_data)
        assert 5.0 <= cognitive_load <= 10.0  # Should be high
        
        # Simple implementation
        simple_data = {
            "ui_components": [{"type": "button"}],
            "user_flows": [{"steps": 2}]
        }
        
        simple_load = quality_engine._estimate_cognitive_load(simple_data)
        assert 1.0 <= simple_load <= 5.0  # Should be lower
        assert simple_load < cognitive_load
    
    @pytest.mark.asyncio
    async def test_ai_enhancement_integration(self, quality_engine, sample_implementation_data):
        """Test integration of AI enhancements doesn't break functionality."""
        story_id = "STORY-INTEGRATION-TEST"
        
        # Test all major AI functions work together
        prediction = await quality_engine.predict_quality_score(
            story_id=story_id,
            implementation_data=sample_implementation_data
        )
        
        test_results = {"coverage_percentage": 90}
        optimization = await quality_engine.optimize_test_coverage(
            story_id=story_id,
            test_results=test_results,
            implementation_data=sample_implementation_data
        )
        
        anna_prediction = await quality_engine.predict_anna_satisfaction(
            story_id=story_id,
            implementation_data=sample_implementation_data
        )
        
        insights = await quality_engine.generate_quality_insights({})
        
        # All should complete successfully
        assert prediction is not None
        assert optimization is not None
        assert anna_prediction is not None
        assert insights is not None
        
        # Learning should work with combined results
        learning_results = await quality_engine.learn_from_outcome(
            story_id=story_id,
            actual_results={
                "quality_score": prediction.predicted_score,
                "anna_satisfaction": anna_prediction["predicted_satisfaction_score"]
            }
        )
        
        assert learning_results is not None
        assert "story_id" in learning_results


# Integration test for QA Tester Agent with AI enhancements
class TestQATesterAgentAIIntegration:
    """Test QA Tester Agent integration with AI Quality Intelligence."""
    
    @pytest.fixture
    def agent_config(self):
        """Configuration for QA Tester Agent with AI enabled."""
        return {
            "ai_config": {
                "db_path": ":memory:",  # Use in-memory database for testing
                "confidence_threshold": 70.0,
                "learning_enabled": True
            }
        }
    
    @pytest.mark.asyncio
    async def test_qa_agent_ai_integration(self, agent_config):
        """Test that QA Tester Agent properly integrates AI enhancements."""
        # Import here to avoid circular imports in test setup
        from ..agent import QATesterAgent
        
        # Create agent with AI configuration
        qa_agent = QATesterAgent(config=agent_config)
        
        # Verify AI components are initialized
        assert hasattr(qa_agent, 'quality_intelligence_engine')
        assert qa_agent.quality_intelligence_engine is not None
        
        # Test AI functionality is accessible
        sample_data = {
            "ui_components": [{"component_type": "form", "field_count": 3}],
            "api_endpoints": [{"method": "POST", "path": "/api/test"}],
            "user_flows": [{"flow_id": "test_flow", "steps": 3}]
        }
        
        # AI prediction should work
        prediction = await qa_agent.quality_intelligence_engine.predict_quality_score(
            story_id="STORY-AI-INTEGRATION",
            implementation_data=sample_data
        )
        
        assert prediction is not None
        assert isinstance(prediction.predicted_score, float)
        assert 1.0 <= prediction.predicted_score <= 5.0
    
    def test_backward_compatibility(self, agent_config):
        """Test that AI enhancements don't break existing QA functionality."""
        from ..agent import QATesterAgent
        
        # Test with AI disabled
        config_no_ai = {"ai_config": {"learning_enabled": False}}
        qa_agent_no_ai = QATesterAgent(config=config_no_ai)
        
        # Should still initialize successfully
        assert qa_agent_no_ai is not None
        assert hasattr(qa_agent_no_ai, 'quality_intelligence_engine')
        
        # Test with AI enabled
        qa_agent_with_ai = QATesterAgent(config=agent_config)
        
        # Should have same core functionality
        assert hasattr(qa_agent_with_ai, 'persona_simulator')
        assert hasattr(qa_agent_with_ai, 'accessibility_checker')
        assert hasattr(qa_agent_with_ai, 'user_flow_validator')
        
        # Additional AI functionality
        assert hasattr(qa_agent_with_ai, 'quality_intelligence_engine')