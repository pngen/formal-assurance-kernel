import unittest
from fak.core.types import ExecutionTrace, CapabilityManifest, CostLedger, PolicyIR, ProofWitness, ProofBundle, compute_content_hash, CounterExample


class TestTypes(unittest.TestCase):
    
    def test_execution_trace(self):
        trace = ExecutionTrace(
            id="test_id",
            steps=[{"op": "call", "args": []}],
            metadata={}
        )
        self.assertEqual(trace.id, "test_id")
        self.assertEqual(len(trace.steps), 1)
        
        # Test validation
        with self.assertRaises(ValueError):
            ExecutionTrace(id="", steps=[], metadata={})
            
        # Test max steps validation
        with self.assertRaises(ValueError):
            ExecutionTrace(
                id="test",
                steps=[{"op": "call", "args": []}] * 100001,  # Exceeds limit
                metadata={}
            )
            
    def test_capability_manifest(self):
        manifest = CapabilityManifest(
            id="test_id",
            agent_id="agent_123",
            capabilities=["read", "write"],
            authority_graph={"read": ["write"]},
            metadata={}
        )
        self.assertEqual(manifest.id, "test_id")
        self.assertEqual(manifest.agent_id, "agent_123")
        
        # Test validation
        with self.assertRaises(ValueError):
            CapabilityManifest(id="", agent_id="test", capabilities=[], authority_graph={}, metadata={})
            
    def test_cost_ledger(self):
        ledger = CostLedger(
            id="test_id",
            entries=[{"operation": "read", "cost": 1.0}],
            total_cost=1.0,
            metadata={}
        )
        self.assertEqual(ledger.id, "test_id")
        self.assertEqual(ledger.total_cost, 1.0)
        
        # Test validation
        with self.assertRaises(ValueError):
            CostLedger(id="", entries=[], total_cost=-1.0, metadata={})
            
    def test_policy_ir(self):
        policy = PolicyIR(
            id="test_id",
            ast={"type": "policy", "rules": []},
            compiled_enforcement=b"compiled_code",
            metadata={}
        )
        self.assertEqual(policy.id, "test_id")
        self.assertEqual(policy.compiled_enforcement, b"compiled_code")
        
        # Test validation
        with self.assertRaises(ValueError):
            PolicyIR(id="", ast={}, compiled_enforcement=b"", metadata={})
            
    def test_counter_example(self):
        example = CounterExample(
            invariant_name="test_invariant",
            error_type="violation",
            details={"reason": "test"},
            step_index=1
        )
        self.assertEqual(example.invariant_name, "test_invariant")
        
    def test_content_hash(self):
        obj = {"key": "value"}
        hash1 = compute_content_hash(obj)
        hash2 = compute_content_hash(obj)
        self.assertEqual(hash1, hash2)
        
        # Different object should produce different hash
        obj2 = {"key": "different_value"}
        hash3 = compute_content_hash(obj2)
        self.assertNotEqual(hash1, hash3)
        
        # Test with dataclass
        trace = ExecutionTrace(
            id="test_id",
            steps=[{"op": "call", "args": []}],
            metadata={}
        )
        hash4 = compute_content_hash(trace)
        self.assertTrue(len(hash4) > 0)
        
        # Test with bytes field (PolicyIR case)
        policy = PolicyIR(
            id="test_policy",
            ast={"type": "policy"},
            compiled_enforcement=b"test_bytes",
            metadata={}
        )
        hash5 = compute_content_hash(policy)
        self.assertTrue(len(hash5) > 0)


if __name__ == '__main__':
    unittest.main()