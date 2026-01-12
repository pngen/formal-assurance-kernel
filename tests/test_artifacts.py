import unittest
from fak.core.artifacts import ArtifactManager
from fak.core.types import ExecutionTrace, CapabilityManifest, CostLedger, PolicyIR


class TestArtifactManager(unittest.TestCase):
    
    def test_store_and_retrieve(self):
        manager = ArtifactManager()
        
        # Create some artifacts
        trace = ExecutionTrace(
            id="test_id",
            steps=[{"op": "call", "args": []}],
            metadata={}
        )
        
        artifact_id = manager.store_artifact(trace)
        retrieved = manager.retrieve_artifact(artifact_id)
        
        self.assertEqual(retrieved.id, "test_id")
        
    def test_validate_integrity(self):
        manager = ArtifactManager()
        
        trace = ExecutionTrace(
            id="test_id",
            steps=[{"op": "call", "args": []}],
            metadata={}
        )
        
        artifact_id = manager.store_artifact(trace)
        integrity_ok = manager.validate_artifact_integrity(artifact_id, trace)
        self.assertTrue(integrity_ok)
        
        # Test with modified artifact
        trace_modified = ExecutionTrace(
            id="test_id",
            steps=[{"op": "call", "args": ["modified"]}],
            metadata={}
        )
        integrity_bad = manager.validate_artifact_integrity(artifact_id, trace_modified)
        self.assertFalse(integrity_bad)
        
    def test_create_bundle(self):
        manager = ArtifactManager()
        
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
        
        bundle = manager.create_bundle(trace, capabilities, cost_ledger, policy_ir)
        
        self.assertIsNotNone(bundle)
        self.assertIsNotNone(bundle.id)
        self.assertTrue(len(bundle.id) > 0)


if __name__ == '__main__':
    unittest.main()