def score(y_true, y_pred):
	if len(set(y_true.flatten())) > 2:
		return sklearn.metrics.f1_score(y_true, y_pred, average="weighted", zero_division=0)
	else:
		return sklearn.metrics.f1_score(y_true, y_pred)