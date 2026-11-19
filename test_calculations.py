import pandas as pd
from calculations import calculate_sse,calculate_allowed_deviation,find_best_ideal



def test_calculate_sse():
    """Tests the calculation of the sum of squared errors."""
    training_values = pd.Series([3, 5, 7])
    ideal_values = pd.Series([2, 5, 6])

    result = calculate_sse(training_values, ideal_values)

    assert result == 2


def test_calculate_allowed_deviation():
    training_values = pd.Series([1, 4, 7])
    ideal_values = pd.Series([2, 4, 5])

    result = calculate_allowed_deviation(training_values,ideal_values)

    expected = 2 * (2**0.5)
    assert abs(result - expected) < 0.000001


def test_find_best_ideal():
   training_values = pd.Series([1, 2, 3])
   ideal_data = pd.DataFrame({"x":[0, 1, 2], "y1":[1, 2, 3], "y2":[4, 5, 6]}) 
   result = find_best_ideal(training_values,ideal_data)
   assert result == "y1"
   
