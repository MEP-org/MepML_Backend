from RestrictedPython import compile_restricted
from RestrictedPython.Guards import safe_builtins
import sklearn.metrics

src = """
def score(yTrue, yPred):
    return sklearn.metrics.accuracy_score(yTrue, yPred)

x = score(y_true, y_pred)
"""


def run(source, y_true, y_pred):
    my_vars = {"y_true": y_true, "y_pred": y_pred, "sklearn": sklearn}
    code = compile(source, '<string>', 'exec')
    exec(code, my_vars)
    print(my_vars["x"])


def run_with_sandbox(source, y_true, y_pred):
    my_builtins = dict(safe_builtins)
    my_vars = {"y_true": y_true, "y_pred": y_pred, "__builtins__": my_builtins, "sklearn": sklearn}
    code = compile_restricted(source, '<string>', 'exec')
    exec(code, my_vars)


run(src, [1, 0, 1], [1, 1, 1])
run_with_sandbox(src, [1, 0, 1], [1, 1, 1])
