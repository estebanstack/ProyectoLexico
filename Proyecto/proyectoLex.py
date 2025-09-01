
import sys


# Configuración

RESERVADAS = {
    "class","def","if","else","elif","while","for","return","print",
    "True","False","None","and","or","not","in","is","break","continue",
    "pass","import","from","as","with","try","except","finally","raise",
    "lambda","yield","global","nonlocal","assert"
}

OPERADORES = {
    "==":"tk_igual_igual",
    "!=":"tk_distinto",
    "<=":"tk_menor_igual",
    ">=":"tk_mayor_igual",
    "->":"tk_flecha",
    "=":"tk_asig",
    "<":"tk_menor",
    ">":"tk_mayor",
    ":":"tk_dos_puntos",
    ",":"tk_coma",
    ".":"tk_punto",
    "(":"tk_par_izq",
    ")":"tk_par_der",
    "{":"tk_llave_izq",
    "}":"tk_llave_der",
    "[":"tk_cor_izq",
    "]":"tk_cor_der",
    "+":"tk_suma",
    "-":"tk_resta",
    "*":"tk_mul",
    "/":"tk_div",
    "%":"tk_mod"
}

PREFIJOS = {"=","!","<",">","-"}


# Clase Buffer (manejo de texto y posición)

class Buffer:
    def __init__(self, text):
        self.text = text
        self.i = 0
        self.line = 1
        self.col = 1

    def eof(self):
        return self.i >= len(self.text)

    def peek(self, k=0):
        idx = self.i + k
        if idx < len(self.text):
            return self.text[idx]
        return ''

    def next(self):
        if self.eof():
            return ''
        ch = self.text[self.i]
        self.i += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def get_pos(self):
        return self.line, self.col


# Clase base para AFD

class Automata:
    def aceptar(self, buf: Buffer):
        """Intenta reconocer un token desde la posición actual.
           Si acepta, devuelve (token, lexema, line, col, chars_consumed)
           Si no, devuelve None."""
        raise NotImplementedError


# AFD Identificadores# 
class AFDIdentificador(Automata):
    def aceptar(self, buf):
        ch = buf.peek()
        if not (ch.isalpha() or ch == '_'):
            return None
        start_line, start_col = buf.get_pos()
        lex = ''
        i = 0
        while not buf.eof() and (buf.peek(i).isalpha() or buf.peek(i).isdigit() or buf.peek(i) == '_'):
            lex += buf.peek(i)
            i += 1
        token = lex if lex in RESERVADAS else "id"
        return (token, lex, start_line, start_col, i)


# AFD Enteros
class AFDEntero(Automata):
    def aceptar(self, buf):
        ch = buf.peek()
        i = 0
        lex = ''
        if ch in '+-':
            if buf.peek(1).isdigit():
                lex += ch
                i += 1
            else:
                return None
        if buf.peek(i).isdigit():
            while not buf.eof() and buf.peek(i).isdigit():
                lex += buf.peek(i)
                i += 1
            return ("tk_entero", lex, buf.line, buf.col, i)
        return None

# AFD Cadenas

class AFDCadena(Automata):
    def aceptar(self, buf):
        ch = buf.peek()
        if ch not in {'"', "'"}:
            return None
        start_line, start_col = buf.get_pos()
        delim = ch
        lex = delim
        i = 1
        escaped = False
        while not buf.eof():
            c = buf.peek(i)
            if c == '':
                return None  # EOF antes de cerrar
            lex += c
            if escaped:
                escaped = False
            else:
                if c == '\\':
                    escaped = True
                elif c == delim:
                    return ("tk_cadena", lex, start_line, start_col, i+1)
            i += 1
        return None
    

# AFD Operadores

class AFDOperador(Automata):
    def aceptar(self, buf):
        ch = buf.peek()
        # probar primero operador de 2 caracteres
        two = ch + buf.peek(1)
        if two in OPERADORES:
            return (OPERADORES[two], two, buf.line, buf.col, 2)
        # si no, probar operador de 1 carácter
        if ch in OPERADORES:
            return (OPERADORES[ch], ch, buf.line, buf.col, 1)
        return None



# Lexer que une todo
class Lexer:
    def __init__(self, text):
        self.buf = Buffer(text)
        self.automatas = [
            AFDCadena(),
            AFDOperador(),  # probar operadores antes que números por signos
            AFDIdentificador(),
            AFDEntero()
        ]

    def analizar(self):
        while not self.buf.eof():
            ch = self.buf.peek()
            if ch.isspace():
                self.buf.next()
                continue
            if ch == '#':
                # ignorar comentario
                while not self.buf.eof() and self.buf.peek() != '\n':
                    self.buf.next()
                continue
            # probar autómatas
            match = None
            for afd in self.automatas:
                match = afd.aceptar(self.buf)
                if match:
                    token, lexema, line, col, n = match
                    for _ in range(n):
                        self.buf.next()
                    self.emitir(token, lexema, line, col)
                    break
            if not match:
                self.error(self.buf.line, self.buf.col)

    def emitir(self, token, lexema, line, col):
        if token in RESERVADAS:
            print(f"<{token},{line},{col}>")
        elif token == "id":
            print(f"<id,{lexema},{line},{col}>")
        elif token == "tk_entero":
            print(f"<tk_entero,{lexema},{line},{col}>")
        elif token == "tk_cadena":
            print(f"<tk_cadena,{lexema},{line},{col}>")
        else:
            print(f"<{token},{line},{col}>")

    def error(self, line, col):
        print(f">>> Error léxico(linea:{line},posicion:{col})")
        sys.exit(1)

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python proyectoLex.py <archivo.py>")
        sys.exit(1)
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    lexer = Lexer(text)
    lexer.analizar()
