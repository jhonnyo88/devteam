"""
QA Tester Agent Contract Models

PURPOSE:
Provides complete Pydantic contract models for QA Tester agent
ensuring type-safe communication with Test Engineer and Quality Reviewer.

EXPORTS:
- QATesterInputContract: Input from Test Engineer
- QATesterOutputContract: Output to Quality Reviewer  
- Utility functions for contract parsing and creation

CONTRACT PROTECTION:
These models enforce DigiNativa's contract system for modular architecture.
"""

from .input_models import (
    QATesterInputContract,
    parse_qa_tester_input_contract
)

from .output_models import (
    QATesterOutputContract,
    create_qa_tester_output_contract
)

__all__ = [
    "QATesterInputContract",
    "QATesterOutputContract", 
    "parse_qa_tester_input_contract",
    "create_qa_tester_output_contract"
]