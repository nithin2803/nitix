from sly import Lexer
from sly import Parser
import re

class NitixLexer(Lexer):
    tokens =  { RBRACE, POWER, LBRACE, LBRACKET, RBRACKET, FUNC, INPUT, VAR, PRINT, BOOL, NUMBER, STRING, IF, ELIF, ELSE, FOR, WHILE, TO, COLON, EQEQ, AND, OR, GEQ, GT, LEQ, LT, NEQ }
    ignore = ' \t'

    ignore_newline = r'\n+'

    literals = { '%', '=', '+', '-', '!', '*', '/', '(', ')', ';', ',' }

    IF = r'if'
    ELSE = r'else'
    ELIF = r'elif'
    FOR = r'for'
    TO = r'to'
    PRINT = r'print'
    WHILE = r'while'
    FUNC = r'func'
    INPUT = r'input'
    COLON = r':'
    BOOL = r'True|False'
    STRING = r'\'.*?\''
    VAR = r'[a-zA-z_][a-zA-Z0-9_]*'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    POWER = r'\*\*'
    AND = r'&'
    OR = r'\|'
    EQEQ = r'=='
    GEQ = r'>='
    LEQ = r'<='
    NEQ = r'!='
    GT = r'>'
    LT  = r'<'


    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    def BOOL(self, t):
        t.value = (t.value == 'True')
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    def error(self, t):
        print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        self.index += 1

class NitixParser(Parser):
    tokens = NitixLexer.tokens
    
    precedence = (
        ('nonassoc', GT, GEQ, LT, LEQ, NEQ, EQEQ),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS'),
        ('left', POWER),
        )

    def init(self):
        self.env = { }

    #statementblock
    @_('statement { statement }')
    def statementblock(self, p):
        return [ p.statement0 ] + p.statement1

    #statement
    @_('FOR var_assign TO expr LBRACE statementblock RBRACE')
    def statement(self, p):
        return ['for_loop', ['for_loop_setup', p.var_assign, p.expr], p.statementblock]

    @_('WHILE condition LBRACE statementblock  RBRACE')
    def statement(self, p):
        return ['while_loop', p.condition, p.statementblock]
    
    @_('IF condition LBRACE statementblock RBRACE { ELIF condition LBRACE statementblock RBRACE } [ ELSE LBRACE statementblock RBRACE ]')
    def statement(self, p):
        return ['if_else', ['branch', p.condition0, p.statementblock0, p.statementblock2], p.condition1, p.statementblock1] 

    @_('FUNC VAR "(" ")" COLON LBRACE statementblock RBRACE')
    def statement(self, p):
        return ['func_def', p.VAR, p.statementblock]

    @_('VAR "(" ")" ";"')
    def statement(self, p):
        return ['func_call', p.VAR]

    @_('VAR "=" INPUT "(" STRING ")" ";"')
    def statement(self, p):
        return ['input_var_assign', p.VAR, p.STRING]

    @_('PRINT "(" exprlist ")" ";"')
    def statement(self, p):
        return ['print', p.exprlist]

    @_('var_assign ";"')
    def statement(self, p):
        return p.var_assign

    @_('expr ";"')
    def statement(self, p):
        return p.expr

    @_('condition ";"')
    def statement(self, p):
        return p.condition

    @_('list ";"')
    def statement(self, p):
        return p.list    

    #var_assign
    @_('VAR "=" expr')
    def var_assign(self, p):
        return ['var_assign', p.VAR, p.expr]

    @_('VAR "=" condition')
    def var_assign(self, p):
        return ['var_assign', p.VAR, p.condition]

    @_('VAR "=" list')
    def var_assign(self, p):
        return ['var_assign', p.VAR, p.condition]

    #list
    @_('LBRACKET exprlist RBRACKET')
    def list(self, p):
        return [ p.exprlist ]

    #exprlist
    @_('expr { "," expr }')
    def exprlist(self, p):
        return [ p.expr0 ] + p.expr1

    @_('condition { "," condition }')
    def exprlist(self, p):
        return [ p.condition0 ] + p.condition1

    @_('expr { "," condition }')
    def exprlist(self, p):
        return [ p.expr ] + p.condition

    @_('condition { "," expr }')
    def exprlist(self, p):
        return [ p.condition ] + p.expr

    #condition   
    @_('expr EQEQ expr')
    def condition(self, p):
        return ['condition_eqeq', p.expr0, p.expr1]

    @_('expr LT expr')
    def condition(self, p):
        return ['condition_lt', p.expr0, p.expr1]

    @_('expr LEQ expr')
    def condition(self, p):
        return ('condition_leq', p.expr0, p.expr1)

    @_('expr GT expr')
    def condition(self, p):
        return ['condition_gt', p.expr0, p.expr1]

    @_('expr GEQ expr')
    def condition(self, p):
        return ['condition_geq', p.expr0, p.expr1]

    @_('expr NEQ expr')
    def condition(self, p):
        return ['condition_neq', p.expr0, p.expr1]

    @_('expr OR expr')
    def condition(self, p):
        return ['condition_or', p.expr0, p.expr1]

    @_('expr AND expr')
    def condition(self, p):
        return ['condition_and', p.expr0, p.expr1]

    @_('BOOL')
    def condition(self, p):
        return ['bool', p.BOOL]

    #expr
    @_('expr POWER expr')
    def expr(self, p):
        return ['pow', p.expr0, p.expr1]
    
    @_('expr "%" expr')
    def expr(self, p):
        return ['mod', p.expr0, p.expr1]
    
    @_('expr "+" expr')
    def expr(self, p):
        return ['add', p.expr0, p.expr1]

    @_('expr "-" expr')
    def expr(self, p):
        return ['sub', p.expr0, p.expr1]

    @_('expr "*" expr')
    def expr(self, p):
        return ['mul', p.expr0, p.expr1]

    @_('expr "/" expr')
    def expr(self, p):
        return ['div', p.expr0, p.expr1]

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return ['neg', p.expr]

    @_('VAR')
    def expr(self, p):
        return ['var', p.VAR]

    @_('NUMBER')
    def expr(self, p):
        return ['num', p.NUMBER]

    @_('STRING')
    def expr(self, p):
        return ['str', p.STRING]

    def error(self, p):
        if p:
            print("SyntaxError at %s token" %p.type, "in line %s at position %s" %(p.lineno, p.index))
        else:
            print("SyntaxError at EOF")
        return
    

class NitixInterpreter:

    def __init__(self, tree, env): 
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int) and not runningFile:
            print(result)
        if isinstance(result, str) and result[0] == '\'' and not runningFile:
            print(result)

    def walkTree(self, node):
        print(node)
        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node
        if isinstance(node, bool):
            return node
        if isinstance(node[0], list):
            for childnode in node:
                result = self.walkTree(childnode)
            return result

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'input_var_assign':
            self.env[node[1]] = input(self.walkTree(node[2]).replace('\'', ''))
            return node[1]

        if node[0] == 'num':
            return node[1]

        if node[0] == 'bool':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'print':
            string = ''
            for i in range(len(node[1])):
                string += str(self.walkTree(node[1][i])).replace('\'', '') + ' '
            print(string)

        if node[0] == 'if_else':
            if self.walkTree(node[1][1]):
                return self.walkTree(node[1][2])
            for elem in node[2]:
                if self.walkTree(elem):
                    return self.walkTree(node[3][node[2].index(elem)])
            if self.walkTree(node[1][3]):
                return self.walkTree(node[1][3])

        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])
        elif node[0] == 'condition_lt':
            return self.walkTree(node[1]) < self.walkTree(node[2])
        elif node[0] == 'condition_leq':
            return self.walkTree(node[1]) <= self.walkTree(node[2])
        elif node[0] == 'condition_gt':
            return self.walkTree(node[1]) > self.walkTree(node[2])
        elif node[0] == 'condition_geq':
            return self.walkTree(node[1]) >= self.walkTree(node[2])
        elif node[0] == 'condition_neq':
            return self.walkTree(node[1]) != self.walkTree(node[2])
        elif node[0] == 'condition_or':
            return self.walkTree(node[1]) or self.walkTree(node[2])
        elif node[0] == 'condition_and':
            return self.walkTree(node[1]) and self.walkTree(node[2])
        

        if node[0] == 'func_def':
            self.env[node[1]] = node[2]

        if node[0] == 'func_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("LookupError: function '%s'() is undefined" % (node[1]))

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])
        elif node[0] == 'neg':
            return -self.walkTree(node[1])
        elif node[0] == 'mod':
            return self.walkTree(node[1]) % self.walkTree(node[2])
        elif node[0] == 'pow':
            print(node)
            return self.walkTree(node[1]) ** self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("LookupError: var '%s' is undefined" % node[1])

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count + 1, loop_limit + 1 ):
                    result = self.walkTree(node[2])
                    if result is not None and not runningFile:
                        print(result)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))

        if node[0] == 'while_loop':
            loop_condition = self.walkTree(node[1])

            while (loop_condition):
                statement = self.walkTree(node[2])
                if statement is not None and not runningFile:
                    print(statement)
                loop_condition = self.walkTree(node[1])
    
if __name__ == '__main__':
    lexer = NitixLexer()
    parser = NitixParser()
    env = {}
    runningFile = False
    recursiveIndex = 0
    while True:
        if not runningFile:
            try:
                text = input('Nitix™: ')
            except EOFError:
                break
            if text:
                lexed = lexer.tokenize(text)
                run_file_regex = r'^run [a-zA-Z0-9_]+\.[a-z]+'
                if(re.search(run_file_regex, text)):
                    runningFile = True
                else:
                    tree = parser.parse(lexed)
                    NitixInterpreter(tree, env)
        else:
            file_name = text.replace('run ', '')
            file = open(file_name, 'r')
            lexed = lexer.tokenize(file.read())
            tree = parser.parse(lexed)
            NitixInterpreter(tree, env)
            runningFile = False
            file.close()
#tree = parser.parse(lexed)
#NitixInterpreter(tree, env)
#for tok in lexed:
#print(tok)


