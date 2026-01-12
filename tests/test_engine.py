import unittest
from fak.core.engine import ProofEngine
from fak.core.types import ExecutionTrace, CapabilityManifest, CostLedger, PolicyIR, InvariantSpec, ProofType


class TestProofEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = ProofEngine()
        
    def test_verify_invariants(self):
        # Create dummy artifacts
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
        
        # Verify invariants
        witness = self.engine.verify_invariants(
            trace, capabilities, cost_ledger, policy_ir, [invariant]
        )
        
        # Check that proof ID was computed
        self.assertIsNotNone(witness.proof_id)
        self.assertNotEqual(witness.proof_id, "")
        
        # Check that witness contains counterexamples (even if empty)
        self.assertIsInstance(witness.counterexamples, list)

    def test_compute_proof_id(self):
        content = {
            "trace_id": "trace123",
            "capabilities_id": "cap456",
            "cost_ledger_id": "cost789",
            "policy_ir_id": "policy000",
            "invariants": ["test_invariant"]
        }
        
        proof_id = self.engine._compute_proof_id(content)
        self.assertIsNotNone(proof_id)
        self.assertTrue(len(proof_id) > 0)

    def test_verify_invariants_timeout(self):
        # Create dummy artifacts
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
        
        # Test with very short timeout
        witness = self.engine.verify_invariants(
            trace, capabilities, cost_ledger, policy_ir, [invariant], timeout_seconds=0.001
        )
        
        # Should not raise exception even with timeout
        self.assertIsNotNone(witness.proof_id)


if __name__ == '__main__':
    unittest.main()