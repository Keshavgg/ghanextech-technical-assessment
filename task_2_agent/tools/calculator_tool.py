"""
Tool: Safe Mathematical Expression Evaluator / Calculator
Author: Keshav Jindal
"""

import ast
import operator
import math
from typing import Dict, Any

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "ceil": math.ceil,
    "floor": math.floor,
    "abs": abs,
    "round": round,
}

ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}

def _eval_node(node):
    if isinstance(node, ast.Constant): # number or constant
        return node.value
    elif isinstance(node, ast.Name):
        if node.id in ALLOWED_CONSTANTS:
            return ALLOWED_CONSTANTS[node.id]
        raise ValueError(f"Unknown constant or variable: '{node.id}'")
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError(f"Operator {op_type.__name__} is not supported.")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unary operator {op_type.__name__} is not supported.")
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct mathematical function calls are supported.")
        func_name = node.func.id
        if func_name in ALLOWED_FUNCTIONS:
            args = [_eval_node(arg) for arg in node.args]
            return ALLOWED_FUNCTIONS[func_name](*args)
        raise ValueError(f"Function '{func_name}' is not in allowed safe math functions.")
    else:
        raise ValueError(f"Expression contains unsupported construct: {type(node).__name__}")

def calculate_expression(expression: str) -> Dict[str, Any]:
    """
    Safely parses and evaluates a mathematical expression using Python AST.
    Guarantees zero arbitrary code execution or injection risks.
    
    Parameters:
        expression (str): A mathematical expression (e.g. "(45 * 12) + sqrt(144)", "2 ** 10", "sin(pi / 2)").
        
    Returns:
        dict: Evaluated numerical result or descriptive error message.
    """
    if not expression or not expression.strip():
        return {"error": "Expression parameter cannot be empty."}

    expr_clean = expression.strip()
    try:
        parsed = ast.parse(expr_clean, mode="eval")
        result = _eval_node(parsed.body)
        
        # Round floating points cleanly if applicable
        if isinstance(result, float) and abs(result - round(result)) < 1e-9:
            result = int(round(result))
        elif isinstance(result, float):
            result = round(result, 6)

        return {
            "success": True,
            "expression": expr_clean,
            "result": result
        }
    except ZeroDivisionError:
        return {"error": "Math error: Division by zero."}
    except Exception as e:
        return {"error": f"Invalid mathematical expression: {str(e)}"}
