import sys
import ast
import astroid  # type: ignore[reportMissingImports]


def extract_file_operations(content):
    """Extract file operations into separate functions"""
    tree = astroid.parse(content)
    file_ops = []
    content_funcs = []

    for node in tree.body:
        if isinstance(node, astroid.FunctionDef):
            has_file_op = False
            for child in node.nodes_of_class((astroid.Call)):
                if isinstance(child.func, astroid.Attribute):
                    if child.func.attrname in ["open", "exists", "isabs", "abspath"]:
                        has_file_op = True
                        break

            if has_file_op:
                file_ops.append(node)
            else:
                content_funcs.append(node)

    return file_ops, content_funcs


def optimize_code(file_path):
    """Optimize code by separating file operations from content processing"""
    with open(file_path, "r") as f:
        content = f.read()

    file_ops, content_funcs = extract_file_operations(content)

    # Generate optimized code with separated concerns
    optimized = []
    for func in file_ops:
        optimized.append(ast.unparse(func))
    for func in content_funcs:
        optimized.append(ast.unparse(func))

    return "\n\n".join(optimized)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a Python file to optimize")
        sys.exit(1)

    file_path = sys.argv[1]
    optimized = optimize_code(file_path)
    print(optimized)
