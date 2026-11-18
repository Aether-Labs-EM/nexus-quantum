import sys
import os
from compiler.lexer import VectorLexer
from compiler.parser import VectorParser
from compiler.transpiler import VectorTranspiler

# ==========================================
# Nexus Quantum CLI - Main Entry Point
# ==========================================

def run_nexus_file(filepath, backend="local"):
    # 1. קריאת קובץ ה-Nexus
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()
        
    print(f"🚀 Nexus Compiler: Processing '{filepath}'...")
    
    # 2. השרשרת: Lexer -> Parser -> Transpiler
    tokens = VectorLexer().tokenize(source_code)
    ast = VectorParser(tokens).parse()
    qasm_code = VectorTranspiler(ast).generate()
    
    print("\n✅ Compilation Successful. Generated QASM:")
    print("-" * 30)
    print(qasm_code)
    print("-" * 30)
    
    # 3. כאן יכנס מנוע ההרצה לחומרה (Runtime)
    if backend == "ibm":
        print("\n📡 Connecting to IBM Quantum Cloud...")
        # נשלב כאן את ה-API של IBM בהמשך!
    elif backend == "google":
        print("\n📡 Connecting to Google Quantum AI...")
        # נשלב כאן את ה-API של Google בהמשך!
    else:
        print("\n💻 Local simulation/compilation finished.")

if __name__ == "__main__":
    # מאפשר להריץ מהטרמינל: python nexus.py examples/hello_world.nx
    if len(sys.argv) < 2:
        print("Usage: python nexus.py <path_to_file.nx> [--ibm | --google]")
    else:
        file_path = sys.argv[1]
        
        # זיהוי דגל חומרה (אם המשתמש ביקש להריץ על IBM)
        target_backend = "local"
        if "--ibm" in sys.argv:
            target_backend = "ibm"
        elif "--google" in sys.argv:
            target_backend = "google"
            
        run_nexus_file(file_path, target_backend)