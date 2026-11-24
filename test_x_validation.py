import pandas as pd
import pytest
from calculations import validate_matching_x

def test_different_x_raises_error():
    training = pd.DataFrame({"x": [1, 2, 3]})
    ideal = pd.DataFrame({"x": [1, 2, 5]})

    with pytest.raises(ValueError):
        validate_matching_x(training, ideal)

def test_matching_x_no_error():
    training = pd.DataFrame({"x": [1, 2, 3]})
    ideal = pd.DataFrame({"x": [1, 2, 3]})

    validate_matching_x(training, ideal)