"""
EventBus - Agent coordination system for DigiNativa AI Team.

PURPOSE:
Enables loose coupling between agents by providing centralized
communication hub for workflow management and agent handoffs.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

from .exceptions import EventBusError, WorkflowError


logger = logging.getLogger(__name__)


class WorkPriority(Enum):
    """Work priority levels."""
    CRITICAL = 1
    HIGH = 2 
    MEDIUM = 3
    LOW = 4


class WorkStatus(Enum):
    """Work status tracking."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkItem:
    """Represents a unit of work in the agent workflow."""
    work_id: str
    story_id: str
    source_agent: str
    target_agent: str
    contract: Dict[str, Any]
    priority: WorkPriority
    status: WorkStatus
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "work_id": self.work_id,
            "story_id": self.story_id,
            "source_agent": self.source_agent,
            "target_agent": self.target_agent,
            "contract": self.contract,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries
        }


@dataclass 
class AgentRegistry:
    """Registry entry for an available agent."""
    agent_id: str
    agent_type: str
    status: str  # 'available', 'busy', 'offline'
    current_work_id: Optional[str] = None
    capabilities: Optional[set] = None
    last_heartbeat: Optional[str] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = set()


class EventBus:
    """
    Central coordination system for AI agent communication.
    
    Enables loose coupling between agents via standardized contracts.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the EventBus."""
        self.config = config or {}
        self.logger = logging.getLogger(f"{__name__}.EventBus")
        
        # Work management
        self.work_queue: List[WorkItem] = []
        self.active_work: Dict[str, WorkItem] = {}
        self.completed_work: Dict[str, WorkItem] = {}
        
        # Agent registry
        self.agents: Dict[str, AgentRegistry] = {}
        self.agent_types: Dict[str, List[str]] = {}
        
        # Configuration
        self.max_concurrent_work = self.config.get("max_concurrent_work", 10)
        self.work_timeout_minutes = self.config.get("work_timeout_minutes", 60)
        
        # DigiNativa agent sequences
        self.valid_agent_sequences = {
            "project_manager": ["game_designer"],
            "game_designer": ["developer"],
            "developer": ["test_engineer"],
            "test_engineer": ["qa_tester"],
            "qa_tester": ["quality_reviewer"],
            "quality_reviewer": ["project_manager"]
        }
        
        self.logger.info("EventBus initialized")
    
    async def register_agent(self, agent_id: str, agent_type: str, 
                           capabilities: Optional[set] = None) -> bool:
        """Register an agent with the EventBus."""
        try:
            # Validate agent type
            valid_types = set(self.valid_agent_sequences.keys()) | {"quality_reviewer"}
            if agent_type not in valid_types:
                raise EventBusError(f"Invalid agent_type: {agent_type}")
            
            # Create registry entry
            registry = AgentRegistry(
                agent_id=agent_id,
                agent_type=agent_type,
                status="available",
                capabilities=capabilities or set(),
                last_heartbeat=datetime.now().isoformat()
            )
            
            # Register
            self.agents[agent_id] = registry
            
            if agent_type not in self.agent_types:
                self.agent_types[agent_type] = []
            
            if agent_id not in self.agent_types[agent_type]:
                self.agent_types[agent_type].append(agent_id)
            
            self.logger.info(f"Agent registered: {agent_id} ({agent_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {e}")
            raise EventBusError(f"Agent registration failed: {e}")
    
    async def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        try:
            if agent_id not in self.agents:
                return False
            
            agent_registry = self.agents[agent_id]
            agent_type = agent_registry.agent_type
            
            # Cancel active work if any
            if agent_registry.current_work_id:
                await self._cancel_work(agent_registry.current_work_id, "Agent unregistered")
            
            # Remove from registries
            del self.agents[agent_id]
            
            if agent_type in self.agent_types and agent_id in self.agent_types[agent_type]:
                self.agent_types[agent_type].remove(agent_id)
                if not self.agent_types[agent_type]:
                    del self.agent_types[agent_type]
            
            self.logger.info(f"Agent unregistered: {agent_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False
    
    async def delegate_to_agent(self, target_agent_type: str, contract: Dict[str, Any], 
                              priority: WorkPriority = WorkPriority.MEDIUM) -> str:
        """Delegate work to an agent via contract."""
        try:
            # Generate work ID
            work_id = f"WORK-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(self.work_queue):03d}"
            
            # Extract contract info
            story_id = contract.get("story_id", "unknown")
            source_agent = contract.get("source_agent", "system")
            
            # Validate target agent type exists
            if target_agent_type not in self.agent_types:
                raise EventBusError(f"No agents available for type: {target_agent_type}")
            
            # Validate agent sequence
            if source_agent != "system":
                if source_agent not in self.valid_agent_sequences:
                    raise EventBusError(f"Invalid source agent: {source_agent}")
                
                valid_targets = self.valid_agent_sequences[source_agent]
                if target_agent_type not in valid_targets:
                    raise EventBusError(f"Invalid sequence: {source_agent} -> {target_agent_type}")
            
            # Create work item
            work_item = WorkItem(
                work_id=work_id,
                story_id=story_id,
                source_agent=source_agent,
                target_agent=target_agent_type,
                contract=contract,
                priority=priority,
                status=WorkStatus.PENDING,
                created_at=datetime.now().isoformat()
            )
            
            # Add to queue in priority order
            await self._enqueue_work(work_item)
            
            self.logger.info(f"Work delegated: {work_id} -> {target_agent_type}")
            return work_id
            
        except Exception as e:
            self.logger.error(f"Failed to delegate work: {e}")
            if isinstance(e, EventBusError):
                raise
            else:
                raise EventBusError(f"Work delegation failed: {e}")
    
    async def get_work_status(self, work_id: str) -> Optional[Dict[str, Any]]:
        """Get status of work item."""
        # Check active work
        if work_id in self.active_work:
            return self.active_work[work_id].to_dict()
        
        # Check completed work
        if work_id in self.completed_work:
            return self.completed_work[work_id].to_dict()
        
        # Check queued work
        for work_item in self.work_queue:
            if work_item.work_id == work_id:
                return work_item.to_dict()
        
        return None
    
    async def cancel_work(self, work_id: str, reason: str = "Cancelled") -> bool:
        """Cancel work."""
        return await self._cancel_work(work_id, reason)
    
    async def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status."""
        return {
            "pending_work": len(self.work_queue),
            "active_work": len(self.active_work),
            "completed_work": len(self.completed_work),
            "registered_agents": len(self.agents),
            "available_agents": len([a for a in self.agents.values() if a.status == "available"]),
            "busy_agents": len([a for a in self.agents.values() if a.status == "busy"]),
            "offline_agents": len([a for a in self.agents.values() if a.status == "offline"]),
            "agent_types": {k: len(v) for k, v in self.agent_types.items()}
        }
    
    async def publish(self, event_type: str, event_data: Dict[str, Any], 
                     agent_id: Optional[str] = None) -> None:
        """
        Publish event for team monitoring and coordination.
        
        Args:
            event_type: Type of event (e.g., 'work_started', 'work_completed', 'error')
            event_data: Event payload data
            agent_id: Optional agent ID that triggered the event
        """
        try:
            event = {
                "event_type": event_type,
                "event_data": event_data,
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat(),
                "event_id": f"EVENT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{len(self.completed_work):03d}"
            }
            
            # Log event for monitoring
            self.logger.info(f"Event published: {event_type} from {agent_id or 'system'}")
            self.logger.debug(f"Event details: {event}")
            
            # In a full implementation, this would publish to message queues,
            # webhooks, or other monitoring systems
            # For now, we log for monitoring purposes
            
        except Exception as e:
            self.logger.error(f"Failed to publish event {event_type}: {e}")
            # Don't raise - event publishing should not break workflows
    
    # Private methods
    
    async def _enqueue_work(self, work_item: WorkItem) -> None:
        """Add work to priority queue."""
        # Insert in priority order
        inserted = False
        for i, existing_work in enumerate(self.work_queue):
            if work_item.priority.value < existing_work.priority.value:
                self.work_queue.insert(i, work_item)
                inserted = True
                break
        
        if not inserted:
            self.work_queue.append(work_item)
        
        self.logger.debug(f"Work enqueued: {work_item.work_id}")
    
    async def _cancel_work(self, work_id: str, reason: str) -> bool:
        """Cancel work with reason."""
        # Check queued work
        for i, work_item in enumerate(self.work_queue):
            if work_item.work_id == work_id:
                work_item.status = WorkStatus.CANCELLED
                work_item.error_message = reason
                work_item.completed_at = datetime.now().isoformat()
                
                self.work_queue.pop(i)
                self.completed_work[work_id] = work_item
                
                self.logger.info(f"Queued work cancelled: {work_id}")
                return True
        
        # Check active work
        if work_id in self.active_work:
            work_item = self.active_work[work_id]
            work_item.status = WorkStatus.CANCELLED
            work_item.error_message = reason
            work_item.completed_at = datetime.now().isoformat()
            
            del self.active_work[work_id]
            self.completed_work[work_id] = work_item
            
            # Free up agent
            for agent in self.agents.values():
                if agent.current_work_id == work_id:
                    agent.status = "available"
                    agent.current_work_id = None
                    break
            
            self.logger.info(f"Active work cancelled: {work_id}")
            return True
        
        return False


# Utility functions

def create_eventbus_config(
    max_concurrent_work: int = 10,
    work_timeout_minutes: int = 60
) -> Dict[str, Any]:
    """Create EventBus configuration."""
    return {
        "max_concurrent_work": max_concurrent_work,
        "work_timeout_minutes": work_timeout_minutes
    }


async def create_work_contract(
    story_id: str,
    source_agent: str,
    target_agent: str,
    work_data: Dict[str, Any],
    dna_compliance: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create standardized work contract."""
    if dna_compliance is None:
        dna_compliance = {
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
    
    return {
        "contract_version": "1.0",
        "story_id": story_id,
        "source_agent": source_agent,
        "target_agent": target_agent,
        "dna_compliance": dna_compliance,
        "input_requirements": {
            "required_files": [],
            "required_data": work_data,
            "required_validations": []
        },
        "output_specifications": {
            "deliverable_files": [],
            "deliverable_data": {},
            "validation_criteria": {}
        },
        "quality_gates": [],
        "handoff_criteria": []
    }