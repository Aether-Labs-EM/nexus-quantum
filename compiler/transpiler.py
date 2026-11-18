# compiler/transpiler.py

# ==========================================
# Vector Compiler 1.0 - Transpiler (Code Generator)
# Target: OpenQASM 3.0
# ==========================================

class VectorTranspiler:
    def __init__(self, ast):
        self.ast = ast
        # התחלה סטנדרטית של קובץ קוונטי אמיתי
        self.qasm_code = [
            "OPENQASM 3.0;",
            'include "stdgates.inc";',
            ""
        ]
        
        # חידוד שפה: מילון תרגום משערי Nexus אלגנטיים לפקודות QASM נמוכות
        self.gate_map = {
            "H": "h",
            "X": "x",
            "Y": "y",
            "Z": "z",
            "CNOT": "cx",
            "RX": "rx",
            "RY": "ry"
        }

    def generate(self):
        for node in self.ast:
            node_type = type(node).__name__
            
            # תרגום הקצאת קיוביטים
            if node_type == "AllocationOp":
                # ב-Nexus: my_qubits = qubits(2).
                # ב-QASM: qubit[2] my_qubits;
                self.qasm_code.append(f"qubit[{node.count}] {node.var_name};")
                
                # אם הוגדרה הגנה, נוסיף אותה כהערה שהמערכת של IBM תוכל לקרוא
                if "protect" in node.kwargs:
                    self.qasm_code.append(f"// @pragma logical_protection {node.kwargs['protect']}")
                
            # תרגום שערים קוונטיים
            elif node_type == "GateOp":
                # ב-Nexus: H(q1).
                # ב-QASM: h q1;
                qasm_gate = self.gate_map.get(node.gate_name, node.gate_name.lower())
                self.qasm_code.append(f"{qasm_gate} {node.target};")
                
            # תרגום זרימת נתונים (Flow)
            elif node_type == "FlowOp":
                # QASM לא תומך טבעית בחצים, אז אנחנו ממירים את זה להערות ניתוב או למדידות
                if node.destination == "out":
                    self.qasm_code.append(f"// Vector Route: Output {node.source} to classical register")
                else:
                    self.qasm_code.append(f"// Vector Route: {node.source} -> {node.destination}")

        return "\n".join(self.qasm_code)

# ==========================================
# מבחן הקומפיילר המלא! (Pipeline Test)
# ==========================================
if __name__ == "__main__":
    from lexer import VectorLexer
    from parser import VectorParser
    
    # 1. קוד המקור שכתבנו ב-Nexus
    nexus_source = """
    my_qubits = qubits(2, protect="Surface").
    H(q1).
    q_res -> out.
    """
    
    print("--- Nexus Source Code ---")
    print(nexus_source.strip())
    
    # 2. השרשרת: Lexer -> Parser -> Transpiler
    tokens = VectorLexer().tokenize(nexus_source)
    ast = VectorParser(tokens).parse()
    qasm_output = VectorTranspiler(ast).generate()
    
    print("\n--- Compiled OpenQASM 3.0 ---")
    print(qasm_output)