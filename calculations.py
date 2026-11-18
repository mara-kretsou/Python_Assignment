def calculate_sse(training_values, ideal_values):
    """Calculates the sum of squared errors."""
    difference = training_values - ideal_values
    squared_errors = difference ** 2
    return squared_errors.sum()

def calculate_allowed_deviation(training_values,ideal_values):
     """Calculates the maximum allowed deviation between training and ideal values."""
     max_difference = (training_values - ideal_values).abs().max()
     allowed_deviation = max_difference * (2**0.5)
     return allowed_deviation
