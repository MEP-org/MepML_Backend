def score(y_true, y_pred):
	return sklearn.metrics.r2_score(y_true, y_pred)
