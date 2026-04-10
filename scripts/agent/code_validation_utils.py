import ast
import re


def validate_python_syntax(code):
    """Check if code has valid Python syntax."""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error: {str(e)}"


def check_main_guard_pattern(code, pattern=None):
    """Check if code contains main guard pattern."""
    if pattern is None:
        pattern = r'if __name__ == ["\']__main__["\']:'

    if re.search(pattern, code):
        return True, ""
    return False, "Missing if __name__ == '__main__': guard"


def compare_code_lengths(original_code, new_code, max_change_ratio=0.5):
    """Compare code lengths and check if change is within acceptable range."""
    original_lines = count_non_empty_lines(original_code)
    new_lines = count_non_empty_lines(new_code)

    change_ratio = (
        abs(original_lines - new_lines) / original_lines if original_lines > 0 else 0
    )

    if change_ratio > max_change_ratio:
        return (
            False,
            f"Code length changed too much: {original_lines} -> {new_lines} ({change_ratio:.1%})",
        )
    return True, ""


def count_non_empty_lines(code):
    """Count non-empty lines in code."""
    return len([line for line in code.split("\n") if line.strip()])


def extract_functions_from_code(code):
    """Extract function names from Python code."""
    function_pattern = r"def\s+(\w+)\s*\([^)]*\):"
    return re.findall(function_pattern, code)


def get_function_code_block(code, func_name, all_functions):
    """Extract code block for a specific function."""
    func_start = code.find(f"def {func_name}")
    if func_start == -1:
        return ""

    next_func_start = None
    for other_func in all_functions:
        if other_func != func_name:
            other_start = code.find(f"def {other_func}", func_start + 1)
            if other_start != -1 and (
                next_func_start is None or other_start < next_func_start
            ):
                next_func_start = other_start

    if next_func_start is None:
        return code[func_start:]
    else:
        return code[func_start:next_func_start]


def validate_function_sizes(code, max_lines=30):
    """Check if all functions are under specified line limit."""
    functions = extract_functions_from_code(code)

    for func_name in functions:
        func_code = get_function_code_block(code, func_name, functions)
        func_lines = count_non_empty_lines(func_code)

        if func_lines > max_lines:
            return False, f"Function {func_name} has {func_lines} lines (>{max_lines})"

    return True, ""


def validate_code_quality(original_code, refactored_code, options=None):
    """Comprehensive code quality validation with configurable options."""
    if options is None:
        options = {
            "check_syntax": True,
            "check_main_guard": True,
            "check_length_similarity": True,
            "check_function_sizes": True,
            "max_change_ratio": 0.5,
            "max_function_lines": 30,
        }

    validations = []

    if options.get("check_syntax", True):
        validations.append(validate_python_syntax(refactored_code))

    if options.get("check_main_guard", True):
        validations.append(check_main_guard_pattern(refactored_code))

    if options.get("check_length_similarity", True):
        max_ratio = options.get("max_change_ratio", 0.5)
        validations.append(
            compare_code_lengths(original_code, refactored_code, max_ratio)
        )

    if options.get("check_function_sizes", True):
        max_lines = options.get("max_function_lines", 30)
        validations.append(validate_function_sizes(refactored_code, max_lines))

    for is_valid, msg in validations:
        if not is_valid:
            return False, msg

    return True, "All validations passed"
