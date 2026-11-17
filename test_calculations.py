import pandas as pd
from calculations import calculate_sse



def test_calculate_sse():
    """Tests the calculation of the sum of squared errors."""
    training_values = pd.Series([3, 5, 7])
    ideal_values = pd.Series([2, 5, 6])

    result = calculate_sse(training_values, ideal_values)

    assert result == 2