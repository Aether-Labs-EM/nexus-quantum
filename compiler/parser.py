# compiler/parser.py

class AllocationOp:
    def __init__(self, var_name, count, kwargs):
        self.var_name = var_name; self.count = count; self.kwargs = kwargs

class GateOp:
    def __init__(self, gate_name, targets):
        self.gate_name = gate_name
        self.targets = targets

class FlowOp:
    def __init__(self, source, destination):
        self.source = source; self.destination = destination

class AlgoOp:
    def __init__(self, name, params, body):
        self.name = name; self.params = params; self.body = body

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

    def parse_target(self):
        target = self.consume('IDENTIFIER').value
        if self.current_token() and self.current_token().type == 'LBRACKET':
            self.consume('LBRACKET')
            index = self.consume('NUMBER').value
            self.consume('RBRACKET')
            target = f"{target}[{index}]"
        return target

    def parse(self):
        statements = []
        while self.current_token() is not None:
            statements.append(self.parse_statement())
        return statements

    def parse_statement(self):
        token = self.current_token()
        
        # 1. זיהוי בלוק אלגוריתם
        if token.type == 'KEYWORD' and token.value == 'algo':
            self.consume('KEYWORD')
            name = self.consume('IDENTIFIER').value
            self.consume('LPAREN')
            params = []
            
            if self.current_token().type == 'IDENTIFIER':
                params.append(self.consume('IDENTIFIER').value)
                while self.current_token() and self.current_token().type == 'COMMA':
                    self.consume('COMMA')
                    params.append(self.consume('IDENTIFIER').value)
                    
            self.consume('RPAREN')
            self.consume('LBRACE')
            
            body = [] 
            while self.current_token() and self.current_token().type != 'RBRACE':
                body.append(self.parse_statement())
            self.consume('RBRACE')
            return AlgoOp(name, params, body)

        # 2. זיהוי הקצאה
        if token.type == 'IDENTIFIER' and self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1].type == 'EQUALS':
            var_name = self.consume('IDENTIFIER').value
            self.consume('EQUALS')
            if self.current_token().value in ['qubit', 'qubits']:
                self.consume('KEYWORD')
                self.consume('LPAREN')
                count = self.consume('NUMBER').value
                kwargs = {}
                while self.current_token() and self.current_token().type == 'COMMA':
                    self.consume('COMMA')
                    key = self.consume('IDENTIFIER').value
                    self.consume('EQUALS')
                    val_tok = self.current_token()
                    kwargs[key] = val_tok.value.strip('"')
                    self.consume(val_tok.type)
                self.consume('RPAREN')
                self.consume('DOT')
                return AllocationOp(var_name, count, kwargs)
                
        # 3. זיהוי זרימת נתונים (Flow)
        if token.type == 'IDENTIFIER':
            temp_pos = self.pos
            try:
                self.parse_target()
                if self.current_token() and self.current_token().type == 'ARROW':
                    self.pos = temp_pos
                    source = self.parse_target()
                    self.consume('ARROW')
                    dest = self.consume(self.current_token().type).value
                    self.consume('DOT')
                    return FlowOp(source, dest)
            except:
                pass
            self.pos = temp_pos

        # 4. זיהוי שערים או קריאה לאלגוריתם (Gate/Call)
        if token.type == 'IDENTIFIER':
            next_tok = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
            
            # שער בודד או קריאה לפונקציה: H(q1). או hello_quantum(q1, q2).
            if next_tok and next_tok.type == 'LPAREN':
                gate = self.consume('IDENTIFIER').value
                self.consume('LPAREN')
                
                targets = []
                if self.current_token().type == 'IDENTIFIER':
                    targets.append(self.parse_target())
                    while self.current_token() and self.current_token().type == 'COMMA':
                        self.consume('COMMA')
                        targets.append(self.parse_target())
                        
                self.consume('RPAREN')
                self.consume('DOT')
                return GateOp(gate, targets)
                
            # שער משורשר (מותנה): q1.q2(CNOT).# שער משורשר (מותנה): q1.q2(CNOT).
            else:
                targets = []
                targets.append(self.parse_target())
                
                # כל עוד יש נקודה, תמשיך לאסוף קיוביטים!
                while self.current_token() and self.current_token().type == 'DOT':
                    self.consume('DOT')
                    
                    if self.current_token().type == 'NUMBER':
                        raise SyntaxError(f"Nexus Syntax Error: Expected a qubit name after the dot, but got '{self.current_token().value}'.")
                    
                    targets.append(self.parse_target())
                    
                self.consume('LPAREN')
                gate = self.consume('IDENTIFIER').value
                self.consume('RPAREN')
                self.consume('DOT')
                return GateOp(gate, targets)
        raise SyntaxError(f"Vector Syntax Error: I don't know how to parse '{token.value}' yet!")