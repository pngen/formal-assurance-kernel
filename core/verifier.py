"""
Standalone verifier for FAK proof bundles.
"""

from typing import Dict, Any
from .types import ProofBundle, ProofWitness, CounterExample
from .engine import ProofEngine


class Verifier:
    """
    Standalone verifier that accepts a proof bundle and re-checks invariants.
    
    Does not depend on original runtime environment.
    """

    def __init__(self):
        self.engine = ProofEngine()

    def verify_bundle(self, bundle: ProofBundle) -> Dict[str, Any]:
        """
        Verify a proof bundle.
        
        Returns binary verdict with diagnostics.
        """
        # Verify bundle ID integrity
        expected_bundle_id = self._compute_bundle_id(bundle)
        if expected_bundle_id != bundle.id:
            return {
                'bundle_id': bundle.id,
                'success': False,
                'error': 'Bundle ID integrity check failed'
            }
            
        results = []
        overall_success = True
        
        for witness in bundle.witnesses:
            try:
                # Re-check each invariant
                success = self.engine.verify_invariants(
                    witness.execution_trace,
                    witness.capability_manifest,
                    witness.cost_ledger,
                    witness.policy_ir,
                    witness.invariants
                )
                
                # Verify that the computed proof ID matches what's in the witness
                # Note: We only check the immutable inputs, not outputs like counterexamples
                if success.proof_id != witness.proof_id:
                    results.append({
                        'success': False,
                        'error': 'Proof ID mismatch',
                        'expected': witness.proof_id,
                        'actual': success.proof_id
                    })
                    overall_success = False
                    continue
                    
                # Check counterexamples for failures
                if success.counterexamples:
                    results.append({
                        'success': False,
                        'invariant_count': len(witness.invariants),
                        'counterexamples': [c.__dict__ for c in success.counterexamples]
                    })
                    overall_success = False
                else:
                    results.append({
                        'success': True,
                        'invariant_count': len(witness.invariants),
                        'counterexamples': []
                    })
                    
            except Exception as e:
                results.append({
                    'error': str(e)
                })
                overall_success = False
                
        return {
            'bundle_id': bundle.id,
            'success': overall_success,
            'results': results
        }
        
    def _compute_bundle_id(self, bundle: ProofBundle) -> str:
        """Compute content-addressable bundle ID."""
        from .types import compute_content_hash
        # Create content for hashing without witness details (which include counterexamples)
        bundle_content = {
            "witnesses": [w.proof_id for w in bundle.witnesses],
            "metadata": bundle.metadata
        }
        return compute_content_hash(bundle_content)