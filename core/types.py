"""
Core data types for FAK.
"""

from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import json


class ProofType(Enum):
    """Types of proofs supported by FAK."""
    BEHAVIORAL_SOUNDNESS = "behavioral_soundness"
    AUTHORITY_NON_ESCALATION = "authority_non_escalation"
    ECONOMIC_INVARIANCE = "economic_invariance"
    SEMANTIC_PRESERVATION = "semantic_preservation"


@dataclass
class ExecutionTrace:
    """Immutable execution trace from DIO."""
    id: str  # content-addressable hash
    steps: List[Dict[str, Any]]
    metadata: Dict[str, Any]

    def __post_init__(self):
        if not self.id:
            raise ValueError("ExecutionTrace must have a valid ID")
        if not isinstance(self.steps, list):
            raise ValueError("ExecutionTrace steps must be a list")
        MAX_TRACE_STEPS = 100000
        if len(self.steps) > MAX_TRACE_STEPS:
            raise ValueError(f"ExecutionTrace exceeds max steps: {MAX_TRACE_STEPS}")


@dataclass
class CapabilityManifest:
    """Capability manifest from ZT-AAS."""
    id: str  # content-addressable hash
    agent_id: str
    capabilities: List[str]
    authority_graph: Dict[str, List[str]]  # adjacency list
    metadata: Dict[str, Any]

    def __post_init__(self):
        if not self.id:
            raise ValueError("CapabilityManifest must have a valid ID")
        if not isinstance(self.capabilities, list):
            raise ValueError("CapabilityManifest capabilities must be a list")
        if not isinstance(self.authority_graph, dict):
            raise ValueError("CapabilityManifest authority_graph must be a dict")


@dataclass
class CostLedger:
    """Cost ledger from ICAE."""
    id: str  # content-addressable hash
    entries: List[Dict[str, Any]]
    total_cost: float
    metadata: Dict[str, Any]

    def __post_init__(self):
        if not self.id:
            raise ValueError("CostLedger must have a valid ID")
        if not isinstance(self.entries, list):
            raise ValueError("CostLedger entries must be a list")
        if self.total_cost < 0:
            raise ValueError("CostLedger total_cost cannot be negative")


@dataclass
class PolicyIR:
    """Policy IR from POC."""
    id: str  # content-addressable hash
    ast: Dict[str, Any]
    compiled_enforcement: bytes
    metadata: Dict[str, Any]

    def __post_init__(self):
        if not self.id:
            raise ValueError("PolicyIR must have a valid ID")
        if not isinstance(self.ast, dict):
            raise ValueError("PolicyIR AST must be a dict")


@dataclass
class InvariantSpec:
    """Invariant specification in DSL."""
    name: str
    description: str
    precondition: Optional[str]  # temporal logic formula
    postcondition: Optional[str]  # temporal logic formula
    temporal_properties: List[str]  # e.g., ["always", "eventually"]
    invariant_type: ProofType

    def __post_init__(self):
        if not self.name:
            raise ValueError("InvariantSpec must have a name")
        if not isinstance(self.temporal_properties, list):
            raise ValueError("InvariantSpec temporal_properties must be a list")


@dataclass
class CounterExample:
    """Detailed counterexample for invariant failure."""
    invariant_name: str
    error_type: str  # e.g., "violation", "timeout", "parse_error"
    details: Dict[str, Any]
    step_index: Optional[int] = None


@dataclass
class ProofWitness:
    """Proof witness bound to execution."""
    proof_id: str  # content-addressable hash of the bundle
    execution_trace: ExecutionTrace
    capability_manifest: CapabilityManifest
    cost_ledger: CostLedger
    policy_ir: PolicyIR
    invariants: List[InvariantSpec]
    counterexamples: List[CounterExample]

    def __post_init__(self):
        if not self.proof_id:
            raise ValueError("ProofWitness must have a valid proof ID")
        if not isinstance(self.counterexamples, list):
            raise ValueError("ProofWitness counterexamples must be a list")


@dataclass
class ProofBundle:
    """Complete proof bundle with artifacts."""
    id: str  # content-addressable hash of the entire bundle
    witnesses: List[ProofWitness]
    metadata: Dict[str, Any]

    def __post_init__(self):
        if not self.id:
            raise ValueError("ProofBundle must have a valid ID")
        if not isinstance(self.witnesses, list):
            raise ValueError("ProofBundle witnesses must be a list")
        MAX_BUNDLE_WITNESSES = 100
        if len(self.witnesses) > MAX_BUNDLE_WITNESSES:
            raise ValueError(f"ProofBundle exceeds max witnesses: {MAX_BUNDLE_WITNESSES}")


def _json_encoder(obj):
    """Handle non-JSON-serializable types."""
    if isinstance(obj, bytes):
        return obj.hex()  # Convert bytes to hex string
    if isinstance(obj, Enum):
        return obj.value
    raise TypeError(f"Object of type {type(obj)} not JSON serializable")


def _dataclass_to_dict(obj):
    """Convert dataclass to dict for serialization."""
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field_name, field_value in asdict(obj).items():
            if isinstance(field_value, Enum):
                result[field_name] = field_value.value
            else:
                result[field_name] = field_value
        return result
    return obj


def compute_content_hash(obj: Any) -> str:
    """Compute SHA256 hash of object's JSON representation."""
    # Handle dataclasses by converting them to dicts
    if hasattr(obj, '__dataclass_fields__'):
        obj = _dataclass_to_dict(obj)
    
    # Handle lists of dataclasses
    if isinstance(obj, list):
        obj = [_dataclass_to_dict(item) for item in obj]
        
    serialized = json.dumps(obj, sort_keys=True, separators=(',', ':'), default=_json_encoder)
    return hashlib.sha256(serialized.encode('utf-8')).hexdigest()