def score(y_true, y_pred):
	return sklearn.metrics.mean_squared_error(y_true, y_pred)
