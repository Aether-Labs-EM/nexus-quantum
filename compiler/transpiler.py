# compiler/transpiler.py

class VectorTranspiler:
    def __init__(self, ast):
        self.ast = ast
        self.qasm_code = [
            "OPENQASM 3.0;",
            'include "stdgates.inc";',
            ""
        ]
        self.gate_map = {
            "H": "h", "X": "x", "Y": "y", "Z": "z", "CNOT": "cx", "RX": "rx", "RY": "ry"
        }

    def generate(self):
        self._generate_nodes(self.ast)
        return "\n".join(self.qasm_code)
        
    def _generate_nodes(self, nodes):
        for node in nodes:
            node_type = type(node).__name__
            
            if node_type == "AlgoOp":
                self.qasm_code.append(f"// --- Algorithm: {node.name} ---")
                self._generate_nodes(node.body) # קורא לעצמו כדי לתרגם את תוכן הבלוק!
                
            elif node_type == "AllocationOp":
                self.qasm_code.append(f"qubit[{node.count}] {node.var_name};")
                if "protect" in node.kwargs:
                    self.qasm_code.append(f"// @pragma logical_protection {node.kwargs['protect']}")
                    
            elif node_type == "GateOp":
                qasm_gate = self.gate_map.get(node.gate_name, node.gate_name.lower())
                targets_str = ", ".join(node.targets) # מחבר את המטרות עם פסיק עבור QASM
                self.qasm_code.append(f"{qasm_gate} {targets_str};")
                
            elif node_type == "FlowOp":
                if node.destination == "out":
                    self.qasm_code.append(f"// Vector Route: Output {node.source} to classical register")
                else:
                    self.qasm_code.append(f"// Vector Route: {node.source} -> {node.destination}")