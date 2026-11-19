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

def find_best_ideal(training_values, ideal_data):
     """Finds the ideal function with the lowest SSE."""
     sse_results = {}
     for ideal_name in ideal_data.columns[1:]:
          sse = ((training_values - ideal_data[ideal_name]) **2).sum()
          sse_results[ideal_name] = sse 

     best_ideal = min(sse_results, key=sse_results.get)
     return best_ideal

