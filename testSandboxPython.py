from MepML.utils.sandbox import Sandbox

src = """
file = open("sensitive_file.txt", "w")
import os
def score(y_true, y_pred):
    return sklearn.metrics.accuracy_score(y_true, y_pred)

x = score(y_true, y_pred)
"""

print(Sandbox.run(src, [1, 0, 1], [1, 1, 1]))


# def run_with_sandbox(source, y_true, y_pred):
#     my_builtins = dict(limited_builtins)
#     # len is not defined
#     my_builtins["len"] = len
#     # NameError: name '_getiter_' is not defined
#     my_builtins["_getiter_"] = iter
#     # NameError: name '_getitem_' is not defined
#     my_builtins["_getitem_"] = lambda x, y: x[y]
#     # NameError: name '_inplacevar_' is not defined
#     # my_builtins["_inplacevar_"] = custom_inplacevar
#     my_vars = {"y_true": y_true, "y_pred": y_pred, "__builtins__": my_builtins, "sklearn": sklearn}
#     code = compile_restricted(source, '<string>', 'exec')
#     exec(code, my_vars)