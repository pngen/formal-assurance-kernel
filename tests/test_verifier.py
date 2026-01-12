import unittest
from fak.core.verifier import Verifier
from fak.core.types import ProofBundle, ProofWitness, ExecutionTrace, CapabilityManifest, CostLedger, PolicyIR, InvariantSpec, ProofType


class TestVerifier(unittest.TestCase):
    
    def test_verify_bundle(self):
        # Create a mock bundle with a witness
        trace = ExecutionTrace(
            id="trace_id",
            steps=[{"op": "call", "args": []}],
            metadata={}
        )
        
        capabilities = CapabilityManifest(
            id="cap_id",
            agent_id="agent_123",
            capabilities=["read"],
            authority_graph={},
            metadata={}
        )
        
        cost_ledger = CostLedger(
            id="cost_id",
            entries=[],
            total_cost=0.0,
            metadata={}
        )
        
        policy_ir = PolicyIR(
            id="policy_id",
            ast={},
            compiled_enforcement=b"",
            metadata={}
        )
        
        invariant = InvariantSpec(
            name="test_invariant",
            description="Test invariant",
            precondition="always (x > 0)",
            postcondition=None,
            temporal_properties=[],
            invariant_type=ProofType.BEHAVIORAL_SOUNDNESS
        )
        
        # Create witness with proper proof ID
        from fak.core.engine import ProofEngine
        engine = ProofEngine()
        witness = engine.verify_invariants(
            trace, capabilities, cost_ledger, policy_ir, [invariant]
        )
        
        bundle = ProofBundle(
            id="bundle_id",
            witnesses=[witness],
            metadata={}
        )
        
        verifier = Verifier()
        result = verifier.verify_bundle(bundle)
        
        # This should now work correctly
        self.assertTrue(result['success'])
        self.assertEqual(len(result['results']), 1)

    def test_verify_bundle_integrity_check(self):
        # Create a bundle with invalid ID
        trace = ExecutionTrace(
            id="trace_id",
            steps=[{"op": "call", "args": []}],
            metadata={}
        )
        
        capabilities = CapabilityManifest(
            id="cap_id",
            agent_id="agent_123",
            capabilities=["read"],
            authority_graph={},
            metadata={}
        )
        
        cost_ledger = CostLedger(
            id="cost_id",
            entries=[],
            total_cost=0.0,
            metadata={}
        )
        
        policy_ir = PolicyIR(
            id="policy_id",
            ast={},
            compiled_enforcement=b"",
            metadata={}
        )
        
        invariant = InvariantSpec(
            name="test_invariant",
            description="Test invariant",
            precondition="always (x > 0)",
            postcondition=None,
            temporal_properties=[],
            invariant_type=ProofType.BEHAVIORAL_SOUNDNESS
        )
        
        from fak.core.engine import ProofEngine
        engine = ProofEngine()
        witness = engine.verify_invariants(
            trace, capabilities, cost_ledger, policy_ir, [invariant]
        )
        
        # Create bundle with wrong ID to test integrity check
        bundle = ProofBundle(
            id="wrong_bundle_id",  # Wrong ID
            witnesses=[witness],
            metadata={}
        )
        
        verifier = Verifier()
        result = verifier.verify_bundle(bundle)
        
        # Should fail integrity check
        self.assertFalse(result['success'])
        self.assertIn('Bundle ID integrity check failed', result.get('error', ''))


if __name__ == '__main__':
    unittest.main()