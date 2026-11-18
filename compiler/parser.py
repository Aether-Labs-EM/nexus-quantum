# compiler/parser.py

# ==========================================
# Vector Compiler 1.0 - Parser (AST Builder)
# ==========================================

# --- מבני הנתונים של העץ הלוגי (AST Nodes) ---

class AllocationOp:
    def __init__(self, var_name, count, kwargs):
        self.var_name = var_name
        self.count = count
        self.kwargs = kwargs # פרמטרים כמו state או protect
        
    def __repr__(self):
        return f"Allocation(Var='{self.var_name}', Count={self.count}, Options={self.kwargs})"

class GateOp:
    def __init__(self, gate_name, target):
        self.gate_name = gate_name
        self.target = target
        
    def __repr__(self):
        return f"GateOperation(Gate='{self.gate_name}', Target='{self.target}')"

class FlowOp:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        
    def __repr__(self):
        return f"FlowOperation(Source='{self.source}', Destination='{self.destination}')"

# --- המנתח התחבירי (The Parser) ---

class VectorParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type):
        token = self.current_token()
        if token and token.type == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(f"Vector Syntax Error: Expected {expected_type} but got {token.type if token else 'EOF'}")

    def parse(self):
        statements = []
        while self.current_token() is not None:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current_token()
        
        # 1. זיהוי פעולת זרימה (Flow): q_res -> out.
        if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'ARROW':
            source = self.consume('IDENTIFIER').value
            self.consume('ARROW')
            dest_token = self.current_token()
            if dest_token.type in ('KEYWORD', 'IDENTIFIER'):
                destination = self.consume(dest_token.type).value
            else:
                raise SyntaxError("Invalid flow destination")
            self.consume('DOT')
            return FlowOp(source, destination)
            
        # 2. זיהוי הקצאת משתנים: my_qubits = qubits(2, protect="Surface").
        if token.type == 'IDENTIFIER' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'EQUALS':
            var_name = self.consume('IDENTIFIER').value
            self.consume('EQUALS')
            
            alloc_token = self.current_token()
            if alloc_token.type == 'KEYWORD' and alloc_token.value in ['qubit', 'qubits']:
                self.consume('KEYWORD')
                self.consume('LPAREN')
                count = self.consume('NUMBER').value
                
                kwargs = {}
                # קריאת כל הפרמטרים הנוספים המופרדים בפסיק
                while self.current_token() and self.current_token().type == 'COMMA':
                    self.consume('COMMA')
                    key = self.consume('IDENTIFIER').value
                    self.consume('EQUALS')
                    val_token = self.current_token()
                    if val_token.type in ('NUMBER', 'STRING'):
                        kwargs[key] = val_token.value.strip('"') # מסירים מרכאות ממחרוזות
                        self.consume(val_token.type)
                    else:
                        raise SyntaxError(f"Invalid value for parameter {key}")
                        
                self.consume('RPAREN')
                self.consume('DOT')
                return AllocationOp(var_name, count, kwargs)
            
        # 3. זיהוי הפעלת שער קוונטי: H(q1).
        if token.type == 'IDENTIFIER':
            gate_name = self.consume('IDENTIFIER').value
            self.consume('LPAREN')
            target = self.consume('IDENTIFIER').value
            self.consume('RPAREN')
            self.consume('DOT')
            return GateOp(gate_name, target)

# ==========================================
# Test the Parser
# ==========================================
if __name__ == "__main__":
    from lexer import VectorLexer
    
    test_code = """
    my_qubits = qubits(2, state=0, protect="Surface").
    H(q1).
    q_res -> out.
    """
    
    lexer = VectorLexer()
    tokens = lexer.tokenize(test_code)
    
    parser = VectorParser(tokens)
    ast_tree = parser.parse()
    
    print("Abstract Syntax Tree (AST):")
    for node in ast_tree:
        print(f"- {node}")