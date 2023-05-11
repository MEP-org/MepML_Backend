def score(y_true, y_pred):
	return sklearn.metrics.recall_score(y_true, y_pred)
