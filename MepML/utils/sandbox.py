import ast
import numpy as np
import sklearn.metrics

class ImportRemover(ast.NodeTransformer):
    def visit_Import(self, node):
        return None

    def visit_ImportFrom(self, node):
        return None


class OpenRemover(ast.NodeTransformer):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "open":
            return None
        return node

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == "open":
            return None
        return node


class Sandbox:
    def run(source, y_true, y_pred):
        tree = ast.parse(source)
        tree = ImportRemover().visit(tree)
        tree = OpenRemover().visit(tree)
        src = ast.unparse(tree)
        my_vars = {"y_true": y_true, "y_pred": y_pred, "sklearn": sklearn, "np": np}
        code = compile(src, '<string>', 'exec')
        exec(code, my_vars)
        return my_vars["x"]
