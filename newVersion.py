'''class Lex ():
    def __init__(self, t_lex, v_lex):
        self.t_lex = t_lex
        self.v_lex = v_lex

    def get_value(self):
        return self.v_lex


new = Lex("Var", 5)
print(new.get_value())'''

class Parser():
    TD = [
        "null",
        "+",  # 1
        "-",  # 2
        "*",  # 3
        "/",  # 4
        "(",  # 5
        ")",  # 6
        "{",  # 7
        "}",  # 8
        "[",  # 9
        "]",  # 10
        ";",  # 11
        "=",  # 12
        ":",  # 13
        ":=",  # 14
        "<",  # 15
        ">",  # 16
        "<>",  # 17
        "<=",  # 18
        ">=",  # 19
        ".",  # 20
        ",",  # 21
        "’",  # 22
        "^",  # 23
        "@"  # 24
    ]

    TW = [
        "null",
        "and",  # 1
        "array",  # 2
        "begin",  # 3
        "case",  # 4
        "const",  # 5
        "div",  # 6
        "do",  # 7
        "downto",  # 8
        "else",  # 9
        "end",  # 10
        "file",  # 11
        "for",  # 12
        "function",  # 13
        "goto",  # 14
        "if",  # 15
        "label",  # 16
        "mod",  # 17
        "nil",  # 18
        "not",  # 19
        "of",  # 20
        "or",  # 21
        "procedure",  # 22
        "program",  # 23
        "record",  # 24
        "repeat",  # 25
        "then",  # 26
        "to",  # 27
        "type",  # 28
        "until",  # 29
        "var",  # 30
        "while",  # 31
        "with",  # 32
        "xor",  # 33
        "true",
        "false"
    ]
    one_sym = ''
    buf = ""
    dict = {}
    poliz = []
    st_lex = []

    def __init__(self):
        pass

    def get_lex(self, file, dict, one_sym):
        buf = []
        cs = 'H'
        d = 0
        if one_sym == '' or one_sym == ' ' or one_sym == '\n' or one_sym == '\r' or one_sym == '\t':
            pass
        elif one_sym in self.TD:
            if one_sym == ':':
                c = file.read(1)
                if c == '=':
                    return ":=", dict, ''
                else:
                    return one_sym, dict, c
            return one_sym, dict, ''
        else:
            buf.append(one_sym)
        while True:
            c = file.read(1)
            if cs == 'H':
                if c == ' ' or c == '\n' or c == '\r' or c == '\t':
                    pass
                elif c.isalpha():
                    buf.append(c)
                    cs = 'IDENT'
                elif c.isdigit():
                    d = int(c)
                    cs = 'NUMB'
                elif (c == '{'):
                    cs = 'COM'
                elif c == ':' or c == '<' or c == '>':
                    buf.append(c)
                    cs = 'ALE'
                elif c == '@':
                    return "End"
                elif c == '!':
                    buf.append(c)
                    cs = 'NEQ'
                else:
                    buf.append(c)
                    if "".join(buf) in self.TD:
                        return "".join(buf), dict, ''
                    else:
                        return "Error1", dict, one_sym
            elif cs == 'IDENT':
                if c.isalpha() or c.isdigit():
                    buf.append(c)
                else:
                    # c = file.read(1)
                    one_sym = c
                    if "".join(buf) in self.TW:
                        dict["".join(buf)] = ("official")
                    else:
                        dict["".join(buf)] = ("ID", False)
                    return "".join(buf), dict, one_sym
            elif cs == 'NUMB':
                if c.isdigit():
                    d = d * 10 + int(c)
                else:
                    # c = file.read(1)
                    one_sym = c
                    return d, dict, one_sym
            elif cs == 'COM':
                if (c == '}'):
                    cs = 'H'
            elif c == '@' or c == '{':
                return "Error2", dict, ''
            elif cs == 'ALE':
                if c == '=':
                    buf.append(c)
                    return "".join(buf), dict, one_sym
                else:
                    # c = file.read(1)
                    one_sym = c
                    return "".join(buf), dict, ''
            else:
                if c == '=':
                    buf.append(c)
                    return "".join(buf), dict, ''

    def gl(self, f):
        self.buf, self.dict, self.one_sym = self.get_lex(f, self.dict, self.one_sym)

    def program(self, f):
        self.gl(f)
        if self.buf == "program":
            print("good!")
        else:
            print("Error: expect 'program'")
            return
        self.gl(f)
        if self.buf in self.dict:
            if self.dict[self.buf][0] == "ID":
                print("good!")
            else:
                print("Error: expect name program")
                return
        else:
            print("Error: expect name program")
            return
        self.gl(f)
        if self.buf == '(':
            print("OK")
        else:
            print("Error: expect left bracket")
            return
        self.gl(f)
        while True:
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    print("good!")
                else:
                    print("Error: expect arg program")
                    return
            else:
                print("Error: expect arg program")
                return
            self.gl(f)
            if self.buf == ',':
                self.gl(f)
            elif self.buf == ')':
                self.gl(f)
                if self.buf == ';':
                    print("good!")
                    return
                else:
                    print("Error: expect semicolon")
                    return
            else:
                print("Error: expect right bracket or comma")
                return

    def const(self, f):
        tmp_var = ''
        self.gl(f)
        while True:
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    tmp_var = self.buf
                    print("good!")
                else:
                    print("Error: expect name of const")
                    return
            else:
                print("Error: error name of const")
                return
            self.gl(f)
            if self.buf == '=':
                print("good!")
            else:
                print("Error: expect '='")
                return
            self.gl(f)
            if str(self.buf).isdigit():
                print("good!")
                self.dict[tmp_var] = ('Const', self.buf)
            else:
                print("Error: expect number")
                return
            self.gl(f)
            if self.buf == ';':
                print("good!")
            else:
                print("Error: expect semicolon")
                return
            self.gl(f)
            if self.buf in self.TW:
                return

    def var(self, f):
        tmp_var = []
        self.gl(f)
        if self.buf == 'begin':
            return
        else:
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    print("good!")
                    tmp_var.append(self.buf)
                else:
                    print("Error: error name of variable")
                    return
            else:
                print("Error: expect name of variable")
                return
            self.gl(f)
            while self.buf == ',':
                self.gl(f)
                if self.buf in self.dict:
                    if self.dict[self.buf][0] == "ID":
                        tmp_var.append(self.buf)
                        print("good!")
                    else:
                        print("Error: expect name of variable")
                        return
                else:
                    print("Error: error name of variable")
                    return
                self.gl(f)
            if self.buf != ':':
                print("Error: expect \":\" ")
                return
            else:
                self.gl(f)
                if (self.buf == "integer" or self.buf == "bool"):
                    for i in tmp_var:
                        self.dict[i] = ("ID", False, self.buf)
                else:
                    print("Error: expect type of variables ")
                    return
                self.gl(f)
                if self.buf == ';':
                    return self.var(f)
                else:
                    print("Error: expect \";\" ")
                    return

    def begin(self, f):
        self.gl(f)
        self.operators(f)
        self.one_sym = ''
        while self.buf == ';':
            self.gl(f)
            self.operators(f)
            self.one_sym = ''
        if self.buf == 'end':
            print("good")
        else:
            print("unexpected:", self.buf)

    def operators(self, f):
        tmp = []
        if self.buf == "read":
            self.readPascal(f)
        elif self.buf == "write":
            self.writePascal(f)
        elif (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
            print("good!")
            self.poliz.append(("POLIZ_ADDRESS", self.buf))
            return self.assignPascal(f)
        else:
            print("Error")
            return

    def assignPascal(self, f):
        self.gl(f)
        if self.buf == ":=":
            self.gl(f)
            self.E(f)
        return

    def E(self, f):
        self.E1(f)
        if (self.buf == "=") or (self.buf == "<=") or (self.buf == ">=") or (self.buf == "<") or (self.buf == ">") or (self.buf == "!="):
            self.st_lex.append(self.buf)
            self.gl(f)
            self.E1(f)

    def E1(self, f):
        self.T(f)
        if (self.buf == "+") or (self.buf == "-") or (self.buf == "or"):
            self.st_lex.append(self.buf)
            self.gl(f)
            self.T(f)

    def T(self, f):
        self.F(f)
        if (self.buf == "*") or (self.buf == "/") or (self.buf == "and"):
            self.st_lex.append(self.buf)
            self.gl(f)
            self.F(f)

    def F(self, f):
        if (self.buf in self.dict) and (self.dict[self.buf][0] == "ID"):
            self.checkID()
            print("good!")
            self.poliz.append(("ID", self.buf))
            self.gl(f)
        elif (self.buf in self.dict) and (self.dict[self.buf][0] == "Const"):
            print("good!")
            self.poliz.append(("Const", self.buf))
            self.gl(f)
        elif str(self.buf).isdigit():
            self.st_lex.append("int")
            self.poliz.append(("Int", self.buf))
            self.gl(f)
        elif self.buf == "true":
            self.st_lex.append("bool")
            self.poliz.append(("Bool", 1))
            self.gl(f)
        elif self.buf == "false":
            self.st_lex.append("bool")
            self.poliz.append(("Bool", 0))
            self.gl(f)
        elif self.buf == "not":
            self.gl(f)
            self.F(f)
            self.checkNot()
        elif self.buf == "(":
            self.gl(f)
            self.E(f)
            if self.buf == ")":
                self.gl(f)
            else:
                print("expect \")\"")
                return
        else:
            print("error")
            return

    def checkNot(self):
        if self.st_lex == [] or self.st_lex[-1] != "bool":
            print("error, wrong type")
            return
        else:
            self.poliz.append(("not", 0))

    def checkID(self):
        if (self.buf in self.dict) and (self.dict[self.buf][0] == "ID") and (self.dict[self.buf][1] == "True") and (len(self.dict[self.buf]) > 2):
                print("good!")
                if self.dict[self.buf][2] == "integer":
                    self.st_lex.append("int")
                else:
                    self.st_lex.append("bool")
        else:
            print(self.buf + " not declared")




    def readPascal(self, f):
        tmp = []
        self.gl(f)
        if self.buf == '(':
            self.gl(f)
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    print("good!")
                    tmp.append(self.buf)
                else:
                    print("Error: error name of variable")
                    return
            else:
                print("Error: error name of variable")
                return
        self.gl(f)
        if self.buf == ')':
            self.gl(f)
            return
        else:
            print("expected: )")
            return

    def writePascal(self, f):
        tmp = []
        self.gl(f)
        if self.buf == '(':
            self.gl(f)
            if self.buf in self.dict:
                if self.dict[self.buf][0] == "ID":
                    print("good!")
                    tmp.append(self.buf)
                else:
                    print("Error: error name of variable")
                    return
            else:
                print("Error: error name of variable")
                return
        self.gl(f)
        if self.buf == ')':
            self.gl(f)
            return
        else:
            print("expected: )")
            return


with open('test2.txt') as f:
    p = Parser()
    p.program(f)
    p.gl(f)
    if p.buf == "const":
        p.const(f)
    else:
        pass
    if p.buf == "var":
        p.var(f)
    else:
        pass
    if p.buf == 'begin':
        p.begin(f)
    print(p.buf)
    print(p.dict)
