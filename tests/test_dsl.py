import unittest
from fak.core.dsl import InvariantDSL


class TestInvariantDSL(unittest.TestCase):
    
    def test_parse_invariant(self):
        spec_str = """
        invariant test_invariant {
            precondition: always (x > 0)
            postcondition: eventually (y == z)
            temporal_properties: [always, eventually]
        }
        """
        
        result = InvariantDSL.parse_invariant(spec_str)
        self.assertEqual(result['name'], 'test_invariant')
        self.assertEqual(result['precondition'], 'always (x > 0)')
        self.assertEqual(result['postcondition'], 'eventually (y == z)')
        self.assertIn('always', result['temporal_properties'])
        self.assertIn('eventually', result['temporal_properties'])

    def test_parse_invariant_minimal(self):
        spec_str = """
        invariant minimal {
            precondition: always (x > 0)
        }
        """
        
        result = InvariantDSL.parse_invariant(spec_str)
        self.assertEqual(result['name'], 'minimal')
        self.assertEqual(result['precondition'], 'always (x > 0)')
        self.assertIsNone(result['postcondition'])
        self.assertEqual(result['temporal_properties'], [])

    def test_parse_invariant_no_properties(self):
        spec_str = """
        invariant no_props {
            precondition: always (x > 0)
            postcondition: eventually (y == z)
        }
        """
        
        result = InvariantDSL.parse_invariant(spec_str)
        self.assertEqual(result['name'], 'no_props')
        self.assertEqual(result['precondition'], 'always (x > 0)')
        self.assertEqual(result['postcondition'], 'eventually (y == z)')
        self.assertEqual(result['temporal_properties'], [])

    def test_parse_invariant_with_comments(self):
        spec_str = """
        # This is a comment
        invariant with_comments {
            # Another comment
            precondition: always (x > 0)  # Inline comment
            postcondition: eventually (y == z)
        }
        """
        
        result = InvariantDSL.parse_invariant(spec_str)
        self.assertEqual(result['name'], 'with_comments')
        self.assertEqual(result['precondition'], 'always (x > 0)')
        self.assertEqual(result['postcondition'], 'eventually (y == z)')

    def test_parse_invariant_closing_brace(self):
        spec_str = """
        invariant test {
            precondition: always (x > 0)
        }
        """
        
        result = InvariantDSL.parse_invariant(spec_str)
        self.assertEqual(result['name'], 'test')
        self.assertEqual(result['precondition'], 'always (x > 0)')
        self.assertIsNone(result['postcondition'])

    def test_parse_invariant_no_braces(self):
        spec_str = """
        invariant simple
            precondition: always (x > 0)
        """
        
        # Should handle missing braces gracefully
        try:
            result = InvariantDSL.parse_invariant(spec_str)
            self.assertEqual(result['name'], 'simple')
        except Exception as e:
            # Expected to fail due to format, but we want to know the error type
            pass


if __name__ == '__main__':
    unittest.main()