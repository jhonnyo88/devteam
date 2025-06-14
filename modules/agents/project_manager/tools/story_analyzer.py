"""
Story Analyzer Tool for Project Manager Agent.

PURPOSE:
Analyzes feature requests and creates comprehensive story breakdowns
that guide the development team through implementation.

CRITICAL IMPORTANCE:
- Transforms raw requirements into actionable development work
- Ensures consistency in story structure across all features
- Estimates complexity and timelines for project planning
- Maintains alignment with DigiNativa's learning objectives

REVENUE IMPACT:
Direct impact on revenue through:
- Accurate complexity estimation leading to better project planning
- Clear requirements reducing development rework
- Consistent story structure improving team velocity
- Better timeline estimates improving client satisfaction
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import re

from ....shared.exceptions import BusinessLogicError, AgentExecutionError


class StoryAnalyzer:
    """
    Advanced story analysis and breakdown tool for Project Manager Agent.
    
    Provides comprehensive analysis of feature requests including:
    - Story breakdown and structure
    - Acceptance criteria generation
    - Complexity assessment and estimation
    - Technical and design requirement analysis
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize Story Analyzer.
        
        Args:
            config: Configuration dictionary
        """
        self.logger = logging.getLogger(f"{__name__}.StoryAnalyzer")
        self.config = config or {}
        
        # Analysis configuration
        self.complexity_factors = self._initialize_complexity_factors()
        self.estimation_guidelines = self._initialize_estimation_guidelines()
        self.story_templates = self._initialize_story_templates()
        
        self.logger.info("Story Analyzer initialized successfully")
    
    async def create_story_breakdown(
        self,
        feature_data: Dict[str, Any],
        dna_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create comprehensive story breakdown from feature data.
        
        Args:
            feature_data: Original feature request data
            dna_analysis: DNA compliance analysis results
            
        Returns:
            Complete story breakdown dictionary
            
        Raises:
            BusinessLogicError: If feature data is insufficient for analysis
        """
        try:
            self.logger.debug("Creating story breakdown")
            
            # Validate input data
            self._validate_feature_data(feature_data)
            
            # Extract core components
            feature_summary = self._create_feature_summary(feature_data)
            user_stories = await self._generate_user_stories(feature_data)
            technical_requirements = self._analyze_technical_requirements(feature_data)
            design_requirements = self._analyze_design_requirements(feature_data, dna_analysis)
            implementation_tasks = self._break_down_implementation_tasks(feature_data)
            
            # Create dependencies and sequencing
            dependencies = self._identify_dependencies(implementation_tasks)
            task_sequence = self._sequence_tasks(implementation_tasks, dependencies)
            
            # Risk assessment
            risks = self._assess_risks(feature_data, technical_requirements)
            
            # Create comprehensive breakdown
            story_breakdown = {
                "story_id": self._generate_story_id(feature_data),
                "feature_summary": feature_summary,
                "user_stories": user_stories,
                "technical_requirements": technical_requirements,
                "design_requirements": design_requirements,
                "implementation_tasks": implementation_tasks,
                "task_sequence": task_sequence,
                "dependencies": dependencies,
                "risks": risks,
                "estimated_completion_time": self._estimate_completion_time(implementation_tasks),
                "quality_metrics": self._define_quality_metrics(feature_data),
                "testing_strategy": self._define_testing_strategy(feature_data),
                "deployment_considerations": self._analyze_deployment_considerations(feature_data),
                "created_at": datetime.now().isoformat(),
                "dna_alignment": dna_analysis
            }
            
            self.logger.debug("Story breakdown created successfully")
            return story_breakdown
            
        except BusinessLogicError:
            # Re-raise business logic errors as-is
            raise
            
        except Exception as e:
            self.logger.error(f"Failed to create story breakdown: {e}")
            raise AgentExecutionError(
                f"Story breakdown creation failed: {e}",
                agent_id="story_analyzer",
                execution_context={"feature_data": feature_data}
            )
    
    async def generate_acceptance_criteria(
        self,
        feature_data: Dict[str, Any],
        story_breakdown: Dict[str, Any]
    ) -> List[str]:
        """
        Generate comprehensive acceptance criteria for the feature.
        
        Args:
            feature_data: Original feature request data
            story_breakdown: Story breakdown data
            
        Returns:
            List of detailed acceptance criteria
        """
        try:
            self.logger.debug("Generating acceptance criteria")
            
            criteria = []
            
            # Base criteria from original request
            original_criteria = feature_data.get("acceptance_criteria", [])
            criteria.extend(original_criteria)
            
            # Generate criteria from user stories
            user_stories = story_breakdown.get("user_stories", [])
            for story in user_stories:
                story_criteria = self._generate_criteria_from_user_story(story)
                criteria.extend(story_criteria)
            
            # Add DNA-specific criteria
            dna_criteria = self._generate_dna_criteria(feature_data)
            criteria.extend(dna_criteria)
            
            # Add technical criteria
            technical_criteria = self._generate_technical_criteria(story_breakdown)
            criteria.extend(technical_criteria)
            
            # Add quality criteria
            quality_criteria = self._generate_quality_criteria(feature_data)
            criteria.extend(quality_criteria)
            
            # Clean up and deduplicate
            criteria = self._clean_and_deduplicate_criteria(criteria)
            
            # Ensure minimum number of criteria
            if len(criteria) < 5:
                additional_criteria = self._generate_fallback_criteria(feature_data)
                criteria.extend(additional_criteria)
            
            self.logger.debug(f"Generated {len(criteria)} acceptance criteria")
            return criteria
            
        except Exception as e:
            self.logger.error(f"Failed to generate acceptance criteria: {e}")
            raise AgentExecutionError(
                f"Acceptance criteria generation failed: {e}",
                agent_id="story_analyzer"
            )
    
    async def assess_complexity(self, story_breakdown: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess feature complexity and provide effort estimates.
        
        Args:
            story_breakdown: Story breakdown data
            
        Returns:
            Complexity assessment dictionary
        """
        try:
            self.logger.debug("Assessing feature complexity")
            
            # Analyze different complexity dimensions
            technical_complexity = self._assess_technical_complexity(story_breakdown)
            design_complexity = self._assess_design_complexity(story_breakdown)
            integration_complexity = self._assess_integration_complexity(story_breakdown)
            testing_complexity = self._assess_testing_complexity(story_breakdown)
            
            # Calculate overall effort points
            effort_points = self._calculate_effort_points(
                technical_complexity,
                design_complexity,
                integration_complexity,
                testing_complexity
            )
            
            # Estimate duration
            estimated_duration = self._estimate_duration_from_effort(effort_points)
            
            # Identify risk factors
            risk_factors = self._identify_complexity_risks(story_breakdown)
            
            # Generate implementation notes
            implementation_notes = self._generate_implementation_notes(
                story_breakdown,
                technical_complexity,
                design_complexity
            )
            
            complexity_assessment = {
                "overall_complexity": self._categorize_complexity(effort_points),
                "effort_points": effort_points,
                "technical_complexity": technical_complexity,
                "design_complexity": design_complexity,
                "integration_complexity": integration_complexity,
                "testing_complexity": testing_complexity,
                "estimated_duration_hours": estimated_duration,
                "estimated_duration_days": round(estimated_duration / 8, 1),
                "risk_factors": risk_factors,
                "confidence_level": self._calculate_confidence_level(story_breakdown),
                "implementation_notes": implementation_notes,
                "complexity_breakdown": {
                    "frontend_work": self._estimate_frontend_effort(story_breakdown),
                    "backend_work": self._estimate_backend_effort(story_breakdown),
                    "testing_work": self._estimate_testing_effort(story_breakdown),
                    "integration_work": self._estimate_integration_effort(story_breakdown)
                },
                "assessment_timestamp": datetime.now().isoformat()
            }
            
            self.logger.debug("Complexity assessment completed")
            return complexity_assessment
            
        except Exception as e:
            self.logger.error(f"Failed to assess complexity: {e}")
            raise AgentExecutionError(
                f"Complexity assessment failed: {e}",
                agent_id="story_analyzer"
            )
    
    def _validate_feature_data(self, feature_data: Dict[str, Any]) -> None:
        """Validate that feature data contains required fields."""
        required_fields = [
            "feature_description", "user_persona", "priority_level"
        ]
        
        for field in required_fields:
            if field not in feature_data:
                raise BusinessLogicError(
                    f"Missing required field for story analysis: {field}",
                    business_rule="story_analysis_requirements",
                    context={"missing_field": field}
                )
        
        # Validate field content
        if not feature_data["feature_description"].strip():
            raise BusinessLogicError(
                "Feature description cannot be empty",
                business_rule="feature_description_requirements"
            )
    
    def _create_feature_summary(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured feature summary."""
        description = feature_data["feature_description"]
        
        # Extract title from description if needed
        lines = description.split('\n')
        title = lines[0].strip() if lines else "Untitled Feature"
        
        # Extract key information
        summary = {
            "title": title,
            "description": description,
            "user_persona": feature_data["user_persona"],
            "priority": feature_data["priority_level"],
            "time_constraint_minutes": feature_data.get("time_constraint_minutes", 10),
            "learning_objectives": feature_data.get("learning_objectives", []),
            "business_value": self._extract_business_value(description),
            "success_metrics": self._define_success_metrics(feature_data)
        }
        
        return summary
    
    async def _generate_user_stories(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate user stories from feature data."""
        user_stories = []
        description = feature_data["feature_description"]
        persona = feature_data["user_persona"]
        
        # Parse existing user stories from description
        story_patterns = [
            r"As\s+(?:a|an)\s+(.+?),\s*I\s+want\s+(.+?)\s+so\s+that\s+(.+?)(?:\.|$)",
            r"As\s+(.+?),\s*I\s+want\s+(.+?)(?:\.|$)"
        ]
        
        for pattern in story_patterns:
            matches = re.findall(pattern, description, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if len(match) == 3:
                    user_stories.append({
                        "role": match[0].strip(),
                        "action": match[1].strip(),
                        "benefit": match[2].strip(),
                        "story": f"As {match[0]}, I want {match[1]} so that {match[2]}"
                    })
                elif len(match) == 2:
                    user_stories.append({
                        "role": match[0].strip(),
                        "action": match[1].strip(),
                        "benefit": "I can accomplish my learning goals",
                        "story": f"As {match[0]}, I want {match[1]} so that I can accomplish my learning goals"
                    })
        
        # Generate default user stories if none found
        if not user_stories:
            user_stories = self._generate_default_user_stories(feature_data)
        
        # Add story metadata
        for i, story in enumerate(user_stories):
            story.update({
                "story_id": f"US-{i+1:03d}",
                "priority": "high" if i == 0 else "medium",
                "estimation": self._estimate_user_story(story),
                "acceptance_criteria": self._generate_story_acceptance_criteria(story)
            })
        
        return user_stories
    
    def _analyze_technical_requirements(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical requirements for the feature."""
        description = feature_data["feature_description"].lower()
        
        # Identify required technologies and components
        frontend_requirements = self._identify_frontend_requirements(description)
        backend_requirements = self._identify_backend_requirements(description)
        database_requirements = self._identify_database_requirements(description)
        integration_requirements = self._identify_integration_requirements(description)
        
        return {
            "frontend": frontend_requirements,
            "backend": backend_requirements,
            "database": database_requirements,
            "integrations": integration_requirements,
            "performance_requirements": self._define_performance_requirements(feature_data),
            "security_requirements": self._define_security_requirements(feature_data),
            "scalability_requirements": self._define_scalability_requirements(feature_data),
            "compatibility_requirements": self._define_compatibility_requirements()
        }
    
    def _analyze_design_requirements(
        self,
        feature_data: Dict[str, Any],
        dna_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze design and UX requirements."""
        return {
            "ui_components": self._identify_required_ui_components(feature_data),
            "user_flows": self._define_user_flows(feature_data),
            "wireframe_requirements": self._define_wireframe_requirements(feature_data),
            "accessibility_requirements": self._define_accessibility_requirements(),
            "responsive_design": self._define_responsive_requirements(),
            "branding_requirements": self._define_branding_requirements(),
            "animation_requirements": self._define_animation_requirements(feature_data),
            "dna_design_constraints": self._extract_dna_design_constraints(dna_analysis)
        }
    
    def _break_down_implementation_tasks(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Break down feature into specific implementation tasks."""
        tasks = []
        
        # Standard task categories for DigiNativa features
        task_categories = [
            ("Frontend Development", self._generate_frontend_tasks),
            ("Backend Development", self._generate_backend_tasks),
            ("Database Work", self._generate_database_tasks),
            ("Integration Work", self._generate_integration_tasks),
            ("Testing", self._generate_testing_tasks),
            ("Documentation", self._generate_documentation_tasks),
            ("Deployment", self._generate_deployment_tasks)
        ]
        
        task_id = 1
        for category, generator in task_categories:
            category_tasks = generator(feature_data)
            for task in category_tasks:
                task.update({
                    "task_id": f"TASK-{task_id:03d}",
                    "category": category,
                    "created_at": datetime.now().isoformat()
                })
                tasks.append(task)
                task_id += 1
        
        return tasks
    
    def _initialize_complexity_factors(self) -> Dict[str, Any]:
        """Initialize complexity assessment factors."""
        return {
            "ui_complexity_weights": {
                "simple_form": 1,
                "complex_form": 3,
                "data_visualization": 4,
                "interactive_game": 5,
                "animation": 3,
                "responsive_layout": 2
            },
            "backend_complexity_weights": {
                "simple_crud": 2,
                "complex_business_logic": 4,
                "external_integration": 3,
                "authentication": 2,
                "file_handling": 3,
                "real_time_features": 5
            },
            "integration_complexity_weights": {
                "github_api": 2,
                "third_party_service": 3,
                "database_migration": 4,
                "authentication_provider": 3
            }
        }
    
    def _initialize_estimation_guidelines(self) -> Dict[str, Any]:
        """Initialize estimation guidelines."""
        return {
            "effort_to_hours": {
                1: 2,    # 1 point = 2 hours
                2: 4,    # 2 points = 4 hours  
                3: 8,    # 3 points = 8 hours (1 day)
                5: 16,   # 5 points = 16 hours (2 days)
                8: 32,   # 8 points = 32 hours (4 days)
                13: 64   # 13 points = 64 hours (8 days)
            },
            "confidence_factors": {
                "well_defined": 0.9,
                "partially_defined": 0.7,
                "poorly_defined": 0.5,
                "unknown": 0.3
            }
        }
    
    def _initialize_story_templates(self) -> Dict[str, Any]:
        """Initialize story templates for common DigiNativa patterns."""
        return {
            "user_registration": {
                "stories": [
                    "As Anna, I want to create an account so that I can access personalized learning content",
                    "As Anna, I want to verify my email so that my account is secure",
                    "As Anna, I want to log in so that I can continue my learning journey"
                ]
            },
            "learning_module": {
                "stories": [
                    "As Anna, I want to view learning objectives so that I understand what I'll learn",
                    "As Anna, I want to interact with learning content so that I can engage actively",
                    "As Anna, I want to track my progress so that I can see my advancement"
                ]
            },
            "assessment": {
                "stories": [
                    "As Anna, I want to take assessments so that I can validate my learning",
                    "As Anna, I want to receive immediate feedback so that I can learn from mistakes",
                    "As Anna, I want to see my results so that I can track my performance"
                ]
            }
        }
    
    # Additional helper methods for complexity assessment
    def _assess_technical_complexity(self, story_breakdown: Dict[str, Any]) -> str:
        """Assess technical complexity level."""
        tech_requirements = story_breakdown.get("technical_requirements", {})
        
        complexity_score = 0
        
        # Frontend complexity
        frontend = tech_requirements.get("frontend", {})
        complexity_score += len(frontend.get("required_components", [])) * 1
        complexity_score += len(frontend.get("animations", [])) * 2
        
        # Backend complexity  
        backend = tech_requirements.get("backend", {})
        complexity_score += len(backend.get("api_endpoints", [])) * 1
        complexity_score += len(backend.get("business_logic", [])) * 2
        
        # Integration complexity
        integrations = tech_requirements.get("integrations", {})
        complexity_score += len(integrations.get("external_apis", [])) * 3
        
        if complexity_score <= 5:
            return "Low"
        elif complexity_score <= 15:
            return "Medium"
        elif complexity_score <= 25:
            return "High"
        else:
            return "Very High"
    
    def _assess_design_complexity(self, story_breakdown: Dict[str, Any]) -> str:
        """Assess design complexity level."""
        design_requirements = story_breakdown.get("design_requirements", {})
        
        complexity_score = 0
        complexity_score += len(design_requirements.get("ui_components", [])) * 1
        complexity_score += len(design_requirements.get("user_flows", [])) * 2
        complexity_score += len(design_requirements.get("wireframe_requirements", [])) * 1
        
        if complexity_score <= 3:
            return "Low"
        elif complexity_score <= 8:
            return "Medium"
        elif complexity_score <= 15:
            return "High"
        else:
            return "Very High"
    
    def _assess_integration_complexity(self, story_breakdown: Dict[str, Any]) -> str:
        """Assess integration complexity level."""
        # Simplified integration assessment
        integrations = story_breakdown.get("technical_requirements", {}).get("integrations", {})
        external_apis = integrations.get("external_apis", [])
        
        if len(external_apis) == 0:
            return "Low"
        elif len(external_apis) <= 2:
            return "Medium"
        else:
            return "High"
    
    def _assess_testing_complexity(self, story_breakdown: Dict[str, Any]) -> str:
        """Assess testing complexity level."""
        # Simplified testing assessment based on implementation tasks
        tasks = story_breakdown.get("implementation_tasks", [])
        testing_tasks = [task for task in tasks if task.get("category") == "Testing"]
        
        if len(testing_tasks) <= 3:
            return "Low"
        elif len(testing_tasks) <= 6:
            return "Medium"
        else:
            return "High"
    
    def _calculate_effort_points(self, tech_complexity: str, design_complexity: str, 
                                integration_complexity: str, testing_complexity: str) -> int:
        """Calculate effort points from complexity assessments."""
        complexity_points = {
            "Low": 1,
            "Medium": 3,
            "High": 5,
            "Very High": 8
        }
        
        total_points = (
            complexity_points.get(tech_complexity, 3) +
            complexity_points.get(design_complexity, 3) +
            complexity_points.get(integration_complexity, 1) +
            complexity_points.get(testing_complexity, 2)
        )
        
        return min(total_points, 13)  # Cap at 13 points (8 days max)
    
    def _estimate_duration_from_effort(self, effort_points: int) -> float:
        """Estimate duration in hours from effort points."""
        effort_to_hours = self.estimation_guidelines["effort_to_hours"]
        
        # Find closest effort point mapping
        for points in sorted(effort_to_hours.keys()):
            if effort_points <= points:
                return float(effort_to_hours[points])
        
        # Fallback for very high effort
        return 64.0
    
    def _categorize_complexity(self, effort_points: int) -> str:
        """Categorize overall complexity based on effort points."""
        if effort_points <= 2:
            return "Simple"
        elif effort_points <= 5:
            return "Medium"
        elif effort_points <= 8:
            return "Complex"
        else:
            return "Very Complex"
    
    def _calculate_confidence_level(self, story_breakdown: Dict[str, Any]) -> float:
        """Calculate confidence level in estimates."""
        # Simplified confidence calculation
        base_confidence = 0.8
        
        # Reduce confidence for complex features
        effort_points = story_breakdown.get("effort_points", 5)
        if effort_points > 8:
            base_confidence -= 0.2
        
        # Reduce confidence for unclear requirements
        user_stories = story_breakdown.get("user_stories", [])
        if len(user_stories) < 3:
            base_confidence -= 0.1
        
        return max(base_confidence, 0.3)
    
    # Simplified implementations for required helper methods
    def _generate_story_id(self, feature_data: Dict[str, Any]) -> str:
        """Generate story ID from feature data."""
        github_number = feature_data.get("github_issue_number")
        if github_number:
            return f"STORY-GH-{github_number}"
        else:
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            return f"STORY-{timestamp}"
    
    def _extract_business_value(self, description: str) -> str:
        """Extract business value from description."""
        # Simplified business value extraction
        return "Improves user learning experience and engagement"
    
    def _define_success_metrics(self, feature_data: Dict[str, Any]) -> List[str]:
        """Define success metrics for the feature."""
        return [
            "Feature completion within time constraint",
            "User satisfaction score > 4.0",
            "Zero critical bugs in production",
            "Performance meets specified requirements"
        ]
    
    def _generate_default_user_stories(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate default user stories when none are found."""
        persona = feature_data["user_persona"]
        description = feature_data["feature_description"]
        
        return [
            {
                "role": persona,
                "action": "use this feature",
                "benefit": "I can achieve my learning objectives",
                "story": f"As {persona}, I want to use this feature so that I can achieve my learning objectives"
            }
        ]
    
    def _estimate_user_story(self, story: Dict[str, Any]) -> int:
        """Estimate effort for a user story."""
        # Simplified estimation
        return 3  # Default 3 points for user stories
    
    def _generate_story_acceptance_criteria(self, story: Dict[str, Any]) -> List[str]:
        """Generate acceptance criteria for a user story."""
        return [
            f"User can {story['action']} successfully",
            "Feature works correctly for the target persona",
            "Feature meets performance requirements"
        ]
    
    # Simplified implementations for technical analysis
    def _identify_frontend_requirements(self, description: str) -> Dict[str, Any]:
        """Identify frontend requirements."""
        return {
            "required_components": ["form", "button", "layout"],
            "animations": [],
            "responsive_design": True
        }
    
    def _identify_backend_requirements(self, description: str) -> Dict[str, Any]:
        """Identify backend requirements."""
        return {
            "api_endpoints": ["/api/feature"],
            "business_logic": ["validation", "processing"],
            "data_models": ["FeatureModel"]
        }
    
    def _identify_database_requirements(self, description: str) -> Dict[str, Any]:
        """Identify database requirements."""
        return {
            "new_tables": [],
            "schema_changes": [],
            "migrations": []
        }
    
    def _identify_integration_requirements(self, description: str) -> Dict[str, Any]:
        """Identify integration requirements."""
        return {
            "external_apis": [],
            "internal_services": []
        }
    
    # More simplified implementations for other required methods
    def _define_performance_requirements(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"response_time_ms": 200, "concurrent_users": 100}
    
    def _define_security_requirements(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"authentication_required": True, "data_encryption": True}
    
    def _define_scalability_requirements(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"horizontal_scaling": True}
    
    def _define_compatibility_requirements(self) -> Dict[str, Any]:
        return {"browsers": ["Chrome", "Firefox", "Safari"], "mobile": True}
    
    def _identify_required_ui_components(self, feature_data: Dict[str, Any]) -> List[str]:
        return ["Button", "Input", "Card", "Layout"]
    
    def _define_user_flows(self, feature_data: Dict[str, Any]) -> List[str]:
        return ["Main user flow", "Error handling flow"]
    
    def _define_wireframe_requirements(self, feature_data: Dict[str, Any]) -> List[str]:
        return ["Main screen wireframe", "Mobile wireframe"]
    
    def _define_accessibility_requirements(self) -> Dict[str, Any]:
        return {"wcag_compliance": "AA", "screen_reader": True}
    
    def _define_responsive_requirements(self) -> Dict[str, Any]:
        return {"mobile_first": True, "breakpoints": ["sm", "md", "lg"]}
    
    def _define_branding_requirements(self) -> Dict[str, Any]:
        return {"style_guide": "DigiNativa", "color_scheme": "primary"}
    
    def _define_animation_requirements(self, feature_data: Dict[str, Any]) -> List[str]:
        return []
    
    def _extract_dna_design_constraints(self, dna_analysis: Dict[str, Any]) -> Dict[str, Any]:
        return {"pedagogical_focus": True, "professional_tone": True}
    
    # Task generation methods (simplified)
    def _generate_frontend_tasks(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"name": "Create UI components", "effort": 3, "description": "Implement required UI components"}
        ]
    
    def _generate_backend_tasks(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"name": "Create API endpoints", "effort": 2, "description": "Implement backend API"}
        ]
    
    def _generate_database_tasks(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return []
    
    def _generate_integration_tasks(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return []
    
    def _generate_testing_tasks(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"name": "Unit tests", "effort": 1, "description": "Write unit tests"},
            {"name": "Integration tests", "effort": 2, "description": "Write integration tests"}
        ]
    
    def _generate_documentation_tasks(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"name": "API documentation", "effort": 1, "description": "Document API endpoints"}
        ]
    
    def _generate_deployment_tasks(self, feature_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"name": "Deploy to staging", "effort": 1, "description": "Deploy feature to staging"}
        ]
    
    # Other required helper methods (simplified)
    def _identify_dependencies(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return []
    
    def _sequence_tasks(self, tasks: List[Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> List[str]:
        return [task["name"] for task in tasks]
    
    def _assess_risks(self, feature_data: Dict[str, Any], tech_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{"risk": "Scope creep", "mitigation": "Clear requirements", "severity": "medium"}]
    
    def _estimate_completion_time(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        total_effort = sum(task.get("effort", 1) for task in tasks)
        return {"total_effort_points": total_effort, "estimated_hours": total_effort * 2}
    
    def _define_quality_metrics(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"code_coverage": 90, "performance_score": 90}
    
    def _define_testing_strategy(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"unit_tests": True, "integration_tests": True, "e2e_tests": True}
    
    def _analyze_deployment_considerations(self, feature_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"deployment_type": "rolling", "rollback_plan": True}
    
    def _generate_criteria_from_user_story(self, story: Dict[str, Any]) -> List[str]:
        return [f"User can {story['action']} as expected"]
    
    def _generate_dna_criteria(self, feature_data: Dict[str, Any]) -> List[str]:
        return [
            "Feature maintains pedagogical value",
            "Feature respects 10-minute time constraint",
            "Feature uses professional tone appropriate for Anna persona"
        ]
    
    def _generate_technical_criteria(self, story_breakdown: Dict[str, Any]) -> List[str]:
        return [
            "All API endpoints respond within 200ms",
            "Frontend components are accessible (WCAG AA)",
            "Feature works on mobile devices"
        ]
    
    def _generate_quality_criteria(self, feature_data: Dict[str, Any]) -> List[str]:
        return [
            "Code coverage is above 90%",
            "No critical security vulnerabilities",
            "Performance score above 90"
        ]
    
    def _clean_and_deduplicate_criteria(self, criteria: List[str]) -> List[str]:
        # Remove duplicates while preserving order
        seen = set()
        cleaned = []
        for criterion in criteria:
            if criterion.strip() and criterion not in seen:
                seen.add(criterion)
                cleaned.append(criterion.strip())
        return cleaned
    
    def _generate_fallback_criteria(self, feature_data: Dict[str, Any]) -> List[str]:
        return [
            "Feature is implemented according to specifications",
            "Feature works correctly for target user persona",
            "Feature meets all performance requirements"
        ]
    
    def _identify_complexity_risks(self, story_breakdown: Dict[str, Any]) -> List[str]:
        return ["Technical complexity", "Timeline constraints"]
    
    def _generate_implementation_notes(self, story_breakdown: Dict[str, Any], 
                                     tech_complexity: str, design_complexity: str) -> str:
        return f"Implementation involves {tech_complexity.lower()} technical complexity and {design_complexity.lower()} design complexity."
    
    # Effort estimation methods (simplified)
    def _estimate_frontend_effort(self, story_breakdown: Dict[str, Any]) -> int:
        return 3
    
    def _estimate_backend_effort(self, story_breakdown: Dict[str, Any]) -> int:
        return 2
    
    def _estimate_testing_effort(self, story_breakdown: Dict[str, Any]) -> int:
        return 2
    
    def _estimate_integration_effort(self, story_breakdown: Dict[str, Any]) -> int:
        return 1