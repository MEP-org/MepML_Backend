from MepML.utils.sandbox import Sandbox

src = """
file = open("test.txt", "r")
def score(true_labels, pred_labels):
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    total = len(true_labels)
    
    for i in range(total):
        if true_labels[i] == 1 and pred_labels[i] == 1:
            true_positives += 1

        elif true_labels[i] == 0 and pred_labels[i] == 1:
            false_positives += 1

        elif true_labels[i] == 1 and pred_labels[i] == 0:
            false_negatives += 1
    
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    f1 = 2 * precision * recall / (precision + recall)
    
    return true_positives

x = score(y_true, y_pred)
"""


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


# run_with_sandbox(src, [1, 0, 1], [1, 1, 1])

print(Sandbox.run(src, [1, 0, 1], [1, 1, 1]))
