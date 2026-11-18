import re

# ==========================================
# Vector Compiler 1.0 - Lexer (Tokenization)
# ==========================================

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class VectorLexer:
    def __init__(self):
        # הגדרת החוקים של שפת Nexus
        self.rules = [
            ('COMMENT',   r'#.*'),
            ('ARROW',     r'->'),                     # חץ זרימת המידע
            ('HELP',      r'\(help\)'),               # קיוביט עזר (RAII)
            ('ANGLE',     r'\d+[><]'),                # זוויות סיבוב (למשל 90>)
            
            # מילות המפתח של השפה (כולל החדשות: simulate, out, send, receive)
            ('KEYWORD',   r'\b(algo|alias|qubits|qubit|measure|if|loop|run|simulate|out|send|receive)\b'), 
            
            ('IDENTIFIER',r'[a-zA-Z_][a-zA-Z0-9_]*'), # שמות משתנים ופונקציות
            ('NUMBER',    r'\d+'),                    # מספרים שלמים
            ('STRING',    r'".*?"'),                  # מחרוזות (טקסט במרכאות)
            ('DOT',       r'\.'),                     # נקודה של סוף פקודה
            ('COMMA',     r','),                      # פסיק
            ('LPAREN',    r'\('),                     # סוגריים ()
            ('RPAREN',    r'\)'),
            ('LBRACE',    r'\{'),                     # סוגריים {}
            ('RBRACE',    r'\}'),
            ('LBRACKET',  r'\['),                     # סוגריים מרובעים [
            ('RBRACKET',  r'\]'),                     # סוגריים מרובעים ]
            ('EQUALS',    r'='),                      # אופרטור השמה
            ('PLUS',      r'\+'),                     # אופרטור חיבור (למתמטיקה קוונטית)
            ('WHITESPACE',r'\s+'),                    # רווחים
        ]
        self.regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.rules))

    def tokenize(self, code):
        tokens = []
        for match in self.regex.finditer(code):
            type = match.lastgroup
            value = match.group()
            
            # מתעלמים מרווחים והערות בזמן פירוק הקוד
            if type == 'WHITESPACE' or type == 'COMMENT':
                continue 
                
            tokens.append(Token(type, value))
        return tokens

# בדיקה מהירה של הקומפיילר:
if __name__ == "__main__":
    test_code = """
    my_algo(q) -> simulate(1000, noise="IBM") -> res.
    q_res -> out.
    q_num1 + q_num2.
    """
    
    lexer = VectorLexer()
    tokens = lexer.tokenize(test_code)
    
    for t in tokens:
        print(t)