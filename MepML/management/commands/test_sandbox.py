from django.core.management.base import BaseCommand
from django.core.files.storage import default_storage
from MepML.utils.sandbox import Sandbox
import numpy as np


class Command(BaseCommand):
    def handle(self, *args, **options):
        src = default_storage.open("metrics/recall.py").read().decode("utf-8")
        print(Sandbox.run(src, np.array([[1], [2], [3]]), np.array([[1], [2], [4]])))


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