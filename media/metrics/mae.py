def score(y_true, y_pred):
	return sklearn.metrics.mean_absolute_error(y_true, y_pred)
