"""
Input contract models for Project Manager Agent.

PURPOSE:
Defines the expected input contract structure for Project Manager Agent,
ensuring type safety and validation for all incoming requests.

CRITICAL IMPORTANCE:
- Enforces contract standards across the system
- Provides type safety for agent inputs
- Enables automatic validation and error detection
- Documents expected data structures
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class FeatureRequestData(BaseModel):
    """
    Feature request data structure for Project Manager input.
    
    This model defines the expected structure for feature requests
    coming from GitHub or other external sources.
    """
    
    feature_description: str = Field(
        ...,
        description="Detailed description of the requested feature",
        min_length=10,
        max_length=5000
    )
    
    acceptance_criteria: List[str] = Field(
        default=[],
        description="List of acceptance criteria for the feature"
    )
    
    user_persona: str = Field(
        default="Anna",
        description="Target user persona for the feature"
    )
    
    priority_level: str = Field(
        ...,
        description="Priority level of the feature request"
    )
    
    time_constraint_minutes: int = Field(
        default=10,
        description="Maximum time allowed for feature completion",
        ge=1,
        le=60
    )
    
    learning_objectives: List[str] = Field(
        default=[],
        description="Learning objectives that this feature should achieve"
    )
    
    gdd_section_reference: Optional[str] = Field(
        default=None,
        description="Reference to Game Design Document section"
    )
    
    github_issue_url: Optional[str] = Field(
        default=None,
        description="GitHub issue URL if applicable"
    )
    
    github_issue_number: Optional[int] = Field(
        default=None,
        description="GitHub issue number if applicable"
    )
    
    requested_by: str = Field(
        default="unknown",
        description="Person or system that requested the feature"
    )
    
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the request was created"
    )
    
    labels: List[str] = Field(
        default=[],
        description="Labels associated with the request"
    )
    
    assignees: List[str] = Field(
        default=[],
        description="People assigned to the request"
    )
    
    milestone: Optional[str] = Field(
        default=None,
        description="Milestone associated with the request"
    )
    
    @validator('priority_level')
    def validate_priority(cls, v):
        """Validate priority level."""
        valid_priorities = ["low", "medium", "high", "critical"]
        if v.lower() not in valid_priorities:
            raise ValueError(f"Priority must be one of: {valid_priorities}")
        return v.lower()
    
    @validator('user_persona')
    def validate_persona(cls, v):
        """Validate user persona."""
        valid_personas = ["Anna"]  # DigiNativa's primary persona
        if v not in valid_personas:
            # Warning but don't fail - allows for future personas
            pass
        return v
    
    @validator('acceptance_criteria')
    def validate_acceptance_criteria(cls, v):
        """Validate acceptance criteria."""
        # Remove empty criteria
        return [criterion.strip() for criterion in v if criterion.strip()]


class InputRequirements(BaseModel):
    """Input requirements for Project Manager Agent contract."""
    
    required_files: List[str] = Field(
        default=[],
        description="List of files required for processing"
    )
    
    required_data: FeatureRequestData = Field(
        ...,
        description="Feature request data"
    )
    
    required_validations: List[str] = Field(
        default=[],
        description="List of validations that must be completed"
    )


class DNAComplianceValidation(BaseModel):
    """DNA compliance validation structure."""
    
    pedagogical_value: bool = Field(
        default=True,
        description="Validates educational/learning focus"
    )
    
    policy_to_practice: bool = Field(
        default=True,
        description="Connects policy to practical application"
    )
    
    time_respect: bool = Field(
        default=True,
        description="Respects user's time (d10 minutes per feature)"
    )
    
    holistic_thinking: bool = Field(
        default=True,
        description="Considers full context and implications"
    )
    
    professional_tone: bool = Field(
        default=True,
        description="Appropriate for public sector professionals"
    )


class ArchitectureCompliance(BaseModel):
    """Architecture compliance validation structure."""
    
    api_first: bool = Field(
        default=True,
        description="All communication via REST APIs"
    )
    
    stateless_backend: bool = Field(
        default=True,
        description="No server-side sessions, all state from client"
    )
    
    separation_of_concerns: bool = Field(
        default=True,
        description="Frontend and backend completely separate"
    )
    
    simplicity_first: bool = Field(
        default=True,
        description="Choose simplest solution that works"
    )


class DNACompliance(BaseModel):
    """DNA compliance structure for contract."""
    
    design_principles_validation: DNAComplianceValidation = Field(
        default_factory=DNAComplianceValidation,
        description="Design principles validation"
    )
    
    architecture_compliance: ArchitectureCompliance = Field(
        default_factory=ArchitectureCompliance,
        description="Architecture compliance validation"
    )


class ProjectManagerInputContract(BaseModel):
    """
    Complete input contract structure for Project Manager Agent.
    
    This model defines the full contract structure that the Project Manager
    Agent expects to receive when processing feature requests.
    """
    
    contract_version: str = Field(
        default="1.0",
        description="Version of the contract format"
    )
    
    story_id: str = Field(
        ...,
        description="Unique identifier for the story",
        regex=r"^STORY-[A-Za-z0-9-]+-\d+$"
    )
    
    source_agent: str = Field(
        default="github",
        description="Agent that created this contract"
    )
    
    target_agent: str = Field(
        default="project_manager",
        description="Agent that should process this contract"
    )
    
    dna_compliance: DNACompliance = Field(
        default_factory=DNACompliance,
        description="DNA compliance validation"
    )
    
    input_requirements: InputRequirements = Field(
        ...,
        description="Input requirements for processing"
    )
    
    output_specifications: Dict[str, Any] = Field(
        default={},
        description="Expected output specifications"
    )
    
    quality_gates: List[str] = Field(
        default=[],
        description="Quality gates that must pass"
    )
    
    handoff_criteria: List[str] = Field(
        default=[],
        description="Criteria for successful handoff"
    )
    
    @validator('source_agent')
    def validate_source_agent(cls, v):
        """Validate source agent."""
        valid_sources = ["github", "project_manager", "game_designer", "developer", 
                        "test_engineer", "qa_tester", "quality_reviewer"]
        if v not in valid_sources:
            raise ValueError(f"Invalid source agent: {v}")
        return v
    
    @validator('target_agent')
    def validate_target_agent(cls, v):
        """Validate target agent."""
        if v != "project_manager":
            raise ValueError("Project Manager can only be target agent for its input contracts")
        return v
    
    class Config:
        """Pydantic configuration."""
        extra = "forbid"  # Don't allow extra fields
        validate_assignment = True  # Validate on assignment
        use_enum_values = True


class GitHubIssueData(BaseModel):
    """
    GitHub issue data model for direct GitHub integration.
    
    This model structures GitHub issue data for processing
    by the Project Manager Agent.
    """
    
    number: int = Field(
        ...,
        description="GitHub issue number"
    )
    
    title: str = Field(
        ...,
        description="GitHub issue title"
    )
    
    body: str = Field(
        default="",
        description="GitHub issue body/description"
    )
    
    state: str = Field(
        default="open",
        description="GitHub issue state"
    )
    
    labels: List[Dict[str, Any]] = Field(
        default=[],
        description="GitHub issue labels"
    )
    
    assignees: List[Dict[str, Any]] = Field(
        default=[],
        description="GitHub issue assignees"
    )
    
    milestone: Optional[Dict[str, Any]] = Field(
        default=None,
        description="GitHub issue milestone"
    )
    
    user: Dict[str, Any] = Field(
        default={},
        description="GitHub user who created the issue"
    )
    
    created_at: str = Field(
        ...,
        description="Timestamp when issue was created"
    )
    
    updated_at: str = Field(
        ...,
        description="Timestamp when issue was last updated"
    )
    
    html_url: str = Field(
        ...,
        description="GitHub issue URL"
    )
    
    comments_data: List[Dict[str, Any]] = Field(
        default=[],
        description="GitHub issue comments"
    )
    
    @validator('state')
    def validate_state(cls, v):
        """Validate GitHub issue state."""
        valid_states = ["open", "closed"]
        if v not in valid_states:
            raise ValueError(f"Invalid issue state: {v}")
        return v


# Utility functions for contract creation

def create_github_contract(issue_data: GitHubIssueData) -> ProjectManagerInputContract:
    """
    Create a Project Manager input contract from GitHub issue data.
    
    Args:
        issue_data: GitHub issue data
        
    Returns:
        Project Manager input contract
    """
    # Extract feature request data from GitHub issue
    feature_data = FeatureRequestData(
        feature_description=f"{issue_data.title}\n\n{issue_data.body}",
        github_issue_url=issue_data.html_url,
        github_issue_number=issue_data.number,
        requested_by=issue_data.user.get("login", "unknown"),
        created_at=issue_data.created_at,
        labels=[label.get("name", "") for label in issue_data.labels],
        assignees=[assignee.get("login", "") for assignee in issue_data.assignees],
        milestone=issue_data.milestone.get("title") if issue_data.milestone else None
    )
    
    # Generate story ID
    story_id = f"STORY-GH-{issue_data.number}"
    
    # Create input requirements
    input_requirements = InputRequirements(
        required_files=[],
        required_data=feature_data,
        required_validations=[
            "github_issue_valid",
            "feature_request_format_correct"
        ]
    )
    
    # Create contract
    contract = ProjectManagerInputContract(
        story_id=story_id,
        source_agent="github",
        target_agent="project_manager",
        input_requirements=input_requirements,
        quality_gates=[
            "github_issue_parsed_correctly",
            "feature_request_data_complete"
        ],
        handoff_criteria=[
            "all_required_data_extracted",
            "issue_format_validated"
        ]
    )
    
    return contract


def create_manual_contract(
    story_id: str,
    feature_description: str,
    priority_level: str = "medium",
    **kwargs
) -> ProjectManagerInputContract:
    """
    Create a Project Manager input contract manually.
    
    Args:
        story_id: Story identifier
        feature_description: Feature description
        priority_level: Priority level
        **kwargs: Additional feature data fields
        
    Returns:
        Project Manager input contract
    """
    # Create feature request data
    feature_data = FeatureRequestData(
        feature_description=feature_description,
        priority_level=priority_level,
        **kwargs
    )
    
    # Create input requirements
    input_requirements = InputRequirements(
        required_data=feature_data,
        required_validations=[
            "manual_request_validated",
            "feature_description_complete"
        ]
    )
    
    # Create contract
    contract = ProjectManagerInputContract(
        story_id=story_id,
        source_agent="github",  # Or other source
        target_agent="project_manager",
        input_requirements=input_requirements,
        quality_gates=[
            "feature_request_data_complete",
            "manual_validation_passed"
        ],
        handoff_criteria=[
            "all_required_data_provided",
            "feature_scope_clear"
        ]
    )
    
    return contract