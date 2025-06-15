"""
Quality Reviewer Contract Models Package.

Provides Pydantic models for type-safe Quality Reviewer agent communication.
"""

from .input_models import QualityReviewerInputContract
from .output_models import QualityReviewerOutputContract

__all__ = [
    "QualityReviewerInputContract",
    "QualityReviewerOutputContract"
]