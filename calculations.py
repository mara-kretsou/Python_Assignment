def calculate_sse(training_values, ideal_values):
    """Calculates the sum of squared errors."""
    difference = training_values - ideal_values
    squared_errors = difference ** 2
    return squared_errors.sum()

