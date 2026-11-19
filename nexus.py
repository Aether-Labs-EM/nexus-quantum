# nexus.py

import sys
from compiler.lexer import VectorLexer
from compiler.parser import VectorParser
from compiler.transpiler import VectorTranspiler
from compiler.runtime import LocalSimulator

def run_nexus_file(file_path):
    print(f"🚀 Nexus Compiler: Processing '{file_path}'...\n")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Lexer (ניתוח מילים)
    tokens = VectorLexer().tokenize(code)
    
    # 2. Parser (בניית עץ לוגי)
    ast = VectorParser(tokens).parse()
    
    # 3. Transpiler (המרת העץ ל-QASM)
    qasm_code = VectorTranspiler(ast).generate()
    print("✅ Compilation Successful. Generated QASM:")
    print("-" * 30)
    print(qasm_code)
    print("-" * 30)
    
    # 4. Runtime (הרצה אוטומטית על סימולטור מקומי)
    print("\n🔬 Running on Local Quantum Simulator...")
    simulator = LocalSimulator(qasm_code)
    counts = simulator.run(shots=1000)
    
    print("📊 Simulation Results:", counts)
    print("💻 Pipeline finished.\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nexus.py <file.nx>")
    else:
        run_nexus_file(sys.argv[1])