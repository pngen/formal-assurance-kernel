"""
FAK - Formal Assurance Kernel

Core modules for formal verification of governance stack components.
"""

from .types import (
    ExecutionTrace,
    CapabilityManifest,
    CostLedger,
    PolicyIR,
    InvariantSpec,
    CounterExample,
    ProofWitness,
    ProofBundle,
    compute_content_hash,
    ProofType
)

from .dsl import InvariantDSL
from .engine import ProofEngine
from .verifier import Verifier
from .artifacts import ArtifactManager

__all__ = [
    'ExecutionTrace',
    'CapabilityManifest',
    'CostLedger',
    'PolicyIR',
    'InvariantSpec',
    'CounterExample',
    'ProofWitness',
    'ProofBundle',
    'compute_content_hash',
    'ProofType',
    'InvariantDSL',
    'ProofEngine',
    'Verifier',
    'ArtifactManager'
]