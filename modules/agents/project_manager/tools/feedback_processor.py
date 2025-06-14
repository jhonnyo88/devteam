"""
Feedback Processor Tool for Project Manager Agent.

PURPOSE:
Processes project owner feedback from approval/rejection decisions,
converts feedback into actionable development tasks, and manages
the revision workflow.

CRITICAL IMPORTANCE:
- Ensures all project owner feedback is properly analyzed
- Converts subjective feedback into objective development tasks
- Maintains quality improvement loop for AI team learning
- Automates revision planning and task prioritization

REVENUE IMPACT:
Direct impact on revenue through:
- Higher client satisfaction through feedback integration
- Faster revision cycles reducing time-to-approval
- Systematic quality improvement reducing future rejections
- Automated workflow reducing manual overhead
"""

import re
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from ....shared.exceptions import BusinessLogicError, DNAComplianceError


class FeedbackCategory(Enum):
    """Categories for feedback classification."""
    DESIGN = "design"
    DEVELOPMENT = "development"
    TESTING = "testing"
    UX = "user_experience"
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"
    DNA_COMPLIANCE = "dna_compliance"
    CONTENT = "content"


class IssuePriority(Enum):
    """Priority levels for feedback issues."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class FeedbackIssue:
    """Structured representation of a feedback issue."""
    description: str
    category: FeedbackCategory
    priority: IssuePriority
    expected_behavior: str
    actual_behavior: str
    acceptance_criteria: List[str]
    estimated_effort_hours: float
    agent_assignment: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "description": self.description,
            "category": self.category.value,
            "priority": self.priority.value,
            "expected_behavior": self.expected_behavior,
            "actual_behavior": self.actual_behavior,
            "acceptance_criteria": self.acceptance_criteria,
            "estimated_effort_hours": self.estimated_effort_hours,
            "agent_assignment": self.agent_assignment
        }


@dataclass
class RevisionPlan:
    """Comprehensive plan for feature revision based on feedback."""
    story_id: str
    original_story_id: str
    revision_number: int
    feedback_summary: str
    total_issues: int
    critical_issues: int
    development_phases: List[Dict[str, Any]]
    estimated_total_hours: float
    estimated_completion_date: str
    success_criteria: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "story_id": self.story_id,
            "original_story_id": self.original_story_id,
            "revision_number": self.revision_number,
            "feedback_summary": self.feedback_summary,
            "total_issues": self.total_issues,
            "critical_issues": self.critical_issues,
            "development_phases": self.development_phases,
            "estimated_total_hours": self.estimated_total_hours,
            "estimated_completion_date": self.estimated_completion_date,
            "success_criteria": self.success_criteria
        }


class FeedbackProcessor:
    """
    Processes project owner feedback and creates revision plans.
    
    Handles conversion of subjective feedback into objective development
    tasks with proper agent assignment and timeline estimation.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize feedback processor.
        
        Args:
            config: Configuration dictionary
        """
        self.logger = logging.getLogger(f"{__name__}.FeedbackProcessor")
        self.config = config or {}
        
        # Effort estimation factors (hours per issue type)
        self.effort_estimates = {
            FeedbackCategory.DESIGN: {"critical": 8, "high": 4, "medium": 2, "low": 1},
            FeedbackCategory.DEVELOPMENT: {"critical": 12, "high": 6, "medium": 3, "low": 1.5},
            FeedbackCategory.TESTING: {"critical": 6, "high": 3, "medium": 1.5, "low": 0.5},
            FeedbackCategory.UX: {"critical": 10, "high": 5, "medium": 2.5, "low": 1},
            FeedbackCategory.PERFORMANCE: {"critical": 16, "high": 8, "medium": 4, "low": 2},
            FeedbackCategory.ACCESSIBILITY: {"critical": 8, "high": 4, "medium": 2, "low": 1},
            FeedbackCategory.DNA_COMPLIANCE: {"critical": 6, "high": 3, "medium": 1.5, "low": 0.5},
            FeedbackCategory.CONTENT: {"critical": 4, "high": 2, "medium": 1, "low": 0.5}
        }
        
        # Agent assignment mapping
        self.agent_assignments = {
            FeedbackCategory.DESIGN: "game_designer",
            FeedbackCategory.DEVELOPMENT: "developer", 
            FeedbackCategory.TESTING: "test_engineer",
            FeedbackCategory.UX: "game_designer",
            FeedbackCategory.PERFORMANCE: "developer",
            FeedbackCategory.ACCESSIBILITY: "qa_tester",
            FeedbackCategory.DNA_COMPLIANCE: "project_manager",
            FeedbackCategory.CONTENT: "game_designer"
        }
        
        self.logger.info("Feedback processor initialized")
    
    async def process_approval_decision(self, approval_issue: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process project owner approval decision.
        
        Args:
            approval_issue: GitHub issue containing approval decision
            
        Returns:
            Processing result with action plan
        """
        try:
            # Parse the approval decision
            decision = self._parse_approval_decision(approval_issue["body"])
            story_id = self._extract_story_id(approval_issue["title"])
            
            self.logger.info(f"Processing approval decision for {story_id}: {decision['status']}")
            
            # Handle based on decision type
            if decision["status"] == "APPROVED":
                return await self._handle_feature_approval(story_id, decision)
            elif decision["status"] == "REJECTED":
                return await self._handle_feature_rejection(story_id, decision)
            elif decision["status"] == "APPROVED_WITH_ISSUES":
                return await self._handle_conditional_approval(story_id, decision)
            else:
                raise BusinessLogicError(
                    f"Invalid approval status: {decision['status']}",
                    business_rule="approval_decision_parsing"
                )
                
        except Exception as e:
            raise BusinessLogicError(
                f"Failed to process approval decision: {e}",
                business_rule="approval_decision_processing",
                context={"issue_number": approval_issue.get("number")}
            )
    
    def _parse_approval_decision(self, issue_body: str) -> Dict[str, Any]:
        """Parse approval decision from issue body."""
        
        # Determine decision status
        status = "PENDING"
        if re.search(r"- \[x\] \*\*APPROVED\*\*", issue_body, re.IGNORECASE):
            status = "APPROVED"
        elif re.search(r"- \[x\] \*\*REJECTED\*\*", issue_body, re.IGNORECASE):
            status = "REJECTED"
        elif re.search(r"- \[x\] \*\*APPROVED WITH MINOR ISSUES\*\*", issue_body, re.IGNORECASE):
            status = "APPROVED_WITH_ISSUES"
        
        # Extract feedback sections
        critical_issues = self._extract_critical_issues(issue_body)
        minor_issues = self._extract_minor_issues(issue_body)
        acceptance_criteria_review = self._extract_acceptance_criteria_review(issue_body)
        quality_ratings = self._extract_quality_ratings(issue_body)
        next_feature_priority = self._extract_next_feature_priority(issue_body)
        
        return {
            "status": status,
            "critical_issues": critical_issues,
            "minor_issues": minor_issues,
            "acceptance_criteria_review": acceptance_criteria_review,
            "quality_ratings": quality_ratings,
            "next_feature_priority": next_feature_priority,
            "feedback_timestamp": datetime.now().isoformat()
        }
    
    def _extract_critical_issues(self, issue_body: str) -> List[Dict[str, Any]]:
        """Extract critical issues from feedback."""
        critical_issues = []
        
        # Find critical issues section
        critical_section_pattern = r"### 🚨 Critical Issues.*?\n(.*?)(?=\n###|\n---|\n$|$)"
        match = re.search(critical_section_pattern, issue_body, re.DOTALL | re.IGNORECASE)
        
        if match:
            critical_text = match.group(1)
            
            # Parse individual issues
            issue_pattern = r"\d+\.\s*\*\*Issue:\*\*\s*(.*?)\s*\*\*Expected:\*\*\s*(.*?)\s*\*\*Actual:\*\*\s*(.*?)\s*\*\*Priority:\*\*\s*(.*?)(?=\n\d+\.|\n\*\*|$)"
            
            for issue_match in re.finditer(issue_pattern, critical_text, re.DOTALL):
                critical_issues.append({
                    "description": issue_match.group(1).strip(),
                    "expected": issue_match.group(2).strip(),
                    "actual": issue_match.group(3).strip(),
                    "priority": issue_match.group(4).strip().lower()
                })
        
        return critical_issues
    
    def _extract_minor_issues(self, issue_body: str) -> List[str]:
        """Extract minor issues from feedback."""
        minor_issues = []
        
        # Find minor issues section
        minor_section_pattern = r"### ⚠️ Minor Issues.*?\n(.*?)(?=\n###|\n---|\n$|$)"
        match = re.search(minor_section_pattern, issue_body, re.DOTALL | re.IGNORECASE)
        
        if match:
            minor_text = match.group(1)
            
            # Extract bullet points
            issue_lines = re.findall(r"^-\s*(.+)$", minor_text, re.MULTILINE)
            minor_issues = [issue.strip() for issue in issue_lines if issue.strip()]
        
        return minor_issues
    
    def _extract_acceptance_criteria_review(self, issue_body: str) -> Dict[str, Any]:
        """Extract acceptance criteria review results."""
        criteria_review = {"passed": [], "failed": []}
        
        # Find acceptance criteria section
        criteria_pattern = r"### ✅ Acceptance Criteria Review.*?\n(.*?)(?=\n###|\n---|\n$|$)"
        match = re.search(criteria_pattern, issue_body, re.DOTALL | re.IGNORECASE)
        
        if match:
            criteria_text = match.group(1)
            
            # Parse individual criteria
            criterion_pattern = r"- \[([ x])\] (.+?):\s*(Met|Not Met)\s*-\s*(.*?)(?=\n-|\n$|$)"
            
            for criterion_match in re.finditer(criterion_pattern, criteria_text, re.DOTALL):
                checked = criterion_match.group(1) == "x"
                criterion_text = criterion_match.group(2).strip()
                status = criterion_match.group(3).strip()
                feedback = criterion_match.group(4).strip()
                
                criterion_data = {
                    "criterion": criterion_text,
                    "status": status,
                    "feedback": feedback
                }
                
                if status.lower() == "met":
                    criteria_review["passed"].append(criterion_data)
                else:
                    criteria_review["failed"].append(criterion_data)
        
        return criteria_review
    
    def _extract_quality_ratings(self, issue_body: str) -> Dict[str, float]:
        """Extract quality ratings from feedback."""
        ratings = {}
        
        # Rating patterns
        rating_patterns = {
            "anna_persona_experience": r"Anna Persona Experience:\*\*\s*([\d.]+)/5\.0",
            "ease_of_use": r"Ease of Use:\*\*\s*([\d.]+)/5\.0",
            "municipal_relevance": r"Municipal Relevance:\*\*\s*([\d.]+)/5\.0",
            "policy_alignment": r"Policy Alignment:\*\*\s*([\d.]+)/5\.0"
        }
        
        for rating_name, pattern in rating_patterns.items():
            match = re.search(pattern, issue_body, re.IGNORECASE)
            if match:
                try:
                    ratings[rating_name] = float(match.group(1))
                except ValueError:
                    self.logger.warning(f"Invalid rating format for {rating_name}: {match.group(1)}")
        
        return ratings
    
    def _extract_next_feature_priority(self, issue_body: str) -> Optional[str]:
        """Extract next feature priority suggestion."""
        priority_pattern = r"Next Feature to Work On:\*\*\s*([^\n]+)"
        match = re.search(priority_pattern, issue_body, re.IGNORECASE)
        
        if match:
            return match.group(1).strip()
        
        return None
    
    def _extract_story_id(self, title: str) -> str:
        """Extract story ID from issue title."""
        story_pattern = r"(STORY-[A-Z0-9-]+)"
        match = re.search(story_pattern, title)
        
        if match:
            return match.group(1)
        
        raise BusinessLogicError(
            f"Could not extract story ID from title: {title}",
            business_rule="story_id_extraction"
        )
    
    async def _handle_feature_approval(self, story_id: str, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Handle approved feature."""
        
        self.logger.info(f"Feature {story_id} approved, proceeding to deployment")
        
        action_plan = {
            "action": "deploy_to_production",
            "story_id": story_id,
            "approval_timestamp": decision["feedback_timestamp"],
            "deployment_ready": True,
            "next_feature_selection": {
                "priority_suggestion": decision.get("next_feature_priority"),
                "auto_start": True
            },
            "follow_up_actions": [
                "deploy_to_production",
                "update_feature_status_to_live",
                "schedule_post_deployment_monitoring",
                "start_next_priority_feature"
            ]
        }
        
        # Handle minor issues if present (track but don't block deployment)
        if decision.get("minor_issues"):
            action_plan["minor_issues_tracking"] = {
                "issues": decision["minor_issues"],
                "action": "create_improvement_backlog_items",
                "priority": "low"
            }
        
        return action_plan
    
    async def _handle_feature_rejection(self, story_id: str, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Handle rejected feature with comprehensive revision planning."""
        
        self.logger.info(f"Feature {story_id} rejected, creating revision plan")
        
        # Analyze feedback and create structured issues
        feedback_issues = await self._analyze_feedback_issues(decision)
        
        # Create revision plan
        revision_plan = await self._create_revision_plan(story_id, feedback_issues, decision)
        
        # Generate revision tasks
        revision_tasks = await self._generate_revision_tasks(revision_plan, feedback_issues)
        
        action_plan = {
            "action": "create_feature_revision",
            "original_story_id": story_id,
            "revision_plan": revision_plan.to_dict(),
            "revision_tasks": revision_tasks,
            "feedback_analysis": {
                "total_issues": len(feedback_issues),
                "critical_issues": len([i for i in feedback_issues if i.priority == IssuePriority.CRITICAL]),
                "categories": list(set(issue.category.value for issue in feedback_issues))
            },
            "next_actions": [
                "create_revision_story",
                "generate_revision_contracts",
                "notify_project_owner_of_revision_plan",
                "start_revision_development"
            ]
        }
        
        return action_plan
    
    async def _handle_conditional_approval(self, story_id: str, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Handle conditional approval with minor issues."""
        
        self.logger.info(f"Feature {story_id} conditionally approved with minor issues")
        
        # Deploy but track issues for future improvement
        action_plan = {
            "action": "deploy_with_issue_tracking",
            "story_id": story_id,
            "approval_timestamp": decision["feedback_timestamp"],
            "deployment_ready": True,
            "issue_tracking": {
                "minor_issues": decision.get("minor_issues", []),
                "improvement_priority": "medium",
                "schedule_improvement": "next_maintenance_cycle"
            },
            "next_actions": [
                "deploy_to_production",
                "create_improvement_backlog",
                "start_next_priority_feature",
                "schedule_improvement_planning"
            ]
        }
        
        return action_plan
    
    async def _analyze_feedback_issues(self, decision: Dict[str, Any]) -> List[FeedbackIssue]:
        """Analyze feedback and convert to structured issues."""
        
        feedback_issues = []
        
        # Process critical issues
        for critical_issue in decision.get("critical_issues", []):
            issue = await self._convert_to_feedback_issue(
                critical_issue,
                IssuePriority.CRITICAL
            )
            feedback_issues.append(issue)
        
        # Process minor issues
        for minor_issue in decision.get("minor_issues", []):
            issue = await self._convert_to_feedback_issue(
                {"description": minor_issue, "expected": "", "actual": "", "priority": "low"},
                IssuePriority.LOW
            )
            feedback_issues.append(issue)
        
        # Process failed acceptance criteria
        for failed_criterion in decision.get("acceptance_criteria_review", {}).get("failed", []):
            issue = await self._convert_to_feedback_issue(
                {
                    "description": f"Acceptance criterion not met: {failed_criterion['criterion']}",
                    "expected": "Criterion should be satisfied",
                    "actual": failed_criterion["feedback"],
                    "priority": "high"
                },
                IssuePriority.HIGH
            )
            feedback_issues.append(issue)
        
        return feedback_issues
    
    async def _convert_to_feedback_issue(
        self,
        raw_issue: Dict[str, Any],
        priority: IssuePriority
    ) -> FeedbackIssue:
        """Convert raw feedback issue to structured FeedbackIssue."""
        
        # Categorize the issue
        category = self._categorize_issue(raw_issue["description"])
        
        # Estimate effort
        effort_hours = self.effort_estimates[category][priority.value]
        
        # Determine agent assignment
        agent_assignment = self.agent_assignments[category]
        
        # Generate acceptance criteria
        acceptance_criteria = self._generate_acceptance_criteria(raw_issue, category)
        
        return FeedbackIssue(
            description=raw_issue["description"],
            category=category,
            priority=priority,
            expected_behavior=raw_issue.get("expected", ""),
            actual_behavior=raw_issue.get("actual", ""),
            acceptance_criteria=acceptance_criteria,
            estimated_effort_hours=effort_hours,
            agent_assignment=agent_assignment
        )
    
    def _categorize_issue(self, description: str) -> FeedbackCategory:
        """Categorize issue based on description keywords."""
        
        description_lower = description.lower()
        
        # Category keywords mapping
        category_keywords = {
            FeedbackCategory.DESIGN: ["design", "layout", "visual", "ui", "interface", "wireframe", "component"],
            FeedbackCategory.DEVELOPMENT: ["code", "functionality", "feature", "logic", "implementation", "bug"],
            FeedbackCategory.TESTING: ["test", "testing", "coverage", "validation", "verification"],
            FeedbackCategory.UX: ["user experience", "ux", "usability", "workflow", "navigation", "interaction"],
            FeedbackCategory.PERFORMANCE: ["performance", "speed", "load", "response time", "optimization"],
            FeedbackCategory.ACCESSIBILITY: ["accessibility", "wcag", "screen reader", "keyboard", "a11y"],
            FeedbackCategory.DNA_COMPLIANCE: ["pedagogical", "policy", "municipal", "learning", "educational"],
            FeedbackCategory.CONTENT: ["content", "text", "copy", "message", "label", "instruction"]
        }
        
        # Score each category
        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in description_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return highest scoring category or default to development
        if category_scores:
            return max(category_scores.items(), key=lambda x: x[1])[0]
        else:
            return FeedbackCategory.DEVELOPMENT
    
    def _generate_acceptance_criteria(
        self,
        raw_issue: Dict[str, Any],
        category: FeedbackCategory
    ) -> List[str]:
        """Generate acceptance criteria for the issue."""
        
        base_criteria = []
        
        if raw_issue.get("expected"):
            base_criteria.append(f"Feature behaves as expected: {raw_issue['expected']}")
        
        # Add category-specific criteria
        category_criteria = {
            FeedbackCategory.DESIGN: [
                "Visual design meets specification",
                "Layout is responsive across devices",
                "Design follows DigiNativa style guidelines"
            ],
            FeedbackCategory.DEVELOPMENT: [
                "Functionality works as specified",
                "Code follows project standards",
                "No regressions in existing features"
            ],
            FeedbackCategory.TESTING: [
                "All tests pass",
                "Coverage requirements met",
                "No critical bugs detected"
            ],
            FeedbackCategory.UX: [
                "User workflow is intuitive",
                "Anna persona can complete tasks efficiently",
                "User feedback is positive"
            ],
            FeedbackCategory.PERFORMANCE: [
                "API response time <200ms",
                "Page load time <2s",
                "Lighthouse score >90"
            ],
            FeedbackCategory.ACCESSIBILITY: [
                "WCAG AA compliance achieved",
                "Screen reader compatibility verified",
                "Keyboard navigation functional"
            ],
            FeedbackCategory.DNA_COMPLIANCE: [
                "All 5 design principles satisfied",
                "Municipal context appropriate",
                "Pedagogical value validated"
            ],
            FeedbackCategory.CONTENT: [
                "Content is clear and professional",
                "Swedish language conventions followed",
                "Municipal terminology accurate"
            ]
        }
        
        base_criteria.extend(category_criteria.get(category, []))
        
        return base_criteria[:5]  # Limit to 5 criteria per issue
    
    async def _create_revision_plan(
        self,
        original_story_id: str,
        feedback_issues: List[FeedbackIssue],
        decision: Dict[str, Any]
    ) -> RevisionPlan:
        """Create comprehensive revision plan."""
        
        # Generate revision story ID
        revision_number = await self._get_next_revision_number(original_story_id)
        revision_story_id = f"{original_story_id}-REV-{revision_number:03d}"
        
        # Create development phases
        development_phases = self._create_development_phases(feedback_issues)
        
        # Calculate timeline
        total_hours = sum(issue.estimated_effort_hours for issue in feedback_issues)
        estimated_completion = datetime.now() + timedelta(hours=total_hours)
        
        # Generate success criteria
        success_criteria = self._generate_revision_success_criteria(feedback_issues, decision)
        
        return RevisionPlan(
            story_id=revision_story_id,
            original_story_id=original_story_id,
            revision_number=revision_number,
            feedback_summary=f"Addressing {len(feedback_issues)} issues from project owner feedback",
            total_issues=len(feedback_issues),
            critical_issues=len([i for i in feedback_issues if i.priority == IssuePriority.CRITICAL]),
            development_phases=development_phases,
            estimated_total_hours=total_hours,
            estimated_completion_date=estimated_completion.isoformat(),
            success_criteria=success_criteria
        )
    
    def _create_development_phases(self, feedback_issues: List[FeedbackIssue]) -> List[Dict[str, Any]]:
        """Create development phases based on issues and dependencies."""
        
        # Group issues by agent
        agent_groups = {}
        for issue in feedback_issues:
            agent = issue.agent_assignment
            if agent not in agent_groups:
                agent_groups[agent] = []
            agent_groups[agent].append(issue)
        
        # Define phase order (based on dependencies)
        phase_order = ["project_manager", "game_designer", "developer", "test_engineer", "qa_tester"]
        
        phases = []
        for agent in phase_order:
            if agent in agent_groups:
                agent_issues = agent_groups[agent]
                total_hours = sum(issue.estimated_effort_hours for issue in agent_issues)
                
                phases.append({
                    "phase_name": f"{agent}_revision",
                    "agent": agent,
                    "issues": [issue.to_dict() for issue in agent_issues],
                    "estimated_hours": total_hours,
                    "dependencies": self._get_phase_dependencies(agent, phases)
                })
        
        return phases
    
    def _get_phase_dependencies(self, agent: str, existing_phases: List[Dict]) -> List[str]:
        """Get dependencies for agent phase."""
        
        dependencies = {
            "game_designer": ["project_manager"],
            "developer": ["game_designer"],
            "test_engineer": ["developer"], 
            "qa_tester": ["test_engineer"]
        }
        
        agent_dependencies = dependencies.get(agent, [])
        return [phase["phase_name"] for phase in existing_phases if phase["agent"] in agent_dependencies]
    
    def _generate_revision_success_criteria(
        self,
        feedback_issues: List[FeedbackIssue],
        decision: Dict[str, Any]
    ) -> List[str]:
        """Generate success criteria for revision."""
        
        criteria = [
            "All critical issues from project owner feedback are resolved",
            "All failed acceptance criteria are now met",
            "Feature quality score improves by at least 10 points",
            "No new regressions are introduced"
        ]
        
        # Add specific criteria based on feedback
        if any(issue.category == FeedbackCategory.PERFORMANCE for issue in feedback_issues):
            criteria.append("Performance metrics meet DigiNativa standards")
        
        if any(issue.category == FeedbackCategory.ACCESSIBILITY for issue in feedback_issues):
            criteria.append("WCAG AA compliance is achieved")
        
        if any(issue.category == FeedbackCategory.DNA_COMPLIANCE for issue in feedback_issues):
            criteria.append("DNA compliance score reaches >4.0/5.0")
        
        return criteria
    
    async def _generate_revision_tasks(
        self,
        revision_plan: RevisionPlan,
        feedback_issues: List[FeedbackIssue]
    ) -> List[Dict[str, Any]]:
        """Generate specific development tasks for revision."""
        
        tasks = []
        
        for phase in revision_plan.development_phases:
            for issue_data in phase["issues"]:
                task = {
                    "task_id": f"{revision_plan.story_id}-{len(tasks)+1:03d}",
                    "story_id": revision_plan.story_id,
                    "agent": phase["agent"],
                    "title": f"Fix: {issue_data['description'][:50]}...",
                    "description": issue_data["description"],
                    "acceptance_criteria": issue_data["acceptance_criteria"],
                    "priority": issue_data["priority"],
                    "estimated_hours": issue_data["estimated_effort_hours"],
                    "category": issue_data["category"],
                    "dependencies": []
                }
                
                tasks.append(task)
        
        return tasks
    
    async def _get_next_revision_number(self, original_story_id: str) -> int:
        """Get next revision number for story."""
        # This would typically query a database or file system
        # For now, return 1 as default
        return 1