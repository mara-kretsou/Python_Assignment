import pandas as pd
from point_mapper import PointMapper
import pytest

def test_maps_point_within_tolerance():
    """Check that a point within the tolerance is mapped."""
    ideal_data = pd.DataFrame({"x": [1, 2], "y1": [10, 20]})
    test_data = pd.DataFrame({"x": [1], "y": [10.2]})
    allowed_differences = {"y1": 0.5}
    mapper = PointMapper(ideal_data)
    result = mapper.map_points(test_data, allowed_differences)
    assert len(result) ==  1

def test_does_not_map_point_outside_tolerance():
    """Check that a point outside tolerance is not mapped."""
    ideal_data = pd.DataFrame({"x": [1, 2], "y1": [10, 20]})
    test_data = pd.DataFrame({"x": [1], "y": [11.0]})
    allowed_differences = {"y1": 0.5}
    mapper = PointMapper(ideal_data)
    result = mapper.map_points(test_data, allowed_differences)
    assert result.empty

def test_raises_error_when_x_is_missing():
    """Check that a missing x-value raises an error."""
    ideal_data = pd.DataFrame({"x": [1, 2], "y1": [10, 20]})
    test_data = pd.DataFrame({"x": [3], "y": [30]})
    allowed_differences = {"y1": 0.5}
    mapper = PointMapper(ideal_data)
    with pytest.raises(ValueError, match="No ideal data found"):
        mapper.map_points(test_data, allowed_differences)

def test_maps_point_at_exact_tolerance():
    """Check that a point exactly at the tolerance is mapped."""
    ideal_data = pd.DataFrame({"x": [1, 2], "y1": [10, 20]})
    test_data = pd.DataFrame({"x": [1], "y": [10.5]})
    allowed_differences = {"y1": 0.5}
    mapper = PointMapper(ideal_data)
    result = mapper.map_points(test_data, allowed_differences)
    assert len(result) ==  1
    assert result.iloc[0]["deviation"] == pytest.approx(0.5)
    
def test_keeps_identical_test_rows():
    """Check that identical test rows are both preserved."""

    ideal_data = pd.DataFrame({"x": [1], "y1": [10.0]})
    test_data = pd.DataFrame({"x": [1, 1], "y": [10.2, 10.2]})
    mapper = PointMapper(ideal_data)
    result = mapper.map_points(test_data, {"y1": 0.5})
    assert len(result) == 2

def test_unmatched_duplicate_coordinates():
    """Check that unmatched duplicate coordinates are preserved."""
    test_data = pd.DataFrame({"x": [2.0, 2.0, 3.0], "y": [10.0, 10.0, 30.0]})

    matches = pd.DataFrame({"test_row_id": [0]})

    mapper = PointMapper(pd.DataFrame({"x": [2.0], "y1": [10.0]}))

    result = mapper.find_unmatched_points(test_data, matches)

    assert result.index.tolist() == [1, 2]
    assert result.iloc[0]["x"] == 2.0
    assert result.iloc[0]["y"] == 10.0

def test_nearly_equal_x():
    """Check that nearly equal floating point X values match."""
    ideal = pd.DataFrame({"x":[0.3], "y1": [10]})
    test = pd.DataFrame({"x": [0.1 + 0.2], "y": [10]})

    mapper = PointMapper(ideal)
    result = mapper.map_points(test, {"y1": 1.0})

    assert len(result) == 1