import os
from Error import RTError
from constants import *
from Context import *
from SymbolTable import *
from Main import run

class RTResult:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.value = None
        self.error = None
        self.func_return_value = None
        self.loop_should_continue = False
        self.loop_should_break = False

    def register(self, res):
        self.error = res.error
        self.func_return_value = res.func_return_value
        self.loop_should_continue = res.loop_should_continue
        self.loop_should_break = res.loop_should_break
        return res.value

    def success(self, value):
        self.reset()
        self.value = value
        return self

    def success_return(self, value):
        self.reset()
        self.func_return_value = value
        return self

    def success_continue(self):
        self.reset()
        self.loop_should_continue = True
        return self

    def success_break(self):
        self.reset()
        self.loop_should_break = True
        return self

    def failure(self, error):
        self.reset()
        self.error = error
        return self

    def should_return(self):
        return(
            self.error or
            self.func_return_value or
            self.loop_should_continue or
            self.loop_should_break
            )

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def modded_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation(other)

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(self.pos_start, other.pos_end, 'Illegal operation',
                       self.context)

class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end,
                                     'Division by zero', self.context)

            return Number(self.value / other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value**other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def modded_by(self, other):
        if isinstance(other, Number):
            return Number(self.value%other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Boolean(self.value == other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Boolean(self.value != other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Boolean(self.value < other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(self.value > other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Boolean(self.value <= other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Boolean(self.value >= other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class Integer(Number):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def copy(self):
        copy = Integer(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class Float(Number):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    def copy(self):
        copy = Float(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

class Boolean(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def copy(self):
        copy = Boolean(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def and_op(self, other):
        if isinstance(other, Boolean):
            return Boolean(self.value
                           and other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def or_op(self, other):
        if isinstance(other, Boolean):
            return Boolean(self.value or other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def notted(self):
        return Boolean(not self.value).set_context(self.context), None

    def is_true(self):
        return self.value

    def __repr__(self):
        return str(self.value)

Boolean.false = Boolean(False)
Boolean.true = Boolean(True)

class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def added_to(self, other):
        if isinstance(other, String) or isinstance(other, Number) or isinstance(other, List):
            return String(self.value + str(other)).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def subbed_by(self, other):
        if isinstance(other, Integer):
            try:
                string = self.value[0 : other.value : ] + self.value[other.value + 1 : :]
                return String(string), None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Character at this index could not be removed from the string because index is out of bounds',
                    self.context)
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, Integer):
            return String(self.value * other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Integer):
            try:
                return String(self.value[other.value]), None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Character at this index could not be retrieved from the string because index is out of bounds',
                    self.context)
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_eq(self, other):
        if isinstance(other, String):
            return Boolean(self.value == other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, String):
            return Boolean(self.value != other.value).set_context(
                self.context), None
        else:
            return None, Value.illegal_operation(self, other)

    def is_true(self):
        return len(self.value) > 0

    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.value}"

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
        self.values = []
        self.get_values()
    
    def get_values(self):
        if len(self.elements) > 0:
            for elem in self.elements:
                self.values.append(elem.value)

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Integer):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be removed from list because index is out of bounds',
                    self.context)
        else:
            return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Integer):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Element at this index could not be retrieved from list because index is out of bounds',
                    self.context)
        else:
            return None, Value.illegal_operation(self, other)

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

class StatementList(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'

#Function
class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<anonymous>"

    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names, args):
        res = RTResult()
        optional_argument = False

        for elem in arg_names:
            if "?" in elem:
                optional_argument = True
                break

        if not optional_argument:
            if len(args) > len(arg_names):
                return res.failure(
                    RTError(
                        self.pos_start, self.pos_end,
                        f"{len(args) - len(arg_names)} too many args passed into {self}",
                        self.context))

            if len(args) < len(arg_names):
                return res.failure(
                    RTError(
                        self.pos_start, self.pos_end,
                        f"{len(arg_names) - len(args)} too few args passed into {self}",
                        self.context))

        return res.success(None)

    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return

    def execute(self, args):
        res = RTResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()

        res.register(
            self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.should_return() and res.func_return_value == None: return res

        ret_value = (value if self.should_auto_return else None) or res.func_return_value or None
        return res.success(ret_value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args):
        res = RTResult()
        exec_ctx = self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        res.register(
            self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.should_return(): return res

        return_value = res.register(method(exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"

    def execute_print(self, exec_ctx):
        print(repr(exec_ctx.symbol_table.get('value')))
        return RTResult().success(None)

    execute_print.arg_names = ['value']

    def execute_print_ret(self, exec_ctx):
        return RTResult().success(
            String(str(exec_ctx.symbol_table.get('value'))))

    execute_print_ret.arg_names = ['value']

    def execute_input(self, exec_ctx):
        prompt = str(exec_ctx.symbol_table.get('prompt?'))
        if prompt != 'None':
            text = input(prompt)
        else:
            text = input()
        return RTResult().success(String(text))

    execute_input.arg_names = ['prompt?']

    def execute_input_int(self, exec_ctx):
        prompt = str(exec_ctx.symbol_table.get('prompt?'))
        while True:
            if prompt != 'None':
                text = input(prompt)
            else:
                text = input()
            try:
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Try again!")
        return RTResult().success(Integer(number))

    execute_input_int.arg_names = ['prompt?']

    def execute_sqrt(self, exec_ctx):
        number = exec_ctx.symbol_table.get("value")

        if not isinstance(number, Number):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Argument must be number", exec_ctx))

        return RTResult().success(Number(math.sqrt(number.value)))

    execute_sqrt.arg_names = ['value']

    def execute_append(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        value = exec_ctx.symbol_table.get("value")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "First argument must be list", exec_ctx))

        list_.elements.append(value)
        return RTResult().success(list_)

    execute_append.arg_names = ["list", "value"]

    def execute_get(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(value, List) and not isinstance(value, String):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "First argument must be list or string", exec_ctx))

        if not isinstance(index, Integer):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Second argument must be an integer", exec_ctx))

        if isinstance(value, List):
            element = value.elements[int(index.value)]
            return RTResult().success(element)
        if isinstance(value, String):
            char = value.value[index.value]
            return RTResult().success(char)

    execute_get.arg_names = ["value", "index"]

    def execute_remove(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")
        index = exec_ctx.symbol_table.get("index")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "First argument must be list", exec_ctx))

        if not isinstance(index, Integer):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Second argument must be number", exec_ctx))

        try:
            element = list_.elements.pop(index.value)
        except:
            return RTResult().failure(
                RTError(
                    self.pos_start, self.pos_end,
                    'Element at this index could not be removed from list because index is out of bounds',
                    exec_ctx))
        return RTResult().success(element)

    execute_remove.arg_names = ["list", "index"]

    def execute_concat(self, exec_ctx):
        listA = exec_ctx.symbol_table.get("listA")
        listB = exec_ctx.symbol_table.get("listB")

        if not isinstance(listA, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "First argument must be list", exec_ctx))

        if not isinstance(listB, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Second argument must be list", exec_ctx))

        list_ = List(listA.elements.extend(listB.elements))
        return RTResult().success(list_)

    execute_concat.arg_names = ["listA", "listB"]

    def execute_sort(self, exec_ctx):
        list_ = exec_ctx.symbol_table.get("list")

        if not isinstance(list_, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Argument must be list", exec_ctx))

        sorted_list = sorted(list_.values)
        new_list = []
        for elem in sorted_list:
            new_list.append(Number(elem))
        return RTResult().success(List(new_list))

    execute_sort.arg_names = ["list"]

    def execute_run(self, exec_ctx):
        filename = exec_ctx.symbol_table.get("filename")

        if not isinstance(filename, String):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Argument must be string", exec_ctx))

        filename = filename.value

        try:
            with open(filename, "r") as file:
                script = file.read()
        except Exception as error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f'Failed to load script \'{filename}\'\n' + str(error),
                exec_ctx
            ))

        _, error = run(filename, script)

        if error:
            return RTResult().failure(RTError(
                self.pos_start, self.pos_end,
                f'Failed to finish executing script \'{filename}\'\n' + error,
                exec_ctx
            ))

        return RTResult().success(None) 

    execute_run.arg_names = ["filename"]

    def execute_len(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        
        if not isinstance(value, String) and not isinstance(value, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Argument must be string or a list", exec_ctx))

        if isinstance(value, String):
            return RTResult().success(Integer(len(value.value)))

        if isinstance(value, List):
            return RTResult().success(Integer(len(value.elements)))

    execute_len.arg_names = ["value"]

    def execute_reverse(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        
        if not isinstance(value, String) and not isinstance(value, List):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Argument must be string or a list", exec_ctx))

        if isinstance(value, String):
            return RTResult().success(String(value.value[::-1]))

        if isinstance(value, List):
            elements = value.elements
            elements.reverse()
            return RTResult().success(List(elements))

    execute_reverse.arg_names = ["value"]

    def execute_type(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        
        is_int = isinstance(exec_ctx.symbol_table.get("value"), Integer)
        if is_int:
            return RTResult().success(String('Integer'))

        is_float = isinstance(exec_ctx.symbol_table.get("value"), Float)
        if is_float:
            return RTResult().success(String('Float'))

        is_str = isinstance(exec_ctx.symbol_table.get("value"), String)
        if is_str:
            return RTResult().success(String('String'))
        
        is_list = isinstance(exec_ctx.symbol_table.get("value"), List)
        if is_list:
            return RTResult().success(String('List'))

        is_function = isinstance(exec_ctx.symbol_table.get("value"), BaseFunction)
        if is_function:
            return RTResult().success(String('Function'))

        is_bool = isinstance(exec_ctx.symbol_table.get("value"), Boolean)
        if is_bool:
            return RTResult().success(String('Boolean'))

    execute_type.arg_names = ["value"]

    def execute_to_int(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        if not isinstance(value, Number):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Argument must be an integer or a float", exec_ctx))
        
        return RTResult().success(Integer(int(value.value)))
    execute_to_int.arg_names = ["value"] 

    def execute_to_float(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        if not isinstance(value, Number):
            return RTResult().failure(
                RTError(self.pos_start, self.pos_end,
                        "Argument must be an integer or a float", exec_ctx))
        
        return RTResult().success(Float(float(value.value)))
    execute_to_float.arg_names = ["value"] 

    def execute_to_str(self, exec_ctx):
        value = exec_ctx.symbol_table.get("value")
        
        return RTResult().success(String(str(value)))
    execute_to_int.arg_names = ["value"] 

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'clear') 
        return RTResult().success(None)
    execute_clear.arg_names = []



# Interpreter
class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')


    def visit_IntegerNode(self, node, context):
        return RTResult().success(
            Integer(node.tok.value).set_context(context).set_pos(
                node.pos_start, node.pos_end))
    
    def visit_FloatNode(self, node, context):
        return RTResult().success(
            Float(node.tok.value).set_context(context).set_pos(
                node.pos_start, node.pos_end))

    def visit_StringNode(self, node, context):
        return RTResult().success(
            String(node.tok.value).set_context(context).set_pos(
                node.pos_start, node.pos_end))

    def visit_ListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            List(elements).set_context(context).set_pos(
                node.pos_start, node.pos_end))

    def visit_StatementListNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
            StatementList(elements).set_context(context).set_pos(
                node.pos_start, node.pos_end))

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(
                RTError(node.pos_start, node.pos_end,
                        f"'{var_name}' is not defined", context))

        value = value.copy().set_pos(node.pos_start,
                                     node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
        elif node.op_tok.type == TT_MOD:
            result, error = left.modded_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.and_op(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.or_op(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res

        error = None

        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(None if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(None if should_return_null else expr_value)

        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return(): return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return(): return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node,
                                                 context))
            if res.should_return(): return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
            None if node.should_return_null else
            StatementList(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return(): return res

            if not condition.is_true(): break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
          None if node.should_return_null else
          StatementList(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_FuncDefNode(self, node, context):
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node,
                              arg_names, node.should_auto_return).set_context(context).set_pos(
                                  node.pos_start, node.pos_end)

        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start,
                                                     node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context) if return_value else None
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = None

        return res.success_return(value)

    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()

    def visit_BreakNode(self, node, context):
        return RTResult().success_break()