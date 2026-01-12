"""
Invariant specification DSL for FAK.
"""

import re
from typing import List, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class TemporalProperty:
    """Represents a temporal property."""
    operator: str  # e.g., "always", "eventually", "within N steps"
    expression: str


class InvariantDSL:
    """
    Minimal DSL for specifying invariants.
    
    Grammar:
        invariant <name> {
            precondition: <temporal_formula>
            postcondition: <temporal_formula>
            temporal_properties: [list of properties]
        }
        
    Temporal formulas are simple expressions like:
        always (x > 0)
        eventually (y == z)
        within 10 steps (p => q)
    """

    @staticmethod
    def parse_invariant(spec_str: str) -> Dict[str, Any]:
        """Parse invariant specification string into structured form."""
        # Remove comments and normalize whitespace
        lines = spec_str.split('\n')
        clean_lines = []
        for line in lines:
            # Remove inline comments
            if '#' in line:
                line = line[:line.find('#')]
            line = line.strip()
            if line:  # Only add non-empty lines
                clean_lines.append(line)
        
        spec_str_clean = '\n'.join(clean_lines)
        
        # Extract invariant name
        invariant_match = re.search(r'invariant\s+(\w+)', spec_str_clean)
        if not invariant_match:
            raise ValueError("Invalid invariant specification format: missing invariant name")
            
        name = invariant_match.group(1)
        
        # Extract fields individually to avoid regex capture issues
        fields = {}
        for field_name in ['precondition', 'postcondition', 'temporal_properties']:
            # Pattern that properly handles closing braces and field boundaries
            pattern = rf'{field_name}:\s*(.*?)(?=\s*(?:precondition|postcondition|temporal_properties|}})\s*|$)'
            match = re.search(pattern, spec_str_clean, re.DOTALL)
            if match:
                value = match.group(1).strip()
                # Remove trailing brace if present (handles closing brace in same line)
                if value.endswith('}'):
                    value = value[:-1].strip()
                fields[field_name] = value
        
        # Handle temporal properties specially since it's a list
        if 'temporal_properties' in fields:
            temp_props = fields['temporal_properties']
            if temp_props.startswith('[') and temp_props.endswith(']'):
                props_list = [p.strip() for p in temp_props[1:-1].split(',') if p.strip()]
            else:
                props_list = []
            fields['temporal_properties'] = props_list
        else:
            fields['temporal_properties'] = []
            
        return {
            'name': name,
            'precondition': fields.get('precondition'),
            'postcondition': fields.get('postcondition'),
            'temporal_properties': fields.get('temporal_properties', [])
        }