import math
import os

from Lexer import *
from Parser import *
from SymbolTable import *
from Context import *

global_symbol_table = SymbolTable()

#Built-in Inputs
def initialize_built_ins():
    from Interpreter import Float, Boolean, BuiltInFunction
    global_symbol_table.set("Null", None)
    global_symbol_table.set("False", Boolean(False))
    global_symbol_table.set("True", Boolean(True))
    global_symbol_table.set("math_pi", Float(math.pi))
    global_symbol_table.set("math_e", Float(math.e))
    global_symbol_table.set("print", BuiltInFunction("print"))
    global_symbol_table.set("print_ret", BuiltInFunction("print_ret"))
    global_symbol_table.set("input", BuiltInFunction("input"))
    global_symbol_table.set("int_input", BuiltInFunction("input_int"))
    global_symbol_table.set("sqrt", BuiltInFunction("sqrt"))
    global_symbol_table.set("run", BuiltInFunction("run"))
    global_symbol_table.set("sort", BuiltInFunction("sort"))
    global_symbol_table.set("len", BuiltInFunction("len"))
    global_symbol_table.set("type", BuiltInFunction("type"))
    global_symbol_table.set("append", BuiltInFunction("append"))
    global_symbol_table.set("get", BuiltInFunction("get"))
    global_symbol_table.set("remove", BuiltInFunction("remove"))
    global_symbol_table.set("concat", BuiltInFunction("concat"))
    global_symbol_table.set("reverse", BuiltInFunction("reverse"))
    global_symbol_table.set("to_int", BuiltInFunction("to_int"))
    global_symbol_table.set("to_float", BuiltInFunction("to_float"))
    global_symbol_table.set("to_str", BuiltInFunction("to_str"))
    global_symbol_table.set("clear", BuiltInFunction("clear"))

#RUN
def run(filename, text):
    from Interpreter import Interpreter
    initialize_built_ins()
    # Generate tokens
    lexer = Lexer(filename, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

#MAIN

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Welcome to the Nitix™ Interpreter')
    while True:
        text = input('Nitix™: ')
        if text.strip() == "": continue
        result, error = run('<shell>', text)

        if error: print("Error: ", error)
        elif result and result.elements[0]:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(result)

