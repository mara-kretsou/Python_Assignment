import pandas as pd
import pytest
from point_mapper import PointMapper

def test_missing_x_raises_error():
    ideal = pd.DataFrame({"x": [1 , 2], "y1": [10, 20]})
    test = pd.DataFrame({"x": [3], "y": [30]})

    mapper = PointMapper(ideal)

    with pytest.raises(ValueError, match="No ideal data found"):
        mapper.map_points(test, {"y1": 1.0})

def test_nearly_equal_x():
    ideal = pd.DataFrame({"x":[0.3], "y1": [10]})
    test = pd.DataFrame({"x": [0.1 + 0.2], "y": [10]})

    mapper = PointMapper(ideal)
    result = mapper.map_points(test, {"y1": 1.0})

    assert len(result) == 1
