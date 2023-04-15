def f1_score(true_labels, pred_labels):
    """
    Computes F1 score given true labels and predicted labels.
    
    Args:
    true_labels: A list of true labels.
    pred_labels: A list of predicted labels.
    
    Returns:
    A floating point number representing the F1 score.
    """

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
    
    return f1
