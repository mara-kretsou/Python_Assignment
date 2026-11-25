"""Calculate function deviations and select the best ideal functions."""


def calculate_sse(training_values, ideal_values):
    """Calculates the sum of squared errors."""
    difference = training_values - ideal_values
    squared_errors = difference**2
    return squared_errors.sum()


def calculate_allowed_deviation(training_values, ideal_values):
    """Calculates the maximum allowed deviation between training and ideal values."""
    max_difference = (training_values - ideal_values).abs().max()
    allowed_deviation = max_difference * (2**0.5)
    return allowed_deviation


def find_best_ideal(training_values, ideal_data):
    """Finds the ideal function with the lowest SSE."""
    sse_results = {}
    for ideal_name in ideal_data.columns[1:]:
        sse = calculate_sse(training_values, ideal_data[ideal_name])
        sse_results[ideal_name] = sse

    best_ideal = min(sse_results, key=sse_results.get)
    return best_ideal


def is_mapping_allowed(deviation, allowed_difference):
    """Checks if a test point's deviation is within the allowed limit."""
    return deviation <= allowed_difference


def select_closest_matches(matches_table):
    """Selects the closest ideal function for each test point."""
    sorted_matches = matches_table.sort_values("deviation")
    unique_columns = (
        ["test_row_id"] if "test_row_id" in matches_table.columns else ["x", "y"]
    )
    final_matches = sorted_matches.drop_duplicates(subset=unique_columns, keep="first")
    return final_matches


def validate_matching_x(training_data, ideal_data):
    """Check that training and ideal X values match."""
    if not training_data["x"].equals(ideal_data["x"]):
        raise ValueError("Training and ideal X values do not match.")
