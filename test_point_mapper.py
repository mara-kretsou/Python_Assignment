import pandas as pd
from point_mapper import PointMapper
import pytest

def test_mapps_point_within_tollerance():
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
    
