"""
Priority Queue Manager for Project Manager Agent.

PURPOSE:
Manages feature priority queue, dependency resolution, and automatic
next feature selection based on project owner preferences and system constraints.

CRITICAL IMPORTANCE:
- Ensures continuous development flow
- Respects project owner priorities and dependencies
- Optimizes team utilization and delivery velocity
- Prevents development bottlenecks from dependency blocking

REVENUE IMPACT:
Direct impact on revenue through:
- Faster feature delivery through optimized prioritization
- Reduced idle time between features
- Better resource utilization across AI team
- Automatic adaptation to changing business priorities
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum

from ....shared.exceptions import BusinessLogicError


class FeatureStatus(Enum):
    """Feature development status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    REJECTED = "rejected"
    REVISION = "revision"


class PriorityLevel(Enum):
    """Feature priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class FeatureDependency:
    """Represents a dependency between features."""
    dependent_story_id: str
    dependency_story_id: str
    dependency_type: str  # "blocks", "requires", "enhances"
    is_blocking: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "dependent_story_id": self.dependent_story_id,
            "dependency_story_id": self.dependency_story_id,
            "dependency_type": self.dependency_type,
            "is_blocking": self.is_blocking
        }


@dataclass
class QueuedFeature:
    """Represents a feature in the priority queue."""
    story_id: str
    title: str
    description: str
    priority: PriorityLevel
    status: FeatureStatus
    created_at: datetime
    estimated_hours: float
    acceptance_criteria: List[str]
    dependencies: List[FeatureDependency] = field(default_factory=list)
    assigned_agent: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "story_id": self.story_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "estimated_hours": self.estimated_hours,
            "acceptance_criteria": self.acceptance_criteria,
            "dependencies": [dep.to_dict() for dep in self.dependencies],
            "assigned_agent": self.assigned_agent,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata
        }


class PriorityQueueManager:
    """
    Manages feature priority queue with dependency resolution.
    
    Handles automatic next feature selection, dependency checking,
    and queue optimization for continuous development flow.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize priority queue manager.
        
        Args:
            config: Configuration dictionary
        """
        self.logger = logging.getLogger(f"{__name__}.PriorityQueueManager")
        self.config = config or {}
        
        # In-memory queue storage (in production, this would use a database)
        self.feature_queue: List[QueuedFeature] = []
        self.dependencies: Dict[str, List[FeatureDependency]] = {}
        
        # Priority weights for sorting
        self.priority_weights = {
            PriorityLevel.CRITICAL: 0,
            PriorityLevel.HIGH: 1,
            PriorityLevel.MEDIUM: 2,
            PriorityLevel.LOW: 3
        }
        
        # Configuration
        self.max_concurrent_features = self.config.get("max_concurrent_features", 1)
        self.dependency_timeout_hours = self.config.get("dependency_timeout_hours", 168)  # 1 week
        
        self.logger.info("Priority queue manager initialized")
    
    async def add_feature_to_queue(
        self,
        story_id: str,
        title: str,
        description: str,
        priority: str,
        acceptance_criteria: List[str],
        estimated_hours: float = 40.0,
        dependencies: Optional[List[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> QueuedFeature:
        """
        Add new feature to priority queue.
        
        Args:
            story_id: Unique story identifier
            title: Feature title
            description: Feature description
            priority: Priority level (critical, high, medium, low)
            acceptance_criteria: List of acceptance criteria
            estimated_hours: Estimated development hours
            dependencies: List of dependency specifications
            metadata: Additional feature metadata
            
        Returns:
            Created QueuedFeature instance
        """
        try:
            # Parse priority
            priority_enum = PriorityLevel(priority.lower())
            
            # Parse dependencies
            feature_dependencies = []
            if dependencies:
                for dep in dependencies:
                    feature_dependencies.append(FeatureDependency(
                        dependent_story_id=story_id,
                        dependency_story_id=dep["dependency_story_id"],
                        dependency_type=dep.get("dependency_type", "blocks"),
                        is_blocking=dep.get("is_blocking", True)
                    ))
            
            # Create queued feature
            queued_feature = QueuedFeature(
                story_id=story_id,
                title=title,
                description=description,
                priority=priority_enum,
                status=FeatureStatus.PENDING,
                created_at=datetime.now(),
                estimated_hours=estimated_hours,
                acceptance_criteria=acceptance_criteria,
                dependencies=feature_dependencies,
                metadata=metadata or {}
            )
            
            # Add to queue
            self.feature_queue.append(queued_feature)
            
            # Update dependencies mapping
            if feature_dependencies:
                self.dependencies[story_id] = feature_dependencies
            
            # Re-sort queue
            await self._sort_queue()
            
            self.logger.info(f"Added feature {story_id} to queue with priority {priority}")
            return queued_feature
            
        except ValueError as e:
            raise BusinessLogicError(
                f"Invalid priority level: {priority}",
                business_rule="priority_validation",
                context={"story_id": story_id, "priority": priority}
            )
        except Exception as e:
            raise BusinessLogicError(
                f"Failed to add feature to queue: {e}",
                business_rule="queue_management",
                context={"story_id": story_id}
            )
    
    async def get_next_available_feature(
        self,
        suggested_priority: Optional[str] = None
    ) -> Optional[QueuedFeature]:
        """
        Get next available feature for development.
        
        Args:
            suggested_priority: Optional story ID suggested by project owner
            
        Returns:
            Next available feature or None if no features available
        """
        try:
            # Filter available features (pending status, no blocking dependencies)
            available_features = await self._get_available_features()
            
            if not available_features:
                self.logger.info("No features available for development")
                return None
            
            # Consider project owner suggestion
            if suggested_priority:
                suggested_feature = self._find_feature_by_id(suggested_priority)
                if suggested_feature and suggested_feature in available_features:
                    self.logger.info(f"Using project owner suggested feature: {suggested_priority}")
                    return suggested_feature
            
            # Return highest priority available feature
            next_feature = available_features[0]
            self.logger.info(f"Selected next feature: {next_feature.story_id}")
            return next_feature
            
        except Exception as e:
            raise BusinessLogicError(
                f"Failed to get next available feature: {e}",
                business_rule="feature_selection"
            )
    
    async def start_feature_development(self, story_id: str, agent: str) -> bool:
        """
        Mark feature as started and assign to agent.
        
        Args:
            story_id: Story ID to start
            agent: Agent assigned to work on feature
            
        Returns:
            True if successfully started, False otherwise
        """
        try:
            feature = self._find_feature_by_id(story_id)
            if not feature:
                raise BusinessLogicError(
                    f"Feature not found in queue: {story_id}",
                    business_rule="feature_existence"
                )
            
            if feature.status != FeatureStatus.PENDING:
                raise BusinessLogicError(
                    f"Feature {story_id} is not in pending status: {feature.status.value}",
                    business_rule="feature_status_transition"
                )
            
            # Check if we can start more features
            in_progress_count = len([f for f in self.feature_queue if f.status == FeatureStatus.IN_PROGRESS])
            if in_progress_count >= self.max_concurrent_features:
                self.logger.warning(f"Maximum concurrent features ({self.max_concurrent_features}) reached")
                return False
            
            # Start the feature
            feature.status = FeatureStatus.IN_PROGRESS
            feature.assigned_agent = agent
            feature.started_at = datetime.now()
            
            self.logger.info(f"Started feature {story_id} with agent {agent}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start feature {story_id}: {e}")
            return False
    
    async def complete_feature(self, story_id: str) -> bool:
        """
        Mark feature as completed.
        
        Args:
            story_id: Story ID to complete
            
        Returns:
            True if successfully completed, False otherwise
        """
        try:
            feature = self._find_feature_by_id(story_id)
            if not feature:
                return False
            
            feature.status = FeatureStatus.COMPLETED
            feature.completed_at = datetime.now()
            
            # Check if this completion unblocks other features
            await self._check_unblocked_features(story_id)
            
            self.logger.info(f"Completed feature {story_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to complete feature {story_id}: {e}")
            return False
    
    async def update_feature_priority(
        self,
        story_id: str,
        new_priority: str,
        reason: Optional[str] = None
    ) -> bool:
        """
        Update feature priority and re-sort queue.
        
        Args:
            story_id: Story ID to update
            new_priority: New priority level
            reason: Optional reason for priority change
            
        Returns:
            True if successfully updated, False otherwise
        """
        try:
            feature = self._find_feature_by_id(story_id)
            if not feature:
                return False
            
            old_priority = feature.priority
            feature.priority = PriorityLevel(new_priority.lower())
            
            # Add to metadata
            feature.metadata["priority_changes"] = feature.metadata.get("priority_changes", [])
            feature.metadata["priority_changes"].append({
                "from": old_priority.value,
                "to": new_priority,
                "timestamp": datetime.now().isoformat(),
                "reason": reason
            })
            
            # Re-sort queue
            await self._sort_queue()
            
            self.logger.info(f"Updated priority for {story_id}: {old_priority.value} -> {new_priority}")
            return True
            
        except ValueError:
            self.logger.error(f"Invalid priority level: {new_priority}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to update priority for {story_id}: {e}")
            return False
    
    async def add_feature_dependency(
        self,
        dependent_story_id: str,
        dependency_story_id: str,
        dependency_type: str = "blocks",
        is_blocking: bool = True
    ) -> bool:
        """
        Add dependency between features.
        
        Args:
            dependent_story_id: Feature that depends on another
            dependency_story_id: Feature that is depended upon
            dependency_type: Type of dependency
            is_blocking: Whether this dependency blocks development
            
        Returns:
            True if successfully added, False otherwise
        """
        try:
            # Validate both features exist
            dependent_feature = self._find_feature_by_id(dependent_story_id)
            dependency_feature = self._find_feature_by_id(dependency_story_id)
            
            if not dependent_feature or not dependency_feature:
                return False
            
            # Check for circular dependencies
            if await self._would_create_circular_dependency(dependent_story_id, dependency_story_id):
                self.logger.warning(f"Circular dependency detected: {dependent_story_id} -> {dependency_story_id}")
                return False
            
            # Create dependency
            dependency = FeatureDependency(
                dependent_story_id=dependent_story_id,
                dependency_story_id=dependency_story_id,
                dependency_type=dependency_type,
                is_blocking=is_blocking
            )
            
            # Add to feature and mapping
            dependent_feature.dependencies.append(dependency)
            
            if dependent_story_id not in self.dependencies:
                self.dependencies[dependent_story_id] = []
            self.dependencies[dependent_story_id].append(dependency)
            
            self.logger.info(f"Added dependency: {dependent_story_id} depends on {dependency_story_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add dependency: {e}")
            return False
    
    async def get_queue_status(self) -> Dict[str, Any]:
        """
        Get current queue status and statistics.
        
        Returns:
            Queue status dictionary
        """
        status_counts = {}
        priority_counts = {}
        
        for feature in self.feature_queue:
            # Count by status
            status = feature.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
            
            # Count by priority
            priority = feature.priority.value
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Calculate average wait time for pending features
        pending_features = [f for f in self.feature_queue if f.status == FeatureStatus.PENDING]
        avg_wait_time = 0
        if pending_features:
            total_wait = sum((datetime.now() - f.created_at).total_seconds() / 3600 for f in pending_features)
            avg_wait_time = total_wait / len(pending_features)
        
        # Identify blocked features
        blocked_features = await self._get_blocked_features()
        
        return {
            "total_features": len(self.feature_queue),
            "status_breakdown": status_counts,
            "priority_breakdown": priority_counts,
            "average_wait_time_hours": round(avg_wait_time, 2),
            "blocked_features_count": len(blocked_features),
            "blocked_features": [f.story_id for f in blocked_features],
            "next_available": await self.get_next_available_feature(),
            "queue_health": self._assess_queue_health()
        }
    
    async def _get_available_features(self) -> List[QueuedFeature]:
        """Get features available for development (no blocking dependencies)."""
        
        available = []
        
        for feature in self.feature_queue:
            if feature.status != FeatureStatus.PENDING:
                continue
            
            # Check if all blocking dependencies are satisfied
            blocking_dependencies = [
                dep for dep in feature.dependencies 
                if dep.is_blocking
            ]
            
            dependencies_satisfied = True
            for dep in blocking_dependencies:
                dep_feature = self._find_feature_by_id(dep.dependency_story_id)
                if not dep_feature or dep_feature.status != FeatureStatus.COMPLETED:
                    dependencies_satisfied = False
                    break
            
            if dependencies_satisfied:
                available.append(feature)
        
        # Sort available features by priority and creation time
        available.sort(key=lambda f: (
            self.priority_weights[f.priority],
            f.created_at
        ))
        
        return available
    
    async def _get_blocked_features(self) -> List[QueuedFeature]:
        """Get features that are blocked by dependencies."""
        
        blocked = []
        
        for feature in self.feature_queue:
            if feature.status != FeatureStatus.PENDING:
                continue
            
            # Check for unsatisfied blocking dependencies
            for dep in feature.dependencies:
                if not dep.is_blocking:
                    continue
                
                dep_feature = self._find_feature_by_id(dep.dependency_story_id)
                if not dep_feature or dep_feature.status != FeatureStatus.COMPLETED:
                    blocked.append(feature)
                    break
        
        return blocked
    
    async def _sort_queue(self) -> None:
        """Sort queue by priority and creation time."""
        
        self.feature_queue.sort(key=lambda f: (
            self.priority_weights[f.priority],
            f.created_at
        ))
    
    async def _check_unblocked_features(self, completed_story_id: str) -> None:
        """Check if completing a feature unblocks others."""
        
        # Find features that depend on the completed feature
        for feature in self.feature_queue:
            if feature.status != FeatureStatus.PENDING:
                continue
            
            for dep in feature.dependencies:
                if dep.dependency_story_id == completed_story_id:
                    self.logger.info(f"Feature {completed_story_id} completion may unblock {feature.story_id}")
    
    async def _would_create_circular_dependency(
        self,
        dependent_id: str,
        dependency_id: str
    ) -> bool:
        """Check if adding dependency would create circular dependency."""
        
        # Simple cycle detection using DFS
        visited = set()
        
        def has_path(from_id: str, to_id: str) -> bool:
            if from_id == to_id:
                return True
            
            if from_id in visited:
                return False
            
            visited.add(from_id)
            
            # Check all dependencies of from_id
            for dep in self.dependencies.get(from_id, []):
                if has_path(dep.dependency_story_id, to_id):
                    return True
            
            return False
        
        # Check if dependency_id already has path to dependent_id
        return has_path(dependency_id, dependent_id)
    
    def _find_feature_by_id(self, story_id: str) -> Optional[QueuedFeature]:
        """Find feature in queue by story ID."""
        
        for feature in self.feature_queue:
            if feature.story_id == story_id:
                return feature
        
        return None
    
    def _assess_queue_health(self) -> Dict[str, Any]:
        """Assess overall queue health and identify issues."""
        
        health = {
            "status": "healthy",
            "issues": [],
            "recommendations": []
        }
        
        # Check for too many blocked features
        blocked_count = len([f for f in self.feature_queue if f.status == FeatureStatus.BLOCKED])
        total_pending = len([f for f in self.feature_queue if f.status == FeatureStatus.PENDING])
        
        if total_pending > 0 and blocked_count / total_pending > 0.3:
            health["status"] = "degraded"
            health["issues"].append("High percentage of blocked features")
            health["recommendations"].append("Review and resolve dependency issues")
        
        # Check for stale dependencies
        now = datetime.now()
        stale_dependencies = []
        
        for feature in self.feature_queue:
            for dep in feature.dependencies:
                dep_feature = self._find_feature_by_id(dep.dependency_story_id)
                if dep_feature and dep_feature.status == FeatureStatus.IN_PROGRESS:
                    if dep_feature.started_at:
                        hours_in_progress = (now - dep_feature.started_at).total_seconds() / 3600
                        if hours_in_progress > self.dependency_timeout_hours:
                            stale_dependencies.append(dep.dependency_story_id)
        
        if stale_dependencies:
            health["status"] = "degraded"
            health["issues"].append(f"Stale dependencies: {stale_dependencies}")
            health["recommendations"].append("Review long-running dependency features")
        
        return health