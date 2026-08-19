"""
Calculator tool — safe arithmetic expression evaluator.
Uses ast module to parse and evaluate only safe mathematical expressions.
"""

import ast
import operator
import math


# Allowed operators and functions
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

SAFE_FUNCTIONS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
}


def _eval_node(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value)}")

    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported operator: {op_type.__name__}")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if op_type == ast.Div and right == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        if op_type == ast.FloorDiv and right == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return SAFE_OPERATORS[op_type](left, right)

    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in SAFE_OPERATORS:
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
        operand = _eval_node(node.operand)
        return SAFE_OPERATORS[op_type](operand)

    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Unsupported function call.")
        func_name = node.func.id
        if func_name not in SAFE_FUNCTIONS:
            raise ValueError(f"Unsupported function: '{func_name}'")
        args = [_eval_node(a) for a in node.args]
        return SAFE_FUNCTIONS[func_name](*args)

    else:
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")


def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression and return the result as a string.

    Args:
        expression: A string containing a mathematical expression
                    (e.g., "25 * 18", "(100 + 50) / 5", "2 ** 10").

    Returns:
        The result as a formatted string, or an error message.
    """
    expression = expression.strip()

    # Replace common natural-language patterns
    expression = expression.replace("×", "*").replace("÷", "/").replace("^", "**")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        return f"Invalid mathematical expression: '{expression}'"

    try:
        result = _eval_node(tree.body)
    except ZeroDivisionError as e:
        return str(e)
    except ValueError as e:
        return f"Calculation error: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

    # Format the result cleanly
    if isinstance(result, float) and result.is_integer():
        result = int(result)

    return str(result)
