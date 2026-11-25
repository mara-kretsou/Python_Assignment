"""Unit tests for function calculations and matching."""

import pytest
import pandas as pd
from calculations import (
    calculate_sse,
    calculate_allowed_deviation,
    find_best_ideal,
    is_mapping_allowed,
    select_closest_matches,
    validate_matching_x,
)


def test_calculate_sse():
    """Tests the calculation of the sum of squared errors."""
    training_values = pd.Series([3, 5, 7])
    ideal_values = pd.Series([2, 5, 6])

    result = calculate_sse(training_values, ideal_values)

    assert result == 2


def test_calculate_allowed_deviation():
    """Tests the calculation of the maximum allowed deviation."""
    training_values = pd.Series([1, 4, 7])
    ideal_values = pd.Series([2, 4, 5])

    result = calculate_allowed_deviation(training_values, ideal_values)

    expected = 2 * (2**0.5)
    assert abs(result - expected) < 0.000001


def test_find_best_ideal():
    """Tests the selection of the ideal function with the lowest SSE."""
    training_values = pd.Series([1, 2, 3])
    ideal_data = pd.DataFrame({"x": [0, 1, 2], "y1": [1, 2, 3], "y2": [4, 5, 6]})
    result = find_best_ideal(training_values, ideal_data)
    assert result == "y1"


def test_mapping_allowed():
    """Tests whether test point mapping is accepted or rejected correctly."""
    assert is_mapping_allowed(1, 2) == True
    assert is_mapping_allowed(3, 2) == False
    assert is_mapping_allowed(2, 2) == True


def test_select_closest_matches():
    """Tests that the mapping with the smallest deviation is selected."""
    matches_table = pd.DataFrame(
        {
            "x": [1, 1],
            "y": [5, 5],
            "ideal_function": ["y1", "y2"],
            "deviation": [0.3, 0.1],
        }
    )
    result = select_closest_matches(matches_table)
    assert result.iloc[0]["ideal_function"] == "y2"
    assert len(result) == 1


def test_different_x_raises_error():
    """Check that different X values raise a ValueError."""
    training = pd.DataFrame({"x": [1, 2, 3]})
    ideal = pd.DataFrame({"x": [1, 2, 5]})

    with pytest.raises(ValueError):
        validate_matching_x(training, ideal)


def test_matching_x_no_error():
    """Tests that matching X values pass validation."""
    training = pd.DataFrame({"x": [1, 2, 3]})
    ideal = pd.DataFrame({"x": [1, 2, 3]})

    validate_matching_x(training, ideal)
