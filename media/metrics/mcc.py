def score(y_true, y_pred):
	return sklearn.metrics.matthews_corrcoef(y_true, y_pred)
