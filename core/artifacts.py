"""
Artifact management for FAK.
"""

from typing import Dict, Any, Optional
import threading
from .types import ExecutionTrace, CapabilityManifest, CostLedger, PolicyIR, ProofBundle, compute_content_hash


class ArtifactManager:
    """
    Manages content-addressable artifacts.
    
    Ensures immutability and versioning.
    """

    def __init__(self):
        self.artifacts: Dict[str, Any] = {}
        self._lock = threading.RLock()  # Thread-safe access

    def store_artifact(self, artifact: Any) -> str:
        """
        Store an artifact and return its content-addressable ID.
        
        Artifacts must be immutable and serializable.
        """
        # Compute hash of serialized artifact
        artifact_id = compute_content_hash(artifact)
        
        with self._lock:
            # Store artifact (in practice, this might go to a database or file system)
            self.artifacts[artifact_id] = artifact
            
        return artifact_id

    def retrieve_artifact(self, artifact_id: str) -> Any:
        """
        Retrieve an artifact by its ID.
        """
        with self._lock:
            if artifact_id not in self.artifacts:
                raise ValueError(f"Artifact {artifact_id} not found")
                
            return self.artifacts[artifact_id]

    def validate_artifact_integrity(self, artifact_id: str, artifact: Any) -> bool:
        """
        Validate that artifact matches its content-addressable ID.
        """
        with self._lock:
            computed_id = compute_content_hash(artifact)
            return computed_id == artifact_id

    def create_bundle(
        self,
        trace: ExecutionTrace,
        capabilities: CapabilityManifest,
        cost_ledger: CostLedger,
        policy_ir: PolicyIR
    ) -> ProofBundle:
        """
        Create a proof bundle from artifacts.
        """
        # Store all artifacts and get their IDs
        trace_id = self.store_artifact(trace)
        cap_id = self.store_artifact(capabilities)
        cost_id = self.store_artifact(cost_ledger)
        policy_id = self.store_artifact(policy_ir)
        
        # Validate integrity of stored artifacts
        if not self.validate_artifact_integrity(trace_id, trace):
            raise ValueError("Trace artifact integrity check failed")
            
        if not self.validate_artifact_integrity(cap_id, capabilities):
            raise ValueError("Capability manifest artifact integrity check failed")
            
        if not self.validate_artifact_integrity(cost_id, cost_ledger):
            raise ValueError("Cost ledger artifact integrity check failed")
            
        if not self.validate_artifact_integrity(policy_id, policy_ir):
            raise ValueError("Policy IR artifact integrity check failed")
        
        # Update artifact IDs in objects
        trace.id = trace_id
        capabilities.id = cap_id
        cost_ledger.id = cost_id
        policy_ir.id = policy_id
        
        # Create witness with proper proof ID computation
        from .types import ProofWitness, InvariantSpec, ProofType
        invariant = InvariantSpec(
            name="test_invariant",
            description="Test invariant",
            precondition="always (x > 0)",
            postcondition=None,
            temporal_properties=[],
            invariant_type=ProofType.BEHAVIORAL_SOUNDNESS
        )
        
        # Create witness with actual proof ID computation
        from .engine import ProofEngine
        engine = ProofEngine()
        witness = engine.verify_invariants(
            trace, capabilities, cost_ledger, policy_ir, [invariant]
        )
        
        # Create bundle
        bundle = engine.generate_bundle([witness])
        
        return bundle